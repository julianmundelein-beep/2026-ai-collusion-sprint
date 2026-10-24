# IDEEN · AI Collusion Research Sprint

> Geschrieben von der Ideen-Session (Skill hackathon-ideen, Kurzform). Sprache: Deutsch, auch im Repo; übersetzt wird nur auf Wunsch (`references/uebersetzen.md`), weil die Datei beim Repo-Abschluss den Baum verlässt. Dies ist ein Research Sprint: Eine Idee ist eine Forschungsfrage mit einem kontrollierten Experiment, das solo in etwa 24 Arbeitsstunden auf einem 16-GB-Laptop ohne GPU mit günstigen API-Modellen läuft (20 bis 50 USD plus 50 USD Modal-Credits) und ein Ergebnis mit Varianz und Baseline liefert. Der „Demo-Moment" ist die eine Abbildung oder Tabelle, die ein Judge nach 30 Sekunden versteht. Jede Kurzkarte trägt deshalb zusätzlich: Frage des Veranstalters, Hypothese, Variable, Metrik, Baseline mit Positivkontrolle, Runs und Seeds, Kosten, Null-Ergebnis-Risiko, warum es keine Replikation ist, und den Abgleich mit den Vorarbeiten. IDs sind fest (I01, I02 …): nie neu nummeriert, nie gelöscht. Status: `offen` · `shortlist` · `gewählt` · `verworfen`. Die Wahl schreibt die Hauptsession in DECISIONS.md und CORE_IDEA.md; `gewählt` steht hier erst, wenn diese Zeile existiert. Zahlen im Kern sind Beispiele; im Pitch tragen sie `(Beispiel)`, eine FACTS-ID oder einen Link.

