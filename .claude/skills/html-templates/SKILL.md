---
name: html-templates
description: Eigenstaendige HTML-Oberflaechen fuer NIGHTCRAWLER und LAFAP bauen — Token-System, die vier Deck-Themen Messing (dunkel, Vorgabe), Blaupause (hell), Kontrast (WCAG AAA) und Phosphor (Nacht), Pruefkette vor jeder Auslieferung. Nutze dies bei jeder Aenderung an templates/*.html oder website/*.html.
---

# HTML-Oberflaechen fuer NIGHTCRAWLER

## Die These, aus der alles folgt

Das Dashboard ist ein **Wachinstrument**, kein Schaufenster. Es laeuft 24/7
und meldet Zustand. Jede gestalterische Entscheidung leitet sich daraus ab:
Ablesbarkeit vor Effekt, Ruhe vor Bewegung, ein einziges wiederkehrendes
Detail statt vieler Verzierungen.

## Die zwei Themen

Umgeschaltet wird ueber `html[data-theme]`, nie ueber Klassen an einzelnen
Elementen. Beide Themen definieren **dieselben** Token — wer eine neue Farbe
braucht, ergaenzt sie in BEIDEN.

**Messing** (dunkel, Standard). Warum nicht Reinschwarz plus `#FFD700`:
das ist die Standardantwort auf "schwarz-gold" und liest sich als
Krypto-Dashboard. Gold ist hier Metall an Geraet — warm, leicht
entsaettigt, auf einer belichteten Flaeche. Der Grund ist deshalb ein warm
verschobener Kohleton (`#0C0B09`), kein Schwarz: erst darauf wirkt Messing
wie Messing.

    --bg #0C0B09   --neon #E8C86A (poliert)   --neon-dim #C9A227 (roh)
    --text #EFE7D6 (warmes Papierweiss, nicht #FFF)

**Blaupause** (hell). Technische Zeichnung statt SaaS-Startseite:
Papierweiss mit einem Hauch Kuehle, Tuscheblau als Text, Stahl als Zweitton.
Dasselbe Instrument bei Tageslicht — nicht ein anderes Produkt.

    --bg #F4F7FB   --neon #1E5EFF   --neon-dim #4A6FA5
    --text #0F2544 (Tuscheblau, kein Schwarz)

**Kontrast** (v4.2-W137, nur Deck). Fuer helle Umgebung und eingeschraenktes
Sehen: jede Text- und Signalfarbe >= 7:1 auf dem Panel (WCAG AAA), keine
Glows, keine Bewegung, 2-px-Rahmen, 3-px-Fokusring. Waehlt sich bei
`prefers-contrast: more` von selbst. Der Vertrag rechnet die Kontraste aus
den Tokens nach — **wer hier eine Farbe aendert, faellt dort, nicht erst beim
Nutzer.**

**Phosphor** (v4.2-W140, nur Deck). Gruener Bildschirmphosphor fuer die
Nacht: Werte und Kopfzeilen glimmen, Fliesstext nicht; jede Farbe >= 4,5:1
(AA). Rot und Bernstein bleiben Warnfarben — ein Fehler darf in einem gruenen
Thema nicht gruen aussehen; auch das prueft der Vertrag.

**Ein neues Thema** braucht drei Dinge, sonst faellt `_test_v42_w140_phosphor_thema`:
einen Token-Block `html[data-theme="name"]{…}`, einen Eintrag in `NC_THEMEN`,
`NC_THEMA_NAME` und `NC_THEMA_ZEICHEN` (eigenes Zeichen), und die Kontraste.

## Die Signatur

Die **Bezel-Kante**: jede `.panel`-Oberkante traegt eine 1px-Linie mit
Verlauf (`--bezel`), wie die Blende eines Rack-Geraets. Das ist das eine
Detail, an dem die Oberflaeche wiedererkannt wird. Alles andere bleibt
still. Kein Neon-Glow — Metall reflektiert, es leuchtet nicht.

## Schrift

Orbitron als Anzeigeschrift, sparsam und nur in Versalien mit weitem
Zeichenabstand. JetBrains Mono fuer alle Zahlen und Daten, immer mit
`font-variant-numeric: tabular-nums` — sonst springen Werte beim
Aktualisieren. Fliesstext laeuft ueber den System-Stack.

**Schriften NIE von fonts.googleapis.com laden.** Dabei geht die IP jedes
Besuchers an Google. Lokal einbinden, siehe website/FONTS.md.

## Arbeitsweise am Dashboard

Das Markup entsteht groesstenteils zur Laufzeit per `innerHTML` im
JavaScript (rund 190 Stellen). Wer das Aussehen aendern will, aendert
deshalb **CSS gegen die bestehenden Klassennamen**, nicht das HTML:
`.panel`, `.head`, `.body`, `.btn`, `.tag`, `.metric`, `.faint`, `.mono`,
`.skel`, `.empty`, `.tbl-wrap`, `.field`, `.dot`, `.led`.

So wirkt eine Aenderung auf alle Ansichten gleichzeitig, ohne eine einzige
Zeile Logik anzufassen.

## Pruefkette — vor JEDER Auslieferung

    node --check           je Script-Block (JSON-LD als JSON pruefen, nicht als JS!)
    Klammerbilanz          je <style>-Block: { == }
    doppelte id=           muessen null sein
    Tag-Bilanz             gegen den Ausgangsstand vergleichen, nicht absolut
                           (div-Tags stecken auch in JS-Strings)
    aria-label             jeder Icon-Knopf ohne Text braucht eines
    Touch-Ziele            min 44px bei @media(pointer:coarse)

`python3 tools/ncpatch.py check` faehrt IDs und CSS-Bilanz automatisch.

## Texte

Ein Schalter benennt sein **Ergebnis**, nicht seinen Zustand: der Knopf
heisst "Blaupause", wenn ein Klick dorthin fuehrt. Leere Zustaende sind
eine Aufforderung, keine Entschuldigung. Fehlermeldungen sagen, was
passiert ist und was zu tun ist — nie nur "Fehler".

Alles auf Deutsch, Satzform, keine Fuellwoerter.

## Was zu vermeiden ist

- Neon-Glow, Leuchtschatten, animierte Verlaeufe im Hintergrund
- Mehr als eine Bewegung gleichzeitig auf dem Schirm
- Farbe als einziger Traeger einer Information (immer Text oder Form dazu)
- `localStorage` ist hier ERLAUBT (eigener Flask-Server, kein Artifact)
