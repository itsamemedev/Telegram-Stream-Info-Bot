# AGENTS.md — NIGHTCRAWLER v37

> 🌐 **Deutsch** (maßgeblich) · die englische Fassung steht in
> [`CLAUDE.en.md`](CLAUDE.en.md).

**Die Arbeitsgrundlage steht in [`CLAUDE.md`](CLAUDE.md). Lies sie zuerst und
vollständig — diese Datei wiederholt sie nicht.**

Das ist Absicht. Zwei Kopien derselben Regeln laufen auseinander, sobald eine
davon gepflegt wird und die andere nicht; genau dieses Fehlerbild hat das
Projekt schon einmal getroffen (der Build-Stempel stand vier Mal im Code und
wanderte nie mit, v4.2). `CLAUDE.md` ist die eine Wahrheit, weil Claude Code
sie nur im Wurzelverzeichnis findet.

Diese Datei existiert, damit Werkzeuge, die nach `AGENTS.md` suchen — Codex,
Cursor, Jules und andere — den Weg dorthin finden.

## Das Minimum, bevor du irgendetwas anfasst

Vier Dinge, an denen hier schon reale Arbeit gescheitert ist:

1. **`bot.py` hat über 23.000 Zeilen / 1,2 MB ≈ 294.000 Token.** Diese Datei
   wird **nie** ganz gelesen und **nie** blind durchsucht. Erst fragen, wo
   etwas steht, dann den Ausschnitt holen:

       python tools/ncpatch.py find "donations"
       python tools/ncpatch.py sym  bot.py send_message
       python tools/ncpatch.py show bot.py 14348 14380

2. **Die Pflicht-Prüfkette läuft vor jeder Auslieferung, ohne Ausnahme.** Sie
   steht in `CLAUDE.md`; kurz: `py_compile`, `pyflakes` (0 Befunde), `ruff`,
   `ncpatch check`, `ncpatch docs`, `i18n_extract --check en` und die vier
   Testdateien. Unter Windows vorher `$env:PYTHONUTF8="1"`.

3. **Die Verträge in `test_restream.py` hängen an wörtlichem Quelltext.**
   Kippt einer, prüfe **zuerst**, ob der Vertrag oder nur sein Anker gebrochen
   ist. Einen Vertrag zu entschärfen, um grün zu werden, ist hier kein
   zulässiger Fix.

4. **Stille `except`-Blöcke sind der Hauptfeind.** Ein `log.warning` erscheint
   in einem ERROR-Log nie. Wenn etwas „nicht mehr geht", suche zuerst das
   `except`, das den Grund frisst — nicht den Fehler.

## Architektur-Grenze, die gilt

`nc/*`, `brain/*` und `discordbot.py` importieren **nie** aus `bot.py`.
Konfiguration kommt per `configure(...)`-Injection. `brain/` ist thread-basiert
und stdlib-only.

## Sprache

Code-Kommentare und alle Ausgaben auf Deutsch. Kommentare erklären **warum**,
nicht was — bevorzugt mit dem konkreten Fehlerbild, das die Zeile verhindert.

## Skills

Unter `.claude/skills/` liegen sieben Arbeitsanweisungen (Navigation, Änderungen
am Bot, HTML-Vorlagen, Betrieb, Datenbank, KI-Backends, Sicherheit). Auch wer
kein Claude Code benutzt, liest sie als Dokumentation — sie beschreiben die
Fallstricke des jeweiligen Bereichs genauer als jeder Kommentar im Code.
