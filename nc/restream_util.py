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
