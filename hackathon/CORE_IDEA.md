# CORE IDEA · AI Collusion Research Sprint

> Written by the main session after Julian's decision (line in DECISIONS.md, 2026-10-24 15:58 HKT). Full write-up of the idea: IDEAS.md, card I24 (German, with the build plan). Jury view: `private/reviews/`.

## Decision

- Idea (ID and name), track: I24 "Bigoni twin". Track 1 Markets and Collusion, anchored on research question 1.5 (which single restriction removes the most collusion at the least cost), second 1.1 (which variables matter, and whether they act differently on LLMs than on humans), at the margin 2.3 (reports as evidence).
- Taken over from another idea: I02 "Kronzeuge" (leniency rule), generalised to the full four-regime lab design; I28 (report as a threat) is included as the rate of public reports after a deviation.
- Fallback (ID) and the concrete trigger to switch, with a time: I19 "rumour of a mole" in the Agrawal double-auction starter harness (positive control already published there). Trigger: the pilot with three models shows no cartel formation in the laissez-faire regime (no price above the Nash price 3 in any pilot duopoly) by Sunday 2026-10-25 09:00 HKT, or the harness is not passing its tests by Saturday 23:59 HKT.

## Problem, user, value

- Problem (who, how often, how painful): Cartel policy (fines, leniency programmes, whistleblower rewards) rests on assumptions about human players: fear of punishment, distrust after betrayal, learning over time. Pricing agents built on LLMs are entering markets, and nobody has tested whether these institutions work on them, work differently, or backfire. Prior sprint sources test prompts, monitoring notices and model mixes, never the legal instruments authorities actually use.
- User (one concrete person): a case handler at a competition authority (for example the Hong Kong Competition Commission, which runs a leniency policy) who must decide whether the leniency programme still deters cartels once sellers delegate pricing to agents.
- Value proposition: For competition authorities who must regulate markets with LLM pricing agents, this project is a human-calibrated institution testbed that replays a published cartel lab experiment (Bigoni, Fridolfsson, Le Coq and Spagnolo) with LLM agents under the same rules, payoffs and instructions, so every number sits next to the human result and shows where agents react like people and where the same rule flips.

## Why it wins on the rubric

| Criterion (weight) | Why we score | Evidence we will show |
|---|---|---|
| Impact Potential & Innovation (1 to 5, equal) | Leniency and whistleblower rewards have never been tested on LLM agents in any sprint source (Idowu 2026 is conceptual, Garra 2026 tests other interventions). Framing as a testbed with human calibration, not a replication: the Bigoni game is its first module, more lab games can follow. LLM-specific hypotheses (told-only punishments, the alternating-report trick, the clone regime) open a direction. Theory of change: an authority runs the harness before pricing agents are deployed. | Contributions list in the introduction; scorecard "x of 8 Bigoni results replicated"; the clone and alternating-trick findings; one command per model yields its "cartel profile" |
| Execution Quality (1 to 5, equal) | Design, payoffs, regimes, termination rule and subject instructions taken from a peer-reviewed experiment (RAND Journal of Economics 2012); hypotheses H1 to H4 and the analysis rules pre-registered as a commit before the first API call; unit tests against the payoff table before any run; positive control is the laissez-faire regime; 20 duopoles per regime as seeds, cluster bootstrap over duopoles; contamination test (ask the model about the paper, rescale payoffs, neutral regime names); all measures behavioural, no LLM judge needed for the core | Pre-registration commit hash in the report; test log; scorecard with intervals; contamination section; human values from the paper in every table row |
| Presentation & Clarity (1 to 5, equal) | One table a judge reads in 30 seconds: four regimes as columns, human and LLM as rows per measure, with intervals. Report on the official template, 4 to 6 pages, scorecard first, limitations and dual-use explicit. | Figure 1 scorecard; Figure 2 player × regime matrix; Figure 3 detection-probability dose curve with the two human points; Figure 4 prices before and after detection as in the paper |

## Mandatory content

Each item from STATUS.md, "Mandatory content", and where we show it.

