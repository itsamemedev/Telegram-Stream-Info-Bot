---
name: nc-datenbank
description: SQL und Schema in NIGHTCRAWLER unter zwei Backends (SQLite und MariaDB) schreiben, ohne eines von beiden zu brechen — was der Übersetzungs-Layer nc.sqlutil kann und was nicht, backend-neutrale Muster, Schema-Migration, Connection-Lebensdauer. Nutze dies bei jeder Änderung an SQL, init_db, Tabellen, Indexen, Queries oder nc/dbwrap.py, nc/sqlutil.py, nc/dbexport.py. Trigger: SQL, Query, Tabelle, Schema, Migration, Spalte, Index, SQLite, MariaDB, DB_BACKEND, db_conn, pymysql, COLLATE.
---

# Datenbank — zwei Backends, ein Code

## Die Grundannahme

Derselbe SQL-Text läuft gegen **MariaDB** (Betrieb und Installer-Vorgabe seit v5.3.1; im Code bleibt SQLite die Vorgabe) und **SQLite**
(`DB_BACKEND=mariadb`, Pool über pymysql). Der gesamte Bot-Code ist
backend-agnostisch geschrieben; die Anpassung macht `nc.sqlutil._translate_sql`
auf dem MariaDB-Pfad. Wer SQL anfasst, muss wissen, wie **wenig** dieser Layer
übersetzt — sonst schreibt man Code, der auf der Entwicklungsmaschine (SQLite)
sauber läuft und in Produktion mit MariaDB crasht.

## Was `_translate_sql` tut — und nur das

    ?  →  %s        Platzhalter, stringbewusst (Fragezeichen in Literalen bleiben)
    %  →  %%        weil PyMySQL '%' als Format-Zeichen liest

**Das ist alles.** Keine Funktionen, keine Collations, keine Dialekt-Syntax.
Alles andere muss der Aufrufer backend-neutral schreiben oder selbst verzweigen.

## Die Muster, die auf beiden Backends halten

| statt SQLite-only | backend-neutral |
|---|---|
| `COLLATE NOCASE` | `LOWER(spalte) LIKE LOWER(?)` |
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `_schema_pk()` |
| `TEXT` als UNIQUE/Index-Spalte | `txt_idx` (→ `VARCHAR(255)` auf MariaDB) |
| `CREATE INDEX IF NOT EXISTS` | `_create_index_safe(conn, sql)` |
| `PRAGMA table_info(t)` | `_migrate_columns(conn, t, expected)` |
| `datetime('now','-7 days')` | Grenzwert in Python berechnen, als Parameter binden |
| `ON CONFLICT(k) DO UPDATE SET …` | `_nc_sqldialekt.bei_konflikt(DB_BACKEND, "k", [...])` |
| Spalte `lines`, `trigger`, `key`, `order` … | in Backticks: `` `lines` `` — auch in jeder Abfrage |
| Zeitstempel als Index-Spalte (`{txt_long}`) | `{ts}` (→ `VARCHAR(64)` auf MariaDB) |

Der letzte Punkt ist der unauffälligste: `datetime('now', ?)` sieht wie
Parametrisierung aus und wird auch korrekt zu `%s` übersetzt — aber die
**Funktion** `datetime()` existiert in MariaDB nicht. Zeitfenster gehören nach
Python:

    grenze = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    conn.execute("... WHERE ts >= ?", (grenze,))

Das funktioniert, weil Datumswerte in **beiden** Backends als ISO-Strings in
TEXT/VARCHAR liegen — nie als natives DATETIME. Diese Entscheidung ist bewusst
und bleibt so; ISO-Strings sortieren lexikografisch korrekt.

Im Bestand gibt es dafür ein zweites, älteres Muster: SQLite-Variante im `try`,
MariaDB-Variante (`NOW() - INTERVAL n DAY`) im `except` — so gelöst bei
`brain_growth` (~Z. 12262) und den Donation-Summen (~Z. 16928). Das funktioniert,
verschluckt aber jeden *anderen* Fehler der ersten Query in den Fallback. Für
neuen Code deshalb die Python-Variante; das Bestandsmuster nur beibehalten, wo es
schon steht.

Ohne beides steht `_rule_based_sql` in `nc/sqlutil.py`: es erzeugt
`datetime('now', …)` und `date('now')` ungeschützt, und das Ergebnis wird in
`api_ai_query` direkt ausgeführt. Dieser NL→SQL-Fallback (greift, wenn kein LLM
antwortet) läuft nur gegen SQLite. Bei Arbeiten dort nicht überrascht sein und
keine neuen Aufrufstellen schaffen.

## Schema

`init_db()` in `bot.py` (ab ~Z. 3750) baut alle Tabellen backend-aware über
Platzhalter, die oben im Block gesetzt werden:

    pk        _schema_pk()      AUTO_INCREMENT-PK in nativer Form
    txt_idx   VARCHAR(255)|TEXT indizierte/unique Textspalte
    txt_long  TEXT              nicht indizierter Text
    txt_big   MEDIUMTEXT|TEXT   große Nutzlast (JSON-Blobs)
    iv        INTEGER           Ganzzahl, beide Backends
    tbl_opts  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 …   (leer bei SQLite)

