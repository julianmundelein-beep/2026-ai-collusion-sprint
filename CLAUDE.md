# CLAUDE.md · AI Collusion Research Sprint (Session-Regeln, im Repo bis zum Abschluss)

Angelegt von hackathon-kickoff am 2026-10-24. Gilt für jede Claude-Session in diesem Repo: im Hauptordner, in Worktrees unter `.claude/worktrees/` und in Cloud-Sessions. Die Datei ist während des Baus committet, damit alle sie kennen, und verlässt beim Repo-Abschluss den Baum wie `hackathon/`.

Hauptordner (lokal): `/Users/julianmundelein/Projects/2026-ai-collusion-sprint`. In einer Cloud-Session gibt es ihn nicht; dein Checkout ist das Repo.

## Zuerst

1. `date` ausführen, dann `hackathon/STATUS.md` lesen (im Worktree und in der Cloud nach dem Holen des Stands, unten „Sessions“): Uhr, Sitzungsplan, Artefakte, nächster Schritt. Passt deine Aufgabe nicht mehr vor die interne Deadline, das sofort sagen.
2. Was du tust und welche Dateien du schreibst, steht in deinem Auftrag und in der Spalte „Writes“ des Sitzungsplans. Fehlt etwas: fragen, nicht raten.

## Dateien

- `hackathon/` liegt mit `private/` in jedem Checkout. In einem Worktree oder in der Cloud holst du vor jeder Aufgabe den neuesten Stand (unten, „Sessions“) und liest dann aus deinem Checkout. Dateien unter `hackathon/` schreiben nur die Sessions im Hauptordner. Worktree- und Cloud-Sessions schreiben dort nur Anhänge an DECISIONS und „Für die Skills“: lokal direkt im Hauptordner (`/Users/julianmundelein/Projects/2026-ai-collusion-sprint/hackathon/…`), damit die Hauptsession sie sofort sieht; in der Cloud im eigenen Checkout, committet im eigenen Zweig (beim Zusammenführen bleiben beide Seiten erhalten).
- Schreib nur deine eigenen Dateien. Für alle offen, nur zum Anhängen: `hackathon/DECISIONS.md` und der Abschnitt „Für die Skills“ am Ende von `hackathon/STATUS.md`.
- Committe nur deine eigenen Dateien, nach jedem fertigen Schritt, immer mit Pfaden: `git commit -m "…" -- <datei> …`. Neue Dateien vorher einzeln `git add <datei>`. Ein Commit ohne Pfade nähme Dateien mit, die eine andere Session im selben Ordner gerade gestaged hat. Nie `git add -A`, `git add .` oder `git commit -a`. Vor jedem Commit `git status` lesen. Meldet Git `index.lock`, arbeitet gerade eine andere Session mit Git: kurz warten und wiederholen, die Lock-Datei nie löschen.
- `STATUS.md` und `DECISIONS.md` committet die Hauptsession. `DESIGN.md` schreibt und committet nur die Design-Session; Änderungswünsche daran meldest du der Hauptsession.
- Während des Baus kommt alles in Git, auch `hackathon/private/` (Jury, Konkurrenz, Reviews, Deck- und Video-Quellen) und diese Datei; das Repo ist dabei privat. Draußen bleiben nur Secrets und große Medien (Video-Exporte, Deck-Renders in `out/`); `.git/info/exclude` hält sie fern. `main` pusht nur die Hauptsession, nach Julians OK. Eine Cloud-Session pusht nur ihren eigenen Zweig.
- Keine Secrets in Dateien, Commits oder Ausgaben (API-Keys, Private Keys, RPC-URLs mit Token): lokal `.env` plus `.env.example`; in der Cloud gibt es keine `.env`, dort kommen Keys als Umgebungsvariablen oder Netzwerk-Secrets der Cloud-Umgebung, die Julian einträgt.
- Keine KI-Spuren und keine Gedankenstriche: Commits und PRs ohne `Co-Authored-By`-, „Generated with“- oder `Claude-Session`-Zeile (`.claude/settings.json` schaltet sie ab, auch in der Cloud), Repo-Dateien ohne Gedankenstriche (Geviertstrich, Halbgeviertstrich mit Leerzeichen), keine weiteren Werkzeug-Notizen (`AGENTS.md` u. ä.) im Baum.
- Arbeitsnotizen (Ideen, Pläne, Recherche, Jury, Notizen) nur unter `hackathon/`, nie in der Repo-Wurzel; sie verlassen beim Abschluss den Baum, zusammen mit dieser Datei und `.claude/settings.json`. In der Historie bleiben sie; Julian will das so.

