"""nc.dbwrap — DB-Zugang: Verbindungs-Wrapper + db_conn() + MariaDB-Pool.

Extrahiert aus bot_v37.py. Der MariaDB-Pfad übersetzt SQLite-Dialekt via
nc.sqlutil._translate_sql und liefert Row-Objekte mit dict-Zugriff, damit der
gesamte Bot-Code backend-agnostisch bleibt.

V37: db_conn() selbst wohnt jetzt hier. Das war der Schlüssel zur weiteren
Modularisierung — über 100 Bot-Funktionen hingen AUSSCHLIESSLICH an diesem
einen Symbol. Die Konfiguration kommt per configure_db() vom Bot (keine
Env-Zugriffe im Modul, damit es testbar bleibt)."""

import logging
import sqlite3
import threading

from nc.sqlutil import _translate_sql

log = logging.getLogger("TikTokBot")

# --- Konfiguration (vom Bot injiziert; Defaults = SQLite-Standalone) --------
DB_PATH = "tiktok_bot.db"
DB_BACKEND = "sqlite"
MARIADB_HOST = "localhost"
MARIADB_PORT = 3306
MARIADB_USER = "tiktok_bot"
MARIADB_PASSWORD = ""
MARIADB_DB = "tiktok_bot"
MARIADB_POOL_SIZE = 10

_WAL_INIT = {"done": False}   # B80: WAL-Modus nur einmal prozessweit setzen
_MARIADB_POOL_INIT_LOCK = threading.Lock()    # F46-Bug-Fix B1


def configure_db(*, db_path=None, backend=None, mariadb=None):
    """Vom Bot beim Start aufgerufen. mariadb: dict mit host/port/user/
       password/db/pool_size."""
    global DB_PATH, DB_BACKEND, MARIADB_HOST, MARIADB_PORT, MARIADB_USER
    global MARIADB_PASSWORD, MARIADB_DB, MARIADB_POOL_SIZE
    if db_path:
        DB_PATH = db_path
    if backend:
        DB_BACKEND = backend
    if mariadb:
        MARIADB_HOST = mariadb.get("host", MARIADB_HOST)
        MARIADB_PORT = mariadb.get("port", MARIADB_PORT)
        MARIADB_USER = mariadb.get("user", MARIADB_USER)
        MARIADB_PASSWORD = mariadb.get("password", MARIADB_PASSWORD)
        MARIADB_DB = mariadb.get("db", MARIADB_DB)
        MARIADB_POOL_SIZE = mariadb.get("pool_size", MARIADB_POOL_SIZE)

# _MARIADB_POOL ist ein LAZY-Pool: der Bot setzt/liest ihn zur Laufzeit.
# Referenz-Muster: das Modul hält den Pool selbst; der Bot greift über
# get_pool()/set_pool() zu (kein import-Zyklus, keine Reihenfolge-Falle).
_MARIADB_POOL = None


def get_pool():
    return _MARIADB_POOL


def set_pool(p):
    global _MARIADB_POOL
    _MARIADB_POOL = p


class _SQLiteConnWrap:
    """Transparenter Wrapper um sqlite3.Connection. Reicht alle Attribute/
    Methoden (execute, executemany, cursor, commit, rollback, row_factory,
    lastrowid via Cursor, ...) unverändert durch — verhält sich nach außen
    identisch zur rohen Connection. Einziger Unterschied: __exit__ ruft
    zusätzlich close(), wie es der MariaDB-Wrapper bereits tut.

    Grund: sqlite3.Connection.__exit__ committet/rollbackt nur die
    Transaktion, schließt aber nicht den zugrunde liegenden DB-Handle.
    Bei 200+ Aufrufstellen von 'with db_conn() as conn:' im Code blieben
    dadurch viele Connections offen bis zum GC statt deterministisch beim
    Verlassen des with-Blocks geschlossen zu werden."""
    __slots__ = ("_conn",)

    def __init__(self, conn):
        self._conn = conn

    def __getattr__(self, name):
        # Alles was nicht explizit unten überschrieben ist, geht direkt
        # an die echte sqlite3.Connection (execute, cursor, row_factory, …)
        return getattr(self._conn, name)

    def __enter__(self):
        self._conn.__enter__()   # startet implizite Transaktion (sqlite3-Verhalten)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            # sqlite3.Connection.__exit__ macht commit (kein exc) / rollback (exc)
            self._conn.__exit__(exc_type, exc, tb)
        finally:
            try:
                self._conn.close()
            except Exception:
                pass   # bereits geschlossen oder anderweitig kaputt — kein Crash hier
        return False    # Exception nicht unterdrücken


