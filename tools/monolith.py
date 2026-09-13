#!/usr/bin/env python3
"""tools/monolith.py — v4.2-W70: wie gross sind die Funktionen wirklich?

Der Plan dieser Reihe sagte: „Monolith zerlegen — RestreamManager (1463),
handle_recording_finished (615), KickModerator (593)." Nachgemessen zeigt
sich, dass das auf die falsche Arbeit zeigt, und zwar doppelt.

**Erstens: in den drei Genannten ist fast nichts mehr zu holen.** Was sich
sauber herausloesen liess, IST laengst heraus — bot.py ruft 674-mal in nc/
hinein. Was bleibt, ist Orchestrierung mit Zustand:

    RestreamManager             77 fremde Globals, 3 reine Methoden (47 Z)
    KickModerator               70 fremde Globals, 1 reine Methode  (6 Z)
    handle_recording_finished   58 fremde Globals, 0 reine Methoden

Die Entscheidungslogik der Moderation zum Beispiel steht schon seit B165 und
W14/W19 in nc/modheuristics.py; in bot.py blieb der Zustand und das Lesen der
Konfiguration. Diese drei nach nc/ zu schieben hiesse, 45 bis 77 Namen per
configure() hineinzureichen — das waere kein Zerlegen, sondern ein riesiges
Parameterobjekt, und es faende an der heikelsten Stelle des Bestands statt.

**Zweitens: die groesste Funktion des Bestands steht gar nicht in bot.py.**

    1730 Z  discordbot.py  _discord_run_once
     718 Z  nc/schema.py   create_schema
     616 Z  bot.py         handle_recording_finished

discordbot.py wurde in v4.2-W15 AUS bot.py herausgeloest, genau gegen dieses
Problem. Die Masse ist dabei umgezogen, nicht kleiner geworden. Ein Mass, das
nur bot.py anschaut, haette das nie gesehen und die Verlagerung als Erfolg
verbucht — deshalb misst dieses Werkzeug den ganzen Produktionscode.

GEZAEHLT WIRD DIE ANZAHL, NICHT DIE LAENGE. Eine Sperre, die jede zusaetzliche
Zeile in einer grossen Funktion meldet, faellt bei jeder normalen Fehlerbehebung
— und wird binnen einer Woche abgeschaltet. Interessant ist etwas anderes: dass
keine NEUE Riesenfunktion entsteht und keine bestehende in die naechste Stufe
rutscht. Dieselbe Ueberlegung wie bei den stillen except-Bloecken in W65.

    python3 tools/monolith.py             Bericht
    python3 tools/monolith.py --sperre    keine neue Riesenfunktion (CI)
    python3 tools/monolith.py --neu-grundlinie
"""

import argparse
import ast
import io
import json
import os
import pathlib
import sys

# v4.2-W83: gemeinsamer Parser. tools/ ist sys.path[0], wenn dieses Werkzeug
# als `python tools/monolith.py` laeuft — genau so steht es in der Pruefkette.
import quelle

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUNDLINIE = os.path.join(WURZEL, ".claude", "monolith_grundlinie.json")
STUFEN = (100, 200, 300, 500)

# v4.2-W74: Zeilen allein zeigen aufs falsche Ziel. nc/schema.py:create_schema
# ist mit 718 Zeilen die laengste Funktion des Bestands — und hat 18
# Verzweigungen, also EINE je 40 Zeilen. Jede andere Riesenfunktion hat eine
# je 3 bis 5:
#
#     718 Z   18 Zweige   40.0 Z/Zw   nc/schema.py:create_schema
#     716 Z  204 Zweige    3.5 Z/Zw   discordbot.py:_discord_run_once
#     616 Z  141 Zweige    4.4 Z/Zw   bot.py:handle_recording_finished
#
# create_schema ist eine Liste aus 42 CREATE TABLE, kein Geflecht: 82 der 88
# Anweisungen sind ein schlichtes conn.execute(...). Sie zu zerlegen waere
# Kosmetik und wuerde an Schema-Code stattfinden, der gegen die
# Produktionsdatenbank laeuft. Deshalb zaehlt dieses Werkzeug jetzt BEIDES.
ZWEIG_STUFEN = (50, 100, 150)

# Was als Verzweigung zaehlt: alles, was den Leser zwingt, sich einen zweiten
# Fall zu merken. Bewusst inklusive `with` und Komprehensionen — auch die
# tragen Zustand, den man beim Lesen mitfuehrt.
_VERZWEIGT = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try,
              ast.ExceptHandler, ast.With, ast.AsyncWith, ast.BoolOp,
              ast.IfExp, ast.comprehension, ast.Assert)


def zweige(knoten) -> int:
    """Wie viele Verzweigungen stecken in dieser Funktion? -> int"""
    return sum(1 for n in ast.walk(knoten) if isinstance(n, _VERZWEIGT))


def _dateien():
    aus = ["bot.py", "discordbot.py", "telegramversand.py", "brain_bridge.py"]
    for muster in ("nc/**/*.py", "brain/**/*.py"):
        aus += [str(p.relative_to(WURZEL)).replace(os.sep, "/")
                for p in sorted(pathlib.Path(WURZEL).glob(muster))
                if "_vendor" not in str(p)]
    return [d for d in aus
            if os.path.isfile(os.path.join(WURZEL, d))
            and not os.path.basename(d).startswith("test_")]


