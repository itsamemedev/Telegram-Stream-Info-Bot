"""nc.dbwrap — DB-Zugang: Verbindungs-Wrapper + db_conn() + MariaDB-Pool.

Extrahiert aus bot.py. Der MariaDB-Pfad übersetzt SQLite-Dialekt via
nc.sqlutil._translate_sql und liefert Row-Objekte mit dict-Zugriff, damit der
gesamte Bot-Code backend-agnostisch bleibt.

V37: db_conn() selbst wohnt jetzt hier. Das war der Schlüssel zur weiteren
Modularisierung — über 100 Bot-Funktionen hingen AUSSCHLIESSLICH an diesem
einen Symbol. Die Konfiguration kommt per configure_db() vom Bot (keine
Env-Zugriffe im Modul, damit es testbar bleibt)."""

import asyncio
import logging
import os
import sqlite3
import threading
import time as _time

from nc.sqlutil import _translate_sql

log = logging.getLogger("TikTokBot")


class DatenbankUnlesbar(sqlite3.DatabaseError):
    """Die Datenbankdatei ist nicht zu oeffnen — mit Diagnose statt Traceback.

    v4.2-W92. Erbt bewusst von sqlite3.DatabaseError: im Bestand faengt
    Code an vielen Stellen `except sqlite3.DatabaseError` oder
    `except Exception`, und diese Stellen sollen sich nicht aendern. Neu
    ist allein, was der Betreiber zu lesen bekommt.

    Der Anlass: am 17.09. lag statt der Datenbank ein 108-MB-Blob mit
    TLS-Verkehr im Arbeitsverzeichnis. Der Bot starb beim Start mit

        sqlite3.DatabaseError: file is not a database

    und sonst nichts — kein Pfad, keine Groesse, kein Hinweis, was die
    Datei stattdessen ist, und vor allem keine Abhilfe. In der
    gefaehrlichsten Lage des Systems (die Daten sind weg oder ueberschrieben)
    ist das dieselbe Art Meldung wie ein blankes "HTTP 403": richtig und
    nutzlos. Die naheliegende Reaktion — Datei loeschen, damit es wieder
    laeuft — kostet Trackings, Aufnahme-Eintraege und den Ledger.
    """


# Die Signaturen, die wir benennen koennen. Mehr Faelle zu raten hilft
# niemandem; was hier nicht steht, wird als "unbekannt" gemeldet, samt Hex.
_SIGNATUREN = (
    (b"SQLite format 3\x00",
     "ein SQLite-Header ist vorhanden, der Inhalt dahinter ist beschaedigt",
     "Chancen auf Rettung: `sqlite3 <datei> \".recover\" | sqlite3 neu.db`"),
    (b"\x17\x03\x03", "am Anfang wie ein TLS-Record (Application Data)",
     "Die Datei wurde von einem anderen Programm ueberschrieben. Was weiter "
     "hinten steht, sagt der Inhalts-Befund unten — ein TLS-Kopf allein "
     "heisst NICHT, dass die ganze Datei verloren ist."),
    (b"\x16\x03", "ein TLS-Handshake",
     "Die Datei wurde von einem anderen Programm ueberschrieben."),
    (b"<!DOCTYPE", "eine HTML-Seite",
     "Vermutlich eine Fehlerseite, die in die Datei geschrieben wurde "
     "(fehlgeleiteter Download)."),
    (b"<html", "eine HTML-Seite", "Siehe oben."),
    (b"PK\x03\x04", "ein ZIP-Archiv",
     "Hier wurde ein Archiv ueber die Datenbank gelegt."),
    (b"\x1f\x8b", "eine gzip-Datei",
     "Vermutlich ein nicht ausgepacktes Backup. `gunzip -c <datei> > neu.db` "
     "und pruefen, ob dabei eine Datenbank herauskommt."),
    (b"{", "JSON oder Text", "Ein fehlgeleiteter Schreibvorgang."),
)


# Woran man einen SQL-Dump erkennt. Bewusst mehrere Marken: ein Dump aus
# `.dump` beginnt anders als einer aus mysqldump oder aus unserem eigenen
# Systemarchiv.
_DUMP_MARKEN = (b"CREATE TABLE", b"INSERT INTO", b"BEGIN TRANSACTION",
                b"PRAGMA foreign_keys")

# v4.2-W94: NUR diese drei beweisen einen Dump. `CREATE TABLE` tut es NICHT —
# SQLite legt den Schema-Text woertlich in `sqlite_master` ab, also steht er
# in JEDER Datenbankdatei. Nachgemessen an einer echten Datei mit 3000
# Zeilen: `CREATE TABLE` 1 Treffer, `INSERT INTO` 0 Treffer; im Dump derselben
# Daten: `INSERT INTO` 3000 Treffer. Die erste Fassung zaehlte `CREATE TABLE`
# mit und hat deshalb jede beschaedigte Datenbank als Dump ausgegeben — samt
# dem Rat `sqlite3 neu.db < datei`, der auf einer Binaerdatei nicht laufen
# KANN. Ein falscher Rat ist in dieser Lage teurer als gar keiner.
_DUMP_BEWEIS = (b"INSERT INTO", b"BEGIN TRANSACTION", b"PRAGMA foreign_keys")

