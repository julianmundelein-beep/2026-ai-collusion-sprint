# STATUS · AI Collusion Research Sprint

> Control file of the main session. Every session reads it first. Only the main session edits it, except the section "Für die Skills" at the end, where every session may append one line.
> Main folder: `/Users/julianmundelein/Projects/2026-ai-collusion-sprint` · Set up: 2026-10-24 · Updated: 2026-10-25 13:10 HKT by the main session

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
- [x] Tests green (51, F23)
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
| 3 | Jury | jury-simulation | main folder | private/reviews/ | Claude | R05 done (7cc61d3): final PDF 4 / 4 / 4 (Presentation 3 to 4 against R03); 10 text to-dos; new runs ranked N2, N5, N1 plus scripted-partner control | local_525668aa-4f92-4e55-8006-1293f749dce9 |
| 4 | Website | design-taste-frontend | own worktree or cloud | web/ (branch) | | dropped (not a deliverable) | |
| 5 | Backend | hackathon-backend | cloud (claude.ai/code), branch `backend` | `cartelbench/` on its branch, README, docs/ | Claude (cloud) | done: round 4 (K1, K2, prompt robustness, K3 price screen, ledger) merged 62fd43e; provider2 (Qwen2.5-32B, Llama-3.1-8B on Modal) merged d6075d5; 60 tests green; 47.18 USD Anthropic, 8.98 USD Modal | cloud |
| 6 | Pitch deck | pitch-deck | main folder | private/deck/ | | dropped (not a deliverable) | |
| 7 | Demo video | video-studio | main folder | private/video/ | | optional (3 to 5 min, decide after R02 and the clock) | |
| 8 | Design | hackathon-design | main folder | DESIGN.md, private/design/ | | optional (only if figures or video need a look) | |
| 9 | Report (paper) | none (skills klare-einreichung, docx) | main folder | paper/report.docx (source), paper/report.md (mirror), paper/report.pdf | Claude | final title in (19890c4); applying the R03 levers (numbers, pre-registration sentence, layout, scoping, Sonnet as exploratory subsection); title length waits for Julian | local_d6d6a6d7-12df-4407-b0dd-9efb32c204cd |

Rows the deliverables in HACKATHON.md do not need are set to `dropped` after the research (row 9 only runs when a report is required).

States: not started · running · waiting for Julian · done · archived · handed to a teammate · dropped

## Artifacts: one source each

Every deliverable from HACKATHON.md, the one place it is made, and who makes it. A second copy is never edited.

| Deliverable | The one source | Session or person | State | Final file submitted |
|---|---|---|---|---|
| Research report (PDF, official template, max 8 pages before references and appendices, plan 4 to 6; abstract 150 to 250 words; authors and affiliations; appendix "Limitations and Dual-Use / Ethical Considerations"; LLM Usage Statement; at least one figure) | `paper/report.docx` on the .docx copy of the official template (Google Doc only if Julian asks); PDF export `paper/report.pdf` is the submission; file `paper/CartelBench_AI-Collusion-Research-Sprint_2026.pdf` | 9 Report | complete draft 597e56c, 8 pages, all arms in | |
| Figure 1 (scorecard dot plot) | `paper/figure1.py` rendered from the backend's `scorecard.json` and `analyze_core_bootstrap.txt` (F19); the backend's own figure files are data, not the report figure | 9 Report (data: 5 Backend) | drawn 7c89414 | |
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
| Numbers consistent across abstract, text, tables, figure and caption: leniency convictions 9 (3 by detection, 6 by report; 7 reporters), NoReport sign and interval, human fine value in panel 7, Result 7 tested and Result 8 not testable | jury R03 (5 of 5) | Table 3, Results, Methods, Figure 1 | open (report) |
| Pre-registration sentence true: amendment 2 before the first paid call, amendment 3 (placebo, second model, pools of 10) after it; hypotheses and decision rules unchanged; pre-registered versus exploratory arms marked | jury R03 (red line) | Methods | open (report) |
| Print layout: no wrapping numbers in Table 3, no label overlap in Figure 1 | jury R03 (5 of 5) | page 7 | open (report) |
| Title under about 15 words with one claim | jury R03 (5 of 5) | page 1 | Julian decides |
| Claims scoped: "to our knowledge", no "any model", mechanisms as interpretation, human values as point estimates; Sonnet as an exploratory subsection with the no-channel caveat | jury R03 (5 of 5) | abstract, Results, Discussion | open (report) |
| No "[F??]" in the PDF: every gap filled or marked "not run"; pre-registration hash with timestamp (F20) | jury R02 (5 of 5) | whole report | done 597e56c, none left |
| Known-effect arms and shifted-grid result reported even if unfavourable | jury R02 (5 of 5) | Table 1, contamination section | done 597e56c |
| Placebo arm: full authority text with prohibition but zero penalty, to separate deterrence from the word "prohibited" | jury R02 (4 of 5) | Table 1 or 2, Discussion | done 597e56c |
| n-table stays in the body, slim | jury R02 (5 of 5) | Results | done 7c89414 |
| Numbers consistent: seeds, convictions, costs, pilot count, one measure throughout | jury R02 (4 of 5) | Methods, Table 3, Appendix C, abstract | done 7c89414 |
| Figure 1 honest and legible: no data in untested panels, plain axis labels, regime difference with interval per panel, Stockholm-Rome span defined in Methods | jury R02 (5 of 5) | Figure 1, Methods | done 7c89414 (paper/figure1.py) |
| No absolutes and no "LLMs" from one model: drop "never", scope to the tested model until a second provider runs | jury R02 (5 of 5) | title, abstract, conclusion | done 7c89414 |
| Explain the coincidences: 0.716 formation in laissez-faire for humans and agents, 3.33 under leniency and reward, collapsing reward intervals | jury R02 (4 of 5) | Results | done 7c89414 (rounding 0.7159; 3.330 and 3.327 are prices without cartels) |
| PDF text layer: fi and fl ligatures lose their Unicode mapping (pdftotext reads "ne" for "fine"); export with a ToUnicode-mapped font or ligatures off | jury session (machine readability) | export | done 7c89414 (fonts without liga feature; pdftotext 0 hits) |

