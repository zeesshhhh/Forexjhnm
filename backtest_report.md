# Strategy report

Generated 2026-11-21T22:32 UTC. Strategies were picked on the older 70% of each chart and tested on the newer 30% they had never seen. **After spread** subtracts a typical broker spread from every trade. R = what you risked per trade (a loss is -1R, a win is +2R).

## 5m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 1799 | 38.3 | -0.149 | -267.2 |
| always macd | 1779 | 35.1 | -0.233 | -413.9 |
| always macd+trend | 1455 | 35.3 | -0.233 | -338.4 |
| always bollinger | 4252 | 34.7 | -0.246 | -1044.6 |
| auto + trend filter | 861 | 33.7 | -0.281 | -241.9 |
| auto (what the bot does now) | 1612 | 33.7 | -0.282 | -454.4 |
| always confluence | 2353 | 32.0 | -0.310 | -729.9 |
| always rsi_reversion | 2703 | 31.8 | -0.318 | -858.9 |
| always confluence+trend | 1181 | 32.1 | -0.320 | -378.2 |
| always rsi_reversion+trend | 800 | 31.9 | -0.323 | -258.2 |
| always ema_rsi+trend | 2102 | 31.4 | -0.351 | -738.6 |
| always ema_rsi | 2414 | 30.7 | -0.371 | -896.5 |

## 15m

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always confluence+trend | 388 | 37.6 | -0.043 | -16.8 |
| auto + trend filter | 373 | 37.5 | -0.063 | -23.6 |
| always rsi_reversion+trend | 265 | 36.6 | -0.072 | -19.1 |
| always bollinger+trend | 609 | 36.6 | -0.073 | -44.2 |
| always macd+trend | 539 | 36.0 | -0.091 | -49.2 |
| always macd | 630 | 35.9 | -0.094 | -59.4 |
| always ema_rsi+trend | 732 | 35.7 | -0.104 | -76.3 |
| always ema_rsi | 828 | 35.0 | -0.124 | -102.5 |
| always confluence | 823 | 30.4 | -0.252 | -207.1 |
| auto (what the bot does now) | 675 | 30.8 | -0.257 | -173.4 |
| always bollinger | 1548 | 29.9 | -0.264 | -408.0 |
| always rsi_reversion | 1024 | 27.8 | -0.325 | -332.3 |

## 1h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always bollinger+trend | 2113 | 33.7 | -0.082 | -173.5 |
| always bollinger | 5237 | 33.4 | -0.091 | -474.7 |
| always ema_rsi | 2611 | 33.3 | -0.097 | -254.1 |
| auto + trend filter | 984 | 33.0 | -0.106 | -104.2 |
| always ema_rsi+trend | 2221 | 33.0 | -0.107 | -237.7 |
| always macd+trend | 1576 | 33.0 | -0.110 | -172.9 |
| auto (what the bot does now) | 1034 | 32.5 | -0.114 | -117.6 |
| always macd | 1903 | 32.8 | -0.116 | -221.2 |
| always rsi_reversion+trend | 882 | 31.7 | -0.137 | -120.5 |
| always confluence+trend | 1150 | 31.8 | -0.140 | -161.1 |
| always confluence | 2563 | 31.6 | -0.144 | -368.6 |
| always rsi_reversion | 3401 | 31.2 | -0.154 | -524.3 |

## 4h

| Method | Trades | Win % | R per trade (after spread) | Total R (after spread) |
|---|---|---|---|---|
| always rsi_reversion | 1023 | 33.9 | -0.031 | -31.8 |
| always bollinger | 1459 | 33.7 | -0.037 | -54.2 |
| auto + trend filter | 379 | 33.2 | -0.049 | -18.4 |
| always confluence | 750 | 32.5 | -0.073 | -54.9 |
| always rsi_reversion+trend | 284 | 31.7 | -0.095 | -27.0 |
| auto (what the bot does now) | 760 | 31.2 | -0.114 | -86.9 |
| always confluence+trend | 343 | 30.3 | -0.138 | -47.4 |
| always macd | 487 | 30.4 | -0.139 | -67.8 |
| always ema_rsi+trend | 593 | 30.2 | -0.146 | -86.4 |
| always ema_rsi | 689 | 30.0 | -0.150 | -103.2 |
| always macd+trend | 394 | 30.0 | -0.153 | -60.1 |
| always bollinger+trend | 562 | 29.5 | -0.163 | -91.6 |

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
| 4h | 1804 | 33.8 | -0.034 | +nan | +nan | -62.1 |
| 15m | 1976 | 37.0 | -0.072 | +nan | +nan | -142.2 |
| 1h | 7083 | 32.6 | -0.112 | +nan | +nan | -790.4 |
| 5m | 5821 | 35.6 | -0.251 | +nan | +nan | -1459.8 |

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


