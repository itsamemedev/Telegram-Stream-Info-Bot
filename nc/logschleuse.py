"""nc.logschleuse — v4.2-W97: das Logging vom Event-Loop abkoppeln.

════════════════════════════════════════════════════════════════════════
DER BEFUND
════════════════════════════════════════════════════════════════════════
Am 18.09. stand der Bot zwischen 22:14 und 22:39 immer wieder still. Der
Wachhund meldete den Loop bis zu **176,5 s blockiert**, dreimal fiel die
Stufe darunter ("LOOP-STALL erkannt"), der Bridge-Tick stand 182 s, eine
Restream-Sitzung lief 225 s ohne ein Bild in den Stillstands-Riegel, der
Discord-Heartbeat war "blocked for more than 10 seconds", und am Ende kam
ein `database is locked`.

Der Voll-Stack-Dump nennt die Stelle, und sie ist nicht die, die man
vermutet. Der Loop-Thread hing nicht in einer Netzoperation, sondern hier:

    File "httpx/_client.py", line 1740, in _send_single_request
        logger.info(
    File "logging/__init__.py", line 1681, in handle
        self.callHandlers(record)
    File "logging/__init__.py", line 1026, in handle
        with self.lock:                     <<< hier stand der Event-Loop

Der Loop wartete auf die **Sperre eines Log-Handlers**. Am Wurzel-Logger
haengen drei synchrone Handler — ein `StreamHandler` auf die Konsole (unter
systemd eine Pipe nach journald, die volllaufen kann) und zwei
`RotatingFileHandler` auf `error.log` und `debug.log`. Jeder `emit()`
schreibt unter dieser Sperre auf die Platte, und 21 Threads teilen sie sich
mit dem Event-Loop.

Was die Sperre in dieser Nacht so lange hielt, stand daneben im Log: eine
787-MB-Aufnahme wurde in immer kleinere Teile zerlegt (`re-split #2 mit
target=11 MB`), Whisper transkribierte im Sekundentakt, der Resolver schrieb
zehn Zeilen pro Minute (siehe `nc.meldetakt`, derselbe Tag), und die
`disk-guard`-Schleife meldete sich 444 s nicht. Auf einer Platte, die unter
Volllast steht, dauert ein Log-Schreibvorgang Sekunden — und **jeder**
`log.info` im Loop wartet mit.

Das ist dieselbe Klasse wie die stillen `except`-Bloecke und die stillen
`return`s: nichts stuerzt ab, nichts meldet sich, es geht bloss nichts. Nur
ist die Ursache diesmal die Meldung selbst.

════════════════════════════════════════════════════════════════════════
DIE ABHILFE
════════════════════════════════════════════════════════════════════════
Eine Schleuse zwischen Logger und Platte: am Wurzel-Logger haengt nur noch
ein `QueueHandler`, der den Datensatz in eine Schlange legt und sofort
zurueckkehrt. Die drei echten Handler bedient ein einziger Hintergrund-
Thread. Damit kostet ein `log.info` im Event-Loop ein `put_nowait` statt
eines Plattenschreibvorgangs, und die Handler-Sperre wird nur noch von
diesem einen Thread genommen — es gibt keinen Wettbewerb mehr.

Zwei Dinge, die dabei nicht untergehen duerfen:

**Die Schlange ist begrenzt.** Eine unbegrenzte Schlange tauscht das
Blockieren gegen einen Speicherverbrauch, der bei haengender Platte
unbegrenzt waechst — aus einem eingefrorenen Loop wuerde ein OOM-Kill. Bei
`MAX_WARTEND` wird der neue Datensatz **verworfen und gezaehlt**, nie
gewartet: eine Schleuse, die blockieren kann, ist keine.

**Verluste werden gemeldet.** Ein stiller Verlust waere genau der Fehler,
gegen den dieses Projekt seine Sperren hat. Der Horcher-Thread schiebt
deshalb vor dem naechsten Datensatz eine eigene Zeile ein, sobald etwas
verlorenging — aus dem Horcher heraus, nicht aus dem Logger, sonst stuende
die Meldung wieder in der Schlange, die gerade voll ist.

Dieses Modul ist **bot-frei**: es kennt nur `logging` und `queue` aus der
Standardbibliothek, richtet nichts ein und oeffnet keine Datei. Es bekommt
den fertig bestueckten Wurzel-Logger hereingereicht und haengt um.
"""
from __future__ import annotations

