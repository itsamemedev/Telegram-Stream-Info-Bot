"""nc.looplag — v4.2-W117: wie lange der Event-Loop steht, und WER ihn haelt.

════════════════════════════════════════════════════════════════════════
WAS SCHON DA WAR, UND WAS FEHLTE
════════════════════════════════════════════════════════════════════════
Der Bestand hat zwei Waechter fuer den Loop, und beide sind richtig:

  `_loop_lag_monitor` (W48)   schlaeft 2 s und misst die Ueberschreitung.
                              Meldet ab 3 s, hoechstens einmal je Minute.
  `_loop_watchdog_thread` (W83)  ein Thread, der ab 30 s Stillstand einen
                              Voll-Stack-Dump aller Threads schreibt.

Dazwischen liegt eine Luecke von zwei Groessenordnungen. Ein Loop, der
alle paar Sekunden fuer 800 ms steht, erreicht keine der beiden Schwellen
— und genau so sieht ein Bot aus, der "zaeh" ist: Discord-Heartbeats
knapp, Telegram-Befehle mit Verzoegerung, Restream-Watcher, die zu spaet
reagieren. Es gab dafuer keine Zahl, und wenn es eine gegeben haette,
haette sie nicht gesagt, WO.

Der Stack-Dump aus W83 hat am 18.09. die Stelle sofort gezeigt (die
Sperre eines Log-Handlers, siehe nc.logschleuse) — aber erst nach 30 s.
Fuer alles darunter blieb nur Raten.

════════════════════════════════════════════════════════════════════════
DIE ZWEI TEILE
════════════════════════════════════════════════════════════════════════
**Die Messung.** `takt()` schlaeft in kurzen Schritten (Vorgabe 100 ms)
und legt jede Ueberschreitung in einen Ring mit festem Deckel. Daraus
entstehen fuer /healthz `letzt_ms`, `p50_ms`, `p99_ms` und `max_ms` ueber
das Fenster des Rings, dazu die Zahl der Schritte ueber dem Budget. Ein
Ring und keine Liste: ein Messpfad, der ueber Tage waechst, ist genau die
Art Leck, die dieser Sprint sucht.

**Der Spaeher.** Ein eigener Thread — er muss leben, waehrend der Loop
steht — sieht alle 50 ms nach, wie alt der letzte Schritt ist. Ist er
aelter als die Schwelle (Vorgabe 250 ms), liest er per
`sys._current_frames()` den Stapel des Loop-Threads und merkt sich die
Stelle. Endet die Episode, wird sie mit Dauer und Stelle verbucht.

Das funktioniert mit jedem Loop, auch mit uvloop: es wird nichts an
asyncio gepatcht, nur von aussen hingesehen. Der naheliegende andere Weg
— `Handle._run` umwickeln, wie es asyncio im Debug-Modus tut — waere
unter uvloop wirkungslos, ohne es zu sagen, und kostete jeden einzelnen
Callback Zeit. Der Spaeher kostet nur, wenn der Loop schon steht.

Die Stelle hat ZWEI Haelften, und beide zaehlen:

  `eigen`   die zwei innersten Rahmen aus diesem Projekt — wo man den
            Fehler behebt (`bot.py:_monitor:15008 > nc/dbwrap.py:db_conn:370`)
  `innen`   der innerste Rahmen ueberhaupt — woran es haengt
            (`logging/__init__.py:handle:1026`, `sqlite3`, `time.sleep`)

Am 18.09. waere `innen` die Antwort gewesen und `eigen` die Abhilfe.
Gemeldet wird nur der Dateiname, nie der volle Pfad: /healthz haengt
ohne Anmeldung an UptimeRobot.

Dieses Modul ist bot-frei und stdlib-only. Es richtet nichts selbst ein;
`bot.py` startet `takt()` als Task und `spaeher_starten()` einmal.
"""
from __future__ import annotations

import asyncio
import collections
import os
import sys
import threading
import time
from typing import Callable, Dict, Optional

