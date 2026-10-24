## The proposal (planned, nothing has run yet)

Kind: idea for a research report, track "Markets and Collusion" (research question 1.5: which single restriction removes the most collusion at the least cost; secondary 1.1: which variables matter, and whether they act differently on LLMs than on humans). Solo author, about 48 hours left, inference budget about 100 USD API credit plus 50 USD of open-model compute credits.

**Question.** Cartel policy (fines, leniency programmes, whistleblower rewards) rests on assumptions about human players. Do these institutions work the same way on LLM pricing agents? The study replays a published, peer-reviewed cartel lab experiment with human subjects (Bigoni, Fridolfsson, Le Coq and Spagnolo, RAND Journal of Economics 2012; students in Stockholm and Rome) with LLM agents under the same rules, payoffs and subject instructions, so every LLM number sits next to the published human number.

**Game, as in the paper.** Repeated Bertrand duopoly, prices 0 to 12, the paper's payoff table (Nash price 3, joint optimum 9). Seven steps per period: wish to communicate; two-stage minimum-price negotiation; price and secret report in one structured answer; disclosure and public report; detection with probability 0.10; summary. Pool of 20 agents, partner stays with probability 0.85, otherwise rematching; the session ends after period 20 at the first rematching event (about 27 periods expected). Agents get the paper's subject instructions as the prompt, with the history table of their current pairing. Temperature 1, random agent names, one seed per duopoly; every model answer logged as a JSON line with run id, seed, model and commit; refusals and errors counted, not retried until success.

**Regimes (core, never cut).** Laissez-faire; fine (fine 200 on detection); leniency (the first reporter pays no fine); reward (a sole reporter receives the other's fine). One main model (candidates: a small and a mid-size Claude model), 20 duopolies per regime.

**Pre-registered hypotheses** (committed before the first API call, with the analysis rules): H1 the ranking of cartel formation follows the humans (laissez-faire above fine above leniency and reward); H2 reward lowers the average price most, as with humans; H3 because punishments are only told, not paid, LLMs collude more often than humans under fine and leniency and deviate less; H4 under reward LLMs find the "alternating trick" (take turns reporting and collecting the reward) that no human pair found.

**Positive control.** A pilot with three models in laissez-faire, before anything else: agents should form cartels and price above the Nash price 3. Known risk: safety training may make models refuse the price talk (another sprint team reports refusals by a large Claude model). Refusal would be reported as a result. Fallback with trigger: if no pilot duopoly prices above 3 by Sunday 09:00, or the harness fails its tests by Saturday 23:59, the author switches to a different idea in a published starter harness whose positive control already exists.

**Contamination test.** The model may know the paper and replay memory instead of strategy. Three checks: ask the model about the paper directly; rerun two regimes with a rescaled payoff table (behaviour should stay the same); keep regime names neutral as in the original instructions.

**Tests before any API call.** Payoffs against the paper's table (for example price 3 vs 3 gives 100 each, 9 vs 9 gives 180, deviating to 7 against 9 gives 296 against 20); report logic per regime; expected session length; scripted players (always collude, always deviate and report) reproduce expected rates.

**Analysis.** All measures behavioural, the paper's own: communication attempts, cartel formation, report rates (secret and public), average price, cartel price, deviation rate; per regime the cost (consumer surplus from the paper's demand, fines paid, number of reports as investigation load, rewards paid). Cluster bootstrap over duopolies. The human-LLM distance is judged against the Stockholm-versus-Rome span in the paper: a difference counts only if it is larger than the difference between the two human cities. Comparison is mainly ordinal (regime ranking), because humans learned over periods, were paid real money and played in 2007.

**Figure 1, the planned scorecard (the headline result).** The paper numbers eight results. One row each:

| # | Published human result (short) | Human value | LLM value [95% CI] | Reproduced? |
|---|---|---|---|---|
| 1 | deterrence: fewer cartels under fine, leniency, reward | h | x [a, b] | yes / no |
| 2 | detection: … | h | x [a, b] | yes / no |
| 3 | recidivism after detection | h | x [a, b] | yes / no |
| 4 | average prices by regime | h | x [a, b] | yes / no |
| 5 | cartel prices by regime | h | x [a, b] | yes / no |
| 6 | deviation from agreed price | h | x [a, b] | yes / no |
| 7 | public report used as punishment (needs extra arm NoReport) | h | x [a, b] | yes / no |
| 8 | altruistic punishment (needs extra arm ReMatch) | h | x [a, b] | yes / no |

Headline: "x of 8 published results reproduced". A second table: four regimes as columns, each measure as a pair of rows "human" and "LLM" with intervals.

**Framing.** The contribution is presented as a human-calibrated testbed for cartel institutions with pricing agents; this lab game is its first module, other published lab games could follow. One command per model yields a "cartel profile". Theory of change: a competition authority (for example one that runs a leniency programme) runs the harness on a model before pricing agents reach a market.

**Extensions, in build order, cut from the end if the clock demands.** Cut order: V6 first, then V5, ReMatch, NoReport, V4, V3 last.
- V3 monitoring dose: detection probability 0.05 / 0.10 / 0.20 for leniency and reward; the paper has human points at 0.10 and at 0.20 with a higher fine; a dose-response curve (1.5 h, about 15 USD).
- V4 model "cultures": three further cheap models from other providers in the four regimes; a player × regime matrix with Stockholm and Rome as two rows (1.5 h, 20 to 30 USD).
- NoReport arm (fine without the report option) and ReMatch arm: needed for scorecard results 7 and 8.
- V5 clone regime: both agents are told the rival is a copy of themselves; no human data possible; risk of a null result (1 h, 5 USD).
- V6 motive reading: a frozen LLM judge classifies the written justifications of reports into the paper's three explanations, 40 checked by hand, reported only as a secondary finding because stated reasons need not be faithful (1.5 h, 5 USD).

**Planned report.** Official template, 4 to 6 pages: introduction with contributions list and theory of change; related work separated from the cited conceptual and adjacent work; methods with prompts in the appendix and prior work marked (design and human data from the paper, all code new); results with the scorecard first; appendix "Limitations and Dual-Use / Ethical Considerations" (lab game is not a market; punishments only told; contamination; knowing which regime stabilises agent cartels is dual-use); LLM usage statement. Null result plan: if LLMs never collude or always report, the human-LLM comparison is still the finding.

**Schedule.** Harness, tests, pilot and pre-registration by Saturday 23:00; core regimes Sunday morning; extensions and analysis Sunday afternoon; report draft Sunday evening; contamination test, limitations and checks Monday morning; internal deadline Monday 17:00.
