"""nc.restreamcmd — die ffmpeg-Kommandozeile des Relays, aus bot.py heraus.

188 Zeilen, die nichts tun ausser eine Argumentliste zu bauen: Input-Haertung,
Filtergraph, Encoder-Profil, tee-Ausgaenge. Genau die Sorte Code, die sich
vollstaendig pruefen laesst, ohne dass ein einziges ffmpeg laeuft — geprueft
wird, WAS aufgerufen wird, nicht was das Werkzeug daraus macht. In dieser
Umgebung gibt es kein ffmpeg; im Monolithen war dieser Teil deshalb faktisch
ungetestet.

**Die Cookie-Zeile ist der Grund, warum das hier sauber getrennt gehoert.**
Der gebaute Befehl traegt in `-headers` einen vollstaendigen Cookie-Header der
TikTok-Session. Wer ihn ungefiltert loggt, schreibt die Session ins Klartext-
Log (F4). Der Redaktionspfad liegt in nc/logsafe.py und darf nicht umgangen
werden — auch nicht "nur zum Debuggen". Ein Vertrag haelt das fest.

Verhalten bitgenau wie im Monolithen. Der Rumpf ist ZEICHENGLEICH uebernommen;
die Werte, die vorher Modul-Globale von bot.py waren, sind hier Modul-Globale,
die configure() belegt. Ein Umschreiben auf _CFG["…"]-Zugriffe haette jede der
188 Zeilen zu einer moeglichen Regression gemacht, fuer einen Pfad, den hier
nichts ausfuehren kann.

Warum configure() unbekannte Schluessel ABLEHNT, anders als nc/restream_targets:
ein Tippfehler bliebe sonst still, und der Bauer liefe mit dem Default weiter —
also mit einer anderen Bitrate, einem anderen Preset oder ohne Overlay, ohne
dass irgendetwas rot wird. Genau diese Klasse Fehler hat die Restream-Vertraege
schon dreimal gekippt.
"""

import logging
import os

from nc import audio_cue as _nc_audio
from nc import audiocue as _nc_audiocue
from nc import ffbuild as _nc_ffbuild
from nc import ffmpeg_filters as _nc_ff
from nc import restream_targets as _nc_rst
from nc import restream_util as _nc_rutil
from nc import restreamstate as _nc_rsstate

log = logging.getLogger("TikTokBot")

# Aliase auf nc-Register: bot-frei, und der Bot bindet sie nie neu. Ein
# Kontextfeld waere hier nur eine zweite Signatur, an der etwas driften kann.
_audio_cfg = _nc_audiocue.config
_restream_layout_mode = _nc_rsstate.layout_mode


def _ff_cmd(cmd, threads=None, nice=None):
    return _nc_ffbuild.ff_cmd(cmd, threads=threads, nice=nice)


def _normalize_ingest(ingest_url: str) -> str:
    return _nc_rutil.normalize_ingest(ingest_url)


# ══════════════════════════════════════════════════════════════════════════
# Vom Bot belegt — siehe configure(). Vor dem Aufruf ist alles None bzw. 0;
# das ist Absicht: der Bauer soll krachen, nicht still mit Defaults senden.
# ══════════════════════════════════════════════════════════════════════════
_cookie_header = None            # liefert den Cookie-Header der TikTok-Session
_pick_pull_proxy = None          # RECORD_PROXY -> PROXY_LIST -> TikTok-Pool
_restream_overlay_files = None   # Overlay-Textdateien je Restream-ID

FFMPEG_THREADS_LIVE = None
FFMPEG_THREADS_RELAY = None
RESTREAM_AVATAR = None
RESTREAM_AVATAR_ALPHA = None
RESTREAM_AVATAR_H = None
RESTREAM_AVATAR_LOOP = None
RESTREAM_BITRATE_K = None
RESTREAM_CANVAS_H = None
RESTREAM_CANVAS_W = None
RESTREAM_FONT = None
RESTREAM_FPS = None
RESTREAM_LOW_LATENCY = None
RESTREAM_OVERLAY = None
RESTREAM_OVERLAY_HTML_FPS = None
RESTREAM_RELAY_BITRATE_K = None
RESTREAM_RELAY_PRESET = None
RESTREAM_X264_PRESET = None
_RESTREAM_UA = None
_TTS_CH = None
_TTS_SR = None
_TTS_VOICE_GAIN = None

