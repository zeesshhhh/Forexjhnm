# Strategy report

Generated 2026-11-21T22:19 UTC. Strategies were picked on the older 70% of each chart and tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from every trade. R = what you risked per trade (a loss is -1R, a win is +2R).

## 5m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 1803 | 38.1 | -0.153 | -275.8 |
| always macd | 1774 | 35.0 | -0.236 | -419.3 |
| always macd+trend | 1451 | 35.1 | -0.236 | -342.5 |
| always bollinger | 4259 | 34.8 | -0.243 | -1034.7 |
| auto (what the bot does now) | 1693 | 34.2 | -0.265 | -448.3 |
| auto + trend filter | 889 | 34.0 | -0.269 | -239.1 |
| always rsi_reversion+trend | 800 | 32.1 | -0.316 | -252.8 |
| always confluence | 2359 | 31.8 | -0.316 | -744.9 |
| always confluence+trend | 1180 | 32.2 | -0.318 | -375.7 |
| always rsi_reversion | 2698 | 31.7 | -0.320 | -862.3 |
| always ema_rsi+trend | 2099 | 31.3 | -0.356 | -748.1 |
| always ema_rsi | 2417 | 30.6 | -0.376 | -907.7 |

## 15m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always confluence+trend | 385 | 37.9 | -0.034 | -13.0 |
| auto + trend filter | 375 | 37.9 | -0.053 | -19.9 |
| always rsi_reversion+trend | 264 | 37.1 | -0.055 | -14.6 |
| always bollinger+trend | 608 | 36.8 | -0.066 | -40.2 |
| always macd+trend | 538 | 35.7 | -0.100 | -54.0 |
| always macd | 629 | 35.6 | -0.102 | -64.1 |
| always ema_rsi+trend | 732 | 35.6 | -0.104 | -76.0 |
| always ema_rsi | 832 | 34.9 | -0.129 | -107.0 |
| always confluence | 822 | 30.7 | -0.243 | -199.6 |
| auto (what the bot does now) | 650 | 30.8 | -0.255 | -165.5 |
| always bollinger | 1549 | 29.9 | -0.264 | -409.2 |
| always rsi_reversion | 1020 | 27.8 | -0.324 | -330.5 |

## 1h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 2109 | 33.5 | -0.089 | -186.9 |
| always bollinger | 5219 | 33.1 | -0.099 | -517.4 |
| always ema_rsi | 2594 | 33.2 | -0.101 | -262.6 |
| always macd+trend | 1565 | 33.3 | -0.101 | -157.4 |
| always ema_rsi+trend | 2212 | 33.2 | -0.103 | -227.7 |
| always macd | 1887 | 33.2 | -0.104 | -196.8 |
| auto + trend filter | 889 | 32.8 | -0.111 | -98.8 |
| always confluence+trend | 1151 | 32.2 | -0.127 | -146.4 |
| always rsi_reversion+trend | 880 | 32.0 | -0.128 | -112.4 |
| auto (what the bot does now) | 1115 | 31.7 | -0.139 | -155.5 |
| always confluence | 2568 | 31.6 | -0.144 | -370.1 |
| always rsi_reversion | 3397 | 31.0 | -0.158 | -537.6 |

## 4h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| auto + trend filter | 369 | 34.1 | -0.021 | -7.7 |
| always rsi_reversion | 1034 | 33.7 | -0.036 | -37.2 |
| always bollinger | 1460 | 33.1 | -0.056 | -81.8 |
| always rsi_reversion+trend | 282 | 32.6 | -0.067 | -18.9 |
| always confluence | 747 | 32.1 | -0.085 | -63.4 |
| auto (what the bot does now) | 762 | 31.0 | -0.120 | -91.5 |
| always ema_rsi | 688 | 30.1 | -0.148 | -101.9 |
| always macd | 486 | 30.0 | -0.150 | -72.8 |
| always ema_rsi+trend | 588 | 29.8 | -0.158 | -92.7 |
| always macd+trend | 387 | 29.7 | -0.159 | -61.7 |
| always confluence+trend | 332 | 29.5 | -0.162 | -53.9 |
| always bollinger+trend | 553 | 29.5 | -0.165 | -91.2 |

