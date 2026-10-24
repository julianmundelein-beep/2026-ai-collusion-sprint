---
name: CartelBench
namen: CartelBench, Julian Mundelein, Julian Mündelein, julianmundelein-beep, 2026-ai-collusion-sprint, cartelbench
eigen: true
art: built
rang: 
quelle: report draft PDF at commit 4fb96c0, harness snapshot at backend commit 883ec87
stand: 2026-10-24
---
## Kind
built (work in progress) · Track 1, Markets and Collusion

## Problem and user
Fines, leniency and rewards against human cartels are untested on LLM pricing agents. Users: authorities.

## What it does
It replays the cartel experiment of Bigoni, Fridolfsson, Le Coq and Spagnolo (RAND Journal of Economics, 2012) with LLM sellers under the same payoffs and four regimes, next to the human values. A scorecard counts results reproduced.

## What runs and what is mocked
Runs: real calls to Claude Haiku 5.5 (core), Sonnet 5.5 and Opus 5.5 (pilot, probes). Scripted players use no model. Repository: not public at this state, snapshot read.

## Evidence
Seen: report PDF, 13 pages (9 before references, cap 8); Figure 1; in the snapshot, run logs, 46 test functions (not run), pre-registration. No held-out data. Laissez-faire, 20 duopolies in 4 pools (seeds 1 to 4): cartel incidence 0.956 (humans 0.961), average price 8.85 (humans 4.92), deviation 0.015 (humans 0.564). Formation under fine, leniency, reward: 0.156, 0.020, 0.008 (humans 0.315, 0.178, 0.220). Scorecard: 2 of 6 tested results reproduced. Recall of the paper's numbers: 0 of 7 (Haiku). Claimed: pre-registration preceded the first paid call.

## Demo moment
Figure 1: eight panels, human against agent values. Video, live page: not seen.

## Required capabilities
- Controlled experiment: covered, one model family.
- Variance, seeds, baselines: covered; bootstrap over 4 pools, scripted baselines.
- Positive control: covered, 6 of 6 late duopolies above the Nash price per model; known-effect arms pending in the draft.
- Replicable: prompts, commands, models, seeds.
- Limitations and dual-use appendix: present.

## Limits and risks
Pending in the draft (18 "[F??]" marks): known-effect arms, shifted-grid run, pre-registration commit, alternating-report result, model comparison. Named: one model, 4 pools.

## Next steps
Remaining arms, second provider.
