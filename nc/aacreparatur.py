"""nc.aacreparatur — v5.13: den Tonkopf einer Aufnahme neu schreiben.

════════════════════════════════════════════════════════════════════════
DER BEFUND (Log vom 26./27.11.)
════════════════════════════════════════════════════════════════════════
Aufnahmen vom 21. bis 23.11. tragen eine Tonspur „aac (HE-AAC), 192000 Hz",
deren Decoder nicht aufgeht: „Error while opening decoder: Invalid data
found". ffprobe gibt dann ohne Ausgabe auf, Teilen und Neukodieren scheitern,
und die Upload-Warteschlange versucht es alle 20 bis 80 Minuten erneut —
„ständig erhalte ich Fehler deshalb" (Betreiber, 27.11.). v5.12.1 hat die
Uploads gerettet, aber mit Stille statt Ton.

Live tritt der Fehler nicht auf: Restream und Audio-Tap dekodieren denselben
TikTok-Ton. Und die Bitraten (38–58 kb/s) sind gewöhnlicher HE-AAC-Ton. Kaputt
ist also der KOPF der Spur in der Datei — die AudioSpecificConfig im
esds-Kasten —, nicht der Ton. Ob TikTok ihn so geschickt hat oder ffmpeg 8
(Lavc62, nach dem Umbau des AAC-Decoders in 7.1) ihn so liest, ist von hier
aus nicht zu klären; die Reparatur braucht die Antwort nicht.

════════════════════════════════════════════════════════════════════════
DIE REPARATUR
════════════════════════════════════════════════════════════════════════
1. Den esds-Kasten der Tonspur finden (moov/trak/mdia/minf/stbl/stsd/mp4a)
   und daneben die Zeitskala der Spur (mdhd) — sie ist die Abtastrate, die
   der Muxer kannte.
2. Kandidaten: AAC-LC mit Kernrate = halbe Zeitskala (HE-AAC, implizit
   signalisiert: der Decoder erkennt SBR/PS selbst) oder = Zeitskala (LC),
   je stereo und mono. Ist die Zeitskala keine AAC-Rate, alle vier Kernraten.
3. Jeden Kandidaten an einer PROBE prüfen — 20 s Ton der Datei, kopiert —
   mit dem ffmpeg DIESES Servers: fehlerfrei dekodieren UND die Dauer muss
   stimmen. Fehlerfrei allein genügt nicht: 44,1 und 48 kHz (und 22,05/24)
   teilen sich die Bandtabellen, der falsche Nachbar dekodiert ohne Fehler —
   und der Ton liefe 8,8 % zu langsam. Die Dauer verrät ihn.
4. Den Kopf im Original an Ort und Stelle überschreiben, GLEICHE Länge (der
   Rest mit Nullen; der Parser liest sie als „keine Erweiterung"). Kein
   Verschieben, keine Kopie der Datei — Offsets und Grösse bleiben, und eine
   mehrstündige Aufnahme ist in Millisekunden repariert. Die alten Bytes
   stehen im Log; geht der Ton danach nicht auf, werden sie zurückgeschrieben.

Bot-frei: nur Dateien, Bytes und ffmpeg über nc.kindprozess.
"""

import logging
import os

from nc import kindprozess as _kind
from nc.ffbuild import ff_cmd

log = logging.getLogger("TikTokBot")

# Abtastraten nach ISO/IEC 14496-3, Tabelle 1.18 (Index = Position).
RATEN = (96000, 88200, 64000, 48000, 44100, 32000, 24000, 22050, 16000, 12000,
         11025, 8000, 7350)
KERN_RATEN = (22050, 24000, 44100, 48000)   # TikTok: HE-AAC 22,05/24 k Kern, LC 44,1/48 k
PROBE_S = 20
DAUER_TOLERANZ = 0.04    # 8,8 % trennt 44,1 von 48 kHz — 4 % liegt sicher dazwischen
MAX_FEHLER = 2           # Fehlerzeilen beim Dekodieren der Probe, die noch gelten


class KeinTonkopf(ValueError):
    """Die Datei hat keine (lesbare) AAC-Tonspur im MP4-Kopf."""


class Tonkopf:
    """Wo der Kopf steht und was die Spur über sich sagt."""

    def __init__(self, dsi_offset, dsi_laenge, asc, zeitskala, kanaele, dauer_s):
        self.dsi_offset = dsi_offset
        self.dsi_laenge = dsi_laenge
        self.asc = asc
        self.zeitskala = zeitskala
        self.kanaele = kanaele
        self.dauer_s = dauer_s


