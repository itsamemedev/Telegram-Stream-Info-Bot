"""nc.ddlsafe — v4.2-W65: idempotentes DDL, das nur das Erwartete schluckt.

Zwei Stellen im Bestand legen Indizes und Spalten bei jedem Start neu an und
fangen dabei ALLES ab:

    nc/ledger.py:118   for stmt in _IDX: try: conn.execute(stmt) except: pass
    nc/schema.py:484   ALTER TABLE … ADD COLUMN …    try: … except: pass

Der Grund dafuer ist richtig: „Index existiert bereits" und „duplicate column"
kommen bei jedem zweiten Start, und eine Meldung, die bei jedem gesunden Start
erscheint, erzieht dazu, Meldungen zu ueberlesen. MariaDB kennt fuer Indizes
ausserdem kein verlaessliches IF NOT EXISTS.

Falsch ist der Umfang. `except Exception: pass` schluckt auch die gesperrte
Datenbank, den Tippfehler im DDL und die fehlende Tabelle — und dann laeuft der
Dienst mit einem Schema weiter, das anders aussieht, als der Code annimmt. Beim
Ledger ist das besonders unangenehm: das ist das Steuer-Journal mit Hash-Kette,
kein Zwischenspeicher.

Der Bot hat fuer denselben Zweck laengst `_create_index_safe` (bot.py:3628) und
prueft dort auf 1061/„exist". Die beiden nc-Module koennen den Helfer nicht
benutzen — `nc/*` importiert nie aus `bot.py`. Deshalb hier dieselbe
Unterscheidung noch einmal, bot-frei und pruefbar.
"""

# Was ein Backend sagt, wenn das Ding schon da ist.
#
#   SQLite    "index idx_x already exists" / "duplicate column name: x"
#   MariaDB   1061 duplicate key name / 1060 duplicate column name
#
# Bewusst als Textmuster UND Fehlernummer: pymysql liefert die Nummer im
# Argument-Tupel, sqlite3 nur den Satz. Wer nur auf eines prueft, uebersieht
# ein Backend — und dann ist die Meldung entweder bei jedem Start da oder nie.
_BEKANNT = ("already exists", "duplicate column", "duplicate key name",
            "existiert bereits", "1060", "1061")


def ist_schon_da(exc) -> bool:
    """War das nur „existiert bereits"? -> bool

    Alles andere ist ein echter Fehler und gehoert gemeldet: eine gesperrte
    Datenbank, ein Tippfehler im DDL, eine fehlende Tabelle.
    """
    t = str(exc).lower()
    return any(m in t for m in _BEKANNT)


def ddl(conn, sql, melden=None) -> bool:
    """Ein idempotentes DDL ausfuehren. -> True, wenn es wirklich lief.

    `melden(text, exc)` bekommt jeden UNERWARTETEN Fehler. Ohne `melden` wird
    ein solcher Fehler GEWORFEN statt geschluckt — eine Bibliothek ohne
    Logger soll nicht still danebengreifen. Der Aufrufer entscheidet, ob er
    das ueberleben will; nur er weiss, ob das Schema fuer ihn tragend ist.

    „Existiert bereits" ist nie ein Fehler und wird nie gemeldet: das ist der
    Normalfall ab dem zweiten Start.
    """
    try:
        conn.execute(sql)
        return True
    except Exception as e:
        if ist_schon_da(e):
            return False
        if melden is None:
            raise
        melden("DDL fehlgeschlagen: %s" % sql.strip().split("\n")[0][:120], e)
        return False
