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
import struct
import threading

log = logging.getLogger("TikTokBot")

NAME = "pausenbild"
# Endung je Art. Geprüft wird an den Kopfbytes, nicht an der Endung: eine
# umbenannte Datei anderen Formats liesse ffmpeg erst beim Sendestart scheitern.
ARTEN = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff"}
MAX_BYTES = 8 * 1024 * 1024
# Längste Kante. Der Füller dekodiert das Bild nur einmal (die loop-Stufe steht
# hinter scale, nc/restreamcmd.fueller), aber dieses eine Mal voll: ein
# 20000×20000-Bild sind 1,6 GB RGBA im Speicher des Füllers — auf einer Box,
# die nebenbei aufnimmt und sendet.
MAX_KANTE = 8192

_KONF = {"ordner": None, "vorgabe": None}
# Zwei Uploads zugleich (zwei Deck-Tabs) dürfen sich nicht gegenseitig die
# Datei unter dem os.replace wegräumen.
_SCHREIBSPERRE = threading.Lock()


def _t(s):
    """Markiert Benutzertext für tools/i18n_extract.py (MARKIERT). Übersetzt
    wird in der Route (nc/routes/restream.py), und ein Grund mit Platzhaltern
    wird dort NACH der Übersetzung gefüllt — wie in nc/mcpdienste.py. Hier
    bleibt der Text deutsch, weil er auch ins Log geht."""
    return s


class BildUngueltig(ValueError):
    """Ein hochgeladenes Pausenbild, das nicht gesendet werden kann.

    `grund` ist der deutsche Satz (Katalogschlüssel), `werte` die Platzhalter
    — übersetzt wird an der Route, nicht hier (nc/ bleibt ohne Anfrage)."""

    def __init__(self, grund, **werte):
        super().__init__(grund.format(**werte) if werte else grund)
        self.grund = grund
        self.werte = werte


def configure(ordner=None, vorgabe=None):
    """Ablageort des eigenen Bilds (der Bot: RECORDINGS_DIR/pausenbild) und
    die Vorgabe (RESTREAM_AVATAR) — die Deck-Routen wählen damit dasselbe Bild
    wie der Füller, ohne den Bot zu fragen."""
    _KONF["ordner"] = ordner
    _KONF["vorgabe"] = vorgabe


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

    `vorgabe` ist der AZRAEL-Avatar des Bots (ohne Angabe der aus
    configure()). Fehlt auch er, sendet der Füller die einfarbige Fläche — ein
    Pausenbild, das ffmpeg nicht öffnen kann, beendete den Füller, und ohne
    Füller verhungert der Sender."""
    pfad = eigenes()
    if pfad:
        return pfad, "eigen"
    vorgabe = vorgabe or _KONF["vorgabe"]
    if vorgabe and os.path.isfile(vorgabe):
        return os.path.abspath(vorgabe), "vorgabe"
    return None, "flaeche"


def _jpeg_masse(daten):
    """Breite und Höhe aus dem ersten SOF-Segment einer JPEG-Datei.

    Die Segmente werden der Reihe nach übersprungen (Länge steht je Segment im
    Kopf); SOF0…SOF15 tragen die Maße, außer C4 (Huffman), C8 (reserviert)
    und CC (Arithmetik) — die liegen im selben Nummernbereich."""
    i = 2
    while i + 4 <= len(daten):
        if daten[i] != 0xFF:
            raise BildUngueltig(_t("Das JPEG ist beschädigt (Segment ohne Kennung)."))
        marke = daten[i + 1]
        if marke == 0xFF:                       # Füllbyte vor der Marke
            i += 1
            continue
        if marke == 0x01 or 0xD0 <= marke <= 0xD8:   # Marken ohne Länge
            i += 2
            continue
        laenge = struct.unpack(">H", daten[i + 2:i + 4])[0]
        if 0xC0 <= marke <= 0xCF and marke not in (0xC4, 0xC8, 0xCC):
            if i + 9 > len(daten):
                break
            hoehe, breite = struct.unpack(">HH", daten[i + 5:i + 9])
            return breite, hoehe
        if marke == 0xDA:                       # Bilddaten ohne Kopf davor
            break
        i += 2 + laenge
    raise BildUngueltig(_t("Im JPEG stehen keine Bildmaße — die Datei ist abgeschnitten oder beschädigt."))


def masse(daten):
    """-> (endung, breite, hoehe) eines PNG oder JPEG, aus den Bytes gelesen.

    Wirft BildUngueltig mit dem Grund. Geprüft wird hier, nicht erst beim
    Senden: ein Bild, das ffmpeg nicht öffnen kann, beendet den Füller bei
    jedem Neustart wieder, und die Sendung zeigt dann gar nichts statt
    AZRAEL."""
    daten = bytes(daten or b"")
    if not daten:
        raise BildUngueltig(_t("Keine Datei im Upload."))
    if len(daten) > MAX_BYTES:
        raise BildUngueltig(_t("Das Bild ist {mb} MB groß, erlaubt sind {max} MB."),
                            mb=round(len(daten) / 1048576, 1), max=MAX_BYTES // 1048576)
    endung = art(daten[:16])
    if not endung:
        raise BildUngueltig(_t("Nur PNG oder JPEG — die Datei ist keines von beiden."))
    try:
        if endung == ".png":
            if daten[12:16] != b"IHDR":
                raise BildUngueltig(_t("Das PNG ist beschädigt (kein IHDR-Kopf)."))
            breite, hoehe = struct.unpack(">II", daten[16:24])
        else:
            breite, hoehe = _jpeg_masse(daten)
    except struct.error:
        raise BildUngueltig(_t("Das Bild ist abgeschnitten — der Kopf ist unvollständig.")) from None
    if not breite or not hoehe:
        raise BildUngueltig(_t("Das Bild hat keine Fläche ({b}×{h})."), b=breite, h=hoehe)
    if max(breite, hoehe) > MAX_KANTE:
        raise BildUngueltig(_t("Das Bild ist {b}×{h} Pixel groß, erlaubt sind höchstens {max} je Kante."),
                            b=breite, h=hoehe, max=MAX_KANTE)
    return endung, breite, hoehe


def speichern(daten):
    """Ein geprüftes Bild als eigenes Pausenbild ablegen. -> (pfad, breite, hoehe).

    Atomar: erst eine Nebendatei, dann os.replace. Ein abgebrochener Upload
    hinterlässt so nie ein halbes Bild, das eigenes() für gültig hielte — sein
    Kopf stimmte ja. Die Datei der anderen Endung geht VOR dem Tausch: eigenes()
    prüft .png vor .jpg, ein altes PNG neben einem neuen JPEG gewönne sonst
    still. Jeder Fehlschlag geht als OSError an den Aufrufer, und die
    Nebendatei geht mit — liegen bleibt nie ein halbes Bild."""
    endung, breite, hoehe = masse(daten)
    with _SCHREIBSPERRE:
        os.makedirs(ordner(), exist_ok=True)
        ziel = os.path.join(ordner(), NAME + endung)
        neben = "%s.%d.neu" % (ziel, threading.get_ident())
        try:
            with open(neben, "wb") as f:
                f.write(daten)
                f.flush()
                os.fsync(f.fileno())
            for andere in ARTEN:
                alt = os.path.join(ordner(), NAME + andere)
                if andere != endung and os.path.exists(alt):
                    os.remove(alt)
            os.replace(neben, ziel)
        finally:
            if os.path.exists(neben):
                os.remove(neben)
    log.info("Pausenbild: eigenes Bild gespeichert (%s, %d×%d, %d KB).",
             endung[1:].upper(), breite, hoehe, len(daten) // 1024)
    return ziel, breite, hoehe


def entfernen() -> int:
    """Das eigene Pausenbild löschen — danach gilt wieder die Vorgabe.
    -> Zahl der gelöschten Dateien. Ein OSError geht an den Aufrufer: wer
    „zurückgesetzt" meldet und das Bild weiter sendet, hat gelogen."""
    weg = 0
    with _SCHREIBSPERRE:
        for endung in ARTEN:
            pfad = os.path.join(ordner(), NAME + endung)
            if os.path.exists(pfad):
                os.remove(pfad)
                weg += 1
    if weg:
        log.info("Pausenbild: eigenes Bild entfernt — es gilt wieder die Vorgabe.")
    return weg


