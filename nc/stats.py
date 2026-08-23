"""nc.stats — Auswertungen & Kennzahlen (reine DB-Aggregation).

Extrahiert aus bot_v37.py, nachdem db_conn() nach nc.dbwrap gewandert
ist — dadurch hängen diese Funktionen an KEINEM Bot-Global mehr."""

import logging
import time as _time_mod
from datetime import datetime, timezone, timedelta  # noqa: F401
import os

from nc.dbwrap import db_conn
from nc.textmore import _parse_iso

log = logging.getLogger("TikTokBot")


def get_per_user_stats(limit: int = 20, sort_by: str = "rec_count") -> list:
    """Per-User-Aggregat über alle Trackings. Liefert eine Liste mit:
       - username, tracking_count (in wie vielen Chats getrackt)
       - rec_count, total_bytes, last_recording_at
       - attempt_count, attempt_ok_count, attempt_fail_count, success_rate
       - last_attempt_outcome
       sort_by ∈ {'rec_count', 'total_bytes', 'success_rate', 'last_recording'}"""
    valid_sorts = {
        "rec_count":      "rec_count DESC",
        "total_bytes":    "total_bytes DESC",
        "success_rate":   "success_rate DESC",
        "last_recording": "last_recording_at DESC",
    }
    order = valid_sorts.get(sort_by, "rec_count DESC")
    # F48: portable Aggregation. Wir machen drei Queries und mergen in Python
    # statt einer JOIN-Bombe — einfacher zu lesen + spielt mit SQLite und
    # MariaDB gleich gut.
    with db_conn() as conn:
        # 1. Recordings pro User (nur die Disk-Einträge zählen)
        rec_rows = conn.execute(
            "SELECT username, COUNT(*) AS rec_count, "
            "MAX(created_at) AS last_recording_at "
            "FROM recordings GROUP BY username").fetchall()
        rec_map = {r["username"]: (r["rec_count"], r["last_recording_at"])
                   for r in rec_rows}

        # 2. Attempts: Erfolge vs Fehler
        att_rows = conn.execute(
            "SELECT username, "
            "COUNT(*) AS attempts, "
            "SUM(CASE WHEN outcome IN ('ok', 'stall_killed_partial') THEN 1 ELSE 0 END) AS ok_count "
            "FROM recording_attempts GROUP BY username").fetchall()
        att_map = {}
        for r in att_rows:
            att = r["attempts"] or 0
            ok = r["ok_count"] or 0
            att_map[r["username"]] = (att, ok)

        # 3. Letzter Outcome je User
        last_outcome = {}
        last_rows = conn.execute(
            "SELECT username, outcome FROM recording_attempts "
            "WHERE id IN (SELECT MAX(id) FROM recording_attempts GROUP BY username)"
        ).fetchall()
        for r in last_rows:
            last_outcome[r["username"]] = r["outcome"]

        # 4. Tracking-Counts pro User
        tr_rows = conn.execute(
            "SELECT username, COUNT(*) AS tc FROM trackings GROUP BY username"
        ).fetchall()
        tr_map = {r["username"]: r["tc"] for r in tr_rows}

        # 5. Recording-Bytes-Summe per User — aus recording_attempts
        # (recordings-Tabelle hat keinen size_bytes-Spalte)
        size_rows = conn.execute(
            "SELECT username, SUM(file_size) AS total FROM recording_attempts "
            "WHERE outcome IN ('ok', 'stall_killed_partial') AND file_size > 0 "
            "GROUP BY username").fetchall()
        size_map = {r["username"]: (r["total"] or 0) for r in size_rows}

    # Union der Usernames
    all_users = set(rec_map) | set(att_map) | set(tr_map)
    result = []
    for u in all_users:
        rc, last_rec = rec_map.get(u, (0, None))
        att, ok = att_map.get(u, (0, 0))
        sr = (ok / att) if att else 0.0
        result.append({
            "username": u,
            "tracking_count": tr_map.get(u, 0),
            "rec_count": rc,
            "total_bytes": size_map.get(u, 0),
            "last_recording_at": last_rec,
            "attempt_count": att,
            "attempt_ok_count": ok,
            "attempt_fail_count": att - ok,
            "success_rate": round(sr, 3),
            "last_attempt_outcome": last_outcome.get(u),
        })

    # F48-Bug-Fix B4: Sort. None-Werte für last_recording_at MÜSSEN ans Ende
    # (User die nie aufgenommen wurden gehören nicht ganz oben). Vorher hat
    # die Lambda das genau umgekehrt gemacht. Auch die anderen Lambdas
    # robuster gegen None gemacht.
    if order == "last_recording_at DESC":
        # Zwei Gruppen: mit Wert (DESC sortieren), ohne Wert (alphabetisch).
        with_val = [r for r in result if r["last_recording_at"]]
        no_val   = [r for r in result if not r["last_recording_at"]]
        with_val.sort(key=lambda x: x["last_recording_at"], reverse=True)
        no_val.sort(key=lambda x: x["username"])
        result = with_val + no_val
    else:
        sort_fns = {
            "rec_count DESC":    lambda x: (-(x["rec_count"] or 0), x["username"]),
            "total_bytes DESC":  lambda x: (-(x["total_bytes"] or 0), x["username"]),
            "success_rate DESC": lambda x: (-(x["success_rate"] or 0),
                                            -(x["rec_count"] or 0), x["username"]),
        }
        result.sort(key=sort_fns.get(order, sort_fns["rec_count DESC"]))
    return result[:limit]


