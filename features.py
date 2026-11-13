"""Extra facts saved with every signal, so the logs can show what wins and what loses:
candle pattern, market direction, RSI zone, volatility, weekday and (optional) high-impact news.

News comes from FinanceCalendar.com (free key, licensed for this use). Set the NEWS_API_KEY secret
to switch it on. Without a key the news fields say "not set up".
"""
import json
import os

import pandas as pd
import requests

from strategies import atr, ema, rsi

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_CACHE = os.path.join("logs", "news_cache.json")
COUNTRY_TO_CCY = {"US": "USD", "EU": "EUR", "DE": "EUR", "GB": "GBP", "JP": "JPY",
                  "CA": "CAD", "AU": "AUD", "CH": "CHF", "NZ": "NZD"}


# ---------------- candles ----------------
def pattern_from(o, h, l, c, po, ph, pl, pc):
    """Candle pattern from the last candle (o, h, l, c) and the one before it (po, ph, pl, pc)."""
    rng = h - l
    if rng <= 0:
        return "none"
    body = abs(c - o)
    upper = h - max(o, c)
    lower = min(o, c) - l
    if c > o and pc < po and c >= po and o <= pc:
        return "bullish engulfing"
    if c < o and pc > po and o >= pc and c <= po:
        return "bearish engulfing"
    if lower >= 2 * body and upper <= max(body, 0.1 * rng):
        return "hammer"                      # long lower wick (bullish pin bar)
    if upper >= 2 * body and lower <= max(body, 0.1 * rng):
        return "shooting star"               # long upper wick (bearish pin bar)
    if body <= 0.1 * rng:
        return "doji"
    if h < ph and l > pl:
        return "inside bar"
    if body >= 0.85 * rng:
        return "bullish marubozu" if c > o else "bearish marubozu"
    return "bullish candle" if c > o else "bearish candle"


def candle_pattern(df, i=-1):
    """Name of the pattern on candle i (default: the last closed candle)."""
    n = len(df)
    i = i % n
    if i < 1:
        return "none"
    O, H, L, C = df["Open"].values, df["High"].values, df["Low"].values, df["Close"].values
    return pattern_from(O[i], H[i], L[i], C[i], O[i - 1], H[i - 1], L[i - 1], C[i - 1])


BULLISH = {"bullish engulfing", "hammer", "bullish marubozu", "bullish candle"}
BEARISH = {"bearish engulfing", "shooting star", "bearish marubozu", "bearish candle"}


def pattern_vs_trade(pattern, side):
    if pattern in BULLISH:
        return "confirms" if side == "BUY" else "against"
    if pattern in BEARISH:
        return "confirms" if side == "SELL" else "against"
    return "neutral"


# ---------------- indicators as plain words ----------------
def rsi_zone(v):
    if v < 30:
        return "oversold (<30)"
    if v < 45:
        return "weak (30-45)"
    if v <= 55:
        return "neutral (45-55)"
    if v <= 70:
        return "strong (55-70)"
    return "overbought (>70)"


def vol_label(ratio):
    """ATR now compared with its 100-candle average."""
    if not ratio == ratio:          # NaN
        return "normal"
    if ratio < 0.8:
        return "low"
    if ratio > 1.25:
        return "high"
    return "normal"


def volatility(df):
    a = atr(df)
    return vol_label(float(a.iloc[-1] / a.rolling(100).mean().iloc[-1])) if len(df) > 120 else "normal"


def direction_label(up, up_big, side):
    want_up = side == "BUY"
    agree = int(bool(up) == want_up) + int(bool(up_big) == want_up)     # plain ints (numpy bools would OR)
    return {2: "with both trends", 1: "mixed", 0: "against both trends"}[agree]


def direction(df, side):
    """Market direction on this chart (EMA 200) and one timeframe up (about EMA 800)."""
    c = df["Close"]
    up = bool(c.iloc[-1] > ema(c, 200).iloc[-1])
    up_big = bool(c.iloc[-1] > ema(c, 800).iloc[-1])
    return ("up" if up else "down"), ("up" if up_big else "down"), direction_label(up, up_big, side)


