"""Settings for the forex signal bot. Edit freely."""
import os

# ---------- Pairs (Yahoo Finance symbols, free, no API key) ----------
MAJORS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]
CROSSES = [
    "EURGBP", "EURJPY", "EURCHF", "EURAUD", "EURCAD", "EURNZD",
    "GBPJPY", "GBPCHF", "GBPAUD", "GBPCAD", "GBPNZD",
    "AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD",
    "CADJPY", "CADCHF", "CHFJPY", "NZDJPY", "NZDCHF", "NZDCAD",
]
FX_PAIRS = MAJORS + CROSSES                     # all 28 pairs
METALS = {"XAUUSD": "GC=F", "XAGUSD": "SI=F"}   # gold & silver (futures prices)

SYMBOLS = {p: f"{p}=X" for p in FX_PAIRS}
SYMBOLS.update(METALS)

# ---------- Timeframes ----------
# name: (yahoo interval, history to download, resample rule or None)
TIMEFRAMES = {
    "5m":  ("5m", "20d", None),
    "15m": ("15m", "30d", None),
    "1h":  ("60m", "180d", None),
    "4h":  ("60m", "360d", "4h"),
    "1d":  ("1d", "10y", None),
}

# Timeframes that can SEND new signals. The others above are only used to finish tracking
# trades that are still open on them. The strategy report showed that only the daily chart
# stayed profitable on unseen data after spread, so only 1d sends signals.
SIGNAL_TIMEFRAMES = ["1d"]

# A signal is only sent if its candle closed at most this long ago (GitHub can start runs late)
MAX_SIGNAL_AGE = {"5m": "12min", "15m": "30min", "1h": "90min", "4h": "5h", "1d": "3D"}

# ---------- Strategy ----------
# "auto" = each pair/timeframe uses the strategy that backtested best on its own history (tested worse).
# Or force one of: "ema_rsi", "macd", "rsi_reversion", "bollinger", "confluence"
STRATEGY = os.getenv("STRATEGY", "bollinger")      # best result in the strategy report (with TREND_FILTER)
MIN_TRADES_FOR_AUTO = 15     # a strategy needs at least this many backtest trades to be picked
MIN_PROFIT_FACTOR = 1.1      # in auto mode, stay silent on pairs where nothing beat this

# Only these strategies can be picked in auto mode (remove names to switch them off)
ALLOWED_STRATEGIES = ["ema_rsi", "macd", "rsi_reversion", "bollinger", "confluence"]

# Pick the strategy on the older 70% of the chart, and only use it if it ALSO made money
# on the newer 30% it never saw. Fewer signals, but the backtest numbers are honest.
PICK_ON_UNSEEN = True
UNSEEN_MIN_PROFIT_FACTOR = 1.0

# Only trade in the direction of the bigger trend (EMA 800 is about EMA 200 one timeframe up)
TREND_FILTER = True

# Skip a new signal if an open trade already bets on the same currency in the same direction
# (e.g. SELL USDJPY is open, so SELL GBPJPY is skipped: both are "buy yen").
ONE_TRADE_PER_CURRENCY = True

# Never have more than this many trades open at the same time (0 = no limit)
MAX_OPEN_TRADES = 6

# Risk: stop-loss and take-profit as multiples of ATR(14)
SL_ATR = 1.5
TP_ATR = 3.0                 # 1:2 risk/reward

# ---------- Logs (the app downloads these as a .zip) ----------
LOG_DIR = "logs"
SNAPSHOT_EVERY_MINUTES = 60  # how often market_snapshot.csv (every pair x timeframe) is rewritten
KEEP_SCAN_LOG_DAYS = 30

# ---------- Where signals go (Android) ----------
# ntfy: install the free "ntfy" app from Play Store, subscribe to your topic name.
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")             # e.g. "ameet-fx-9f3k2" (keep it hard to guess)
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")
# Telegram (optional): token from @BotFather, chat id from @userinfobot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

STATE_FILE = os.getenv("STATE_FILE", "sent_signals.json")
