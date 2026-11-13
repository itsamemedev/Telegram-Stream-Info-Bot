"""nc.chatbild — v5.9-W205: der Chat-Kasten des Studio-Sendebilds als Bild aus Chromium.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber: „Emojis sollten im Restream-Chat zu sehen sein." Den Chat
schrieb ffmpeg mit drawtext, und drawtext kennt genau EINE Schrift — keinen
Rueckfall je Zeichen. Jedes Emoji wurde ein Kaestchen (W203 hat sie deshalb
zunaechst herausgenommen). Chromium faellt je Zeichen auf eine andere Schrift
zurueck und zeichnet mit fonts-noto-color-emoji farbig.

Also zeichnet Chromium den Kasten (`templates/chatbild.html`, Route
`/overlay/chat`), und ffmpeg legt das Bild genau dorthin, wo der Text-Chat
stand. Der Aufbau ist der des HTML-Overlays (W160/W170), weil dessen
gefaehrlichster Fehlerfall derselbe ist — ein stockender Bild-Eingang haelt
den GANZEN ffmpeg an:

* ein DAUERHAFTER Browser (nc/overlaybrowser.Dauerbrowser), kein Kaltstart je
  Bild — gemessen 0,08 statt 0,86 CPU-s;
* ein Schuss-Faden erneuert das PNG (atomar ersetzt);
* ein Schreiber-Faden schiebt mit FESTEM Takt das jeweils letzte gute PNG in
  die FIFO — ffmpeg hungert nie, auch wenn ein Schuss misslingt.

Startet der Browser nicht, liefert `starten()` None, und der Aufrufer bleibt
beim Text-Chat (Emoji dann herausgefiltert, aber kein Kaestchen).

Bot-frei: Browser-Klasse, Pfade und Takt kommen vom Aufrufer.
"""

import logging
import os
import threading
import time

log = logging.getLogger(__name__)

_LAUF = {}          # schluessel -> {"fifo","png","stop","browser","faeden"}


def an() -> bool:
    """RESTREAM_CHAT_BILD (Vorgabe an). Zur Laufzeit gelesen (.env kommt spaeter)."""
    return (os.getenv("RESTREAM_CHAT_BILD", "1") or "1").strip().lower() not in (
        "0", "false", "nein", "no", "off", "aus")
_SPERRE = threading.Lock()


def _bild_schreiben(browser, png):
    daten = browser.schuss(timeout=15)
    if len(daten) < 100:
        raise RuntimeError("leeres Bild (%d Bytes)" % len(daten))
    tmp = png + ".tmp"
    with open(tmp, "wb") as f:
        f.write(daten)
    os.replace(tmp, png)


def _schiessen(browser, png, stop, takt, melden):
    """Erneuert das PNG. Ein misslungener Schuss ist kein Ausfall (der
    Schreiber wiederholt das letzte Bild) — aber wenn KEINER mehr gelingt,
    friert der Chat ein, und das muss jemand erfahren: `melden` ist
    _loop_fehler des Bots (erste Meldung sofort, dann gedrosselt)."""
    while not stop.is_set():
        try:
            _bild_schreiben(browser, png)
        except Exception as e:
            melden("chatbild-schuss", e)
        stop.wait(takt)


def _schreiben(fifo, png, stop, takt):
    """Fester Takt in die FIFO. open() blockiert, bis ffmpeg liest."""
    try:
        with open(fifo, "wb") as f:
            while not stop.is_set():
                try:
                    with open(png, "rb") as im:
                        f.write(im.read())
                    f.flush()
                except (BrokenPipeError, ConnectionResetError):
                    # ffmpeg weg (Neustart oder Ende des Restreams) — der
                    # Schreiber endet; der naechste Start legt einen neuen an.
                    log.info("Chat-Kasten: ffmpeg hat %s geschlossen — Schreiber endet.", fifo)
                    return
                stop.wait(takt)
    except OSError as e:
        if not stop.is_set():
            log.warning("Chat-Kasten: FIFO %s geschlossen (%s) — der Restream "
                        "laeuft ohne neue Chat-Bilder weiter.", fifo, e)


def starten(schluessel, browser_klasse, binpath, url, groesse, ordner, fps=1.0,
            nice=None, melden=None, anlauf_s=1.5):
    """Browser starten, erstes Bild schreiben, FIFO anlegen, Faeden los.

    -> FIFO-Pfad, oder None (dann bleibt der Aufrufer beim Text-Chat)."""
    beenden(schluessel)
    melden = melden or (lambda name, e: log.warning("%s: %s", name, e))
    os.makedirs(ordner, exist_ok=True)
    png = os.path.join(ordner, "chatbild_%s.png" % schluessel)
    fifo = os.path.join(ordner, "chatbild_%s.fifo" % schluessel)
    browser = browser_klasse(binpath, url, groesse, nice=nice)
    try:
        browser.starten(timeout=20)
        # Die Seite holt den Chat per fetch — vor dem ersten Bild kurz Zeit
        # lassen, sonst ist das Preflight-Bild ein leerer Kasten.
        time.sleep(anlauf_s)
        _bild_schreiben(browser, png)
        if os.path.exists(fifo):
            os.unlink(fifo)
        os.mkfifo(fifo)
    except Exception as e:
        browser.beenden()
        log.warning("Chat-Kasten: Chromium-Bild nicht moeglich (%s: %s) — der Chat "
                    "bleibt Text (Emoji dann ohne Bild).", type(e).__name__, e)
        return None
    stop = threading.Event()
    takt = 1.0 / max(0.2, float(fps))
    faeden = [threading.Thread(target=_schiessen, args=(browser, png, stop, takt, melden),
                               daemon=True, name="chatbild-schuss"),
              threading.Thread(target=_schreiben, args=(fifo, png, stop, takt),
                               daemon=True, name="chatbild-fifo")]
    for t in faeden:
        t.start()
    with _SPERRE:
        _LAUF[schluessel] = {"fifo": fifo, "png": png, "stop": stop,
                             "browser": browser, "faeden": faeden}
    log.info("Chat-Kasten aktiv fuer %s: %s px, %.1f Bild/s (Emoji farbig).",
             schluessel, groesse, 1.0 / takt)
    return fifo


def _schreiber_wecken(fifo):
    """Ein Schreiber, der in open(fifo, "wb") haengt, kehrt erst zurueck, wenn
    ein Leser kommt — startet ffmpeg nie, stuende er fuer immer (W179)."""
    try:
        fd = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
        os.close(fd)
    except OSError as e:
        # FIFO schon weg — dann wartet auch niemand darauf.
        log.debug("Chat-Kasten: %s nicht zu wecken (%s).", fifo, e)


def beenden(schluessel):
    with _SPERRE:
        st = _LAUF.pop(schluessel, None)
    if not st:
        return
    st["stop"].set()
    _schreiber_wecken(st["fifo"])
    st["browser"].beenden()
    for p in (st["fifo"], st["png"]):
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass   # Aufraeumen: schon weg


def lage():
    """Fuer /healthz und das Deck: welche Kaesten laufen, lebt ihr Browser."""
    with _SPERRE:
        return {str(k): {"browser_lebt": bool(v["browser"].lebt())} for k, v in _LAUF.items()}
