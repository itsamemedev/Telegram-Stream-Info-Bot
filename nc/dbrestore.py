"""nc.dbrestore — v4.2-W96: eine Sicherung im Deck auswaehlen, pruefen, einsetzen.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
W95 hat den Deck-Import dichtgemacht: ein Systemarchiv-Dump wird abgelehnt,
statt halb eingespielt zu werden. Richtig — aber damit gab es im Deck gar
keinen Weg mehr zurueck, und der Betreiber wollte genau den:

    "Ich starte mit einer leeren Datenbank klar startet der bot...
     Also los jetzt"

Das ist der Weg, der ohne Werkzeugkasten auskommt: leere Datenbank, Bot
laeuft, Deck erreichbar, Sicherung von dort einspielen.

════════════════════════════════════════════════════════════════════════
DIE FALLE, DIE DEN GANZEN VORGANG STILL WERTLOS MACHT
════════════════════════════════════════════════════════════════════════
SQLite laeuft hier im **WAL-Modus** (nc/dbwrap.py setzt journal_mode=WAL).
Neben `tiktok_bot.db` liegen deshalb `tiktok_bot.db-wal` und `-shm`. Wer nur
die Hauptdatei ersetzt, bekommt das hier — gemessen, nicht vermutet:

    Hauptdatei getauscht, -wal liegengelassen
      gelesen:   [('@leer_bestand',)]        <- die ALTEN Daten
      integrity: ok

SQLite spielt das alte WAL auf die neue Datei und liefert den alten Stand
zurueck, **mit sauberem integrity_check**. Die Wiederherstellung waere
lautlos verschwunden, und der Betreiber haette keinen einzigen Hinweis:
kein Fehler, keine Warnung, eine gesunde Datenbank mit falschem Inhalt.
Das ist die gefaehrlichste Form eines Fehlers, die dieses Projekt kennt.

Deshalb legt `einsetzen()` **alle drei** Dateien zur Seite. Mit -wal und
-shm weggeraeumt liest dieselbe Probe die Sicherung:

      gelesen: ['@aus_sicherung_0', '@aus_sicherung_1', '@aus_sicherung_2']

════════════════════════════════════════════════════════════════════════
UND DIE ZWEITE, DIE MAN NICHT WEGPROGRAMMIEREN KANN
════════════════════════════════════════════════════════════════════════
Der laufende Bot haelt die alte Datei am **inode** fest. Nach dem Tausch
liest und schreibt er weiter in die weggeraeumte Datei — gemessen: eine
danach eingefuegte Zeile ist nach dem Neustart weg. Das ist keine Schwaeche
dieses Moduls, sondern wie Unix funktioniert; es bedeutet nur, dass der
Neustart SOFORT folgen muss. Das Modul sagt es, statt es zu verschweigen.

Bot-frei und ohne Flask: hier stehen nur Dateioperationen und SQLite.
"""
from __future__ import annotations

import logging
import os
import shutil
import sqlite3
import tarfile
import tempfile
from datetime import datetime, timezone
from urllib.request import pathname2url

log = logging.getLogger("TikTokBot")

# Vokabular, das nur ein `.iterdump()`-Dump hat. `CREATE TABLE` allein taugt
# NICHT — es steht auch in jeder SQLite-Datei, weil das Schema woertlich in
# sqlite_master liegt (W94).
DUMP_MARKEN = ("BEGIN TRANSACTION", "CREATE TABLE", "INSERT INTO")

# Die Beiwerk-Dateien des WAL-Modus. Sie MUESSEN beim Tausch mit, sonst
# spielt SQLite das alte WAL auf die neue Datenbank — siehe Modulkopf.
BEIWERK = ("-wal", "-shm", "-journal")

# Die ersten 16 Bytes jeder SQLite-Datei (https://sqlite.org/fileformat.html).
SQLITE_KOPF = b"SQLite format 3\x00"


