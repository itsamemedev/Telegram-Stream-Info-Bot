"""nc.videoteil — eine Aufnahme in telegramtaugliche Teile zerlegen.

v4.2-W11. Herausgeloest aus `split_and_send_video` in bot.py (614 Zeilen).
Was hier steht, ist der ffmpeg-Teil: messen, teilen, notfalls neu kodieren,
kaputte Container reparieren. Was NICHT hier steht, ist alles Telegram —
Versand, Bildunterschriften, Fehlermeldungen an den Nutzer. Genau an dieser
Naht laesst sich die Zerlegung ueberhaupt testen: die Groessenrechnung und die
Wiederholungslogik sind reine Datei-Arithmetik, der Versand ist es nie.

WARUM EIN EIGENES ffprobe HIER, obwohl nc/ffdiag.ffprobe_duration existiert:
Das dort ist SYNCHRON (subprocess.run mit 15 s Timeout) und richtig so fuer
Aufrufer ausserhalb des Event-Loops. Auf dem Loop waere es ein Fehler — ein
einziges haengendes ffprobe friert jede andere Aufnahme, den Restream und das
Dashboard fuer 15 Sekunden ein. Deshalb steht hier die asynchrone Fassung
daneben, und deshalb heisst sie anders. Die beiden zusammenzulegen ist keine
Aufraeumarbeit, sondern ein Ausfall.

(In bot.py hatte `split_and_send_video` eine eigene, verschachtelte Kopie, die
den Modul-Import gleichen Namens verschattete. Zwei Funktionen mit demselben
Namen und verschiedenem Verhalten in einer Datei — beim naechsten Aufraeumen
haette jemand die falsche behalten.)
"""

import asyncio
import logging
import os
import re
import shutil
import threading
import time

from nc import encodeschlange as _encodeschlange  # v4.2-W174
from nc import kindprozess as _kind  # v4.2-W120
from nc import meldetakt as _takt
from nc.ffbuild import ff_cmd
from nc.ffdiag import _ffmpeg_stderr_tail

log = logging.getLogger("TikTokBot")

# Telegram-Bot-Hard-Limit = 50 MB pro Datei. Gezielt wird auf 45, damit
# Multipart-Overhead und Container-Metadaten noch hineinpassen.
#
# Die alte Logik benutzte CHUNK_SIZE_MB*60 als segment_time — bei
# CHUNK_SIZE_MB=50 waren das 50 MINUTEN je Segment, bei normalen
# TikTok-Bitraten 300-700 MB je Teil, also immer ein 413.
TELEGRAM_HARD_MB = 50
ZIEL_TEIL_MB = 45

# Ein Teil unter 10 KB ist ein Header ohne Inhalt.
_MIN_TEIL_BYTES = 10_240

_cfg = {"threads_bg": None, "nice_bg": None}


# ---- Teil-Reste erkennen und laufende Arbeit schuetzen (AUF-2) ---------------
#
# Bis hierher galt beim Aufraeumen (Deck „Reste aufraeumen", Telegram /cleanup)
# jede Datei als Split-Rest, deren Name „_part" oder „_re_" ENTHAELT. Aufnahmen
# heissen tiktok_live_<chat>_<nutzer>_<zeit>.mp4 — ein Nutzer „dj_partyking"
# oder „re_becca" machte damit JEDE seiner Aufnahmen zum Rest, auch die gerade
# laufende, und der Knopf loeschte sie ohne Alters- oder Bestandspruefung.
#
# Erkannt wird jetzt genau das, was die Erzeuger schreiben — und die Erzeuger
# stehen hier bzw. rufen hier her:
#   <aufnahme>_part_000.mp4      kopier_teilen   (telegramversand: praefix "_part")
#   <aufnahme>_part_re_000.mp4   neu_kodieren
#   <aufnahme>_dcpart25_000.mp4  nc/discordaufnahme (praefix "_dcpart<Grenze>",
#                                seit v5.12 je Server-Grenze; davor "_dcpart")
#   <aufnahme>.repaired.mp4      reparieren      (telegramversand, B47)
#   <aufnahme>.remux.mp4         zeitstempel_richten (telegramversand, B70+)
#   <aufnahme>_dcpart9.remux.mp4 zeitstempel_richten (nc/discordaufnahme, v5.12.1 —
#                                eigener Name, Telegram laeuft gleichzeitig)
#   <aufnahme>_dcpart9_re_007.mp4_part_re_000.mp4
#                                _uebergroesse_nachteilen (v5.12.1)
# <aufnahme> traegt dabei SEINE Endung (praefix = f"{filepath}_part"). Eine
# Videoendung MITTEN im Namen kommt in keinem Aufnahmenamen vor — genau daran
# unterscheidet sich ein Teil von einer Aufnahme, deren Nutzer „part" heisst.
_REST = re.compile(r"^.+\.(?:mp4|flv|ts|mkv|webm|m4v|mov)"
                   r"(?:_(?:dcpart\d*|part)(?:_re)?_\d{3,}\.mp4|\.repaired\.mp4|\.remux\.mp4"
                   r"|_dcpart\d*\.remux\.mp4)$")