def lage() -> dict:
    """Was gerade als Pausenbild gilt, für das Deck. Ohne Pfad: der Ablageort
    ist Sache des Servers, das Deck braucht nur Herkunft, Format und Maße."""
    pfad, herkunft = waehlen()
    erg = {"herkunft": herkunft, "format": "", "breite": 0, "hoehe": 0,
           "bytes": 0, "geaendert": 0, "max_bytes": MAX_BYTES, "max_kante": MAX_KANTE}
    if not pfad:
        return erg
    try:
        with open(pfad, "rb") as f:
            kopf = f.read(256 * 1024)
        erg["bytes"] = os.path.getsize(pfad)
        erg["geaendert"] = int(os.path.getmtime(pfad))
        endung, erg["breite"], erg["hoehe"] = masse(kopf)
        erg["format"] = endung[1:].upper()
    except (OSError, BildUngueltig) as e:
        # Die Vorgabe darf größer oder anders gebaut sein als ein Upload —
        # das Bild bleibt gültig, nur die Maße fehlen dann in der Anzeige.
        log.info("Pausenbild: Maße von %s nicht lesbar (%s).", os.path.basename(pfad), e)
    return erg


def datei(pfad):
    """-> (pfad, mimetype) eines Bilds aus waehlen(), für die Vorschau im Deck;
    (None, None), wenn es sich nicht lesen lässt (gemeldet). Der Pfad stammt
    nie aus der Anfrage — ob überhaupt ein Bild gilt, fragt der Aufrufer
    waehlen(), denn die Fläche ist eine Lage und kein Fehler."""
    try:
        with open(pfad, "rb") as f:
            endung = art(f.read(16))
    except OSError as e:
        log.warning("Pausenbild %s nicht lesbar (%s).", pfad, e)
        return None, None
    # abspath: Flask löst einen relativen Pfad in send_file gegen den Ordner
    # der App auf, nicht gegen das Arbeitsverzeichnis — RECORDINGS_DIR ist
    # relativ, und die Vorschau zeigte dann 404, obwohl gesendet wird.
    return (os.path.abspath(pfad),
            {".png": "image/png", ".jpg": "image/jpeg"}.get(endung, "application/octet-stream"))
