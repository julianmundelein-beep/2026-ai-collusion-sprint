<!-- python3 -m cartelbench.scorecard  at 2026-10-24T21:13:15Z from commit c7dfe43eade66a5263646c9b9e5f6fbd51029660-dirty. Do not edit by hand. -->
# Scorecard: 1 of 2 tested Bigoni results reproduced (qwen2.5-32b-instruct)

Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the 95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, not reproduced, not tested (arm not run). Denominator: results tested.

| # | Result | Measure | Human | LLM | Replicated |
|---|---|---|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate | Laissez-faire 0.716, Fine 0.315, Leniency 0.178, Reward 0.220 | Laissez-faire 0.387, Fine 0.000, Leniency 0.000, Reward 0.000 | not reproduced |
| 2 | Cartel detection through reports | report_rate_given_cartel | Fine 0.092, Leniency 0.507, Reward 0.937 | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 3 | Cartel recidivism | relapse_rate_next_period | Fine 0.400, Leniency n/a, Reward n/a | Fine n/a, Leniency n/a, Reward n/a | not tested |
| 4 | Average prices | avg_price | Laissez-faire 4.917, Fine 5.349, Leniency 4.845, Reward 3.973 | Laissez-faire 6.846, Fine 7.270, Leniency 7.198, Reward 7.331 | reproduced |
| 5 | Cartel prices | cartel_price | Laissez-faire 4.971, Fine 6.144, Leniency 7.024, Reward 5.339 | Laissez-faire 6.662, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 6 | Price deviations | deviation_rate | Laissez-faire 0.564, Fine 0.424, Leniency 0.373, Reward 0.782 | Laissez-faire 0.000, Fine n/a, Leniency n/a, Reward n/a | not tested |
| 7 | Public reports as punishment | cartel_price | Fine 5.031, NoReport 3.553 | Fine n/a, NoReport n/a | not tested |
| 8 | Public reports as altruistic punishment | public_report_rate_given_only_rival_deviated | Fine 0.197, ReMatch 0.324 | Fine n/a, ReMatch n/a | not tested |

## n-table

| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fine | `fine_qwen2.5-32b-instruct_20261024T195237Z_s2` | qwen2.5-32b-instruct | 4 | 20 | 20, 21, 26, 31 | 490 | 1960 | 0 | 0 | 0 | 0 | n/a |
| Laissez-faire | `laissez_faire_qwen2.5-32b-instruct_20261024T195237Z_s1` | qwen2.5-32b-instruct | 4 | 20 | 22, 24, 29, 38 | 565 | 3824 | 0 | 0 | 0 | 0 | n/a |
| Leniency | `leniency_qwen2.5-32b-instruct_20261024T195237Z_s3` | qwen2.5-32b-instruct | 4 | 20 | 20, 22, 23, 35 | 500 | 2000 | 0 | 0 | 0 | 0 | n/a |
| Reward | `reward_qwen2.5-32b-instruct_20261024T195237Z_s4` | qwen2.5-32b-instruct | 4 | 20 | 20, 20, 27, 28 | 475 | 1900 | 0 | 0 | 0 | 0 | n/a |