Jede neue Tabelle nutzt **alle** davon und endet auf `){tbl_opts}` — also
`f"""CREATE TABLE …"""`, nicht `"""CREATE TABLE …"""`. Ein vergessenes `f` ist
der häufigste Fehler hier: der Text enthält dann wörtlich `{pk}` und die
Tabelle entsteht nie.

Das Schema steht seit dem Umzug in `nc/schema.py` (`create_schema`), die
Platzhalter liefert `nc.schema.parameter(backend)` — dieselbe Tabelle für
`init_db()` und für `tools/zu_mariadb.py`.

**Bis v4.2-W143 war es auf MariaDB nie lauffähig**, und niemand hatte es gegen
einen Server gefahren: `lines` und `trigger` sind reservierte Wörter (1064),
und neun indizierte Spalten waren `{txt_long}` (1071, Schlüssel über 3072
Bytes). Dazu zwei Upserts mit `ON CONFLICT`, die auf MariaDB still nie
buchten. Der Vertrag `_test_v42_w143_mariadb_schema_und_dialekt` schneidet das
MariaDB-Schema ohne Server mit und prüft beides statisch. **Wer am Schema
arbeitet, fährt es einmal gegen einen echten MariaDB** — ein Schema, das nur
SQLite gesehen hat, ist für MariaDB ungeprüft.

## SQLite → MariaDB umziehen

    bash tools/update.sh --mariadb          (oder geführt: bash tools/update.sh)
    venv/bin/python tools/zu_mariadb.py --dry-run

`nc/mariadbumzug.py`: Quelle nur lesend (`mode=ro`, `integrity_check`), Ziel
muss leer sein, Export im Dialekt des Ziels, Schema anlegen, Import, **jede
Tabelle nachzählen** — erst dann schreibt `zu_mariadb.py` `DB_BACKEND=mariadb`
in die `.env` (vorher `.env.vor-mariadb-<zeit>`). Ob der Bot noch läuft,
entscheidet ein offenes Handle in `/proc`, nicht die mtime: beim sauberen
Stopp schreibt SQLite die Datei noch einmal (Checkpoint). Rückweg:
`DB_BACKEND=sqlite`, die Datei bleibt liegen.

## Spalten nachrüsten, nicht Tabellen neu bauen

`CREATE TABLE IF NOT EXISTS` überspringt existierende Tabellen — eine neue Spalte
entsteht dadurch **nicht**, und Queries crashen später mit `no such column`. Neue
Spalten gehören immer zusätzlich in `_migrate_columns`:

    _migrate_columns(conn, "trackings", {"priority_level": "INT DEFAULT 0"})

`_migrate_columns` schluckt Fehler bewusst und loggt auf `info`/`warning`. Nach
einer Schema-Änderung deshalb im Log gezielt nach `DB-Migration` greifen — ohne
das läuft der Dienst mit fehlender Spalte scheinbar normal weiter.

## Connection-Lebensdauer

`with db_conn() as conn:` schließt die Verbindung deterministisch beim Verlassen
des Blocks — auf **beiden** Backends (`_SQLiteConnWrap.__exit__` ruft `close()`,
weil `sqlite3.Connection.__exit__` nur committet).

Daraus folgt die Regel, die schon einmal verletzt wurde: **kein `conn.execute()`
außerhalb des `with`-Blocks.** Auf SQLite fällt das zufällig nicht auf, auf
MariaDB ist es ein Use-after-free — die Connection ist zurück im Pool und der
nächste Nutzer bekommt sie. Beim Aufbau von Ergebnislisten aus mehreren Queries
muss der **ganze** Aufbau in den Block, nicht nur die erste Query.

`cur.lastrowid` funktioniert auf beiden Backends und ist der Weg zur neuen ID —
`RETURNING` nicht verwenden.

Rows verhalten sich auf beiden Backends wie Dicts (`row["spalte"]`). Numerischer
Index (`row[1]`) funktioniert nur auf SQLite und steckt zu Recht nur in
`PRAGMA`-Auswertungen.

## Prüfung vor Auslieferung

Es gibt keine MariaDB auf der Entwicklungsmaschine — SQLite-Läufe beweisen also
nichts über MariaDB. Ersatzweise nach jeder SQL-Änderung gezielt gegenlesen:

    python tools/ncpatch.py grep "COLLATE\|datetime('now'\|AUTOINCREMENT\|PRAGMA " bot.py

Jeder Treffer außerhalb von `_schema_pk`/`_migrate_columns` ist erklärungspflichtig.

    python -m py_compile bot.py && python test_nc_modules.py

`nc/dbexport.py` kann ein Backend in den Dialekt des anderen exportieren
(`/api/db/export?dialect=mariadb|sqlite`) — das ist der Migrationsweg, kein
Prüfwerkzeug.
