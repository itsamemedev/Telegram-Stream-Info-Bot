#!/usr/bin/env python3
"""tools/tonspur_reparieren.py — v5.13: unlesbare Tonköpfe im Bestand reparieren.

Aufnahmen vom 21. bis 23.11. tragen eine AAC-Tonspur, deren Kopf ffmpeg nicht
öffnet („Error while opening decoder: Invalid data found"). Der Bot repariert
das seit v5.13 selbst — am Ende jeder Aufnahme und vor jedem Upload. Dieses
Werkzeug macht dasselbe für den ganzen Bestand auf einmal, ohne Bot:

    python3 tools/tonspur_reparieren.py recordings/             # reparieren
    python3 tools/tonspur_reparieren.py --nur-pruefen recordings/

Geändert werden je Datei nur die wenigen Bytes des Tonkopfs, gleiche Länge,
an Ort und Stelle (Begründung in nc/aacreparatur.py). Die alten Bytes stehen
in der Ausgabe. Ausgelassen werden Teil-Reste von Uploads und Dateien, an
denen eben noch geschrieben wurde (--alter-min, Vorgabe 10).

Exitcode: 0 alles gesund oder repariert, 1 mindestens eine Datei unrettbar
(bzw. mit --nur-pruefen: kaputt), 2 Aufruf falsch.
"""
import argparse
import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nc import aacreparatur as R          # noqa: E402
from nc import videoteil as V             # noqa: E402

ENDUNGEN = (".mp4", ".m4v", ".mov")


def dateien(pfade, alter_min):
    grenze = time.time() - alter_min * 60
    for pfad in pfade:
        if os.path.isfile(pfad):
            kandidaten = [pfad]
        else:
            kandidaten = [os.path.join(w, n) for w, _d, namen in os.walk(pfad) for n in namen]
        for p in sorted(kandidaten):
            if not p.lower().endswith(ENDUNGEN) or V.ist_rest(p) or ".tonprobe." in p:
                continue
            try:
                if os.path.getmtime(p) > grenze:
                    print("  übersprungen (eben noch geschrieben): %s" % p)
                    continue
            except OSError as e:
                print("  übersprungen (%s): %s" % (e, p))
                continue
            yield p


async def pruefen(p):
    try:
        R.tonkopf(p)
    except (R.KeinTonkopf, OSError, IndexError):
        return {"lage": "kein_ton"}
    fehler, _s = await R.dekodiert(p)
    return {"lage": "gesund" if not fehler else "kaputt", "grund": "; ".join(fehler[:2])}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pfade", nargs="+", help="Dateien oder Ordner")
    ap.add_argument("--nur-pruefen", action="store_true", help="nichts ändern, nur melden")
    ap.add_argument("--alter-min", type=float, default=10.0,
                    help="jüngere Dateien auslassen (Minuten, Vorgabe 10)")
    a = ap.parse_args(argv)
    zaehl = {}
    for p in dateien(a.pfade, a.alter_min):
        erg = asyncio.run(pruefen(p) if a.nur_pruefen else R.reparieren(p, wer="Werkzeug"))
        lage = erg.get("lage", "?")
        zaehl[lage] = zaehl.get(lage, 0) + 1
        if lage in ("gesund", "kein_ton"):
            continue
        zusatz = (" %s → %s" % (erg.get("alt"), erg.get("neu")) if lage == "repariert"
                  else " (%s)" % (erg.get("grund") or ""))
        print("  %-10s %s%s" % (lage, p, zusatz))
    print("Tonspuren: " + (", ".join("%s %d" % kv for kv in sorted(zaehl.items()))
                           or "keine Dateien"))
    return 1 if (zaehl.get("unrettbar") or zaehl.get("kaputt")) else 0


if __name__ == "__main__":
    sys.exit(main())
