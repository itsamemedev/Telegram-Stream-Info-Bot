"""nc.betriebslage — v4.2-W121: Start, Stopp und "degradiert, aber lebendig".

Drei Fragen, auf die der Bestand keine Antwort hatte:

**Wie lange dauert ein Neustart?** `systemctl restart` ist der Weg, ueber
den jedes Update wirkt (CLAUDE.md, Update-Funktion). Wann der Bot danach
wieder Live-Starts erkennt, stand nirgends. `bereit()` haelt den Zeitpunkt
fest, an dem die erste Pruefrunde eingereiht ist; /healthz traegt die Dauer.

**Was wird beim Stopp aus einer laufenden Aufnahme?** Der Abbruchzweig von
`handle_recording_finished` schickte ffmpeg SIGKILL und trug die Datei
nicht ein. Die Datei blieb liegen, ohne Datenbankzeile — genau die
"Waise", die `/api/rec/orphans/clean` zum Loeschen anbietet (W91). Jeder
Neustart, also jedes Update, machte so aus jeder laufenden Aufnahme einen
Loeschkandidaten. `sichern_beim_stopp()` entscheidet, ob eine Datei
eingetragen wird.

**Ist der Bot "degradiert" oder "tot"?** `/healthz` kennt `ok` (Loops
leben, Datenbank antwortet) und den HTTP-Code dazu — UptimeRobot haengt
daran und bleibt unveraendert. Dazwischen lag nichts: ein Bot mit 800 ms
Loop-Lag, voller fd-Tabelle oder umgangener Log-Schleuse war "ok".
`bewerten()` sammelt die weichen Gruende in eine Liste mit Klartext.

Bot-frei, rein rechnend; die Uhr kommt herein.
"""
from __future__ import annotations

import os
import time
from typing import Optional

# Gemessen beim Import dieses Moduls — bot.py importiert es frueh. Der
# Prozessstart selbst liegt ein paar hundert Millisekunden davor (Python,
# die ersten Importe); das ist bewusst nicht mitgezaehlt, weil es sich
# nicht von hier aus aendern laesst.
_START = time.monotonic()
ZUSTAND = {"bereit_s": None, "stopp_s": None}

# Unter dieser Groesse ist eine Datei ein Kopf ohne Inhalt (dieselbe Grenze
# wie nc.videoteil._MIN_TEIL_BYTES).
MIN_BYTES = 10_240


def bereit(jetzt: Optional[float] = None) -> Optional[float]:
    """Den Zeitpunkt der Betriebsbereitschaft festhalten — nur beim ersten
       Aufruf. -> Sekunden seit Start, oder None, wenn schon gesetzt."""
    # Ein Ausgang: "schon gesetzt" ist kein Misserfolg, sondern der
    # Normalfall ab der zweiten Runde (tools/blindstellen.py).
    erst = ZUSTAND["bereit_s"] is None
    if erst:
        jetzt = time.monotonic() if jetzt is None else jetzt
        ZUSTAND["bereit_s"] = round(jetzt - _START, 1)
    return ZUSTAND["bereit_s"] if erst else None


def sichern_beim_stopp(pfad: str) -> bool:
    """Gehoert die Datei einer beim Stopp abgebrochenen Aufnahme in die
       Datenbank? Ja, wenn sie da ist und mehr als einen Kopf traegt.

    Auch eine kurze oder nicht ganz fertige Aufnahme: das Format ist
    fragmentiertes MP4 (`+empty_moov+frag_keyframe`, nc/reccmd.py), das
    ueberlebt einen Abbruch abspielbar. Und selbst eine kaputte Datei ist
    mit Eintrag besser dran — sie ist im Deck sichtbar, reparierbar (B47)
    und loeschbar; ohne Eintrag ist sie unsichtbar und ein Loeschkandidat."""
    return bool(pfad) and os.path.isfile(pfad) and os.path.getsize(pfad) >= MIN_BYTES


