"""Paper-trading lab: every pair x every timeframe x every strategy, traded on paper in the background.

Nothing here is sent to a broker. Each lab trade has the same stop loss / take profit rules as the main
signals (1.5 x ATR / 3 x ATR) and records the same facts (candle pattern, market direction, RSI zone,
volatility, news), so the logs show which timeframe, strategy and indicator actually make money.

Files (in logs/lab/):
  lab_state.json          open lab trades, the latest closed ones, running totals since the lab started
  trades/YYYY-MM-DD.csv   every closed lab trade of that day (kept 30 days)
  lab_performance.json    last 30 days grouped by setup, timeframe, strategy, pattern, direction, ...
"""
import csv
import json
import os

import pandas as pd

import config
import features
from strategies import STRATEGIES, atr, rsi

LAB_DIR = os.path.join(getattr(config, "LOG_DIR", "logs"), "lab")
STATE = os.path.join(LAB_DIR, "lab_state.json")
TRADES_DIR = os.path.join(LAB_DIR, "trades")
PERF = os.path.join(LAB_DIR, "lab_performance.json")

LEN = {"5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h", "1d": "1D"}
MAX_OPEN_BARS = {"5m": 288, "15m": 192, "1h": 168, "4h": 120, "1d": 60}
RECENT_CLOSED = 200

FEATURE_COLS = ["pattern", "pattern_vs_trade", "trend", "bigger_trend", "direction_vs_trade", "rsi_zone",
                "volatility", "weekday", "session", "news_next_24h", "news_prev_24h", "news_titles"]
CSV_COLS = (["id", "pair", "tf", "side", "strategy", "signal_candle_utc", "entry", "sl", "tp", "stop_pips",
             "status", "closed_at_utc", "exit", "pips", "result_r", "spread_pips", "pips_net", "r_net"] + FEATURE_COLS)
MAJORS = {"EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"}


def spread_pips(pair):
    """Typical broker spread in pips (change in config.SPREAD_PIPS). Paid once per trade."""
    sp = getattr(config, "SPREAD_PIPS", {})
    if pair in sp:
        return float(sp[pair])
    if pair in ("XAUUSD", "XAGUSD"):
        return float(sp.get("metals", 3.0))
    return float(sp.get("majors", 1.2) if pair in MAJORS else sp.get("crosses", 2.5))


def add_net(t):
    """Result after spread: pips minus the spread, and R minus spread / stop distance."""
    if t.get("r_net") is not None or t.get("result_r") is None:
        return t
    sp = spread_pips(t["pair"])
    stop = abs(float(t["entry"]) - float(t["sl"])) / pip_size(t["pair"]) or 1e-9
    t["spread_pips"] = sp
    t["pips_net"] = round(float(t["pips"]) - sp, 1)
    t["r_net"] = round(float(t["result_r"]) - sp / stop, 3)
    return t


def pip_size(pair):
    if pair == "XAUUSD":
        return 0.1
    if pair == "XAGUSD":
        return 0.01
    return 0.01 if "JPY" in pair else 0.0001


def decimals(pair):
    return 2 if pair.startswith("XA") else 3 if "JPY" in pair else 5


CONV = {"EUR": "EURUSD", "GBP": "GBPUSD", "AUD": "AUDUSD", "NZD": "NZDUSD",
        "JPY": "USDJPY", "CHF": "USDCHF", "CAD": "USDCAD"}


def rates_from(dfs):
    """Latest prices of the 7 USD pairs, to turn pips into dollars."""
    out = {}
    for (pair, tf), df in dfs.items():
        if df is None or df.empty or pair not in CONV.values():
            continue
        if pair not in out or tf in ("5m", "15m"):
            out[pair] = float(df["Close"].iloc[-1])
    return out


def usd_per_pip_1lot(pair, rates):
    """Dollar value of 1 pip for 1.00 lot (100,000 units; gold 100 oz; silver 5,000 oz)."""
    if pair == "XAUUSD":
        return 10.0
    if pair == "XAGUSD":
        return 50.0
    q = pair[3:]
    if q == "USD":
        to_usd = 1.0
    elif q in ("JPY", "CHF", "CAD"):
        r = rates.get("USD" + q)
        to_usd = 1.0 / r if r else None
    else:
        to_usd = rates.get(q + "USD")
    return None if to_usd is None else 100000 * pip_size(pair) * to_usd


def _now():
    return pd.Timestamp.now(tz="UTC")