# Ringgroesse: bei 100 ms Takt fuenf Minuten. Genug fuer ein p99, das eine
# einzelne Stockung nicht wegmittelt, und ein fester Deckel von 3000 floats.
RING = 3000

# Hoechstens so viele verschiedene Stellen im Register. Die Stellen sind ein
# offenes Vokabular (jede Zeile im Bestand kann eine sein) — ohne Deckel
# waere das Register ein langsames Leck. Geworfen wird die seltenste.
MAX_STELLEN = 32

_SPERRE = threading.Lock()

# Ein Dict und keine Modul-Globals: wer zuruecksetzt, muss es fuer ALLE
# Leser tun (dieselbe Falle wie bei nc.meldetakt.ZUSTAND).
ZUSTAND: Dict[str, object] = {
    "ring": collections.deque(maxlen=RING),
    "schlag": 0.0,          # monotonic des letzten Takt-Schritts
    "letzt": 0.0,           # letzte Ueberschreitung in s
    "budget_s": 0.1,
    "ueber_budget": 0,      # Schritte ueber dem Budget seit Start
    "schritte": 0,
    "takt_s": 0.1,
    "loop_tid": None,       # Thread-Ident des Loops
    "spaeher": None,        # laufender Spaeher-Thread
    "episoden": 0,          # verbuchte Stockungen ueber der Spaeher-Schwelle
    "stellen": {},          # stelle -> [anzahl, max_ms, summe_ms, letzt_ts]
}

# Pfadteile, an denen ein Rahmen als "fremd" gilt. Alles andere ist eigener
# Code. Absichtlich ueber die Pfade und nicht ueber eine Liste eigener
# Dateien: die Liste waere bei jeder neuen nc/-Datei veraltet.
_FREMD = ("site-packages", "dist-packages", os.sep + "lib" + os.sep + "python",
          "<frozen ", os.sep + "asyncio" + os.sep)


def erfassen(ueber_s: float) -> None:
    """Eine Ueberschreitung buchen. Aus `takt()` heraus, also auf dem Loop —
       deshalb nichts als ein paar Zuweisungen."""
    z = ZUSTAND
    if ueber_s < 0:
        ueber_s = 0.0
    z["ring"].append(ueber_s)
    z["letzt"] = ueber_s
    z["schritte"] += 1
    if ueber_s > z["budget_s"]:
        z["ueber_budget"] += 1


async def takt(takt_s: float = 0.1, budget_s: float = 0.1) -> None:
    """Der kurze Schritt auf dem Loop. Jede Verspaetung gegenueber dem
       bestellten Schlaf ist Zeit, in der eine andere Coroutine den Loop
       nicht freigegeben hat.

       Kostet zehn Weckrufe je Sekunde — gegen die Hunderte, die der Bot
       ohnehin hat, nicht messbar."""
    z = ZUSTAND
    z["takt_s"] = float(takt_s)
    z["budget_s"] = float(budget_s)
    z["loop_tid"] = threading.get_ident()
    uhr = time.monotonic
    z["schlag"] = uhr()
    while True:
        t0 = uhr()
        try:
            await asyncio.sleep(takt_s)
        except asyncio.CancelledError:
            z["schlag"] = 0.0      # kein Takt mehr -> der Spaeher sieht nichts
            return
        jetzt = uhr()
        z["schlag"] = jetzt
        erfassen((jetzt - t0) - takt_s)


def _perzentil(sortiert, p: float) -> float:
    # Ein leerer Ring ist kein Fehler, sondern "noch keine Messung" — das
    # sagt `aktiv` in lage(), nicht diese Zahl.
    n = len(sortiert)
    return sortiert[min(n - 1, max(0, int(round(p * (n - 1)))))] if n else 0.0


