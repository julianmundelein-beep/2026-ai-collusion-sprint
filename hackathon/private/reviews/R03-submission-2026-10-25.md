# R03 · submission · 2026-10-25

> Jury simulation, not real scores. The personas are assumptions built from public professional profiles; every entry was reduced to content, evidence and demo before scoring; the simulation compares entries and finds weaknesses, it does not predict placements. See "Limits".

## Round

| | |
|---|---|
| Subject | submission |
| State | submission PDF at commit 19890c4 (title of DECISIONS 2026-10-25 00:05; body as 597e56c), harness at backend c14c944 |
| Mode | schnell: 5 jurors × 1 run(s), 5 valid of 5 |
| Jurors | Jasmine Li, Debayan Gupta, Luis Cosio, Kaushik Prabhakar, Neeraj Kumar Singh Beshane |
| Model | claude-opus-5-5 (session default) |
| Entries | 1 own, 4 competitors, anonymised, random order per packet (seed 62586810) |
| Rubric | Dimension 1: Impact Potential & Innovation 33.33 %, Dimension 2: Execution Quality 33.33 %, Dimension 3: Presentation & Clarity 33.34 % |
| Cost | 375.222 tokens for the jurors |

## Summary

The submission ranks 1 of 5 for the first time (total median 40 on the 10 to 50 scale, IQR 40 to 40), ahead of the carrier study (36.7); all five jurors rank it first and call it the most complete controlled experiment in the field. Read in full with the printed page, however, all five give Presentation 3, not 4: the 30-word title, a Table 3 whose columns break numbers apart, Figure 1 labels that overlap the axis, and four numeric contradictions that every deep-dive juror found (leniency convictions, NoReport interval, human price in panel 7, Result 7 testable or not). The fixes need no new run: correct the numbers and the pre-registration sentence, repair the layout, scope the claims and label the Sonnet result as exploratory.

## Ranking

| # | Entry | | Total median | Spread (IQR) | Min–max | Dimension 1: Impact Potential & Innovation | Dimension 2: Execution Quality | Dimension 3: Presentation & Clarity | Median rank | Top 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **CartelBench** | own | 40 | 40–40 | 36.7–40 | 4 | 4 | 4 | 1 | 100 % |
| 2 | vector-channel-countermeasures |  | 36.7 | 36.7–36.7 | 33.3–36.7 | 3 | 4 | 4 | 2 | 100 % |
| 3 | plus-factors-on-the-ledger |  | 30 | 30–33.3 | 30–33.3 | 3 | 3 | 3 | 3 | 100 % |
| 4 | cartel-rivalry-study |  | 26.7 | 26.7–30 | 26.7–30 | 3 | 3 | 2 | 4 | 0 % |
| 5 | mole-in-the-market |  | 20 | 16.7–20 | 16.7–23.3 | 3 | 1 | 2 | 5 | 0 % |

Total = weights × score × 10. The jurors scored the official 1 to 5 levels, so totals run from 10 to 50, as in R01 and R02; weights are equal because the organizers publish none. Spread = middle half of the 5 juror runs. Top 3 = share of runs that rank the entry in the top three.

## Our entries by criterion

### CartelBench

| Criterion | Weight | Median | Spread | Why (condensed) | +2 points if |
|---|---|---|---|---|---|
| Dimension 1: Impact Potential & Innovation | 33.33 % | 4 | 4–4 | Four of five: 4, a policy-relevant first test of leniency and rewards on LLM agents against a human baseline. Cosio: 3, an extension of known LLM-collusion replications. | Show that the divergence holds across providers and derive one concrete rule for authorities (four of five); Cosio: test adaptive evasion, as Sonnet's 5.54 to 6.29 hints. |
| Dimension 2: Execution Quality | 33.33 % | 4 | 4–4 | All five: 4. Positive control, placebo, shifted grid, second model, bootstrap and an honest 2 of 7 scorecard; one seed per regime and few reward and leniency cartels hold it below 5. | More seeds per regime, a second provider, more leniency and reward cartels (five of five); Li: penalties actually deducted to separate framing from incentives. |
| Dimension 3: Presentation & Clarity | 33.34 % | 4 | 4–4 | Scoring round, all five: 4, from the dossier. Deep dive with the full text and the printed page, all five: 3 (title length, broken Table 3, Figure 1 overlap, contradictions). | Reconcile the formation and incidence numbers that three jurors read as contradictory (placebo 0.714 incidence beside laissez-faire 0.716 formation) and lead with one sentence for authorities (four of five). |

