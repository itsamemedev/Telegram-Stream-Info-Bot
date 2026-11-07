"""nc.linkvideo — YouTube-/TikTok-Link gepostet, Video als Antwort (bot-frei).

v4.2-W169. Gemeldet am 07.11.: „Wenn ich in Discord oder Telegram einen
YouTube- oder TikTok-Link poste, sollte der Bot das Video downloaden und
direkt uploaden als Antwort auf den gesendeten Link."

Hier steht alles, was Telegram und Discord gemeinsam haben: welche Links
zaehlen, der yt-dlp-Aufruf, das Einpassen in das Upload-Limit und der
Klartext eines Fehlschlags. Das Senden selbst macht der jeweilige Bot-Teil —
er kennt sein Limit (Telegram 50 MB, Discord je nach Boost-Stufe).

Drei Entscheidungen, die zaehlen:

* **Live-Links sind kein Video.** `tiktok.com/@name/live` ist das Tracking-
  Thema dieses Bots, kein Download; yt-dlp liefe dort bis zum Zeitlimit.
  Erkannt werden nur Einzelvideos, und `--match-filter !is_live` faengt den
  Rest (ein YouTube-Link, der gerade live ist).
* **Erst passend waehlen, dann verkleinern.** yt-dlp nimmt zuerst eine
  Fassung unter dem Limit; nur wenn es keine gibt, wird nach dem Download
  neu kodiert (`verkleinern`, eingereicht von bot.py — dieselbe Funktion wie
  fuer die Discord-Clips, keine zweite Bitratenrechnung).
* **Jeder Fehlschlag bekommt einen Satz mit Grund.** Ein stilles Nichts auf
  einen geposteten Link sieht aus wie ein toter Bot (Klasse W81).
"""

import asyncio
import logging
import os
import re
import shutil
import tempfile
from urllib.parse import urlsplit

from nc import kindprozess as _kind

_log = logging.getLogger("TikTokBot")

_KONF = {
    "verkleinern": None,     # async (pfad, limit_mb) -> pfad|None
    "tiktok_cookies": None,  # Pfad der TikTok-Cookie-Datei (Netscape)
    "proxy": None,           # () -> str|None, z.B. RECORD_PROXY
    "arbeitsdir": None,      # Basisordner fuer Downloads
}

# Hoechstens so viele Links je Nachricht — eine eingefuegte Linkliste soll
# nicht zwanzig Downloads anstossen.
MAX_LINKS = 3

_YT = re.compile(
    r"https?://(?:www\.|m\.|music\.)?(?:youtube\.com/(?:watch\?(?:[^\s<>]*?&)?v=[\w-]{11}"
    r"|shorts/[\w-]{11})|youtu\.be/[\w-]{11})[^\s<>]*", re.I)
_TT = re.compile(
    r"https?://(?:(?:www\.|m\.)?tiktok\.com/@[\w.-]+/video/\d+"
    r"|(?:vm|vt)\.tiktok\.com/[\w-]+|(?:www\.)?tiktok\.com/t/[\w-]+)/?[^\s<>]*", re.I)


def configure(**kw):
    for k, v in kw.items():
        if k not in _KONF:
            raise TypeError("nc.linkvideo.configure: unbekannt %s" % k)
        _KONF[k] = v


def an() -> bool:
    """LINK_VIDEO (Vorgabe an). Als Funktion gelesen — .env kommt spaeter."""
    return (os.getenv("LINK_VIDEO", "1") or "").strip().lower() not in ("0", "false", "no", "off")


def _zahl(name, vorgabe):
    roh = (os.getenv(name, "") or "").strip()
    return float(roh) if roh.replace(".", "", 1).isdigit() else float(vorgabe)


def max_dauer_s() -> int:
    """LINK_VIDEO_MAX_MIN (Vorgabe 20): laengere Videos werden nicht geladen —
    ein zweistuendiger Mitschnitt passt in kein Upload-Limit, auch nicht
    verkleinert, und bindet den Server minutenlang."""
    return int(_zahl("LINK_VIDEO_MAX_MIN", 20) * 60)


def abklingzeit_s() -> float:
    """LINK_VIDEO_COOLDOWN_S (Vorgabe 15) je Absender."""
    return _zahl("LINK_VIDEO_COOLDOWN_S", 15)