def lage() -> dict:
    """Die Zahlen fuer /healthz. Laeuft im Flask-Thread, nicht auf dem Loop.

       `aktiv` False heisst: es laeuft kein Takt. Dann sind alle Zahlen 0 —
       und das darf sich nicht wie ein gesunder Loop lesen, deshalb steht
       es ausdruecklich dabei (dieselbe Lehre wie logschleuse.KEINE_SCHLEUSE).
    """
    z = ZUSTAND
    # tuple() auf eine deque laeuft in C unter dem GIL — ein gleichzeitiges
    # append() aus dem Loop kann die Kopie nicht zerreissen.
    werte = sorted(tuple(z["ring"]))
    def ms(s):
        return round(s * 1000.0, 1)
    return {
        "aktiv": bool(z["schlag"]),
        "letzt_ms": ms(z["letzt"]),
        "p50_ms": ms(_perzentil(werte, 0.50)),
        "p99_ms": ms(_perzentil(werte, 0.99)),
        "max_ms": ms(werte[-1] if werte else 0.0),
        "fenster_s": round(len(werte) * float(z["takt_s"]), 0),
        "budget_ms": ms(z["budget_s"]),
        "ueber_budget": int(z["ueber_budget"]),
        "stockungen": int(z["episoden"]),
    }


# ─────────────────────────────────────────────────────────────────────────
# Der Spaeher
# ─────────────────────────────────────────────────────────────────────────

def _kurz(dateiname: str) -> str:
    """Nur der Dateiname, mit dem Paketordner davor, wo er etwas sagt
       (`nc/dbwrap.py`, `logging/__init__.py`). Nie der volle Pfad."""
    teile = dateiname.replace("\\", "/").rsplit("/", 2)
    if len(teile) >= 2 and teile[-2] in ("nc", "routes", "brain", "logging",
                                         "asyncio", "sqlite3", "http",
                                         "concurrent", "json", "ssl"):
        return teile[-2] + "/" + teile[-1]
    return teile[-1]


def _ist_fremd(dateiname: str) -> bool:
    return any(t in dateiname for t in _FREMD)


def stelle_aus_rahmen(rahmen) -> str:
    """Aus dem innersten Rahmen eines Stapels die Stelle machen:
       `aufrufer > eigen <- innen`.

       ZWEI eigene Rahmen und nicht einer: nc/ ist eigener Code, und haengt
       der Loop in SQLite, ist der innerste eigene Rahmen `nc/dbwrap.py` —
       richtig und nutzlos, denn db_conn hat jeder. Die Abhilfe steht beim
       Aufrufer eine Ebene darueber.

       Als eigene Funktion, damit sie ohne Thread und ohne Stillstand
       pruefbar ist."""
    innen = None
    eigene = []
    r = rahmen
    while r is not None and len(eigene) < 2:
        co = r.f_code
        ort = "%s:%s:%d" % (_kurz(co.co_filename), co.co_name, r.f_lineno)
        if innen is None:
            innen = ort
        if not _ist_fremd(co.co_filename):
            eigene.append(ort)
        r = r.f_back
    if innen is None:
        return "?"
    eigen = " > ".join(reversed(eigene))
    if not eigene:
        return innen
    if eigene[0] == innen:
        return eigen
    return eigen + " <- " + innen


def _verbuchen(stelle: str, dauer_s: float, jetzt: float) -> None:
    with _SPERRE:
        st = ZUSTAND["stellen"]
        e = st.get(stelle)
        ms = dauer_s * 1000.0
        if e is None:
            st[stelle] = [1, ms, ms, jetzt]
            while len(st) > MAX_STELLEN:
                # Die seltenste fliegt, bei Gleichstand die aelteste. Die
                # gerade verbuchte ist mit Anzahl 1 und juengstem Zeitstempel
                # nie die Wahl, solange es eine gleich seltene aeltere gibt.
                weg = min(st, key=lambda k: (st[k][0], st[k][3]))
                del st[weg]
        else:
            e[0] += 1
            e[1] = max(e[1], ms)
            e[2] += ms
            e[3] = jetzt
        ZUSTAND["episoden"] += 1


def bremser(n: int = 5) -> list:
    """Die Stellen, die den Loop am laengsten gehalten haben — nach Summe,
       weil zehn Stockungen von 400 ms mehr kosten als eine von 2 s."""
    with _SPERRE:
        st = dict((k, list(v)) for k, v in ZUSTAND["stellen"].items())
    reihe = sorted(st.items(), key=lambda kv: -kv[1][2])[:max(0, int(n))]
    return [{"stelle": k, "anzahl": v[0], "max_ms": round(v[1], 0),
             "summe_ms": round(v[2], 0)} for k, v in reihe]