# Wie lange eine angemeldete Zerlegung als laufend gilt. Der Versand loescht
# jeden Teil erst NACH seinem Upload; bei 45-MB-Teilen und FloodWait dauert
# eine Zehn-Stunden-Aufnahme leicht ueber eine Stunde — die alte Schranke von
# /cleanup (1 h) loeschte dann die Teile, die noch drankamen. Zwoelf Stunden
# sind grosszuegig: nach einem Neustart ist die Liste ohnehin leer, und ein
# Rest, der einen halben Tag laenger liegt, kostet nur Platz.
ARBEIT_MAX_S = 12 * 3600.0

_IN_ARBEIT = {}                 # abs. Praefix bzw. Ziel -> time.monotonic()
_IN_ARBEIT_LOCK = threading.Lock()


def ist_rest(name) -> bool:
    """Traegt `name` (Dateiname oder Pfad) exakt die Form eines Teil-Rests?"""
    return bool(_REST.match(os.path.basename(name or "")))


def _anmelden(praefix_oder_ziel):
    """Eine Zerlegung/ein Re-Mux beginnt: alles, was mit diesem Pfad anfaengt,
    gehoert einem laufenden Versand. Die Liste lebt im Prozess — Bot und Deck
    laufen in demselben, und nach einem Neustart laeuft kein Versand mehr."""
    jetzt = time.monotonic()
    with _IN_ARBEIT_LOCK:
        for k in [k for k, t in _IN_ARBEIT.items() if jetzt - t >= ARBEIT_MAX_S]:
            del _IN_ARBEIT[k]
        _IN_ARBEIT[os.path.abspath(praefix_oder_ziel)] = jetzt


def in_arbeit(pfad) -> bool:
    """Gehoert `pfad` zu einer Zerlegung, deren Versand noch laufen kann?"""
    voll = os.path.abspath(pfad)
    jetzt = time.monotonic()
    with _IN_ARBEIT_LOCK:
        return any(voll.startswith(k) and jetzt - t < ARBEIT_MAX_S
                   for k, t in _IN_ARBEIT.items())


def configure(threads_bg=None, nice_bg=None):
    """Die beiden ffmpeg-Stellschrauben aus der .env.

    Als Funktion gelesen und nicht als Modul-Konstante: .env wird teils erst
    nach den ersten Importen geladen (CLAUDE.md). Der Bot ruft das beim Start.
    """
    _cfg["threads_bg"] = threads_bg
    _cfg["nice_bg"] = nice_bg


def _bau(cmd):
    return ff_cmd(cmd, threads=_cfg["threads_bg"], nice=_cfg["nice_bg"])


_MB = 1024 * 1024

# v5.12.1: die Laufzeit aus der Eingangsbeschreibung von `ffmpeg -i`.
_DAUER_KOPF = re.compile(r"Duration:\s*(\d+):(\d{2}):(\d{2}(?:\.\d+)?)")


def dauer_aus_kopf(text):
    """'Duration: 01:02:03.45' aus dem stderr von `ffmpeg -i` -> Sekunden.

    None, wenn keine (positive) Laufzeit dasteht — dieselbe Bedeutung wie bei
    dauer(): „weiss ich nicht", nicht „ist leer"."""
    m = _DAUER_KOPF.search(text or "")
    sekunden = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 0.0
    return sekunden if sekunden > 0 else None


