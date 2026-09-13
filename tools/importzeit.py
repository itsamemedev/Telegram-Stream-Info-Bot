#!/usr/bin/env python3
"""tools/importzeit.py — v4.2-W67: liest jemand die .env, bevor es sie gibt?

CLAUDE.md nennt die Falle beim Namen:

    „Modul-Konstanten frieren `.env` ein. `.env` wird teils erst nach den
     ersten Imports geladen. Konfiguration als Funktion lesen
     (`_backend_conf()`), nie als Modul-Konstante."

Der Satz stimmte, nur hat ihn nichts geprueft — und der Bestand hat ihn
gebrochen. `nc/freeai.py` baute seine Basen-Liste auf Modul-Ebene, und weil
`nc/news.py`, `nc/marketing.py` und `nc/routes/ai.py` das Modul in der
Import-Reihe von bot.py mitziehen, geschah das rund 130 Zeilen VOR
`load_dotenv()`. Folge: `POLLINATIONS_API_KEY` und `LLM7_TOKEN` standen in der
.env und haben nie einen Request erreicht.

WARUM DIESES WERKZEUG DEN BOT WIRKLICH STARTET statt den Quelltext zu lesen:
ein AST-Lauf findet nur das woertliche `os.getenv` auf Modul-Ebene. Von den
fuenf echten Faellen fand er EINEN. Die anderen vier standen in
`_default_bases()` — einer Funktion, die auf Modul-Ebene AUFGERUFEN wird. Die
Aufrufkette sieht man statisch nicht, die Ausfuehrung schon.

    python3 tools/importzeit.py            Bericht
    python3 tools/importzeit.py --sperre   keine Lesung vor load_dotenv (CI)
    python3 tools/importzeit.py --statisch schneller AST-Blick ohne Start
"""

import argparse
import ast
import contextlib
import os
import sys

# v4.2-W83: gemeinsamer Parser, der eine unlesbare Datei meldet statt sie zu
# ueberspringen. Auch der schwache Blick (--statisch) soll nicht behaupten,
# er habe nachgesehen, wenn er es nicht konnte.
import quelle
import tempfile
import traceback

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _pfad(datei):
    try:
        return os.path.relpath(datei, WURZEL)
    except ValueError:
        return datei


@contextlib.contextmanager
def mitschnitt():
    """Jede .env-Lesung aus EIGENEM Quelltext mitschreiben.

    Liefert `(stand, roh)`. Sobald `stand["geladen"]` True ist, wird nichts
    mehr aufgezeichnet — das ist der Moment von load_dotenv(). Eigener
    Kontextmanager, damit die Vertragspruefung das Abfangen testen kann,
    ohne den ganzen Bot zu starten.
    """
    stand = {"geladen": False}
    roh = []

    def merken(name):
        if stand["geladen"]:
            return
        # -3: merken -> Ersatzfunktion -> Aufrufer. Der Aufrufer ist gesucht.
        st = traceback.extract_stack()[-3]
        d = _pfad(st.filename)
        # Nur EIGENER Quelltext. aiohttp liest PYTHONASYNCIODEBUG, ssl liest
        # SSLKEYLOGFILE — beides beim Import und beides voellig richtig, denn
        # das sind Umgebungsschalter des Interpreters und stehen nie in der
        # .env. Ein Pruefer, der sie meldet, hat 6 Zeilen Rauschen und 0
        # Aussage; der echte Fall geht darin unter.
        if d.startswith("..") or os.path.isabs(d) or "<" in d:
            return
        roh.append((d, st.lineno, name))

    # ALLE DREI SCHREIBWEISEN abfangen. Nur os.getenv zu ersetzen reicht
    # nicht: os.environ.get() und os.environ[...] gehen daran vorbei, und
    # beide stehen im Bestand. Ein Pruefer, der zwei Drittel der Zugriffe
    # nicht sieht, meldet Ruhe, wo keine ist.
    echt_getenv = os.getenv
    umgebung = type(os.environ)
    echt_get, echt_item = umgebung.get, umgebung.__getitem__

    def getenv(k, d=None):
        merken(k)
        return echt_getenv(k, d)

    def get(self, k, d=None):
        merken(k)
        return echt_get(self, k, d)

    def item(self, k):
        merken(k)
        return echt_item(self, k)

    os.getenv, umgebung.get, umgebung.__getitem__ = getenv, get, item
    try:
        yield stand, roh
    finally:
        os.getenv = echt_getenv
        umgebung.get, umgebung.__getitem__ = echt_get, echt_item


