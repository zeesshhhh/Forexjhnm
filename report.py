"""Honest strategy test, run on GitHub (where price data is available).

The bot picks the strategy that did best on past data. That past data is the same data it was tested on,
so the backtest numbers look better than real trading. This script does it the honest way:
  * pick on the OLDER 70% of the history,
  * then judge on the NEWER 30% the pick has never seen,
  * and subtract a typical broker spread from every trade.
It writes backtest_report.md (easy to read) and backtest_report.json (for Claude).
"""
import json
import time

import numpy as np
import pandas as pd

import config
from strategies import STRATEGIES, atr, ema

PERIODS = {                    # as much history as Yahoo gives for free
    "5m": ("5m", "59d", None),
    "15m": ("15m", "59d", None),
    "1h": ("60m", "720d", None),
    "4h": ("60m", "720d", "4h"),
    "1d": ("1d", "10y", None),
}
TRAIN_SHARE = 0.7
MIN_TRADES = config.MIN_TRADES_FOR_AUTO
MIN_PF = config.MIN_PROFIT_FACTOR
SL_ATR, TP_ATR = config.SL_ATR, config.TP_ATR

MAJORS = {"EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"}


def pip_size(pair):
    if pair == "XAUUSD":
        return 0.1
    if pair == "XAGUSD":
        return 0.01
    return 0.01 if "JPY" in pair else 0.0001


def spread_pips(pair):
    """Typical retail spread, in pips."""
    if pair in MAJORS:
        return 1.2
    if pair == "XAUUSD":
        return 3.0       # about $0.30
    if pair == "XAGUSD":
        return 3.0       # about $0.03
    return 2.5


_cache = {}
TF_LEN = {"5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h", "1d": "1D"}


def drop_open_candle(df, tf):
    now = pd.Timestamp.now(tz="UTC")
    if tf == "1d":
        return df[df.index.tz_convert("UTC").normalize() < now.normalize()]
    return df[df.index + pd.Timedelta(TF_LEN[tf]) <= now]


