#!/usr/bin/env python3
"""tools/release_notes.py — Release-Text aus nc/version.py und dem CHANGELOG.

Warum ein Skript und keine drei Zeilen Bash im Workflow: der Text ist die
einzige Stelle, an der ein Aussenstehender erfaehrt, was eine Fassung bringt.
Er gehoert damit an dieselbe Quelle wie der Dashboard-Footer und das
"Was ist neu"-Panel — nc/version.py. Wer ihn im Workflow zusammenbaut, hat die
vierte Kopie derselben Wahrheit, und genau daran ist der Build-Stempel schon
einmal auseinandergelaufen (v4.2).

Warum NICHT der ganze CHANGELOG-Abschnitt: [4.2] hat 126 Eintraege und
239.000 Zeichen. Das GitHub-Limit fuer einen Release-Text liegt bei 125.000 —
ein Release mit angehaengtem Volltext waere nicht lang, sondern abgelehnt.
Deshalb Highlights plus Verweis.

    python3 tools/release_notes.py            # Fassung aus nc/version.py
    python3 tools/release_notes.py 4.1        # eine bestimmte Fassung
"""
from __future__ import annotations

import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WURZEL)

# GitHub lehnt laengere Release-Texte ab. Mit Reserve fuer den Verweis unten.
MAX_ZEICHEN = 120_000


def _version_daten(fassung=None):
    import nc.version as v
    fassung = fassung or v.VERSION
    treffer = [c for c in v.CHANGELOG if c.get("version") == fassung]
    if not treffer:
        raise SystemExit(
            f"ABBRUCH — nc/version.py kennt keine Fassung {fassung}. "
            f"Bekannt: {', '.join(c.get('version', '?') for c in v.CHANGELOG)}")
    return fassung, treffer[0]


def _wellen_zaehlen(fassung):
    """Wie viele Eintraege traegt der CHANGELOG-Abschnitt dieser Fassung?

    Die Zahl steht im Release-Text, damit der Verweis auf den CHANGELOG nicht
    ins Leere zeigt ("Details siehe dort" ohne zu sagen, wie viel dort steht).
    """
    pfad = os.path.join(WURZEL, "docs", "CHANGELOG.md")
    try:
        with open(pfad, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return 0
    marke = f"## [{fassung}]"
    i = text.find(marke)
    if i < 0:
        return 0
    j = text.find("\n## [", i + len(marke))
    return text[i:j if j > 0 else len(text)].count("\n### ")


def bauen(fassung=None) -> str:
    fassung, eintrag = _version_daten(fassung)
    titel = eintrag.get("title") or ""
    datum = eintrag.get("date") or ""
    zeilen = [f"## NIGHTCRAWLER v{fassung}" + (f" — „{titel}“" if titel else ""), ""]
    if datum:
        zeilen += [f"*{datum}*", ""]

    for punkt in eintrag.get("highlights") or []:
        zeilen.append(f"- {punkt}")
    zeilen.append("")

    n = _wellen_zaehlen(fassung)
    zeilen += [
        "### Vollständige Historie",
        "",
        (f"Der Abschnitt `[{fassung}]` in "
         f"[`docs/CHANGELOG.md`](docs/CHANGELOG.md) trägt "
         + (f"**{n} Einträge** " if n else "")
         + "mit Befund, Ursache und Gegenprobe je Welle. Er steht bewusst "
           "nicht hier: er ist länger als ein Release-Text sein darf."),
        "",
        "### Auslieferung",
        "",
        "Ausgeliefert wird als ZIP **über den Bestand**, nicht per `git pull` —",
        "`.env`, Datenbank, Cookies und Aufnahmen bleiben unangetastet.",
        "Die Anleitung steht in [`docs/START_HIER.txt`](docs/START_HIER.txt).",
    ]
    text = "\n".join(zeilen)

    if len(text) > MAX_ZEICHEN:
        # Lieber sichtbar kuerzen als vom Server abgelehnt werden.
        text = (text[:MAX_ZEICHEN]
                + "\n\n*(gekürzt — siehe `docs/CHANGELOG.md`)*")
    return text


def main(argv):
    fassung = argv[1] if len(argv) > 1 else None
    sys.stdout.write(bauen(fassung) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