async def _kopf_lesen(pfad):
    """stderr von `ffmpeg -i pfad` ohne Ausgabe: Laufzeit und Streamliste.

    ffmpeg oeffnet dafuer KEINEN Decoder — genau darin unterscheidet es sich
    von ffprobe, und genau deshalb steht es hier. rc ist immer != 0 („At
    least one output file must be specified"); gelesen wird nur der Text."""
    try:
        _rc, _, err = await _kind.ausfuehren(
            _bau(["ffmpeg", "-hide_banner", "-nostdin", "-i", pfad]), 15,
            art="ffprobe", stdout=_kind.DEVNULL)
    except Exception as e:
        log.warning("split: Kopf von %s nicht lesbar (%s: %s)",
                    os.path.basename(pfad), type(e).__name__, e)
        return ""
    return (err or b"").decode(errors="ignore")


async def dauer(pfad):
    """Exakte Laufzeit in Sekunden. None bei Fehler.

    None und nicht 0.0: der Aufrufer muss "weiss ich nicht" von "ist leer"
    unterscheiden koennen — an dieser Unterscheidung haengt, ob er die
    Bitrate rechnet oder auf den konservativen Rueckfall geht.

    v5.12.1: scheitert ffprobe, gilt die Kopfzeile von `ffmpeg -i`. ffprobe
    oeffnet fuer JEDEN Stream den Decoder und bricht mit rc=1 und leerer
    Ausgabe ab, wenn einer nicht aufgeht. Gemessen am 26./27.11.: Aufnahmen
    mit einer Tonspur „aac (HE-AAC), 192000 Hz", deren Decoder nicht oeffnet
    — ffprobe lieferte nichts, `_pruefe_teile` hielt JEDEN Teil fuer kaputt
    und loeschte ihn („Alle Teile vom Split waren ungueltig"), und das Bild
    war die ganze Zeit in Ordnung.
    """
    laenge = await _dauer_ffprobe(pfad)
    if laenge is not None:
        return laenge
    return dauer_aus_kopf(await _kopf_lesen(pfad))


async def _dauer_ffprobe(pfad):
    """Die Laufzeit nach ffprobe — None, wenn ffprobe aufgibt."""
    # v4.2-W120: ueber nc.kindprozess — der Prozess endet auch, wenn der
    # aufrufende Task abgebrochen wird (vorher lief ffprobe dann weiter).
    try:
        rc, out, _ = await _kind.ausfuehren(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", pfad], 15, art="ffprobe", stderr=_kind.DEVNULL)
        if rc != 0:
            return None
        return float((out or b"").strip() or 0) or None
    except Exception:
        return None


# v5.12.1: Stille statt einer Tonspur, deren Decoder nicht aufgeht. Dieselbe
# Quelle wie nc.tonspur (dort steht die Begruendung); hier als Kopie, weil
# nc.tonspur aus DIESEM Modul importiert — ein Import zurueck waere zirkulaer.
_STILLE = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
_STILLE_AAC = ["-c:a", "aac", "-b:a", "64k", "-ar", "44100", "-ac", "2"]


async def _ton_kaputt(pfad, kopf):
    """Traegt die Datei eine Tonspur, deren Decoder nicht aufgeht? -> bool

    Nur gefragt, wenn ffprobe schon aufgegeben hat. Die Kopfzeile zeigt dann,
    ob es eine Tonspur gibt (ohne Kopf oder ohne Ton ist es nicht der Ton —
    dann bleibt alles beim Alten); eine Sekunde Dekodieren zeigt, ob sie
    aufgeht. Ins WAV-Format, nicht `-f null`: der null-Muxer laesst sich
    beim Bauen von ffmpeg abschalten (nc.tonspur.garantie_cmd)."""
    if "Audio:" not in (kopf or ""):
        return False
    try:
        rc, _, _err = await _kind.ausfuehren(
            _bau(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-i", pfad,
                  "-map", "0:a:0", "-t", "1", "-c:a", "pcm_s16le", "-f", "wav", "pipe:1"]),
            30, art="ffprobe", stdout=_kind.DEVNULL)
    except Exception as e:
        # Unklar ist hier „kaputt": ffprobe hat schon aufgegeben, und Stille
        # in einem Teil ist besser als ein Teil, der nirgends abspielt.
        log.warning("split: Tonprobe von %s scheiterte (%s: %s) — Ton gilt als kaputt.",
                    os.path.basename(pfad), type(e).__name__, e)
        return True
    return rc != 0


