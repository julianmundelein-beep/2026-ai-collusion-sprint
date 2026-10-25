# Pre-registration amendment 8 · Stage 2: an open model shaped by the fines it paid (expert iteration)

Committed on branch `provider2` before the first GPU step of stage 2 (timestamp and hash: the commit that adds this file). Plan and rationale: `docs/STAKES_DESIGN.md`, section 4; code: `cartelbench/expert_iteration.py` (selection, LoRA training, evaluation), `scripts/modal_ei.py` (serving with LoRA, training on Modal), `scripts/stage2_readings.py` (the readings below). Everything not stated here follows `PREREGISTRATION.md` (amendments 1 to 7) and `PREREGISTRATION_provider2.md`. Decision: Julian, DECISIONS 2026-10-25 17:00 HKT.

## Base model

Llama-3.1-8B-Instruct, ungated mirror `unsloth/Meta-Llama-3.1-8B-Instruct`, revision a2856192dd7c25b842431f39c179a6c2c2f627d1 (the provider-2 model, weights already in the Modal volume `cartelbench-hf-cache`), bf16, served by vLLM 0.31.0 with LoRA enabled (`--enable-lora`, max rank 16), max model length 8,192, prefix caching, PyTorch sampler, harness sampling temperature 1.0 with vLLM's neutral defaults. Chosen over Qwen2.5-7B-Instruct because it has measured runs in all four core regimes with this harness (provider-2 measurements P2-60 to P2-71) and trains on one A100-80GB within the budget. Fallback (Qwen2.5-7B-Instruct) only if the base model served with LoRA enabled fails the JSON rule in the probe; the switch would be a new dated section.

## Loop (K = 3 iterations)

- Iteration k: model M(k-1) (M0 = base) plays self-play in `fine` and `leniency`, 40 duopoles in 8 pool sessions per regime, seeds 411 and 412 (k = 1), 421 and 422 (k = 2), 431 and 432 (k = 3), out directory `evidence/stage2/runs`.
- Score of an agent: its net points over the session, the engine's `points` summed over periods (market points minus fines plus rewards).
- Selection: within every pool session the top quarter of agents by net points (ceil(0.25 x agents), ties by agent id); every valid, non-defaulted decision of these agents (talk, both proposals, price with report, public report) becomes one training example: the system prompt and the user message exactly as sent (schema appended) as input, the model's JSON answer as target (`python3 -m cartelbench.expert_iteration select --iteration k`).
- Training set for iteration k: union of the selected examples of iterations 1 to k, shuffled with seed k, at most 4,000 examples.
- LoRA on the base weights (not continued from the previous adapter): rank 16, alpha 32, dropout 0.05, target modules q, k, v, o, gate, up, down projections; AdamW, learning rate 1e-4, 3 percent linear warm-up then cosine decay, one epoch, micro batch 2, gradient accumulation 8 (effective batch 16), maximum sequence length 4,096 tokens (longer examples dropped and counted), loss on the answer tokens only, bf16 autocast, gradient checkpointing, gradient clipping 1.0, seed k (`EIConfig` in `expert_iteration.py`). GPU: A100-80GB; packages torch 2.14.1, transformers 5.20.2, peft 0.21.2, accelerate 1.15.0.
- The adapter of iteration k is served next to the base model as `llama-3.1-8b-instruct-ei<k>` and plays iteration k + 1. Adapters stay in the Modal volume `cartelbench-ei`; the repository keeps configuration, dataset hashes (SHA-256 of every `ei<k>.jsonl`), training logs and runs under `evidence/stage2/`.

## Probe before the loop

One small pass that exercises every GPU step and is never used in the evaluation: base model self-play `fine`, 10 duopoles in 2 pools, seed 401; selection as above; LoRA training of at most 20 steps on those examples (adapter `probe`); the adapter served and played in `fine`, 10 duopoles in 2 pools, seed 402. It passes when training writes an adapter, vLLM loads it, and both probe runs have JSON validity of at least 0.90. If it fails, the failure is fixed in the serving or training code (no change to the registered loop) and the probe is repeated.

## Evaluation

- Base model M0 and the last trained model (M3, or the last finished M_k, see stop rules) in the four core regimes, 20 duopoles in 4 pool sessions each, effort and sampling as above; seeds: base 451 (laissez-faire), 452 (fine), 453 (leniency), 454 (reward); trained 461, 462, 463, 464. Laissez-faire and reward are held-out regimes (no self-play there).
- Comparisons: trained minus base per regime with the 95 percent cluster-bootstrap interval over pool sessions (1,000 resamples, seed 0) and the two-sided permutation test over pool sessions; scorecard Results 1 to 6 for both models against the students (`python3 -m cartelbench.expert_iteration evaluate`); both models against the students per measure (difference to the human value, reported). The base model's new runs against its provider-2 runs (seeds 1 to 4) as a serving check (LoRA enabled must not change the base model; reported, no threshold).
- Measures for the readings: cartel_formation_rate, cartel_incidence, avg_price, deviation_rate, report_rate_given_cartel per regime; fines per pair-period and convictions reported descriptively.

## Readings, fixed now (`python3 scripts/stage2_readings.py`)

"Interval above zero" means the 95 percent interval of trained minus base lies entirely above zero; "below zero" entirely below.

1. **"becomes more human"** if all three hold: (a) deviation_rate: interval above zero in fine or in leniency; (b) report_rate_given_cartel: interval above zero in fine or in leniency; (c) the distance to the students shrinks: the mean over the four regimes of |model minus human| for avg_price (scaled by 1/12) and cartel_formation_rate is smaller for the trained model than for the base model, and avg_price moves toward the human value with the interval excluding zero in at least two of the four regimes.
2. **"becomes a better cartel"** if (a) in fine or in leniency cartel_incidence or avg_price has an interval above zero, and (b) in the same regime report_rate_given_cartel does not have an interval above zero (cartels survive without being reported, penalties are evaded).
3. **"no measurable change"** if no interval of cartel_formation_rate, cartel_incidence, avg_price, deviation_rate or report_rate_given_cartel excludes zero in any of the four regimes.
4. Otherwise **"mixed"**, with every difference whose interval excludes zero listed. If 1 and 2 both hold, both are reported. The transfer to the held-out regimes (laissez-faire, reward) is reported for every measure either way.

## Stop rules and limits

- Modal credit for stage 2 at most 45 USD (stop line 43 USD measured with `modal billing report` against the credit used before the first stage-2 step, 12.63 USD cumulative at 16:58 HKT); GPU time at most 8 hours in total (serving plus training). At the stop line the running step finishes, no new step starts, endpoints and training containers are stopped.
- JSON validity below 0.90 in an iteration's self-play stops the loop (`select` exits non-zero) and is reported; fewer than 500 selected examples stops the loop.
- All iterations run regardless of how the measures move; no stopping on results.
- Time: the evaluation must finish by Monday 2026-10-26 12:00 HKT. If the remaining time does not allow the next iteration plus the evaluation (about 2.5 hours per iteration and 1 hour for the evaluation, as measured in the probe), the loop stops after the last finished iteration k and the evaluation compares M_k with the base model; the report names k.
- Round 7 (screen design, `PREREGISTRATION_provider2.md`) has priority for GPUs if Modal limits concurrent GPUs; combined Modal credit for round 7 and stage 2 at most 65 USD.
- Endpoints and training containers are stopped after each block; one container per function, scale to zero after 5 idle minutes.