# ── MP4-Kasten lesen ─────────────────────────────────────────────────────────

def _kaesten(f, start, ende):
    """(typ, beginn, inhalt, schluss) jedes Kastens zwischen start und ende."""
    pos = start
    while pos + 8 <= ende:
        f.seek(pos)
        kopf = f.read(16)
        if len(kopf) < 8:
            return
        groesse, typ, inhalt = int.from_bytes(kopf[:4], "big"), kopf[4:8], pos + 8
        if groesse == 1 and len(kopf) == 16:
            groesse, inhalt = int.from_bytes(kopf[8:16], "big"), pos + 16
        elif groesse == 0:
            groesse = ende - pos
        if groesse < 8:
            return
        yield typ, pos, inhalt, min(pos + groesse, ende)
        pos += groesse


def _kind_kasten(f, start, ende, typ):
    for t, _b, inhalt, schluss in _kaesten(f, start, ende):
        if t == typ:
            return inhalt, schluss
    raise KeinTonkopf("kein %s-Kasten" % typ.decode("ascii", "replace"))


def _laenge(daten, i):
    """Deskriptor-Länge (bis zu vier Bytes mit Fortsetzungsbit) -> (laenge, i)."""
    n = 0
    for _ in range(4):
        b = daten[i]
        i += 1
        n = (n << 7) | (b & 0x7F)
        if not b & 0x80:
            break
    return n, i


def _dsi_in_esds(daten):
    """-> (beginn, laenge) der DecoderSpecificInfo im Inhalt eines esds-Kastens.

    ISO/IEC 14496-1: ES_Descriptor (0x03) → DecoderConfigDescriptor (0x04,
    13 feste Bytes) → DecoderSpecificInfo (0x05) = die AudioSpecificConfig."""
    i = 4                                    # Version und Flags des Kastens
    if daten[i] != 0x03:
        raise KeinTonkopf("esds ohne ES_Descriptor")
    _n, i = _laenge(daten, i + 1)
    flags = daten[i + 2]
    i += 3
    if flags & 0x80:
        i += 2                               # dependsOn_ES_ID
    if flags & 0x40:
        i += 1 + daten[i]                    # URL
    if flags & 0x20:
        i += 2                               # OCR_ES_Id
    if daten[i] != 0x04:
        raise KeinTonkopf("esds ohne DecoderConfigDescriptor")
    _n, i = _laenge(daten, i + 1)
    i += 13
    if daten[i] != 0x05:
        raise KeinTonkopf("esds ohne DecoderSpecificInfo")
    laenge, i = _laenge(daten, i + 1)
    if laenge < 2 or i + laenge > len(daten):
        raise KeinTonkopf("DecoderSpecificInfo mit %d Bytes" % laenge)
    return i, laenge


def tonkopf(pfad):
    """Den AAC-Tonkopf der Datei finden. -> Tonkopf; wirft KeinTonkopf/OSError."""
    with open(pfad, "rb") as f:
        f.seek(0, os.SEEK_END)
        ende = f.tell()
        moov = _kind_kasten(f, 0, ende, b"moov")
        for t, _b, inhalt, schluss in _kaesten(f, *moov):
            if t != b"trak":
                continue
            mdia = _kind_kasten(f, inhalt, schluss, b"mdia")
            hdlr = _kind_kasten(f, *mdia, b"hdlr")
            f.seek(hdlr[0] + 8)
            if f.read(4) != b"soun":
                continue
            mdhd = _kind_kasten(f, *mdia, b"mdhd")
            f.seek(mdhd[0])
            kopf = f.read(32)
            if kopf[0] == 1:
                zeitskala = int.from_bytes(kopf[20:24], "big")
                dauer = int.from_bytes(kopf[24:32], "big")
            else:
                zeitskala = int.from_bytes(kopf[12:16], "big")
                dauer = int.from_bytes(kopf[16:20], "big")
            stbl = _kind_kasten(f, *_kind_kasten(f, *_kind_kasten(f, *mdia, b"minf"),
                                                 b"stbl"), b"stsd")
            mp4a = _kind_kasten(f, stbl[0] + 8, stbl[1], b"mp4a")
            f.seek(mp4a[0])
            eintrag = f.read(28)
            version = int.from_bytes(eintrag[8:10], "big")
            kanaele = int.from_bytes(eintrag[16:18], "big")
            kinder = mp4a[0] + 28 + {1: 16, 2: 36}.get(version, 0)
            esds = _kind_kasten(f, kinder, mp4a[1], b"esds")
            f.seek(esds[0])
            daten = f.read(esds[1] - esds[0])
            beginn, laenge = _dsi_in_esds(daten)
            return Tonkopf(esds[0] + beginn, laenge, daten[beginn:beginn + laenge],
                           zeitskala, kanaele, (dauer / zeitskala) if zeitskala else 0.0)
    raise KeinTonkopf("keine Tonspur in der Datei")