def get_activity_pulse(minutes: int = 60) -> list:
    """1min-Buckets über die letzten N Minuten:
       - recording_attempts started
       - recording_attempts ended (success)
       - recording_attempts ended (fail)
       Returns list of {minute_ago, started, ok, fail}."""
    minutes = max(5, min(int(minutes or 60), 1440))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=minutes)
    buckets = {}
    for i in range(minutes):
        bucket_time = now - timedelta(minutes=minutes - 1 - i)
        bucket_key = bucket_time.strftime("%Y-%m-%dT%H:%M")
        buckets[bucket_key] = {"minute_ago": minutes - 1 - i,
                                "ts": bucket_time.isoformat(),
                                "started": 0, "ok": 0, "fail": 0}
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT started_at, outcome FROM recording_attempts "
                "WHERE started_at >= ?",
                (cutoff.isoformat(),)).fetchall()
    except Exception:
        return list(buckets.values())
    for r in rows:
        try:
            d = datetime.fromisoformat(r["started_at"].replace("Z", "+00:00"))
            key = d.strftime("%Y-%m-%dT%H:%M")
            b = buckets.get(key)
            if not b: continue
            b["started"] += 1
            o = r["outcome"]
            if o in ("ok", "stall_killed_partial"):
                b["ok"] += 1
            elif o not in ("running", None):
                b["fail"] += 1
        except Exception: pass
    return list(buckets.values())


def get_lives_heatmap(username: str) -> dict:
    """24x7 grid: für welche (weekday, hour) gab es bisher live-Detektionen.
       Datenquelle: recording_attempts (alle, auch fehlgeschlagene), weil
       'lebte zu Zeitpunkt X' = check returned status=live.
       MariaDB-portabel: SUBSTR vom ISO-Timestamp."""
    grid = [[0]*24 for _ in range(7)]    # [weekday(0=Mon)][hour]
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT started_at FROM recording_attempts "
                "WHERE username = ? AND started_at >= ?",
                (username,
                 (datetime.now(timezone.utc) - timedelta(days=90)).isoformat())
            ).fetchall()
    except Exception:
        return {"grid": grid, "total": 0}
    total = 0
    for r in rows:
        try:
            d = datetime.fromisoformat(r["started_at"].replace("Z", "+00:00"))
            grid[d.weekday()][d.hour] += 1
            total += 1
        except Exception: pass
    return {"grid": grid, "total": total, "lookback_days": 90}


