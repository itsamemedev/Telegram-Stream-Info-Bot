# Schriften lokal ablegen

Die Seite laedt Orbitron und JetBrains Mono nicht mehr von
fonts.googleapis.com. Grund: dabei uebertraegt der Browser jedes Besuchers
dessen IP-Adresse an Google, ohne Einwilligung. Fuer eine deutsche Seite
mit Impressum und Datenschutzhinweis ist das ein vermeidbares Risiko
(LG Muenchen I, 20.01.2022, Az. 3 O 17493/20).

Das ist eine technische Massnahme, keine Rechtsberatung — die Einordnung
in deinen Datenschutzhinweis machst du oder dein Anwalt.

## Die Dateien liegen bei — erledigt (v4.2-W88)

`website/fonts/` traegt die sechs Schnitte, die `lafap_index.html` per
`@font-face` anfordert. Vorher fehlte der Ordner ganz: alle sechs Anfragen
liefen auf 404, `document.fonts` meldete sechsmal `status: error`, und die
Seite rendete durchgehend in den System-Rueckfaellen (`sans-serif` statt
Orbitron, generisches `monospace` statt JetBrains Mono). Kaputt war nichts —
aber vom Terminal-Look blieb nichts uebrig.

    fonts/orbitron-500.woff2          8,0 KB
    fonts/orbitron-700.woff2          7,8 KB
    fonts/orbitron-900.woff2          7,7 KB
    fonts/jetbrainsmono-400.woff2    20,2 KB
    fonts/jetbrainsmono-500.woff2    20,9 KB
    fonts/jetbrainsmono-700.woff2    21,0 KB
                                    ------
                                    100 KB gesamt

Beide Schriften stehen unter der SIL Open Font License; die Lizenztexte
liegen als `fonts/OFL-Orbitron.txt` und `fonts/OFL-JetBrainsMono.txt`
daneben. **Die OFL verlangt, dass sie mitgeliefert werden** — wer die
Schriften verschiebt, nimmt sie mit.

## Neu bauen (wenn eine Fassung veraltet)

Gebaut wurde aus den Variable Fonts des offiziellen `google/fonts`-Bestands,
auf statische Schnitte festgestellt und auf den Zeichensatz beschraenkt, den
die Seite braucht. Ohne diese Beschraenkung ist JetBrains Mono je Schnitt
rund zehnmal so gross — bei einer Seite, die sechs Schnitte laedt, ist das
der Unterschied zwischen 100 KB und einem Megabyte.

    pip install fonttools brotli
    curl -L -o "Orbitron.ttf" \
      "https://raw.githubusercontent.com/google/fonts/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
    curl -L -o "JetBrainsMono.ttf" \
      "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"

    python3 - <<'EOF'
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    from fontTools import subset
    U = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
         "U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,"
         "U+FEFF,U+FFFD")                       # wie Google Webfonts "latin"
    for datei, praefix, gewichte in (("Orbitron.ttf", "orbitron", (500,700,900)),
                                     ("JetBrainsMono.ttf", "jetbrainsmono", (400,500,700))):
        for w in gewichte:
            f = TTFont(datei)
            instantiateVariableFont(f, {"wght": w}, inplace=True, updateFontNames=True)
            o = subset.Options(); o.layout_features = ["*"]; o.name_IDs = ["*"]
            s = subset.Subsetter(options=o)
            s.populate(unicodes=subset.parse_unicodes(U)); s.subset(f)
            f.flavor = "woff2"; f.save("fonts/%s-%d.woff2" % (praefix, w))
    EOF

Wer eine Datei austauscht, faehrt danach die Gegenprobe — sie ist der
eigentliche Punkt, denn ein 404 auf eine Schrift bricht nichts und faellt
deshalb monatelang niemandem auf:

    python3 -m http.server 8777 --directory website
    # in der Browser-Konsole:
    [...document.fonts].map(f => f.family + ' ' + f.status)
    # erwartet: sechsmal "loaded", nie "error"

**Nie von fonts.googleapis.com laden.** Dabei uebertraegt der Browser jedes
Besuchers dessen IP-Adresse an Google, ohne Einwilligung. Fuer eine deutsche
Seite mit Impressum und Datenschutzhinweis ist das ein vermeidbares Risiko
(LG Muenchen I, 20.01.2022, Az. 3 O 17493/20). Das ist eine technische
Massnahme, keine Rechtsberatung.

## og-card.png — erledigt

Die Seite verweist auf `https://lafap.de/og-card.png` (1200x630). Ohne
diese Datei zeigten Discord, WhatsApp und Telegram beim Teilen des Links
eine graue Karte.

Die Karte liegt jetzt bei: `website/og-card.png`, gebaut aus
`website/og-card.svg` im Terminal-Look der Seite (Phosphor/Cyan, Akronym
wie im Hero, Sentinel-Kern). Beim Ausrollen muss sie im **Wurzel-**
Verzeichnis der Domain landen, nicht in einem Unterordner — der
og:image-Verweis ist absolut.

Neu bauen nach einer Aenderung an der SVG (beliebiger Renderer, hier
Chromium headless):

    chromium --headless --screenshot=og-card.png \
             --window-size=1200,630 og-card.svg

Aendert sich der Bildinhalt, muss der Cache der Plattformen brechen —
Discord und WhatsApp halten OG-Bilder lange. Dafuer den Dateinamen
versionieren (`og-card-2.png`) und den Verweis in `lafap_index.html`
mitziehen.
