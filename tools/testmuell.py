#!/usr/bin/env python3
"""tools/testmuell.py — v4.2-W90: haelt die Vertragssuiten davon ab, die
Platte zu fuellen.

════════════════════════════════════════════════════════════════════════
WARUM DIESES WERKZEUG
════════════════════════════════════════════════════════════════════════
Die Suiten legten 35 temporaere Verzeichnisse an und raeumten drei davon
weg. Auf der Maschine, auf der W89 entstand, waren nach einem Tag Arbeit
5093 Verzeichnisse mit rund 30 GB aufgelaufen, und die Pruefkette brach
mitten im Lauf ab:

    /dev/vda  252G  38G  1.1M  100% /
    OSError: [Errno 28] No space left on device

Kein Vertrag war rot, keine Sperre fiel — es ging nur nichts mehr. In der
CI faellt das nie auf: ein Lauf, frischer Container, danach ist die
Maschine weg. Genau deshalb konnte es unbemerkt wachsen, und genau deshalb
braucht es eine Sperre statt eines Vorsatzes.

Gemessen wird zweierlei, beides mit Grenze NULL — wie bei `importzeit` und
anders als bei den Ratschen aus W65/W66, denn hier gibt es keinen Bestand
zu dulden, sondern einen behobenen Zustand zu halten:

  (1) `mkdtemp()` in einer Suite. Wer so ein Verzeichnis anlegt, raeumt es
      nicht weg — 32 von 35 Fundstellen haben es nicht getan. `pruefhilfen
      .verzeichnis()` registriert es und loescht es per atexit, auch nach
      einem gefallenen Vertrag.

  (2) Ein Schreibvorgang ab 1 MiB aus einem konstanten Bytes-Muster. Der
      Kostentreiber war eine einzige Zeile:

          f.write(b"\\0" * (300 * 1024 * 1024))    # 300 MB (sparse)

      Der Kommentar sagt „sparse", der Code ist das Gegenteil: erst ein
      300-MB-Objekt im RAM, dann 300 MB echte Nullen auf die Platte —
      0,31 s und +300 MB RSS je Lauf, fuer eine Zahl, die
      `os.path.getsize()` auch von einer Datei mit bloss gesetzter Groesse
      liefert. `pruefhilfen.attrappe()` nutzt `truncate()`: gemessen 0,000 s
      und 0 statt 614.400 belegten Bloecken.

Wer wirklich Bytes braucht — weil der gepruefte Code den Inhalt liest und
nicht die Groesse —, traegt die Fundstelle unten in AUSNAHMEN ein, mit
Begruendung. Eine leere Liste ist hier der Normalfall, kein Versaeumnis.
"""

import argparse
import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quelle as _quelle                                       # noqa: E402

# Die Suiten, die die Pflicht-Pruefkette faehrt. Alle vier muessen in der
# Messung stecken: ein Glob ins Leere laesst die Sperre gruen melden, ohne
# nachgesehen zu haben — der Fehler, den W83 in vier Werkzeugen gefunden hat.
SUITEN = ["test_nc_modules.py", "test_restream.py", "test_smoke.py",
          "test_m2_bridge.py"]

# Das Modul, das die beiden Helfer traegt — dort sind mkdtemp und truncate
# nicht Befund, sondern Behebung.
ERLAUBT = {"pruefhilfen.py"}

# Fundstellen, die echte Bytes brauchen: (Datei, Zeile) -> Begruendung.
AUSNAHMEN = {}

MIB = 1024 * 1024
GRENZE = MIB          # ab hier lohnt die Attrappe; darunter ist es Rauschen


# Die Rechenarten, die in einer Groessenangabe vorkommen. Bewusst knapp:
# was hier fehlt, wird als "nicht entscheidbar" behandelt und nicht geraten.
_RECHNEN = {
    ast.Mult: lambda a, b: a * b,
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Pow: lambda a, b: a ** b if 0 <= b <= 64 else None,
    ast.LShift: lambda a, b: a << b if 0 <= b <= 64 else None,
}


