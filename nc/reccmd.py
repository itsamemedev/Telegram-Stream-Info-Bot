"""nc.reccmd — die Kommandozeilen des Recorders, aus bot.py heraus (v4.2-W17).

400 Zeilen, die entscheiden, WOMIT aufgenommen wird (nativer ffmpeg-Pull oder
yt-dlp) und mit welchen Argumenten. Das ist der Pfad, an dem der Betrieb
haengt: faellt er aus, gibt es keine Aufnahme — und im Monolithen war er aus
demselben Grund ungetestet wie der Relay-Bauer (W16), naemlich weil er an
zwanzig Bot-Globals hing und hier kein ffmpeg laeuft.

**Zwei Dinge tragen hier das Risiko:**

1. *Der Cookie.* Beide Befehle transportieren die TikTok-Session — der native
   Pfad als `-headers`-Blob, yt-dlp als `--cookies <Datei>`. Wer sie
   ungefiltert loggt, schreibt die Session ins Klartext-Log (F4). Der
   Redaktionspfad liegt in nc/ffdiag.redact_cmd_for_log und deckt BEIDE Formen
   ab; ein Vertrag haelt das fest.
2. *Der 403-Umschalter.* Blockt TikTok die CDN-URL fuer unsere Egress-IP,
   stellt der Bot den User zeitweise auf yt-dlp um. Faellt diese Weiche
   falsch, nimmt der Bot mit dem Pfad auf, der garantiert 403 bekommt — und
   das sieht im Log aus wie ein toter Stream, nicht wie ein Konfigurations-
   fehler.

Verhalten bitgenau wie im Monolithen; der Rumpf ist ZEICHENGLEICH uebernommen.
Die Werte, die vorher Modul-Globale von bot.py waren, sind hier Modul-Globale,
die configure() belegt — dieselbe Begruendung wie in nc/restreamcmd.py: ein
Umschreiben auf Woerterbuch-Zugriffe haette jede der 400 Zeilen zu einer
moeglichen Regression gemacht, fuer einen Pfad, den hier nichts ausfuehren
kann.

configure() lehnt unbekannte UND fehlende Schluessel ab. Ein stiller Default
hiesse hier: falscher Recorder, fehlende Cookies, kein Thread-Deckel — und
nichts wird rot.
"""

import asyncio
import logging
import shutil
import time as _time_mod
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:            # nur fuer die Signatur-Annotation
    # NICHT zur Laufzeit importieren: der Vertrags-Job der CI installiert nur
    # orjson und flask. Ein echter Import haette den Job an einem nackten
    # ImportError sterben lassen, ohne dass ein einziger Vertrag laeuft.
    import aiohttp

from nc.ffbuild import ff_cmd as _ff_cmd_roh
from nc.preflight import _preflight_url
from nc.proxyutil import _pick_pull_proxy

log = logging.getLogger("TikTokBot")


def _ff_cmd(cmd, threads=None, nice=None):
    return _ff_cmd_roh(cmd, threads=threads, nice=nice)


# ══════════════════════════════════════════════════════════════════════════
# Vom Bot belegt — siehe configure(). Vorher alles None: ein Zugriff davor
# soll krachen und nicht still mit einem Default aufnehmen.
# ══════════════════════════════════════════════════════════════════════════
_cookie_header = None                # Cookie-Header der TikTok-Session
_ensure_cookie_file_netscape = None  # schreibt die Netscape-Cookie-Datei
_pick_checked_pull_proxy = None      # Proxy, der vorher geprueft wurde
_stream_url_ttl = None               # Restlaufzeit der signierten Quell-URL
log_event = None                     # Ereignisprotokoll
resolve_tiktok_live_stream = None    # loest eine frische Quell-URL auf

# Geteilter Zustand: DIESELBEN Objekte wie im Bot, keine Kopien. Eine zweite
# Kopie, und der 403-Umschalter zaehlte in einem Dict, waehrend der Recorder
# das andere liest.
_REC_403_UNTIL = None
_REC_PROXY = None
_REC_PROXY_FAILED = None
_REC_PROXY_LOCK = None