def links(text) -> list:
    """Die ladbaren Links einer Nachricht, in Reihenfolge, ohne Doppel,
    hoechstens MAX_LINKS. Ein Satzzeichen am Ende gehoert nicht zum Link."""
    treffer = sorted([(m.start(), m.group(0)) for rx in (_YT, _TT)
                      for m in rx.finditer(text or "")])
    aus = []
    for _pos, url in treffer:
        url = url.rstrip(").,;:!?>'\"]")
        if url not in aus:
            aus.append(url)
    return aus[:MAX_LINKS]


def ist_tiktok(url) -> bool:
    """Gehoert der Link zu TikTok? Am HOSTNAMEN entschieden, nicht am Text —
    `https://youtu.be/x?ref=tiktok.com` ist YouTube, und TikTok-Cookies und
    -Proxy haben dort nichts zu suchen (CodeQL, PR #211)."""
    host = (urlsplit(url or "").hostname or "").lower()
    return host == "tiktok.com" or host.endswith(".tiktok.com")


def befehl(ytdlp, url, vorlage, limit_mb, max_dauer, cookies=None, proxy=None) -> list:
    """Der yt-dlp-Aufruf. Format: zuerst eine fertige mp4 unter dem Limit,
    dann bis 720p zusammengesetzt (das verkleinert sich gut), zuletzt das
    Beste. Die Gesamtgrenze verhindert einen 4-GB-Download, der ohnehin nie
    in ein Upload-Limit passt."""
    fmt = ("b[ext=mp4][filesize<{L}M]/b[ext=mp4][filesize_approx<{L}M]/"
           "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[height<=720]+ba/b[height<=720]/b"
           ).format(L=int(limit_mb))
    cmd = [ytdlp, "--no-playlist", "--no-progress", "--no-warnings",
           "-f", fmt, "--merge-output-format", "mp4",
           "--max-filesize", "%dM" % max(300, int(limit_mb) * 10),
           "--match-filter", "!is_live & duration <=? %d" % int(max_dauer),
           "-o", vorlage, "--no-simulate",
           "--print", "after_move:%(filepath)s\t%(title).180s"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    if proxy:
        cmd += ["--proxy", proxy]
    cmd.append(url)
    return cmd


def ausgabe_lesen(out) -> tuple:
    """(pfad, titel) aus der letzten --print-Zeile — oder ("", "")."""
    zeilen = [z.partition("\t") for z in (out or "").splitlines()]
    gute = [(p.strip(), t.strip()) for p, tab, t in zeilen if tab and p.strip()]
    return (gute or [("", "")])[-1]


# (Muster im stderr, Klartext mit Abhilfe). Reihenfolge = Vorrang.
_GRUENDE = (
    ("does not pass filter", "das Video ist zu lang (über LINK_VIDEO_MAX_MIN) oder gerade live"),
    ("is live", "das ist ein laufender Livestream, kein Video"),
    ("sign in to confirm", "YouTube verlangt eine Anmeldung (Bot-Sperre gegen die Server-IP) — "
                           "Cookies in LINK_VIDEO_YT_COOKIES_PATH hinterlegen"),
    ("confirm your age", "altersbeschränkt — ohne angemeldete Cookies nicht ladbar"),
    ("age-restricted", "altersbeschränkt — ohne angemeldete Cookies nicht ladbar"),
    ("private", "das Video ist privat"),
    ("unavailable", "das Video ist nicht (mehr) verfügbar"),
    ("removed", "das Video wurde entfernt"),
    ("file is larger than max-filesize", "die Datei ist zu groß"),
    ("http error 403", "Zugriff verweigert (403) — für TikTok helfen frische Cookies "
                       "oder RECORD_PROXY"),
    ("http error 404", "nicht gefunden (404)"),
    ("unsupported url", "dieser Link wird nicht unterstützt"),
)


def grund(err) -> str:
    """Klartext eines yt-dlp-Fehlschlags. Ohne Treffer die letzte
    ERROR-Zeile — gekuerzt, aber nie leer."""
    text = (err or "").lower()
    for muster, satz in _GRUENDE:
        if muster in text:
            return satz
    zeilen = [z for z in (err or "").splitlines() if z.strip()]
    fehler = [z for z in zeilen if "ERROR" in z] or zeilen or ["unbekannt"]
    return fehler[-1].replace("ERROR:", "").strip()[:200] or "unbekannt"


def werkzeug(which=shutil.which):
    """Pfad von yt-dlp — oder "" (dann sagt der Aufrufer es laut)."""
    return which("yt-dlp") or which("yt_dlp") or ""


def _cookies_fuer(url):
    if ist_tiktok(url):
        return _KONF["tiktok_cookies"]
    return (os.getenv("LINK_VIDEO_YT_COOKIES_PATH", "") or "").strip() or None


async def holen(url, limit_mb) -> dict:
    """Video laden und ins Limit einpassen.

    -> {"pfad", "titel", "grund", "ordner"}. `pfad` leer heisst Fehlschlag,
    `grund` sagt warum. `ordner` raeumt der Aufrufer mit `aufraeumen()` weg —
    auch im Fehlerfall, sonst bleiben Teil-Downloads liegen."""
    ytdlp = werkzeug()
    erg = {"pfad": "", "titel": "", "grund": "", "ordner": ""}
    if not ytdlp:
        erg["grund"] = "yt-dlp ist nicht installiert (pip install yt-dlp)"
        return erg
    basis = _KONF["arbeitsdir"] or tempfile.gettempdir()
    os.makedirs(basis, exist_ok=True)
    erg["ordner"] = tempfile.mkdtemp(prefix="link-", dir=basis)
    proxy = _KONF["proxy"]() if callable(_KONF["proxy"]) else _KONF["proxy"]
    cmd = befehl(ytdlp, url, os.path.join(erg["ordner"], "%(id)s.%(ext)s"), limit_mb,
                 max_dauer_s(), _cookies_fuer(url), proxy if ist_tiktok(url) else None)
    try:
        rc, out, err = await _kind.ausfuehren(cmd, max_dauer_s() + 180, art="yt-dlp-link")
    except (asyncio.TimeoutError, OSError) as e:
        erg["grund"] = ("der Download hat das Zeitlimit überschritten"
                        if isinstance(e, asyncio.TimeoutError)
                        else "yt-dlp ließ sich nicht starten: %s" % e)
        _log.warning("Link-Video %s: %s", url, erg["grund"])
        return erg
    pfad, erg["titel"] = ausgabe_lesen(out.decode("utf-8", "replace"))
    if rc != 0 or not pfad or not os.path.isfile(pfad):
        erg["grund"] = grund(err.decode("utf-8", "replace"))
        return erg
    if os.path.getsize(pfad) > limit_mb * 1024 * 1024:
        klein = await _KONF["verkleinern"](pfad, limit_mb) if _KONF["verkleinern"] else None
        if not klein:
            erg["grund"] = "auch verkleinert größer als %d MB" % int(limit_mb)
            return erg
        pfad = klein
    erg["pfad"] = pfad
    return erg


def aufraeumen(erg) -> None:
    """Den Arbeitsordner eines `holen()` entfernen (Fehlschlag eingeschlossen)."""
    if erg and erg.get("ordner"):
        shutil.rmtree(erg["ordner"], ignore_errors=True)


def bildunterschrift(titel, url) -> str:
    """Kurz: Titel und Quelle. Der Link steht in der Nachricht darueber."""
    quelle = "TikTok" if ist_tiktok(url) else "YouTube"
    return ("🎬 %s · %s" % ((titel or "Video")[:180], quelle))


# Gemeinsam fuer Telegram und Discord: EIN Deckel fuer gleichzeitige
# Downloads (ein Download ist ein yt-dlp plus womoeglich ein ffmpeg — zwei
# Plattformen mit je eigenem Deckel waeren doppelt so viel Last) und eine
# Abklingzeit je Absender. Modulglobal, nicht am Client-Objekt (W-Regel).
_ZULETZT = {}
_SPERRE = {"s": None}


def darf(absender, jetzt) -> bool:
    """True und Zeit merken — oder False, wenn derselbe Absender innerhalb
    der Abklingzeit schon einen Download ausgeloest hat."""
    if jetzt - _ZULETZT.get(absender, -1e9) < abklingzeit_s():
        return False
    _ZULETZT[absender] = jetzt
    if len(_ZULETZT) > 2000:                 # nicht endlos wachsen
        grenze = jetzt - abklingzeit_s()
        for k in [k for k, t in _ZULETZT.items() if t < grenze]:
            _ZULETZT.pop(k, None)
    return True


def sperre():
    """Der gemeinsame Semaphor (LINK_VIDEO_PARALLEL, Vorgabe 1). Erst im
    laufenden Loop angelegt, dann fuer immer derselbe."""
    if _SPERRE["s"] is None:
        _SPERRE["s"] = asyncio.Semaphore(max(1, int(_zahl("LINK_VIDEO_PARALLEL", 1))))
    return _SPERRE["s"]
