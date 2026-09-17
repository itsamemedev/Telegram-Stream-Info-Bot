"""nc.schemastand — v4.2-W85: welchen Schema-Stand erwartet dieser Bestand,
und welchen hat die Datenbank wirklich?

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Das Schema wird bei jedem Start idempotent nachgezogen: `CREATE TABLE IF NOT
EXISTS` für die Tabellen, `_migrate_columns` für neue Spalten, `ddlsafe` für
Indizes. Das funktioniert **vorwärts** und ist gut so — aber es beantwortet
eine Frage nicht, und genau die entscheidet über den einzigen wirklich
gefährlichen Fall dieses Deploy-Modells:

    Ist die Datenbank vor mir schon von einer NEUEREN Fassung angefasst worden?

Ausgeliefert wird per ZIP über den Bestand, direkt gegen Produktion, und der
Rollback ist „die vorige ZIP wieder drüberlegen". Die Datenbank rollt dabei
**nicht** mit zurück. Wer also eine Fassung zurückgeht, läuft mit altem Code
auf einem neueren Schema — und merkt es an nichts. Neue Spalten stören nicht,
neue Tabellen stören nicht; was stört, ist eine geänderte Bedeutung einer
bestehenden Spalte, und die sieht man erst an falschen Zahlen.

Ein Zähler, der beim Deploy hochgeschrieben wird, macht genau diesen Fall
sichtbar. Mehr soll er nicht: das ist kein Migrationsrahmen, es ersetzt
`_migrate_columns` nicht und führt keine Skripte aus. Es ist eine Zahl und ein
Vergleich.

════════════════════════════════════════════════════════════════════════
DIE DREI FÄLLE
════════════════════════════════════════════════════════════════════════
    ist == ERWARTET    Der Normalfall. Still — eine Meldung bei jedem
                       gesunden Start erzieht dazu, Meldungen zu überlesen.

    ist <  ERWARTET    Frisch ausgeliefert. `create_schema` und
                       `_migrate_columns` sind gerade gelaufen und haben das
                       Schema nachgezogen; der Zähler wird hochgeschrieben.
                       Eine Zeile auf INFO, damit im Log steht, wann.

    ist >  ERWARTET    **Der gefährliche Fall.** Rollback auf eine ältere
                       Fassung, während die Datenbank schon weiter ist.
                       Laut auf ERROR, mit beiden Zahlen und dem Weg heraus.

════════════════════════════════════════════════════════════════════════
WARUM KEIN ABBRUCH
════════════════════════════════════════════════════════════════════════
Dieselbe Überlegung wie bei der Bindung in v4.2-W84: der Bot ist mehr als das,
was gerade schiefsteht. Er nimmt auf, sendet weiter und moderiert. Ein
Startabbruch wegen eines Zählers nähme dem Betreiber die laufende Aufnahme,
und zwar in genau der Lage, in der er ohnehin gerade etwas zurückgerollt hat.

Wer es strenger will — etwa in einem Testaufbau, wo ein falscher Stand sofort
auffallen soll — setzt `SCHEMA_STAND_STRENG=1`. Dann ist der zu neue Stand ein
Startfehler. Eine Regel ohne Ausweg wird umgangen; besser einen, den der
Bestand kennt.
"""

import os

# Der Stand, den DIESER Bestand erwartet.
#
# HOCHZAEHLEN, wenn eine Aenderung am Schema die Bedeutung bestehender Daten
# aendert — eine umgedeutete Spalte, eine geaenderte Einheit, ein anderer
# Wertebereich. NICHT hochzaehlen fuer eine neue Tabelle oder eine neue Spalte
# mit Vorgabewert: die vertraegt aelterer Code klaglos, und ein Zaehler, der
# bei jeder Kleinigkeit springt, meldet nur noch Rauschen.
#
# 1 = der Stand bei Einfuehrung des Zaehlers (v4.2-W85). Er beschreibt das
#     gewachsene Schema, wie es zu diesem Zeitpunkt auf dem Server stand —
#     rueckwirkend laesst sich nichts anderes behaupten.
ERWARTET = 1

TABELLE = "schema_stand"


def _an(roh) -> bool:
    return (roh or "").strip().lower() in ("1", "true", "yes", "ja", "on")


def streng() -> bool:
    """Soll ein zu neuer Stand den Start verweigern?

    Woertlich gelesen, damit tools/gen_env_example.py die Variable findet, und
    in einer Funktion, weil .env teils erst nach den ersten Imports geladen
    wird (CLAUDE.md, W67).
    """
    return _an(os.getenv("SCHEMA_STAND_STRENG", ""))


