"""nc.dbgesundheit — wie geht es der Datenbank? (bot-frei, fuer den Datenbank-Waechter)

v4.2-W146. Seit W143 kann die Datenbank MariaDB sein und seit W145 traegt sie
die Einstellungen des Decks — sie ist damit der eine Ort, ohne den der Bot
weder weiss, wen er verfolgt, noch wie er eingestellt ist. Beobachtet hat sie
bis hierher niemand: /healthz fragt `SELECT 1`, und das sagt nur ja oder nein.

Gemessen wird hier, was vorher ausfaellt als ein `SELECT 1`:

  * Latenz der Probe — eine Datenbank, die 2 s fuer `SELECT 1` braucht, laesst
    jede Abfrage des Decks und jeden Statuswechsel warten;
  * Groesse und Zuwachs — die Platte meldet der Platten-Waechter, aber nicht,
    WER sie fuellt;
  * bei SQLite die Groesse der `-wal`-Datei. Laeuft der Checkpoint nicht (ein
    Leser haelt eine Transaktion offen), waechst sie ohne Grenze, und jeder
    Lesezugriff wird langsamer — ohne einen einzigen Fehler;
  * Schema-Stand gegen den Code (W85) und ob die Einstellungen beim Start aus
    der Datenbank geladen wurden (W145).

Nur Lesen, eine Verbindung, ein paar kurze Abfragen — der Waechter laeuft alle
fuenf Minuten im Brain-Thread, nie auf dem Event-Loop.
"""

import logging
import os
import time

log = logging.getLogger("TikTokBot")


def messen(db_conn, backend, db_path=None, schema_stand=None, schema_erwartet=None,
           einst_start=None, uhr=time.perf_counter):
    """{"ok", "backend", "latenz_ms", "groesse_b", "wal_b", "tabellen",
        "einstellungen", "schema_stand", "schema_erwartet", "einst_fehler", "fehler"}"""
    aus = {"ok": False, "backend": backend or "sqlite", "latenz_ms": None,
           "groesse_b": None, "wal_b": None, "tabellen": None, "einstellungen": None,
           "schema_stand": schema_stand, "schema_erwartet": schema_erwartet,
           "einst_fehler": (einst_start or {}).get("fehler"), "fehler": None}
    t0 = uhr()
    try:
        with db_conn() as conn:
            conn.execute("SELECT 1").fetchone()
            aus["latenz_ms"] = round((uhr() - t0) * 1000.0, 1)
            if aus["backend"] == "mariadb":
                r = conn.execute(
                    "SELECT COUNT(*) AS n, COALESCE(SUM(data_length + index_length), 0) AS b "
                    "FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE()").fetchone()
                aus["tabellen"], aus["groesse_b"] = int(r["n"]), int(r["b"])
                da = conn.execute("SELECT COUNT(*) AS n FROM information_schema.TABLES "
                                  "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'einstellungen'"
                                  ).fetchone()["n"]
            else:
                aus["tabellen"] = int(conn.execute(
                    "SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table'").fetchone()["n"])
                da = conn.execute("SELECT COUNT(*) AS n FROM sqlite_master "
                                  "WHERE type='table' AND name='einstellungen'").fetchone()["n"]
            if da:
                aus["einstellungen"] = int(conn.execute(
                    "SELECT COUNT(*) AS n FROM einstellungen").fetchone()["n"])
        aus["ok"] = True
    except Exception as e:
        # Der Waechter meldet das als kritischen Befund; die Zeile hier steht
        # im Log, auch wenn die Benachrichtigung ausgeschaltet ist.
        log.warning("Datenbank-Messung: %s nicht abfragbar: %s: %s", backend or "sqlite",
                    type(e).__name__, e)
        aus["fehler"] = "%s: %s" % (type(e).__name__, e)
    if aus["backend"] != "mariadb" and db_path:
        # Die Dateigroessen auch dann, wenn die Abfrage scheiterte: eine
        # riesige -wal neben einer gesperrten Datei ist oft die Erklaerung.
        if os.path.isfile(db_path):
            aus["groesse_b"] = os.path.getsize(db_path)
        wal = db_path + "-wal"
        aus["wal_b"] = os.path.getsize(wal) if os.path.isfile(wal) else 0
    return aus
