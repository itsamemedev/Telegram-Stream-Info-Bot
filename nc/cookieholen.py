"""nc.cookieholen — v4.2-W10: Cookies selbst beschaffen statt von Hand einfügen.

Zwei Wege, beide bot-frei und ohne Fremdpaket auf der Modul-Ebene:

  1. **Gast-Abruf** (`hole_gastcookies`). Ein normaler HTTPS-Aufruf auf
     tiktok.com mit dem Browser-Fingerabdruck aus `nc/tiktokheaders.py`.
     TikTok setzt dabei die Anti-Bot-Tokens per Set-Cookie: `ttwid`,
     `tt_chain_token`, `tt_csrf_token`, `msToken`, `store-idc`, …
     Das ist genau der Teil, der still rotiert und den Recorder nach ein
     paar Tagen in ein 403 laufen lässt — er lässt sich ohne Login holen
     und braucht keinen Menschen.

  2. **Browser-Import** (`aus_browser`). Liest das Cookie-Profil eines lokal
     installierten Browsers — über `browser_cookie3`, falls vorhanden, sonst
     über `yt-dlp --cookies-from-browser`. Nur so kommt ein echter
     `sessionid_ss` in die Datei, ohne dass jemand eine Extension bedient.
     Auf dem Server (kein Browser, kein Profil) scheitert das absichtlich
     mit einer klaren Meldung statt still.

**Was der Gast-Abruf NICHT kann:** einen Login ersetzen. `sessionid_ss`
entsteht nur beim Anmelden im Browser. Deshalb fasst der Gast-Weg
Auth-Cookies grundsätzlich nicht an — er ergänzt und erneuert ausschließlich
die rotierenden Anti-Bot-Tokens. Ein Gast-`odin_tt` über einen
eingeloggten zu schreiben wäre ein stiller Logout, und der Fehlerbild wäre
wieder „403, aber die Cookies sind doch frisch".

**Warum nach Domain gefiltert wird:** ein Browser-Profil enthält die Cookies
*aller* Seiten — Bank, Mail, alles. Was hier nicht nach TikTok gehört, wird
verworfen, bevor es in die Datei kommt. `tiktok_cookies.txt` liegt im Bestand
und in jedem Backup; sie ist kein Abladeplatz für fremde Sitzungen.
"""

import os
import shutil
import subprocess
import time as _time
import urllib.request
from http.cookiejar import CookieJar, MozillaCookieJar

from nc.cookies import (DATEI_SPERRE, _cookies_input_to_netscape,
                        _dedupe_cookie_text)
from nc.tiktokheaders import HEADERS as _TT_HEADERS

# Die Seiten, die beim ersten Aufruf die Anti-Bot-Tokens setzen. Zwei, weil
# msToken oft erst beim zweiten Aufruf (mit ttwid im Gepäck) mitkommt.
GAST_URLS = ("https://www.tiktok.com/", "https://www.tiktok.com/explore")

# Was ein Gast-Abruf überschreiben darf: rotierende Anti-Bot-Tokens.
# Alles andere wird nur ERGÄNZT, wenn es fehlt.
ANTIBOT = {
    "ttwid", "tt_csrf_token", "tt_chain_token", "msToken", "msToken_KR",
    "s_v_web_id", "store-idc", "store-country-code", "store-country-sign",
    "tt-target-idc", "tt-target-idc-sign", "delay_guest_mode_vid",
    "tiktok_webapp_theme", "tt_ticket_guard_client_web_domain",
}

# Was einen eingeloggten Zustand ausmacht. Ein Gast-Abruf fasst davon nichts
# an — auch nicht ergänzend: ein Gast-odin_tt neben einem echten sessionid
# ist genau die Mischung, die TikTok mit 403 quittiert.
AUTH = {
    "sessionid", "sessionid_ss", "sid_tt", "sid_guard", "sid_ucp_v1",
    "ssid_ucp_v1", "uid_tt", "uid_tt_ss", "odin_tt", "cmpl_token",
    "passport_csrf_token", "passport_csrf_token_default", "multi_sids",
    "passport_auth_status", "passport_auth_status_ss",
}

# Nur diese Domains dürfen aus einem Browser-Profil in die Datei. Siehe
# Modul-Kopf: ein Profil enthält alles, was der Mensch je besucht hat.
TIKTOK_DOMAINS = ("tiktok.com", "tiktokv.com", "byteoversea.com",
                  "ttwstatic.com", "musical.ly")


