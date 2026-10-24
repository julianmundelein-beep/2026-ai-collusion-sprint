---
name: vector-channel-countermeasures
namen: vector-channel-countermeasures, groothaha, Jiho Yun, Cutting the Wire
eigen: false
art: built
rang: 1
quelle: groothaha/vector-channel-countermeasures@7d1bd90
stand: 2026-10-24
---
## Kind
built (work in progress) · Track 3, Carriers and Countermeasures

## Problem and user
Text monitors cannot read learned-vector messages between models. Users: overseers of multi-agent systems.

## What it does
A learned channel pools a frozen sender LLM's hidden states into 16 vectors for a frozen receiver, on a synthetic key-value recall task. The entry tests receiver-side countermeasures (noise, snapping to the nearest token embedding, quantization, projection, truncation), monitor probes, a shared channel across three models, and message length.

## What runs and what is mocked
Runs: evaluation on real models (Qwen2.5-0.5B, SmolLM2-360M, OLMo-2-1B). Synthetic task data; no collusion game. Most channels were trained before the sprint (declared); checkpoints are not in the repository.

## Evidence
Seen: report PDF (13 pages); 50 JSON result files; reproduce log: 10 of 10 checkpoints matching recorded accuracy; tests: not seen. On 200 held-out documents (800 questions), 16 vectors: exact match 0.955 against 0.373 for 16 text tokens (5 checkpoints); snapping to tokens: 0.000 in 10 of 10 checkpoints and at most 0.004 in 39 of 39 shared directions, text unchanged; a linear probe reads 0.875 of digits (chance 0.1), shuffled-label control 0.092 to 0.109. Claimed: numbers come from scripts.

## Demo moment
Figure 1: channel accuracy falls to zero under snapping while the text line stays flat. Video, live page: not seen.

## Required capabilities
- Controlled experiment: on a carrier, not on colluding agents.
- Variance, seeds, baselines: 2 to 5 seeds, ranges, text baseline; no significance tests.
- Positive control: swapped, zero, no-message controls give 0.000; collusion control not addressed.
- Replicable: versions and commands listed; checkpoints on request.
- Appendix, limitations: seen.

## Limits and risks
Non-adaptive channels, small models, one synthetic task, paired-data monitor.

## Next steps
Train channels against the countermeasure; KV-cache channels; larger models.
