"""nc.meldetakt — v4.2-W81: einen GRUND melden, ohne das Log zu fluten.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Der Bestand hat zwei Drosseln, und beide passen hier nicht:

  `_loop_fehler(name, exc)` in bot.py drosselt **Ausnahmen** von
  Dauerschleifen. Der Resolver wirft aber keine Ausnahme — er kehrt
  ordentlich zurueck und sagt "unknown". Es gibt kein `exc`.

  `nc.audiotap.melden(...)` drosselt genau die richtige Sache, kennt aber
  nur den Audio-Tap: sie erwartet die Kategorien aus `ABHILFE` und wird mit
  Zeitstempeln von aussen gefuettert.

Was fehlte, ist die allgemeine Fassung: ein **Grund** mit einem Namen, der
sichtbar sein muss, aber nicht hundertmal pro Minute.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber meldete am 13.09. zwei Fehlerbilder:

    "whisper/transkript funktioniert immer noch nicht"
    "Chats koennen von online tiktok Usern geladen werden aber keine
     gueltigen streams"

Beide Wege scheitern **ohne Absturz**: `_resolve_via_webcast_api_v2` hat
elf Rueckgaben mit leerem Ergebnis, acht davon auf `log.debug`, drei ganz
ohne Meldung; `_whisper_transcribe` verschluckt jeden Fehler auf `debug`.
`stillecheck` faellt dort nicht — es gibt keinen stillen `except`, sondern
ein stilles `return`. `tools/blindstellen.py` misst genau diese Klasse und
zaehlte 498 Faelle im Produktionscode.

Warum die Zeilen ueberhaupt auf `debug` standen, ist kein Versehen: der
Resolver laeuft pro Poll-Durchlauf und pro verfolgtem Nutzer. Ungedrosselt
auf `warning` gehoben waere das Log nach einer Stunde unlesbar — und eine
unlesbare Warnung ist so gut wie keine. Die Drossel ist deshalb die
Voraussetzung dafuer, dass die Meldung ueberhaupt laut werden DARF.

════════════════════════════════════════════════════════════════════════
DIE REGEL
════════════════════════════════════════════════════════════════════════
Dieselbe wie bei `_loop_fehler` und `audiotap.melden`, damit es im Bestand
nicht drei verschiedene Rhythmen gibt:

  - die **erste** Meldung eines Schluessels sofort
  - ein **Wechsel des Grundes** sofort — dass sich das Fehlerbild geaendert
    hat, ist die eigentliche Nachricht (403 statt Timeout heisst etwas
    voellig anderes)
  - sonst hoechstens alle `ABSTAND_S`, mit der Zahl der unterdrueckten Faelle

Dieses Modul ist **bot-frei und uhrfrei**: es loggt nicht selbst und liest
keine Zeit, sondern bekommt `jetzt` hereingereicht und antwortet nur, OB
gemeldet werden soll und mit welchem Zusatz. Damit ist es ohne Bot, ohne
Schlaf und ohne Monkeypatching testbar — dieselbe Linie wie nc.audiotap.
"""
from __future__ import annotations

from typing import Dict, Tuple

# Abstand zwischen zwei Meldungen desselben Grundes. 900 s wie bei
# _loop_fehler und audiotap — bewusst identisch, nicht neu erfunden.
ABSTAND_S = 900.0

# Register: schluessel -> [letzte_meldung_ts, unterdrueckt, letzter_grund]
# Ein Dict und keine Modul-Globals: wer den Zustand zuruecksetzt, muss ihn
# fuer ALLE Leser zuruecksetzen (dieselbe Falle wie bei _RESTREAM_ACTIVE,
# W18, und nc.whispercfg.MODELL).
ZUSTAND: Dict[str, list] = {}


def melden(schluessel: str, grund: str, jetzt: float,
           abstand_s: float = None) -> Tuple[bool, int]:
    """Soll dieser Grund jetzt laut gemeldet werden? -> (melden, unterdrueckt)

    `schluessel` trennt die Drosseln voneinander — sinnvoll ist der Kanal,
    nicht der einzelne Nutzer ("resolver" statt "resolver:@peter"). Sonst
    drosselt jeder Nutzer fuer sich, und bei 200 verfolgten Kanaelen ist die
    Drossel wirkungslos.

    `unterdrueckt` ist die Zahl der seit der letzten lauten Meldung
    verschluckten Faelle — sie gehoert IN die Meldung, sonst liest sich ein
    Dauerfehler wie ein Einzelfall.
    """
    ab = ABSTAND_S if abstand_s is None else float(abstand_s)
    st = ZUSTAND.get(schluessel)
    if st is None:
        ZUSTAND[schluessel] = [float(jetzt), 0, grund]
        return True, 0
    if grund != st[2]:
        # Wechsel des Fehlerbildes — immer sofort, samt bisheriger Zahl.
        unterdrueckt = st[1]
        ZUSTAND[schluessel] = [float(jetzt), 0, grund]
        return True, unterdrueckt
    if float(jetzt) - st[0] >= ab:
        unterdrueckt = st[1]
        st[0], st[1] = float(jetzt), 0
        return True, unterdrueckt
    st[1] += 1
    return False, st[1]


def zusatz(unterdrueckt: int) -> str:
    """Der Klammerzusatz fuer die Meldung — leer, wenn nichts unterdrueckt
       wurde. Als eigene Funktion, damit alle Aufrufer denselben Wortlaut
       benutzen statt je einen eigenen zu formulieren."""
    if not unterdrueckt:
        return ""
    return f" ({unterdrueckt} weitere unterdrueckt)"


def zuruecksetzen(schluessel: str = None) -> None:
    """Nach einem Erfolg vergessen, damit der naechste Ausfall wieder sofort
       gemeldet wird. Ohne das bliebe ein behobener und dann erneut
       auftretender Fehler bis zu 15 Minuten unsichtbar."""
    if schluessel is None:
        ZUSTAND.clear()
    else:
        ZUSTAND.pop(schluessel, None)