def bewerten(d: dict) -> tuple:
    """Weiche Gruende sammeln. -> ("ok" | "degradiert" | "gestoert", [gruende])

    `gestoert` heisst: das harte Kriterium (`ok` aus /healthz) ist verletzt.
    `degradiert`: der Bot arbeitet, aber etwas davon kostet gerade Leistung
    oder Sichtbarkeit. Jeder Grund ist ein Satz mit Abhilfe, kein Code."""
    gruende = []
    lag = d.get("loop_lag") or {}
    if lag.get("aktiv") and (lag.get("p99_ms") or 0) >= 500:
        gruende.append("Event-Loop p99 %.0f ms — Stelle in /api/debug/threads "
                       "(loop_bremser)" % lag["p99_ms"])
    fd = ((d.get("gegendruck") or {}).get("fd")) or {}
    if fd.get("grenze", -1) > 0 and fd.get("offen", -1) >= 0.7 * fd["grenze"]:
        gruende.append("%d von %d Dateideskriptoren belegt — LimitNOFILE "
                       "pruefen oder Leck suchen" % (fd["offen"], fd["grenze"]))
    if (d.get("log_synchron") or 0) > 0:
        gruende.append("ein Log-Handler schreibt an der Schleuse vorbei — "
                       "error.log nennt ihn")
    if (d.get("log_wartend") or 0) < 0:
        gruende.append("Log-Schleuse laeuft nicht — Logging ist synchron")
    if d.get("laufstand") == "veraltet":
        gruende.append("Update eingespielt, aber nicht neu gestartet")
    if d.get("tunnel") == "fehler":
        gruende.append("Egress-Tunnel antwortet nicht")
    kinder = d.get("kinder") or {}
    if (kinder.get("aeltester_s") or 0) >= 1800:
        gruende.append("ein Hilfsprozess laeuft seit %.0f min — haengt im "
                       "Kernel (Platte?)" % (kinder["aeltester_s"] / 60.0))
    if not d.get("ok", True):
        return "gestoert", gruende
    return ("degradiert" if gruende else "ok"), gruende


# ═════════════════════════════════════════════════════════════════════════
# v4.2-W133: der Abbau, der nicht endet
# ═════════════════════════════════════════════════════════════════════════
#
# Der Stall-Dump vom 31.10. 00:35 zeigt den Hauptthread in
# `asyncio/runners.py:close` — `main()` war fertig, aufgeraeumt war auch.
# `asyncio.run` wartete beim Schliessen auf den Default-Executor, und ein
# Arbeiter darin hing in `urlopen` (nc/freeai.chat_sync aus
# nc/evolution.cycle). Mit `AI_TIMEOUT=0` darf so ein Aufruf 3600 s dauern.
# Der neue Prozess kam erst neun Minuten spaeter hoch; dazwischen stand
# kein einziger Grund im Log, nur der Fehlalarm "Event-Loop eingefroren".
#
# Die Arbeiter eines ThreadPoolExecutor sind keine Daemon-Threads, und die
# Standardbibliothek wartet beim Beenden auf jeden. Ein haengender
# Netzaufruf haelt damit den ganzen Prozess — bei systemd bis zum SIGKILL
# nach TimeoutStopSec, und ein SIGKILL ist fuer OnFailure= ein Fehlschlag.
#
# Die Wache wird erst gestellt, wenn `main()` fertig aufgeraeumt hat. Was
# danach noch laeuft, hat keine Arbeit mehr, nur einen Aufruf, auf dessen
# Antwort niemand wartet.

ABSCHIED_FRIST_S = 20.0


def haengende_threads() -> list:
    """Namen der Threads, auf die das Beenden warten wuerde: nicht-Daemon,
       ohne den Hauptthread. Die Wache selbst ist ein Daemon und faellt
       damit von allein heraus — ein eigener Ausschluss fuer sie war
       nachweislich wirkungslos (Mutationsprobe W133)."""
    import threading
    haupt = threading.main_thread()
    return sorted(t.name for t in threading.enumerate()
                  if t.is_alive() and not t.daemon and t is not haupt)


def abschiedswache(code: int, frist_s: float, beenden, melden=None,
                   schlafen=time.sleep):
    """Den Prozess nach `frist_s` beenden, falls er dann noch lebt.

    `beenden(code)` ist im Betrieb `os._exit`; `melden(text)` bekommt die
    Begruendung VOR dem Ende, damit sie im Log steht. Endet der Prozess
    vorher von selbst, stirbt die Wache als Daemon mit ihm — sie kostet im
    Normalfall nichts. `frist_s <= 0` schaltet sie ab. -> der Thread oder None.
    """
    import threading
    t = None

    def _lauf():
        schlafen(frist_s)
        namen = haengende_threads()
        if melden is not None:
            melden("Abbau haengt seit %.0f s an %s — der Prozess endet jetzt "
                   "hart mit Exitcode %d. Aufgeraeumt ist schon; was noch "
                   "laeuft, wartet auf einen Netzaufruf ohne kurzes Timeout "
                   "(AI_TIMEOUT=0 heisst 3600 s). Frist: ABSCHIED_FRIST_S."
                   % (frist_s, ", ".join(namen) or "keinem benannten Thread",
                      code))
        beenden(code)

    if frist_s and frist_s > 0:
        t = threading.Thread(target=_lauf, name="abschiedswache", daemon=True)
        t.start()
    return t