def load_state():
    try:
        with open(STATE) as f:
            st = json.load(f)
    except Exception:
        st = {}
    st.setdefault("started", _now().isoformat())
    sigs = st.pop("signals", [])                                   # stored once, split on load
    st["open"] = [t for t in sigs if t.get("status") == "open"]
    st["recent_closed"] = [t for t in sigs if t.get("status") != "open"]
    st.setdefault("last_bar", {})
    st.setdefault("pending", {"new": [], "closed": []})
    st.setdefault("last_digest", "")
    st.setdefault("totals", {"closed": 0, "won": 0, "lost": 0, "total_r": 0.0, "total_pips": 0.0})
    for k in ("won_r", "lost_r", "usd_1lot", "won_usd_1lot", "lost_usd_1lot"):
        st["totals"].setdefault(k, 0.0)
    return st


def save_state(st):
    os.makedirs(LAB_DIR, exist_ok=True)
    out = {k: v for k, v in st.items() if k not in ("open", "recent_closed")}
    out["updated"] = _now().isoformat()
    out["signals"] = st["open"] + st["recent_closed"]         # same shape the app reads for main signals
    with open(STATE, "w") as f:
        json.dump(out, f, separators=(",", ":"))


def _close(t, status, price, when):
    side = 1 if t["side"] == "BUY" else -1
    risk = abs(t["entry"] - t["sl"]) or 1e-9
    t.update({"status": status, "exit": round(float(price), 6), "closed_at": pd.Timestamp(when).isoformat(),
              "pips": round(side * (price - t["entry"]) / pip_size(t["pair"]), 1),
              "result_r": round(side * (price - t["entry"]) / risk, 2)})
    add_net(t)


def _check_open(t, df):
    """Same rules as the main bot: SL first if both are touched in one candle; time limit closes at market."""
    after = df[df.index > pd.Timestamp(t["bar_time"])]
    buy = t["side"] == "BUY"
    H, L = after["High"].values, after["Low"].values
    for k in range(len(after)):
        if (L[k] <= t["sl"]) if buy else (H[k] >= t["sl"]):
            _close(t, "sl", t["sl"], after.index[k])
            return True
        if (H[k] >= t["tp"]) if buy else (L[k] <= t["tp"]):
            _close(t, "tp", t["tp"], after.index[k])
            return True
    if len(after) >= MAX_OPEN_BARS[t["tf"]]:
        _close(t, "expired", after["Close"].iloc[-1], after.index[-1])
        return True
    return False


def _migrate_csv(path):
    """Rewrites a day file made before the spread columns existed."""
    if not os.path.exists(path):
        return
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        if r.fieldnames == CSV_COLS:
            return
        rows = list(r)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            try:
                add_net(row)
            except Exception:
                pass
            w.writerow({k: row.get(k, "") for k in CSV_COLS})


def _append_csv(trades):
    os.makedirs(TRADES_DIR, exist_ok=True)
    by_day = {}
    for t in trades:
        by_day.setdefault(t["closed_at"][:10], []).append(t)
    for day, ts in by_day.items():
        path = os.path.join(TRADES_DIR, f"{day}.csv")
        _migrate_csv(path)
        new = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
            if new:
                w.writeheader()
            for t in ts:
                f_ = t.get("features") or {}
                row = {k: t.get(k) for k in CSV_COLS}
                row.update({"signal_candle_utc": t["bar_time"], "closed_at_utc": t["closed_at"],
                            "stop_pips": round(abs(t["entry"] - t["sl"]) / pip_size(t["pair"]), 1)})
                row.update({k: f_.get(k) for k in CSV_COLS if k in f_})
                w.writerow(row)
    keep = getattr(config, "LAB_KEEP_DAYS", 30)
    cutoff = (_now() - pd.Timedelta(days=keep)).strftime("%Y-%m-%d")
    for name in os.listdir(TRADES_DIR):
        if name.endswith(".csv") and name[:10] < cutoff:
            os.remove(os.path.join(TRADES_DIR, name))


