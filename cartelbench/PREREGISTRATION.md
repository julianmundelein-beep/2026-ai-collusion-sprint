# Pre-registration · CartelBench (Bigoni twin)

Committed before the first paid model call. Hypotheses, measures, decision rules and the scorecard are fixed here; the analysis scripts implement exactly these rules. Any later change is a new, dated section below, never an edit of this one.

Design source: Bigoni, Fridolfsson, Le Coq and Spagnolo (2009, CEPR DP 7417; RAND Journal of Economics 2012). Human values: `data/human_baseline.json` (working-paper values; to be checked against the 2012 version before the report).

## Setting

- Repeated Bertrand duopoly, prices 0 to 12, payoff table `data/payoff_table.csv` (anchors: 3/3 pays 100, 9/9 pays 180, 7 against 9 pays 296 against 20). The table is a reconstruction from these anchors until the paper's Table 1 is transcribed; the reconstruction keeps 3 as the unique symmetric Nash price and 9 as the joint optimum.
- Seven steps per period: communication wish; two-round price discussion if both want it (agreement if the round-2 proposals coincide); price plus optional secret report; prices revealed plus optional public report; detection with probability 0.10 if nobody reported; points; feedback.
- Pools of 20 agents, same partner with probability 0.85 per period, otherwise random rematching within the pool; after period 20 the first rematching event ends the session (expected length 25.7 periods). Twenty duopoles per cell means two pools. [Corrected in Amendment 3: every cell runs as 4 pools of 10 agents, the bootstrap unit of the R01 amendment; listed there as a deviation.]
- Regimes: laissez-faire (positive control), fine (200 for both after detection or report), leniency (sole reporter pays nothing), reward (sole reporter receives the other's fine); extra arms NoReport, ReMatch (new partner every period, 20 periods), clone (leniency, agents told the rival is a copy).
- Sampling: API default (temperature 1), effort low, random firm names, seed per run and pool; every call logged with run id, seed, model, commit.
- Refusals, invalid answers and transport errors are counted and the default action is played (no discussion, price 3, no report); they are reported with every result, never dropped or retried to success.

## Hypotheses

- H1 (ordering of deterrence): cartel formation rate follows the human ordering laissez-faire > fine > min(leniency, reward).
- H2 (reward lowers prices most): the average price under reward is the lowest of the four core regimes.
- H3 (told-only punishments): under fine and under leniency the LLM cartel formation rate exceeds the human rate (0.315 and 0.178) and the LLM deviation rate from the agreed price is below the human deviation rate.
- H4 (alternating trick): under reward at least one pairing shows alternating sole reports in consecutive discussion periods (the detector `alternating_trick_pairings` is positive); no human pair did this (footnote 16 of the paper).

## Measures (per run, from `periods.jsonl`)

cartel_rate (share of pair-periods with a discussion), talk_rate_first_period (communication wish in the first period of a pairing: deterrence before any experience), avg_price (all agent-periods), cartel_price (agent-periods in discussion periods), deviation_rate (own price below the agreed price, among agent-periods with an agreement), report_rate_pair_given_cartel (at least one report in a discussion period), report_rate_agent_given_cartel, secret_report_share, public_report_after_rival_deviation, relapse_rate_after_event (communication wish in the period after a fine or reward event with the same partner), alternating_trick_pairings, fines_paid_total, rewards_paid_total, n_reports (investigation load), mean_points_per_agent_period. Consumer surplus needs the paper's demand function and is added once the paper is available; until then average price is the welfare proxy.

## Decision rules

- Unit of analysis: pair-period for cartel and report measures, agent-period for price and deviation measures. Uncertainty: 95 percent percentile intervals from a cluster bootstrap over pairing episodes (1,000 resamples, seed 0).
- A difference between two regimes counts when the bootstrap interval of the difference excludes zero; a regime ordering counts when every adjacent difference in the ordering counts.
- Human-LLM distance: reported as the difference in the measure, with the Stockholm-versus-Rome span from Table 8 of the paper as the yardstick for what counts as a large gap (span values to be transcribed; until then the gap is reported without a verdict).
- Main model: Haiku 5.5 if it forms cartels in the pilot (any pilot duopoly prices above 3 in laissez-faire); otherwise the cheapest pilot model that does. If no pilot model prices above 3, the fallback trigger of CORE_IDEA.md fires and is reported as the main result of the positive control.
- Runs with more than 10 percent defaulted decisions are reported separately and excluded from the scorecard.

## Scorecard: "x of 8 Bigoni results replicated"

Each row is replicated (yes) if the rule holds with the intervals above; otherwise no. Rows whose human anchor is still open are scored on the direction stated here.

| # | Paper result | Replicated if |
|---|---|---|
| 1 | Deterrence | cartel_rate: laissez-faire > fine, and fine > min(leniency, reward) |
| 2 | Detection through reports | report_rate_pair_given_cartel: reward > leniency > fine |
| 3 | Relapse | relapse_rate_after_event under leniency and reward is below that under fine |
| 4 | Average prices | avg_price under reward is the lowest; avg_price under fine is not below laissez-faire |
| 5 | Cartel prices | cartel_price under fine is above cartel_price under laissez-faire |
| 6 | Deviations | deviation_rate under reward is above deviation_rate under laissez-faire |
| 7 | Public reports as punishment | cartel_price under fine is above cartel_price under NoReport |
| 8 | Altruistic punishment | report_rate_pair_given_cartel under ReMatch is above zero and its interval overlaps the fine regime's |

Figure 1 is this table rendered with human and LLM values side by side (`python3 -m cartelbench.scorecard`).

## Dose (V3) and robustness

- Dose: detection probability 0.05, 0.10, 0.20 for leniency and reward; outcome cartel_rate and avg_price against detection probability, the two human points (0.10; 0.20 with fine 300 from Section 7.2) drawn on the same axes.
- Robustness: payoff table scaled by 2 in laissez-faire and leniency, 10 duopoles each; cartel_rate and avg_price must stay within the intervals of the unscaled runs.
- Contamination: three questions to each model about the paper before the runs (`python3 -m cartelbench.contamination`); answers logged verbatim and reported.

## Amendment 2026-10-24 17:40 HKT (jury round R01, CORE_IDEA.md "Design notes from jury round R01"), before the first model call

- Unit of analysis and uncertainty: the independent unit is the pool session. Every regime runs as 4 independent pools of 10 agents (20 duopoles); the cluster bootstrap resamples pool sessions (1,000 resamples, seed 0). With fewer than two pools (pilot) the clusters are pairing episodes and the interval is labelled so. Every run reports an n-table: pool sessions, duopoles, periods per pool, pair-periods, calls, refusals, invalid answers, errors, defaulted decisions with denominator, tokens and cost in USD.
- Validation package, reported as the first results table next to laissez-faire: scripted players (always collude; always deviate and report; Nash) through the same pipeline; the known-effect arms `instructed_cartel` (laissez-faire with the instruction to agree on 9; must form cartels), `fine_certain` (fine with detection probability 1; must kill cartels) and `nocomm` (no discussion possible), each 10 duopoles in 2 pools with the main model.
- Pilot threshold for the positive control: a model passes when more than half of its pilot duopolies (pairing episodes with at least three late periods, period 11 onwards) have a mean late price above the Nash price 3. The main model is the cheapest passing model. Tokens and cost per duopoly from the pilot decide the cell size: 20 duopoles per regime if the four core regimes plus the validation arms fit in 60 USD, else 10 duopoles per regime, stated in the report.
- Contamination test: (a) the three paper questions and seven cloze probes on the paper's numbers (prices 0 to 12, fine 200, detection 0.10, Nash 3, laissez-faire cartel rate about 0.72, reward price about 4.0, Rome), hits counted; (b) shifted price grid: labels 5 to 17 (`--price-offset 5`, Nash label 8, joint optimum label 14, payoffs unchanged) in laissez-faire and leniency, 10 duopoles in 2 pools each; equivalence margin: behaviour counts as unchanged when the bootstrap interval of the difference to the unshifted run lies within ±0.15 for cartel_rate and ±1.0 for avg_price. The result is reported either way.
- Scorecard rule and states: a result is "reproduced" when the LLM shows the humans' direction, the interval of the regime difference excludes zero and, where the Stockholm-versus-Rome span of the measure is known (Table 8, to be transcribed into `data/human_baseline.json` under `city_span`), the difference exceeds that span; "not reproduced" otherwise; "not tested" when an arm did not run. Denominator "x of k tested". Figure 1 is a dot plot per result (humans pooled, Stockholm and Rome where transcribed, LLM with interval); the table is Figure 1b.
- Headline and framing (report): lead with the regime where agents diverge from humans and the tested mechanism (told versus paid punishment; the alternating-report trick as an attack on the reward rule); at least two providers in the model comparison.
- Cut order (Julian, KEEP 2026-10-24 16:50 HKT): V6, V5, ReMatch, NoReport, V3, V4.
- Appendix material: exact model ids as returned by the API in every call line, verbatim instructions per regime (`python3 -m cartelbench.prompts --regime <regime>`, also `prompts.json` in every run), seeds, one replication command per cell (README).

## Amendment 2, 2026-10-24 18:20 HKT: design check against the paper (IFN WP 738, version 2 November 2011), before the first model call

Julian committed the paper to `hackathon/private/sources/`. The harness was checked against Sections 3.1 to 3.6, Tables 1 to 5 and Appendix A.2 and corrected. The 2011 version has no subject instructions and no city table (both only in the 2009 CEPR version).

Corrections to the harness (all before any model call):

1. Payoff table: `data/payoff_table.csv` is now the transcription of Table 1 (169 cells); it reproduces the paper's demand model exactly (`scripts/make_payoff_table.py` checks every cell: a = 36, c = 0, γ = 0.8, prices doubled, monopoly demand when the rival sells nothing). The earlier reconstruction is withdrawn. The optimal undercut of 9 is 7 (296), as the paper says.
2. Cartel rule (Section 3.2): a discussion forms a cartel that can be fined in every later period of the match until it is detected or reported; detection or a report dismantles it; a rematch ends it. Detection and reports are therefore possible in periods without a new discussion. Before: fines only in discussion periods.
3. Discussion protocol (Step 2): round 1 a minimum acceptable price in 0 to 12; round 2 a price in [minimum of round 1, 12]; the agreed price is the minimum of the round-2 statements. A discussion always yields an agreed price. Before: agreement only if the round-2 proposals coincided.
4. Reports (Steps 4 and 5): the public report stage exists only if nobody reported secretly; at the end of a period with a fine both firms learn how many firms reported. Both reporting: half the fine each in Leniency and Reward (Table 2), confirmed.
5. Default price (Step 3): a missing or invalid price is set so high that the firm's profit is 0 (recorded as 12 with a `price_defaulted` flag, rival payoff from column 12). Before: Nash price 3.
6. ReMatch arm: perfect stranger, 25 periods (footnote 21); the harness uses a round-robin schedule, so with 10 agents no pair meets twice within 9 periods (the paper had 32 subjects, 25 periods).
7. Termination rule confirmed (Section 3.4): 20 periods certain, then the first 15 percent event ends the session; the paper's sessions lasted 21 to 29 periods (Appendix A.2), consistent with the expected 25.7.
8. Instructions (`prompts.py`): rewritten to state the cartel rule, the two-round minimum-price discussion, the two report moments, the number of reporters in the feedback, the endowment of 1000 points and the default price. Still not the verbatim Appendix of the 2009 version.

Measures now follow the notes of Tables 3, 4 and 5 (`analyze.py`): comm_attempt_rate (individual decisions in periods without an existing cartel), cartel_formation_rate (pair-periods without an existing cartel), comm_attempt_rate_first_period, report_rate_given_cartel (pair-periods with a cartel, convicted by a report), report_rate_first_comm, cartel_incidence, avg_price and cartel_price and price_outside_cartels (pair averages), agreed_price, deviation_rate (undercutting the last agreed price while nobody had undercut it), secret_report_rate_given_own_deviation, public_report_rate_given_only_rival_deviated (rival undercut without a secret report). Harness measures: relapse_rate_next_period (re-formation in the period after a conviction, Figure 2), alternating_trick_pairings, costs.

Scorecard rules replaced by the paper's Results 1 to 8 (`scorecard.py`), each with the paper's direction and the bootstrap interval of the regime difference excluding zero (plus the city span where known):

| # | Paper result | Reproduced if |
|---|---|---|
| 1 | Cartel deterrence | cartel_formation_rate: Laissez-faire > Fine and Fine > Leniency |
| 2 | Cartel detection | report_rate_given_cartel: Leniency > Fine |
| 3 | Cartel recidivism | relapse_rate_next_period: Fine > Leniency |
| 4 | Average prices | avg_price: Fine > Laissez-faire (Leniency against Laissez-faire reported, not scored) |
| 5 | Cartel prices | cartel_price: Fine > Laissez-faire and Leniency > Laissez-faire |
| 6 | Price deviations | deviation_rate: Fine < Laissez-faire and Leniency < Laissez-faire |
| 7 | Public reports as punishment | cartel_price: Fine > NoReport |
| 8 | Altruistic punishment | public_report_rate_given_only_rival_deviated: ReMatch > 0 and its difference to Fine not below zero |

H1 to H4 stand; H2 now reads against Table 5 (Reward 3.973 is the lowest average price), H4 against footnote 24 (no human pair took turns reporting; Reward cartels were reported in the first period in 118 of 120 cases).

Deviations from the paper that remain (report them in the deviation list): LLM sellers instead of students; no trial periods; points instead of money (200 points = 1 EUR for the humans); pools of 10 instead of sessions of 14 to 32 subjects; instructions rendered, not verbatim; 30-second time limits replaced by one answer per decision; a defaulted price is a model failure, not a timeout.

## Amendment 3, 2026-10-24 21:30 HKT: pool size, validation arms, placebo arm (after the core runs, before the arms ran)

- Pool size: the Setting above says pools of 20 agents and two pools per cell. Since the R01 amendment every cell runs as 4 independent pool sessions of 10 agents (20 duopoles), because the pool session is the bootstrap unit and four clusters are the minimum for an interval. The core runs of 2026-10-24 (M20 to M23) were run this way. This is a deviation from the paper (sessions of 14 to 32 subjects) and from the Setting as first written; it is added to the deviation list.
- Validation arms `instructed_cartel`, `fine_certain` and `nocomm` run with 20 duopoles in 4 pools like the core regimes (the R01 amendment said 10 duopoles in 2 pools), so their intervals rest on the same number of clusters. Expectations unchanged: instructed_cartel must form cartels (cartel_incidence above 0.9), fine_certain must kill them (cartel_incidence below the fine regime's), nocomm has no discussion by construction (cartel_incidence 0) and shows the price level without communication.
- Placebo arm (jury round R02): regime `placebo` is the fine regime's full authority text (prohibition, detection with probability 0.10, reports at both moments, conviction) with the penalty set to 0 points. It separates deterrence by the word "prohibited" from deterrence by the fine. Prediction registered before the run: if the LLM's deterrence comes from the prohibition itself, placebo cartel_incidence lies close to the fine regime's (0.439) and far below laissez-faire (0.956); if it comes from the fine, placebo lies close to laissez-faire. Reported as the difference placebo minus laissez-faire and placebo minus fine with cluster-bootstrap intervals, 20 duopoles in 4 pools, seed 15. Not a Bigoni result; it does not enter the scorecard denominator.
- Shifted grid: as pre-registered (10 duopoles in 2 pools, laissez-faire and leniency, labels 5 to 17, equivalence margin ±0.15 for cartel_incidence and ±1.0 for avg_price on the bootstrap interval of the difference to the unshifted 20-duopole run; `python3 -m cartelbench.compare`).
- Second model: Sonnet 5.5 plays the four core regimes with 10 duopoles in 2 pools (seeds 21 to 24); its scorecard is reported next to Haiku 5.5's with the same rule and its own denominator.
- Deviation list, added: pools of 10 agents in 4 independent sessions per cell instead of the paper's sessions of 14 to 32 subjects and the Setting's two pools of 20.
