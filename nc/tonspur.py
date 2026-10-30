"""nc.tonspur — v4.2-W106: jede Aufnahme und jeder Restream traegt eine Tonspur.

Der Betreiber hat „fehlende Tonspuren in Aufnahmen und Restreams" gemeldet.
Nachgesehen wurde, wo eine Datei oder ein Sendestrom ohne Ton entstehen kann,
und es sind zwei verschiedene Fehlerbilder — eines still, eines laut, aber
an der falschen Stelle:

1. *Die Aufnahme* (`nc/reccmd._build_native_cmd`) lief mit `-c copy` und
   OHNE `-map`. ffmpegs Vorgabeauswahl nimmt dann „ein Video, ein Audio, falls
   vorhanden". Hat die Quelle keinen Ton — oder liefert sie ihn erst nach dem
   Probe-Fenster —, entsteht eine reine Videodatei. Kein Fehler, kein rc != 0,
   keine Zeile im Log. Der Betreiber merkt es beim Abspielen.

2. *Der Restream* (`nc/restreamcmd.build`) mappt im Transcode- und im
   TTS-Pfad hart `0:a`. Bei einer tonlosen Quelle stirbt ffmpeg sofort mit
   „Stream map '0:a' matches no streams". Das ist weder Netz noch Codec
   (`nc/restream_stability.is_codec_failure` sagt korrekt Nein), also
   verbrennt der Manager sein Reconnect-Budget an einem Fehler, der bei
   JEDEM Versuch identisch wiederkommt. Im reinen Copy-Pfad ohne Stimme gab
   es dagegen gar kein `-map` — dort ging still ein Strom ohne Ton raus.

Die Antwort ist in beiden Faellen dieselbe Stille-Quelle (`anullsrc`), nur an
verschiedenen Stellen eingesetzt:

* Restream: reaktiv. `ist_tonlos_fehler()` erkennt den Abbruch an der
  ffmpeg-Meldung, der Manager merkt sich den rid und baut neu MIT Stille.
  Kein ffprobe vor jedem Start — das wuerde jeden gesunden Sendestart um
  Sekunden verzoegern, um einen seltenen Fall abzufangen, den ffmpeg selbst
  in unter einer Sekunde meldet.
* Aufnahme: nachtraeglich. Vorab ist nicht sicher zu wissen, ob Ton kommt
  (das Probe-Fenster entscheidet), also mappt der Recorder Ton optional
  (`0:a:0?`) und `sichern()` prueft die FERTIGE Datei. Fehlt die Spur, wird
  sie mit `-c:v copy` nachgeruestet — billig, das Bild wird nicht angefasst.

Bewusst NICHT gemacht: die Quelle immer mit Stille zu mischen. Das gaebe
entweder zwei Tonspuren (FLV kann nur eine) oder verlangte `[0:a]` im
Filtergraphen — und genau das stirbt bei der tonlosen Quelle.
"""

import asyncio
import json
import logging
import os
import re
import time
from typing import List, Optional

from nc import meldetakt as _takt
from nc import kindprozess as _kind  # v4.2-W120
from nc.videoteil import _bau, platz_reicht

log = logging.getLogger("TikTokBot")

# Ein Format fuer alles, was diesen Bestand verlaesst: dieselben Werte wie die
# TTS-Haeppchen (nc/audio_cue: 44100 Hz, stereo) und wie der Restream-Encoder.
# Ein zweites Format haette an der amix-Stelle eine Resampling-Stufe mehr
# bedeutet, ohne dass jemand es merkt.
STILLE_QUELLE = "anullsrc=channel_layout=stereo:sample_rate=44100"
AAC_ARGS = ("-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2")

# Drosselkanal fuer alle Meldungen dieses Moduls. Der Schluessel ist der
# KANAL, nicht der Nutzer — bei 40 Trackings in derselben Lage drosselt ein
# Schluessel je Nutzer gar nichts (CLAUDE.md, W81/W97).
KANAL = "tonspur"

