"""nc.trackingdb — v4.0-W50: die zwei Tracking-Status-Helfer, aus bot.py gelöst.

Beide operieren auf der trackings-Tabelle und stehen im selben Live-Transitions-
Fluss. Verbatim übernommen; die DB-Verbindung wird injiziert (der Aufrufer öffnet
sie via db_conn), damit die reine SQL-/Entscheidungslogik gegen ein echtes
In-Memory-SQLite testbar ist — inklusive der korrektheitskritischen Atomarität
von claim_transition.
"""


def claim_transition(conn, tracking_id, going_live):
    """F27: Atomarer Status-Übergang für Live-Notifications. Setzt last_live von
       [prev] auf [target] und gibt True zurück, WENN die Zeile tatsächlich
       geändert wurde — so sendet nur EIN Worker die Notification (Race zu).
       Zwei Worker, die gleichzeitig 'going live' sehen, werden hier
       deserialisiert: einer gewinnt das UPDATE (rowcount=1), der andere
       verliert (rowcount=0)."""
    target = 1 if going_live else 0
    prev = 0 if going_live else 1
    cur = conn.execute(
        "UPDATE trackings SET last_live=? WHERE id=? AND last_live=?",
        (target, tracking_id, prev))
    conn.commit()
    return cur.rowcount == 1


def get_state(conn, tracking_id):
    """F27: Frische Werte aus DB statt der stale Row aus der Queue.
       Returns (last_live, recording, paused) oder (None, None, None) wenn nicht
       da. paused wird mit zurückgegeben, damit der Aufrufer pausierte Trackings
       von Live-Notifications ausschliessen kann."""
    row = conn.execute(
        "SELECT last_live, recording, paused FROM trackings WHERE id=?",
        (tracking_id,)).fetchone()
    if not row:
        return None, None, None
    paused = bool(row["paused"]) if "paused" in row.keys() else False
    return bool(row["last_live"]), bool(row["recording"]), paused


# ═════════════════════════════════════════════════════════════════════════
# v4.0-W117: elf weitere Tracking-Zugriffe, verbatim aus bot.py
#
# Warum sie hierher gehoeren und nicht in nc/ctx.py: das /api/trackings-
# Blueprint braucht sie, der Bot (Telegram-Kommandos, Live-Worker) aber auch.
# Ueber den Kontext waeren das fuenf weitere Slots gewesen — der steht
# vertraglich bei 25 und ist voll. Als Modul kosten sie null: beide Seiten
# importieren. Dasselbe Muster wie nc/recdb.py (W104) und nc/donationsdb.py.
#
# Der Bot behaelt jeden Namen und delegiert; die Koerper hier sind bitgenau
# die alten, inklusive der stillen `except: return []`-Pfade — das Dashboard
# soll bei klemmender Tabelle leer bleiben statt 500 zu liefern.
#
# Zwei Dinge kommen per Injection, weil sie im Bot leben und dort bleiben:
# die Backend-abhaengigen Integritaetsfehler, der Quota-Deckel, das
# Ereignisprotokoll — und `on_resume`, das beim Entpausen den In-Memory-Zustand
# des Recorders aufraeumt. Diesen Zustand ins Modul zu ziehen waere ein
# Zustandsriss: er gehoert dem Live-Worker, nicht der Datenbank.
# ═════════════════════════════════════════════════════════════════════════

import logging
import re
from datetime import datetime, timezone
from typing import List, Optional

from nc.dbwrap import db_conn
from nc.textutil import clean_username

log = logging.getLogger("TikTokBot")

# Vom Bot injiziert. Defaults sind bewusst harmlos statt None: ein nicht
# verdrahtetes Modul soll lesen koennen, nicht mit AttributeError sterben.
DB_INTEGRITY_ERRORS = ()
MAX_TRACKINGS_PER_CHAT = 0
log_event = lambda *a, **k: None          # noqa: E731
_on_resume = lambda tracking_id: None     # noqa: E731


