"""nc.gegendruck — v4.2-W118: abregeln mit Ansage statt still ueberlaufen.

════════════════════════════════════════════════════════════════════════
DIE DREI LUECKEN
════════════════════════════════════════════════════════════════════════
**Kein Deckel fuer Aufnahmen.** Restreams sind seit V37-MAXLIVE auf
`RESTREAM_MAX_CONCURRENT` gedeckelt, Aufnahmen auf gar nichts. Jede
Aufnahme ist ein ffmpeg mit zwei Pipes in den Bot, ein Schreibstrom auf
die Platte und ein Abschluss-Task. Gehen nach einem Neustart oder an
einem Abend 40 Nutzer gleichzeitig live, startet der Bot 40 Prozesse —
und was dann zuerst ausgeht, entscheidet der Zufall.

**Die Dateideskriptoren gingen zuerst aus.** Die Unit aus
tools/installer.sh setzte kein `LimitNOFILE`, der Bot hob nichts an:
der Dienst lief mit dem Soft-Limit **1024**. Ein voller fd-Tisch meldet
sich nicht als "zu viele Aufnahmen", sondern ueberall gleichzeitig und
nirgends verstaendlich — `sqlite3.OperationalError: unable to open
database file`, aiohttp ohne Verbindung, ffmpeg-Start mit `EMFILE`,
und `WATCHDOG_FD_WARN` (800) warnte erst knapp davor.

**Eine volle Pruef-Schlange verwarf still.** `check_all_trackings`
schob bei `QueueFull` den aeltesten Eintrag hinaus — ohne Zeile. Der
verworfene Nutzer wurde danach erst nach dem In-Flight-Riegel wieder
geprueft; ein Live-Start konnte so Minuten zu spaet erkannt werden, und
niemand erfuhr, dass die Worker nicht nachkommen.

════════════════════════════════════════════════════════════════════════
WAS DIESES MODUL ENTSCHEIDET
════════════════════════════════════════════════════════════════════════
Nur die Entscheidung und die Zahlen — kein Prozess, kein Log, kein Bot.
`bot.py` fragt vor jedem Start und meldet die Antwort ueber
nc.meldetakt. Eine abgewiesene Aufnahme nimmt KEINEN Lock: der naechste
Poll (30 s fuer einen Live-Nutzer) fragt von selbst wieder, sobald ein
Platz frei ist. Abregeln heisst hier verzoegern, nicht verlieren.

Rangfolge bei der Abweisung: die fd-Sperre vor dem Deckel. Ein voller
fd-Tisch ist die Lage, in der der Bot gleich auch Datenbank und Netz
verliert — sie ist die eigentliche Nachricht.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import threading
from typing import Optional, Tuple

# `resource` gibt es nur auf POSIX. Ueber find_spec statt ueber einen
# ImportError-Auffang: wo es fehlt, ist das keine Stoerung, sondern die
# Plattform — und ein stiller `except` waere hier nicht von einer echten
# Stoerung zu unterscheiden.
_resource = (importlib.import_module("resource")
             if importlib.util.find_spec("resource") else None)
_PROC_FD = "/proc/self/fd"

# Ab diesem Anteil des Soft-Limits wird kein neuer Kindprozess mehr
# gestartet. 85 % lassen bei 1024 rund 150 fds fuer Datenbank, Sockets und
# Logdateien — genug, damit der Bot seine eigene Lage noch melden kann.
FD_SPERRE_ANTEIL = 0.85

# Hoechstens so weit wird das Soft-Limit angehoben. Mehr braucht kein
# realistischer Bestand, und ein Limit in der Groessenordnung des
# Hard-Limits (524288 unter systemd) macht aus einem fd-Leck einen
# Speicherverbrauch, den man erst am OOM-Kill bemerkt.
FD_ZIEL = 65536

_SPERRE = threading.Lock()
ZAEHLER = {"abgewiesen": {}, "verworfen": 0}


def deckel_auto(kerne: Optional[int] = None) -> int:
    """Vorgabe fuer MAX_PARALLEL_AUFNAHMEN=0: vier je Kern, mindestens acht.

    Eine Aufnahme mit `-c copy` kostet kaum CPU; was sie begrenzt, sind
    Plattenstroeme und fds. Vier je Kern ist auf der 8-Kern-Box 32 — weit
    ueber dem gemessenen Alltag, und genau dafuer gedacht: ein Riegel gegen
    den Ausreisser, nicht eine Drossel fuer den Normalbetrieb."""
    k = kerne if kerne is not None else (os.cpu_count() or 2)
    return max(8, 4 * int(k))


def fd_lage() -> dict:
    """Offene Dateideskriptoren gegen das Soft-Limit. -> {offen, grenze, anteil}

    `offen` ist -1, wenn das System es nicht verraet (kein /proc, Windows) —
    dann sperrt nichts. Eine unbekannte Lage darf keine Aufnahme kosten."""
    offen = len(os.listdir(_PROC_FD)) if os.path.isdir(_PROC_FD) else -1
    grenze = (int(_resource.getrlimit(_resource.RLIMIT_NOFILE)[0])
              if _resource is not None else -1)
    anteil = (offen / grenze) if (offen >= 0 and grenze > 0) else 0.0
    return {"offen": offen, "grenze": grenze, "anteil": round(anteil, 3)}


def fd_grenze_anheben(ziel: int = FD_ZIEL) -> Tuple[int, int]:
    """Soft-Limit fuer Dateideskriptoren bis zum Hard-Limit anheben.
       -> (vorher, nachher). Gleich heisst: nichts zu tun oder nicht moeglich.

    Im Prozess und nicht nur in der Unit: der Betreiber spielt Updates
    ueber nc/updater ein, und der Installer laeuft dabei nie wieder. Eine
    Abhilfe, die nur in der Unit steht, erreicht keine bestehende
    Installation."""
    resource = _resource
    if resource is None:
        return (-1, -1)
    weich, hart = resource.getrlimit(resource.RLIMIT_NOFILE)
    obergrenze = int(ziel) if hart == resource.RLIM_INFINITY else min(int(hart), int(ziel))
    if weich != resource.RLIM_INFINITY and weich < obergrenze:
        resource.setrlimit(resource.RLIMIT_NOFILE, (obergrenze, hart))
        return (int(weich), obergrenze)
    return (int(weich), int(weich))


def start_entscheiden(aktiv: int, deckel: int,
                      fd: Optional[dict] = None) -> Tuple[bool, str, str]:
    """Darf ein weiterer Kindprozess starten? -> (erlaubt, grund, text)

    `deckel` <= 0 heisst: kein Deckel (nur die fd-Sperre gilt). `grund` ist
    ein festes Vokabular ("fd", "deckel", ""), damit die Drossel in
    nc.meldetakt am Paar (Kanal, Grund) greifen kann."""
    # Ein unbekanntes `offen` (-1) erreicht die Schwelle nie; eine eigene
    # Pruefung darauf waere ein zweiter Riegel ohne Wirkung (die
    # Mutationsprobe hat genau das gezeigt). Die Grenze muss bekannt sein,
    # sonst waere 0.85 * -1 eine Schwelle, die alles sperrt.
    if fd and fd.get("grenze", -1) > 0 \
            and fd.get("offen", -1) >= FD_SPERRE_ANTEIL * fd["grenze"]:
        return (False, "fd",
                "%d von %d Dateideskriptoren belegt (%.0f %%) — kein neuer "
                "Prozess, sonst verliert der Bot gleich auch Datenbank und Netz. "
                "Abhilfe: LimitNOFILE=65536 in der systemd-Unit und Neustart; "
                "steigt die Zahl ohne neue Aufnahmen weiter, ist es ein Leck "
                "(/api/debug/threads)."
                % (fd["offen"], fd["grenze"], 100.0 * fd["offen"] / fd["grenze"]))
    if deckel > 0 and aktiv >= deckel:
        return (False, "deckel",
                "%d Aufnahmen laufen, Deckel %d erreicht — die naechste startet, "
                "sobald eine endet (der Live-Check fragt alle 30 s neu). "
                "Abhilfe, wenn die Box mehr traegt: MAX_PARALLEL_AUFNAHMEN "
                "erhoehen." % (aktiv, deckel))
    return (True, "", "")


def abgewiesen(art: str, grund: str) -> None:
    with _SPERRE:
        k = art + ":" + grund
        ZAEHLER["abgewiesen"][k] = ZAEHLER["abgewiesen"].get(k, 0) + 1


def verworfen() -> int:
    """Einen aus der vollen Pruef-Schlange verworfenen Eintrag zaehlen."""
    with _SPERRE:
        ZAEHLER["verworfen"] += 1
        return ZAEHLER["verworfen"]


def lage(aktiv: int, deckel: int, schlange: int = -1,
         schlange_max: int = -1) -> dict:
    """Fuer /healthz: Zahlen, keine Namen. Liest /proc einmal."""
    with _SPERRE:
        abw = dict(ZAEHLER["abgewiesen"])
        verw = ZAEHLER["verworfen"]
    return {"aufnahmen": int(aktiv), "aufnahmen_deckel": int(deckel),
            "fd": fd_lage(), "abgewiesen": abw,
            "pruef_schlange": int(schlange), "pruef_schlange_max": int(schlange_max),
            "pruef_verworfen": verw}


def zuruecksetzen() -> None:
    """Nur fuer die Vertraege."""
    with _SPERRE:
        ZAEHLER["abgewiesen"] = {}
        ZAEHLER["verworfen"] = 0
