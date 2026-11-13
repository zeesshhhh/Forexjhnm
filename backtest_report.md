# Strategy report

Generated 2026-11-13T15:45 UTC. Strategies were picked on the older 70% of each chart and tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from every trade. R = what you risked per trade (a loss is -1R, a win is +2R).

## 5m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| auto + trend filter | 892 | 35.8 | -0.231 | -206.0 |
| always bollinger+trend | 1840 | 35.7 | -0.237 | -436.8 |
| always macd | 1710 | 35.2 | -0.244 | -417.3 |
| always macd+trend | 1376 | 35.0 | -0.256 | -352.0 |
| always bollinger | 4301 | 34.7 | -0.261 | -1122.0 |
| auto (what the bot does now) | 1474 | 33.6 | -0.298 | -438.9 |
| always rsi_reversion | 2785 | 33.0 | -0.299 | -831.7 |
| always rsi_reversion+trend | 830 | 32.5 | -0.317 | -263.4 |
| always confluence | 2323 | 32.1 | -0.328 | -761.4 |
| always confluence+trend | 1139 | 32.0 | -0.341 | -388.0 |
| always ema_rsi+trend | 2029 | 32.1 | -0.344 | -697.2 |
| always ema_rsi | 2367 | 31.6 | -0.355 | -839.8 |

## 15m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| auto + trend filter | 404 | 35.9 | -0.112 | -45.4 |
| always confluence+trend | 415 | 35.4 | -0.114 | -47.4 |
| always rsi_reversion+trend | 298 | 35.2 | -0.127 | -37.7 |
| always bollinger+trend | 616 | 34.6 | -0.140 | -86.2 |
| always macd+trend | 529 | 32.9 | -0.193 | -102.0 |
| always macd | 632 | 32.8 | -0.196 | -123.9 |
| always ema_rsi+trend | 719 | 32.7 | -0.198 | -142.1 |
| auto (what the bot does now) | 744 | 32.1 | -0.219 | -162.6 |
| always ema_rsi | 835 | 31.8 | -0.223 | -185.8 |
| always bollinger | 1552 | 31.1 | -0.236 | -367.0 |
| always confluence | 865 | 30.5 | -0.255 | -220.7 |
| always rsi_reversion | 1051 | 29.7 | -0.278 | -292.4 |

## 1h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger | 5222 | 33.7 | -0.082 | -429.1 |
| always bollinger+trend | 2130 | 33.4 | -0.091 | -194.7 |
| always ema_rsi | 2617 | 32.8 | -0.115 | -300.6 |
| auto + trend filter | 886 | 32.7 | -0.116 | -103.1 |
| always macd+trend | 1585 | 32.7 | -0.119 | -189.1 |
| always macd | 1913 | 32.6 | -0.123 | -235.4 |
| always ema_rsi+trend | 2232 | 32.5 | -0.124 | -277.0 |
| auto (what the bot does now) | 1122 | 32.2 | -0.126 | -141.8 |
| always confluence | 2563 | 31.7 | -0.141 | -362.6 |
| always rsi_reversion | 3395 | 31.5 | -0.143 | -485.6 |
| always rsi_reversion+trend | 898 | 31.2 | -0.153 | -137.7 |
| always confluence+trend | 1158 | 31.3 | -0.154 | -178.7 |

## 4h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger | 1468 | 34.2 | -0.023 | -34.0 |
| always rsi_reversion | 998 | 34.1 | -0.027 | -27.3 |
| always confluence | 746 | 32.4 | -0.076 | -57.0 |
| always rsi_reversion+trend | 280 | 31.4 | -0.102 | -28.7 |
| auto (what the bot does now) | 723 | 31.5 | -0.104 | -75.1 |
| always ema_rsi+trend | 603 | 30.5 | -0.135 | -81.5 |
| always bollinger+trend | 575 | 30.4 | -0.136 | -78.1 |
| always ema_rsi | 699 | 30.1 | -0.149 | -104.3 |
| always confluence+trend | 347 | 30.0 | -0.149 | -51.7 |
| always macd | 493 | 29.8 | -0.156 | -76.8 |
| always macd+trend | 398 | 29.4 | -0.169 | -67.3 |
| auto + trend filter | 373 | 28.4 | -0.192 | -71.7 |

## 1d

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 346 | 39.3 | +0.161 | +55.6 |
| always rsi_reversion+trend | 138 | 37.0 | +0.091 | +12.6 |
| always ema_rsi+trend | 346 | 35.5 | +0.047 | +16.4 |
| always confluence+trend | 191 | 35.1 | +0.032 | +6.1 |
| auto (what the bot does now) | 410 | 34.6 | +0.021 | +8.5 |
| always ema_rsi | 417 | 34.1 | +0.001 | +0.6 |
| always bollinger | 790 | 33.4 | -0.015 | -11.5 |
| always rsi_reversion | 479 | 33.2 | -0.021 | -10.1 |
| always macd+trend | 247 | 32.8 | -0.038 | -9.4 |
| auto + trend filter | 231 | 31.6 | -0.071 | -16.4 |
| always confluence | 388 | 30.9 | -0.090 | -35.0 |
| always macd | 291 | 30.9 | -0.092 | -26.9 |