## Waiting for

- Julian: shorter title (jury R03 options) or keep; decide whether the 82 cloud commits authored "Claude <noreply@anthropic.com>" stay in the public history (rewriting would change the pre-registration hashes cited in the report)
- Julian: licence (gate open since 2026-10-24)
- Report session: apply title, affiliation and the cut to 8 pages (sent 19:55 HKT)
- Julian: tell the cloud backend session that Figure 1 should be a 4x2 grid or use larger type (2x4 is too small at 6.5 inch width)
- Julian: confirm the main-model rule (Haiku 5.5 as main model if it passes the pilot, Sonnet 5.5 as one V4 culture with 10 duopoles) and the project name (CartelBench recommended)
- Julian: Modal account and credits (form in the inbox, per Discord) for the second provider in V4; the cloud environment reaches only api.anthropic.com, so V4 runs locally
- Julian: Discord check (keys from the organizers, Modal credit redemption, pinned announcements), send the email draft in HACKATHON.md
- Julian: tell the cloud backend session that `ANTHROPIC_API_KEY` is set (entered 2026-10-24 16:55 HKT; the VM reads it after its next pause) and to merge main for the jury notes; licence decided later, before submission
- Julian: pick project name, one sentence, why sentence, slogan from CORE_IDEA.md "Message"
- Julian: Anthropic API key into the backend's compute.env when the session asks

## Next step

Round 5 runs (DECISIONS 11:15): cloud backend registers amendment 6 and runs N2, N5 and the Claude cells of the scripted-partner control on branch `backend`; local session provider2 runs N1 and the Qwen and Llama control cells on Modal after amendment 6 is on origin/backend. Then the report session applies the ten R05 to-dos and the new numbers in one pass; then the close-out resumes (SUBMISSION.md, removal of internal files, repo public). Licence done (405ee0f). Video in the cloud on branch `video`.

## Für die Skills

Append only, every session, one line each: `YYYY-MM-DD · <session> · <skill> · <problem> · <suggestion>`. Skills are not changed during the hackathon; afterwards a skill workshop session in `~/claude-tools` works through this list.

