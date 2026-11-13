"""Forex signal bot: scans all pairs/timeframes and pushes new signals to your Android phone.

    python bot.py            # scan once (used by GitHub Actions every 5 min)
    python bot.py --loop     # keep running, scan every 5 min (PC or Termux on Android)
    python bot.py --test     # send a test notification
    python bot.py --dry      # scan and print signals, don't send
"""
import json
import os
import sys
import time

import pandas as pd
import requests

import config
import logbook
from backtest import backtest
from data import INTERVAL_LEN, get_candles
from strategies import STRATEGIES, atr, ema, macd, rsi


# ---------------- notifications ----------------
def notify(title, body, priority="high", tags="chart_with_upwards_trend"):
    sent = False
    if config.NTFY_TOPIC:
        try:
            requests.post(f"{config.NTFY_SERVER}/{config.NTFY_TOPIC}", data=body.encode(),
                          headers={"Title": title, "Priority": priority, "Tags": tags}, timeout=15)
            sent = True
        except Exception as e:
            print(f"[ntfy] {e}")
    if config.TELEGRAM_TOKEN and config.TELEGRAM_CHAT_ID:
        try:
            requests.post(f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage",
                          json={"chat_id": config.TELEGRAM_CHAT_ID, "text": f"{title}\n\n{body}"}, timeout=15)
            sent = True
        except Exception as e:
            print(f"[telegram] {e}")
    if not sent:
        print("[notify] No NTFY_TOPIC or Telegram set; printing only.")
    return sent


