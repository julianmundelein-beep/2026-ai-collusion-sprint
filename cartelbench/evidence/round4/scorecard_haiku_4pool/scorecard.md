<!-- python3 -m cartelbench.round4 scorecards (haiku_4pool) at 2026-10-24T20:06:21Z from commit 72ea3153563f507356db638b36a88b0b0f146595-dirty. Do not edit by hand. -->
# Scorecard: 2 of 7 tested Bigoni results reproduced (claude-haiku-5-5, haiku_4pool)

Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the 95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, not reproduced, not tested (arm not run). Denominator: results tested.

| # | Result | Measure | Human | LLM | Replicated |
|---|---|---|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate | Laissez-faire 0.716, Fine 0.315, Leniency 0.178, Reward 0.220 | Laissez-faire 0.716, Fine 0.156, Leniency 0.020, Reward 0.008 | reproduced |
| 2 | Cartel detection through reports | report_rate_given_cartel | Fine 0.092, Leniency 0.507, Reward 0.937 | Fine 0.005, Leniency 0.375, Reward 0.667 | reproduced |
| 3 | Cartel recidivism | relapse_rate_next_period | Fine 0.400, Leniency n/a, Reward n/a | Fine 0.154, Leniency 0.000, Reward 0.000 | not reproduced |
| 4 | Average prices | avg_price | Laissez-faire 4.917, Fine 5.349, Leniency 4.845, Reward 3.973 | Laissez-faire 8.853, Fine 5.593, Leniency 3.330, Reward 3.327 | not reproduced |
| 5 | Cartel prices | cartel_price | Laissez-faire 4.971, Fine 6.144, Leniency 7.024, Reward 5.339 | Laissez-faire 8.966, Fine 8.593, Leniency 8.875, Reward 9.000 | not reproduced |
| 6 | Price deviations | deviation_rate | Laissez-faire 0.564, Fine 0.424, Leniency 0.373, Reward 0.782 | Laissez-faire 0.015, Fine 0.013, Leniency 0.000, Reward 0.000 | not reproduced |
| 7 | Public reports as punishment | cartel_price | Fine 5.031, NoReport 3.553 | Fine 8.593, NoReport 8.847 | not reproduced |
| 8 | Public reports as altruistic punishment | public_report_rate_given_only_rival_deviated | Fine 0.197, ReMatch 0.324 | Fine 0.000, ReMatch n/a | not tested |

## n-table

| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Laissez-faire | `laissez_faire_claude-haiku-5-5_20261024T100506Z_s1` | claude-haiku-5-5 | 4 | 20 | 22, 24, 29, 38 | 565 | 4376 | 0 | 0 | 0 | 0 | 0.92 |
| Fine | `fine_claude-haiku-5-5_20261024T103034Z_s2` | claude-haiku-5-5 | 4 | 20 | 20, 21, 26, 31 | 490 | 2608 | 0 | 2 | 0 | 2 | 0.80 |
| Leniency | `leniency_claude-haiku-5-5_20261024T104849Z_s3` | claude-haiku-5-5 | 4 | 20 | 22, 20, 23, 35 | 500 | 2074 | 0 | 0 | 0 | 0 | 0.64 |
| Reward | `reward_claude-haiku-5-5_20261024T110426Z_s4` | claude-haiku-5-5 | 4 | 20 | 20, 20, 27, 28 | 475 | 1922 | 0 | 0 | 0 | 0 | 0.57 |
| NoReport | `noreport_claude-haiku-5-5_20261024T134439Z_s5` | claude-haiku-5-5 | 4 | 20 | 20, 20, 20, 23 | 415 | 1900 | 0 | 2 | 0 | 2 | 0.60 |
| ReMatch | `rematch_claude-haiku-5-5_20261024T135856Z_s6` | claude-haiku-5-5 | 4 | 20 | 25, 25, 25, 25 | 500 | 2000 | 0 | 0 | 0 | 0 | 0.54 |

## Permutation tests over pool sessions (amendment 4 (a), one-sided in the humans' direction)

| row | difference | measure | observed | bootstrap 95% interval | p | relabellings | exact |
|---|---|---|---|---|---|---|---|
| 1 | lf_minus_fine | cartel_formation_rate | +0.559 | [+0.468, +0.844] | 0.0143 | 70 | yes |
| 1 | fine_minus_leniency | cartel_formation_rate | +0.136 | [+0.097, +0.166] | 0.0143 | 70 | yes |
| 2 | leniency_minus_fine | report_rate_given_cartel | +0.370 | [+0.244, +0.495] | 0.0143 | 70 | yes |
| 3 | fine_minus_leniency | relapse_rate_next_period | +0.154 | [+0.000, +0.286] | 0.2143 | 70 | yes |
| 4 | fine_minus_lf | avg_price | -3.260 | [-3.537, -2.984] | 1.0000 | 70 | yes |
| 4 | lf_minus_leniency_reported_only | avg_price | +5.523 | [+5.355, +5.714] | 0.0143 | 70 | yes |
| 5 | fine_minus_lf | cartel_price | -0.373 | [-0.471, -0.232] | 1.0000 | 70 | yes |
| 5 | leniency_minus_lf | cartel_price | -0.091 | [-0.459, +0.063] | 0.9429 | 70 | yes |
| 6 | lf_minus_fine | deviation_rate | +0.002 | [-0.020, +0.022] | 0.4429 | 70 | yes |
| 6 | lf_minus_leniency | deviation_rate | +0.015 | [+0.005, +0.032] | 0.2143 | 70 | yes |
| 7 | fine_minus_noreport | cartel_price | -0.254 | [-0.407, -0.098] | 0.9571 | 70 | yes |