COOKIE_FILE = None
FFMPEG_NICE_RECORD = None
FFMPEG_THREADS_RECORD = None
RECORDER_PREF = None
RECORD_403_YTDLP = None
_STREAM_URL_MIN_TTL = None

_PFLICHT = (
    "cookie_header", "ensure_cookie_file_netscape", "pick_checked_pull_proxy",
    "stream_url_ttl", "log_event", "resolve_tiktok_live_stream",
    "REC_403_UNTIL", "REC_PROXY", "REC_PROXY_FAILED", "REC_PROXY_LOCK",
    "COOKIE_FILE", "FFMPEG_NICE_RECORD", "FFMPEG_THREADS_RECORD",
    "RECORDER_PREF", "RECORD_403_YTDLP", "STREAM_URL_MIN_TTL",
)

# Namen, die im Rumpf einen fuehrenden Unterstrich tragen. Der Aufrufer soll
# ihn nicht mitschreiben muessen; die Zuordnung steht hier statt in einer
# Heuristik, damit ein neuer Schluessel eine bewusste Zeile ist.
_UNTERSTRICH = {
    "cookie_header", "ensure_cookie_file_netscape", "pick_checked_pull_proxy",
    "stream_url_ttl", "REC_403_UNTIL", "REC_PROXY", "REC_PROXY_FAILED",
    "REC_PROXY_LOCK", "STREAM_URL_MIN_TTL",
}


def configure(**kw):
    """Der Bot reicht seine Werte einmal beim Start herein."""
    unbekannt = sorted(set(kw) - set(_PFLICHT))
    fehlt = sorted(set(_PFLICHT) - set(kw))
    if unbekannt or fehlt:
        raise ValueError(
            "reccmd.configure: unbekannt=%s fehlt=%s" % (unbekannt, fehlt))
    g = globals()
    for k, v in kw.items():
        g["_" + k if k in _UNTERSTRICH else k] = v


def _find_external_recorder():
    """Findet yt-dlp falls auf dem System. Nur für Pref-Logik.
       F43: Liefert nur noch yt-dlp (streamlink raus). Rückgabetyp ist single
       Wert, nicht mehr Tuple — die zwei Call-Sites wurden mit-angepasst."""
    return shutil.which("yt-dlp") or shutil.which("yt_dlp")


