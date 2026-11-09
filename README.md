# Forex Signal Bot + Android app

Scans **28 forex pairs + gold & silver** on **15m, 1h, 4h and 1d**, and sends BUY/SELL signals
with entry, stop loss and take profit to your phone. Price data is free (Yahoo Finance, no API key).

## Which strategy is "most profitable"?
No strategy wins on every pair or in every market. So the bot uses **auto mode**: for each
pair and timeframe it backtests 5 strategies on that pair's recent history and only uses the one
that did best. If none of them made money there (profit factor below 1.1), the bot stays silent on that pair.

| Strategy | Idea |
|---|---|
| `ema_rsi` | EMA 9/21 cross in the direction of EMA 200, RSI confirms |
| `macd` | MACD signal-line cross on a pullback, with the trend |
| `rsi_reversion` | RSI comes back from below 30 / above 70 |
| `bollinger` | Price re-enters the Bollinger Band |
| `confluence` | 2+ strategies agree within 3 candles |

Every signal: stop loss = 1.5 × ATR, take profit = 3 × ATR (risk:reward 1:2).
To see the results for yourself: `python backtest.py 1h` (or `4h`, `15m`, `1d`).

## Step 1: Get the app on your phone (2 min)
1. Install **ntfy** from the Play Store (free, no account needed).
2. Tap **+** and subscribe to a topic name only you know, e.g. `ameet-fx-7k29q`.

*(Or use Telegram instead: make a bot with @BotFather to get a token, and get your chat id from @userinfobot.)*

## Step 2: Run the bot for free, 24/7 (GitHub Actions)
1. Make a free GitHub account, create a **private** repository, and upload all these files
   (including the `.github/workflows/signals.yml` folder).
2. Repository → **Settings → Secrets and variables → Actions → New secret**:
   `NTFY_TOPIC` = your topic name (or `TELEGRAM_TOKEN` + `TELEGRAM_CHAT_ID`).
3. Go to **Actions** → enable workflows → **forex-signals → Run workflow** to test.

It then runs every 15 minutes, Sunday to Friday. (GitHub can sometimes start it a few minutes late.)

## Step 3: Get the FX Signals Android app (built by GitHub, no PC needed)
The `android/` folder is the app. GitHub builds it for you:
1. In your repository open **Actions → build-android-app**. It runs on its own when you upload
   the files. You can also tap **Run workflow**. Wait about 3–5 minutes for the green tick.
2. Open the repository's **Releases** (main page, right side) → newest release → download **FXSignals.apk**
   on your phone.
3. Open the file. Android will ask to allow installing from this source (Chrome or Files). Allow it, then tap **Install**.
   If Play Protect warns that it doesn't recognise the app, tap **More details → Install anyway**.
   This happens because you built the app yourself and it isn't from the Play Store.
4. Make a read-only token: GitHub → **Settings → Developer settings → Personal access tokens →
   Fine-grained tokens → Generate new token**. Under **Repository access**, pick only this repository.
   Set **Permissions → Contents** to **Read-only**.
5. Open the app → ⚙ → enter your GitHub username, the repository name and the token → **Save & load**.

The app lists every signal the bot has sent (newest first). You can filter by timeframe or search a pair,
and tap a price to copy it. Notifications still come through ntfy/Telegram. To change the app, edit the files in
`android/` (the screen is `android/app/src/main/assets/index.html`). GitHub then builds a new version that
installs over the old one.

> Keep the repository **private**. It holds the app's signing key (`android/app/debug.keystore`).

## Alternative: run it on the phone itself (Termux)
```
pkg install python git
pip install -r requirements.txt
export NTFY_TOPIC=ameet-fx-7k29q
python bot.py --test      # you should get a notification
python bot.py --loop      # scans every 5 minutes while Termux is open
```
The same commands work on a Windows/Mac/Linux PC.

## Settings
Edit `config.py`: pairs, timeframes, strategy (`auto` or one name), SL/TP size.

## Important
Signals come from past price patterns. A good backtest does not promise future profit, and
Yahoo prices can differ slightly from your broker's. Try it on a **demo account** first, risk at most
1–2% per trade, and always check the chart. This is not financial advice.