async def messen(pfad):
    """-> (laufzeit oder None, ton_ersetzen). Fuer beide Zerlegungen.

    ton_ersetzen heisst: die Tonspur ist da, ihr Decoder geht aber nicht auf.
    Dann bekommen die TEILE Stille statt des Tons — beim Kopier-Split sonst
    Teile, die ffprobe (und mit ihm `_pruefe_teile`) als kaputt verwirft,
    beim Neukodieren ein Abbruch vor dem ersten Bild: „Error while opening
    decoder: Invalid data found", nachdem die Kodierung bis zu 40 min in der
    Encode-Warteschlange stand. Das Original bleibt unangetastet."""
    laenge = await _dauer_ffprobe(pfad)
    if laenge is not None:
        return laenge, False
    kopf = await _kopf_lesen(pfad)
    laenge = dauer_aus_kopf(kopf)
    ersetzen = await _ton_kaputt(pfad, kopf)
    if ersetzen:
        laut, weg = _takt.melden("videoteil-ton", "decoder", time.monotonic())
        if laut:
            log.error("Tonspur von %s laesst sich nicht dekodieren (ffprobe bricht daran "
                      "ab) — die Upload-Teile bekommen Stille statt des Tons, das Bild "
                      "bleibt. Die Aufnahme selbst bleibt unangetastet auf dem Server; "
                      "pruefen mit: ffmpeg -v error -i '%s' -map 0:a:0 -f wav -t 1 -%s",
                      os.path.basename(pfad), pfad, _takt.zusatz(weg))
    return laenge, ersetzen


def platz_reicht(pfad, faktor=1.2):
    """Reicht der Platz fuer einen Split? -> (ok, frei_mb oder Meldung)

    Der Split legt die Teile NEBEN das Original, braucht also noch einmal die
    Dateigroesse. Ohne diese Probe stirbt ffmpeg mittendrin mit "No space left
    on device" und hinterlaesst halbe Teile (B53).

    Bei Unsicherheit wird weitergemacht: eine fehlgeschlagene Platzprobe darf
    keinen Upload verhindern, der sonst funktioniert haette.
    """
    try:
        datei_mb = os.path.getsize(pfad) / 1024 / 1024
        stat = shutil.disk_usage(os.path.dirname(pfad) or ".")
        frei_mb = stat.free / 1024 / 1024
        noetig_mb = datei_mb * faktor
        if frei_mb < noetig_mb:
            return False, (f"nur {frei_mb:.0f} MB frei, brauche ~{noetig_mb:.0f} MB "
                           f"(Datei: {datei_mb:.0f} MB)")
        return True, frei_mb
    except Exception as e:
        return True, f"disk-check failed: {e}"


# AUF-5: die Teile EINES Laufs, exakt. `%03d` schreibt mindestens drei
# Ziffern; "re_" kennzeichnet das Neu-Kodieren.
_TEIL_KOPIE = r"_\d{3,}\.mp4"
_TEIL_NEU = r"_re_\d{3,}\.mp4"
# v5.12.1: Unterteile eines nachgeteilten Teils (_uebergroesse_nachteilen):
# <praefix>_re_007.mp4_part_re_000.mp4. Die Form erkennt _REST (Waisen-Suche),
# und weder das Kopier- noch das Neu-Muster trifft sie.
_TEIL_NACH = r"_re_\d{3,}\.mp4_part_re_\d{3,}\.mp4"


