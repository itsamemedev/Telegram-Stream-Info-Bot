#!/usr/bin/env python3
"""i18n_wrap — Benutzertexte in den Blueprints an der Quelle umschliessen.

    python3 tools/i18n_wrap.py --check           # was fehlt noch? (aendert nichts)
    python3 tools/i18n_wrap.py --write           # t(...) setzen, Helfer ergaenzen
    python3 tools/i18n_wrap.py --write nc/routes/ops.py

════════════════════════════════════════════════════════════════════════
WARUM DAS EIN WERKZEUG IST UND KEINE HANDARBEIT
════════════════════════════════════════════════════════════════════════
Die 243 Routen in `nc/routes/` antworten im Fehlerfall mit deutschem Text.
Uebersetzt werden kann er nur AN DER QUELLE: im Browser landet er meist
verkettet in einem Knoten (`"Fehler: " + d.error`), ein Katalogeintrag fuer
den blossen Text traefe dort nie (siehe tools/i18n_extract.py).

Von Hand waeren das ueber hundert Stellen in einundzwanzig Dateien — und die
EINE vergessene faellt niemandem auf, weil eine deutsch gebliebene Zeile
aussieht wie eine, die es noch nicht gibt. Genau die Ueberlegung wie bei der
Shell-Uebersetzung (W17): lieber an einer Stelle richtig als hundertmal
einzeln.

Das Werkzeug schreibt **textuell**, nicht per AST-Ausgabe: `ast.unparse`
wuerde die ganze Datei umformatieren und den Diff unlesbar machen. Stattdessen
werden die Spaltenpositionen der Literale benutzt und von hinten nach vorn
ersetzt, damit die Offsets gueltig bleiben.

Bewusst NICHT angefasst:

* **f-Strings.** Ihr Wert steht erst zur Laufzeit fest; als Katalogschluessel
  waeren sie wertlos.
* **Mehrzeilige Literale** (implizite Verkettung ueber Zeilengrenzen). Sie
  werden gemeldet, nicht umgeschrieben — dort ist Handarbeit ehrlicher als
  eine Heuristik, die die Einrueckung zerlegt.
* **Logzeilen.** Die bleiben deutsch (CLAUDE.md): sie sind fuer den
  Betreiber und laufen nie durch die Uebersetzungsschicht.
"""

import argparse
import ast
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Schluessel, unter denen Text an einen MENSCHEN geht. `error` ist der Regelfall
# im Dashboard; die anderen kommen vereinzelt vor.
SENKE_KW = {"error", "hinweis", "msg", "message", "warn"}

# Ein Text ist Benutzertext, wenn er ueberhaupt Sprache enthaelt. Reine
# Bezeichner, Codes und Pfade fliegen raus.
_WORT = re.compile(r"[A-Za-zÄÖÜäöüß]{3}")

# Nur zum MELDEN, nie zum Entscheiden: welche Texte schon englisch dastehen.
#
# Der Katalog hat als Vertrag: der deutsche String ist der Schluessel
# (nc/i18n.py). Eine englische Fehlermeldung in einer deutschen API bricht das
# — und eine Identitaets-Uebersetzung ("file not found" -> "file not found")
# saehe in der Abdeckungszahl aus wie geleistete Arbeit, wo keine war. Die
# Loesung ist, den Quelltext deutsch zu formulieren, nicht den Katalog
# aufzuweichen.
#
# Diese Liste taugt ausdruecklich NICHT als Filter fuers Umschliessen: sie hat
# falsche Negative ("leere Frage" enthaelt weder Umlaut noch Funktionswort und
# gaelte als englisch). Ein Umschliessen mehr schadet nie — ein faelschlich
# unterlassenes bleibt fuer immer deutsch.
_DEUTSCH = re.compile(
    r"[ÄÖÜäöüß]|\b(?:der|die|das|den|dem|des|ein|eine|einen|einem|und|oder|nicht|"
    r"kein|keine|keinen|wird|wurde|werden|ist|sind|war|waren|hat|haben|kann|"
    r"koennen|muss|muessen|soll|bitte|noch|schon|nur|auch|mehr|alle|jede|jeder|"
    r"beim|vom|zum|zur|fuer|mit|ohne|nach|vor|ueber|unter|seit|Fehler|Datei|"
    r"Ziel|Quelle|Zeit|Datum|Name|Anzahl|Grund|Stand|Wert|Seite|Sprache|erforderlich|"
    r"gespeichert|geladen|gestartet|gestoppt|laeuft|fehlt|fehlen|unbekannt)\b")

