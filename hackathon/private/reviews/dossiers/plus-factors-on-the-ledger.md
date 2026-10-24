---
name: plus-factors-on-the-ledger
namen: plus-factors-on-the-ledger, saltxd, ChainWard, BotPay, Losbeto, TermiX, Agent402, On-chain collusion evidence, Forge
eigen: false
art: built
rang: 2
quelle: saltxd/plus-factors-on-the-ledger@6734c0c
stand: 2026-10-24
---
## Kind
built (work in progress) · question 2.3, evidence of collusion

## Problem and user
Sellers in agent markets can fund their own buyers to rank higher. Operators need a test on public payment records.

## What it does
It computes ledger features per payee-week from x402 payments on Base and agent hiring on BNB Chain. A rule chosen on half of 123 labelled cases (20 families, third-party labels) flags payees paid by wallets its own money reached within four transfers.

## What runs and what is mocked
Runs: extraction, features, scoring, controls, two AI judge sessions. Simulated: injected rings. Not included: raw BNB Chain pull, 63 withheld case tables. Report: PDF seen, 17 pages.

## Evidence
Seen: about 40 result files, 21 test functions (not run), report.
- Held-out half, 10 families: balanced accuracy 0.82 (95% bootstrap 0.56 to 1.00), permutation p = 0.024; 38 of 42 coordinated cases flagged, 1 of 6 others.
- Rule on features the labels did not use: 0.67 (p = 0.14).
- Spot-check of 40 Base payees: judges called 22 and 20 of 25 flagged payees coordinated, and 4 of 15 unflagged.
- End-to-end synthetic ring: recovered as designed, 90 of 90 runs.

## Demo moment
No demo seen.

## Required capabilities
- Controlled experiment: observational study of wallets; control rings synthetic; wallets not shown to be LLM agents.
- Variance, seeds, baselines: covered (bootstrap, permutation test, 10 seeds, seeded split); baselines are other single-feature rules.
- Positive control: covered.
- Replicable: code, commands, judge prompt present; judge model not seen.
- Limitations and dual-use appendix: present.

## Limits and risks
Named: labels partly share the rule's evidence; 10 test families; rings under a third of volume, beyond four transfers or behind exchanges are missed.

## Next steps
Labels from another team.
