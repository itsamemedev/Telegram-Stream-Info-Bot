"""nc.chatnachtrag — der Chat einer beim Stopp gesicherten Aufnahme (rein, bot-frei).

v4.2-W163. Bis hierher legte `_aufnahme_beim_stopp_sichern` den Chat als
`<aufnahme>.ass` NEBEN die Datei (Review #203). Das loeste das Problem nicht,
es verschob es auf die Platte:

* Telegram, das Deck und jeder Player ausser VLC/mpv sehen die Beilage nie —
  die Aufnahme war fuer den Betreiber genauso ohne Chat wie vorher.
* Kein Loeschweg kannte sie. Retention, Papierkorb, Dubletten und Archiv
  fassen die Videodatei an (sieben Stellen), die Beilage blieb liegen — eine
  Halde, die mit jedem Neustart waechst.
* Das Archiv kopierte nur die Videodatei; dort war der Chat dann ganz weg.

Hier jetzt der andere Weg: beim Stopp wird der Chat in die DATENBANK
vorgemerkt (ein INSERT, keine Wartezeit fuer das Herunterfahren), und beim
naechsten Start arbeitet der Bot ihn genauso in die Datei ein wie bei jeder
normal beendeten Aufnahme — eingebrannt oder als Untertitelspur, ueber
dieselbe Funktion. Am Ende sieht die Aufnahme aus wie jede andere, und es
liegt nichts neben ihr.

Die Tabelle steht im Schema (nc.schema.modultabellen), damit der Umzug nach
MariaDB sie kennt — der Fehler aus W150 (Tabellen, die erst beim ersten
Gebrauch entstehen) soll sich nicht wiederholen.
"""

import json
import os
from datetime import datetime, timezone

TABELLE = "aufnahme_chat_nachtrag"
# Nach so vielen gescheiterten Starts gibt der Nachtrag auf — eine Datei, die
# ffmpeg dreimal nicht verarbeiten konnte, wird es beim vierten Mal auch nicht,
# und ein Eintrag, der ewig bleibt, kostet bei jedem Start einen ffmpeg-Lauf.
MAX_VERSUCHE = 3


def ensure_schema(conn, backend="sqlite"):
    """Tabelle anlegen. Idempotent, in beiden Dialekten."""
    if backend == "mariadb":
        from nc import schema as _schema
        conn.execute(
            "CREATE TABLE IF NOT EXISTS " + TABELLE + " ("
            " id BIGINT AUTO_INCREMENT PRIMARY KEY,"
            " pfad TEXT NOT NULL,"
            " nutzer VARCHAR(191) NOT NULL,"
            " chat MEDIUMTEXT NOT NULL,"
            " erstellt VARCHAR(64) NOT NULL,"
            " versuche INTEGER NOT NULL DEFAULT 0,"
            " groesse BIGINT,"
            " mtime_ns BIGINT"
            ")" + _schema.parameter("mariadb")["tbl_opts"])
    else:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS " + TABELLE + " ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " pfad TEXT NOT NULL,"
            " nutzer TEXT NOT NULL,"
            " chat TEXT NOT NULL,"
            " erstellt TEXT NOT NULL,"
            " versuche INTEGER NOT NULL DEFAULT 0,"
            " groesse INTEGER,"
            " mtime_ns INTEGER)")


def stempel(pfad):
    """(Groesse, mtime_ns) der Datei — woran der Nachtrag erkennt, dass sie
    noch die ist, die beim Stopp vorlag."""
    st = os.stat(pfad)
    return int(st.st_size), int(st.st_mtime_ns)


def vormerken(conn, pfad, nutzer, chat) -> None:
    """Den Chat einer Aufnahme fuer den naechsten Start ablegen — mit dem
    Stempel der Datei, wie sie JETZT ist."""
    roh = json.dumps([[round(float(t), 3), str(w), str(x)] for t, w, x in chat],
                     ensure_ascii=False, separators=(",", ":"))
    groesse, mtime_ns = stempel(pfad)
    conn.execute("INSERT INTO " + TABELLE + " (pfad, nutzer, chat, erstellt, versuche, "
                 "groesse, mtime_ns) VALUES (?,?,?,?,0,?,?)",
                 (pfad, nutzer, roh, datetime.now(timezone.utc).isoformat(),
                  groesse, mtime_ns))


def unveraendert(eintrag) -> bool:
    """Ist die Datei noch die vom Stopp? (Review #207)

    Das Einarbeiten ERSETZT die Datei und traegt erst danach in der Datenbank
    ab. Scheitert dieser zweite Schritt (gesperrte Datenbank, Absturz,
    Neustart mittendrin), steht der Eintrag beim naechsten Start noch da —
    und ohne diese Pruefung braennte der Nachtrag den Chat ein zweites Mal in
    eine Datei, die ihn schon traegt. Eine Datei, die sich seit dem Stopp
    veraendert hat, ist bearbeitet (von uns oder von Hand) — sie wird nicht
    noch einmal angefasst."""
    if eintrag.get("groesse") is None or eintrag.get("mtime_ns") is None:
        return True                 # ohne Stempel: nichts zu vergleichen
    return stempel(eintrag["pfad"]) == (int(eintrag["groesse"]), int(eintrag["mtime_ns"]))


def lesen(roh) -> list:
    """JSON aus der Tabelle -> [(t, wer, text)]. Wirft ValueError, wenn der
    Inhalt nicht dieses Format hat — der Aufrufer verwirft den Eintrag dann
    laut, statt ihn bei jedem Start erneut zu versuchen."""
    daten = json.loads(roh or "")
    if not isinstance(daten, list):
        raise ValueError("kein JSON-Array")
    return [(float(e[0]), str(e[1]), str(e[2])) for e in daten]


def offene(conn) -> list:
    """[{id, pfad, nutzer, chat_roh, versuche}] in Entstehungsreihenfolge."""
    rows = conn.execute("SELECT id, pfad, nutzer, chat, versuche, groesse, mtime_ns FROM " +
                        TABELLE + " ORDER BY id").fetchall()
    return [{"id": r["id"], "pfad": r["pfad"], "nutzer": r["nutzer"],
             "chat_roh": r["chat"], "versuche": int(r["versuche"] or 0),
             "groesse": r["groesse"], "mtime_ns": r["mtime_ns"]} for r in rows]


def erledigt(conn, eintrag_id) -> None:
    conn.execute("DELETE FROM " + TABELLE + " WHERE id=?", (eintrag_id,))


def eingearbeitet(conn, eintrag_id, pfad, groesse) -> None:
    """Der Chat steckt in der Datei. Die Groesse im Deck folgt ihr — sonst
    stimmt die Speicherprognose (nc/storage.py) nicht mehr."""
    conn.execute("UPDATE recordings SET file_size=? WHERE filepath=?", (int(groesse), pfad))
    erledigt(conn, eintrag_id)


def fehlversuch(conn, eintrag) -> bool:
    """Einen gescheiterten Versuch zaehlen. -> True, wenn damit aufgegeben ist
    (der Eintrag ist dann geloescht)."""
    if eintrag["versuche"] + 1 >= MAX_VERSUCHE:
        erledigt(conn, eintrag["id"])
        return True
    conn.execute("UPDATE " + TABELLE + " SET versuche=versuche+1 WHERE id=?",
                 (eintrag["id"],))
    return False
