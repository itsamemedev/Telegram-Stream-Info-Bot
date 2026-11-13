"""nc.cfgstore — app_config lesen und schreiben, backend-agnostisch.

v4.0-W62c brachte den Upsert, v4.0-W111 die Leseseite: get() und set_()
lagen bis dahin als _cfg_get/_cfg_set im Monolithen, obwohl sie exakt zu
diesem Modul gehoeren. Sie sind Vorarbeit fuer das /api/ai-Blueprint —
dort wurden sie sonst zu zwei Eintraegen im Laufzeitkontext, obwohl sie
reiner Datenzugriff sind.

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


# ── v4.0-W111: die Leseseite, aus bot.py geloest ────────────────────────

import json as _json                                          # noqa: E402
from datetime import datetime as _dt, timezone as _tz         # noqa: E402

from nc.dbwrap import db_conn as _db_conn                     # noqa: E402


def get(key, default=None):
    """Liest einen JSON-Wert aus app_config. default bei Fehlen/Fehler."""
    try:
        with _db_conn() as conn:
            row = conn.execute("SELECT v FROM app_config WHERE k=?", (key,)).fetchone()
        if not row or row["v"] is None:
            return default
        try:
            return _json.loads(row["v"])
        except Exception:
            return row["v"]
    except Exception:
        return default


def lesen(key, fehlt=None):
    """Wie get(), aber STRENG: ein Datenbankfehler und ein unlesbarer Wert fliegen durch.

    v5.6-W198. get() antwortet auf beides mit der Vorgabe — fuer eine Anzeige
    richtig, fuer Lesen-Aendern-Schreiben gefaehrlich: wer eine Liste liest,
    einen Eintrag anhaengt und zurueckschreibt, macht aus einer gesperrten
    Datenbank (Alltag bei laufendem Recorder) ein Loeschen aller anderen
    Eintraege. Dieselbe Klasse wie _find_orphans in W91: „ich weiss nicht, was
    in der Datenbank steht" ist nicht „es steht nichts darin".

    `fehlt` gilt NUR, wenn der Schluessel wirklich nicht da ist."""
    with _db_conn() as conn:
        row = conn.execute("SELECT v FROM app_config WHERE k=?", (key,)).fetchone()
    if not row or row["v"] is None:
        return fehlt
    return _json.loads(row["v"])


def set_(key, value):
    """Upsert eines JSON-Werts in app_config (backend-agnostisch ohne UPSERT-SQL).

    Heisst set_ und nicht set, weil set eine eingebaute Funktion ist — ein
    Modul-Attribut mit dem Namen waere zwar erlaubt, liest sich beim Aufruf
    aber wie ein Fehler.
    """
    payload = _json.dumps(value, ensure_ascii=False)
    now = _dt.now(_tz.utc).isoformat()
    with _db_conn() as conn:
        upsert(conn, key, payload, now)
    return value


# ── v5.8-W199: Lesen-Aendern-Schreiben an EINER Stelle ──────────────────

import copy as _copy                                          # noqa: E402
import threading as _threading                                # noqa: E402

# Eine Sperre fuer alle Schluessel: die Aenderungen sind Klicks im Deck,
# selten und kurz. Je Schluessel eine eigene Sperre zu fuehren waere
# Buchhaltung ohne messbaren Gewinn.
_AENDERN = _threading.RLock()


class FalscheForm(ValueError):
    """Der gespeicherte Wert hat nicht die erwartete Form (Liste statt Objekt …).

    Dann wird NICHT geschrieben: wer ihn ueberschriebe, loeschte etwas, das er
    nicht versteht."""


def aendern(key, aenderung, fehlt=None, art=None):
    """Streng lesen, aendern, schreiben — unter Sperre. -> der neue Wert.

    v5.8-W199. W198 hat die Klasse an EINER Stelle behoben (MCP-Server), und
    sieben weitere standen daneben: /api/schedule/add|remove, die
    Konfiguration von Marketing, News, Co-Host, Highlight-Radar und Signalton.
    Jede las mit get(key, []) und schrieb das Ergebnis zurueck. get() liefert
    bei einem Datenbankfehler die Vorgabe — „Zeitplan hinzufuegen" bei
    gesperrter Datenbank (Alltag bei laufendem Recorder) schrieb damit eine
    Liste mit EINEM Eintrag und loeschte alle anderen; „Takt aendern" setzte
    Ziele und Ruhezeiten still auf die Vorgabe zurueck. Und ohne Sperre
    verloren zwei gleichzeitige Klicks einen davon (waitress bedient parallel).

    aenderung(alt) -> neu. `alt` kommt aus lesen(): ein Datenbankfehler oder
    ein unlesbarer Wert fliegt durch, `fehlt` gilt NUR, wenn der Schluessel
    wirklich fehlt (als Kopie — eine Vorgabe-Liste wird nie geteilt). `art`
    prueft die Form. Wirft die Aenderung, wird nichts geschrieben.
    """
    with _AENDERN:
        alt = lesen(key, _copy.deepcopy(fehlt))
        if art is not None and not isinstance(alt, art):
            raise FalscheForm("app_config[%s] ist %s, erwartet %s"
                              % (key, type(alt).__name__,
                                 getattr(art, "__name__", art)))
        neu = aenderung(alt)
        set_(key, neu)
    return neu
