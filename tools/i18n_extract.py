#!/usr/bin/env python3
"""i18n_extract — die uebersetzbaren Zeichenketten einsammeln und den Katalog pflegen.

    python3 tools/i18n_extract.py                 # Bericht: was ist da, was fehlt
    python3 tools/i18n_extract.py --write en      # locales/en.json ergaenzen (nie ueberschreiben)
    python3 tools/i18n_extract.py --check en      # Vertrag: fehlende + verwaiste Eintraege

Warum die deutsche Zeichenkette der Schluessel ist, steht in nc/i18n.py. Hier
steht die andere Haelfte: **wie man merkt, dass der Katalog auseinanderlaeuft.**
Ohne diese Pruefung waere der Preis des Verfahrens unsichtbar — ein geaenderter
deutscher Satz faellt still auf Deutsch zurueck, und niemand sieht es.

`--write` ergaenzt nur; eine bestehende Uebersetzung wird NIE angefasst. Sonst
wuerde ein Lauf des Werkzeugs geleistete Arbeit ueberschreiben.
"""

import argparse
import ast
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES = os.path.join(ROOT, "locales")

HTML_DATEIEN = ["templates/dashboard.html", "templates/brain.html",
                "templates/overlay.html", "website/lafap_index.html",
                "website/impressum.html", "website/datenschutz.html"]
PY_DATEIEN = ["bot.py"]

# Ein Text ist uebersetzbar, wenn er ueberhaupt Sprache enthaelt. Reine Zahlen,
# Symbole, CSS-Werte und Platzhalter fliegen raus.
_WORT = re.compile(r"[A-Za-zÄÖÜäöüß]{3}")
# Deutsche Marker: Umlaute oder Funktionswoerter. Englische Fachbegriffe wie
# "Restream" oder "Dashboard" sind in beiden Sprachen gleich und brauchen
# keinen Eintrag — sie werden hier bewusst NICHT eingesammelt.
_DEUTSCH = re.compile(
    r"[ÄÖÜäöüß]|\b(?:der|die|das|den|dem|des|ein|eine|einen|einem|und|oder|nicht|"
    r"kein|keine|keinen|wird|wurde|werden|ist|sind|war|waren|hat|haben|kann|"
    r"koennen|muss|muessen|soll|bitte|noch|schon|nur|auch|mehr|alle|jede|jeder|"
    r"beim|vom|zum|zur|fuer|mit|ohne|nach|vor|ueber|unter|seit|Fehler|Datei|"
    r"Ziel|Quelle|Zeit|Datum|Name|Anzahl|Grund|Stand|Wert|Seite|Sprache|"
    r"gespeichert|geladen|gestartet|gestoppt|laeuft|fehlt|fehlen|unbekannt)\b")

_SKIP_ATTR_WERTE = re.compile(r"^[\d\s.,:%#/+-]*$")


def _ist_uebersetzbar(text):
    t = (text or "").strip()
    if len(t) < 3 or not _WORT.search(t):
        return False
    if t.startswith("{{") or t.startswith("${") or t.startswith("&"):
        return False
    # Reine Bezeichner (CSS-Klassen, IDs, Dateinamen, URLs) sind kein Text.
    if re.fullmatch(r"[\w./#:-]+", t):
        return False
    if t.startswith("http://") or t.startswith("https://"):
        return False
    return bool(_DEUTSCH.search(t))


def _html_strings(pfad):
    """Textknoten, uebersetzbare Attribute und deutschsprachige JS-Literale."""
    roh = io.open(os.path.join(ROOT, pfad), encoding="utf-8").read()
    ohne_js = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", "",
                     roh, flags=re.S)
    raus = set()
    for t in re.findall(r">([^<>]+)<", ohne_js):
        if _ist_uebersetzbar(t):
            raus.add(t.strip())
    for a in re.findall(r'(?:placeholder|title|aria-label|alt)="([^"]{3,})"', ohne_js):
        if _ist_uebersetzbar(a) and not _SKIP_ATTR_WERTE.match(a):
            raus.add(a.strip())
    js = "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", roh, flags=re.S))
    for a, b, c in re.findall(r"'([^'\\\n]{4,})'|\"([^\"\\\n]{4,})\"|`([^`\\\n]{4,})`", js):
        s = a or b or c
        if _ist_uebersetzbar(s):
            raus.add(s.strip())
    return raus


