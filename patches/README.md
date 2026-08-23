# patches/

Anker-Patches für `tools/ncpatch.py`. Eine Datei je Entwicklungswelle.

**Der Bezugspunkt ist der Stand VOR der Welle.** Ein Patch, dessen Welle
bereits eingespielt ist, findet seine Anker deshalb nicht mehr —
`ncpatch verify` meldet dann „Anker 0x gefunden". Das ist kein Fehler,
sondern der Beweis, dass die Welle drin ist.

Wozu die Dateien trotzdem hier liegen: die Auslieferung läuft per ZIP über
den Bestand auf dem Server (siehe `.claude/skills/nc-betrieb`). Weicht der
Bestand vom Repository ab, ist der Patch der kleinste sichere Weg, genau
diese Änderung nachzuziehen — alles-oder-nichts, mit automatischer
Sicherung und anschließender Prüfung.

| Datei | Welle | Inhalt |
|---|---|---|
| `w113_restream_stability.json` | v4.0-W113 | Wiederanlauf-Härte des Restreams (`bot_v37.py`) |
| `w114_website_3d.json` | v4.0-W114 | Die öffentliche Seite im Raum (`website/lafap_index.html`, `impressum.html`, `datenschutz.html`) |
| `w115_relay_sicht.json` | v4.0-W115 | Relays sichtbar + bewacht, Stillstand im Panel, Quellen-Wächter (`bot_v37.py`, `templates/dashboard.html`) |
| `w116_alterung_flattern_rate.json` | v4.0-W116 | tee-Fehler altern, Flattern eskaliert, Raten-Einbruch bei der Aufnahme (`bot_v37.py`) |

**W114 braucht zusätzlich zwei NEUE Dateien**, die ein Anker-Patch nicht
anlegen kann: `website/raum.css` und `website/raum.js`. **W116 ebenso:**
`nc/flapguard.py` (neu) und die Erweiterung in `nc/recdiag.py`. Beide gehören ins
Archiv und müssen vor dem Patch im `website/`-Ordner liegen — sonst laden
die drei Seiten ins Leere und bleiben flach (kaputt geht dabei nichts).