## By juror

| Juror | CartelBench: total, rank | Own top 3 | Verdict on our entry |
|---|---|---|---|
| Jasmine Li | 40, 1 of 5 | CartelBench, vector-channel-countermeasures, plus-factors-on-the-ledger | Most complete entry: controlled, positive-controlled, placebo-tested, honest scorecard; the told-not-paid framing caveat is the open question. |
| Debayan Gupta | 40, 1 of 5 | CartelBench, vector-channel-countermeasures, plus-factors-on-the-ledger | Strongest entry: a controlled, pre-registered human-versus-LLM replication with real controls and an honest scorecard. |
| Luis Cosio | 36.7, 1.5 of 5 | CartelBench, vector-channel-countermeasures, plus-factors-on-the-ledger | Most complete controlled experiment of the field; the Sonnet tacit-pricing finding is the real security story and deserves the lead. |
| Kaushik Prabhakar | 40, 1 of 5 | CartelBench, vector-channel-countermeasures, cartel-rivalry-study | Most complete entry: real controlled experiment with positive control and placebo; the framing finding is interesting for evaluators. |
| Neeraj Kumar Singh Beshane | 40, 1 of 5 | CartelBench, vector-channel-countermeasures, plus-factors-on-the-ledger | Most complete controlled experiment in the field, with honest negative replication results and verifiable logs. |

## Red lines (checked by the jury session)