def write_performance():
    """Last 30 days of closed lab trades, grouped like the main performance log (plus 'Setup')."""
    import logbook
    rows = []
    if os.path.isdir(TRADES_DIR):
        for name in sorted(os.listdir(TRADES_DIR)):
            if not name.endswith(".csv"):
                continue
            with open(os.path.join(TRADES_DIR, name), newline="") as f:
                for r in csv.DictReader(f):
                    try:
                        rr = float(r["r_net"]) if r.get("r_net") not in (None, "") else float(add_net(dict(r))["r_net"])
                    except Exception:
                        continue
                    n = r.get("news_next_24h")
                    feats = {k: r.get(k) for k in FEATURE_COLS if r.get(k) not in (None, "")}
                    if n not in (None, "", "not set up"):
                        try:
                            feats["news_next_24h"] = int(n)
                        except ValueError:
                            pass
                    rows.append({"pair": r["pair"], "tf": r["tf"], "side": r["side"], "strategy": r["strategy"],
                                 "status": r["status"], "result_r": rr, "closed_at": r["closed_at_utc"],
                                 "features": feats})
    perf = logbook.performance(rows)
    setup = {}
    for s in rows:
        setup.setdefault(f"{s['tf']} {s['strategy']}", []).append(s["result_r"])
    srows = []
    for v, rs in setup.items():
        wins = sum(1 for r in rs if r > 0)
        srows.append({"value": v, "trades": len(rs), "wins": wins, "win_rate": round(100 * wins / len(rs), 1),
                      "total_r": round(sum(rs), 2), "avg_r": round(sum(rs) / len(rs), 3)})
    srows.sort(key=lambda r: (-r["avg_r"], -r["trades"]))
    perf["factors"].insert(0, {"name": "Setup (timeframe + strategy)", "rows": srows})
    perf["window"] = f"last {getattr(config, 'LAB_KEEP_DAYS', 30)} days"
    perf["after_spread"] = True
    os.makedirs(LAB_DIR, exist_ok=True)
    with open(PERF, "w") as f:
        json.dump(perf, f, indent=1)


def _digest(st, notify, force=False):
    every = getattr(config, "LAB_ALERT_EVERY_MINUTES", 30)
    new, closed = st["pending"]["new"], st["pending"]["closed"]
    if not new and not closed:
        return
    last = st.get("last_digest")
    if not force and last and _now() - pd.Timestamp(last) < pd.Timedelta(minutes=every):
        return
    lines = []
    if new:
        by_tf = {}
        for n in new:
            by_tf[n["tf"]] = by_tf.get(n["tf"], 0) + 1
        lines.append(f"New: {len(new)} (" + ", ".join(f"{k} {v}" for k, v in by_tf.items()) + ")")
        for n in new[:6]:
            lines.append(f"  {n['side']} {n['pair']} {n['tf']} {n['strategy']} @ {n['entry']:.{decimals(n['pair'])}f}")
        if len(new) > 6:
            lines.append(f"  ...and {len(new) - 6} more")
    if closed:
        won = sum(1 for c in closed if c["r"] > 0)
        lines.append(f"Closed: {len(closed)} ({won} won, {len(closed) - won} lost), "
                     f"{sum(c['r'] for c in closed):+.1f}R after spread")
    t = st["totals"].get("net") or st["totals"]
    lines.append(f"Lab since start: {t['closed']} closed, {t['won']} won, {t['total_r']:+.1f}R after spread")
    if notify:
        notify(f"\U0001F9EA Lab: {len(new)} new, {len(closed)} closed", "\n".join(lines),
               priority="low", tags="test_tube")
    st["pending"] = {"new": [], "closed": []}
    st["last_digest"] = _now().isoformat()


def _empty_net():
    return {"closed": 0, "won": 0, "lost": 0, "total_r": 0.0, "won_r": 0.0, "lost_r": 0.0,
            "usd_1lot": 0.0, "won_usd_1lot": 0.0, "lost_usd_1lot": 0.0}


def _backfill_net(st, rates):
    """Once: after-spread totals for trades closed before this update (from the day files)."""
    n = _empty_net()
    if os.path.isdir(TRADES_DIR):
        for name in sorted(os.listdir(TRADES_DIR)):
            if not name.endswith(".csv"):
                continue
            path = os.path.join(TRADES_DIR, name)
            _migrate_csv(path)
            with open(path, newline="") as f:
                for r in csv.DictReader(f):
                    try:
                        rn, pn = float(r["r_net"]), float(r["pips_net"])
                    except Exception:
                        continue
                    n["closed"] += 1
                    n["won" if rn > 0 else "lost"] += 1
                    n["total_r"] += rn
                    n["won_r" if rn > 0 else "lost_r"] += rn
                    v = usd_per_pip_1lot(r["pair"], rates)
                    if v is not None:
                        n["usd_1lot"] += pn * v
                        n["won_usd_1lot" if rn > 0 else "lost_usd_1lot"] += pn * v
    st["totals"]["net"] = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in n.items()}
    for t in st["recent_closed"]:
        add_net(t)


