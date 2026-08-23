#!/usr/bin/env python3
"""bp_analyse — was kostet es, eine Routengruppe als Blueprint herauszulösen?

Warum es das gibt: Welle 3 der Zerlegung (docs/MODULARISIERUNG.md) sind rund
dreizehn Blueprints. Welches als nächstes dran ist, soll nicht Bauchgefühl
entscheiden, sondern die Kopplung — und die ist messbar. Das Werkzeug beantwortet
für jede Gruppe drei Fragen:

  1. Wie viele Zeilen und Routen bringt sie?
  2. Welche Bot-Helfer benutzt NUR sie (die ziehen mit um und sind Gewinn)?
  3. Welche Helfer und Globals braucht sie darüber hinaus (die müssen in
     nc/ctx.py — und der Kontext soll klein bleiben)?

Die Kennzahl unten ist "Zeilen je ctx-Eintrag": wie viel Monolith man los wird
pro Stück neuer Kopplung. Hoch ist gut.

    python3 tools/bp_analyse.py                 # alle Gruppen, nach Kosten sortiert
    python3 tools/bp_analyse.py /api/archive    # eine Gruppe im Detail

Es ändert nichts. Reine Analyse.
"""

import ast
import builtins
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOT = os.path.join(ROOT, "bot_v37.py")
BUILTINS = set(dir(builtins))

# Was schon aus dem Monolithen heraus ist, taucht nicht mehr auf — die Datei
# ist die einzige Quelle. Blueprints in nc/routes/ werden bewusst NICHT
# mitgezaehlt: gefragt ist, was noch drin steckt.


def _load():
    src = io.open(BOT, encoding="utf-8").read()
    tree = ast.parse(src)
    topfn = {n.name for n in tree.body
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    glob = set()
    for n in tree.body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                if isinstance(t, ast.Name):
                    glob.add(t.id)
    imported = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            for a in n.names:
                imported[a.asname or a.name] = f"from {n.module} import {a.name}"
        elif isinstance(n, ast.Import):
            for a in n.names:
                imported[(a.asname or a.name).split(".")[0]] = f"import {a.name}"
    return src, tree, topfn, glob, imported


def _paths(node):
    out = []
    for d in node.decorator_list:
        m = re.search(r"route\('([^']+)'", ast.unparse(d))
        if m:
            out.append(m.group(1))
    return out


def _span(node):
    start = min([d.lineno for d in node.decorator_list] + [node.lineno])
    return start, node.end_lineno


def _deps(node, topfn, glob, imported):
    """Fremdbezuege einer Funktion, getrennt nach Herkunft."""
    local = {a.arg for a in node.args.args + node.args.kwonlyargs + node.args.posonlyargs}
    if node.args.vararg:
        local.add(node.args.vararg.arg)
    if node.args.kwarg:
        local.add(node.args.kwarg.arg)
    for x in ast.walk(node):
        if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store):
            local.add(x.id)
        if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x is not node:
            local.add(x.name)
        if isinstance(x, (ast.Import, ast.ImportFrom)):
            for a in x.names:
                local.add((a.asname or a.name).split(".")[0])
    fns, gls, imps = set(), set(), set()
    dyn = False
    for x in ast.walk(node):
        # globals().get("...") umgeht jede Namensanalyse — das MUSS auffallen,
        # sonst verschiebt man eine Funktion, deren Abhaengigkeit unsichtbar ist.
        if isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == "globals":
            dyn = True
        if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
            i = x.id
            if i in local or i in BUILTINS:
                continue
            if i in topfn:
                fns.add(i)
            elif i in imported:
                imps.add(i)
            elif i in glob and i != "dashboard_app":
                gls.add(i)
    return fns, gls, imps, dyn