def _build_native_cmd(stream_url: str, output_file: str, duration_secs: int,
                      pull_proxy: Optional[str] = None) -> List[str]:
    """ffmpeg-Befehl der eine HLS- oder FLV-URL aufnimmt. -c copy = keine Re-Enkodierung.
       F44: FLV-Unterstützung. Der AAC-Bitstream-Filter (aac_adtstoasc) wird nur
       für HLS/MPEG-TS-Quellen gesetzt — bei FLV ist die AAC bereits in ASC-Form
       und ffmpeg würde einen WARN-Log schreiben (funktioniert aber). Filter nur
       wo nötig spart einen Wall-of-warnings im Log.
       F45: Reconnect-Flags härter eingestellt für Streams mit flaky Verbindung
       (TikTok-CDN-Hickups, kurze TCP-RSTs etc). Vorher endeten Aufnahmen oft
       nach ~14s mit rc=-9 wenn mitten in einem Reconnect-Versuch ein I/O-Error
       kam. Jetzt: Reconnect-Window 30s (statt 5s), HTTP-Error-Retry,
       rw_timeout auf 60s, multiple_requests aktiv. Werte sind konservativ
       gewählt — ffmpeg kann auf diesen Settings bis zu 30s "ruhig" sein bevor
       wir aufgeben. Der Stall-Watchdog (90s) fängt echte Hänger eh noch ab.

       B56 (Production-Bug 2026-05-25): Operator hat berichtet dass `native+api`
       (HLS) funktioniert, `native+api-flv` aber nicht. Root-Cause:
       (a) `+frag_keyframe` wartet auf einen H.264-Keyframe bevor das erste
           Fragment geschrieben wird. Bei FLV-Streams mit GOP=4-5s + AVC
           Sequence Header als erstem Video-Tag kann ffmpeg minutenlang
           buffern ohne einen einzigen Byte zu schreiben.
       (b) `-multiple_requests` (HTTP keep-alive) ist für single-connection
           HTTP-FLV Streams irrelevant und kann Verwirrung stiften.
       (c) Kein `-timeout` Flag → ffmpeg hängt bis OS TCP-timeout (~60s)
           wenn TikTok FLV-CDN keinen Body sendet → unser stall_watchdog
           SIGKILLt vor jeglichem stderr-Output = "empty stderr".
       Fix: FLV-spezifische cmd-Variante ohne `+frag_keyframe`, ohne
       `-multiple_requests`, MIT `-timeout` für connection-establishment.

       B58: -hide_banner entfernt — wir BRAUCHEN den Banner als Diagnose-
       Info wenn ffmpeg vor jeglichem Stream-Output stirbt (B55-Fallback
       gibt den Banner zurück). Ohne Banner: 'empty stderr' wie vorher,
       keine Diagnose möglich."""
    cookie_hdr = _cookie_header()
    headers_list = []
    if cookie_hdr:
        headers_list.append(f"Cookie: {cookie_hdr}")
    headers_list.append("Referer: https://www.tiktok.com/")
    # ffmpeg erwartet die headers als ein Argument, durch \r\n getrennt,
    # mit abschließendem \r\n
    headers_blob = "\r\n".join(headers_list) + "\r\n"

    # B56: Stream-Format detection — beeinflusst Mux-Flags + Reconnect-Strategie
    url_lc = stream_url.lower()
    is_hls = ".m3u8" in url_lc
    is_flv = (".flv" in url_lc or "/flv/" in url_lc or "pull-flv" in url_lc)

    cmd = [
        "ffmpeg",
        "-y",
        # B58: KEIN -hide_banner mehr. Der Banner enthält wichtige Diagnose-
        # Info (ffmpeg version, build config, libavformat version etc) die
        # B55 als fallback verwendet wenn der Stream gar nicht startet.
        "-loglevel", "warning",
        # B56/Fix: -timeout NUR für HLS (siehe is_hls-Block unten). Bei FLV kennt
        # älteres ffmpeg (4.x) die Option nicht → "Option timeout not found" → Input
        # öffnet gar nicht. rw_timeout (unten) deckt Connect+Read bei HTTP ab.
        # F45: HTTP-Reconnect-Verhalten — robust gemacht.
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "30",                # 30s patience für reconnect
        # B124-FIX: NICHT mehr "4xx,5xx". Das schloss 404 und 403 ein — beide
        # sind bei TikTok TERMINAL, nicht vorübergehend:
        #   404 = die CDN-Pull-URL ist weg. Sie trägt ein expire=<ts> im
        #         Query-String; nach Ablauf oder Edge-Wechsel existiert sie
        #         nicht mehr. Dieselbe URL erneut anzufragen kann per
        #         Definition nie gelingen.
        #   403 = blockiert (Cookies/Proxy). Wiederholen verschärft das nur.
        # Beobachtet am 2026-07-24 bei @tatjana335: fünf Reconnects über
        # 60 Sekunden gegen ein 404, danach Abbruch ohne eine Sekunde Material.
        # Die einzige Rettung wäre gewesen, die Stream-URL NEU AUFZULÖSEN —
        # und genau das tut der Bot beim nächsten Versuch, sobald ffmpeg
        # schnell aufgibt. Die eigene Diagnose-Empfehlung im Code sagt das
        # seit Langem ("bei 404 schnell aufhören statt zu hämmern"), nur die
        # ffmpeg-Argumente folgten ihr nicht.
        # Es bleiben die WIRKLICH vorübergehenden Codes.
        # BEWUSST KEIN -reconnect_delay_total_max: die Option gibt es erst ab
        # ffmpeg 6.1. Eine unbekannte Option laesst den Input gar nicht erst
        # oeffnen (siehe -timeout-Kommentar oben) — das wuerde JEDE Aufnahme
        # brechen. Der Deckel entsteht ohnehin dadurch, dass 404 jetzt gar
        # nicht mehr zum Wiederverbinden fuehrt.
        "-reconnect_on_http_error", "408,429,500,502,503,504",
        "-reconnect_on_network_error", "1",          # retry auf TCP/network errors
        # B56: -rw_timeout auf 30s gesenkt (war 60s). Unser stall_watchdog
        # killt nach 45s. Wenn ffmpeg's eigener rw_timeout später als unser
        # Watchdog liegt, killen wir ffmpeg BEVOR es einen Error meldet =
        # "empty stderr". Jetzt: rw_timeout 30s < watchdog 45s → ffmpeg
        # liefert "Connection timed out" stderr-Output, wir sehen die Ursache.
        "-rw_timeout", "30000000",
    ]
    # B59 (Production-Bug 2026-05-29): @thomasschwarz180 — ffmpeg loopte mit
    # "Will reconnect at <byte>... Input/output error" und beendete dann mit
    # "Could not write header (incorrect codec parameters ?)". Root-Cause:
    # ffmpeg konnte aus dem flaky Input nicht genug Daten lesen um die Codec-
    # Parameter (codec-id, Auflösung, Sample-Rate) zu bestimmen → der MP4-
    # Header-Write (selbst mit +empty_moov) scheiterte, 0-Byte-File, Watchdog
    # killte bei 60s. Fix: analyzeduration + probesize hochsetzen (Default 5s/
    # 5MB → 10s/15MB) damit ffmpeg bei langsamer/teilweiser Codec-Lieferung
    # länger probt bevor es den Header schreibt. Beide sind Input-Optionen,
    # müssen VOR -i stehen. 10s liegt unter dem 45s-Stall-Threshold.
    cmd += [
        "-analyzeduration", "10000000",              # 10s (statt default 5s)
        "-probesize", "15000000",                    # 15 MB (statt default 5MB)
    ]
    # B56: -multiple_requests nur für HLS (lädt viele segments mit keep-alive).
    # Für FLV (single long-running connection) irrelevant + kann CDNs verwirren.
    if is_hls:
        cmd += ["-multiple_requests", "1"]   # -timeout komplett entfernt: älteres ffmpeg kennt die Option für HTTP/HLS nicht → "Option timeout not found". rw_timeout deckt Connect+Read ab.
        # F82: TikTok-CDN liefert m3u8 mit falschem MIME-Type ("mime type is not
        # rfc8216 compliant" im Prod-Log) und teils untypischen Segment-Endungen.
        # Neuere ffmpeg-Builds BLOCKIEREN dann Segmente. ALL = Endungs-Check aus
        # (Option existiert seit ffmpeg 3.x → auch auf dem Server-4.x sicher).
        cmd += ["-allowed_extensions", "ALL"]
    # B56: FLV-spezifisch: +flush_packets = ffmpeg flusht Packets sofort zum
    # Output. Verhindert dass der Muxer minutenlang buffert.
    if is_flv:
        cmd += ["-fflags", "+flush_packets"]
    else:
        # B60 (Prod-Bug 2026-06-22): @senekayra0/@hasischaosqueen1601k25 — HLS-Input
        # lieferte Packets OHNE PTS ("Timestamps are unset", "pts has no value" x370)
        # + non-monotonic DTS. Folge: MP4-Muxer schrieb nichts mehr -> Datei wuchs
        # nicht -> stall_killed nach ~12min. +genpts erzeugt fehlende Presentation-
        # Timestamps, +flush_packets schreibt sofort raus (Datei waechst sichtbar).
        # B60+: +igndts ergaenzt — ignoriert die kaputten Input-DTS direkt (gleiche
        # Kombi wie der bewaehrte Remux unten). Behebt "Non-monotonic DTS" an der Quelle,
        # +genpts fuellt fehlende PTS, +flush_packets schreibt sofort raus.
        cmd += ["-fflags", "+genpts+igndts+flush_packets"]
    cmd += [
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/131.0.0.0 Safari/537.36",
        "-headers", headers_blob,
    ]
    # PULL über den gewählten Proxy: pull_proxy kommt von build_recording_cmd (RECORD_PROXY
    # → PROXY_LIST → TikTok-validierter Pool, rotiert bei Block). Ohne Vorgabe: selbst wählen.
    # -http_proxy ist Input-Option, muss vor -i stehen; gilt für http UND https (CONNECT).
    _pp = pull_proxy if pull_proxy is not None else _pick_pull_proxy()
    if _pp:
        cmd += ["-http_proxy", _pp]
    cmd += [
        "-i", stream_url,
        "-t", str(duration_secs),                    # Maximale Aufnahmedauer
        "-c", "copy",                                # Kein Re-Encoding
    ]
    if is_hls:
        cmd += ["-bsf:a", "aac_adtstoasc"]           # nur für HLS/TS nötig

    # B56: Mux-Flags je nach Input-Format wählen
    if is_flv:
        # FLV → MP4 ohne +frag_keyframe. Begründung:
        # +frag_keyframe würde auf einen H.264-IDR-Keyframe warten bevor das
        # erste moof-Fragment geschrieben wird. Bei TikTok-FLV mit GOP=4-5s
        # und AVC Sequence Header als erstem Tag heißt das: minutenlanges
        # Buffering ohne ein einziges Byte auf Disk → stall_watchdog killt.
        # Stattdessen: +empty_moov+default_base_moof reicht für Crash-
        # Resilience (B51), +frag_duration 2s schreibt zeit-basierte
        # Fragments unabhängig von Keyframes.
        cmd += [
            "-movflags", "+empty_moov+default_base_moof+faststart",
            "-frag_duration", "2000000",             # 2s Time-based Fragments
            "-max_interleave_delta", "0",            # B60: Interleave-Stall vermeiden
            "-avoid_negative_ts", "make_zero",
            output_file,
        ]
    else:
        # HLS (oder Unknown) → volle B51-Settings mit +frag_keyframe.
        # Bei HLS funktioniert das einwandfrei weil TS-Segmente meist
        # bei Keyframes anfangen + Codec-Bootstrap direkt geliefert wird.
        cmd += [
            "-movflags", "+empty_moov+frag_keyframe+default_base_moof+faststart",
            "-frag_duration", "2000000",
            # B60: Muxer NICHT auf Stream-Interleaving warten lassen (sonst buffert
            # er bei kaputten DTS endlos -> Datei stoppt -> stall). Sofort schreiben.
            "-max_interleave_delta", "0",
            "-avoid_negative_ts", "make_zero",       # non-monotonic/negative DTS glaetten
            output_file,
        ]
    # V37-CPU: -c copy braucht praktisch keine Rechenzeit, aber ffmpeg startet
    # ohne Deckel trotzdem Threads pro Kern. nice haelt die Aufnahme hinter dem
    # Sendebild — sie ist I/O-gebunden und verliert dadurch nichts.
    return _ff_cmd(cmd, threads=FFMPEG_THREADS_RECORD, nice=FFMPEG_NICE_RECORD)


