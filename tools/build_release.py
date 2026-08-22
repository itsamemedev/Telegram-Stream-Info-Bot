#!/usr/bin/env python3
"""Baut das Auslieferungsarchiv NIGHTCRAWLER_v37_<BUILD>.zip.

    python tools/build_release.py B138

Warum im Projekt und nicht als Einmal-Skript: der Build muss reproduzierbar
sein. Was ins Archiv gehoert, ist eine Projektentscheidung — sie gehoert
versioniert, nicht in ein Wegwerf-Skript.

Regeln aus CLAUDE.md, die hier durchgesetzt werden:
  * .env liegt NIE im Archiv (echte Variablen, Cookies, OAuth-Tokens, Keys).
    .env.example faehrt seit v4.0-W100 MIT — reine Vorlage aller Variablen, sie
    ueberschreibt nie eine bestehende .env (anderer Dateiname).
  * .claude/skills gehoeren MIT ins Archiv — nur dort findet Claude Code sie.
  * Datenbank, Aufnahmen, Logs, Caches: niemals.

Am Ende laeuft eine Gegenprobe: kein Treffer auf .env/.sqlite/.pem/.key, und
jede enthaltene .py-Datei wird aus dem ENTPACKTEN Archiv nachcompiliert. Ein
Archiv, das nicht compiliert, verlaesst diese Maschine nicht.
"""
import hashlib
import os
import py_compile
import sys
import tempfile
import zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = (sys.argv[1] if len(sys.argv) > 1 else "B138").upper()
ZIEL = os.path.join(WURZEL, f"NIGHTCRAWLER_v37_{BUILD}.zip")

DATEIEN = [
    "bot_v37.py", "brain_bridge.py",
    "CLAUDE.md", "DEPLOY.md", "README_V37.md", "START_HIER.txt",
    "SETUP_LLAMACPP.md", "SETUP_TWITCH_OAUTH.md", "SETUP_YT_OAUTH.md",
    "llama-server.service", "requirements.txt",
    ".gitignore", ".gitattributes",
    "test_smoke.py", "test_nc_modules.py", "test_restream.py",
    "test_m2_bridge.py",
    ".env.example",
]
ORDNER = ["brain", "nc", "templates", "website", "tools", ".claude", "docs"]

# .env bleibt DRAUSSEN (echte Secrets). .env.example (nur Vorlage, überschreibt
# nie eine bestehende .env) faehrt seit v4.0-W100 MIT — Doku aller Variablen.
AUS = {".env"}
AUS_ENDUNG = (".pyc", ".pyo", ".bak", ".tmp", ".log", ".sqlite", ".sqlite3",
              ".db", ".zip", ".tgz", ".pem", ".key")
AUS_ORDNER = {"__pycache__", ".ruff_cache", ".git", "recordings", "build",
              "node_modules", ".pytest_cache"}


def erlaubt(relpfad, name):
    if name in AUS or name.lower().endswith(AUS_ENDUNG):
        return False
    return not (set(os.path.normpath(relpfad).split(os.sep)) & AUS_ORDNER)


def main():
    drin = []
    with zipfile.ZipFile(ZIEL, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in DATEIEN:
            p = os.path.join(WURZEL, f)
            if not os.path.exists(p):
                print(f"  FEHLT: {f}")
                continue
            if erlaubt(f, f):
                z.write(p, f)
                drin.append(f)
        for d in ORDNER:
            basis = os.path.join(WURZEL, d)
            if not os.path.isdir(basis):
                print(f"  FEHLT (Ordner): {d}")
                continue
            for wurzel, unter, dateien in os.walk(basis):
                unter[:] = [u for u in unter if u not in AUS_ORDNER]
                for name in sorted(dateien):
                    voll = os.path.join(wurzel, name)
                    rel = os.path.relpath(voll, WURZEL).replace(os.sep, "/")
                    if erlaubt(rel, name):
                        z.write(voll, rel)
                        drin.append(rel)

    # ── Gegenprobe 1: nichts Geheimes ───────────────────────────────────
    # .env.example ist ausdruecklich erlaubt (nur Vorlage); jede andere .env* nicht.
    verdacht = [n for n in drin
                if (".env" in n.lower() and os.path.basename(n).lower() != ".env.example")
                or n.lower().endswith((".sqlite", ".db", ".pem", ".key"))]
    if verdacht:
        print(f"ABBRUCH — Geheimnisverdacht im Archiv: {verdacht}")
        os.remove(ZIEL)
        return 1

    # ── Gegenprobe 2: entpacken und compilieren ─────────────────────────
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIEL) as z:
            if z.testzip() is not None:
                print("ABBRUCH — ZIP defekt")
                return 1
            z.extractall(tmp)
        n = fehler = 0
        for w, _, fs in os.walk(tmp):
            for f in fs:
                if f.endswith(".py"):
                    n += 1
                    try:
                        py_compile.compile(os.path.join(w, f), doraise=True)
                    except Exception as e:
                        fehler += 1
                        print(f"  COMPILE-FEHLER {f}: {e}")
        if fehler:
            print(f"ABBRUCH — {fehler} Datei(en) compilieren nicht")
            os.remove(ZIEL)
            return 1

    gr = os.path.getsize(ZIEL)
    h = hashlib.sha256(open(ZIEL, "rb").read()).hexdigest()[:16]
    print(f"{len(drin)} Dateien · {n} .py aus dem Archiv compiliert · 0 Fehler")
    print("Geheimnis-Gegenprobe: SAUBER")
    print(f"{os.path.basename(ZIEL)}  {gr/1024/1024:.2f} MB  sha256:{h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
