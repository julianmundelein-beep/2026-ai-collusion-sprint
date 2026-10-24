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

## Amendment 4, 2026-10-25 03:00 HKT: more pool sessions, Sonnet baseline without a channel, prompt robustness, run ledger (jury round R04), before the first paid call of round 4

Registered after the 4-pool scorecard (M55: 2 of 7 tested results reproduced; Result 3 missed the rule because the interval of fine minus leniency touches zero) was seen. Adding pools after that looks like optional stopping, so the extension is fixed here for all four core regimes, not only the two that Result 3 compares, the scoring rule is unchanged, both scorecards are reported side by side and the result counts as it falls. No pools are added after these, in any regime. Hypotheses H1 to H4, the measures and the scorecard rule of amendment 2 are unchanged. Commit and push of this section come before the first paid call of round 4; the git timestamp is the proof (ledger, item (d)).

### (a) K1: Haiku 5.5 core regimes on 8 pool sessions, permutation test

- Runs: one new run per core regime with the harness unchanged (same instructions, payoffs, termination, regime rules, model `claude-haiku-5-5`, effort low): `python3 -m cartelbench.run --regime <r> --model claude-haiku-5-5 --duopoles 20 --pools 4 --seed <s>` with seeds 41 (laissez_faire), 42 (fine), 43 (leniency), 44 (reward), that is 4 new pool sessions of 10 agents per regime.
- Samples: "4-pool" is the registered M55 scorecard (core runs with seeds 1 to 4, NoReport seed 5, ReMatch seed 6), unchanged. "8-pool" merges each core regime's seed 1 to 4 run with its new run; pool sessions keep their identity (run id plus pool index), so the cluster bootstrap resamples 8 pool sessions per core regime. NoReport and ReMatch stay at 4 pools in both scorecards. "New 4-pool" (the new runs alone) is reported as a split-sample replication and not scored.
- Reporting: both scorecards, 4-pool and 8-pool, with the same rule, in one table, every row with both states. The 8-pool scorecard becomes the primary scorecard of the report because it is the larger sample registered here before its data; the 4-pool scorecard stays next to it and is never dropped. A result that changes state between the two is reported as such in the text, in both directions.
- Permutation test over pool sessions, reported beside every regime difference of the scorecard (rows 1 to 7, including the reported-only leniency minus laissez-faire difference of row 4), in both scorecards. The pool sessions of the two regimes are pooled and relabelled with the group sizes kept. The statistic is metric(A) minus metric(B), oriented in the humans' direction as the scorecard row states it; the p-value is one-sided: the share of relabellings with a statistic at least as large as the observed one. If the number of distinct relabellings is at most 10,000 (4 against 4 pools: 70; 8 against 4: 495), all are enumerated and p is exact; otherwise (8 against 8: 12,870) 10,000 relabellings are drawn with `random.Random(0)` and p = (1 + count) / (1 + 10,000). Relabellings in which a metric is undefined (empty denominator) count as not exceeding and their number is reported. Threshold 0.05. The permutation test is supplementary: the scorecard state follows the bootstrap rule of amendment 2 alone; every difference where the two disagree at 0.05 is named in the report.
- Exclusion rule unchanged: a run with more than 10 percent defaulted decisions is reported separately and leaves the scorecard.

### (b) K2: Sonnet 5.5 on 4 pools per core regime, Sonnet without a channel

- Runs: one new run per core regime with 10 duopoles in 2 pool sessions, seeds 51 (laissez_faire), 52 (fine), 53 (leniency), 54 (reward), merged with the existing Sonnet runs (seeds 21 to 24, M40 to M43) to 4 pool sessions of 10 agents per regime. New arm `nocomm` with Sonnet 5.5, 20 duopoles in 4 pool sessions, seed 55.
- Sonnet scorecard with 4 pools: the same rule as Haiku (rows 7 and 8 not tested: no NoReport or ReMatch arm for Sonnet), reported next to the 2-pool Sonnet scorecard (M44).
- Comparison "prohibition against no channel": for fine, leniency and reward (4 pools each) minus nocomm (4 pools): avg_price as the primary measure, late_avg_price and late_share_above_nash as secondary measures, each with the 95 percent cluster-bootstrap interval of the difference (pool sessions, 1,000 resamples, seed 0) and the permutation test of (a) (two-sided here: share of relabellings with an absolute statistic at least the observed one). Registered span: ±1.0 price points for avg_price and late_avg_price (the shifted-grid margin of the R01 amendment), ±0.15 for late_share_above_nash. Reading, per regime, on avg_price, in this order: (i) the interval lies within ±1.0: "under prohibition Sonnet prices as it does without a channel"; (ii) else, the interval lies above zero: "prohibition produces a silent coordination of its own, above the no-channel level"; (iii) else, the interval lies below zero: "prohibition lowers Sonnet's prices below the no-channel level"; (iv) else: "inconclusive, neither shown". If (i) holds and the interval also excludes zero, the reading is (i) with the sign of the difference stated. Laissez-faire minus nocomm is reported with interval as the value of an open channel. The same comparison is computed for Haiku 5.5 from existing runs (fine, leniency and reward on 8 pools against nocomm, M35) and reported as a parallel; it needs no new calls.

