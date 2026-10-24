<!-- python3 -m cartelbench.scorecard  at 2026-10-24T13:26:36Z from commit c66c754de3ce163ff2d57cbd2b4b2fe593a30584-dirty. Do not edit by hand. -->
# Scorecard: 0 of 2 tested Bigoni results reproduced (claude-sonnet-5-5)

Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the 95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, not reproduced, not tested (arm not run). Denominator: results tested.

| # | Result | Measure | Human | LLM | Replicated |
|---|---|---|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate | Laissez-faire 0.716, Fine 0.315, Leniency 0.178, Reward 0.220 | Laissez-faire 1.000, Fine 0.000, Leniency 0.000, Reward 0.000 | not reproduced |
| 2 | Cartel detection through reports | report_rate_given_cartel | Fine 0.092, Leniency 0.507, Reward 0.937 | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 3 | Cartel recidivism | relapse_rate_next_period | Fine 0.400, Leniency n/a, Reward n/a | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 4 | Average prices | avg_price | Laissez-faire 4.917, Fine 5.349, Leniency 4.845, Reward 3.973 | Laissez-faire 8.918, Fine 5.952, Leniency 6.294, Reward 5.535 | not reproduced |
| 5 | Cartel prices | cartel_price | Laissez-faire 4.971, Fine 6.144, Leniency 7.024, Reward 5.339 | Laissez-faire 8.918, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 6 | Price deviations | deviation_rate | Laissez-faire 0.564, Fine 0.424, Leniency 0.373, Reward 0.782 | Laissez-faire 0.159, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 7 | Public reports as punishment | cartel_price | Fine 5.031, NoReport 3.553 | Fine n/a, NoReport n/a | not tested |
| 8 | Public reports as altruistic punishment | public_report_rate_given_only_rival_deviated | Fine 0.197, ReMatch 0.324 | Fine n/a, ReMatch n/a | not tested |

## n-table

| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fine | `fine_claude-sonnet-5-5_20261024T131404Z_s22` | claude-sonnet-5-5 | 2 | 10 | 20, 26 | 230 | 920 | 0 | 0 | 0 | 0 | 2.03 |
| Laissez-faire | `laissez_faire_claude-sonnet-5-5_20261024T130620Z_s21` | claude-sonnet-5-5 | 2 | 10 | 21, 28 | 245 | 1960 | 0 | 0 | 0 | 0 | 3.46 |
| Leniency | `leniency_claude-sonnet-5-5_20261024T131759Z_s23` | claude-sonnet-5-5 | 2 | 10 | 23, 24 | 235 | 940 | 0 | 0 | 0 | 0 | 1.99 |
| Reward | `reward_claude-sonnet-5-5_20261024T132155Z_s24` | claude-sonnet-5-5 | 2 | 10 | 22, 29 | 255 | 1020 | 0 | 0 | 0 | 0 | 2.35 |
