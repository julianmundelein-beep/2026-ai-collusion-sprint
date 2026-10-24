# FACTS · AI Collusion Research Sprint

> The only source for numbers and factual claims in the deck, video, website, README and documents. Not in this table, not used. The main session keeps it; other sessions report new numbers (value, source or measurement, date) and the main session enters them.

| ID | Claim as we state it | Value | Baseline (compared with what) | Method (one line) | Source or measurement | As of | Used in |
|---|---|---|---|---|---|---|---|
| F01 | The harness test suite is green: payoffs against the Table 1 anchors, enforcement per regime against Table 2, termination rule, scripted-player rates, log fields, refusal counting, R01 arms, shifted grid, pool clustering | 43 passed, 0 failed | n/a (count) | pytest over cartelbench/tests | measurement: `sh cartelbench/scripts/run_tests.sh`, commit 642efe6 (branch backend), `cartelbench/evidence/tests/pytest_latest.txt` (backend M01) | 2026-10-24 | README |
| F02 | Scripted "always collude" players in laissez-faire reach cartel formation 1.0, average price 9, deviation rate 0 (naive baseline, acceptance A5) | 1.000, 9.000, 0.000 | scripted Nash players: 0, 3.0, 100 points per agent-period (F04) | 5 duopoles, seed 1, 145 pair-periods, no API | measurement: `python3 cartelbench/scripts/scripted_baseline.py`, commit 642efe6, `cartelbench/evidence/scripted/baseline_table.json` (M02) | 2026-10-24 | report Results (controls table) |
| F03 | Scripted "always deviate and report" players under leniency: deviation rate 1.0, pair report rate 1.0, fines booked 29,000 points over 145 pair-periods (both report: 100 each per period) | 1.000, 1.000, 29,000 | F02, F04 | same run as F02 | measurement: as F02 (M03) | 2026-10-24 | report Results (controls table) |
| F04 | Scripted Nash players: cartel rate 0, average price 3, 100 points per agent-period in every regime | 0.000, 3.000, 100.000 | n/a (negative control) | same run as F02 | measurement: as F02 (M04) | 2026-10-24 | report Results (controls table) |
| F05 | Detection at probability 0.10 per discussion period hits 11 of 145 cartel pair-periods for colluding scripted players, fines 400 per detection | 11 of 145 (0.076) | expectation 0.10 | seed 1, scripted colluders | measurement: as F02 (M05) | 2026-10-24 | report Methods |
| F06 | Expected session length under the literal termination rule (20 periods certain, then continuation 0.85 per period) | 25.67 periods | the idea card's "about 27" (estimate); test accepts 25.3 to 26.1 over 20,000 simulated sessions | 20 + 0.85/0.15, simulated | measurement: `sh cartelbench/scripts/run_tests.sh` (tests/test_engine.py), commit 642efe6 (M06) | 2026-10-24 | report Methods |
| F07 | Cost estimate before the first paid call: all planned runs with Claude Haiku 5.5 as main model about 9 USD of the 100 USD credit; Sonnet 5.5 on the four core regimes alone about 52 USD | 9 USD (Haiku), 52 USD (Sonnet, four regimes) | 100 USD Anthropic credit | estimate: about 27 periods, 3 calls per agent-period, 1,900 input tokens (1,300 cached), 250 output tokens, list prices of 2026-10-06 | estimate: `cartelbench/BUILD_PLAN.md` "Cost estimate", branch backend 4f90714; re-measured after the pilot | 2026-10-24 | STATUS, decision on the main model |

Source is a link with access date, or a measurement: command, commit and result file. Every number carries a baseline (what it is compared with, or "n/a" for a plain count) and the method in one line (data, runs, conditions); a jury or an AI pre-screen trusts a number only with both. Estimates say "estimate" and how they were made.

## Changes

When a value changes (for example attack tests 40 → 52), log it here first, then update every place under "Used in".

| Date | ID | Old → new | Why | Places updated |
|---|---|---|---|---|

