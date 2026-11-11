"""nc.forkriegel — v5.1-W183: ein wartender Fork bekommt Vortritt vor Whisper.

════════════════════════════════════════════════════════════════════════
DER BEFUND (Produktionslog 11.11.)
════════════════════════════════════════════════════════════════════════
Seit v4.0-W76 serialisiert EIN Lock (`bot._FORK_NATIVE_LOCK`) jeden Fork
gegen die native Whisper-Arbeit — richtig, sonst erbt das Kind gesperrte
CTranslate2-Mutexe und der Loop haengt. Die beiden Seiten warten aber
verschieden:

    Whisper-Thread   _FORK_NATIVE_LOCK.acquire()            blockierend
    Fork (im Loop)   acquire(blocking=False) alle 20 ms     pollend

Bei mehreren Transkriptionen hintereinander geht das Lock von Thread zu
Thread, ohne je frei zu sein, wenn der Poller nachsieht. W76 rechnete mit
„Bruchteil bis ~2 s" je Chunk. Am 11.11. lief `medium` mit RTF 2,74 — 30 s
je Chunk, drei Transkriptionen parallel angemeldet. Ab 18:13 lief die
Live-Check-Schlange voll (4809 verworfen bis 18:31), um 18:34 meldete der
Watchdog live-worker-0 und -3 seit 450 s ohne Lebenszeichen: jeder Worker,
der yt-dlp oder ffmpeg starten wollte, stand in diesem Poll.

Der Riegel hier gibt dem Fork Vortritt: wer forken will, meldet sich an,
und ein Whisper-Thread, der den nativen Abschnitt BETRETEN will, wartet,
bis kein Fork mehr ansteht — hoechstens `max_warten_s`, damit eine Kette
von Spawns Whisper nicht ihrerseits aushungert. Ein laufender Abschnitt
wird nie unterbrochen; der Fork wartet hoechstens auf dessen Ende.

Bot-frei, stdlib. Das Lock selbst bleibt im Bot (`_FORK_NATIVE_LOCK`);
dieses Modul regelt nur die Reihenfolge davor.
"""

import contextlib
import threading
import time


class Vortritt:
    """Zaehlt wartende Forks; native Abschnitte lassen ihnen den Vortritt."""

    def __init__(self, max_warten_s=5.0):
        self.max_warten_s = float(max_warten_s)
        self._bed = threading.Condition(threading.Lock())
        self._wartend = 0
        self.gewartet_s = 0.0         # Summe, fuer /healthz und den Vertrag
        self.ueberzogen = 0           # so oft lief Whisper trotz wartendem Fork an

    def wartend(self) -> int:
        with self._bed:
            return self._wartend

    @contextlib.contextmanager
    def anmelden(self):
        """Um das Warten des Forks auf das Lock legen (Loop-Seite)."""
        with self._bed:
            self._wartend += 1
        try:
            yield
        finally:
            with self._bed:
                self._wartend -= 1
                if self._wartend <= 0:
                    self._wartend = 0
                    self._bed.notify_all()

    def abwarten(self) -> bool:
        """Vor dem Betreten eines nativen Abschnitts (Thread-Seite).

        -> True, wenn kein Fork (mehr) ansteht; False, wenn die Frist
        abgelaufen ist und trotzdem betreten wird."""
        t0 = time.monotonic()
        with self._bed:
            frei = self._bed.wait_for(lambda: self._wartend == 0,
                                      timeout=self.max_warten_s)
            if not frei:
                self.ueberzogen += 1
        self.gewartet_s += time.monotonic() - t0
        return frei
