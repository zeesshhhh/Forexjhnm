# Strategy report

Generated 2026-11-17T16:43 UTC. Strategies were picked on the older 70% of each chart and tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from every trade. R = what you risked per trade (a loss is -1R, a win is +2R).

## 5m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 1827 | 37.8 | -0.172 | -314.3 |
| auto + trend filter | 862 | 36.4 | -0.208 | -179.7 |
| always macd | 1788 | 35.8 | -0.225 | -402.2 |
| always macd+trend | 1453 | 35.9 | -0.228 | -331.1 |
| always bollinger | 4249 | 35.1 | -0.249 | -1056.3 |
| always rsi_reversion | 2669 | 33.5 | -0.281 | -751.3 |
| always confluence | 2292 | 32.8 | -0.301 | -690.3 |
| always rsi_reversion+trend | 794 | 32.5 | -0.315 | -250.3 |
| always confluence+trend | 1160 | 32.8 | -0.316 | -366.2 |
| auto (what the bot does now) | 1824 | 32.8 | -0.324 | -590.7 |
| always ema_rsi+trend | 2094 | 31.9 | -0.349 | -731.3 |
| always ema_rsi | 2429 | 31.3 | -0.363 | -881.4 |

## 15m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always confluence+trend | 403 | 37.0 | -0.072 | -29.0 |
| auto + trend filter | 422 | 35.8 | -0.112 | -47.3 |
| always rsi_reversion+trend | 271 | 35.4 | -0.121 | -32.9 |
| always bollinger+trend | 602 | 35.0 | -0.127 | -76.4 |
| always ema_rsi+trend | 707 | 34.5 | -0.146 | -102.9 |
| always macd | 635 | 33.6 | -0.172 | -109.4 |
| always ema_rsi | 818 | 33.5 | -0.176 | -143.7 |
| always macd+trend | 540 | 33.1 | -0.185 | -99.8 |
| always confluence | 845 | 30.6 | -0.250 | -211.2 |
| auto (what the bot does now) | 803 | 30.3 | -0.272 | -218.2 |
| always bollinger | 1522 | 29.8 | -0.272 | -413.6 |
| always rsi_reversion | 1007 | 28.5 | -0.313 | -315.2 |

## 1h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 2107 | 33.5 | -0.089 | -187.7 |
| auto + trend filter | 849 | 33.3 | -0.091 | -77.6 |
| always bollinger | 5238 | 33.3 | -0.094 | -494.3 |
| always ema_rsi | 2602 | 32.9 | -0.109 | -283.9 |
| always macd+trend | 1576 | 32.7 | -0.117 | -185.0 |
| always ema_rsi+trend | 2214 | 32.7 | -0.118 | -260.3 |
| always macd | 1905 | 32.5 | -0.124 | -235.3 |
| auto (what the bot does now) | 1099 | 32.1 | -0.130 | -142.6 |
| always rsi_reversion+trend | 883 | 31.3 | -0.152 | -133.8 |
| always confluence | 2565 | 31.3 | -0.152 | -388.8 |
| always confluence+trend | 1142 | 31.4 | -0.152 | -173.1 |
| always rsi_reversion | 3414 | 31.1 | -0.158 | -539.8 |

## 4h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always rsi_reversion | 1010 | 33.9 | -0.033 | -33.4 |
| always bollinger | 1469 | 33.8 | -0.036 | -53.1 |
| always confluence | 749 | 32.2 | -0.084 | -62.9 |
| always rsi_reversion+trend | 283 | 31.8 | -0.092 | -25.9 |
| auto (what the bot does now) | 763 | 31.5 | -0.106 | -81.1 |
| always ema_rsi+trend | 597 | 30.7 | -0.131 | -78.1 |
| auto + trend filter | 387 | 30.2 | -0.138 | -53.5 |
| always ema_rsi | 693 | 30.3 | -0.141 | -97.9 |
| always macd | 494 | 30.2 | -0.146 | -71.9 |
| always bollinger+trend | 565 | 30.1 | -0.147 | -82.8 |
| always confluence+trend | 347 | 30.0 | -0.148 | -51.5 |
| always macd+trend | 399 | 29.8 | -0.156 | -62.4 |

## 1d

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 348 | 38.8 | +0.146 | +50.7 |
| always rsi_reversion+trend | 139 | 36.7 | +0.083 | +11.6 |
| always ema_rsi+trend | 344 | 35.5 | +0.045 | +15.4 |
| auto (what the bot does now) | 397 | 35.0 | +0.032 | +12.7 |
| always confluence+trend | 191 | 34.6 | +0.017 | +3.2 |
| always ema_rsi | 415 | 34.0 | -0.001 | -0.3 |
| always bollinger | 793 | 33.3 | -0.018 | -14.6 |
| always rsi_reversion | 480 | 33.1 | -0.023 | -11.1 |
| always macd+trend | 246 | 32.9 | -0.034 | -8.3 |
| auto + trend filter | 237 | 31.6 | -0.070 | -16.5 |
| always macd | 289 | 30.8 | -0.096 | -27.8 |
| always confluence | 388 | 30.7 | -0.098 | -38.0 |


