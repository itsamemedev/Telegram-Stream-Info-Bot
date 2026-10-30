"""nc.schnappschuss — v4.2-W119: eine Auswertung fuer alle, die gleichzeitig fragen.

`/api/pulse` ist der Herzschlag des Decks: jeder offene Tab fragt alle 5 s,
und jede Antwort baut vier Auswertungen neu (Zaehler, Bandbreite,
Health-Score, Sendeleiste). Mit Desktop, Handy-PWA und einem zweiten
Fenster sind das zwoelf Auswertungen in fuenf Sekunden fuer dieselben
Zahlen — und unter waitress laufen sie gleichzeitig in mehreren Threads
gegen dieselbe SQLite.

Ein Schnappschuss mit kurzer Gueltigkeit macht daraus hoechstens eine je
Gueltigkeit, egal wie viele Tabs offen sind. Die Sperre um das Erzeugen
ist der Single-Flight: wer waehrenddessen fragt, wartet und bekommt den
frischen Wert, statt selbst zu rechnen.

**Die Sperre wartet nicht unbegrenzt.** Haengt die Erzeugung (SQLite unter
Plattenlast, W29), staende sonst jeder Pulse-Aufruf in der Schlange, bis
alle waitress-Threads belegt sind — dann antwortet das Deck gar nicht mehr,
auch nicht auf den Knopf, mit dem man nachsehen will. Nach `warte_s` gibt
es den letzten Wert mit `veraltet`, und gibt es keinen, rechnet der
Aufrufer selbst.

Bot-frei, stdlib-only, die Uhr ist injizierbar.
"""
from __future__ import annotations

import threading
import time
from typing import Callable, Tuple


class Schnappschuss:
    def __init__(self, gueltig_s: float = 2.0, warte_s: float = 5.0,
                 uhr: Callable[[], float] = time.monotonic):
        self.gueltig_s = float(gueltig_s)
        self.warte_s = float(warte_s)
        self._uhr = uhr
        self._sperre = threading.Lock()
        self._wert = None
        self._stand = None          # Zeitpunkt der Erzeugung, None = nie
        self.zaehler = {"erzeugt": 0, "geteilt": 0, "veraltet": 0}

    def _frisch(self, jetzt: float) -> bool:
        return self._stand is not None and jetzt - self._stand < self.gueltig_s

    def holen(self, erzeuger: Callable[[], object]) -> Tuple[object, bool]:
        """-> (wert, veraltet). `veraltet` ist True nur, wenn die Erzeugung
           eines anderen Aufrufers laenger als `warte_s` haengt."""
        if self._frisch(self._uhr()):
            self.zaehler["geteilt"] += 1
            return self._wert, False
        if not self._sperre.acquire(timeout=self.warte_s):
            if self._stand is not None:
                self.zaehler["veraltet"] += 1
                return self._wert, True
            # Noch nie erzeugt und der erste haengt: selbst rechnen ist
            # besser als nichts zu antworten.
            return erzeuger(), False
        try:
            # Zweite Pruefung unter der Sperre: wer gewartet hat, findet den
            # Wert des Vorgaengers vor (dieselbe Lehre wie nc.livecache, W103).
            if self._frisch(self._uhr()):
                self.zaehler["geteilt"] += 1
                return self._wert, False
            wert = erzeuger()
            # Die Uhr NACH dem Erzeugen (W103): sonst verschenkt der Wert die
            # Dauer seiner eigenen Berechnung.
            self._wert, self._stand = wert, self._uhr()
            self.zaehler["erzeugt"] += 1
            return wert, False
        finally:
            self._sperre.release()
