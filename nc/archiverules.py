"""nc.archiverules — v4.1-W24: die Auto-Archiv-Regeln, Datenzugriff und Anwendung.

Vier Funktionen, die im Monolithen zwei Aufrufergruppen hatten: die drei
Routen unter `/api/auto-archive-rules` und den Regel-Lauf aus dem
Wartungspfad. Beim Herauslösen der Routen wäre `run_archive_rules` sonst
kopiert worden — eine Funktion, die **Dateien anfasst und Datenbankstände
fortschreibt**, ist der schlechteste Kandidat für ein Duplikat.

Die eigentliche Bedingungsauswertung liegt schon seit W110 in
nc/archive.py (`evaluate_archive_rule`), der Dateinamen-Schutz in
nc/textmore.py (`_safe_archive_filename`). Dieses Modul klammert beides mit
dem Datenzugriff zusammen.

**`archive_dir` und `log_event` kommen als Argument herein**, nicht aus einer
Modul-Konstante: das Archivverzeichnis ist eine .env-Einstellung des
Monolithen, und das Ereignisprotokoll kann nur der laufende Bot schreiben.
Ohne `log_event` läuft der Regel-Lauf trotzdem — er protokolliert dann nur
nicht, statt zu scheitern.

Im Fehlertext und im Kommentar steht weiterhin **ARCHIVE_DIR**, obwohl der
Parameter `archive_dir` heisst: der Betreiber sucht die .env-Variable, nicht
den Python-Namen. Ein blindes Umbenennen hätte genau das zerlegt (die Falle
aus W22, dort per ast.parse gefangen).
"""

import json
import logging
import os
import shutil
from datetime import datetime, timezone
from typing import Optional

from nc.archive import add_archive_entry, evaluate_archive_rule
from nc.dbwrap import db_conn
from nc.textmore import _safe_archive_filename

log = logging.getLogger("TikTokBot")


def list_archive_rules() -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, name, condition_json, action_json, enabled, "
                "       last_run, last_match_count, created_at "
                "FROM auto_archive_rules ORDER BY id DESC").fetchall()
    except Exception:
        return []

def add_archive_rule(name: str, condition: dict, action: dict) -> Optional[int]:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "INSERT INTO auto_archive_rules "
                "(name, condition_json, action_json, enabled, created_at) "
                "VALUES (?,?,?,1,?)",
                (name[:200],
                 json.dumps(condition, ensure_ascii=False)[:2000],
                 json.dumps(action, ensure_ascii=False)[:2000],
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        log.warning(f"add_archive_rule: {e}")
        return None

def delete_archive_rule(rule_id: int) -> bool:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "DELETE FROM auto_archive_rules WHERE id=?", (rule_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception:
        return False


def run_archive_rules(rule_id: Optional[int] = None, archive_dir: str = "",
                      log_event=None) -> dict:
    """Wendet eine oder alle aktiven Regeln an. Action: 'copy_to_archive'
       (zur Zeit einzige supported action)."""
    if not archive_dir:
        return {"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}
    rules = list_archive_rules()
    if rule_id is not None:
        rules = [r for r in rules if r["id"] == rule_id]
    if not rules:
        return {"ok": True, "processed": 0, "results": []}
    try:
        with db_conn() as conn:
            recs = conn.execute(
                "SELECT id, username, filepath, file_size, duration_secs, created_at "
                "FROM recordings WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 5000"
            ).fetchall()
    except Exception as e:
        return {"ok": False, "error": str(e)}

    results = []
    for rule in rules:
        if not rule["enabled"]: continue
        try:
            cond = json.loads(rule["condition_json"] or "{}")
            act = json.loads(rule["action_json"] or "{}")
        except Exception:
            continue
        action_kind = (act.get("action") or "").lower()
        matched = []
        archived = 0
        skipped = 0
        for r in recs:
            row_dict = {"id": r["id"], "username": r["username"],
                        "filepath": r["filepath"], "file_size": r["file_size"],
                        "duration_secs": r["duration_secs"]}
            if not evaluate_archive_rule(cond, row_dict):
                continue
            matched.append(r["id"])
            if action_kind != "copy_to_archive":
                continue
            # Copy zu ARCHIVE_DIR — nur wenn noch nicht da
            src = r["filepath"]
            if not src or not os.path.isfile(src):
                skipped += 1; continue
            try:
                base = os.path.basename(src)
                fname = _safe_archive_filename(base)
                # Skip wenn schon eingespielt (gleicher Filename existiert)
                target = os.path.join(archive_dir, fname)
                if os.path.exists(target):
                    # Schon vorhanden — skip
                    skipped += 1; continue
                shutil.copy2(src, target)
                size = os.path.getsize(target)
                add_archive_entry(
                    filename=fname, filepath=target,
                    title=None, notes=f"auto-archive von rule '{rule['name']}'",
                    size=size, mime=None,
                    source_url=f"recording/{r['id']}")
                archived += 1
            except Exception as e:
                skipped += 1
                log.warning(f"archive rule '{rule['name']}' on rec#{r['id']}: {e}")
        try:
            with db_conn() as conn:
                conn.execute(
                    "UPDATE auto_archive_rules SET last_run=?, last_match_count=? WHERE id=?",
                    (datetime.now(timezone.utc).isoformat(), len(matched), rule["id"]))
                conn.commit()
        except Exception: pass
        results.append({
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "matched": len(matched),
            "archived": archived,
            "skipped": skipped,
        })
        # Ohne laufenden Bot gibt es kein Ereignisprotokoll — das ist kein
        # Grund, den Regel-Lauf scheitern zu lassen.
        if log_event:
            log_event("archive.rule.run", "info",
                      f"Rule '{rule['name']}': matched={len(matched)} "
                      f"archived={archived}",
                      {"rule_id": rule["id"], "matched": len(matched),
                       "archived": archived})
    return {"ok": True, "processed": len(results), "results": results}
