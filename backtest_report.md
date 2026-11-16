# Strategy report

Generated 2026-11-16T17:31 UTC. Strategies were picked on the older 70% of each chart and tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from every trade. R = what you risked per trade (a loss is -1R, a win is +2R).

## 5m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 1811 | 36.7 | -0.207 | -375.1 |
| auto + trend filter | 851 | 36.0 | -0.224 | -190.2 |
| always macd | 1729 | 35.2 | -0.242 | -418.4 |
| always macd+trend | 1405 | 35.3 | -0.246 | -346.0 |
| always bollinger | 4270 | 34.5 | -0.265 | -1131.5 |
| auto (what the bot does now) | 1984 | 33.7 | -0.301 | -597.5 |
| always rsi_reversion | 2732 | 32.6 | -0.306 | -835.1 |
| always rsi_reversion+trend | 813 | 32.7 | -0.310 | -252.3 |
| always confluence | 2303 | 31.8 | -0.331 | -761.9 |
| always ema_rsi+trend | 2060 | 32.0 | -0.346 | -711.8 |
| always confluence+trend | 1139 | 31.8 | -0.347 | -395.4 |
| always ema_rsi | 2398 | 31.3 | -0.365 | -874.7 |

## 15m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always confluence+trend | 404 | 36.6 | -0.078 | -31.7 |
| auto + trend filter | 422 | 35.8 | -0.110 | -46.6 |
| always rsi_reversion+trend | 292 | 34.9 | -0.134 | -39.2 |
| always bollinger+trend | 609 | 34.5 | -0.144 | -87.8 |
| always ema_rsi+trend | 693 | 34.3 | -0.148 | -102.9 |
| always ema_rsi | 811 | 33.5 | -0.173 | -140.3 |
| always macd | 612 | 33.0 | -0.187 | -114.7 |
| always macd+trend | 515 | 33.0 | -0.189 | -97.3 |
| auto (what the bot does now) | 759 | 30.7 | -0.258 | -195.7 |
| always confluence | 853 | 30.0 | -0.268 | -228.9 |
| always bollinger | 1552 | 29.3 | -0.289 | -448.2 |
| always rsi_reversion | 1044 | 28.1 | -0.324 | -338.6 |

## 1h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger | 5198 | 33.2 | -0.095 | -491.9 |
| auto + trend filter | 827 | 33.3 | -0.099 | -82.0 |
| always bollinger+trend | 2121 | 33.1 | -0.102 | -215.5 |
| always macd+trend | 1581 | 32.7 | -0.119 | -187.8 |
| always macd | 1904 | 32.6 | -0.121 | -231.3 |
| always ema_rsi | 2594 | 32.5 | -0.124 | -320.5 |
| always ema_rsi+trend | 2215 | 32.3 | -0.129 | -286.3 |
| auto (what the bot does now) | 1116 | 31.7 | -0.141 | -156.8 |
| always confluence | 2560 | 31.4 | -0.151 | -386.2 |
| always confluence+trend | 1161 | 31.4 | -0.154 | -178.8 |
| always rsi_reversion | 3385 | 31.1 | -0.155 | -524.9 |
| always rsi_reversion+trend | 899 | 31.1 | -0.155 | -139.1 |

## 4h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always rsi_reversion | 997 | 34.2 | -0.023 | -22.9 |
| always bollinger | 1455 | 33.7 | -0.038 | -56.0 |
| always rsi_reversion+trend | 279 | 32.3 | -0.077 | -21.6 |
| always confluence | 736 | 32.2 | -0.083 | -61.1 |
| auto (what the bot does now) | 723 | 31.7 | -0.099 | -71.9 |
| always bollinger+trend | 564 | 30.3 | -0.140 | -78.7 |
| always ema_rsi | 694 | 30.3 | -0.143 | -99.2 |
| auto + trend filter | 368 | 29.9 | -0.147 | -54.2 |
| always macd | 488 | 30.1 | -0.147 | -71.6 |
| always ema_rsi+trend | 595 | 30.1 | -0.148 | -88.3 |
| always macd+trend | 389 | 29.8 | -0.156 | -60.5 |
| always confluence+trend | 334 | 29.0 | -0.176 | -58.9 |

## 1d

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 346 | 39.0 | +0.152 | +52.7 |
| always rsi_reversion+trend | 138 | 37.0 | +0.091 | +12.6 |
| always ema_rsi+trend | 346 | 35.5 | +0.047 | +16.4 |
| auto (what the bot does now) | 397 | 35.0 | +0.032 | +12.7 |
| always confluence+trend | 191 | 35.1 | +0.032 | +6.1 |
| always ema_rsi | 417 | 34.1 | +0.001 | +0.6 |
| always bollinger | 791 | 33.4 | -0.016 | -12.6 |
| always rsi_reversion | 479 | 33.2 | -0.021 | -10.1 |
| always macd+trend | 246 | 32.9 | -0.034 | -8.3 |
| auto + trend filter | 240 | 31.2 | -0.082 | -19.6 |
| always confluence | 388 | 30.9 | -0.090 | -35.0 |
| always macd | 289 | 30.8 | -0.096 | -27.8 |


# What wins and what loses: bollinger + trend filter (1d)

985 past trades, total -18.3R after spread. All available history, after spread. Rows with fewer than 30 trades are mostly luck.

## Timeframe (same setup, all pairs)

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| 1d | 985 | 33.3 | -0.019 | -18.3 |
| 4h | 1799 | 33.9 | -0.030 | -53.9 |
| 15m | 1965 | 36.8 | -0.082 | -160.2 |
| 1h | 7078 | 32.3 | -0.120 | -846.2 |
| 5m | 5782 | 35.2 | -0.271 | -1564.4 |

