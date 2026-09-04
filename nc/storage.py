"""nc.storage — v4.1-W24: Speicherplatz melden und Aufnahmen aufraeumen.

Zwei Funktionen aus dem Monolithen, die je zwei Aufrufergruppen hatten: das
Dashboard-Widget (`/api/storage`) und der stuendliche Aufraeumlauf, sowie der
Gesundheitswert, der `disk.used_percent` liest. Beim Herausloesen der Routen
waere `cleanup()` sonst kopiert worden — sie **loescht Dateien**, und
Kopien loeschender Funktionen laufen irgendwann auseinander.

**Die Verzeichnisse kommen als Argument herein**, nicht aus os.getenv: der
Aufrufer kennt sie schon, und ein zweiter Lesepfad waere eine zweite Wahrheit
ueber die beiden wichtigsten Verzeichnisse des Bestands.

`cleanup()` loescht Dateien, **nicht** die Datenbankeintraege. Das ist
Absicht: der Betreiber soll weiter sehen, dass es die Aufnahme gab — sie ist
nur nicht mehr abrufbar. Wer hier ein DELETE ergaenzt, nimmt ihm die
Historie. (Die andere Richtung — Eintrag UND Datei weg — macht bewusst
nc/retention.py.)
"""

import logging
import os
import shutil
import time

from nc.dbwrap import db_conn
from nc.stats import _dir_stats

log = logging.getLogger("TikTokBot")


def stats(recordings_dir: str, archive_dir: str = "",
          retain_days: int = 0) -> dict:
    """Dashboard-Widget-Daten. Liefert Recordings + Archive + freier Platz."""
    rec_stats = _dir_stats(recordings_dir)
    arch_stats = _dir_stats(archive_dir) if archive_dir else {"exists": False}
    # Freier Platz auf der Disk wo recordings_dir liegt
    try:
        st = shutil.disk_usage(recordings_dir if os.path.isdir(recordings_dir) else ".")
        # B1-Fix: used_percent ergänzen. api_health_score und api_ai_diagnose
        # haben das Feld erwartet, fanden es aber nie — Disk-Component im
        # Health-Score blieb deshalb permanent bei 70/100 mit Note "?".
        used_pct = round(st.used / st.total * 100, 1) if st.total else None
        disk = {"total_bytes": st.total, "used_bytes": st.used,
                "free_bytes": st.free, "used_percent": used_pct}
    except Exception as e:
        log.warning(f"disk_usage failed: {e}")
        disk = {"total_bytes": None, "used_bytes": None,
                "free_bytes": None, "used_percent": None}
    # DB-Count der Recording-Einträge (Datei evt. gelöscht aber DB-Eintrag bleibt)
    try:
        with db_conn() as conn:
            db_count = conn.execute("SELECT COUNT(*) AS c FROM recordings").fetchone()
            db_count = db_count["c"] if db_count else 0
    except Exception as e:
        log.warning(f"recordings count failed: {e}")
        db_count = None
    return {
        "recordings_dir": rec_stats,
        "archive_dir":    arch_stats,
        "disk":           disk,
        "db_recording_count": db_count,
        "retention_days": retain_days,
    }

def cleanup(recordings_dir: str, days: int = 0,
            dry_run: bool = False) -> dict:
    """Löscht Recordings-Files älter als `days` Tage von Disk. DB-Einträge
       werden NICHT gelöscht (User kann immer noch sehen dass es Aufnahmen
       gab — sie sind nur nicht mehr abrufbar). Wenn dry_run=True: zählt nur.

       Aufrufer: hourly background task (wenn retain_days > 0)
       oder manueller Dashboard-Button."""
    if days <= 0:
        return {"deleted": 0, "freed_bytes": 0, "skipped": 0, "errors": 0,
                "reason": "RECORDINGS_RETAIN_DAYS=0 (cleanup disabled)"}
    if not os.path.isdir(recordings_dir):
        return {"deleted": 0, "freed_bytes": 0, "skipped": 0, "errors": 0,
                "reason": f"{recordings_dir} does not exist"}
    cutoff = time.time() - (days * 86400)
    deleted = 0; freed = 0; skipped = 0; errors = 0
    try:
        for entry in os.scandir(recordings_dir):
            if not entry.is_file(follow_symlinks=False):
                continue
            try:
                st = entry.stat(follow_symlinks=False)
            except OSError:
                errors += 1; continue
            if st.st_mtime >= cutoff:
                skipped += 1; continue
            if dry_run:
                deleted += 1; freed += st.st_size
                continue
            try:
                os.remove(entry.path)
                deleted += 1; freed += st.st_size
            except OSError as e:
                log.warning(f"cleanup_old_recordings: {entry.path}: {e}")
                errors += 1
    except OSError as e:
        log.warning(f"cleanup_old_recordings scandir: {e}")
        return {"deleted": deleted, "freed_bytes": freed, "skipped": skipped,
                "errors": errors + 1, "error": str(e)}
    return {"deleted": deleted, "freed_bytes": freed, "skipped": skipped,
            "errors": errors, "dry_run": dry_run, "retain_days": days}