HELFER = '''

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)
'''


def _ist_text(s):
    t = (s or "").strip()
    if len(t) < 3 or not _WORT.search(t):
        return False
    # Reine Bezeichner/Codes ("not_found", "db", "quota_exceeded") sind
    # Maschinenwerte, die das Dashboard auswertet — die duerfen sich NICHT
    # aendern, sonst greift eine Fallunterscheidung im JS nicht mehr.
    if re.fullmatch(r"[a-z0-9_.:/-]+", t):
        return False
    return True


def _englisch(quelle):
    """Benutzertexte, die schon englisch dastehen. Kein Uebersetzungsfall —
       aber ein Befund: eine deutsche API antwortet dort englisch."""
    baum = ast.parse(quelle)
    schon = _in_t_aufruf(baum)
    raus = set()
    for n in ast.walk(baum):
        werte = []
        if isinstance(n, ast.Call):
            werte = [kw.value for kw in n.keywords if kw.arg in SENKE_KW]
        elif isinstance(n, ast.Dict):
            werte = [v for k, v in zip(n.keys, n.values)
                     if isinstance(k, ast.Constant) and k.value in SENKE_KW]
        for v in werte:
            if not (isinstance(v, ast.Constant) and isinstance(v.value, str)):
                continue
            if id(v) in schon:
                continue
            t = v.value.strip()
            if (len(t) >= 3 and _WORT.search(t)
                    and not re.fullmatch(r"[a-z0-9_.:/-]+", t)
                    and not _DEUTSCH.search(t)):
                raus.add(t)
    return raus


def _in_t_aufruf(baum):
    """Alle Konstanten, die schon erstes Argument eines t()/_t() sind."""
    drin = set()
    for n in ast.walk(baum):
        if not isinstance(n, ast.Call) or not n.args:
            continue
        f = n.func
        name = f.attr if isinstance(f, ast.Attribute) else (
            f.id if isinstance(f, ast.Name) else None)
        if name in ("t", "_t"):
            drin.add(id(n.args[0]))
    return drin


def _kandidaten(quelle):
    """[(zeile, spalte_von, spalte_bis, text)] — die Literale, die ein t() brauchen."""
    baum = ast.parse(quelle)
    schon = _in_t_aufruf(baum)
    raus = []
    for n in ast.walk(baum):
        werte = []
        if isinstance(n, ast.Call):
            werte = [kw.value for kw in n.keywords if kw.arg in SENKE_KW]
        elif isinstance(n, ast.Dict):
            werte = [v for k, v in zip(n.keys, n.values)
                     if isinstance(k, ast.Constant) and k.value in SENKE_KW]
        for v in werte:
            if not (isinstance(v, ast.Constant) and isinstance(v.value, str)):
                continue          # f-String oder Ausdruck: nicht unser Fall
            if id(v) in schon or not _ist_text(v.value):
                continue
            raus.append((v.lineno, v.col_offset, v.end_lineno, v.end_col_offset,
                         v.value))
    return raus


