"""Forex signal bot: scans all pairs/timeframes and pushes new signals to your Android phone.

    python bot.py            # scan once (used by GitHub Actions every 15 min)
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
from backtest import rank_strategies
from data import INTERVAL_LEN, get_candles
from strategies import STRATEGIES, atr, rsi


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


def pick_strategy(df):
    """Returns (strategy name, backtest stats) or (None, None) if nothing is good enough."""
    if config.STRATEGY != "auto":
        return config.STRATEGY, None
    best = rank_strategies(df)[0]
    if best["trades"] < config.MIN_TRADES_FOR_AUTO or best["profit_factor"] < config.MIN_PROFIT_FACTOR:
        return None, None
    return best["strategy"], best


def check(pair, tf, df):
    if df is None or len(df) < 250:
        return None
    name, stats = pick_strategy(df)
    if not name:
        return None
    side = STRATEGIES[name](df).iloc[-1]
    if side == 0:
        return None
    bar_time = df.index[-1]
    # ignore stale candles (weekend, data delay, late GitHub run): it must have closed recently
    closed_at = bar_time + pd.Timedelta(INTERVAL_LEN[tf])
    if pd.Timestamp.now(tz="UTC") - closed_at > pd.Timedelta(getattr(config, "MAX_SIGNAL_AGE", {}).get(tf, "2h")):
        return None
    price, a = df["Close"].iloc[-1], atr(df).iloc[-1]
    return {
        "pair": pair, "tf": tf, "side": "BUY" if side > 0 else "SELL", "strategy": name,
        "entry": price,
        "sl": price - side * config.SL_ATR * a,
        "tp": price + side * config.TP_ATR * a,
        "rsi": rsi(df["Close"]).iloc[-1],
        "bar_time": bar_time.isoformat(), "stats": stats,
    }


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
    lines.append(f"Candle closed: {pd.Timestamp(s['bar_time']).strftime('%d %b %H:%M UTC')}")
    lines.append("Not financial advice. Check the chart before trading.")
    return title, "\n".join(lines)


# ---------------- signal history + results (read by the Android app) ----------------
HISTORY_FILE = "signals.json"
KEEP_SIGNALS = 300
# a trade that hits neither SL nor TP is closed at market after this many candles
MAX_OPEN_BARS = {"5m": 288, "15m": 192, "1h": 168, "4h": 120, "1d": 60}


def pip_size(pair):
    if pair == "XAUUSD":
        return 0.1
    if pair == "XAGUSD":
        return 0.01
    return 0.01 if "JPY" in pair else 0.0001


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
        },
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


def scan(dry=False):
    state = load_state()
    rows = load_history()
    for r in rows:
        r.setdefault("id", f"{r['pair']}|{r['tf']}|{r['bar_time']}")
        r.setdefault("status", "open")
    found, changed = 0, False
    for tf in config.TIMEFRAMES:
        for pair in config.SYMBOLS:
            df = get_candles(pair, tf)
            for row in update_results(rows, pair, tf, df):
                changed = True
                title, body = format_result(row)
                print(f"\n{title}\n{body}")
                if not dry:
                    notify(title, body, priority="default", tags="white_check_mark" if row["status"] == "tp" else "x")
            sig = check(pair, tf, df)
            if not sig:
                continue
            key = f"{pair}|{tf}|{sig['bar_time']}"
            if key in state:
                continue
            title, body = format_signal(sig)
            print(f"\n{title}\n{body}")
            if not dry:
                notify(title, body, tags="green_circle" if sig["side"] == "BUY" else "red_circle")
            state[key] = sig["bar_time"]
            rows.insert(0, to_row(sig))
            found += 1
            changed = True
    if not dry:
        save_state(state)
        if changed:
            save_history(rows)
    print(f"\n[{pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC] scan done, {found} new signal(s).")
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