def session(ts):
    h = ts.tz_convert("UTC").hour
    if h < 7:
        return "Asia"
    if h < 12:
        return "London"
    if h < 16:
        return "London + New York"
    if h < 21:
        return "New York"
    return "late / Sydney"


# ---------------- news (optional) ----------------
def _load_cache():
    try:
        with open(NEWS_CACHE) as f:
            return json.load(f)
    except Exception:
        return {"fetched_utc_day": "", "events": []}


def refresh_news():
    """At most once per UTC day (2 requests): high-impact events for the next 7 days. Returns events."""
    cache = _load_cache()
    if not NEWS_API_KEY:
        return None
    today = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d")
    if cache.get("fetched_utc_day") == today:
        return cache["events"]
    events = {e["id"]: e for e in cache.get("events", []) if e.get("id")}
    ok = False
    for countries in ("US,EU,GB,JP", "CA,AU,CH,NZ,DE"):
        try:
            r = requests.get("https://www.financecalendar.com/wp-json/fc/v1/today",
                             params={"country": countries, "impact": "high"},
                             headers={"X-API-Key": NEWS_API_KEY, "User-Agent": "fx-signal-bot"}, timeout=20)
            if r.status_code != 200:
                print(f"[news] HTTP {r.status_code} for {countries}")
                continue
            for e in r.json().get("events", []):
                ccy = COUNTRY_TO_CCY.get(e.get("country", ""))
                if not ccy or not e.get("time_utc"):
                    continue
                key = e.get("id") or f"{e.get('name')}|{e.get('time_utc')}"
                events[key] = {"id": key, "name": e.get("name", ""), "currency": ccy, "time_utc": e["time_utc"]}
            ok = True
        except Exception as ex:
            print(f"[news] {ex}")
    cutoff = (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=14)).isoformat()
    kept = sorted((e for e in events.values() if e["time_utc"] >= cutoff), key=lambda e: e["time_utc"])
    if ok:
        os.makedirs(os.path.dirname(NEWS_CACHE), exist_ok=True)
        with open(NEWS_CACHE, "w") as f:
            json.dump({"fetched_utc_day": today, "source": "FinanceCalendar.com (https://www.financecalendar.com)",
                       "events": kept}, f, indent=1)
    return kept


def news_near(pair, when, events):
    """High-impact events for this pair's currencies in the 24 hours before and after `when`."""
    if events is None:
        return {"news_next_24h": "not set up", "news_prev_24h": "not set up", "news_titles": ""}
    ccys = {pair[:3], pair[3:]} - {"XAU", "XAG"}
    t = pd.Timestamp(when)
    nxt, prv = [], []
    for e in events:
        if e["currency"] not in ccys:
            continue
        et = pd.Timestamp(e["time_utc"])
        if t <= et <= t + pd.Timedelta(hours=24):
            nxt.append(e)
        elif t - pd.Timedelta(hours=24) <= et < t:
            prv.append(e)
    return {"news_next_24h": len(nxt), "news_prev_24h": len(prv),
            "news_titles": "; ".join(f"{e['currency']} {e['name']}" for e in nxt[:4])}


# ---------------- everything for one signal ----------------
def describe(df, pair, tf, side, events, signal_time):
    p = candle_pattern(df)
    trend, big, agree = direction(df, side)
    f = {
        "pattern": p,
        "pattern_vs_trade": pattern_vs_trade(p, side),
        "trend": trend,
        "bigger_trend": big,
        "direction_vs_trade": agree,
        "rsi_zone": rsi_zone(float(rsi(df["Close"]).iloc[-1])),
        "volatility": volatility(df),
        "weekday": df.index[-1].day_name(),                 # day of the signal candle
        "session": "daily candle" if tf == "1d" else session(pd.Timestamp(signal_time)),
    }
    f.update(news_near(pair, signal_time, events))
    return f
