"""nc.archive — Archiv-Regeln, Retention, Duplikat-Scan.

Extrahiert aus bot_v37.py. Reine Datei-/DB-Logik ohne Bot-Globals."""

import logging
from datetime import datetime, timezone, timedelta  # noqa: F401
import os

from hashlib import md5 as _md5, sha256 as _sha256
from typing import Optional

from nc.dbwrap import db_conn
from nc.sqlutil import _archive_where_clause, _archive_sort_clause

log = logging.getLogger("TikTokBot")


def run_archive_file_check():
    """F38: Geht ALLE Archive-DB-Einträge durch und prüft ob die Datei
       physisch existiert. Liefert {missing: [{id, filename, filepath}, ...],
       checked: N, missing_count: M, total_size_missing}.
       Read-only — entfernt nichts. Der User entscheidet was mit fehlenden
       Einträgen passieren soll.
    """
    missing = []
    checked = 0
    total_size_missing = 0
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, filename, filepath, size_bytes, created_at "
                "FROM archive ORDER BY id DESC").fetchall()
        for r in rows:
            checked += 1
            fp = r["filepath"]
            if not fp or not os.path.exists(fp):
                missing.append({
                    "id":         r["id"],
                    "filename":   r["filename"],
                    "filepath":   fp or "",
                    "size_bytes": r["size_bytes"] or 0,
                    "created_at": (r["created_at"] or "")[:19].replace("T", " "),
                })
                total_size_missing += (r["size_bytes"] or 0)
    except Exception as e:
        log.warning(f"run_archive_file_check failed: {e}")
    return {
        "checked":            checked,
        "missing_count":      len(missing),
        "total_size_missing": total_size_missing,
        "missing":            missing,
    }


def evaluate_archive_rule(condition: dict, recording_row) -> bool:
    """Sehr einfache rule-engine. Conditions:
       {min_size_mb: 50}   → file_size >= 50 MB
       {username_contains: "music"}
       {min_duration_secs: 600}
       {username_in: ["alice", "bob"]}
       Operator AND-verknüpft alle keys."""
    try:
        size_mb = (recording_row.get("file_size") or 0) / 1024 / 1024
        if "min_size_mb" in condition:
            if size_mb < float(condition["min_size_mb"]): return False
        if "max_size_mb" in condition:
            if size_mb > float(condition["max_size_mb"]): return False
        if "min_duration_secs" in condition:
            d = recording_row.get("duration_secs") or 0
            if d < int(condition["min_duration_secs"]): return False
        if "username_contains" in condition:
            u = (recording_row.get("username") or "").lower()
            if str(condition["username_contains"]).lower() not in u: return False
        if "username_in" in condition:
            wanted = [str(x).lower() for x in (condition["username_in"] or [])]
            if (recording_row.get("username") or "").lower() not in wanted:
                return False
        return True
    except Exception as e:
        log.debug(f"evaluate_archive_rule: {e}")
        return False


def get_archive_entries_paged(*, page=1, per_page=25, sort='date', direction='desc',
                              kind='all', query=None, date_from=None, date_to=None):
    """F38: Liefert (entries, total_filtered, total_all).
       - entries: nur die aktuelle Seite
       - total_filtered: Anzahl nach Filter (für Pagination-Header)
       - total_all: Anzahl insgesamt (für Header-Stat)
    """
    page = max(1, int(page))
    per_page = max(1, min(int(per_page), 200))   # hard cap damit niemand 10k zieht
    offset = (page - 1) * per_page

    where_sql, params = _archive_where_clause(kind=kind, query=query, date_from=date_from, date_to=date_to)
    order_sql = _archive_sort_clause(sort, direction)

    try:
        with db_conn() as conn:
            total_all = conn.execute("SELECT COUNT(*) FROM archive").fetchone()[0]
            total_filtered_row = conn.execute(
                f"SELECT COUNT(*) FROM archive {where_sql}", params).fetchone()
            total_filtered = total_filtered_row[0] if total_filtered_row else 0
            rows = conn.execute(
                f"SELECT id, filename, filepath, title, notes, size_bytes, "
                f"mime_type, source_url, created_at FROM archive "
                f"{where_sql} {order_sql} LIMIT ? OFFSET ?",
                params + [per_page, offset]).fetchall()
            return rows, total_filtered, total_all
    except Exception as e:
        log.warning(f"get_archive_entries_paged failed: {e}")
        return [], 0, 0


