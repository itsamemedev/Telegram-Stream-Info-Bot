"""nc.schriftzeichen — v5.9-W203: nur Zeichen ins Sendebild, die die Schrift zeichnen kann.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Screenshot des Betreibers vom Sendebild: hinter fast jeder Chatzeile ein
Kaestchen — „Familia och nööö gute Besserung□", „Krankenhaus□". Das sind die
Emoji der Zuschauer. Das Sendebild schreibt ffmpeg mit drawtext in EINER
Schrift (RESTREAM_FONT, DejaVu), und drawtext kennt keinen Rueckfall auf eine
zweite Schrift: was DejaVu nicht hat, wird das Ersatzzeichen. Eine Emoji-
Schrift nachzuinstallieren hilft drawtext nicht — es fragt nur die eine.

Also werden die Zeichen herausgenommen, die die Schrift NICHT hat. Welche
das sind, sagt die Schrift selbst: `fc-query --format=%{charset}` liefert
ihre Zeichentabelle. Gibt es fc-query nicht, gilt eine vorsichtige Vermutung
(Emoji-Ebene, Variantenwaehler, Verbinder, private Zeichen) — sie nimmt
weniger heraus als die Tabelle, aber nie einen Buchstaben.

Gefragt wird einmal je Schrift und in einem eigenen Faden: die Overlay-
Dateien schreibt die Restream-Schleife jede Sekunde, und ein Unterprozess
dort haelt den Event-Loop an (W97). Bis die Tabelle da ist, gilt die
Vermutung.
"""

import bisect
import logging
import os
import re
import shutil
import subprocess
import threading

log = logging.getLogger(__name__)

# schrift -> Liste (von, bis) oder None (nicht lesbar); fehlt der Schluessel,
# laeuft die Abfrage noch oder hat nie begonnen.
_TABELLEN = {}
_LAUFEND = set()
_SPERRE = threading.Lock()

# Zeichen, die drawtext steuern oder die ein Umbruch braucht — nie entfernen.
_IMMER = {"\n", " "}


_BEREICH = re.compile(r"([0-9a-fA-F]+)(?:-([0-9a-fA-F]+))?")


def _bereiche(roh):
    """„20-7e a0-2e9 300" -> [(0x20, 0x7e), (0xa0, 0x2e9), (0x300, 0x300)].

    Ein Teil in unbekanntem Format verwirft die GANZE Tabelle (ValueError,
    der Aufrufer nennt den Grund): eine halbe Tabelle naehme alle Zeichen
    danach still aus dem Sendebild. Leere Ausgabe -> None."""
    aus = []
    for teil in str(roh or "").split():
        t = _BEREICH.fullmatch(teil)
        if t is None:
            raise ValueError("unbekanntes Format in der Zeichentabelle: %r" % teil[:20])
        a = int(t.group(1), 16)
        aus.append((a, int(t.group(2), 16) if t.group(2) else a))
    return sorted(aus) or None


def _abfragen(schrift):
    """fc-query fuer EINE Schrift; Ergebnis in _TABELLEN (auch None = nicht lesbar)."""
    tabelle, grund = None, ""
    prog = shutil.which("fc-query")
    if not prog:
        grund = "fc-query fehlt (Paket fontconfig)"
    else:
        try:
            r = subprocess.run([prog, "--format=%{charset}\\n", schrift],
                               capture_output=True, text=True, timeout=15)
            tabelle = _bereiche(r.stdout.splitlines()[0] if r.stdout else "")
            if tabelle is None:
                grund = "keine Zeichentabelle in der Ausgabe (rc=%s)" % r.returncode
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            grund = "%s: %s" % (type(e).__name__, e)
            log.debug("Sendebild: fc-query fuer %s gescheitert: %s", schrift, grund)
    with _SPERRE:
        _TABELLEN[schrift] = tabelle
        _LAUFEND.discard(schrift)
    if tabelle is None:
        # Kein Ausfall des Sendebilds — es gilt die Vermutung. Einmal je
        # Schrift sagen, warum, damit Kaestchen im Bild eine Erklaerung haben.
        log.info("Sendebild: Zeichentabelle von %s nicht lesbar (%s) — Emoji und "
                 "fremde Zeichen werden nur geschaetzt entfernt.", schrift, grund)


def vorbereiten(schrift):
    """Die Tabelle dieser Schrift im Hintergrund holen (einmal je Schrift)."""
    if not schrift:
        return
    with _SPERRE:
        if schrift in _TABELLEN or schrift in _LAUFEND:
            return
        _LAUFEND.add(schrift)
    threading.Thread(target=_abfragen, args=(schrift,), daemon=True,
                     name="schriftzeichen").start()


def tabelle(schrift):
    """Die Zeichentabelle, wenn schon bekannt — sonst None (dann gilt die Vermutung)."""
    with _SPERRE:
        return _TABELLEN.get(schrift)


def _in(cp, bereiche):
    """Liegt `cp` in einem der (sortierten) Bereiche? Binaere Suche: der
    letzte Bereich, der bei oder vor `cp` beginnt, muss ihn enthalten."""
    i = bisect.bisect_right(bereiche, (cp, 0x110000)) - 1
    return i >= 0 and bereiche[i][0] <= cp <= bereiche[i][1]


def vermutlich_unzeichenbar(ch) -> bool:
    """Ohne Tabelle: was keine Textschrift hat. Nie ein Buchstabe."""
    cp = ord(ch)
    return (cp >= 0x1F000                       # Emoji, Spielkarten, Domino, Flaggen-Buchstaben
            or 0xFE00 <= cp <= 0xFE0F           # Variantenwaehler (VS16 macht ❤ zu ❤️)
            or cp in (0x200D, 0x20E3)           # Verbinder, Tastenkappe
            or 0xE000 <= cp <= 0xF8FF           # private Zeichen
            or 0xF0000 <= cp)                   # private Ebenen, Tags


def zeichenbar(text, schrift=None) -> str:
    """`text` ohne die Zeichen, die `schrift` nicht hat.

    Steuerzeichen ausser dem Zeilenumbruch fallen immer weg — drawtext zeigt
    auch fuer ein Wagenruecklauf-Zeichen ein Kaestchen. Doppelte Leerzeichen,
    die dabei entstehen, bleiben: sie verschieben nichts, und eine Zeile, die
    sich zusammenzieht, waere ein zweiter Umbruch nach dem ersten."""
    if not text:
        return text or ""
    bereiche = tabelle(schrift) if schrift else None
    aus = []
    for ch in str(text):
        if ch in _IMMER:
            aus.append(ch)
            continue
        cp = ord(ch)
        if cp < 0x20 or 0x7F <= cp < 0xA0:
            continue
        if bereiche is not None:
            if _in(cp, bereiche):
                aus.append(ch)
        elif not vermutlich_unzeichenbar(ch):
            aus.append(ch)
    return "".join(aus)


def schrift_von(finder):
    """Die Schrift, die gerade gilt — `finder` ist ein Aufrufbares oder ein Pfad."""
    try:
        s = finder() if callable(finder) else finder
    except Exception as e:
        log.warning("Sendebild: Schrift nicht bestimmbar (%s: %s) — Zeichen werden "
                    "geschaetzt gefiltert.", type(e).__name__, e)
        return None
    return s if s and os.path.isfile(s) else None