def archive(verzeichnis: str):
    """Welche Systemarchive liegen da? -> Liste, juengstes zuerst.

    Jeder Eintrag: {name, groesse, geaendert}. Bewusst ohne Blick INS
    Archiv — das Auspacken kostet Sekunden, und diese Liste laedt das Deck
    bei jedem Aufruf.
    """
    aus = []
    if not verzeichnis or not os.path.isdir(verzeichnis):
        return aus
    for name in os.listdir(verzeichnis):
        if not (name.startswith("nightcrawler_sys_") and name.endswith(".tar.gz")):
            continue
        pfad = os.path.join(verzeichnis, name)
        try:
            st = os.stat(pfad)
        except OSError as e:
            # Nicht still: was hier durchfaellt, FEHLT dem Betreiber in der
            # Auswahlliste — und er sucht dann nach einer Sicherung, die es
            # gibt. Das ist keine Aufraeumstelle, sondern eine Blindstelle.
            log.warning("Sicherungsliste: %s uebersprungen (%s)", pfad, e)
            continue
        aus.append({"name": name, "groesse": st.st_size,
                    "geaendert": datetime.fromtimestamp(
                        st.st_mtime, timezone.utc).isoformat()})
    return sorted(aus, key=lambda e: e["name"], reverse=True)


def dump_aus_archiv(pfad: str, ziel_verz: str):
    """Holt db/tiktok_bot_*.sql aus einem Archiv. -> (pfad_oder_None, grund)

    Mit Grund statt nacktem None: "Im Archiv liegt kein Dump" und "der
    Eintrag liess sich nicht lesen" schicken den Betreiber an voellig
    verschiedene Stellen, und ein blankes None macht beide gleich.

    Positiv ausgewaehlt, nicht negativ gefiltert: daneben liegt
    `db/brain_<stempel>.sql`, und ein Filter "alles ausser brain" waere nur
    durch Zufall richtig — sortiert steht `brain` vor `tiktok_bot` (W95).
    """
    with tarfile.open(pfad, "r:gz") as tar:
        kandidaten = [m for m in tar.getmembers()
                      if m.isfile() and m.name.startswith("db/")
                      and m.name.endswith(".sql")
                      and os.path.basename(m.name).startswith("tiktok_bot_")]
        if not kandidaten:
            return None, ("Im Archiv liegt kein db/tiktok_bot_*.sql. Nachsehen, "
                          "was drin ist: tar -tzf %s | head" % os.path.basename(pfad))
        m = sorted(kandidaten, key=lambda x: x.name)[-1]
        quelle = tar.extractfile(m)
        if quelle is None:
            # Nicht erreichbar, solange die Auswahl oben auf isfile() besteht:
            # extractfile liefert nur bei nicht-regulaeren Eintraegen None, und
            # die sind schon gefiltert. Die Mutationsprobe hat das bestaetigt.
            # Der Zweig bleibt als Riegel fuer den Tag, an dem jemand isfile()
            # lockert — als Behauptung "das faengt etwas ab" steht er hier
            # aber ausdruecklich NICHT.
            return None, ("%s laesst sich aus dem Archiv nicht lesen — der "
                          "Eintrag ist kein regulaerer Dateiinhalt." % m.name)
        # Einzeln und mit flachem Namen: ein Archiv mit "../" im Pfad duerfte
        # sonst ausserhalb des Zielverzeichnisses schreiben.
        ziel = os.path.join(ziel_verz, os.path.basename(m.name))
        with open(ziel, "wb") as f:
            shutil.copyfileobj(quelle, f)
        return ziel, ""


def einspielen(sql_pfad: str, ziel_db: str):
    """Baut aus dem Dump eine NEUE Datenbank. -> (ok, befund, tabellen)"""
    with open(sql_pfad, encoding="utf-8", errors="replace") as f:
        sql = f.read()
    fehlend = [m for m in DUMP_MARKEN if m not in sql]
    if fehlend:
        return False, ("Das sieht nicht nach einem Systemarchiv-Dump aus "
                       "(es fehlt: %s)." % ", ".join(fehlend)), []
    con = sqlite3.connect(ziel_db)
    try:
        con.executescript(sql)
        con.commit()
        # Der Vollstaendigkeit halber, nicht als Sicherung: was hier wirklich
        # traegt, ist executescript(). Eine gerade aus SQL gebaute Datenbank
        # ist strukturell heil (W95).
        befund = con.execute("PRAGMA integrity_check").fetchone()[0]
        if befund != "ok":
            return False, str(befund).splitlines()[0], []
        tabellen = []
        for (name,) in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
            n = con.execute('SELECT count(*) FROM "%s"' % name).fetchone()[0]
            tabellen.append((name, n))
        return True, "ok", tabellen
    except sqlite3.DatabaseError as e:
        log.warning("Wiederherstellung: der Dump liess sich nicht einspielen "
                    "(%s)", e)
        return False, str(e), []
    finally:
        con.close()


