"""nc.procdiag — Prozess-/Thread-Diagnose, aus bot_v37 herausgelöst (Phase-1-Zerlegung).

Drei pure, seiteneffektarme Helfer, die zur W83/W88-Observability gehören und
KEINEN geteilten Zustand mit dem Monolithen brauchen — daher als erster,
risikoarmer Schnitt ausgelagert. Verhalten bitgenau wie im Original; die
einzige Abhängigkeit (das Log-Verzeichnis) wird injiziert statt importiert, um
Zirkularität zu vermeiden. Der Monolith behält dünne Wrapper gleichen Namens,
sodass alle Aufrufer und Verträge unverändert bleiben.
"""

import os
import glob
import time
from datetime import datetime


def prune_stall_dumps(log_dir, keep: int = 10):
    """v4.0-W88: der Loop-Watchdog schreibt logs/loop_stall_*.txt — die häuften
       sich sonst unbegrenzt. Nur die neuesten `keep` behalten."""
    try:
        files = sorted(glob.glob(os.path.join(log_dir, "loop_stall_*.txt")),
                       key=os.path.getmtime)
        for f in (files[:-keep] if keep > 0 else files):
            try:
                os.remove(f)
            except OSError:
                pass
    except Exception:
        pass


def zombie_child_count() -> int:
    """v4.0-W88: Anzahl DEFUNKTER (Zombie-)Kindprozesse dieses Prozesses (Linux).
       Nur lesend über /proc — 0 auf Nicht-Linux oder bei Fehlern. Macht die
       W75-Zombie-Klasse beobachtbar, ohne den Prozess anzufassen."""
    try:
        mypid = os.getpid()
        n = 0
        for d in os.listdir("/proc"):
            if not d.isdigit():
                continue
            try:
                with open("/proc/%s/stat" % d) as fh:
                    parts = fh.read().rsplit(") ", 1)
                if len(parts) != 2:
                    continue
                fields = parts[1].split()
                state, ppid = fields[0], int(fields[1])
                if state == "Z" and ppid == mypid:
                    n += 1
            except (OSError, ValueError, IndexError):
                continue
        return n
    except Exception:
        return 0


def dump_all_threads(log_dir, reason: str = "manuell"):
    """v4.0-W88: Voll-Stack-Dump ALLER Threads ins Journal + Datei. Von SIGUSR1
       (on-demand) und vom Loop-Watchdog genutzt."""
    import faulthandler
    path = None
    try:
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, "threaddump_%d.txt" % int(time.time()))
        with open(path, "w") as fh:
            fh.write("THREAD-DUMP (%s) %s\n\n"
                     % (reason, datetime.now().isoformat(timespec="seconds")))
            faulthandler.dump_traceback(file=fh, all_threads=True)
    except Exception:
        pass
    try:
        faulthandler.dump_traceback(all_threads=True)
    except Exception:
        pass
    return path
