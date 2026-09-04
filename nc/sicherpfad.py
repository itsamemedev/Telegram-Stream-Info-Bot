"""nc.sicherpfad — ein Riegel gegen Pfad-Ausbruch, überall derselbe.

WARUM DIESES MODUL, obwohl die Riegel schon da waren
════════════════════════════════════════════════════════════════════════
CodeQL meldet 241 offene Befunde, die grosse Mehrheit „Uncontrolled data
used in path expression". Nachgesehen tragen fast alle betroffenen Stellen
bereits eine Pruefung — nur jede in einer anderen Form:

    nc/updater.py       os.path.abspath + p.startswith(root + os.sep) + raise
    nc/routes/archive   os.path.basename + Zeichensatz-Regex (textmore)
    nc/updater.rollback os.path.basename + Praefix/Suffix-Erlaubnisliste
    nc/i18n             Mitgliedschaft in einem festen Tupel
    nc/routes/ops       Nachschlagen in einem festen Dict

Vier Formen fuer eine Frage. Das hat zwei Folgen, und beide sind teuer:

1. **Die statische Analyse erkennt keine davon als Riegel.** Sie sieht
   Anfragedaten in einem Pfadausdruck und meldet. 241 Meldungen, die
   niemand mehr einzeln liest — und in denen der eine echte Befund
   untergeht, wenn er kommt.
2. **Eine neue Stelle erbt keinen Riegel.** Wer eine Route dazuschreibt,
   muss die Regel kennen. Vier Vorbilder heissen: er sucht sich eins aus,
   oder keins.

Deshalb EINE Funktion, in EINER Form, und ein Vertrag, der neue Senken
ohne sie meldet. Der Sicherheitsgewinn liegt nicht darin, ein offenes Loch
zu schliessen — die meisten waren zu — sondern darin, dass der Riegel ab
jetzt sichtbar, gleich und pruefbar ist.

WAS DIE PRUEFUNG WIRKLICH LEISTET
════════════════════════════════════════════════════════════════════════
`realpath` statt `abspath`: nur `realpath` loest Symlinks auf. Ein Link
`archiv/raus -> /etc` besteht jede `abspath`-Pruefung und fuehrt trotzdem
nach /etc. Das ist der Fall, den `abspath` NICHT faengt und der in
CLAUDE.md unter „stille Fehlpfade" gemeint ist.

`commonpath` statt `startswith`: `/daten/archiv2` beginnt mit
`/daten/archiv`, liegt aber nicht darin. Ein `startswith` ohne den
angehaengten Trenner laesst genau das durch.
"""
import os
import re

# Was in einem Dateinamen stehen darf. Bewusst eng: alles andere wird zu
# einem Unterstrich. Der Punkt ist erlaubt (Endungen), die Auswertung von
# ".." uebernimmt sicherer_name selbst.
_ERLAUBT = re.compile(r"[^\w. \-()]", re.ASCII)
_MEHRFACH = re.compile(r"_+")


def sicherer_name(name, vorgabe="datei.bin"):
    """Ein Dateiname ohne Pfadanteil und ohne Sonderzeichen.

    `os.path.basename` zuerst: damit ist "../../etc/passwd" schon "passwd",
    bevor die Zeichenpruefung ueberhaupt laeuft. Danach bleibt kein "/"
    und kein "\\" mehr uebrig, den man wieder zusammensetzen koennte.
    """
    if not name:
        return vorgabe
    # Beide Trenner: ein Windows-Pfad in einem Upload-Namen ("..\\..\\x")
    # ueberlebt basename() auf Linux, weil dort "\\" ein normales Zeichen ist.
    roh = str(name).replace("\\", "/")
    basis = os.path.basename(roh).strip()
    basis = _ERLAUBT.sub("_", basis)
    basis = _MEHRFACH.sub("_", basis).strip("._- ")
    # "." und ".." sind nach dem Strippen leer, aber sicher ist sicher.
    if not basis or basis in (".", ".."):
        return vorgabe
    return basis


def unter(basis, pfad):
    """Liegt `pfad` wirklich innerhalb von `basis`? Symlinks aufgeloest."""
    try:
        b = os.path.realpath(basis)
        p = os.path.realpath(pfad)
        return p == b or os.path.commonpath([b, p]) == b
    except (ValueError, OSError):
        # ValueError: commonpath ueber verschiedene Laufwerke/Wurzeln.
        # Im Zweifel NEIN — ein Pfad, den wir nicht einordnen koennen, ist
        # keiner, den wir anfassen.
        return False


def sicher_join(basis, name, vorgabe="datei.bin"):
    """Genau EIN Pfad unterhalb von `basis`, aus einem fremden Namen.

    Zwei Riegel hintereinander, absichtlich doppelt:
    1. `sicherer_name` nimmt jeden Pfadanteil heraus.
    2. `unter` prueft das Ergebnis noch einmal am fertigen Pfad — das
       faengt Symlinks, die erst auf dem Dateisystem existieren.

    Wirft `ValueError`, wenn das Ergebnis ausbricht. Ein stiller Rueckfall
    auf einen Ersatzpfad waere hier falsch: der Aufrufer wuerde in eine
    Datei schreiben, die er nicht gemeint hat.
    """
    ziel = os.path.join(basis, sicherer_name(name, vorgabe))
    if not unter(basis, ziel):
        raise ValueError("Pfad verlaesst das Verzeichnis: %r" % (name,))
    return ziel


def pruefe_unter(basis, pfad, was="Pfad"):
    """Wie `unter`, wirft aber statt False zurueckzugeben.

    Fuer bestehende Pfade aus der Datenbank: die sind nicht vom Nutzer
    gebaut, koennen aber aus einer aelteren, laxeren Version stammen.
    """
    if not unter(basis, pfad):
        raise ValueError("%s liegt ausserhalb von %r: %r" % (was, basis, pfad))
    return os.path.realpath(pfad)
