"""nc.overlaybrowser — v4.2-W170: EIN Chromium je Restream statt einer je Bild.

Gemeldet am 07.11.: „durch die hohe CPU-Last bricht der ganze Stream
zusammen." Der HTML-Overlay-Modus (Vorgabe seit W160) startete fuer JEDES
Overlay-Bild einen frischen Chromium — `--headless=new --screenshot=…`, also
Kaltstart, Seitenaufbau, `--virtual-time-budget=2500`, Ende. Bei 1 Bild/s je
Restream. Nachgemessen (Chrome 14x, 1080x1920):

    Kaltstart je Bild          0,86 CPU-s   (0,76 s Wanduhr)
    dauerhafter Browser        0,08 CPU-s   (inkl. der laufenden Seite)

Ein Kaltstart je Sekunde ist damit fast ein ganzer Kern je Restream, und er
kommt in Spitzen: ein Dutzend Prozesse (Zygote, Renderer, Netz) auf nice 0,
gleichrangig mit dem Transcode. Der faellt dabei unter Echtzeit, liest die
Quelle zu langsam, das CDN verwirft Pakete — die Kette aus W108
(nc/lastvorsorge.py), nur mit einer Ursache, die keine Drosselstufe trifft:
die Drossel senkt die Encoder-Last, der Chromium bleibt.

Hier bleibt der Browser offen und wird ueber `--remote-debugging-pipe`
gesteuert (fd 3/4, NUL-getrennte JSON-Nachrichten, das DevTools-Protokoll).
Das braucht kein Fremdpaket und keinen offenen Port — ein Debug-Port auf
localhost waere fuer jeden lokalen Prozess eine Fernsteuerung des Browsers.

Nebenbei zeigt das Overlay jetzt, was es zeigen soll: `templates/overlay.html`
pollt selbst alle 2,5 s und blendet Sprechblasen und Alerts mit Timern ein.
Eine je Bild frisch geladene Seite hat davon nie etwas erlebt.

Bot-frei und stdlib-only. Synchron gebaut, der Bot ruft `schuss()` per
`asyncio.to_thread` — ein Lesen auf der Pipe darf den Event-Loop nicht halten.
"""

import base64
import fcntl
import json
import logging
import os
import select
import signal
import shutil
import subprocess
import threading
import time

log = logging.getLogger("nc.overlaybrowser")


class OverlayBrowserFehler(RuntimeError):
    """Browser nicht startbar, gestorben oder ohne Antwort."""


# Nach einem Absturz nicht in jedem Takt neu starten: ein Chromium, der beim
# Start stirbt, waere sonst genau der Kaltstart je Bild, den dieses Modul
# abschafft — nur mit Fehlermeldung.
NEUSTART_RUHE_S = 30.0


def _groesse(text):
    """`B,H` wie von nc.restream_util.fenstergroesse geliefert. Kein stiller
    Rueckfall auf eine Vorgabe: ein Overlay in falscher Groesse liegt verzerrt
    oder abgeschnitten im Sendebild — lieber ein Fehler, der den Einzelschuss
    waehlt und das im Log sagt."""
    teile = str(text).split(",")
    if len(teile) != 2 or not all(t.strip().isdigit() for t in teile):
        raise OverlayBrowserFehler("Fenstergroesse %r ist nicht B,H" % (text,))
    return int(teile[0]), int(teile[1])


def browser_cmd(binpath, nice=None):
    """Kommandozeile des dauerhaften Browsers. Seite und Groesse kommen erst
    ueber das Protokoll — auf der Kommandozeile steht nichts aus der .env."""
    cmd = [binpath, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--hide-scrollbars", "--mute-audio", "--no-first-run",
           "--disable-background-networking", "--disable-extensions",
           "--remote-debugging-pipe", "about:blank"]
    # Das Overlay ist Teil des Sendebilds, aber ein verspaetetes Overlay-Bild
    # wiederholt nur das letzte — ein verspaeteter Transcode verliert die
    # Quelle. Deshalb tritt der Browser zurueck.
    if nice and int(nice) > 0 and shutil.which("nice"):
        cmd[0:0] = ["nice", "-n", str(int(nice))]
    return cmd


