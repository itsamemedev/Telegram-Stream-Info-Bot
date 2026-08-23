# Schriften lokal ablegen

Die Seite laedt Orbitron und JetBrains Mono nicht mehr von
fonts.googleapis.com. Grund: dabei uebertraegt der Browser jedes Besuchers
dessen IP-Adresse an Google, ohne Einwilligung. Fuer eine deutsche Seite
mit Impressum und Datenschutzhinweis ist das ein vermeidbares Risiko
(LG Muenchen I, 20.01.2022, Az. 3 O 17493/20).

Das ist eine technische Massnahme, keine Rechtsberatung — die Einordnung
in deinen Datenschutzhinweis machst du oder dein Anwalt.

## Dateien holen (einmalig)

Beide Schriften stehen unter der SIL Open Font License und duerfen
selbst gehostet werden.

    cd website && mkdir -p fonts && cd fonts

    # Orbitron (500, 700, 900)
    curl -L -o orbitron-500.woff2 \
      "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
    # Variable Font -> mit fonttools in statische woff2 wandeln:
    pip install fonttools brotli
    python3 - <<'PY'
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    for w in (500,700,900):
        f = TTFont("Orbitron[wght].ttf")
        instantiateVariableFont(f, {"wght": w}, inplace=True)
        f.flavor = "woff2"
        f.save(f"orbitron-{w}.woff2")
    PY

Einfacher, wenn du nicht basteln willst: die fertigen woff2 von
gwfh.mranftl.com (Google Webfonts Helper) herunterladen — dort Orbitron
und JetBrains Mono waehlen, Zeichensatz "latin", und die Dateien so
benennen:

    fonts/orbitron-500.woff2
    fonts/orbitron-700.woff2
    fonts/orbitron-900.woff2
    fonts/jetbrainsmono-400.woff2
    fonts/jetbrainsmono-500.woff2
    fonts/jetbrainsmono-700.woff2

## Bis dahin

Die Seite funktioniert auch OHNE die Dateien: `font-display:swap` sorgt
dafuer, dass der Browser sofort die Fallback-Schrift zeigt. Es sieht nur
weniger nach Terminal aus. Kaputt ist nichts.

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