# ── Kandidaten ───────────────────────────────────────────────────────────────

def asc_lc(rate, kanaele) -> bytes:
    """AudioSpecificConfig AAC-LC: Objekttyp 2, Ratenindex, Kanäle, drei Nullbits."""
    wert = (2 << 11) | (RATEN.index(rate) << 7) | ((kanaele & 0x0F) << 3)
    return wert.to_bytes(2, "big")


def kandidaten(zeitskala, kanaele=2):
    """Die Köpfe, die in Frage kommen — wahrscheinlichste zuerst.

    Die Kanalzahl kommt aus dem mp4a-Eintrag der Spur und steht vorn.
    Gemessen: einen Stereo-Strom unter einem Mono-Kopf dekodiert ffmpeg OHNE
    Fehler (der Decoder passt sich still an) — die Prüfung an der Probe
    trennt mono und stereo also nicht, die Reihenfolge muss es tun."""
    if zeitskala in RATEN:
        raten = ([zeitskala // 2] if (zeitskala // 2) in RATEN else []) + [zeitskala]
    else:
        raten = list(KERN_RATEN)
    folge = [k for k in (kanaele, 2, 1) if k in (1, 2)]
    folge = list(dict.fromkeys(folge))
    return [asc_lc(r, k) for r in raten for k in folge]


def gepolstert(asc, laenge) -> bytes:
    """Auf die Länge der alten DecoderSpecificInfo — der Rest Nullbits."""
    return bytes(asc) + b"\x00" * (laenge - len(asc))


def _schreiben(pfad, offset, daten, zeit=None):
    """Bytes an Ort und Stelle. `zeit` (os.stat-Ergebnis): Zugriffs- und
    Aenderungszeit danach wieder darauf setzen — die Aufbewahrung richtet sich
    nach dem Alter der Aufnahme, und eine Reparatur macht sie nicht neu."""
    with open(pfad, "r+b") as f:
        f.seek(offset)
        f.write(daten)
        f.flush()
        os.fsync(f.fileno())
    if zeit is not None:
        os.utime(pfad, ns=(zeit.st_atime_ns, zeit.st_mtime_ns))


# ── Prüfen mit dem ffmpeg dieses Servers ─────────────────────────────────────

async def dekodiert(pfad, zeitlimit=60.0):
    """-> (fehlerzeilen, sekunden): die Tonspur nach PCM, 8 kHz mono.

    Die feste Ausgaberate macht die Sekunden unabhängig davon, was der Decoder
    für eine Rate meldet: Bytes / 16000. Wirft OSError/TimeoutError."""
    rc, out, err = await _kind.ausfuehren(
        ff_cmd(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-i", pfad,
                "-map", "0:a:0", "-ac", "1", "-ar", "8000", "-c:a", "pcm_s16le",
                "-f", "s16le", "pipe:1"], threads=1),
        zeitlimit, art="ffmpeg-tonprobe")
    zeilen = [z for z in (err or b"").decode("utf-8", "replace").splitlines() if z.strip()]
    if rc != 0:
        zeilen.append("rc=%s" % rc)
    return zeilen, len(out) / 16000.0


async def _probe_bauen(pfad, ziel, sekunden=PROBE_S, zeitlimit=120.0):
    """20 s Ton der Aufnahme, kopiert — der Kopf kommt unverändert mit."""
    rc, _out, err = await _kind.ausfuehren(
        ff_cmd(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", pfad,
                "-map", "0:a:0", "-t", str(sekunden), "-c", "copy", "-f", "mp4", ziel],
               threads=1),
        zeitlimit, art="ffmpeg-tonprobe", stdout=_kind.DEVNULL)
    if rc != 0 or not os.path.isfile(ziel):
        raise KeinTonkopf("Probe nicht herstellbar: %s" % (
            (err or b"").decode("utf-8", "replace").strip()[-200:] or "rc=%s" % rc))


