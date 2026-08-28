#!/usr/bin/env python3
"""route_inventory — die Routentabelle vor und nach einer Welle vergleichen.

Warum das existiert: der Pflichtbeleg jeder Blueprint-Welle ist, dass kein
Pfad verschwindet (docs/MODULARISIERUNG.md, Abschnitt 4 Schritt 7). Eine
Zaehlung reicht dafuer nicht — es muss Pfad UND methods sein, sonst faellt eine
Route weg und eine andere kommt hinzu, ohne dass die Zahl sich ruehrt.

    python3 tools/route_inventory.py            > vorher.txt
    ... Welle ...
    python3 tools/route_inventory.py --diff vorher.txt
"""
import argparse
import ast
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _routes(pfad):
    """(pfad, methods) je Dekorator in einer Datei. Liest per ast, nie per Regex —
       ein Regex haelt @app.route in einem Docstring fuer eine Route."""
    try:
        baum = ast.parse(open(pfad, encoding="utf-8").read())
    except SyntaxError as e:
        print(f"SYNTAXFEHLER {pfad}: {e}", file=sys.stderr)
        return []
    raus = []
    for knoten in ast.walk(baum):
        if not isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dek in knoten.decorator_list:
            if not isinstance(dek, ast.Call):
                continue
            name = ast.unparse(dek.func)
            if not name.endswith(".route"):
                continue
            if not dek.args or not isinstance(dek.args[0], ast.Constant):
                continue
            weg = dek.args[0].value
            meth = ["GET"]
            for kw in dek.keywords:
                if kw.arg == "methods":
                    try:
                        meth = sorted(ast.literal_eval(kw.value))
                    except Exception:
                        meth = ["?"]
            raus.append(f"{weg} [{','.join(meth)}]")
    return raus


def sammeln():
    dateien = [os.path.join(ROOT, "bot.py")] + sorted(
        glob.glob(os.path.join(ROOT, "nc", "routes", "*.py")))
    alle = []
    for d in dateien:
        alle += _routes(d)
    return sorted(alle)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--diff", help="Datei mit der Tabelle von vorher")
    a = p.parse_args()
    jetzt = sammeln()
    if not a.diff:
        for z in jetzt:
            print(z)
        print(f"# {len(jetzt)} Regeln", file=sys.stderr)
        return 0
    vorher = [z.rstrip("\n") for z in open(a.diff, encoding="utf-8")
              if z.strip() and not z.startswith("#")]
    weg = sorted(set(vorher) - set(jetzt))
    neu = sorted(set(jetzt) - set(vorher))
    print(f"vorher {len(vorher)} · jetzt {len(jetzt)}")
    for z in weg:
        print("  VERLOREN", z)
    for z in neu:
        print("  NEU     ", z)
    if len(vorher) != len(jetzt) or weg or neu:
        print("ABBRUCHGRUND: Routentabelle nicht identisch")
        return 1
    print("Routentabelle identisch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