def messen():
    """Bot starten und jede .env-Lesung VOR load_dotenv() mitschreiben.

    -> [(datei, zeile, name)] in Aufrufreihenfolge, Duplikate entfernt.
    """
    sys.path.insert(0, WURZEL)
    import test_smoke as TS          # dieselbe Stub-Schicht wie der Rauchtest

    os.chdir(tempfile.mkdtemp())
    os.environ.update(TELEGRAM_TOKEN="x", TELEGRAM_CHAT_ID="1",
                      DASHBOARD_PORT="0", LIVE_REACT_ENABLED="0",
                      DB_BACKEND="sqlite")
    TS._install_stubs()

    import dotenv
    echt_ld = dotenv.load_dotenv

    with mitschnitt() as (stand, roh):

        def ld(*a, **kw):
            stand["geladen"] = True
            return echt_ld(*a, **kw)

        dotenv.load_dotenv = ld
        try:
            import importlib.util as u
            spec = u.spec_from_file_location("bot",
                                             os.path.join(WURZEL, "bot.py"))
            modul = u.module_from_spec(spec)
            spec.loader.exec_module(modul)
        finally:
            dotenv.load_dotenv = echt_ld

    if not stand["geladen"]:
        raise SystemExit("importzeit: load_dotenv() lief ueberhaupt nicht — "
                         "der Messpunkt fehlt, das Ergebnis waere wertlos.")

    aus, gesehen = [], set()
    for d, z, n in roh:
        if (d, z, n) in gesehen:
            continue
        gesehen.add((d, z, n))
        aus.append((d, z, n))
    return aus


def _statisch():
    """AST-Blick: .env-Lesungen, die beim Import laufen (ohne Aufrufketten)."""
    def knoten(baum):
        treffer = []

        def geh(k, in_fn):
            for kind in ast.iter_child_nodes(k):
                if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.Lambda)):
                    geh(kind, True)
                    continue
                if not in_fn and _ist_env(kind):
                    treffer.append(kind.lineno)
                geh(kind, in_fn)

        geh(baum, False)
        return treffer

    liste = []
    for wurzel, ordner, dateien in os.walk(WURZEL):
        ordner[:] = [d for d in ordner
                     if d not in (".git", "node_modules", "__pycache__",
                                  ".venv", "_vendor")]
        for fn in dateien:
            if not fn.endswith(".py") or fn.startswith("test_"):
                continue
            liste.append(os.path.join(wurzel, fn))
    fehlt = quelle.pflicht_erfuellt(liste)
    if fehlt:
        raise quelle.QuelleUnlesbar(
            "Diese Dateien gehoeren in den Blick, stehen aber nicht in der "
            "Liste: " + ", ".join(fehlt))
    aus = {}
    for pfad, baum in quelle.baeume(liste):
        t = knoten(baum)
        if t:
            aus[pfad] = sorted(set(t))
    return aus


def _ist_env(k):
    if isinstance(k, ast.Call) and isinstance(k.func, ast.Attribute):
        if k.func.attr == "getenv":
            return True
        if (k.func.attr == "get" and isinstance(k.func.value, ast.Attribute)
                and k.func.value.attr == "environ"):
            return True
    if isinstance(k, ast.Subscript) and isinstance(k.value, ast.Attribute):
        return k.value.attr == "environ"
    return False


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true")
    p.add_argument("--statisch", action="store_true")
    a = p.parse_args(argv)

    if a.statisch:
        stand = _statisch()
        print("Modul-Ebene liest .env (nur woertlich, ohne Aufrufketten):")
        for d in sorted(stand, key=lambda d: -len(stand[d])):
            print(f"  {len(stand[d]):4d}  {d}")
        print("\nDas ist der SCHWACHE Blick. Fuer die Wahrheit ohne --statisch "
              "laufen lassen.")
        return 0

    treffer = messen()
    if not treffer:
        print("importzeit: OK — keine .env-Lesung vor load_dotenv()")
        return 0

    print(f"importzeit: {len(treffer)} .env-Lesung(en) VOR load_dotenv().")
    print("Diese Werte kommen NICHT aus der .env, sondern aus dem Default im "
          "Quelltext — egal, was der Betreiber eingetragen hat.\n")
    for d, z, n in treffer:
        print(f"  {d}:{z}   {n}")
    print("\n  Abhilfe: den Wert in einer FUNKTION lesen statt in einer "
          "Modul-Konstante. CLAUDE.md nennt _backend_conf() als Vorbild.")
    return 1 if a.sperre else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except quelle.QuelleUnlesbar as e:
        sys.exit(quelle.abbruch(e))
    except BrokenPipeError:
        os._exit(0)