- 2026-10-24 · Ideen · hackathon-ideen · Research-Sprint-Format: Kurzkarte und Prüfkarte kennen keine Felder für Forschungsfrage, Hypothese, Variable, Metrik, Baseline mit Positivkontrolle, Runs und Seeds, Kosten, Null-Ergebnis-Risiko, Replikationsprüfung gegen Vorarbeiten; Kurzform erlaubt nur zwei Tracks, der Auftrag nannte drei · Variante „Research Sprint" im Skill: diese Felder in die Kurzkarte, Prüfskript liest sie, Trackzahl in der Kurzform als Parameter; Platzhalter „–" in der Vorlage (Nichtkunden-Ebene, „0–5") verstößt gegen die Gedankenstrich-Regel des Dateivertrags, Vorlage auf „keine" und „0 bis 5" ändern
- 2026-10-24 · Jury · jury-simulation · `runde.py` liest „not published (plan: equal)“ nicht als Gewicht und bricht ab; die Juroren-Vorlage erzwingt 0 bis 10 und „Total 0 to 100“, obwohl die Rubrik 1 bis 5 mit wörtlichen Stufen hat (hier per `--rubrik` JSON und Nachbearbeitung der Pakete gelöst) · Option `--gleich` für gleiche Gewichte bei unveröffentlichten Gewichten; Skala aus der Rubrik übernehmen (`--skala 1-5`), Totaltext danach richten
- 2026-10-24 · Jury · jury-simulation · Kein Paket für ideenspezifische Fragen (Replikation oder neu, trägt die Positivkontrolle, Streichreihenfolge); Juroren bewerten Ideen in Dimension 2 nach dem Stand statt nach dem Potenzial · eigener Pakettyp „Detailprüfung“ je Juror (wie die Vortragsprüfung, frischer Kontext, ohne Konkurrenz) mit Auswertung im Bericht; Hinweis in der Vorlage schärfen, dass Ideen in Execution nach dem Plan bewertet werden
- 2026-10-24 · Bericht · klare-einreichung · `pruefen.py --rubrik` verlangt je Kriterium eine eigene Überschrift, obwohl die offizielle Vorlage die Gliederung vorgibt und der Skill selbst sagt, dass die Kriterien dann als Unterpunkte hineinkommen; im Report steht deshalb eine dreizeilige Leseanleitung mit den Kriteriennamen, damit kein FEHLT bleibt · Option `--rubrik-unterpunkte`: Kriterium gilt als abgedeckt, wenn sein Name in einer Zeile unter 120 Zeichen vorkommt; Glossar-Warnung „Begriffe nicht benutzt“ listet auch benutzte Begriffe (research question, positive control), weil die ganze Tabellenzelle gesucht wird, besser je Begriff vor dem Semikolon prüfen
- 2026-10-24 · Backend (cloud) · hackathon-backend · Die Standard-Cloud-Umgebung erreicht keine Verlags- und Preprint-Server (hhs.se, ifn.se, cepr.org, ssrn.com, arxiv.org); das Backend musste die Auszahlungstabelle des Quellpapiers aus vier Ankerwerten rekonstruieren statt sie abzuschreiben · Abschnitt „In der Cloud“: die Hauptsession legt Quellpapiere und Vorlagen vor dem Start einer Cloud-Backend-Session unter hackathon/private/sources/ ab und pusht main; BUILD_PLAN-Vorlage bekommt eine Zeile „Quellen im Checkout“
- 2026-10-25 · Jury · jury-simulation · Reine Detailrunden (R04 „was fehlt für eine 5“, Kandidatenbewertung) kennt `runde.py` nicht: kein Pakettyp, kein Bericht-Gerüst, kein Datenblock, sodass die nächste Bewertungsrunde keinen Vorrundenvergleich findet · Pakettyp `detail` mit Fragenkatalog als Datei (`--fragen`), Auswertung zu Konsens-Tabellen und ein Datenblock, der auf die letzte Bewertungsrunde verweist
- 2026-10-25 · Zweiter Anbieter · hackathon-backend · Modal startet GPU-Funktionen erst mit hinterlegter Zahlungsmethode, auch wenn Sprint-Credits da sind (alle GPU-Typen); vLLM 0.31 im debian_slim-Image stürzt beim Start ab, weil der FlashInfer-Sampler nvcc per JIT braucht · Abschnitt „Offene Modelle auf Modal“: Zahlungsmethode vor dem Start prüfen lassen (Credits decken die Läufe), Gewichte per CPU-Funktion ins Volume laden, VLLM_USE_FLASHINFER_SAMPLER=0 setzen oder CUDA-devel-Image nehmen; Startbefehl in zsh als Funktion statt als Variable
- 2026-10-25 · Backend (cloud) · hackathon-backend · Parallele Läufe teilen sich das Org-Limit für gleichzeitige Requests über alle Modelle; 9 Läufe mit zusammen 44 Requests liefen nach den SDK-Retries in 429-Fehler (4.23 USD verloren, Läufe abgebrochen und neu gestartet), weil der Skill nur Rate-Limits je Plattform nennt · in BUILD_PLAN-Vorlage und Abschnitt „Plattformgrenzen“ eine Zeile „gleichzeitige Requests je Organisation, Summe über alle parallelen Läufe“ mit Startwert 20 und einem Wächter, der Fehler im Log sofort meldet; Launch-Log (Start- und Endzeile je Lauf) als Standard, damit Abbrüche im Ledger stehen