def _wert(knoten):
    """Der konstante Wert eines Ausdrucks, oder None.

    `300 * 1024 * 1024` steht als verschachtelter BinOp im Baum, nicht als
    Zahl — ohne Auswertung findet die Sperre genau die Schreibvorgaenge
    nicht, die gross genug sind, um wehzutun.

    `ast.literal_eval` kann das NICHT: es erlaubt `+` und `-` nur fuer
    komplexe Zahlen und lehnt jede Multiplikation ab. Der erste Entwurf
    dieses Werkzeugs benutzte es trotzdem — und liess die 300-MB-Zeile
    durch, fuer die es gebaut wurde. Gefangen hat das die Mutationsprobe,
    nicht das Nachdenken. Deshalb hier eine eigene, sehr kleine Auswertung:
    Zahlen, Bytes, und die fuenf Rechenarten oben. Kein `eval`.
    """
    if isinstance(knoten, ast.Constant):
        return knoten.value
    if isinstance(knoten, ast.BinOp):
        rechne = _RECHNEN.get(type(knoten.op))
        if rechne is None:
            return None
        links, rechts = _wert(knoten.left), _wert(knoten.right)
        if not isinstance(links, int) or not isinstance(rechts, int):
            return None
        try:
            return rechne(links, rechts)
        except (ArithmeticError, ValueError):
            return None
    return None


def finde(baum):
    """-> (mkdtemp-Zeilen, [(Zeile, Bytes)])"""
    tmp, gross = [], []
    for k in ast.walk(baum):
        if (isinstance(k, ast.Call) and isinstance(k.func, ast.Attribute)
                and k.func.attr == "mkdtemp"):
            tmp.append(k.lineno)
        # f.write(b"..." * N) — das Muster, das 300 MB gekostet hat.
        if (isinstance(k, ast.Call) and isinstance(k.func, ast.Attribute)
                and k.func.attr == "write" and len(k.args) == 1
                and isinstance(k.args[0], ast.BinOp)
                and isinstance(k.args[0].op, ast.Mult)):
            bo = k.args[0]
            muster = _wert(bo.left)
            if not isinstance(muster, bytes):
                continue
            mal = _wert(bo.right)
            if not isinstance(mal, int):
                continue                 # variable Groesse: nicht entscheidbar
            n = len(muster) * mal
            if n >= GRENZE:
                gross.append((k.lineno, n))
    return tmp, gross


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--sperre", action="store_true",
                   help="Exitcode 1, sobald eine Fundstelle existiert")
    args = p.parse_args()

    pfade = [_quelle.WURZEL / n for n in SUITEN]
    fehlt = [n for n, pf in zip(SUITEN, pfade) if not pf.is_file()]
    if fehlt:
        raise _quelle.QuelleUnlesbar(
            "Diese Suiten fehlen und wurden NICHT geprueft: %s\n"
            "Umbenannt? Dann diese Liste nachziehen — eine Sperre, die ins "
            "Leere zeigt, meldet gruen, ohne nachgesehen zu haben."
            % ", ".join(fehlt))

    befunde = []
    for pfad, baum in _quelle.baeume(pfade):
        rel = os.path.basename(str(pfad))
        if rel in ERLAUBT:
            continue
        tmp, gross = finde(baum)
        for ln in tmp:
            if (rel, ln) in AUSNAHMEN:
                continue
            befunde.append((rel, ln, "mkdtemp() — nimm pruefhilfen.verzeichnis()"))
        for ln, n in gross:
            if (rel, ln) in AUSNAHMEN:
                continue
            befunde.append((rel, ln, "schreibt %.0f MiB echt — nimm "
                                     "pruefhilfen.attrappe()" % (n / MIB)))

    if not befunde:
        print("testmuell: OK — die %d Suiten legen nichts an, was liegen "
              "bleibt, und schreiben nichts ab %d MiB" % (len(SUITEN),
                                                          GRENZE // MIB))
        return 0

    print("testmuell: %d Fundstelle(n)\n" % len(befunde))
    for rel, ln, was in sorted(befunde):
        print("  %s:%d  %s" % (rel, ln, was))
    if args.sperre:
        print("\nSPERRE: Grenze ist null. Eine Suite, die Verzeichnisse "
              "liegen laesst, fuellt die Platte des Entwicklers — gemessen "
              "5093 Verzeichnisse und 30 GB an einem Tag, bis die "
              "Pruefkette mit ENOSPC abbrach.")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except _quelle.QuelleUnlesbar as e:
        sys.exit(_quelle.abbruch(e))