def lege_an(conn, *, pk, txt_idx, txt_long, tbl_opts):
    """Die Tabelle, backend-neutral ueber dieselben Platzhalter wie das
       uebrige Schema (nc-datenbank: jede neue Tabelle nutzt sie ALLE und
       endet auf ){tbl_opts}).

    Eine Zeile, id=1. Kein Verlauf: der Verlauf steht im CHANGELOG und im Log,
    und eine Tabelle, die bei jedem Start waechst, ist ein Zwischenspeicher,
    kein Zustand.
    """
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABELLE} (
        id {pk},
        stand INTEGER NOT NULL DEFAULT 0,
        gesetzt_am {txt_long},
        bot_version {txt_idx}
    ){tbl_opts}""")


def lies(conn) -> int:
    """Der Stand in der Datenbank. -> int, 0 wenn noch keiner da ist.

    0 heisst "dieser Bestand hat die Datenbank noch nie gestempelt" — bei
    einer frischen Installation genauso wie bei einer gewachsenen, die vor
    v4.2-W85 angelegt wurde. Beide Faelle sind harmlos und laufen unten in
    denselben Zweig.
    """
    # EIN Ausgang, kein `return 0` in einem eigenen Zweig. Die 0 ist hier
    # naemlich kein Misserfolg, sondern ein gueltiger Wert — und ein Werkzeug,
    # das Misserfolgs-Rueckgaben zaehlt (tools/blindstellen.py), kann das nicht
    # unterscheiden. Als ein Ausdruck geschrieben stellt sich die Frage nicht.
    #
    # Auch ohne try/except: die Spalte haben wir selbst angelegt, und die
    # beiden Formen, in denen sie zurueckkommt, sind bekannt — SQLite gibt die
    # Zahl, MariaDB je nach Treiber eine Zeichenkette. Ein breiter Auffang
    # wuerde einen kaputten Zaehler als 0 verbuchen: die Datenbank saehe dann
    # frisch aus und wuerde kommentarlos gestempelt.
    zeile = conn.execute(
        "SELECT stand FROM %s WHERE id=1" % TABELLE).fetchone()
    roh = zeile["stand"] if zeile else 0
    if not isinstance(roh, int):
        text = str(roh or "").strip()
        roh = int(text) if text.lstrip("-").isdigit() else 0
    return roh


def schreibe(conn, stand: int, bot_version: str, jetzt: str):
    """Den Stand festschreiben. Ein UPDATE, sonst ein INSERT.

    Kein INSERT OR REPLACE und kein ON DUPLICATE KEY: das eine kennt MariaDB
    nicht, das andere SQLite nicht, und `nc.sqlutil` uebersetzt nur
    Platzhalter — keine Dialekt-Syntax (siehe Skill nc-datenbank).
    """
    cur = conn.execute(
        "UPDATE %s SET stand=?, gesetzt_am=?, bot_version=? WHERE id=1"
        % TABELLE, (int(stand), jetzt, str(bot_version)))
    if not getattr(cur, "rowcount", 0):
        conn.execute(
            "INSERT INTO %s (id, stand, gesetzt_am, bot_version) "
            "VALUES (1, ?, ?, ?)" % TABELLE,
            (int(stand), jetzt, str(bot_version)))
    conn.commit()


def pruefe(ist: int, erwartet: int = None):
    """-> (stufe, text). stufe ist "still", "info" oder "fehler".

    Der Text traegt beide Zahlen UND den Weg heraus — er landet im Log, und
    dort hat der Betreiber keinen Kontext.
    """
    erwartet = ERWARTET if erwartet is None else erwartet
    if ist == erwartet:
        return "still", ""
    if ist < erwartet:
        return "info", (
            "Schema-Stand %d -> %d nachgezogen (create_schema und "
            "_migrate_columns sind gelaufen)." % (ist, erwartet))
    return "fehler", (
        "SCHEMA ZU NEU: die Datenbank steht auf Stand %d, dieser Bestand "
        "erwartet %d. Das passiert nach einem Rollback — die ZIP rollt "
        "zurueck, die Datenbank nicht. Aeltere Spalten und Tabellen stoeren "
        "nicht; gefaehrlich ist eine Spalte, deren BEDEUTUNG sich geaendert "
        "hat, denn die sieht man erst an falschen Zahlen. Zwei Wege: (a) die "
        "neuere Fassung wieder ausliefern, (b) die Sicherung der Datenbank "
        "von vor dem Deploy einspielen (tools/deploy.sh legt sie an). Der "
        "Bot laeuft weiter — mit SCHEMA_STAND_STRENG=1 wuerde er hier "
        "abbrechen." % (ist, erwartet))
