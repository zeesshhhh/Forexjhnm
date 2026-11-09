"""Backtester: replays each strategy over history with ATR stop-loss / take-profit.

Run it yourself to see which strategy is most profitable on which pair:
    python backtest.py              # all pairs, 1h
    python backtest.py 4h EURUSD    # one timeframe / pair
"""
import sys

import numpy as np
import pandas as pd

import config
from strategies import STRATEGIES, atr


def backtest(df, signal_fn, sl_atr=config.SL_ATR, tp_atr=config.TP_ATR):
    """Returns stats dict. Results in R (1R = amount risked). One trade at a time.
    If SL and TP are both touched in the same candle, it counts as a loss (conservative)."""
    sig = signal_fn(df).values
    a = atr(df).values
    hi, lo, cl = df["High"].values, df["Low"].values, df["Close"].values
    rr = tp_atr / sl_atr
    results, i, n = [], 210, len(df)          # skip warm-up for EMA 200
    while i < n - 1:
        side = sig[i]
        if side == 0 or np.isnan(a[i]):
            i += 1
            continue
        entry = cl[i]
        sl = entry - side * sl_atr * a[i]
        tp = entry + side * tp_atr * a[i]
        j, outcome = i + 1, None
        while j < n:
            hit_sl = lo[j] <= sl if side > 0 else hi[j] >= sl
            hit_tp = hi[j] >= tp if side > 0 else lo[j] <= tp
            if hit_sl:
                outcome = -1.0
                break
            if hit_tp:
                outcome = rr
                break
            j += 1
        if outcome is None:                  # still open at end of data: mark to market
            outcome = side * (cl[-1] - entry) / (sl_atr * a[i])
        results.append(outcome)
        i = j + 1
    r = np.array(results)
    wins, losses = r[r > 0].sum(), -r[r < 0].sum()
    return {
        "trades": len(r),
        "win_rate": float((r > 0).mean() * 100) if len(r) else 0.0,
        "total_R": float(r.sum()),
        "profit_factor": float(wins / losses) if losses > 0 else (float("inf") if wins > 0 else 0.0),
    }


def rank_strategies(df):
    """All strategies scored on this data, best first."""
    rows = [{"strategy": name, **backtest(df, fn)} for name, fn in STRATEGIES.items()]
    rows = [r for r in rows if r["trades"] >= config.MIN_TRADES_FOR_AUTO] or rows
    return sorted(rows, key=lambda r: (r["profit_factor"], r["total_R"]), reverse=True)


if __name__ == "__main__":
    from data import get_candles

    tf = sys.argv[1] if len(sys.argv) > 1 else "1h"
    pairs = sys.argv[2:] or list(config.SYMBOLS)
    summary = {k: [] for k in STRATEGIES}
    for p in pairs:
        df = get_candles(p, tf)
        if df is None:
            print(f"{p}: no data")
            continue
        print(f"\n=== {p} {tf} ({len(df)} candles) ===")
        for r in rank_strategies(df):
            summary[r["strategy"]].append(r["total_R"])
            print(f"  {r['strategy']:<14} trades {r['trades']:>4}  win {r['win_rate']:5.1f}%  "
                  f"PF {r['profit_factor']:5.2f}  total {r['total_R']:+7.1f}R")
    print(f"\n=== Overall ({tf}, sum of R across pairs) ===")
    for k, v in sorted(summary.items(), key=lambda kv: -sum(kv[1])):
        print(f"  {k:<14} {sum(v):+8.1f}R over {len(v)} pairs")