| Red line | Checked | Result |
|---|---|---|
| Hidden instructions to AI graders | yes | none. No text in render mode 3, no white text (the 12 white fills are page backgrounds), no fonts under 4 pt, no JavaScript, annotations, forms or embedded files; every word of the PDF's text layer appears in the mirror except template and hyphenation residue ("With Apart Research" is the template's header line); no grader-directed phrases. PDF metadata title is "report" (harmless, could be the paper title). The ligature loss of R02 is fixed. |
| Polished numbers | yes, with one finding | No number is inflated: every checked value matches its FACTS row or the measurement file, and the human values come from F15's transcription. But one process sentence is false as written: "Nothing changed after the first call." Amendment 3 of the pre-registration was committed at 13:10 UTC (commit 3930456), after the first paid call at 09:49 UTC and after the core runs; it fixes pool size at 4 pools of 10, enlarges the validation arms to 20 duopolies, and adds the placebo arm and the second model. Hypotheses and decision rules are unchanged since the first pre-registration commit (aeb16a0, checked by diff). The pre-registered robustness check (payoff table scaled by 2) is not reported, and the R01 amendment's "at least two providers" is not met; neither appears in the deviation list. Fix: "Hypotheses and decision rules did not change after the first call; Amendment 3 (after the core runs) set the pool size, enlarged the validation arms and added the placebo arm and the second model; the scaled-payoff check did not run." The leniency split (see improvement 1) repeats a wording already in FACTS F16. Four numbers lack a FACTS row: 0.7159, 3.330 and 3.327, 118 of 120 human reward cartels, and "460 to 510 decisions" (derivable from F28's pair-periods). |
| Someone else's work as ours | yes | none. Design, payoff table and human values are credited to Bigoni et al.; the harness contains no third-party code markers; the LLM Usage Statement names Claude Code for code and drafting. Note for repository hygiene: 82 commits on the backend branch carry the author name "Claude", which the LLM statement covers but CLAUDE.md's no-AI-traces rule may not want in the public history. |

## Deep dive on the submission (separate packets)

Each juror read the full submission text (author, name and repository link blanked) and the printed page with Table 3 and Figure 1, in a fresh context without competitors. Raw answers: `roh/R03/detail-J*.json`, input `roh/R03/detail-submission-rendered.md`, crop of the overlap `roh/R03/figure1-overlap-crop.png`.

| Question | Li | Gupta | Cosio | Prabhakar | Beshane | Consensus |
|---|---|---|---|---|---|---|
| Scores now (I / E / P) | 4 / 4 / 3 | 4 / 4 / 3 | 4 / 4 / 3 | 4 / 4 / 3 | 4 / 4 / 3 | 4 / 4 / 3, 5 of 5 |
| First 30 seconds match the title | partly | partly | partly | partly | partly | partly, 5 of 5 |
| Title works | partly | partly | partly | partly | partly | partly, 5 of 5 |
| Second model finding | punchline | punchline | punchline | punchline | punchline | second punchline, 5 of 5 |
| Replication, extension or new | extension | extension | extension | extension | extension | extension, 5 of 5 |
| Controls table | yes | yes | yes | yes | yes | yes |
| Placebo arm | yes | yes | yes | yes | yes | yes |
| Shifted grid | partly | yes | partly | yes | yes | yes, 3 of 5 |
| n-table | partly | yes | partly | partly | yes | partly, 3 of 5 |
| Pre-registration hash | yes | yes | yes | yes | partly | yes, 4 of 5 |
| No absolutes | partly | partly | partly | partly | partly | partly, 5 of 5 |
| Figure 1 honest and readable | partly | partly | partly | partly | partly | partly, 5 of 5 |

- **What sticks in 30 seconds (all five, nearly in the same words).** Haiku forms cartels as often as the students but does not undercut them, and told fines, leniency and rewards deter it far more than they deterred people; three add "2 of 7 reproduce". The Sonnet result does not stick from title and abstract alone.
- **Title.** All five: the substance is right, but about 30 words, two claims and a slogan; "what survives holds its price, with or without a word" is cryptic before the Sonnet section and joins two different things (Haiku cartels near 9, Sonnet's silent 5.5 to 6.3; Li). Their options: "Same Game, Different Players: Cartel Enforcement Deters LLM Pricing Agents More Than People, but Not Silent Coordination" (Li); "Told Fines and Leniency Deter LLM Pricing Agents More Than People, but Surviving Cartels Hold the Monopoly Price" (Cosio); "Same Game, Different Players: Cartel Fines, Leniency and Rewards on LLM Pricing Agents Against a Human Baseline" (Gupta); "Fines, Leniency and Rewards on LLM Pricing Agents: A Human-Calibrated Replay of a Cartel Experiment" (Beshane); "Do Antitrust Instruments Deter LLM Cartels? Replaying a Human Leniency Experiment with Claude Pricing Agents" (Prabhakar).
- **Sonnet result.** All five call it a second punchline, not a dilution: enforcement that works through reports is blind to coordination without messages, the finding closest to oversight evasion (Li, Cosio, Beshane). All five want it in its own short subsection after the Haiku results, with one hedged abstract sentence; Gupta and Prabhakar would take it out of the title. All five name the weakness: 2 pools, no intervals, and no Sonnet no-channel arm, while Haiku without a channel prices 5.26 and humans under fine 5.35, so "coordination" could be a pricing prior or failure to best-respond.
- **Overclaims named by all or nearly all.** "Shows that recall does not drive the numbers" (5); "any model before agents reach a market" (5); Sonnet "coordination ... beyond the reach of these instruments" (5); mechanism sentences while reasons are not analysed (5); "first measurement" without "to our knowledge" (4); "the word prohibited removes about half" when the placebo keeps the whole authority text (4); "deters more than people" as a point comparison without human variance or a test (4); "H2 holds weakly" for a tie (Gupta, Cosio).
- **Gaps.** Which arms were pre-registered and which exploratory (4); no variance on the human side (4); Sonnet without intervals and no-channel baseline (5); one provider (5); four clusters for a percentile bootstrap (3); reasons not analysed (3).
- **Biggest risk.** Three of five: the visible contradictions in a paper that sells rigor make a careful judge distrust every number (Gupta, Cosio, Beshane). Li: deterrence may be safety-trained compliance with "prohibited". Prabhakar: "more than people" rests on 4 pools and 4 to 10 cartels.

## Summary test

A reader in a fresh context got only the submission text. Main claim: "Told-only fines, leniency and reward rules deter explicit cartels among LLM pricing agents much more than they deterred human subjects, but the cartels that do survive keep the monopoly price, and one model keeps prices supracompetitive with no communication at all, which these instruments cannot reach." Against the Message in CORE_IDEA.md (replay with identical rules; where the instruments work on agents as on humans and where they flip): the comparison, the flip, the audience (competition authorities) and the limits arrive, and the Sonnet result reaches the reader as the second half of the claim. One risk for Impact: the reader's first sentence calls the work "a replication", not a testbed; the introduction's contributions list could say "testbed" before "replay".

## Change since the previous round

Previous: R02-report-draft-2026-10-24.md. Setup differs: Konkurrenz 3 gleich, 1 neu, 1 weg. Read the changes with care.

| Entry | Total | Rank | Dimension 1: Impact Potential & Innovation | Dimension 2: Execution Quality | Dimension 3: Presentation & Clarity |
|---|---|---|---|---|---|
| CartelBench | 33.3 → 40 (+6.7) | 2/5 → 1/5 | 4 → 4 | 3 → 4 | 3 → 4 |

Execution and Presentation each rose from 3 to 4 in the scoring round because the R02 gaps are closed: known-effect arms, placebo, shifted grid, pre-registration hash, second model and the extra arms are in, the body fits 8 pages, and no placeholder is left. The R02 deep dive predicted 4 / 4 / 4 once filled and cut; the R03 deep dive confirms 4 for Impact and Execution but gives Presentation 3, because the layout and the new contradictions only show in the full text. The field moved too: the carrier study rose from 33.3 to 36.7, and the spy entry was rescored on a newer state (55553c0), still without a real run.

## The three most effective improvements

All three without a new experiment, together within two hours, sorted by effect.

1. **Correct the numbers and the pre-registration sentence (Execution; 5 of 5 deep-dive jurors list the contradictions, all name them the biggest risk or among the fixes, gain "half point" from four).** Table 3 and the leniency text: the run has 9 convictions, 3 by detection and 6 by report, with 7 firm reports and fines of 2,400 points (`summary.json` of the leniency run: n_convictions 9, n_detections 3, n_reports 7, fines_paid_total 2,400). One report event was probably a double report; the backend confirms. Write "9 (3 / 6), 7 reports" and "6 of 9 convictions by report". NoReport: the same sign and the same interval in text and Figure 1 (text +0.25 [+0.10, +0.40], panel 7 -0.25 [-0.41, -0.10]). Panel 7: say in the caption that the human fine value there (5.03) comes from the paper's NoReport comparison, not Table 2 (6.14). Methods: Result 7 is tested, only Result 8 is not testable. Name the laissez-faire core run as the positive control and the pilot as the model filter. State the formation-rate denominator (pair-periods without a running cartel; leniency 5 of 247). Print 3 decimals where an interval touches zero (Results 3 and 6). Replace "Nothing changed after the first call" (see red lines). Shows in: Table 3, Results, Methods, Figure 1 caption.
2. **Repair the printed layout and shorten the title (Presentation; 5 of 5 rate the title "partly" and Figure 1 "partly", 4 of 5 name Table 3).** Widen the Calls and USD columns of Table 3 so "4,376" and "0.92" do not wrap, move the difference labels in Figure 1 below the tick labels, and cut the title under about 15 words; the jurors' options are in the deep-dive section. Expected gain: Presentation 3 to 4 in the full read (+1, +3.3 total). Shows in: page 1, page 7.
3. **Scope the claims and label the Sonnet result (Execution, protects Impact; 5 of 5 list the same overclaims).** "To our knowledge" before "first measurement"; drop "any model"; the shifted grid "shows recall does not drive the numbers" becomes "behaviour is unchanged within the registered margins"; mechanisms (invitation to collect, the clone's expectation, incentives versus undercutting) as interpretation; "the word prohibited" becomes "the authority text without a penalty"; human values as point estimates without a test; Sonnet in its own short subsection marked exploratory (2 pools, no intervals, no Sonnet no-channel arm, Haiku without a channel prices 5.26 and humans under fine 5.35). Mark which arms were pre-registered and which came with Amendment 3. Expected gain: keeps Execution at 4 against a careful reader; Li, Gupta and Beshane rate it "half point" or "small".

## Was die Jury in jedem Fall sehen will

- **Zahlen widerspruchsfrei zwischen Abstract, Text, Tabellen, Abbildung und Bildunterschrift** (5 von 5 Detailprüfern fanden dieselben vier Widersprüche): Kronzeugen-Verurteilungen, NoReport-Intervall, menschlicher Bußgeld-Kartellpreis in Panel 7, Ergebnis 7 testbar oder nicht. Ort: Tabelle 3, Results, Methods, Figure 1.
- **Druckbild ohne Bruch** (5 von 5 zu Figure 1, 4 von 5 zu Tabelle 3): keine umbrechenden Zahlen in Tabellenspalten, keine Beschriftung über Achsenbeschriftung. Ort: Seite 7.
- **Titel unter etwa 15 Wörtern mit einer Aussage** (5 von 5 „partly“). Ort: Seite 1.
- **Vorregistriert und explorativ getrennt** (4 von 5 fragen danach): welche Arme in der Vorregistrierung standen, welche mit Amendment 3 kamen, und dass Hypothesen und Entscheidungsregeln unverändert blieben. Ort: Methods.
- **Keine Aussage über das Gemessene hinaus** (5 von 5): kein „first“ ohne „to our knowledge“, kein „any model“, Mechanismen als Deutung, Mensch-gegen-Agent als Punktvergleich ohne Test. Ort: Abstract, Discussion.
- **Sonnet-Befund als eigene, explorative Unterziffer mit Baseline-Vorbehalt** (5 von 5 „second punchline“, 4 von 5 vermissen die Sonnet-Variante ohne Kanal). Ort: Results.
- Weiter offen, mit neuem Lauf: zweiter Anbieter (5 von 5), mehr Seeds und mehr Kartelle unter Kronzeuge und Belohnung (5 von 5), Begründungen der Agenten auswerten (Li, Cosio), Permutationstest über Pools (Gupta, Prabhakar).

## Notes for the main session

- **Scale, weights, jurors as in R01 and R02.** Official 1 to 5 levels, equal weights; totals run from 10 to 50.
- **State judged.** Submission PDF at 19890c4 (the final title of DECISIONS 2026-10-25 00:05; body identical to 597e56c apart from the title, one abstract sentence and the closing sentence), harness at backend c14c944.
- **Dossiers.** Three competitor dossiers reused (repositories unchanged since R02); the spy entry moved (506e3d1 to 55553c0) and got a new dossier, mole-in-the-market-1025. Our dossier eigen-submission is new; before the packets were built, the jury session added one line with Sonnet's average prices (5.54 to 6.29), a main result of the abstract that the writer had left out.
- **Scoring round versus full read.** The dossier hides the printed layout, so the scoring round's Presentation 4 is an upper bound; the full read gives 3 from all five. The three formation-versus-incidence complaints in the scoring round partly come from the dossier listing laissez-faire formation (0.716) next to placebo incidence (0.714); the PDF itself labels both, but the placebo paragraph uses incidence only.
- **For the report session, in this order.** The pre-registration sentence; the leniency split; the NoReport sign and bound; the panel 7 human value in the caption; Result 7 testable in Methods; the positive-control naming; formation denominators; Table 3 column widths; Figure 1 label overlap; the title; the overclaim list; Sonnet as an exploratory subsection; pre-registered versus Amendment 3 arms. All without a new run.
- **For the backend session.** Confirm the leniency report split (one double report?) from `periods.jsonl`; confirm the NoReport interval used by the figure and by F34.
- **For FACTS.** Four numbers in the PDF have no FACTS row: 0.7159; 3.330 and 3.327; 118 of 120 human reward cartels reported in their first period; 460 to 510 Sonnet decisions. F16's "9 convictions (3 detections, 7 reports)" should read "9 convictions (3 by detection, 6 by report; 7 reports)" once the backend confirms.
- **For Julian.** The title (five options above; all five jurors find the current one too long), and whether the 82 commits authored "Claude" on the backend branch stay in the public history.

## Limits

- The personas are assumptions from public professional profiles (`private/JUDGES.md`). Real judges have their own day, read decks and watch videos, and talk to each other.
- Language models prefer polished text. Every entry was therefore reduced by the same brief to content, evidence and demo; style should not count, but some of it remains.
- All simulated jurors share one model. Repeated runs show sampling noise, not how much real judges disagree; the real spread is larger.
- Dossiers rest on what was visible (public repos, our own material). Competitors change until the deadline.
- Use the numbers to compare entries and to find weaknesses. They do not predict a placement.

## Data

```json
{"runde": "R03", "datum": "2026-10-25", "gegenstand": "submission", "stand": "submission PDF at commit 19890c4 (title of DECISIONS 2026-10-25 00:05; body as 597e56c), harness at backend c14c944", "modus": "schnell", "modell": "claude-opus-5-5 (session default)", "laeufe": 1, "juroren": ["Jasmine Li", "Debayan Gupta", "Luis Cosio", "Kaushik Prabhakar", "Neeraj Kumar Singh Beshane"], "kriterien": [{"name": "Dimension 1: Impact Potential & Innovation", "gewicht": 33.33, "wortlaut": "How much would this matter for the field if it worked? How innovative is it? For scores of 4-5: is this actually new to the field, or replicating recent work?\" 1 \"Negligible. No clear problem addressed, or no meaningful novelty.\" 2 \"Limited. Addresses a real problem but with a generic or well-trodden approach. Incremental at best.\" 3 \"Moderate. Clear problem with a reasonable approach; some novelty in framing or method beyond routine application of existing tools.\" 4 \"Significant. Important problem with an original approach, or identifies a neglected problem area. A valuable contribution others could build on.\" 5 \"Exceptional. Tackles a critical problem with a genuinely novel approach, or opens a new research direction. Clear theory of change. You'd be excited to share this with researchers in the area.", "id": "C1"}, {"name": "Dimension 2: Execution Quality", "gewicht": 33.33, "wortlaut": "How sound are methodology, implementation, and findings?\" 1 \"Seriously flawed. Methodology broken, results uninterpretable, or implementation doesn't work.\" 2 \"Weak. Approach has significant gaps: missing validation, flawed experimental design, or incomplete implementation.\" 3 \"Competent. Technically solid given the short duration. Methodology makes sense, results are interpretable, limitations acknowledged, work builds toward clear conclusions.\" 4 \"Strong. Thorough methodology with convincing validation. Results clearly support conclusions. Immediately useful for future work.\" 5 \"Exceptional. Ambitious scope executed rigorously. Surprising findings, novel methods, or unusually robust validation.", "id": "C2"}, {"name": "Dimension 3: Presentation & Clarity", "gewicht": 33.34, "wortlaut": "How clearly are work, findings, and impact potential communicated?\" 1 \"Incomprehensible. Cannot determine what the project is actually claiming or doing.\" 2 \"Hard to follow. Key information buried, missing, or diluted by excessive length. Significant effort to extract main points.\" 3 \"Clear enough. Can understand the problem, approach, and results without undue effort. Core content clearly present: problem, method, findings, limitations.\" 4 \"Well presented. Easy to follow, well-structured, appropriate level of detail. Target audience would get it quickly.\" 5 \"Exceptionally clear. A pleasure to read. Complex ideas made accessible. Could serve as a model for how to present this type of work.", "id": "C3"}], "bonus": [], "tokens": 375222, "eintraege": {"eigen-submission": {"name": "CartelBench", "eigen": true, "art": "built", "rang": null, "quelle": "submission PDF at commit 19890c4, harness snapshot at backend commit c14c944", "stand": "2026-10-25", "gesamt": {"median": 40.0, "q1": 40.0, "q3": 40.0, "min": 36.67, "max": 40.0, "n": 5}, "kriterien": {"C1": {"median": 4, "q1": 4.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}, "C2": {"median": 4, "q1": 4.0, "q3": 4.0, "min": 4, "max": 4, "n": 5}, "C3": {"median": 4, "q1": 4.0, "q3": 4.0, "min": 4, "max": 4, "n": 5}}, "bonus": null, "rang_median": 1.0, "top3": 1.0}, "vector-channel-countermeasures": {"name": "vector-channel-countermeasures", "eigen": false, "art": "built", "rang": 1, "quelle": "groothaha/vector-channel-countermeasures@7d1bd90", "stand": "2026-10-24", "gesamt": {"median": 36.67, "q1": 36.67, "q3": 36.67, "min": 33.33, "max": 36.67, "n": 5}, "kriterien": {"C1": {"median": 3, "q1": 3.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}, "C2": {"median": 4, "q1": 3.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}, "C3": {"median": 4, "q1": 4.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}}, "bonus": null, "rang_median": 2.0, "top3": 1.0}, "plus-factors-on-the-ledger": {"name": "plus-factors-on-the-ledger", "eigen": false, "art": "built", "rang": 2, "quelle": "saltxd/plus-factors-on-the-ledger@6734c0c", "stand": "2026-10-24", "gesamt": {"median": 30.0, "q1": 30.0, "q3": 33.33, "min": 30.0, "max": 33.33, "n": 5}, "kriterien": {"C1": {"median": 3, "q1": 3.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}, "C2": {"median": 3, "q1": 3.0, "q3": 3.0, "min": 3, "max": 3, "n": 5}, "C3": {"median": 3, "q1": 3.0, "q3": 3.0, "min": 3, "max": 3, "n": 5}}, "bonus": null, "rang_median": 3.0, "top3": 1.0}, "mole-in-the-market-1025": {"name": "mole-in-the-market", "eigen": false, "art": "built", "rang": 14, "quelle": "adamattar-pixel/mole-in-the-market@55553c0", "stand": "2026-10-24", "gesamt": {"median": 20.0, "q1": 16.67, "q3": 20.0, "min": 16.67, "max": 23.33, "n": 5}, "kriterien": {"C1": {"median": 3, "q1": 3.0, "q3": 3.0, "min": 2, "max": 3, "n": 5}, "C2": {"median": 1, "q1": 1.0, "q3": 1.0, "min": 1, "max": 2, "n": 5}, "C3": {"median": 2, "q1": 2.0, "q3": 2.0, "min": 1, "max": 2, "n": 5}}, "bonus": null, "rang_median": 5.0, "top3": 0.0}, "cartel-rivalry-study": {"name": "cartel-rivalry-study", "eigen": false, "art": "built", "rang": 3, "quelle": "horigyns/cartel-rivalry-study@b3f62d8", "stand": "2026-10-24", "gesamt": {"median": 26.67, "q1": 26.67, "q3": 30.0, "min": 26.67, "max": 30.0, "n": 5}, "kriterien": {"C1": {"median": 3, "q1": 3.0, "q3": 4.0, "min": 3, "max": 4, "n": 5}, "C2": {"median": 3, "q1": 3.0, "q3": 3.0, "min": 3, "max": 3, "n": 5}, "C3": {"median": 2, "q1": 2.0, "q3": 2.0, "min": 2, "max": 2, "n": 5}}, "bonus": null, "rang_median": 4.0, "top3": 0.0}}, "roh": {"J1-L1": {"eigen-submission": {"C1": 4, "C2": 4, "C3": 4}, "vector-channel-countermeasures": {"C1": 4, "C2": 3, "C3": 3}, "cartel-rivalry-study": {"C1": 3, "C2": 3, "C3": 2}, "mole-in-the-market-1025": {"C1": 2, "C2": 1, "C3": 2}, "plus-factors-on-the-ledger": {"C1": 3, "C2": 3, "C3": 3}}, "J2-L1": {"vector-channel-countermeasures": {"C1": 3, "C2": 4, "C3": 4}, "eigen-submission": {"C1": 4, "C2": 4, "C3": 4}, "mole-in-the-market-1025": {"C1": 3, "C2": 2, "C3": 2}, "cartel-rivalry-study": {"C1": 4, "C2": 3, "C3": 2}, "plus-factors-on-the-ledger": {"C1": 3, "C2": 3, "C3": 3}}, "J3-L1": {"mole-in-the-market-1025": {"C1": 3, "C2": 1, "C3": 2}, "vector-channel-countermeasures": {"C1": 4, "C2": 3, "C3": 4}, "cartel-rivalry-study": {"C1": 3, "C2": 3, "C3": 2}, "plus-factors-on-the-ledger": {"C1": 4, "C2": 3, "C3": 3}, "eigen-submission": {"C1": 3, "C2": 4, "C3": 4}}, "J4-L1": {"eigen-submission": {"C1": 4, "C2": 4, "C3": 4}, "mole-in-the-market-1025": {"C1": 3, "C2": 1, "C3": 1}, "vector-channel-countermeasures": {"C1": 3, "C2": 4, "C3": 4}, "plus-factors-on-the-ledger": {"C1": 3, "C2": 3, "C3": 3}, "cartel-rivalry-study": {"C1": 4, "C2": 3, "C3": 2}}, "J5-L1": {"plus-factors-on-the-ledger": {"C1": 4, "C2": 3, "C3": 3}, "cartel-rivalry-study": {"C1": 3, "C2": 3, "C3": 2}, "mole-in-the-market-1025": {"C1": 3, "C2": 1, "C3": 2}, "eigen-submission": {"C1": 4, "C2": 4, "C3": 4}, "vector-channel-countermeasures": {"C1": 3, "C2": 4, "C3": 4}}}}
```