# Die Meldung von ffmpeg, wenn ein Audio-Spezifizierer ins Leere greift.
# Zwei Formen, beide gegen ffmpeg 4.4 bis 7.1 gleichlautend:
#   Stream map '0:a' matches no streams.
#   Stream specifier ':a' in filtergraph description [0:a]volume=… matches no streams.
# NUR Audio zaehlt: ein '0:v', das ins Leere greift, ist eine kaputte Quelle
# und braucht keine Stille, sondern eine neue URL.
_TONLOS = re.compile(
    r"stream (?:map '\d+:a(?::\d+)?\??'|specifier ':a(?::\d+)?')"
    r"[^\n]*matches no streams")


def stille_eingabe() -> List[str]:
    """Die Eingabeargumente einer endlosen Stille-Quelle.

    Endlos ist richtig: die Aufnahme begrenzt `-t`/`-shortest`, der Restream
    laeuft ohnehin so lange wie das Bild. Eine endliche Stille wuerde den
    Sendestrom nach ihrem Ende ohne Ton weiterlaufen lassen — das Fehlerbild,
    gegen das dieses Modul antritt.
    """
    return ["-f", "lavfi", "-i", STILLE_QUELLE]


def ist_tonlos_fehler(text) -> bool:
    """Starb ffmpeg daran, dass die Quelle keinen Ton hat?"""
    return bool(_TONLOS.search((text or "").lower()))


def hat_ton(ffprobe_json) -> Optional[bool]:
    """Traegt die Datei eine Tonspur? True / False / None (weiss nicht).

    None und nicht False, wenn die Antwort keine Streams nennt: eine Datei
    ohne erkannte Streams ist kaputt oder leer, und ihr Stille anzuhaengen
    wuerde einen Defekt hinter einer gueltig aussehenden Datei verstecken.
    Unlesbares JSON wirft ValueError — der Aufrufer meldet es.
    """
    daten = json.loads(ffprobe_json) if isinstance(ffprobe_json, (str, bytes)) \
        else ffprobe_json
    streams = daten.get("streams") if isinstance(daten, dict) else None
    arten = {s.get("codec_type") for s in (streams or []) if isinstance(s, dict)}
    if "audio" in arten:
        return True
    if "video" in arten:
        return False
    return None


def pruef_cmd(pfad) -> List[str]:
    return ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
            "-of", "json", pfad]


def nachruest_cmd(eingabe, ausgabe) -> List[str]:
    """Stille als Tonspur dazulegen, das Bild bleibt unangetastet.

    `-shortest`, weil die Stille endlos ist; ohne ihn liefe der Remux, bis
    die Platte voll ist. `+faststart` wie jede andere fertige Aufnahme.
    """
    return _bau(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-i", eingabe, *stille_eingabe(),
                 "-map", "0:v:0", "-map", "1:a:0",
                 "-c:v", "copy", *AAC_ARGS,
                 "-shortest", "-movflags", "+faststart", ausgabe])


def garantie_cmd() -> List[str]:
    """0,2 s Stille ueber DENSELBEN Eingang und Encoder wie Aufnahme und
    Restream, in den FLV-Muxer des Restreams, auf stdout.

    Nicht `-f null`: der null-Muxer laesst sich beim Bauen von ffmpeg
    getrennt abschalten, die Produktion braucht ihn nie, und ein Build ohne
    ihn haette hier „fail" gemeldet, obwohl der Rueckfall funktioniert
    (Codex-Befund auf PR #156)."""
    return _bau(["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error",
                 *stille_eingabe(), "-t", "0.2", *AAC_ARGS, "-f", "flv", "pipe:1"])