## Candle pattern

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| bearish engulfing | 3 | 66.7 | +0.983 | +2.9 |
| bullish engulfing | 9 | 55.6 | +0.650 | +5.9 |
| shooting star | 130 | 40.8 | +0.207 | +26.9 |
| inside bar | 20 | 40.0 | +0.180 | +3.6 |
| none | 5 | 40.0 | +0.165 | +0.8 |
| bearish candle | 11 | 36.4 | +0.063 | +0.7 |
| bullish candle | 15 | 33.3 | -0.023 | -0.3 |
| doji | 645 | 31.8 | -0.064 | -41.0 |
| hammer | 143 | 30.8 | -0.095 | -13.5 |
| bullish marubozu | 1 | 0.0 | -1.042 | -1.0 |
| bearish marubozu | 3 | 0.0 | -1.058 | -3.2 |

## Candle vs trade

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| against | 157 | 45.2 | +0.339 | +53.2 |
| neutral | 670 | 32.1 | -0.055 | -36.6 |
| confirms | 158 | 26.6 | -0.221 | -34.9 |

## Market direction

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| mixed | 472 | 33.7 | -0.007 | -3.3 |
| with both trends | 513 | 32.9 | -0.029 | -15.0 |

## RSI zone

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| oversold (<30) | 54 | 35.2 | +0.044 | +2.4 |
| weak (30-45) | 503 | 34.4 | +0.017 | +8.4 |
| strong (55-70) | 386 | 31.9 | -0.065 | -25.1 |
| overbought (>70) | 42 | 31.0 | -0.095 | -4.0 |

## Volatility

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| normal | 775 | 34.1 | +0.004 | +3.0 |
| low | 75 | 33.3 | -0.021 | -1.6 |
| high | 135 | 28.9 | -0.146 | -19.7 |

## Buy or sell

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| BUY | 557 | 34.5 | +0.019 | +10.7 |
| SELL | 428 | 31.8 | -0.068 | -29.0 |

## Pair type

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| gold / silver | 62 | 40.3 | +0.180 | +11.2 |
| major | 249 | 33.3 | -0.010 | -2.5 |
| cross | 674 | 32.6 | -0.040 | -27.0 |

## Weekday

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| Wednesday | 199 | 42.2 | +0.249 | +49.5 |
| Tuesday | 197 | 35.5 | +0.049 | +9.7 |
| Sunday | 101 | 32.7 | -0.037 | -3.7 |
| Monday | 222 | 30.2 | -0.112 | -24.9 |
| Thursday | 175 | 28.6 | -0.160 | -28.0 |
| Friday | 91 | 26.4 | -0.229 | -20.9 |

## Year

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| 2025 | 76 | 46.1 | +0.364 | +27.6 |
| 2023 | 112 | 43.8 | +0.297 | +33.2 |
| 2024 | 111 | 40.5 | +0.197 | +21.9 |
| 2022 | 101 | 32.7 | -0.034 | -3.4 |
| 2026 | 132 | 32.6 | -0.042 | -5.6 |
| 2019 | 98 | 31.6 | -0.073 | -7.1 |
| 2020 | 85 | 30.6 | -0.098 | -8.3 |
| 2017 | 26 | 26.9 | -0.207 | -5.4 |
| 2018 | 127 | 24.4 | -0.285 | -36.2 |
| 2021 | 117 | 23.9 | -0.300 | -35.1 |

## Pair

| Value | Trades | Win % | Avg R | Total R |
|---|---|---|---|---|
| GBPJPY | 37 | 45.9 | +0.369 | +13.6 |
| NZDUSD | 37 | 45.9 | +0.366 | +13.6 |
| GBPCAD | 27 | 44.4 | +0.321 | +8.7 |
| XAGUSD | 31 | 45.2 | +0.306 | +9.5 |
| AUDUSD | 37 | 43.2 | +0.285 | +10.6 |
| GBPNZD | 28 | 39.3 | +0.169 | +4.7 |
| CHFJPY | 29 | 37.9 | +0.123 | +3.6 |
| EURCAD | 33 | 36.4 | +0.074 | +2.4 |
| XAUUSD | 31 | 35.5 | +0.055 | +1.7 |
| EURGBP | 25 | 36.0 | +0.048 | +1.2 |
| AUDCHF | 31 | 35.5 | +0.036 | +1.1 |
| GBPUSD | 35 | 34.3 | +0.021 | +0.7 |
| EURJPY | 38 | 34.2 | +0.013 | +0.5 |
| AUDJPY | 39 | 33.3 | -0.017 | -0.6 |
| AUDCAD | 33 | 33.3 | -0.023 | -0.8 |
| NZDCHF | 33 | 33.3 | -0.031 | -1.0 |
| USDCAD | 34 | 32.4 | -0.039 | -1.3 |
| EURCHF | 28 | 32.1 | -0.066 | -1.9 |
| GBPAUD | 35 | 31.4 | -0.069 | -2.4 |
| CADJPY | 38 | 31.6 | -0.071 | -2.7 |
| EURNZD | 39 | 30.8 | -0.089 | -3.5 |
| USDJPY | 33 | 30.3 | -0.098 | -3.2 |
| GBPCHF | 28 | 28.6 | -0.164 | -4.6 |
| NZDCAD | 28 | 28.6 | -0.166 | -4.7 |
| CADCHF | 28 | 28.6 | -0.176 | -4.9 |
| NZDJPY | 29 | 27.6 | -0.191 | -5.5 |
| EURUSD | 40 | 25.0 | -0.260 | -10.4 |
| EURAUD | 39 | 23.1 | -0.321 | -12.5 |
| USDCHF | 33 | 21.2 | -0.376 | -12.4 |
| AUDNZD | 29 | 13.8 | -0.612 | -17.8 |