import logging
import queue
import sys as _sys
import threading
from logging.handlers import QueueHandler, QueueListener

# Wieviele Datensaetze warten duerfen. 20000 Zeilen sind bei der Formatlaenge
# dieses Projekts rund 4 MB — genug, um jede gemessene Stockung zu ueberbruecken
# (die laengste war 176 s bei rund 10 Zeilen/s), und klein genug, dass eine
# dauerhaft haengende Platte den Prozess nicht auffrisst.
MAX_WARTEND = 20000

# Zaehler der verworfenen Datensaetze. Unter `_SPERRE`, weil ihn jeder
# loggende Thread erhoeht und der Horcher ihn abraeumt.
_SPERRE = threading.Lock()
_VERLOREN = [0]

# Der laufende Horcher, damit `entkoppeln` zweimal aufgerufen werden kann,
# ohne zwei Threads auf dieselben Handler zu setzen (Import-Reihenfolge,
# Test-Wiederholung). Eine Liste und keine Modul-Konstante: wer zuruecksetzt,
# muss es fuer ALLE Leser tun.
_HORCHER: list = [None]


class Schleuse(QueueHandler):
    """Legt den Datensatz in die Schlange — und wartet dabei nie.

    `QueueHandler.enqueue` ruft `put_nowait`, faengt aber nichts: bei voller
    Schlange flogen `queue.Full` bis in den Aufrufer, also mitten in den
    Event-Loop. Genau dort darf aus einer Logzeile kein Fehler werden.
    """

    def enqueue(self, record):
        try:
            self.queue.put_nowait(record)
        except queue.Full:
            with _SPERRE:
                _VERLOREN[0] += 1


class _Horcher(QueueListener):
    """Der eine Thread, der die echten Handler bedient.

    Er meldet Verluste selbst, statt sie einem Aufrufer zu ueberlassen: wer
    die Zahl kennt, ist dieser Thread, und er ist der einzige, der sie
    ausgeben kann, ohne sie wieder in die volle Schlange zu legen.
    """

    def handle(self, record):
        n = _verluste_abraeumen()
        if n:
            super().handle(_verlustsatz(n))
        super().handle(record)


def _verluste_abraeumen() -> int:
    with _SPERRE:
        n, _VERLOREN[0] = _VERLOREN[0], 0
    return n


def _verlustsatz(n: int) -> logging.LogRecord:
    """Die Zeile ueber verworfene Datensaetze — mit Abhilfe, nicht nur mit
       der Zahl. Ein blankes "n verloren" ist dieselbe Art Meldung wie ein
       blankes 'HTTP 403'."""
    satz = logging.LogRecord(
        name="TikTokBot", level=logging.ERROR, pathname=__file__, lineno=0,
        msg=("Log-Schleuse: %d Zeilen verworfen — die Schlange (%d Plaetze) "
             "war voll. Die Platte kommt beim Schreiben nicht nach. Pruefen: "
             "Plattenlast (iostat), freier Platz, und ob gerade eine grosse "
             "Aufnahme zerlegt wird. Der Bot laeuft weiter, es fehlen nur "
             "diese Zeilen."),
        args=(n, MAX_WARTEND), exc_info=None)
    satz.funcName = "Schleuse"
    return satz


