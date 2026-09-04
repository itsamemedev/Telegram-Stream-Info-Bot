"""nc.retention — v4.1-W24: Aufnahmen älter als N Tage finden und löschen.

Vorher stand das als `_retention_scan` im Monolithen und hatte zwei Aufrufer:
die Dauerschleife `_retention_loop` und die beiden Routen unter
`/api/retention`. Beim Herauslösen der Routen wäre daraus eine Kopie geworden
— und eine Kopie einer LÖSCHENDEN Funktion ist genau die Art Duplikat, die
irgendwann auseinanderläuft. Deshalb wandert die Logik hierher, und beide
Aufrufer rufen dieselbe Funktion.

════════════════════════════════════════════════════════════════════════
DIE HÄRTUNG IST DER KERN, NICHT BEIWERK
════════════════════════════════════════════════════════════════════════
`scan(..., delete=True)` löscht Dateien. Gelöscht wird ausschliesslich, was
per `os.path.abspath` nachweislich INNERHALB des Aufnahme-Verzeichnisses
liegt. Der Pfad kommt aus der Datenbank, und ein `filepath`, der dort
irgendwann mit `../` oder als absoluter Systempfad landet, würde sonst
mitgelöscht. Ein Vertrag hält die Prüfung fest — wer sie entfernt, baut aus
einer Aufräumfunktion ein Löschwerkzeug für das ganze Dateisystem.

Der Aufnahme-Ordner wird als Argument übergeben, nicht hier gelesen: der
Aufrufer weiss ihn schon, und ein zweiter os.getenv-Pfad wäre eine zweite
Wahrheit über das wichtigste Verzeichnis des Bestands.
"""

import logging
import os
from datetime import datetime, timedelta, timezone

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")


def scan(days, recordings_dir, delete=False):
    """Aufnahmen älter als `days` Tage zählen und optional löschen.

    -> {"count": int, "freed_bytes": int}

    Fehler werden geschluckt und auf debug geloggt — das ist ein Aufräumpfad,
    dessen Fehlschlag folgenlos ist (CLAUDE.md nennt genau das als die
    legitime Ausnahme vom Verbot stiller except-Blöcke). Der Rückgabewert
    bleibt in jedem Fall wohlgeformt; die Routen rechnen mit ihm.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rec_root = os.path.abspath(recordings_dir)
    freed = 0
    count = 0
    removed = []
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, filepath FROM recordings WHERE created_at < ?",
                (cutoff,)).fetchall()
            for r in rows:
                fp = r["filepath"] or ""
                # Härtung: nur echte Dateien im Aufnahme-Verzeichnis
                # zählen/löschen. Siehe Modul-Kopf — diese vier Zeilen sind
                # der Unterschied zwischen Aufräumen und Datenverlust.
                try:
                    safe = bool(fp) and os.path.abspath(fp).startswith(rec_root + os.sep)
                except Exception:
                    safe = False
                if not (safe and os.path.isfile(fp)):
                    continue
                sz = 0
                try:
                    sz = os.path.getsize(fp)
                except Exception:
                    pass
                count += 1
                freed += sz
                if delete:
                    try:
                        os.remove(fp)
                        removed.append(r["id"])
                    except Exception as e:
                        log.debug("retention rm %s: %s", fp, e)
            if delete and removed:
                marks = ",".join("?" * len(removed))
                conn.execute("DELETE FROM recordings WHERE id IN (" + marks + ")",
                             removed)
    except Exception as e:
        log.debug("retention scan: %s", e)
    return {"count": count, "freed_bytes": freed}
