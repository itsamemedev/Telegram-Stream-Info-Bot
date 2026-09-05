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
import glob
import logging
import os
import shutil

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


def configure(threads_bg=None, nice_bg=None):
    """Die beiden ffmpeg-Stellschrauben aus der .env.

    Als Funktion gelesen und nicht als Modul-Konstante: .env wird teils erst
    nach den ersten Importen geladen (CLAUDE.md). Der Bot ruft das beim Start.
    """
    _cfg["threads_bg"] = threads_bg
    _cfg["nice_bg"] = nice_bg


def _bau(cmd):
    return ff_cmd(cmd, threads=_cfg["threads_bg"], nice=_cfg["nice_bg"])


async def _toete(p):
    """Prozess abraeumen. kill() ALLEIN reicht nicht — ohne wait() bleibt ein
    Zombie stehen, und nach ein paar hundert Aufnahmen ist die Prozesstabelle
    voll (F42-B4)."""
    if p is None:
        return
    try:
        p.kill()
    except Exception:
        pass
    try:
        await asyncio.wait_for(p.wait(), timeout=2)
    except Exception:
        pass


async def dauer(pfad):
    """Exakte Laufzeit in Sekunden via ffprobe. None bei Fehler.

    None und nicht 0.0: der Aufrufer muss "weiss ich nicht" von "ist leer"
    unterscheiden koennen — an dieser Unterscheidung haengt, ob er die
    Bitrate rechnet oder auf den konservativen Rueckfall geht.
    """
    p = None
    try:
        p = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", pfad,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL)
        try:
            out, _ = await asyncio.wait_for(p.communicate(), timeout=15)
        except asyncio.TimeoutError:
            await _toete(p)
            return None
        if p.returncode != 0:
            return None
        return float((out or b"").strip() or 0) or None
    except Exception:
        if p and p.returncode is None:
            await _toete(p)
        return None


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


async def _pruefe_teile(muster):
    """Die erzeugten Teile durchsehen und Schrott wegwerfen (B52).

    Ohne diese Pruefung landen header-only-Dateien und Teile ohne Stream beim
    Upload — und der scheitert dann mit einer Telegram-Fehlermeldung, die
    nichts ueber die Ursache sagt.
    """
    kandidaten = sorted(glob.glob(muster))
    gut = []
    for teil in kandidaten:
        try:
            groesse = os.path.getsize(teil)
            if groesse < _MIN_TEIL_BYTES:
                log.warning("split: Teil %s ist nur %dB — geloescht",
                            os.path.basename(teil), groesse)
                try:
                    os.remove(teil)
                except OSError:
                    pass
                continue
            if (await dauer(teil) or 0) <= 0:
                log.warning("split: Teil %s hat keine erkennbare Dauer — "
                            "vermutlich kaputt, geloescht", os.path.basename(teil))
                try:
                    os.remove(teil)
                except OSError:
                    pass
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
    groesse_mb = os.path.getsize(pfad) / 1024 / 1024
    laenge = await dauer(pfad)
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

    cmd = _bau(["ffmpeg", "-y", "-i", pfad, "-c", "copy", "-map", "0",
                "-f", "segment", "-segment_time", str(seg),
                "-segment_format", "mp4", "-reset_timestamps", "1",
                "-movflags", "+faststart",
                f"{praefix}_%03d.mp4"])
    p = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
    # Ohne Zeitdeckel blockiert ein haengendes ffmpeg (korrupter Input mit
    # read-hang) den Event-Loop unbegrenzt und friert JEDE andere Aufnahme ein.
    deckel = max(300, int(seg * 4) + 120)
    try:
        _, stderr = await asyncio.wait_for(p.communicate(), timeout=deckel)
    except asyncio.TimeoutError:
        await _toete(p)
        return None, f"ffmpeg split timeout nach {deckel}s (segment_time={seg})"
    if p.returncode != 0:
        # Der echte Fehler steht am ENDE von stderr; der Anfang ist Banner.
        schwanz = _ffmpeg_stderr_tail(stderr.decode(errors="ignore"), max_len=800)
        return None, (f"[rc={p.returncode}] ffmpeg -segment_time {seg} → "
                      f"{praefix}_%03d.mp4\n{schwanz}")

    kandidaten, gut = await _pruefe_teile(f"{praefix}_*.mp4")
    if not gut:
        return None, "Alle Teile vom Split waren ungueltig (ffprobe-failed)"
    if len(gut) < len(kandidaten):
        log.warning("split: %d/%d Teile verworfen wegen Validierungsfehler — "
                    "%d verbleiben", len(kandidaten) - len(gut), len(kandidaten), len(gut))
    return gut, None