def configure(*, integrity_errors=None, max_trackings_per_chat=None,
              log_event_fn=None, on_resume=None):
    """Vom Bot einmal beim Start gerufen.

    `on_resume` bekommt die tracking_id, wenn ein Tracking entpaust wird, und
    raeumt die In-Memory-Zaehler des Recorders auf. Ohne das wuerde der naechste
    stall_killed-Streak das Tracking sofort wieder pausieren (B54).
    """
    global DB_INTEGRITY_ERRORS, MAX_TRACKINGS_PER_CHAT, log_event, _on_resume
    if integrity_errors is not None:
        DB_INTEGRITY_ERRORS = integrity_errors
    if max_trackings_per_chat is not None:
        MAX_TRACKINGS_PER_CHAT = max_trackings_per_chat
    if log_event_fn is not None:
        log_event = log_event_fn
    if on_resume is not None:
        _on_resume = on_resume


def bulk_add_trackings(group_id: int, usernames: list, added_by: int) -> dict:
    """F56: Bulk-Import — viele Usernames auf einmal anlegen. Returns Stats:
         { added: [...], duplicates: [...], invalid: [...], quota_exceeded: [...] }
       'duplicates' = bereits in diesem Chat getrackt.
       'invalid' = leere oder regex-failing Usernames.
       'quota_exceeded' = nach MAX_TRACKINGS_PER_CHAT abgewiesen.
       Durchläuft die Liste defensiv: ein einzelner Fehler stoppt nicht den Rest.

       F56-Bug-Fix B22: Per-Row COMMIT + ROLLBACK bei Fehler.
       Vorher hatten wir EINEN großen TXN für alle Inserts. Auf MariaDB-Seite
       war das gefährlich: wenn ein einzelner INSERT mit z.B. Lock-Timeout
       fehlschlug, war die TXN poisoned — alle FOLGENDEN INSERTs scheiterten
       auch (selbst die guten), und der finale conn.commit() warf alles weg.
       Jetzt: jeder Insert ist sein eigener TXN. Bei Fehler explizit rollback,
       weitermachen. Etwas mehr Roundtrips, aber bulletproof gegen
       Partial-Failure-Szenarien.

       F64: MAX_TRACKINGS_PER_CHAT enforcement. Zählt vorab existing + plant
       wie viele dazukommen, schneidet danach ab mit quota_exceeded-Markierung."""
    added, duplicates, invalid, quota_exceeded = [], [], [], []
    now_iso = datetime.now(timezone.utc).isoformat()
    seen_in_batch = set()
    with db_conn() as conn:
        # Bereits existierende auf einmal abrufen — spart N+1 Queries
        existing_rows = conn.execute(
            "SELECT username FROM trackings WHERE group_id=?", (group_id,)
        ).fetchall()
        existing = {r["username"] for r in existing_rows}
        # F64: Wie viel Headroom haben wir noch in diesem Chat?
        if MAX_TRACKINGS_PER_CHAT > 0:
            remaining_quota = MAX_TRACKINGS_PER_CHAT - len(existing)
        else:
            remaining_quota = None   # unbegrenzt

        for raw in usernames:
            u = clean_username(raw) if raw else None
            if not u:
                invalid.append(raw); continue
            if u in seen_in_batch:
                # Doppelt im Input — als Duplicate werten
                duplicates.append(u); continue
            seen_in_batch.add(u)
            if u in existing:
                duplicates.append(u); continue
            # F64: Quota-Check vor INSERT
            if remaining_quota is not None and remaining_quota <= 0:
                quota_exceeded.append(u)
                continue
            try:
                conn.execute(
                    "INSERT INTO trackings (group_id, username, added_by, created_at) "
                    "VALUES (?,?,?,?)",
                    (group_id, u, added_by, now_iso))
                # B22: per-Row commit damit ein späterer Fehler nicht alle
                # früheren INSERTs invalidiert
                conn.commit()
                added.append(u)
                if remaining_quota is not None:
                    remaining_quota -= 1
            except DB_INTEGRITY_ERRORS:
                # Race: jemand anders fügt parallel hinzu. Als Duplicate werten.
                # B22: rollback wegen MariaDB-TXN-State (no-op auf SQLite, aber nötig
                # damit die nächste INSERT-Iteration auf MariaDB nicht in poisoned-TXN landet).
                try: conn.rollback()
                except Exception: pass
                duplicates.append(u)
            except Exception as e:
                # B22: NON-IntegrityError (Lock-Timeout, Connection-Lost, etc.) —
                # rollback + weiter. Sonst poisoned die TXN auf MariaDB und alle
                # folgenden INSERTs scheitern auch.
                try: conn.rollback()
                except Exception: pass
                log.warning(f"bulk_add_trackings: {u}: {e}")
                invalid.append(u)
        # Final commit ist no-op (jede Row hat schon commited oder rolled back)
        # aber schadet nicht — bleibt aus Konsistenz drin.
    return {"added": added, "duplicates": duplicates, "invalid": invalid,
            "quota_exceeded": quota_exceeded}


