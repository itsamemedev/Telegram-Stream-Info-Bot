"""tools/loopblocker.py — v4.2-W117: blockierende Aufrufe direkt im Event-Loop.

════════════════════════════════════════════════════════════════════════
WARUM DIESES WERKZEUG
════════════════════════════════════════════════════════════════════════
Jede grosse Stockung dieses Bestands hatte dieselbe Form: ein synchroner
Aufruf, der direkt in einer `async def` steht und damit den GANZEN Bot
anhaelt — nicht nur die eine Abfrage.

  W26/W29  `with db_conn()` in `_handle_single_tracking`: 30 bis 68 s
           Blockade unter Plattenlast, Discord trennt mit "heartbeat
           blocked". `db_async` ist seither der Weg — der Bestand hatte
           trotzdem weiter ueber fuenfzig solcher Stellen.
  W97      die Sperre eines Log-Handlers, bis 176 s.
  W117     `_intel_index_one` rechnete die Einbettungen einer ganzen
           Aufnahme auf dem Loop.

Gemessen wird, was sich im Syntaxbaum sicher erkennen laesst: ein Aufruf
aus der Liste `BLOCKIEREND`, dessen NAECHSTE umschliessende Funktion eine
`async def` ist. Eine verschachtelte `def _lauf(): with db_conn()`, die
per `asyncio.to_thread` laeuft, zaehlt damit richtig NICHT — sie ist genau
die Abhilfe.

Was das Werkzeug nicht sieht: eine synchrone Hilfsfunktion, die selbst
blockiert und aus einer `async def` gerufen wird. Dafuer gibt es zur
Laufzeit den Spaeher aus nc/looplag.py, der die Zeile nennt. Die beiden
ergaenzen sich: dieses hier haelt die sichtbare Klasse fest, der Spaeher
findet die unsichtbare.

Wie bei stillecheck (W65) und blindstellen (W81) darf der Bestand bleiben
— Telegram- und Discord-Befehle laufen selten, und jede Stelle einzeln
umzubauen waere Risiko ohne Nutzen. Er darf nur nicht WACHSEN.
"""
from __future__ import annotations

import argparse
import ast
import json
import pathlib
import sys

import quelle as _quelle

WURZEL = pathlib.Path(__file__).resolve().parent.parent
GRUNDLINIE = WURZEL / ".claude" / "loopblocker_grundlinie.json"

# Aufrufnamen, wie sie im Quelltext stehen. Ueber den Namen und nicht ueber
# den aufgeloesten Import: bot.py importiert `time as _time_mod` und
# `subprocess as _subprocess`, und eine Liste ohne diese Aliase haette die
# Haelfte uebersehen.
BLOCKIEREND = frozenset({
    "db_conn", "sqlite3.connect", "open",
    "time.sleep", "_time_mod.sleep", "_time.sleep",
    "subprocess.run", "subprocess.call", "subprocess.check_call",
    "subprocess.check_output", "_subprocess.run", "_subprocess.call",
    "_subprocess.check_call", "_subprocess.check_output",
    "requests.get", "requests.post", "requests.request", "requests.put",
    "urllib.request.urlopen", "urlopen",
    "shutil.copy", "shutil.copy2", "shutil.copyfile", "shutil.move",
    "shutil.rmtree", "os.walk",
})


def dateien():
    aus = [WURZEL / n for n in ("bot.py", "discordbot.py",
                                "telegramversand.py", "brain_bridge.py")]
    aus += sorted((WURZEL / "nc").rglob("*.py"))
    aus += sorted((WURZEL / "brain").glob("*.py"))
    return [p for p in aus if p.exists() and not p.name.startswith("test_")]


def _name(knoten):
    if isinstance(knoten, ast.Name):
        return knoten.id
    if isinstance(knoten, ast.Attribute):
        basis = _name(knoten.value)
        return (basis + "." + knoten.attr) if basis else None
    return None


def sammle(rel: str, baum) -> list:
    """-> [(datei, zeile, funktion, aufruf), …] fuer jeden blockierenden
       Aufruf, dessen naechste umschliessende Funktion async ist."""
    aus = []

    def lauf(knoten, umschl):
        for kind in ast.iter_child_nodes(knoten):
            neu = umschl
            if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef)):
                neu = kind
            elif isinstance(kind, ast.Lambda):
                neu = kind          # ein Lambda laeuft meist in to_thread
            if (isinstance(kind, ast.Call)
                    and isinstance(umschl, ast.AsyncFunctionDef)):
                n = _name(kind.func)
                if n in BLOCKIEREND:
                    aus.append((rel, kind.lineno, umschl.name, n))
            lauf(kind, neu)

    lauf(baum, None)
    return aus


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sperre", action="store_true",
                    help="faellt, wenn mehr Stellen als in der Grundlinie")
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
        alle.extend(sammle(str(p), baum))

    if args.datei:
        treffer = [a for a in alle if a[0] == args.datei]
        for rel, ln, fn, n in sorted(treffer):
            print(f"{rel}:{ln}  {fn}  {n}")
        print(f"\n{len(treffer)} blockierende Aufrufe in {args.datei}")
        return 0

    gesamt = len(alle)
    proDatei = {}
    for a in alle:
        proDatei[a[0]] = proDatei.get(a[0], 0) + 1
    print(f"Blockierende Aufrufe direkt in async def: {gesamt}\n")
    for rel in sorted(proDatei, key=lambda r: -proDatei[r])[:10]:
        print(f"  {proDatei[rel]:5d}  {rel}")

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
            print(f"\nSPERRE: {gesamt} blockierende Aufrufe im Loop, Grundlinie "
                  f"{basis} (+{gesamt - basis}). Ein synchroner Aufruf in einer "
                  f"async def haelt den GANZEN Bot an. Abhilfe: db_async(...) "
                  f"fuer die Datenbank, asyncio.to_thread(...) fuer alles "
                  f"andere. Die Stellen: --datei <pfad>.")
            return 1
        if gesamt < basis:
            print(f"\nGrundlinie {basis} liegt UEBER dem Bestand {gesamt} — "
                  f"nachziehen mit --setze-grundlinie.")
            return 1
        print(f"\nloopblocker: OK — {gesamt} == Grundlinie {basis}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except _quelle.QuelleUnlesbar as e:
        sys.exit(_quelle.abbruch(e))
