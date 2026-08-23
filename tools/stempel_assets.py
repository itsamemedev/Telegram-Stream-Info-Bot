#!/usr/bin/env python3
"""stempel_assets — v4.0-W117: Cache-Stempel fuer die geteilten Website-Dateien.

WARUM: raum.css und raum.js werden von allen drei oeffentlichen Seiten
unversioniert geladen. Nach einem Deploy haelt ein Browser mit warmem Cache
die alte Fassung — die Seite bleibt dann still flach statt kaputt (das ist
so gebaut), aber die Aenderung kommt eben nicht an. Und weil nichts bricht,
faellt es auch niemandem auf.

Der Stempel ist die ersten 10 Zeichen eines SHA-256 ueber den Dateiinhalt:
gleicher Inhalt -> gleicher Stempel -> Cache bleibt gueltig; geaenderter
Inhalt -> neue URL -> der Browser holt sie. Kein Zeitstempel, keine
Build-Nummer, nichts das man von Hand hochzaehlen und vergessen kann.

    python tools/stempel_assets.py           # stempeln
    python tools/stempel_assets.py --check   # nur pruefen (Exit 1 = veraltet)

Der Vertrag test_v40_w117_asset_stempel in test_restream.py faehrt --check
mit. Ein vergessener Lauf faellt damit in der Pruefkette auf und nicht beim
Betrachter.
"""
import hashlib
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(WURZEL, "website")
ASSETS = ("raum.css", "raum.js")
SEITEN = ("lafap_index.html", "impressum.html", "datenschutz.html")


def stempel(name):
    with open(os.path.join(WEB, name), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:10]


def muster(name):
    """href="raum.css" ODER href="raum.css?v=abc123" — beides treffen."""
    return re.compile(r'((?:href|src)=")' + re.escape(name) + r'(?:\?v=[0-9a-f]+)?(")')


def main():
    pruefen = "--check" in sys.argv
    marken = {a: stempel(a) for a in ASSETS}
    veraltet, geaendert = [], []
    for seite in SEITEN:
        pfad = os.path.join(WEB, seite)
        if not os.path.exists(pfad):
            print("  FEHLT: %s" % seite)
            veraltet.append(seite)
            continue
        with open(pfad, encoding="utf-8") as fh:
            alt = fh.read()
        neu = alt
        for a, m in marken.items():
            neu, n = muster(a).subn(r'\g<1>' + a + "?v=" + m + r"\g<2>", neu)
            if not n:
                print("  %s: %s wird nicht eingebunden" % (seite, a))
        if neu != alt:
            if pruefen:
                veraltet.append(seite)
            else:
                with open(pfad, "w", encoding="utf-8") as fh:
                    fh.write(neu)
                geaendert.append(seite)

    if pruefen:
        if veraltet:
            print("VERALTET — bitte `python tools/stempel_assets.py` ausfuehren "
                  "(%s)" % ", ".join(veraltet))
            return 1
        print("Stempel aktuell (%s)" % ", ".join("%s=%s" % kv for kv in marken.items()))
        return 0
    print("gestempelt: %s" % (", ".join(geaendert) if geaendert else "nichts zu tun"))
    for a, m in marken.items():
        print("  %s -> ?v=%s" % (a, m))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