def get_trackings_for_group(group_id: int):
    with db_conn() as conn:
        return conn.execute("SELECT * FROM trackings WHERE group_id=?", (group_id,)).fetchall()


def get_all_active_trackings(include_paused: bool = False):
    """F53: Default skip paused trackings — Worker holt nur was wirklich
       gepollt werden soll. Dashboard nutzt include_paused=True um die
       Tabelle vollständig anzuzeigen (mit Pause-Badge)."""
    with db_conn() as conn:
        if include_paused:
            return conn.execute("SELECT * FROM trackings").fetchall()
        # paused IS NULL fängt auch alte Rows ab die noch keine paused-Spalte hatten
        # (Migration ist defensiv aber sicher ist sicher).
        return conn.execute(
            "SELECT * FROM trackings WHERE COALESCE(paused, 0) = 0").fetchall()


def set_tracking_paused(tracking_id: int, paused: bool) -> bool:
    """F53: Pause/Resume Toggle. Returns True wenn Row existiert (egal ob
       der Wert geändert wurde), False wenn tracking_id nicht existiert.

       F53-Bug-Fix B33: Vorher returnten wir `rowcount > 0`. Auf MariaDB ist
       rowcount aber die Anzahl der TATSÄCHLICH GEÄNDERTEN Rows (nicht der
       MATCHED). Folge: bei einem schon-paused Tracking → rowcount=0 →
       return False → Dashboard kriegt 404 'not found' obwohl das Tracking
       existiert. SQLite zeigt das Problem nicht. Fix: Existenz separat
       checken, dann UPDATE.

       B54: Beim RESUME (paused=False) werden auch die auto_disabled-Flags
       gecleart. Sonst würde das Tracking sofort wieder gepaust werden beim
       nächsten stall_killed-Streak (was die in-memory states schon haben).
       Beim PAUSE wird auto_disabled NICHT gesetzt (manueller Pause ≠ Auto)."""
    with db_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM trackings WHERE id=? LIMIT 1",
            (tracking_id,)).fetchone()
        if not exists:
            return False
        if paused:
            conn.execute("UPDATE trackings SET paused=1 WHERE id=?",
                         (tracking_id,))
        else:
            # B54: explizit auto_disable-Flags löschen beim Resume
            conn.execute(
                "UPDATE trackings SET paused=0, "
                "  auto_disabled_at=NULL, auto_disabled_reason=NULL "
                "WHERE id=?",
                (tracking_id,))
            # In-memory states wegputzen damit der Streak nicht sofort wieder zuschlägt.
            # v4.0-W117: die fuenf Dicts gehoeren dem Live-Worker im Bot; das
            # Modul ruft nur zurueck, statt fremden Laufzeitzustand zu halten.
            _on_resume(tracking_id)
        conn.commit()
        return True