class _MariaDBRowProxy:
    """Macht ein DictCursor-Result (dict) zugriffsfähig sowohl per Key (row['x'])
       als auch per Index (row[0]). Damit ist es drop-in-kompatibel zu
       sqlite3.Row im bestehenden Code."""
    __slots__ = ('_d', '_keys')
    def __init__(self, d):
        self._d = d
        self._keys = list(d.keys()) if d else []
    def __getitem__(self, k):
        if isinstance(k, int):
            return self._d[self._keys[k]]
        return self._d[k]
    def __contains__(self, k): return k in self._d
    def __iter__(self): return iter(self._keys)
    def keys(self): return self._keys
    def get(self, k, default=None): return self._d.get(k, default)
    def __repr__(self): return f"_MariaDBRowProxy({self._d})"


class _MariaDBCursorWrap:
    """Übersetzt SQL-Statements + wickelt die Ergebnisse in _MariaDBRowProxy."""
    def __init__(self, cursor):
        self._c = cursor
        self.lastrowid = None
        self.rowcount = 0

    def execute(self, sql, params=()):
        translated = _translate_sql(sql)
        # PyMySQL erwartet tuple oder list
        if isinstance(params, dict):
            self._c.execute(translated, params)
        else:
            if not isinstance(params, (list, tuple)):
                params = (params,)
            self._c.execute(translated, params)
        self.lastrowid = self._c.lastrowid
        self.rowcount = self._c.rowcount
        return self

    def executemany(self, sql, seq):
        translated = _translate_sql(sql)
        self._c.executemany(translated, seq)
        self.rowcount = self._c.rowcount
        return self

    def fetchone(self):
        r = self._c.fetchone()
        return _MariaDBRowProxy(r) if r else None

    def fetchall(self):
        return [_MariaDBRowProxy(r) for r in self._c.fetchall()]

    def __iter__(self):
        for r in self._c:
            yield _MariaDBRowProxy(r)

    def close(self):
        try: self._c.close()
        except Exception: pass


class _MariaDBConnWrap:
    """Wraps a pymysql Connection to mimic sqlite3.Connection's interface.
       - execute(sql, params) creates a cursor implicitly (like SQLite)
       - commit/rollback pass through
       - works as context manager (closes connection back to pool on exit)"""
    def __init__(self, conn):
        self._conn = conn
        self._cursor = None

    def execute(self, sql, params=()):
        # SQLite-Style: conn.execute → impliziter Cursor
        cur = _MariaDBCursorWrap(self._conn.cursor())
        cur.execute(sql, params)
        return cur

    def executemany(self, sql, seq):
        cur = _MariaDBCursorWrap(self._conn.cursor())
        cur.executemany(sql, seq)
        return cur

    def cursor(self):
        return _MariaDBCursorWrap(self._conn.cursor())

    def commit(self):
        try: self._conn.commit()
        except Exception as e:
            log.warning(f"MariaDB commit failed: {e}")
            raise

    def rollback(self):
        try: self._conn.rollback()
        except Exception: pass

    def close(self):
        """Return connection to pool (or close if pool full).
           F46-Bug-Fix B3: Vor Rückgabe einen rollback() machen — falls die
           letzte Operation in einem inkonsistenten Txn-State gelandet ist
           (z.B. commit() ist gefailt), bekommt der nächste Pool-User sonst
           eine Connection mit pending-txn-state.
           B3-erweitert: wenn put_nowait scheitert (Pool voll, sollte nie
           passieren), Slot-Counter dekrementieren — sonst leakt _created."""
        if self._conn is None:    # already closed/returned
            return
        conn = self._conn
        self._conn = None
        try:
            try: conn.rollback()
            except Exception: pass
            if _MARIADB_POOL is not None:
                try:
                    _MARIADB_POOL._q.put_nowait(conn)
                    return
                except Exception:
                    pass
            # Hier: Pool voll oder gar kein Pool — Conn wirklich schließen
            conn.close()
            if _MARIADB_POOL is not None:
                # Slot freigeben weil die Conn jetzt weg ist
                with _MARIADB_POOL._lock:
                    _MARIADB_POOL._created = max(0, _MARIADB_POOL._created - 1)
        except Exception: pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # Mimics sqlite3.Connection: commit on success, rollback on exception.
        # Then close (returns to pool).
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.close()
        return False    # do not suppress exception