# configure()-Injection statt Modul-Konstanten: der Weg nach draussen (Proxy)
# wird pro Aufruf gewaehlt — ueber die Server-IP antwortet TikTok gern mit 403,
# und ein beim Import eingefrorener Wert waere entweder leer oder veraltet.
# CLAUDE.md, "Modul-Konstanten frieren .env ein".
_KONF = {"proxy_waehler": None, "log": None}


def configure(proxy_waehler=None, log=None):
    """Vom Bot einmal beim Start gerufen. proxy_waehler ist ein Callable ohne
       Argumente, das denselben Proxy liefert wie Resolve und Pull."""
    if proxy_waehler is not None:
        _KONF["proxy_waehler"] = proxy_waehler
    if log is not None:
        _KONF["log"] = log


def _proxy(vorgabe=None):
    if vorgabe:
        return vorgabe
    waehler = _KONF["proxy_waehler"]
    if not callable(waehler):
        return None
    try:
        return waehler()
    except Exception:
        return None


def _gehoert_zu_tiktok(domain: str, domains=None) -> bool:
    d = (domain or "").lstrip(".").lower()
    return any(d == t or d.endswith("." + t) for t in (domains or TIKTOK_DOMAINS))


def hole_gastcookies(urls=None, timeout=15, proxy=None, domains=None) -> dict:
    """Holt die Anti-Bot-Cookies per HTTPS-Aufruf. Returns
       {name: (wert, domain, ablauf_unix)}. Wirft nur bei totalem Fehlschlag —
       ein einzelner nicht erreichbarer Aufruf wird geschluckt, solange der
       andere etwas liefert.

       `urls` und `domains` sind Parameter und keine Konstanten, damit der
       Vertrag den Weg gegen einen lokalen Stub fahren kann, ohne TikTok zu
       brauchen — und damit ein Spiegel-Endpunkt nachrüstbar bleibt.

       Kein aiohttp, keine Session: das hier läuft einmal alle paar Stunden
       aus einem Thread, urllib reicht und hält das Modul stdlib-only."""
    jar = CookieJar()
    handler = [urllib.request.HTTPCookieProcessor(jar)]
    if proxy:
        handler.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    opener = urllib.request.build_opener(*handler)

    kopf = dict(_TT_HEADERS)
    # Kein gzip/br: wir wollen nur die Kopfzeilen. Eine Antwort, die niemand
    # auspackt, ist der schnellste Weg zu einem Fehler ohne Erkenntnis.
    kopf["Accept-Encoding"] = "identity"
    kopf["sec-fetch-site"] = "none"

    letzter_fehler = None
    for url in (urls or GAST_URLS):
        req = urllib.request.Request(url, headers=kopf)
        try:
            with opener.open(req, timeout=timeout) as r:
                r.read(2048)          # Verbindung sauber zu Ende, Rest egal
        except Exception as e:
            letzter_fehler = e
            continue
        kopf["sec-fetch-site"] = "same-origin"

    gefunden = {}
    for c in jar:
        if not _gehoert_zu_tiktok(c.domain, domains):
            continue
        if not c.value:
            continue
        gefunden[c.name] = (c.value, c.domain or ".tiktok.com",
                            int(c.expires or 0))
    if not gefunden and letzter_fehler is not None:
        raise letzter_fehler
    return gefunden