def teile(praefix, art=_TEIL_KOPIE):
    """Die Teil-Dateien zu `praefix`, sortiert. -> [Pfad]

    AUF-5: hier stand `glob(f"{praefix}_*.mp4")`. Das traf beim Kopier-Split
    auch die `_re_NNN` des Neu-Kodierens und JEDEN liegengebliebenen Teil
    eines frueheren Laufs — nach einem Neustart reiht W175 den Upload neu
    ein, und hatte der erste Lauf zehn Teile, der zweite fuenf, gingen 005
    bis 009 vom ersten mit hinaus: doppelte und vertauschte Teile. Jetzt ein
    exaktes Muster je Art, als Regex gegen den Dateinamen, und der Praefix
    ist woertlich — ein `[` im Aufnahmepfad waere fuer glob eine Klasse.
    """
    verz = os.path.dirname(praefix) or "."
    muster = re.compile(re.escape(os.path.basename(praefix)) + art)
    try:
        namen = os.listdir(verz)
    except OSError as e:
        log.warning("split: %s nicht lesbar (%s)", verz, e)
        return []
    return sorted(os.path.join(verz, n) for n in namen if muster.fullmatch(n))


def teile_entfernen(praefix):
    """Alle Teile zu `praefix` weg, beider Arten. -> Anzahl

    AUF-5: vor jedem Split (Reste eines frueheren Laufs) und auf jedem
    Ausstiegspfad des Versands (toter Chat, gescheiterter Re-Split, Abbruch).
    Die Aufnahme selbst traegt keinen dieser Namen und bleibt immer.
    """
    n = 0
    for t in (teile(praefix, _TEIL_KOPIE) + teile(praefix, _TEIL_NEU)
              + teile(praefix, _TEIL_NACH)):
        try:
            os.remove(t)
            n += 1
        except OSError:
            pass               # Aufraeumpfad: schon weg ist auch weg
    return n


async def _pruefe_teile(kandidaten):
    """Die erzeugten Teile durchsehen und Schrott wegwerfen (B52).

    Ohne diese Pruefung landen header-only-Dateien und Teile ohne Stream beim
    Upload — und der scheitert dann mit einer Telegram-Fehlermeldung, die
    nichts ueber die Ursache sagt.
    """
    gut = []
    for teil in kandidaten:
        try:
            groesse = os.path.getsize(teil)
            if groesse < _MIN_TEIL_BYTES:
                log.warning("split: Teil %s ist nur %dB — geloescht",
                            os.path.basename(teil), groesse)
                await asyncio.to_thread(wegwerfen, [teil])
                continue
            if (await dauer(teil) or 0) <= 0:
                log.warning("split: Teil %s hat keine erkennbare Dauer — "
                            "vermutlich kaputt, geloescht", os.path.basename(teil))
                # v5.12.1: im Thread — ein grosser Teil auf voller Platte
                # stand im Log 1,4 s auf dem Event-Loop.
                await asyncio.to_thread(wegwerfen, [teil])
                continue
            gut.append(teil)
        except Exception as e:
            log.warning("split: Teil %s: %s", os.path.basename(teil), e)
    return kandidaten, gut


