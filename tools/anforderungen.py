#!/usr/bin/env python3
"""anforderungen — requirements.txt gegen eine Python-Umgebung abgleichen (v4.2-W123).

    .venv/bin/python tools/anforderungen.py                  Bericht, Tabulator-getrennt
    .venv/bin/python tools/anforderungen.py --datei X.txt    andere Liste

Wird mit DEM Interpreter aufgerufen, dessen Umgebung geprueft werden soll —
tools/update.sh ruft es mit .venv/bin/python auf. Eine Zeile je Anforderung:

    ok|fehlt|alt|entfaellt <TAB> name <TAB> installiert <TAB> anforderung <TAB> pflicht|optional

WARUM NICHT `pip install -r requirements.txt` UND FERTIG: das ist der
Installationsweg, keine Auskunft. Er braucht das Netz schon fuer die Frage,
ob ueberhaupt etwas fehlt, und seine Ausgabe sagt nicht, WAS fehlte. update.sh
soll vorher sagen, was es tun wird, und danach, was es getan hat — ein
zweiter Lauf auf einem vollstaendigen Bestand darf nichts anfassen.

WARUM NICHT `pip check`: das prueft nur die Abhaengigkeiten installierter
Pakete untereinander. Ein Paket, das gar nicht installiert ist, meldet es nie.

Die Optional-Markierung steht in requirements.txt selbst (Kommentar mit
`[optional]`), nicht in einer zweiten Liste hier: zwei Listen fuer denselben
Zweck laufen auseinander (W98, W100).

Kein Fremdpaket: `packaging` kommt, wenn nicht installiert, aus pip selbst
(pip._vendor.packaging). Fehlt beides, bricht das Werkzeug mit Exitcode 2 ab
und sagt warum — es raet nicht "alles fehlt".
"""

import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPTIONAL_MARKE = "[optional]"


def _packaging():
    """(Requirement, InvalidRequirement) — aus packaging oder aus pip."""
    try:
        from packaging.requirements import InvalidRequirement, Requirement
        return Requirement, InvalidRequirement
    except ImportError:
        pass
    try:
        from pip._vendor.packaging.requirements import InvalidRequirement, Requirement
        return Requirement, InvalidRequirement
    except ImportError:
        return None, None


def normiert(name):
    """PEP 503: 'PyMySQL', 'pymysql' und 'py_mysql' sind dasselbe Paket."""
    return re.sub(r"[-_.]+", "-", name).lower()


def zeilen(pfad):
    """[(anforderungstext, optional)] aus einer requirements-Datei."""
    raus = []
    for roh in io.open(pfad, encoding="utf-8"):
        text, _, kommentar = roh.partition("#")
        text = text.strip()
        if not text or text.startswith("-"):
            continue
        raus.append((text, OPTIONAL_MARKE in kommentar))
    return raus


def installierte():
    """{normierter name: version} der laufenden Umgebung."""
    from importlib import metadata
    aus = {}
    for d in metadata.distributions():
        name = d.metadata.get("Name")
        if name:
            aus[normiert(name)] = d.version
    return aus


def abgleich(pfad, vorhanden=None):
    """[(status, name, installiert, anforderung, art)] — die eigentliche Arbeit.

    `vorhanden` ist fuer die Vertraege: {normierter name: version}. Ohne wird
    die laufende Umgebung gelesen.
    """
    Requirement, InvalidRequirement = _packaging()
    if Requirement is None:
        raise RuntimeError("weder 'packaging' noch pip in dieser Umgebung — "
                           "Abgleich nicht moeglich (python -m ensurepip)")
    if vorhanden is None:
        vorhanden = installierte()
    raus = []
    for text, optional in zeilen(pfad):
        art = "optional" if optional else "pflicht"
        try:
            req = Requirement(text)
        except InvalidRequirement as e:
            # Eine kaputte Zeile ist ein Befund, kein Ueberspringen — sonst
            # meldet der Abgleich "alles da" fuer eine Liste, die pip gar
            # nicht lesen koennte.
            raise RuntimeError("ungueltige Zeile in %s: %r (%s)" % (pfad, text, e)) from e
        if req.marker is not None and not req.marker.evaluate():
            raus.append(("entfaellt", req.name, "-", str(req.specifier) or "*", art))
            continue
        ist = vorhanden.get(normiert(req.name))
        if ist is None:
            status = "fehlt"
        elif req.specifier and not req.specifier.contains(ist, prereleases=True):
            status = "alt"
        else:
            status = "ok"
        raus.append((status, req.name, ist or "-", str(req.specifier) or "*", art))
    return raus


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datei", default=os.path.join(ROOT, "requirements.txt"))
    a = ap.parse_args(argv)
    try:
        for zeile in abgleich(a.datei):
            print("\t".join(zeile))
    except (OSError, RuntimeError) as e:
        print("anforderungen: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