# ---------------- state (no duplicate alerts) ----------------
def load_state():
    try:
        with open(config.STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    cutoff = (pd.Timestamp.now(tz="UTC") - pd.Timedelta("10D")).isoformat()
    state = {k: v for k, v in state.items() if v >= cutoff}       # keep the file small
    with open(config.STATE_FILE, "w") as f:
        json.dump(state, f, indent=0)


# ---------------- signal logic ----------------
def decimals(pair):
    return 2 if pair.startswith("XA") else 3 if "JPY" in pair else 5


def pip_size(pair):
    if pair == "XAUUSD":
        return 0.1
    if pair == "XAGUSD":
        return 0.01
    return 0.01 if "JPY" in pair else 0.0001


def _r(v, n=6):
    try:
        return round(float(v), n)
    except Exception:
        return None


def indicators(df, pair):
    """Indicator values on the last closed candle (saved with each signal and in the logs)."""
    c = df["Close"]
    m_line, m_sig = macd(c)
    mid = c.rolling(20).mean()
    sd = c.rolling(20).std()
    a = atr(df).iloc[-1]
    e200 = ema(c, 200).iloc[-1]
    return {
        "candle_time": df.index[-1].isoformat(), "close": _r(c.iloc[-1]), "rsi14": _r(rsi(c).iloc[-1], 2),
        "ema9": _r(ema(c, 9).iloc[-1]), "ema21": _r(ema(c, 21).iloc[-1]), "ema200": _r(e200),
        "trend": "up" if c.iloc[-1] > e200 else "down",
        "macd": _r(m_line.iloc[-1], 7), "macd_signal": _r(m_sig.iloc[-1], 7),
        "macd_hist": _r(m_line.iloc[-1] - m_sig.iloc[-1], 7),
        "atr14": _r(a, 7), "atr_pips": _r(a / pip_size(pair), 1),
        "bb_upper": _r(mid.iloc[-1] + 2 * sd.iloc[-1]), "bb_mid": _r(mid.iloc[-1]),
        "bb_lower": _r(mid.iloc[-1] - 2 * sd.iloc[-1]),
    }


def trend_filtered(fn, mult=4):
    """Drops signals against the bigger trend (EMA 800 is about EMA 200 one timeframe up)."""
    def f(df):
        s = fn(df)
        t = ema(df["Close"], 200 * mult)
        c = df["Close"]
        s = s.where(~((s > 0) & (c <= t)), 0)
        return s.where(~((s < 0) & (c >= t)), 0)
    return f


def signal_fn(name):
    fn = STRATEGIES[name]
    return trend_filtered(fn) if getattr(config, "TREND_FILTER", False) else fn


def _ranked(df, names):
    rows = [{"strategy": n, **backtest(df, signal_fn(n))} for n in names]
    rows = [r for r in rows if r["trades"] >= config.MIN_TRADES_FOR_AUTO]
    return sorted(rows, key=lambda r: (r["profit_factor"], r["total_R"]), reverse=True)


def pick_strategy(df):
    """Returns (strategy name, stats, reason). name is None when nothing is good enough."""
    if config.STRATEGY != "auto":
        return config.STRATEGY, None, "fixed strategy"
    names = [n for n in getattr(config, "ALLOWED_STRATEGIES", list(STRATEGIES)) if n in STRATEGIES]
    if not names:
        return None, None, "no strategies allowed in config"
    if getattr(config, "PICK_ON_UNSEEN", False):
        split = int(len(df) * 0.7)
        ranked = _ranked(df.iloc[:split], names)                 # choose on the older 70%
        if not ranked or ranked[0]["profit_factor"] < config.MIN_PROFIT_FACTOR:
            return None, None, "no strategy made money on older data"
        best = ranked[0]
        test = backtest(df.iloc[max(0, split - 215):], signal_fn(best["strategy"]))   # judge on the newer 30%
        stats = {"trades": best["trades"], "win_rate": best["win_rate"], "profit_factor": best["profit_factor"],
                 "test_trades": test["trades"], "test_win_rate": round(test["win_rate"], 1),
                 "test_profit_factor": round(min(test["profit_factor"], 99.0), 2)}
        if test["trades"] < 3 or test["profit_factor"] < getattr(config, "UNSEEN_MIN_PROFIT_FACTOR", 1.0):
            return None, stats, f"{best['strategy']} failed on newer data (PF {stats['test_profit_factor']})"
        return best["strategy"], stats, "ok"
    ranked = _ranked(df, names)
    if not ranked or ranked[0]["profit_factor"] < config.MIN_PROFIT_FACTOR:
        return None, None, "no strategy good enough"
    return ranked[0]["strategy"], ranked[0], "ok"


def analyze(pair, tf, df, scan_time):
    """Returns (signal or None, snapshot row for the logs)."""
    snap = {"scan_time_utc": scan_time, "pair": pair, "tf": tf, "candles": 0 if df is None else len(df)}
    if df is None or df.empty:
        snap["note"] = "no price data"
        return None, snap
    if len(df) < 250:
        snap["note"] = "not enough candles"
        return None, snap
    ind = indicators(df, pair)
    snap.update(ind)
    name, stats, why = pick_strategy(df)
    if stats:
        snap.update({"backtest_trades": stats.get("trades"), "backtest_win_rate": _r(stats.get("win_rate"), 1),
                     "backtest_pf": _r(min(stats.get("profit_factor", 0), 99), 2),
                     "unseen_trades": stats.get("test_trades"), "unseen_pf": stats.get("test_profit_factor")})
    if not name:
        snap["note"] = why
        return None, snap
    snap["strategy"] = name
    side = signal_fn(name)(df).iloc[-1]
    if side == 0:
        snap["note"] = "no signal on last candle"
        return None, snap
    bar_time = df.index[-1]
    # ignore stale candles (weekend, data delay, late GitHub run): it must have closed recently
    closed_at = bar_time + pd.Timedelta(INTERVAL_LEN[tf])
    age = pd.Timestamp.now(tz="UTC") - closed_at
    if age > pd.Timedelta(getattr(config, "MAX_SIGNAL_AGE", {}).get(tf, "2h")):
        snap["note"] = f"signal too old ({int(age.total_seconds() // 60)} min)"
        return None, snap
    price, a = df["Close"].iloc[-1], atr(df).iloc[-1]
    snap["signal"] = "BUY" if side > 0 else "SELL"
    snap["note"] = "signal"
    return {
        "pair": pair, "tf": tf, "side": "BUY" if side > 0 else "SELL", "strategy": name,
        "entry": price,
        "sl": price - side * config.SL_ATR * a,
        "tp": price + side * config.TP_ATR * a,
        "rsi": rsi(df["Close"]).iloc[-1],
        "bar_time": bar_time.isoformat(), "stats": stats, "indicators": ind,
    }, snap


def format_signal(s):
    d = decimals(s["pair"])
    arrow = "🟢 BUY" if s["side"] == "BUY" else "🔴 SELL"
    title = f"{arrow} {s['pair']} ({s['tf']})"
    lines = [
        f"Entry: {s['entry']:.{d}f}",
        f"Stop loss: {s['sl']:.{d}f}",
        f"Take profit: {s['tp']:.{d}f}",
        f"R:R 1:{config.TP_ATR / config.SL_ATR:.1f} | RSI {s['rsi']:.0f}",
        f"Strategy: {s['strategy']}",
    ]
    if s["stats"]:
        st = s["stats"]
        lines.append(f"Backtest: {st['trades']} trades, {st['win_rate']:.0f}% win, PF {st['profit_factor']:.2f}")
        if st.get("test_trades") is not None:
            lines.append(f"On unseen data: {st['test_trades']} trades, {st['test_win_rate']:.0f}% win, "
                         f"PF {st['test_profit_factor']:.2f}")
    lines.append(f"Candle closed: {pd.Timestamp(s['bar_time']).strftime('%d %b %H:%M UTC')}")
    lines.append("Not financial advice. Check the chart before trading.")
    return title, "\n".join(lines)


# ---------------- signal history + results (read by the Android app) ----------------
HISTORY_FILE = "signals.json"
KEEP_SIGNALS = 300
# a trade that hits neither SL nor TP is closed at market after this many candles
MAX_OPEN_BARS = {"5m": 288, "15m": 192, "1h": 168, "4h": 120, "1d": 60}


def load_history():
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f).get("signals", [])
    except Exception:
        return []


