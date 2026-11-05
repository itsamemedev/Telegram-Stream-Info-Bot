"""nc.quellprobe — v4.2-W141: welcher Weg bringt fuer @nutzer eine Adresse,
die ffmpeg wirklich ziehen kann?

Der Betreiber am 05.11.: „7 User live keiner wird restreamt weil angeblich
keine flv oder hls streams empfangen werden können." Das „angeblich" ist die
eigentliche Frage. Der Bot sieht nur das Ergebnis seiner eigenen Kette und
sagt „weder FLV noch HLS"; ob TikTok der Server-IP gar nichts gibt, ob eine
andere Form (CMAF/DASH/MP4) dabei ist oder ob die Adresse zwar kommt, beim
Abruf aber 403 antwortet, sind drei verschiedene Lagen mit drei
verschiedenen Abhilfen. CLAUDE.md: „Erst gegen den Server messen, dann
einbauen."

Gemessen wird auf dem SERVER, weil dort die IP und der Proxy sind, durch die
auch der Bot geht — seit v4.2-W142 auch per Telegram/Discord (`/quelle name`,
der Kern liegt deshalb hier in nc/ und nicht mehr in tools/):

    venv/bin/python tools/quellprobe.py nutzername
    venv/bin/python tools/quellprobe.py nutzername --ohne-proxy
    venv/bin/python tools/quellprobe.py nutzername --json

Vier Proben, jede fuer sich:
  1. yt-dlp --dump-single-json: ALLE Formate mit Protokoll, Container, Codec
     und Restlaufzeit — auch die, die der Bot bis W141 verwarf.
  2. Die Live-Seite selbst (HTML): die eingebetteten Stream-Adressen, gelesen
     mit derselben Auswahl wie der Bot (nc.streamsel).
  3. ffprobe auf jede gefundene Adresse: antwortet sie mit Bild und Ton?
  4. yt-dlp als Durchreicher (`-o -`): kommen Bytes an, auch wenn keine
     Adresse direkt ziehbar ist? Dann waere ein yt-dlp-Zubringer der Weg.

Es wird nichts gesendet, nichts aufgenommen und nichts in die Datenbank
geschrieben. Cookies und Proxy-Zugangsdaten erscheinen nie in der Ausgabe;
CDN-Adressen werden auf Host und Laufzeit gekuerzt.
"""
import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import time
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# v4.2-W142: seit die Probe aus dem Bot laeuft (/quelle), gehoert jeder
# Fehlschlag auch ins Log — in der Ausgabe allein waere er nach dem Lesen weg.
log = logging.getLogger("TikTokBot")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
_ZUGANG = re.compile(r"(?<=//)[^/@\s]+@|^[^/@\s:]+:[^/@\s]+@")


def maske(proxy):
    """Zugangsdaten aus einer Proxy-Adresse entfernen — auch schemalos
    (nutzer:pass@host), dieselbe Lehre wie nc/proxyutil in W105."""
    return _ZUGANG.sub("***@", proxy or "") if proxy else ""


def ttl(url, jetzt=None):
    """Restsekunden aus expire=/x-expires= der Adresse, sonst None."""
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(url or "").query)
    werte = [(q.get(k) or [""])[0] for k in ("expire", "x-expires", "expires")]
    ziffern = [v for v in werte if v.isdigit()]
    return (int(ziffern[0]) - int(jetzt if jetzt is not None else time.time())
            if ziffern else None)


def kurz(url):
    """Host + Dateiendung + Restlaufzeit — genug zum Zuordnen, nichts Signiertes."""
    t = urllib.parse.urlsplit(url or "")
    pfad = t.path.rsplit("/", 1)[-1]
    endung = pfad.rsplit(".", 1)[-1] if "." in pfad else "?"
    rest = ttl(url)
    return "%s …%s%s" % (t.netloc, endung,
                         "" if rest is None else " (läuft in %ss ab)" % rest)


def form(url, protokoll="", ext=""):
    """flv | hls | dash | cmaf | mp4 | andere — dieselbe Einteilung wie der Bot."""
    from nc import ytdlpurl
    if ytdlpurl._ist_flv(url, protokoll, ext):
        return "flv"
    if ytdlpurl._ist_hls(url, protokoll, ext):
        return "hls"
    return ytdlpurl._andere_art(url, protokoll, ext) or "andere"


