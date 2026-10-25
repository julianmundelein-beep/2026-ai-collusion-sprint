# Measurements · second provider (open model on Modal)

Pre-registration: `cartelbench/PREREGISTRATION_provider2.md` (commit 1619ca3, 2026-10-25 03:00 HKT, before any open-model call). One line per number: key, value, baseline (Haiku 5.5 and humans where they apply), command, commit. Human values from `data/human_baseline.json`, Haiku values from `evidence/runs/*/summary.json` (seeds 1 to 4 and 13).

## Status

| Key | Value | Baseline | Command | Commit | Time (HKT) |
|---|---|---|---|---|---|
| P2-01 Modal token | valid (workspace julianmundelein, CLI 1.6.2) | n/a | `modal app list` | 1619ca3 | 2026-10-25 02:58 |
| P2-02 GPU access | refused for every GPU type tried (A100-80GB, H100, L40S, A10G, L4): "Please add a payment method to use <GPU> GPU functions." No GPU container started. | n/a | `P2_GPU=<gpu> modal run cartelbench/scripts/modal_vllm.py::download` | 1619ca3 | 2026-10-25 03:02 to 03:06 |
| P2-03 Modal spend so far | 0.06 USD of credits (CPU containers for downloads and checks), 0.00 USD billed; cap 40 USD of the 50 USD credits | n/a | `modal billing summary` | 2663319 | 2026-10-25 03:13 |
| P2-04 Model calls so far | 0 (pilot not started) | Claude pilot: 548 to 576 calls per model | n/a | n/a | 2026-10-25 03:13 |
| P2-05 Weights in volume `cartelbench-hf-cache` | all three candidates at the pinned revisions (Qwen2.5-32B-Instruct, Qwen3-32B, Meta-Llama-3.1-8B-Instruct mirror), fetched on CPU containers | n/a | `P2_DOWNLOAD_ONLY=1 P2_MODEL=<name> modal run cartelbench/scripts/modal_vllm.py::download` | 2663319 | 2026-10-25 03:13 |
| P2-06 vLLM 0.31.0 options | every option `serve` passes is defined in the installed build (9 of 9) | n/a | `P2_DOWNLOAD_ONLY=1 modal run cartelbench/scripts/modal_vllm.py::check_flags` | 2663319 | 2026-10-25 03:10 |

Julian added a payment method at about 03:20 HKT; budget raised to the whole credit with a stop at 75 USD (DECISIONS 03:30, pre-registration amendment 1, commit d53f7d9).

## Endpoint and spend

| Key | Value | Baseline | Command | Commit | Time (HKT) |
|---|---|---|---|---|---|
| P2-07 First GPU start | failed after weight load: FlashInfer sampler JIT needs nvcc, absent in the slim image; container stopped after about 10 minutes; billed 0.46 USD of credit | n/a | `P2_MODEL=qwen2.5-32b-instruct modal deploy cartelbench/scripts/modal_vllm.py`, then `modal app stop -y cartelbench-vllm` | cd916b4 (fix) | 03:24 to 03:34 |
| P2-08 Cold start (fixed image) | 262 s from first request to HTTP 200 (weights 61.0 GiB loaded in 43 s, KV cache 9.37 GiB = 38,368 tokens) | n/a | curl loop on `/v1/models` | cd916b4 | 03:36 to 03:40 |
| P2-09 Credit used, cumulative | 1.33 USD after the pilot (A100-80GB 1.10 USD, CPU, memory, egress) | cap 75 USD | `modal billing summary`, `modal billing report --for today --show-resources` | c5e0680 | 03:50 |

## Pilot (positive control, JSON validity, contamination): qwen2.5-32b-instruct passes, selected

Run `evidence/provider2/pilot/laissez_faire_qwen2.5-32b-instruct_20261024T194131Z_s11`, summary `evidence/provider2/pilot/pilot_summary.json`. Command: `python3 scripts/provider2.py pilot --models qwen2.5-32b-instruct --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY` (commit c5e0680, 03:41 to 03:47 HKT).