# ------------------------------------------------------------------
# db_conn + MariaDB-Pool (V37: aus bot_v37.py hierher)
# ------------------------------------------------------------------

def _mariadb_connect():
    """Holt eine Connection aus dem Pool. Bei Pool-Erschöpfung blockierend
       (max_size=10 sollte für den Bot reichen — wir haben ~4 Worker plus
       Flask + Reaper).

       F46-Bug-Fix B1: Pool-Init unter eigenem Module-Lock — sonst können
       zwei Threads gleichzeitig die None-Check passieren und zwei Pools
       erzeugen → der zweite leakt.
       F46-Bug-Fix B2: connect() darf nicht UNTER dem Pool-Lock laufen —
       das blockiert andere Threads für die volle connect_timeout (10s).
       Wir nehmen ein Slot-Reservation-Pattern: erst _created unter Lock
       incrementieren, dann außerhalb des Locks tatsächlich connecten.
       Wenn der Connect fehlschlägt, _created wieder dekrementieren."""
    if get_pool() is None:
        # B1: Doppelte Initialisierung verhindern
        with _MARIADB_POOL_INIT_LOCK:
            if get_pool() is None:
                import pymysql
                from pymysql.cursors import DictCursor
                import queue
                p = type('Pool', (), {})()
                p._q = queue.Queue(maxsize=MARIADB_POOL_SIZE)
                p._lock = threading.Lock()
                p._created = 0
                p._pymysql = pymysql
                p._DictCursor = DictCursor
                set_pool(p)
    p = get_pool()

    def _new_connection():
        return p._pymysql.connect(
            host=MARIADB_HOST, port=MARIADB_PORT,
            user=MARIADB_USER, password=MARIADB_PASSWORD,
            database=MARIADB_DB, charset="utf8mb4",
            autocommit=False,
            cursorclass=p._DictCursor,
            connect_timeout=10, read_timeout=30, write_timeout=30)

    # Versuche eine bestehende zu kriegen
    conn = None
    try:
        conn = p._q.get_nowait()
    except Exception:
        # Keine idle — Slot reservieren oder warten
        slot_reserved = False
        with p._lock:
            if p._created < MARIADB_POOL_SIZE:
                p._created += 1
                slot_reserved = True
        if slot_reserved:
            # B2: connect() OUTSIDE des Pool-Locks
            try:
                conn = _new_connection()
            except Exception:
                # Connect fehlgeschlagen — Slot wieder freigeben sonst leakt's
                with p._lock:
                    p._created -= 1
                raise
        else:
            # Pool voll — auf Rückgabe einer existierenden Conn warten
            try:
                conn = p._q.get(timeout=10)
            except Exception:
                log.error(f"MariaDB connect: pool exhausted ({MARIADB_POOL_SIZE} "
                          f"connections all in use), waited 10s")
                raise

    # Connection-Liveness-Check (TCP kann zwischendurch droppen)
    try:
        conn.ping(reconnect=True)
    except Exception:
        try: conn.close()
        except Exception: pass
        try:
            conn = _new_connection()
        except Exception:
            # Replacement fehlgeschlagen — Slot freigeben
            with p._lock:
                p._created -= 1
            raise
    return conn


