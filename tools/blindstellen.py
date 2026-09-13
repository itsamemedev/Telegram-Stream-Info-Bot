"""tools/blindstellen.py — v4.2-W81: Fehlerpfade, die nichts sagen.

════════════════════════════════════════════════════════════════════════
WARUM DIESES WERKZEUG
════════════════════════════════════════════════════════════════════════
`stillecheck.py` misst `except`-Bloecke ohne Meldung. Das ist die eine
Haelfte. Die andere Haelfte hat der Betreiber am 13.09. gemeldet:

    "whisper/transkript funktioniert immer noch nicht"
    "Chats koennen von online tiktok Usern geladen werden aber keine
     gueltigen streams"

Beides sind Funktionen, die **erfolgreich zurueckkehren** — mit einem
leeren Ergebnis. Kein Absturz, kein `except`, also faellt `stillecheck`
nicht. Der Grund steht trotzdem nirgends, weil der Rueckgabe eine Meldung
auf `log.debug` vorausgeht oder gar keine.

Ein `log.debug` erscheint in einem ERROR- oder INFO-Log **nie** (CLAUDE.md:
"Ein log.warning erscheint in einem ERROR-Log nie"). Fuer den Betreiber ist
ein Fehlerpfad auf `debug` deshalb dasselbe wie `pass`.

Gemessen im Resolver (bot.py `_resolve_via_webcast_api_v2`): neun
Rueckgaben mit leerem Ergebnis, davon sechs auf `log.debug` und drei ganz
ohne Meldung. Der Betreiber sieht "keine gueltigen streams" und hat keine
einzige Zeile, die sagt warum.

════════════════════════════════════════════════════════════════════════
WAS GEZAEHLT WIRD
════════════════════════════════════════════════════════════════════════
Eine **Blindstelle** ist ein `return`, das ein Misserfolgs-Ergebnis
liefert (None, "", [], {}, False, ("unknown", None) …), und auf dessen Weg
dorthin im selben Zweig keine Meldung auf `info`/`warning`/`error`/
`exception` steht.

Nicht gezaehlt wird:
  - die einzige/letzte Rueckgabe einer reinen Praedikatsfunktion
    (`def ist_x() -> bool`) — dort IST False das Ergebnis, kein Fehler
  - Funktionen, die gar keinen Erfolgs-Rueckgabewert haben
  - Aufraeumpfade und der Fehlerkanal selbst (dieselbe Regel wie
    stillecheck)

Der Bestand darf bleiben, er darf nur nicht **wachsen** — `--sperre`
faellt, sobald eine Blindstelle dazukommt. Genau wie bei W65/W66.
"""
from __future__ import annotations

import argparse
import ast
import json
import pathlib
import sys

# v4.2-W83: gemeinsamer Parser. Dieses Werkzeug hatte den weitesten Auffang
# von allen — `except Exception: return []`. Eine Datei, die nicht parst,
# meldete damit NULL Blindstellen, und null liest sich in der Summe wie ein
# sauberer Befund.
import quelle as _quelle

WURZEL = pathlib.Path(__file__).resolve().parent.parent
GRUNDLINIE = WURZEL / ".claude" / "blindstellen_grundlinie.json"

# Produktionscode — dieselbe Menge wie tools/monolith.py
def dateien():
    aus = [WURZEL / n for n in ("bot.py", "discordbot.py",
                                "telegramversand.py", "brain_bridge.py")]
    aus += sorted((WURZEL / "nc").rglob("*.py"))
    aus += sorted((WURZEL / "brain").glob("*.py"))
    return [p for p in aus if p.exists() and not p.name.startswith("test_")]


def flach(knoten):
    """Wie ast.walk, aber ohne Abstieg in verschachtelte Verzweigungen und
       Funktionen — nur der unbedingt ausgefuehrte Teil dieser Anweisung."""
    stapel = [knoten]
    while stapel:
        k = stapel.pop()
        yield k
        for kind in ast.iter_child_nodes(k):
            if isinstance(kind, (ast.If, ast.Try, ast.ExceptHandler,
                                 ast.For, ast.AsyncFor, ast.While,
                                 ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.Lambda, ast.ClassDef, ast.IfExp)):
                continue
            stapel.append(kind)


LAUTE = {"info", "warning", "warn", "error", "exception", "critical", "fatal"}