## Zahlen und Entscheidungen

- Zahlen und Faktenbehauptungen nur aus `hackathon/FACTS.md`. Eine neue Zahl (Messung, Quelle) meldest du der Hauptsession mit Wert, Quelle oder Befehl und Datum; sie trägt sie ein. Vorher verwendest du sie nicht.
- Vor jeder Änderung an einem Artefakt die `KEEP`-Zeilen in `hackathon/DECISIONS.md` lesen („bleibt so“). Neue Daten einarbeiten, frühere Festlegungen bleiben, bis Julian sie in einer neuen Zeile aufhebt.
- Trifft Julian eine Entscheidung, hängst du sie sofort als Zeile an `hackathon/DECISIONS.md` an (Ort wie oben unter „Dateien“).

## Sessions

- Eine Session pro Artefakt. Arbeitet laut STATUS schon eine andere Session oder ein Teammitglied an deinem Artefakt: aufhören und Julian fragen, welcher Stand gilt.
- Worktree-Sessions holen vor jeder neuen Aufgabe den Hauptstand: `git merge main` im Worktree. Cloud-Sessions: `git fetch origin main && git merge origin/main`. Konflikte lösen statt verwerfen; in `DECISIONS.md` und am Ende von `STATUS.md` beide Seiten behalten.
- Dein Abschlussbericht erreicht die Hauptsession nur mit den ersten 400 Zeichen. Also zuerst: was fertig ist, welche Dateien, was die Hauptsession tun muss (Zahlen für FACTS, Änderungswunsch an DESIGN.md, Zweig zusammenführen, Entscheidung festschreiben), was offen ist.
- Cloud-Sessions melden sich nicht von selbst bei der Hauptsession. Dein Stand muss deshalb im gepushten Zweig stehen: Code, Plan und Messungen committet, der Bericht als letzte Antwort für Julian.

## Skills

Skills werden während des Hackathons nicht umgebaut. Ein Skill-Problem (falsche Anleitung, fehlender Schritt, Skriptfehler) kommt nur als Zeile unter „Für die Skills“ ans Ende von `hackathon/STATUS.md` (Ort wie oben unter „Dateien“): `JJJJ-MM-TT · <session> · <skill> · <problem> · <vorschlag>`.

## Julian

- Deutsch, direkt, ohne Vorrede.
- Das Claude-Gedächtnis hängt am Ordner; das aus `~/claude-tools` gilt hier nicht. Julians Vorlieben stehen in den Skills (pitch-deck `references/praeferenzen.md`, video-studio `references/stil.md`), lokal in `~/studio/me/` und im Vault (`Weiterbildung/Kontext-*.md`).
- Sprache: Ideen (`IDEAS.md`), Design (`DESIGN.md`, `private/design/`), Pitch-Deck und Video entstehen deutsch und werden so committet und gepusht. Englisch muss erst der Abgabestand sein; übersetzt wird beim Repo-Abschluss, was dann im Baum bleibt. Code, README, `docs/` und die übrigen Vertragsdateien schreibst du gleich englisch.
- Nichts senden, einreichen, registrieren, deployen oder veröffentlichen ohne Julians ausdrückliches OK. Mails und Formulartexte schreibst du als Entwurf; persönliche Daten und Pässe gibt Julian selbst ein.
- Bei Formulierungen (Name, Slogan, Why-Satz) zwei bis drei Optionen mit Empfehlung, Julian wählt.

Prüfen vor jedem Push (lokal, Hauptsession): `python3 ~/.claude/skills/hackathon-kickoff/scripts/pruefen.py repo /Users/julianmundelein/Projects/2026-ai-collusion-sprint`