def empfehlung(befunde):
    """Ein Satz, was zu tun ist — aus den Ergebnissen, nicht geraten.

    `befunde`: {"kandidaten": [{"form", "ffprobe_ok"}…], "durchreicher_bytes": n,
                "ytdlp_fehler": str|None, "html_fehler": str|None}"""
    kand = befunde.get("kandidaten") or []
    gut = [k for k in kand if k.get("ffprobe_ok")]
    if any(k["form"] in ("flv", "hls") for k in gut):
        return ("Eine FLV/HLS-Adresse ist ziehbar. Bekommt der Bot sie trotzdem "
                "nicht, liegt es am Zeitpunkt oder am Cache — den Restream im "
                "Deck neu starten und das Log auf 'live-ohne-URL' ansehen.")
    if gut:
        return ("Nur die dritte Form (%s) ist ziehbar. Seit W141 nimmt der Bot "
                "sie als letzte Quelle — ein Update genügt."
                % ", ".join(sorted({k["form"] for k in gut})))
    if befunde.get("durchreicher_bytes", 0) > 0:
        return ("Keine Adresse ist direkt ziehbar, aber yt-dlp reicht den Stream "
                "durch. Damit ist ein yt-dlp-Zubringer für den Restream der Weg "
                "— das ist die nächste Welle; bitte diese Ausgabe mitschicken.")
    if kand:
        return ("Adressen kommen, aber keine antwortet ffprobe (meist 403 für die "
                "Server-IP). Abhilfe: RECORD_PROXY auf einen Residential-/Mobil-"
                "Proxy, oder den Tunnel einschalten — dann mit Proxy erneut messen.")
    return ("Kein Weg liefert eine Adresse. Ist der Nutzer wirklich live? Wenn ja: "
            "TikTok gibt dieser IP nichts heraus — Proxy/Tunnel, und Cookies "
            "erneuern (Deck → Cookies → Abrufen).")


def _env():
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(WURZEL, ".env"))
    except ImportError:
        print("Hinweis: python-dotenv fehlt — es zählt nur die Umgebung.")
    cookies = os.path.join(WURZEL, "tiktok_cookies.txt")
    return (os.getenv("RECORD_PROXY") or "").strip(), (cookies if os.path.isfile(cookies) else None)


def probe_ytdlp(nutzer, proxy, cookies):
    exe = shutil.which("yt-dlp") or shutil.which("yt_dlp")
    if not exe:
        return [], "yt-dlp nicht installiert"
    cmd = [exe, "--no-warnings", "--no-playlist", "--dump-single-json",
           "--socket-timeout", "10", "--user-agent", UA,
           "--referer", "https://www.tiktok.com/"]
    if proxy:
        cmd += ["--proxy", proxy]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append("https://www.tiktok.com/@%s/live" % nutzer)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    except subprocess.TimeoutExpired:
        log.info("Quellprobe @%s: yt-dlp nach 40 s abgebrochen", nutzer)
        return [], "Zeitüberschreitung nach 40 s"
    if r.returncode != 0 or not r.stdout.strip().startswith("{"):
        letzte = (r.stderr.strip().splitlines() or ["(keine Ausgabe)"])[-1]
        return [], maske(letzte)[:200]
    data = json.loads(r.stdout)
    aus = []
    for f in data.get("formats") or []:
        u = f.get("url") or f.get("manifest_url")
        if u:
            aus.append({"weg": "yt-dlp", "id": f.get("format_id"),
                        "form": form(u, f.get("protocol") or "", f.get("ext") or ""),
                        "vcodec": f.get("vcodec"), "url": u})
    return aus, None


def probe_html(nutzer, proxy):
    from nc import streamsel
    req = urllib.request.Request("https://www.tiktok.com/@%s/live" % nutzer,
                                 headers={"User-Agent": UA,
                                          "Accept-Language": "de-DE,de;q=0.9"})
    handler = []
    if proxy and proxy.startswith("http"):
        handler.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    elif proxy:
        return [], "SOCKS-Proxy — der HTML-Abruf hier kann nur HTTP-Proxys (yt-dlp oben schon)"
    try:
        html = urllib.request.build_opener(*handler).open(req, timeout=20).read().decode(
            "utf-8", "ignore")
    except Exception as e:
        grund = "%s: %s" % (type(e).__name__, maske(str(e))[:160])
        log.info("Quellprobe @%s: Live-Seite nicht abrufbar (%s)", nutzer, grund)
        return [], grund
    aus = []
    for m in re.finditer(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.S):
        try:
            obj = json.loads(m.group(1))
        except ValueError as e:
            # Nicht jedes application/json-Skript ist JSON im strengen Sinn;
            # eins zu ueberspringen ist richtig, still bleibt es trotzdem nicht.
            log.debug("Quellprobe @%s: Skriptblock kein JSON (%s)", nutzer, e)
            continue
        treffer = streamsel.find_stream_urls(obj) or {}
        for k in ("flv_url", "hls_url", "other_url"):
            if treffer.get(k):
                aus.append({"weg": "html", "id": k, "form": form(treffer[k]),
                            "vcodec": treffer.get("vcodec"), "url": treffer[k]})
    if not aus and "captcha" in html.lower():
        return [], "TikTok zeigt eine Prüfseite (Captcha) statt der Live-Seite"
    return aus, (None if aus else "keine Stream-Adresse im HTML")