def _build_ytdlp_cmd(bin_path: str, url: str, output_file: str, duration_secs: int,
                     pull_proxy: Optional[str] = None) -> List[str]:
    """yt-dlp + ffmpeg als External-Downloader.
    VERBESSERUNG: --concurrent-fragments 4 für schnelleres Segment-Laden,
    --retries erhöht, --retry-sleep für stabileres Verhalten bei CDN-Hickups,
    UA auf Chrome 131 aktualisiert."""
    cmd = [
        bin_path, url,
        "-o", output_file,
        "--no-part",
        "--no-progress",
        "--no-warnings",
        "--retries", "10",
        "--fragment-retries", "10",
        "--retry-sleep", "linear=1::2",
        "--socket-timeout", "30",
        "--concurrent-fragments", "4",
        "--http-chunk-size", "10M",
        "--external-downloader", "ffmpeg",
        "--external-downloader-args", f"ffmpeg:-t {duration_secs}",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36",
        "--referer", "https://www.tiktok.com/",
        "--add-header", "sec-fetch-site:same-origin",
        "--add-header", "sec-fetch-mode:navigate",
    ]
    # PULL über den gewählten Proxy (RECORD_PROXY → PROXY_LIST → TikTok-validierter Pool).
    _pp = pull_proxy if pull_proxy is not None else _pick_pull_proxy()
    if _pp:
        cmd += ["--proxy", _pp]
    if _ensure_cookie_file_netscape():
        cmd += ["--cookies", COOKIE_FILE]
    return cmd


