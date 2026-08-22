#!/usr/bin/env python3
"""ncpatch — anker-basiertes Patchen des NIGHTCRAWLER-Monolithen.

WARUM: bot_v37.py hat ~29.000 Zeilen / 1,4 MB. Die Datei in ein LLM-Kontext-
fenster zu laden kostet ~400k Token PRO Durchgang. Dieses Tool erlaubt
chirurgische Änderungen über eindeutige Textanker, ohne die Datei je
vollständig zu lesen oder zu schreiben.

Patch-Format: eine JSON-Datei mit einer Liste von Operationen.

  [
    {"file": "bot_v37.py",
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
  python3 ncpatch.py grep  "such-text" bot_v37.py   [-C 3]       # Anker finden
  python3 ncpatch.py show  bot_v37.py 24721 24760                # Zeilen zeigen
  python3 ncpatch.py sym   bot_v37.py _discord_start             # Symbol-Zeilen
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
            markup = re.sub(r"<script[^>]*>.*?</script>", "", markup, flags=re.S)
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
            for i, m in enumerate(re.finditer(
                    r"<script([^>]*)>(.*?)</script>", html, re.S), 1):
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
# bot_v37.py kostet ein Vielfaches dessen, was der gesuchte Ausschnitt
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

    haupt = "bot_v37.py"
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
