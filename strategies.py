"""Indicators and signal strategies. Each strategy returns a Series: +1 buy, -1 sell, 0 nothing,
evaluated on the CLOSE of each bar (no look-ahead)."""
import numpy as np
import pandas as pd


# ---------------- indicators ----------------
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def atr(df, n=14):
    pc = df["Close"].shift()
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - pc).abs(), (df["Low"] - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def macd(close, f=12, s=26, sig=9):
    line = ema(close, f) - ema(close, s)
    return line, ema(line, sig)


def _cross_up(a, b):
    return (a > b) & (a.shift() <= b.shift())


def _cross_dn(a, b):
    return (a < b) & (a.shift() >= b.shift())


def _to_signal(buy, sell, index):
    out = pd.Series(0, index=index)
    out[buy.fillna(False)] = 1
    out[sell.fillna(False)] = -1
    return out


# ---------------- strategies ----------------
def ema_rsi(df):
    """Trend: EMA 9/21 crossover, in the direction of EMA 200, confirmed by RSI."""
    c = df["Close"]
    f, s, t, r = ema(c, 9), ema(c, 21), ema(c, 200), rsi(c)
    buy = _cross_up(f, s) & (c > t) & (r > 50) & (r < 70)
    sell = _cross_dn(f, s) & (c < t) & (r < 50) & (r > 30)
    return _to_signal(buy, sell, df.index)


def macd_trend(df):
    """Momentum: MACD crosses its signal line, filtered by EMA 200 trend."""
    c = df["Close"]
    line, sig = macd(c)
    t = ema(c, 200)
    buy = _cross_up(line, sig) & (line < 0) & (c > t)     # pullback buy in uptrend
    sell = _cross_dn(line, sig) & (line > 0) & (c < t)
    return _to_signal(buy, sell, df.index)


def rsi_reversion(df):
    """Mean reversion: RSI leaves oversold/overbought zone."""
    r = rsi(df["Close"])
    buy = (r > 30) & (r.shift() <= 30)
    sell = (r < 70) & (r.shift() >= 70)
    return _to_signal(buy, sell, df.index)


def bollinger(df):
    """Mean reversion: close re-enters the Bollinger band (20, 2) with RSI agreement."""
    c = df["Close"]
    mid = c.rolling(20).mean()
    sd = c.rolling(20).std()
    lo, hi = mid - 2 * sd, mid + 2 * sd
    r = rsi(c)
    buy = (c > lo) & (c.shift() <= lo.shift()) & (r < 45)
    sell = (c < hi) & (c.shift() >= hi.shift()) & (r > 55)
    return _to_signal(buy, sell, df.index)


def confluence(df):
    """Signal when 2+ strategies agree within the last 3 bars, and the newest one fires now."""
    sigs = [ema_rsi(df), macd_trend(df), rsi_reversion(df), bollinger(df)]
    recent = [s.rolling(3).sum().clip(-1, 1) for s in sigs]
    votes = sum(recent)
    fired_now = sum(s.abs() for s in sigs) > 0
    buy = (votes >= 2) & fired_now
    sell = (votes <= -2) & fired_now
    return _to_signal(buy, sell, df.index)


STRATEGIES = {
    "ema_rsi": ema_rsi,
    "macd": macd_trend,
    "rsi_reversion": rsi_reversion,
    "bollinger": bollinger,
    "confluence": confluence,
}