def save_history(rows):
    data = {"updated": pd.Timestamp.now(tz="UTC").isoformat(), "signals": rows[:KEEP_SIGNALS]}
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=1)


def to_row(s):
    st = s["stats"]
    return {
        "id": f"{s['pair']}|{s['tf']}|{s['bar_time']}",
        "pair": s["pair"], "tf": s["tf"], "side": s["side"], "strategy": s["strategy"],
        "entry": round(float(s["entry"]), 6), "sl": round(float(s["sl"]), 6), "tp": round(float(s["tp"]), 6),
        "rsi": round(float(s["rsi"]), 1), "decimals": decimals(s["pair"]), "bar_time": s["bar_time"],
        "stats": None if not st else {
            "trades": st["trades"], "win_rate": round(st["win_rate"], 1),
            "profit_factor": round(min(st["profit_factor"], 99.0), 2),   # JSON can't hold infinity
            **({k: st[k] for k in ("test_trades", "test_win_rate", "test_profit_factor") if k in st}),
        },
        "indicators": s.get("indicators"),
        "status": "open",
    }


def close_trade(row, status, price, when):
    side = 1 if row["side"] == "BUY" else -1
    risk = abs(row["entry"] - row["sl"]) or 1e-9
    row.update({
        "status": status,                       # "tp", "sl" or "expired"
        "exit": round(float(price), 6),
        "closed_at": pd.Timestamp(when).isoformat(),
        "pips": round(side * (price - row["entry"]) / pip_size(row["pair"]), 1),
        "result_r": round(side * (price - row["entry"]) / risk, 2),
    })


def update_results(rows, pair, tf, df):
    """Checks this pair/timeframe's open signals against new candles. Returns closed rows."""
    closed = []
    if df is None or df.empty:
        return closed
    for row in rows:
        if row.get("pair") != pair or row.get("tf") != tf or row.get("status", "open") != "open":
            continue
        after = df[df.index > pd.Timestamp(row["bar_time"])]     # candles after the signal candle
        buy = row["side"] == "BUY"
        for t, c in after.iterrows():
            hit_sl = c["Low"] <= row["sl"] if buy else c["High"] >= row["sl"]
            hit_tp = c["High"] >= row["tp"] if buy else c["Low"] <= row["tp"]
            if hit_sl:                       # both in one candle counts as SL (same rule as backtest)
                close_trade(row, "sl", row["sl"], t)
                break
            if hit_tp:
                close_trade(row, "tp", row["tp"], t)
                break
        else:
            if len(after) >= MAX_OPEN_BARS.get(tf, 200):
                close_trade(row, "expired", after["Close"].iloc[-1], after.index[-1])
        if row.get("status", "open") != "open":
            closed.append(row)
    return closed


def format_result(row):
    d = row.get("decimals", 5)
    icon = {"tp": "✅ TP hit", "sl": "❌ SL hit", "expired": "⏱ Closed (time limit)"}[row["status"]]
    title = f"{icon}: {row['pair']} {row['side']} ({row['tf']})"
    body = (f"Result: {row['pips']:+.1f} pips ({row['result_r']:+.2f}R)\n"
            f"Entry {row['entry']:.{d}f} → Exit {row['exit']:.{d}f}")
    return title, body