# Werte, die "es hat nicht geklappt" bedeuten
def ist_misserfolg(knoten) -> bool:
    if knoten is None:
        return True                              # nacktes `return`
    if isinstance(knoten, ast.Constant):
        return knoten.value in (None, "", 0, False)
    if isinstance(knoten, (ast.List, ast.Dict, ast.Set)):
        # leeres Literal
        if isinstance(knoten, ast.Dict):
            return not knoten.keys
        return not knoten.elts
    if isinstance(knoten, ast.Tuple):
        # Statuspaare wie ("live", info) / ("offline", None) / ("unknown", None).
        #
        # Die erste Fassung dieses Werkzeugs hat hier falsch gemessen und
        # `("offline", None)` als Blindstelle gemeldet. Das ist keine: TikTok
        # sagt "dieser Nutzer sendet nicht", und der Bot gibt das weiter — eine
        # DEFINITIVE Antwort, ueber die es nichts zu melden gibt. Wer sie laut
        # protokollierte, erzeugte bei jedem Poll-Durchlauf eine Zeile.
        #
        # Massgeblich ist deshalb der Status-String, nicht die leere Nutzlast
        # daneben: nur ein Ergebnislos-Marker ist ein Fehlerpfad.
        if not knoten.elts:
            return True
        kopf = knoten.elts[0]
        if isinstance(kopf, ast.Constant) and isinstance(kopf.value, str):
            return kopf.value in ("", "unknown", "fail", "error", "ratelimited")
        return all(ist_misserfolg(e) for e in knoten.elts)
    return False


# Je Datei: Namen von Funktionen, deren Rumpf selbst laut meldet. Ein Aufruf
# so einer Funktion IST eine Meldung — sonst zaehlt das Werkzeug jeden
# ausgelagerten Meldekanal (`_loop_fehler`, `_alert`, `_resolver_stumm`) als
# Blindstelle und treibt den Bestand dazu, ueberall wieder rohe log-Zeilen
# hinzuschreiben statt die gedrosselten Kanaele zu benutzen.
#
# Bewusst nur EINE Ebene tief und nur dateiweit: das genuegt fuer die
# Helfer des Bestands und laesst sich nicht dadurch aushebeln, dass man
# eine leere Funktion dazwischenschiebt — die meldet ja nicht laut.
LAUTE_HELFER: set = set()


def sammle_laute_helfer(baum) -> set:
    """Reine MELDEKANAELE der Datei — nicht jede Funktion, die irgendwo loggt.

       Die erste Fassung hat hier zu grosszuegig gemessen: sie nahm jede
       Funktion mit einem lauten Log auf, und damit galt ein Aufruf von
       `_resolve_via_webcast_api_v2` als Meldung — obwohl die Funktion nur im
       ERFOLGSFALL loggt. Genau der Fehlerpfad, um den es geht, wurde so
       weggerechnet.

       Ein Meldekanal ist deshalb eine Funktion, die laut loggt UND kein
       Ergebnis liefert (`_loop_fehler`, `_alert`, `_resolver_stumm`). Wer ein
       Ergebnis zurueckgibt, ist Fachlogik: dass sie irgendwo eine Zeile
       schreibt, sagt nichts ueber DIESEN Rueckgabepfad."""
    aus = set()
    for fn in ast.walk(baum):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        hat_laut = False
        liefert = False
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                    and n.func.attr in LAUTE:
                hat_laut = True
            if isinstance(n, ast.Return) and n.value is not None:
                liefert = True
        if hat_laut and not liefert:
            aus.add(fn.name)
    return aus


def meldet_laut(knoten) -> bool:
    """Steht in DIESER Anweisung ein Log-Aufruf auf info oder lauter?

       Bewusst FLACH: es wird nicht in verschachtelte Verzweigungen
       abgestiegen. Der Grund ist ein Messfehler der ersten Fassung — sie
       benutzte `ast.walk`, und damit galt ein `log.warning` in einem
       BELIEBIGEN frueheren `if`-Zweig als Meldung fuer jeden spaeteren
       Rueckgabepfad desselben Blocks. Eine einzige Mutation liess dadurch
       acht Blindstellen verschwinden statt einer.

       Gefragt ist aber: laeuft auf dem Weg zu DIESEM `return` garantiert
       eine Meldung? Ein Log in einem Zweig, den dieser Pfad nicht nimmt,
       beantwortet das mit nein. Deshalb zaehlen nur Anweisungen, die
       unbedingt ausgefuehrt werden."""
    for n in flach(knoten):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr in LAUTE:
                return True
        # eigene Meldekanaele des Bestands
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id in ("_loop_fehler", "_alert", "log_event", "_warn",
                             "melde", "_melde") or n.func.id in LAUTE_HELFER:
                return True
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr in ("_loop_fehler", "log_event", "melde"):
                return True
    return False


def praedikat(fn) -> bool:
    """Reine Ja/Nein-Funktion? Dann ist False ein Ergebnis, kein Fehler."""
    name = fn.name.lower()
    if name.startswith(("ist_", "is_", "hat_", "has_", "kann_", "can_",
                        "darf_", "braucht_", "sollte_", "should_")):
        return True
    r = fn.returns
    if isinstance(r, ast.Name) and r.id == "bool":
        return True
    return False


def returns_von(fn):
    """Alle `return`-Knoten DIESER Funktion, ohne verschachtelte Definitionen.

       Als eigene Funktion statt als Closure in der Schleife: eine Closure
       ueber `rets` bindet die Schleifenvariable und ist genau das Muster,
       das ruff mit B023 meldet — hier harmlos, weil sofort aufgerufen, aber
       eine Zeitbombe, sobald jemand den Aufruf verschiebt."""
    aus = []
    stapel = [fn]
    while stapel:
        k = stapel.pop()
        for kind in ast.iter_child_nodes(k):
            if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.Lambda, ast.ClassDef)):
                continue
            if isinstance(kind, ast.Return):
                aus.append(kind)
            stapel.append(kind)
    return aus


