# STATUS · AI Collusion Research Sprint

> Control file of the main session. Every session reads it first. Only the main session edits it, except the section "Für die Skills" at the end, where every session may append one line.
> Main folder: `/Users/julianmundelein/Projects/2026-ai-collusion-sprint` · Set up: 2026-10-24 · Updated: 2026-10-24 14:20 HKT by the main session

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
- [ ] Idea chosen: CORE_IDEA.md written, decision in DECISIONS.md
- [ ] Licence decided with the team (DECISIONS.md)
- [ ] Toolchain proven (hello world runs or is deployed)
- [ ] Happy path runs end to end with real evidence
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
| 1 | Framework research | hackathon-kickoff (research) | main folder | HACKATHON.md, official/, private/JUDGES.md, private/COMPETITION.md | Claude | waiting for Julian (template download OK, Discord check); HACKATHON.md, JUDGES.md, COMPETITION.md committed ac903d5 | local_51c0819d-c7e3-4cb4-8036-c263bc6b9c22 |
| 2 | Ideas | hackathon-ideen | main folder | IDEAS.md | Claude | waiting for Julian (which ideas to check fully, or round 2); round 1 committed 44785f6, 23 ideas, shortlist top 5 plus wildcard | local_4ab37d7f-a4ea-4382-9837-d275681d3cb0 |
| 3 | Jury | jury-simulation | main folder | private/reviews/ | | not started | |
| 4 | Website | design-taste-frontend | own worktree or cloud | web/ (branch) | | dropped (not a deliverable) | |
| 5 | Backend | hackathon-backend | own worktree or cloud | code folder on its branch, README | | not started | |
| 6 | Pitch deck | pitch-deck | main folder | private/deck/ | | dropped (not a deliverable) | |
| 7 | Demo video | video-studio | main folder | private/video/ | | optional (3 to 5 min, decide after R02 and the clock) | |
| 8 | Design | hackathon-design | main folder | DESIGN.md, private/design/ | | optional (only if figures or video need a look) | |
| 9 | Report (paper) | none | main folder | the official report document, paper/ | | not started (the one required deliverable) | |

Rows the deliverables in HACKATHON.md do not need are set to `dropped` after the research (row 9 only runs when a report is required).

States: not started · running · waiting for Julian · done · archived · handed to a teammate · dropped

## Artifacts: one source each

Every deliverable from HACKATHON.md, the one place it is made, and who makes it. A second copy is never edited.

| Deliverable | The one source | Session or person | State | Final file submitted |
|---|---|---|---|---|
| Research report (PDF, official template, max 8 pages before references and appendices, plan 4 to 6; abstract 150 to 250 words; authors and affiliations; appendix "Limitations and Dual-Use / Ethical Considerations"; LLM Usage Statement; at least one figure) | Julian's Google Doc copy of the official template (copy link in HACKATHON.md, Links); PDF export is the submission; file `<ProjectTitle>_AI-Collusion-Research-Sprint_2026.pdf` | 9 Report | not started | |
| Public GitHub repo (optional) | this repo, README from the backend session | 5 Backend | not started | |
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

## Waiting for

- Julian: download OK for the template (.docx and .pdf export of the Google Doc) to hackathon/official/
- Julian: Discord check (pinned announcements, help-desk channel, Modal credits), send the email draft in HACKATHON.md
- Julian: pick ideas from the shortlist for the full check, then jury round R01

## Next step

Julian picks 2 to 3 shortlist ideas for the full check; jury round R01 on the shortlist; then the choice, CORE_IDEA.md, R02, backend (experiments) and report in parallel.

## Für die Skills

Append only, every session, one line each: `YYYY-MM-DD · <session> · <skill> · <problem> · <suggestion>`. Skills are not changed during the hackathon; afterwards a skill workshop session in `~/claude-tools` works through this list.

- 2026-10-24 · Ideen · hackathon-ideen · Research-Sprint-Format: Kurzkarte und Prüfkarte kennen keine Felder für Forschungsfrage, Hypothese, Variable, Metrik, Baseline mit Positivkontrolle, Runs und Seeds, Kosten, Null-Ergebnis-Risiko, Replikationsprüfung gegen Vorarbeiten; Kurzform erlaubt nur zwei Tracks, der Auftrag nannte drei · Variante „Research Sprint" im Skill: diese Felder in die Kurzkarte, Prüfskript liest sie, Trackzahl in der Kurzform als Parameter; Platzhalter „–" in der Vorlage (Nichtkunden-Ebene, „0–5") verstößt gegen die Gedankenstrich-Regel des Dateivertrags, Vorlage auf „keine" und „0 bis 5" ändern