def analyse(prefix, tree, topfn, glob, imported):
    sel = [n for n in tree.body
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
           and any(p == prefix or p.startswith(prefix + "/") for p in _paths(n))]
    if not sel:
        return None
    names = {n.name for n in sel}
    lines = sum(_span(n)[1] - _span(n)[0] + 1 for n in sel)

    F, G, I, dyn = set(), set(), set(), []
    for n in sel:
        f, g, i, d = _deps(n, topfn, glob, imported)
        F |= f
        G |= g
        I |= i
        if d:
            dyn.append(n.name)

    # Ein Helfer zieht nur dann mit um, wenn ihn sonst NIEMAND benutzt.
    extern = {}
    for n in tree.body:
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) or n.name in names:
            continue
        called = {x.func.id for x in ast.walk(n)
                  if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)}
        for f in F & called:
            extern.setdefault(f, []).append(n.name)
    mit = sorted(f for f in F if f not in extern)
    zuctx = sorted(f for f in F if f in extern)

    # Mitgezogene Helfer bringen eigene Zeilen — und eigene Abhaengigkeiten.
    body = {n.name: n for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    mitlines = 0
    for h in mit:
        if h in body:
            s, e = _span(body[h])
            mitlines += e - s + 1
            hf, hg, _, hd = _deps(body[h], topfn, glob, imported)
            G |= hg
            for x in hf:
                if x not in names and x not in mit:
                    zuctx.append(x)
            if hd:
                dyn.append(h)
    zuctx = sorted(set(zuctx))

    # Reine Delegationen sind KEINE echte Kopplung: wenn die Bot-Funktion nur
    # "return _nc_x.y(...)" macht, kann das Blueprint direkt aus nc.x
    # importieren und braucht dafuer keinen Kontext-Eintrag. Ohne diese
    # Unterscheidung meldet das Werkzeug Kosten, die es gar nicht gibt — genau
    # so sah /api/ai nach der W111-Vorarbeit unveraendert teuer aus.
    body_all = {n.name: n for n in tree.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    direkt = {}
    for f in list(zuctx):
        n = body_all.get(f)
        if not n:
            continue
        koerper = [x for x in n.body if not (isinstance(x, ast.Expr)
                                             and isinstance(x.value, ast.Constant))]
        if len(koerper) != 1 or not isinstance(koerper[0], ast.Return):
            continue
        val = koerper[0].value
        if not (isinstance(val, ast.Call) and isinstance(val.func, ast.Attribute)
                and isinstance(val.func.value, ast.Name)):
            continue
        # REINE Weitergabe heisst: jedes Argument ist unveraendert ein Parameter
        # der Huelle. Sonst tut die Huelle mehr, als sie zugibt, und ein
        # Direktimport bekaeme die falsche Signatur — _arg_int liest zusaetzlich
        # request.args.get(name) und war genau so ein Fehlalarm.
        params = {a.arg for a in n.args.args + n.args.kwonlyargs}
        rein = all(isinstance(x, ast.Name) and x.id in params for x in val.args) and \
            all(isinstance(k.value, ast.Name) and k.value.id in params
                for k in val.keywords)
        if rein:
            imp = imported.get(val.func.value.id, "")
            # aus "from nc import cfgstore" / "import nc.claude" den Modulpfad
            # ziehen, damit die Ausgabe ein benutzbarer Import ist
            if imp.startswith("from "):
                teile = imp.split()
                ziel = f"{teile[1]}.{teile[3]}"
            elif imp.startswith("import "):
                ziel = imp.split()[1]
            else:
                ziel = val.func.value.id
            direkt[f] = f"{ziel}.{val.func.attr}"
            zuctx.remove(f)


    # Wer ruft die ROUTEN selbst intern auf? Das ist keine Kopplung ueber
    # Helfer und wurde deshalb frueher nicht gemeldet — in W110 hat es
    # zugeschlagen: /sysres und die Aggregat-Route rufen api_system_resources
    # bzw. api_health_score direkt auf. Nach dem Umzug fehlten sie im
    # Monolithen. Sie sind kein Hindernis (der Bot importiert sie aus dem
    # Blueprint), aber man muss es VORHER wissen.
    intern = {}
    for n in tree.body:
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) or n.name in names:
            continue
        called = {x.func.id for x in ast.walk(n)
                  if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)}
        called |= {x.id for x in ast.walk(n) if isinstance(x, ast.Name)}
        for r in names & called:
            intern.setdefault(r, []).append(n.name)

    kosten = len(zuctx) + len(G)
    return {"prefix": prefix, "routes": len(sel), "lines": lines,
            "mit": mit, "mitlines": mitlines, "ctx_fns": zuctx,
            "globals": sorted(G), "imports": sorted(I), "dyn": sorted(set(dyn)),
            "intern": intern, "direkt": direkt,
            "kosten": kosten,
            "ratio": round((lines + mitlines) / kosten, 1) if kosten else 999.0}


