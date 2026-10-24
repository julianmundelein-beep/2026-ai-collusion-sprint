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

## Main runs

Not run.