def entkoppeln(wurzel: logging.Logger, max_wartend: int = None) -> QueueListener:
    """Alle Handler des Wurzel-Loggers hinter eine Schlange haengen.

    Gibt den laufenden Horcher zurueck. Ein zweiter Aufruf gibt denselben
    zurueck und haengt nichts um — sonst stuenden zwei Threads auf denselben
    Handlern und das Log waere doppelt.

    `respect_handler_level=True` ist nicht Beiwerk: ohne das schreibt der
    Horcher JEDEN Datensatz in JEDEN Handler, und `error.log` bekaeme die
    kompletten DEBUG-Zeilen. Die Trennung der beiden Dateien haengt genau
    daran.
    """
    if _HORCHER[0] is not None:
        return _HORCHER[0]
    echte = [h for h in wurzel.handlers if not isinstance(h, QueueHandler)]
    if not echte:
        raise ValueError("Wurzel-Logger hat keine Handler zum Entkoppeln")
    schlange = queue.Queue(maxsize=int(max_wartend or MAX_WARTEND))
    for h in echte:
        wurzel.removeHandler(h)
    wurzel.addHandler(Schleuse(schlange))
    horcher = _Horcher(schlange, *echte, respect_handler_level=True)
    horcher.daemon = True
    horcher.start()
    _HORCHER[0] = horcher
    return horcher


def stoppen(zeitlimit: float = 5.0) -> bool:
    """Schlange leeren und den Horcher beenden. -> lief einer?

    Gehoert an das Ende des Prozesses: ohne das gehen die letzten Zeilen
    verloren, und ausgerechnet die letzten sind beim Absturz die
    interessanten. `zeitlimit` greift nicht in `QueueListener.stop()` — es
    ist der Deckel fuer das Warten auf den Thread, damit ein haengender
    Handler den Abschied nicht verhindert.
    """
    horcher = _HORCHER[0]
    if horcher is None:
        return False
    _HORCHER[0] = None
    try:
        horcher.enqueue_sentinel()
    except Exception as e:
        # NICHT still: ist die Schlange voll, kommt das Wachtzeichen nicht
        # hinein, der Horcher endet als Daemon mit dem Prozess — und die
        # letzten Zeilen sind weg. Ausgerechnet die letzten sind beim
        # Absturz die interessanten, also gehoert das gesagt.
        #
        # Auf stderr und nicht ueber `logging`: hier wird das Log gerade
        # abgebaut, eine Logzeile landete in genau der Schlange, die das
        # Problem ist. Denselben Weg nimmt bot.py beim Aufbau der Schleuse.
        print(f"[exit] Log-Schleuse: Wachtzeichen kam nicht durch ({e}) — "
              f"die letzten Logzeilen koennen fehlen.", file=_sys.stderr,
              flush=True)
    t = getattr(horcher, "_thread", None)
    if t is not None:
        t.join(timeout=float(zeitlimit))
        horcher._thread = None
    return True


# Antwort von `wartend()`, wenn gar keine Schleuse laeuft. Bewusst KEINE 0:
# null Wartende liest sich gesund, und "es laeuft keine Schleuse" ist das
# Gegenteil davon — dann schreibt der Event-Loop wieder selbst auf die Platte,
# also genau der Zustand, den diese Welle behebt. Dieselbe Lehre wie bei
# nc.webserver.tls_lage (W93): eine eindeutige Antwort schlaegt einen Wert,
# der nach Normalbetrieb aussieht.
KEINE_SCHLEUSE = -1


def wartend() -> int:
    """Wieviele Datensaetze gerade in der Schlange stehen — fuer /healthz.

    Eine Schlange, die dauerhaft voll steht, ist die Vorstufe zum Verlust
    und gehoert sichtbar, bevor die erste Zeile faellt. `KEINE_SCHLEUSE`
    heisst: es gibt keine Schlange, das Logging laeuft synchron.
    """
    horcher = _HORCHER[0]
    if horcher is None:
        return KEINE_SCHLEUSE
    return horcher.queue.qsize()


def verloren() -> int:
    """Bisher verworfene Datensaetze, ohne den Zaehler abzuraeumen."""
    with _SPERRE:
        return _VERLOREN[0]


def zuruecksetzen() -> None:
    """Nur fuer die Vertraege: Horcher vergessen und Zaehler nullen."""
    stoppen(zeitlimit=2.0)
    with _SPERRE:
        _VERLOREN[0] = 0
