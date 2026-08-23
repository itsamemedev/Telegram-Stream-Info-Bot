#!/usr/bin/env python3
"""bp_extract — eine Routengruppe aus bot_v37 in ein Blueprint heben.

Macht den mechanischen Teil von Welle 3 (docs/MODULARISIERUNG.md): Routen und
die Helfer, die nur sie benutzen, verbatim herausschneiden, die Aufrufe auf ihre
neuen Herkünfte umschreiben, das Modul schreiben und den Monolithen kürzen.

Was es NICHT macht und bewusst dir überlässt: die Verdrahtung im Bot
(nc.ctx.configure + register_blueprint), die Vertragswanderung und die
Prüfkette. Das sind Entscheidungen, keine Mechanik — es druckt dafür am Ende
eine Checkliste mit den konkreten Namen.

    python3 tools/bp_extract.py /api/insights insights            # Trockenlauf
    python3 tools/bp_extract.py /api/insights insights --apply

**Namen werden über tokenize ersetzt, nie über Regex.** Beim ersten Anlauf von
W107 traf eine Regex-Ersetzung auch INNERHALB einer Zeichenkette: aus
"ARCHIVE_DIR nicht konfiguriert" wurde '_c().cfg["ARCHIVE_DIR"] nicht
konfiguriert', und die Datei war syntaktisch kaputt. Der Tokenizer unterscheidet
Namen von Strings und Kommentaren; ein Regex kann das nicht.
"""

import argparse
import ast
import io
import os
import re
import sys
import token as T
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOT = os.path.join(ROOT, "bot_v37.py")

# Namen, die in jedem Blueprint gleich aufgelöst werden. Alles andere muss der
# Aufrufer über --ctx / --cfg angeben, damit nichts still im Kontext landet.
FESTE_IMPORTE = {
    "db_conn": "from nc.dbwrap import db_conn",
    "_parse_iso": "from nc.textmore import _parse_iso",
    "_nc_envnum": "from nc import envnum as _nc_envnum",
}
FLASK_NAMEN = {"jsonify", "request", "Response", "abort", "send_file"}
STDLIB = {"os", "re", "json", "time", "shutil", "asyncio", "subprocess", "signal"}
DATETIME = {"datetime", "timedelta", "timezone"}


def _paths(node):
    out = []
    for d in node.decorator_list:
        m = re.search(r"route\('([^']+)'", ast.unparse(d))
        if m:
            out.append(m.group(1))
    return out


def _span(node):
    return min([d.lineno for d in node.decorator_list] + [node.lineno]), node.end_lineno


def rewrite_names(src, mapping):
    """Ersetzt freie NAMEN nach mapping. Strings, Kommentare und Attributzugriffe
       (x.NAME) bleiben unangetastet — genau daran scheitert eine Regex."""
    lines = src.splitlines(keepends=True)
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    edits = []
    for i, tk in enumerate(toks):
        if tk.type != T.NAME or tk.string not in mapping:
            continue
        if i > 0 and toks[i - 1].type == T.OP and toks[i - 1].string == ".":
            continue                       # Attributzugriff, nicht unser Name
        if i > 0 and toks[i - 1].type == T.NAME and toks[i - 1].string in ("def", "class"):
            continue                       # eigene Definition
        if tk.start[0] != tk.end[0]:
            continue
        edits.append((tk.start, tk.end, mapping[tk.string]))
    for (sr, sc), (_er, ec), rep in reversed(edits):
        ln = lines[sr - 1]
        lines[sr - 1] = ln[:sc] + rep + ln[ec:]
    return "".join(lines)