## 1d

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 350 | 38.6 | +0.139 | +48.6 |
| always rsi_reversion+trend | 138 | 37.0 | +0.091 | +12.6 |
| always ema_rsi+trend | 344 | 35.7 | +0.053 | +18.4 |
| auto (what the bot does now) | 393 | 35.1 | +0.035 | +13.8 |
| always confluence+trend | 191 | 34.6 | +0.017 | +3.2 |
| always ema_rsi | 415 | 34.2 | +0.007 | +2.7 |
| always macd+trend | 246 | 33.3 | -0.021 | -5.2 |
| always bollinger | 796 | 33.2 | -0.022 | -17.7 |
| always rsi_reversion | 478 | 33.1 | -0.025 | -11.9 |
| auto + trend filter | 222 | 32.0 | -0.060 | -13.3 |
| always macd | 289 | 31.1 | -0.085 | -24.7 |
| always confluence | 388 | 30.7 | -0.098 | -37.9 |


# What wins and what loses: bollinger + trend filter (1d)

987 past trades, total -20.4R after spread. All available history, after spread. Rows with fewer than 30 trades are mostly luck.

Older half = trades before 2022-05-15, newer half = from then on.

## Every daily strategy

| Strategy | Trades | Win % | Avg R | Older half | Newer half | Years positive |
|---|---|---|---|---|---|---|
| macd+trend | candle against | 128 | 54.7 | +0.621 | +0.567 | +0.686 | 8/10 |
| macd | candle against | 145 | 54.5 | +0.615 | +0.557 | +0.687 | 10/10 |
| rsi_reversion+trend | candle against | 48 | 54.2 | +0.608 | +0.630 | +0.568 | 6/9 |
| confluence | candle against | 186 | 53.2 | +0.580 | +0.638 | +0.483 | 9/10 |
| rsi_reversion | candle against | 222 | 50.0 | +0.484 | +0.553 | +0.386 | 9/10 |
| confluence+trend | candle against | 85 | 47.1 | +0.393 | +0.394 | +0.392 | 7/9 |
| bollinger | candle against | 392 | 45.7 | +0.352 | +0.487 | +0.191 | 7/10 |
| bollinger+trend | candle against | 156 | 45.5 | +0.347 | +0.327 | +0.368 | 8/10 |
| ema_rsi | candle against | 194 | 43.3 | +0.281 | +0.224 | +0.340 | 8/10 |
| ema_rsi+trend | candle against | 166 | 42.8 | +0.265 | +0.194 | +0.346 | 8/10 |
| confluence | 1227 | 35.9 | +0.061 | +0.115 | -0.004 | 7/10 |
| confluence+trend | 560 | 35.9 | +0.058 | +0.012 | +0.105 | 5/10 |
| rsi_reversion | 1515 | 34.3 | +0.012 | +0.000 | +0.027 | 6/10 |
| bollinger | 2505 | 34.0 | +0.003 | -0.004 | +0.010 | 5/10 |
| ema_rsi | 1311 | 33.9 | -0.003 | -0.077 | +0.078 | 6/10 |
| rsi_reversion+trend | 358 | 33.8 | -0.003 | -0.103 | +0.092 | 4/10 |
| ema_rsi+trend | 1117 | 33.8 | -0.007 | -0.129 | +0.129 | 4/10 |
| macd+trend | 795 | 33.3 | -0.020 | -0.165 | +0.144 | 4/10 |
| bollinger+trend | 987 | 33.2 | -0.021 | -0.167 | +0.124 | 3/10 |
| macd | 938 | 33.2 | -0.025 | -0.112 | +0.074 | 2/10 |

## Ideas that held up in both halves (40+ trades each)

- Candle pattern: shooting star (older +0.248R, newer +0.194R)
- Candle vs trade: against (older +0.327R, newer +0.368R)
- Weekday: Wednesday (older +0.416R, newer +0.150R)

