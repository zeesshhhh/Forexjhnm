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
    # ignore stale bars (e.g. weekend / data delay): last closed bar must be recent
    if pd.Timestamp.now(tz="UTC") - bar_time > 3 * pd.Timedelta(INTERVAL_LEN[tf]) + pd.Timedelta("1h"):
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


def save_history(new_signals, path="signals.json", keep=300):
    """signals.json is what the Android app reads (newest first)."""
    try:
        with open(path) as f:
            old = json.load(f).get("signals", [])
    except Exception:
        old = []
    rows = []
    for s in new_signals:
        st = s["stats"]
        rows.append({
            "pair": s["pair"], "tf": s["tf"], "side": s["side"], "strategy": s["strategy"],
            "entry": round(float(s["entry"]), 6), "sl": round(float(s["sl"]), 6), "tp": round(float(s["tp"]), 6),
            "rsi": round(float(s["rsi"]), 1), "decimals": decimals(s["pair"]), "bar_time": s["bar_time"],
            "stats": None if not st else {
                "trades": st["trades"], "win_rate": round(st["win_rate"], 1),
                "profit_factor": round(min(st["profit_factor"], 99.0), 2),   # JSON can't hold infinity
            },
        })
    data = {"updated": pd.Timestamp.now(tz="UTC").isoformat(), "signals": (rows + old)[:keep]}
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def scan(dry=False):
    state = load_state()
    found, new_signals = 0, []
    for tf in config.TIMEFRAMES:
        for pair in config.SYMBOLS:
            sig = check(pair, tf, get_candles(pair, tf))
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
            new_signals.append(sig)
            found += 1
    if not dry:
        save_state(state)
        if new_signals:
            save_history(new_signals)
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