def _retention_match(rules):
    """Wählt Aufnahmen die eine Retention-Regel treffen WÜRDEN (Vorschau).
       rules: {older_than_days, min_mb, keep_rated, keep_starred, keep_label}"""
    # BUG-FIX: int()/float() auf User-Input wirft ValueError bei nicht-numerischen
    # Werten → unkontrollierter 500. Außerdem: older_than_days=999999 erzeugt
    # einen datetime vor Unix-Epoch → falsche SQLite-Ergebnisse.
    try:
        older = max(0, min(int(rules.get("older_than_days") or 0), 3650))
    except (ValueError, TypeError):
        older = 0
    try:
        min_mb = max(0.0, float(rules.get("min_mb") or 0))
    except (ValueError, TypeError):
        min_mb = 0.0
    keep_rated = bool(rules.get("keep_rated"))
    keep_starred = bool(rules.get("keep_starred", True))
    keep_label = (rules.get("keep_label") or "").strip()
    cond = ["1=1"]
    params = []
    if older > 0:
        cut = (datetime.now(timezone.utc) - timedelta(days=older)).isoformat()
        cond.append("created_at < ?")
        params.append(cut)
    if min_mb > 0:
        cond.append("file_size >= ?")
        params.append(int(min_mb * 1048576))
    if keep_starred:
        cond.append("COALESCE(starred,0)=0")
    if keep_rated:
        cond.append("rating IS NULL")
    if keep_label:
        cond.append("COALESCE(label,'') <> ?")
        params.append(keep_label)
    sql = ("SELECT id, username, filepath, created_at, file_size, rating, starred, label "
           "FROM recordings WHERE " + " AND ".join(cond) + " ORDER BY created_at ASC LIMIT 1000")
    with db_conn() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def _scan_for_duplicates(scan_root, full_hash_max_bytes=100 * 1024 * 1024):
    """Returns (dup_groups, stats) für scan_root."""
    if not os.path.isdir(scan_root):
        return [], {"error": f"directory not found: {scan_root}"}

    files_by_size = {}
    scan_count = 0
    for root, dirs, files in os.walk(scan_root):
        # Skip hidden + tmp dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "tmp"]
        for fname in files:
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)
            try:
                sz = os.path.getsize(fpath)
                if sz == 0:
                    continue
                files_by_size.setdefault(sz, []).append(fpath)
                scan_count += 1
            except OSError:
                continue

    dup_groups = []
    hash_calls = 0
    for size, paths in files_by_size.items():
        if len(paths) < 2:
            continue
        # Same size = potential dups → hash
        hashes = {}
        for p in paths:
            try:
                h = _md5(usedforsecurity=False)  # Datei-Dedup, KEIN Security-Hash → FIPS-sicher + dokumentiert Intent
                with open(p, "rb") as f:
                    if size <= full_hash_max_bytes:
                        # full hash
                        for chunk in iter(lambda: f.read(65536), b""):
                            h.update(chunk)
                        key = h.hexdigest()
                    else:
                        # header-hash für große Dateien (first MB)
                        h.update(f.read(1024 * 1024))
                        key = h.hexdigest() + "_hdr"
                hashes.setdefault(key, []).append(p)
                hash_calls += 1
            except OSError:
                continue
        for key, paths_with_same_hash in hashes.items():
            if len(paths_with_same_hash) >= 2:
                dup_groups.append({
                    "size_bytes": size,
                    "size_mb": round(size / 1024 / 1024, 2),
                    "hash": key,
                    "partial_hash": key.endswith("_hdr"),
                    "count": len(paths_with_same_hash),
                    "wasted_bytes": size * (len(paths_with_same_hash) - 1),
                    "files": [{
                        "path": p,
                        "name": os.path.basename(p),
                        "dir": os.path.dirname(p),
                        "mtime": int(os.path.getmtime(p)),
                    } for p in sorted(paths_with_same_hash)],
                })

    # Sort by wasted space (biggest savings first)
    dup_groups.sort(key=lambda g: g["wasted_bytes"], reverse=True)
    return dup_groups, {
        "scanned_files": scan_count,
        "hash_computed_for": hash_calls,
        "duplicate_groups": len(dup_groups),
        "total_wasted_bytes": sum(g["wasted_bytes"] for g in dup_groups),
    }


def compute_recording_fingerprint(filepath: str,
                                   sample_bytes: int = 1024 * 1024) -> Optional[str]:
    """SHA256 von den ersten N Bytes. Bei kompletten Duplikaten reicht das
       (Stream-Anfang ist identisch). Vollständiger Hash wäre teuer für
       GB-große Files."""
    try:
        h = _sha256()
        with open(filepath, "rb") as f:
            chunk = f.read(sample_bytes)
            if not chunk: return None
            h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        log.debug(f"compute_recording_fingerprint({filepath}): {e}")
        return None
