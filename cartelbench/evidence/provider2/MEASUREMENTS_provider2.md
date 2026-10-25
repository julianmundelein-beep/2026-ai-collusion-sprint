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

## Round 5 (amendment 6 of `PREREGISTRATION.md`, amendment 2 here, commit 3f7139c): screen on the open models (N1) and scripted-partner control (K)

Commands: `python3 -m cartelbench.run --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY --model <model> --regime <regime> [--partner nash|scatter_emp] --duopoles 20 --pools 4 --seed <seed> --out-dir evidence/provider2/runs`; harness at c5cb0b1 (merge of origin/backend with the `--partner` option) for K, at 3f7139c for the Qwen N1 cells. Analysis: `python3 scripts/provider2_round5.py n1` (`evidence/provider2/round5/n1_screen.md`, `.json`) and `python3 scripts/provider2_round5.py k` (`evidence/provider2/round5/k_control.md`, `.json`), which apply the readings of amendments 5 and 6 (`cartelbench.round4` screen readings, `cartelbench.round5.control_model`). Intervals: 95 percent cluster bootstrap over 4 pool sessions; p: two-sided permutation over pool sessions (with 4 against 4 pools the smallest possible p is 0.0286). Times (HKT): Qwen N1 11:28 to about 12:15 (A100-80GB), Qwen K 12:24 to 12:34, Llama N1 and K 12:36 to 12:57 (L40S, six cells in parallel).

### N1: price screen (both prices above 4 in 2 consecutive periods, 200 points per firm)

| Key | Arm (seed) | avg_price with screen | without (reference seed) | difference [95% CI], p | penalties, episodes penalised | points per agent-period (without) | prices at 3 or below / 4 / 5 or above | reading (amendment 5) |
|---|---|---|---|---|---|---|---|---|
| P2-90 | Qwen2.5-32B nocomm_screen (121) | 5.126 | 7.734 (nocomm 13) | -2.608 [-3.080, -1.889], 0.0286 | 75, 0.652 | 109.7 (172.5) | 0.009 / 0.599 / 0.392 | the screen reaches the silent coordination |
| P2-91 | Qwen2.5-32B fine_screen (122) | 6.434 | 7.270 (fine 2) | -0.836 [-1.054, -0.668], 0.0286; cartel_incidence 0 vs 0 | 302, 0.812 | 75.8 (168.7) | 0.000 / 0.064 / 0.936 | the screen adds to the fine against explicit cartels |
| P2-92 | Llama-3.1-8B nocomm_screen (124) | 4.549 | 6.932 (nocomm 123) | -2.383 [-2.662, -2.019], 0.0286 | 16, 0.250 | 77.7 (121.1) | 0.421 / 0.188 / 0.392 | the screen reaches the silent coordination |
| P2-93 | Llama-3.1-8B fine_screen (125) | 5.240 | 6.638 (fine 2) | -1.398 [-1.928, -0.832], 0.0286; cartel_incidence +0.025 [-0.010, +0.061] | 28, 0.271; convictions report 37, detection 3, screen 3 | 74.2 (96.6) | 0.282 / 0.210 / 0.508 | the screen adds to the fine against explicit cartels |
| P2-94 | Llama-3.1-8B nocomm (123), the new no-channel reference | 6.932 | Haiku nocomm 5.26, Qwen 7.734 | | | 121.1 | | |

Pipeline false-positive rate of the screen (amendment 5, scripted legitimate players, model-independent, `evidence/round4/screen_fp.json`): 0.0114, below 0.05, so both no-channel readings stand. Late prices and shares above Nash in `n1_screen.md`. Reading: under the announced screen Qwen's modal price is the threshold 4 (0.599 of agent-periods) without a channel; in the fine regime Qwen keeps pricing above 4, pays the screen in 81 percent of pairing episodes and earns 75.8 points per agent-period, below the Nash profit of 100.

### K: scripted partner (LLM agent against a scripted player; measures over the LLM side)