def _stream_url_is_fresh(url: Optional[str], min_ttl: Optional[int] = None) -> bool:
    """True wenn die URL noch >= min_ttl Sekunden gültig ist. Hat die URL kein
       expire-Token, können wir's nicht prüfen → optimistisch True."""
    ttl = _stream_url_ttl(url)
    if ttl is None:
        return True
    return ttl >= (min_ttl if min_ttl is not None else _STREAM_URL_MIN_TTL)


async def build_recording_cmd(username: str, output_file: str, duration_secs: int,
                              session: Optional["aiohttp.ClientSession"] = None,
                              preferred: Optional[str] = None,
                              prefetched_info: Optional[dict] = None
                              ) -> tuple:
    """Returns (cmd_list, recorder_name) — wählt nach RECORDER_PREF und Verfügbarkeit.
       Async, weil der native Recorder die Stream-URL erst auflösen muss.

       F22: 'preferred' überschreibt RECORDER_PREF NUR für diesen Call.
            Spezialwert 'native_api' = native Recorder mit API-only Resolver
            (kein HTML-Fallback). Wird nach Aufnahme-Fehlschlägen vom Caller
            gesetzt um auf den vertrauenswürdigsten Pfad zu pinnen.
       F35: 'prefetched_info' — die Detection hat eventuell schon die HLS-URL
            geholt. Statt einen zweiten Roundtrip zu machen reichen wir das
            durch. Spart 1-2s pro Recording-Start + reduziert API-Last.
       F42: native_api fällt jetzt auf yt-dlp zurück wenn es selbst scheitert.
            Vorher war's ein Hard-Pin → der User sah "kein Recorder verfügbar"
            obwohl yt-dlp installiert war.
       F43: streamlink wurde komplett entfernt. Es funktionierte in der Praxis
            nicht mehr mit TikTok. Recorder-Kette ist jetzt: native → yt-dlp."""
    pref = (preferred or RECORDER_PREF).lower()
    # V37-403: hat dieser User zuletzt wiederholt 403 kassiert, für die Dauer des
    # Cooldowns auf yt-dlp erzwingen (signiert Requests selbst → umgeht CDN-403).
    # 'preferred' (expliziter Force-Versuch des Operators) hat Vorrang.
    if RECORD_403_YTDLP and not preferred:
        _until = _REC_403_UNTIL.get(username, 0)
        if _until > _time_mod.time():
            if pref not in ("ytdlp",):
                log.info("V37-403: @%s → yt-dlp erzwungen (403-Schutz aktiv, "
                         "noch %ds).", username, int(_until - _time_mod.time()))
            pref = "ytdlp"
        elif _until:
            _REC_403_UNTIL.pop(username, None)   # Cooldown abgelaufen → native retry
    has_ffmpeg = bool(shutil.which("ffmpeg"))
    ytdlp_bin = _find_external_recorder()
    url = f"https://www.tiktok.com/@{username}/live"

    # Pull-Proxy für DIESEN Versuch wählen: zuletzt geblockte Proxys dieses Users
    # ausschließen → Rotation (Anti-Buffering). Wird in _REC_PROXY[username] gemerkt,
    # damit handle_recording_finished den Proxy je nach Ausgang belohnt/rauswirft.
    with _REC_PROXY_LOCK:
        _excl = set(_REC_PROXY_FAILED.get(username) or ())
    _pull_proxy = await _pick_checked_pull_proxy(username=username, exclude=_excl)
    with _REC_PROXY_LOCK:
        _REC_PROXY[username] = _pull_proxy
    if _pull_proxy:
        log.info("@%s: Pull über Proxy%s", username,
                 (f" (rotiert, {len(_excl)} geblockt ausgeschlossen)" if _excl else ""))

    # F42: Diagnostik-Liste — jede _try_*-Funktion appendet bei Fehlschlag
    # einen menschenlesbaren Grund. Wird am Ende geloggt wenn nichts klappt.
    failure_reasons = []

    async def _try_native(mode="auto"):
        if not has_ffmpeg:
            failure_reasons.append("native: ffmpeg nicht installiert (apt install ffmpeg)")
            return None
        # F35: Wenn Detection schon eine URL geliefert hat — direkt nehmen.
        # F44 (Bug-Fix): Vorher haben wir NUR auf hls_url geprüft. Streams die
        # TikTok nur als FLV ausliefert (kommt bei manchen Rooms vor) sind
        # dadurch fälschlicherweise als "kein Recorder" markiert worden, obwohl
        # ffmpeg FLV genauso gut aufnimmt. Jetzt: hls_url BEVORZUGT, flv_url
        # als Fallback akzeptiert.
        def _has_stream_url(d):
            return bool(d and (d.get("hls_url") or d.get("flv_url")))
        info = prefetched_info if _has_stream_url(prefetched_info) else None
        # B58: prefetched URL aus der Detection könnte schon (fast) abgelaufen
        # sein. Vor Gebrauch das expire-Token prüfen — wenn < min TTL → verwerfen
        # und frisch auflösen. Das verhindert die "sofort-404"-Aufnahmen.
        if info is not None:
            purl = info.get("hls_url") or info.get("flv_url")
            if not _stream_url_is_fresh(purl):
                ttl = _stream_url_ttl(purl)
                log.info(f"@{username}: prefetched Stream-URL stale "
                         f"(ttl={ttl}s < {_STREAM_URL_MIN_TTL}s) → frisch auflösen")
                info = None
        if info is None:
            if session is None:
                failure_reasons.append(f"native: keine HTTP-Session vorhanden "
                                       f"(mode={mode}, build wurde ohne scraper-Session aufgerufen)")
                return None
            info = await resolve_tiktok_live_stream(username, session, mode=mode)
        if not _has_stream_url(info):
            failure_reasons.append(f"native: HLS/FLV-URL-Resolve fehlgeschlagen "
                                   f"(mode={mode} — meist Rate-Limit von TikTok "
                                   f"oder Stream ist gerade nicht erreichbar)")
            return None
        # F44: HLS bevorzugen (besser segmentiert, robuster bei Reconnects),
        # FLV als Fallback nehmen.
        stream_url = info.get("hls_url") or info.get("flv_url")
        stream_url = await _preflight_url(stream_url, who=f"@{username}")   # V37-B91
        if not stream_url:
            failure_reasons.append("native: Preflight — Stream-URL(s) "
                                   "antworten 404 (tot/Battle-Stage)")
            return None
        # B58: auch die frisch aufgelöste URL prüfen — wenn die schon kurz vor
        # Ablauf ist (Stream evtl. am Enden / TikTok-Token sehr kurz), loggen wir
        # das zur Diagnose. Aufnehmen tun wir trotzdem (besser als gar nicht).
        rttl = _stream_url_ttl(stream_url)
        if rttl is not None and rttl < _STREAM_URL_MIN_TTL:
            log.warning(f"@{username}: aufgelöste URL hat nur {rttl}s TTL "
                        f"(< {_STREAM_URL_MIN_TTL}s) — Aufnahme startet, aber "
                        f"URL-Refresh-Watchdog wird früh greifen")
        via = info.get("via", "?")
        suffix = {"webcast_api": "+api", "html_universal": "+html",
                  "html_sigi": "+html-sigi", "html_next": "+html-next",
                  "html_initial_state": "+html-init"}.get(via, "")
        # VERBESSERUNG: Resolver-Weg für Evolution-Lernfunktion loggen.
        # Evolution-Analyse liest diese Events um den besten Resolver-Pfad zu lernen.
        try:
            log_event("stream.resolve.ok", "info",
                      f"@{username}: resolve via {via}",
                      {"username": username, "via": via,
                       "has_hls": bool(info.get("hls_url")),
                       "has_flv": bool(info.get("flv_url"))})
        except Exception:
            pass
        # F44: Wenn nur FLV verfügbar war, Suffix erweitern damit Dashboard das sieht
        if not info.get("hls_url"):
            suffix += "-flv"
        return _build_native_cmd(stream_url, output_file, duration_secs, pull_proxy=_pull_proxy), f"native{suffix}"

    def _try_ytdlp():
        if not ytdlp_bin:
            failure_reasons.append("yt-dlp: Binary nicht im PATH gefunden "
                                   "(pip install -U yt-dlp ODER apt install yt-dlp)")
            return None
        return _build_ytdlp_cmd(ytdlp_bin, url, output_file, duration_secs, pull_proxy=_pull_proxy), "ytdlp"

    def _log_all_failures(pref_used):
        """F42: Ein zusammenfassender ERROR-Log mit allen Gründen.
           Macht klar OB es ein Installationsproblem ist oder ein Resolve-Problem."""
        if not failure_reasons:
            return    # paranoia — shouldn't happen
        # F43: streamlink raus der Liste der "verfügbaren" Recorder
        no_recorders_installed = (not has_ffmpeg) and (not ytdlp_bin)
        if no_recorders_installed:
            headline = "KEIN Recorder installiert — bitte ffmpeg ODER yt-dlp installieren"
        else:
            avail = []
            if has_ffmpeg:  avail.append("ffmpeg")
            if ytdlp_bin:   avail.append("yt-dlp")
            headline = (f"Recorder-Kandidaten ALLE gescheitert (verfügbar: {', '.join(avail)}, "
                        f"versucht: pref={pref_used})")
        log.error(f"@{username}: {headline}\n  " + "\n  ".join(failure_reasons))

    # F22 + F42 + F43: Wenn auf native_api gepinnt und das scheitert, fall through
    # auf yt-dlp — hat unabhängiges Resolve und kann trotz API-Rate-Limit
    # funktionieren. (streamlink-Fallback wurde in F43 entfernt.)
    if pref == "native_api":
        r = await _try_native(mode="api_only")
        if r: return r
        try:
            r = _try_ytdlp()
        except Exception as e:
            failure_reasons.append(f"_try_ytdlp: exception {e}")
            r = None
        if r:
            log.info(f"@{username}: native_api gescheitert, fallback auf {r[1]}")
            return r
        _log_all_failures("native_api")
        return None, None

    if pref == "native":
        r = await _try_native(mode="auto")
        if r: return r
        _log_all_failures("native")
        return None, None
    if pref == "ytdlp":
        r = _try_ytdlp()
        if r: return r
        _log_all_failures("ytdlp")
        return None, None

    # F43: auto-Kette = native → yt-dlp (kein streamlink mehr)
    for fn in (_try_native, _try_ytdlp):
        try:
            r = await fn() if asyncio.iscoroutinefunction(fn) else fn()
        except Exception as e:
            failure_reasons.append(f"{fn.__name__}: exception {e}")
            r = None
        if r:
            return r
    _log_all_failures("auto")
    return None, None