async def reparieren(pfad, wer="?"):
    """Den Tonkopf von `pfad` reparieren, wenn der Ton nicht aufgeht.

    -> {"lage": "gesund"|"repariert"|"unrettbar"|"kein_ton", "alt": hex,
        "neu": hex, "grund": text}. Wirft nicht (bis auf Abbruch)."""
    try:
        kopf = tonkopf(pfad)
    except (KeinTonkopf, OSError, IndexError) as e:
        # Normalfall fuer tonlose Aufnahmen und andere Container — INFO, weil
        # der Aufrufer danach die Stille nimmt und das selbst meldet.
        log.info("Tonspur %s (%s): kein lesbarer AAC-Kopf (%s: %s) — nichts zu "
                 "reparieren.", wer, os.path.basename(pfad), type(e).__name__, e)
        return {"lage": "kein_ton", "grund": "%s: %s" % (type(e).__name__, e)}
    try:
        fehler, _s = await dekodiert(pfad, zeitlimit=60.0)
    except Exception as e:
        log.warning("Tonspur %s (%s): die Tonprobe selbst scheiterte (%s: %s) — keine "
                    "Reparatur. ffmpeg im PATH?", wer, os.path.basename(pfad),
                    type(e).__name__, e)
        return {"lage": "unrettbar", "grund": "Tonprobe: %s: %s" % (type(e).__name__, e),
                "alt": kopf.asc.hex()}
    if not fehler:
        return {"lage": "gesund", "alt": kopf.asc.hex()}
    probe = "%s.tonprobe.mp4" % pfad
    try:
        await _probe_bauen(pfad, probe)
        pk = tonkopf(probe)
        erwartet = pk.dauer_s
        gewaehlt, versucht = None, []
        for asc in kandidaten(kopf.zeitskala, kopf.kanaele):
            _schreiben(probe, pk.dsi_offset, gepolstert(asc, pk.dsi_laenge))
            f, sek = await dekodiert(probe, zeitlimit=60.0)
            passt = erwartet > 0 and abs(sek - erwartet) <= DAUER_TOLERANZ * erwartet
            versucht.append("%s: %d Fehler, %.1f/%.1f s" % (asc.hex(), len(f), sek, erwartet))
            if len(f) <= MAX_FEHLER and passt:
                gewaehlt = asc
                break
        if gewaehlt is None:
            log.error("Tonspur %s (%s): Kopf %s ist unlesbar, und kein Ersatzkopf passt "
                      "(%s) — der Ton bleibt unrettbar, Uploads bekommen Stille.",
                      wer, os.path.basename(pfad), kopf.asc.hex(), "; ".join(versucht))
            return {"lage": "unrettbar", "alt": kopf.asc.hex(), "grund": "; ".join(versucht)}
        zeit = os.stat(pfad)
        _schreiben(pfad, kopf.dsi_offset, gepolstert(gewaehlt, kopf.dsi_laenge), zeit)
        try:
            fehler, _s = await dekodiert(pfad, zeitlimit=60.0)
        except BaseException:
            # Ohne Urteil kein neuer Kopf im Original — auch beim Abbruch.
            _schreiben(pfad, kopf.dsi_offset, kopf.asc, zeit)
            raise
        if len(fehler) > MAX_FEHLER:
            _schreiben(pfad, kopf.dsi_offset, kopf.asc, zeit)
            log.error("Tonspur %s (%s): Ersatzkopf %s half an der Probe, am Original nicht "
                      "(%s) — alter Kopf %s zurückgeschrieben.", wer, os.path.basename(pfad),
                      gewaehlt.hex(), fehler[:2], kopf.asc.hex())
            return {"lage": "unrettbar", "alt": kopf.asc.hex(), "grund": "Original: %s" % fehler[:2]}
        log.warning("Tonspur %s repariert (%s): Kopf %s war unlesbar (Zeitskala %d Hz), "
                    "jetzt %s — der Ton ist zurück.", wer, os.path.basename(pfad),
                    kopf.asc.hex(), kopf.zeitskala, gewaehlt.hex())
        return {"lage": "repariert", "alt": kopf.asc.hex(), "neu": gewaehlt.hex()}
    except Exception as e:
        log.error("Tonspur %s (%s): Reparatur gescheitert (%s: %s) — die Datei ist "
                  "unverändert.", wer, os.path.basename(pfad), type(e).__name__, e)
        return {"lage": "unrettbar", "alt": kopf.asc.hex(), "grund": "%s: %s" % (
            type(e).__name__, e)}
    finally:
        try:
            os.remove(probe)
        except OSError:
            pass                         # Aufraeumpfad: nie angelegt ist auch weg