## Timeframe (same setup, all pairs)

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| 1d | 987 | 33.2 | -0.021 | +nan | +nan | -20.4 |
| 4h | 1792 | 33.7 | -0.036 | +nan | +nan | -64.6 |
| 15m | 1972 | 37.2 | -0.068 | +nan | +nan | -134.8 |
| 1h | 7062 | 32.5 | -0.115 | +nan | +nan | -810.0 |
| 5m | 5821 | 35.6 | -0.250 | +nan | +nan | -1452.6 |

## Candle pattern

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| bearish engulfing | 3 | 66.7 | +0.983 | -1.027 | +1.988 | +2.9 |
| bullish engulfing | 9 | 55.6 | +0.650 | +0.492 | +0.967 | +5.9 |
| shooting star | 131 | 41.2 | +0.220 | +0.248 | +0.194 | +28.9 |
| none | 5 | 40.0 | +0.165 | +0.455 | -0.029 | +0.8 |
| inside bar | 21 | 38.1 | +0.123 | -0.205 | +0.484 | +2.6 |
| bearish candle | 11 | 36.4 | +0.063 | +0.097 | -0.028 | +0.7 |
| bullish candle | 14 | 35.7 | +0.048 | -0.278 | +0.484 | +0.7 |
| doji | 647 | 31.8 | -0.062 | -0.250 | +0.114 | -40.1 |
| hammer | 142 | 29.6 | -0.130 | -0.219 | -0.032 | -18.5 |
| bullish marubozu | 1 | 0.0 | -1.042 | +nan | -1.042 | -1.0 |
| bearish marubozu | 3 | 0.0 | -1.058 | -1.080 | -1.014 | -3.2 |

## Candle vs trade

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| against | 156 | 45.5 | +0.347 | +0.327 | +0.368 | +54.2 |
| neutral | 673 | 32.1 | -0.054 | -0.244 | +0.124 | -36.7 |
| confirms | 158 | 25.9 | -0.240 | -0.322 | -0.142 | -37.9 |

## Market direction

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| mixed | 476 | 34.0 | +0.003 | -0.104 | +0.106 | +1.6 |
| with both trends | 511 | 32.5 | -0.043 | -0.224 | +0.140 | -22.0 |

## RSI zone

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| oversold (<30) | 54 | 35.2 | +0.044 | -0.484 | +0.286 | +2.4 |
| weak (30-45) | 510 | 34.5 | +0.020 | -0.163 | +0.200 | +10.2 |
| overbought (>70) | 41 | 31.7 | -0.072 | -0.107 | -0.027 | -3.0 |
| strong (55-70) | 382 | 31.4 | -0.078 | -0.152 | -0.001 | -30.0 |

## Volatility

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| normal | 776 | 33.9 | -0.001 | -0.098 | +0.109 | -1.0 |
| low | 77 | 33.8 | -0.008 | -0.305 | +0.134 | -0.6 |
| high | 134 | 29.1 | -0.140 | -0.662 | +0.181 | -18.7 |

## Buy or sell

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| BUY | 564 | 34.6 | +0.022 | -0.183 | +0.211 | +12.6 |
| SELL | 423 | 31.4 | -0.078 | -0.147 | -0.003 | -32.9 |

## Pair type

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| gold / silver | 63 | 39.7 | +0.162 | +0.078 | +0.266 | +10.2 |
| major | 250 | 34.0 | +0.010 | -0.174 | +0.185 | +2.5 |
| cross | 674 | 32.3 | -0.049 | -0.190 | +0.089 | -33.0 |

## Weekday

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| Wednesday | 203 | 42.9 | +0.268 | +0.416 | +0.150 | +54.4 |
| Tuesday | 198 | 35.4 | +0.044 | -0.115 | +0.216 | +8.7 |
| Sunday | 100 | 32.0 | -0.057 | -0.483 | +0.292 | -5.7 |
| Monday | 220 | 30.0 | -0.118 | -0.381 | +0.187 | -25.9 |
| Thursday | 172 | 28.5 | -0.162 | -0.301 | -0.017 | -27.9 |
| Friday | 94 | 25.5 | -0.255 | -0.308 | -0.204 | -24.0 |

