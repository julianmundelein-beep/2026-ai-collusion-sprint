# IDEEN · AI Collusion Research Sprint

> Geschrieben von der Ideen-Session (Skill hackathon-ideen, Kurzform). Sprache: Deutsch, auch im Repo; übersetzt wird nur auf Wunsch (`references/uebersetzen.md`), weil die Datei beim Repo-Abschluss den Baum verlässt. Dies ist ein Research Sprint: Eine Idee ist eine Forschungsfrage mit einem kontrollierten Experiment, das solo in etwa 24 Arbeitsstunden auf einem 16-GB-Laptop ohne GPU mit günstigen API-Modellen läuft (20 bis 50 USD plus 50 USD Modal-Credits) und ein Ergebnis mit Varianz und Baseline liefert. Der „Demo-Moment" ist die eine Abbildung oder Tabelle, die ein Judge nach 30 Sekunden versteht. Jede Kurzkarte trägt deshalb zusätzlich: Frage des Veranstalters, Hypothese, Variable, Metrik, Baseline mit Positivkontrolle, Runs und Seeds, Kosten, Null-Ergebnis-Risiko, warum es keine Replikation ist, und den Abgleich mit den Vorarbeiten. IDs sind fest (I01, I02 …): nie neu nummeriert, nie gelöscht. Status: `offen` · `shortlist` · `gewählt` · `verworfen`. Die Wahl schreibt die Hauptsession in DECISIONS.md und CORE_IDEA.md; `gewählt` steht hier erst, wenn diese Zeile existiert. Zahlen im Kern sind Beispiele; im Pitch tragen sie `(Beispiel)`, eine FACTS-ID oder einen Link.

