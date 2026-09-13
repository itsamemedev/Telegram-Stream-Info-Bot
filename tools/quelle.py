"""tools/quelle.py — v4.2-W83: die EINE Stelle, an der Produktionscode
geparst wird, und die einzige, die entscheiden darf, was beim Scheitern
passiert.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Fünf Werkzeuge zählen den Bestand und sperren sein Wachstum: monolith
(Riesenfunktionen), stillecheck (stille `except`), blindstellen (stumme
`return`), importzeit (.env vor load_dotenv), vertragscheck (feste Fenster).
Jedes davon hatte seine eigene Parse-Schleife, und jede endete gleich:

    try:
        baum = ast.parse(...)
    except (OSError, SyntaxError):
        continue                        # blindstellen sogar: except Exception

Das ist genau der stille `except`-Block, gegen den diese Werkzeuge gebaut
wurden — im Werkzeug selbst. Und er ist dort schlimmer als im Bot, denn er
dreht die Aussage der Messung um: `bot.py` sind 24.044 Zeilen und rund 650
Funktionen. Fällt die Datei aus der Messung, meldet nicht etwa eine Sperre
"ich konnte nicht nachsehen" — sie meldet einen **Fortschritt**.

Gemessen am 13.09. auf Python 3.11 (dort scheitert `ast.parse(bot.py)` an
PEP 701, f-string mit Backslash, Zeile 16235):

    stillecheck --sperre  ->  "OK — 733 stille Bloecke, –352 seit der
                               Grundlinie"                        Exit 0
    monolith   --sperre  ->  "OK — 100 Z: 22, 200 Z: 6 …"         Exit 0

    tatsaechlich (3.13):      1085 stille Bloecke
                              100 Z: 63, 200 Z: 16

Die Sperre meldet nicht nur "in Ordnung", sie meldet, dass 352 stille
Blöcke verschwunden seien. Wer das liest, hakt ab. Dass die CI 3.12/3.13
fährt und dort richtig misst, rettet nur die CI — jede lokale Prüfung auf
einem älteren Interpreter lügt, und ein Syntaxfehler in `bot.py` machte
**jede** Zählsperre leichter statt rot.

════════════════════════════════════════════════════════════════════════
DIE REGEL
════════════════════════════════════════════════════════════════════════
Eine Datei, die nicht gelesen werden kann, ist kein Grund weiterzuzählen.
Sie ist ein Grund abzubrechen — mit Exitcode 2, damit "ich konnte nicht
nachsehen" von "der Bestand ist gewachsen" (Exit 1) unterscheidbar bleibt.

Dazu die Gegenprobe, die den eigentlichen Schaden abfängt: `pflicht_erfuellt`
prüft, dass die grossen Dateien überhaupt in der Messung stecken. Ein
Tippfehler in einem Glob nimmt `bot.py` genauso lautlos aus der Zählung wie
ein Parse-Fehler — nur ohne Ausnahme, an der man ihn festmachen könnte.
"""

import ast
import io
import os
import pathlib
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent

# Ohne diese Dateien ist keine Bestandsmessung aussagekraeftig — bot.py allein
# ist rund die Haelfte des Produktionscodes. Wer hier etwas ergaenzt, macht die
# Pruefung schaerfer; wer etwas entfernt, macht sie blind.
PFLICHT = ("bot.py", "discordbot.py", "brain_bridge.py", "telegramversand.py")

# Ab hier parst ast.parse die f-strings aus bot.py (PEP 701). Steht in
# README.md als harte Mindestversion; hier noch einmal, weil die Fehlermeldung
# unten sonst nur "SyntaxError" saegt und niemand auf den Interpreter kommt.
MINDEST = (3, 12)


class QuelleUnlesbar(Exception):
    """Mindestens eine Produktionsdatei liess sich nicht parsen.

    Traegt die volle Erklaerung im Text — sie landet direkt im CI-Log, und
    dort hat niemand den Kontext dieses Moduls."""


def _relativ(pfad) -> str:
    p = pathlib.Path(pfad)
    try:
        return str(p.resolve().relative_to(WURZEL)).replace(os.sep, "/")
    except ValueError:
        return str(p).replace(os.sep, "/")


def parse(pfad):
    """Parst EINE Datei. -> ast.Module, oder QuelleUnlesbar.

    Kein Rueckgabewert None, kein leerer Baum: ein Aufrufer, der das Ergebnis
    einfach benutzt, soll den Fehler nicht versehentlich verschlucken koennen.
    """
    voll = pfad if os.path.isabs(str(pfad)) else os.path.join(WURZEL, str(pfad))
    rel = _relativ(voll)
    try:
        quelle = io.open(voll, encoding="utf-8").read()
    except OSError as e:
        raise QuelleUnlesbar(f"{rel}: nicht lesbar — {e}") from e
    try:
        return ast.parse(quelle, filename=rel)
    except SyntaxError as e:
        raise QuelleUnlesbar(
            f"{rel}:{e.lineno}: {e.msg}") from e


def baeume(pfade):
    """Parst alle Dateien. -> [(relativer Pfad, ast.Module)].

    Sammelt ALLE Fehler und wirft einmal — wer drei kaputte Dateien hat, will
    sie in einem Lauf sehen, nicht in dreien.
    """
    aus, kaputt = [], []
    for p in pfade:
        try:
            aus.append((_relativ(p), parse(p)))
        except QuelleUnlesbar as e:
            kaputt.append(str(e))
    if kaputt:
        raise QuelleUnlesbar(_erklaerung(kaputt))
    return aus


def _erklaerung(kaputt) -> str:
    zeilen = ["Produktionscode nicht lesbar — die Messung waere still zu "
              "NIEDRIG ausgefallen:", ""]
    zeilen += ["  " + k for k in kaputt]
    zeilen.append("")
    if sys.version_info < MINDEST:
        zeilen += [
            f"  Dieser Interpreter ist Python {sys.version_info.major}."
            f"{sys.version_info.minor}. NIGHTCRAWLER braucht mindestens "
            f"{MINDEST[0]}.{MINDEST[1]} — bot.py nutzt f-strings mit "
            "Backslash (PEP 701), die darunter schon beim Parsen sterben.",
            "  Abhilfe: python3.12 oder neuer benutzen. Die Zahlen aus einem "
            "aelteren Lauf sind wertlos, nicht bloss unvollstaendig.",
        ]
    else:
        zeilen += [
            "  Abhilfe: den Syntaxfehler beheben. Bis dahin misst KEINE der "
            "Sperren (monolith, stillecheck, blindstellen, importzeit) den "
            "Bestand vollstaendig — und alle melden dadurch zu gute Zahlen.",
        ]
    return "\n".join(zeilen)


def pflicht_erfuellt(gesehen):
    """Steckten die grossen Dateien ueberhaupt in der Messung? -> [fehlend]

    Gegen den Fall, den keine Ausnahme meldet: ein Glob, der ins Leere zeigt,
    eine Datei, die umbenannt wurde. Die Messung laeuft dann sauber durch und
    ist trotzdem wertlos.
    """
    da = {_relativ(g) for g in gesehen}
    return [n for n in PFLICHT
            if n not in da and (WURZEL / n).is_file()]


def abbruch(exc_oder_text) -> int:
    """Meldet den Grund auf stderr und liefert den Exitcode 2.

    ZWEI, nicht eins: "ich konnte nicht nachsehen" ist etwas anderes als "der
    Bestand ist gewachsen". Beides ist in der CI rot, aber nur eines davon
    behebt man im Code.
    """
    print(str(exc_oder_text), file=sys.stderr)
    return 2
