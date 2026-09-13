#!/usr/bin/env python3
"""tools/abhaengigkeiten.py — v4.2-W68: ist jedes Fremdpaket erklaert?

Zwei Fragen, die bisher niemand gestellt hat.

**1. Ist requirements.txt vollstaendig?** Der Vertrag aus v4.1-W31 prueft nur
die MODUL-EBENE und nur gegen requirements-smoke.txt. Genau die teuren Pakete
werden aber erst IN Funktionen importiert — boto3, faster_whisper, redis,
pymysql, httpx, requests, socks, websockets_proxy. Fuer die gab es keine
Pruefung. Ein `import stripe` in einer Funktion faellt heute niemandem auf: auf
dem Server laeuft es (dort wurde es irgendwann von Hand nachinstalliert), und
eine frische Installation nach requirements.txt stirbt Monate spaeter an einer
Stelle, die niemand mit dem Import in Verbindung bringt.

**2. Traegt jeder Eintrag eine Untergrenze?** Bis W68 trug keiner von 17 eine.

Drei Sorten Import zaehlen bewusst NICHT als Verstoss, und alle drei stehen so
im Bestand:

    mitgeliefert   nc/_vendor/segno — liegt im Archiv, kein pip noetig
    optional       `try: import browser_cookie3 / except ImportError:` —
                   der Code faengt das Fehlen ab und sagt warum
    Werkzeug       tools/*.py ist keine Laufzeit. Pillow steht deshalb in
                   keiner requirements-Datei, und ein Vertrag aus W53 haelt
                   das ausdruecklich fest.

Wer diese drei nicht kennt, meldet drei Fehlalarme und wird abgeschaltet.

    python3 tools/abhaengigkeiten.py            Bericht
    python3 tools/abhaengigkeiten.py --sperre   nichts Unerklaertes (CI)
"""

import argparse
import ast
import io
import os
import pathlib
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Importname -> pip-Name. Nur was sich unterscheidet steht hier.
PIPNAME = {"dotenv": "python-dotenv", "discord": "discord.py",
           "socks": "PySocks", "pymysql": "PyMySQL", "PIL": "Pillow",
           "telegram": "python-telegram-bot", "faster_whisper": "faster-whisper"}

# Liegt im Archiv unter nc/_vendor/ — nie ueber pip.
#
# Heute traegt diese Liste fuer segno nichts bei: die beiden Aufrufstellen
# in nc/qrsvg.py stehen in einem try/except Exception und gelten damit
# ohnehin als optional. Sie bleibt trotzdem, denn sie deckt den Fall, den
# es sonst nicht gaebe: ein mitgeliefertes Paket UNGESCHUETZT importiert.
MITGELIEFERT = {"segno"}

# Kein Laufzeit-Code. Pillow haengt hier dran und darf nirgends auftauchen.
KEINE_LAUFZEIT = ("tools/", "test_")

LOKAL = {"nc", "brain", "bot", "brain_bridge", "tools", "discordbot",
         "telegramversand", "test_smoke", "test_nc_modules", "test_restream"}


def _importe(pfad):
    """-> (pflicht, optional). Modul-Ebene UND Funktionsrumpf.

    Optional heisst: irgendwo ueber dem Import faengt ein `except` einen
    ImportError mit ab. Der Code kommt dann ohne das Paket aus und sagt das
    auch — `browser_cookie3` ist der Fall, um den es geht.
    """
    baum = ast.parse(pathlib.Path(pfad).read_text(encoding="utf-8"))
    pflicht, optional = set(), set()

    def namen(k):
        if isinstance(k, ast.Import):
            return [a.name.split(".")[0] for a in k.names]
        if isinstance(k, ast.ImportFrom) and k.level == 0 and k.module:
            return [k.module.split(".")[0]]
        return []

    def lauf(koerper, weich):
        for k in koerper:
            for n in namen(k):
                if n in sys.stdlib_module_names or n in LOKAL:
                    continue
                (optional if weich else pflicht).add(n)
            if isinstance(k, ast.Try):
                faengt = any(
                    h.type is None or any(w in ast.unparse(h.type) for w in (
                        "ImportError", "ModuleNotFoundError", "Exception",
                        "BaseException"))
                    for h in k.handlers)
                lauf(k.body, weich or faengt)
                for h in k.handlers:
                    lauf(h.body, True)
                lauf(k.orelse, weich or faengt)
                lauf(k.finalbody, weich)
            else:
                # In JEDEN Rumpf absteigen, nicht nur in if/try. Genau die
                # Importe in Funktionen sind der ungepruefte Teil, und die
                # stecken in FunctionDef, With, For und async-Varianten.
                for feld in ("body", "orelse", "finalbody"):
                    kinder = getattr(k, feld, None)
                    if isinstance(kinder, list) and kinder \
                            and isinstance(kinder[0], ast.stmt):
                        lauf(kinder, weich)

    lauf(baum.body, False)
    return pflicht, optional - pflicht


