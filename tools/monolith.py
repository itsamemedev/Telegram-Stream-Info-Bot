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

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUNDLINIE = os.path.join(WURZEL, ".claude", "monolith_grundlinie.json")
STUFEN = (100, 200, 300, 500)


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
    """-> [(datei, name, zeile, laenge)] fuer den ganzen Produktionscode."""
    aus = []
    for d in _dateien():
        try:
            baum = ast.parse(io.open(os.path.join(WURZEL, d),
                                     encoding="utf-8").read())
        except (OSError, SyntaxError):
            continue

        # datei als Vorgabewert gebunden, nicht aus der Schleife gelesen:
        # ruff B023. Hier harmlos, weil sofort aufgerufen — aber genau diese
        # Sorte Bindung ist spaeter der Fehler, den niemand findet.
        def geh(knoten, datei=d, praefix=""):
            for n in knoten.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    aus.append((datei, praefix + n.name, n.lineno,
                                n.end_lineno - n.lineno + 1))
                elif isinstance(n, ast.ClassDef):
                    geh(n, datei, n.name + ".")

        geh(baum)
    return aus


def bericht():
    """-> {stufe: anzahl} — wie viele Funktionen ueber jeder Stufe liegen."""
    alle = funktionen()
    return {str(s): len([f for f in alle if f[3] > s]) for s in STUFEN}


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
              + ", ".join(f"ueber {s}: {n}" for s, n in zahlen.items()))
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
                print(f"  ueber {s} Zeilen: {war} -> {ist}")
            print("\n  Abhilfe: die Funktion in benannte Schritte zerlegen. "
                  "Sie in eine andere Datei zu verschieben hilft NICHT — "
                  "gemessen wird der ganze Produktionscode, genau weil "
                  "discordbot.py die Masse aus bot.py uebernommen hat, ohne "
                  "sie kleiner zu machen.")
            return 1
        print("monolith: OK — "
              + ", ".join(f"ueber {s}: {n}" for s, n in zahlen.items())
              + ", keine neue")
        return 0

    alle = sorted(funktionen(), key=lambda f: -f[3])
    print("Funktionen im Produktionscode: %d" % len(alle))
    for s in STUFEN:
        print(f"  ueber {s:3d} Zeilen: {zahlen[str(s)]}")
    print("\nDie groessten:")
    for d, nm, z, n in alle[:15]:
        print(f"  {n:5d} Z  {d}:{z}  {nm}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os._exit(0)