def aus_browser(browser: str, timeout=120) -> dict:
    """Liest die TikTok-Cookies aus einem lokal installierten Browser.
       Returns dasselbe Format wie hole_gastcookies(). Wirft mit klarem Text,
       wenn weder browser_cookie3 noch yt-dlp den Weg gehen können.

       browser: chrome | chromium | firefox | edge | brave | opera | vivaldi | safari

       Der Import wird bewusst NICHT auf dem Server erwartet — dort gibt es
       kein Profil. Er ist für den Rechner gedacht, an dem der Mensch sitzt."""
    name = (browser or "").strip().lower()
    if not name:
        raise ValueError("Kein Browser angegeben")

    # Weg A: browser_cookie3, falls installiert. Kein Unterprozess, filtert
    # selbst nach Domain. Bewusst ein Import IN der Funktion — auf dem Server
    # ist das Paket nicht da, und die Modul-Ebene soll darüber nicht stolpern.
    try:
        import browser_cookie3          # noqa: PLC0415
    except ImportError:
        browser_cookie3 = None
    if browser_cookie3 is not None:
        holen = getattr(browser_cookie3, name, None)
        if holen is None:
            raise ValueError(f"browser_cookie3 kennt '{name}' nicht")
        jar = holen(domain_name="tiktok.com")
        gefunden = {c.name: (c.value, c.domain or ".tiktok.com", int(c.expires or 0))
                    for c in jar if c.value and _gehoert_zu_tiktok(c.domain)}
        if gefunden:
            return gefunden
        raise RuntimeError(f"{name}: keine TikTok-Cookies im Profil "
                           "(im Browser eingeloggt?)")

    # Weg B: yt-dlp. Liegt auf dem Bestand ohnehin oft als Recorder-Alternative.
    ytdlp = shutil.which("yt-dlp")
    if not ytdlp:
        raise RuntimeError(
            "Browser-Import nicht möglich: weder das Python-Paket "
            "'browser_cookie3' noch 'yt-dlp' ist installiert. "
            "pip install browser_cookie3 — oder Cookies über das Deck einfügen.")

    ziel = None
    try:
        import tempfile
        fd, ziel = tempfile.mkstemp(prefix="ncck", suffix=".txt")
        os.close(fd)
        os.chmod(ziel, 0o600)          # Zugangsdaten, auch für zwei Sekunden
        # --simulate: yt-dlp lädt nichts, schreibt den Cookie-Jar aber beim
        # Beenden trotzdem. Der Rückgabewert ist deshalb NICHT das Kriterium —
        # die Extraktion darf scheitern, die Cookies stehen dann trotzdem da.
        subprocess.run(
            [ytdlp, "--cookies-from-browser", name, "--cookies", ziel,
             "--simulate", "--skip-download", "--ignore-errors",
             "--no-warnings", "--ignore-config", "https://www.tiktok.com/"],
            capture_output=True, timeout=timeout, check=False)
        with open(ziel, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"yt-dlp hat nach {timeout}s nicht geantwortet "
                           "(Browser offen? Profil gesperrt?)") from e
    finally:
        if ziel:
            try:
                os.remove(ziel)
            except OSError:
                pass

    netscape, anzahl = _cookies_input_to_netscape(text)
    if anzahl <= 0:
        raise RuntimeError(f"yt-dlp lieferte keine Cookies aus '{name}' "
                           "(falsches Profil, oder der Browser läuft noch)")
    gefunden = {}
    for zeile in netscape.splitlines():
        if not zeile or zeile.startswith("#"):
            continue
        f = zeile.split("\t")
        if len(f) < 7 or not _gehoert_zu_tiktok(f[0]):
            continue
        gefunden[f[5]] = (f[6], f[0], int(f[4] or 0))
    if not gefunden:
        raise RuntimeError(f"{name}: Cookies gelesen, aber keine für TikTok")
    return gefunden


def zusammenfuehren(alt_text: str, neue: dict, gast=True):
    """Mischt frisch geholte Cookies in den vorhandenen Bestand.
       Returns (netscape_text, ergaenzt: list, ersetzt: list).

       Regel — und die ist der ganze Punkt der Funktion:
         * Gast-Abruf fasst nichts aus AUTH an, weder ersetzend noch ergänzend.
         * Ein Wert wird nur ersetzt, wenn er sich wirklich unterscheidet.
         * Alles, was schon da ist und nicht neu kommt, bleibt unverändert —
           auch Cookies, die wir nicht kennen."""
    text, _ = _cookies_input_to_netscape(alt_text or "")
    zeilen = text.splitlines()

    ergaenzt, ersetzt = [], []
    vorhanden = {}                     # name -> index in zeilen
    for i, z in enumerate(zeilen):
        if not z or z.startswith("#"):
            continue
        f = z.split("\t")
        if len(f) >= 7:
            vorhanden.setdefault(f[5], i)

    for name, (wert, domain, ablauf) in sorted(neue.items()):
        if gast and name in AUTH:
            continue
        i = vorhanden.get(name)
        if i is None:
            zeile = "\t".join([domain, "TRUE" if domain.startswith(".") else "FALSE",
                               "/", "TRUE", str(int(ablauf or 0)), name, wert])
            zeilen.append(zeile)
            ergaenzt.append(name)
            continue
        f = zeilen[i].split("\t")
        if f[6] == wert:
            continue
        f[6] = wert
        if ablauf and int(ablauf) > int(f[4] or 0):
            f[4] = str(int(ablauf))    # Ablauf mitziehen, sonst altert der Wert
        zeilen[i] = "\t".join(f)
        ersetzt.append(name)

    fertig, _ = _dedupe_cookie_text("\n".join(zeilen) + "\n")
    return fertig, ergaenzt, ersetzt


