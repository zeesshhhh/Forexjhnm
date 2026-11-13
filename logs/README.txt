Log files kept in the repository (the Android app downloads them as a .zip).

logs/trades.csv            every signal: pair, timeframe, strategy, indicators at the signal, result
logs/market_snapshot.csv   every pair x timeframe: price, indicators, chosen strategy, why there was / wasn't a signal
logs/scans/YYYY-MM-DD.csv  one line per scan: time, duration, data problems, new signals, closed trades
logs/last_scan.txt         full printed output of the latest scan (errors show up here)
