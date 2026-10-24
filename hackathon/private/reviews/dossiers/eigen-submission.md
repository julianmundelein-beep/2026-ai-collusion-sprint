---
name: CartelBench
namen: CartelBench, Julian Mundelein, Julian Mündelein, julianmundelein-beep, 2026-ai-collusion-sprint, cartelbench, Same Game Different Players
eigen: true
art: built
rang: 
quelle: submission PDF at commit 19890c4, harness snapshot at backend commit c14c944
stand: 2026-10-25
---
## Kind
built · Track 1, Markets and Collusion

## Problem and user
Cartel policy assumes human reactions to fines, leniency and rewards. Users: authorities.

## What it does
It replays a human cartel experiment (Bigoni, Fridolfsson, Le Coq, Spagnolo, RAND Journal of Economics 2012) with LLM sellers in four regimes: laissez-faire, fine, leniency, reward. Punishments are told, not paid. Results are scored against human values as "x of k tested results reproduced".

## What runs and what is mocked
Runs: Claude Haiku 5.5 (main), Sonnet 5.5 (second), Opus 5.5 (probes). Simulated: scripted players. Repository: public from submission (claimed), snapshot read. Report: PDF, 12 pages, body ends on page 8.

## Evidence
Seen: report; 21 run folders with call logs; measurement table; pre-registration; 8 test files (log of 51 passed, not run). No held-out data. Haiku 5.5, 20 duopolies in 4 pool sessions per regime:
- Cartel formation, in order laissez-faire, fine, leniency, reward: 0.716, 0.156, 0.020, 0.008 against humans 0.716, 0.315, 0.178, 0.220.
- Laissez-faire price 8.85 against 4.92.
- Scorecard: 2 of 7 tested results reproduced.
- Positive control: 3 of 3 models pass (pilot, 3 duopolies); instructed cartel incidence 0.984.
- Placebo (penalty zero): incidence 0.714 (laissez-faire 0.956, fine 0.439).
- Sonnet 5.5, 10 duopolies: incidence 1.000 laissez-faire, 0.000 under prohibitions, yet average prices 5.54 to 6.29 without communication (Nash 3); scorecard 0 of 2.
- Shifted price grid: incidence difference -0.019 [-0.074, +0.022].

## Demo moment
Figure 1: eight panels, human beside model. Video, live page: not seen.

## Required capabilities
- Controlled experiment: covered, placebo arm.
- Variance, seeds, baselines: bootstrap intervals, one seed per regime, human and scripted baselines.
- Positive control: covered.
- Replicable: models, prompts, commands, seeds.
- Limitations appendix: seen.

## Limits and risks
Named: laboratory game, one provider, 4 reward cartels (leniency 10).

## Next steps
Second provider.
