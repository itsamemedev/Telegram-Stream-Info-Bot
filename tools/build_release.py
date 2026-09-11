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
    # Bot-seitig, alle vier: bot.py importiert discordbot und telegramversand
    # ZUR LAUFZEIT (erst in der Funktion, nicht am Dateikopf). Fehlen sie im
    # Archiv, stirbt der Import in einem breiten except und Discord bzw. der
    # Aufnahme-Versand sind still tot — genau das Fehlerbild, das laut
    # CLAUDE.md schon einmal monatelang unsichtbar blieb.
    "bot.py", "brain_bridge.py", "discordbot.py", "telegramversand.py",
    # Die Anleitungen liegen seit dem Aufraeumen unter docs/ und kommen ueber
    # ORDNER mit — hier einzeln aufzuzaehlen wuerde sie doppelt einpacken und
    # bei jeder Umbenennung ein "FEHLT:" ins Protokoll schreiben.
    "CLAUDE.md", "CLAUDE.en.md", "AGENTS.md", "README.md", "README.en.md",
    "LICENSE",
    "llama-server.service", "requirements.txt", "requirements-smoke.txt",
    ".gitignore", ".gitattributes",
    "test_smoke.py", "test_nc_modules.py", "test_restream.py",
    "test_m2_bridge.py",
    ".env.example",
    # Standbild-Rueckfall des gebrannten Avatars (v4.2-W31). Ohne die Datei
    # faellt die Kette Feeder -> Schleife -> Standbild ins Leere und die Ecke
    # bleibt leer, ohne dass irgendwo ein Fehler steht.
    "azrael_avatar.png",
]
# locales/ traegt den Uebersetzungskatalog (v4.1-W6): fehlt er, faellt jede
# Ausgabe auf Deutsch zurueck — ohne Fehlermeldung, weil genau das der
# gewollte Rueckfall ist. assets/ traegt die Avatar-Schleifen (v4.2-W32).
ORDNER = ["brain", "nc", "templates", "website", "tools", ".claude", "docs",
          "locales", "assets"]

# .env bleibt DRAUSSEN (echte Secrets). .env.example (nur Vorlage, überschreibt
# nie eine bestehende .env) faehrt seit v4.0-W100 MIT — Doku aller Variablen.
AUS = {".env"}
AUS_ENDUNG = (".pyc", ".pyo", ".bak", ".tmp", ".log", ".sqlite", ".sqlite3",
              ".db", ".zip", ".tgz", ".pem", ".key")
AUS_ORDNER = {"__pycache__", ".ruff_cache", ".git", "recordings", "build",
              "node_modules", ".pytest_cache",
              # Arbeitskopien paralleler Agenten liegen unter .claude/, und
              # .claude/ faehrt mit. Gepackt wird aus dem Dateisystem, nicht
              # aus dem git-Index — .gitignore allein haelt sie NICHT auf.
              "worktrees"}


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

    # ── Gegenprobe 1b: kein eigener Modul-Import ins Leere ───────────────
    # DATEIEN ist eine Liste von Hand, und die veraltet still: discordbot.py
    # (v4.2-W15) und telegramversand.py (v4.2-W19) wurden aus dem Monolithen
    # geloest und standen ueber vier Wellen NICHT im Archiv. bot.py importiert
    # beide erst zur Laufzeit in der Funktion — der ImportError landet dann in
    # einem breiten except und der Betreiber sieht nur, dass Discord und der
    # Aufnahme-Versand "nicht mehr gehen".
    #
    # Statt die Liste zu pflegen wird sie deshalb geprueft: welcher Name im
    # Archiv wird importiert und liegt als Modul in der Wurzel, ist aber selbst
    # nicht mitgekommen? Ein Namensvergleich haette dieselbe Luecke gehabt.
    eigene = {f[:-3] for f in os.listdir(WURZEL)
              if f.endswith(".py") and os.path.isfile(os.path.join(WURZEL, f))}
    mit = {n for n in drin if n.endswith(".py") and "/" not in n}
    gebraucht = set()
    for rel in sorted(mit):
        with open(os.path.join(WURZEL, rel), encoding="utf-8") as _fh:
            for zeile in _fh:
                w = zeile.split()
                if len(w) >= 2 and w[0] in ("import", "from"):
                    name = w[1].split(".")[0].rstrip(",")
                    if name in eigene:
                        gebraucht.add(name)
    fehlt_modul = sorted(m for m in gebraucht if f"{m}.py" not in mit)
    if fehlt_modul:
        print(f"ABBRUCH — importiert, aber nicht im Archiv: {fehlt_modul}")
        print("          (in DATEIEN aufnehmen — sonst stirbt der Import still)")
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
    with open(ZIEL, "rb") as _fh:
        h = hashlib.sha256(_fh.read()).hexdigest()[:16]
    print(f"{len(drin)} Dateien · {n} .py aus dem Archiv compiliert · 0 Fehler")
    print("Geheimnis-Gegenprobe: SAUBER")
    print(f"{os.path.basename(ZIEL)}  {gr/1024/1024:.2f} MB  sha256:{h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
