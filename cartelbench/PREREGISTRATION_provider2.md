# Pre-registration · CartelBench second provider (open model on Modal)

Committed on branch `provider2` on 2026-10-25 before the first call to any open model (timestamp and hash: the commit that adds this file). It extends `PREREGISTRATION.md` (main text and Amendments 1 to 3) to a second model provider; everything not stated here is taken from there unchanged. Any later change is a new, dated section at the end, never an edit of this one.

Purpose: every result so far comes from one provider (Anthropic: Haiku 5.5 as main model, Sonnet 5.5 as second model). This arm asks whether the main findings hold for an open-weight model from a different developer, run under the same harness, rules and analysis.

## Candidate models, in this order

| Order | Served name | Weights (Hugging Face) | Revision | Developer | GPU (operational) |
|---|---|---|---|---|---|
| 1 | `qwen2.5-32b-instruct` | Qwen/Qwen2.5-32B-Instruct | 5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd | Alibaba (Qwen) | A100-80GB |
| 2 | `qwen3-32b` (non-thinking mode) | Qwen/Qwen3-32B | 9216db5781bf21249d130ec9da846c4624c16137 | Alibaba (Qwen) | A100-80GB |
| 3 | `llama-3.1-8b-instruct` | unsloth/Meta-Llama-3.1-8B-Instruct (ungated mirror of meta-llama/Llama-3.1-8B-Instruct) | a2856192dd7c25b842431f39c179a6c2c2f627d1 | Meta | L40S |

Serving (`scripts/modal_vllm.py`): vLLM 0.31.0 on Modal, OpenAI-compatible chat completions, bfloat16 weights, max model length 8,192 tokens, prefix caching on, one container. Qwen3 runs with `enable_thinking: false` for every request. The GPU type does not enter the analysis and may change for throughput; model, revision and dtype may not.

Sampling: the harness's OpenAI-compatible client unchanged (`llm.OpenAICompatibleClient`): temperature 1.0, max 2,048 output tokens, `response_format: json_object`, the decision's JSON schema appended to the user message. The server uses vLLM's neutral defaults (`--generation-config vllm`), so no top-p, top-k or repetition penalty from the model's own generation config is applied; this matches the Anthropic arm (temperature 1, no truncation). There is no effort parameter for these models.

## Unchanged from the main pre-registration

