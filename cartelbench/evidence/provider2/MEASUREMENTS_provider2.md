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