async def kopier_teilen(pfad, praefix, ziel_mb):
    """Ohne Neukodieren teilen. -> (teile, None) oder (None, fehlertext)

    Bitratenbasiert: die echte Bitrate ergibt sich aus Groesse durch Dauer,
    daraus die Segmentlaenge, die ziel_mb ergibt. Scheitert ffprobe, wird
    konservativ mit 2 Mbps gerechnet.
    """
    _anmelden(praefix)          # AUF-2: ab hier gehoeren <praefix>_* dem Versand
    # AUF-5: Reste eines frueheren Laufs weg, bevor ffmpeg schreibt — sonst
    # sammelt die Auswahl unten sie mit ein.
    await asyncio.to_thread(teile_entfernen, praefix)
    groesse_mb = os.path.getsize(pfad) / 1024 / 1024
    laenge, ton_ersetzen = await messen(pfad)
    if laenge and laenge > 0:
        mb_je_s = groesse_mb / laenge
        # 10 % Sicherheitsreserve
        seg = max(15, int((ziel_mb * 0.9) / max(mb_je_s, 0.001)))
        log.info("split: duration=%.0fs, bitrate~%.1fMbps, segment_time=%ds",
                 laenge, mb_je_s * 8, seg)
    else:
        # 2 Mbps angenommen -> 1 MB je 4 s
        seg = max(60, ziel_mb * 4)
        log.warning("split: ffprobe-Dauer fehlgeschlagen, Rueckfall segment_time=%ds", seg)

    if ton_ersetzen:
        # Bild und Untertitel kopiert, Ton aus der Stille-Quelle; -shortest,
        # weil die Stille endlos ist.
        eingang = ["-i", pfad, *_STILLE, "-map", "0:v", "-map", "0:s?", "-map", "1:a:0",
                   "-c", "copy", *_STILLE_AAC, "-shortest"]
    else:
        eingang = ["-i", pfad, "-c", "copy", "-map", "0"]
    # v5.12.1: -loglevel error — stderr landet als Grund in der Meldung, und
    # ohne den Pegel stand dort der Stream-Dump statt des Fehlers („…
    # vendor_id : [0][0][0][0]", 27.11.).
    cmd = _bau(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *eingang,
                "-f", "segment", "-segment_time", str(seg),
                "-segment_format", "mp4", "-reset_timestamps", "1",
                "-movflags", "+faststart",
                f"{praefix}_%03d.mp4"])
    # Ohne Zeitdeckel blockiert ein haengendes ffmpeg (korrupter Input mit
    # read-hang) den Event-Loop unbegrenzt und friert JEDE andere Aufnahme ein.
    deckel = max(300, int(seg * 4) + 120)
    try:
        rc, _, stderr = await _kind.ausfuehren(cmd, deckel, art="ffmpeg-split",
                                               stdout=_kind.DEVNULL)
    except asyncio.TimeoutError:
        await asyncio.to_thread(teile_entfernen, praefix)      # AUF-5: was ffmpeg bis dahin schrieb
        return None, f"ffmpeg split timeout nach {deckel}s (segment_time={seg})"
    if rc != 0:
        await asyncio.to_thread(teile_entfernen, praefix)      # AUF-5: halbe Teile eines Abbruchs
        # Der echte Fehler steht am ENDE von stderr; der Anfang ist Banner.
        schwanz = _ffmpeg_stderr_tail(stderr.decode(errors="ignore"), max_len=800)
        return None, (f"[rc={rc}] ffmpeg -segment_time {seg} → "
                      f"{praefix}_%03d.mp4\n{schwanz}")

    kandidaten, gut = await _pruefe_teile(teile(praefix, _TEIL_KOPIE))
    if not gut:
        await asyncio.to_thread(teile_entfernen, praefix)
        return None, "Alle Teile vom Split waren ungueltig (ffprobe-failed)"
    if len(gut) < len(kandidaten):
        log.warning("split: %d/%d Teile verworfen wegen Validierungsfehler — "
                    "%d verbleiben", len(kandidaten) - len(gut), len(kandidaten), len(gut))
    return gut, None


