"""Log files kept in the repository (the Android app downloads them as a .zip).

logs/trades.csv            every signal: pair, timeframe, strategy, indicators at the signal, result
logs/market_snapshot.csv   every pair x timeframe: price, indicators, chosen strategy, why there was / wasn't a signal
logs/scans/YYYY-MM-DD.csv  one line per scan: time, duration, data problems, new signals, closed trades
logs/last_scan.txt         full printed output of the latest scan (errors show up here)
"""
import csv
import io
import os
import sys

import pandas as pd

import config

LOG_DIR = getattr(config, "LOG_DIR", "logs")

INDICATOR_COLS = ["candle_time", "close", "rsi14", "ema9", "ema21", "ema200", "trend", "macd", "macd_signal",
                  "macd_hist", "atr14", "atr_pips", "bb_upper", "bb_mid", "bb_lower"]

TRADE_COLS = (["id", "pair", "tf", "side", "strategy", "signal_candle_utc", "entry", "sl", "tp", "stop_pips",
               "target_pips", "status", "closed_at_utc", "exit", "pips", "result_r",
               "backtest_trades", "backtest_win_rate", "backtest_pf",
               "unseen_trades", "unseen_win_rate", "unseen_pf"]
              + ["ind_" + c for c in INDICATOR_COLS])

SNAPSHOT_COLS = (["scan_time_utc", "pair", "tf", "candles", "strategy", "backtest_trades", "backtest_win_rate",
                  "backtest_pf", "unseen_trades", "unseen_pf", "signal", "note"] + INDICATOR_COLS)

SCAN_COLS = ["scan_time_utc", "seconds", "checked", "no_data", "new_signals", "skipped_same_currency",
             "trades_closed", "open_trades", "errors"]

README = __doc__


class Capture:
    """Copies everything printed during a scan, so it can be saved to last_scan.txt."""

    def __init__(self):
        self.buf = io.StringIO()
        self._old = None

    def write(self, s):
        self.buf.write(s)
        if self._old:
            self._old.write(s)

    def flush(self):
        if self._old:
            self._old.flush()

    def __enter__(self):
        self._old = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, *exc):
        sys.stdout = self._old
        self._old = None
        return False

    def text(self):
        return self.buf.getvalue()


def _path(*parts):
    return os.path.join(LOG_DIR, *parts)


def _write_csv(path, cols, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})
    new = out.getvalue()
    try:
        with open(path) as f:
            if f.read() == new:
                return                      # unchanged: keep the file as it is
    except FileNotFoundError:
        pass
    with open(path, "w", newline="") as f:
        f.write(new)


def trade_rows(signals, pip_size):
    out = []
    for s in signals:
        st = s.get("stats") or {}
        ind = s.get("indicators") or {}
        p = pip_size(s["pair"])
        r = {
            "id": s.get("id"), "pair": s["pair"], "tf": s["tf"], "side": s["side"], "strategy": s.get("strategy"),
            "signal_candle_utc": s.get("bar_time"), "entry": s.get("entry"), "sl": s.get("sl"), "tp": s.get("tp"),
            "stop_pips": round(abs(s["entry"] - s["sl"]) / p, 1), "target_pips": round(abs(s["tp"] - s["entry"]) / p, 1),
            "status": s.get("status", "open"), "closed_at_utc": s.get("closed_at"), "exit": s.get("exit"),
            "pips": s.get("pips"), "result_r": s.get("result_r"),
            "backtest_trades": st.get("trades"), "backtest_win_rate": st.get("win_rate"),
            "backtest_pf": st.get("profit_factor"), "unseen_trades": st.get("test_trades"),
            "unseen_win_rate": st.get("test_win_rate"), "unseen_pf": st.get("test_profit_factor"),
        }
        for c in INDICATOR_COLS:
            r["ind_" + c] = ind.get(c)
        out.append(r)
    return out


def _snapshot_age_minutes():
    try:
        with open(_path("market_snapshot.csv")) as f:
            row = next(csv.DictReader(f))
        return (pd.Timestamp.now(tz="UTC") - pd.Timestamp(row["scan_time_utc"])).total_seconds() / 60
    except Exception:
        return 1e9


def write_all(signals, pip_size, snapshots, summary, printed, force=False):
    """Called once at the end of every scan."""
    os.makedirs(_path("scans"), exist_ok=True)
    if not os.path.exists(_path("README.txt")):
        with open(_path("README.txt"), "w") as f:
            f.write(README)

    _write_csv(_path("trades.csv"), TRADE_COLS, trade_rows(signals, pip_size))

    every = getattr(config, "SNAPSHOT_EVERY_MINUTES", 60)
    if force or _snapshot_age_minutes() >= every - 2:
        _write_csv(_path("market_snapshot.csv"), SNAPSHOT_COLS, snapshots)
        with open(_path("last_scan.txt"), "w") as f:
            f.write(printed)

    day = pd.Timestamp(summary["scan_time_utc"]).strftime("%Y-%m-%d")
    path = _path("scans", f"{day}.csv")
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCAN_COLS, extrasaction="ignore")
        if new_file:
            w.writeheader()
        w.writerow(summary)

    keep = getattr(config, "KEEP_SCAN_LOG_DAYS", 30)
    cutoff = (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=keep)).strftime("%Y-%m-%d")
    for name in os.listdir(_path("scans")):
        if name.endswith(".csv") and name[:10] < cutoff:
            os.remove(_path("scans", name))
