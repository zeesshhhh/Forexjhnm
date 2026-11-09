"""Free price data from Yahoo Finance (no API key)."""
import pandas as pd

import config

INTERVAL_LEN = {"15m": "15min", "1h": "1h", "4h": "4h", "1d": "1D"}


def get_candles(pair, tf):
    """Closed candles only (the still-forming last candle is dropped). Returns None on failure."""
    import yfinance as yf

    interval, period, resample = config.TIMEFRAMES[tf]
    try:
        df = yf.Ticker(config.SYMBOLS[pair]).history(period=period, interval=interval, auto_adjust=False)
    except Exception as e:
        print(f"[data] {pair} {tf}: {e}")
        return None
    if df is None or df.empty:
        return None
    df = df[["Open", "High", "Low", "Close"]].dropna()
    df.index = pd.to_datetime(df.index, utc=True)
    if resample:
        df = df.resample(resample, origin="epoch").agg(
            {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    return drop_open_candle(df, tf)


def drop_open_candle(df, tf):
    if tf == "1d":
        today = pd.Timestamp.now(tz="UTC").normalize()
        return df[df.index.tz_convert("UTC").normalize() < today]
    now = pd.Timestamp.now(tz="UTC")
    return df[df.index + pd.Timedelta(INTERVAL_LEN[tf]) <= now]
