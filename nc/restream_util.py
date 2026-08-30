"""nc.restream_util — v4.0-W25: reine Restream-Helfer, aus bot.py extrahiert.

Zwei kleine, aber auf kritischen Pfaden sitzende Funktionen — beide ohne jede
Bot-Kopplung (nur stdlib), deshalb verlustfrei herauslösbar und bitgenau gegen
den Monolith geprüft:

* normalize_ingest        — RTMPS-Ingest-URL für AWS-IVS/Kick korrekt machen
                            (Port :443 + /app), sonst bricht der TLS-Handshake.
* looks_like_source_expired — unterscheidet eine ABGELAUFENE TikTok-Pull-URL
                            (Normalfall, ~6 min Gültigkeit) von einem echten
                            Fehler, damit ein Ablauf nicht gegen MAX_RECONNECTS
                            zählt.

Der Bot ruft nur noch hierher durch; Signaturen und Verhalten unverändert.
"""

from urllib.parse import urlsplit, urlunsplit


def normalize_ingest(ingest_url: str) -> str:
    """WHY: AWS-IVS / Kick (*.live-video.net) brauchen ZWINGEND :443 + /app im
       Pfad. Eine nackte Host-URL (rtmps://host/) ergibt sonst rtmps://host/<key>
       und der TLS-Handshake bricht mit 'IO error: End of file' (ffmpeg rc=251)
       ab. Ergänzt fehlenden Port (rtmps→443) und App-Pfad, ohne vorhandene zu
       verdoppeln. Andere Endpunkte bleiben unverändert (nur Port-Default)."""
    u = (ingest_url or "").strip().rstrip("/")
    if not u:
        return u
    try:
        p = urlsplit(u)
        scheme = (p.scheme or "rtmps").lower()
        host = p.hostname or ""
        if not host:
            return u
        if p.port is not None:
            netloc = f"{host}:{p.port}"
        elif scheme == "rtmps":
            netloc = f"{host}:443"          # RTMPS-Default; IVS verlangt ihn explizit
        else:
            netloc = host
        path = p.path or ""
        if "live-video.net" in host and not path.strip("/"):
            path = "/app"                   # IVS/Kick-Applikationspfad
        return urlunsplit((scheme, netloc, path, "", ""))
    except Exception:
        return u


def looks_like_source_expired(text):
    """Ist der Abbruch durch eine ABGELAUFENE TikTok-Quell-URL entstanden?

    TikTok liefert signierte Pull-URLs mit begrenzter Gueltigkeit — in der
    Praxis rund sechs Minuten. Laeuft eine ab, meldet ffmpeg 404/403 bzw.
    'Stream ends prematurely' + einen Reconnect-Versuch auf DIESELBE, jetzt
    tote URL. Das ist kein Fehlversuch, sondern der Normalfall — es hilft nur
    eine NEU aufgeloeste URL, nicht Backoff/Reconnect.
    """
    t = (text or "").lower()
    if "404 not found" in t or "403 forbidden" in t:
        return True
    # 'Stream ends prematurely' allein reicht nicht — das kommt auch bei einem
    # echten Streamende. Erst zusammen mit einem Reconnect-Versuch ist es der
    # Ablauf-Fall.
    return "stream ends prematurely" in t and "will reconnect" in t


def url_host(url: str) -> str:
    """v4.1-W10: Hostname aus einer rtmp(s)-URL — ohne Schema, Port, Pfad und
    Key, lowercase. Hiess in bot.py _url_host (B141) und wird jetzt von zwei
    Stellen gebraucht: dem tee-Fehler-Labeling und der Abbruch-Diagnose."""
    if not url or "://" not in url:
        return ""
    rest = url.split("://", 1)[1]
    return rest.split("/", 1)[0].split(":", 1)[0].strip().lower()


def betroffene_ziele(tail, targets):
    """Welche Restream-Ziele nennt dieser ffmpeg-stderr-Auszug beim Namen?

    Rückgabe: die Namen aus `targets` ([(name, url), …]), deren INGEST-HOST im
    Text vorkommt — in der Reihenfolge von `targets`, ohne Dubletten.

    WARUM das gebraucht wird: die Abbruch-Diagnose in bot.py schrieb bei jedem
    'Input/output error' und jedem 'End of file' kategorisch "Kick-Ingest nimmt
    die Verbindung nicht an" — auch dann, wenn im Auszug ausschliesslich der
    TWITCH-Slave stand. Der Betreiber suchte danach am falschen Ende: Kick-Key
    prüfen, Kick-App prüfen, IP-Block bei Kick prüfen, während Twitch das
    Problem war. Ein Diagnosetext, der auf die falsche Plattform zeigt, ist
    schlimmer als gar keiner.

    Kick und Twitch liegen BEIDE auf live-video.net (beide fahren AWS IVS) —
    deshalb wird auf den vollen Host verglichen, nie auf den Plattformnamen:
    'twitch' kommt in Twitchs eigener Ingest-URL gar nicht vor.
    """
    text = (tail or "").lower()
    out = []
    for name, url in (targets or []):
        host = url_host(url)
        if host and host in text and name not in out:
            out.append(name)
    return out


def fenstergroesse(text, fallback="1080,1920"):
    """`W,H` aus reinen Ziffern — oder der Fallback.

    v4.1-W10 (CodeQL py/command-line-injection): dieser Wert landet in
    `--window-size=…` auf der Chromium-Kommandozeile. Er stammt aus der .env
    (RESTREAM_OVERLAY_HTML_SIZE) bzw. aus einer ffprobe-Messung. Die
    Kommandozeile wird als LISTE uebergeben, es gibt also keine Shell — aber
    ein Wert wie "800,600 --dump-dom" waere trotzdem ein zweites Argument fuer
    Chromium. Hier kommt nur durch, was aus zwei Zahlen besteht.

    Ein Trennzeichen `,` oder `x` wird akzeptiert (beides steht in echten
    .env-Dateien), ausgegeben wird immer die Chromium-Schreibweise mit Komma.
    """
    import re
    m = re.fullmatch(r"\s*(\d{1,5})\s*[,x]\s*(\d{1,5})\s*", str(text or ""))
    if not m:
        return fallback
    b, h = int(m.group(1)), int(m.group(2))
    if not (0 < b <= 16384 and 0 < h <= 16384):
        return fallback
    return f"{b},{h}"


def http_url(text, fallback=""):
    """Nur http/https lassen wir auf eine Kommandozeile.

    v4.1-W10: die Overlay-URL kommt aus der .env und wird an Chromium
    uebergeben. `file:///etc/shadow` waere dort eine gueltige Seite, und ein
    Wert, der mit `--` beginnt, waere ueberhaupt keine URL, sondern ein
    weiteres Argument.
    """
    t = str(text or "").strip()
    low = t.lower()
    if low.startswith("http://") or low.startswith("https://"):
        return t
    return fallback