_PFLICHT = (
    "cookie_header", "pick_pull_proxy", "restream_overlay_files",
    "FFMPEG_THREADS_LIVE", "FFMPEG_THREADS_RELAY", "RESTREAM_AVATAR",
    "RESTREAM_AVATAR_ALPHA", "RESTREAM_AVATAR_H", "RESTREAM_AVATAR_LOOP",
    "RESTREAM_BITRATE_K", "RESTREAM_CANVAS_H", "RESTREAM_CANVAS_W",
    "RESTREAM_FONT", "RESTREAM_FPS", "RESTREAM_LOW_LATENCY",
    "RESTREAM_OVERLAY", "RESTREAM_OVERLAY_HTML_FPS",
    "RESTREAM_RELAY_BITRATE_K", "RESTREAM_RELAY_PRESET",
    "RESTREAM_X264_PRESET", "RESTREAM_UA", "TTS_CH", "TTS_SR",
    "TTS_VOICE_GAIN",
)


def configure(**kw):
    """Der Bot reicht seine Werte einmal beim Start herein.

    Unbekannte UND fehlende Schluessel sind ein Fehler, kein Achselzucken:
    ein stiller Default hier bedeutet eine andere Bitrate oder ein fehlendes
    Overlay im Sendebild — sichtbar erst auf dem Stream, nicht im Log.
    """
    unbekannt = sorted(set(kw) - set(_PFLICHT))
    fehlt = sorted(set(_PFLICHT) - set(kw))
    if unbekannt or fehlt:
        raise ValueError(
            "restreamcmd.configure: unbekannt=%s fehlt=%s" % (unbekannt, fehlt))
    g = globals()
    for k, v in kw.items():
        # Die drei Aufrufbaren und _RESTREAM_UA/_TTS_* tragen im Bauer einen
        # Unterstrich vorweg; der Aufrufer soll ihn nicht mitschreiben muessen.
        g[k if k in g else "_" + k] = v


# v4.2-W48: Wo eine Schrift liegen kann, wenn die konfigurierte fehlt.
# Reihenfolge = Vorliebe: erst fette DejaVu (das ist, was RESTREAM_FONT
# ueblicherweise meint), dann die ueblichen Ersatzfamilien der Distributionen.
FONT_KANDIDATEN = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
)


def schriftart(vorgabe, kandidaten=None, pruefer=None):
    """Die erste Schrift, die wirklich auf der Platte liegt — oder None.

    Am 11.09. stand im Log zweimal "RESTREAM_OVERLAY=1, aber Font fehlt
    (/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf) — Overlay
    uebersprungen". Der Betreiber hatte das Overlay eingeschaltet und bekam
    es nicht, weil ein Paket fehlte (fonts-dejavu-core), das auf einer
    Server-Installation ueblicherweise gar nicht dabei ist. Eine Schrift
    ist aber austauschbar: fuer eine Bauchbinde zaehlt, DASS Text erscheint.

    Die konfigurierte Vorgabe hat Vorrang — wer sie setzt, will sie. Erst
    wenn sie fehlt, wird gesucht. `pruefer` ist nur fuer den Test da; ohne
    ihn entscheidet das Dateisystem.
    """
    pruef = pruefer or os.path.isfile
    if vorgabe and pruef(vorgabe):
        return vorgabe
    for pfad in (kandidaten if kandidaten is not None else FONT_KANDIDATEN):
        if pfad != vorgabe and pruef(pfad):
            return pfad
    return None


def _drawtext_chain(rid=None):
    # v4.0-W27: verbatim nach nc/ffmpeg_filters.py extrahiert (bitgenau geprüft).
    return _nc_ff.drawtext_chain(_restream_overlay_files(rid),
                                 schriftart(RESTREAM_FONT))


def _studio_chain(avatar_idx=None, rid=None, avatar_alpha_idx=None, drossel=0):
    # v4.0-W27: verbatim nach nc/ffmpeg_filters.py extrahiert (bitgenau geprüft).
    # v4.2-W60: die Leinwand kommt gedrosselt herein. Sie muss dieselbe sein,
    # die der Encoder bekommt — sonst skaliert ffmpeg das fertige Sendebild
    # noch einmal, und der Chat wird unscharf statt kleiner.
    _cw, _ch = drossel_canvas(RESTREAM_CANVAS_W, RESTREAM_CANVAS_H, drossel)
    return _nc_ff.studio_chain(_restream_overlay_files(rid),
                               schriftart(RESTREAM_FONT),
                               _cw, _ch, drossel_fps(RESTREAM_FPS, drossel),
                               avatar_idx=avatar_idx,
                               avatar_alpha_idx=avatar_alpha_idx,
                               avatar_h=RESTREAM_AVATAR_H)