def candles(pair, tf):
    import yfinance as yf
    interval, period, resample = PERIODS[tf]
    key = (pair, interval, period)
    if key not in _cache:
        df = None
        for attempt in range(3):
            try:
                df = yf.Ticker(config.SYMBOLS[pair]).history(period=period, interval=interval, auto_adjust=False)
                break
            except Exception as e:
                print(f"[data] {pair} {tf}: {e}")
                time.sleep(3)
        if df is None or df.empty:
            _cache[key] = None
        else:
            df = df[["Open", "High", "Low", "Close"]].dropna()
            df.index = pd.to_datetime(df.index, utc=True)
            _cache[key] = df
    df = _cache[key]
    if df is None:
        return None
    if resample:
        df = df.resample(resample, origin="epoch").agg(
            {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    df = drop_open_candle(df, tf)
    # drop broken candles (zero or inverted ranges)
    df = df[(df["High"] >= df["Low"]) & (df["Low"] > 0)]
    return df


def with_trend(fn, mult=4):
    """Only trade in the direction of the bigger trend: EMA(200 x 4) is about EMA 200 one timeframe up."""
    def f(df):
        s = fn(df)
        t = ema(df["Close"], 200 * mult)
        c = df["Close"]
        s = s.where(~((s > 0) & (c <= t)), 0)
        s = s.where(~((s < 0) & (c >= t)), 0)
        return s
    return f


VARIANTS = {}
for _name, _fn in STRATEGIES.items():
    VARIANTS[_name] = _fn
    VARIANTS[_name + "+trend"] = with_trend(_fn)


def trades(df, sig, pair):
    """List of (entry_index, R before costs, R after spread). One trade at a time; SL first if both in one candle."""
    a = atr(df).values
    hi, lo, cl = df["High"].values, df["Low"].values, df["Close"].values
    sig = sig.values
    rr = TP_ATR / SL_ATR
    out, i, n = [], 210, len(df)
    p, spr = pip_size(pair), spread_pips(pair)
    while i < n - 1:
        side = sig[i]
        if side == 0 or not np.isfinite(a[i]) or a[i] <= 0:
            i += 1
            continue
        entry = cl[i]
        risk = SL_ATR * a[i]
        sl, tp = entry - side * risk, entry + side * TP_ATR * a[i]
        j, r = i + 1, None
        while j < n:
            if (lo[j] <= sl) if side > 0 else (hi[j] >= sl):
                r = -1.0
                break
            if (hi[j] >= tp) if side > 0 else (lo[j] <= tp):
                r = rr
                break
            j += 1
        if r is None:
            break                                  # still open at the end: not counted
        cost = spr * p / risk                      # spread as a share of the stop distance
        out.append((i, r, r - cost, risk / p))
        i = j + 1
    return out


def stats(rs):
    rs = list(rs)
    if not rs:
        return {"trades": 0, "win_rate": 0.0, "pf": 0.0, "total_r": 0.0}
    r = np.array(rs)
    wins, losses = r[r > 0].sum(), -r[r < 0].sum()
    return {"trades": int(len(r)), "win_rate": round(float((r > 0).mean() * 100), 1),
            "pf": round(float(wins / losses), 2) if losses > 0 else 99.0, "total_r": round(float(r.sum()), 1)}


def main():
    t0 = time.time()
    rows = []                                   # one row per pair x tf x variant
    for tf in PERIODS:
        for pair in config.SYMBOLS:
            df = candles(pair, tf)
            if df is None or len(df) < 600:
                print(f"skip {pair} {tf}: {0 if df is None else len(df)} candles")
                continue
            split = int(len(df) * TRAIN_SHARE)
            for vname, fn in VARIANTS.items():
                tr = trades(df, fn(df), pair)
                train = [t for t in tr if t[0] < split]
                test = [t for t in tr if t[0] >= split]
                rows.append({
                    "tf": tf, "pair": pair, "variant": vname, "candles": len(df),
                    "test_from": df.index[split].isoformat(),
                    "train": stats(t[1] for t in train),
                    "test": stats(t[1] for t in test),
                    "test_after_spread": stats(t[2] for t in test),
                    "avg_stop_pips": round(float(np.mean([t[3] for t in tr])), 1) if tr else None,
                })
            print(f"{tf} {pair}: {len(df)} candles")

    # ---- selection methods, judged on the unseen 30% ----
    def pick(cands):
        ok = [c for c in cands if c["train"]["trades"] >= MIN_TRADES and c["train"]["pf"] >= MIN_PF]
        return max(ok, key=lambda c: (c["train"]["pf"], c["train"]["total_r"])) if ok else None

    methods = {}
    by_key = {}
    for r in rows:
        by_key.setdefault((r["tf"], r["pair"]), []).append(r)

    def add(method, tf, r):
        m = methods.setdefault(method, {}).setdefault(tf, {"raw": [], "net": [], "pairs": 0})
        if r is None:
            return
        m["pairs"] += 1
        m["raw"].append(r["test"])
        m["net"].append(r["test_after_spread"])

    for (tf, pair), cands in by_key.items():
        base = [c for c in cands if not c["variant"].endswith("+trend")]
        trend = [c for c in cands if c["variant"].endswith("+trend")]
        add("auto (what the bot does now)", tf, pick(base))
        add("auto + trend filter", tf, pick(trend))
        for c in cands:
            add("always " + c["variant"], tf, c)

    def combine(parts):
        n = sum(p["trades"] for p in parts)
        if not n:
            return {"trades": 0, "win_rate": 0.0, "pf": 0.0, "total_r": 0.0}
        wins = sum(p["trades"] * p["win_rate"] / 100 for p in parts)
        tot = sum(p["total_r"] for p in parts)
        return {"trades": n, "win_rate": round(100 * wins / n, 1), "total_r": round(tot, 1),
                "r_per_trade": round(tot / n, 3)}

    summary = {}
    for method, tfs in methods.items():
        for tf, m in tfs.items():
            summary.setdefault(tf, {})[method] = {"pairs_traded": m["pairs"], "before_spread": combine(m["raw"]),
                                                   "after_spread": combine(m["net"])}

    report = {"generated": pd.Timestamp.now(tz="UTC").isoformat(), "seconds": round(time.time() - t0),
              "settings": {"sl_atr": SL_ATR, "tp_atr": TP_ATR, "train_share": TRAIN_SHARE,
                           "min_trades": MIN_TRADES, "min_pf": MIN_PF},
              "summary": summary, "rows": rows}
    with open("backtest_report.json", "w") as f:
        json.dump(report, f)

    lines = ["# Strategy report", "",
             f"Generated {report['generated'][:16]} UTC. Strategies were picked on the older 70% of each chart and "
             "tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from "
             "every trade. R = what you risked per trade (a loss is -1R, a win is +2R).", ""]
    for tf in PERIODS:
        if tf not in summary:
            continue
        lines += [f"## {tf}", "", "| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |",
                  "|---|---|---|---|---|"]
        items = sorted(summary[tf].items(), key=lambda kv: -kv[1]["after_spread"].get("r_per_trade", -9)
                       if kv[1]["after_spread"]["trades"] >= 20 else 9)
        for method, s in items:
            a = s["after_spread"]
            if not a["trades"]:
                continue
            lines.append(f"| {method} | {a['trades']} | {a['win_rate']} | {a.get('r_per_trade', 0):+.3f} | {a['total_r']:+.1f} |")
        lines.append("")
    with open("backtest_report.md", "w") as f:
        f.write("\n".join(lines))
    print(f"done in {report['seconds']}s")


if __name__ == "__main__":
    main()