def sammle(prefix):
    """prefix darf mehrere kommagetrennte Praefixe enthalten.

    Warum: manche Themen verteilen sich auf mehrere URL-Praefixe
    (/api/health-score und /api/system-resources sind beide Systemzustand).
    Fuer jedes ein eigenes Ein-Routen-Modul waere Zersplitterung — ein Modul
    ist ein THEMA, nicht ein Praefix.
    """
    prefixe = [x.strip() for x in prefix.split(",") if x.strip()]
    src = io.open(BOT, encoding="utf-8").read()
    tree = ast.parse(src)
    routes = [n for n in tree.body
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
              and any(p == pre or p.startswith(pre + "/")
                      for p in _paths(n) for pre in prefixe)]
    if not routes:
        raise SystemExit(f"keine Routen unter {prefix}")
    namen = {n.name for n in routes}

    # Helfer, die AUSSER diesen Routen niemand aufruft, ziehen mit um.
    aufrufe = set()
    for n in routes:
        aufrufe |= {x.func.id for x in ast.walk(n)
                    if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)}
    top = {n.name: n for n in tree.body
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    extern = set()
    for n in tree.body:
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) or n.name in namen:
            continue
        called = {x.func.id for x in ast.walk(n)
                  if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)}
        extern |= (aufrufe & called)
    movers = [top[h] for h in sorted(aufrufe & set(top)) if h not in extern and h not in namen]
    return src, tree, routes, movers


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix", help="z.B. /api/insights; mehrere mit Komma trennen, "
                                   "wenn sie thematisch EIN Modul ergeben")
    ap.add_argument("modul", help="Dateiname ohne .py, z.B. insights")
    ap.add_argument("--ctx", default="", help="Bot-Namen, die ueber nc.ctx kommen: alt=neu,alt=neu")
    ap.add_argument("--cfg", default="", help="Namen, die aus ctx.cfg kommen: NAME,NAME")
    ap.add_argument("--imports", default="", help="zusaetzliche Importzeilen, mit ; getrennt")
    ap.add_argument("--apply", action="store_true", help="wirklich schreiben")
    a = ap.parse_args()

    src, tree, routes, movers = sammle(a.prefix)
    lines = src.splitlines(keepends=True)
    stuecke = sorted([(*_span(n), n.name, "route") for n in routes]
                     + [(*_span(n), n.name, "helfer") for n in movers])
    gesamt = sum(e - s + 1 for s, e, _, _ in stuecke)

    print(f"\n=== {a.prefix} -> nc/routes/{a.modul}.py ===")
    print(f"{len(routes)} Routen, {len(movers)} mitgezogene Helfer, {gesamt} Zeilen")
    for s, e, n, art in stuecke:
        print(f"   {art:<7} {n:<40} {s}-{e}")

    ctxmap = {}
    for paar in filter(None, a.ctx.split(",")):
        alt, neu = paar.split("=")
        ctxmap[alt] = f"_c().{neu}"
    for k in filter(None, a.cfg.split(",")):
        ctxmap[k] = f'_c().cfg["{k}"]'

    koerper = "\n\n\n".join("".join(lines[s - 1:e]).rstrip()
                            for s, e, _, art in stuecke if art == "helfer")
    rt = "\n\n\n".join("".join(lines[s - 1:e]).rstrip()
                       for s, e, _, art in stuecke if art == "route")
    body = ((koerper + "\n\n\n" if koerper else "") + rt)
    body = rewrite_names(body, ctxmap).replace("@dashboard_app.route(", "@bp.route(")

    # Welche freien Namen bleiben uebrig? Die muessen importiert werden.
    import builtins
    offen = set()
    probe = ast.parse(body)
    lokal = set()
    for n in ast.walk(probe):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            lokal.add(n.id)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lokal.add(n.name)
            lokal |= {x.arg for x in n.args.args + n.args.kwonlyargs}
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for x in n.names:
                lokal.add((x.asname or x.name).split(".")[0])
        # 'except Exception as e' bindet e ebenfalls lokal — ohne das meldet der
        # Extraktor jede gefangene Ausnahme als unaufgeloesten Namen.
        if isinstance(n, ast.ExceptHandler) and n.name:
            lokal.add(n.name)
        if isinstance(n, ast.Lambda):
            lokal |= {x.arg for x in n.args.args + n.args.kwonlyargs}
        if isinstance(n, (ast.comprehension,)):
            for t in ast.walk(n.target):
                if isinstance(t, ast.Name):
                    lokal.add(t.id)
    for n in ast.walk(probe):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            if n.id not in lokal and n.id not in dir(builtins):
                offen.add(n.id)

    imp = ["from flask import Blueprint" + (", " + ", ".join(sorted(offen & FLASK_NAMEN))
                                            if offen & FLASK_NAMEN else "")]
    if offen & STDLIB:
        imp = [f"import {m}" for m in sorted(offen & STDLIB)] + imp
    if offen & DATETIME:
        imp.insert(0, "from datetime import " + ", ".join(sorted(offen & DATETIME)))
    for n in sorted(offen):
        if n in FESTE_IMPORTE:
            imp.append(FESTE_IMPORTE[n])
    zusatz = [z.strip() for z in a.imports.split(";") if z.strip()]
    imp += zusatz
    # Was --imports selbst bindet, gilt als aufgeloest. Ohne das meldete das
    # Werkzeug genau die Namen als offen, die der Aufrufer gerade nachgereicht
    # hat, und brach mit --apply ab.
    gebunden = set()
    for zeile in zusatz:
        try:
            for n in ast.walk(ast.parse(zeile)):
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    for al in n.names:
                        gebunden.add((al.asname or al.name).split(".")[0])
        except SyntaxError:
            print(f"⚠ --imports nicht parsebar, ignoriert: {zeile!r}")
    rest = sorted(offen - FLASK_NAMEN - STDLIB - DATETIME - set(FESTE_IMPORTE)
                  - gebunden - {"bp", "_c", "log", "_ctx"})

    kopf = f'''"""nc.routes.{a.modul} — die Routen unter {a.prefix} als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot_v37.
"""

{chr(10).join(dict.fromkeys(imp))}

from nc import ctx as _ctx

bp = Blueprint("{a.modul}", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


'''
    ziel = os.path.join(ROOT, "nc", "routes", a.modul + ".py")
    if rest:
        print(f"\n⚠ NICHT aufgeloest — als --ctx/--cfg/--imports nachreichen: {rest}")
    if not a.apply:
        print("\nTrockenlauf. Mit --apply schreiben.")
        return 0
    if rest:
        print("\nAbbruch: erst die offenen Namen aufloesen.")
        return 1

    io.open(ziel, "w", encoding="utf-8").write(kopf + body + "\n")
    for s, e, _, _ in sorted(stuecke, reverse=True):
        del lines[s - 1:e]
    io.open(BOT, "w", encoding="utf-8").write("".join(lines))
    print(f"\ngeschrieben: nc/routes/{a.modul}.py")
    print(f"bot_v37.py gekuerzt um {gesamt} Zeilen")
    print(f"""
NOCH ZU TUN (Mechanik ist durch, Entscheidungen nicht):
  1. Import + Registrierung in bot_v37.py:
         from nc.routes import {a.modul} as _nc_routes_{a.modul}
         dashboard_app.register_blueprint(_nc_routes_{a.modul}.bp)
     HINTER die letzte injizierte Definition, sonst 'undefined name'.
  2. nc.ctx.configure(...) um die neuen Eintraege erweitern.
  3. pyflakes bot_v37.py — tote Importe entfernen, die nur die Routen brauchten.
  4. Routentabelle gegen die Basislinie vergleichen (346 Regeln, keine verloren).
  5. Gebrochene Vertragsanker migrieren, KEINEN loeschen.
  6. ncpatch map + volle Pruefkette inklusive test_smoke.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