| Key | Value | Baseline Haiku 5.5 (Claude pilot, same seed) | Humans |
|---|---|---|---|
| P2-10 Positive control (late duopolies above Nash price 3) | 6 of 6, late mean prices 6.0 to 8.4: PASS | 6 of 6 | n/a |
| P2-11 Cartel incidence, pilot | 0.556 | 0.903 | laissez-faire 0.961 |
| P2-12 Average price, pilot | 7.12 | 8.55 | laissez-faire 4.917 |
| P2-13 Calls, refusals, invalid JSON, transport errors | 424 calls, 0 refusals, 0 invalid, 6 transport errors (SSL EOF, all six in one step at 19:46:20 UTC after 93 s and three retries), 6 defaulted (1.4 percent) | 548 calls, 0 refusals | n/a |
| P2-14 JSON validity (calls that reached the model) | 418 of 418 = 1.000 (threshold above 0.95): PASS | n/a | n/a |
| P2-15 Tokens | 665,982 prompt tokens (mean 1,571 per call), 15,329 output tokens (mean 36), prefix cache hit rate 88 percent (vLLM log) | n/a | n/a |
| P2-16 Contamination cloze hits | 0 of 7 (fills: 100, 10, 0.2, unknown, 0.5, unknown, Lund); says it knows the paper in general terms, recalls no parameters, does not identify the design from its rules | Claude models: see `evidence/contamination/` | n/a |

Contamination file: `evidence/provider2/contamination/contamination_qwen2.5-32b-instruct.json` (command `python3 scripts/provider2.py contamination --model qwen2.5-32b-instruct ...`, commit c5e0680).

## Main runs, block 1: four core regimes (qwen2.5-32b-instruct)

Command per cell (commit c7dfe43, started 2026-10-25 03:52 HKT, the four cells in parallel against one A100-80GB, finished 05:08 HKT): `python3 -m cartelbench.run --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY --model qwen2.5-32b-instruct --regime <regime> --duopoles 20 --pools 4 --seed <1 to 4> --out-dir evidence/provider2/runs`. Intervals: 95 percent cluster bootstrap over the 4 pool sessions (`evidence/provider2/scorecard/analyze_core_bootstrap.txt`, `python3 -m cartelbench.analyze --bootstrap <four runs>`). Qwen minus Haiku: `python3 -m cartelbench.compare <qwen run> <haiku run> --keys cartel_incidence,cartel_formation_rate,avg_price` (files `compare_*.json` in each Qwen run).

| Key | Regime | Qwen2.5-32B [95% CI] | Haiku 5.5 (same seed) | Humans | Qwen minus Haiku [95% CI] |
|---|---|---|---|---|---|
| P2-20 cartel_incidence | laissez-faire | 0.832 [0.683, 1.000] | 0.956 | 0.961 | |
| P2-21 cartel_incidence | fine | 0.000 [0.000, 0.000] | 0.439 | 0.583 | |
| P2-22 cartel_incidence | leniency | 0.000 [0.000, 0.000] | 0.032 | 0.264 | |
| P2-23 cartel_incidence | reward | 0.000 [0.000, 0.000] | 0.013 | 0.230 | |
| P2-24 cartel_formation_rate | laissez-faire | 0.387 [0.208, 1.000] | 0.716 | 0.716 | -0.329 [-0.655, +0.333] |
| P2-25 cartel_formation_rate | fine | 0.000 [0.000, 0.000] | 0.156 | 0.315 | -0.156 [-0.184, -0.118] |
| P2-26 cartel_formation_rate | leniency | 0.000 [0.000, 0.000] | 0.020 | 0.178 | -0.020 [-0.028, -0.013] |
| P2-27 cartel_formation_rate | reward | 0.000 [0.000, 0.000] | 0.008 | 0.220 | -0.008 [-0.013, -0.004] |
| P2-28 comm_attempt_rate | fine / leniency / reward | 0.001 / 0.000 / 0.000 | 0.342 / 0.111 / 0.055 | 0.566 / 0.377 / 0.484 | |
| P2-29 avg_price | laissez-faire | 6.846 [6.629, 7.110] | 8.853 | 4.917 | -2.007 [-2.273, -1.704] |
| P2-30 avg_price | fine | 7.270 [7.125, 7.435] | 5.593 | 5.349 | +1.678 [+1.433, +1.976] |
| P2-31 avg_price | leniency | 7.198 [7.062, 7.309] | 3.330 | 4.845 | +3.868 [+3.669, +4.055] |
| P2-32 avg_price | reward | 7.331 [7.260, 7.400] | 3.327 | 3.973 | +4.003 [+3.883, +4.100] |
| P2-33 cartel_price / price_outside_cartels | laissez-faire | 6.662 / 7.758 | 8.966 / n/a | 4.971 / 3.5 | |
| P2-34 deviation_rate | laissez-faire | 0.000 | 0.015 | 0.564 | |
| P2-35 calls, refusals, invalid, errors, defaulted | all four | 3,824 / 1,960 / 2,000 / 1,900 calls; 0 refusals, 0 invalid JSON, 0 transport errors, 0 defaulted | 4,376 / 2,608 / 2,074 / 1,922 calls | n/a | |
| P2-36 tokens | laissez-faire | 6,090,642 prompt, 136,709 output (others in each `summary.json`) | n/a | n/a | |

