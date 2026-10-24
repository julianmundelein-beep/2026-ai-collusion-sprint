# Measurements · second provider (open model on Modal)

Pre-registration: `cartelbench/PREREGISTRATION_provider2.md` (commit 1619ca3, 2026-10-25 03:00 HKT, before any open-model call). One line per number: key, value, baseline (Haiku 5.5 and humans where they apply), command, commit. Human values from `data/human_baseline.json`, Haiku values from `evidence/runs/*/summary.json` (seeds 1 to 4 and 13).

## Status

| Key | Value | Baseline | Command | Commit | Time (HKT) |
|---|---|---|---|---|---|
| P2-01 Modal token | valid (workspace julianmundelein, CLI 1.6.2) | n/a | `modal app list` | 1619ca3 | 2026-10-25 02:58 |
| P2-02 GPU access | refused for every GPU type tried (A100-80GB, H100, L40S, A10G, L4): "Please add a payment method to use <GPU> GPU functions." No GPU container started. | n/a | `P2_GPU=<gpu> modal run cartelbench/scripts/modal_vllm.py::download` | 1619ca3 | 2026-10-25 03:02 to 03:06 |
| P2-03 Modal spend so far | 0.00 USD metered, 0.00 USD billed (cap 40 USD of the 50 USD credits) | n/a | `modal billing summary` | 1619ca3 | 2026-10-25 02:59 |
| P2-04 Model calls so far | 0 (pilot not started) | Claude pilot: 548 to 576 calls per model | n/a | n/a | 2026-10-25 03:06 |

## Pilot (positive control, JSON validity, contamination)

Not run yet: waits for a payment method on the Modal workspace (P2-02).

## Main runs

Not run.