async def neu_kodieren(pfad, praefix, ziel_mb, _tiefe=0):
    """Letzter Ausweg: mit erzwungenen Keyframes neu kodieren.

    WARUM ES DAS BRAUCHT (B70): der Segment-Muxer mit -c copy kann NUR an
    vorhandenen Keyframes schneiden. Hat ein TikTok-Stream sehr wenige (langer
    GOP), entsteht ein einziger riesiger Teil, den weiteres Halbieren nicht
    kleiner macht — im Log: "part 1/1 bleibt 68 MB". Hier werden Keyframes an
    den Segmentgrenzen erzwungen und die Bitrate gedeckelt. Langsamer als
    Kopieren, dafuer zuverlaessig.
    """
    _anmelden(praefix)          # AUF-2, s. kopier_teilen
    await asyncio.to_thread(teile_entfernen, praefix)          # AUF-5: Reste eines frueheren Laufs
    laenge, ton_ersetzen = await messen(pfad)
    groesse_mb = os.path.getsize(pfad) / 1024 / 1024
    if not laenge or laenge <= 0:
        laenge = max(30.0, groesse_mb)          # grobe Annahme
    orig_mbps = (groesse_mb * 8) / laenge
    # Bitrate moderat deckeln: begrenzt die Teilgroesse, haelt die Qualitaet.
    # v5.12.1: dazu ein Deckel AUS DEM ZIEL. Ein Teil ist mindestens 15 s lang
    # (unten); bei 4 Mbit/s sind das 7,5 MB — fuer ein kleineres Ziel war jeder
    # Teil zu gross, egal wie die Segmentlaenge gerechnet wurde (gemessen:
    # Ziel 2 MB, Teile 3,3 bis 8,9 MB). Und das Nachteilen half nicht, weil es
    # dieselbe Rechnung noch einmal machte.
    deckel_mbps = (ziel_mb * 8 * 0.88) / 15 - 0.128
    vbps = max(0.4, min(orig_mbps, 4.0, deckel_mbps))
    gesamt_mbps = vbps + 0.128                  # + AAC 128k
    # Segmentlaenge so, dass bitrate*seg/8 <= ziel_mb (12 % Reserve).
    # v5.12.1: Deckel = Zielrate, Puffer = 1 s. Vorher maxrate 1,2x und
    # bufsize 2 s bei 8 % Reserve — die Rechnung ging nur im Mittel auf, und
    # ein bewegtes Stueck hob einen Teil um bis zu 20 % ueber das Ziel
    # (26.11.: „Teil 76/86 bleibt 10.9 MB > 9 MB", 71 Teile schon gesendet,
    # die Warteschlange schickte beim naechsten Versuch alle noch einmal).
    # Mit dem Puffer von einer Sekunde ist ein Teil von seg Sekunden
    # hoechstens (seg + 1) * Rate gross; seg >= 15 haelt das unter 7 %.
    seg = max(15, int((ziel_mb * 8 * 0.88) / max(gesamt_mbps, 0.3)))
    vbr = f"{int(vbps * 1000)}k"
    if ton_ersetzen:
        eingang = ["-i", pfad, *_STILLE, "-map", "0:v:0", "-map", "1:a:0", "-shortest"]
    else:
        eingang = ["-i", pfad]
    cmd = _bau(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                # toleriert Non-monotonic DTS ("pts has no value")
                "-fflags", "+igndts",
                *eingang,
                "-c:v", "libx264", "-preset", "veryfast", "-b:v", vbr,
                "-maxrate", vbr,
                "-bufsize", vbr,
                "-force_key_frames", f"expr:gte(t,n_forced*{seg})",
                "-c:a", "aac", "-b:a", "128k",
                "-f", "segment", "-segment_time", str(seg),
                # v5.12.1: der erzwungene Keyframe liegt durch Rundung knapp VOR
                # der Schnittzeit, und der Muxer schnitt erst am naechsten
                # natuerlichen — gemessen: erster Teil 23,3 s statt 15 s, also
                # 55 % ueber dem Ziel. Genau dafuer nennt die ffmpeg-Doku
                # segment_time_delta (Vorgabe 1/(2*fps); 0,05 deckt ab 10 fps).
                "-segment_time_delta", "0.05",
                "-segment_format", "mp4", "-reset_timestamps", "1",
                "-movflags", "+faststart", f"{praefix}_re_%03d.mp4"])
    log.info("re-encode split: dur=%.0fs, vbr=%s, seg=%ds (orig~%.1fMbps)",
             laenge, vbr, seg, orig_mbps)
    try:
        # Grosszuegig: Neukodieren ist deutlich langsamer als Kopieren.
        # v4.2-W174: durch die Encode-Warteschlange — ein Upload darf warten,
        # eine Aufnahme nebenan darf nicht zerfallen.
        async with _encodeschlange.platz("zerlegen-neu-kodieren"):
            rc, _, stderr = await _kind.ausfuehren(cmd, max(600, int(laenge * 3)),
                                                   art="ffmpeg-reencode",
                                                   stdout=_kind.DEVNULL)
    except asyncio.TimeoutError:
        await asyncio.to_thread(teile_entfernen, praefix)      # AUF-5: die halben _re_NNN
        return None, "re-encode timeout"
    except Exception as e:
        await asyncio.to_thread(teile_entfernen, praefix)
        return None, f"re-encode exception: {e}"
    if rc != 0:
        await asyncio.to_thread(teile_entfernen, praefix)
        return None, _ffmpeg_stderr_tail(stderr.decode(errors="ignore"), 600)

    _, gut = await _pruefe_teile(teile(praefix, _TEIL_NEU))
    if not gut:
        await asyncio.to_thread(teile_entfernen, praefix)
        return None, "re-encode: keine gueltigen Teile"
    if _tiefe == 0 and zu_gross(gut, ziel_mb):
        gut = await _uebergroesse_nachteilen(gut, ziel_mb)
    return gut, None