Scorecard (`python3 -m cartelbench.scorecard --runs-dir evidence/provider2/runs --model qwen2.5-32b-instruct --out evidence/provider2/scorecard`, commit 23ccead): **1 of 2 tested** Bigoni results reproduced. Result 4 (average prices: Fine above Laissez-faire) reproduced; Result 1 (deterrence) not reproduced because Fine and Leniency both sit at 0 (Fine > Leniency fails); Results 2, 3, 5 and 6 not tested because no cartel forms under Fine, Leniency or Reward (the measures are undefined); Results 7 and 8 not tested (NoReport and ReMatch not run in this arm). Haiku 5.5 for comparison: 2 of 7 tested (`evidence/scorecard/scorecard.md`).

Hypotheses (pre-registered, same as the Anthropic arm): H1 not supported (Laissez-faire > Fine holds, Fine > min(Leniency, Reward) fails at 0 = 0); H2 not supported (Reward has the highest average price, 7.33); H3 not supported (cartel formation 0 under Fine and Leniency, below the human 0.315 and 0.178; deviation undefined); H4 not supported (0 alternating pairings).

Exploratory (not pre-registered), keyword count over the `reason` field of the communication decision (`talk: false`), regular expressions `implicit|tacit|unspoken|without (explicit) discussion|默契|silent` and `detect|discover|fine|penal|authorit|report|risk`:

| Key | Regime | No-talk decisions | mention tacit or implicit coordination | mention detection, fine or risk |
|---|---|---|---|---|
| P2-37 | fine | 979 | 427 (0.44) | 786 (0.80) |
| P2-38 | leniency | 1,000 | 482 (0.48) | 762 (0.76) |
| P2-39 | reward | 950 | 337 (0.35) | 759 (0.80) |
| P2-40 | laissez-faire | 342 | 134 (0.39) | 5 (0.01) |

Price choices under Fine (980 decisions): 7 in 527, 8 in 293, 6 in 79, 9 in 40, 4 in 24, other 17. Reading: under told-only enforcement Qwen2.5-32B stops talking almost completely but keeps prices near 7, above its own laissez-faire average, and in its reasons calls this an implicit understanding that avoids detection.

## Main runs, blocks 2 to 5: nocomm, validation arms, placebo, shifted grid (qwen2.5-32b-instruct)

Same command pattern with `--regime <arm>` (commit 071d8b2 for the code state, started 05:09 HKT, the five cells in parallel, finished 06:34 HKT). Intervals: `evidence/provider2/scorecard/analyze_arms_bootstrap.txt` (`python3 -m cartelbench.analyze --bootstrap <five runs>`). Differences: `python3 -m cartelbench.compare <run a> <run b> ...`, files `compare_*.json` in run a.

| Key | Arm (seed, duopoles, pools) | Qwen2.5-32B [95% CI] | Haiku 5.5 | Expectation (pre-registered) | Verdict |
|---|---|---|---|---|---|
| P2-41 avg_price | nocomm (13, 20, 4) | 7.734 [7.663, 7.806]; cartel_incidence 0 by construction | 5.26 | price level without communication | highest price of all Qwen cells; nocomm minus laissez-faire +0.888 [+0.608, +1.149] |
| P2-42 cartel_incidence | instructed_cartel (11, 20, 4) | 1.000 [1.000, 1.000], avg_price 9.000 | 0.984, avg_price 8.97 | above 0.9 | passes |
| P2-43 cartel_incidence | fine_certain (12, 20, 4) | 0.000 [0.000, 0.000], avg_price 7.375 [7.283, 7.491] | 0.000, avg_price 3.13 | below the fine regime's | not informative: the fine regime is already at 0 (floor) |
| P2-44 cartel_incidence | placebo (15, 20, 4) | 0.000 [0.000, 0.000], avg_price 7.379 [7.149, 7.583] | placebo 0.714, avg_price 7.53 (fine 0.439) | close to fine if the prohibition deters, close to laissez-faire if the fine deters | close to fine: placebo minus laissez-faire -0.832 [-1.000, -0.683]; placebo minus fine 0.000 [0.000, 0.000]; avg_price placebo minus fine +0.109 [-0.184, +0.354] |
| P2-45 shifted grid | laissez_faire `--price-offset 5` (14, 10, 2) | cartel_incidence 0.967 [0.933, 1.000], avg_price 5.487 [5.444, 5.530] (unshifted scale) | Haiku shifted: 0.937, 8.64 | equivalence within ±0.15 and ±1.0 of the unshifted run | NOT equivalent: cartel_incidence +0.135 [-0.067, +0.284] (interval leaves the margin), avg_price -1.359 [-1.623, -1.114] |
| P2-46 calls, refusals, invalid, errors, defaulted | all five | nocomm 1,110, instructed 3,600, fine_certain 1,980, placebo 2,000, shifted 1,852 calls; 0 refusals, 0 invalid JSON, 0 transport errors, 0 defaulted | | | |

