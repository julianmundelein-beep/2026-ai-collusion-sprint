# STATUS · AI Collusion Research Sprint

> Control file of the main session. Every session reads it first. Only the main session edits it, except the section "Für die Skills" at the end, where every session may append one line.
> Main folder: `/Users/julianmundelein/Projects/2026-ai-collusion-sprint` · Set up: 2026-10-24 · Updated: 2026-10-24 19:30 HKT by the main session

## Clock

| | Official (time zone) | Julian (HKT, UTC+08:00) | Source |
|---|---|---|---|
| Submission deadline | Sun 2026-10-25 23:59 AoE (UTC-12) = Mon 2026-10-26 11:59 UTC | Mon 2026-10-26 19:59 HKT | Sprint page, Guidelines tab (2026-10-24) |
| Internal deadline (official minus 3 h) | Mon 2026-10-26 08:59 UTC | Mon 2026-10-26 16:59 HKT | |
| Registration deadline | none stated; sign-up open on the sprint page | | Sprint page (2026-10-24) |
| Next fixed time (check-in, pitch slot) | | | |

## Team

| Person | GitHub | Owns | Available |
|---|---|---|---|
| Julian | julianmundelein-beep | everything (solo team) | Sat 2026-10-24 to Mon 2026-10-26 16:59 HKT |

## Gates (in this order)

- [x] Team and eligibility checked (solo, open globally, no background required)
- [x] Rules researched: HACKATHON.md complete (`pruefen.py rahmen` passes 2026-10-24), official template found (Google Doc), copy in official/ pending Julian's download OK
- [ ] Registered; questions to the organizers sent, including mandatory content
- [x] Idea chosen: I24 Bigoni twin, CORE_IDEA.md written 2026-10-24 16:25 HKT, decision in DECISIONS.md 15:58 HKT
- [ ] Licence decided with the team (DECISIONS.md)
- [x] Toolchain proven: engine, tests, scripted players and real model calls (F01 to F06, F09)
- [x] Happy path runs end to end with real evidence (pilot F09, core runs F13 and F14, 2026-10-24)
- [ ] Tests green
- [ ] Deck, video and docs final; numbers checked against FACTS.md; talk time measured
- [ ] Repo closed out: SUBMISSION.md, DESIGN.md and everything else left in the tree in English, working notes, private/ and the session CLAUDE.md out of the tree (`pruefen.py abgabe` passes), repo public, release with video
- [ ] Every text a jury or AI pre-screen reads checked with the skill klare-einreichung (`pruefen.py` without FEHLT, summary test matches the message)
- [ ] Read by a person without context (first 30 seconds: what is it, does it run, what is proven)
- [ ] Red lines: no hidden instructions to AI graders, no invented or polished numbers, no one else's work as ours
- [ ] Submitted; confirmation received and noted in DECISIONS.md

## Session plan

At most two long build sessions plus one short session at the same time. One session per artifact. Finished sessions are archived. Areas a teammate owns get the teammate's name instead of a session.

| # | Session | Skill | Where | Writes | Owner | State | Session |
|---|---|---|---|---|---|---|---|
| 0 | Main session | hackathon-kickoff | main folder | STATUS, FACTS, CORE_IDEA; commits DECISIONS | Julian + Claude | running | AI Collusion Research Sprint · Hauptsession |
| 1 | Framework research | hackathon-kickoff (research) | main folder | HACKATHON.md, official/, private/JUDGES.md, private/COMPETITION.md | Claude | done (HACKATHON.md, JUDGES.md, COMPETITION.md, official/ committed); kept open for COMPETITION rescans | local_51c0819d-c7e3-4cb4-8036-c263bc6b9c22 |
| 2 | Ideas | hackathon-ideen | main folder | IDEAS.md | Claude | done (two rounds, 39 ideas, I24 chosen with build plan, commit d5e8cf9); archive on Julian's OK | local_4ab37d7f-a4ea-4382-9837-d275681d3cb0 |
| 3 | Jury | jury-simulation | main folder | private/reviews/ | Claude | R01 done (e9f0c70): idea rank 2 of 4, medians 4 / 2 / 3; stays open for R02 on the first running state | local_525668aa-4f92-4e55-8006-1293f749dce9 |
| 4 | Website | design-taste-frontend | own worktree or cloud | web/ (branch) | | dropped (not a deliverable) | |
| 5 | Backend | hackathon-backend | cloud (claude.ai/code), branch `backend` | `cartelbench/` on its branch, README, docs/ | Claude (cloud) | second cloud session running: four core regimes done with scorecard and Figure 1 (F13 to F19), branch `origin/backend` at 883ec87 (19:20 HKT); next: validation arms, second model, dose, NoReport, ReMatch, clone in cut order | cloud |
| 6 | Pitch deck | pitch-deck | main folder | private/deck/ | | dropped (not a deliverable) | |
| 7 | Demo video | video-studio | main folder | private/video/ | | optional (3 to 5 min, decide after R02 and the clock) | |
| 8 | Design | hackathon-design | main folder | DESIGN.md, private/design/ | | optional (only if figures or video need a look) | |
| 9 | Report (paper) | none (skills klare-einreichung, docx) | main folder | paper/report.docx (source), paper/report.md (mirror), paper/report.pdf | Claude | running (started 2026-10-24 19:05 HKT) | local_d6d6a6d7-12df-4407-b0dd-9efb32c204cd |

