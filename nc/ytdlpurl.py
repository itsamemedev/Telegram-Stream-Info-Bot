"""nc.ytdlpurl — die Stream-URL aus der yt-dlp-Auskunft lesen (v4.2-W102).

**Der Befund, gegen den dieses Modul existiert.** `_resolve_via_ytdlp` in
`bot.py` ruft yt-dlp mit `--dump-single-json` auf und las das Ergebnis so:

    if data.get("is_live") or data.get("formats") or data.get("manifest_url") \\
       or data.get("url"):
        return "live", None

Die drei Schluessel, die eine Adresse TRAGEN, wurden als Ja/Nein-Frage
gelesen und die Adresse danach weggeworfen. Im Docstring stand als
Begruendung, der Recorder loese ohnehin selbst auf — das stimmt fuer den
Recorder (er startet yt-dlp noch einmal) und ist fuer den **Restream**
falsch: der braucht eine URL und hat keinen yt-dlp-Rang.

Schlimmer war der Satz, der daraus wurde. In `bot.py` und in
`nc/livefolge.braucht_url_nachschlag` stand als Tatsache:

    yt-dlp hilft hier NICHT: _resolve_via_ytdlp gibt auch bei 'live'
    grundsaetzlich info=None zurueck. Nur der HTML-Weg traegt eine URL.

Das ist eine Aussage ueber **unsere Huelle**, nicht ueber yt-dlp — und sie
war selbsterfuellend: yt-dlp trug keine URL, weil wir sie verwarfen. Genau
die Klasse, vor der CLAUDE.md warnt: ein Kommentar ueber die Eingabe ist
kein Beweis ueber die Eingabe.

Warum das ausgerechnet dieser Weg ist: yt-dlp erzeugt TikToks
Anti-Bot-Signaturen selbst und kommt damit durch, wo der eigene
HTTP-Resolver 403 bekommt (so steht es im Docstring derselben Funktion).
Gemessen am 11.09. melden **71 % der Aufloesungen „live" ohne URL** —
TikTok gibt sie einer Datacenter-IP nicht heraus. In genau diesem Fall ist
yt-dlp der einzige Weg, der noch eine Adresse liefert.

**FLV vor HLS.** Fuer den Restream ist FLV die stabile Quelle — EINE
fortlaufende Verbindung statt einer Kette signierter Segmente; HLS reisst
ab (`rc=187`, „mime type is not rfc8216 compliant"). Dieselbe Regel wie in
`nc/livefolge.hat_stream_url` und `nc/restreamcmd`.

Reine Rechnung, kein yt-dlp, kein Netz: so laesst sich die Zuordnung
pruefen, ohne einen Live-Stream zu brauchen.
"""

# Woran eine HLS-Adresse erkennbar ist. `m3u8_native` und `m3u8` sind die
# beiden protocol-Werte, die yt-dlp fuer HLS setzt.
_HLS_PROTOKOLLE = ("m3u8", "m3u8_native")
_FLV_PROTOKOLLE = ("flv", "http_flv")


def _ist_hls(url, protokoll="", ext=""):
    u = (url or "").lower()
    return (".m3u8" in u or (protokoll or "").lower() in _HLS_PROTOKOLLE
            or (ext or "").lower() == "m3u8")


def _ist_flv(url, protokoll="", ext=""):
    u = (url or "").lower()
    # Die Endung steht bei TikTok vor dem Query-Teil (…/stream.flv?expire=…),
    # deshalb `.flv` im ganzen String und nicht endswith: ein endswith haette
    # jede signierte FLV-Adresse verworfen, und genau die sind es alle.
    return (".flv" in u or (protokoll or "").lower() in _FLV_PROTOKOLLE
            or (ext or "").lower() == "flv")


def _kandidaten(data):
    """Alle (url, protokoll, ext) aus der yt-dlp-Auskunft — Formate zuerst.

    `formats` ist die vollstaendige Liste; `url` und `manifest_url` auf der
    obersten Ebene sind das von yt-dlp selbst gewaehlte Format. Beide Quellen
    werden gelesen, weil `--dump-single-json` je nach Extractor-Version nur
    eine von beiden fuellt — wer sich auf eine verlaesst, bekommt bei der
    anderen Fassung wortlos nichts.
    """
    aus = []
    for f in (data.get("formats") or []):
        if not isinstance(f, dict):
            continue
        for schluessel in ("url", "manifest_url"):
            u = f.get(schluessel)
            if u:
                aus.append((str(u), str(f.get("protocol") or ""),
                            str(f.get("ext") or "")))
    for schluessel in ("url", "manifest_url"):
        u = data.get(schluessel)
        if u:
            aus.append((str(u), str(data.get("protocol") or ""),
                        str(data.get("ext") or "")))
    return aus


def urls_aus_json(data):
    """{"hls_url": …, "flv_url": …, "via": "ytdlp"} — fehlende Schluessel fehlen.

    Leeres Woerterbuch, wenn keine der beiden Formen vorkommt. Das ist eine
    Aussage und kein Fehler: yt-dlp kann „live" sagen und trotzdem nur
    Formate liefern, die wir nicht pullen koennen.
    """
    # EIN Ausgang, nicht zwei: `return {}` an dieser Stelle war ein stummer
    # Misserfolgs-Rueckweg (tools/blindstellen.py zaehlt genau das), und die
    # Funktion hat in Wahrheit nur ein Ergebnis — die leere Zuordnung IST die
    # Antwort "keine der beiden Formen dabei". Wer sie meldet, ist der Aufrufer;
    # dieses Modul loggt nicht (siehe Modultext).
    if not isinstance(data, dict):
        data = {}
    hls = flv = None
    for url, protokoll, ext in _kandidaten(data):
        if flv is None and _ist_flv(url, protokoll, ext):
            flv = url
        elif hls is None and _ist_hls(url, protokoll, ext):
            hls = url
        if flv and hls:
            break
    aus = {}
    if hls:
        aus["hls_url"] = hls
    if flv:
        aus["flv_url"] = flv
    if aus:
        # `via` landet im Dashboard-Suffix und in stream.resolve.ok — ohne ihn
        # waere im Log nicht zu sehen, WELCHER Weg die Adresse gebracht hat,
        # und genau das ist hier die Nachricht.
        aus["via"] = "ytdlp"
    return aus