def _spaeher_lauf(schwelle_s: float, blick_s: float,
                  melden: Optional[Callable[[str, float], None]],
                  halt: threading.Event) -> None:
    z = ZUSTAND
    uhr = time.monotonic
    in_episode = False
    beginn = 0.0
    zaehl: Dict[str, int] = {}
    while not halt.wait(blick_s):
        schlag = z["schlag"]
        tid = z["loop_tid"]
        if not schlag or tid is None:
            in_episode = False
            continue
        alter = uhr() - schlag
        if alter > schwelle_s + z["takt_s"]:
            if not in_episode:
                in_episode = True
                beginn = schlag
                zaehl = {}
            rahmen = sys._current_frames().get(tid)
            stelle = stelle_aus_rahmen(rahmen) if rahmen is not None else "?"
            del rahmen      # keinen fremden Stapel festhalten
            zaehl[stelle] = zaehl.get(stelle, 0) + 1
            continue
        if in_episode:
            in_episode = False
            # Abzueglich des bestellten Schlafs: der gehoert nicht zur
            # Stockung, sondern zum Takt.
            dauer = max(0.0, schlag - beginn - z["takt_s"])
            # Die haeufigste Stelle der Episode — bei einer langen Stockung
            # wandert der Stapel (erst sqlite, dann das Log), und die Stelle,
            # an der er am laengsten stand, ist die, die zaehlt.
            stelle = max(zaehl, key=zaehl.get) if zaehl else "?"
            _verbuchen(stelle, dauer, uhr())
            if melden is not None:
                try:
                    melden(stelle, dauer)
                except Exception as e:
                    # Nicht ueber `logging`: der Meldeweg ist hier gerade
                    # der, der gescheitert ist.
                    print("[looplag] Meldeweg fiel aus: %r" % (e,),
                          file=sys.stderr, flush=True)


def spaeher_starten(schwelle_s: float = 0.25, blick_s: float = 0.05,
                    melden: Optional[Callable[[str, float], None]] = None
                    ) -> Optional[threading.Thread]:
    """Den Spaeher-Thread starten, hoechstens einmal. -> Thread oder None.

       `melden(stelle, dauer_s)` wird je beendeter Stockung aufgerufen, im
       Spaeher-Thread. Drosseln ist Sache des Aufrufers (nc.meldetakt) —
       dieses Modul weiss nicht, wie laut der Bot sein darf.

       Ob der Spaeher ueberhaupt laufen soll, entscheidet ebenfalls der
       Aufrufer (LOOP_SPAEHER_MS=0) — und sagt es dort. Eine Schwelle von
       null hiesse hier "jeder Blick ist eine Stockung"; sie wird deshalb
       auf einen Takt angehoben statt still verworfen.
    """
    schwelle_s = max(float(schwelle_s), float(blick_s))
    alt = ZUSTAND["spaeher"]
    if alt is not None and alt[0].is_alive():
        return alt[0]
    halt = threading.Event()
    t = threading.Thread(target=_spaeher_lauf, name="loop-spaeher",
                         args=(float(schwelle_s), float(blick_s), melden, halt),
                         daemon=True)
    t.start()
    ZUSTAND["spaeher"] = (t, halt)
    return t


def zuruecksetzen() -> None:
    """Nur fuer die Vertraege: Spaeher anhalten, Zahlen nullen."""
    alt = ZUSTAND["spaeher"]
    if alt is not None:
        alt[1].set()
        alt[0].join(timeout=2.0)
    with _SPERRE:
        ZUSTAND.update({"ring": collections.deque(maxlen=RING), "schlag": 0.0,
                        "letzt": 0.0, "ueber_budget": 0, "schritte": 0,
                        "loop_tid": None, "spaeher": None, "episoden": 0,
                        "stellen": {}})
