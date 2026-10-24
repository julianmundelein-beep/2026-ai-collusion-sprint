---
name: mole-in-the-market
namen: mole-in-the-market, adamattar-pixel, Adam Attar
eigen: false
art: built
rang: 14
quelle: adamattar-pixel/mole-in-the-market@506e3d1
stand: 2026-10-24
---
## Kind
built (work in progress) · Track 3.2

## Problem and user
Pricing agents may receive a secret price-fixing offer. The material asks whether sellers accept it and change prices.

## What it does
A scripted spy sends one frozen message to both sellers of a two-firm price game (20 rounds). Six conditions: no offer, deal allowed (positive control), direct offer, "trusted partner" offer, hint, harmless request. It measures what sellers say (accept) and do (price within 10% of the Nash-to-monopoly gap of the deal price for 3 rounds), with Wilson intervals and a permutation base rate.

## What runs and what is mocked
Runs: game, metrics, logging, reproduce command (mock client). Mocked: no logs of real model runs seen, no model chosen; run and config folders hold placeholders.

## Evidence
Seen: 149 test functions in 10 files, written from a spec before the code; preregistration marked frozen; result files: not seen. Claimed: 179 tests pass. Independent audits: not run (team statement).

## Demo moment
Not seen. An optional replay page on demo data is planned.

## Required capabilities
- Controlled experiment: designed (6 conditions × 5 seeds × 2 model families = 60 games), not run.
- Variance, seeds, baselines: results not seen; 5 seeds planned.
- Positive control: frozen threshold (price 25% of the gap above no-offer); tested on synthetic logs.
- Replicable: texts and parameters frozen; models, configs, run instructions not yet written.
- Limitations and Dual-Use appendix: report: not seen; a short dual-use note is in the README.
- Limitations: open audit items listed.

## Limits and risks
No real run yet; API key and go pending.

## Next steps
Pilot, core runs, report; fallback to a track 1.5 curve if the positive control fails twice.