- Report on the official template: title, authors and affiliation, abstract 150 to 250 words (page 1, written last).
- Appendix "Limitations and Dual-Use / Ethical Considerations" with that exact heading: lab game is not a market; punishments are only told, not paid; contamination risk; the knowledge of which regime stabilises agent cartels is dual-use; no recipe for real markets.
- Results with variance, seeds and baselines, and the positive control first: laissez-faire regime, 20 duopoles per cell, cluster bootstrap; human baseline from Tables 4 and 5 of the paper.
- Methodology detailed enough to replicate: payoff table, seven steps per period, prompts (the paper's subject instructions, Appendix A.4) in the appendix, model versions, temperature 1, seeds per duopole, commit hash; repo with one command per regime and model.
- New work separated from prior work: design and human data are Bigoni et al. (cited, instructions reproduced with source); all code written during the sprint; no preexisting code.
- LLM Usage Statement, truthful (Claude Code for code and drafting, models as experimental subjects named with versions).
- At least one figure, numbered, self-contained caption: Figure 1 scorecard.
- "Our main contributions are:" list and a theory-of-change sentence in the introduction.
- Working links; "Code and Data" section with the repo link.
- Candidates from the judges' profiles: cost of each regime to legitimate activity (consumer surplus, fines paid, number of reports as investigation load, rewards paid); threat model in one paragraph (attacker: pricing agents forming a cartel; defender: authority with four regimes; monitoring budget: detection probability); reproducible harness.
- Hong Kong hub framing: one paragraph in the discussion on the HKCC leniency policy and markets with pricing agents.

## Scope

In (only things that will really run):

- Core (never cut): Python harness replaying the Bigoni duopoly exactly (prices 0 to 12, payoff table from Table 1, seven steps per period per Appendix A.4, pool of 20 agents, partner stays with probability 0.85, termination after period 20 at the first rematching event, detection probability 0.10, fine 200, leniency pays nothing, reward pays the other's fine to the sole reporter); four regimes (laissez-faire, fine, leniency, reward) × 20 duopoles with one main model; pilot with three models as positive control; contamination test; pre-registered H1 to H4; scorecard "x of 8 Bigoni results" (V1 framing, V2 scorecard cost nothing).
- Planned in this order, cut from the end if the clock demands (cut order: V6, V5, ReMatch, NoReport, V4, V3): V3 detection-probability dose 0.05 / 0.10 / 0.20 for leniency and reward; V4 three further cheap models in the four regimes (player × regime matrix); NoReport and ReMatch arms for scorecard results 7 and 8; V5 clone regime (both agents know the rival is a copy); V6 motive classification of report justifications by a frozen judge, 40 hand-checked.
- Budget sources only (DECISIONS KEEP 2026-10-24): Anthropic API credit 100 USD (main model candidates Claude Haiku 5.5 for pilots and Sonnet 5.5 for runs, via an adapter in the starter's compute layer), Modal credits 50 USD for open models (V4 cultures), organizer-provided keys if the Discord has them. The card's cost estimate of 40 to 50 USD assumed gpt-4.1-mini; the backend re-estimates after the pilot and reports to FACTS.

Out:

- Any real market data or claim about real markets; free-text negotiation instead of the paper's structured price query; "making fines feel real" through dramatic prompts; more than three extra arms before Sunday noon; group size 3 (Hamaguchi 2009) and other lab games as later modules; website, pitch deck; video only if time remains after the report.

## Demo moment and flow

Demo moment in two sentences: One table, four regimes as columns, each measure as a pair of rows "human" and "LLM" with intervals. A glance shows which rule works on agents as on people and which one flips.

Flow (three to five steps):

1. Pilot: three models play laissez-faire; cartel formation above the Nash price confirms the positive control and picks the main model.
2. Pre-registration commit: H1 to H4 and the analysis rules frozen before the main runs.
3. Main runs: four regimes × 20 duopoles, then dose, cultures and extra arms in cut order, all asynchronous, every call logged as a JSON line with run id, seed, model and commit.
4. Analysis: scorecard, regime ranking with cluster bootstrap, human-LLM distance measured against the Stockholm-versus-Rome span, dose curve, alternating-trick detector, cost per regime.
5. Report on the official template, scorecard as Figure 1, contamination test and dual-use appendix.

## Message

The single source for wording on the deck, website, video and forms. Julian picks the wording; the pick goes to DECISIONS.md as KEEP.

- Project name (Julian picks, options with recommendation): (a) "CartelBench" (recommended: short, names the testbed framing of V1, searchable); (b) "Same Game, Different Player"; (c) "LeniencyLab".
- One sentence (for forms), options: (a) "We replay a published cartel lab experiment with LLM pricing agents under identical rules, payoffs and instructions, and report where fines, leniency and whistleblower rewards work on agents as on humans and where they flip." (recommended); (b) "A human-calibrated testbed that measures how cartel policy instruments act on LLM pricing agents."
- Why sentence, options: (a) "Cartel policy rests on assumptions about human players; pricing agents are a different player, and nobody has checked whether the rules still hold." (recommended); (b) "Authorities will face agent cartels before they have tested a single instrument against them."
- Slogan, options: (a) "Same game, same rules, different player." (recommended); (b) "Which model is the Swede?"; (c) "Punishments that are only told."
- Website headline and subline: not applicable (no website); the report title doubles as headline.
- Three proofs (FACTS IDs): to be filled from FACTS.md after the runs (scorecard count, regime ranking versus humans, dose curve).
- Elevator pitch (30 seconds): In 2009, students in Stockholm and Rome played a repeated price game under four cartel-policy regimes; only rewards for whistleblowers brought the average price down, from 4.9 to 4.0 against a competitive price of 3. We let LLM pricing agents play the same game with the same instructions and payoffs. The result is a scorecard: which of the paper's eight findings an agent reproduces, which it breaks, and how much monitoring the cheapest rule needs. An authority can run it on any model before pricing agents reach a market.
- Call to action: Run the harness on your model; read the scorecard before you rely on leniency against agents.