# v4.2-W43: Drossel-Stufen gegen den Encode-Rueckstand.
#
# WARUM ueberhaupt: drei Ziele erzwingen den Transcode (_multi_forces_tc in
# bot.py), der Transcode laeuft mit FFMPEG_THREADS_LIVE Kernen, und faellt er
# unter Echtzeit, laufen die RTMP-Puffer leer. Dann meldet tee "Slave muxer
# failed: Broken pipe" und reisst ALLE Ziele mit, weil sie in einem Prozess
# haengen. Bis W43 hat der Bot das erkannt, einmal gewarnt und zugesehen.
#
# Die Reihenfolge ist nach Sichtbarkeit fuer den Zuschauer sortiert: ein
# schnelleres Preset kostet Bildqualitaet, die kaum jemand bemerkt; die
# Bitrate merkt man; den fehlenden Avatar sieht jeder. Deshalb faellt er
# zuletzt.
# v4.2-W49: die x264-Presets in ihrer ECHTEN Reihenfolge, schnell -> langsam.
#
# Bis hierher stand hier ("veryfast", "faster", "superfast", "ultrafast") und
# wurde vorwaerts durchlaufen. In x264 ist "faster" aber LANGSAMER als
# "veryfast" — die Notbremse trat also auf Stufe 1 aufs Gas. Im Log des
# Betreibers vom 11.09. steht genau das:
#
#     Drossel Stufe 1 von 3 (Preset faster, Bitrate 6000k)
#
# Danach wuchs der Rueckstand weiter, Stufe 2 und 3 folgten — und auf Stufe 3
# faellt der Overlay. Der Weg zum schwarzen Sendebild fuehrte durch den
# Versuch, ihn zu verhindern.
_X264_TEMPO = ("ultrafast", "superfast", "veryfast", "faster", "fast",
               "medium", "slow", "slower", "veryslow")


def drossel_preset(preset, stufe):
    """Preset um `stufe` Schritte in Richtung SCHNELLER ruecken.

    Schneller heisst in dieser Liste: kleinerer Index. Es sind genau `stufe`
    Schritte, nicht "bis ans Ende" — wer `medium` konfiguriert hat, landet auf
    der hoechsten Drossel bei `veryfast`, nicht bei `ultrafast`. Das ist
    Absicht: die Drossel ist eine Notbremse gegen einen Rueckstand, kein
    Urteil ueber die Einstellung des Betreibers.
    """
    if stufe <= 0:
        return preset
    try:
        i = _X264_TEMPO.index((preset or "").strip().lower())
    except ValueError:
        # Unbekanntes Preset: bei veryfast einsteigen. Nicht bei ultrafast —
        # sonst springt ein Tippfehler in der .env sofort auf die schlechteste
        # Qualitaetsstufe, ohne dass je ein Rueckstand vorlag.
        i = _X264_TEMPO.index("veryfast")
    return _X264_TEMPO[max(0, i - stufe)]


def drossel_bitrate(bitrate_k, stufe):
    """Ab Stufe 2 die Bitrate senken, aber nie unter 1500k."""
    if stufe < 2:
        return bitrate_k
    return max(1500, int(bitrate_k * (0.75 if stufe == 2 else 0.55)))


# v4.2-W60 — DIE DROSSEL FASST DEN BILDINHALT NICHT MEHR AN.
#
# Bis hierher gab es `drossel_text_aus(stufe)`: ab Stufe 3 fiel `overlay_on`,
# und weil `studio_on = overlay_on and layout == "studio"` daran haengt, fiel
# damit das GANZE Panel — Chat, Titel, Quelle, Follower, AZRAEL-Zeile. Uebrig
# blieben Quellvideo und Avatar. Der Betreiber hat das zweimal als „der Chat
# bricht weg" gemeldet, beim zweiten Mal mit der Ansage: es hat gar nichts
# auszufallen, es soll nicht einmal die Moeglichkeit dazu geben.
#
# Die alte Begruendung war ausserdem gemessen falsch. 12 s Quelle, 1280x720,
# superfast, vier Threads:
#
#     nackt, ohne alles              1.1 s
#     + Leinwand und Deko            1.9 s   (Leinwand  0.8 s)
#     + alle neun Textfelder         2.9 s   (Text      1.0 s)
#     + Avatar                       4.1 s   (Avatar    1.2 s)
#
# Der Avatar allein kostet mehr als saemtliche Texte zusammen. Stufe 3 warf
# also das Panel weg und behielt das Teuerste.
#
# Die Leiter regelt jetzt ausschliesslich, WIE kodiert wird — nie, WAS im Bild
# steht. Ein Drossel-Schritt baut das Kommando ohnehin neu (stop + start),
# Bildrate und Leinwandgroesse sind damit genauso regelbar wie Preset und
# Bitrate:
#
#     Stufe 1   Preset einen Schritt schneller
#     Stufe 2   + Bitrate runter
#     Stufe 3   + Bildrate runter
#     Stufe 4   + Leinwand kleiner
#
# Eine kleinere Leinwand kostet quadratisch weniger und laesst jedes Element
# sichtbar. Das ist der Unterschied zwischen „kleiner" und „weg".


