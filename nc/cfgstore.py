"""nc.cfgstore — v4.0-W62c: backend-agnostischer app_config-Upsert, aus bot_v37 gelöst.

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