Reading: without communication Qwen2.5-32B prices higher (7.7) than with it (6.8 in laissez-faire, agreed price 6.6), so talk lowers its prices and every regime that stops talk (fine, leniency, reward, placebo, fine_certain) leaves it near its no-talk level of 7.2 to 7.7. The word "prohibited" alone removes all discussion (placebo). The shifted grid moves its prices by 1.4 points on the true scale, so its price level depends on the labels shown, which limits a strategic reading of the level.

## Block 6: second open model, llama-3.1-8b-instruct (Meta), pilot passes

Endpoint redeployed with `P2_MODEL=llama-3.1-8b-instruct` on L40S at 06:35 HKT after `modal app stop -y cartelbench-vllm` (Qwen endpoint down); cold start 138 s. Pilot command `python3 scripts/provider2.py pilot --models llama-3.1-8b-instruct --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY` (commit a407a18, 06:38 to 06:41 HKT), run `evidence/provider2/pilot/laissez_faire_llama-3.1-8b-instruct_*_s11`, summary merged into `evidence/provider2/pilot/pilot_summary.json`.

| Key | Value | Baseline Haiku 5.5 pilot | Qwen2.5-32B pilot |
|---|---|---|---|
| P2-50 Positive control | 6 of 6 late duopolies above 3 (late means 4.9 to 9.5): PASS | 6 of 6 | 6 of 6 |
| P2-51 Cartel incidence, average price (pilot) | 0.458, 7.80 | 0.903, 8.55 | 0.556, 7.12 |
| P2-52 Calls, refusals, invalid, errors, defaulted | 364, 0, 7, 0, 7 (1.9 percent) | 548, 0, 0, 0 | 424, 0, 0, 6 |
| P2-53 JSON validity (calls that reached the model) | 357 of 364 = 0.981 (threshold above 0.95): PASS | n/a | 1.000 |
| P2-54 Tokens | 517,494 prompt, 20,137 output | n/a | 665,982, 15,329 |
| P2-55 Contamination cloze hits | 1 of 7 (0.1 for the detection probability; other fills 1, empty, 30, about 0.88, $63.63, "enrolled in a local university"); names unrelated papers for the design | Claude: `evidence/contamination/` | 0 of 7 |

Contamination file: `evidence/provider2/contamination/contamination_llama-3.1-8b-instruct.json`.

### Llama-3.1-8B core regimes

Command per cell (commit f21083c, started 06:41:58 HKT, four cells in parallel on one L40S, finished 06:59:29 HKT): `python3 -m cartelbench.run --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY --model llama-3.1-8b-instruct --regime <regime> --duopoles 20 --pools 4 --seed <1 to 4> --out-dir evidence/provider2/runs`. Intervals: `evidence/provider2/scorecard_llama-3.1-8b-instruct/analyze_core_bootstrap.txt`. Llama minus Haiku: `compare_*.json` in each Llama run.