def vorbereiten(archiv_pfad: str, ziel_db: str):
    """Archiv -> geprüfte neue Datenbankdatei. -> (ok, befund, tabellen)

    Ruehrt die laufende Datenbank NICHT an. Existiert `ziel_db` schon, wird
    nichts ueberschrieben — das Ziel koennte die laufende Datenbank sein.
    """
    if os.path.exists(ziel_db):
        return False, "%s gibt es schon — es wird nichts ueberschrieben." % (
            os.path.basename(ziel_db)), []
    with tempfile.TemporaryDirectory(prefix="dbrest-") as tmp:
        sql = archiv_pfad
        if archiv_pfad.endswith((".tar.gz", ".tgz")):
            try:
                sql, grund = dump_aus_archiv(archiv_pfad, tmp)
            except (tarfile.TarError, OSError) as e:
                log.warning("Wiederherstellung: %s ist nicht zu lesen (%s)",
                            archiv_pfad, e)
                return False, "Das Archiv ist nicht zu lesen: %s" % e, []
            if not sql:
                log.warning("Wiederherstellung: %s", grund)
                return False, grund, []
        ok, befund, tabellen = einspielen(sql, ziel_db)
    if not ok and os.path.exists(ziel_db):
        # Die halb gebaute Datei ist wertlos und stuende beim naechsten
        # Versuch als "gibt es schon" im Weg.
        try:
            os.remove(ziel_db)
        except OSError:
            pass               # Aufraeumpfad, Fehlschlag folgenlos
    return ok, befund, tabellen


def _zurueck(weggeraeumt):
    """Verschobenes an seinen Platz zurueck. Laut, wenn das misslingt.

    Ein gescheitertes Zurueckdrehen ist der schlimmste Zustand dieses
    Moduls: die laufende Datenbank liegt unter fremdem Namen, die neue ist
    nicht am Platz, und der Bot startet nicht mehr. Das darf auf keinen Fall
    still passieren — dann sucht der Betreiber seine Datenbank und weiss
    nicht einmal, dass sie unter `.vor_wiederherstellung_*` daneben liegt.
    """
    for ziel, quelle in reversed(weggeraeumt):
        try:
            os.rename(ziel, quelle)
        except OSError as e:
            log.error("Wiederherstellung: %s liess sich NICHT zurueck nach %s "
                      "legen (%s). Die Datei liegt jetzt unter dem "
                      "Ausweichnamen — von Hand zurueckbenennen, sonst "
                      "startet der Bot nicht.", ziel, quelle, e)


def pruefen(pfad: str):
    """Ist `pfad` eine heile SQLite-Datenbank? -> (ok, grund)

    v5.11.2-SEC-2: `einsetzen()` pruefte bis hierher nur `isfile`. Die Route
    nahm jeden Namen im Datenbankverzeichnis — `bot.py`, `.env`, eine alte
    `.vor_wiederherstellung_*` — legte die laufende Datenbank samt -wal/-shm
    zur Seite und setzte die fremde Datei ein. Nach dem Neustart: "file is
    not a database", Exitcode 3 (W92), der Bot ist aus. Ein Knopf im Deck
    durfte damit den ganzen Betrieb abschalten.

    Entschieden wird wie in tools/dbkopf.py (W94): der Kopf muss stimmen,
    und `PRAGMA integrity_check` muss woertlich "ok" sagen — nichts sonst.
    "Keine Ausnahme" als Kriterium haette dort eine zu 85 % leere Datenbank
    als Rettung ausgegeben.

    Nur lesend: der Kopf mit "rb", die Datenbank per `mode=ro`. Eine Pruefung,
    die die gepruefte Datei veraendert (ein -journal anlegt, ein WAL
    einspielt), prueft am Ende etwas anderes als das, was eingesetzt wird.
    Die Meldung nennt nur den Dateinamen — sie geht als API-Antwort ans Deck.
    """
    name = os.path.basename(pfad)
    try:
        with open(pfad, "rb") as f:
            kopf = f.read(len(SQLITE_KOPF))
    except OSError as e:
        log.warning("Wiederherstellung: %s nicht lesbar (%s)", pfad, e)
        return False, "%s ist nicht zu lesen (%s)." % (name, type(e).__name__)
    if kopf != SQLITE_KOPF:
        return False, ("%s ist keine SQLite-Datenbank (die ersten Bytes: %s)."
                       % (name, kopf.hex() or "leer"))
    try:
        con = sqlite3.connect("file:%s?mode=ro" % pathname2url(os.path.abspath(pfad)),
                              uri=True)
        try:
            befund = [r[0] for r in con.execute("PRAGMA integrity_check").fetchall()]
        finally:
            con.close()
    except sqlite3.DatabaseError as e:
        log.warning("Wiederherstellung: %s nicht pruefbar (%s)", pfad, e)
        return False, "%s laesst sich nicht pruefen: %s" % (name, e)
    if befund != ["ok"]:
        return False, ("integrity_check fuer %s meldet: %s"
                       % (name, (befund[0] if befund else "nichts"))[:300])
    return True, "ok"