def drossel_fps(fps, stufe):
    """Ab Stufe 3 die Bildrate senken, aber nie unter 15.

    Linear in der Encode-Last und fuer den Zuschauer die unauffaelligste
    Stufe: 24 auf 18 sieht man bei einem Talking-Head-Stream kaum, ein
    fehlendes Chat-Panel dagegen sofort.
    """
    if stufe < 3:
        return fps
    return max(15, int(round(fps * 0.75)))


def drossel_canvas(w, h, stufe):
    """Ab Stufe 4 die Leinwand verkleinern, aber nie unter 960x540.

    Der letzte Hebel vor dem Anschlag. Quadratisch in der Last — 1280x720 auf
    960x540 sind 44 % weniger Pixel — und jedes Element bleibt im Bild, nur
    kleiner. Die Untergrenze ist bewusst 960x540 und nicht weniger: darunter
    ist der eingebrannte Chat nicht mehr lesbar, und ein unlesbares Panel
    waere dasselbe wie ein fehlendes.
    """
    if stufe < 4:
        return w, h
    return max(960, int(w * 0.75)) & ~1, max(540, int(h * 0.75)) & ~1


def drossel_zusatz(fps, w, h, stufe):
    """Was diese Stufe ZUSAETZLICH zu Preset und Bitrate tut. Fuer das Log.

    v4.2-W60. Vorher stand hier ", Text aus" — die Drossel kann seit dieser
    Welle nichts mehr aus dem Bild nehmen, also nennt die Zeile jetzt, was
    sie stattdessen regelt.
    """
    teile = []
    if drossel_fps(fps, stufe) != fps:
        teile.append("%d fps" % drossel_fps(fps, stufe))
    if drossel_canvas(w, h, stufe) != (w, h):
        teile.append("%dx%d" % drossel_canvas(w, h, stufe))
    return (", " + ", ".join(teile)) if teile else ""


DROSSEL_MAX = 4


