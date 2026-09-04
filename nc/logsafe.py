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
