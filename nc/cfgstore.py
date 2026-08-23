"""nc.cfgstore — app_config lesen und schreiben, backend-agnostisch.

v4.0-W62c brachte den Upsert, v4.0-W111 die Leseseite: get() und set_()
lagen bis dahin als _cfg_get/_cfg_set im Monolithen, obwohl sie exakt zu
diesem Modul gehoeren. Sie sind Vorarbeit fuer das /api/ai-Blueprint —
dort wurden sie sonst zu zwei Eintraegen im Laufzeitkontext, obwohl sie
reiner Datenzugriff sind.

upsert schreibt einen Key/Value ohne UPSERT-SQL (funktioniert auf beiden DB-
Backends): erst UPDATE; ändert das nichts (rowcount 0/-1) und der Key fehlt,
INSERT — und falls dazwischen ein anderer Thread schon eingefügt hat
(IntegrityError am UNIQUE-Index), nochmals UPDATE. Die Serialisierung des Werts
und der Zeitstempel bleiben beim Aufrufer; die conn wird injiziert, daher gegen
echtes In-Memory-SQLite testbar — inklusive des Race-Fallbacks.
"""


def upsert(conn, key, payload, now):
    """Key mit bereits serialisiertem payload + Zeitstempel now in app_config
       schreiben (anlegen oder aktualisieren). TOCTOU-sicher."""
    cur = conn.execute("UPDATE app_config SET v=?, updated_at=? WHERE k=?",
                       (payload, now, key))
    # rowcount ist bei beiden Backends verfügbar; 0 → noch nicht vorhanden
    if getattr(cur, "rowcount", 0) in (0, -1):
        exists = conn.execute("SELECT 1 FROM app_config WHERE k=?", (key,)).fetchone()
        if not exists:
            try:
                conn.execute("INSERT INTO app_config (k, v, updated_at) VALUES (?,?,?)",
                             (key, payload, now))
            except Exception:
                # TOCTOU: zwei Threads sahen UPDATE=0 und SELECT=not-exists und
                # versuchten beide INSERT; der zweite trifft den UNIQUE-Index.
                # Fallback: nochmals UPDATE (jetzt existiert der Key sicher).
                conn.execute("UPDATE app_config SET v=?, updated_at=? WHERE k=?",
                             (payload, now, key))
    conn.commit()


# ── v4.0-W111: die Leseseite, aus bot_v37 geloest ────────────────────────

import json as _json                                          # noqa: E402
from datetime import datetime as _dt, timezone as _tz         # noqa: E402

from nc.dbwrap import db_conn as _db_conn                     # noqa: E402


def get(key, default=None):
    """Liest einen JSON-Wert aus app_config. default bei Fehlen/Fehler."""
    try:
        with _db_conn() as conn:
            row = conn.execute("SELECT v FROM app_config WHERE k=?", (key,)).fetchone()
        if not row or row["v"] is None:
            return default
        try:
            return _json.loads(row["v"])
        except Exception:
            return row["v"]
    except Exception:
        return default


def set_(key, value):
    """Upsert eines JSON-Werts in app_config (backend-agnostisch ohne UPSERT-SQL).

    Heisst set_ und nicht set, weil set eine eingebaute Funktion ist — ein
    Modul-Attribut mit dem Namen waere zwar erlaubt, liest sich beim Aufruf
    aber wie ein Fehler.
    """
    payload = _json.dumps(value, ensure_ascii=False)
    now = _dt.now(_tz.utc).isoformat()
    with _db_conn() as conn:
        upsert(conn, key, payload, now)
    return value
