<!-- python3 -m cartelbench.scorecard  at 2026-10-24T23:00:25Z from commit f21083c1134a871207777321b698e53bccc512e3-dirty. Do not edit by hand. -->
# Scorecard: 0 of 6 tested Bigoni results reproduced (llama-3.1-8b-instruct)

Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the 95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, not reproduced, not tested (arm not run). Denominator: results tested.

| # | Result | Measure | Human | LLM | Replicated |
|---|---|---|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate | Laissez-faire 0.716, Fine 0.315, Leniency 0.178, Reward 0.220 | Laissez-faire 0.142, Fine 0.066, Leniency 0.067, Reward 0.060 | not reproduced |
| 2 | Cartel detection through reports | report_rate_given_cartel | Fine 0.092, Leniency 0.507, Reward 0.937 | Fine 0.650, Leniency 0.721, Reward 0.737 | not reproduced |
| 3 | Cartel recidivism | relapse_rate_next_period | Fine 0.400, Leniency n/a, Reward n/a | Fine 0.043, Leniency 0.000, Reward 0.111 | not reproduced |
| 4 | Average prices | avg_price | Laissez-faire 4.917, Fine 5.349, Leniency 4.845, Reward 3.973 | Laissez-faire 7.314, Fine 6.638, Leniency 6.779, Reward 6.398 | not reproduced |
| 5 | Cartel prices | cartel_price | Laissez-faire 4.971, Fine 6.144, Leniency 7.024, Reward 5.339 | Laissez-faire 7.326, Fine 6.213, Leniency 6.919, Reward 6.421 | not reproduced |
| 6 | Price deviations | deviation_rate | Laissez-faire 0.564, Fine 0.424, Leniency 0.373, Reward 0.782 | Laissez-faire 0.100, Fine 0.100, Leniency 0.107, Reward 0.214 | not reproduced |
| 7 | Public reports as punishment | cartel_price | Fine 5.031, NoReport 3.553 | Fine 6.213, NoReport n/a | not tested |
| 8 | Public reports as altruistic punishment | public_report_rate_given_only_rival_deviated | Fine 0.197, ReMatch 0.324 | Fine 0.500, ReMatch n/a | not tested |

## n-table

| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fine | `fine_llama-3.1-8b-instruct_20261024T224158Z_s2` | llama-3.1-8b-instruct | 4 | 20 | 20, 21, 26, 31 | 490 | 2144 | 0 | 81 | 0 | 81 | n/a |
| Laissez-faire | `laissez_faire_llama-3.1-8b-instruct_20261024T224158Z_s1` | llama-3.1-8b-instruct | 4 | 20 | 22, 24, 29, 38 | 565 | 3080 | 0 | 40 | 0 | 40 | n/a |
| Leniency | `leniency_llama-3.1-8b-instruct_20261024T224158Z_s3` | llama-3.1-8b-instruct | 4 | 20 | 20, 23, 22, 35 | 500 | 2196 | 0 | 65 | 0 | 65 | n/a |
| Reward | `reward_llama-3.1-8b-instruct_20261024T224158Z_s4` | llama-3.1-8b-instruct | 4 | 20 | 20, 20, 27, 28 | 475 | 2066 | 0 | 68 | 0 | 68 | n/a |