# What wins and what loses: bollinger + trend filter (1d)

988 past trades, total -18.4R after spread. All available history, after spread. Rows with fewer than 30 trades are mostly luck.

Older half = trades before 2022-05-15, newer half = from then on.

## Every daily strategy

| Strategy | Trades | Win % | Avg R | Older half | Newer half | Years positive |
|---|---|---|---|---|---|---|
| confluence | 1226 | 36.1 | +0.064 | +0.117 | -0.000 | 7/10 |
| confluence+trend | 564 | 35.8 | +0.055 | +0.008 | +0.105 | 5/10 |
| rsi_reversion | 1513 | 34.4 | +0.014 | +0.000 | +0.030 | 6/10 |
| bollinger | 2501 | 34.1 | +0.006 | -0.001 | +0.013 | 5/10 |
| ema_rsi+trend | 1119 | 33.9 | -0.003 | -0.122 | +0.129 | 5/10 |
| ema_rsi | 1310 | 33.8 | -0.005 | -0.076 | +0.075 | 6/10 |
| macd+trend | 801 | 33.6 | -0.012 | -0.144 | +0.139 | 4/10 |
| bollinger+trend | 988 | 33.3 | -0.019 | -0.170 | +0.132 | 3/10 |
| macd | 940 | 33.2 | -0.024 | -0.106 | +0.070 | 3/10 |
| rsi_reversion+trend | 363 | 33.1 | -0.025 | -0.146 | +0.092 | 4/10 |

## Ideas that held up in both halves (40+ trades each)

- Candle pattern: shooting star (older +0.221R, newer +0.194R)
- Candle vs trade: against (older +0.326R, newer +0.368R)
- Weekday: Wednesday (older +0.399R, newer +0.171R)

## Timeframe (same setup, all pairs)

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| 1d | 988 | 33.3 | -0.019 | +nan | +nan | -18.4 |
| 4h | 1808 | 34.0 | -0.027 | +nan | +nan | -48.5 |
| 15m | 1954 | 36.4 | -0.092 | +nan | +nan | -180.1 |
| 1h | 7095 | 32.4 | -0.118 | +nan | +nan | -838.4 |
| 5m | 5788 | 35.5 | -0.259 | +nan | +nan | -1498.9 |

## Candle pattern

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| bearish engulfing | 3 | 66.7 | +0.983 | -1.027 | +1.988 | +2.9 |
| bullish engulfing | 9 | 55.6 | +0.650 | +0.492 | +0.967 | +5.9 |
| shooting star | 130 | 40.8 | +0.207 | +0.221 | +0.194 | +26.9 |
| none | 5 | 40.0 | +0.165 | +0.455 | -0.029 | +0.8 |
| inside bar | 21 | 38.1 | +0.123 | -0.205 | +0.484 | +2.6 |
| bearish candle | 11 | 36.4 | +0.063 | +0.097 | -0.028 | +0.7 |
| bullish candle | 14 | 35.7 | +0.048 | -0.278 | +0.484 | +0.7 |
| doji | 647 | 32.0 | -0.057 | -0.250 | +0.123 | -37.1 |
| hammer | 144 | 29.9 | -0.122 | -0.211 | -0.017 | -17.6 |
| bullish marubozu | 1 | 0.0 | -1.042 | +nan | -1.042 | -1.0 |
| bearish marubozu | 3 | 0.0 | -1.058 | -1.080 | -1.014 | -3.2 |

## Candle vs trade

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| against | 156 | 45.5 | +0.347 | +0.326 | +0.368 | +54.2 |
| neutral | 673 | 32.2 | -0.050 | -0.244 | +0.132 | -33.6 |
| confirms | 159 | 25.8 | -0.245 | -0.338 | -0.130 | -38.9 |

## Market direction

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| mixed | 475 | 33.9 | -0.001 | -0.129 | +0.123 | -0.3 |
| with both trends | 513 | 32.7 | -0.035 | -0.207 | +0.140 | -18.0 |

## RSI zone

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| oversold (<30) | 55 | 36.4 | +0.079 | -0.346 | +0.286 | +4.3 |
| weak (30-45) | 509 | 34.4 | +0.016 | -0.178 | +0.209 | +8.3 |
| overbought (>70) | 40 | 32.5 | -0.049 | -0.066 | -0.027 | -1.9 |
| strong (55-70) | 384 | 31.5 | -0.076 | -0.156 | +0.010 | -29.0 |

## Volatility

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| normal | 776 | 34.0 | +0.003 | -0.100 | +0.120 | +2.0 |
| low | 77 | 33.8 | -0.008 | -0.304 | +0.134 | -0.6 |
| high | 135 | 28.9 | -0.146 | -0.669 | +0.181 | -19.7 |

## Buy or sell

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| BUY | 564 | 34.6 | +0.022 | -0.189 | +0.219 | +12.6 |
| SELL | 424 | 31.6 | -0.073 | -0.147 | +0.007 | -31.0 |

## Pair type

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| gold / silver | 63 | 39.7 | +0.162 | +0.078 | +0.266 | +10.2 |
| major | 250 | 33.6 | -0.002 | -0.199 | +0.185 | -0.5 |
| cross | 675 | 32.6 | -0.041 | -0.186 | +0.101 | -28.0 |

