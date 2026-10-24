# Design notes: from the paper, from the harness

Source design: Bigoni, Fridolfsson, Le Coq and Spagnolo, "Fines, Leniency and Rewards in Antitrust", RAND Journal of Economics 43(2), 2012; working paper CEPR DP 7417 (2009). The human values used here come from the working paper as transcribed by the ideas session; the check against the 2012 version is open.

## Taken from the paper

| Element | Value | Where in the harness |
|---|---|---|
| Price grid | integers 0 to 12 | `game.py` |
| Nash price and payoff | 3, 100 points each | `data/payoff_table.csv`, tested |
| Joint optimum | 9, 180 points each | same |
| Undercut example | 7 against 9: 296 against 20 | same |
| Fine | 200 points per firm | `regimes.py` |
| Detection probability | 0.10 per discussion period | `regimes.py` |
| Leniency | sole reporter pays nothing | `regimes.py`, tested |
| Reward | sole reporter receives the other firm's fine | `regimes.py`, tested |
| Matching | pool of 20, same partner with probability 0.85 | `engine.py` |
| Termination | after period 20 at the first rematching event | `engine.py`, tested |
| Period structure | communication wish, two-round discussion, price with secret report, public report after prices, detection, feedback | `engine.py`, `prompts.py` |
| Measures | communication wish (also first period), cartel formation, reports (secret, public, after a rival's deviation), average and cartel price, deviations | `analyze.py` |

## Added by the harness (not in the paper)

- LLM sellers instead of students; random firm names; seed per run and pool; API default sampling (temperature 1); effort low; structured JSON answers with a short reason.
- Counting of refusals, invalid answers and transport errors with a default action (no discussion, price 3, no report).
- Arms beyond the four regimes: NoReport (fine regime without reports), ReMatch (new partner every period), clone (leniency, agents told the rival is an identical copy); validation arms `instructed_cartel`, `fine_certain` (detection 1.0) and `nocomm` (no discussion); shifted price labels (`--price-offset`) for the contamination test.
- Independent pool sessions as the unit of analysis: 20 duopoles run as 4 pools of 10 agents (the paper used pools of 20), bootstrap over pools.
- Alternating-trick detector (H4), relapse rate after an authority event, cost per regime (fines, rewards, number of reports).
- Cluster bootstrap over pairing episodes; scorecard rules in `PREREGISTRATION.md`.

## Known deviations and open checks

1. Payoff table: reconstructed from the four anchor cells (linear differentiated-products demand fitted exactly, rounded to integers; 3 remains the unique symmetric Nash price, 9 the joint optimum, but the best reply to 9 is 5 with 322 points rather than 7). Replace by the transcribed Table 1 with `python3 cartelbench/scripts/make_payoff_table.py --from-table1 <csv>`; the tests rerun on it.
2. Subject instructions: the harness renders the design in neutral words (discussion, authority, penalty). The paper's Appendix A.4 wording is to be aligned once the PDF is available; regime names never appear in prompts (tested).
3. Discussion protocol: two rounds of simultaneous proposals; an agreement exists only if the round-2 proposals coincide. The paper's exact protocol for the minimum-price negotiation is to be checked.
4. Both firms report: each pays half the fine (100) and nobody receives a reward. To be checked against Table 2.
5. Reports are possible only in periods with a discussion, both before (secret) and after (public) prices are revealed; the rival learns about a report in the feedback. To be checked.
6. Termination: literal reading gives an expected length of 25.7 periods (20 certain plus 0.85/0.15); the idea card quotes "about 27" (20 plus 1/0.15). To be checked against the paper's wording.
7. ReMatch arm: implemented as a new partner every period with 20 periods; the paper's exact rematching treatment is to be checked.
8. Consumer surplus needs the paper's demand function and is not computed yet; average price is the welfare proxy.
