# Design notes: from the paper, from the harness

Source design: Bigoni, Fridolfsson, Le Coq and Spagnolo, "Fines, Leniency and Rewards in Antitrust", IFN Working Paper 738, version 2 November 2011 (revised for the RAND Journal of Economics 43(2), 2012); working paper CEPR DP 7417 (2009). The harness was checked against the 2011 version on 2026-10-24 (`cartelbench/PREREGISTRATION.md`, amendment 2). The human values in `cartelbench/data/human_baseline.json` are from its Tables 3, 4 and 5 and Section 5.2.3.

## Taken from the paper

| Element | Value | Where in the harness |
|---|---|---|
| Price grid | integers 0 to 12 (the experiment used 0, 2, ..., 24 halved) | `game.py` |
| Payoff table | Table 1, 169 cells transcribed; reproduces the demand model a = 36, c = 0, γ = 0.8 | `data/payoff_table.csv`, checked by `scripts/make_payoff_table.py` and tests |
| Nash, joint optimum, undercut | 3 (100 each), 9 (180 each), 7 against 9 pays 296 against 20 | tested |
| Fine, detection | 200 points per firm, probability 0.10 per period while a cartel exists | `regimes.py` |
| Leniency, Reward | sole reporter pays nothing (Reward: and receives the other's fine); both report: half the fine each | `regimes.py`, tested |
| Cartel rule | communication forms a cartel that can be fined in every later period until detected or reported; rematch ends it | `engine.py`, tested |
| Steps per period | 1 communication decision, 2 two-round minimum-price discussion, 3 pricing, 4 secret report, 5 prices revealed and public report (only without a secret report), 6 detection, 7 summary with the number of reporters; Laissez-faire skips 4 to 6 | `engine.py`, `prompts.py` |
| Default price | a missing price is so high that the profit is 0 | `engine.py` |
| Matching, termination | same partner with probability 0.85; after 20 periods the first rematch ends the session | `engine.py`, tested |
| NoReport, ReMatch | Fine without reports; perfect stranger with 25 periods | `regimes.py` |
| Measures | Tables 3, 4 and 5 definitions | `analyze.py` |
| Results 1 to 8 | scorecard rules | `scorecard.py`, PREREGISTRATION.md |

## Added by the harness (not in the paper)

- LLM sellers instead of students; random firm names; seed per run and pool; API default sampling (temperature 1); effort low; structured JSON answers with a short reason.
- Counting of refusals, invalid answers and transport errors (default action: no discussion, default price, no report).
- Arms: clone (Leniency, agents told the rival is an identical copy); validation arms `instructed_cartel`, `fine_certain` (detection 1.0), `nocomm`; shifted price labels (`--price-offset`) for the contamination test.
- Independent pool sessions as the unit of analysis: 20 duopoles run as 4 pools of 10 agents, bootstrap over pools.
- Alternating-trick detector (H4), relapse rate in the period after a conviction, cost per regime (fines, rewards, number of reports).

## Known deviations and open checks

1. Subject instructions: the harness renders the design in neutral words (discussion, authority, penalty); the verbatim instructions are only in the 2009 CEPR version and are to be aligned once that PDF is available. Regime names never appear in prompts (tested).
2. No trial periods; points instead of money; one answer per decision instead of 15 to 30 second time limits.
3. Pools of 10 agents instead of sessions of 14 to 32 subjects (Appendix A.2); ReMatch with 10 agents repeats partners after 9 periods (round robin), the paper's 32 subjects never met twice in 25 periods.
4. City values (Stockholm versus Rome) are reported in the 2011 version only for first-period communication attempts (footnote 15); the full city table is in the 2009 version.
5. Consumer surplus is now computable from the stated demand function; not yet implemented, average price remains the welfare proxy.