def _dateien():
    aus = ["bot.py", "discordbot.py", "telegramversand.py", "brain_bridge.py"]
    for muster in ("nc/**/*.py", "brain/**/*.py"):
        aus += [str(p) for p in sorted(pathlib.Path(WURZEL).glob(muster))
                if "_vendor" not in str(p)]
    fertig = []
    for d in aus:
        p = d if os.path.isabs(d) else os.path.join(WURZEL, d)
        rel = os.path.relpath(p, WURZEL).replace(os.sep, "/")
        if not os.path.isfile(p) or rel.startswith(KEINE_LAUFZEIT):
            continue
        if os.path.basename(rel).startswith("test_"):
            continue
        fertig.append(rel)
    return fertig


def grenze(roh):
    """-> die Untergrenze einer requirements-Zeile, oder '' ohne."""
    fuer = roh.split(";")[0]
    for teil in fuer.split(","):
        teil = teil.strip()
        for t in (">=", "=="):
            if t in teil:
                return teil.split(t, 1)[1].strip()
    return ""


def _gelistet(datei="requirements.txt"):
    """-> {pip-name klein: rohe Zeile}."""
    aus = {}
    pfad = os.path.join(WURZEL, datei)
    for zeile in io.open(pfad, encoding="utf-8").read().splitlines():
        roh = zeile.split("#")[0].strip()
        if not roh:
            continue
        name = roh.split(";")[0]
        for trenn in (">=", "==", "<=", "~=", "!=", ">", "<"):
            name = name.split(trenn)[0]
        aus[name.strip().lower()] = roh
    return aus


def bericht():
    """-> (unerklaert, ohne_grenze, tot)."""
    gelistet = _gelistet()
    gebraucht, unerklaert = set(), []
    for d in _dateien():
        pflicht, optional = _importe(os.path.join(WURZEL, d))
        for n in pflicht:
            if n in MITGELIEFERT:
                continue
            pip = PIPNAME.get(n, n)
            gebraucht.add(pip.lower())
            if pip.lower() not in gelistet:
                unerklaert.append((d, n, pip))
        for n in optional:
            if n not in MITGELIEFERT:
                gebraucht.add(PIPNAME.get(n, n).lower())
    # Eine Untergrenze ist das Mindeste. Ein nackter Name laesst pip auf einer
    # alten Maschine eine Fassung von 2019 aufloesen, und der Fehler kommt dann
    # als AttributeError irgendwo tief im Code an, nicht als klare Ansage.
    ohne = sorted(n for n, roh in gelistet.items()
                  if not any(t in roh for t in (">=", "==", "~=")))
    tot = sorted(set(gelistet) - gebraucht)
    # Und die Untergrenzen der beiden Dateien muessen uebereinstimmen. Sonst
    # installiert die CI eine andere Fassungsreihe, als requirements.txt fuer
    # Produktion zusagt — ein gruener Rauchtest waere dann eine Aussage ueber
    # die falsche Bibliothek.
    rauch = _gelistet("requirements-smoke.txt")
    uneins = sorted((n, grenze(gelistet[n]), grenze(r))
                    for n, r in rauch.items()
                    if n in gelistet and grenze(r) != grenze(gelistet[n]))
    return sorted(set(unerklaert)), ohne, tot, uneins


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true")
    a = p.parse_args(argv)

    unerklaert, ohne, tot, uneins = bericht()
    gelistet = _gelistet()
    lock = os.path.join(WURZEL, "requirements.lock.txt")

    if unerklaert:
        print("abhaengigkeiten: Import ohne Eintrag in requirements.txt.")
        print("Auf dem Server laeuft das — dort wurde es irgendwann von Hand "
              "nachinstalliert. Eine frische Installation stirbt daran.\n")
        for d, n, pip in unerklaert:
            print(f"  {d}   import {n}   -> fehlt als '{pip}'")
    if ohne:
        print("\nabhaengigkeiten: Eintrag ohne Untergrenze:")
        for n in ohne:
            print(f"  {gelistet[n]}")
        print("  Ohne >= loest pip auf einer alten Maschine irgendetwas auf, "
              "und der Fehler kommt als AttributeError tief im Code an.")
    if tot:
        print("\nabhaengigkeiten: gelistet, aber nirgends importiert: "
              + ", ".join(tot))

    if uneins:
        print("\nabhaengigkeiten: requirements.txt und requirements-smoke.txt "
              "nennen verschiedene Untergrenzen:")
        for n, a_, b_ in uneins:
            print(f"  {n}: requirements.txt >= {a_ or '(keine)'} , "
                  f"smoke >= {b_ or '(keine)'}")
        print("  Dann prueft die CI eine Fassungsreihe, die der Bot nicht "
              "benutzt.")

    if not (unerklaert or ohne or tot or uneins):
        print(f"abhaengigkeiten: OK — {len(gelistet)} Pakete, alle erklaert "
              f"und mit Untergrenze")
        if not os.path.isfile(lock):
            # Kein Fehler: die Datei kann nur auf dem Server entstehen. Aber
            # sie soll auch nicht still fehlen — requirements.txt verspricht
            # sie seit ihrer ersten Fassung im Kopfkommentar.
            print("  Hinweis: requirements.lock.txt fehlt weiterhin. Die "
                  "exakten Fassungen kennt nur der Server:")
            print("    python3 -m pip freeze > requirements.lock.txt")
        return 0
    return 1 if a.sperre else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os._exit(0)
