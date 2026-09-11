"""nc.logsafe — v4.0-W32: sicherheitsrelevante Log-Redaction, aus bot.py gelöst.

Ein Stream-Key ist das Passwort des Kanals — wer ihn hat, sendet auf fremdem
Namen. ffmpeg schreibt bei tee-Fehlern die volle Ziel-URL inkl. Key nach stderr;
landet das im Log/Screenshot/Support-Upload, wandert der Key nach draussen.
redact_stream_urls ersetzt den Key durch <KEY:Länge…letzte4>, lässt Host+Pfad
für die Fehlersuche stehen. Rein (Regex wird hereingereicht), bitgenau geprüft.
"""

import re

# Default-Regex identisch zum Monolithen; der Bot reicht seine kompilierte
# Instanz herein, damit es genau EINE Wahrheit gibt.
RE_STREAM_URL = re.compile(
    r"(rtmps?://[^\s'\"]*?/(?:app|live2|live)/)([^\s'\"]+)", re.I)


def redact_stream_urls(text, rx=RE_STREAM_URL):
    """Stream-Keys aus beliebigem Text entfernen (ffmpeg-stderr, Fehlertexte).

    Host und Pfad bleiben stehen: an ihnen erkennt man das Ziel, und genau das
    braucht die Fehlersuche. Vom Key bleiben Länge und die letzten vier Zeichen —
    damit lässt er sich gegen das Plattform-Dashboard vergleichen, ohne ihn
    preiszugeben.
    """
    def _ersetz(m):
        key = m.group(2)
        return f"{m.group(1)}<KEY:{len(key)}z…{key[-4:] if len(key) > 8 else ''}>"
    try:
        return rx.sub(_ersetz, text)
    except Exception:
        # Im Zweifel lieber die ganze Zeile verwerfen als einen Key ausgeben.
        return "<Zeile wegen Redact-Fehler unterdrueckt>"


def url_ohne_zugang(url):
    """v4.0-W118 (SEC): Zugangsdaten aus einer URL entfernen, Rest lesbar lassen.

    REDIS_URL & Co. duerfen ein Passwort tragen (redis://:geheim@host:6379/0).
    /api/system gab die URL bisher unveraendert aus — die Antwort landet im
    Browser-Cache, in Screenshots und in jedem Support-Log. Host und Port
    bleiben stehen, denn genau die braucht die Fehlersuche.

    v4.1-W32: aus bot.py hierher. Es ist dieselbe Aufgabe wie
    redact_stream_urls — etwas Geheimes aus einem Text nehmen, ohne den Text
    unbrauchbar zu machen — und gehoert deshalb in dieselbe Datei.
    """
    try:
        u = (url or "").strip()
        if "@" not in u or "//" not in u:
            return u
        schema, rest = u.split("//", 1)
        zugang, ziel = rest.rsplit("@", 1)
        benutzer = zugang.split(":", 1)[0]
        return f"{schema}//{benutzer + ':' if benutzer else ''}<geheim>@{ziel}"
    except Exception:
        return "<URL unterdrueckt>"


# --- v4.2-W46: was in einem ffmpeg-stderr sonst noch geheim ist -----------
#
# redact_stream_urls oben deckt RTMP-Sendeschluessel ab — also die Ziel-Seite.
# Der Audio-Tap der Live-Reaktion zieht aber von der QUELL-Seite, und dort
# steht die signierte TikTok-Pull-URL:
#
#   https://pull-hls-f16-va01.tiktokcdn.com/stage/stream-123.m3u8
#       ?expire=1757620800&sign=8f3c...&session_id=...
#
# Wer diese URL hat, zieht den Stream mit — und bekommt mit session_id unter
# Umstaenden mehr. Bis W46 war das egal, weil das stderr des Taps nach
# DEVNULL ging und nie jemand sah. Genau das aendert W46, und deshalb muss
# der Riegel VOR dem ersten Log stehen, nicht danach.

RE_PULL_URL = re.compile(r"(https?://[^\s'\"]+?)\?([^\s'\"]+)", re.I)

RE_COOKIE_ZEILE = re.compile(r"(?im)^(\s*cookie\s*:).*$")


def redact_pull_urls(text, rx=RE_PULL_URL):
    """Signatur und Sitzungsdaten aus einer Quell-URL nehmen, Rest lesbar lassen.

    Der Query-Teil traegt die Signatur; Schema, Host und Pfad bleiben stehen,
    weil genau die die Fehlersuche braucht (welches CDN, welcher Knoten,
    welcher Stream). Die Zahl der Parameter bleibt als Hinweis erhalten —
    eine URL ganz ohne Query sieht sonst aus wie eine, der die Signatur
    fehlt, und das ist ein anderer Fehler.
    """
    def _ersetz(m):
        n = len([p for p in m.group(2).split("&") if p])
        return f"{m.group(1)}?<signiert:{n}p>"
    try:
        return rx.sub(_ersetz, text)
    except Exception:
        return "<Zeile wegen Redact-Fehler unterdrueckt>"


def redact_cookie_zeilen(text, rx=RE_COOKIE_ZEILE):
    """Eine ganze Cookie-Kopfzeile schwaerzen.

    ffmpeg echot bei hoeherem Loglevel den -headers-Block zurueck. Anders als
    bei einer URL gibt es hier nichts Erhaltenswertes: dass ein Cookie gesetzt
    war, ist die ganze Information.
    """
    try:
        return rx.sub(r"\1 <redacted>", text)
    except Exception:
        return "<Zeile wegen Redact-Fehler unterdrueckt>"


def fuer_log(text, rx_stream=None):
    """Alle drei Riegel in EINEM Aufruf — der Weg, den neuer Code nimmt.

    Warum gebuendelt: bis W46 musste jede neue Log-Stelle selbst wissen,
    welche Redact-Funktionen es gibt. Genau so entsteht die Stelle, die eine
    davon vergisst. Wer Fremdtext loggt, ruft diese Funktion und ist fertig.
    """
    if not text:
        return ""
    t = redact_stream_urls(text, rx_stream) if rx_stream else redact_stream_urls(text)
    t = redact_pull_urls(t)
    return redact_cookie_zeilen(t)