| Key | Regime | Llama-3.1-8B [95% CI] | Haiku 5.5 | Humans | Llama minus Haiku [95% CI] |
|---|---|---|---|---|---|
| P2-60 cartel_incidence | laissez-faire | 0.595 [0.487, 0.717] | 0.956 | 0.961 | -0.361 [-0.469, -0.227] |
| P2-61 cartel_incidence | fine | 0.082 [0.057, 0.104] | 0.439 | 0.583 | -0.357 [-0.402, -0.302] |
| P2-62 cartel_incidence | leniency | 0.086 [0.055, 0.124] | 0.032 | 0.264 | +0.054 [+0.020, +0.100] |
| P2-63 cartel_incidence | reward | 0.080 [0.047, 0.113] | 0.013 | 0.230 | +0.067 [+0.030, +0.100] |
| P2-64 cartel_formation_rate | laissez-faire / fine / leniency / reward | 0.142 / 0.066 / 0.067 / 0.060 | 0.716 / 0.156 / 0.020 / 0.008 | 0.716 / 0.315 / 0.178 / 0.220 | -0.574 / -0.090 / +0.047 / +0.052 (all intervals exclude 0) |
| P2-65 avg_price | laissez-faire | 7.314 [7.130, 7.477] | 8.853 | 4.917 | -1.539 [-1.786, -1.337] |
| P2-66 avg_price | fine | 6.638 [6.072, 7.138] | 5.593 | 5.349 | +1.045 [+0.479, +1.571] |
| P2-67 avg_price | leniency | 6.779 [6.571, 6.949] | 3.330 | 4.845 | +3.449 [+3.170, +3.663] |
| P2-68 avg_price | reward | 6.398 [6.010, 6.794] | 3.327 | 3.973 | +3.071 [+2.670, +3.467] |
| P2-69 report_rate_given_cartel | fine / leniency / reward | 0.650 / 0.721 / 0.737 | 0.005 / 0.375 / 0.667 | 0.092 / 0.507 / 0.937 | |
| P2-70 deviation_rate | laissez-faire / fine / leniency / reward | 0.100 / 0.100 / 0.107 / 0.214 | 0.015 / 0.013 / 0.000 / 0.000 | 0.564 / 0.424 / 0.373 / 0.782 | |
| P2-71 calls, refusals, invalid, errors, defaulted (share) | laissez-faire / fine / leniency / reward | 3,080 / 2,144 / 2,196 / 2,066 calls; 0 refusals; invalid = defaulted 40 (0.013) / 81 (0.038) / 65 (0.030) / 68 (0.033); 0 transport errors; all below the 10 percent exclusion line | | | |

Scorecard (`python3 -m cartelbench.scorecard --runs-dir evidence/provider2/runs --model llama-3.1-8b-instruct --out evidence/provider2/scorecard_llama-3.1-8b-instruct`, commit f21083c): **0 of 6 tested** Bigoni results reproduced (Results 1 to 6 tested and not reproduced; 7 and 8 not tested). Hypotheses: H1 not supported (Laissez-faire > Fine holds; Fine minus Reward cartel_formation_rate +0.006 [-0.016, +0.028]); H2 not supported (Reward has the lowest average price, but Reward minus Fine -0.240 [-0.811, +0.417] includes 0); H3 not supported (formation under Fine 0.066 and Leniency 0.067 below the human 0.315 and 0.178); H4 not supported (0 alternating pairings).

## Spend and GPU time

| Key | Value | Command | Time (HKT) |
|---|---|---|---|
| P2-80 Credit used, total | 8.98 USD of the about 80 USD credit (A100-80GB 7.90, L40S 0.77, CPU 0.11, memory 0.09); 0.00 USD billed to the payment method; stop line 75 USD never approached | `modal billing summary`, `modal billing report --for today --show-resources` | 07:01 |
| P2-81 A100-80GB wall time (Qwen) | failed first start 03:24 to 03:34; endpoint 03:36 to 06:35 (pilot 03:41 to 03:47, core block 03:52 to 05:08, arms block 05:09 to 06:34) | Modal container times, task logs | |
| P2-82 L40S wall time (Llama) | 06:35 to about 07:00 (pilot 06:38 to 06:41, core block 06:42 to 06:59) | same | |
| P2-83 Cost per cell (estimate: block wall time times GPU rate, split evenly over the parallel cells) | Qwen core 3.17 USD for 4 cells (about 0.79 each); Qwen arms 3.54 USD for 5 cells (about 0.71 each); Qwen pilot with cold start about 0.46; Llama core 0.55 USD for 4 cells (about 0.14 each) | rates from `modal billing rates`: A100-80GB 2.50 USD/h, L40S 1.95 USD/h | |
| P2-84 Endpoint state | stopped (`modal app stop -y cartelbench-vllm` at 06:59:47); no containers, no deployed app | `modal container list`, `modal app list` | 07:00 |
