"""Log files kept in the repository (the Android app downloads them as a .zip).

logs/trades.csv            every signal: pair, timeframe, strategy, indicators at the signal, result
logs/market_snapshot.csv   every pair x timeframe: price, indicators, chosen strategy, why there was / wasn't a signal
logs/scans/YYYY-MM-DD.csv  one line per scan: time, duration, data problems, new signals, closed trades
logs/last_scan.txt         full printed output of the latest scan (errors show up here)
logs/performance.csv/.json closed trades grouped by timeframe, strategy, candle pattern, market direction,
                           RSI zone, volatility, weekday and news: which ones win and which lose
"""
import csv
import io
import json
import os
import sys

import pandas as pd

import config

LOG_DIR = getattr(config, "LOG_DIR", "logs")

FEATURE_COLS = ["pattern", "pattern_vs_trade", "trend", "bigger_trend", "direction_vs_trade", "rsi_zone",
                "volatility", "weekday", "session", "news_next_24h", "news_prev_24h", "news_titles"]

INDICATOR_COLS = ["candle_time", "close", "rsi14", "ema9", "ema21", "ema200", "trend", "macd", "macd_signal",
                  "macd_hist", "atr14", "atr_pips", "bb_upper", "bb_mid", "bb_lower"]

TRADE_COLS = (["id", "pair", "tf", "side", "strategy", "signal_candle_utc", "entry", "sl", "tp", "stop_pips",
               "target_pips", "status", "closed_at_utc", "exit", "pips", "result_r",
               "backtest_trades", "backtest_win_rate", "backtest_pf",
               "unseen_trades", "unseen_win_rate", "unseen_pf"]
              + ["ind_" + c for c in INDICATOR_COLS] + FEATURE_COLS)

SNAPSHOT_COLS = (["scan_time_utc", "pair", "tf", "candles", "strategy", "backtest_trades", "backtest_win_rate",
                  "backtest_pf", "unseen_trades", "unseen_pf", "signal", "note"] + INDICATOR_COLS)

SCAN_COLS = ["scan_time_utc", "seconds", "checked", "no_data", "new_signals", "skipped_same_currency",
             "skipped_max_open", "trades_closed", "open_trades", "errors"]

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
        f = s.get("features") or {}
        for c in FEATURE_COLS:
            r[c] = f.get(c)
        out.append(r)
    return out


# ---------------- what wins and what loses ----------------
def _pair_group(pair):
    if pair in ("XAUUSD", "XAGUSD"):
        return "gold / silver"
    return "major" if "USD" in pair else "cross"


def _news_bucket(f):
    n = f.get("news_next_24h")
    if not isinstance(n, int):
        return "not recorded"
    return "yes" if n > 0 else "no"


FACTORS = [
    ("Timeframe", lambda s, f: s["tf"]),
    ("Strategy", lambda s, f: s.get("strategy") or "?"),
    ("Buy or sell", lambda s, f: s["side"]),
    ("Pair type", lambda s, f: _pair_group(s["pair"])),
    ("Pair", lambda s, f: s["pair"]),
    ("Candle pattern", lambda s, f: f.get("pattern", "not recorded")),
    ("Candle vs trade", lambda s, f: f.get("pattern_vs_trade", "not recorded")),
    ("Market direction", lambda s, f: f.get("direction_vs_trade", "not recorded")),
    ("RSI zone", lambda s, f: f.get("rsi_zone", "not recorded")),
    ("Volatility", lambda s, f: f.get("volatility", "not recorded")),
    ("Weekday", lambda s, f: f.get("weekday", "not recorded")),
    ("Session", lambda s, f: f.get("session", "not recorded")),
    ("High-impact news in next 24h", lambda s, f: _news_bucket(f)),
]


def _result_r(s):
    if isinstance(s.get("result_r"), (int, float)):
        return float(s["result_r"])
    return 0.0


def performance(signals):
    """Closed trades grouped by each factor. Returns a JSON-able dict."""
    closed = [s for s in signals if s.get("status") in ("tp", "sl", "expired")]
    out = {"closed_trades": len(closed),
           "last_closed_utc": max((s.get("closed_at") or "" for s in closed), default=""),
           "total_r": round(sum(_result_r(s) for s in closed), 2), "factors": []}
    for name, fn in FACTORS:
        groups = {}
        for s in closed:
            v = str(fn(s, s.get("features") or {}))
            groups.setdefault(v, []).append(_result_r(s))
        rows = []
        for v, rs in groups.items():
            wins = sum(1 for r in rs if r > 0)
            rows.append({"value": v, "trades": len(rs), "wins": wins, "win_rate": round(100 * wins / len(rs), 1),
                         "total_r": round(sum(rs), 2), "avg_r": round(sum(rs) / len(rs), 3)})
        rows.sort(key=lambda r: (-r["avg_r"], -r["trades"]))
        out["factors"].append({"name": name, "rows": rows})
    return out


def write_performance(signals):
    perf = performance(signals)
    flat = [{"factor": f["name"], **r} for f in perf["factors"] for r in f["rows"]]
    _write_csv(_path("performance.csv"), ["factor", "value", "trades", "wins", "win_rate", "total_r", "avg_r"], flat)
    new = json.dumps(perf, indent=1)
    try:
        with open(_path("performance.json")) as f:
            if f.read() == new:
                return
    except FileNotFoundError:
        pass
    with open(_path("performance.json"), "w") as f:
        f.write(new)


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
    write_performance(signals)

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