Rows the deliverables in HACKATHON.md do not need are set to `dropped` after the research (row 9 only runs when a report is required).

States: not started · running · waiting for Julian · done · archived · handed to a teammate · dropped

## Artifacts: one source each

Every deliverable from HACKATHON.md, the one place it is made, and who makes it. A second copy is never edited.

| Deliverable | The one source | Session or person | State | Final file submitted |
|---|---|---|---|---|
| Research report (PDF, official template, max 8 pages before references and appendices, plan 4 to 6; abstract 150 to 250 words; authors and affiliations; appendix "Limitations and Dual-Use / Ethical Considerations"; LLM Usage Statement; at least one figure) | `paper/report.docx` on the .docx copy of the official template (Google Doc only if Julian asks); PDF export `paper/report.pdf` is the submission; file `<ProjectTitle>_AI-Collusion-Research-Sprint_2026.pdf` | 9 Report | in progress | |
| Public GitHub repo (optional) | this repo; harness in `cartel/` (name per Julian's pick) on branch `backend`, README from the backend session | 5 Backend | not started | |
| Video demo, 3 to 5 min (optional, URL only, judges review the PDF) | private/video/ | 7 Demo video | optional | |
| Submission form: project summary, tracks, publishing yes/no, team name, location, member name, email, Discord, Scholar | SUBMISSION.md (draft texts), Julian fills personal fields | main session | not started | |

## Mandatory content

Everything the rules, the organizers or the jury simulation expect to see, and where we show it.

| What | From (rules, organizers, jury simulation) | Shown in | State |
|---|---|---|---|
| Appendix "Limitations and Dual-Use / Ethical Considerations": what the result does and does not establish, how setup or findings could ease real collusion or hinder detection | Guidelines, Submission Requirements | report appendix | open |
| Abstract 150 to 250 words, title, authors and affiliations | Guidelines | report page 1 | open |
| New work done during the sprint clearly separated from prior work; preexisting code marked in README and report | Guidelines, Important Notes | report Methodology, README | open |
| Results with variance, seeds, baselines and a positive control | Guidelines, Recommended Report Structure | report Results | open |
| Methodology detailed enough to replicate: models, prompts, environments, seeds, metrics | Guidelines | report Methodology, repo | open |
| Rubric: Impact Potential & Innovation, Execution Quality, Presentation & Clarity, each 1 to 5, no weights published | Guidelines, Judging Criteria | report structure | open |
| LLM Usage Statement, truthful; "Our main contributions are:" list; theory of change sentence | template, rubric | report last section, Introduction | open |
| Template conflicts (appendix heading, Methods vs Methodology, 4 vs 8 pages): keep template headings, add appendix with the exact Guidelines heading, plan 4 to 6 pages | HACKATHON.md, Official templates | report | decided by the research session, question in the mail |
| Candidates from the judges' profiles: false-positive rate next to detection rate, cost of the countermeasure to legitimate performance, threat model in security terms, reproducible harness | private/JUDGES.md | report Methods, Results, Discussion | candidate, confirm in R01/R02 |
| Candidate from the HK hub framing: one paragraph on what the result means for financial systems | aisafetyhk.org | report Discussion | candidate |
| n-table per regime and model: independent units (pool sessions), duopolies, periods, calls, refusals and parse errors with denominator, cost; how refusals enter each measure | jury R01 (5 of 5) | report Methods and Results | open |
| Pre-registration evidenced: commit hash and timestamp before the first API call, list of all deviations | jury R01 (5 of 5) | report Methods, repo | open |
| Contamination test with a pre-registered equivalence margin, reported even if it fails: shifted price grid (Nash and optimum move, not uniform rescaling), cloze probe on the paper's numbers | jury R01 (5 of 5) | report Results, own section | open |
| Positive and negative controls in one table or figure: scripted players through the same pipeline, known-effect arm, no-communication arm, laissez-faire with n and interval | jury R01 (5 of 5) | first figure or table in Results | open |
| Human versus LLM with Stockholm and Rome separate, cluster-bootstrap intervals, reproduction rule in the caption, three states (reproduced, not, not tested), "x of k tested" | jury R01 (5 of 5) | Figure 1 | open |
| One paragraph separating strategic deterrence from a reaction to the words fine, leniency, reward, since punishments are only told | jury R01 (4 of 5) | Discussion, Limitations appendix | open |
| Exact model IDs with date, verbatim prompts, seeds, one replication command | jury R01 (2 of 5) | appendix, README | open |
| Headline is the divergence from humans with a tested mechanism, not the reproduction count; at least two providers so the claim is about LLMs | jury R01 (5 of 5 levers) | title, abstract, contributions, Figure 1 caption | open |

## Waiting for

- Report session: draft with Results; then jury round R02 on the draft (Julian's decision 19:35 HKT)
- Julian: project name and affiliation for the report session
- Julian: confirm the main-model rule (Haiku 5.5 as main model if it passes the pilot, Sonnet 5.5 as one V4 culture with 10 duopoles) and the project name (CartelBench recommended)
- Julian: Modal account and credits (form in the inbox, per Discord) for the second provider in V4; the cloud environment reaches only api.anthropic.com, so V4 runs locally
- Julian: Discord check (keys from the organizers, Modal credit redemption, pinned announcements), send the email draft in HACKATHON.md
- Julian: tell the cloud backend session that `ANTHROPIC_API_KEY` is set (entered 2026-10-24 16:55 HKT; the VM reads it after its next pause) and to merge main for the jury notes; licence decided later, before submission
- Julian: pick project name, one sentence, why sentence, slogan from CORE_IDEA.md "Message"
- Julian: Anthropic API key into the backend's compute.env when the session asks

## Next step

Report session writes Results and the abstract from F13 to F19; jury round R02 on that draft; cloud backend runs the extras in cut order (validation arms first, then a second model for V4, dose, NoReport, ReMatch, clone); main session merges `refs/heads/backend` into main on Julian's word before the report is final.

## Für die Skills

Append only, every session, one line each: `YYYY-MM-DD · <session> · <skill> · <problem> · <suggestion>`. Skills are not changed during the hackathon; afterwards a skill workshop session in `~/claude-tools` works through this list.

- 2026-10-24 · Ideen · hackathon-ideen · Research-Sprint-Format: Kurzkarte und Prüfkarte kennen keine Felder für Forschungsfrage, Hypothese, Variable, Metrik, Baseline mit Positivkontrolle, Runs und Seeds, Kosten, Null-Ergebnis-Risiko, Replikationsprüfung gegen Vorarbeiten; Kurzform erlaubt nur zwei Tracks, der Auftrag nannte drei · Variante „Research Sprint" im Skill: diese Felder in die Kurzkarte, Prüfskript liest sie, Trackzahl in der Kurzform als Parameter; Platzhalter „–" in der Vorlage (Nichtkunden-Ebene, „0–5") verstößt gegen die Gedankenstrich-Regel des Dateivertrags, Vorlage auf „keine" und „0 bis 5" ändern
- 2026-10-24 · Jury · jury-simulation · `runde.py` liest „not published (plan: equal)“ nicht als Gewicht und bricht ab; die Juroren-Vorlage erzwingt 0 bis 10 und „Total 0 to 100“, obwohl die Rubrik 1 bis 5 mit wörtlichen Stufen hat (hier per `--rubrik` JSON und Nachbearbeitung der Pakete gelöst) · Option `--gleich` für gleiche Gewichte bei unveröffentlichten Gewichten; Skala aus der Rubrik übernehmen (`--skala 1-5`), Totaltext danach richten
- 2026-10-24 · Jury · jury-simulation · Kein Paket für ideenspezifische Fragen (Replikation oder neu, trägt die Positivkontrolle, Streichreihenfolge); Juroren bewerten Ideen in Dimension 2 nach dem Stand statt nach dem Potenzial · eigener Pakettyp „Detailprüfung“ je Juror (wie die Vortragsprüfung, frischer Kontext, ohne Konkurrenz) mit Auswertung im Bericht; Hinweis in der Vorlage schärfen, dass Ideen in Execution nach dem Plan bewertet werden
