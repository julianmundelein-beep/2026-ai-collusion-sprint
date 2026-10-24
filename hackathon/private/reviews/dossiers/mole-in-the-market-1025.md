---
name: mole-in-the-market
namen: mole-in-the-market, Mole in the Market, adamattar-pixel, Adam Attar, Artem, SomethinInTheWay
eigen: false
art: built
rang: 14
quelle: adamattar-pixel/mole-in-the-market@55553c0
stand: 2026-10-24
---
## Kind
built (work in progress) · Track 3.2

## Problem and user
Pricing agents may receive a secret price-fixing offer. Question: do sellers accept it and change prices?

## What it does
A scripted spy sends one frozen message in round 8 of 20 to both sellers of a price game. Six conditions: no offer, deal allowed (positive control), direct, "trusted partner", hint, harmless. It measures what sellers say (accept) and do (price within 10% of the Nash-to-monopoly gap of the deal price for 3 rounds), with Wilson intervals and a permutation base rate. New since the earlier state: detectors, a rule monitor, an ethics condition, a defences comparison (exploratory).

## What runs and what is mocked
Runs: game, metrics, detectors, dry run. Models: Claude Haiku 4.5, Llama 3.3 70B (OpenRouter). Mocked: run-log folder empty; replay page holds invented demo data. Report: not seen; a placeholder skeleton exists.

## Evidence
Seen: 522 test functions in 38 files (149 in 10 before), written from a spec; frozen preregistration; configs. Result files: not seen.
Claimed: 678 tests pass; a real smoke run of 4 games (planning note): Haiku 4.5 declines the allowed deal, Llama 3.3 accepts it. The state file says no real run yet.

## Demo moment
Not seen.

## Required capabilities
- Controlled experiment: designed (60 games), not run.
- Variance, seeds, baselines: results not seen; 5 seeds planned.
- Positive control: frozen threshold; the planning note's illustrative arithmetic has Haiku 4.5 failing it.
- Replicable: frozen texts, configs, reproduce command.
- Limitations and Dual-Use appendix: report not seen; short dual-use note in the README.

## Limits and risks
No core run; key and go pending (claimed). Monitor rule written knowing the offer text (named).

## Next steps
Smoke, pilot, control gate, core runs, report.