## Year

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| 2025 | 76 | 46.1 | +0.364 | +nan | +0.364 | +27.6 |
| 2023 | 111 | 43.2 | +0.281 | +nan | +0.281 | +31.2 |
| 2024 | 111 | 40.5 | +0.197 | +nan | +0.197 | +21.9 |
| 2022 | 100 | 33.0 | -0.024 | +0.200 | -0.155 | -2.4 |
| 2020 | 84 | 32.1 | -0.051 | -0.051 | +nan | -4.3 |
| 2026 | 136 | 31.6 | -0.071 | +nan | -0.071 | -9.6 |
| 2019 | 96 | 31.2 | -0.085 | -0.085 | +nan | -8.1 |
| 2017 | 31 | 29.0 | -0.144 | -0.144 | +nan | -4.5 |
| 2021 | 119 | 24.4 | -0.287 | -0.287 | +nan | -34.1 |
| 2018 | 123 | 23.6 | -0.310 | -0.310 | +nan | -38.1 |

## Pair

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| GBPJPY | 37 | 45.9 | +0.369 | +0.224 | +0.492 | +13.6 |
| NZDUSD | 38 | 44.7 | +0.330 | +0.223 | +0.417 | +12.5 |
| XAGUSD | 31 | 45.2 | +0.306 | -0.000 | +0.558 | +9.5 |
| GBPCAD | 26 | 42.3 | +0.257 | -1.011 | +0.927 | +6.7 |
| AUDUSD | 38 | 42.1 | +0.251 | +0.274 | +0.223 | +9.5 |
| GBPNZD | 28 | 39.3 | +0.169 | -0.409 | +0.836 | +4.7 |
| CHFJPY | 29 | 37.9 | +0.123 | +0.342 | -0.010 | +3.6 |
| EURCAD | 33 | 36.4 | +0.074 | +0.396 | -0.268 | +2.4 |
| USDCAD | 34 | 35.3 | +0.049 | -0.219 | +0.389 | +1.7 |
| EURGBP | 25 | 36.0 | +0.048 | +0.130 | -0.041 | +1.2 |
| AUDCAD | 31 | 35.5 | +0.041 | +0.290 | -0.225 | +1.3 |
| XAUUSD | 32 | 34.4 | +0.022 | +0.130 | -0.186 | +0.7 |
| GBPUSD | 35 | 34.3 | +0.021 | -0.375 | +0.492 | +0.7 |
| USDJPY | 30 | 33.3 | -0.007 | -1.012 | +0.359 | -0.2 |
| EURJPY | 39 | 33.3 | -0.014 | -0.199 | +0.226 | -0.5 |
| NZDCHF | 33 | 33.3 | -0.031 | -0.426 | +0.576 | -1.0 |
| CADJPY | 37 | 32.4 | -0.045 | -0.306 | +0.297 | -1.7 |
| AUDCHF | 31 | 32.3 | -0.061 | -0.331 | +0.135 | -1.9 |
| EURCHF | 28 | 32.1 | -0.066 | -0.333 | +0.165 | -1.9 |
| EURNZD | 39 | 30.8 | -0.089 | -0.261 | +0.093 | -3.5 |
| AUDJPY | 40 | 30.0 | -0.116 | +0.031 | -0.264 | -4.7 |
| GBPAUD | 34 | 29.4 | -0.129 | -0.261 | -0.057 | -4.4 |
| GBPCHF | 28 | 28.6 | -0.164 | -0.092 | -0.226 | -4.6 |
| NZDCAD | 28 | 28.6 | -0.166 | -0.422 | +0.129 | -4.7 |
| CADCHF | 28 | 28.6 | -0.176 | -0.482 | +0.022 | -4.9 |
| NZDJPY | 30 | 26.7 | -0.219 | -0.221 | -0.216 | -6.6 |
| EURUSD | 40 | 25.0 | -0.260 | -0.260 | -0.260 | -10.4 |
| EURAUD | 39 | 23.1 | -0.321 | -0.382 | -0.264 | -12.5 |
| USDCHF | 35 | 22.9 | -0.327 | -0.345 | -0.307 | -11.4 |
| AUDNZD | 31 | 19.4 | -0.446 | -0.454 | -0.428 | -13.8 |
