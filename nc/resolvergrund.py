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
        "TikToks API antwortet mit einem Serverfehler (500/503/504), auch nach "
        "dem Zweitversuch. Meist transient; haelt es an, ist der Proxy-Pool "
        "schlecht.",
    "http_502":
        "502 vom TikTok-Edge, auch nach dem Zweitversuch. Wichtig fuer die "
        "Unterscheidung: Diese Antwort kam ueber die stehende TLS-Verbindung "
        "ZURUECK — ein Proxy, der selbst nicht durchkommt, laesst schon den "
        "CONNECT scheitern und erscheint hier als 'netz', nicht als 502. Ein "
        "502 heisst also: die Verbindung stand, und die Gegenseite hat "
        "abgelehnt. Dauerhaft auf allen Nutzern deutet das auf eine "
        "IP-Reputation hin, die TikTok am Edge abweist statt sie zu "
        "bedienen — dieselbe Abhilfe wie bei 403 (RECORD_PROXY mit "
        "Residential/Mobile). Die Verteilung ueber alle Statuscodes zeigt "
        "/api/stats/tiktok-status.",
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
    # v4.2-W102: der Fall, den der Restream bis dahin als "nicht live" verbucht
    # hat. Er ist das GEGENTEIL von offline: der Raum lebt, der Chat haengt
    # dran, nur die Adresse kommt nicht heraus.
    "ytdlp_abgeschaltet":
        "yt-dlp ist installiert, aber der Schutzschalter hat es abgeschaltet "
        "(zu viele Fehlschlaege in Folge). Damit fehlt gerade der Weg, der "
        "TikToks Signaturen selbst erzeugt und am haeufigsten durchkommt. Er "
        "kommt von selbst zurueck; haelt es an, ist der Proxy das Problem "
        "(RECORD_PROXY) oder yt-dlp zu alt (`pip install -U yt-dlp`).",
    "quelle_ohne_url":
        "Der Nutzer ist LIVE (der Chat verbindet sich und laeuft durchs "
        "Transkript), aber keiner der Aufloesungswege gibt eine Stream-Adresse "
        "heraus — ohne Adresse kann der Restream nicht starten. Das ist NICHT "
        "'offline'. TikTok haelt die Adresse vor einer Datacenter-IP oft "
        "zurueck; Gast-Cookies helfen dagegen nicht, sie erneuern nur die "
        "Anti-Bot-Tokens. Abhilfe: RECORD_PROXY auf einen Residential-/"
        "Mobil-Proxy setzen oder den Tunnel einschalten, und pruefen, dass "
        "yt-dlp installiert ist (es signiert selbst und kommt am haeufigsten "
        "durch).",
}

# v4.2-W102: die Lage der QUELLE, abgeleitet aus dem Fehlertext, den
# `RestreamManager._resolve_source` zurueckgibt.
#
# Der Anlass: der Aufrufer schrieb `src_live = not _err` und machte damit aus
# fuenf verschiedenen Lagen zwei. "offline" (der Streamer sendet nicht) und
# "keine spielbare Quell-URL" (er sendet, wir kommen nicht an den Stream) sind
# vollkommen verschiedene Nachrichten mit vollkommen verschiedener Abhilfe —
# der Waechter sah beide als `source_live=False` und meldete "Quelle nicht
# live — kein Start". Dieselbe Klasse wie `audio=False` fuer drei Ursachen
# (W55) und `None` = "tot" in nc/preflight (W89).
# Kein Hindernis. Ausdruecklich benannt und nicht "" — eine leere Zeichenkette
# liest sich wie "nichts herausgefunden", und das ist das Gegenteil. Dieselbe
# Lehre wie `log_wartend = -1` statt 0 in W97: eine 0 liest sich wie
# Normalbetrieb.
LAGE_OK = "ok"
LAGE_OFFLINE = "offline"
LAGE_OHNE_URL = "ohne_url"
LAGE_UNBEKANNT = "unbekannt"
LAGE_ABO = "abo"
LAGE_FEHLER = "fehler"


def quelle_lage(err) -> str:
    """Fehlertext aus `_resolve_source` -> Lage-Schluessel.

    `err` ist falsy, wenn eine URL da ist — dann LAGE_OK. Gepruefte
    Reihenfolge: die eindeutigen Zeichenketten zuerst, der Rest ist ein Fehler.
    Ein unbekannter Text wird NIE still verschluckt, er wird LAGE_FEHLER und
    taucht damit im Log auf.
    """
    e = (err or "").strip()
    if not e:
        return LAGE_OK
    if e == "offline":
        return LAGE_OFFLINE
    if e == "unknown":
        return LAGE_UNBEKANNT
    if e.startswith("Abo-Stream"):
        return LAGE_ABO
    if "keine spielbare Quell-URL" in e:
        return LAGE_OHNE_URL
    return LAGE_FEHLER


def quelle_laut(lage: str) -> bool:
    """Gehoert diese Lage ins Log, oder ist sie Normalbetrieb?

    "offline" ist der Alltag — ein getrackter Nutzer sendet die meiste Zeit
    nicht, und eine Zeile pro Pruefung waere Rauschen. "abo" ist eine bewusste
    Entscheidung des Betreibers (B148). Alles andere ist ein Hindernis und
    gehoert gesagt, gedrosselt.
    """
    return lage in (LAGE_OHNE_URL, LAGE_UNBEKANNT, LAGE_FEHLER)


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
    if status == 502:
        # v4.2-W82: eigener Grund. Der Betreiber meldete am 13.09. "die
        # Live-Abfragen geben 502 aus", und die Sammelkategorie 5xx haette
        # das als "meist transient" abgetan — waehrend ein dauerhafter 502
        # ueber alle Nutzer dieselbe Ursache hat wie ein 403.
        return "http_502"
    if 500 <= status <= 599:
        return "http_5xx"
    return "http_andere"