def _collect_session_stats(username, since_epoch):
    """F84: Bilanz einer Live-Session für das Offline-Embed: Dauer, Anzahl
       Aufnahmen seit Live-Gang, Gesamtgröße auf Platte. Sync (DB + getsize)
       — Aufrufer nutzt asyncio.to_thread."""
    out = {"dur_min": None, "recs": 0, "size_mb": 0}
    try:
        if since_epoch:
            out["dur_min"] = max(0, int((_time_mod.time() - since_epoch) / 60))
            since_iso = datetime.fromtimestamp(since_epoch, tz=timezone.utc).isoformat()
        else:
            since_iso = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
        with db_conn() as conn:
            rows = conn.execute("SELECT filepath FROM recordings WHERE username=? AND created_at >= ?",
                                ((username or "").lstrip("@"), since_iso)).fetchall()
        out["recs"] = len(rows)
        total = 0
        for r in rows:
            try:
                fp = r["filepath"]
                if fp and os.path.exists(fp):
                    total += os.path.getsize(fp)
            except Exception:
                pass
        out["size_mb"] = round(total / (1024 * 1024), 1)
        try:
            with db_conn() as conn:
                r = conn.execute("SELECT COUNT(*) AS c FROM stream_chapters "
                                 "WHERE username=? AND created_at >= ?",
                                 ((username or "").lstrip("@"), since_iso)).fetchone()
            out["moments"] = r["c"] if r else 0     # F87: Hype-Momente der Session
        except Exception:
            out["moments"] = 0
    except Exception as e:
        log.debug("session-stats: %s", e)
    return out


def _streamer_health(username, conn):
    """Composite-Score 0-100 aus Erfolgsquote, Volumen, Aktualität."""
    cut = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    r = conn.execute(
        "SELECT COUNT(*) AS att, "
        "SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok, "
        "MAX(started_at) AS last FROM recording_attempts WHERE username=? AND started_at >= ?",
        (username, cut)).fetchone()
    att, ok_n, last = int(r["att"] or 0), int(r["ok"] or 0), r["last"]
    rate = (100.0 * ok_n / att) if att else 0
    recency = 0
    if last:
        dt = _parse_iso(last)
        if dt:
            # BUG-FIX: _parse_iso kann naive datetime zurückgeben — aware machen vor Subtraktion
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_d = (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
            recency = max(0, 100 - age_d * 7)        # frisch=100, ~14d→0
    vol = min(100, att * 5)
    score = round(0.55 * rate + 0.25 * recency + 0.20 * vol)
    return {"score": score, "ok_rate": round(rate, 1), "attempts": att,
            "successes": ok_n, "last": last,
            "grade": ("A" if score >= 80 else "B" if score >= 60 else
                      "C" if score >= 40 else "D" if score >= 20 else "F")}


def _dir_stats(path):
    """Aggregiert Size + File-Count + älteste/neueste Mtime für ein Verzeichnis.
       Defensive: nicht-existent → leere Stats. OSError pro Datei: skip."""
    if not path or not os.path.isdir(path):
        return {"path": path, "exists": False,
                "file_count": 0, "total_bytes": 0,
                "oldest_mtime": None, "newest_mtime": None}
    total = 0; count = 0
    oldest = None; newest = None
    try:
        for entry in os.scandir(path):
            if not entry.is_file(follow_symlinks=False):
                continue
            try:
                st = entry.stat(follow_symlinks=False)
            except OSError:
                continue
            total += st.st_size
            count += 1
            m = st.st_mtime
            if oldest is None or m < oldest: oldest = m
            if newest is None or m > newest: newest = m
    except OSError as e:
        log.warning(f"_dir_stats({path}): {e}")
    return {"path": path, "exists": True,
            "file_count": count, "total_bytes": total,
            "oldest_mtime": oldest, "newest_mtime": newest}


def get_recordings_heatmap() -> dict:
    """Global: wann starten Recordings (24x7)."""
    grid = [[0]*24 for _ in range(7)]
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT created_at FROM recordings "
                "WHERE created_at >= ? AND deleted_at IS NULL",
                ((datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),)
            ).fetchall()
    except Exception:
        return {"grid": grid, "total": 0}
    total = 0
    for r in rows:
        try:
            d = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
            grid[d.weekday()][d.hour] += 1
            total += 1
        except Exception: pass
    return {"grid": grid, "total": total, "lookback_days": 30}