def garantie(timeout=10):
    """v4.2-W114: kann dieses ffmpeg die Stille-Spur ueberhaupt erzeugen?
    -> (stufe, text) fuer den Preflight.

    Die ganze Ton-Garantie aus W106 haengt an zwei Faehigkeiten — dem
    lavfi-Eingang `anullsrc` und dem AAC-Encoder. Fehlt eine (abgespeckte
    ffmpeg-Builds, statische Minimal-Pakete), stirbt jeder Rueckfall auf
    Stille, und zwar genau in dem Moment, in dem eine Quelle keinen Ton hat.
    „ffmpeg installiert" sagt darueber nichts; deshalb laeuft hier ein
    echter Kurzlauf statt eines Blicks auf `-filters`.
    """
    import subprocess
    try:
        p = subprocess.run(garantie_cmd(), capture_output=True,
                           timeout=timeout, stdin=subprocess.DEVNULL)
    # Jeder Fehlerzweig meldet auch ins Log (gedrosselt): der Preflight wird
    # nur angesehen, wenn jemand hinsieht, der Selbsttest nur beim Start.
    except FileNotFoundError:
        _melde("warning", "garantie", "Tonspur-Garantie: ffmpeg fehlt.")
        return "fail", "ffmpeg fehlt — ohne ffmpeg keine Aufnahme und keine Stille-Spur"
    except subprocess.TimeoutExpired:
        _melde("warning", "garantie", "Tonspur-Garantie: Probelauf nach %d s "
               "abgebrochen.", timeout)
        return "warn", ("Probelauf nach %d s abgebrochen — Maschine ueberlastet? "
                        "Die Stille-Spur ist damit ungeprueft." % timeout)
    except OSError as e:
        # Der Ausnahmetext (Pfade, Rechte) geht ins Log, nicht in die
        # Preflight-Antwort — die liest der Browser (CodeQL, PR #156).
        _melde("warning", "garantie", "Tonspur-Garantie: ffmpeg nicht startbar (%s).", e)
        return "fail", "ffmpeg nicht startbar — Grund im Log (Tonspur-Garantie)"
    if p.returncode == 0:
        return "ok", "Stille-Spur (anullsrc) und AAC verfuegbar"
    err = (p.stderr or b"").decode("utf-8", "replace")
    zeile = (err.strip().splitlines() or ["rc=%s" % p.returncode])[-1][:160]
    _melde("error", "garantie", "Tonspur-Garantie: ffmpeg kann keine Stille-Spur "
           "erzeugen (%s) — Abhilfe: sudo apt install ffmpeg.", zeile)
    return "fail", ("ffmpeg kann keine Stille-Spur erzeugen (%s) — eine Quelle "
                    "ohne Ton ergaebe Aufnahmen und Restreams ohne Tonspur. "
                    "Abhilfe: ffmpeg mit lavfi und AAC installieren "
                    "(sudo apt install ffmpeg)." % zeile)


class Fehlschlag(Exception):
    """Ein Werkzeuglauf hat nichts Brauchbares geliefert; der Text sagt warum."""


def _melde(stufe, grund, text, *args):
    """Gedrosselt melden — erste Meldung sofort, dann hoechstens alle 15 min."""
    laut, weg = _takt.melden(KANAL, grund, time.time())
    if not laut:
        return
    if stufe == "error":
        log.error(text + _takt.zusatz(weg), *args)
    else:
        log.warning(text + _takt.zusatz(weg), *args)


def _wegraeumen(pfad):
    try:
        os.remove(pfad)
    except OSError:
        pass                            # lag gar nicht erst da


async def _lauf(cmd, timeout):
    """-> (rc, stdout, stderr). Wirft Fehlschlag, wenn der Lauf nicht zustande
    kam — ein Rueckgabewert „kein Ergebnis" waere der stille Pfad, gegen den
    dieses Modul antritt."""
    # v4.2-W120: ueber nc.kindprozess — abgeraeumt wird dort, auf jedem Weg,
    # auch beim Abbruch des Aufrufers.
    try:
        return await _kind.ausfuehren(cmd, timeout, art=cmd[0])
    except asyncio.TimeoutError:
        raise Fehlschlag("%s antwortete %d s lang nicht" % (cmd[0], timeout)) from None
    except (OSError, ValueError) as e:
        raise Fehlschlag("%s liess sich nicht starten: %s" % (cmd[0], e)) from e


def _text(err, rc):
    return (err or b"").decode("utf-8", "replace").strip()[:300] or "rc=%s" % rc


