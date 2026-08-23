---
name: nc-navigation
description: Etwas in NIGHTCRAWLER finden, ohne Token zu verbrennen — die Reihenfolge Karte, Symbol, Ausschnitt statt Suche über den 1,5-MB-Monolithen. Nutze dies IMMER als ersten Schritt, bevor du bot.py, templates/dashboard.html oder ein nc//brain/-Modul liest, und bei jeder Frage der Form "wo ist X", "welche Route", "welcher Command", "wie heißt die Funktion für". Trigger: wo ist, finden, suchen, welche Route, welcher Endpoint, Slash-Command, Funktion für, Zeile, INDEX, Karte, navigieren.
---

# Navigation — erst wissen wo, dann lesen

## Das Kostenbild, das die Regel begründet

    bot.py                  ~400.000 Token   niemals lesen
    .claude/INDEX.md             ~12.000 Token   nur wenn wirklich alles gebraucht wird
    ncpatch find <begriff>          ~100 Token   der Normalfall
    ncpatch show <von> <bis>     50-500 Token   der eigentliche Ausschnitt

Ein blinder Volltext-Scan über den Monolithen kostet mehr als hundert gezielte
Zugriffe. Der teure Teil ist fast nie der Code, den man braucht — es ist das
Suchen danach.

## Die Reihenfolge

**1. Fragen, wo es steht.** Nie mit einer Suche über die Datei anfangen.

    python tools/ncpatch.py find "donations"      # Routen, Commands, Module
    python tools/ncpatch.py find "restream" -n 8

Antwortet aus `.claude/INDEX.md` und liefert Zeilennummern. Die Karte kennt
alle 283 Flask-Routen (mit `methods=`), 45 Discord-Slash-Commands, Discord-Events,
450 Top-Level-Funktionen mit Zeilenbereich sowie die öffentliche API jedes
`nc/`- und `brain/`-Moduls.

**2. Den Bereich eingrenzen.** Bei einem bekannten Funktionsnamen direkt:

    python tools/ncpatch.py sym bot.py api_donations_summary
    # -> FunctionDef api_donations_summary: Z.16907-16960 (54 Zeilen)

**3. Nur diesen Ausschnitt lesen.**

    python tools/ncpatch.py show bot.py 16907 16960

**4. Erst wenn die Karte nichts hergibt**, gezielt greppen — mit Muster, nie
mit einem Begriff, der hundertfach vorkommt:

    python tools/ncpatch.py grep "router.route(" bot.py -C 3

## Wann die Karte neu gebaut werden muss

    python tools/ncpatch.py map

Nach jeder Änderung an Routen, Slash-Commands oder Top-Level-Funktionen — sonst
zeigen die Zeilennummern daneben. Der Lauf dauert unter einer Sekunde und liest
per `ast`, nicht per Regex; ein Syntaxfehler in einem `nc/`-Modul erscheint als
Zeile in der Karte statt als Absturz.

Die Karte ist ein **Erzeugnis**, keine Quelle. Sie wird nie von Hand
bearbeitet, und ein Widerspruch zwischen Karte und Code heißt immer: Karte neu
bauen.

## Was Karte und Symbolsuche nicht können

`ncpatch sym` und die Karte sehen **Top-Level**-Definitionen. Verschachtelte
Funktionen, Closures und Methoden innerhalb von Klassen stehen nicht drin —
dafür `grep` mit `def name` als Muster.

Für Fragen, die über Namen hinausgehen — „wer ruft das auf?", „was gibt das
zurück?" — ist der Sprachserver das schärfere Werkzeug: `findReferences`,
`incomingCalls`, `hover` und `goToDefinition` beantworten das, ohne eine Zeile
Quelltext in den Kontext zu holen. Bei „Funktion X ändern, wer hängt dran?"
sind `findReferences`/`incomingCalls` immer billiger als jede Suche.

## Templates

`templates/dashboard.html` ist der zweite große Brocken. Markup entsteht dort zu
großen Teilen zur Laufzeit per `innerHTML` (rund 190 Stellen) — die Suche nach
einem sichtbaren Text im HTML geht deshalb oft ins Leere. Statt nach dem
angezeigten Text nach der **Klasse** oder der **Element-ID** suchen, und
Aussehen über CSS gegen bestehende Klassennamen ändern statt über das Markup.

## Der Reflex, der am meisten spart

Bevor eine Datei geöffnet wird, die Frage stellen: *brauche ich den Inhalt oder
nur den Ort?* Fast immer ist es der Ort. Und wenn es der Inhalt ist, dann von
Zeile bis Zeile — nie die Datei.