# Die acht von SQLite erlaubten Seitengroessen. Ist die Dateigroesse durch
# eine davon teilbar, liegt der Verdacht nahe, dass die Seiten noch da sind
# und nur der 100-Byte-Kopf ueberschrieben wurde — der Fall vom 18.09.:
# 401408 = 4096 x 98.
_SEITENGROESSEN = (512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)


def _proben(pfad: str, groesse: int, n: int = 65536):
    """Anfang, Mitte und Ende — nicht die ganze Datei.

    Eine Datenbank kann 100 MB und mehr haben; sie im Fehlerfall komplett zu
    lesen, kostet Zeit und Speicher an der Stelle, an der beides gerade knapp
    sein kann.
    """
    aus = []
    try:
        with open(pfad, "rb") as f:
            for wo in (0, max(0, groesse // 2 - n // 2), max(0, groesse - n)):
                f.seek(wo)
                stueck = f.read(n)
                if stueck:
                    aus.append((wo, stueck))
                if groesse <= n:
                    break
    except OSError as e:
        log.warning("datei_diagnose: Proben aus %s nicht lesbar: %s", pfad, e)
    return aus


def _inhalt_befund(pfad: str, groesse: int) -> list:
    """Was steht WEITER HINTEN? -> Zeilen fuer die Diagnose.

    v4.2-W92, nachgeschaerft am echten Fall: die erste Fassung sah nur die
    ersten 16 Bytes, erkannte dort einen TLS-Record und riet "aus der Datei
    ist nichts zu holen". Beim Betreiber steckten dahinter 33.444 Zeilen mit
    CREATE-TABLE- und INSERT-Vokabular — ein SQL-Dump, also seine
    vollstaendigen Daten. Der Rat war falsch, und ein falscher Rat in dieser
    Lage kostet mehr als gar keiner: er haette die Datei als verloren
    abgehakt.

    Drei Messungen, dieselben, die man von Hand machen wuerde: steckt
    irgendwo ein SQLite-Header, sieht es nach SQL-Dump aus, und laesst sich
    der Inhalt komprimieren (verschluesselte Daten tun das nicht).
    """
    import zlib
    zeilen = ["", "Inhalt (Proben aus Anfang, Mitte und Ende):"]
    proben = _proben(pfad, max(0, groesse))
    if not proben:
        return zeilen + ["  nicht lesbar."]

    kopf_gefunden = None
    dump_marken = set()
    dump_beweis = set()
    roh = druck = 0
    for wo, stueck in proben:
        i = stueck.find(b"SQLite format 3\x00")
        if i >= 0 and kopf_gefunden is None:
            kopf_gefunden = wo + i
        for marke in _DUMP_MARKEN:
            if marke in stueck:
                dump_marken.add(marke.decode())
        for marke in _DUMP_BEWEIS:
            if marke in stueck:
                dump_beweis.add(marke.decode())
        roh += len(stueck)
        druck += sum(1 for b in stueck if 32 <= b < 127 or b in (9, 10, 13))

    if kopf_gefunden is not None:
        zeilen.append("  Ein SQLite-Header liegt bei Byte %d — die Datenbank "
                      "steckt also DAHINTER." % kopf_gefunden)
        zeilen.append("  Rettung: dd if=%s bs=1 skip=%d of=gerettet.db"
                      % (os.path.basename(pfad), kopf_gefunden))
    # v4.2-W94: der haeufigste echte Schaden zuerst — die Seiten sind noch da,
    # nur der Kopf ist weg. Erkennbar am Seitenraster, und er schliesst den
    # Dump-Verdacht aus: eine Datei, die exakt aus SQLite-Seiten besteht, ist
    # keine Textdatei.
    raster = [sg for sg in _SEITENGROESSEN
              if groesse >= 512 and groesse % sg == 0]
    if raster and not dump_beweis and kopf_gefunden is None:
        zeilen.append("  Die Groesse ist ein genaues Vielfaches der "
                      "SQLite-Seitengroesse (%s) — das spricht dafuer, dass "
                      "nur der 100-Byte-KOPF ueberschrieben wurde und die "
                      "Seiten dahinter noch stehen."
                      % ", ".join(str(s_) for s_ in raster))
        zeilen.append("  Rettung: den Kopf neu setzen, die Seitengroesse "
                      "durchprobieren, integrity_check entscheiden lassen:")
        zeilen.append("    python3 tools/dbkopf.py %s -o gerettet.db"
                      % os.path.basename(pfad))
        zeilen.append("  Das Werkzeug fasst die Eingabedatei nicht an.")
    if dump_beweis:
        zeilen.append("  SQL-Dump-Vokabular gefunden (%s) — das sieht nach "
                      "einem Dump aus, nicht nach einer Datenbankdatei."
                      % ", ".join(sorted(dump_marken)))
        zeilen.append("  Rettung: die Datei als SQL einlesen, statt sie als "
                      "Datenbank zu oeffnen:")
        zeilen.append("    sqlite3 neu.db < %s" % os.path.basename(pfad))
        zeilen.append("  Steht Muell davor, erst ab der ersten CREATE-Zeile "
                      "abschneiden:")
        zeilen.append("    tail -c +$(grep -abo -m1 'CREATE TABLE' %s | "
                      "cut -d: -f1) %s > sauber.sql"
                      % (os.path.basename(pfad), os.path.basename(pfad)))

    if roh:
        anteil = 100.0 * druck / roh
        zeilen.append("  Druckbarer Anteil: %.0f %%" % anteil)
        try:
            klein = len(zlib.compress(b"".join(p for _w, p in proben), 6))
            rate = roh / max(1, klein)
            zeilen.append("  Komprimierbar auf 1:%.1f" % rate)
            if rate < 1.1 and not dump_beweis and kopf_gefunden is None \
                    and not raster:
                zeilen.append("  Das spricht fuer verschluesselte oder "
                              "zufaellige Daten — daraus ist nichts zu "
                              "gewinnen, hier hilft nur die Sicherung.")
            elif rate >= 2.0 or dump_beweis or raster:
                zeilen.append("  Das spricht fuer STRUKTURIERTE Daten. Diese "
                              "Datei aufzugeben waere verfrueht.")
        except zlib.error as e:
            log.warning("datei_diagnose: Kompressionsprobe fehlgeschlagen: %s", e)
    return zeilen


def datei_diagnose(pfad: str) -> str:
    """Was ist diese Datei, wenn sie keine Datenbank ist? -> Klartext.

    Bewusst ohne sqlite3: wir lesen 16 Bytes und sagen, was wir sehen. Die
    Funktion laeuft nur im Fehlerfall, da ist die Lesung billig.
    """
    zeilen = []
    zeilen.append("Datei: %s" % os.path.abspath(pfad))

    if not os.path.exists(pfad):
        zeilen.append("Sie existiert nicht. SQLite haette hier eine neue, "
                      "leere Datenbank angelegt — dass es das nicht tat, "
                      "heisst: der Pfad ist nicht beschreibbar.")
        zeilen.append("Abhilfe: Rechte auf das Verzeichnis pruefen.")
        return "\n".join(zeilen)

    try:
        groesse = os.path.getsize(pfad)
        zeilen.append("Groesse: %d Bytes (%.1f MB)" % (groesse, groesse / 1048576.0))
    except OSError as e:
        log.warning("datei_diagnose: Groesse von %s nicht lesbar: %s", pfad, e)
        zeilen.append("Groesse nicht lesbar: %s" % e)
        groesse = -1

    if groesse == 0:
        zeilen.append("Die Datei ist LEER. Eine leere Datei ist keine "
                      "Datenbank — SQLite legt nur bei FEHLENDER Datei neu an.")
        zeilen.append("Abhilfe: die leere Datei zur Seite legen (nicht "
                      "loeschen), dann startet der Bot mit einer frischen "
                      "Datenbank. Vorher pruefen, ob eine Sicherung existiert.")
        return "\n".join(zeilen)

    kopf = b""
    try:
        with open(pfad, "rb") as f:
            kopf = f.read(16)
    except OSError as e:
        log.warning("datei_diagnose: %s nicht lesbar: %s — meist ein "
                    "Rechteproblem am Verzeichnis", pfad, e)
        zeilen.append("Der Anfang war nicht zu lesen: %s" % e)
        return "\n".join(zeilen)

    zeilen.append("Erste Bytes: %s" % " ".join("%02x" % b for b in kopf))

    for muster, was, abhilfe in _SIGNATUREN:
        if kopf.startswith(muster):
            zeilen.append("Das ist %s." % was)
            zeilen.append("Abhilfe: %s" % abhilfe)
            break
    else:
        zeilen.append("Der Inhalt passt zu keinem bekannten Format — es ist "
                      "jedenfalls keine SQLite-Datenbank (die begaenne mit "
                      "53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00).")

    zeilen.extend(_inhalt_befund(pfad, groesse))

    zeilen.append("")
    zeilen.append("WICHTIG: diese Datei NICHT loeschen und nicht "
                  "ueberschreiben. Erst sichern:")
    zeilen.append("    cp -av %s ~/db_forensik_$(date +%%F_%%H%%M)_%s"
                  % (os.path.basename(pfad), os.path.basename(pfad)))
    zeilen.append("Dann die Sicherungen pruefen: das taegliche Systemarchiv "
                  "legt die Datenbank IMMER als SQL-Dump ab (LOCAL_BACKUP_DIR"
                  "/system bzw. S3 unter system/).")
    return "\n".join(zeilen)

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
    __slots__ = ("_conn", "_herkunft")

    def __init__(self, conn, herkunft=None):
        self._conn = conn
        self._herkunft = herkunft        # (pfad, (dev, ino)) — v5.2-W191, Vorrat

    def __getattr__(self, name):
        # Alles was nicht explizit unten überschrieben ist, geht direkt
        # an die echte sqlite3.Connection (execute, cursor, row_factory, …)
        return getattr(self._conn, name)

    def __enter__(self):
        self._conn.__enter__()   # startet implizite Transaktion (sqlite3-Verhalten)
        return self

    def __exit__(self, exc_type, exc, tb):
        conn, self._conn = self._conn, _GESCHLOSSEN
        try:
            # sqlite3.Connection.__exit__ macht commit (kein exc) / rollback (exc)
            conn.__exit__(exc_type, exc, tb)
        finally:
            # v5.2-W191: zurueck in den Vorrat statt schliessen — ausser nach
            # einem Datenbankfehler (die Verbindung koennte selbst der Grund
            # sein). Die Huelle zeigt ab jetzt auf _GESCHLOSSEN: ein Zugriff
            # nach dem with wirft wie bisher, statt still auf einer Verbindung
            # zu arbeiten, die inzwischen ein anderer Thread benutzt.
            kaputt = exc_type is not None and issubclass(exc_type, sqlite3.DatabaseError)
            if kaputt or not _vorrat_ablegen(conn, self._herkunft):
                try:
                    conn.close()
                except Exception:
                    pass   # bereits geschlossen oder anderweitig kaputt — kein Crash hier
        return False    # Exception nicht unterdrücken


class _Geschlossen:
    """Platzhalter nach dem with-Block: jeder Zugriff wirft wie eine
    geschlossene sqlite3-Verbindung (ProgrammingError)."""
    __slots__ = ()

    def __getattr__(self, name):
        raise sqlite3.ProgrammingError("Cannot operate on a closed database.")


_GESCHLOSSEN = _Geschlossen()


# ── v5.2-W191: Vorrat freier SQLite-Verbindungen ────────────────────────
# Gedeckelt (DB_VORRAT, Vorgabe 4), prozess-global, LIFO. Jede Verbindung
# traegt (pfad, (st_dev, st_ino)) der Datei, die sie geoeffnet hat. Passt
# das beim Herausgeben nicht mehr — Datei getauscht, Pfad umkonfiguriert —,
# wird sie NICHT wieder ausgegeben: sonst hielte der Vorrat die alte Datei am
# Inode fest (die WAL-Falle aus W96, nur dauerhaft). Verworfene Verbindungen
# werden abgelegt statt geschlossen: das letzte close() einer WAL-Datenbank
# loescht `<pfad>-wal` per NAME — nach einem Tausch waere das die WAL der
# NEUEN Datei.
_VORRAT = []
_VORRAT_LOCK = threading.Lock()
_VORRAT_PID = {"pid": os.getpid()}
_ABGELEGT = []                       # verworfen, nie geschlossen (s.o.)
_ABGELEGT_MAX = 32
_VORRAT_STAT = {"neu": 0, "wieder": 0, "verworfen": 0}


def vorrat_groesse() -> int:
    """DB_VORRAT: so viele freie Verbindungen werden aufgehoben (0 = aus).
    Als Funktion gelesen, nicht als Konstante (CLAUDE.md, .env-Reihenfolge)."""
    roh = os.getenv("DB_VORRAT", "4").strip()
    return max(0, min(16, int(roh))) if roh.isdigit() else 4


def _kennung(pfad):
    """(st_dev, st_ino) der Datei oder None (gibt es nicht / nicht lesbar —
    dann wird die Verbindung nicht aufgehoben, sondern geschlossen)."""
    if not os.path.exists(pfad):
        return None
    st = os.stat(pfad)
    return (st.st_dev, st.st_ino)


def _vorrat_grund_melden(e):
    """Letzter Grund, warum eine Verbindung nicht zurueck in den Vorrat kam —
    steht in /healthz (vorrat_lage), denn hier wird nicht geloggt (dbwrap
    sitzt unter dem Log-Pfad mancher Aufrufer)."""
    _VORRAT_STAT["letzter_grund"] = "%s: %s" % (type(e).__name__, e)


def _ablegen(conn):
    if len(_ABGELEGT) < _ABGELEGT_MAX:
        _ABGELEGT.append(conn)
    else:
        conn.close()
    _VORRAT_STAT["verworfen"] += 1


def _vorrat_nehmen():
    """-> (conn, herkunft) aus dem Vorrat oder None."""
    if not _VORRAT:
        return None
    with _VORRAT_LOCK:
        if _VORRAT_PID["pid"] != os.getpid():
            # Nach einem fork gehoeren die Verbindungen dem Elternprozess —
            # weder benutzen noch schliessen, nur vergessen.
            _VORRAT.clear()
            _ABGELEGT.clear()
            _VORRAT_PID["pid"] = os.getpid()
            return None
        jetzt = (DB_PATH, _kennung(DB_PATH))
        while _VORRAT:
            conn, herkunft = _VORRAT.pop()
            if herkunft == jetzt and jetzt[1] is not None:
                _VORRAT_STAT["wieder"] += 1
                return conn, herkunft
            _ablegen(conn)
    return None


def _vorrat_ablegen(conn, herkunft) -> bool:
    """Saubere Verbindung zurueck in den Vorrat. -> False = selbst schliessen."""
    if not herkunft or herkunft[1] is None or herkunft[0] != DB_PATH:
        return False
    try:
        offen = conn.in_transaction      # wirft bei geschlossener Verbindung
        if offen:
            conn.rollback()
    except sqlite3.Error as e:
        _vorrat_grund_melden(e)
        return False
    with _VORRAT_LOCK:
        if _VORRAT_PID["pid"] != os.getpid() or len(_VORRAT) >= vorrat_groesse():
            return False
        _VORRAT.append((conn, herkunft))
    return True


def vorrat_leeren():
    """Alle freien Verbindungen schliessen — VOR einem Tausch der
    Datenbankdatei (nc.dbrestore.einsetzen). Danach oeffnet jeder Zugriff
    neu. -> wie viele."""
    with _VORRAT_LOCK:
        weg = list(_VORRAT)
        _VORRAT.clear()
    for conn, _h in weg:
        conn.close()                 # vor dem Tausch: die WAL gehoert noch ihr
    return len(weg)


def vorrat_lage() -> dict:
    """Fuer /healthz: wie oft neu geoeffnet, wie oft wiederverwendet.
    v5.2-W192: unter MariaDB der Pool dort — der SQLite-Vorrat ist dann leer
    und seine Nullen saehen aus wie ein Vorrat, der nichts tut."""
    if DB_BACKEND == "mariadb":
        return dict(mariadb_lage(), backend="mariadb")
    return dict(backend="sqlite", **_VORRAT_STAT, frei=len(_VORRAT), groesse=vorrat_groesse(),
                abgelegt=len(_ABGELEGT))


from decimal import Decimal as _Decimal


def _zahl(v):
    """Decimal -> int, wenn ganzzahlig, sonst float (wie SQLite liefert)."""
    return int(v) if v == v.to_integral_value() else float(v)


class _MariaDBRowProxy:
    """Macht ein DictCursor-Result (dict) zugriffsfähig sowohl per Key (row['x'])
       als auch per Index (row[0]). Damit ist es drop-in-kompatibel zu
       sqlite3.Row im bestehenden Code."""
    __slots__ = ('_d', '_keys')
    def __init__(self, d):
        # v4.2-W154: Decimal wie SQLite als Zahl. MariaDB liefert AVG/SUM und
        # DECIMAL-Spalten als decimal.Decimal; SQLite gibt float/int. Gemessen
        # beim Betreiber nach dem Umzug: "learned_params persist failed: Object
        # of type Decimal is not JSON serializable" — json.dumps kennt Decimal
        # nicht, und jede Stelle, die eine Summe ins Deck oder in die Datenbank
        # schreibt, stuerzte genauso. Umgewandelt wird hier, an der einen
        # Stelle, durch die jede MariaDB-Zeile geht.
        if d:
            d = {k: (_zahl(v) if isinstance(v, _Decimal) else v) for k, v in d.items()}
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
        # v4.2-W150: ohne Parameter None statt () — pymysql formatiert dann
        # nicht, und ein '%' in einem Literal bleibt, was es ist. Bewusst
        # dieselben zwei Aufrufe wie vorher: CodeQL fuehrt hier zwei bekannte
        # Fehlalarme (py/sql-injection, gebundene Parameter, W3).
        if params is None or (isinstance(params, (list, tuple)) and len(params) == 0):
            params = None
        translated = _translate_sql(sql, mit_parametern=params is not None)
        # PyMySQL erwartet tuple oder list
        if isinstance(params, dict):
            self._c.execute(translated, params)
        else:
            if params is not None and not isinstance(params, (list, tuple)):
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
        # v5.2-W192: nach einem erfolgreichen commit() im __exit__ ist die
        # Verbindung sauber — das rollback() in close() waere eine weitere
        # Rundreise zum Server, die nichts mehr zurueckrollt.
        self._sauber = False

    def execute(self, sql, params=()):
        # SQLite-Style: conn.execute → impliziter Cursor
        def _lauf():
            cur = _MariaDBCursorWrap(self._conn.cursor())
            cur.execute(sql, params)
            return cur
        return self._erste_mit_wiederanlauf(_lauf)

    def executemany(self, sql, seq):
        def _lauf():
            cur = _MariaDBCursorWrap(self._conn.cursor())
            cur.executemany(sql, seq)
            return cur
        return self._erste_mit_wiederanlauf(_lauf)

    def cursor(self):
        self._conn._nc_ungeprueft = False      # ab hier kein Wiederanlauf
        return _MariaDBCursorWrap(self._conn.cursor())

    def _erste_mit_wiederanlauf(self, lauf):
        """v5.2-W192: die ERSTE Anweisung auf einer Verbindung, die ohne ping
        ausgeliehen wurde, darf einen Abriss einmal ueberleben.

        Ohne das kostete der gesparte ping nach jedem Server-Neustart genau
        einen gescheiterten Aufruf (gegen MariaDB 10.11 gemessen: 2013 Lost
        connection). Wiederholt wird nur die erste Anweisung: davor lief in
        dieser Transaktion nichts, also geht nichts doppelt oder verloren."""
        erst = getattr(self._conn, "_nc_ungeprueft", False)
        self._conn._nc_ungeprueft = False
        try:
            return lauf()
        except Exception as e:
            if not (erst and _verbindung_verloren(e)):
                raise
            _mariadb_grund_melden(e)
            _MARIADB_STAT["wiederangelaufen"] += 1
            tot, self._conn = self._conn, None
            try:
                tot.close()
            except Exception as e2:
                _mariadb_grund_melden(e2)
            _mariadb_pool_leeren()            # die freien haengen am selben Server
            try:
                self._conn = _mariadb_neue_verbindung(_MARIADB_POOL)
            except Exception:
                p = _MARIADB_POOL
                if p is not None:             # Slot der toten Verbindung freigeben
                    with p._lock:
                        p._created = max(0, p._created - 1)
                raise
            return lauf()

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
            if not self._sauber:
                try: conn.rollback()
                except Exception: pass
            if _MARIADB_POOL is not None:
                conn._nc_frei_seit = _time.monotonic()   # v5.2-W192, s. _mariadb_connect
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
                self._sauber = True
            else:
                self.rollback()
        except Exception as e:
            # Commit gescheitert: die Verbindung kann selbst der Grund sein.
            if _verbindung_verloren(e):
                self._verloren_abgeben()
            raise
        finally:
            if exc is not None and _verbindung_verloren(exc):
                self._verloren_abgeben()
            self.close()
        return False    # do not suppress exception

    def _verloren_abgeben(self):
        """v5.2-W192: Verbindung weg (Server-Neustart, Netz) — NICHT zurueck in
        den Pool. Und die freien gleich mit: sie haengen am selben toten Server,
        und seit nicht mehr bei jedem Ausleihen gepingt wird, faende sonst jede
        von ihnen den Abriss erst mit dem naechsten Aufrufer."""
        conn, self._conn = self._conn, None
        if conn is None:
            return
        try:
            conn.close()
        except Exception as e:
            _mariadb_grund_melden(e)
        _MARIADB_STAT["verloren"] += 1
        p = _MARIADB_POOL
        if p is not None:
            with p._lock:
                p._created = max(0, p._created - 1)
            _mariadb_pool_leeren()


# ------------------------------------------------------------------
# db_conn + MariaDB-Pool (V37: aus bot.py hierher)
# ------------------------------------------------------------------

# ── v5.2-W192: MariaDB-Pool — Kennzahlen und Abriss ─────────────────────
_MARIADB_STAT = {"erstellt": 0, "wieder": 0, "pings": 0, "pings_gespart": 0,
                 "gewartet": 0, "erschoepft": 0, "verloren": 0, "wiederangelaufen": 0}
# Fehlercodes fuer "Verbindung weg" (CR_SERVER_GONE_ERROR, CR_SERVER_LOST,
# CR_CONN_HOST_ERROR, CR_SERVER_LOST_EXTENDED, ER_CONNECTION_KILLED u. a.).
_VERLOREN_CODES = frozenset((2003, 2006, 2013, 2055, 1927, 4031))


def _mariadb_grund_melden(e):
    """Letzter Grund aus dem Pool (Ping gescheitert, close() auf toten Socket)
    — steht in /healthz (mariadb_lage). dbwrap loggt hier nicht: es sitzt
    unter dem Log-Pfad mancher Aufrufer, und ein Abriss trifft viele zugleich."""
    _MARIADB_STAT["letzter_grund"] = "%s: %s" % (type(e).__name__, e)


def _ping_nach_s() -> float:
    """MARIADB_PRUEFEN_NACH_S: ab so viel Leerlauf wird vor dem Ausleihen gepingt
    (Vorgabe 30; 0 = jedes Mal, wie vor W192). Als Funktion gelesen."""
    roh = os.getenv("MARIADB_PRUEFEN_NACH_S", "30").strip()
    return float(roh) if roh.replace(".", "", 1).isdigit() else 30.0


def _verbindung_verloren(e) -> bool:
    """Ist das ein Abriss der Verbindung (nicht ein Fehler der Abfrage)?"""
    if type(e).__name__ == "InterfaceError":
        return True                       # PyMySQL: "(0, '')" = Socket zu
    code = e.args[0] if getattr(e, "args", None) else None
    return isinstance(code, int) and code in _VERLOREN_CODES


def _mariadb_pool_leeren():
    """Alle freien Pool-Verbindungen schliessen (nach einem Abriss)."""
    p = _MARIADB_POOL
    n = 0
    while p is not None:
        try:
            conn = p._q.get_nowait()
        except Exception:
            break                         # leer
        try:
            conn.close()
        except Exception as e:
            _mariadb_grund_melden(e)
        with p._lock:
            p._created = max(0, p._created - 1)
        n += 1
    return n


def mariadb_lage() -> dict:
    """Fuer /healthz: Groesse, belegt, frei und was der Pool getan hat."""
    p = _MARIADB_POOL
    frei = p._q.qsize() if p is not None else 0
    erstellt = p._created if p is not None else 0
    return dict(_MARIADB_STAT, groesse=MARIADB_POOL_SIZE, offen=erstellt,
                frei=frei, belegt=max(0, erstellt - frei),
                ping_nach_s=_ping_nach_s())


def _mariadb_neue_verbindung(p):
    """Eine frische PyMySQL-Verbindung mit den Einstellungen des Pools."""
    return p._pymysql.connect(
        host=MARIADB_HOST, port=MARIADB_PORT,
        user=MARIADB_USER, password=MARIADB_PASSWORD,
        database=MARIADB_DB, charset="utf8mb4",
        autocommit=False,
        cursorclass=p._DictCursor,
        connect_timeout=10, read_timeout=30, write_timeout=30)


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
        return _mariadb_neue_verbindung(p)

    # Versuche eine bestehende zu kriegen
    conn = None
    try:
        conn = p._q.get_nowait()
        _MARIADB_STAT["wieder"] += 1
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
                _MARIADB_STAT["erstellt"] += 1
            except Exception:
                # Connect fehlgeschlagen — Slot wieder freigeben sonst leakt's
                with p._lock:
                    p._created -= 1
                raise
        else:
            # Pool voll — auf Rückgabe einer existierenden Conn warten
            _MARIADB_STAT["gewartet"] += 1
            try:
                conn = p._q.get(timeout=10)
            except Exception:
                _MARIADB_STAT["erschoepft"] += 1
                log.error(f"MariaDB connect: pool exhausted ({MARIADB_POOL_SIZE} "
                          f"connections all in use), waited 10s")
                raise

    # Connection-Liveness-Check (TCP kann zwischendurch droppen).
    # v5.2-W192: nur nach Leerlauf. Vorher lief ping() bei JEDEM Ausleihen —
    # gemessen 37 us je Zugriff auf localhost, ueber ein echtes Netz ein
    # Vielfaches, und das fuer eine Verbindung, die Millisekunden vorher noch
    # benutzt wurde. Eine frisch benutzte Verbindung, die trotzdem gerade
    # abgerissen ist, faellt beim Gebrauch auf; __exit__ gibt sie dann ab und
    # leert den Pool (_verloren_abgeben). ping(reconnect=True) ist in PyMySQL
    # ausserdem abgekuendigt — ersetzt wird durch eine neue Verbindung.
    frei_seit = getattr(conn, "_nc_frei_seit", None)
    if frei_seit is None or _time.monotonic() - frei_seit >= _ping_nach_s():
        _MARIADB_STAT["pings"] += 1
        try:
            conn.ping(reconnect=False)
        except Exception as e:
            _mariadb_grund_melden(e)
            try: conn.close()
            except Exception: pass
            try:
                conn = _new_connection()
            except Exception:
                # Replacement fehlgeschlagen — Slot freigeben
                with p._lock:
                    p._created -= 1
                raise
    else:
        _MARIADB_STAT["pings_gespart"] += 1
        conn._nc_ungeprueft = True             # s. _erste_mit_wiederanlauf
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
    # v5.2-W191: zuerst aus dem Vorrat (siehe _vorrat_nehmen). Eine frische
    # Verbindung kostete gemessen 180 us (Oeffnen, fuenf PRAGMAs, Schema
    # einlesen), eine wiederverwendete 2 us — und der 8-MB-Seiten-Cache unten
    # wurde mit jeder Verbindung verworfen, also nie warm.
    _aus_vorrat = _vorrat_nehmen()
    if _aus_vorrat is not None:
        return _SQLiteConnWrap(*_aus_vorrat)
    # SQLite path (default)
    # B80-Fix: 'database is locked' unter Last (Whisper + Restream + Polling +
    # Dashboard gleichzeitig). Drei Ursachen behoben:
    #  (a) timeout 10s → 30s: mehr Geduld bei kurzen Schreib-Locks.
    #  (b) busy_timeout-PRAGMA: SQLite WARTET aktiv auf Lock-Freigabe statt sofort
    #      OperationalError zu werfen (der Python-timeout allein deckt nicht jeden Pfad).
    #  (c) journal_mode=WAL ist eine DAUERHAFTE Datei-Eigenschaft — es bei JEDER
    #      Connection zu setzen ist ein Schreibzugriff, der selbst blockieren kann.
    #      Jetzt nur EINMAL prozessweit (per Flag) statt ~208×/Tick.
    # check_same_thread=False: eine Verbindung aus dem Vorrat bedient
    # nacheinander verschiedene Threads (nie zwei zugleich — sie ist bis zum
    # Ende des with-Blocks ausgeliehen).
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=30000")    # 30s aktiv auf Locks warten
        if not _WAL_INIT["done"]:
            try:
                conn.execute("PRAGMA journal_mode=WAL")
                _WAL_INIT["done"] = True
            except sqlite3.DatabaseError:
                # journal_mode faellt bei einer kaputten Datei genauso — aber
                # hier NICHT diagnostizieren, sonst haengt das Flag und jede
                # weitere Connection wiederholt den WAL-Versuch. Das naechste
                # PRAGMA unten faellt ohnehin und liefert die Diagnose.
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
    except sqlite3.DatabaseError as e:
        # v4.2-W92: HIER starb der Start am 17.09. — mit dem nackten Satz
        # "file is not a database" und einem Traceback durch drei Dateien.
        # sqlite3.connect() selbst wirft nicht: es oeffnet die Datei erst
        # beim ersten PRAGMA, das den Header braucht. Deshalb faellt es an
        # dieser Stelle und nicht oben.
        #
        # Die Verbindung wird geschlossen, bevor die Diagnose laeuft: sonst
        # haelt jeder gescheiterte Versuch ein Datei-Handle auf eine Datei,
        # die der Betreiber gleich sichern will.
        try:
            conn.close()
        except sqlite3.Error:
            pass        # Aufraeumpfad: ein close() auf eine kaputte Datei
                        # darf fehlschlagen, das aendert an der Lage nichts
        raise DatenbankUnlesbar(
            "Die Datenbank ist nicht zu oeffnen: %s\n\n%s"
            % (e, datei_diagnose(DB_PATH))) from e
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
    _VORRAT_STAT["neu"] += 1
    return _SQLiteConnWrap(conn, (DB_PATH, _kennung(DB_PATH)))


# ═══════════════════════════════════════════════════════════════════════════
# v4.1-W29: Datenbankarbeit NEBEN dem Event-Loop
# ═══════════════════════════════════════════════════════════════════════════
#
# BEFUND AUS DEM BETRIEBSLOG (2026-09-03). Der Waechter meldete Blockaden von
# 30 bis 68 Sekunden; die Stack-Abzuege zeigten unter anderem
#
#     _handle_single_tracking -> try_acquire_recording_lock
#       -> db_conn().__exit__ -> close()
#
# SQLite blockiert unter Plattenlast. Steht der Aufruf direkt in einer
# async-Funktion, blockiert er nicht die Abfrage, sondern den GANZEN Bot:
# keine Live-Pruefungen, kein Telegram, Discord trennt mit "heartbeat
# blocked". W26 hat die zwei Stellen behoben, die in den Abzuegen standen —
# im Bestand sind es weit ueber hundert.
#
# `db_async` ist der Weg dorthin. Sie nimmt eine Funktion, die eine
# Verbindung bekommt, und fuehrt sie mitsamt Verbindungsaufbau und -abbau in
# einem Thread aus:
#
#     rows = await db_async(lambda c: c.execute("SELECT …").fetchall())
#
# Die Verbindung entsteht IM Thread und stirbt dort. Das ist keine
# Bequemlichkeit, sondern Pflicht: eine sqlite3-Verbindung gehoert dem
# Thread, der sie geoeffnet hat (`check_same_thread`), und eine ueber die
# Thread-Grenze gereichte Verbindung wirft zur Laufzeit.

async def db_async(fn, *args, **kwargs):
    """`fn(conn, *args, **kwargs)` mit eigener Verbindung in einem Thread.

    Der Rueckgabewert ist der von `fn`. Ausnahmen kommen unveraendert beim
    Aufrufer an — hier wird bewusst nichts geschluckt: wer eine Abfrage
    absetzt, muss ihr Scheitern sehen koennen.

    ACHTUNG bei Cursorn: was `fn` zurueckgibt, muss die Verbindung ueberleben.
    `fetchall()` liefert Zeilen, `execute()` liefert einen Cursor — und der ist
    nach dem `with`-Block tot. Deshalb IMMER im `fn` auslesen, nie danach.
    """
    def _lauf():
        with db_conn() as conn:
            return fn(conn, *args, **kwargs)

    return await asyncio.to_thread(_lauf)