async def pruefen(pfad, timeout=20) -> Optional[bool]:
    """Traegt die fertige Datei Ton? None, wenn sich das nicht klaeren liess."""
    try:
        rc, out, err = await _lauf(pruef_cmd(pfad), timeout)
        if rc != 0:
            raise Fehlschlag(_text(err, rc))
        lage = hat_ton(out)
        if lage is None:
            raise Fehlschlag("ffprobe nennt weder Bild noch Ton — Datei leer "
                             "oder kaputt")
        return lage
    except (Fehlschlag, ValueError) as e:
        _melde("warning", "ffprobe",
               "Tonspur: ob %s Ton traegt, liess sich nicht klaeren (%s) — "
               "Stille wird NICHT angehaengt. Abhilfe: fehlt ffprobe, "
               "sudo apt install ffmpeg.", pfad, e)
        return None


async def sichern(pfad, wer="?", timeout=600) -> dict:
    """Stellt sicher, dass die fertige Aufnahme eine Tonspur traegt.

    -> {"lage": "ton"|"nachgeruestet"|"unbekannt"|"fehlgeschlagen",
        "groesse": Bytes der Datei danach}

    Scheitert das Nachruesten, bleibt das Original liegen: eine Aufnahme ohne
    Ton ist schlechter als eine mit, aber unendlich besser als keine.
    """
    lage = await pruefen(pfad)
    if lage is not False:
        return {"lage": "ton" if lage else "unbekannt", "groesse": _groesse(pfad)}

    ok, frei = platz_reicht(pfad, faktor=1.05)
    if not ok:
        _melde("error", "platz",
               "Tonspur %s: Aufnahme OHNE Ton (%s), und fuer die Nachruestung "
               "fehlt der Platz (%s). Abhilfe: Platte freiraeumen; die Datei "
               "bleibt stumm.", wer, pfad, frei)
        return {"lage": "fehlgeschlagen", "groesse": _groesse(pfad)}

    stamm, endung = os.path.splitext(pfad)
    tmp = stamm + ".tonspur" + (endung or ".mp4")
    try:
        rc, _out, err = await _lauf(nachruest_cmd(pfad, tmp), timeout)
        if rc != 0 or not os.path.isfile(tmp) or os.path.getsize(tmp) == 0:
            raise Fehlschlag(_text(err, rc))
        os.replace(tmp, pfad)
    except (Fehlschlag, OSError) as e:
        _wegraeumen(tmp)
        _melde("error", "fehlgeschlagen",
               "Tonspur %s: Aufnahme OHNE Ton (%s), Nachruestung gescheitert: "
               "%s. Abhilfe: ffmpeg mit lavfi pruefen (ffmpeg -f lavfi -i "
               "anullsrc -t 1 -f null -).", wer, pfad, e)
        return {"lage": "fehlgeschlagen", "groesse": _groesse(pfad)}
    _melde("warning", "nachgeruestet",
           "Tonspur %s: die Quelle lieferte keinen Ton — Stille-Spur "
           "nachgeruestet (%s). Spielt jetzt ueberall ab; hoerbar ist nichts, "
           "weil die Quelle nichts gesendet hat.", wer, pfad)
    return {"lage": "nachgeruestet", "groesse": _groesse(pfad)}


def _groesse(pfad):
    try:
        return os.path.getsize(pfad)
    except OSError as e:
        _melde("warning", "groesse",
               "Tonspur: Groesse von %s nicht lesbar (%s).", pfad, e)
        return 0


def hat_tonspur(cmd, optional_ok=False) -> bool:
    """Vertragshelfer: garantiert dieser ffmpeg-Befehl eine Tonspur im Ausgang?

    Ja heisst: ein `-map` greift auf Ton (`N:a…` oder den Filter-Ausgang
    `[a]`). Ohne jedes `-map` gilt die Vorgabeauswahl von ffmpeg, und die
    nimmt bei tonloser Quelle still nur das Bild: das ist hier ein Nein, kein
    Vielleicht. Ein optionales `0:a:0?` ist nur dann genug, wenn der Aufrufer
    die fertige Datei nachprueft (`optional_ok`, der Recorder mit `sichern`).
    """
    maps = [cmd[i + 1] for i, a in enumerate(cmd[:-1]) if a == "-map"]
    for m in maps:
        if m == "[a]" or re.match(r"^\d+:a(:\d+)?$", m):
            return True
        if optional_ok and re.match(r"^\d+:a(:\d+)?\?$", m):
            return True
    return False