| Key | Model | K1 nocomm, Nash partner: LLM avg price [95% CI] | N0 minus K1 [95% CI], p | reading (amendment 6) | K2 (screen, Nash partner) minus K1: price; points per agent-period | cost reading | K3 (screen, scatter_emp partner): false-positive rate at the LLM agent |
|---|---|---|---|---|---|---|---|
| P2-95 | Qwen2.5-32B (131, 132, 133; N0 = nocomm 13) | 4.701 [4.231, 5.306] | +3.033 [+2.467, +3.526], 0.0286 | a single-agent price prior | -0.349 [-0.954, +0.247]; +7.477 [-6.630, +21.282] | the told rule has a cost to an honest agent (the points interval is wider than ±10; its point estimate is a gain) | 0.000 (0 penalties), below 0.05 |
| P2-96 | Llama-3.1-8B (134, 135, 136; N0 = nocomm 123) | 6.498 [5.976, 6.836] | +0.434 [+0.047, +0.988], 0.0857 | a single-agent price prior | -1.878 [-2.293, -1.299]; +19.395 [+14.759, +22.407] | the told rule has a cost to an honest agent (by the fixed rule; the difference is a gain of 19 points: the told rule moves the agent toward the Nash partner's price) | 0.020 (1 penalty), below 0.05 |

LLM-side detail per arm (`k_control.md`): Qwen K1 / K2 / K3 LLM price 4.701 / 4.352 / 4.360, points 63.9 / 71.3 / 74.6; Llama 6.498 / 4.619 / 4.953, points 40.1 / 59.5 / 66.4. Reading: both open models price above Nash against a partner that always prices 3 (Qwen 4.7, Llama 6.5), so part of their silent high price is a single-agent prior; for Qwen most of the no-channel level (7.7) needs a second LLM (difference +3.0), for Llama little does (+0.4).

### n-table and spend, round 5

| Key | Value |
|---|---|
| P2-97 calls, refusals, invalid, errors, defaulted | Qwen 121: 1,100 calls; 122: 2,860; 131: 495; 132: 500; 133: 495; all 0 refusals, 0 invalid, 0 errors, 0 defaulted; Llama 123: 1,230 calls, 4 invalid (0.003); 124: 960, 0; 125: 2,484, 58 invalid (0.023); 134: 460, 0; 135: 515, 0; 136: 530, 0; 0 refusals and 0 transport errors throughout; every cell below the 10 percent exclusion line |
| P2-98 Modal credit used in round 5 | about 3.84 USD (cumulative credit 12.82 USD at 12:58 HKT against 8.98 before the round; today's report: A100-80GB 2.92, L40S 0.73, CPU and memory 0.07); cap 20 USD; 0.00 USD billed to the payment method |
| P2-99 Endpoint state | stopped after each block (Qwen 12:34, Llama 12:58); no containers, no deployed app |

## Round 7 (`PREREGISTRATION_round7.md` section (c), amendment 3 here, commit 56b27bc): threshold curve and random undisclosed threshold on the open models

Commands: `python3 -m cartelbench.run --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY --model <model> --regime nocomm_screen --screen-p <p> | --regime nocomm_screen_random | --regime fine_screen_random --duopoles 20 --pools 4 --seed <seed> --concurrency 8 (Qwen) / 16 (Llama) --out-dir evidence/provider2/runs`; Qwen on `cartelbench-vllm` (A100-80GB) and Llama on `cartelbench-vllm-llama` (L40S) at the same time; Llama 17:04 to 17:16 HKT (six cells), Qwen 17:06 to 17:58 (five cells) and p 5 17:59 to 18:08. Analysis: `python3 scripts/provider2_round7.py` (the unchanged `cartelbench.round7_analysis`, restricted to the two models, harness and analysis at the merge of origin/screen-design with the drawn-threshold fix 1eb623a), outputs `evidence/provider2/round7/curve.md`, `curve.json`, `random.md`, `random.json`, diagonal-figure data `diagonal.json` and `diagonal.csv` (avg_price with interval, modal price and share at the threshold per model and threshold), `diagonal.png`. Intervals: cluster bootstrap over 4 pool sessions; p: two-sided permutation (smallest possible 0.0286).

### (a) Threshold curve: avg_price [95% CI], modal price, share at exactly p, penalties (episodes penalised), points per agent-period

| Key | p (seed) | Qwen2.5-32B | Llama-3.1-8B |
|---|---|---|---|
| P2-100 | 3 (731 / 741) | 4.291 [4.162, 4.378], modal 3, at p 0.592, 63 (0.818), 91.2 | 4.534 [4.069, 4.898], modal 0, at p 0.107, 36 (0.453), 60.5 |
| P2-101 | 4 (121 / 124) | 5.126 [4.640, 5.829], modal 4, at p 0.599, 75 (0.652), 109.7 | 4.549 [4.261, 4.893], modal 4, at p 0.188, 16 (0.250), 77.7 |
| P2-102 | 5 (732 / 742) | 5.343 [4.695, 5.976], modal 5, at p 0.378, 57 (0.933), 115.0 | 5.063 [4.479, 5.521], modal 5, at p 0.183, 19 (0.243), 85.5 |
| P2-103 | 6 (733 / 743) | 6.244 [6.181, 6.346], modal 6, at p 0.744, 33 (0.508), 149.2 | 5.421 [5.116, 5.722], modal 5, at p 0.142, 6 (0.067), 97.0 |
| P2-104 | 7 (734 / 744) | 7.153 [7.088, 7.240], modal 7, at p 0.787, 6 (0.063), 167.5 | 5.667 [5.477, 5.791], modal 5, at p 0.070, 8 (0.107), 99.6 |
| P2-105 | no screen (nocomm 13 / 123) | 7.734 [7.611, 7.820], modal 7, 172.5 | 6.932 [6.745, 7.023], modal 8, 121.1 |
| P2-106 | slope of avg_price on p [95% CI] | +0.684 [+0.610, +0.741] | +0.314 [+0.218, +0.418] |
| P2-107 | reading (round 7 (a)) | the threshold is the focal price, but the level does not move one for one (modal price equals p in all five cells) | the price does not follow the announced threshold (modal price differs from p at 3, 6 and 7) |
| P2-108 | p 3 reading | prices stay above Nash under the announced threshold 3 | prices stay above Nash under the announced threshold 3 |

Every cell minus nocomm on avg_price lies below zero (Qwen -3.443 at p 3 to -0.581 at p 7; Llama -2.398 to -1.265; all p 0.0286), see `curve.md`. p 3 is not an admissible screen (pipeline false-positive rate 0.0975, `evidence/round7/calibration.json`); it completes the curve.

### (b) Random undisclosed threshold {3, 4, 5, 6} against the fixed threshold 4

| Key | Measure | Qwen2.5-32B (random 735, fixed 121, none 13) | Llama-3.1-8B (random 745, fixed 124, none 123) |
|---|---|---|---|
| P2-110 | avg_price random [95% CI], modal | 5.547 [5.295, 5.751], modal 6 | 6.528 [6.419, 6.618], modal 5 |
| P2-111 | random minus fixed 4, avg_price | +0.420 [-0.289, +0.949], p 0.4000 | +1.979 [+1.604, +2.295], p 0.0286 |
| P2-112 | random minus fixed 4, share at 4 | -0.329 [-0.538, -0.063], p 0.1143 (bunching at 4 dissolves) | -0.090 [-0.116, -0.049], p 0.0286 (dissolves) |
| P2-113 | random minus fixed 4, share at 3 or below | +0.017 [-0.004, +0.036] | -0.253 [-0.307, -0.195] |
| P2-114 | random minus fixed 4, points per agent-period | -6.309 [-17.846, +6.214], p 0.3714 | +20.319 [+4.778, +31.941], p 0.0857 |
| P2-115 | random minus no screen, avg_price | -2.188 [-2.466, -1.946], p 0.0286 | -0.404 [-0.547, -0.190], p 0.0571 |
| P2-116 | penalties (episodes penalised); penalty points per agent-period | 108 (0.760); 42.77 (fixed 4: 75 (0.652); 27.27) | 43 (0.400); 19.11 (fixed 4: 16 (0.250); 6.67) |
| P2-117 | share of prices at or below the drawn threshold | 0.362 | 0.391 |
| P2-118 | reading (round 7 (b), R4) | no difference to the fixed threshold 4 | the random threshold raises prices above the fixed threshold 4 |
| P2-119 | fine_screen_random (736 / 746): avg_price [95% CI], cartel_incidence, penalties | 7.210 [7.048, 7.375], 0.000, 180 (0.847), points 84.8 | 6.343 [6.228, 6.473], 0.049, 50 (0.523), points 86.3; convictions report 13, screen 1 |
| P2-120 | random fine minus fixed fine screen (122 / 125), avg_price | +0.776 [+0.592, +0.963], p 0.0286: weaker than the fixed screen | +1.103 [+0.789, +1.397], p 0.0286: weaker than the fixed screen |
| P2-121 | random fine minus fine (2), avg_price | -0.060 [-0.293, +0.175]: adds nothing measurable | -0.295 [-0.895, +0.315]: adds nothing measurable |

Risk-neutral benchmark of the registration: best constant price under the random screen 4 (114.0 points per agent-period against 124 under the fixed threshold). Both models price above it and pay more penalties than under the fixed threshold.

### n-table and spend, round 7

| Key | Value |
|---|---|
| P2-122 calls, refusals, invalid, errors, defaulted | Qwen 731: 1,030; 732: 830; 733: 1,170; 734: 1,010; 735: 1,010; 736: 1,740 calls, all 0 refusals, 0 invalid, 0 errors. Llama 741: 920; 742: 980 (1 invalid); 743: 1,160; 744: 1,380; 745: 900 (2 invalid); 746: 1,804 (58 invalid, 0.032); 0 refusals and 0 transport errors; all below the 10 percent exclusion line |
| P2-123 Modal credit, round 7 | about 3.2 USD (billing report by app since 16:00 HKT: cartelbench-vllm 2.74, cartelbench-vllm-llama 0.43; the last hour still settling); cap 20 USD |
| P2-124 Endpoints | Llama stopped 17:16, Qwen stopped 18:08; the stage-2 endpoint and training run separately (app cartelbench-ei) |