def schreibe(datei: str, netscape_text: str, auth_pflicht=False):
    """Schreibt die cookies.txt — validiert, mit Backup, atomar.
       Returns (anzahl, backup_angelegt). Wirft, wenn das Ergebnis nicht
       ladbar wäre oder ein verlangtes Auth-Cookie fehlt.

       Reihenfolge ist Absicht: erst .tmp schreiben und LADEN, dann sichern,
       dann tauschen. Wer zuerst tauscht und danach prüft, hat im Fehlerfall
       schon den funktionierenden Bestand überschrieben."""
    tmp = datei + ".neu.tmp"
    fd = os.open(tmp, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(netscape_text)
        cj = MozillaCookieJar(tmp)
        cj.load(ignore_discard=True, ignore_expires=True)
        namen = {c.name for c in cj}
        if auth_pflicht and not (namen & {"sessionid_ss", "sessionid"}):
            raise RuntimeError("kein Auth-Cookie (sessionid_ss/sessionid) dabei")
        with DATEI_SPERRE:
            backup = False
            if os.path.exists(datei):
                try:
                    shutil.copy2(datei, datei + ".bak")
                    backup = True
                except OSError:
                    pass
            os.replace(tmp, datei)
            tmp = None
        return len(namen), backup
    finally:
        if tmp:
            try:
                os.remove(tmp)
            except OSError:
                pass


def aktualisiere(datei: str, quelle="gast", browser=None, timeout=15,
                 proxy=None, log=None) -> dict:
    """Der eine Aufruf, den Bot, Deck und Telegram-Befehl teilen.

       quelle: 'gast'    — Anti-Bot-Tokens per HTTPS holen (kein Login nötig)
               'browser' — komplettes TikTok-Profil aus einem Browser lesen

       proxy=None heißt NICHT "direkt", sondern "nimm den konfigurierten
       Weg" (siehe configure). Direkt geht es nur, wenn auch kein Wähler
       hinterlegt ist.

       Returns einen Bericht, der auch im Fehlerfall vollständig ist —
       ok=False plus 'error'. Wirft nicht: die Aufrufer sind eine Route, ein
       Telegram-Befehl und eine Dauerschleife; keiner davon soll an einem
       nicht erreichbaren TikTok sterben."""
    log = log or _KONF["log"]
    bericht = {"ok": False, "source": quelle, "browser": browser,
               "fetched": 0, "added": [], "replaced": [], "total": 0,
               "auth_cookie": False, "backed_up": False, "error": None,
               "ts": int(_time.time())}
    try:
        if quelle == "browser":
            neue = aus_browser(browser or "chrome", timeout=max(timeout, 60))
            gast = False
        else:
            neue = hole_gastcookies(timeout=timeout, proxy=_proxy(proxy))
            gast = True
        bericht["fetched"] = len(neue)
        if not neue:
            bericht["error"] = "TikTok hat keine Cookies gesetzt"
            return bericht

        alt = ""
        if os.path.exists(datei):
            with open(datei, "r", encoding="utf-8", errors="replace") as f:
                alt = f.read()
        text, ergaenzt, ersetzt = zusammenfuehren(alt, neue, gast=gast)
        bericht["added"], bericht["replaced"] = ergaenzt, ersetzt

        if not ergaenzt and not ersetzt:
            # Nichts geändert: NICHT schreiben. Ein Schreibvorgang ohne
            # Änderung setzt die mtime — und damit meldet das Deck
            # "Cookies frisch", während in Wahrheit alles beim Alten ist.
            bericht["ok"] = True
            bericht["total"] = sum(1 for z in text.splitlines()
                                   if z and not z.startswith("#"))
            bericht["auth_cookie"] = ("\tsessionid_ss\t" in text
                                      or "\tsessionid\t" in text)
            return bericht

        anzahl, backup = schreibe(datei, text, auth_pflicht=(quelle == "browser"))
        bericht.update(ok=True, total=anzahl, backed_up=backup)
        bericht["auth_cookie"] = ("\tsessionid_ss\t" in text
                                  or "\tsessionid\t" in text)
        if log:
            log.warning("Cookies automatisch bezogen (%s): %d neu, %d erneuert, "
                        "%d in der Datei", quelle, len(ergaenzt), len(ersetzt), anzahl)
    except Exception as e:
        bericht["error"] = str(e) or e.__class__.__name__
        if log:
            log.warning("Cookie-Auto-Bezug (%s) fehlgeschlagen: %s", quelle, e)
    return bericht