def funktionen():
    """-> [(datei, name, zeile, laenge)] fuer den ganzen Produktionscode.

    v4.2-W83: parst ueber tools/quelle.py und bricht ab, statt eine
    unlesbare Datei zu ueberspringen. Vorher stand hier
    `except (OSError, SyntaxError): continue` — und weil bot.py rund die
    Haelfte des Produktionscodes ist, meldete dieses Werkzeug auf einem
    Interpreter unter 3.12 "22 Funktionen ueber 100 Zeilen" statt 63 und
    liess die Sperre gruen durchlaufen.
    """
    aus = []
    dateien = _dateien()
    fehlt = quelle.pflicht_erfuellt(dateien)
    if fehlt:
        raise quelle.QuelleUnlesbar(
            "Diese Dateien gehoeren in die Messung, stehen aber nicht in der "
            "Liste: " + ", ".join(fehlt) + "\n  Ohne sie ist die Zahl unten "
            "wertlos — bot.py allein ist rund die Haelfte des Bestands.")
    for d, baum in quelle.baeume(dateien):

        # datei als Vorgabewert gebunden, nicht aus der Schleife gelesen:
        # ruff B023. Hier harmlos, weil sofort aufgerufen — aber genau diese
        # Sorte Bindung ist spaeter der Fehler, den niemand findet.
        def geh(knoten, datei=d, praefix=""):
            for n in knoten.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    aus.append((datei, praefix + n.name, n.lineno,
                                n.end_lineno - n.lineno + 1, zweige(n)))
                elif isinstance(n, ast.ClassDef):
                    geh(n, datei, n.name + ".")

        geh(baum)
    return aus


def bericht():
    """-> {stufe: anzahl} ueber BEIDE Achsen.

    Zeilen als "100" … und Verzweigungen als "zw50" … — in einem Woerterbuch,
    damit die Sperre und die Grundlinie unveraendert damit umgehen koennen.
    """
    alle = funktionen()
    aus = {str(s): len([f for f in alle if f[3] > s]) for s in STUFEN}
    aus.update({"zw%d" % s: len([f for f in alle if f[4] > s])
                for s in ZWEIG_STUFEN})
    return aus


def _lade():
    try:
        return json.load(io.open(GRUNDLINIE, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true")
    p.add_argument("--neu-grundlinie", action="store_true")
    a = p.parse_args(argv)

    zahlen = bericht()

    if a.neu_grundlinie:
        os.makedirs(os.path.dirname(GRUNDLINIE), exist_ok=True)
        io.open(GRUNDLINIE, "w", encoding="utf-8").write(
            json.dumps({"stufen": zahlen}, ensure_ascii=False, indent=2) + "\n")
        print("Grundlinie eingefroren: "
              + ", ".join("%s %s: %d" % (s.removeprefix("zw"),
                                         "Zw" if s.startswith("zw") else "Z", n)
                          for s, n in zahlen.items()))
        return 0

    if a.sperre:
        basis = _lade()
        if basis is None:
            print("monolith: KEINE GRUNDLINIE — einmal --neu-grundlinie laufen "
                  "lassen und die Datei mit einchecken.")
            return 1
        alt = basis.get("stufen", {})
        gewachsen = [(s, alt.get(s, 0), n) for s, n in zahlen.items()
                     if n > alt.get(s, 0)]
        if gewachsen:
            print("monolith: NEUE Riesenfunktion. Entweder ist eine "
                  "dazugekommen, oder eine bestehende ist in die naechste "
                  "Stufe gerutscht.")
            for s, war, ist in gewachsen:
                einheit = ("Verzweigungen" if s.startswith("zw") else "Zeilen")
                print(f"  ueber {s.removeprefix('zw')} {einheit}: {war} -> {ist}")
            print("\n  Abhilfe: die Funktion in benannte Schritte zerlegen. "
                  "Sie in eine andere Datei zu verschieben hilft NICHT — "
                  "gemessen wird der ganze Produktionscode, genau weil "
                  "discordbot.py die Masse aus bot.py uebernommen hat, ohne "
                  "sie kleiner zu machen.")
            return 1
        print("monolith: OK — "
              + ", ".join("%s %s: %d" % (s.removeprefix("zw"),
                                         "Zw" if s.startswith("zw") else "Z", n)
                          for s, n in zahlen.items())
              + " — keine neue")
        return 0

    alle = funktionen()
    print("Funktionen im Produktionscode: %d" % len(alle))
    for s in STUFEN:
        print(f"  ueber {s:3d} Zeilen:       {zahlen[str(s)]}")
    for s in ZWEIG_STUFEN:
        print(f"  ueber {s:3d} Verzweigungen: {zahlen['zw%d' % s]}")
    print("\nNach VERZWEIGUNGEN — das ist die Liste, die zaehlt:")
    print(f"  {'Zeilen':>6} {'Zweige':>6} {'Z/Zw':>5}  Funktion")
    for d, nm, z, n, v in sorted(alle, key=lambda f: -f[4])[:12]:
        print(f"  {n:6d} {v:6d} {n / v if v else 0:5.1f}  {d}:{z}  {nm}")
    print("\nNach ZEILEN — lang heisst nicht schwer:")
    print(f"  {'Zeilen':>6} {'Zweige':>6} {'Z/Zw':>5}  Funktion")
    for d, nm, z, n, v in sorted(alle, key=lambda f: -f[3])[:8]:
        print(f"  {n:6d} {v:6d} {n / v if v else 0:5.1f}  {d}:{z}  {nm}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except quelle.QuelleUnlesbar as e:
        # Exit 2, nicht 1: "ich konnte nicht nachsehen" ist etwas anderes als
        # "der Bestand ist gewachsen". Beides rot, nur eines im Code behebbar.
        sys.exit(quelle.abbruch(e))
    except BrokenPipeError:
        os._exit(0)
