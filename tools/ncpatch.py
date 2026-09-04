#!/usr/bin/env python3
"""ncpatch — anker-basiertes Patchen des NIGHTCRAWLER-Monolithen.

WARUM: bot.py hat ~29.000 Zeilen / 1,4 MB. Die Datei in ein LLM-Kontext-
fenster zu laden kostet ~400k Token PRO Durchgang. Dieses Tool erlaubt
chirurgische Änderungen über eindeutige Textanker, ohne die Datei je
vollständig zu lesen oder zu schreiben.

Patch-Format: eine JSON-Datei mit einer Liste von Operationen.

  [
    {"file": "bot.py",
     "id":   "B120-discord-supervisor",
     "op":   "replace",              # replace | insert_after | insert_before | delete
     "anchor": "    try:\n        await client.start(DISCORD_BOT_TOKEN)\n",
     "new":    "    ...neuer Code...\n",
     "count":  1}                    # erwartete Trefferzahl (Default 1)
  ]

Garantien:
  * Anker MUSS exakt `count` mal vorkommen — sonst Abbruch OHNE Änderung.
  * Alles-oder-nichts: erst wenn ALLE Ops passen, wird geschrieben.
  * Automatische .bak-Sicherung + Validierung nach dem Schreiben.

Aufruf:
  python3 ncpatch.py apply  patches/w2_ai.json      [--root .]
  python3 ncpatch.py verify patches/w2_ai.json      [--root .]   # dry-run
  python3 ncpatch.py check                          [--root .]   # Validierung
  python3 ncpatch.py docs                           [--root .]   # Doku-Zahlen
  python3 ncpatch.py grep  "such-text" bot.py   [-C 3]       # Anker finden
  python3 ncpatch.py show  bot.py 24721 24760                # Zeilen zeigen
  python3 ncpatch.py sym   bot.py _discord_start             # Symbol-Zeilen
  python3 ncpatch.py map                                         # .claude/INDEX.md bauen
  python3 ncpatch.py find  "donations"                           # wo ist X? (aus der Karte)
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import tempfile
import re
import shutil
import subprocess
import sys

# ───────────────────────────────────────────────────────────── Hilfen


# v4.2-W2: die beiden Tag-Muster als benannte Konstanten — vorher standen sie
# woertlich an ihren Fundstellen, und der Vertrag musste sie aus dem Quelltext
# zurueckparsen. Ein Muster, das man testen will, gehoert an EINE Stelle.
#
# `\b` nach dem Namen: sonst passt auch `<scriptfoo`.
# `</script\s*>`: der Browser beendet das Element auch bei `</script >` und
# `</script\n>`. Ein Muster ohne das `\s*` haelt dort NICHT an und frisst den
# Rest der Datei — eine ID aus einem JS-String wurde dann als doppelte
# Markup-ID gemeldet, ein Fehlalarm, der das Werkzeug unglaubwuerdig macht.
RE_SCRIPT_WEG = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.S | re.I)
RE_SCRIPT_BLOCK = re.compile(r"<script\b([^>]*)>(.*?)</script\s*>", re.S | re.I)


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _write(path: str, text: str) -> None:
    tmp = path + ".ncpatch.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def _load_ops(patch_path: str) -> list:
    ops = json.loads(_read(patch_path))
    if isinstance(ops, dict):
        ops = ops.get("ops") or []
    return ops


# ───────────────────────────────────────────────────── Kern: apply/verify


def plan(ops: list, root: str) -> tuple[dict, list]:
    """Prüft alle Ops gegen die Dateien. Gibt (neue_inhalte, probleme)."""
    buffers: dict[str, str] = {}
    problems: list[str] = []

    for i, op in enumerate(ops):
        oid = op.get("id") or f"op#{i}"
        fname = op["file"]
        path = os.path.join(root, fname)
        if not os.path.exists(path):
            problems.append(f"[{oid}] Datei fehlt: {fname}")
            continue
        if fname not in buffers:
            buffers[fname] = _read(path)
        text = buffers[fname]

        anchor = op["anchor"]
        want = int(op.get("count", 1))
        got = text.count(anchor)
        if got != want:
            problems.append(
                f"[{oid}] Anker {got}x gefunden, erwartet {want}x "
                f"in {fname}. Anker-Anfang: {anchor[:70]!r}")
            continue

        kind = op.get("op", "replace")
        if kind == "replace":
            text = text.replace(anchor, op["new"], want)
        elif kind == "insert_after":
            text = text.replace(anchor, anchor + op["new"], want)
        elif kind == "insert_before":
            text = text.replace(anchor, op["new"] + anchor, want)
        elif kind == "delete":
            text = text.replace(anchor, "", want)
        else:
            problems.append(f"[{oid}] unbekannte op: {kind}")
            continue
        buffers[fname] = text

    return buffers, problems


def cmd_verify(args) -> int:
    ops = _load_ops(args.patch)
    _, problems = plan(ops, args.root)
    if problems:
        print("FEHLGESCHLAGEN — keine Datei angefasst:")
        for p in problems:
            print("  •", p)
        return 1
    print(f"OK — alle {len(ops)} Operationen passen sauber.")
    return 0


def cmd_apply(args) -> int:
    ops = _load_ops(args.patch)
    buffers, problems = plan(ops, args.root)
    if problems:
        print("ABBRUCH — keine Datei angefasst:")
        for p in problems:
            print("  •", p)
        return 1

    for fname, text in buffers.items():
        path = os.path.join(args.root, fname)
        bak = path + ".bak"
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        _write(path, text)
        print(f"geschrieben: {fname}  (Backup: {os.path.basename(bak)})")

    print(f"\n{len(ops)} Operationen angewendet. Validierung:")
    return validate(args.root, list(buffers))


# ───────────────────────────────────────────────────────── Validierung


def validate(root: str, files: list | None = None) -> int:
    """Die NIGHTCRAWLER-Pflichtprüfungen: py_compile, pyflakes, ruff,
    JS-Blöcke via node --check, CSS-Klammern, doppelte HTML-IDs."""
    files = files or [f for f in os.listdir(root) if f.endswith(".py")]
    pyfiles = [os.path.join(root, f) for f in files if f.endswith(".py")]
    rc = 0

    for f in pyfiles:
        r = subprocess.run([sys.executable, "-m", "py_compile", f],
                           capture_output=True, text=True)
        if r.returncode:
            print(f"  py_compile FEHLER {f}\n{r.stderr[:800]}")
            rc = 1
    if not rc:
        print("  py_compile: OK")

    for tool, extra in (("pyflakes", []),
                        ("ruff", ["check", "--select", "F,E9,B",
                                  "--ignore", "B905"])):
        r = subprocess.run([sys.executable, "-m", tool] + extra + pyfiles,
                           capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if tool == "ruff" and "All checks passed" in out:
            print("  ruff: OK")
            continue
        if out and "No module named" in out:
            print(f"  {tool}: nicht installiert — übersprungen")
            continue
        if out:
            print(f"  {tool}: BEFUNDE\n{out[:1500]}")
            rc = 1
        else:
            print(f"  {tool}: OK")

    # HTML: doppelte IDs, CSS-Klammerbilanz, JS-Syntax.
    #
    # website/ war hier frueher NICHT dabei — die oeffentliche Seite lief damit
    # durch keine einzige Pruefung, waehrend templates/ geprueft wurde. Beide
    # sind ausgeliefertes HTML, beide gehoeren geprueft.
    html_ok = True
    for sub in ("templates", "website"):
        tdir = os.path.join(root, sub)
        if not os.path.isdir(tdir):
            continue
        for name in sorted(os.listdir(tdir)):
            if not name.endswith(".html"):
                continue
            rel = f"{sub}/{name}"
            html = _read(os.path.join(tdir, name))

            # IDs nur im echten Markup zaehlen. Ohne das Strippen zaehlen
            # id="..." aus HTML-Kommentaren und aus JS-Strings mit, die Markup
            # bauen — beides erzeugt Fehlalarme statt Befunde.
            markup = re.sub(r"<!--.*?-->", "", html, flags=re.S)
            # v4.2-W2: `</script\s*>` statt `</script>`. Der Browser beendet
            # das Element auch bei `</script >` und `</script\n>`; ein Muster
            # ohne das \s* haelt an so einer Stelle NICHT an und frisst den
            # Rest der Datei — hier waeren dann alle folgenden IDs still
            # ungeprueft. Dasselbe gilt fuer den oeffnenden Tag: `<script`
            # muss an einer Tag-Grenze enden, sonst passt auch `<scriptfoo`.
            markup = RE_SCRIPT_WEG.sub("", markup)
            ids = re.findall(r'\bid="([^"]+)"', markup)
            dup = {x for x in ids if ids.count(x) > 1}
            if dup:
                print(f"  {rel}: DOPPELTE IDs -> {sorted(dup)[:10]}")
                rc = 1
                html_ok = False

            for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S):
                css = m.group(1)
                if css.count("{") != css.count("}"):
                    print(f"  {rel}: CSS-Klammern unbalanciert "
                          f"({css.count('{')} auf / {css.count('}')} zu)")
                    rc = 1
                    html_ok = False

            # JS/JSON-LD in den Bloecken. Die Hausregel verlangt node --check
            # von Hand; hier laeuft es automatisch mit, sonst wird es vergessen.
            # v4.2-W2: dieselbe Tag-Grenze wie oben. Ein `</script >` im
            # Deck haette hier zwei Bloecke zu einem verschmolzen — der
            # node --check waere dann an einer Datei gelaufen, die es so
            # nie gab, und haette entweder Unsinn gemeldet oder Echtes
            # uebersehen.
            for i, m in enumerate(RE_SCRIPT_BLOCK.finditer(html), 1):
                attrs, code = m.group(1), m.group(2)
                if "src=" in attrs or not code.strip():
                    continue
                if "json" in attrs.lower():
                    try:
                        json.loads(code)
                    except Exception as e:
                        print(f"  {rel}: Script #{i} ist kein gueltiges JSON — {e}")
                        rc = 1
                        html_ok = False
                    continue
                if not shutil.which("node"):
                    continue
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                                 encoding="utf-8") as fh:
                    fh.write(code)
                    tmp = fh.name
                try:
                    pr = subprocess.run(["node", "--check", tmp],
                                        capture_output=True, text=True)
                    if pr.returncode != 0:
                        first = (pr.stderr or "").strip().splitlines()
                        print(f"  {rel}: Script #{i} JS-SYNTAXFEHLER — "
                              f"{first[0] if first else '?'}")
                        rc = 1
                        html_ok = False
                finally:
                    os.unlink(tmp)
    if html_ok:
        node_note = "" if shutil.which("node") else ", JS uebersprungen (kein node)"
        print(f"  html: OK (IDs + CSS + JS in templates/ und website/{node_note})")
    return rc


def cmd_check(args) -> int:
    return validate(args.root)


# ─────────────────────────────────────────────────── Anker-Suche/Anzeige


def cmd_grep(args) -> int:
    path = os.path.join(args.root, args.file)
    lines = _read(path).splitlines()
    hits = 0
    for i, line in enumerate(lines, 1):
        if args.pattern in line:
            hits += 1
            lo, hi = max(1, i - args.context), min(len(lines), i + args.context)
            print(f"--- {args.file}:{i}")
            for j in range(lo, hi + 1):
                print(f"{j:>7}{'>' if j == i else ' '} {lines[j-1]}")
    print(f"\n{hits} Treffer.")
    return 0


def cmd_show(args) -> int:
    path = os.path.join(args.root, args.file)
    lines = _read(path).splitlines()
    for j in range(max(1, args.start), min(len(lines), args.end) + 1):
        print(f"{j:>7} {lines[j-1]}")
    return 0


def cmd_sym(args) -> int:
    """Zeilenbereich eines Top-Level-Symbols — statt die Datei zu scannen."""
    path = os.path.join(args.root, args.file)
    tree = ast.parse(_read(path))
    found = False
    for node in ast.walk(tree):
        if getattr(node, "name", None) == args.name and hasattr(node, "lineno"):
            print(f"{type(node).__name__} {args.name}: "
                  f"Z.{node.lineno}-{node.end_lineno} "
                  f"({node.end_lineno - node.lineno + 1} Zeilen)")
            found = True
    return 0 if found else 1


# ──────────────────────────────────────────────── Karte (map / find)
#
# WARUM: der teuerste Fehler an diesem Projekt ist, den Monolithen zu
# durchsuchen, um herauszufinden WO etwas steht. Jeder blinde Scan über
# bot.py kostet ein Vielfaches dessen, was der gesuchte Ausschnitt
# selbst kostet. `map` destilliert die Datei einmal in ein paar KB;
# `find` beantwortet daraus die Frage "wo ist X?" ohne die Datei
# überhaupt zu öffnen.


def _const(node):
    """Literal aus einem AST-Knoten, sonst None."""
    return node.value if isinstance(node, ast.Constant) else None


def _dec_name(dec) -> str:
    """Punktierter Name eines Dekorators, unabhängig von Call/Attribute."""
    d = dec.func if isinstance(dec, ast.Call) else dec
    parts = []
    while isinstance(d, ast.Attribute):
        parts.append(d.attr)
        d = d.value
    if isinstance(d, ast.Name):
        parts.append(d.id)
    return ".".join(reversed(parts))


def _kw(dec, key):
    if not isinstance(dec, ast.Call):
        return None
    for k in dec.keywords:
        if k.arg == key:
            if isinstance(k.value, ast.Constant):
                return k.value.value
            if isinstance(k.value, (ast.List, ast.Tuple)):
                return [_const(e) for e in k.value.elts]
    return None


def _scan(path: str) -> dict:
    """Ein AST-Durchlauf, alle Fakten. Kein Regex auf Quelltext."""
    tree = ast.parse(_read(path))
    out = {"routes": [], "slash": [], "events": [], "defs": [], "classes": []}
    toplevel = {id(n) for n in tree.body}

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
            continue
        if isinstance(node, ast.ClassDef):
            if id(node) in toplevel:
                out["classes"].append((node.lineno, node.end_lineno, node.name))
            continue

        tagged = False
        for dec in node.decorator_list:
            name = _dec_name(dec)
            if name.endswith(".route"):
                pfad = _const(dec.args[0]) if isinstance(dec, ast.Call) and dec.args else "?"
                methoden = _kw(dec, "methods") or ["GET"]
                out["routes"].append((node.lineno, pfad,
                                      "/".join(str(m) for m in methoden),
                                      node.name))
                tagged = True
            elif name.endswith("tree.command"):
                out["slash"].append((node.lineno,
                                     _kw(dec, "name") or node.name,
                                     (_kw(dec, "description") or "")[:60]))
                tagged = True
            elif name.endswith(".event"):
                out["events"].append((node.lineno, node.name))
                tagged = True
        if not tagged and id(node) in toplevel:
            out["defs"].append((node.lineno, node.end_lineno, node.name))
    return out


def _index_path(root: str) -> str:
    return os.path.join(root, ".claude", "INDEX.md")


def cmd_map(args) -> int:
    root = args.root
    ziel = _index_path(root)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)

    haupt = "bot.py"
    d = _scan(os.path.join(root, haupt))
    z = ["# NIGHTCRAWLER — Navigationskarte\n",
         "Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an",
         "Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.",
         "Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.\n"]

    z.append(f"## Flask-Routen in {haupt} ({len(d['routes'])})\n")
    z.append("```")
    for ln, pfad, meth, fn in sorted(d["routes"], key=lambda r: r[1]):
        z.append(f"{ln:>6}  {meth:<16} {pfad:<48} {fn}")
    z.append("```\n")

    # Seit Welle 2 der Zerlegung liegen Routen auch in nc/routes/*.py als
    # Blueprints. Ohne sie hier wuerde `ncpatch find` genau die Routen nicht
    # mehr finden, die aus dem Monolithen heraus sind — und die Kernregel des
    # Projekts ("erst fragen wo etwas steht") liefe ins Leere.
    bp_dir = os.path.join(root, "nc", "routes")
    bp_routes = []
    if os.path.isdir(bp_dir):
        for name in sorted(os.listdir(bp_dir)):
            if not name.endswith(".py") or name == "__init__.py":
                continue
            rel = f"nc/routes/{name}"
            for ln, pfad, meth, fn in _scan(os.path.join(bp_dir, name))["routes"]:
                bp_routes.append((rel, ln, pfad, meth, fn))
    if bp_routes:
        z.append(f"## Flask-Routen in Blueprints, nc/routes/ ({len(bp_routes)})\n")
        z.append("```")
        for rel, ln, pfad, meth, fn in sorted(bp_routes, key=lambda r: r[2]):
            z.append(f"{ln:>6}  {meth:<16} {pfad:<48} {fn}   [{rel}]")
        z.append("```\n")

    z.append(f"## Discord-Slash-Commands ({len(d['slash'])})\n")
    z.append("```")
    for ln, name, beschr in sorted(d["slash"], key=lambda r: r[1]):
        z.append(f"{ln:>6}  /{name:<22} {beschr}")
    z.append("```\n")

    if d["events"]:
        z.append(f"## Discord-Events ({len(d['events'])})\n")
        z.append("```")
        for ln, name in sorted(d["events"], key=lambda r: r[1]):
            z.append(f"{ln:>6}  {name}")
        z.append("```\n")

    z.append(f"## Top-Level-Symbole in {haupt} "
             f"({len(d['defs'])} Funktionen, {len(d['classes'])} Klassen)\n")
    z.append("```")
    alle = ([(a, b, f"class {c}") for a, b, c in d["classes"]]
            + [(a, b, c) for a, b, c in d["defs"]])
    for lo, hi, name in sorted(alle, key=lambda r: r[2]):
        z.append(f"{lo:>6}-{hi:<6} {name}")
    z.append("```\n")

    # Bibliotheken: öffentliche API je Modul, eine Zeile pro Modul
    for paket in ("nc", "brain"):
        pdir = os.path.join(root, paket)
        if not os.path.isdir(pdir):
            continue
        z.append(f"## {paket}/ — öffentliche Symbole\n")
        z.append("```")
        for datei in sorted(os.listdir(pdir)):
            if not datei.endswith(".py"):
                continue
            try:
                m = _scan(os.path.join(pdir, datei))
            except SyntaxError as e:
                z.append(f"{datei:<22} SYNTAXFEHLER Z.{e.lineno}")
                continue
            namen = sorted(
                [f"class {c}" for _, _, c in m["classes"] if not c.startswith("_")]
                + [n for _, _, n in m["defs"] if not n.startswith("_")])
            z.append(f"{datei:<22} {', '.join(namen) if namen else '—'}")
        z.append("```\n")

    text = "\n".join(z)
    _write(ziel, text)
    print(f"geschrieben: {os.path.relpath(ziel, root)}  "
          f"({len(text)//1024} KB, ~{len(text)//4} Token)")
    # ASCII in der Konsolen-Ausgabe: die Windows-Konsole faellt sonst auf
    # cp1252 zurueck und ersetzt Sonderzeichen durch Fragezeichen.
    print(f"  {len(d['routes'])} Routen | {len(d['slash'])} Slash-Commands | "
          f"{len(d['defs'])} Funktionen | {len(d['classes'])} Klassen")
    return 0


def cmd_find(args) -> int:
    """Wo ist X? Beantwortet aus der Karte statt aus der Datei."""
    ziel = _index_path(args.root)
    if not os.path.exists(ziel):
        print("Keine Karte vorhanden — erst `ncpatch map` laufen lassen.")
        return 1
    muster = args.query.lower()
    treffer = [z for z in _read(ziel).splitlines()
               if muster in z.lower() and z.strip()
               and not z.startswith(("#", "```", "Erzeugt", "Zahlen"))]
    for z in treffer[:args.limit]:
        print(z)
    rest = len(treffer) - args.limit
    print(f"\n{len(treffer)} Treffer" + (f" ({rest} nicht gezeigt)" if rest > 0 else ""))
    return 0 if treffer else 1


# ─────────────────────────────────────────── Doku: Zahlen und Anker

# WARUM: README.md und CLAUDE.md nennen Dutzende Kennzahlen — Routen, Zeilen,
# Module, Agenten, .env-Variablen. Die sind zweimal still auseinandergelaufen:
# das README sprach von 345 Routen (echte 355), 34.487 Zeilen (echte 32.569)
# und 12 Sentinel-Agenten, waehrend 13 registriert waren — swap und proxy
# fehlten in der Tabelle ganz. Alle diese Zahlen stehen im Quelltext. Dieser
# Befehl vergleicht sie, statt sie zu glauben.
#
# Bewusst NICHT Teil von `check`: `check` laeuft in deploy.sh vor dem
# Umschwenken auf Produktion. Eine veraltete Zahl im README darf einen Deploy
# nicht aufhalten — sie gehoert in die CI, wo sie vor dem Merge auffaellt.

# Einheit -> erlaubte Werte. Mehrere Werte, weil eine Zahl legitim in
# Teilmengen auftritt ("355 Routen (265 in bot.py, 90 in nc/routes/)").
def _kennzahlen(root: str) -> tuple[dict, dict]:
    d = _scan(os.path.join(root, "bot.py"))
    zeilen = len(_read(os.path.join(root, "bot.py")).splitlines())

    bp_dir = os.path.join(root, "nc", "routes")
    bp_dateien = [f for f in sorted(os.listdir(bp_dir))
                  if f.endswith(".py") and f != "__init__.py"] \
        if os.path.isdir(bp_dir) else []
    bp_routen = sum(len(_scan(os.path.join(bp_dir, f))["routes"])
                    for f in bp_dateien)

    def _module(pfad: str) -> int:
        p = os.path.join(root, pfad)
        if not os.path.isdir(p):
            return 0
        return len([f for f in os.listdir(p) if f.endswith(".py")
                    and f != "__init__.py" and not f.startswith("test_")])

    # Die Sentinel-Flotte: jede Agentenklasse traegt ihren Namen als
    # Klassenattribut. Die Basisklasse heisst selbst "agent" und zaehlt nicht.
    agenten = {m.group(1) for m in re.finditer(
        r'^\s*name\s*=\s*"([a-z_]+)"',
        _read(os.path.join(root, "brain", "agents.py")), re.M)} - {"agent"}

    # Telegram-Befehle stehen als Tupel-Liste in der Registrierung, nicht als
    # Dekorator — deshalb ueber den AST statt ueber _scan.
    tg = 0
    for node in ast.walk(ast.parse(_read(os.path.join(root, "bot.py")))):
        if not isinstance(node, ast.For) or not isinstance(node.iter, ast.Tuple):
            continue
        if "CommandHandler" not in ast.dump(node):
            continue
        tg = max(tg, len(node.iter.elts))

    env = os.path.join(root, ".env.example")
    variablen = len({m.group(1) for m in re.finditer(
        r"^#?\s*([A-Z][A-Z0-9_]{2,})=", _read(env), re.M)}) if os.path.exists(env) else 0

    routen = len(d["routes"]) + bp_routen
    einheiten = {
        "Routen":            {routen, len(d["routes"]), bp_routen},
        "API-Routen":        {routen, len(d["routes"]), bp_routen},
        "Flask-Routen":      {routen, len(d["routes"]), bp_routen},
        "Blueprints":        {len(bp_dateien)},
        "Flask-Blueprints":  {len(bp_dateien)},
        "Slash-Commands":    {len(d["slash"])},
        "Funktionen":        {len(d["defs"])},
        "Fachmodule":        {_module("nc")},
        # Auf Tausender abgerundet ist zulaessig ("bot.py hat ueber 32.000
        # Zeilen") — alles andere muss die exakte Zahl sein.
        "Zeilen":            {zeilen, zeilen // 1000 * 1000},
        "Befehle":           {tg},
        "Variablen":         {variablen},
        "Wächter":           {len(agenten)},
        "Wächter-Agenten":   {len(agenten)},
    }
    # Tabellenzeilen nennen die Zahl NACH dem Begriff: "| Sentinel-Agenten | 13 |"
    labels = {
        "Flask-Routen":            einheiten["Routen"],
        "Discord-Slash-Commands":  einheiten["Slash-Commands"],
        "Fachmodule":              einheiten["Fachmodule"],
        "Sentinel-Agenten":        einheiten["Wächter"],
        "Konfigurationsvariablen": einheiten["Variablen"],
    }
    return einheiten, labels


def _befehle(root: str) -> dict[str, set[str]]:
    """Die registrierten Befehlsnamen. WARUM zusaetzlich zur Zahl: wer einen
    46. Slash-Command hinzufuegt und im README brav "46" schreibt, ohne den
    Namen in die Liste zu setzen, kaeme durch eine reine Zaehlpruefung."""
    pfad = os.path.join(root, "bot.py")
    discord = {name for _, name, _ in _scan(pfad)["slash"]}

    # Telegram registriert ueber eine Tupel-Liste, nicht ueber Dekoratoren.
    telegram: set[str] = set()
    for node in ast.walk(ast.parse(_read(pfad))):
        if (isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple)
                and "CommandHandler" in ast.dump(node)):
            namen = {e.elts[0].value for e in node.iter.elts
                     if isinstance(e, ast.Tuple) and isinstance(e.elts[0], ast.Constant)}
            if len(namen) > len(telegram):
                telegram = namen
    return {"Discord": discord, "Telegram": telegram}


def _slug(titel: str) -> str:
    """GitHubs Anker-Regel: kleinschreiben, Satzzeichen und Emoji raus,
    Leerzeichen zu '-'. NICHT trimmen — genau deshalb faengt der Anker einer
    Emoji-Ueberschrift mit '-' an, und genau daran starb der Discord-Badge."""
    t = re.sub(r"[`*\[\]().,:„“\"/]", "", titel).lower()
    behalten = "".join(c for c in t
                       if re.match(r"[\w \-]", c) or c == "️")
    return "#" + behalten.replace(" ", "-")


def _doku_zeilen(text: str):
    """Zeilen ohne Codebloecke — Mermaid ausgenommen, dort stehen Kennzahlen
    in den Diagramm-Beschriftungen und sollen mitgeprueft werden."""
    fence = None
    for nr, zeile in enumerate(text.split("\n"), 1):
        if zeile.startswith("```"):
            fence = None if fence is not None else zeile[3:].strip().lower()
            continue
        if fence is not None and fence != "mermaid":
            continue
        yield nr, zeile


def cmd_docs(args) -> int:
    root = args.root
    einheiten, labels = _kennzahlen(root)
    rc = 0

    def zahl(s: str) -> int:
        return int(s.replace(".", "").replace(" ", ""))

    muster = re.compile(r"(\d[\d.]*)\s*\**\s*(" +
                        "|".join(sorted(einheiten, key=len, reverse=True)) + r")\b")
    # Nur die Dateien, deren Zahlen aus dem Quelltext stammen. docs/CHANGELOG
    # und README_V37 halten bewusst historische Staende fest — dort waere eine
    # "veraltete" Zahl richtig.
    for datei in ("README.md", "CLAUDE.md", "docs/INSTALL.md",
                  "docs/ROADMAP.md", "docs/TROUBLESHOOTING.md"):
        pfad = os.path.join(root, datei)
        if not os.path.exists(pfad):
            continue
        text = _read(pfad)
        for nr, zeile in _doku_zeilen(text):
            for m in muster.finditer(zeile):
                wert, einheit = zahl(m.group(1)), m.group(2)
                if wert not in einheiten[einheit]:
                    erlaubt = " oder ".join(f"{v:,}".replace(",", ".")
                                            for v in sorted(einheiten[einheit]))
                    print(f"  {datei}:{nr}: {m.group(1)} {einheit} — "
                          f"echt sind {erlaubt}")
                    rc = 1
            if zeile.startswith("|"):
                zellen = [z.strip() for z in zeile.strip("|").split("|")]
                if len(zellen) >= 2 and zellen[0].strip("*` ") in labels:
                    erlaubt = labels[zellen[0].strip("*` ")]
                    treffer = re.search(r"(\d[\d.]*)", zellen[1])
                    if treffer and zahl(treffer.group(1)) not in erlaubt:
                        print(f"  {datei}:{nr}: {zellen[0]} = "
                              f"{treffer.group(1)} — echt sind "
                              f"{' oder '.join(str(v) for v in sorted(erlaubt))}")
                        rc = 1

    # v4.1-W17: Version und Codename gegen nc/version.py. Die Zahlenpruefung
    # oben faengt sie NICHT — "4.0" ist keine Einheit, und genau deshalb stand
    # im deutschen README ein halbes Jahr lang "4.0 Restream Control Room",
    # waehrend nc/version.py und das englische README schon bei 4.1 waren.
    # Wer die Fassung anhebt, aendert nc/version.py; alles andere zieht nach.
    vpfad = os.path.join(root, "nc", "version.py")
    if os.path.exists(vpfad):
        vq = _read(vpfad)
        mv = re.search(r'^VERSION\s*=\s*"([^"]+)"', vq, re.M)
        mc = re.search(r'^CODENAME\s*=\s*"([^"]+)"', vq, re.M)
        if mv:
            for datei in ("README.md", "README.en.md"):
                pfad = os.path.join(root, datei)
                if not os.path.exists(pfad):
                    continue
                for nr, zeile in _doku_zeilen(_read(pfad)):
                    if not re.search(r"\|\s*(Aktuelle Version|Current version)\s*\|", zeile):
                        continue
                    mz = re.search(r"\*\*([0-9]+\.[0-9]+)\*\*", zeile)
                    if mz and mz.group(1) != mv.group(1):
                        print(f"  {datei}:{nr}: Version {mz.group(1)} — "
                              f"nc/version.py sagt {mv.group(1)}")
                        rc = 1
                    # Der Codename nur im deutschen README: das englische
                    # fuehrt bewusst eine Uebersetzung ("Public Voice").
                    if mc and datei == "README.md" and mc.group(1) not in zeile:
                        print(f"  {datei}:{nr}: Codename fehlt oder veraltet — "
                              f"nc/version.py sagt {mc.group(1)!r}")
                        rc = 1

    readme = os.path.join(root, "README.md")
    if os.path.exists(readme):
        text = _read(readme)

        # Die Befehlslisten namentlich, nicht nur ihre Laenge.
        for kanal, (von, bis) in (("Telegram", ("### Telegram", "<details>")),
                                  ("Discord", ("<summary><h3>Discord", "</details>"))):
            try:
                a = text.index(von)
                ausschnitt = text[a:text.index(bis, a)]
            except ValueError:
                print(f"  README.md: Befehlsliste {kanal} nicht gefunden — "
                      f"Anker {von!r} fehlt, Pruefung faellt aus")
                rc = 1
                continue
            # Der Lookahead haelt "`/sys_*`" aus der Liste heraus: das ist
            # ein Sammelbegriff im Fliesstext, kein registrierter Befehl.
            gelistet = set(re.findall(r"`/([a-z_]+)(?=[`\s])", ausschnitt))
            echt = _befehle(root)[kanal]
            for fehlt in sorted(echt - gelistet):
                print(f"  README.md: /{fehlt} ist registriert, steht aber in "
                      f"keiner {kanal}-Liste")
                rc = 1
            for zuviel in sorted(gelistet - echt):
                print(f"  README.md: /{zuviel} steht in der {kanal}-Liste, "
                      f"ist aber nicht registriert")
                rc = 1

        # Interne Anker. Zwei Badges zeigten ins Leere, einer davon nur wegen
        # des unsichtbaren Variation Selectors im Emoji der Ueberschrift.
        anker = {_slug(m.group(1).strip())
                 for nr, z in _doku_zeilen(text)
                 for m in [re.match(r"^#{1,6}\s+(.*)$", z)] if m}
        for nr, zeile in _doku_zeilen(text):
            for ziel in re.findall(r"\]\((#[^)]+)\)", zeile):
                if ziel not in anker:
                    print(f"  README.md:{nr}: toter Anker {ziel!r}")
                    rc = 1

    print("  doku: BEFUNDE — Zahlen von Hand nachgezogen?" if rc else
          "  doku: OK (Zahlen und interne Anker gegen den Quelltext geprueft)")
    return rc


# ────────────────────────────────────────────────────────────── CLI


def main() -> int:
    p = argparse.ArgumentParser(prog="ncpatch")
    p.add_argument("--root", default=".", help="Projektwurzel")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, fn in (("apply", cmd_apply), ("verify", cmd_verify)):
        s = sub.add_parser(name)
        s.add_argument("patch")
        s.set_defaults(func=fn)

    s = sub.add_parser("check"); s.set_defaults(func=cmd_check)

    s = sub.add_parser("docs"); s.set_defaults(func=cmd_docs)

    s = sub.add_parser("grep")
    s.add_argument("pattern"); s.add_argument("file")
    s.add_argument("-C", "--context", type=int, default=2)
    s.set_defaults(func=cmd_grep)

    s = sub.add_parser("show")
    s.add_argument("file"); s.add_argument("start", type=int)
    s.add_argument("end", type=int)
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("sym")
    s.add_argument("file"); s.add_argument("name")
    s.set_defaults(func=cmd_sym)

    s = sub.add_parser("map"); s.set_defaults(func=cmd_map)

    s = sub.add_parser("find")
    s.add_argument("query")
    s.add_argument("-n", "--limit", type=int, default=40)
    s.set_defaults(func=cmd_find)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