def teilen() -> bool:
    """OVERLAY_BROWSER_TEILEN (Vorgabe 1): ein Chromium fuer alle Restreams.

    v5.2-W193. Gemessen (Chromium 14x, headless): ein Dauerbrowser belegt rund
    400 MB PSS in 14 Prozessen — je Restream. Ein weiterer Tab im selben
    Browser braucht nur einen weiteren Renderer. 0 = ein Browser je Restream
    wie bis W192 (Rueckweg, falls ein Tab den anderen stoert). Als Funktion
    gelesen, nicht als Konstante."""
    return os.getenv("OVERLAY_BROWSER_TEILEN", "1").strip().lower() not in (
        "0", "false", "nein", "no", "aus", "off")


def _gruppe_lebend(pgid):
    """PIDs der Prozessgruppe, die noch leben (Zombies zaehlen nicht — eine
    verwaiste Leiche raeumt init ab, sie belegt weder CPU noch Speicher).
    Ohne /proc (kein Linux): [] — dann gibt es nichts nachzusehen."""
    if not os.path.isdir("/proc"):
        return []
    lebend = []
    for d in (e for e in os.listdir("/proc") if e.isdigit()):
        try:
            with open("/proc/%s/stat" % d, "rb") as f:
                felder = f.read().rsplit(b")", 1)[1].split()
        except (OSError, IndexError):
            continue   # Prozess zwischen listdir und open beendet: genau das Ziel
        if int(felder[3]) == pgid and felder[0] != b"Z":
            lebend.append(d)
    return lebend


