# patches/

Anker-Patches für `tools/ncpatch.py`. Eine Datei je Entwicklungswelle.

**Der Bezugspunkt ist der Stand VOR der Welle.** Ein Patch, dessen Welle
bereits eingespielt ist, findet seine Anker deshalb nicht mehr —
`ncpatch verify` meldet dann „Anker 0x gefunden". Das ist kein Fehler,
sondern der Beweis, dass die Welle drin ist.

Wozu es den Ordner gibt: weicht der Bestand auf dem Server vom Repository ab
(ein Handgriff direkt dort, eine liegengebliebene ZIP), ist ein Patch der
kleinste sichere Weg, genau eine Änderung nachzuziehen — alles-oder-nichts,
mit automatischer Sicherung und anschließender Prüfung:

    python tools/ncpatch.py verify patches/<welle>.json   # Trockenlauf
    python tools/ncpatch.py apply  patches/<welle>.json   # legt .bak an

**Derzeit liegt hier kein offener Patch.** v5.6-W197 hat die vier aus
v4.0-W113 bis W116 entfernt: ihr Bezugsstand ist seit über achtzig Wellen
überholt, jeder Anker darin trifft heute ins Leere, und ausgeliefert wird
über die Update-Funktion bzw. das ZIP (siehe `.claude/skills/nc-betrieb`).
Wer sie braucht, findet sie in der Git-Historie.

## Cache-Stempel der öffentlichen Seite

Nach **jeder** Änderung an `website/raum.css` oder `website/raum.js` einmal

    python tools/stempel_assets.py          # stempeln
    python tools/stempel_assets.py --check  # nur prüfen (Exit 1 = veraltet)

laufen lassen — sonst holt ein Browser mit warmem Cache die alte Fassung. Der
Vertrag `test_v40_w117_asset_stempel` fährt `--check` mit, ein vergessener
Lauf fällt also in der Prüfkette auf.