def _umschliessen(pfad, schreiben):
    quelle = io.open(pfad, encoding="utf-8").read()
    kand = _kandidaten(quelle)
    if not kand:
        return 0, 0, []
    zeilen = quelle.split("\n")
    mehrzeilig = [k for k in kand if k[0] != k[2]]
    einzeilig = [k for k in kand if k[0] == k[2]]

    # Von hinten nach vorn, damit die Spaltenpositionen gueltig bleiben.
    #
    # UEBER BYTES schneiden, nicht ueber Zeichen: `col_offset` im AST ist ein
    # UTF-8-BYTE-Offset. In einer Zeile mit Umlaut oder Gedankenstrich vor dem
    # Literal verrutscht ein Zeichen-Slice um genau die Zahl der Mehrbytes —
    # und schrieb hier prompt `), )400` statt `), 400`. Dass es sofort auffiel,
    # liegt nur am ast.parse() unten; ohne das haette es still kaputte
    # Blueprints geschrieben.
    for lz, cv, _lb, cb, _txt in sorted(einzeilig, reverse=True):
        b = zeilen[lz - 1].encode("utf-8")
        zeilen[lz - 1] = (b[:cv] + b"_t(" + b[cv:cb] + b")" + b[cb:]).decode("utf-8")
    neu = "\n".join(zeilen)

    if "_nc_i18n" not in quelle:
        # Import an die bestehende nc-Gruppe anhaengen, alphabetisch.
        m = list(re.finditer(r"^from nc import \w+ as _nc_\w+.*$", neu, re.M))
        zeile = "from nc import i18n as _nc_i18n"
        if m:
            neu = neu[:m[0].start()] + zeile + "\n" + neu[m[0].start():]
        else:
            m2 = re.search(r"^from flask import .*$", neu, re.M)
            assert m2, "kein Anker fuer den Import in %s" % pfad
            neu = neu[:m2.end()] + "\n\n" + zeile + neu[m2.end():]
    if re.search(r"^def _t\(", neu, re.M) is None:
        # Hinter die bp = Blueprint(...)-Zeile, wo auch _c() steht.
        m3 = re.search(r'^bp = Blueprint\(.*\)$', neu, re.M)
        assert m3, "kein Anker fuer den Helfer in %s" % pfad
        neu = neu[:m3.end()] + HELFER + neu[m3.end():]

    ast.parse(neu)      # nie kaputten Code schreiben
    if schreiben:
        io.open(pfad, "w", encoding="utf-8", newline="").write(neu)
    return len(einzeilig), len(mehrzeilig), [k[4] for k in mehrzeilig]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dateien", nargs="*")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    dateien = a.dateien or sorted(glob.glob(os.path.join(ROOT, "nc/routes/*.py")))
    ges_e = ges_m = 0
    offen = []
    for p in dateien:
        if p.endswith("__init__.py"):
            continue
        e, m, texte = _umschliessen(p, a.write)
        if e or m:
            print("  %-28s %3d umschlossen%s"
                  % (os.path.relpath(p, ROOT).replace("\\", "/"), e,
                     (" · %d mehrzeilig (Handarbeit)" % m) if m else ""))
            offen += [(os.path.relpath(p, ROOT), t) for t in texte]
        ges_e += e
        ges_m += m
    print("gesamt: %d %s, %d mehrzeilig"
          % (ges_e, "umschlossen" if a.write else "offen", ges_m))
    for datei, t in offen:
        print("   HAND  %s: %s" % (datei, t[:70]))

    # Der Nebenbefund: Stellen, an denen eine deutsche API englisch antwortet.
    # Kein Fehler und kein Uebersetzungsfall — aber sichtbar, statt in einer
    # Identitaets-Uebersetzung zu verschwinden, die wie geleistete Arbeit
    # aussaehe.
    eng = set()
    for p in dateien:
        if not p.endswith("__init__.py"):
            eng |= _englisch(io.open(p, encoding="utf-8").read())
    if eng:
        print("englisch im Quelltext (Formulierung, keine Uebersetzung): %d" % len(eng))
    if a.check and ges_e:
        print("Blueprints uebersetzen nicht alle Benutzertexte "
              "— `python3 tools/i18n_wrap.py --write` laufen lassen.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
