#!/usr/bin/env python3
"""tools/vertragscheck.py — v4.2-W66: Fenster fester Laenge finden und messen.

CLAUDE.md warnt vor dieser Bruchstelle mit Namen:

    „Ebenso die Fenster der Form `src[i:i + 3000]`: waechst die Funktion
     darueber hinaus, meldet der Test etwas als fehlend, das zwei Zeilen
     weiter unten steht."

Es sind **47 Stueck** in den beiden Vertrags-Suiten. Genau eines davon hat in
W62 zugeschlagen: `src[j:j + 4200]` reichte nicht mehr ueber den gewachsenen
Frame-Feeder und meldete „kein fester Takt", waehrend `stop.wait(takt)` zwei
Zeilen dahinter stand. Ein Vertrag, der bei gesundem Code faellt, kostet eine
Runde und lehrt, Vertragsbrueche nicht ernst zu nehmen.

ALLE 47 BLIND UMZUBAUEN WAERE SCHLIMMER ALS SIE ZU LASSEN. Ein zu grosses
Fenster laesst einen Vertrag durchgehen, der durchfallen muesste — in W64 hat
genau das eine Mutationsprobe still durchrutschen lassen, weil im selben Rumpf
ein zweiter Aufruf desselben Namens stand. Deshalb misst dieses Werkzeug erst,
welche Fenster ueberhaupt eng sind:

    --spielraum   jedes Fenster einzeln verkleinern und die Suite fahren.
                  Faellt sie, war das Fenster fast voll — dieses gehoert
                  umgebaut. Faellt sie nicht, hat es Luft und bleibt.

Das ist dieselbe Idee wie die Mutationsproben dieser Reihe, nur umgekehrt: statt
zu fragen „merkt der Vertrag einen Fehler?" fragt es „merkt der Vertrag, dass
sein Fenster schrumpft?".

    python3 tools/vertragscheck.py               Bericht
    python3 tools/vertragscheck.py --sperre      keine NEUEN Fenster (CI)
    python3 tools/vertragscheck.py --neu-grundlinie
    python3 tools/vertragscheck.py --spielraum   messen, welche eng sind
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tokenize

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUNDLINIE = os.path.join(WURZEL, ".claude", "vertrag_grundlinie.json")
SUITEN = ("test_nc_modules.py", "test_restream.py")

# src[i:i + 3000] und Verwandte. Zwei Zeichen Zahl aufwaerts: `s[i:i+1]` ist
# ein Zeichen-Zugriff und keine Fenster-Wette.
FENSTER = re.compile(r"(\w+)\[\s*(\w+)\s*:\s*\2\s*\+\s*(\d{2,})\s*\]")


def finde(pfad):
    """-> [(zeile, ausdruck, groesse)] — nur CODE, keine Prosa.

    Kommentare und Zeichenketten werden vorher geleert. Ohne das zaehlt der
    Pruefer jedes Fenster mit, das jemand in einem Docstring ERWAEHNT — und
    davon gibt es hier reichlich, weil CLAUDE.md und die Wellen-Kommentare
    die Form `src[i:i + 3000]` als abschreckendes Beispiel zitieren. Beim
    Bauen hat er sich prompt an seiner eigenen Dokumentation verschluckt und
    behauptet, die umgebauten Fenster seien zurueck.

    Mit tokenize, nicht mit einem Regex ueber Anfuehrungszeichen: ein
    Doppelkreuz in einer Zeichenkette und ein Anfuehrungszeichen in einem
    Kommentar bringen jede naive Trennung durcheinander.
    """
    quelle = io.open(os.path.join(WURZEL, pfad), encoding="utf-8").read()
    zeilen = quelle.splitlines()
    try:
        for t in tokenize.generate_tokens(io.StringIO(quelle).readline):
            if t.type not in (tokenize.COMMENT, tokenize.STRING):
                continue
            (z1, s1), (z2, s2) = t.start, t.end
            for z in range(z1, min(z2, len(zeilen)) + 1):
                if z - 1 >= len(zeilen):
                    break
                a = s1 if z == z1 else 0
                b = s2 if z == z2 else len(zeilen[z - 1])
                zeilen[z - 1] = (zeilen[z - 1][:a]
                                 + " " * (b - a) + zeilen[z - 1][b:])
    except (tokenize.TokenError, IndentationError):
        pass                     # unvollstaendige Datei: lieber roh zaehlen
    aus = []
    for nr, zeile in enumerate(zeilen, 1):
        for m in FENSTER.finditer(zeile):
            aus.append((nr, m.group(0), int(m.group(3))))
    return aus


def bericht():
    return {p: finde(p) for p in SUITEN}


def _lade():
    try:
        return json.load(io.open(GRUNDLINIE, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _spielraum(anteil=0.7):
    """Jedes Fenster einzeln verkleinern und die zugehoerige Suite fahren.

    Faellt sie, war weniger als `1 - anteil` Luft drin — das Fenster ist eng
    und der naechste Zuwachs im geprueften Quelltext bringt es zum Kippen.
    """
    eng, weit, kaputt = [], [], []
    for pfad, treffer in bericht().items():
        quelle = io.open(os.path.join(WURZEL, pfad), encoding="utf-8").read()
        for nr, ausdruck, groesse in treffer:
            klein = ausdruck.replace(str(groesse), str(max(20, int(groesse * anteil))))
            # JE ZEILE ersetzen, nicht global. Der erste Entwurf nahm
            # quelle.replace(ausdruck, klein) und uebersprang jeden Ausdruck,
            # der mehr als einmal in der Datei steht — das waren 17 von 47,
            # ein Drittel der Messung fiel unter den Tisch. Ausgerechnet die
            # haeufigen Formen (`src[i:i + 1400]` steht dreimal) blieben damit
            # ungemessen.
            zeilen = quelle.splitlines(keepends=True)
            if nr > len(zeilen) or ausdruck not in zeilen[nr - 1]:
                kaputt.append((pfad, nr, ausdruck, "Zeile passt nicht"))
                continue
            zeilen[nr - 1] = zeilen[nr - 1].replace(ausdruck, klein)
            io.open(os.path.join(WURZEL, pfad), "w",
                    encoding="utf-8").write("".join(zeilen))
            try:
                r = subprocess.run([sys.executable, pfad], cwd=WURZEL,
                                   capture_output=True, text=True,
                                   env=dict(os.environ, PYTHONUTF8="1"))
            finally:
                io.open(os.path.join(WURZEL, pfad), "w",
                        encoding="utf-8").write(quelle)
            (eng if r.returncode else weit).append((pfad, nr, ausdruck, groesse))
            print(("  ENG   " if r.returncode else "  Luft  ")
                  + f"{pfad}:{nr}  {ausdruck}", flush=True)
    return eng, weit, kaputt


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true")
    p.add_argument("--neu-grundlinie", action="store_true")
    p.add_argument("--spielraum", action="store_true")
    p.add_argument("--anteil", type=float, default=0.7,
                   help="auf welchen Anteil verkleinert wird (Vorgabe 0.7)")
    a = p.parse_args()

    stand = bericht()
    zahlen = {d: len(t) for d, t in stand.items()}

    if a.neu_grundlinie:
        os.makedirs(os.path.dirname(GRUNDLINIE), exist_ok=True)
        io.open(GRUNDLINIE, "w", encoding="utf-8").write(
            json.dumps({"fenster": zahlen, "summe": sum(zahlen.values())},
                       ensure_ascii=False, indent=2) + "\n")
        print(f"Grundlinie eingefroren: {sum(zahlen.values())} Fenster")
        return 0

    if a.spielraum:
        print(f"Jedes Fenster auf {int(a.anteil * 100)} % verkleinern und die "
              f"Suite fahren:\n")
        eng, weit, kaputt = _spielraum(a.anteil)
        print(f"\n  ENG (Vertrag faellt beim Schrumpfen): {len(eng)}")
        print(f"  Luft:                                 {len(weit)}")
        if kaputt:
            print(f"  nicht messbar (Ausdruck mehrdeutig):  {len(kaputt)}")
        if eng:
            print("\nDiese gehoeren auf einen mitwachsenden Anker:")
            for d, nr, ausdruck, _g in eng:
                print(f"  {d}:{nr}  {ausdruck}")
        return 0

    if a.sperre:
        basis = _lade()
        if basis is None:
            print("vertrag: KEINE GRUNDLINIE — einmal --neu-grundlinie laufen "
                  "lassen und die Datei mit einchecken.")
            return 1
        alt = basis.get("fenster", {})
        gewachsen = [(d, alt.get(d, 0), n) for d, n in sorted(zahlen.items())
                     if n > alt.get(d, 0)]
        if gewachsen:
            print("vertrag: NEUE Fenster fester Laenge. CLAUDE.md nennt sie "
                  "namentlich als Bruchstelle: waechst der gepruefte Quelltext "
                  "darueber hinaus, meldet der Vertrag etwas als fehlend, das "
                  "zwei Zeilen weiter unten steht.")
            for d, war, ist in gewachsen:
                print(f"  {d}: {war} -> {ist}")
            print("\n  Abhilfe: den Bereich mitwachsen lassen statt ihn zu "
                  "raten — bis zur naechsten Top-Level-Definition, oder mit "
                  "ast ueber den umschliessenden Rumpf.")
            return 1
        print(f"vertrag: OK — {sum(zahlen.values())} Fenster, keine neuen")
        return 0

    print(f"Fenster fester Laenge in den Vertrags-Suiten: "
          f"{sum(zahlen.values())}")
    for d, t in stand.items():
        print(f"\n  {d}: {len(t)}")
        for nr, ausdruck, _g in t:
            print(f"    {nr:6d}  {ausdruck}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os._exit(0)