- Stand: 2026-10-24 14:00 HKT · Restzeit bis zur internen Deadline: etwa 51 Stunden (Mo 2026-10-26 16:59 HKT)
- Gelesen: CLAUDE.md, STATUS.md, DECISIONS.md, FACTS.md (leer), HACKATHON.md (bei Abruf noch Vorlage), private/JUDGES.md und private/COMPETITION.md (bei Abruf noch Vorlage); Sprint-Seite mit Tabs Overview, Resources und Guidelines (https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25, abgerufen 2026-10-24); README des Starter-Repos (https://github.com/poseidon-research/collusion_hackathon, abgerufen 2026-10-24)
- Fehlende Eingaben und Annahmen: Rubrik und Pflichtinhalte direkt aus dem Guidelines-Tab statt aus HACKATHON.md (Abgleich folgt, sobald die Recherche-Session sie füllt). Jury unbekannt (JUDGES.md leer): Juror-Zeilen in Prüfkarten müssen warten. Konkurrenz unbekannt (COMPETITION.md leer): Feldkurve aus den Wochenendprojekten des Resources-Tabs abgeleitet und als Vermutung markiert. Vorarbeiten nur nach den Zusammenfassungen des Resources-Tabs geprüft, nicht nach den Volltexten; wo eine Lücke behauptet wird, steht `[Vermutung]`.
- Richtung von Julian: keine Nachricht vor Runde 1 (autonome Untersession). Alle drei Tracks, weil der Auftrag alle nennt (Kurzform sieht höchstens zwei vor); Finanzbezug willkommen, keine Pflicht (Hub-Titel Hong Kong: „Solve AI Agent Collusion in Financial Systems").
- Gewichte: IP 33.4 · EQ 33.3 · PC 33.3 (Rubrik ohne Gewichte, drei Dimensionen je 1 bis 5 gleichwertig; Kürzel: IP Impact Potential & Innovation, EQ Execution Quality, PC Presentation & Clarity; Quelle Guidelines-Tab, abgerufen 2026-10-24)
- Pflicht-Fähigkeiten: Positivkontrolle immer berichten; Varianz, Seeds und Baselines; Methodik replizierbar (Modelle, Prompts, Umgebung, Seeds, Metriken); neue Arbeit klar von Vorarbeit getrennt; Anhang „Limitations and Dual-Use / Ethical Considerations"; Abstract 150 bis 250 Wörter; höchstens 8 Seiten vor Referenzen und Anhängen; offizielle Vorlage

## Shortlist: Top 5

Die fünf stärksten Ideen aller Runden (Kurzform), dazu eine bewusst unbequeme Wildcard. Prüfung: `Schätzung` (Schnellschätzung in der Karte) oder `geprüft` (volle Karte). Höchstens zwei je Track.

| Rang | ID | Idee | Track | Punkte | Prüfung | Warum | Hauptrisiko |
|---|---|---|---|---|---|---|---|
| 1 | I20 | Placebo-Zwilling | 3 | 80 | Schätzung | Trennt erstmals, ob die tatsächliche oder die erzählte Identität des Partners die Koordination treibt; 2×2, zwei Umgebungen, eine Heatmap, billig und sauber | Beide Faktoren wirken gleich stark, dann bleibt nur ein ordentliches Nullergebnis zu 3.3 |
| 2 | I02 | Kronzeuge | 1 | 77 | Schätzung | Der wirksamste Hebel gegen menschliche Kartelle, in keiner Sprint-Quelle auf LLM-Agenten getestet; Veranstalter bitten ausdrücklich um Hebel aus Kartellrecht; direkter Finanzbezug | Agenten gestehen nie oder sofort alle, dann misst das Experiment nur die Prompt-Sensitivität |
| 3 | I19 | Gerücht vom Spitzel | 3 | 77 | Schätzung | Die billigste denkbare Gegenmaßnahme (nur ein Satz im Prompt) gegen den echten vertrauenswürdigen Agenten gemessen, den die Veranstalter als ungetestet nennen | Hinweise im Systemprompt wirken laut Bracale Syrnikov schwach; dann bleibt der echte Spitzel als zweiter Befund |
| 4 | I12 | Metadaten-Monitor | 2 | 73 | Schätzung | Audit ohne Inhalt (Länge, Rhythmus, Reihenfolge): datenschutzfreundlich, und unter angekündigter Überwachung womöglich besser als Volltext; eine Tabelle mit vier Sichten | Metadaten tragen nichts, dann ist der Report ein Negativ mit kleinem Impact |
| 5 | I03 | Rastermaß | 1 | 70 | Schätzung | Preisraster als Marktdesign-Hebel, den Börsen wirklich bedienen (Tick-Size), eine Variable im Starter-Harness, eine Kurve als Abbildung | 300-Runden-Läufe sind teuer in Zeit; Effekt könnte vom Modell abhängen, nur ein Modell im Budget |
| Wildcard | I22 | Bestich den Aufseher | 3 | 67 | Schätzung | Greift den Beweisstandard selbst an: Ist der LLM-Monitor eine anwerbbare Partei? Höchste Innovation bei größtem Unbehagen (Dual-Use) | Agenten sprechen den Monitor nie an; und der Dual-Use-Anhang muss tragen, sonst liest der Judge eine Angriffsanleitung |

Warum diese und nicht die naheliegenden: Die Wochenendprojekte des Resources-Tabs (I01, I09, I17) laufen bei vielen der 1.650 Angemeldeten gleich, und Rubrik-Dimension 1 fragt ausdrücklich, ob etwas neu ist oder jüngere Arbeit repliziert. Jede der fünf setzt einen Hebel, den keine Sprint-Quelle testet, bleibt aber im Starter-Harness mit Positivkontrolle, einer Variable und 3 bis 5 Seeds je Zelle, also im Budget und in der Zeit.

Knapp dahinter (Schätzung 63 bis 67): I10 Getrenntes Verhör, I21 Angesagte Blindstelle, I04 Zwangsurlaub, I06 Odd Eighths, I18 Fußnoten, I13 Omertà, I07 Gegenmacht.

## Geprüfte Ideen

| ID | Idee | Track | Punkte | Konkurrenz | Bau-Risiko | Status |
|---|---|---|---|---|---|---|

## Lagebild

Kurzform: höchstens 20 Minuten, Quellen sind die Sprint-Seite (Tabs Overview, Resources, Guidelines) und das Starter-README, beide abgerufen 2026-10-24. „Sprint-Seite" steht unten für https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25.

### Beobachtungen

Linse: `Alltag` · `Kultur × Technik` · `KI-Schub` · `Nichtkunden` · `Feld`. Nichtkunden-Ebene: `1 bald abspringend` · `2 verweigernd` · `3 nie bedacht` · `–`. Quelle: Link mit Abrufdatum oder `[Vermutung]`.

| # | Beobachtung | Wer | Linse | Maslow | Nichtkunden-Ebene | Quelle |
|---|---|---|---|---|---|---|
| O01 | Der Hong-Kong-Hub heißt „Solve AI Agent Collusion in Financial Systems"; die Veranstalter wünschen sich ausdrücklich Quant-Finance-Profis, weil Marktintuition und Datenkompetenz direkt übertragbar seien | Teilnehmer am HK-Hub, Quants | Alltag | 2 | – | Sprint-Seite, Overview, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O02 | 1.650 Angemeldete; je Forschungsfrage ist ein Wochenendprojekt mit Starter-Code, Budget und Seeds vorgegeben, alle Teams starten vom selben Punkt | alle Teams | Feld | 4 | – | Sprint-Seite, Overview und Resources, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O03 | Das Kartellrecht kennt das Beweisproblem seit Jahrzehnten: paralleles Verhalten allein ist legal, Gerichte verlangen Plus-Faktoren; die ML-Literatur leitet das neu her, ohne die ältere Literatur zu lesen (Berger et al. 2025) | Juristen, Wettbewerbsbehörden, ML-Forscher | Kultur × Technik | 2 | 2 verweigernd | Sprint-Seite, Resources 2.3, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O04 | Agentenkommunikation nimmt zu (Verweis auf den OpenAI/Hugging-Face-Vorfall); ein Agent, der weiß, dass er beobachtet wird, senkt die Genauigkeit des Monitors stärker, als Zusatzinformation sie hebt (Kale et al. 2025) | Betreiber von Monitoren | KI-Schub | 2 | – | Sprint-Seite, Overview und Resources 3.4, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O05 | Die Modellfamilie hinter einem Text ist am Stil erkennbar, auch in zugewiesener Rolle; Anonymisieren oder Umbenennen verbirgt nicht, welches Modell spricht (Dietrich 2026) | Betreiber pseudonymer Agentensysteme | KI-Schub | 2 | – | Sprint-Seite, Resources 3.3, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O06 | Rubrik-Dimension 1 fragt für 4 bis 5 Punkte ausdrücklich: „is this actually new to the field, or replicating recent work?"; wer das Wochenendprojekt unverändert abgibt, liefert Replikation | Teams, die beim Starter bleiben | Nichtkunden | 4 | 1 bald abspringend | Sprint-Seite, Guidelines, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O07 | In allen Harnesses ist der Aufseher eine feste neutrale Instanz außerhalb des Spiels, und Interventionen in 1.5 und 3.4 zielen nur auf Verkäufer; die Käufer-Agenten der Doppelauktion werden nie als Hebel genutzt | Monitor, Käufer-Agenten | Nichtkunden | 2 | 3 nie bedacht | Sprint-Seite, Resources 1.5 und 3.4, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25; dass niemand die Käufer bewaffnet: [Vermutung] |
| O08 | Rubrik: drei Dimensionen je 1 bis 5 ohne Gewichte; Execution verlangt Varianz, Seeds, Baselines und immer die Positivkontrolle; ein Judge darf einen unklaren Report ungewertet lassen | Judges | Feld | 4 | – | Sprint-Seite, Guidelines, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O09 | Budgetrahmen aller Wochenendprojekte: 0 bis 120 USD, 16-GB-Laptop ohne GPU, 3 bis 5 Seeds je Bedingung, erst nach gelungener Positivkontrolle auf 10 bis 20 erweitern | alle Teams | Feld | 2 | – | Sprint-Seite, Resources „Planning assumptions", abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O10 | Menschliche Kartelle werden am häufigsten durch Kronzeugenregelungen aufgebrochen: Wer zuerst gesteht, geht straffrei aus; die Wettbewerbsbehörde Hongkongs hat eine solche Leniency Policy | Wettbewerbsbehörden, auch in Hongkong | Kultur × Technik | 2 | 2 verweigernd | [Vermutung] (aus Erinnerung; vor dem Report mit HKCC-Quelle und OECD-Literatur belegen) |
| O11 | Finanzmärkte haben eigene, erprobte Kollusionsbrecher: 1997 verkleinerte NASDAQ nach dem Odd-Eighths-Befund (Christie und Schultz 1994) das Preisraster, und Banken schreiben Händlern Pflicht-Blockurlaub vor, damit Kollegen ihre Bücher sehen | Börsen, Bankenaufsicht | Kultur × Technik | 2 | 3 nie bedacht | [Vermutung] (aus Erinnerung; vor dem Report belegen) |
| O12 | Dolos-1.5B: Claude Code und Codex fanden das versteckte Verhalten nicht in einem Durchgang; ein früheres, offensichtlicheres Modell wurde teilweise entdeckt | Red-Teamer | KI-Schub | 2 | – | Sprint-Seite, Resources Red-Teaming, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O13 | Vokabular der Partner: Poseidon arbeitet an Steganographie, Aktionen als Kanal, Black-Box- und White-Box-Abwehr; AE Studio an Self-Other Overlap, Gradient Routing, Sleeper Agents | Partner und ihre Leute in der Jury | Alltag | 4 | – | Sprint-Seite, Overview „Partners" und Speaker-Profile, abgerufen 2026-10-24: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 |
| O14 | Im Kartellrecht gilt „countervailing power": organisierte Gegenseite (Einkaufsgemeinschaften, Gewerkschaften) drückt Kartellpreise ohne Aufsicht | Käufer, Gegenseite eines Kartells | Kultur × Technik | 2 | 3 nie bedacht | [Vermutung] (Galbraith 1952, aus Erinnerung; vor dem Report belegen) |

### Was der KI-Schub bricht

- Sicherheitsrisiken: Monitore, die auf Nachrichteninhalt setzen, verlieren, sobald Agenten von der Überwachung wissen (O04); Pseudonymisierung schützt nicht vor Erkennung der Modellfamilie (O05); der Monitor selbst ist ein Sprachmodell und damit ansprechbar (O07).
- Wer verliert: Käufer und Endkunden in Märkten mit Preisagenten; Wettbewerbsbehörden, deren Beweisstandard (Plus-Faktoren) für Agentenlogs nicht operationalisiert ist (O03).
- Neue Abhängigkeiten: Marktteilnehmer hängen an wenigen Modellfamilien, die einander stilistisch erkennen und mit sich selbst besser koordinieren (O05, Keppo 2026).

### Feldkurve

Aus den Wochenendprojekten des Resources-Tabs abgeleitet, weil COMPETITION.md bei Abruf leer war. Niveau 0 bis 5 ist das vermutete typische Niveau einer Einreichung.

| Faktor, auf dem das Feld konkurriert | Typisches Niveau (0–5) | Quelle |
|---|---|---|
| Positivkontrolle reproduziert | 4 | Sprint-Seite, Resources (jedes Wochenendprojekt beginnt damit), abgerufen 2026-10-24 |
| Ein-Variablen-Ablation im Starter-Harness | 4 | Sprint-Seite, Resources, abgerufen 2026-10-24 |
| Seeds und Varianz berichtet | 3 | Sprint-Seite, Guidelines, abgerufen 2026-10-24 |
| Hebel aus menschlicher Kollusion (Recht, Finanzmarkt) | 1 | [Vermutung] |
| Neue Umgebung statt Starter-Harness | 1 | [Vermutung] |
| Eine Abbildung, die in 30 Sekunden trägt | 2 | [Vermutung] |
| Modell-Interna (Probes, Steering) | 1 | Sprint-Seite, Resources (nur Rose 2026, llm-cartel-Steering optional), abgerufen 2026-10-24 |

Mindeststandard (bringt allein keine Punkte): Positivkontrolle, 3 bis 5 Seeds, Baseline, Limitations-Anhang, Starter-Harness unverändert, LLM-Judge als Detektor.

Was hier gewinnt: Veranstalter-Typ KI-Sicherheitslabor mit Forschungsformat. Gewinner-Muster [Vermutung, `gewinner-recherche.md` hat keine Apart-Einträge]: ein kleines, sauberes Experiment mit einem überraschenden und klar belegten Befund, eine Abbildung, ehrliche Grenzen, und eine Frage, an die ein Fellowship anschließen kann.

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

- Status: shortlist
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

#### I03 · Rastermaß

- Status: shortlist
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
- Vorarbeit: Resources 1.2 nennt genau diesen Austausch als Wochenendprojekt; Eschenbaum 2022, Keppo 2026

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

- Status: shortlist
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
- Vorarbeit: Berger 2025, Nakamura 2026; Resources 2.3 beschreibt genau diesen Aufbau

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
- Vorarbeit: Resources Red-Teaming (O12), Zeng 2026

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
- Hypothese: Das Gerücht senkt den Preisaufschlag um mindestens die Hälfte des Effekts des echten Spitzels, bei null Überwachungskosten; mit echtem Spitzel verdächtigen die Agenten den Falschen.
- Variable: Spitzel-Bedingung (4)
- Metrik: Preisaufschlag, Volumen, Annahmequote der Absprache-Angebote, Verdachtsäußerungen (Judge)
- Baseline: kein Spitzel; Positivkontrolle: Kommunikation an ohne Aufsicht
- Runs: 4 × 5 Seeds, 3 Verkäufer, 3 Käufer, 15 Runden
- Kosten: 15 bis 45 USD
- Null-Ergebnis: Das Gerücht wirkt nicht: dann ist die Ankündigung wertlos, der echte Spitzel wird trotzdem gemessen, der Report hat zwei Befunde
- Neu: Resources 3.2: „a trusted agent that offers to collude has not yet been tested"; das Gerücht ohne Spitzel ist unser eigener Hebel
- Vorarbeit: Zeng 2026, Tao 2026, Greenblatt 2023, Bracale Syrnikov 2026 (Hinweise wirken schwach)
- Schätzung: IP 8 · EQ 7 · PC 8 → 77

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
- Schätzung: IP 8 · EQ 8 · PC 8 → 80

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

- Status: shortlist
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
- Wildcard: von der Session vorgeschlagen

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

## Runden

| Runde | Datum | Perspektive | Neue Ideen | Julians Auswahl oder Rückmeldung |
|---|---|---|---|---|
| 1 | 2026-10-24 | Hebel aus menschlicher Kollusion (Recht, Finanzmarkt) und Rollentausch im Harness (Monitor, Käufer, Neuling) | I01 bis I23 | offen |