def exposure(pair, side):
    """BUY EURJPY = +EUR, -JPY. Gold/silver count as their own 'currency' against USD."""
    d = 1 if side == "BUY" else -1
    return {pair[:3]: d, pair[3:]: -d}


def same_currency_clash(sig, rows):
    new = exposure(sig["pair"], sig["side"])
    for r in rows:
        if r.get("status", "open") != "open":
            continue
        old = exposure(r["pair"], r["side"])
        if any(old.get(c) == d for c, d in new.items()):
            return f"{r['pair']} {r['side']} ({r['tf']})"
    return None


def scan(dry=False):
    with logbook.Capture() as cap:
        t0 = pd.Timestamp.now(tz="UTC")
        scan_time = t0.isoformat()
        state = load_state()
        rows = load_history()
        for r in rows:
            r.setdefault("id", f"{r['pair']}|{r['tf']}|{r['bar_time']}")
            r.setdefault("status", "open")
        found = skipped = closed_n = no_data = checked = 0
        changed = False
        snaps = []
        for tf in config.TIMEFRAMES:
            for pair in config.SYMBOLS:
                checked += 1
                df = get_candles(pair, tf)
                if df is None:
                    no_data += 1
                for row in update_results(rows, pair, tf, df):
                    changed = True
                    closed_n += 1
                    title, body = format_result(row)
                    print(f"\n{title}\n{body}")
                    if not dry:
                        notify(title, body, priority="default", tags="white_check_mark" if row["status"] == "tp" else "x")
                try:
                    sig, snap = analyze(pair, tf, df, scan_time)
                except Exception as e:                       # one bad chart must not stop the scan
                    print(f"[analyze error] {pair} {tf}: {e}")
                    sig, snap = None, {"scan_time_utc": scan_time, "pair": pair, "tf": tf, "note": f"error: {e}"}
                snaps.append(snap)
                if not sig:
                    continue
                key = f"{pair}|{tf}|{sig['bar_time']}"
                if key in state:
                    snap["note"] = "signal already sent"
                    continue
                state[key] = sig["bar_time"]
                clash = same_currency_clash(sig, rows) if getattr(config, "ONE_TRADE_PER_CURRENCY", False) else None
                if clash:
                    snap["note"] = f"skipped: same currency as open {clash}"
                    print(f"[skip] {sig['side']} {pair} ({tf}): same currency bet as open {clash}")
                    skipped += 1
                    continue
                title, body = format_signal(sig)
                print(f"\n{title}\n{body}")
                if not dry:
                    notify(title, body, tags="green_circle" if sig["side"] == "BUY" else "red_circle")
                rows.insert(0, to_row(sig))
                found += 1
                changed = True
        if not dry:
            save_state(state)
            if changed:
                save_history(rows)
        secs = (pd.Timestamp.now(tz="UTC") - t0).total_seconds()
        print(f"\n[{pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC] scan done in {secs:.0f}s: {found} new signal(s), "
              f"{skipped} skipped (same currency), {closed_n} closed, {no_data} chart(s) without data.")
    if not dry:
        printed = cap.text()
        errors = [ln for ln in printed.splitlines() if ln.startswith("[") and "error" in ln.lower()
                  or ln.startswith("[data]") or ln.startswith("[ntfy]") or ln.startswith("[telegram]")]
        summary = {"scan_time_utc": scan_time, "seconds": round(secs), "checked": checked, "no_data": no_data,
                   "new_signals": found, "skipped_same_currency": skipped, "trades_closed": closed_n,
                   "open_trades": sum(1 for r in rows if r.get("status", "open") == "open"),
                   "errors": " | ".join(errors[:3])[:300]}
        try:
            logbook.write_all(rows, pip_size, snaps, summary, printed, force=bool(changed or skipped or errors))
        except Exception as e:
            print(f"[log error] {e}")
    return found


if __name__ == "__main__":
    args = set(sys.argv[1:])
    if "--test" in args:
        ok = notify("✅ Forex bot connected", "Test message: signals will arrive here.", priority="default")
        sys.exit(0 if ok else 1)
    if "--loop" in args:
        while True:
            try:
                scan()
            except Exception as e:
                print(f"[scan error] {e}")
            time.sleep(300)
    else:
        scan(dry="--dry" in args)