def sammle(pfad: pathlib.Path, baum=None):
    """-> [(datei, zeile, funktion)]

    v4.2-W83: parst ueber tools/quelle.py und wirft QuelleUnlesbar, statt
    eine unlesbare Datei als "null Blindstellen" zu verbuchen.
    """
    if baum is None:
        baum = _quelle.parse(pfad)
    rel = str(pfad.relative_to(WURZEL)).replace("\\", "/")
    global LAUTE_HELFER
    LAUTE_HELFER = sammle_laute_helfer(baum)
    aus = []

    for fn in ast.walk(baum):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if praedikat(fn):
            continue
        rets = returns_von(fn)
        if not rets:
            continue
        # hat die Funktion ueberhaupt einen Erfolgsrueckgabewert?
        if not any(not ist_misserfolg(r.value) for r in rets):
            continue
        # Zweig-Kontext je return: der umschliessende Block
        eltern = {}
        for n in ast.walk(fn):
            for k in ast.iter_child_nodes(n):
                eltern[k] = n
        for r in rets:
            if not ist_misserfolg(r.value):
                continue
            # Aufwaerts bis zum naechsten Verzweigungsknoten und dort pruefen
            laut = False
            k = r
            tiefe = 0
            while k is not None and tiefe < 6:
                p = eltern.get(k)
                if p is None:
                    break
                if isinstance(p, (ast.If, ast.Try, ast.ExceptHandler,
                                  ast.For, ast.While, ast.With)):
                    # Geschwister im selben Block vor dem return
                    for feld in ("body", "orelse", "finalbody"):
                        for stmt in getattr(p, feld, []) or []:
                            if getattr(stmt, "lineno", 0) <= r.lineno and meldet_laut(stmt):
                                laut = True
                    if laut:
                        break
                    tiefe += 1
                k = p
            if not laut:
                # auch direkte Geschwister auf Funktionsebene pruefen
                for stmt in fn.body:
                    if getattr(stmt, "lineno", 0) <= r.lineno and meldet_laut(stmt):
                        laut = True
                        break
            if not laut:
                aus.append((rel, r.lineno, fn.name))
    return aus


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sperre", action="store_true",
                    help="faellt, wenn mehr Blindstellen als in der Grundlinie")
    ap.add_argument("--setze-grundlinie", action="store_true")
    ap.add_argument("--datei", help="nur diese Datei zeigen")
    args = ap.parse_args()

    liste = dateien()
    fehlt = _quelle.pflicht_erfuellt(liste)
    if fehlt:
        raise _quelle.QuelleUnlesbar(
            "Diese Dateien gehoeren in die Messung, stehen aber nicht in der "
            "Liste: " + ", ".join(fehlt))
    alle = []
    for p, baum in _quelle.baeume(liste):
        alle.extend(sammle(WURZEL / p, baum))

    proDatei = {}
    for rel, ln, fn in alle:
        proDatei.setdefault(rel, []).append((ln, fn))

    if args.datei:
        for ln, fn in sorted(proDatei.get(args.datei, [])):
            print(f"{args.datei}:{ln}  {fn}")
        print(f"\n{len(proDatei.get(args.datei, []))} Blindstellen in {args.datei}")
        return 0

    gesamt = len(alle)
    print(f"Blindstellen (stumme Misserfolgs-Rueckgaben): {gesamt}\n")
    for rel in sorted(proDatei, key=lambda r: -len(proDatei[r]))[:15]:
        print(f"  {len(proDatei[rel]):5d}  {rel}")

    if args.setze_grundlinie:
        GRUNDLINIE.parent.mkdir(parents=True, exist_ok=True)
        GRUNDLINIE.write_text(json.dumps({"gesamt": gesamt}, indent=2) + "\n",
                              encoding="utf-8")
        print(f"\nGrundlinie gesetzt: {gesamt}")
        return 0

    if args.sperre:
        if not GRUNDLINIE.exists():
            print("\nKeine Grundlinie — erst --setze-grundlinie laufen lassen.")
            return 1
        basis = json.loads(GRUNDLINIE.read_text(encoding="utf-8"))["gesamt"]
        if gesamt > basis:
            print(f"\nSPERRE: {gesamt} Blindstellen, Grundlinie {basis} "
                  f"(+{gesamt - basis}). Ein Fehlerpfad ohne Meldung ist fuer "
                  f"den Betreiber dasselbe wie `pass`.")
            return 1
        if gesamt < basis:
            print(f"\nGrundlinie {basis} liegt UEBER dem Bestand {gesamt} — "
                  f"nachziehen mit --setze-grundlinie.")
            return 1
        print(f"\nOK: {gesamt} == Grundlinie {basis}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except _quelle.QuelleUnlesbar as e:
        sys.exit(_quelle.abbruch(e))