def db_conn():
    """Returns a DB connection. Supports BOTH SQLite (default) and MariaDB
       depending on DB_BACKEND env var. Returns a context-managed connection
       that behaves identically in both backends:
       - cursor methods: execute(sql, params), executemany, fetchone, fetchall
       - results are dict-like (row['col'] works in both)
       - placeholders: use '?' uniformly — translator below converts to '%s' for MariaDB
       - lastrowid available on cursor after INSERT
       - context manager auto-commits on clean exit, rolls back on exception

       F46: MariaDB-Support eingebaut. Switch via env: DB_BACKEND=mariadb +
       MARIADB_HOST/PORT/USER/PASSWORD/DB. SQLite bleibt der Default damit
       bestehende Installationen ohne Änderung weiterlaufen."""
    if DB_BACKEND == "mariadb":
        return _MariaDBConnWrap(_mariadb_connect())
    # SQLite path (default)
    # B80-Fix: 'database is locked' unter Last (Whisper + Restream + Polling +
    # Dashboard gleichzeitig). Drei Ursachen behoben:
    #  (a) timeout 10s → 30s: mehr Geduld bei kurzen Schreib-Locks.
    #  (b) busy_timeout-PRAGMA: SQLite WARTET aktiv auf Lock-Freigabe statt sofort
    #      OperationalError zu werfen (der Python-timeout allein deckt nicht jeden Pfad).
    #  (c) journal_mode=WAL ist eine DAUERHAFTE Datei-Eigenschaft — es bei JEDER
    #      Connection zu setzen ist ein Schreibzugriff, der selbst blockieren kann.
    #      Jetzt nur EINMAL prozessweit (per Flag) statt ~208×/Tick.
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")    # 30s aktiv auf Locks warten
    if not _WAL_INIT["done"]:
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            _WAL_INIT["done"] = True
        except Exception:
            pass
    conn.execute("PRAGMA foreign_keys=ON")
    # F82: Performance-PRAGMAs (per-Connection, daher hier bei jedem Open).
    # synchronous=NORMAL ist DER empfohlene Modus unter WAL: FULL (Default)
    # fsynct bei jedem Commit — unter WAL unnötig, NORMAL bleibt crash-sicher
    # (schlimmstenfalls fehlt der allerletzte Commit nach Stromausfall).
    # Bei ~208 db_conn-Stellen + Polling-Workern der größte Einzelhebel.
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")     # Sorts/Temp-B-Trees im RAM statt /tmp
    conn.execute("PRAGMA cache_size=-8000")      # 8 MB Page-Cache (Default 2 MB) für Dashboard-Aggregationen
    # FIX (Header "Was offen bleibt"): sqlite3.Connection ist als Context-
    # Manager NUR für die Transaktion (commit bei Erfolg, rollback bei
    # Exception) — die zugrunde liegende Connection selbst wird in
    # __exit__ NICHT geschlossen. Bei 208 Aufrufstellen von
    # "with db_conn() as conn:" im Code bedeutet das: jede einzelne offene
    # Connection lebt bis der GC sie einsammelt (CPython: meist sofort
    # durch Refcounting, aber nicht garantiert — unter Last/PyPy/zyklischen
    # Referenzen kann das zu offenen File-Handles auf die .db-Datei führen).
    # _SQLiteConnWrap schließt die Connection zusätzlich in __exit__,
    # analog zum bereits korrekten MariaDB-Pfad oben.
    return _SQLiteConnWrap(conn)