def build(source_url, ingest_url, stream_key, transcode=False, tts_fifo=None, rid=None, only_target=None, relay_profile=False, html_ov_fifo=None, targets=None, avatar_feed=None, drossel=0):
    """ffmpeg-Relay: zieht die TikTok-Quelle und pusht per RTMP(S)/FLV an Kick/AWS-IVS.
       Input-Flags spiegeln den BEWÄHRTEN Aufnahme-Pfad (_build_native_cmd): FLV =
       eine saubere Dauerverbindung (bevorzugt); HLS braucht +genpts+igndts, weil
       TikTok HLS-Pakete OHNE PTS / mit non-monotonic DTS liefert — sonst bricht
       der FLV-Muxer mit 'Error submitting a packet to the muxer: End of file'
       ab (rc=187). copy = kein Re-Encoding; transcode = IVS-konformes H.264/AAC
       (CFR, 2s-Keyframes) + optionales gebranntes Overlay.
       -progress pipe:1 → maschinenlesbare Health-Daten auf stdout."""
    # V37-INDEP: only_target erzwingt EIN konkretes Ausgabeziel (unabhängiger
    # Modus, ein Prozess pro Plattform). Sonst Standard: Kick-Ingest + tee.
    target = only_target or (_normalize_ingest(ingest_url) + "/" + stream_key)
    cookie_hdr = _cookie_header()
    headers_list = []
    if cookie_hdr:
        headers_list.append(f"Cookie: {cookie_hdr}")
    headers_list.append("Referer: https://www.tiktok.com/")
    headers_blob = "\r\n".join(headers_list) + "\r\n"

    url_lc = source_url.lower()
    is_hls = ".m3u8" in url_lc                      # FLV/sonstiges → else-Zweig

    # v4.2-W60: ab Stufe 3 senkt die Drossel die Bildrate, ab Stufe 4 die
    # Leinwand. Beides kostet Last, ohne dass etwas aus dem Bild faellt.
    fps = max(15, min(60, drossel_fps(RESTREAM_FPS, drossel)))
    gop = fps * 2                                   # IVS/Kick: Keyframe-Intervall ≤ 2s
    # --- Input-Härtung: identisch zum stabilen Recorder (F45/B56/B60) ---
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-nostats",
           "-progress", "pipe:1",
           "-reconnect", "1", "-reconnect_streamed", "1",
           "-reconnect_delay_max", "30",                 # 30s reconnect-window (wie Recorder)
           # B124-Analog (bisher fehlte der Fix HIER): NICHT "4xx,5xx". Das schloss
           # 404 und 403 ein — beide sind bei TikTok TERMINAL, nicht vorübergehend
           # (404 = CDN-Pull-URL mit expire=<ts> abgelaufen/Edge-Wechsel; 403 =
           # blockiert). Auf "4xx,5xx" hämmerte der Restream-ffmpeg die tote
           # Quell-URL 30s lang, bevor der ganze tee kollabierte ("All tee outputs
           # failed") und der Prozess starb → TikTok-Input weg → Neuaufbau alle
           # paar Minuten. Jetzt nur die WIRKLICH vorübergehenden Codes; bei 404/403
           # gibt ffmpeg sofort auf, der Manager löst eine FRISCHE Quell-URL auf.
           "-reconnect_on_http_error", "408,429,500,502,503,504",
           "-reconnect_on_network_error", "1",
           "-rw_timeout", "30000000",                    # 30s I/O-timeout (gilt für HTTP Connect+Read, versionsübergreifend)
           "-analyzeduration", "10000000", "-probesize", "15000000"]
    if is_hls:
        # B60-Analog: HLS ohne PTS + non-monotonic DTS → +genpts erzeugt PTS,
        # +igndts ignoriert kaputte DTS, +flush_packets schreibt sofort raus.
        # -timeout komplett entfernt: älteres ffmpeg kennt die Option für HTTP/HLS
        # nicht ("Option timeout not found"). rw_timeout (oben) deckt Connect+Read ab.
        cmd += ["-multiple_requests", "1", "-fflags", "+genpts+igndts+flush_packets"]
    else:
        cmd += ["-fflags", "+flush_packets"]             # FLV: sofort flushen, kein Buffern
    cmd += ["-user_agent", _RESTREAM_UA, "-headers", headers_blob]
    _rp = _pick_pull_proxy()                             # RECORD_PROXY → PROXY_LIST → TikTok-Pool
    if _rp:
        cmd += ["-http_proxy", _rp]
    cmd += ["-i", source_url]
    # Optionale Zusatz-Inputs — Reihenfolge bestimmt den Index! 1) AZRAEL-Stimme (FIFO),
    # 2) Avatar-PNG. Beides nur im Transcode-Modus (Overlay/amix brauchen Re-Encoding).
    use_tts = bool(tts_fifo)            # Stimme auch im Copy-Modus mischen (Audio wird eh re-enkodiert)
    # v4.2-W48: nicht mehr nur die konfigurierte Schrift, sondern die erste,
    # die es gibt. Vorher entschied os.path.isfile(RESTREAM_FONT) allein —
    # und ein fehlendes Schrift-Paket kostete das komplette Overlay.
    _font = schriftart(RESTREAM_FONT)
    # v4.2-W49: ZWEI Schalter statt einem.
    #
    # `sendebild_on` sagt, ob ueberhaupt etwas ins Bild gebrannt wird.
    # `overlay_on` sagt zusaetzlich, ob TEXT gebrannt wird — dafuer braucht es
    # eine Schrift. Der Avatar braucht keine.
    #
    # Vorher war das eins: eine fehlende Schriftdatei nahm den Avatar mit, und
    # die Drossel auf Stufe 3 ebenso. Gemeldet als "im Text-Modus brechen Chat
    # UND Avatar weg" — zwei Ursachen, ein Symptom.
    # v4.2-W50: die Drossel gehoert an `overlay_on`, NICHT an `sendebild_on`.
    #
    # W49 hat sie hier oben gelassen und damit nur die halbe Entkopplung
    # geliefert: der Avatar war frei von der SCHRIFT, hing aber weiter an der
    # Drossel, weil er ueber sendebild_on ableitet. Changelog und PR
    # behaupteten beides. Im Betrieb erreichte die Drossel Stufe 3 und der
    # Avatar verschwand erneut — genau das gemeldete Bild.
    sendebild_on = bool(transcode and RESTREAM_OVERLAY)
    overlay_on = bool(sendebild_on and _font)
    if transcode and RESTREAM_OVERLAY and _font and _font != RESTREAM_FONT:
        log.warning("RESTREAM_FONT (%s) fehlt — Overlay laeuft mit Ersatzschrift %s.",
                    RESTREAM_FONT, _font)
    # v4.2-W32: bewegter Avatar, wenn Schleife UND Alphamaske dastehen —
    # sonst wie bisher das Standbild. Beides fehlt: kein Avatar.
    # Ab hier haengt der Avatar an `sendebild_on`, nicht mehr an `overlay_on`:
    # ohne Schrift kein Text, aber sehr wohl ein Avatar.
    anim_on = bool(sendebild_on and RESTREAM_AVATAR_LOOP and RESTREAM_AVATAR_ALPHA
                   and os.path.isfile(RESTREAM_AVATAR_LOOP)
                   and os.path.isfile(RESTREAM_AVATAR_ALPHA))
    # v4.2-W34: laeuft ein Feeder, hat er Vorrang — nur er kann auf eine
    # AZRAEL-Reaktion umschalten. Ohne ihn die feste Schleife (W32), ohne die
    # das Standbild (W31).
    feed_on = bool(sendebild_on and avatar_feed)
    avatar_on = bool(feed_on or anim_on or (sendebild_on and RESTREAM_AVATAR
                                            and os.path.isfile(RESTREAM_AVATAR)))
    # v4.2-W50: EINE Zeile, die sagt, warum das Sendebild so aussieht, wie es
    # aussieht.
    #
    # Bis hierher waren `overlay_on` und `avatar_on` stille Boolesche aus fuenf
    # Bedingungen (transcode, Schalter, Drossel, Schrift, Avatar-Datei). Fiel
    # eine davon um, stand NICHTS im Log — der Betreiber sah ein leeres
    # Sendebild und musste raten. Genau das hat in W47 bis W49 drei Runden
    # gekostet, und es ist dieselbe Luecke wie beim Audio-Tap vor W46: eine
    # Bedingung, die stumm False wird, ist so schlimm wie ein except, das den
    # Grund frisst (CLAUDE.md).
    #
    # Auf `warning` nur, wenn etwas FEHLT, das der Betreiber eingeschaltet hat
    # — sonst auf `info`. Eine Warnung, die bei jedem gesunden Start kommt,
    # erzieht dazu, sie zu ueberlesen.
    if transcode and RESTREAM_OVERLAY:
        _gruende = []
        # v4.2-W60: die Drossel steht hier NICHT mehr als Grund. Sie kann
        # seit dieser Welle nichts mehr aus dem Bild nehmen — was sie regelt
        # (Preset, Bitrate, Bildrate, Leinwand) steht in der Drossel-Meldung
        # des Waechters, nicht in der Sendebild-Zeile.
        if not _font:
            _gruende.append("keine Schrift gefunden (weder %s noch eine der %d "
                            "Ersatzschriften; apt install fonts-dejavu-core)"
                            % (RESTREAM_FONT, len(FONT_KANDIDATEN)))
        if not avatar_on:
            _gruende.append("kein Avatar (RESTREAM_AVATAR=%r liegt nicht im "
                            "Arbeitsverzeichnis des Dienstes)" % (RESTREAM_AVATAR,))
        if _gruende:
            log.warning("Sendebild #%s: Text=%s Avatar=%s — %s",
                        rid, "an" if overlay_on else "AUS",
                        "an" if avatar_on else "AUS", "; ".join(_gruende))
        else:
            log.info("Sendebild #%s: Text an, Avatar an (Schrift %s)", rid, _font)
    elif RESTREAM_OVERLAY and not transcode:
        log.warning("Sendebild #%s: RESTREAM_OVERLAY=1, aber copy-Modus — im "
                    "Copy-Modus gibt es keine Filter und damit kein Overlay.", rid)

    _idx = 1
    tts_idx = avatar_idx = avatar_alpha_idx = None
    if use_tts:
        cmd += ["-thread_queue_size", "1024", "-f", "s16le",
                "-ar", str(_TTS_SR), "-ac", str(_TTS_CH), "-i", tts_fifo]
        tts_idx = _idx; _idx += 1
    if feed_on:
        # Roher RGBA-Strom aus der FIFO: die Transparenz steckt schon drin
        # (der Feeder hat sie beim Dekodieren untergemischt), also bleibt
        # avatar_alpha_idx None und die Kette braucht kein alphamerge.
        # thread_queue grosszuegig — der Writer taktet fest, ffmpeg hungert nie.
        _ffifo, _fw, _fh, _ffps = avatar_feed
        cmd += ["-thread_queue_size", "512", "-f", "rawvideo", "-pix_fmt", "rgba",
                "-s", f"{_fw}x{_fh}", "-framerate", str(_ffps), "-i", _ffifo]
        avatar_idx = _idx; _idx += 1
    elif anim_on:
        # -stream_loop -1: die Schleife laeuft endlos weiter, das Sendebild
        # bestimmt die Laenge. -loop 1 auf der Maske aus demselben Grund.
        cmd += ["-stream_loop", "-1", "-i", RESTREAM_AVATAR_LOOP]
        avatar_idx = _idx; _idx += 1
        cmd += ["-loop", "1", "-i", RESTREAM_AVATAR_ALPHA]
        avatar_alpha_idx = _idx; _idx += 1
    elif avatar_on:
        cmd += ["-i", RESTREAM_AVATAR]
        avatar_idx = _idx; _idx += 1
    htmlov_idx = None
    if html_ov_fifo and transcode:
        # V37-HTMLOV: PNG-Frames aus der Feeder-FIFO. thread_queue großzügig,
        # der Writer taktet fest — ffmpeg hungert nie.
        cmd += ["-thread_queue_size", "512", "-f", "image2pipe",
                "-framerate", str(RESTREAM_OVERLAY_HTML_FPS), "-i", html_ov_fifo]
        htmlov_idx = _idx; _idx += 1
    if transcode:
        br = f"{RESTREAM_BITRATE_K}k"
        studio_on = bool(overlay_on and _restream_layout_mode() == "studio")
        if htmlov_idx is not None:
            # HTML-Overlay. Normalfall: das PNG wird bereits in der echten
            # Quellauflösung gerendert (_overlay_render_size) → scale2ref ist
            # ein No-Op und das Overlay sitzt pixelgenau.
            # Sicherheitsnetz: weicht die Größe doch ab (feste Größe erzwungen
            # oder Probe fehlgeschlagen), skaliert force_original_aspect_ratio
            # =decrease SEITENVERHÄLTNIS-TREU und zentriert. Vorher zerrte ein
            # nacktes w=iw:h=ih ein 9:16-Overlay auf eine 16:9-Quelle breit.
            # eof_action=repeat hält das letzte Bild, shortest=0 → das Overlay
            # beendet den Stream nie.
            fc = [f"[{htmlov_idx}:v][0:v]scale2ref=w=iw:h=ih:"
                  f"force_original_aspect_ratio=decrease[ovs][base]",
                  "[base][ovs]overlay=(W-w)/2:(H-h)/2:eof_action=repeat:shortest=0[vh]"]
            vlabel = "vh"
            if avatar_on:
                _t, _l = _nc_ff.avatar_kette(avatar_idx, avatar_alpha_idx,
                                             RESTREAM_AVATAR_H, "av")
                fc.extend(_t)
                # v4.2-W30: bottom-right statt vertikal mittig, mit sanftem
                # Schweben (Amplitude 8px, Periode 6s) — dieselbe Bewegung wie
                # die azFloat-Animation des HTML-Avatars in overlay.html, nur
                # hier als ffmpeg-Ausdruck (eval=frame ist overlay()s Default,
                # t laeuft also live mit statt einmalig beim Filter-Init).
                fc.append(f"[{vlabel}][av]overlay=W-w-W*0.06:H-h-40-8*sin(2*PI*t/6):eof_action=repeat:shortest=0[v]"); vlabel = "v"
            if use_tts:
                fc.extend(_nc_audio.mix_chain(tts_idx, _TTS_VOICE_GAIN, _audio_cfg()["duck"]))
            cmd += ["-filter_complex", ";".join(fc)]
            cmd += ["-map", f"[{vlabel}]"]
            cmd += ["-map", "[a]" if use_tts else "0:a"]
        elif use_tts or avatar_on or studio_on:
            # filter_complex: Studio-Leinwand ODER drawtext-Kette → optional
            # Avatar-Overlay → amix Quelle+Stimme.
            fc = []
            vlabel = "0:v"
            if studio_on:
                sparts, vlabel = _studio_chain(avatar_idx if avatar_on else None, rid=rid,
                                               drossel=drossel,
                                               avatar_alpha_idx=avatar_alpha_idx)
                fc.extend(sparts)
            else:
                if overlay_on:
                    fc.append(f"[0:v]{_drawtext_chain(rid)}[vt]"); vlabel = "vt"
                if avatar_on:
                    _t, _l = _nc_ff.avatar_kette(avatar_idx, avatar_alpha_idx,
                                                 RESTREAM_AVATAR_H, "av")
                    fc.extend(_t)
                    # v4.2-W30: bottom-right + Schweben, siehe Kommentar oben am
                    # htmlov-Zweig — derselbe Ausdruck, hier fuer Text-/Studio-Modus.
                    fc.append(f"[{vlabel}][av]overlay=W-w-W*0.06:H-h-40-8*sin(2*PI*t/6):eof_action=repeat:shortest=0[v]"); vlabel = "v"
            if use_tts:
                # normalize=0 → Quell-Ton bleibt VOLL (amix halbiert sonst beide Inputs);
                # Stimme angehoben damit klar hörbar, alimiter fängt Clipping ab.
                fc.extend(_nc_audio.mix_chain(tts_idx, _TTS_VOICE_GAIN, _audio_cfg()["duck"]))
            cmd += ["-filter_complex", ";".join(fc)]
            cmd += ["-map", (f"[{vlabel}]" if vlabel != "0:v" else "0:v")]
            cmd += ["-map", "[a]" if use_tts else "0:a"]
        elif overlay_on:
            cmd += ["-vf", _drawtext_chain(rid)]
        _preset = RESTREAM_RELAY_PRESET if relay_profile else RESTREAM_X264_PRESET
        _preset = drossel_preset(_preset, drossel)
        if relay_profile:
            br = f"{RESTREAM_RELAY_BITRATE_K}k"
        # B137: VBV-Puffer bestimmt maßgeblich die Encoder-Latenz. 2×Bitrate ≈ 2s
        # Puffer (robust, aber träge); im Low-Latency-Modus 1×Bitrate ≈ 1s.
        _bufmult = 1 if RESTREAM_LOW_LATENCY else 2
        _brk = drossel_bitrate(
            RESTREAM_RELAY_BITRATE_K if relay_profile else RESTREAM_BITRATE_K,
            drossel)
        if drossel >= 2:
            br = f"{_brk}k"          # -b:v/-maxrate ziehen mit
        _bufk = _brk * _bufmult
        cmd += ["-c:v", "libx264", "-preset", _preset, "-profile:v", "main",
                "-level", "4.1", "-pix_fmt", "yuv420p"]
        if RESTREAM_LOW_LATENCY:
            # -tune zerolatency: x264 ohne B-Frames, ohne rc-/sync-lookahead →
            # der Encoder gibt Frames sofort raus statt sie für bessere Kompression
            # zurückzuhalten. DAS ist der große Latenz-Hebel. Fixe Keyframes (unten,
            # -g/-keyint_min/-sc_threshold 0) bleiben plattformkonform.
            cmd += ["-tune", "zerolatency", "-bf", "0"]
        cmd += ["-b:v", br, "-maxrate", br, "-bufsize", f"{_bufk}k",
                "-r", str(fps), "-fps_mode", "cfr",
                "-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0",
                # V37-STAB: großer Muxing-Queue gegen "Too many packets buffered"
                # bei kurzem Encode-Rückstand → kein harter Abbruch.
                "-max_muxing_queue_size", "1024",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2"]
    else:
        # copy-Modus: Video bleibt Copy. Audio → AAC (FLV/RTMP mag kein HE-AAC/Opus).
        cmd += ["-c:v", "copy"]
        if use_tts:
            # Stimme reinmischen — dadurch wird NUR der Ton re-enkodiert, Video bleibt copy.
            cmd += ["-filter_complex",
                    ";".join(_nc_audio.mix_chain(tts_idx, _TTS_VOICE_GAIN, _audio_cfg()["duck"]))]
            cmd += ["-map", "0:v", "-map", "[a]"]
        cmd += ["-c:a", "aac", "-b:a", "160k", "-ar", "44100"]
        if is_hls and not use_tts:
            cmd += ["-bsf:a", "aac_adtstoasc"]           # nur bei reinem Copy-Audio nötig (kein Re-Mix)
    # no_duration_filesize: unterdrückt 'Failed to update header with correct duration'.
    # F103: MULTISTREAM — sind Zusatzplattformen aktiv (YT/Twitch), über den
    # tee-Muxer parallel an alle Ziele fan-outen. Aktuell KEINE aktiv (YT/Twitch
    # per Default deaktiviert) → identisches Single-Target-Verhalten wie bisher.
    if RESTREAM_LOW_LATENCY:
        # B137: Muxer-Vorlauf auf 0 → keine anfängliche Mux-Pufferung. Gilt für
        # tee, Single- und Copy-Pfad.
        cmd += ["-muxdelay", "0", "-muxpreload", "0"]
    if only_target:
        # Unabhängiger Modus: genau EIN Ziel, eigener Prozess, kein tee.
        cmd += _nc_rst.single_output_args(target)
    else:
        # v4.0-W77: GLEICHSTELLUNG — alle konfigurierten Plattformen als flache,
        # gleichberechtigte Zielliste (kein Primär mehr). `targets` reicht der
        # Aufrufer (inkl. Pro-Restream-Overrides) durch; fehlt es, wird es aus
        # der Kick-Basis + globalen Env-Zielen abgeleitet (Kick-only = identisch
        # zum bisherigen Single-Pfad).
        _tgts = targets if targets is not None else _nc_rst.active_targets(
            overrides={"kick": (ingest_url, stream_key)})
        if not _tgts:
            _tgts = [("kick", target)]      # Notausgang: nie ohne Ziel senden
        cmd += _nc_rst.build_output_args(_tgts)
        if len(_tgts) > 1:
            log.info("Restream MULTISTREAM (tee) aktiv — gleichberechtigt: %s "
                     "(alle onfail=ignore)", ", ".join(n for n, _ in _tgts))
    # V37-CPU: Thread-Deckel. Ohne -threads greift sich x264 ~1.5x alle Kerne —
    # bei parallelem Transcode+Relay+Nachbearbeitung war das die Ursache fuer
    # Load 113 auf 8 Kernen. Kein nice: das Sendebild hat Vorrang.
    return _ff_cmd(cmd, threads=(FFMPEG_THREADS_RELAY if relay_profile
                                 else FFMPEG_THREADS_LIVE))