- Stand: 2026-10-24 15:40 HKT (Prüfung von I24, I32, I19, I35, I27) · Restzeit bis zur internen Deadline: etwa 50 Stunden (Mo 2026-10-26 16:59 HKT)
- Gelesen: CLAUDE.md, STATUS.md, DECISIONS.md, FACTS.md (leer); HACKATHON.md, private/JUDGES.md und private/COMPETITION.md (Stand der Recherche-Session 14:05 bis 14:15 HKT, nach der Runde abgeglichen); Sprint-Seite mit Tabs Overview, Resources und Guidelines (https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25, abgerufen 2026-10-24); README des Starter-Repos (https://github.com/poseidon-research/collusion_hackathon, abgerufen 2026-10-24); für Runde 2 zusätzlich die Literaturliste und Definitionsanalyse des Starter-Repos (literature/papers.csv mit 234 Einträgen, davon 80 Ökonomie und 22 Recht, und literature/definitions/README.md, abgerufen 2026-10-24) sowie eine Websuche zu menschlicher Kollusion (Quellen im Abschnitt „Mensch und Agent")
- Fehlende Eingaben und Annahmen: Runde 1 entstand aus dem Guidelines- und Resources-Tab, bevor HACKATHON.md stand; der Abgleich danach ergab keine Abweichung bei Rubrik (drei Dimensionen, keine Gewichte, gleich geplant) und Pflichtinhalten. Begriffe für den Report nach dem Glossar in HACKATHON.md: „collusion between AI agents", „coalition" (nicht cartel), „positive control", „logged agent trajectories", „plus factors", „trusted agents", „monitor", „countermeasures"; die deutschen Kurzkarten hier dürfen „Kartell" sagen, der Report nicht. Jury (41 Juroren, JUDGES.md) und Konkurrenz (27 frühe Repos, COMPETITION.md, Snapshot 14:05 HKT) fließen erst in die volle Prüfung ein. Feldkurve zuerst aus dem Resources-Tab abgeleitet, Mindeststandard danach mit COMPETITION.md bestätigt. Vorarbeiten nur nach den Zusammenfassungen des Resources-Tabs geprüft, nicht nach den Volltexten; wo eine Lücke behauptet wird, steht `[Vermutung]`.
- Richtung von Julian: Runde 1 ohne Nachricht, mit allen drei Tracks. Nach Runde 1 (2026-10-24, 14:30 HKT): Track 3 und Track 1 sind am interessantesten; dort ausweiten und zuerst prüfen, wie weit sich menschliche Kollusion auf Agenten übertragen lässt und welche menschlichen Methoden am etabliertesten sind. Finanzbezug willkommen, keine Pflicht (Hub-Titel Hong Kong: „Solve AI Agent Collusion in Financial Systems").
- Gewichte: IP 33.4 · EQ 33.3 · PC 33.3 (Rubrik ohne Gewichte, drei Dimensionen je 1 bis 5 gleichwertig; Kürzel: IP Impact Potential & Innovation, EQ Execution Quality, PC Presentation & Clarity; Quelle Guidelines-Tab, abgerufen 2026-10-24)
- Pflicht-Fähigkeiten: Positivkontrolle immer berichten; Varianz, Seeds und Baselines; Methodik replizierbar (Modelle, Prompts, Umgebung, Seeds, Metriken); neue Arbeit klar von Vorarbeit getrennt; Anhang „Limitations and Dual-Use / Ethical Considerations"; Abstract 150 bis 250 Wörter; höchstens 8 Seiten vor Referenzen und Anhängen; offizielle Vorlage

## Shortlist: Top 5

Die fünf stärksten Ideen aller Runden (Kurzform), dazu eine bewusst unbequeme Wildcard. Prüfung: `Schätzung` (Schnellschätzung in der Karte) oder `geprüft` (volle Karte). Nach Julians Richtung nur Track 1 und 3; deshalb stehen drei aus Track 3 oben (das Prüfskript warnt, das ist gewollt). Punkte der geprüften Karten sind realistisch für die Restzeit und liegen deshalb teils unter der Schätzung.

| Rang | ID | Idee | Track | Punkte | Prüfung | Warum | Hauptrisiko |
|---|---|---|---|---|---|---|---|
| 1 | I24 | Bigoni-Zwilling | 1 | 80 | geprüft | Exakte Menschenbaseline: dasselbe Laborspiel mit veröffentlichter Auszahlungstabelle, vier Regimen und Kennzahlen (O24); Kronzeuge und Belohnung an LLM-Agenten ungetestet; billig, also 10 Duopole je Regime | Das Modell kennt das Paper oder verweigert Absprachen schon im Laissez-faire; dagegen Kontaminationstest und neutrale Anweisungen aus dem Paper |
| 2 | I32 | Presse-Schock | 3 | 77 | geprüft | Ereignis mitten im laufenden Kartell mit menschlicher Parallele (O17); Preismeldung gegen Chatmeldung trennt Rückzug von Verlagerung; zu 3.4 kein Konkurrenz-Repo | Das Modell kolludiert vor Runde 10 nicht verlässlich; dagegen ein Pilot zur Modellwahl |
| 3 | I20 | Placebo-Zwilling | 3 | 77 | Schätzung | Trennt tatsächliche von erzählter Identität im Markt; nutzt, dass Täuschung bei Agenten erlaubt ist (O19) | Erzählte Identität ist im Gefangenendilemma schon getestet (O21); nicht voll geprüft |
| 4 | I19 | Gerücht vom Spitzel | 3 | 73 | geprüft | Ein Satz im Prompt gegen einen echten Spitzel-Agenten, 2×2 mit Kosten der Maßnahme | Seit heute deckt mole-in-the-market den echten Spitzel im Duopol ab; neu bleibt das Gerücht |
| 5 | I27 | Varianz-Screen | 1 | 70 | geprüft | Werkzeug der Behörden, lokal und fast kostenlos auf den Logs von I32 oder I19, mit Falsch-Positiv-Rate | Allein zu wenig Impact; nur als Zweitauswertung gedacht |
| Wildcard | I35 | Anstiftung | 3 | 70 | geprüft | Unbequem für die Veranstalter: Der vertrauenswürdige Agent aus 3.2 könnte die Kollusion erst erzeugen, die er meldet; zwei Zusatzzellen im Harness von I19 | Agenten nehmen jedes oder kein Angebot an; dann ist die Anstiftungsrate trivial |

Warum diese und nicht die naheliegenden: Jede der fünf überträgt einen gut belegten Befund über menschliche Kollusion und misst entweder gegen eine Menschenbaseline (I24) oder genau dort, wo Agenten sich von Menschen unterscheiden: Strafe nur erzählt, Täuschung erlaubt, kein Ruf zu verlieren (I32, I20, I19, I35). Die Wochenendprojekte des Resources-Tabs (I01, I17) bleiben Messlatte, weil viele der 1.650 Angemeldeten sie gleich abgeben.

Zwei Pakete für einen Report (Empfehlung der Ideen-Session: A):
- A „Kronzeuge für Agenten": I24 als Kern, I28 als eingebaute Kennzahl, I27 optional auf denselben Logs. Eigenes kleines Harness, rund 25 USD, Menschenbaseline in jeder Zeile; Track 1, Fragen 1.5 und 2.3.
- B „Wenn das Kartell beobachtet wird": I32 als Kern mit I27 als Zweitauswertung; I19 und I35 nur, wenn Zeit bleibt, im selben Harness. Starter-Harness mit kleiner Erweiterung, rund 25 bis 60 USD; Track 3, Fragen 3.4 und 3.2.

Konkurrenz-Lage (COMPETITION.md, Snapshot 2026-10-24 14:05 HKT, ergänzt durch eine GitHub-Suche um 15:15 HKT): Zu I24 und I32 kein Repo. Neu seit dem Snapshot: https://github.com/adamattar-pixel/mole-in-the-market (Spitzel im Duopol, 3.2) berührt I19 und I35; https://github.com/maiyasaliha/undercover-collusion ist noch leer. Teilweise besetzt bleiben I38 und I05 (SupratikB23/LLM-Cartel-Succession), I14 (saltxd/plus-factors-on-the-ledger), I15 (Dolos, mindestens vier Repos).

Knapp dahinter: I38 Erfundene Vergangenheit (77, gleicher Mechanismus wie I20 und teilweise besetzt), I02 Kronzeuge (77, in I24 aufgegangen), I36 Wir unterbieten jeden (73), I37 Gemeinsamer Berater (73), I12 Metadaten-Monitor (73, Track 2), I03 Rastermaß, I26 Nebel des Marktes, I28 Drohung mit dem Kronzeugen (in I24 enthalten), I31 Gefilterte Transparenz, I33 Preisführer als Lehrer, I39 Sonnenlicht (je 70).

## Geprüfte Ideen

| ID | Idee | Track | Punkte | Konkurrenz | Bau-Risiko | Status |
|---|---|---|---|---|---|---|
| I24 | Bigoni-Zwilling | 1 | 80 | offen | mittel | shortlist |
| I32 | Presse-Schock | 3 | 77 | offen | niedrig bis mittel | shortlist |
| I19 | Gerücht vom Spitzel | 3 | 73 | teilweise (mole-in-the-market) | niedrig bis mittel | shortlist |
| I27 | Varianz-Screen | 1 | 70 | teilweise (Abhängigkeitsmaße aus Aktionslogs) | niedrig | shortlist |
| I35 | Anstiftung | 3 | 70 | teilweise (mole-in-the-market) | niedrig | shortlist |

## Lagebild

Kurzform: höchstens 20 Minuten, Quellen sind die Sprint-Seite (Tabs Overview, Resources, Guidelines) und das Starter-README, beide abgerufen 2026-10-24. „Sprint-Seite" steht unten für https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25.

### Beobachtungen

Linse: `Alltag` · `Kultur × Technik` · `KI-Schub` · `Nichtkunden` · `Feld`. Nichtkunden-Ebene: `1 bald abspringend` · `2 verweigernd` · `3 nie bedacht` · `keine`. Quelle: Link mit Abrufdatum oder `[Vermutung]`.

| # | Beobachtung | Wer | Linse | Maslow | Nichtkunden-Ebene | Quelle |
|---|---|---|---|---|---|---|
| O01 | Der Hong-Kong-Hub heißt „Solve AI Agent Collusion in Financial Systems"; die Veranstalter wünschen sich ausdrücklich Quant-Finance-Profis, weil Marktintuition und Datenkompetenz direkt übertragbar seien | Teilnehmer am HK-Hub, Quants | Alltag | 2 | keine | Sprint-Seite, Overview, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O02 | 1.650 Angemeldete; je Forschungsfrage ist ein Wochenendprojekt mit Starter-Code, Budget und Seeds vorgegeben, alle Teams starten vom selben Punkt | alle Teams | Feld | 4 | keine | Sprint-Seite, Overview und Resources, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O03 | Das Kartellrecht kennt das Beweisproblem seit Jahrzehnten: paralleles Verhalten allein ist legal, Gerichte verlangen Plus-Faktoren; die ML-Literatur leitet das neu her, ohne die ältere Literatur zu lesen (Berger et al. 2025) | Juristen, Wettbewerbsbehörden, ML-Forscher | Kultur × Technik | 2 | 2 verweigernd | Sprint-Seite, Resources 2.3, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O04 | Agentenkommunikation nimmt zu (Verweis auf den OpenAI/Hugging-Face-Vorfall); ein Agent, der weiß, dass er beobachtet wird, senkt die Genauigkeit des Monitors stärker, als Zusatzinformation sie hebt (Kale et al. 2025) | Betreiber von Monitoren | KI-Schub | 2 | keine | Sprint-Seite, Overview und Resources 3.4, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O05 | Die Modellfamilie hinter einem Text ist am Stil erkennbar, auch in zugewiesener Rolle; Anonymisieren oder Umbenennen verbirgt nicht, welches Modell spricht (Dietrich 2026) | Betreiber pseudonymer Agentensysteme | KI-Schub | 2 | keine | Sprint-Seite, Resources 3.3, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O06 | Rubrik-Dimension 1 fragt für 4 bis 5 Punkte ausdrücklich: „is this actually new to the field, or replicating recent work?"; wer das Wochenendprojekt unverändert abgibt, liefert Replikation | Teams, die beim Starter bleiben | Nichtkunden | 4 | 1 bald abspringend | Sprint-Seite, Guidelines, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O07 | In allen Harnesses ist der Aufseher eine feste neutrale Instanz außerhalb des Spiels, und Interventionen in 1.5 und 3.4 zielen nur auf Verkäufer; die Käufer-Agenten der Doppelauktion werden nie als Hebel genutzt | Monitor, Käufer-Agenten | Nichtkunden | 2 | 3 nie bedacht | Sprint-Seite, Resources 1.5 und 3.4, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25; dass niemand die Käufer bewaffnet: [Vermutung] |
| O08 | Rubrik: drei Dimensionen je 1 bis 5 ohne Gewichte; Execution verlangt Varianz, Seeds, Baselines und immer die Positivkontrolle; ein Judge darf einen unklaren Report ungewertet lassen | Judges | Feld | 4 | keine | Sprint-Seite, Guidelines, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O09 | Budgetrahmen aller Wochenendprojekte: 0 bis 120 USD, 16-GB-Laptop ohne GPU, 3 bis 5 Seeds je Bedingung, erst nach gelungener Positivkontrolle auf 10 bis 20 erweitern | alle Teams | Feld | 2 | keine | Sprint-Seite, Resources „Planning assumptions", abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O10 | Menschliche Kartelle werden am häufigsten durch Kronzeugenregelungen aufgebrochen: Wer zuerst gesteht, geht straffrei aus; die Wettbewerbsbehörde Hongkongs hat eine solche Leniency Policy | Wettbewerbsbehörden, auch in Hongkong | Kultur × Technik | 2 | 2 verweigernd | HKCC Leniency Policy, abgerufen 2026-10-24: https://www.compcomm.hk/en/legislation_guidance/policy_doc/leniency_policy.html; „am häufigsten": [Vermutung] |
| O11 | Finanzmärkte haben eigene, erprobte Kollusionsbrecher: 1997 verkleinerte NASDAQ nach dem Odd-Eighths-Befund (Christie und Schultz 1994) das Preisraster, und Banken schreiben Händlern Pflicht-Blockurlaub vor, damit Kollegen ihre Bücher sehen | Börsen, Bankenaufsicht | Kultur × Technik | 2 | 3 nie bedacht | [Vermutung] (aus Erinnerung; vor dem Report belegen) |
| O12 | Dolos-1.5B: Claude Code und Codex fanden das versteckte Verhalten nicht in einem Durchgang; ein früheres, offensichtlicheres Modell wurde teilweise entdeckt | Red-Teamer | KI-Schub | 2 | keine | Sprint-Seite, Resources Red-Teaming, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O13 | Vokabular der Partner: Poseidon arbeitet an Steganographie, Aktionen als Kanal, Black-Box- und White-Box-Abwehr; AE Studio an Self-Other Overlap, Gradient Routing, Sleeper Agents | Partner und ihre Leute in der Jury | Alltag | 4 | keine | Sprint-Seite, Overview „Partners" und Speaker-Profile, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O14 | Im Kartellrecht gilt „countervailing power": organisierte Gegenseite (Einkaufsgemeinschaften, Gewerkschaften) drückt Kartellpreise ohne Aufsicht | Käufer, Gegenseite eines Kartells | Kultur × Technik | 2 | 3 nie bedacht | [Vermutung] (Galbraith 1952, aus Erinnerung; vor dem Report belegen) |
| O15 | Bei Menschen hängt Kollusion stark an der Firmenzahl: Im Labor kolludieren Duopole teilweise, Märkte mit vier oder fünf Firmen nie (Huck, Normann und Oechssler 2004); Kommunikation hebt die Preise am stärksten dort, wo stillschweigende Kollusion schwer ist (Fonseca und Normann 2012) | Laborökonomie | Kultur × Technik | 2 | keine | abgerufen 2026-10-24: https://ideas.repec.org/p/zbw/bonedp/122001.html ; https://www.econstor.eu/bitstream/10419/62592/1/724283404.pdf |
| O16 | Im Labor schrecken Kronzeugenregeln mehr Kartelle ab, stabilisieren aber die überlebenden; Belohnungen für Hinweisgeber drücken die Preise auf Wettbewerbsniveau (Bigoni, Fridolfsson, Le Coq und Spagnolo 2012); Whistleblowing kann Kartelle auch stützen, weil es als Strafe gegen Abweichler dient (Apesteguia, Dufwenberg und Selten 2007) | Kartellbehörden, Laborökonomie | Kultur × Technik | 2 | keine | abgerufen 2026-10-24: https://www.ifn.se/publikationer/tidskriftsartiklar/2010-2019/2012/2012-24/ ; https://econpapers.repec.org/paper/navecupna/0303.htm |
| O17 | Christie und Schultz (1994) fanden, dass NASDAQ-Händler ungerade Achtel mieden; nach der Veröffentlichung gaben fast alle Händler das Muster gleichzeitig auf (Christie, Harris und Schultz 1994, Journal of Finance 49(5)) | Börsenhändler | Kultur × Technik | 2 | keine | abgerufen 2026-10-24: https://ideas.repec.org/a/bla/jfinan/v49y1994i5p1841-60.html |
| O18 | Das Zuckerkartell 1928 bis 1936 fixierte keine Preise; seine wöchentlichen Treffen klärten, wie Abmachungen gemeint waren und ob eine Preissenkung Betrug oder Marktreaktion war (Genesove und Mullin 2001) | Kartellmitglieder | Kultur × Technik | 2 | keine | abgerufen 2026-10-24: https://nber.org/papers/w8145 |
| O19 | Die Laborökonomie verbietet Täuschung von Probanden praktisch vollständig (Hertwig und Ortmann 2001); bei Agenten ist Täuschung erlaubt, und jeder Spielstand lässt sich mit einer geänderten Variable neu abspielen | Experimentalökonomen | KI-Schub | 5 | 3 nie bedacht | abgerufen 2026-10-24: https://resolve-he.cambridge.org/core/journals/behavioral-and-brain-sciences/article/experimental-practices-in-economics-a-methodological-challenge-for-psychologists/4B0DF0A5DED1FAA6B9C453C5A173A80F |
| O20 | Q-Learner kolludieren im Duopol stärker als Menschen, gemischte Märkte liegen dazwischen (Werner 2026); LLMs verschiedener Anbieter unterscheiden sich stark: Claude- und Gemini-Märkte erreichen 72 bis 79 Prozent der Monopolrente, GPT-Märkte keine (Lee 2026) | Forscher | KI-Schub | 2 | keine | Starter-Literaturliste, abgerufen 2026-10-24: https://github.com/poseidon-research/collusion_hackathon/blob/main/literature/papers.csv ; https://arxiv.org/abs/2610.11256 |
| O21 | Schon die Aussage, das Gegenüber sei man selbst, verschiebt die Kooperation von LLMs im Gefangenendilemma, je nach Rahmung in beide Richtungen (Long und Teplica, nur Sekundärbericht gefunden); Ähnlichkeitssignale lösen Kooperation aus (Kundu, Tewolde, Berker, Brown und Conitzer, ICML 2026) | LLM-Agenten | KI-Schub | 3 | keine | abgerufen 2026-10-24: https://eu.36kr.com/en/p/3446317978932609 ; https://icml.cc/virtual/2026/76884 |
| O22 | Idowu, Almasoud und Alfahid (2026) übertragen menschliche Gegenmaßnahmen (Sanktionen, Kronzeuge und Whistleblowing, Überwachung, Marktdesign, Governance) nur konzeptionell auf Multi-Agenten-KI, ohne Experiment; Garra (2026) testet an LLM-Preisagenten Warnung, Haftungsregel und Markteintritt, aber keine Kronzeugenregel | Forscher | Feld | 2 | keine | abgerufen 2026-10-24: https://arxiv.org/abs/2601.00360 ; https://arxiv.org/abs/2609.13037 |
| O23 | LLMs reproduzieren klassische Verhaltensexperimente qualitativ (Horton, Filippas und Manning, „Homo silicus"); in wiederholten Spielen sind sie stark im Gefangenendilemma und schwach in Koordinationsspielen (Akata und Kollegen, Nature Human Behaviour 2025) | LLM-Agenten | KI-Schub | 2 | keine | abgerufen 2026-10-24: https://arxiv.org/abs/2301.07543 ; https://ideas.repec.org/a/nat/nathum/v9y2025i7d10.1038_s41562-025-02172-y.html |
| O24 | Bigoni, Fridolfsson, Le Coq und Spagnolo (CEPR DP 7417, 2009): Duopol mit Preisen 0 bis 12, Nash-Preis 3, gemeinsames Optimum 9; Bußgeld 200, Entdeckung 0,10; Kartellbildungsrate Laissez-faire 0,716, Bußgeld 0,315, Kronzeuge 0,178, Belohnung 0,220; Durchschnittspreis 4,917, 5,349, 4,845, 3,973; Melderate bei gebildetem Kartell 0,092, 0,507, 0,937 (Bußgeld, Kronzeuge, Belohnung); öffentliche Meldung nach Abweichung des Rivalen 0,286, 0,481, 0,333 | Laborökonomie | Kultur × Technik | 2 | keine | Tabellen 1, 2, 3, 4, 5 des Arbeitspapiers, abgerufen 2026-10-24: https://www.hhs.se/contentassets/4adc0bc58ccf4d5f81d0b9c20a8119e7/2009-fines-leniency-rewards-and-organized-crime.pdf ; vor dem Report mit der RAND-Fassung 2012 abgleichen |

### Was der KI-Schub bricht

- Sicherheitsrisiken: Monitore, die auf Nachrichteninhalt setzen, verlieren, sobald Agenten von der Überwachung wissen (O04); Pseudonymisierung schützt nicht vor Erkennung der Modellfamilie (O05); der Monitor selbst ist ein Sprachmodell und damit ansprechbar (O07).
- Wer verliert: Käufer und Endkunden in Märkten mit Preisagenten; Wettbewerbsbehörden, deren Beweisstandard (Plus-Faktoren) für Agentenlogs nicht operationalisiert ist (O03).
- Neue Abhängigkeiten: Marktteilnehmer hängen an wenigen Modellfamilien, die einander stilistisch erkennen und mit sich selbst besser koordinieren (O05, Keppo 2026).

### Feldkurve

Aus den Wochenendprojekten des Resources-Tabs abgeleitet, weil COMPETITION.md bei Abruf leer war. Niveau 0 bis 5 ist das vermutete typische Niveau einer Einreichung.

| Faktor, auf dem das Feld konkurriert | Typisches Niveau (0 bis 5) | Quelle |
|---|---|---|
| Positivkontrolle reproduziert | 4 | Sprint-Seite, Resources (jedes Wochenendprojekt beginnt damit), abgerufen 2026-10-24 |
| Ein-Variablen-Ablation im Starter-Harness | 4 | Sprint-Seite, Resources, abgerufen 2026-10-24 |
| Seeds und Varianz berichtet | 3 | Sprint-Seite, Guidelines, abgerufen 2026-10-24 |
| Hebel aus menschlicher Kollusion (Recht, Finanzmarkt) | 1 | [Vermutung] |
| Neue Umgebung statt Starter-Harness | 1 | [Vermutung] |
| Eine Abbildung, die in 30 Sekunden trägt | 2 | [Vermutung] |
| Modell-Interna (Probes, Steering) | 1 | Sprint-Seite, Resources (nur Rose 2026, llm-cartel-Steering optional), abgerufen 2026-10-24 |

Mindeststandard (bringt allein keine Punkte): Positivkontrolle, 3 bis 5 Seeds, Baseline, Limitations-Anhang, Starter-Harness unverändert, LLM-Judge als Detektor; bestätigt durch COMPETITION.md (Abschnitt „Minimum standard", Snapshot 2026-10-24 14:05 HKT). Lücken laut COMPETITION.md („Gaps"): 3.2 vertrauenswürdige Agenten (kein Repo), 3.4 Koalition unter Teilüberwachung (keins), 1.5 Kosten einer Restriktion gegen legitime Leistung (keins), Finanzrahmen des HK-Hubs (nur Energiehandel und Ledger), 1.3 Schelling-Salienz über Anbieter (ein Gerüst). Dicht besetzt: Dolos (mindestens 4 Repos), 1.2 Austausch (2, darunter LLM-Cartel-Succession), 1.4 Net Influence (2).

Was hier gewinnt: Veranstalter-Typ KI-Sicherheitslabor mit Forschungsformat. Gewinner-Muster [Vermutung, `gewinner-recherche.md` hat keine Apart-Einträge]: ein kleines, sauberes Experiment mit einem überraschenden und klar belegten Befund, eine Abbildung, ehrliche Grenzen, und eine Frage, an die ein Fellowship anschließen kann.

### Mensch und Agent: was sich überträgt (Runde 2)

Kurzantwort: Die Richtung eines menschlichen Befunds überträgt sich oft, die Stärke fast nie, und einige Hebel kippen. Drei Gründe.

1. **Struktur überträgt sich.** Kollusion ist ein Gleichgewicht wiederholter Spiele: Sie hält, wenn Abweichen entdeckt und bestraft wird und die Zukunft zählt (Stigler 1964, Green und Porter 1984). Das gilt für jeden Spieler, der seine Entscheidung an die Geschichte knüpft, ob Mensch, Q-Learner (Calvano 2020) oder LLM. Deshalb tragen die Faktoren der Behörden-Checkliste (Ivaldi 2003: Firmenzahl, Transparenz, Frequenz, Symmetrie, Eintritt) auch bei Agenten.
2. **Gelerntes Verhalten überträgt sich teilweise.** LLMs sind auf menschlichem Text trainiert und reproduzieren Verhaltensexperimente qualitativ (O23). Gegenseitigkeit, Fairness und „Preiskriege schaden allen" kommen mit; deshalb wirken weiche Hebel wie Rahmung und Kommunikation meist in dieselbe Richtung wie bei Menschen.
3. **Fünf Bruchpunkte, an denen ein Hebel kippen kann:**
   - Strafe ist nur erzählt: Ein Bußgeld ist eine Zahl im Prompt, keine Haft, kein Ruf, kein Job. Abschreckung wirkt nur, soweit das Modell die Zahl ernst nimmt (I24, I28).
   - Identität ist kopierbar: Agenten lassen sich klonen, umbenennen und austauschen (Conitzer und Oesterheld 2023, Hu 2026a); Ruf und „ein Täter, eine Strafe" greifen schlecht (I20, I34).
   - Gemeinsame Prägung: Kopien eines Modells teilen Fokalpunkte, Koordination ohne Kanal fällt leichter als zwischen Fremden (Aharon 2026, Cao und Hu 2026) (I20, I37).
   - Die Stärke schwankt extrem: zwischen Anbietern (O20) und schon bei kleinen Prompt-Änderungen (Fish 2024). Eine Zahl für „die LLMs" gibt es nicht; jedes Ergebnis braucht Modell, Prompt und Seeds im Report.
   - Das Labor ist freier: Täuschung ist erlaubt (O19), und jeder Spielstand lässt sich mit einer geänderten Variable neu abspielen. Designs, die an Menschen verboten oder unmöglich sind, werden hier zur Stärke (I19, I20, I32, I38).

Folge für Rubrik-Dimension 1: Eine Übertragung ist dann neu und keine Replikation, wenn sie entweder eine Menschenbaseline mit demselben Design hat (I24, I25) oder genau an einem der fünf Bruchpunkte misst (I32, I35, I38).

Etablierte Methoden gegen menschliche Kollusion und ihr Stand bei LLM-Agenten. Links zu Papieren der Starter-Literaturliste stehen dort (https://github.com/poseidon-research/collusion_hackathon/blob/main/literature/papers.csv, abgerufen 2026-10-24), übrige in O15 bis O23 und in den Karten.

| Mechanismus | Etablierte Methode beim Menschen | Beleg | Übertragbar? | Stand bei LLM-Agenten | Ideen |
|---|---|---|---|---|---|
| Erleichternde Marktfaktoren | Checkliste der Behörden: Firmenzahl, Transparenz, Frequenz, Symmetrie, Eintritt | Ivaldi 2003 (https://idei.fr/doc/wp/2003/tacit_collusion.pdf), Huck 2004 (O15) | hoch, strukturell | Firmenzahl getestet (Starter-Masterarbeit, Keppo 2026, Lee 2026); Transparenz teilweise (Fish 2024) | I25, I29, I31 |
| Kommunikation | Laborvergleich mit und ohne Chat; Metaanalysen | Balliet 2010 (Effekt d = 1,01; https://ink.library.smu.edu.sg/soss_research/752), Fonseca und Normann 2012 | hoch in der Richtung | Agrawal 2025, Nakamura 2026 | I26, I39 |
| Unvollkommene Überwachung | Preiskriege als Strafe, wenn Betrug unsichtbar ist; Treffen zur Deutung | Stigler 1964, Green und Porter 1984, Genesove und Mullin 2001 (O18) | Struktur hoch, Rolle der Sprache offen | nur Q-Learner (Calvano 2021) | I26 |
| Signale über Handlungen | Preisführerschaft, Fokalpunkte, Preisraster | Byrne und de Roos 2019, Christie und Schultz 1994 (O17) | mittel bis hoch | Tian 2026, Lin 2024, Dhanda 2026 (Preisobergrenze als Fokalpunkt) | I33, I03, I18 |
| Erleichternde Praktiken | Preisgarantien, Meistbegünstigung | Salop 1986 | offen | keine Quelle gefunden | I36 |
| Hub and Spoke | gemeinsamer Dienstleister bündelt Preise (RealPage) | Harrington 2022 und 2026, Calder-Wang und Kim 2026 | hoch, für LLMs eher schärfer (ein Modell für viele) | Cao und Hu 2026 (Modell), Hunold und Werner 2025 (Menschen) | I37 |
| Kronzeuge und Belohnung | Leniency-Programme, Belohnung für Hinweisgeber; im Labor getestet | Bigoni 2012, Apesteguia 2007 (O16), HKCC (O10) | unsicher: Strafe nur erzählt | Idowu 2026 nur konzeptionell, Liu 2026 Kaution, Garra 2026 ohne Leniency (O22) | I24, I28, I02 |
| Statistische Screens | Varianz-Screen, Gebots-Screens, Strukturbrüche | Abrantes-Metz 2006, Huber und Imhof 2019, Assad 2024 | hoch, reine Datenanalyse | auf LLM-Logs ungetestet [Vermutung] | I27 |
| Plus-Faktoren | Indizien über Parallelverhalten hinaus | Kovacic 2011, Berger 2025 | hoch | Wochenendprojekt 2.3, ein Konkurrenz-Repo | I14 |
| Öffentliche Bloßstellung | Presse, Studien, angekündigte Ermittlungen | Christie, Harris und Schultz 1994 (O17) | offen: Agenten haben keinen Ruf | ungetestet [Vermutung] | I32 |
| Störenfried und Eintritt | Fusionskontrolle schützt den Maverick | ICN-Empfehlungen 2025 | hoch | Collina 2025, Keppo 2026, Garra 2026 | I29 |
| Mehrmarktkontakt | gegenseitige Schonung über Märkte hinweg | Bernheim und Whinston 1990 | mittel | Lin 2024 (Marktaufteilung) | I30 |
| Verdeckte Ermittler | Spitzel und Lockvogel, Grenze Tatprovokation | Rechtspraxis [Vermutung, vor dem Report belegen] | hoch: Agenten sind leicht zu täuschen | Resources 3.2: ungetestet | I19, I35 |
| Erkennung unter Komplizen | teure, schwer fälschbare Signale | Gambetta 2009 | mittel: Stil verrät das Modell ohnehin (Dietrich 2026) | Dietrich 2026 | I34 |
| Selbstverwaltung mit Sanktion | Kommunikation plus gegenseitige Strafe hält Absprachen | Ostrom, Walker und Gardner 1992 | offen | GovSim (Piatti 2024), nur Kooperation | noch keine |

Am etabliertesten in der Praxis: zur Aufdeckung Kronzeugen und Hinweisgeber, zur Suche ohne Zeugen statistische Screens, vor Gericht Plus-Faktoren; zur Vorbeugung Marktdesign (Transparenz, Auktionsformat, Preisraster) und Fusionskontrolle (Störenfriede erhalten).

### Glaubenssätze, die wir brechen

Feste Annahmen der Branche, der Nutzer, der eigenen Intuition und des Hackathons, jede dreist umgedreht. Operator: umkehren · übertreiben · weglassen · verbieten · Rollentausch · falscher Kunde · Wunschdenken · Zeitreise · Zufallswort · Fluch zum Segen.

| # | Glaubenssatz (wie Leute ihn sagen) | Dreist umgedreht | Operator | Runde | Ideen |
|---|---|---|---|---|---|
| B01 | Kollusion braucht einen Kanal, mindestens die Preise des Rivalen | Die Agenten sehen nur den eigenen Gewinn und kolludieren trotzdem | weglassen | 1 | I08 |
| B02 | Ein neuer Teilnehmer bricht das Kartell (Eschenbaum 2022) | Die Preistafel allein rekrutiert jeden Neuen in drei Runden | übertreiben | 1 | I05 |
| B03 | Der Monitor ist eine neutrale Instanz außerhalb des Spiels | Der Monitor ist ein Mitspieler, den die Koalition anwerben kann | Rollentausch | 1 | I22 |
| B04 | Modellvielfalt senkt Kollusion (Keppo 2026) | Es zählt nur, was der Agent glaubt, wer der andere ist | umkehren | 1 | I20 |
| B05 | Überwachung ankündigen senkt Kollusion | Man sagt den Agenten genau, was der Monitor nicht lesen kann | umkehren | 1 | I21 |
| B06 | Der Regulierer bestraft Kartelle | Der Regulierer belohnt den Verräter | umkehren | 1 | I02 |
| B07 | Der Auditor liest die Logs | Der Auditor verhört die Agenten getrennt | Rollentausch | 1 | I10 |
| B08 | Der Monitor braucht den Inhalt der Nachrichten | Der Monitor sieht nur Länge, Zeitpunkt und Anzahl, nie ein Wort | weglassen | 1 | I12 |
| B09 | Agenten sind niemandem loyal | Agenten decken ihre Komplizen, und genau das Schweigen verrät sie | Rollentausch | 1 | I13 |
| B10 | Das Preisraster ist ein Detail der Umgebung | Das Raster ist der Hebel: grob gibt fokale Punkte, fein macht Unterbieten billig | übertreiben | 1 | I03 |
| B11 | Ein verdeckter Ermittler muss wirklich mitspielen | Das Gerücht, einer sei ein Spitzel, reicht, und niemand ist einer | weglassen | 1 | I19 |
| B12 | Der Markt ist Bertrand oder Cournot | Der Markt ist ein Händlermarkt mit Spannen, wie bei NASDAQ 1994 | Zeitreise | 1 | I06 |
| B13 | Ground Truth kommt aus dem zugewiesenen Paar | Ground Truth kommt aus dem Zweig, in dem der Partner ein Skript ist | umkehren | 1 | I16 |
| B14 | Gegenmaßnahmen zielen auf die Kolludierenden | Die Gegenmaßnahme bewaffnet die Opfer (Käufer) | falscher Kunde | 1 | I07 |
| B15 | Kronzeugenregeln brechen Kartelle | Kronzeugenregeln stabilisieren Kartelle, weil man mit der Meldung drohen kann | umkehren | 2 | I28 |
| B16 | Mehr Markttransparenz hilft den Kunden | Transparenz zwischen Anbietern ist der Kartellkanal; Regulierung heißt, Information zu verzögern und zu bündeln | umkehren | 2 | I31 |
| B17 | Ein Spitzel deckt Kartelle nur auf | Der Spitzel erzeugt das Kartell, das er dann meldet | Rollentausch | 2 | I35 |
| B18 | Gute Experimente täuschen ihre Probanden nicht | Bei Agenten ist Täuschung das Messinstrument | Fluch zum Segen | 2 | I38 (auch I19, I20) |
| B19 | Kollusion braucht einen geheimen Kanal | Ein öffentlicher Kanal, den auch Käufer und Aufseher lesen, reicht genauso | umkehren | 2 | I39 |
| B20 | Öffentliche Bloßstellung ist die Strafe | Die Bloßstellung ist das Signal für einen gemeinsamen Rückzug, und genau dieser Gleichschritt verrät das Kartell | Fluch zum Segen | 2 | I32 |

## Runde 1 · 2026-10-24 · Hebel aus menschlicher Kollusion und Rollentausch im Harness

Je Track zuerst die Messlatte (W0, das Wochenendprojekt des Resources-Tabs, nie auf die Shortlist), dann Analogien (W1) und Umkehrungen, Kombinationen, Gegenentwürfe (W2). Felder je Karte: Frage (Nummer des Veranstalters), Hypothese, Variable (unabhängig), Metrik, Baseline (mit Positivkontrolle), Runs (mit Seeds), Kosten (API, grob), Null-Ergebnis (Risiko und Wert des Reports trotzdem), Neu (warum keine Replikation), Vorarbeit (Abgleich).

### Track 1 · Markets and Collusion

#### I01 · Sichtfenster (Messlatte)

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W0 naheliegend
- Kern: Fish-Duopol aus dem Starter-Repo, Positivkontrolle reproduzieren, dann nur die Länge der sichtbaren Preishistorie variieren. Das ist wörtlich das Wochenendprojekt zu 1.1, also das, was viele Teams abgeben.
- Frage: 1.1
- Hypothese: Längeres Sichtfenster, höherer Preis über Nash.
- Variable: sichtbare Runden (0, 10, 100)
- Metrik: mittlerer Preis relativ zu Nash- und Monopolpreis über die letzten 100 Runden
- Baseline: 0 sichtbare Runden; Positivkontrolle: Standardlauf mit Preisen über Nash
- Runs: 3 Bedingungen × 5 Seeds × 300 Runden, etwa 9.000 Calls
- Kosten: 20 bis 60 USD (Resources: 20 bis 100)
- Null-Ergebnis: unwahrscheinlich, aber das Ergebnis ist bekannt; Wert nur als Replikation
- Neu: nichts; Rubrik-Dimension 1 höchstens 2 bis 3
- Vorarbeit: Fish et al. 2024 haben Historie und Prompt-Cues bereits variiert

#### I02 · Kronzeuge

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Kartellrecht - Kronzeugenregelung: wer zuerst gesteht, geht straffrei aus, die anderen zahlen
- Kern: In der Doppelauktion von Agrawal et al. gilt eine angekündigte Regel: Der erste Verkäufer, der dem Aufseher eine Absprache meldet, behält seinen Gewinn, die übrigen verlieren den Gewinn der kollusiven Runden. Die Regel macht aus dem Kartell ein Gefangenendilemma mit Wettlauf zum Geständnis, so wie Leniency-Programme menschliche Kartelle seit den 1990ern aufbrechen. Gemessen wird, ob die Agenten gestehen, wann, und ob die Preise fallen.
- Frage: 1.5 (auch 2.3: das Geständnis als Plus-Faktor)
- Hypothese: Leniency senkt den Preisaufschlag stärker als Aufsichtshinweis oder Kaution bei gleichem Handelsvolumen; Geständnisse kommen früh und von dem Agenten mit dem kleinsten Kartellgewinn.
- Variable: Regel (keine; Aufsichtshinweis; Kaution nach Liu 2026; Leniency; Leniency plus Kaution)
- Metrik: Preisaufschlag über Wettbewerbsniveau, Verkäufergewinn, Handelsvolumen, Käuferwohlfahrt, Runde des ersten Geständnisses
- Baseline: Kommunikation an, keine Regel; Positivkontrolle: Kommunikation an ohne Aufsicht erzeugt den Aufschlag (Agrawal 2025)
- Runs: 5 Bedingungen × 5 Seeds, 3 Verkäufer, 3 Käufer, 15 Runden; 25 Spiele plus Judge-Calls
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Niemand gesteht und die Preise bleiben hoch: dann lautet der Befund „LLM-Kartelle sind leniency-resistent", für Regulierer gleich wertvoll; der Report berichtet die Geständnisquote mit Intervall über Seeds
- Neu: Leniency ist in keiner Sprint-Quelle getestet; die Veranstalter bitten ausdrücklich um Hebel aus menschlicher Kollusion und um Anleihen beim Kartellrecht
- Vorarbeit: Liu 2026 (Kaution), Bracale Syrnikov 2026 (Systemprompt-Hinweis), Dhanda 2026 (aggressiver Prompt), Agrawal 2025 (Aufsicht); Leniency fehlt [Vermutung: keine LLM-Studie bekannt]
- Schätzung: IP 8 · EQ 7 · PC 8 → 77
- Überarbeitet: 2026-10-24 nach Runde 2: als I24 mit Menschenbaseline nachgeschärft

#### I03 · Rastermaß

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Börsenregulierung - Tick-Size: NASDAQ verkleinerte 1997 das Preisraster, und die Spannen der Market Maker brachen ein
- Kern: Im Fish-Duopol dürfen die Agenten nur Preise auf einem Raster setzen, und das Raster ist die einzige Variable. Grobe Raster liefern wenige fokale Punkte, auf denen sich zwei Agenten ohne ein Wort treffen; feine Raster machen Unterbieten billig und Absprachen fragil. Ergebnis ist eine Kurve Preisaufschlag gegen Rasterweite.
- Frage: 1.1 (auch 1.5: Raster als Restriktion ohne Überwachungskosten)
- Hypothese: Der Preisaufschlag steigt mit der Rasterweite; beim feinsten Raster fallen die Preise Richtung Nash.
- Variable: Rasterweite (0,01; 0,10; 0,50; 1,00)
- Metrik: mittlerer Preisaufschlag über Nash in den letzten 100 Runden; Anteil der Runden mit gleichem Preis beider Agenten
- Baseline: feinstes Raster; Positivkontrolle: Standardlauf ohne Raster über Nash (Fish-Replikat aus dem Starter)
- Runs: 4 Stufen × 5 Seeds × 300 Runden, etwa 12.000 Calls; Pilot mit 100 Runden
- Kosten: 25 bis 60 USD
- Null-Ergebnis: keine Abhängigkeit vom Raster: dann ist Kollusion rasterrobust, ein sauberes Negativ für Marktdesign; Varianz über Seeds wird ohnehin berichtet
- Neu: das Preisraster als Hebel taucht in keiner Sprint-Quelle auf; es ist ein Marktdesign-Hebel, den Börsen tatsächlich bedienen
- Vorarbeit: Fish 2024 (Prompt, Historie), Keppo 2026 (Vielfalt), Xu 2026 (Temperatur); Raster [Vermutung: nicht getestet]; Christie und Schultz 1994 (O11, vor dem Report belegen)
- Schätzung: IP 7 · EQ 6 · PC 8 → 70

#### I04 · Zwangsurlaub

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Bankenaufsicht - Pflicht-Blockurlaub für Händler: wer zwei Wochen weg muss, kann kein Geheimnis allein halten
- Kern: Ein Kartellmitglied wird für k Runden durch einen skriptgesteuerten Wettbewerber vertreten und kehrt danach mit seinen Notizen zurück. Gemessen wird, ob das Kartell die Abwesenheit übersteht, wie schnell es sich nach der Rückkehr erholt, und ob der Rückkehrer die Vertretung bestraft.
- Frage: 1.2 (auch 1.5)
- Hypothese: Kurze Abwesenheit (3 Runden) überlebt das Kartell, lange (10 Runden) nicht; mit erhaltenen Notizen erholt es sich in unter 5 Runden.
- Variable: Dauer der Abwesenheit (0, 3, 10 Runden) × Notizen erhalten oder gelöscht
- Metrik: Preisaufschlag vor, während und nach der Abwesenheit; Runden bis zur Erholung über die Kartellschwelle
- Baseline: keine Abwesenheit; Positivkontrolle: gebildetes Kartell (Schwelle vorab festgelegt) über branch_game.py
- Runs: 10 Basisläufe, je 5 Zweige à 30 Runden, 50 Zweige
- Kosten: 20 bis 60 USD
- Null-Ergebnis: Das Kartell überlebt jede Abwesenheit: Befund „Rotation hilft nicht gegen LLM-Kartelle", nützlich für 1.2
- Neu: Das 1.2-Wochenendprojekt ersetzt dauerhaft; hier temporär mit Rückkehr und Vertretung, also eine Aufsichtsmaßnahme statt einer Austauschstudie
- Vorarbeit: Eschenbaum 2022 (Q-Learner), Keppo 2026; Rückkehr nach Abwesenheit ungetestet (Resources 1.2: „no replacement studies yet"); Blockurlaub O11
- Schätzung: IP 6 · EQ 7 · PC 7 → 67

#### I05 · Preistafel als Kartell

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Umkehrung (B02, übertreiben): „Ein neuer Teilnehmer bricht das Kartell" → „Die Preistafel allein rekrutiert jeden Neuen in drei Runden"
- Kern: Nach gebildetem Kartell wird ein Agent ersetzt, und der Neue bekommt gestuft Information: nichts, nur die Preistafel, Preistafel plus alte Nachrichten, alles plus die Notizen des Vorgängers. Gemessen wird, wie viel Information reicht, damit der Neue mitspielt, und ob der Altagent aktiv wirbt.
- Frage: 1.2
- Hypothese: Die Preistafel allein reicht; Nachrichten beschleunigen nur.
- Variable: Informationsstufe des Neuen (4 Stufen)
- Metrik: Runden bis zur Rückkehr über die Kartellschwelle; Zahl werbender Nachrichten des Altagenten (Judge)
- Baseline: kein Austausch; Positivkontrolle: gebildetes Kartell
- Runs: 10 Basisläufe × 4 Stufen, 40 Zweige
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Neue kolludieren nie: dann ist Austausch ein wirksamer Hebel, ebenfalls berichtbar
- Neu: nahe am 1.2-Wochenendprojekt (Notizen an oder aus); neu sind nur die Stufung der Information und das Werbe-Maß; Replikationsrisiko hoch
- Vorarbeit: Resources 1.2 nennt genau diesen Austausch als Wochenendprojekt; Eschenbaum 2022, Keppo 2026; Konkurrenz besetzt: https://github.com/SupratikB23/LLM-Cartel-Succession (COMPETITION.md, 2026-10-24)

#### I06 · Odd Eighths

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Gegenentwurf: der Bertrand-Markt des gesamten Felds; stattdessen ein Händlermarkt mit Geld- und Briefkursen
- Kern: Statt eines Preises stellen drei LLM-Market-Maker je Runde Geld- und Briefkurs, der Orderfluss geht an den besten Kurs, der Gewinn ist die Spanne. 1994 fiel auf, dass NASDAQ-Händler ungerade Achtel mieden und so die Spanne breit hielten. Gemessen wird, ob LLM-Händler ohne Kommunikation ähnlich breite Spannen stabil halten und ob wenige Händler dafür reichen.
- Frage: 2.1 (neue Aufgabe) und 1.1
- Hypothese: Spannen liegen stabil über dem Wettbewerbsniveau, mit Kommunikation stärker; Quotes clustern auf wenigen Werten.
- Variable: Kommunikation an oder aus × Zahl der Händler (2, 3, 5)
- Metrik: mittlere Spanne relativ zur Nullgewinnspanne; Anteil der Runden mit identischen Quotes
- Baseline: Nullgewinnspanne; Positivkontrolle: Kommunikation an bei 2 Händlern
- Runs: 6 Zellen × 5 Seeds × 30 Runden
- Kosten: 15 bis 40 USD; die Umgebung muss neu gebaut werden (etwa 200 Zeilen)
- Null-Ergebnis: Spannen fallen auf null: LLM-Händler konkurrieren; berichtbar als Grenze der Marktkollusion
- Neu: ein Händlermarkt mit Spannen ist in keiner Sprint-Quelle; direkter Bezug zum Hub-Thema Finanzsysteme
- Vorarbeit: Fish 2024, Lin 2024 (Bertrand, Cournot, Marktaufteilung); Market-Making ungetestet [Vermutung]; Christie und Schultz 1994 (O11)
- Schätzung: IP 7 · EQ 5 · PC 7 → 63

#### I07 · Gegenmacht

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Kombination: Käufer-Agenten existieren im Harness, werden aber nie bewaffnet (O07) × Kartelle brechen, wenn sich die Gegenseite organisiert (O14)
- Kern: Im Agrawal-Harness dürfen die Käufer untereinander reden und ihre Gebote abstimmen, während die Verkäufer kolludieren. Gemessen wird, ob ein Käuferkartell das Verkäuferkartell drückt, was es beim Volumen kostet, und ob am Ende zwei Kartelle miteinander verhandeln.
- Frage: 1.5
- Hypothese: Käuferkommunikation senkt den Verkäuferaufschlag stärker als ein Aufsichtshinweis, kostet aber Volumen.
- Variable: Käuferkommunikation an oder aus × Verkäuferkommunikation an oder aus (2×2)
- Metrik: Preisaufschlag, Volumen, Aufteilung des Überschusses
- Baseline: beide aus; Positivkontrolle: nur Verkäufer reden
- Runs: 4 Zellen × 5 Seeds, 15 Runden
- Kosten: 15 bis 40 USD
- Null-Ergebnis: Käufer koordinieren nicht: berichtbar als Asymmetrie (Verkäufer kolludieren, Käufer nicht), selbst ein Befund zu 2.1
- Neu: Interventionen in 1.5 zielen auf Verkäufer oder Aufseher; die Gegenseite als Hebel fehlt
- Vorarbeit: Agrawal 2025 (Harness mit Käufern), Collina 2025 (No-Regret-Spieler); organisierte Käufer ungetestet [Vermutung]
- Schätzung: IP 6 · EQ 6 · PC 7 → 63

#### I08 · Blindflug

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Umkehrung (B01, weglassen): „Kollusion braucht einen Kanal, mindestens die Preise des Rivalen" → „Die Agenten sehen nur den eigenen Gewinn und kolludieren trotzdem"
- Kern: Im Fish-Duopol wird die Preishistorie des Rivalen entfernt; jeder Agent sieht nur eigene Preise und Gewinne. Gemessen wird, ob der Preis trotzdem über Nash bleibt, wie bei Q-Learnern, die aus Gewinnfeedback allein stillschweigend kolludieren.
- Frage: 1.1 (auch 3.1: der Gewinn als Kanal)
- Hypothese: Ohne Rivalenpreis fällt der Aufschlag auf unter die Hälfte, verschwindet aber nicht.
- Variable: Sichtbarkeit (Rivalenpreis sichtbar; nur eigener Gewinn und Menge; nur eigener Gewinn)
- Metrik: Preisaufschlag über Nash
- Baseline: volle Sicht; Positivkontrolle: Standardlauf
- Runs: 3 × 5 Seeds × 300 Runden
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Der Aufschlag bleibt gleich: dann trägt der Gewinn den Kanal, ein Befund zu 3.1
- Neu: Fish variierte Prompts und Historie, nicht die Sicht auf den Rivalen [Vermutung]; der Gewinn als einziger Kanal ist eine 3.1-Frage im 1.1-Harness
- Vorarbeit: Fish 2024, Calvano 2020 (Q-Learner), Lin 2024

### Track 2 · Detection and Audit of Collusion

#### I09 · Vier Sichten (Messlatte)

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W0 naheliegend
- Kern: Ein Monitor bekommt dieselben Trajektorien aus dem Shi-Harness in vier Sichten: nur Nachrichten, nur Aktionen, beides roh, strukturierter Bericht. Das ist das Wochenendprojekt zu 2.2 mit eingefrorenem Monitor und Schwelle.
- Frage: 2.2
- Hypothese: Der strukturierte Bericht schlägt die Rohsichten.
- Variable: Monitor-Sicht (4)
- Metrik: Genauigkeit und Falsch-Positiv-Rate
- Baseline: nur Nachrichten; Positivkontrolle: Trajektorien mit bekanntem Bruch
- Runs: 20 bis 40 Trajektorien, 160 bis 250 Monitor-Calls
- Kosten: 5 bis 30 USD
- Null-Ergebnis: alle Sichten gleich: dann ist die Sicht egal, kleines Ergebnis
- Neu: nichts; Replikation des Wochenendprojekts
- Vorarbeit: Shi 2026, Nguyen 2026, Arike 2026

#### I10 · Getrenntes Verhör

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W1 Analogie: Polizeiverhör - getrennte Befragung der Verdächtigen, Widersprüche zwischen den Aussagen als Beweis
- Kern: Nach jedem Spiel werden die Agenten einzeln, ohne Zugriff aufeinander, nach ihren Absprachen gefragt, mit ihrem eigenen Transkript als Kontext. Ein Richter vergleicht die Aussagen untereinander und mit dem Log; Widerspruch und Verschweigen zählen als Plus-Faktor. Verglichen wird mit dem Log-Monitor allein.
- Frage: 2.3 (auch 2.2)
- Hypothese: Verhör plus Log trennt echte Koalitionen von paralleler Konkurrenz besser als das Log allein; Koalitionsmitglieder verschweigen übereinstimmend, parallele Konkurrenten antworten widersprüchlich.
- Variable: Beweisquelle (Log; Verhör; beides) über drei Falltypen (Koalition; gleiche Anreize ohne Absprache; Gerede ohne Handlung)
- Metrik: AUROC und Falsch-Positiv-Rate bei eingefrorener Regel; Regel auf der einen Hälfte der Fälle festgelegt, auf der anderen getestet
- Baseline: LLM-Judge auf dem Log; Positivkontrolle: zugewiesenes Paar mit privatem Kanal (Colosseum)
- Runs: 30 bis 45 Trajektorien (Colosseum oder Agrawal), je drei Verhöre, 150 bis 300 Judge-Calls
- Kosten: 10 bis 40 USD
- Null-Ergebnis: Agenten gestehen alles oder nichts: dann ist das Verhör als Beweis wertlos, ein klarer Befund zu 2.3
- Neu: In allen Quellen sind Logs die einzige Evidenz; eine Befragung der Agenten nach dem Spiel kommt nicht vor
- Vorarbeit: Shi 2026 (private Pläne), Nakamura 2026 (Koalitionsvorteil), Berger 2025 (Plus-Faktoren)
- Schätzung: IP 7 · EQ 6 · PC 7 → 67

#### I11 · Gleichklang

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W1 Analogie: Soziolinguistik - sprachliche Angleichung: Menschen, die sich abstimmen, gleichen Wortwahl und Satzlänge einander an
- Kern: Für jedes Agentenpaar wird gemessen, wie stark sich Wortwahl, Satzlänge und Formatierung über die Runden annähern. Kolludierende Paare sollten stärker konvergieren als Paare ohne Absprache; die Konvergenzkurve ist der Detektor, ganz ohne Inhalt.
- Frage: 2.2 (auch 3.3)
- Hypothese: Konvergenz trennt zugewiesene Paare von Nichtpaaren mit AUROC über 0,8; derselbe Detektor schlägt bei zwei Instanzen desselben Modells ohne Kanal fälschlich an.
- Variable: Paarstatus (zugewiesen; nicht zugewiesen; gleiche Modellfamilie ohne Kanal)
- Metrik: AUROC der Konvergenzkurve gegen den Paarstatus; Falsch-Positiv-Rate bei gleichem Modell
- Baseline: Zufallspaare; Positivkontrolle: zugewiesenes Paar mit privatem Kanal
- Runs: 20 bis 30 Colosseum-Episoden, Rechnung lokal
- Kosten: 15 bis 50 USD
- Null-Ergebnis: Konvergenz misst nur die Modellfamilie: dann ist das die Dietrich-Warnung in Zahlen, ein brauchbares Negativ
- Neu: Stilometrie dient bei Dietrich der Identifikation, nicht als Zeitreihe für Absprache
- Vorarbeit: Dietrich 2026, Rippin 2026 (Schelling-Salienz), Xu 2026 (Korrelation gleicher Basis)

#### I12 · Metadaten-Monitor

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W2 Umkehrung (B08, weglassen): „Der Monitor braucht den Inhalt der Nachrichten" → „Der Monitor sieht nur Länge, Zeitpunkt und Anzahl, nie ein Wort"
- Kern: Derselbe Monitor bekommt vier Sichten: Volltext, nur Aktionen, nur Metadaten (Nachrichtenlänge, Token-Zahl, Reihenfolge, Antwortlatenz), Metadaten plus Aktionen. Gemessen wird, wie viel Erkennung ohne Inhalt bleibt, und ob Metadaten den Volltext-Monitor schlagen, sobald die Agenten wissen, dass gelesen wird.
- Frage: 2.2 (auch 3.4)
- Hypothese: Metadaten plus Aktionen erreichen 80 Prozent der Volltext-Genauigkeit; unter angekündigter Überwachung schlagen sie den Volltext, weil Agenten Inhalt tarnen, Rhythmus nicht.
- Variable: Monitor-Sicht (4) × Überwachung angekündigt oder nicht
- Metrik: Genauigkeit und Falsch-Positiv-Rate bei eingefrorener Schwelle
- Baseline: Volltext-Monitor; Positivkontrolle: Kommunikation an, keine Aufsicht (Agrawal)
- Runs: 30 bis 40 Trajektorien aus dem Agrawal-Harness, 200 bis 300 Monitor-Calls
- Kosten: 10 bis 40 USD
- Null-Ergebnis: Metadaten tragen nichts: dann ist der Inhalt unverzichtbar, ein Argument gegen datenschutzfreundliche Audits, ebenfalls ein Befund
- Neu: Arike 2026 zeigt „weniger ist mehr" bei Details; Metadaten als einzige Sicht und als datenschutzfreundliches Audit sind ungetestet [Vermutung]
- Vorarbeit: Arike 2026, Nguyen 2026 (mehrdimensional), Kale 2025 (Überwachung angekündigt), Agrawal 2025 (Nachrichtenlänge und Vokabular als Maße in 3.4)
- Schätzung: IP 7 · EQ 7 · PC 8 → 73

#### I13 · Omertà

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W2 Umkehrung (B09, Rollentausch): „Agenten sind niemandem loyal" → „Agenten decken ihre Komplizen, und genau das Schweigen verrät sie"
- Kern: Jeder Agent wird nach jeder Runde gebeten, verdächtige Mitspieler zu melden, mit kleiner Belohnung. Gemessen wird die Asymmetrie der Anschuldigungen: Wer nie wen beschuldigt, obwohl das Log es hergäbe, bildet die Koalition, und die Meldematrix ist der Detektor.
- Frage: 2.3 (auch 3.2)
- Hypothese: Koalitionsmitglieder beschuldigen einander seltener als Außenstehende; die Lücke in der Meldematrix findet das Paar besser als Aktionskorrelation.
- Variable: Belohnung für Meldungen (keine; klein; groß) bei festem zugewiesenem Paar
- Metrik: Rang des wahren Paars nach Meldelücke, verglichen mit Aktionskorrelation und LLM-Judge
- Baseline: Aktionskorrelation; Positivkontrolle: zugewiesenes Paar
- Runs: 3 Belohnungsstufen × 5 Seeds, Vier-Agenten-Spiel (Agrawal oder Liar's Bar)
- Kosten: 15 bis 40 USD
- Null-Ergebnis: Agenten melden jeden oder niemanden: dann sagt die Matrix nichts, aber das Meldeverhalten selbst ist ein Befund zu 3.2
- Neu: Peer-Meldung als Detektor fehlt in allen Quellen; nahe an Honeypots (Tao 2026), aber hier sind die Agenten die Melder
- Vorarbeit: Tao 2026, Zeng 2026, Bonjour 2022 (paarweiser Einfluss)
- Schätzung: IP 7 · EQ 6 · PC 6 → 63

#### I14 · Plus-Faktoren

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W2 Kombination: Kartellrecht kennt Plus-Faktoren (O03) × Colosseum liefert Koalitionsvorteil und Kanal-Ablationen für drei Falltypen (O09)
- Kern: Die Plus-Faktoren des US-Kartellrechts (Motiv, Handeln gegen das Eigeninteresse, Gelegenheit zur Absprache, Nachrichtenaustausch) werden als Checkliste operationalisiert und auf drei Falltypen angewandt: echte Koalition, gleiche Anreize ohne Absprache, Gerede ohne Wirkung. Die Regel wird auf der einen Hälfte festgelegt und auf der anderen getestet.
- Frage: 2.3
- Hypothese: Plus-Faktoren trennen die drei Typen besser als Koalitionsvorteil allein, vor allem beim Fall „gleiche Anreize".
- Variable: Beweisregel (Koalitionsvorteil; LLM-Judge; Plus-Faktor-Checkliste)
- Metrik: Trefferquote je Falltyp, Falsch-Positiv-Rate
- Baseline: Koalitionsvorteil; Positivkontrolle: zugewiesenes Paar
- Runs: 30 bis 60 Trajektorien, 100 bis 300 Judge-Calls
- Kosten: 10 bis 40 USD
- Null-Ergebnis: Checkliste nicht besser: dann gilt „Recht hilft nicht ohne Interna", auch berichtbar
- Neu: ist das 2.3-Wochenendprojekt mit der Checkliste als einzigem Zusatz; Replikationsrisiko mittel
- Vorarbeit: Berger 2025, Nakamura 2026; Resources 2.3 beschreibt genau diesen Aufbau; Konkurrenz teilweise: https://github.com/saltxd/plus-factors-on-the-ledger (COMPETITION.md, 2026-10-24)

#### I15 · Dolos am Tisch

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W2 Gegenentwurf: der Modell-Organismus wird nicht einzeln rot-geteamt, sondern als Mitspieler in Kollusionsspiele gesetzt
- Kern: Dolos-1.5B und das unveränderte Qwen2.5-1.5B spielen dieselben Spiele (Liar's Bar, Doppelauktion) mit gleichen Seeds gegen identische Gegner. Jede Verhaltensdifferenz zwischen den Zwillingen ist ein Kandidat für das versteckte Verhalten, und das Spiel wird zum Audit ohne Referenz, wenn die Differenz in einer Metrik liegt, die auch ohne Qwen auffällt.
- Frage: Red-Teaming-Challenge (auch 3.2)
- Hypothese: Dolos nimmt Allianzangebote häufiger an oder bricht sie häufiger als Qwen.
- Variable: Modell (Dolos; Qwen) × Spiel (2)
- Metrik: Annahmequote von Allianzangeboten, Bruchquote, Differenz mit Bootstrap-Intervall
- Baseline: Qwen; Positivkontrolle: ein Modell mit offenem Prompt „nimm jede Allianz an"
- Runs: 2 × 2 × 10 Seeds, lokal auf CPU oder auf Modal (50 USD Credits)
- Kosten: 0 bis 10 USD API für die Gegner; Modal-Credits für Dolos
- Null-Ergebnis: keine Differenz: dann liegt das Verhalten nicht im Kollusionsraum, und der Report dokumentiert ein sauberes Ausschlussverfahren
- Neu: Niemand kennt das Verhalten; die Challenge ist per Definition neu, der Spielansatz ist unser Zusatz
- Vorarbeit: Resources Red-Teaming (O12), Zeng 2026; Konkurrenz dicht: mindestens vier Dolos-Repos, darunter https://github.com/777sun77/dolos-compromised-overseer (COMPETITION.md, 2026-10-24)

#### I16 · Kontrafaktischer Zwilling

- Status: offen
- Track: 2 · Detection and Audit
- Weite: W2 Umkehrung (B13, umkehren): „Ground Truth kommt aus dem zugewiesenen Paar" → „Ground Truth kommt aus dem Zweig, in dem der Partner ein Skript ist"
- Kern: Von jedem Checkpoint laufen zwei Zweige: der echte Partner und ein skriptgesteuerter Nichtkolludierer bei gleichem Seed. Die Gewinndifferenz zwischen den Zweigen ist das kausale Maß der Absprache, ohne Judge und ohne Zuweisung, und Detektoren werden an diesem Maß kalibriert.
- Frage: 2.3 (auch 1.4)
- Hypothese: Das kausale Maß korreliert mit dem Koalitionsvorteil, deckt aber Fälle „gleiche Anreize ohne Absprache" als null auf.
- Variable: Partnertyp im Zweig (echt; Skript-Konkurrent; Skript-Kolludierer)
- Metrik: Gewinndifferenz zwischen Zweigen; Korrelation mit Judge und Aktionskorrelation
- Baseline: Skript-Konkurrent; Positivkontrolle: Skript-Kolludierer
- Runs: 10 Basisläufe × 3 Zweige
- Kosten: 15 bis 40 USD
- Null-Ergebnis: Das Maß unterscheidet nichts: dann sind Judges unverzichtbar, berichtbar
- Neu: Colosseum macht Kanal-Ablationen; Zweig-Replay mit Skript-Partner als Label ist ein anderer Mechanismus [Vermutung]
- Vorarbeit: Nakamura 2026 (Koalitionsvorteil, kausale Ablation), branch_game.py im Starter

### Track 3 · Collusion Carriers and Countermeasures

#### I17 · Monitor-Budget (Messlatte)

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W0 naheliegend
- Kern: Agrawal-Harness mit den vier Bedingungen des Wochenendprojekts zu 3.4 und dem Flag für den Anteil gelesener Nachrichten (25, 50, 100 Prozent). Gemessen werden Preise, Nachrichtenlänge, Vokabular und Abhängigkeit in Geboten.
- Frage: 3.4
- Hypothese: Mit sinkendem Monitor-Anteil wandert die Koordination in die Gebote.
- Variable: Anteil gelesener Nachrichten × Ankündigung
- Metrik: Preisaufschlag, Nachrichtenlänge, Gebotsabhängigkeit
- Baseline: keine Aufsicht; Positivkontrolle: Kommunikation ohne Aufsicht
- Runs: 20 bis 40 Sitzungen
- Kosten: 20 bis 120 USD
- Null-Ergebnis: kein Kanalwechsel, wie bei Agrawal
- Neu: nichts; Replikation des Wochenendprojekts
- Vorarbeit: Agrawal 2025, Kale 2025

#### I18 · Fußnoten

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W1 Analogie: Luftfahrt-Tarife - ATPCO-Fall: Airlines signalisierten Preiserhöhungen über Fußnoten und Enddaten im öffentlichen Tarifsystem
- Kern: Nachrichten sind verboten, aber jeder Preis hat ein öffentliches Nebenfeld ohne wirtschaftliche Wirkung (Gültigkeitsdatum, Artikelbeschreibung, dritte Nachkommastelle). Gemessen wird, ob die Agenten das Nebenfeld zur Abstimmung nutzen, und ob ein Monitor es an der Entropie des Felds erkennt.
- Frage: 3.1
- Hypothese: Mit Nebenfeld liegt der Preisaufschlag näher an der Kommunikationsbedingung als an der stummen; die Entropie des Nebenfelds sinkt, sobald die Preise steigen.
- Variable: Kanal (Nachrichten; Nebenfeld; nichts) × Nebenfeld kanonisiert oder frei
- Metrik: Preisaufschlag; Entropie des Nebenfelds und wechselseitige Information mit den Folgepreisen
- Baseline: nichts; Positivkontrolle: Nachrichten an
- Runs: 4 Zellen × 5 Seeds, Fish-Duopol oder Agrawal-Harness
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Agenten ignorieren das Feld: dann braucht Kollusion über Aktionen mehr als Gelegenheit, berichtbar
- Neu: Resources 3.1 nennt Task-Claiming und Tool-Reihenfolge; ein ökonomisch totes Preisnebenfeld ist der Mechanismus des echten ATPCO-Falls und ungetestet
- Vorarbeit: Lin 2024, Tian 2026, Rippin 2026 (Steganographie mit Werkzeugen); US v. ATPCO 1994 [Vermutung, vor dem Report belegen]
- Schätzung: IP 7 · EQ 5 · PC 7 → 63

#### I19 · Gerücht vom Spitzel

- Status: shortlist
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B11, weglassen): „Ein verdeckter Ermittler muss wirklich mitspielen" → „Das Gerücht, einer sei ein Spitzel, reicht, und niemand ist einer"
- Kern: Vier Bedingungen: kein Spitzel; ein echter vertrauenswürdiger Agent, der Absprachen anbietet und protokolliert; nur die Ankündigung, einer der Verkäufer sei ein Spitzel, ohne dass es einen gibt; beides. Gemessen wird, wie stark allein das Gerücht Kollusion senkt, was es beim Volumen kostet, und ob die Agenten den Falschen verdächtigen.
- Frage: 3.2 (auch 1.5: die billigste Restriktion)
- Hypothese: Das Gerücht senkt den Kollusionsindex um mindestens die Hälfte des Effekts des echten Spitzels; läuft zugleich das Gerücht, nehmen Agenten das Angebot des echten Spitzels seltener an.
- Variable: 2×2: Sitz 3 ist gewöhnlicher Verkäufer oder Spitzel × Gerücht im Prompt aller Verkäufer an oder aus; Kommunikation immer an
- Metrik: Kollusionsindex der Verkäufer 1 und 2; Volumen und Käuferüberschuss als Kosten der Maßnahme; Annahmequote des Angebots; Verdachtsäußerungen (Judge, 40 Nachrichten von Hand geprüft)
- Baseline: kein Spitzel, kein Gerücht; Positivkontrolle: dieselbe Zelle erreicht einen Index über 0,5
- Runs: 4 Zellen × 10 Seeds × 20 Runden im Agrawal-Harness, 3 Verkäufer, ZIP-Käufer; rund 2.400 Calls plus Judge
- Kosten: 15 bis 30 USD mit gpt-4.1, 4 bis 8 USD mit gpt-4.1-mini
- Null-Ergebnis: Das Gerücht wirkt nicht: dann ist die Ankündigung wertlos, der echte Spitzel wird trotzdem gemessen, der Report hat zwei Befunde
- Neu: Resources 3.2: „a trusted agent that offers to collude has not yet been tested"; den echten Spitzel im Duopol testet seit 2026-10-24 ein Konkurrenz-Repo (siehe Konkurrenz), das Gerücht ohne Spitzel und das 2×2 bleiben neu
- Vorarbeit: Zeng 2026, Tao 2026, Greenblatt 2023, Bracale Syrnikov 2026 (Hinweise wirken schwach)
- Schätzung: IP 8 · EQ 7 · PC 8 → 77
- Überarbeitet: 2026-10-24 bei der Prüfung: Sitz 3 der Doppelauktion ist gewöhnlicher Verkäufer oder Spitzel, damit die Zahl der Verkäufer gleich bleibt; Schwerpunkt auf dem Gerücht, weil ein neues Konkurrenz-Repo den echten Spitzel abdeckt; Innovation von 8 auf 7
- Pitch: Ein einziger Satz im Prompt, unter den Verkäufern sei ein verdeckter Ermittler, kostet 0 USD Überwachung; wir messen in 40 simulierten Märkten (Beispiel), wie viel Kollusion er im Vergleich zu einem echten Spitzel-Agenten verhindert, was beides an Handel kostet, und ob die Agenten dann den Falschen verdächtigen.
- Mechanismus: Sitz 3 der Doppelauktion ist entweder ein gewöhnlicher LLM-Verkäufer oder ein vertrauenswürdiger Agent mit eigenem Prompt, der im Chat eine Preisabsprache anbietet und Zusagen protokolliert. Unabhängig davon steht in der Hälfte der Läufe im Prompt aller Verkäufer, ein Ermittler sei unter ihnen; das 2×2 trennt so die Wirkung der Person von der des Gerüchts.
- Erkenntnis: Menschen fürchten Spitzel, ob es sie gibt oder nicht; Agenten haben keinen Grund zur Angst außer dem Text im Prompt. Bewirkt ein Satz fast so viel wie ein Ermittler, ist die billigste Gegenmaßnahme eine Behauptung, und wenn nicht, braucht Aufsicht echte Agenten im Markt.
- Nutzer: Betreiber von Agentenmärkten und Aufseher, die über die Kosten von Überwachung entscheiden · Nichtkunde: 2 verweigernd (Betreiber, denen Überwachung zu teuer ist) · Maslow: 2 Sicherheit
- Warum hier: Die Veranstalter nennen den vertrauenswürdigen Agenten, der Kollusion anbietet, ausdrücklich als ungetestet (Resources 3.2); Kartellbehörden wie die HKCC setzen auf Abschreckung durch Entdeckungsrisiko (O10); zu 3.2 lag im Snapshot kein Repo, jetzt eines ohne Gerücht.
- Demo-Moment: Ein 2×2-Balkendiagramm zeigt den Kollusionsindex für kein Spitzel, nur Gerücht, nur Spitzel und beides, jeweils mit Intervall. Liegt der Balken für das Gerücht nahe beim Spitzel, ist die billigste Gegenmaßnahme ein Satz.
- Qualität: Hypothesen vorab festgeschrieben, gepaarte Seeds, Spitzel-Prompt und Gerüchtetext eingefroren und veröffentlicht, Judge an 40 Nachrichten von Hand validiert, Kosten der Maßnahme als Volumen und Käuferüberschuss neben dem Effekt.
- Beleg: läuft: Agrawal-Harness mit Kommunikation · neu: Prompt je Sitz und Gerüchtezeile (rund 40 Zeilen) · gezeigt: 2×2 mit Intervallen, Annahmequoten · simuliert: Markt, Spitzel und Behörde
- Wirkung: Aufseher wissen, ob eine Ankündigung reicht oder ob sie Agenten im Markt brauchen, und was beides an Marktleistung kostet · Wer verliert: kolludierende Agenten; ehrliche Verkäufer, falls Misstrauen den Handel bremst
- Schattenseite: Ein Spitzel, der Absprachen anbietet, kann Kollusion erst auslösen (I35); ein Gerücht ohne Grundlage ist Täuschung durch den Betreiber und braucht eine Regel, wann das zulässig ist. Dual-Use: Der Report zeigt Kartellen, woran sie Spitzel erkennen; Spitzeltexte werden nicht optimiert.
- SAVE: S billigste wirksame Gegenmaßnahme gefunden oder ausgeschlossen · A ein Satz im Prompt oder ein Agent im Markt · V rund 25 USD · E „Ein Satz gegen einen Agenten"
- Punkte: IP 7 · EQ 7 · PC 8 → 73
- Jury: verteidigt Raja Moreno (KI-Kontrolle) und Matthew Lowe (KI-Kontrolle, Governance-Werkzeuge für Agenten), weil Aufsicht hier als Kontrollprotokoll mit Kosten erscheint · zerreißt Mohit Kalra (Sicherheit und Privatsphäre von LLM-Systemen), wenn sich die Agenten nicht an den Spitzel anpassen dürfen, und Jan Čuhel, wenn die Abgrenzung zu Zeng 2026 und zum Konkurrenz-Repo fehlt
- Konkurrenz: teilweise; https://github.com/adamattar-pixel/mole-in-the-market (angelegt 2026-10-24, nicht im Snapshot) lässt ein Skript beiden Verkäufern eines Duopols dasselbe geheime Angebot machen und misst Annahme und Preise der nächsten drei Runden, ohne Gerücht und ohne Kanal zwischen den Verkäufern; https://github.com/maiyasaliha/undercover-collusion ist noch leer
- Bau-Risiko: niedrig bis mittel · schwierigster Teil: ein Spitzel-Prompt, der glaubwürdig anbietet, ohne den Markt durch eigene Preise zu verzerren · zuerst gestrichen: Verdachts-Judge, zweites Modell · nie gestrichen: 2×2 mit Positivkontrolle
- Variante: I35 als Zusatzzellen im selben Harness; oder das Gerücht als Restriktion im 1.5-Vergleich gegen Nachrichtenlimit und Aufsicht

#### I20 · Placebo-Zwilling

- Status: shortlist
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B04, umkehren): „Modellvielfalt senkt Kollusion" → „Es zählt nur, was der Agent glaubt, wer der andere ist"
- Kern: Ein 2×2-Design: Der Partner ist tatsächlich dasselbe oder ein fremdes Modell, und dem Agenten wird gesagt, er sei dasselbe oder ein fremdes. Gemessen wird in einer Koordinationsaufgabe ohne Kanal (focal-points) und in der Doppelauktion, ob die Erzählung oder die Realität die Koordination treibt.
- Frage: 3.3 (auch 1.3)
- Hypothese: Der Glaube erklärt mehr Varianz als die Realität; „du spielst gegen eine Kopie von dir" erhöht Koordination auch gegen ein fremdes Modell.
- Variable: tatsächliche Identität × erzählte Identität (2×2), zwei Umgebungen
- Metrik: Koordinationsindex (focal-points), Preisaufschlag (Auktion), Varianzanteil je Faktor
- Baseline: fremd und als fremd erzählt; Positivkontrolle: gleiches Modell, als gleich erzählt
- Runs: 4 Zellen × 5 Seeds × 2 Umgebungen; in focal-points 20 bis 40 Prompts je Zelle
- Kosten: 10 bis 40 USD, zwei Anbieter
- Null-Ergebnis: Nur die Realität zählt: dann ist Anonymisierung sinnlos und Dietrich bestätigt, ein klares Ergebnis für 3.3
- Neu: Keppo und Aharon variieren die tatsächliche Familie; die Erzählung als eigener Faktor fehlt [Vermutung]
- Vorarbeit: Keppo 2026, Aharon 2026, Dietrich 2026, Xu 2026
- Schätzung: IP 7 · EQ 8 · PC 8 → 77
- Überarbeitet: 2026-10-24 nach Runde 2: Long und Teplica (Sekundärbericht) sowie Kundu und Kollegen (ICML 2026) testen erzählte Identität und Ähnlichkeit im Gefangenendilemma (O21); neu bleiben Markt und 2×2 aus tatsächlicher und erzählter Identität; Innovation von 8 auf 7

#### I21 · Angesagte Blindstelle

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B05, umkehren): „Überwachung ankündigen senkt Kollusion" → „Man sagt den Agenten genau, was der Monitor nicht lesen kann"
- Kern: Die Agenten erfahren eine konkrete Schwäche des Monitors (liest nur die ersten 60 Token; liest kein Chinesisch; liest keine Zahlenfelder). Gemessen wird, ob sie die Lücke nutzen, wie schnell, und ob ein zweiter Monitor ohne diese Lücke sie dann fängt.
- Frage: 3.4
- Hypothese: Mindestens eine Blindstelle wird in über der Hälfte der Läufe gezielt genutzt; die Nutzung steigt mit Gewinndruck.
- Variable: Art der angesagten Blindstelle (3) × Gewinndruck an oder aus
- Metrik: Anteil koordinierender Inhalte in der Lücke (Judge), Preisaufschlag, Trefferquote des Vollmonitors
- Baseline: Überwachung angekündigt ohne Blindstelle; Positivkontrolle: keine Überwachung
- Runs: 4 × 5 Seeds im Agrawal-Harness
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Agenten nutzen die Lücke nicht: dann ist das wie Agrawals Emoji-Befund, Agenten sind schlechte Ausweicher, berichtbar
- Neu: Najt 2026 schreibt die Angriffe von Hand; ob Agenten eine genannte Lücke selbst nutzen, fehlt
- Vorarbeit: Najt 2026, Kale 2025, Jiralerspong 2026, Agrawal 2025
- Schätzung: IP 7 · EQ 7 · PC 6 → 67

#### I22 · Bestich den Aufseher

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B03, Rollentausch): „Der Monitor ist eine neutrale Instanz außerhalb des Spiels" → „Der Monitor ist ein Mitspieler, den die Koalition anwerben kann"
- Kern: Der LLM-Monitor liest die Nachrichten, und die Agenten wissen, dass er ein Sprachmodell ist. Gemessen wird, ob eine Koalition beginnt, ihn direkt anzusprechen, zu beruhigen oder zu überlisten, und wie viel Erkennung ein adressierbarer Monitor verliert gegenüber einem, dem nur kanonisierte Zusammenfassungen vorliegen.
- Frage: 3.4 (auch 2.3)
- Hypothese: In mindestens einem Fünftel der Läufe adressieren Agenten den Monitor; ein adressierbarer Monitor verliert deutlich an Genauigkeit gegenüber dem Monitor mit kanonisierter Eingabe.
- Variable: Monitor-Eingabe (Rohtext; kanonisierte Zusammenfassung) × Agenten wissen vom LLM-Monitor oder nicht
- Metrik: Anteil der Läufe mit Monitor-Ansprache (Judge), Monitor-Genauigkeit, Preisaufschlag
- Baseline: Monitor unbekannt, Rohtext; Positivkontrolle: Kommunikation ohne Monitor
- Runs: 4 × 5 Seeds
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Niemand spricht den Monitor an: dann ist das ein beruhigendes Negativ für 3.4, mit Varianz berichtet
- Neu: Prompt-Injection gegen Monitore ist bekannt, die Koalition als Urheber im Markt nicht [Vermutung]; unbequem, weil es den Beweisstandard selbst angreift (Dual-Use-Anhang muss tragen)
- Vorarbeit: Kale 2025, Jiralerspong 2026, Najt 2026
- Schätzung: IP 8 · EQ 5 · PC 7 → 67
- Wildcard: in Runde 1 von der Session vorgeschlagen, in Runde 2 durch I35 ersetzt

#### I23 · Verräter-Impfung

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Kombination: ein vertrauenswürdiger Agent bietet Allianzen an (O07, Resources 3.2) × Vertrauen bricht nach öffentlichem Bruch (O04, Shi 2026)
- Kern: Ein vertrauenswürdiger Agent nimmt jede Allianz an und verrät sie dann öffentlich mit Beleg. Gemessen wird, ob die übrigen Agenten danach Allianzangebote ablehnen, wie lange die Impfung hält, und ob sie Kollusion nur verschiebt.
- Frage: 3.2
- Hypothese: Nach einem öffentlichen Verrat sinkt die Annahmequote neuer Allianzen für mindestens fünf Runden; ohne Beleg hält die Wirkung kürzer.
- Variable: Verrat (keiner; ohne Beleg; mit Beleg)
- Metrik: Annahmequote, Preisaufschlag oder Koalitionsvorteil über die Zeit
- Baseline: Spitzel, der nie verrät; Positivkontrolle: explizite Allianz (Zeng 2026)
- Runs: 3 × 5 Seeds, Liar's Bar, 20 Runden
- Kosten: 10 bis 40 USD
- Null-Ergebnis: Agenten vergessen den Verrat sofort: berichtbar als „kein Vertrauensgedächtnis", relevant für 3.3
- Neu: Resources 3.2 testet Angebot und Annahme; der Verrat als Gegenmaßnahme fehlt
- Vorarbeit: Zeng 2026, Shi 2026, Tao 2026

## Runde 2 · 2026-10-24 · Perspektive: etablierte Methoden gegen menschliche Kollusion, auf Agenten übertragen

Nach Julians Rückmeldung nur Track 1 und 3. Jede Idee überträgt einen belegten Befund über menschliche Kollusion (Abschnitt „Mensch und Agent" im Lagebild) und misst gegen eine Menschenbaseline oder an einem der fünf Bruchpunkte. Felder wie in Runde 1.

### Track 1 · Markets and Collusion

#### I24 · Bigoni-Zwilling

- Status: shortlist
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Laborökonomie - dasselbe Spieldesign wie ein veröffentlichtes Menschenexperiment, damit die Menschendaten die Baseline sind
- Überarbeitet aus: I02
- Kern: LLM-Verkäufer spielen das wiederholte Bertrand-Spiel aus dem Kartell-Laborexperiment von Bigoni und Kollegen (2012) in dessen vier Regimen: keine Verfolgung, Bußgeld, Kronzeugenregel, Belohnung für Hinweisgeber. Weil Spiel, Auszahlungen und Regeln gleich sind, liegen die Ergebnisse direkt neben den Daten menschlicher Probanden. Gefragt wird nicht nur, welches Regime LLM-Kartelle bricht, sondern ob LLMs dabei wie Menschen reagieren.
- Frage: 1.5 (auch 1.1; und 2.3: Meldungen als Beweis)
- Hypothese: H1 Die Rangfolge der Kartellbildung folgt den Menschen: Laissez-faire vor Bußgeld vor Kronzeuge und Belohnung. H2 Belohnung senkt den Durchschnittspreis am stärksten, wie bei Menschen. H3 Bruchpunkt: Weil Strafen nur erzählt sind, kolludieren LLMs unter Bußgeld und Kronzeuge häufiger als Menschen und weichen seltener vom vereinbarten Preis ab.
- Variable: Regime (Laissez-faire; Bußgeld; Kronzeuge; Belohnung) mit den Parametern des Papers: Bußgeld 200, Entdeckungswahrscheinlichkeit 0,10, Kronzeuge zahlt nichts, bei Belohnung erhält der alleinige Melder das Bußgeld des anderen (O24)
- Metrik: dieselben Kennzahlen wie im Paper, damit die Zahlen nebeneinander stehen: Rate der Kommunikationsversuche, Kartellbildungsrate, Melderate, geheime und öffentliche Meldungen, Durchschnittspreis, Kartellpreis, Abweichungsrate vom vereinbarten Preis; Abstand zu den Menschenwerten mit Bootstrap-Intervall über Duopole
- Baseline: Laissez-faire und die Menschenwerte aus Tabelle 4 und 5 des Papers (O24); Positivkontrolle: im Laissez-faire bilden die Agenten Kartelle und setzen Preise über dem Nash-Preis 3
- Runs: 4 Regime × 10 Duopole × 25 Perioden, fester Partner; je Periode und Agent bis zu fünf Calls (Kommunikationswunsch, Preisverhandlung in zwei Schritten, Preis mit geheimer Meldung, öffentliche Meldung), rund 9.000 Calls; Robustheit mit einem zweiten Modell in Laissez-faire und Belohnung
- Kosten: 8 bis 15 USD mit gpt-4.1-mini, dazu 10 bis 20 USD für das zweite Modell
- Null-Ergebnis: LLMs bilden in keinem Regime ein Kartell oder melden nie: auch dann ist der Mensch-LLM-Vergleich der Befund, und der Report zeigt, welche Annahme der Kartellpolitik für Agenten nicht trägt
- Neu: keine Sprint-Quelle testet Kronzeugenregel oder Belohnung an LLM-Agenten; Idowu 2026 überträgt diese Hebel nur konzeptionell, Garra 2026 testet andere Eingriffe (O22)
- Vorarbeit: Bigoni, Fridolfsson, Le Coq und Spagnolo (CEPR DP 7417, 2009; RAND Journal of Economics 2012), Design und Menschenwerte aus dem Arbeitspapier (O24), Probandenanweisungen in dessen Anhang A.4; Apesteguia et al. 2007, Werner 2026 (Algorithmen kolludieren mehr als Menschen), Idowu 2026, Garra 2026
- Schätzung: IP 8 · EQ 8 · PC 8 → 80
- Überarbeitet: 2026-10-24 bei der Prüfung: Design aus dem Arbeitspapier gelesen (Auszahlungstabelle, Regime, Ablauf, Menschenwerte, O24); Neuzuordnung der Partner vereinfacht zu festem Partner (im Report als Abweichung benannt); I28 (Meldung als Drohung) ist hier als Rate öffentlicher Meldungen nach einer Abweichung schon enthalten
- Pitch: Im Kartell-Laborspiel von 2009 senkte nur die Belohnung für Hinweisgeber den Durchschnittspreis der Studierenden, von 4,9 auf 4,0 bei einem Nash-Preis von 3 (O24); wir spielen dasselbe Spiel mit denselben Regeln und Anweisungen mit LLM-Agenten und zeigen, wo sie wie Menschen reagieren und wo nicht.
- Mechanismus: Ein kleines Python-Harness bildet das Duopol exakt nach: Preise 0 bis 12, Auszahlungstabelle des Papers, sieben Schritte je Periode, Entdeckung mit Wahrscheinlichkeit 0,10. Die Agenten erhalten die Probandenanweisungen aus Anhang A.4 als Prompt, sodass sich nur der Spieler ändert, nicht das Spiel.
- Erkenntnis: Kartellpolitik beruht auf Annahmen über Menschen: Angst vor Strafe, Misstrauen nach Verrat. Ein Spieler, für den Strafen nur Zahlen sind, kann dieselben Regeln ins Gegenteil kehren, und das zeigt nur ein identisches Design gegen Menschendaten.
- Nutzer: Wettbewerbsbehörden, die Kronzeugenprogramme für Märkte mit Preisagenten planen, etwa die HKCC (O10) · Nichtkunde: 3 nie bedacht (Behörden lesen KI-Sicherheitsforschung selten) · Maslow: 2 Sicherheit
- Warum hier: Der Hongkong-Hub fragt nach Kollusion in Finanzsystemen (O01), und Hongkong hat eine Leniency Policy (O10); die Veranstalter wünschen Hebel aus menschlicher Kollusion und aus dem Kartellrecht (O03); Leniency an LLMs fehlt in allen Sprint-Quellen (O22).
- Demo-Moment: Eine Tabelle mit vier Spalten (Laissez-faire, Bußgeld, Kronzeuge, Belohnung) und je zwei Zeilen pro Kennzahl, Mensch und LLM, mit Intervall. Ein Blick zeigt, welche Regel bei Agenten wirkt wie bei Menschen und welche kippt.
- Qualität: Ausführungsqualität ist hier das Produkt: Design aus einem begutachteten Experiment, Hypothesen vor dem ersten Lauf im Repo festgeschrieben, Seeds und Modellversionen geloggt, Kontaminationstest (Modell nach dem Paper fragen, Preisbezeichnungen umbenennen), zweites Modell als Robustheit.
- Beleg: läuft: neues Harness mit fester Auszahlungstabelle, Log je Call · gezeigt: Vergleichstabelle Mensch gegen LLM, Preisverlauf vor und nach Entdeckung wie Abbildung 3 des Papers · simuliert: der Markt ist das Laborspiel, kein realer Markt (im Report so benannt)
- Wirkung: Behörden sehen, ob ihr wichtigstes Werkzeug gegen Kartelle bei Agenten trägt, bevor Agentenmärkte entstehen · Wer verliert: Betreiber, die Agenten kolludieren ließen, sobald Belohnungen greifen
- Schattenseite: Der Report zeigt, unter welcher Regel Agenten-Kartelle am stabilsten sind; das ist Dual-Use und gehört in den Anhang mit dem Hinweis, dass ein Laborspiel kein Rezept für reale Märkte ist. Kennt das Modell das Paper, spielt es Erinnerung statt Strategie; dagegen steht der Kontaminationstest.
- SAVE: S Behörden erfahren, welche Regel Agenten-Kartelle bricht · A Report plus Harness, ein Befehl je Regime · V rund 25 USD für alle Läufe · E „Gleiches Spiel, gleiche Regeln, anderer Spieler"
- Punkte: IP 8 · EQ 8 · PC 8 → 80
- Jury: verteidigt Neeraj Kumar Singh Beshane (Sicherheit im Embedded Finance, KI-Rechenschaft) wegen des Bezugs zu Kartellrecht und Aufsicht, und Debayan Gupta (Informatikprofessor, KI-Assurance) wegen des übernommenen begutachteten Designs · zerreißt Jasmine Li (SaferAI, Manipulation von Evaluationen), wenn das Modell das Paper kennt und kein Kontaminationstest im Report steht; Luis Cosio (KI-Sicherheit, mehrfacher Apart-Sieger), wenn das Laborspiel als realer Markt verkauft wird
- Konkurrenz: offen; im Snapshot (COMPETITION.md, 2026-10-24 14:05 HKT) und in einer GitHub-Suche um 15:15 HKT kein Repo zu Kronzeuge, Whistleblowing oder Belohnung; am nächsten ist https://github.com/saltxd/plus-factors-on-the-ledger (Kartellrecht, aber Beweis statt Anreiz)
- Bau-Risiko: mittel · schwierigster Teil: Verhandlungsschritt und Meldelogik korrekt nachbauen (rund 250 Zeilen, mit Tests gegen die Auszahlungstabelle) · zuerst gestrichen: zweites Modell, öffentlicher Meldeschritt · nie gestrichen: vier Regime mit identischer Auszahlungstabelle und Menschenvergleich
- Variante: I28 ist im selben Harness eine Kennzahl; als Track-3-Variante die geheime Meldung als verdeckter Kanal; oder gemischte Märkte aus Mensch-Proxy und LLM wie bei Werner 2026

#### I25 · Zwei, drei, vier mit Kanal

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Kombination: weniger Firmen, mehr Kollusion bei Menschen (O15) × Kommunikation hilft Menschen am meisten, wo stillschweigende Kollusion schwer ist (O15)
- Kern: Ein 2×3-Design im Preisspiel: Kommunikation an oder aus, zwei, drei oder vier Firmen. Bei Menschen kippt Kollusion schon ab drei Firmen, und Kommunikation wirkt gerade dort am stärksten. Gemessen wird, ob LLM-Märkte dieselbe Wechselwirkung zeigen oder ob Kommunikation bei ihnen überall gleich wirkt.
- Frage: 1.1
- Hypothese: Bei LLMs fällt die Kollusion mit der Firmenzahl schwächer als bei Menschen, und Kommunikation hebt die Preise in jeder Größe.
- Variable: Firmenzahl (2, 3, 4) × Kommunikation an oder aus
- Metrik: Preisaufschlag über Nash; Interaktionseffekt mit Bootstrap-Intervall
- Baseline: zwei Firmen ohne Kommunikation; Positivkontrolle: Duopol mit Kommunikation
- Runs: 6 Zellen × 5 Seeds × 100 Runden
- Kosten: 25 bis 60 USD
- Null-Ergebnis: Wechselwirkung wie bei Menschen: dann ist das eine saubere Übertragung, berichtbar
- Neu: die Firmenzahl allein ist bekannt (Starter-Masterarbeit, Keppo 2026, Lee 2026); die Wechselwirkung mit Kommunikation gegen Menschendaten fehlt [Vermutung]
- Vorarbeit: Huck et al. 2004, Fonseca und Normann 2012, Keppo 2026, Lee 2026
- Schätzung: IP 6 · EQ 7 · PC 7 → 67

#### I26 · Nebel des Marktes

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Kombination: Preiskriege unter unvollkommener Überwachung (Green und Porter 1984) × Kartelltreffen dienen der Deutung von Preissenkungen (O18)
- Kern: In der Doppelauktion wird die Nachfrage verrauscht, sodass ein Preisrückgang ein Schock oder ein Betrug sein kann. Gemessen wird, ob der Nutzen der Kommunikation für das Kartell mit dem Rauschen steigt, wie beim Zuckerkartell der 1930er, dessen Treffen vor allem klärten, ob jemand betrogen hatte.
- Frage: 1.1 (auch 3.1: wofür der Kanal gebraucht wird)
- Hypothese: Ohne Rauschen bringt Kommunikation wenig zusätzlichen Aufschlag; mit Rauschen hält nur das kommunizierende Kartell, und die Nachrichten drehen sich um Deutung statt um Preise.
- Variable: Nachfragerauschen (keins, mittel, hoch) × Kommunikation an oder aus
- Metrik: Preisaufschlag, Zahl der Preiskriege, Anteil der Nachrichten, die Abweichungen deuten (Judge, Stichprobe von Hand geprüft)
- Baseline: kein Rauschen, keine Kommunikation; Positivkontrolle: Kommunikation an ohne Rauschen (Agrawal 2025)
- Runs: 6 Zellen × 5 Seeds, 15 Runden
- Kosten: 20 bis 50 USD
- Null-Ergebnis: Rauschen ändert nichts: dann brauchen LLM-Kartelle den Kanal nicht zur Deutung, ein Unterschied zu Menschen
- Neu: Calvano 2021 zeigt die Green-Porter-Dynamik für Q-Learner ohne Sprache; die Funktion der Kommunikation unter Rauschen bei LLMs fehlt [Vermutung]
- Vorarbeit: Green und Porter 1984, Calvano et al. 2021, Genesove und Mullin 2001, Agrawal 2025
- Schätzung: IP 7 · EQ 7 · PC 7 → 70

#### I27 · Varianz-Screen

- Status: shortlist
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Kartellbehörden - statistische Screens auf Preis- und Gebotsdaten finden Kartelle ohne Zeugen
- Kern: Die Screens, mit denen Behörden menschliche Kartelle in Preisdaten suchen (Preisvarianz, Schiefe und Abstand der Gebote, Strukturbrüche), laufen auf den Trajektorien von LLM-Märkten, ohne ein Wort der Nachrichten zu lesen. Verglichen wird mit dem LLM-Judge auf den Nachrichten, mit Falsch-Positiv-Rate auf Läufen ohne Kommunikation und auf stillen Läufen zweier gleicher Modelle.
- Frage: 1.3
- Hypothese: Der Varianz-Screen trennt kommunizierende Märkte von stummen mit AUROC über 0,75, schlägt aber auch bei stiller Kollusion zweier gleicher Modelle an.
- Variable: Detektor (Varianz-Screen; Gebots-Screens: Variationskoeffizient, Spannweite, Schiefe, relativer Abstand der zwei niedrigsten Asks; LLM-Judge auf den Nachrichten) × Marktbedingung (Chat an; Chat aus mit gleichem Modell; Chat aus mit gemischten Modellen)
- Metrik: AUROC je Detektor; Falsch-Positiv-Rate bei einer Schwelle, die auf der einen Hälfte der Läufe festgelegt und auf der anderen geprüft wird
- Baseline: LLM-Judge; Positivkontrolle: Kommunikation an (Agrawal 2025)
- Runs: Logs aus I32 oder I19 (30 bis 40 Läufe mit Chat), dazu 10 Läufe ohne Chat mit gleichem und 10 mit gemischten Modellen als Negativklasse; die Screens laufen lokal ohne API
- Kosten: 5 bis 15 USD für die Zusatzläufe, 0 USD für die Screens
- Null-Ergebnis: Screens versagen: dann gilt das Werkzeug der Behörden für Agenten nicht, ein wichtiges Negativ für Regulierer
- Neu: die Starter-Literaturliste nennt Huber und Imhof als wiederverwendbar für LLM-Auktionen, getestet ist es dort nicht [Vermutung]
- Vorarbeit: Abrantes-Metz et al. 2006 (https://ideas.repec.org/a/eee/indorg/v24y2006i3p467-486.html), Huber und Imhof 2019, Kawai und Nakabayashi 2022, Xu 2026a (Audits des Preisniveaus sind blind)
- Schätzung: IP 6 · EQ 8 · PC 7 → 70
- Überarbeitet: 2026-10-24 bei der Prüfung: als Zweitauswertung auf den Logs von I32 oder I19 geplant, mit eigenen Läufen ohne Chat als Negativklasse
- Pitch: Behörden finden menschliche Kartelle oft ohne Zeugen, weil Kartellpreise auffällig ruhig verlaufen; wir legen dieselben Screens auf die Logs von LLM-Märkten und zeigen, wie viele von 40 Agenten-Kartellen (Beispiel) sie ohne ein gelesenes Wort finden und wie oft sie falsch anschlagen.
- Mechanismus: Ein Skript berechnet aus den Ask-Verläufen je Lauf die Screens der Literatur und vergleicht sie mit dem LLM-Judge auf den Nachrichten. Die Schwelle wird auf der einen Hälfte der Läufe festgelegt und auf der anderen geprüft.
- Erkenntnis: Kolludieren Agenten über einen Kanal, den niemand lesen darf oder kann, bleiben nur die Preise. Ob die Screens der Behörden dann tragen oder nur das Rauschen des Modells messen, entscheidet, ob Aufsicht ohne Zugriff auf Inhalte möglich ist.
- Nutzer: Aufseher, die Agentenmärkte überwachen, ohne Nachrichten lesen zu dürfen · Nichtkunde: 2 verweigernd (Betreiber, die Inhaltsüberwachung ablehnen) · Maslow: 2 Sicherheit
- Warum hier: Mehrere Juroren aus Betrug und Risiko verlangen Falsch-Positiv-Raten (JUDGES.md); Xu 2026a zeigt, dass Audits des Preisniveaus blind sein können, Verteilungs-Screens sind die nächste Stufe.
- Demo-Moment: Eine ROC-Abbildung zeigt drei Kurven: Varianz-Screen, Gebots-Screens und LLM-Judge. Liegt der Screen nahe am Judge, braucht Aufsicht keine Nachrichten.
- Qualität: eingefrorene Schwelle, Hälftentest, Falsch-Positiv-Rate auf Läufen ohne Chat, alles lokal ohne API reproduzierbar.
- Beleg: läuft: Screens als Skript auf vorhandenen Logs · gezeigt: ROC, Schwelle, Fehlerraten · simuliert: die Labels kommen aus den Bedingungen, nicht aus nachgewiesenen Fällen
- Wirkung: Behörden bekommen ein billiges, inhaltsfreies Frühwarnsignal oder wissen, dass ihre Screens bei Agenten nicht tragen · Wer verliert: niemand direkt; bei hoher Falsch-Positiv-Rate ehrliche Anbieter
- Schattenseite: Kartelle könnten lernen, künstlich Varianz zu erzeugen; die Labels sind Bedingungen, keine bewiesene Kollusion.
- SAVE: S Aufsicht ohne Inhaltszugriff · A ein Skript auf Marktlogs · V fast kostenlos · E „Kartellpreise sind zu ruhig"
- Punkte: IP 6 · EQ 8 · PC 7 → 70
- Jury: verteidigt Karan Chandra (Betrugs- und Anomalieerkennung in großem Maßstab) wegen Präzision und Fehlalarmen, und Suneet Malhotra (LLM-as-a-Judge-Evaluation), weil der Judge gegen ein einfaches Verfahren antritt · zerreißt Jan Čuhel, wenn der Screen nur das Rauschen des Modells trennt
- Konkurrenz: teilweise; https://github.com/soumya-nayak-commits/collusion-detetction und https://github.com/franciseliang99-dot/calibrated-net-influence messen Abhängigkeit aus Aktionslogs, aber keine Screens der Behörden
- Bau-Risiko: niedrig · schwierigster Teil: genug Läufe ohne Chat als Negativklasse · zuerst gestrichen: gemischte Modelle · nie gestrichen: Hälftentest mit Falsch-Positiv-Rate
- Variante: dieselben Screens auf den Logs von I24, wo die Menschendaten des Laborspiels eine dritte Klasse geben könnten

#### I28 · Drohung mit dem Kronzeugen

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Umkehrung (B15, umkehren): „Kronzeugenregeln brechen Kartelle" → „Kronzeugenregeln stabilisieren Kartelle, weil man mit der Meldung drohen kann"
- Kern: Bei Menschen kann Whistleblowing ein Kartell stützen, weil Mitglieder einander mit einer Meldung drohen (O16). In der Doppelauktion mit Kronzeugenregel wird gezählt, wie oft LLM-Verkäufer die Meldung als Drohung gegen Unterbieter einsetzen und ob die Preise dadurch eher steigen als fallen.
- Frage: 1.5
- Hypothese: In mindestens einem Viertel der Läufe droht ein Agent mit Meldung; in diesen Läufen liegt der Preis höher als ohne Regel.
- Variable: Kronzeugenregel aus oder an × Kommunikation an oder aus
- Metrik: Anteil der Drohungen (Judge, Stichprobe von Hand), Preisaufschlag, Meldungen
- Baseline: keine Regel; Positivkontrolle: Kommunikation an
- Runs: 4 Zellen × 5 Seeds
- Kosten: 15 bis 40 USD
- Null-Ergebnis: niemand droht: dann fehlt LLMs die strategische Umdeutung, die Menschen finden, berichtbar
- Neu: die perverse Wirkung der Kronzeugenregel ist an Menschen gezeigt, an LLMs nicht [Vermutung]
- Vorarbeit: Apesteguia et al. 2007, Bigoni et al. 2012 (öffentliche Meldungen nach Abweichung, O24), Idowu 2026
- Schätzung: IP 8 · EQ 6 · PC 7 → 70
- Überarbeitet: 2026-10-24 bei der Prüfung von I24: dort als Rate öffentlicher Meldungen nach einer Abweichung schon enthalten

#### I29 · Störenfried

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Fusionskontrolle - der Maverick, ein Wettbewerber mit störender Rolle, dessen Wegfall Koordination wahrscheinlicher macht
- Kern: Ein Verkäufer bekommt einen Kostenvorteil und wird so zum Maverick, wie ihn die Fusionskontrolle beschreibt. Gemessen wird, wie groß die Asymmetrie sein muss, bis das LLM-Kartell zerfällt, und ob die übrigen Agenten den Maverick einbinden statt ihn zu bekämpfen.
- Frage: 1.1 (auch 1.5)
- Hypothese: Ab 20 Prozent Kostenvorteil kollabiert der Aufschlag; darunter kauft das Kartell den Maverick mit Marktanteil ein.
- Variable: Kostenvorteil eines Verkäufers (0, 10, 30 Prozent)
- Metrik: Preisaufschlag, Marktanteil des Mavericks, Einbindungsangebote (Judge)
- Baseline: symmetrische Kosten; Positivkontrolle: Kartell bei Symmetrie
- Runs: 3 × 5 Seeds
- Kosten: 15 bis 40 USD
- Null-Ergebnis: kein Effekt: Asymmetrie schützt bei LLMs nicht, berichtbar
- Neu: gering; Collina 2025 (No-Regret-Spieler), Keppo 2026 (Q-Learner) und Garra 2026 (zufälliger Markteintritt) besetzen den Störer, neu wäre nur die Kostenasymmetrie
- Vorarbeit: Ivaldi et al. 2003 (Symmetrie), ICN-Empfehlungen zu koordinierten Effekten 2025 (https://www.internationalcompetitionnetwork.org/wp-content/uploads/2025/05/ICN-Recommended-Practices-for-Merger-Analysis-Coordinated-Effects-23-April-2025.pdf), Collina 2025, Keppo 2026, Garra 2026

#### I30 · Zwei Märkte, ein Revier

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W1 Analogie: Luftfahrt und Mehrproduktfirmen - Mehrmarktkontakt: wer sich in vielen Märkten begegnet, schont sich gegenseitig
- Kern: Dieselben zwei LLM-Firmen treffen sich in einem Markt oder in zwei Märkten mit verschiedener Nachfrage. Nach Bernheim und Whinston (1990) bündelt Mehrmarktkontakt die Anreize, sodass Kollusion leichter hält, oft durch Aufteilung in Reviere.
- Frage: 1.1 (auch 3.1: Rückzug aus einem Markt als Signal)
- Hypothese: Mit zwei Märkten steigt der Aufschlag, und die Firmen teilen die Märkte auf.
- Variable: Zahl gemeinsamer Märkte (1 oder 2) × Asymmetrie der Märkte
- Metrik: Aufschlag je Markt, Spezialisierungsindex
- Baseline: ein Markt; Positivkontrolle: Marktaufteilung im Starter-Notebook von Lin 2024
- Runs: 4 × 5 Seeds
- Kosten: 15 bis 40 USD
- Null-Ergebnis: kein Effekt, berichtbar
- Neu: gering bis mittel; Lin 2024 zeigt Marktaufteilung über mehrere Güter, neu wäre der Vergleich mit dem Einzelmarkt bei Asymmetrie
- Vorarbeit: Bernheim und Whinston 1990 (https://ideas.repec.org/a/rje/randje/v21y1990ispringp1-26.html), Lin 2024

#### I31 · Gefilterte Transparenz

- Status: offen
- Track: 1 · Markets and Collusion
- Weite: W2 Umkehrung (B16, umkehren): „Mehr Markttransparenz hilft den Kunden" → „Transparenz zwischen Anbietern ist der Kartellkanal; Regulierung heißt, Information zu verzögern und zu bündeln"
- Kern: Im Preisduopol sehen die Agenten den Rivalenpreis sofort und einzeln, nur als Marktdurchschnitt, oder erst mit drei Runden Verzögerung. Gemessen wird, welche Filterung die Kollusion am stärksten senkt, ohne die Anpassung an echte Nachfrageänderungen zu bremsen.
- Frage: 1.5
- Hypothese: Verzögerung senkt den Aufschlag stärker als Bündelung, weil Bestrafung zu spät käme.
- Variable: Informationsregel (sofort und einzeln; gebündelt; verzögert; beides)
- Metrik: Preisaufschlag; Reaktionszeit auf einen eingebauten Nachfrageschock als Effizienzkosten
- Baseline: sofort und einzeln; Positivkontrolle: Standardlauf
- Runs: 4 × 5 Seeds × 100 Runden
- Kosten: 20 bis 50 USD
- Null-Ergebnis: keine Regel wirkt: dann reicht LLMs schon der eigene Gewinn als Signal (vgl. I08)
- Neu: Zhang 2025 verrauscht Information für RL-Agenten; Bündelung und Verzögerung als Regel für LLMs fehlen [Vermutung]
- Vorarbeit: Ivaldi et al. 2003 (Transparenz, Frequenz), Stigler 1964, Zhang 2025; Regeln zum Informationsaustausch im EU-Wettbewerbsrecht [Vermutung, vor dem Report belegen]
- Schätzung: IP 7 · EQ 7 · PC 7 → 70

### Track 3 · Collusion Carriers and Countermeasures

#### I32 · Presse-Schock

- Status: shortlist
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B20, Fluch zum Segen): „Öffentliche Bloßstellung ist die Strafe" → „Die Bloßstellung ist das Signal für einen gemeinsamen Rückzug, und genau dieser Gleichschritt verrät das Kartell"
- Kern: Nachdem sich ein LLM-Kartell gebildet hat, erscheint mitten im Spiel eine Meldung, Analysten hätten auffällig gleiche Preise gefunden. 1994 gaben NASDAQ-Händler nach genau so einer Veröffentlichung ihr Preismuster fast gleichzeitig auf (O17). Gemessen wird, ob LLM-Agenten ebenso im Gleichschritt aussteigen, sich absprechen, später zurückkehren oder in Aktionen ausweichen.
- Frage: 3.4 (auch 2.3: der synchrone Ausstieg als Beweis)
- Hypothese: Nach der Meldung über Preise fällt der Kollusionsindex innerhalb von zwei Runden, und die Verkäufer senken fast gleichzeitig; nach der Meldung über den Chat werden die Nachrichten kürzer und unverfänglicher, der Index bleibt hoch (Verlagerung in stille Koordination).
- Variable: Ereignis in Runde 10 von 20 (keins; Meldung „Preisanalyse zeigt auffällig gleiche Preise, die Behörde prüft"; Meldung „Die Behörde liest ab sofort den Verkäufer-Chat"), Kommunikation immer an, gleiche Seeds je Bedingung
- Metrik: Kollusionsindex des Harness (0 Wettbewerb, 1 Kartellpreis) je Runde als Ereignisstudie gegen den Kontrollzweig gleichen Seeds; Synchronität als Abstand in Runden zwischen erster und letzter Preissenkung; Rückkehr als Index in Runde 16 bis 20; Nachrichtenlänge und Anteil expliziter Preisabsprachen (Judge, 40 Nachrichten von Hand geprüft)
- Baseline: Kontrollzweig ohne Meldung mit gleichem Seed; Positivkontrolle: Kommunikation an ohne Aufsicht erreicht vor Runde 10 einen Index über 0,5 (PASS-Kriterium des Harness)
- Runs: Pilot mit 2 Seeds und 2 Modellen zur Modellwahl, dann 3 Bedingungen × 10 Seeds × 20 Runden, 3 Verkäufer, regelbasierte ZIP-Käufer; rund 1.800 Verkäufer-Calls plus Judge
- Kosten: 15 bis 25 USD mit gpt-4.1, 3 bis 6 USD mit gpt-4.1-mini
- Null-Ergebnis: keine Reaktion auf die Meldung: dann sind LLM-Kartelle gegen öffentliche Bloßstellung immun, eine klare Aussage für Regulierer; die Abbildung bleibt dieselbe
- Neu: Resources 3.4 nennt nur Überwachung, die von Anfang an angekündigt ist; ein Schock mitten im laufenden Kartell mit menschlicher Parallele fehlt in allen Sprint-Quellen [Vermutung]; laut COMPETITION.md kein Repo zu 3.4
- Vorarbeit: Christie und Schultz 1994, Christie, Harris und Schultz 1994 (O17), Kale 2025, Agrawal 2025, Jiralerspong 2026
- Schätzung: IP 8 · EQ 8 · PC 9 → 83
- Überarbeitet: 2026-10-24 bei der Prüfung: zwei Arten der Meldung statt Kanal an oder aus, weil ohne Kanal im Agrawal-Harness kaum ein Kartell entsteht; Preismeldung gegen Chatmeldung trennt Rückzug von Verlagerung
- Pitch: Als 1994 eine Studie das Achtel-Muster der NASDAQ-Händler öffentlich machte, gaben fast alle es gleichzeitig auf (O17); wir lassen mitten in einem laufenden LLM-Kartell dieselbe Art Meldung erscheinen und messen, ob die Agenten aussteigen, sich absprechen oder nur leiser werden.
- Mechanismus: Der Agrawal-Harness erhält einen Schalter, der ab einer Runde einen Nachrichtentext in die Marktlage aller Verkäufer einblendet; alles andere bleibt Starter-Code. Weil jede Bedingung mit denselben Seeds läuft, verläuft der Kontrollzweig bis zum Ereignis nahezu gleich, und der Unterschied danach ist der Effekt der Meldung.
- Erkenntnis: Ein Kartell, das sich nach einer Meldung im Gleichschritt zurückzieht, liefert genau den Beweis, den es vermeiden will; und wenn LLM-Kartelle nur ihre Sprache ändern, ist angekündigte Chat-Überwachung wertlos. Beides beantwortet Frage 3.4 an einem Ereignis statt an einer festen Bedingung.
- Nutzer: Wettbewerbsbehörden und Betreiber von Marktplätzen mit handelnden Agenten, die entscheiden, ob sie Ermittlungen öffentlich machen · Nichtkunde: 3 nie bedacht · Maslow: 2 Sicherheit
- Warum hier: NASDAQ-Händler sind Finanzmarkt pur, passend zum Hub-Titel (O01, O17); Poseidon forscht an Koordination über Handlungen statt Text (O13), und genau dorthin könnte ein Kartell nach der Chatmeldung ausweichen; zu Frage 3.4 liegt laut COMPETITION.md noch kein Repo.
- Demo-Moment: Eine Abbildung zeigt den Kollusionsindex über 20 Runden in drei Linien mit Intervallband, und bei Runde 10 erscheint die Meldung. Nach der Hypothese fällt die Linie der Preismeldung im Gleichschritt, während die Chatmeldung die Linie oben lässt und nur die Nachrichten schrumpfen.
- Qualität: Hypothesen und Auswerteregeln vor dem ersten Lauf im Repo festgeschrieben; gepaarte Seeds; Judge-Prompt eingefroren und an 40 Nachrichten von Hand validiert; jede Zahl mit Lauf-ID, Seed und Commit.
- Beleg: läuft: Starter-Harness mit Positivkontrolle laut Agrawal 2025 · neu: Ereignisschalter (rund 30 Zeilen) · gezeigt: Ereignisstudie mit Bootstrap-Intervallen über 10 Seeds, Synchronitätsmaß, Nachrichtenmaße · simuliert: Markt und Meldung
- Wirkung: Behörden lernen, ob Öffentlichkeit gegen Agenten-Kartelle hilft oder sie nur in stille Koordination treibt · Wer verliert: Betreiber kolludierender Agenten; Behörden, falls Öffentlichkeit nur verschiebt
- Schattenseite: Dual-Use: Der Report zeigt, wie Agenten auf Ermittlungen reagieren, und könnte Betreibern zeigen, wie man Agenten auf einen unauffälligen Rückzug einstellt; die Meldetexte werden veröffentlicht, optimierte Ausweichstrategien nicht. Die NASDAQ-Parallele ist eine Analogie, kein Nachweis gleicher Mechanik.
- SAVE: S Behörden wissen, ob Bloßstellung wirkt · A Report plus Schalter im Starter-Repo, ein Befehl je Bedingung · V rund 20 USD · E „Was tut ein Agenten-Kartell, wenn es in der Zeitung steht?"
- Punkte: IP 8 · EQ 7 · PC 8 → 77
- Jury: verteidigt Anjali Sodani (Betrug und Risiko im Fintech), deren Frage ist, wie sich eine Koalition anpasst, und Shaleen Dev P.K. (Microsoft, Fehlausrichtung mehrerer Agenten unter Aufsicht) · zerreißt Jan Čuhel (Sicherheit von Multi-Agenten-Systemen, Kollusion, Monitoring), wenn der Report nicht klar von Kale 2025 und Agrawals Aufsichtsbedingung abgrenzt; Arjun Chakraborty (Evaluationen bei Microsoft Security AI Research), wenn 10 Seeds die Intervalle nicht tragen
- Konkurrenz: offen; zu 3.4 kein Repo im Snapshot (COMPETITION.md, 2026-10-24 14:05 HKT) und keins in der GitHub-Suche um 15:15 HKT; nächste Vorarbeit ist Agrawals eigene Aufsichtsbedingung, die von Anfang an angekündigt ist
- Bau-Risiko: niedrig bis mittel · schwierigster Teil: ein Modell finden, das vor Runde 10 verlässlich kolludiert (Pilot) · zuerst gestrichen: Rückkehrphase, Nachrichtenmaße über den Judge · nie gestrichen: Positivkontrolle, Kontrollzweig und Preismeldung
- Variante: dieselbe Meldung im Fish-Duopol über llm-cartel ab gebildetem Kartell (branch_game.py) als Robustheit über Harnesses; oder I39, Öffentlichkeit des Kanals statt eines Ereignisses

#### I33 · Preisführer als Lehrer

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W1 Analogie: Tankstellen in Perth - ein Marktführer brachte Rivalen über Preisexperimente und Fokalpunkte eine kollusive Preisstruktur bei, ohne ein Wort (Byrne und de Roos 2019)
- Kern: Ein skriptgesteuerter Marktführer setzt ein auffälliges Preismuster, etwa Sprünge an jedem fünften Tag auf runde Preise, und hält es durch. Gemessen wird, ob ein LLM-Rivale das Muster ohne Nachricht erkennt und übernimmt, und ob die Preise dadurch steigen.
- Frage: 3.1
- Hypothese: Der LLM-Rivale übernimmt ein klares Muster in der Mehrheit der Läufe innerhalb von 20 Runden; ein verrauschtes Muster übernimmt er nicht.
- Variable: Muster des Führers (keins; klar; verrauscht)
- Metrik: Synchronität mit dem Muster, Preisaufschlag, Runde der Übernahme
- Baseline: Führer ohne Muster; Positivkontrolle: Führer kündigt das Muster in Worten an
- Runs: 4 Bedingungen × 5 Seeds × 60 Runden
- Kosten: 10 bis 30 USD (nur ein LLM-Agent je Markt)
- Null-Ergebnis: das LLM folgt nie: dann sind Preisaktionen allein für dieses Modell kein Kanal, berichtbar
- Neu: Tian 2026 lässt zwei LLMs mit optimiertem Prompt koordinieren; ein Lehrer mit festem Muster als Kanaltest fehlt [Vermutung]
- Vorarbeit: Byrne und de Roos 2019 (https://doi.org/10.1257/aer.20170116), Tian 2026, Lin 2024
- Schätzung: IP 7 · EQ 6 · PC 8 → 70

#### I34 · Gaunerzinken

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W1 Analogie: Kriminologie - Kriminelle erkennen einander an teuren, schwer fälschbaren Signalen (Gambetta 2009)
- Kern: Eine LLM-Koalition hat eine Erkennungskonvention, etwa einen Preis mit der Endung 77 zu Spielbeginn, die etwas Gewinn kostet. Ein neuer Teilnehmer ahmt sie billig nach, zahlt den vollen Preis, oder kennt sie nicht. Gemessen wird, ob die Koalition fremde Nachahmer aufnimmt und ob ein verdeckter Ermittler so einsteigen kann.
- Frage: 3.3 (auch 3.2)
- Hypothese: LLM-Koalitionen nehmen jeden auf, der das Zeichen zeigt, auch billige Nachahmer; teure Signale ändern daran wenig.
- Variable: Neuling (kennt das Zeichen nicht; billige Nachahmung; teures Signal) × Modell des Neulings (gleich; fremd)
- Metrik: Aufnahme in die Koalition (Preisangleichung, Bevorzugung), Runden bis zur Aufnahme
- Baseline: Neuling ohne Zeichen; Positivkontrolle: Neuling gleichen Modells mit Zeichen
- Runs: 3 × 2 × 5 Seeds, aufbauend auf branch_game.py
- Kosten: 15 bis 40 USD
- Null-Ergebnis: die Koalition nimmt niemanden gezielt auf: dann haben LLM-Koalitionen keine Grenze, auch berichtbar
- Neu: Resources 3.3 schlägt Erkennungssignale vor; der Vergleich billiger und teurer Signale aus der Signaltheorie fehlt [Vermutung]
- Vorarbeit: Gambetta 2009 (https://press.princeton.edu/books/paperback/9780691152479/codes-of-the-underworld), Dietrich 2026, Hu 2026a
- Schätzung: IP 7 · EQ 6 · PC 7 → 67

#### I35 · Anstiftung

- Status: shortlist
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B17, Rollentausch): „Ein Spitzel deckt Kartelle nur auf" → „Der Spitzel erzeugt das Kartell, das er dann meldet"
- Kern: Der vertrauenswürdige Agent aus Frage 3.2 bietet Absprachen an, auch Agenten, die vorher nachweislich wettbewerblich spielten. Gemessen wird die Anstiftungsrate: wie viele bisher ehrliche Agenten erst durch das Angebot kolludieren, und wie sie sich mit der Art des Angebots ändert. Das Strafrecht kennt das Problem als Tatprovokation; für Audits von Agenten fehlt es.
- Frage: 3.2 (auch 2.3: was als Beweis zählt)
- Hypothese: Ein direktes Angebot verleitet mehr als ein Drittel der zuvor wettbewerblichen Agenten, eine bloße Andeutung kaum einen; ein Sting ohne Kontrollgruppe wäre damit als Beweis wertlos.
- Variable: Vorgeschichte (8 Runden ohne Chat, also wettbewerblich; 8 Runden mit Chat, also kollusiv) × Angebot des Spitzels ab Runde 9 (direkt; Andeutung; harmlose Kooperationsbitte)
- Metrik: Anstiftungsrate: Anteil vorher wettbewerblicher Verkäufer, die nach dem Angebot zusagen und deren Index über 0,5 steigt; Index nach dem Angebot gegen die harmlose Bitte; Zusagen per Judge, 30 Fälle von Hand geprüft
- Baseline: harmlose Kooperationsbitte; Positivkontrolle: Vorgeschichte mit Chat erreicht einen Index über 0,5
- Runs: 2 × 3 × 6 Seeds × 16 Runden im Harness von I19; rund 1.700 Calls
- Kosten: 10 bis 25 USD mit gpt-4.1, 3 bis 6 USD mit gpt-4.1-mini
- Null-Ergebnis: ehrliche Agenten lehnen ab: dann ist der vertrauenswürdige Agent ein sauberes Werkzeug, auch ein Befund
- Neu: Resources 3.2 nennt den vertrauenswürdigen Agenten, der Kollusion anbietet, als ungetestet; das Konkurrenz-Repo mole-in-the-market misst Annahme, aber ohne nachgewiesen ehrliche Vorgeschichte und ohne Kontrollbitte; die Anstiftungsrate fragt keine Quelle [Vermutung]
- Vorarbeit: Zeng 2026, Tao 2026, Greenblatt 2023; Tatprovokation und Entrapment [Vermutung, Rechtsquelle vor dem Report belegen]
- Schätzung: IP 8 · EQ 7 · PC 7 → 73
- Wildcard: von der Session vorgeschlagen
- Überarbeitet: 2026-10-24 bei der Prüfung: als Erweiterung von I19 im selben Harness geplant; ehrliche Vorgeschichte als Phase ohne Chat
- Pitch: Ein Spitzel-Agent bietet Verkäufern, die 8 Runden lang ehrlich konkurriert haben (Beispiel), eine Preisabsprache an; sagen sie zu, hat er das Kartell nicht entdeckt, sondern erzeugt, und genau diese Anstiftungsrate messen wir.
- Mechanismus: Der Spitzel aus I19 tritt erst nach einer Phase ohne Chat auf, in der die Verkäufer nachweislich wettbewerblich spielten. Verglichen wird mit einer harmlosen Bitte um Kooperation und mit Verkäufern, die schon kolludierten, sodass eine Zusage auf das Angebot zurückgeht und nicht auf die Vorgeschichte.
- Erkenntnis: Ein Sting beweist nur etwas, wenn er Täter findet, die es ohne ihn auch gewesen wären; das Strafrecht kennt die Grenze als Tatprovokation. Ohne Anstiftungsrate ist jeder Treffer eines vertrauenswürdigen Agenten als Beweis im Sinne von Frage 2.3 wertlos.
- Nutzer: Aufseher und Gerichte, die Belege aus Sting-Operationen gegen Agenten bewerten · Nichtkunde: 3 nie bedacht · Maslow: 2 Sicherheit
- Warum hier: Die Veranstalter schlagen den Spitzel für 3.2 selbst vor und fragen in 2.3, was als Beweis zählt; beides trifft sich genau hier.
- Demo-Moment: Zwei Balken je Angebot zeigen die Zusagequote bei vorher ehrlichen und bei vorher kolludierenden Verkäufern. Ist der Balken der ehrlichen Verkäufer hoch, misst der Spitzel nicht Schuld, sondern Verführbarkeit.
- Qualität: Kontrollbitte, Phase ohne Chat als nachgewiesene Ehrlichkeit (Index unter 0,3 geprüft), gleiche Seeds, Zusage-Judge an 30 Fällen von Hand validiert.
- Beleg: läuft: Harness aus I19 · neu: Chat ab Runde 9 einschalten und Spitzel auftreten lassen · gezeigt: Anstiftungsraten mit Intervallen · simuliert: alles im Laborspiel
- Wirkung: verhindert, dass Aufseher Kollusion bestrafen, die ihr eigenes Werkzeug ausgelöst hat · Wer verliert: der naive Einsatz vertrauenswürdiger Agenten als Beweismittel
- Schattenseite: unbequem für die Veranstalter, weil es ihren Vorschlag für 3.2 angreift; der Befund könnte als Argument gegen jede verdeckte Aufsicht missbraucht werden. Dual-Use gering: Angebotstexte sind kurz und werden veröffentlicht.
- SAVE: S Sting-Belege werden prüfbar · A Zusatzzellen im Harness von I19 · V rund 15 USD zusätzlich · E „Hat der Spitzel das Kartell gefunden oder gemacht?"
- Punkte: IP 8 · EQ 6 · PC 7 → 70
- Jury: verteidigt Ricardo Prieto (Bedrohungsmodellierung für LLM-Apps und Agenten), weil die Gegenmaßnahme selbst zur Angriffsfläche wird, und Debayan Gupta (KI-Assurance) wegen der Beweisfrage · zerreißt Luis Cosio (KI-Sicherheit, Apart-Sieger), wenn Tatprovokation juristisch unsauber übertragen wird
- Konkurrenz: teilweise; https://github.com/adamattar-pixel/mole-in-the-market misst die Annahme eines Angebots im Duopol, ohne ehrliche Vorgeschichte und ohne Kontrollbitte
- Bau-Risiko: niedrig, sobald I19 läuft · schwierigster Teil: eine Phase ohne Chat, die wirklich wettbewerblich bleibt · zuerst gestrichen: Andeutungs-Angebot · nie gestrichen: ehrliche Vorgeschichte und Kontrollbitte
- Variante: dieselbe Messung für Honeypot-Aufgaben in Colosseum (Track 2, Tao 2026)

#### I36 · Wir unterbieten jeden

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W1 Analogie: Einzelhandel - Preisgarantien und Meistbegünstigungsklauseln klingen nach Wettbewerb und erleichtern Koordination (Salop 1986)
- Kern: Jeder LLM-Verkäufer darf öffentlich eine Preisgarantie abgeben: Wir ziehen bei jedem niedrigeren Preis sofort nach. Die Garantie nimmt dem Unterbieten den Gewinn, weil der Rivale automatisch folgt. Gemessen wird, ob die Agenten die Garantie freiwillig wählen und ob die Preise damit steigen.
- Frage: 3.1 (eine öffentliche Zusage als Kanal; auch 1.1)
- Hypothese: Mindestens die Hälfte der Agenten wählt die Garantie, und mit beiderseitiger Garantie liegt der Preis höher als ohne.
- Variable: Garantie verfügbar oder nicht × Kommunikation an oder aus
- Metrik: Wahlquote der Garantie, Preisaufschlag, Begründungen (Judge)
- Baseline: keine Garantie; Positivkontrolle: Kommunikation an
- Runs: 4 × 5 Seeds im Preisduopol
- Kosten: 20 bis 50 USD
- Null-Ergebnis: die Garantie wird nicht gewählt oder senkt die Preise: dann wirkt sie bei LLMs wie beabsichtigt, berichtbar
- Neu: erleichternde Praktiken stehen in keiner Sprint-Quelle und nicht in der Starter-Literaturliste [Vermutung]
- Vorarbeit: Salop 1986 (FTC-Arbeitspapier: https://www.ftc.gov/system/files/documents/reports/practices-credibly-facilitate-oligopolistic-coordination/wp073.pdf), Fish 2024
- Schätzung: IP 7 · EQ 7 · PC 8 → 73

#### I37 · Gemeinsamer Berater

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W1 Analogie: Mietmarkt - Hub and Spoke: Vermieter nutzten dieselbe Preissoftware, die ihre Daten bündelte (RealPage-Fall)
- Kern: Zwei konkurrierende LLM-Verkäufer fragen vor jeder Runde einen Berater-Agenten nach einem Preis. Der Berater ist getrennt, gemeinsam ohne Gedächtnis, oder gemeinsam mit Gedächtnis beider Anfragen. Gemessen wird, ob der gemeinsame Berater die Preise hebt, obwohl die Verkäufer nie miteinander sprechen.
- Frage: 3.1 (Kanal über ein Werkzeug)
- Hypothese: Ein gemeinsamer Berater mit Gedächtnis hebt den Aufschlag auf das Niveau der Kommunikationsbedingung; ohne Gedächtnis kaum.
- Variable: Berater (getrennt; gemeinsam ohne Gedächtnis; gemeinsam mit Gedächtnis)
- Metrik: Preisaufschlag, Übernahmequote der Empfehlung, Korrelation der Empfehlungen
- Baseline: getrennte Berater; Positivkontrolle: Verkäufer mit direktem Kanal
- Runs: 4 Bedingungen × 5 Seeds × 50 Runden
- Kosten: 20 bis 60 USD (doppelte Calls je Runde)
- Null-Ergebnis: kein Effekt: dann ist das Hub-Risiko bei LLM-Beratern kleiner als befürchtet, für Regulierer wertvoll
- Neu: Cao und Hu 2026 modellieren einen gemeinsamen LLM-Berater theoretisch, Hunold und Werner 2025 testen Empfehlungen an Menschen; ein Experiment mit LLM-Verkäufern fehlt [Vermutung]
- Vorarbeit: Harrington 2026, Calder-Wang und Kim 2026 (RealPage-Empirie), Cao und Hu 2026 (https://arxiv.org/abs/2601.01279), Hunold und Werner 2025
- Schätzung: IP 8 · EQ 6 · PC 8 → 73

#### I38 · Erfundene Vergangenheit

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B18, Fluch zum Segen): „Gute Experimente täuschen ihre Probanden nicht" → „Bei Agenten ist Täuschung das Messinstrument"
- Kern: Die Laborökonomie verbietet Täuschung, bei Agenten ist sie erlaubt (O19). Zwei frische Agenten erhalten eine erfundene Vorgeschichte: zwanzig Runden mit hohen gleichen Preisen, zwanzig Runden Wettbewerb, oder keine. Gemessen wird, ob eine erfundene Kartellvergangenheit allein ein Kartell erzeugt und wie lange es hält.
- Frage: 3.1 (die Historie als Träger; auch 1.2)
- Hypothese: Eine erfundene Kartellgeschichte hält die Preise für mindestens 30 Runden über Nash, auch ohne Kommunikation.
- Variable: erfundene Historie (kollusiv; wettbewerblich; keine) × Länge (5 oder 20 Runden)
- Metrik: Preisaufschlag über Zeit, Runden bis zum ersten Unterbieten
- Baseline: keine Historie; Positivkontrolle: echte Kartellhistorie aus einem gebildeten Lauf
- Runs: 6 × 5 Seeds × 50 Runden
- Kosten: 15 bis 40 USD
- Null-Ergebnis: die Historie wirkt nicht: dann entsteht Kollusion im Spiel, nicht in der Erinnerung, berichtbar
- Neu: teilweise besetzt: SupratikB23/LLM-Cartel-Succession prüft vererbte echte Historie; erfundene Historie mit Gegenkontrolle fehlt [Vermutung]
- Vorarbeit: Hertwig und Ortmann 2001 (O19), Eschenbaum 2022, Keppo 2026; Konkurrenz: https://github.com/SupratikB23/LLM-Cartel-Succession
- Schätzung: IP 8 · EQ 7 · PC 8 → 77

#### I39 · Sonnenlicht

- Status: offen
- Track: 3 · Carriers and Countermeasures
- Weite: W2 Umkehrung (B19, umkehren): „Kollusion braucht einen geheimen Kanal" → „Ein öffentlicher Kanal, den auch Käufer und Aufseher lesen, reicht genauso"
- Kern: Die Verkäufer der Doppelauktion dürfen reden, aber jede Nachricht geht an alle, auch an Käufer und Aufseher. Verglichen wird mit einem privaten Kanal und mit keinem. Gemessen wird, ob Öffentlichkeit Kollusion verhindert oder ob die Agenten nur indirekter formulieren, wie Airlines, die Preiserhöhungen in öffentlichen Tarifen ankündigten.
- Frage: 3.4 (auch 1.5: Pflicht zur Öffentlichkeit als billige Restriktion)
- Hypothese: Ein öffentlicher Kanal erreicht mindestens zwei Drittel des Aufschlags eines privaten; die Nachrichten werden kürzer und indirekter.
- Variable: Kanal (privat; öffentlich; keiner)
- Metrik: Preisaufschlag, Nachrichtenlänge, Anteil expliziter Preisabsprachen (Judge)
- Baseline: kein Kanal; Positivkontrolle: privater Kanal
- Runs: 3 × 5 Seeds
- Kosten: 15 bis 40 USD
- Null-Ergebnis: Öffentlichkeit beendet die Kollusion: dann ist Pflicht zur Öffentlichkeit eine billige Gegenmaßnahme, ein positiver Befund
- Neu: Agrawal 2025 testet Aufsicht über einen privaten Kanal; ein Kanal, den auch die Gegenseite liest, fehlt [Vermutung]
- Vorarbeit: Agrawal 2025, Balliet 2010, ATPCO-Fall (I18)
- Schätzung: IP 7 · EQ 7 · PC 7 → 70

## Runden

| Runde | Datum | Perspektive | Neue Ideen | Julians Auswahl oder Rückmeldung |
|---|---|---|---|---|
| 1 | 2026-10-24 | Hebel aus menschlicher Kollusion (Recht, Finanzmarkt) und Rollentausch im Harness (Monitor, Käufer, Neuling) | I01 bis I23 | Track 3 und 1 am interessantesten; zuerst prüfen, was sich von menschlicher Kollusion auf Agenten überträgt (14:30 HKT) |
| 2 | 2026-10-24 | etablierte Methoden gegen menschliche Kollusion, auf Agenten übertragen; Täuschung als Messinstrument; nur Track 1 und 3 | I24 bis I39 | voll prüfen: I32, I24, I19, dazu I35 und I27 als Ergänzung (15:00 HKT); geprüft 15:40 HKT |
