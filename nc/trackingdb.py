"""nc.trackingdb — v4.0-W50: die zwei Tracking-Status-Helfer, aus bot_v37 gelöst.

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