def run(dfs, events=None, notify=None, dry=False):
    """dfs: {(pair, tf): candles}. Called once per scan, after the main signals."""
    if not getattr(config, "LAB_ENABLED", False):
        return {"new": 0, "closed": 0, "open": 0}
    st = load_state()
    max_age = getattr(config, "MAX_SIGNAL_AGE", {})
    names = [n for n in getattr(config, "LAB_STRATEGIES", list(STRATEGIES)) if n in STRATEGIES]
    tfs = getattr(config, "LAB_TIMEFRAMES", list(LEN))

    # 1) results for open lab trades
    rates = rates_from(dfs)
    if "net" not in st["totals"]:
        _backfill_net(st, rates)
    still, closed_now = [], []
    for t in st["open"]:
        df = dfs.get((t["pair"], t["tf"]))
        if df is not None and not df.empty and _check_open(t, df):
            closed_now.append(t)
        else:
            still.append(t)
    st["open"] = still
    for t in closed_now:
        tot = st["totals"]
        tot["closed"] += 1
        tot["won" if t["result_r"] > 0 else "lost"] += 1
        tot["total_r"] = round(tot["total_r"] + t["result_r"], 2)
        tot["total_pips"] = round(tot["total_pips"] + t["pips"], 1)
        k = "won_r" if t["result_r"] > 0 else "lost_r"
        tot[k] = round(tot[k] + t["result_r"], 2)
        v = usd_per_pip_1lot(t["pair"], rates)               # dollars at 1.00 lot, for the lot-size paper account
        if v is not None:
            t["usd_1lot"] = round(t["pips"] * v, 2)
            tot["usd_1lot"] = round(tot["usd_1lot"] + t["usd_1lot"], 2)
            k2 = "won_usd_1lot" if t["result_r"] > 0 else "lost_usd_1lot"
            tot[k2] = round(tot[k2] + t["usd_1lot"], 2)
        n = tot["net"]
        n["closed"] += 1
        n["won" if t["r_net"] > 0 else "lost"] += 1
        n["total_r"] = round(n["total_r"] + t["r_net"], 3)
        kn = "won_r" if t["r_net"] > 0 else "lost_r"
        n[kn] = round(n[kn] + t["r_net"], 3)
        if v is not None:
            u = round(t["pips_net"] * v, 2)
            n["usd_1lot"] = round(n["usd_1lot"] + u, 2)
            ku = "won_usd_1lot" if t["r_net"] > 0 else "lost_usd_1lot"
            n[ku] = round(n[ku] + u, 2)
        st["pending"]["closed"].append({"r": t["r_net"]})
    st["recent_closed"] = (sorted(closed_now, key=lambda t: t["closed_at"], reverse=True) + st["recent_closed"])[:RECENT_CLOSED]

    # 2) new lab trades: one open trade at a time per pair x timeframe x strategy
    open_combos = {(t["pair"], t["tf"], t["strategy"]) for t in st["open"]}
    new_now = []
    for (pair, tf), df in dfs.items():
        if tf not in tfs or df is None or len(df) < 250:
            continue
        bar_time = df.index[-1]
        age = _now() - (bar_time + pd.Timedelta(LEN[tf]))
        if age > pd.Timedelta(max_age.get(tf, "2h")):
            continue
        a = r14 = None
        for name in names:
            combo = f"{pair}|{tf}|{name}"
            if (pair, tf, name) in open_combos or st["last_bar"].get(combo) == bar_time.isoformat():
                continue
            try:
                side = STRATEGIES[name](df).iloc[-1]
            except Exception as e:
                print(f"[lab error] {pair} {tf} {name}: {e}")
                continue
            if side == 0:
                continue
            if a is None:
                a = float(atr(df).iloc[-1])
                r14 = round(float(rsi(df["Close"]).iloc[-1]), 1)
            price = float(df["Close"].iloc[-1])
            side_s = "BUY" if side > 0 else "SELL"
            try:
                facts = features.describe(df, pair, tf, side_s, events, bar_time + pd.Timedelta(LEN[tf]))
            except Exception:
                facts = {}
            t = {"id": f"{combo}|{bar_time.isoformat()}", "lab": True, "pair": pair, "tf": tf, "side": side_s,
                 "strategy": name, "entry": round(price, 6),
                 "sl": round(price - side * config.SL_ATR * a, 6), "tp": round(price + side * config.TP_ATR * a, 6),
                 "rsi": r14, "decimals": decimals(pair), "bar_time": bar_time.isoformat(), "status": "open",
                 "stats": None, "features": facts}
            st["open"].append(t)
            open_combos.add((pair, tf, name))
            st["last_bar"][combo] = bar_time.isoformat()
            new_now.append(t)
            st["pending"]["new"].append({"pair": pair, "tf": tf, "side": side_s, "strategy": name, "entry": price})

    if dry:
        return {"new": len(new_now), "closed": len(closed_now), "open": len(st["open"])}
    if closed_now:
        _append_csv(closed_now)
    _digest(st, notify)
    save_state(st)
    write_performance()
    return {"new": len(new_now), "closed": len(closed_now), "open": len(st["open"])}