async def neu_kodieren(pfad, praefix, ziel_mb):
    """Letzter Ausweg: mit erzwungenen Keyframes neu kodieren.

    WARUM ES DAS BRAUCHT (B70): der Segment-Muxer mit -c copy kann NUR an
    vorhandenen Keyframes schneiden. Hat ein TikTok-Stream sehr wenige (langer
    GOP), entsteht ein einziger riesiger Teil, den weiteres Halbieren nicht
    kleiner macht — im Log: "part 1/1 bleibt 68 MB". Hier werden Keyframes an
    den Segmentgrenzen erzwungen und die Bitrate gedeckelt. Langsamer als
    Kopieren, dafuer zuverlaessig.
    """
    laenge = await dauer(pfad)
    groesse_mb = os.path.getsize(pfad) / 1024 / 1024
    if not laenge or laenge <= 0:
        laenge = max(30.0, groesse_mb)          # grobe Annahme
    orig_mbps = (groesse_mb * 8) / laenge
    # Bitrate moderat deckeln: begrenzt die Teilgroesse, haelt die Qualitaet.
    vbps = max(0.4, min(orig_mbps, 4.0))
    gesamt_mbps = vbps + 0.128                  # + AAC 128k
    # Segmentlaenge so, dass bitrate*seg/8 <= ziel_mb (8 % Reserve)
    seg = max(15, int((ziel_mb * 8 * 0.92) / max(gesamt_mbps, 0.3)))
    vbr = f"{int(vbps * 1000)}k"
    cmd = _bau(["ffmpeg", "-y",
                # toleriert Non-monotonic DTS ("pts has no value")
                "-fflags", "+igndts",
                "-i", pfad,
                "-c:v", "libx264", "-preset", "veryfast", "-b:v", vbr,
                "-maxrate", f"{int(vbps * 1000 * 1.2)}k",
                "-bufsize", f"{int(vbps * 1000 * 2)}k",
                "-force_key_frames", f"expr:gte(t,n_forced*{seg})",
                "-c:a", "aac", "-b:a", "128k",
                "-f", "segment", "-segment_time", str(seg),
                "-segment_format", "mp4", "-reset_timestamps", "1",
                "-movflags", "+faststart", f"{praefix}_re_%03d.mp4"])
    log.info("re-encode split: dur=%.0fs, vbr=%s, seg=%ds (orig~%.1fMbps)",
             laenge, vbr, seg, orig_mbps)
    p = None
    try:
        p = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        # Grosszuegig: Neukodieren ist deutlich langsamer als Kopieren.
        _, stderr = await asyncio.wait_for(p.communicate(),
                                           timeout=max(600, int(laenge * 3)))
    except asyncio.TimeoutError:
        await _toete(p)
        return None, "re-encode timeout"
    except Exception as e:
        return None, f"re-encode exception: {e}"
    if p.returncode != 0:
        return None, _ffmpeg_stderr_tail(stderr.decode(errors="ignore"), 600)

    _, gut = await _pruefe_teile(f"{praefix}_re_*.mp4")
    if not gut:
        return None, "re-encode: keine gueltigen Teile"
    return gut, None


async def _mux(pfad, ziel, flags, deckel=300):
    """Neu muxen ohne neu zu kodieren. -> (ok, fehlertext)"""
    p = None
    try:
        p = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y", *flags, "-i", pfad,
            "-c", "copy", "-movflags", "+faststart", ziel,
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        _, stderr = await asyncio.wait_for(p.communicate(), timeout=deckel)
    except asyncio.TimeoutError:
        await _toete(p)
        return False, "timeout"
    except Exception as e:
        return False, str(e)
    if p.returncode == 0 and os.path.exists(ziel) and os.path.getsize(ziel) > 0:
        return True, None
    if os.path.exists(ziel):
        try:
            os.remove(ziel)
        except OSError:
            pass
    return False, (_ffmpeg_stderr_tail(stderr.decode(errors="ignore"), 400)
                   if stderr else f"rc={p.returncode}")


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