## Weekday

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| Wednesday | 200 | 43.0 | +0.272 | +0.399 | +0.171 | +54.5 |
| Tuesday | 197 | 35.0 | +0.034 | -0.136 | +0.216 | +6.7 |
| Sunday | 100 | 33.0 | -0.027 | -0.416 | +0.292 | -2.7 |
| Monday | 223 | 30.0 | -0.116 | -0.392 | +0.205 | -25.9 |
| Thursday | 175 | 28.6 | -0.160 | -0.292 | -0.017 | -28.0 |
| Friday | 93 | 25.8 | -0.247 | -0.292 | -0.204 | -22.9 |

## Year

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| 2025 | 76 | 46.1 | +0.364 | +nan | +0.364 | +27.6 |
| 2023 | 112 | 43.8 | +0.297 | +nan | +0.297 | +33.2 |
| 2024 | 111 | 40.5 | +0.197 | +nan | +0.197 | +21.9 |
| 2022 | 100 | 33.0 | -0.024 | +0.200 | -0.155 | -2.4 |
| 2019 | 99 | 32.3 | -0.052 | -0.052 | +nan | -5.1 |
| 2026 | 134 | 32.1 | -0.057 | +nan | -0.057 | -7.6 |
| 2020 | 85 | 31.8 | -0.063 | -0.063 | +nan | -5.3 |
| 2017 | 27 | 25.9 | -0.237 | -0.237 | +nan | -6.4 |
| 2021 | 117 | 23.9 | -0.300 | -0.300 | +nan | -35.1 |
| 2018 | 127 | 23.6 | -0.309 | -0.309 | +nan | -39.2 |

## Pair

| Value | Trades | Win % | Avg R | Older half | Newer half | Total R |
|---|---|---|---|---|---|---|
| GBPJPY | 37 | 45.9 | +0.369 | +0.224 | +0.492 | +13.6 |
| NZDUSD | 37 | 45.9 | +0.366 | +0.300 | +0.417 | +13.6 |
| GBPCAD | 27 | 44.4 | +0.321 | -1.011 | +0.986 | +8.7 |
| XAGUSD | 31 | 45.2 | +0.306 | -0.000 | +0.558 | +9.5 |
| AUDUSD | 36 | 41.7 | +0.238 | +0.251 | +0.223 | +8.6 |
| GBPNZD | 28 | 39.3 | +0.169 | -0.409 | +0.836 | +4.7 |
| CHFJPY | 29 | 37.9 | +0.123 | +0.342 | -0.010 | +3.6 |
| EURCAD | 33 | 36.4 | +0.074 | +0.396 | -0.268 | +2.4 |
| EURGBP | 25 | 36.0 | +0.048 | +0.130 | -0.041 | +1.2 |
| AUDCAD | 31 | 35.5 | +0.041 | +0.212 | -0.167 | +1.3 |
| XAUUSD | 32 | 34.4 | +0.022 | +0.130 | -0.186 | +0.7 |
| GBPUSD | 35 | 34.3 | +0.021 | -0.375 | +0.492 | +0.7 |
| USDCAD | 35 | 34.3 | +0.019 | -0.259 | +0.389 | +0.7 |
| EURJPY | 38 | 34.2 | +0.013 | -0.159 | +0.226 | +0.5 |
| AUDCHF | 32 | 34.4 | +0.003 | -0.166 | +0.135 | +0.1 |
| NZDCHF | 33 | 33.3 | -0.031 | -0.426 | +0.576 | -1.0 |
| EURCHF | 28 | 32.1 | -0.066 | -0.333 | +0.165 | -1.9 |
| GBPAUD | 35 | 31.4 | -0.069 | -0.088 | -0.057 | -2.4 |
| CADJPY | 38 | 31.6 | -0.071 | -0.338 | +0.297 | -2.7 |
| EURNZD | 39 | 30.8 | -0.089 | -0.261 | +0.093 | -3.5 |
| AUDJPY | 39 | 30.8 | -0.093 | +0.031 | -0.224 | -3.6 |
| USDJPY | 33 | 30.3 | -0.098 | -1.012 | +0.359 | -3.2 |
| GBPCHF | 28 | 28.6 | -0.164 | -0.092 | -0.226 | -4.6 |
| NZDCAD | 28 | 28.6 | -0.166 | -0.422 | +0.129 | -4.7 |
| CADCHF | 28 | 28.6 | -0.176 | -0.482 | +0.022 | -4.9 |
| NZDJPY | 29 | 27.6 | -0.191 | -0.164 | -0.216 | -5.5 |
| EURUSD | 41 | 26.8 | -0.205 | -0.153 | -0.260 | -8.4 |
| EURAUD | 39 | 23.1 | -0.321 | -0.382 | -0.264 | -12.5 |
| USDCHF | 33 | 21.2 | -0.376 | -0.450 | -0.307 | -12.4 |
| AUDNZD | 31 | 16.1 | -0.542 | -0.597 | -0.428 | -16.8 |
