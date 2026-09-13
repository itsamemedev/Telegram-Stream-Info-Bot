"""nc.resolvergrund — v4.2-W81: warum die Stream-Aufloesung nichts geliefert hat.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Meldung des Betreibers am 13.09.:

    "Chats koennen von online tiktok Usern geladen werden aber keine
     gueltigen streams"

Das ist ein praezises Fehlerbild, und es ist ein anderes als "der Nutzer
ist offline": der Chat verbindet sich, der Raum LEBT also. Nur die
Stream-Adresse kommt nicht heraus.

Im Log stand dazu nichts. `_resolve_via_webcast_api_v2` hat elf Ausgaenge
mit leerem Ergebnis — acht auf `log.debug`, drei voellig stumm
(`return "unknown", None` ohne jede Zeile). `stillecheck` faellt dort
nicht: es gibt keinen stillen `except`, sondern ein stilles `return`. Der
Betreiber sieht das Ergebnis und hat keinen einzigen Hinweis auf die
Ursache — und die Ursachen sind vollkommen verschieden: ein 403 verlangt
einen Proxy, ein 429 verlangt Geduld, ein Parse-Fehler verlangt einen
Blick auf TikToks Antwortformat.

Dieses Modul rechnet nicht und loggt nicht. Es haelt nur die Zuordnung
"was ist passiert" -> "was heisst das und was tut der Betreiber", damit
derselbe Satz nicht an elf Stellen im Monolithen einzeln formuliert wird.
Dieselbe Bauart wie nc.audiotap.ABHILFE.
"""
from __future__ import annotations

# Grund-Schluessel -> Klartext fuer den Betreiber. Bewusst mit Abhilfe:
# "HTTP 403" allein hat schon einmal wochenlang niemandem geholfen.
GRUND = {
    "http_5xx":
        "TikToks API antwortet mit einem Serverfehler, auch nach dem "
        "Zweitversuch mit frischem Proxy. Meist transient; haelt es an, ist "
        "der Proxy-Pool schlecht.",
    "http_403":
        "TikTok blockt die abfragende IP. Das ist der haeufigste Fall bei "
        "einer Datacenter-Adresse: der Chat kommt ueber die signierte "
        "TikTokLive-Verbindung durch, die Stream-URL nicht. RECORD_PROXY "
        "(Residential/Mobile) setzen.",
    "http_andere":
        "Unerwarteter HTTP-Status von der Webcast-API. Wenn er bleibt, hat "
        "TikTok den Endpunkt geaendert.",
    "netz":
        "Die Anfrage kam gar nicht durch (Timeout, DNS, Proxy tot). Netz und "
        "Proxy-Pool pruefen — derselbe Grund wie bei abbrechenden Aufnahmen.",
    "kein_json":
        "Die Antwort war kein JSON. Typisch fuer eine Captcha- oder "
        "Blockseite, die mit HTTP 200 ausgeliefert wird.",
    "status_code":
        "Die API meldet einen Fehlerstatus im JSON. Steht dort dauerhaft "
        "derselbe Code, sind die Cookies abgelaufen.",
    "unbekannter_raumstatus":
        "Der Raum meldet einen Status, den der Bot nicht kennt. Nicht als "
        "offline gewertet — der naechste Durchlauf versucht es erneut.",
    "kein_stream_data":
        "Der Raum ist live, die Antwort enthaelt aber keinen stream_data-"
        "Block. Genau das Bild aus v4.2-W51: TikTok gibt einer Datacenter-IP "
        "die Adresse nicht heraus. RECORD_PROXY setzen.",
    "stream_data_kaputt":
        "Der stream_data-Block liess sich nicht lesen. Wenn das bleibt, hat "
        "TikTok das Format geaendert — dann muss nc.streamsel nach.",
    "keine_spielbare_url":
        "stream_data war da, enthielt aber weder HLS noch FLV. Meist ein "
        "Raum, dessen Qualitaetsstufen leer ausgeliefert werden.",
    "html_http":
        "Der HTML-Weg kam nicht durch (kein HTTP 200). Zusammen mit einem "
        "geblockten API-Weg heisst das: die IP ist verbrannt.",
    "html_netz":
        "Der HTML-Weg kam gar nicht erst durch. Netz oder Proxy.",
    "html_kein_tag":
        "Die Live-Seite kam an, enthielt aber keines der vier bekannten "
        "Script-Tags mit Live-Daten. Das ist der Fall, in dem TikTok die "
        "Seitenstruktur geaendert hat — nc._resolve_via_html braucht dann "
        "ein neues Muster.",
    "kein_ytdlp":
        "yt-dlp ist nicht installiert — der dritte Aufloesungsweg existiert "
        "auf dieser Maschine gar nicht. Er ist der einzige, der TikToks "
        "Anti-Bot-Signaturen selbst erzeugt und deshalb oft durchkommt, wo "
        "die eigenen HTTP-Wege 403 bekommen. `pip install yt-dlp`.",
    "beide_wege_leer":
        "Weder die Webcast-API noch der HTML-Weg haben eine Stream-URL "
        "geliefert. Der Recorder kann nicht starten. Haeufigste Ursache: "
        "kein Residential-Proxy (RECORD_PROXY).",
}


def text(grund: str) -> str:
    """Klartext zu einem Grund-Schluessel. Unbekannt -> der Schluessel selbst,
       damit eine neue Kategorie im Log auftaucht statt zu verschwinden."""
    return GRUND.get(grund, grund or "unbekannt")


def http_grund(status: int) -> str:
    """HTTP-Status -> Grund-Schluessel. 403 bekommt einen EIGENEN, weil die
       Abhilfe eine voellig andere ist als bei 500 oder 404."""
    # Bewusst ohne try/except: ein stiller `except` waere hier zwar harmlos,
    # er zaehlt aber gegen die Ratsche aus v4.2-W65 — und die Pruefung ist
    # ohnehin genauer als ein abgefangener int()-Fehler.
    if not isinstance(status, int) or isinstance(status, bool):
        return "http_andere"
    if status == 403:
        return "http_403"
    if 500 <= status <= 599:
        return "http_5xx"
    return "http_andere"