def main():
    src, tree, topfn, glob, imported = _load()
    prefixe = {}
    for n in tree.body:
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for p in _paths(n):
            teile = p.strip("/").split("/")
            key = "/" + "/".join(teile[:2]) if teile[0] == "api" and len(teile) > 1 else "/" + teile[0]
            prefixe[key] = True
            break

    if len(sys.argv) > 1:
        r = analyse(sys.argv[1], tree, topfn, glob, imported)
        if not r:
            print("keine Routen unter", sys.argv[1])
            return 1
        print(f"\n=== {r['prefix']} ===")
        print(f"{r['routes']} Routen, {r['lines']} Zeilen"
              f" (+ {r['mitlines']} Zeilen mitgezogene Helfer)")
        print(f"\nziehen mit ({len(r['mit'])}): {r['mit']}")
        print(f"\n-> nc/ctx.py, Funktionen ({len(r['ctx_fns'])}): {r['ctx_fns']}")
        if r["direkt"]:
            print(f"-> direkt importierbar, KEIN ctx noetig ({len(r['direkt'])}):")
            for k, v in sorted(r["direkt"].items()):
                print(f"     {k}  ->  {v}")
        print(f"-> nc/ctx.py, Globals ({len(r['globals'])}): {r['globals']}")
        print(f"\nDirektimporte aus nc/stdlib ({len(r['imports'])}): {r['imports']}")
        if r["intern"]:
            print("\n⚠ Routen, die der Bot INTERN aufruft — nach dem Umzug aus dem")
            print("  Blueprint importieren, sonst fehlen sie im Monolithen:")
            for k, v in sorted(r["intern"].items()):
                print(f"    {k}  <- {', '.join(sorted(set(v)))}")
        if r["dyn"]:
            print(f"\n⚠ globals()-Zugriff — Abhaengigkeit unsichtbar, HANDPRUEFUNG: {r['dyn']}")
        print(f"\nKosten {r['kosten']} ctx-Eintraege · "
              f"{r['ratio']} Zeilen je Eintrag")
        return 0

    rows = [analyse(p, tree, topfn, glob, imported) for p in sorted(prefixe)]
    rows = [r for r in rows if r and r["lines"] >= 40]
    rows.sort(key=lambda r: -r["ratio"])
    print(f"\n{'Praefix':<20}{'Rt':>4}{'Zeilen':>8}{'+Helfer':>9}"
          f"{'ctx-Fn':>8}{'ctx-Gl':>8}{'Zeilen/Eintrag':>16}  dyn")
    print("  " + "-" * 76)
    for r in rows:
        warn = "⚠" if r["dyn"] else ""
        print(f"  {r['prefix']:<18}{r['routes']:>4}{r['lines']:>8}{r['mitlines']:>9}"
              f"{len(r['ctx_fns']):>8}{len(r['globals']):>8}{r['ratio']:>16}  {warn}")
    print("\nHoch = viel Monolith los pro Stueck neuer Kopplung. Oben anfangen.")
    print("Detail:  python3 tools/bp_analyse.py <praefix>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