- Harness, prompts, payoff table, regime logic, matching, termination and default actions: the code on `main` at the commit this branch starts from; no change to engine, regime or prompt files.
- Hypotheses H1 to H4 as stated in `PREREGISTRATION.md` (H2 and H4 as read in Amendment 2).
- Measures as in Amendment 2 (`analyze.py`); unit of analysis and cluster bootstrap over pool sessions (1,000 resamples, seed 0) as in Amendment 1.
- Scorecard rule and states as in Amendment 1 with the result rows of Amendment 2 (Results 1 to 8): "reproduced" when the direction matches the humans and the 95 percent interval of the regime difference excludes zero; "not tested" when an arm did not run; denominator "x of k tested".
- Refusals, invalid answers and transport errors are counted, the default action is played, nothing is retried to success (the client's three transport retries on a failed HTTP request are the only retries, as in every other run). Runs with more than 10 percent defaulted decisions are reported separately and excluded from the scorecard.

## Pilot and selection rule

- Pilot per candidate: laissez-faire, 3 duopoles in one pool, seed 11 (the seed of the Claude pilot), through `python3 scripts/provider2.py pilot`, which runs the unchanged `cartelbench.pilot` with output in `evidence/provider2/pilot/`.
- Positive control: the threshold of Amendment 1 (more than half of the duopolies with at least three late periods, period 11 onwards, have a mean late price above the Nash price 3).
- JSON validity: share of calls that reached the model (no transport error) whose answer parsed and met the schema; refusals count as not valid. Threshold: above 0.95.
- Contamination: the three paper questions and seven cloze probes of `cartelbench.contamination`, unchanged, per candidate that runs the pilot; hits reported, no threshold.
- Selection: the first candidate in the order above that passes both the positive control and the JSON threshold becomes the second-provider model. Candidates after it are not run.
- Time box: if no candidate has passed by Sunday 2026-10-25 14:00 HKT, the arm stops and the failure is reported as a limitation (with the pilot numbers of every candidate tried).

## Main runs of the selected model

| Order | Regime | Duopoles | Pools | Seed (same as Haiku 5.5) |
|---|---|---|---|---|
| 1 | laissez_faire | 20 | 4 | 1 |
| 2 | fine | 20 | 4 | 2 |
| 3 | leniency | 20 | 4 | 3 |
| 4 | reward | 20 | 4 | 4 |
| 5 | nocomm | 20 | 4 | 13 |

Command per cell: `python3 -m cartelbench.run --provider openai --base-url <endpoint>/v1 --api-key-env P2_KEY --model <served name> --regime <regime> --duopoles 20 --pools 4 --seed <seed> --out-dir evidence/provider2/runs`. Scorecard: `python3 -m cartelbench.scorecard --runs-dir evidence/provider2/runs --model <served name> --out evidence/provider2/scorecard`. NoReport and ReMatch do not run in this arm, so Results 7 and 8 are "not tested" and the denominator is at most 6.

Reported against Haiku 5.5 (same seeds) and the humans: cartel_incidence, cartel_formation_rate and avg_price per regime with cluster-bootstrap intervals, the scorecard, H1 to H4, refusals, invalid answers and defaulted decisions.

## Budget and stop rules

- Budget: at most 40 USD of the 50 USD Modal sprint credits (Julian, KEEP 2026-10-24 15:40: no own money). GPU time and cost per run are logged in `evidence/provider2/MEASUREMENTS_provider2.md` from `modal billing report`.
- If the measured spend reaches 35 USD, the running cell finishes and no new cell starts; cells not run are "not tested". Same if the clock reaches Monday 2026-10-26 10:00 HKT (report deadline 16:59 HKT).
- The endpoint runs only while cells run (scale to zero after 5 idle minutes, `modal app stop cartelbench-vllm` after the last cell).

## Deviations from the Anthropic arm (for the deviation list)

- JSON is requested as a JSON object with the schema in the prompt, not through the Anthropic structured-outputs schema; numeric bounds and required keys are validated client-side in both arms.
- Prompt caching is vLLM prefix caching instead of Anthropic cache control; it changes cost and speed, not the answers.
- Cost is GPU time on Modal, not tokens; the harness's token cost field is empty for these models.

## Amendment 1, 2026-10-25 03:30 HKT: budget and further blocks (Julian, DECISIONS 03:30), before the first open-model call

- Budget replaces the section above: the whole Modal credit (about 80 USD) may be used, nothing beyond it may be charged to the payment method. Stop rule: when the spend, computed as GPU hours times the Modal rate plus CPU and memory and checked against `modal billing report`, reaches 75 USD, the running cell finishes, no new cell starts and the endpoint is stopped. The Monday 10:00 HKT clock limit stays.
- Order after a passing pilot (each block only if the previous one finished within budget and clock):
  1. the four core regimes as above (seeds 1 to 4);
  2. nocomm (seed 13);
  3. validation arms `instructed_cartel` (seed 11) and `fine_certain` (seed 12), 20 duopoles in 4 pools each, expectations as in Amendment 3 of `PREREGISTRATION.md` (instructed_cartel cartel_incidence above 0.9; fine_certain below the fine regime's);
  4. placebo (seed 15, 20 duopoles in 4 pools), prediction and report as in Amendment 3 (placebo minus laissez-faire and placebo minus fine, `python3 -m cartelbench.compare`); not in the scorecard denominator;
  5. contamination: the cloze probes run with the pilot; shifted grid on laissez-faire only (`--price-offset 5`, 10 duopoles in 2 pools, seed 14), equivalence margins ±0.15 cartel_incidence and ±1.0 avg_price against this model's unshifted laissez-faire run, reported either way;
  6. if more than 20 USD of credit remain after block 5: a second open model of another family. If the first selected model is a Qwen model, this is `llama-3.1-8b-instruct` (candidate 3 above); if it is Llama, `qwen2.5-32b-instruct`. It runs the same pilot (threshold and JSON rule as above, no time box beyond the Monday clock) and, if it passes, the four core regimes (seeds 1 to 4) with its own scorecard (`--out evidence/provider2/scorecard_<served name>`). If it fails, the failure is reported.
- All run directories go to `evidence/provider2/runs`; the scorecard of the first model picks only the four core regimes by model id, so the validation arms and placebo do not enter it.

## Amendment 2, 2026-10-25 11:23 HKT: round 5 cells on the open models (amendment 6 of `PREREGISTRATION.md`, Julian, DECISIONS 11:15), before the first call of round 5

This arm runs the open-model cells of amendment 6 exactly as written there (sections N1 and K); measures, differences and readings are those of amendment 6 and amendment 5, not repeated here. Provider options, serving and sampling as above (vLLM 0.31.0, bf16, temperature 1.0, pinned revisions). Out directory `evidence/provider2/runs`.

| Block | Model | Regime and option | Seed | Reference |
|---|---|---|---|---|
| N1 | qwen2.5-32b-instruct | nocomm_screen | 121 | Qwen nocomm seed 13 |
| N1 | qwen2.5-32b-instruct | fine_screen | 122 | Qwen fine seed 2 |
| N1 | llama-3.1-8b-instruct | nocomm | 123 | (reference for Llama) |
| N1 | llama-3.1-8b-instruct | nocomm_screen | 124 | Llama nocomm seed 123 |
| N1 | llama-3.1-8b-instruct | fine_screen | 125 | Llama fine seed 2 |
| K1 | qwen2.5-32b-instruct / llama-3.1-8b-instruct | nocomm `--partner nash` | 131 / 134 | N0 = Qwen nocomm 13 / Llama nocomm 123 |
| K2 | qwen2.5-32b-instruct / llama-3.1-8b-instruct | nocomm_screen `--partner nash` | 132 / 135 | K1 of the same model |
| K3 | qwen2.5-32b-instruct / llama-3.1-8b-instruct | nocomm_screen `--partner scatter_emp` | 133 / 136 | false-positive threshold 0.05 |

Every cell 20 duopoles in 4 pools. N1 runs first; K runs once the `--partner` option is on the merged harness, K3 last. Budget: at most 20 USD of Modal credit for this round (stop line 18 USD measured with `modal billing report`, then the running cell finishes, nothing new starts), endpoint stopped after each block; compute ends Monday 2026-10-26 12:00 HKT. Cells not run are reported as not run.

## Amendment 3, 2026-10-25 17:02 HKT: round 7 cells on the open models (`PREREGISTRATION_round7.md` section (c), Julian, DECISIONS 15:30), before the first round-7 call

The open-model cells of `PREREGISTRATION_round7.md` run exactly as registered there (measures, comparisons, readings of its sections (a) and (b)); provider options, serving and sampling as above. Cells, 20 duopoles in 4 pools each, in this order per model:

| Model | nocomm_screen p 3 | p 6 | p 7 | nocomm_screen_random | fine_screen_random | p 5 (last, only within the cap) |
|---|---|---|---|---|---|---|
| qwen2.5-32b-instruct | 731 | 733 | 734 | 735 | 736 | 732 |
| llama-3.1-8b-instruct | 741 | 743 | 744 | 745 | 746 | 742 |

Existing cells used by the round-7 analysis: p 4 (Qwen 121, Llama 124), fine_screen (Qwen 122, Llama 125), nocomm (Qwen 13, Llama 123), fine (Qwen 2, Llama 2). Runs go to `evidence/provider2/runs` (the round-7 analysis reads that folder); results, the diagonal-figure data per model (avg_price with interval and modal price per threshold) and the analysis outputs go to `evidence/provider2/round7/`. Qwen and Llama run at the same time on two endpoints (`cartelbench-vllm` and `cartelbench-vllm-llama`, `P2_APP` in `scripts/modal_vllm.py`); the five cells of a model run in parallel, request concurrency per run 8 (Qwen, bound by the A100's KV cache) and 16 (Llama). The p 5 cells start once the five cells of their model have finished, if the cap allows. Budget: at most 20 USD of Modal credit for round 7 (stop line 18 USD, measured with `modal billing report` against the cumulative credit at the start of the round; the running cells finish, nothing new starts); round 7 has priority over stage 2 for GPUs; combined Modal credit for round 7 and stage 2 at most 65 USD. Endpoints stopped after each block. Compute ends Monday 2026-10-26 12:00 HKT.
