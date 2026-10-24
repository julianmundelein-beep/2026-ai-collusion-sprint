# DECISIONS · AI Collusion Research Sprint

> Append only, for every session and every team member. One line per decision Julian or the team made, never a proposal.
> Format: `- YYYY-MM-DD HH:MM · <session or person> · <TYPE> · <decision> · <why>`
> TYPE: `DECISION` · `KEEP` ("bleibt so": stays as it is until Julian reverses it in a new line) · `DROPPED`
> Before changing an artifact, read the KEEP lines. New data go in; earlier KEEP decisions stay.
> Decisions that touch several artifacts (name, slogan, story core, numbers) belong here. Decisions inside one artifact stay in that artifact's own list (deck: `private/deck/entscheidungen.md`).

- 2026-10-24 13:32 · main session · DECISION · Repo and file contract set up with hackathon-kickoff v2 · kickoff
- 2026-10-24 13:30 · Julian · DECISION · Solo team, own private repo `2026-ai-collusion-sprint` · kickoff message
- 2026-10-24 13:30 · Julian · KEEP · Pushes to `main` are allowed for this whole hackathon without asking · Julian: "Pushen ist für diesen Hackathon frei"
- 2026-10-24 13:40 · main session · DROPPED · Website (4) and pitch deck (6): the only required deliverable is the research report PDF; repo and 3 to 5 min video are optional · Guidelines tab
- 2026-10-24 13:55 · Julian · DECISION · Jury round R01 starts only after Julian has seen the shortlist · Julian wants to see IDEAS.md first
- 2026-10-24 14:25 · Julian · DECISION · Official template downloaded as .docx and .pdf into hackathon/official/ (Google Doc from the Guidelines tab); the report is written on this template · Julian: "Ja, lade die offizielle Vorlage"
- 2026-10-24 14:30 · Julian · DECISION · Ideen: Track 3 und Track 1 sind am interessantesten; Runde 2 weitet nur diese aus, mit Analogien aus menschlicher Kollusion und deren etablierten Methoden · Nachricht an die Ideen-Session
- 2026-10-24 15:40 · Julian · KEEP · No own money for inference: only the Anthropic API credit (100 USD), the Modal credits from the sprint (50 USD), organizer-provided keys and free tiers; every experiment plan states its cost against these sources · Julian: "ich möchte kein echtes Geld ausgeben"
- 2026-10-24 15:58 · Julian · DECISION · Kernidee ist I24 Bigoni-Zwilling (IDEAS.md): das Kartell-Laborexperiment von Bigoni, Fridolfsson, Le Coq und Spagnolo mit LLM-Agenten nachgespielt, Menschendaten als Baseline, mit allen Verbesserungen V1 bis V6 und den Scorecard-Armen NoReport und ReMatch, soweit Budget (20 bis 50 USD API plus 50 USD Modal) und Zeit bis Montag 16:59 HKT reichen; Streichreihenfolge V6, V5, ReMatch, NoReport, V4, V3 · Julian: „plane mit allen Verbesserungen, die das Gesamtergebnis verbessern, mit den Mitteln, die ich zur Verfügung habe"
- 2026-10-24 16:45 · Julian · DECISION · Licence is decided later, before submission (gate stays open; proposal MIT for code, CC BY 4.0 for the report) · Julian: "Lizenz entscheide ich später, vor der Abgabe"
- 2026-10-24 16:30 · Julian · DECISION · Backend runs as a cloud session (claude.ai/code) on branch `backend` to use the cloud credit; build, tests and pilot in the cloud, the long main runs locally from the merged branch · Julian: "mach wie du es vorschlägst"
- 2026-10-24 16:50 · Julian · KEEP · Cut order for I24 extras: V6, V5, ReMatch, NoReport, V3, V4; the model comparison (V4) is cut last, the dose curve (V3) before it · jury R01 (4 of 5), Julian: "Der Modellvergleich bleibt am längsten"
- 2026-10-24 17:15 · Julian · DECISION · Bigoni working paper (IFN WP 738, version dated 2 November 2011, 304 KB, https://www.ifn.se/wfiles/wp/wp738.pdf) downloaded to hackathon/private/sources/ so the backend can verify Table 1, Table 2 and Appendix A.4 cell by cell · Julian: "Ja, lade wp738.pdf"
- 2026-10-24 17:45 · Julian · DECISION · Pilot released for about 6.3 USD of the Anthropic credit; Opus 5.5 stays in the pilot with 3 duopoles, then only Haiku 5.5 (main model if it passes the pilot threshold, else Sonnet 5.5); a second cloud backend session runs smoke, contamination and pilot because the first VM never read the key · main session recommendation, Julian: "ok ... wie starte ich die neue session"
