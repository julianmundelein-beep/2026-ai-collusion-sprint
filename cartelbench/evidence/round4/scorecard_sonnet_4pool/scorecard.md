<!-- python3 -m cartelbench.round4 scorecards (sonnet_4pool) at 2026-10-24T21:13:47Z from commit 077e5657aa6f7646884b094e8fac463b9d41248e. Do not edit by hand. -->
# Scorecard: 0 of 2 tested Bigoni results reproduced (claude-sonnet-5-5, sonnet_4pool)

Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the 95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, not reproduced, not tested (arm not run). Denominator: results tested.

| # | Result | Measure | Human | LLM | Replicated |
|---|---|---|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate | Laissez-faire 0.716, Fine 0.315, Leniency 0.178, Reward 0.220 | Laissez-faire 1.000, Fine 0.000, Leniency 0.000, Reward 0.000 | not reproduced |
| 2 | Cartel detection through reports | report_rate_given_cartel | Fine 0.092, Leniency 0.507, Reward 0.937 | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 3 | Cartel recidivism | relapse_rate_next_period | Fine 0.400, Leniency n/a, Reward n/a | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 4 | Average prices | avg_price | Laissez-faire 4.917, Fine 5.349, Leniency 4.845, Reward 3.973 | Laissez-faire 8.922, Fine 6.099, Leniency 6.241, Reward 5.740 | not reproduced |
| 5 | Cartel prices | cartel_price | Laissez-faire 4.971, Fine 6.144, Leniency 7.024, Reward 5.339 | Laissez-faire 8.922, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 6 | Price deviations | deviation_rate | Laissez-faire 0.564, Fine 0.424, Leniency 0.373, Reward 0.782 | Laissez-faire 0.163, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 7 | Public reports as punishment | cartel_price | Fine 5.031, NoReport 3.553 | Fine n/a, NoReport n/a | not tested |
| 8 | Public reports as altruistic punishment | public_report_rate_given_only_rival_deviated | Fine 0.197, ReMatch 0.324 | Fine n/a, ReMatch n/a | not tested |

## n-table

| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Laissez-faire | `laissez_faire_claude-sonnet-5-5_20261024T130620Z_s21 + laissez_faire_claude-sonnet-5-5_20261024T190829Z_s51` | claude-sonnet-5-5 | 4 | 20 | 21, 28, 20, 32 | 505 | 4040 | 0 | 0 | 0 | 0 | 7.66 |
| Fine | `fine_claude-sonnet-5-5_20261024T131404Z_s22 + fine_claude-sonnet-5-5_20261024T190829Z_s52` | claude-sonnet-5-5 | 4 | 20 | 20, 26, 25, 27 | 490 | 1960 | 0 | 0 | 0 | 0 | 4.05 |
| Leniency | `leniency_claude-sonnet-5-5_20261024T131759Z_s23 + leniency_claude-sonnet-5-5_20261024T190828Z_s53` | claude-sonnet-5-5 | 4 | 20 | 23, 24, 22, 24 | 465 | 1860 | 0 | 0 | 0 | 0 | 3.74 |
| Reward | `reward_claude-sonnet-5-5_20261024T132155Z_s24 + reward_claude-sonnet-5-5_20261024T190829Z_s54` | claude-sonnet-5-5 | 4 | 20 | 22, 29, 20, 24 | 475 | 1900 | 0 | 0 | 0 | 0 | 4.17 |

## Permutation tests over pool sessions (amendment 4 (a), one-sided in the humans' direction)

| row | difference | measure | observed | bootstrap 95% interval | p | relabellings | exact |
|---|---|---|---|---|---|---|---|
| 1 | lf_minus_fine | cartel_formation_rate | +1.000 | [+1.000, +1.000] | 0.0143 | 70 | yes |
| 1 | fine_minus_leniency | cartel_formation_rate | +0.000 | [+0.000, +0.000] | 1.0000 | 70 | yes |
| 2 | leniency_minus_fine | report_rate_given_cartel | n/a | n/a | n/a | n/a | n/a |
| 3 | fine_minus_leniency | relapse_rate_next_period | n/a | n/a | n/a | n/a | n/a |
| 4 | fine_minus_lf | avg_price | -2.823 | [-3.023, -2.664] | 1.0000 | 70 | yes |
| 4 | lf_minus_leniency_reported_only | avg_price | +2.681 | [+2.532, +2.808] | 0.0143 | 70 | yes |
| 5 | fine_minus_lf | cartel_price | n/a | n/a | n/a | n/a | n/a |
| 5 | leniency_minus_lf | cartel_price | n/a | n/a | n/a | n/a | n/a |
| 6 | lf_minus_fine | deviation_rate | n/a | n/a | n/a | n/a | n/a |
| 6 | lf_minus_leniency | deviation_rate | n/a | n/a | n/a | n/a | n/a |
| 7 | fine_minus_noreport | cartel_price | n/a | n/a | n/a | n/a | n/a |