# Is the candle filter real?

Avg R after spread. against = candle against the trade; close_against = closed against the trade vs the previous close (no open price used); against_no_gap = against, only where the open is next to the previous close.

| TF | Strategy | All | Against | Close against | Against, no gap |
|---|---|---|---|---|---|
| 5m | ema_rsi | -0.385 (7546) | -0.273 (1036) | -0.306 (1096) | -0.245 (694) |
| 5m | ema_rsi+trend | -0.374 (6549) | -0.242 (884) | -0.312 (908) | -0.219 (608) |
| 5m | macd | -0.308 (5599) | -0.086 (755) | -0.253 (768) | -0.088 (526) |
| 5m | macd+trend | -0.310 (4641) | -0.065 (627) | -0.275 (627) | -0.079 (443) |
| 5m | rsi_reversion | -0.299 (8888) | -0.165 (517) | - | +0.021 (274) |
| 5m | rsi_reversion+trend | -0.295 (2589) | +0.003 (192) | - | +0.091 (110) |
| 5m | bollinger | -0.272 (13765) | -0.186 (2018) | -0.278 (1644) | -0.172 (1241) |
| 5m | bollinger+trend | -0.251 (5821) | -0.067 (874) | -0.238 (680) | -0.070 (578) |
| 5m | confluence | -0.309 (7525) | -0.159 (639) | -0.434 (445) | -0.044 (403) |
| 5m | confluence+trend | -0.310 (3718) | -0.033 (435) | -0.349 (375) | +0.117 (309) |
| 15m | ema_rsi | -0.271 (2793) | -0.132 (364) | -0.219 (450) | -0.172 (276) |
| 15m | ema_rsi+trend | -0.241 (2426) | -0.072 (312) | -0.196 (388) | -0.104 (236) |
| 15m | macd | -0.228 (2043) | -0.017 (258) | -0.065 (308) | -0.010 (210) |
| 15m | macd+trend | -0.202 (1717) | +0.038 (208) | -0.041 (247) | +0.028 (167) |
| 15m | rsi_reversion | -0.230 (3192) | -0.204 (126) | - | -0.125 (92) |
| 15m | rsi_reversion+trend | -0.132 (892) | -0.345 (54) | - | -0.400 (39) |
| 15m | bollinger | -0.187 (4886) | -0.061 (517) | -0.190 (552) | -0.045 (381) |
| 15m | bollinger+trend | -0.072 (1976) | +0.019 (217) | -0.044 (214) | +0.004 (170) |
| 15m | confluence | -0.218 (2687) | -0.115 (202) | -0.239 (180) | -0.165 (163) |
| 15m | confluence+trend | -0.177 (1329) | -0.018 (151) | -0.237 (163) | -0.119 (121) |
| 1h | ema_rsi | -0.127 (8775) | -0.184 (1045) | -0.181 (1382) | -0.177 (878) |
| 1h | ema_rsi+trend | -0.132 (7448) | -0.165 (848) | -0.176 (1120) | -0.158 (709) |
| 1h | macd | -0.137 (6298) | -0.160 (707) | -0.141 (954) | -0.145 (587) |
| 1h | macd+trend | -0.134 (5166) | -0.124 (594) | -0.167 (801) | -0.119 (498) |
| 1h | rsi_reversion | -0.147 (11443) | -0.132 (428) | - | -0.071 (337) |
| 1h | rsi_reversion+trend | -0.145 (3057) | -0.134 (112) | - | -0.034 (87) |
| 1h | bollinger | -0.106 (17395) | -0.094 (2102) | -0.126 (2536) | -0.106 (1830) |
| 1h | bollinger+trend | -0.112 (7083) | -0.100 (760) | -0.099 (932) | -0.129 (654) |
| 1h | confluence | -0.146 (8747) | -0.112 (591) | -0.109 (554) | -0.104 (504) |
| 1h | confluence+trend | -0.144 (3956) | -0.073 (347) | -0.074 (422) | -0.012 (294) |
| 4h | ema_rsi | -0.059 (2267) | +0.026 (246) | +0.100 (382) | +0.009 (230) |
| 4h | ema_rsi+trend | -0.054 (1960) | -0.024 (208) | +0.078 (320) | -0.048 (195) |
| 4h | macd | -0.108 (1594) | +0.060 (184) | -0.107 (255) | +0.056 (171) |
| 4h | macd+trend | -0.120 (1329) | +0.069 (153) | -0.113 (215) | +0.063 (143) |
| 4h | rsi_reversion | -0.038 (3160) | -0.042 (131) | - | -0.114 (109) |
| 4h | rsi_reversion+trend | -0.018 (844) | -0.023 (35) | - | +0.011 (31) |
| 4h | bollinger | -0.043 (4706) | -0.012 (671) | -0.025 (851) | -0.000 (626) |
| 4h | bollinger+trend | -0.034 (1804) | +0.116 (198) | +0.020 (292) | +0.124 (189) |
| 4h | confluence | -0.047 (2330) | +0.015 (163) | +0.209 (162) | -0.033 (141) |
| 4h | confluence+trend | -0.044 (1019) | +0.070 (96) | +0.140 (118) | +0.047 (87) |
| 1d | ema_rsi | -0.003 (1311) | +0.281 (194) | +0.056 (204) | -0.490 (17) |
| 1d | ema_rsi+trend | -0.007 (1117) | +0.265 (166) | +0.118 (177) | -0.557 (13) |
| 1d | macd | -0.025 (938) | +0.615 (145) | +0.029 (166) | +0.660 (25) |
| 1d | macd+trend | -0.020 (795) | +0.621 (128) | +0.096 (148) | +0.716 (19) |
| 1d | rsi_reversion | +0.012 (1515) | +0.484 (222) | - | +0.485 (10) |
| 1d | rsi_reversion+trend | -0.003 (358) | +0.608 (48) | - | +1.982 (2) |
| 1d | bollinger | +0.003 (2505) | +0.352 (392) | -0.037 (400) | +0.325 (78) |
| 1d | bollinger+trend | -0.021 (987) | +0.347 (156) | -0.063 (157) | +0.354 (48) |
| 1d | confluence | +0.061 (1227) | +0.580 (186) | +0.105 (80) | +0.486 (14) |
| 1d | confluence+trend | +0.058 (560) | +0.393 (85) | +0.300 (66) | +0.650 (9) |