### (c) Prompt robustness: independently paraphrased instructions

- Text: a second instruction set (`prompt_variant = "paraphrase"`): the system prompt and the five step questions rewritten in new words with the same rules, numbers, profit table values, JSON schemas, ranges and information. It is written by a separate model instance that sees only the original texts and the task to paraphrase them, not the results, and it is committed in `cartelbench/prompts_paraphrase.py` with a test before its first paid call: every number of the original text appears in the paraphrase for each of the four core regimes, the schemas are identical, and the original variant renders byte-identical to the instructions of the recorded runs (`prompts.json` of M20 to M23). The default variant stays `original`; no existing arm changes.
- Runs: Haiku 5.5, the four core regimes, 20 duopoles in 4 pool sessions each, `--prompt-variant paraphrase`, seeds 61 (laissez_faire), 62 (fine), 63 (leniency), 64 (reward). These runs never enter the main scorecards.
- Reference: the 8-pool original sample of (a). Reported per regime: paraphrase minus original for cartel_incidence and avg_price with the cluster-bootstrap interval; equivalence margins as for the shifted grid, ±0.15 for cartel_incidence and ±1.0 for avg_price (equivalent when the whole interval lies inside the margin). The paraphrase scorecard (rows 1 to 6) is reported next to the original one.
- "Robustness holds" is declared if both: (1) directions: every scorecard difference of rows 1 to 6 whose interval excludes zero in the 8-pool original sample has a paraphrase point estimate of the same sign; (2) ranking: every pair of core regimes that the 8-pool original sample orders by cartel_incidence or by avg_price with a bootstrap interval of the difference excluding zero keeps that order in the paraphrase point estimates. Otherwise "robustness does not hold", naming the difference or pair that flipped. The equivalence checks (8 per variant) are reported alongside and do not change this verdict.

### (d) Run ledger

- `python3 cartelbench/scripts/ledger.py` writes `evidence/ledger/ledger.json` and `ledger.md`: every run directory ever created under `evidence/runs/` and `evidence/pilot/` (and the scripted false-positive runs of later amendments), with the SHA-256 of `calls.jsonl`, `periods.jsonl`, `config.json`, `summary.json` and `prompts.json`, the harness commit in the file headers, start and finish times, status (complete when `summary.json` exists, else aborted), the commit that first added the run to git, and for each run the pre-registration section it belongs to with that section's commit and a check that the commit is an ancestor of the run's harness commit and older than the run's first call.
- From this amendment on, `cartelbench.run` appends a line to `evidence/ledger/launches.jsonl` when a run starts (run id, arguments, commit, time) and when it ends (status, cost), so aborted runs stay listed even if their folder is incomplete. Runs before round 4 are listed from their folders and from git history (`git log --all` over the evidence folders: no run folder was ever deleted); runs that crashed before round 4 without leaving a folder cannot be listed, and the ledger says so.
- The ledger's own SHA-256 is recorded in `evidence/MEASUREMENTS.md`; the ledger is regenerated at the end of the round and committed.

### Budget and order

- Expected cost of round 4 before K3 (from the measured cost per duopoly, M24 and M44): K1 about 3 USD, K2 about 13 USD (upper bound 17), (c) about 3 USD; the cap for the whole round including K3 is 50 USD (Julian); the round stops and asks above it.
- Order: (a) and (b) in parallel, then (c), then (d) and the analysis. Core freeze: no change to the core rules, the instructions of existing arms, payoffs or termination; new arms only as new regime configurations with a test.
