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
  - ein **neuer Grund** sofort — dass sich das Fehlerbild geaendert hat, ist
    die eigentliche Nachricht (403 statt Timeout heisst etwas voellig
    anderes)
  - sonst hoechstens alle `ABSTAND_S`, mit der Zahl der unterdrueckten Faelle

════════════════════════════════════════════════════════════════════════
WAS "NEU" HEISST — v4.2-W97
════════════════════════════════════════════════════════════════════════
Bis W97 hiess "neu" schlicht: anders als beim letzten Aufruf. Das setzt
voraus, dass ein Kanal zu einer Zeit EINEN vorherrschenden Grund hat. Der
Resolver-Kanal tut das nicht — er laeuft pro Poll ueber 40 verfolgte Nutzer,
und jeder Nutzer erzeugt der Reihe nach `status_code`, dann `html_kein_tag`.
Damit war **jeder** Aufruf ein Wechsel, und die Drossel griff nie:

    2026-09-18 14:43:28 … @xxxderspenderxxx ergebnislos [status_code]
    2026-09-18 14:43:28 … @xxxderspenderxxx ergebnislos [html_kein_tag]
    2026-09-18 14:43:28 … @HannoverPorsche  ergebnislos [status_code]
    2026-09-18 14:43:29 … @HannoverPorsche  ergebnislos [html_kein_tag]

Gemessen im Log vom 19.09.: **13675 Zeilen aus `_resolver_stumm` in 22
Stunden**, rund zehn pro Minute, 5315 davon mit einem Unterdrueckt-Zaehler
— der Beweis, dass der Wechsel-Pfad dauernd feuerte. Das ist genau der
Zustand, den dieses Modul verhindern sollte, nur eine Ebene tiefer als der
Nutzer-Schluessel, vor dem sein eigener Docstring warnt.

Die Drossel merkt sich deshalb seither eine Ruhezeit **je (Kanal, Grund)**.
Ein wirklich neuer Grund meldet weiter sofort — er hatte ja keine —, ein
zurueckkehrender erst nach `ABSTAND_S`. Abwechselnde Gruende drosseln sich
damit gegenseitig nicht mehr weg.

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

# Register: schluessel -> [unterdrueckt, {grund: letzte_meldung_ts}]
# Ein Dict und keine Modul-Globals: wer den Zustand zuruecksetzt, muss ihn
# fuer ALLE Leser zuruecksetzen (dieselbe Falle wie bei _RESTREAM_ACTIVE,
# W18, und nc.whispercfg.MODELL).
ZUSTAND: Dict[str, list] = {}

# Deckel fuer die Gruende je Kanal. Die meisten Kanaele haben ein geschlossenes
# Vokabular (nc.resolvergrund kennt 16), aber nicht alle: "stats-json" nimmt
# `str(info)[:80]` als Grund, und das ist offen. Ohne Deckel waere die Drossel
# ein langsames Speicherleck — dieselbe Klasse wie eine Grundlinie, die bei
# jeder Welle mitwaechst. Weggeworfen wird der aelteste Eintrag; die Abwaegung
# steht bei `_aufraeumen`.
MAX_GRUENDE = 64


def melden(schluessel: str, grund: str, jetzt: float,
           abstand_s: float = None) -> Tuple[bool, int]:
    """Soll dieser Grund jetzt laut gemeldet werden? -> (melden, unterdrueckt)

    `schluessel` trennt die Drosseln voneinander — sinnvoll ist der Kanal,
    nicht der einzelne Nutzer ("resolver" statt "resolver:@peter"). Sonst
    drosselt jeder Nutzer fuer sich, und bei 200 verfolgten Kanaelen ist die
    Drossel wirkungslos.

    `unterdrueckt` ist die Zahl der seit der letzten lauten Meldung
    verschluckten Faelle — sie gehoert IN die Meldung, sonst liest sich ein
    Dauerfehler wie ein Einzelfall. Sie zaehlt je KANAL, nicht je Grund: der
    Betreiber will wissen, wie viel dieser Kanal gerade verschluckt, und
    nicht dieselbe Zahl auf sechzehn Gruende verteilt lesen.

    v4.2-W97: die Ruhezeit haengt am Paar (Kanal, Grund). Vorher genuegte ein
    Grund, der sich vom VORIGEN unterschied — bei einem Kanal mit mehreren
    gleichzeitig laufenden Gruenden war damit jeder Aufruf ein Wechsel und
    die Drossel wirkungslos (13675 Zeilen in 22 Stunden, siehe Modulkopf).
    """
    ab = ABSTAND_S if abstand_s is None else float(abstand_s)
    jetzt = float(jetzt)
    st = ZUSTAND.get(schluessel)
    if st is None:
        ZUSTAND[schluessel] = [0, {grund: jetzt}]
        return True, 0

    unterdrueckt, gesehen = st
    zuletzt = gesehen.get(grund)
    if zuletzt is None or jetzt - zuletzt >= ab:
        # Entweder ein Grund, der in diesem Fenster noch nicht laut war —
        # dann ist er die Nachricht —, oder einer, dessen Ruhezeit um ist.
        gesehen[grund] = jetzt
        _aufraeumen(gesehen)
        st[0] = 0
        return True, unterdrueckt

    st[0] = unterdrueckt + 1
    return False, st[0]


def _aufraeumen(gesehen: Dict[str, float]) -> None:
    """Ueber `MAX_GRUENDE` hinaus den aeltesten Grund vergessen.

    Die erste Fassung dieses Deckels warf nur Gruende weg, die laenger als
    zwei Fenster still waren — und war damit wirkungslos. Der Fall, gegen
    den er gebaut ist, sind viele Gruende in kurzer Folge ("stats-json"
    nimmt `str(info)[:80]`); die sind alle jung, also fiel keiner heraus.
    Der eigene Vertrag hat das gefangen: 192 Eintraege bei MAX_GRUENDE = 64.
    Ein Deckel, der nur im gutmuetigen Fall greift, ist keiner.

    Geworfen wird deshalb nach Alter, ohne Ruecksicht auf die Ruhezeit — mit
    offener Abwaegung: ein verworfener Grund meldet beim naechsten Auftreten
    einmal zusaetzlich laut. Das kostet EINE Zeile. Ein Register, das
    unbegrenzt waechst, kostet den Prozess.

    Der aelteste ist dabei der mit der aeltesten lauten Meldung, also der,
    dessen Ruhezeit ohnehin am naechsten am Ablauf steht. Der zuletzt
    gemeldete — der, der gerade drosselt — bleibt.
    """
    while len(gesehen) > MAX_GRUENDE:
        aeltester = min(gesehen, key=gesehen.__getitem__)
        del gesehen[aeltester]


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