Gaps between the previous close and the open: 5m: 47.3% of bars over 0.1 ATR; 15m: 48.4% of bars over 0.1 ATR; 1h: 45.4% of bars over 0.1 ATR; 4h: 10.0% of bars over 0.1 ATR; 1d: 85.2% of bars over 0.1 ATR

# Yahoo daily candles vs broker-style daily candles (same dates)

30 pairs, 2024-02-19 to 2026-11-19. Gaps (open far from previous close): Yahoo 83.9% of days, broker-style 17.3%.

| Strategy | Yahoo all | Yahoo against | Broker all | Broker against | Broker close-against |
|---|---|---|---|---|---|
| ema_rsi | -0.095 (276) | +0.232 (48) | -0.009 (279) | -0.055 (28) | -0.084 (45) |
| ema_rsi+trend | -0.109 (244) | +0.183 (40) | -0.020 (255) | -0.019 (24) | -0.019 (42) |
| macd | -0.157 (198) | +0.334 (31) | -0.135 (200) | -0.442 (26) | +0.060 (39) |
| macd+trend | -0.142 (181) | +0.364 (26) | -0.130 (182) | -0.393 (24) | -0.016 (36) |
| rsi_reversion | -0.198 (293) | +0.117 (37) | -0.132 (278) | +0.103 (8) | - |
| rsi_reversion+trend | -0.134 (68) | +0.772 (5) | +0.015 (64) | +1.987 (1) | - |
| bollinger | -0.111 (503) | -0.050 (87) | -0.016 (521) | -0.087 (58) | +0.065 (83) |
| bollinger+trend | +0.073 (198) | +0.443 (37) | +0.149 (203) | +0.480 (22) | +0.070 (22) |
| confluence | -0.220 (256) | +0.305 (34) | -0.087 (245) | +0.383 (15) | +0.333 (20) |
| confluence+trend | -0.137 (119) | +0.823 (13) | +0.008 (114) | +0.481 (10) | +0.382 (15) |