def _py_strings(pfad):
    """Deutschsprachige Literale im Python-Quelltext — ohne Docstrings.

    Docstrings und Kommentare erklaeren den Code fuer Entwickler und gehoeren
    NICHT in den Katalog: sie erreichen nie einen Benutzer, wuerden ihn aber um
    Hunderte Eintraege aufblaehen. Der AST unterscheidet das zuverlaessig,
    ein Regex nicht.
    """
    quelle = io.open(os.path.join(ROOT, pfad), encoding="utf-8").read()
    baum = ast.parse(quelle)
    docstrings = set()
    for n in ast.walk(baum):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            d = ast.get_docstring(n, clean=False)
            if d:
                docstrings.add(d)
    raus = set()
    for n in ast.walk(baum):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if n.value in docstrings:
                continue
            if _ist_uebersetzbar(n.value):
                raus.add(n.value.strip())
        elif isinstance(n, ast.JoinedStr):
            # f-Strings: nur die festen Teile. Der Platzhalter selbst ist Daten.
            fest = "".join(x.value for x in n.values
                           if isinstance(x, ast.Constant) and isinstance(x.value, str))
            if _ist_uebersetzbar(fest) and len(fest.strip()) > 6:
                raus.add(fest.strip())
    return raus


def sammeln():
    gefunden = {}
    for p in HTML_DATEIEN:
        if os.path.exists(os.path.join(ROOT, p)):
            for s in _html_strings(p):
                gefunden.setdefault(s, set()).add(p)
    for p in PY_DATEIEN:
        if os.path.exists(os.path.join(ROOT, p)):
            for s in _py_strings(p):
                gefunden.setdefault(s, set()).add(p)
    return gefunden


def _laden(sprache):
    pfad = os.path.join(LOCALES, "%s.json" % sprache)
    if not os.path.exists(pfad):
        return {"sprache": sprache, "strings": {}}
    with io.open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _speichern(sprache, daten):
    os.makedirs(LOCALES, exist_ok=True)
    daten["strings"] = dict(sorted(daten.get("strings", {}).items()))
    with io.open(os.path.join(LOCALES, "%s.json" % sprache), "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", metavar="SPRACHE", help="fehlende Schluessel ergaenzen (leer)")
    ap.add_argument("--check", metavar="SPRACHE", help="Vertrag: fehlend + verwaist melden")
    ap.add_argument("--liste", metavar="SPRACHE", help="fehlende Schluessel ausgeben, einer je Zeile")
    a = ap.parse_args()

    gefunden = sammeln()
    print("gefunden: %d uebersetzbare Zeichenketten in %d Dateien"
          % (len(gefunden), len(HTML_DATEIEN) + len(PY_DATEIEN)))

    sprache = a.write or a.check or a.liste
    if not sprache:
        je_datei = {}
        for s, dateien in gefunden.items():
            for d in dateien:
                je_datei[d] = je_datei.get(d, 0) + 1
        for d, n in sorted(je_datei.items(), key=lambda x: -x[1]):
            print("   %-34s %4d" % (d, n))
        return 0

    daten = _laden(sprache)
    vorhanden = daten.get("strings", {})
    fehlend = sorted(s for s in gefunden if s not in vorhanden)
    verwaist = sorted(k for k in vorhanden if k not in gefunden)

    if a.liste:
        for s in fehlend:
            print(json.dumps(s, ensure_ascii=False))
        return 0

    print("Katalog %s: %d Eintraege | fehlend: %d | verwaist: %d"
          % (sprache, len(vorhanden), len(fehlend), len(verwaist)))

    if a.check:
        if verwaist:
            print("\nVERWAIST — im Quelltext nicht mehr gefunden (Text geaendert?):")
            for k in verwaist[:20]:
                print("   %s" % k[:100])
            if len(verwaist) > 20:
                print("   ... und %d weitere" % (len(verwaist) - 20))
        if fehlend:
            print("\nFEHLEND — ohne Uebersetzung, faellt auf Deutsch zurueck:")
            for k in fehlend[:20]:
                print("   %s" % k[:100])
            if len(fehlend) > 20:
                print("   ... und %d weitere" % (len(fehlend) - 20))
        return 1 if (fehlend or verwaist) else 0

    for s in fehlend:
        vorhanden[s] = ""
    daten["strings"] = vorhanden
    daten.setdefault("sprache", sprache)
    _speichern(sprache, daten)
    print("geschrieben: locales/%s.json (%d neue leere Eintraege)" % (sprache, len(fehlend)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
