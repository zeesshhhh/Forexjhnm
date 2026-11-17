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
from strategies import STRATEGIES, atr, ema, rsi

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


def factor_report():
    """Every past trade of the CURRENT setup, grouped by timeframe, candle pattern, market direction,
    RSI zone, volatility, weekday and pair type (after spread). Uses the same rules as the live logs."""
    import features
    name = config.STRATEGY if config.STRATEGY in STRATEGIES else "bollinger"
    use_trend = getattr(config, "TREND_FILTER", False)
    fn = with_trend(STRATEGIES[name]) if use_trend else STRATEGIES[name]
    detail_tfs = getattr(config, "SIGNAL_TIMEFRAMES", ["1d"])
    per_tf, rows = {}, []
    for tf in PERIODS:
        for pair in config.SYMBOLS:
            df = candles(pair, tf)
            if df is None or len(df) < 600:
                continue
            sig = fn(df)
            tr = trades(df, sig, pair)
            per_tf.setdefault(tf, []).extend(t[2] for t in tr)
            if tf not in detail_tfs or not tr:
                continue
            O, H, L, C = df["Open"].values, df["High"].values, df["Low"].values, df["Close"].values
            r14 = rsi(df["Close"]).values
            a = atr(df)
            ratio = (a / a.rolling(100).mean()).values
            e200 = ema(df["Close"], 200).values
            e800 = ema(df["Close"], 800).values
            sv = sig.values
            for (i, r_raw, r_net, _stop) in tr:
                side = "BUY" if sv[i] > 0 else "SELL"
                pat = features.pattern_from(O[i], H[i], L[i], C[i], O[i - 1], H[i - 1], L[i - 1], C[i - 1])
                rows.append({
                    "r": r_net, "tf": tf, "side": side, "pair": pair,
                    "pair_type": "gold / silver" if pair in ("XAUUSD", "XAGUSD") else ("major" if "USD" in pair else "cross"),
                    "pattern": pat, "pattern_vs_trade": features.pattern_vs_trade(pat, side),
                    "direction": features.direction_label(C[i] > e200[i], C[i] > e800[i], side),
                    "rsi_zone": features.rsi_zone(float(r14[i])), "volatility": features.vol_label(float(ratio[i])),
                    "weekday": df.index[i].day_name(), "year": str(df.index[i].year),
                    "time": df.index[i].isoformat(),
                })

    # older half vs newer half of all trades (same number of trades in each): an idea only counts
    # if it works in BOTH halves, otherwise it is probably luck
    times = sorted(t["time"] for t in rows)
    split = times[len(times) // 2] if times else ""

    def table(values_and_rs):
        groups = {}
        for item in values_and_rs:
            v, r = item[0], item[1]
            newer = item[2] if len(item) > 2 else None
            g = groups.setdefault(str(v), {"all": [], "old": [], "new": []})
            g["all"].append(r)
            if newer is not None:
                g["new" if newer else "old"].append(r)
        out = []
        for v, g in groups.items():
            rs = g["all"]
            wins = sum(1 for r in rs if r > 0)
            row = {"value": v, "trades": len(rs), "wins": wins, "win_rate": round(100 * wins / len(rs), 1),
                   "total_r": round(float(sum(rs)), 1), "avg_r": round(float(sum(rs)) / len(rs), 3)}
            for k in ("old", "new"):
                if g[k]:
                    row[f"{k}_trades"] = len(g[k])
                    row[f"{k}_avg_r"] = round(float(sum(g[k])) / len(g[k]), 3)
            out.append(row)
        return sorted(out, key=lambda r: (-r["avg_r"], -r["trades"]))

    factors = [{"name": "Timeframe (same setup, all pairs)",
                "rows": table((tf, r) for tf, rs in per_tf.items() for r in rs)}]
    for label, key in [("Candle pattern", "pattern"), ("Candle vs trade", "pattern_vs_trade"),
                       ("Market direction", "direction"), ("RSI zone", "rsi_zone"), ("Volatility", "volatility"),
                       ("Buy or sell", "side"), ("Pair type", "pair_type"), ("Weekday", "weekday"),
                       ("Year", "year"), ("Pair", "pair")]:
        factors.append({"name": label, "rows": table((t[key], t["r"], t["time"] >= split) for t in rows)})

    # every daily strategy (with and without the trend filter), older vs newer half and by year
    by_variant = []
    for vname, vfn in VARIANTS.items():
        rs = []
        for tf in detail_tfs:
            for pair in config.SYMBOLS:
                df = candles(pair, tf)
                if df is None or len(df) < 600:
                    continue
                for (i, _r, r_net, _s) in trades(df, vfn(df), pair):
                    rs.append((vname, r_net, df.index[i].isoformat() >= split, str(df.index[i].year)))
        if not rs:
            continue
        row = table((v, r, newer) for v, r, newer, _y in rs)[0]
        years = {}
        for _v, r, _n, y in rs:
            years.setdefault(y, []).append(r)
        row["years_positive"] = sum(1 for y in years.values() if sum(y) > 0)
        row["years"] = len(years)
        by_variant.append(row)
    by_variant.sort(key=lambda r: -r["avg_r"])

    # ideas that held up in both halves (at least 40 trades in each)
    robust = []
    for fct in factors[1:]:
        for r in fct["rows"]:
            if r.get("old_trades", 0) >= 40 and r.get("new_trades", 0) >= 40 and r["old_avg_r"] > 0 and r["new_avg_r"] > 0:
                robust.append({"factor": fct["name"], **r})
    return {"setup": name + (" + trend filter" if use_trend else ""), "timeframes": detail_tfs,
            "split": split, "daily_strategies": by_variant, "robust_ideas": robust,
            "trades": len(rows), "total_r": round(float(sum(t["r"] for t in rows)), 1),
            "note": "All available history, after spread. Rows with fewer than 30 trades are mostly luck.",
            "factors": factors}


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

    try:
        fac = factor_report()
    except Exception as e:
        print(f"[factor report error] {e}")
        fac = None
    report = {"generated": pd.Timestamp.now(tz="UTC").isoformat(), "seconds": round(time.time() - t0),
              "factors": fac,
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
    if fac:
        lines += ["", f"# What wins and what loses: {fac['setup']} ({', '.join(fac['timeframes'])})", "",
                  f"{fac['trades']} past trades, total {fac['total_r']:+.1f}R after spread. {fac['note']}", ""]
        lines += [f"Older half = trades before {fac['split'][:10]}, newer half = from then on.", "",
                  "## Every daily strategy", "", "| Strategy | Trades | Win % | Avg R | Older half | Newer half | Years positive |",
                  "|---|---|---|---|---|---|---|"]
        for r in fac["daily_strategies"]:
            lines.append(f"| {r['value']} | {r['trades']} | {r['win_rate']} | {r['avg_r']:+.3f} | "
                         f"{r.get('old_avg_r', 0):+.3f} | {r.get('new_avg_r', 0):+.3f} | {r['years_positive']}/{r['years']} |")
        lines += ["", "## Ideas that held up in both halves (40+ trades each)", ""]
        lines += [f"- {r['factor']}: {r['value']} (older {r['old_avg_r']:+.3f}R, newer {r['new_avg_r']:+.3f}R)"
                  for r in fac["robust_ideas"]] or ["- none"]
        lines.append("")
        for fct in fac["factors"]:
            lines += [f"## {fct['name']}", "", "| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |",
                      "|---|---|---|---|---|---|---|"]
            for r in fct["rows"]:
                lines.append(f"| {r['value']} | {r['trades']} | {r['win_rate']} | {r['avg_r']:+.3f} | "
                             f"{r.get('old_avg_r', float('nan')):+.3f} | {r.get('new_avg_r', float('nan')):+.3f} | {r['total_r']:+.1f} |")
            lines.append("")
    with open("backtest_report.md", "w") as f:
        f.write("\n".join(lines))
    print(f"done in {report['seconds']}s")


if __name__ == "__main__":
    main()