def add_tracking_tag(tracking_id: int, tag: str) -> bool:
    """Tag normalisiert (lowercase, gestrippt, max 30 chars)."""
    tag = (tag or "").strip().lower()[:30]
    if not tag or not re.match(r'^[a-z0-9_\-]+$', tag):
        return False
    try:
        with db_conn() as conn:
            conn.execute(
                "INSERT INTO tracking_tags (tracking_id, tag, created_at) "
                "VALUES (?,?,?)",
                (tracking_id, tag, datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return True
    except DB_INTEGRITY_ERRORS:
        return False    # bereits vorhanden
    except Exception as e:
        log.warning(f"add_tracking_tag: {e}")
        return False


def remove_tracking_tag(tracking_id: int, tag: str) -> bool:
    tag = (tag or "").strip().lower()
    if not tag: return False
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "DELETE FROM tracking_tags WHERE tracking_id=? AND tag=?",
                (tracking_id, tag))
            conn.commit()
            return cur.rowcount > 0
    except Exception:
        return False


def get_tags_for_tracking(tracking_id: int) -> List[str]:
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT tag FROM tracking_tags WHERE tracking_id=? ORDER BY tag",
                (tracking_id,)).fetchall()
        return [r["tag"] for r in rows]
    except Exception:
        return []


def get_all_tags_with_counts() -> List[dict]:
    """Alle Tags + Anzahl Trackings die diesen Tag haben."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT tag, COUNT(*) AS cnt FROM tracking_tags "
                "GROUP BY tag ORDER BY cnt DESC, tag ASC"
            ).fetchall()
        return [{"tag": r["tag"], "count": r["cnt"]} for r in rows]
    except Exception:
        return []


def set_tracking_priority(tracking_id: int, level: int,
                          custom_interval: Optional[int] = None) -> bool:
    """level 0=normal, 1=high (15s), 2=vip (10s). Custom interval overrides level."""
    level = max(0, min(2, int(level)))
    if custom_interval is not None:
        custom_interval = max(5, min(3600, int(custom_interval)))
    try:
        with db_conn() as conn:
            # Existiert tracking?
            exists = conn.execute(
                "SELECT 1 FROM trackings WHERE id=?", (tracking_id,)).fetchone()
            if not exists: return False
            # Upsert via DELETE+INSERT (portabel SQLite+MariaDB)
            conn.execute("DELETE FROM tracking_priority WHERE tracking_id=?",
                         (tracking_id,))
            conn.execute(
                "INSERT INTO tracking_priority "
                "(tracking_id, priority_level, custom_interval_secs, updated_at) "
                "VALUES (?,?,?,?)",
                (tracking_id, level, custom_interval,
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
        log_event("tracking.priority", "info",
                  f"Tracking #{tracking_id} priority={level} interval={custom_interval}",
                  {"tracking_id": tracking_id, "level": level,
                   "custom_interval": custom_interval})
        return True
    except Exception as e:
        log.warning(f"set_tracking_priority: {e}")
        return False


def get_tracking_priority(tracking_id: int) -> dict:
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT priority_level, custom_interval_secs FROM tracking_priority "
                "WHERE tracking_id=?", (tracking_id,)).fetchone()
        if not row:
            return {"level": 0, "custom_interval": None}
        return {"level": row["priority_level"] or 0,
                "custom_interval": row["custom_interval_secs"]}
    except Exception:
        return {"level": 0, "custom_interval": None}


def get_priority_poll_interval(tracking_id: int, default_interval: int) -> int:
    """Polling-Intervall basierend auf Priority. Wird von _schedule_next_check
       benutzt. Höhere Priority = kürzeres Intervall."""
    p = get_tracking_priority(tracking_id)
    if p["custom_interval"] is not None:
        return p["custom_interval"]
    if p["level"] >= 2:    return min(default_interval, 10)    # VIP
    if p["level"] >= 1:    return min(default_interval, 15)    # high
    return default_interval
