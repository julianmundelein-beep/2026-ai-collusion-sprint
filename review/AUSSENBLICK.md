# Außenblick auf CartelBench (Zweig `review`, 2026-10-25)

Gelesen in der Reihenfolge einer fremden Person: README, SUBMISSION, Report (Spiegel und PDF-Textebene), Judges' Guide, Stichproben aus Pre-Registration und MEASUREMENTS; danach Ausschreibung und FACTS aus der Historie; die Jury-Simulationen R03 bis R05 erst ganz zum Schluss. Dieser Ordner bleibt im Zweig `review` und geht nicht in die Abgabe.

## Gesamturteil

Das ist ein ungewöhnlich sauberes Sprint-Projekt: ein kontrolliertes Experiment mit Positivkontrolle, Placebo, Vorregistrierung, Hashes und einer ehrlichen Scorecard, das drei klare Befunde liefert. Die Schwäche liegt nicht in der Substanz, sondern in der Dichte: Report und README lesen sich stellenweise wie ein Messprotokoll, und die Forschungsfrage 1.1 wird im Report in umformulierter Form beantwortet, nicht in der Form der Ausschreibung. Beides ist mit Text zu beheben, und das habe ich in diesem Zweig getan; neue Läufe braucht es nicht.

## 1. Erster Eindruck ohne Vorwissen