def einsetzen(live_db: str, neue_db: str, stempel: str = None):
    """Die geprüfte Datei an die Stelle der laufenden setzen.
       -> (ok, meldung, weggeraeumt)

    DIE WAL-FALLE: es genuegt NICHT, die Hauptdatei zu ersetzen. Bleibt
    `-wal` liegen, spielt SQLite es auf die neue Datei und liefert den ALTEN
    Stand zurueck — mit sauberem integrity_check, also voellig lautlos.
    Deshalb wandern Hauptdatei UND Beiwerk zur Seite, und zwar bevor die
    neue Datei am Platz liegt.
    """
    if not os.path.isfile(neue_db):
        return False, "%s gibt es nicht." % os.path.basename(neue_db), []
    # SEC-2: VOR dem Wegraeumen pruefen. Danach ist es zu spaet — dann liegt
    # die laufende Datenbank schon unter dem Ausweichnamen.
    heil, grund = pruefen(neue_db)
    if not heil:
        log.error("Wiederherstellung abgelehnt: %s", grund)
        return False, grund + " Es wurde nichts veraendert.", []
    stempel = stempel or datetime.now().strftime("%Y%m%d_%H%M%S")
    # v5.2-W191: freie Verbindungen VOR dem Tausch schliessen. Ihr letztes
    # close() loescht `<pfad>-wal` per Namen — nach dem Tausch die WAL der
    # neuen Datei (nc/dbwrap.py, Vorrat).
    from nc import dbwrap as _dbwrap
    _dbwrap.vorrat_leeren()
    weggeraeumt = []
    for endung in ("",) + BEIWERK:
        quelle = live_db + endung
        if not os.path.exists(quelle):
            continue
        ziel = "%s.vor_wiederherstellung_%s" % (quelle, stempel)
        try:
            os.rename(quelle, ziel)
        except OSError as e:
            # Halb weggeraeumt ist der gefaehrlichste Zustand: zurueckdrehen,
            # was schon verschoben wurde, und mit klarer Meldung abbrechen.
            log.error("Wiederherstellung: %s liess sich nicht zur Seite legen "
                      "(%s) — drehe zurueck.", quelle, e)
            _zurueck(weggeraeumt)
            return False, ("%s liess sich nicht zur Seite legen (%s) — es "
                           "wurde nichts veraendert." % (quelle, e)), []
        weggeraeumt.append((ziel, quelle))
    try:
        shutil.copy2(neue_db, live_db)
    except OSError as e:
        log.error("Wiederherstellung: %s liess sich nicht einsetzen (%s) — "
                  "drehe zurueck.", neue_db, e)
        _zurueck(weggeraeumt)
        return False, ("Die neue Datenbank liess sich nicht einsetzen (%s) — "
                       "der vorige Stand ist zurueckgelegt." % e), []
    return True, ("Eingesetzt. JETZT NEU STARTEN: der laufende Prozess haelt "
                  "die alte Datei am inode fest und schreibt weiter hinein — "
                  "alles, was er bis zum Neustart schreibt, ist danach weg. "
                  "sudo systemctl restart tiktok-bot"), [z for z, _q in weggeraeumt]
