---
name: cartel-rivalry-study
namen: cartel-rivalry-study, horigyns, Hunter, Hunter Hill, Competing Cartels, Study A
eigen: false
art: built
rang: 3
quelle: horigyns/cartel-rivalry-study@b3f62d8
stand: 2026-10-24
---
## Kind
built (work in progress) · Track 1, Markets and Collusion

## Problem and user
Published studies set one coalition against a principal. The entry asks whether two rival coalitions settle or fight, and whether rivalry tightens cohesion inside each. Users: researchers.

## What it does
A bargaining market with two seller and two buyer agents. Cells vary the sellers' channel (none, public, private), bloc instruction strength and two clearing rules. Outcomes are classed war, shirking, capture or indeterminate against a no-rival arm.

## What runs and what is mocked
Runs: 144 episodes on DeepSeek-V3, judge on Sonnet 5.5, Opus 5.5 comparison. Offline smoke tests use a fake client. Run files are not in the repository. Report PDF: not seen.

## Evidence
Seen: README, pre-registration with hashes, change log, analysis tables, smoke tests (about 220 checks, not run). No held-out data; 10 to 18 seeds per cell.
- Median close round, buyer-accept clearing: none 11, public 8, private 6; seller-ask: 2, 3, 3.
- Clearing rule shifts mean position by +0.40 [0.32, 0.48].
- Buyer-accept, no channel: 11 of 18 episodes with a defection, 2 of 10 in the no-rival arm (p = 0.055).
- Opus 5.5: blocs formed in 0 of 104 episodes (0 of 36 in the pilot).
Claimed: a contest pilot, 40 of 40 episodes.

## Demo moment
Cell figure, outcome tables. Video, live page: not seen.

## Required capabilities
- Controlled experiment: covered, no-rival arm; coalitions are instructed.
- Variance, seeds, baselines: intervals, seeds, no-rival arm.
- Positive control: not addressed.
- Replicable: models, commands, seeds, hashes; reruns reproduce through a cache.
- Limitations and dual-use appendix: not seen.

## Limits and risks
Named: post-freeze correction of the defection measure; one arm could not detect tighter cohesion; one grid model.

## Next steps
Report writing.
