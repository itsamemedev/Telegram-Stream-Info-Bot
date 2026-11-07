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
import os
import select
import signal
import shutil
import subprocess
import threading
import time


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


class Dauerbrowser:
    """Ein headless Chromium mit EINER Seite, aus der Bilder geholt werden."""

    def __init__(self, binpath, url, groesse, nice=None):
        self.binpath = binpath
        self.url = url
        self.groesse = groesse
        self.nice = nice
        self._proc = None
        self._w = self._r = None
        self._puffer = b""
        self._id = 0
        self._sitzung = None
        self._sperre = threading.Lock()
        self._letzter_start = 0.0
        self.starts = 0

    # ── Lebenszyklus ──────────────────────────────────────────────────
    def lebt(self):
        return self._proc is not None and self._proc.poll() is None

    def starten(self, timeout=20.0):
        with self._sperre:
            self._starten(timeout)

    def _starten(self, timeout):
        self._beenden()
        self._letzter_start = time.monotonic()
        breite, hoehe = _groesse(self.groesse)
        r_zu, w_zu = os.pipe()     # wir -> Chromium (dort fd 3)
        r_von, w_von = os.pipe()   # Chromium -> wir (dort fd 4)

        def _fds():
            # Erst weit nach oben kopieren, dann auf 3/4 legen: die Pipes
            # koennen selbst auf 3 oder 4 liegen, wenn der Bot dort nichts
            # offen hat, und ein direktes dup2(r_zu, 3) ueberschriebe dann
            # ein w_von, das zufaellig auf 3 liegt.
            a = fcntl.fcntl(r_zu, fcntl.F_DUPFD, 10)
            b = fcntl.fcntl(w_von, fcntl.F_DUPFD, 10)
            os.dup2(a, 3)
            os.dup2(b, 4)

        try:
            # start_new_session: Chromium forkt Zygote und Renderer. Beim
            # Beenden geht das Signal an die ganze Gruppe — sonst bleiben
            # Renderer als Waisen liegen und rechnen weiter.
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
        self.starts += 1
        frist = time.monotonic() + timeout
        ziel = self._aufruf("Target.createTarget", {"url": "about:blank"},
                            frist=frist)["targetId"]
        self._sitzung = self._aufruf(
            "Target.attachToTarget", {"targetId": ziel, "flatten": True},
            frist=frist)["sessionId"]
        # Transparenter Hintergrund — dasselbe wie
        # --default-background-color=00000000 beim Einzelschuss; ohne das
        # deckt das Overlay das Quellbild weiss ab.
        self._aufruf("Emulation.setDefaultBackgroundColorOverride",
                     {"color": {"r": 0, "g": 0, "b": 0, "a": 0}}, frist=frist)
        self._aufruf("Emulation.setDeviceMetricsOverride",
                     {"width": breite, "height": hoehe,
                      "deviceScaleFactor": 1, "mobile": False}, frist=frist)
        self._aufruf("Page.navigate", {"url": self.url}, frist=frist)
        self._warten_bis_geladen(frist)

    def _warten_bis_geladen(self, frist):
        # Page.navigate antwortet, bevor die neue Seite steht. Ein Bild in
        # dieser Luecke scheitert mit „Not attached to an active page" —
        # gemessen beim Neustart nach einem Absturz, wo der erste Schuss
        # direkt folgt. Ein Neustart, der zuverlaessig mit Fehler endet, waere
        # ein Neustart je NEUSTART_RUHE_S und nie ein Bild.
        letzter = None
        while time.monotonic() < frist:
            try:
                erg = self._aufruf("Runtime.evaluate",
                                   {"expression": "document.readyState",
                                    "returnByValue": True}, frist=frist)
                if (erg.get("result") or {}).get("value") == "complete":
                    return
            except OverlayBrowserFehler as e:
                if self._proc is None or self._proc.poll() is not None:
                    raise
                letzter = e
            time.sleep(0.1)
        raise OverlayBrowserFehler("Seite nicht geladen: %s" % (letzter or self.url))

    def beenden(self):
        with self._sperre:
            self._beenden()

    def _beenden(self):
        p, self._proc = self._proc, None
        for fd in (self._w, self._r):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass   # Aufraeumen: schon zu ist so gut wie zu
        self._w = self._r = None
        self._sitzung = None
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

    # ── Bild ──────────────────────────────────────────────────────────
    def schuss(self, timeout=15.0):
        """PNG-Bytes des aktuellen Overlays. Startet einen gestorbenen Browser
        neu, aber hoechstens alle NEUSTART_RUHE_S. Wirft OverlayBrowserFehler."""
        with self._sperre:
            if not self.lebt():
                rest = NEUSTART_RUHE_S - (time.monotonic() - self._letzter_start)
                if self.starts and rest > 0:
                    raise OverlayBrowserFehler(
                        "Chromium gestorben (rc %s), Neustart in %.0f s"
                        % (self._proc.returncode if self._proc else "?", rest))
                self._starten(timeout)
            try:
                erg = self._aufruf("Page.captureScreenshot", {"format": "png"},
                                   frist=time.monotonic() + timeout)
            except OverlayBrowserFehler:
                # Ein Browser, der nicht antwortet, wird nicht wieder gesund —
                # beenden, damit der naechste Takt neu startet statt wieder
                # 15 s zu warten.
                self._beenden()
                raise
            return base64.b64decode(erg.get("data") or "")

    # ── Protokoll ─────────────────────────────────────────────────────
    def _aufruf(self, methode, params, frist):
        if self._w is None:
            raise OverlayBrowserFehler("Browser nicht gestartet")
        self._id += 1
        nachricht = {"id": self._id, "method": methode, "params": params}
        if self._sitzung and not methode.startswith("Target."):
            nachricht["sessionId"] = self._sitzung
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
            # Ereignisse (ohne id) und fremde Antworten ueberspringen.
            if antwort.get("id") != self._id:
                continue
            if "error" in antwort:
                raise OverlayBrowserFehler("%s: %s" % (
                    methode, antwort["error"].get("message", antwort["error"])))
            return antwort.get("result") or {}