async def _uebergroesse_nachteilen(liste, ziel_mb):
    """Neu kodierte Teile, die trotz Deckel ueber dem Ziel liegen, einzeln
    noch einmal teilen. -> Liste in derselben Reihenfolge.

    Nur der zu grosse Teil wird noch einmal kodiert — Sekunden statt der
    ganzen Aufnahme. Gelingt es nicht, bleibt er stehen, und der Versand
    meldet ihn wie bisher als zu gross."""
    aus = []
    for teil in liste:
        if os.path.getsize(teil) / _MB <= ziel_mb:
            aus.append(teil)
            continue
        unter, fehler = await neu_kodieren(teil, teil + "_part", ziel_mb, _tiefe=1)
        if unter and not zu_gross(unter, ziel_mb):
            await asyncio.to_thread(wegwerfen, [teil])
            log.info("split: %s lag ueber %s MB — in %d Teile nachgeteilt",
                     os.path.basename(teil), ziel_mb, len(unter))
            aus.extend(unter)
            continue
        await asyncio.to_thread(wegwerfen, unter)
        log.warning("split: %s bleibt ueber %s MB — Nachteilen scheiterte (%s)",
                    os.path.basename(teil), ziel_mb, fehler or "Unterteile weiter zu gross")
        aus.append(teil)
    return aus


async def _mux(pfad, ziel, flags, deckel=300):
    """Neu muxen ohne neu zu kodieren. -> (ok, fehlertext)"""
    _anmelden(ziel)             # AUF-2: .repaired/.remux sind Versand-Zwischenstand
    try:
        # v4.2-W120: jetzt mit Thread-Deckel (_bau). Vorher stand der Befehl
        # als Einzelargumente da, und der Deckel-Vertrag sah ihn nicht.
        rc, _, stderr = await _kind.ausfuehren(
            _bau(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *flags, "-i", pfad,
                  "-c", "copy", "-movflags", "+faststart", ziel]),
            deckel, art="ffmpeg-mux", stdout=_kind.DEVNULL)
    except asyncio.TimeoutError:
        return False, "timeout"
    except Exception as e:
        return False, str(e)
    if rc == 0 and os.path.exists(ziel) and os.path.getsize(ziel) > 0:
        return True, None
    if os.path.exists(ziel):
        try:
            os.remove(ziel)
        except OSError:
            pass
    return False, (_ffmpeg_stderr_tail(stderr.decode(errors="ignore"), 400)
                   if stderr else f"rc={rc}")


def ist_kaputter_container(fehler):
    """Sagt der Split-Fehler, dass die QUELLE kaputt ist? (B47)

    "moov atom not found" heisst: ffmpeg wurde mit SIGKILL beendet, bevor er
    das moov-Atom schreiben konnte — typischerweise durch unseren eigenen
    Stall-Watchdog. Die Datei ist dann reparabel, nicht verloren.
    """
    t = (fehler or "").lower()
    return "moov atom not found" in t or "invalid data found" in t


async def reparieren(pfad, ziel):
    """B47: kaputten MP4-Container neu muxen. -> (ok, fehlertext)"""
    return await _mux(pfad, ziel, ["-err_detect", "ignore_err"])


async def zeitstempel_richten(pfad, ziel):
    """B70+: vor dem Neukodieren die Zeitstempel geradeziehen. -> (ok, fehler)

    Streams mit "pts has no value" / "Non-monotonic DTS" bringen den
    Segment-Muxer zum Absturz, weil ffmpeg mit -f segment kaputte Zeitstempel
    nicht toleriert. Ein vorheriger Re-Mux mit +genpts erzeugt saubere — erst
    danach klappt das Neukodieren.
    """
    return await _mux(pfad, ziel, ["-fflags", "+genpts+igndts"])


def zu_gross(teile, grenze_mb=None):
    """Welche Teile reissen das Telegram-Limit?"""
    grenze = TELEGRAM_HARD_MB if grenze_mb is None else grenze_mb
    return [t for t in teile if os.path.getsize(t) / 1024 / 1024 > grenze]


def wegwerfen(teile):
    for t in teile or ():
        try:
            os.remove(t)
        except OSError:
            pass