def probe_ffprobe(url, proxy):
    exe = shutil.which("ffprobe")
    if not exe:
        return False, "ffprobe nicht installiert"
    cmd = [exe, "-v", "error", "-rw_timeout", "15000000", "-user_agent", UA,
           "-headers", "Referer: https://www.tiktok.com/\r\n"]
    if proxy and proxy.startswith("http"):
        cmd += ["-http_proxy", proxy]
    cmd += ["-show_entries", "stream=codec_type,codec_name", "-of", "json", url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        log.info("Quellprobe: ffprobe nach 30 s abgebrochen (%s)", kurz(url))
        return False, "Zeitüberschreitung"
    if r.returncode == 0:
        arten = sorted("%s=%s" % (s.get("codec_type"), s.get("codec_name"))
                       for s in json.loads(r.stdout or "{}").get("streams", []))
        return bool(arten), ", ".join(arten) or "keine Spuren"
    return False, maske((r.stderr.strip().splitlines() or ["?"])[-1])[:160]


def probe_durchreicher(nutzer, proxy, cookies, grenze=2_000_000, frist=25):
    """Wie viele Bytes reicht `yt-dlp -o -` in `frist` Sekunden durch?"""
    exe = shutil.which("yt-dlp") or shutil.which("yt_dlp")
    if not exe:
        log.info("Quellprobe @%s: kein yt-dlp — Durchreicher nicht prüfbar", nutzer)
        return 0
    cmd = [exe, "-q", "--no-warnings", "-o", "-", "--user-agent", UA]
    if proxy:
        cmd += ["--proxy", proxy]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append("https://www.tiktok.com/@%s/live" % nutzer)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n, ende = 0, time.time() + frist
    try:
        os.set_blocking(p.stdout.fileno(), False)
        while time.time() < ende and n < grenze and p.poll() is None:
            stueck = p.stdout.read(65536)
            if stueck:
                n += len(stueck)
            else:
                time.sleep(0.2)
    finally:
        p.kill()
        p.wait(timeout=10)
    return n


def messen(nutzer, proxy, cookies, ausgabe=print):
    """Alle vier Proben; jede Zeile geht an `ausgabe`. Rueckgabe: die Befunde
    samt "empfehlung". Blockiert bis rund zwei Minuten — der Bot ruft es
    deshalb in einem Thread (asyncio.to_thread), nie auf dem Loop."""
    ausgabe("Quellprobe @%s · Proxy: %s · Cookies: %s"
            % (nutzer, maske(proxy) or "keiner", "ja" if cookies else "nein"))
    yt, yt_fehler = probe_ytdlp(nutzer, proxy, cookies)
    ausgabe("1) yt-dlp: %d Formate%s" % (len(yt), "" if not yt_fehler else " — " + yt_fehler))
    ht, ht_fehler = probe_html(nutzer, proxy)
    ausgabe("2) HTML:   %d Adressen%s" % (len(ht), "" if not ht_fehler else " — " + ht_fehler))
    kandidaten = (yt + ht)[:12]
    ausgabe("3) ffprobe je Adresse:")
    for k in kandidaten:
        k["ffprobe_ok"], k["ffprobe"] = probe_ffprobe(k["url"], proxy)
        ausgabe("   %-6s %-5s %-8s %s  →  %s %s" % (
            k["weg"], k["form"], (k.get("vcodec") or "")[:8], kurz(k["url"]),
            "OK" if k["ffprobe_ok"] else "FEHLER", k["ffprobe"]))
        k["url"] = kurz(k["url"])       # ab hier nichts Signiertes mehr im Ergebnis
    if not kandidaten:
        ausgabe("   (keine Adresse zu prüfen)")
    n = probe_durchreicher(nutzer, proxy, cookies)
    ausgabe("4) yt-dlp als Durchreicher (25 s): %d Bytes" % n)
    befunde = {"kandidaten": kandidaten, "durchreicher_bytes": n,
               "ytdlp_fehler": yt_fehler, "html_fehler": ht_fehler}
    befunde["empfehlung"] = empfehlung(befunde)
    ausgabe("EMPFEHLUNG: " + befunde["empfehlung"])
    return befunde


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("nutzer")
    ap.add_argument("--ohne-proxy", action="store_true", help="RECORD_PROXY ignorieren")
    ap.add_argument("--json", action="store_true", help="maschinenlesbar")
    a = ap.parse_args(argv)
    proxy, cookies = _env()
    befunde = messen(a.nutzer.lstrip("@").strip(), "" if a.ohne_proxy else proxy, cookies)
    if a.json:
        print(json.dumps(befunde, ensure_ascii=False, indent=2))
    return 0