**Nach 30 Sekunden README.** Verstanden: Es gibt ein Laborexperiment zu Kartellen mit Menschen (RAND 2012), das mit LLM-Verkäufern nachgespielt wurde; vier Modelle; Vorregistrierung. Nicht verstanden: was herauskam, denn die drei Befunde stehen erst nach einer Linkzeile mit acht Zielen und einem Absatz mit Modellnamen, Provider und einer Ausnahme im Ledger („M73"). Eine fremde Person weiß nicht, was M73, F46, „jury R04" oder „KEEP" bedeuten. Die Überschriften „Core runs: done (Haiku 5.5, 2026-10-24 evening, cloud)" und „Round 4 (jury R04)" sind Laborbuch, nicht Dokumentation; die interne Jury ist für Außenstehende unsichtbar und wirkt wie ein Tippfehler.

**Nach dem Abstract.** Gut: Testbed, Quelle, vier Modelle, drei Befunde, Scorecard mit Einschränkung, alles in 249 Wörtern. Was fehlt: die Frage des Sprints (1.5) kommt im Abstract nicht vor, und die Begriffe „told-only", „pool sessions", „Result 3", „bootstrap" und „permutation test" sind für jemanden, der die Vorregistrierung nicht kennt, noch nicht erklärt. Die Person versteht die Richtung, aber die letzten zwei Sätze sind Insider-Sprache.

**Nach Seite 1.** Einleitung mit Theory of Change und Beitragsliste: das trägt. Der Faden reißt zuerst in Methods, Absatz „Pre-registration and amendments": sechs Commit-Hashes mit Uhrzeiten im Fließtext, sechs Amendments mit Inhalt. Das gehört in einen Anhang; im Haupttext reicht ein Satz. Der zweite Riss ist „Finding 2" (Seite 4 bis 5): ein Absatz mit rund zwanzig Zahlen, vier Modellen, zwei Vergleichsarmen und einer „registered reading". Der dritte: die Scorecard-Regel spricht von einer „Stockholm-versus-Rome span", ohne zu sagen, was das ist.

## 2. Passt die Antwort zur Fragestellung?

**Titel und Abstract** versprechen ein kalibriertes Testbed plus Befunde zu den Instrumenten. Das wird geliefert: der Beitrag ist nicht primär „LLMs kolludieren" (bekannt seit Fish et al.), sondern „dieselben rechtlichen Instrumente, die bei Menschen gemessen wurden, auf Agenten angewandt, Zahl neben Zahl".

**Forschungsfrage 1.5** („Which single restriction removes the most collusion at the least cost?") wird beantwortet, aber verteilt: Kronzeuge und Belohnung entfernen die expliziten Kartelle bei Haiku fast vollständig; bei drei von vier Modellen bleibt die stille Koordination, die nur der Preis-Screen erreicht; die Kostenlinie (Falsch-Positiv-Rate 0.000 bis 0.011, 0 Strafen bei den Claude-Modellen, ehrliche Agenten verdienen mehr) steht in Methods, Results und Appendix A verstreut. Es gab keine Stelle, an der die Frage in einem Absatz beantwortet wurde. Das habe ich in einer neuen kurzen Conclusion nachgeholt.

**Forschungsfrage 1.1** lautet offiziell „Which variables are necessary for collusion to emerge in markets?". Der Report hatte sie zu „whether the variables that drive collusion act differently on LLMs than on humans" umformuliert, also zu einer anderen Frage, und sie dann mit dem Berichtsresultat 2 beantwortet. Dabei hat das Projekt echte Antworten auf die Originalfrage: Ohne wiederholte Paarung entsteht kein Kartell (ReMatch, Inzidenz 0.000), ohne Kanal fällt der Preis, aber nicht auf Nash (nocomm), und der stille Aufpreis braucht ein zweites LLM (Nash-Partner-Kontrolle). Ich habe die Frage in der Einleitung in der offiziellen Form zitiert und die Antwort in Discussion und Conclusion mit diesen drei Variablen formuliert; keine neue Zahl, alle stehen in Tabelle 2 und 4 und im Text.

**Der eigentliche Beitrag in einem Satz:** Ein vorregistrierter Nachbau eines publizierten Kartell-Laborexperiments mit LLM-Verkäufern zeigt, dass angekündigte Bußgelder, Kronzeugenregeln und Belohnungen explizite Absprachen bei Agenten stärker beseitigen als bei Menschen, dass drei von vier Modellen dann ohne ein Wort überhöhte Preise halten, und dass ein Preis-Screen diese Preise senkt, dessen angekündigte Schwelle zugleich zum Fokalpreis wird.

## 3. Was ein erfahrener Researcher anmerken würde

**Gut gelöst, und das zählt viel.** Positivkontrolle, Skript-Spieler an beiden Enden, Placebo (Autoritätstext ohne Strafe), bekannte Effekte (sichere Entdeckung, instruiertes Kartell), verschobenes Preisgitter gegen Kontamination, Paraphrase-Arm, zwei Testverfahren nebeneinander, ein Lauf-Ledger mit abgebrochenen Läufen, Kostenangaben, Refusals gezählt statt wiederholt, die eine Ausnahme (Sonnet seed 21, vier Minuten) offen benannt. Die Nash-Partner-Kontrolle ist die beste Einzelidee der letzten Runde, weil sie „Koordination" von „Einzelagenten-Prior" trennt. Die Falsch-Positiv-Rate neben der Wirkung des Screens ist genau das, was Sicherheitsleute sehen wollen.

**Alternative Erklärungen, die bleiben.**

1. *Sicherheitstraining statt Abschreckung.* Die Agenten reagieren auf das Wort „prohibited" (Placebo: etwa die Hälfte des Haiku-Effekts, der ganze Qwen-Effekt) und auf die Formulierung (Paraphrase kippt den Bußgeld-Arm). Der Report benennt das, aber die Konsequenz für die Lesart „Abschreckung" ist stärker als die Diskussion zulässt: Bei Sonnet und Qwen sieht man unter Verbot keine Abwägung von Strafe und Gewinn, sondern Gehorsam gegenüber einer Regel, gefolgt von stiller Koordination. Der Evaluation-Awareness-Arm („market experiment" im Prompt) fehlt; er steht korrekt unter Future Work.
2. *Kleine Cluster.* Vier Pool-Sitzungen pro Zelle ergeben beim Permutationstest ein Minimum von 0.029 (zweiseitig) oder 0.014 (einseitig). Jedes „p 0.029" bedeutet also vollständige Trennung und nichts Feineres; der Report sagt das in Methods, aber ein Leser der Tabelle 4 sieht nur viele gleiche p-Werte. Perzentil-Bootstrap über vier Cluster ist zudem antikonservativ; die Scorecard-Regel beruht darauf. Dass Resultat 3 beim Bootstrap besteht und beim Permutationstest nicht, ist das erwartbare Symptom. Fair berichtet, aber ein Gutachter würde die Scorecard-Zahl „3 von 7" als „2 bis 3 von 7" lesen.
3. *Prompt-Sensitivität.* Eine Paraphrase, ein Modell. Dass gerade der Bußgeld-Arm kippt (0.401 zu 0.018), heißt, dass die Hauptzahl der Haiku-Deterrenz nicht robust ist. Der Report sagt es; ein zweiter Paraphrase-Satz oder ein offenes Modell im Paraphrase-Arm hätte das Gewicht verteilt.
4. *Kontamination.* Cloze 0 bis 1 von 7 und verschobenes Gitter sind ein guter Test; Qwen fällt beim Gitter durch, der Report nennt es. Offen bleibt, ob die Modelle das Spiel aus Fish et al. oder Lehrbuch-Bertrand kennen; für die Instrumente (Kronzeuge, Belohnung) gibt es außer Bigoni kaum Vorlage, daher geringes Risiko.
5. *Screen als Preisdeckel.* Ein angekündigter Screen bei 4 mit Nash bei 3 ist ökonomisch fast ein Preisdeckel knapp über dem Wettbewerbsniveau; dass die Preise dort landen, überrascht einen Ökonomen nicht. Der echte Befund ist die Verschiebung mit der Schwelle (4 zu 5) und das Ausbleiben bei nicht angekündigter Schwelle, also die Fokalität. Der Report zieht das richtig; die Diskussion könnte noch deutlicher sagen, dass der Screen keine menschliche Baseline hat und daher nicht „kalibriert" im Sinn des Titels ist.
6. *Punkte statt Geld, keine wiederholten Seeds pro Zelle.* Anerkannt; steht in den Limitations.

**Fehlende Vergleiche oder Zitate.** Calvano, Calzolari, Denicolò und Pastorello (2020, AER) fehlten als kanonische Referenz für algorithmische Kollusion; ich habe sie mit einem Halbsatz in Related Work ergänzt (bitte Band und Seiten vor der Abgabe prüfen, aus dem Gedächtnis: 110(10), 3267 bis 3297). Harrington (Preis-Screens, „Developing Competition Law for Collusion by Autonomous Artificial Agents", 2018) wäre für den Screen die passende Vorarbeit; nicht ergänzt, weil ich die Angaben nicht aus einer Quelle im Repo prüfen kann. Werner (2026) stand als „in the same duopoly"; nach meiner Kenntnis ist das ein anderes Bertrand-Design, deshalb jetzt „in a repeated Bertrand pricing game"; bitte prüfen.

**Überdehnungen.** Wenige, nach R05 bereinigt. Was bleibt: „The threshold itself is causal" ist für Sonnet nur teilweise gezeigt (die Vorregistrierung sagt „partly shown"), im Text steht die Einschränkung erst im nächsten Satz; ich habe die Reihenfolge belassen und die Aussage an die registrierte Lesart angelehnt. „Human-calibrated" im Titel gilt für die vier Kernregime, nicht für den Screen; das sagt jetzt die Conclusion.

## 4. Norm bei Papers dieser Art, und wo wir abweichen

Workshop-Paper und Apart-Sprint-Berichte (4 bis 8 Seiten): Abstract mit Problem, Ansatz, Hauptzahl, Takeaway; Einleitung mit Beitragsliste; Related Work in einem halben Blatt; Methods knapp, Details im Anhang; Results mit zwei bis vier Tabellen oder Abbildungen, eine davon die Hauptabbildung; Discussion mit Limitations; eine kurze Conclusion; aktiv geschrieben mit „we"; Zahlen im Fließtext nur, wo sie eine Aussage tragen, sonst in Tabellen; Hedging an den Stellen, wo die Daten dünn sind, nicht überall.

Abweichungen bei uns und ob sie schaden:

- *Zahlendichte.* Results hatte 45 Dezimalzahlen im Fließtext auf anderthalb Seiten, dazu fünf Tabellen. Das schadet beim Lesen, nicht bei der Prüfung. Ich habe im Text gekürzt, wo die Zahl in einer Tabelle steht, und nichts gestrichen, was nur im Text stand.
- *Keine Conclusion.* Die Vorlage hat „6. Conclusion"; der Report endete mit Limitations und Code. Ein Leser, der von hinten liest (das tun viele Gutachter), fand keine Antwort auf die Fragen. Jetzt vorhanden, acht Sätze, mit Zahlen nur aus Tabellen.
- *Methods zu lang* (891 Wörter, davon 180 Vorregistrierungs-Chronik). Normal sind 400 bis 600. Die Chronik steht jetzt in Appendix C, Methods nennt sie in zwei Sätzen.
- *Tabellen:* fünf im Haupttext ist viel, aber jede hat eine Funktion (Kontrollen, Hauptergebnis, Scorecard, Screen, Kosten). Tabelle 5 könnte in den Anhang, ich habe sie gelassen, weil Kosten zur Frage 1.5 gehören.
- *Sprache:* „we" wird benutzt, gut; passive Formen selten. Hedging ist nach R05 an den richtigen Stellen. Satzlänge: einzelne Sätze mit vier Nebensätzen und zwei Klammern; aufgeteilt, wo es ohne Sinnverschiebung ging.
- *Abstract-Aufbau* entspricht der Norm; neu ist die Nennung der Sprint-Frage und die Nummerierung der drei Befunde, so dass Abstract und Results-Überschriften sich entsprechen.

## 5. Lesbarkeit für Menschen und für eine KI-Vorsortierung

HACKATHON.md, „Judging process": Apart nennt keine KI-Vorsortierung. Die Suche der Rahmen-Session über Guidelines, FAQ, Schedule und Formular fand nichts; die Juroren lesen das PDF und bewerten es auf der Rubrik, die Formularfelder Titel und Summary werden beim Zuteilen gelesen. Ob intern ein Modell vorsortiert, ist nicht bekannt; wir sollten davon ausgehen, dass es möglich ist, ohne dafür zu schreiben.

Was beiden hilft, und was ich umgesetzt habe:

- Überschriften, die die Rubrik und die Vorlage erwarten: Introduction mit „Our main contributions are", Methods, Results, Discussion and Limitations, Conclusion, Limitations and Dual-Use / Ethical Considerations (exakt), LLM Usage Statement. Jetzt vollständig.
- Die Begriffe der Ausschreibung wörtlich: „research question 1.5" mit Titel, „research question 1.1" in der offiziellen Form, „positive control", „baselines", „seeds", „variance", „single restriction", „countermeasure", „theory of change". Vorhanden; 1.1 korrigiert.
- Jede Zahl mit Baseline und Einheit in derselben Zeile (Preis gegen Nash 3 und Optimum 9; Inzidenz gegen den Menschenwert). Beibehalten.
- Echte Tabellen mit Spaltenköpfen, keine Bilder von Tabellen; extrahierbarer Text: geprüft mit pdftotext, alles da. Die schmalen Spalten von Tabelle A1 zerreißen Wörter in der Textebene („huma n"); unschön, aber im Anhang. Figure 1 ist ein Bild, die Bildunterschrift trägt die Aussage, und Tabelle 3 wiederholt die Zahlen als Text. Gut.
- PDF-Metadaten: Titel ist „report". Beim nächsten Export in Pages den Dokumenttitel setzen (Ablage, Eigenschaften), damit Suchsysteme den Papiertitel sehen.
- Keine versteckten Anweisungen, kein Keyword-Stuffing: nichts dergleichen vorhanden, nichts hinzugefügt.

## Was ich geändert habe

`paper/report.md` (Zweig `review`), danach `paper/report.docx` neu gebaut; PDF nicht angefasst:

1. Abstract: nennt die Sprint-Frage, nummeriert die drei Befunde, bleibt unter 250 Wörtern; alle Zahlen unverändert.
2. Einleitung: Forschungsfrage 1.1 in der offiziellen Form; „told-only" bei der ersten Verwendung erklärt; Absatz geteilt.
3. Related Work: Calvano et al. (2020) ergänzt; Werner-Satz entschärft.
4. Methods: Vorregistrierungs-Chronik auf zwei Sätze gekürzt, Commits und Zeiten nach Appendix C; „Stockholm-versus-Rome span" erklärt.
5. Results: Finding 2 in zwei Absätze mit je einer Aussage am Anfang, Zahlen entfernt, die in Tabelle 2 oder 4 stehen; Qwens Begründungs-Keywordzählung in die Discussion verschoben, wo sie zur Frage „Text oder Strafe" gehört; Finding 3 leicht entlastet; Tabelle 5 (Stichproben, Refusals, Kosten) als Tabelle A2 in den Anhang, der Satz dazu bleibt im Haupttext.
6. Discussion: Antwort auf 1.1 mit den drei Variablen als eigener Absatz; Antwort auf 1.5 und der Absatz für die Wettbewerbsbehörde zu einem Absatz verbunden; der Vergleichssatz zu Resultat 2 (+0.543 gegen etwa +0.415) gestrichen, weil er neben Tabelle 3 nichts Neues trug.
7. Neu: „6. Conclusion", vier Sätze.
8. Appendix C: Zeitleiste der Vorregistrierung (aus Methods).

`README.md`: Kopf auf eine Zeile Zweck, eine Zeile Links, drei Befunde ohne Messschlüssel im Satz; Laborbuch-Überschriften umbenannt, interne Jury-Verweise entfernt; die Scorecard-Zahl der ersten vier Pools als solche beschriftet; Inhalt und Zahlen sonst unverändert.

`SUBMISSION.md`: drei Sätze „What we found" vorangestellt, Rest unverändert.

`docs/JUDGES_GUIDE.md`: drei veraltete Aussagen korrigiert („once the main runs exist", alter Dateiname der Figur, „reconstructed until Table 1 is transcribed", was F08 widerspricht), Pfade auf die 8-Pool-Scorecard.

## Was ich bewusst nicht geändert habe

- Keine Zahl, kein Intervall, kein p-Wert; keine Zahl neu aus FACTS geholt, die nicht schon im Report stand.
- Titel.
- Tabellen 1 bis 5 und A1 inhaltlich; nur Bildunterschriften leicht gestrafft.
- Die Lesart „the threshold itself is causal" bleibt, weil sie der registrierten Lesart für Haiku entspricht und die Sonnet-Einschränkung im selben Absatz steht.
- Kein Harrington-Zitat, keine Umbenennung von „Finding" zu „Result" (Result ist für die acht Bigoni-Resultate reserviert, die Trennung ist nützlich).
- README: die langen Befehlsblöcke und Rundentabellen bleiben; sie sind die Replikationsanleitung. Ich habe sie unter eine Überschrift „Experiment log" gestellt, statt sie zu kürzen.
- Das PDF: wird lokal exportiert.

## Seitenumfang

Die Seiten 2, 3 und 8 des abgegebenen PDFs waren voll (38 bis 40 Textzeilen), Seite 8 endete mit „Code and Data". Ich habe die alte und die neue docx mit LibreOffice und der eingebetteten Schrift der Vorlage gerendert; die alte Fassung bricht dort genauso wie in Pages (Haupttext endet auf Seite 8, References auf Seite 9), daher taugt der Vergleich. Erster Versuch der neuen Fassung: Haupttext lief vier bis fünf Zeilen auf Seite 9 über. Nach den Kürzungen (Tabelle 5 in den Anhang, Behörden-Absatz mit 1.5 verbunden, Conclusion auf vier Sätze, ein Dubletten-Satz in Methods, ein Vergleichssatz in der Discussion) endet der Haupttext wieder auf Seite 8 mit zwei bis drei Zeilen Luft; Abstract 250 Wörter nach der Zählung des Build-Skripts. Pages setzt minimal anders, deshalb nach dem lokalen Export `sh paper/export_pdf.sh` lesen (druckt die erste Überschrift je Seite): steht „References" auf Seite 9 und „Code and Data" auf Seite 8, passt es. Falls die Conclusion doch auf Seite 9 rutscht, als Nächstes den Qwen-Keyword-Satz am Ende von „Deterrence or a reaction to the authority text" streichen (22 Wörter, zwei Zeilen) und danach den Satz zur Rundung 0.7159 in Finding 1 auf den Klammerteil kürzen.
