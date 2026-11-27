"""nc.pausenbild — v5.13: das Bild der Sendepause in der 24/7-Sendung.

Gewünscht vom Betreiber am 27.11.: „für die Zeit, wo kein getrackter User
live ist, ein Pausenbild, das in der Abwesenheit live gestreamt wird, bis der
nächste getrackte User live kommt" — im Standard- und im Text-Modus des
Restreams. Das Pausenbild ist der Füller der Sendebrücke (nc/sendebruecke.py)
und läuft durch denselben Sender wie die Quelle; jedes Overlay (html, text,
Studio, Burn-in) liegt deshalb auch über dem Pausenbild, ohne eigenen Weg.

Welches Bild, entschieden am 27.11.:

    1. ein eigenes, hochgeladenes Bild (`<ordner>/pausenbild.png|.jpg`)
    2. sonst AZRAEL (RESTREAM_AVATAR, Vorgabe azrael_avatar.png)
    3. sonst die einfarbige Fläche wie bis v5.12

Ohne Text im Bild: jeder Text im Sendebild wäre Benutzertext und müsste durch
die Übersetzung (Begründung aus W130). Wer „Gleich geht's weiter" zeigen
will, lädt ein Bild mit diesem Text hoch.

Das Modul liest nur Dateien und Kopfbytes — ffmpeg baut nc/restreamcmd, den
Ablageort reicht der Bot per configure() herein (unter RECORDINGS_DIR, wie die
OAuth-Speicher: der tägliche Aufräumer löscht dort nur Videodateien).
"""

import logging
import os

log = logging.getLogger("TikTokBot")

NAME = "pausenbild"
# Endung je Art. Geprüft wird an den Kopfbytes, nicht an der Endung: eine
# umbenannte Datei anderen Formats liesse ffmpeg erst beim Sendestart scheitern.
ARTEN = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff"}
MAX_BYTES = 8 * 1024 * 1024

_KONF = {"ordner": None}


def configure(ordner=None):
    """Ablageort des eigenen Bilds (der Bot: RECORDINGS_DIR/pausenbild)."""
    _KONF["ordner"] = ordner


def ordner() -> str:
    return _KONF["ordner"] or os.path.join("recordings", NAME)


def art(kopf) -> str:
    """Endung zu den ersten Bytes einer Datei: '.png', '.jpg' oder ''."""
    kopf = bytes(kopf or b"")
    return next((endung for endung, magie in ARTEN.items() if kopf.startswith(magie)), "")


def eigenes():
    """Pfad des eigenen Pausenbilds, oder None.

    Eine Datei, deren Kopf nicht zur Endung passt, zählt nicht — und wird
    gemeldet, weil der Betreiber sonst ein hochgeladenes Bild erwartet und
    AZRAEL sieht."""
    for endung in ARTEN:
        pfad = os.path.join(ordner(), NAME + endung)
        if not os.path.isfile(pfad):
            continue
        try:
            with open(pfad, "rb") as f:
                kopf = f.read(16)
        except OSError as e:
            log.warning("Pausenbild %s nicht lesbar (%s) — es gilt die Vorgabe.", pfad, e)
            continue
        if art(kopf) == endung:
            return pfad
        log.warning("Pausenbild %s ist kein %s-Bild (Kopf %s) — es gilt die Vorgabe.",
                    pfad, endung[1:].upper(), kopf[:8].hex())
    return None


def waehlen(vorgabe=None):
    """-> (pfad oder None, herkunft) mit herkunft 'eigen', 'vorgabe' oder 'flaeche'.

    `vorgabe` ist der AZRAEL-Avatar des Bots. Fehlt auch er, sendet der Füller
    die einfarbige Fläche — ein Pausenbild, das ffmpeg nicht öffnen kann,
    beendete den Füller, und ohne Füller verhungert der Sender."""
    pfad = eigenes()
    if pfad:
        return pfad, "eigen"
    if vorgabe and os.path.isfile(vorgabe):
        return os.path.abspath(vorgabe), "vorgabe"
    return None, "flaeche"