class _Verbindung:
    """Ein Chromium-Prozess und seine Steuer-Pipe. Mehrere Tabs teilen sie;
    jeder Aufruf laeuft unter `sperre` (RLock), Antworten kommen nach id."""

    def __init__(self, binpath, nice=None):
        self.binpath = binpath
        self.nice = nice
        self._proc = None
        self._w = self._r = None
        self._puffer = b""
        self._id = 0
        self.sperre = threading.RLock()
        self.generation = 0          # zaehlt Starts: ein Tab erkennt daran den Neustart
        self.letzter_start = 0.0
        self.tabs = set()

    def lebt(self):
        return self._proc is not None and self._proc.poll() is None

    def starten(self):
        self.beenden()
        self.letzter_start = time.monotonic()
        r_zu, w_zu = os.pipe()     # wir -> Chromium (dort fd 3)
        r_von, w_von = os.pipe()   # Chromium -> wir (dort fd 4)

        def _fds():
            # Nach dem fork, vor dem exec: die Pipe-Enden auf 3 und 4 legen.
            # Erst wegkopieren — liegt r_zu zufaellig schon auf 4, wuerde das
            # zweite dup2 es ueberschreiben.
            a = fcntl.fcntl(r_zu, fcntl.F_DUPFD, 10)
            b = fcntl.fcntl(w_von, fcntl.F_DUPFD, 10)
            os.dup2(a, 3)
            os.dup2(b, 4)

        try:
            # Eigene Prozessgruppe: beenden() trifft mit killpg auch Zygote
            # und Renderer, die sonst als Waisen weiterliefen.
            self._proc = subprocess.Popen(
                browser_cmd(self.binpath, self.nice), pass_fds=(r_zu, w_von, 3, 4),
                preexec_fn=_fds, start_new_session=True,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except OSError as e:
            for fd in (r_zu, w_zu, r_von, w_von):
                os.close(fd)
            raise OverlayBrowserFehler("Chromium nicht startbar: %s" % e) from e
        os.close(r_zu)
        os.close(w_von)
        self._w, self._r = w_zu, r_von
        self._puffer = b""
        self.generation += 1

    def beenden(self):
        p, self._proc = self._proc, None
        for fd in (self._w, self._r):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass   # Aufraeumen: schon zu ist so gut wie zu
        self._w = self._r = None
        if p is None:
            return
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass       # Aufraeumen: Gruppe schon weg
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log.warning("Overlay-Browser: pid %s nach SIGKILL nicht beendet "
                            "— bleibt als Zombie, bis er endet.", p.pid)
        # v5.3.1: SIGKILL an die Gruppe ist zugestellt, nicht vollzogen. Zygote
        # und Renderer sind nicht unsere Kinder, p.wait() wartet nur auf den
        # Hauptprozess — in der CI stand ein Helfer danach noch in /proc
        # (W170-Vertrag, 1 von 4 Laeufen). Kurz warten, bis die Gruppe leer ist.
        frist = time.monotonic() + 2.0
        rest = _gruppe_lebend(p.pid)
        while rest and time.monotonic() < frist:
            time.sleep(0.01)
            rest = _gruppe_lebend(p.pid)
        if rest:
            log.warning("Overlay-Browser: %d Prozess(e) der Gruppe %s leben 2 s nach "
                        "SIGKILL noch (%s) — haengen vermutlich im Kernel (Platte/NFS).",
                        len(rest), p.pid, ",".join(rest[:5]))

    def aufruf(self, methode, params, frist, sitzung=None):
        if self._w is None:
            raise OverlayBrowserFehler("Browser nicht gestartet")
        self._id += 1
        nachricht = {"id": self._id, "method": methode, "params": params}
        # Target.* geht an den Browser selbst, alles andere an die Seite.
        if sitzung and not methode.startswith("Target."):
            nachricht["sessionId"] = sitzung
        try:
            os.write(self._w, json.dumps(nachricht).encode() + b"\0")
        except OSError as e:
            raise OverlayBrowserFehler("%s: Pipe zu (%s)" % (methode, e)) from e
        while True:
            while b"\0" not in self._puffer:
                rest = frist - time.monotonic()
                if rest <= 0:
                    raise OverlayBrowserFehler("%s: keine Antwort" % methode)
                bereit, _, _ = select.select([self._r], [], [], rest)
                if not bereit:
                    continue
                stueck = os.read(self._r, 1 << 20)
                if not stueck:
                    raise OverlayBrowserFehler("%s: Chromium beendet" % methode)
                self._puffer += stueck
            roh, self._puffer = self._puffer.split(b"\0", 1)
            antwort = json.loads(roh)
            if antwort.get("id") != self._id:
                continue            # Ereignis oder Antwort eines anderen Tabs
            if "error" in antwort:
                raise OverlayBrowserFehler("%s: %s" % (
                    methode, antwort["error"].get("message", antwort["error"])))
            return antwort.get("result") or {}


VERSUCH_S = 3.0                   # je Ladeversuch (v5.6-W197), nicht je Start
_GETEILT = {}                     # (binpath, nice) -> _Verbindung
_GETEILT_SPERRE = threading.Lock()


def _verbindung_fuer(binpath, nice):
    """Die geteilte Verbindung fuer diesen Browser — oder eine eigene."""
    if not teilen():
        return _Verbindung(binpath, nice)
    with _GETEILT_SPERRE:
        v = _GETEILT.get((binpath, nice))
        if v is None:
            v = _GETEILT[(binpath, nice)] = _Verbindung(binpath, nice)
        return v


def lage() -> dict:
    """Fuer /healthz: wie viele Browser fuer wie viele Tabs laufen."""
    with _GETEILT_SPERRE:
        vs = list(_GETEILT.values())
    return {"teilen": teilen(), "browser": sum(1 for v in vs if v.lebt()),
            "tabs": sum(len(v.tabs) for v in vs)}


class Dauerbrowser:
    """Ein Overlay-Tab in einem headless Chromium, aus dem Bilder geholt werden.

    v5.2-W193: der Chromium dahinter ist geteilt (teilen()); dieser Tab hat
    seine eigene Seite, Groesse und Sitzung. Die oeffentliche Schnittstelle ist
    dieselbe wie bis W192 — starten(), schuss(), beenden(), lebt(), starts."""

    def __init__(self, binpath, url, groesse, nice=None):
        self.binpath = binpath
        self.url = url
        self.groesse = groesse
        self.nice = nice
        self._v = None
        self._ziel = None
        self._sitzung = None
        self._gen = -1
        self.starts = 0

    @property
    def _proc(self):
        """Der Chromium-Prozess hinter diesem Tab (fuer Diagnose und Vertrag)."""
        return self._v._proc if self._v is not None else None

    def _verbindung(self):
        if self._v is None:
            self._v = _verbindung_fuer(self.binpath, self.nice)
        return self._v

    def lebt(self):
        v = self._v
        return (v is not None and v.lebt() and self._sitzung is not None
                and self._gen == v.generation)

    def starten(self, timeout=20.0):
        v = self._verbindung()
        with v.sperre:
            self._starten(timeout)

    def _starten(self, timeout):
        v = self._verbindung()
        breite, hoehe = _groesse(self.groesse)
        frist = time.monotonic() + timeout
        if not v.lebt():
            v.starten()
        v.tabs.add(self)
        self._sitzung = None
        self.starts += 1
        ziel = v.aufruf("Target.createTarget", {"url": "about:blank"},
                        frist=frist)["targetId"]
        self._ziel = ziel
        sitzung = v.aufruf("Target.attachToTarget", {"targetId": ziel, "flatten": True},
                           frist=frist)["sessionId"]
        # Transparenter Hintergrund: ohne das deckt das Overlay-Bild das
        # Quellbild weiss ab.
        v.aufruf("Emulation.setDefaultBackgroundColorOverride",
                 {"color": {"r": 0, "g": 0, "b": 0, "a": 0}}, frist=frist, sitzung=sitzung)
        v.aufruf("Emulation.setDeviceMetricsOverride",
                 {"width": breite, "height": hoehe,
                  "deviceScaleFactor": 1, "mobile": False}, frist=frist, sitzung=sitzung)
        v.aufruf("Page.navigate", {"url": self.url}, frist=frist, sitzung=sitzung)
        self._warten_bis_geladen(v, sitzung, frist)
        self._sitzung = sitzung
        self._gen = v.generation

    def _warten_bis_geladen(self, v, sitzung, frist):
        letzter = None
        while time.monotonic() < frist:
            try:
                # v5.6-W197: jeder Versuch mit EIGENER kurzer Frist. Bis hierher
                # bekam er die ganze Startfrist — antwortete Chromium auf einen
                # Versuch nicht (Ausfuehrungskontext waehrend der Navigation
                # neu, Maschine unter Last bei nice 12), frass dieser eine die
                # 30 s, und ein zweiter Versuch fand nie statt: „Seite nicht
                # geladen: Runtime.evaluate: keine Antwort" (W170-Vertrag in
                # der CI, 3.14). Eine verspaetete Antwort auf den alten Versuch
                # verwirft aufruf() an der id.
                erg = v.aufruf("Runtime.evaluate",
                               {"expression": "document.readyState",
                                "returnByValue": True},
                               frist=min(frist, time.monotonic() + VERSUCH_S),
                               sitzung=sitzung)
                if (erg.get("result") or {}).get("value") == "complete":
                    return
            except OverlayBrowserFehler as e:
                if not v.lebt():
                    raise
                letzter = e
            time.sleep(0.1)
        raise OverlayBrowserFehler("Seite nicht geladen: %s" % (letzter or self.url))

    def beenden(self):
        """Den Tab schliessen; war er der letzte, den ganzen Browser."""
        v = self._v
        if v is None:
            return
        with v.sperre:
            v.tabs.discard(self)
            if self._ziel and v.lebt() and v.tabs and self._gen == v.generation:
                try:
                    v.aufruf("Target.closeTarget", {"targetId": self._ziel},
                             frist=time.monotonic() + 5)
                except OverlayBrowserFehler as e:
                    log.warning("Overlay-Browser: Tab liess sich nicht schliessen (%s) "
                                "— er belegt Speicher bis zum naechsten Neustart.", e)
            self._ziel = self._sitzung = None
            if not v.tabs:
                v.beenden()

    def schuss(self, timeout=15.0):
        """PNG-Bytes des aktuellen Overlays. Startet einen gestorbenen Browser
        neu, aber hoechstens alle NEUSTART_RUHE_S. Wirft OverlayBrowserFehler."""
        v = self._verbindung()
        with v.sperre:
            if not self.lebt():
                if not v.lebt():
                    rest = NEUSTART_RUHE_S - (time.monotonic() - v.letzter_start)
                    if self.starts and rest > 0:
                        raise OverlayBrowserFehler(
                            "Chromium gestorben (rc %s), Neustart in %.0f s"
                            % (v._proc.returncode if v._proc else "?", rest))
                self._starten(timeout)
            try:
                erg = v.aufruf("Page.captureScreenshot", {"format": "png"},
                               frist=time.monotonic() + timeout, sitzung=self._sitzung)
            except OverlayBrowserFehler:
                # Ein haengender Browser haengt fuer alle Tabs — beenden, sonst
                # wartet jeder Takt jedes Restreams wieder 15 s auf nichts.
                v.beenden()
                raise
            return base64.b64decode(erg.get("data") or "")
