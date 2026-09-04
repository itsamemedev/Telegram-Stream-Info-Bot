"""nc.systemprobe — die Sonden, die /api/system beantwortet.

Warum es das gibt: `/api/system` fragt vier Dinge ab, die alle nichts mit dem
Bot-Loop zu tun haben — laeuft Redis, welche Version, wie viele KI-Aufrufe
zaehlt es, und welcher Recorder wuerde gerade greifen. Im Monolithen hingen
sie an den Modul-Konstanten REDIS_URL und RECORDER_PREF und waren damit
unbeweglich, obwohl der Code selbst reine stdlib ist.

Die Redis-Sonden sprechen RESP direkt ueber einen Socket statt ueber das
redis-Paket. Das ist Absicht und bleibt so: die Sonde muss auch dann eine
Antwort liefern, wenn das Paket fehlt — sonst meldet das Deck "Redis tot",
weil eine Bibliothek nicht installiert ist.

Konfiguration kommt per configure(), nicht per os.getenv() auf Modul-Ebene.
CLAUDE.md: ".env wird teils erst nach den ersten Imports geladen" — eine
Modul-Konstante haette hier die leere Vorgabe eingefroren.
"""
import socket as _socket
import time as _time
from urllib.parse import urlparse as _urlparse

# Der Bot fror diese Werte ebenfalls beim Import ein; hier passiert nichts
# anderes, nur an einer Stelle, die man ueberschreiben kann.
_CONF = {"redis_url": "redis://localhost:6379/0", "recorder_pref": "auto"}

# 5 Sekunden: das Dashboard pollt /api/system im Sekundentakt. Ohne Deckel
# haette jede Kachel einen eigenen TCP-Verbindungsaufbau ausgeloest.
TTL = 5.0
_CACHE = {}


def configure(**kw):
    """Vom Bot einmal beim Start gerufen. Unbekannte Schluessel fliegen auf."""
    for k, v in kw.items():
        if k not in _CONF:
            raise KeyError("nc.systemprobe kennt %r nicht" % k)
        _CONF[k] = v


def recorder_pref():
    return _CONF["recorder_pref"]


def redis_url():
    return _CONF["redis_url"]


def cached_probe(key, fn, *args, **kwargs):
    """Ergebnis fuer TTL Sekunden festhalten. Auch None und False zaehlen als
       Ergebnis — sonst probiert eine tote Sonde bei jedem Aufruf neu."""
    jetzt = _time.monotonic()
    hat = _CACHE.get(key)
    if hat and hat[1] > jetzt:
        return hat[0]
    wert = fn(*args, **kwargs)
    _CACHE[key] = (wert, jetzt + TTL)
    return wert


def cache_leeren():
    """Nur fuer Tests — der Betrieb laesst den Deckel stehen."""
    _CACHE.clear()


def _ziel():
    u = _urlparse(_CONF["redis_url"])
    return (u.hostname or "localhost"), (u.port or 6379)


def redis_alive(timeout=1.0):
    """RAW-TCP-Ping an Redis. Sendet PING und prueft +PONG."""
    def _sonde():
        try:
            with _socket.create_connection(_ziel(), timeout=timeout) as sock:
                sock.sendall(b"*1\r\n$4\r\nPING\r\n")
                return b"PONG" in sock.recv(64)
        except Exception:
            return False
    return cached_probe("redis_alive", _sonde)


def redis_version(timeout=1.0):
    """INFO server -> redis_version. None bei Fehler."""
    def _sonde():
        try:
            with _socket.create_connection(_ziel(), timeout=timeout) as sock:
                sock.sendall(b"*2\r\n$4\r\nINFO\r\n$6\r\nserver\r\n")
                data = b""
                while b"\r\n\r\n" not in data and len(data) < 8192:
                    stueck = sock.recv(4096)
                    if not stueck:
                        break
                    data += stueck
            for zeile in data.decode("utf-8", errors="ignore").splitlines():
                if zeile.startswith("redis_version:"):
                    return zeile.split(":", 1)[1].strip()
        except Exception:
            pass
        return None
    return cached_probe("redis_version", _sonde)


def ai_calls_total():
    """Liest ai_calls_total via rohem RESP. 0 wenn Redis nicht da."""
    try:
        with _socket.create_connection(_ziel(), timeout=1.0) as sock:
            sock.sendall(b"*2\r\n$3\r\nGET\r\n$15\r\nai_calls_total\r\n")
            data = sock.recv(128).decode("utf-8", errors="ignore")
        if data.startswith("$-1"):
            return 0
        if data.startswith("$"):
            teile = data.split("\r\n", 2)
            if len(teile) >= 2:
                try:
                    return int(teile[1])
                except ValueError:
                    return 0
    except Exception:
        pass
    return 0


def active_recorder(which=None):
    """Welcher Recorder wuerde greifen — ohne etwas aufzuloesen.

    `which` ist shutil.which; als Parameter, damit der Vertrag die Auswahl
    pruefen kann, ohne ffmpeg zu installieren.
    """
    if which is None:
        import shutil
        which = shutil.which
    hat_ffmpeg = bool(which("ffmpeg"))
    hat_ytdlp = bool(which("yt-dlp") or which("yt_dlp"))
    pref = _CONF["recorder_pref"]
    if pref == "native":
        return "native" if hat_ffmpeg else None
    if pref == "ytdlp":
        return "ytdlp" if hat_ytdlp else None
    if hat_ffmpeg:
        return "native"
    if hat_ytdlp:
        return "ytdlp"
    return None
