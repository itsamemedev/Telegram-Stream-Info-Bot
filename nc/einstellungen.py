"""nc.einstellungen — Einstellungen in der Datenbank, im Deck einstellbar (bot-frei).

v4.2-W145. Der Betreiber am 05.11.: „Was auch praktisch wäre wenn alle
Einstellungen von der env in der Mariadb Datenbank landen und man alles im
dashboard einstellen kann ohne die lästige env anpassen zu müssen."

WIE ES WIRKT
  Tabelle `einstellungen` (SQLite oder MariaDB, wie der Rest). Beim Start
  liest `in_umgebung_laden()` sie DIREKT nach load_dotenv() und legt jeden
  Wert in os.environ — vor den Modul-Konstanten von bot.py. Damit gilt:

      Deck (Datenbank)  >  .env  >  Vorgabe im Code

  Die .env bleibt der Rueckweg: wer eine Zeile im Deck zuruecksetzt, bekommt
  wieder den Wert aus der Datei. Viele Werte liest der Bot nur beim Start —
  eine Aenderung im Deck wirkt deshalb sicher erst nach einem Neustart; das
  Deck sagt das und bietet den Knopf an. Werte, die zur Laufzeit gelesen
  werden, wirken sofort (os.environ wird mitgesetzt).

WAS DAS DECK NICHT DARF — und warum
  Geschuetzt sind Schluessel, die entscheiden, welcher Code laeuft, welche
  Programme gestartet werden, wer das Deck erreicht oder wo die Datenbank
  liegt. Aus dem Deck heraus waere jeder davon ein Fernsteuer-Knopf auf den
  Server: UPDATE_REPO auf ein fremdes Repo, und die Update-Funktion spielt
  fremden Code ein; FFMPEG_BIN auf ein beliebiges Programm; TRUSTED_PROXIES
  so gesetzt, dass jede Anfrage als Loopback gilt und ohne Anmeldung durch
  kommt (bot._auth_guard). Dieselbe Begruendung wie beim Opt-in fuer
  UPDATE_RESTART_CMD (W104). Diese Schluessel stehen nur in der .env, und
  ein Eintrag in der Tabelle wird beim Laden ignoriert und GEMELDET.

  Geheimnisse (Tokens, Schluessel, Passwoerter, Cookies, Proxy-Adressen mit
  Zugangsdaten) sind nur schreibbar: das Deck erfaehrt, OB ein Wert gesetzt
  ist, nie welcher.

Kein automatischer Umzug aus der .env: `uebernehmen()` ist ein Knopf. Liefe
er still beim Start, wirkte danach jede Aenderung an der .env nicht mehr —
und genau das saehe aus wie ein Fehler.
"""

import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone

from nc import dbwrap as _dbwrap
from nc import envdatei as _envdatei
from nc import sqldialekt as _sqldialekt

log = logging.getLogger("TikTokBot")

TABELLE = "einstellungen"
MAX_LAENGE = 4096

# ── Was geschuetzt ist ──────────────────────────────────────────────────────
_GRUND_DB = "db"
_GRUND_ZUGANG = "zugang"
_GRUND_BEFEHL = "befehl"

SCHUTZ_EXAKT = {
    # Wer das Deck erreicht — aus dem Deck geaendert, sperrt es sich auf oder aus.
    "DASHBOARD_TOKEN": _GRUND_ZUGANG, "DASHBOARD_PIN": _GRUND_ZUGANG,
    "DASHBOARD_PIN_MAX_AGE_S": _GRUND_ZUGANG, "DASHBOARD_OFFEN_ERLAUBEN": _GRUND_ZUGANG,
    "DASHBOARD_PORT": _GRUND_ZUGANG, "DASHBOARD_TLS_CERT": _GRUND_ZUGANG,
    "DASHBOARD_TLS_KEY": _GRUND_ZUGANG, "DASHBOARD_WERKZEUG": _GRUND_ZUGANG,
    "WEB_HOST": _GRUND_ZUGANG, "TRUSTED_PROXIES": _GRUND_ZUGANG,
    # Der Dienstname steht in Neustart-Befehlen, die das Deck anzeigt.
    "SERVICE_NAME": _GRUND_BEFEHL,
}
SCHUTZ_PRAEFIX = (("DB_", _GRUND_DB), ("MARIADB_", _GRUND_DB), ("UPDATE_", _GRUND_BEFEHL))
SCHUTZ_ENDUNG = ("_CMD", "_BIN", "_PATH", "_DIR", "_EXE", "_FILE", "_COMMAND", "_SCRIPT")

# ── Was geheim ist ──────────────────────────────────────────────────────────
# Gemessen wird an NAMENSTEILEN, nicht an Teilzeichenketten. Die erste Fassung
# suchte "_KEY" am Ende und uebersah KICK_STREAM_KEY_BACKUP — einen echten
# Stream-Schluessel; sie suchte "COOKIE" irgendwo und versteckte
# COOKIE_AUTO_FETCH=1, einen Schalter. Der Generator der Vorlage hat dieselbe
# Klasse andersherum: sein "_PIN" trifft COMMUNITY_LIVE_PING_ENABLED.
GEHEIM_TEILE = {"TOKEN", "SECRET", "PASSWORD", "PASSWD", "PASS", "KEY", "APIKEY",
                "PIN", "WEBHOOK", "PRIVATE", "CREDENTIAL", "CREDENTIALS",
                "SIGNATURE", "SID", "SESSIONID"}
# Adressen, die Zugangsdaten tragen koennen (nutzer:pass@host).
GEHEIM_EXAKT = {"RECORD_PROXY", "PROXY_LIST", "REDIS_URL"}

# Seit dem Start im Deck geaendert — fuer den Neustart-Hinweis.
_GEAENDERT = set()
_SPERRE = threading.Lock()
_ZUSTAND = {"env_pfad": None, "beispiel_pfad": None, "start": None}


def _t(s):
    """Markiert Benutzertext fuer tools/i18n_extract.py (MARKIERT). Uebersetzt
    wird in der Route — die Sprache steht erst je Anfrage fest."""
    return s


SCHUTZ_TEXT = {
    _GRUND_DB: _t("Die Datenbank-Verbindung muss feststehen, bevor die Datenbank "
                  "gelesen wird — nur in der .env."),
    _GRUND_ZUGANG: _t("Regelt, wer das Deck erreicht. Aus dem Deck geändert, könnte "
                      "es sich selbst aufsperren oder aussperren — nur in der .env."),
    _GRUND_BEFEHL: _t("Bestimmt, welcher Code eingespielt wird, welche Programme "
                      "laufen oder wo Dateien liegen. Aus dem Deck wäre das ein "
                      "Fernsteuer-Knopf auf den Server — nur in der .env."),
}


def gueltiger_name(name):
    return bool(name) and len(name) <= 128 and name[0].isalpha() and \
        all(c.isupper() or c.isdigit() or c == "_" for c in name)


def schutzgrund(name):
    """None, wenn das Deck den Schluessel setzen darf, sonst der Grund-Schluessel.
    „None" ist hier die Antwort „frei", kein Fehlerpfad."""
    return (SCHUTZ_EXAKT.get(name)
            or next((g for p, g in SCHUTZ_PRAEFIX if name.startswith(p)), None)
            or (_GRUND_BEFEHL if name.endswith(SCHUTZ_ENDUNG) else None))


def geheim(name):
    return name in GEHEIM_EXAKT or bool(GEHEIM_TEILE.intersection(name.split("_")))


# ── Katalog aus .env.example ────────────────────────────────────────────────

def katalog(pfad):
    """[{name, gruppe, vorgabe, beschreibung}] aus der generierten Vorlage.

    .env.example entsteht aus dem Quelltext (tools/gen_env_example.py) und
    traegt jede Variable, die der Bot liest — sie ist damit die vollstaendige
    Liste, ohne eine zweite zu pflegen (W100: zwei Listen laufen auseinander).
    `# NAME=wert` heisst „Vorgabe aktiv", `NAME=` ohne # heisst „bitte setzen"."""
    aus, gruppe, text = [], "", []
    if not pfad or not os.path.isfile(pfad):
        log.warning("Einstellungen: Vorlage %s fehlt — das Deck zeigt nur Werte aus "
                    "Datenbank und .env.", pfad)
        return aus
    with open(pfad, encoding="utf-8") as fh:
        for roh in fh:
            z = roh.rstrip("\n")
            s = z.lstrip("# ").strip()
            if z.startswith("# ──"):
                gruppe = s.strip("─ ").strip()
                text = []
                continue
            kandidat = s.split("=", 1)[0] if "=" in s else ""
            if kandidat and gueltiger_name(kandidat) and "<" not in kandidat:
                aus.append({"name": kandidat, "gruppe": gruppe,
                            "vorgabe": s.split("=", 1)[1] if z.startswith("#") else "",
                            "beschreibung": " ".join(text)})
                text = []
            elif z.startswith("#") and s and not s.startswith("=") and not s.startswith("(") \
                    and gruppe and not gruppe.startswith("MUSTER"):
                text.append(s)
            else:
                text = []
    return aus


# ── Beim Start: Datenbank → os.environ ──────────────────────────────────────

def in_umgebung_laden(env, env_pfad=None, beispiel_pfad=None):
    """Die Werte aus der Tabelle in `env` legen — direkt nach load_dotenv().

    Mit eigener, kurzer Verbindung: dbwrap ist zu diesem Zeitpunkt noch nicht
    konfiguriert (das geschieht mit Werten, die erst danach gelesen werden).
    Rueckgabe fuer die Startzeile: {"geladen", "ueberstimmt", "ignoriert",
    "fehler", "quelle"}. Ein Fehler ist NICHT fatal — es gilt dann die .env —,
    wird aber gemeldet: still auf die .env zurueckzufallen hiesse, dass eine im
    Deck gesetzte Einstellung ohne Hinweis nicht wirkt."""
    _ZUSTAND.update(env_pfad=env_pfad, beispiel_pfad=beispiel_pfad)
    aus = {"geladen": 0, "ueberstimmt": [], "ignoriert": [], "fehler": None, "quelle": ""}
    try:
        zeilen, aus["quelle"] = _start_lesen(env)
    except Exception as e:
        aus["fehler"] = "%s: %s" % (type(e).__name__, e)
        log.error("Einstellungen aus der Datenbank NICHT geladen (%s) — es gilt die .env. "
                  "Im Deck gesetzte Werte wirken bis zum naechsten erfolgreichen Start nicht.",
                  aus["fehler"])
        _ZUSTAND["start"] = aus
        return aus
    for name, wert in zeilen:
        if not gueltiger_name(name) or schutzgrund(name):
            aus["ignoriert"].append(name)
            continue
        if env.get(name) != wert:
            aus["ueberstimmt"].append(name)
        env[name] = wert
        aus["geladen"] += 1
    if aus["ignoriert"]:
        # Ein geschuetzter Schluessel in der Tabelle ist kein Zufall: jemand
        # hat ihn am Deck vorbei eingetragen. Laut, mit Namen.
        log.error("Einstellungen: %d geschuetzte Schluessel in der Datenbank ignoriert "
                  "(%s) — sie gelten nur aus der .env.", len(aus["ignoriert"]),
                  ", ".join(sorted(aus["ignoriert"])[:10]))
    _ZUSTAND["start"] = aus
    return aus


def _start_lesen(env):
    """[(name, wert)] aus der Tabelle — oder [] ohne Datei/Tabelle (erster Start)."""
    if (env.get("DB_BACKEND") or "sqlite").strip().lower() == "mariadb":
        import pymysql                      # optional — nur mit MariaDB
        con = pymysql.connect(
            host=env.get("MARIADB_HOST") or "127.0.0.1",
            port=int(env.get("MARIADB_PORT") or 3306),
            user=env.get("MARIADB_USER") or "nightcrawler",
            password=env.get("MARIADB_PASSWORD") or "",
            database=env.get("MARIADB_DB") or "nightcrawler",
            connect_timeout=5, charset="utf8mb4")
        try:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM information_schema.TABLES "
                        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s", (TABELLE,))
            if not cur.fetchone()[0]:
                return [], "mariadb (Tabelle noch nicht angelegt)"
            cur.execute("SELECT schluessel, wert FROM %s" % TABELLE)
            return [(r[0], r[1] or "") for r in cur.fetchall()], "mariadb"
        finally:
            con.close()
    pfad = env.get("DB_PATH") or "tiktok_bot.db"
    if not os.path.isfile(pfad):
        return [], "sqlite (noch keine Datei)"
    # Nur lesend: der Start darf hier nichts anlegen — eine fehlende Datei
    # entscheidet init_db, nicht dieser Leser (W92).
    con = sqlite3.connect("file:%s?mode=ro" % pfad, uri=True, timeout=5)
    try:
        if not con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                           (TABELLE,)).fetchone():
            return [], "sqlite (Tabelle noch nicht angelegt)"
        return [(r[0], r[1] or "") for r in
                con.execute("SELECT schluessel, wert FROM %s" % TABELLE)], "sqlite"
    finally:
        con.close()


def startbericht():
    return _ZUSTAND["start"]


# ── Zur Laufzeit: lesen, setzen, zuruecksetzen, uebernehmen ─────────────────

def db_werte():
    """{name: {"wert", "geaendert_um", "geaendert_von"}} aus der Tabelle."""
    with _dbwrap.db_conn() as conn:
        rows = conn.execute("SELECT schluessel, wert, geaendert_um, geaendert_von "
                            "FROM einstellungen").fetchall()
    return {r["schluessel"]: {"wert": r["wert"] or "", "geaendert_um": r["geaendert_um"],
                              "geaendert_von": r["geaendert_von"]} for r in rows}


class Abgelehnt(ValueError):
    """Eine Aenderung, die nicht angenommen wird — `grund` ist die Antwort.

    Ein eigenes Attribut statt str(e): nach aussen geht nur, was dieses Modul
    selbst als Grund formuliert hat (W30 — kein roher Ausnahmetext ins Deck)."""

    def __init__(self, grund):
        super().__init__(grund)
        self.grund = grund


def pruefen(name, wert):
    """Wirft Abgelehnt mit Grund; sonst None."""
    if not gueltiger_name(name):
        raise Abgelehnt(_t("Kein gültiger Name — nur Großbuchstaben, Ziffern und _."))
    if schutzgrund(name):
        raise Abgelehnt(SCHUTZ_TEXT[schutzgrund(name)])
    if not isinstance(wert, str):
        raise Abgelehnt(_t("Der Wert muss Text sein."))
    if "\n" in wert or "\r" in wert or "\0" in wert:
        raise Abgelehnt(_t("Der Wert darf keinen Zeilenumbruch enthalten."))
    if len(wert) > MAX_LAENGE:
        raise Abgelehnt(_t("Der Wert ist zu lang (höchstens 4096 Zeichen)."))


def setzen(name, wert, von="deck", env=None):
    """In die Tabelle und in die laufende Umgebung. Wirft Abgelehnt."""
    pruefen(name, wert)
    env = os.environ if env is None else env
    jetzt = datetime.now(timezone.utc).isoformat()
    sql = ("INSERT INTO einstellungen (schluessel, wert, geaendert_um, geaendert_von) "
           "VALUES (?,?,?,?) " + _sqldialekt.bei_konflikt(
               _dbwrap.DB_BACKEND, "schluessel",
               ["wert=excluded.wert", "geaendert_um=excluded.geaendert_um",
                "geaendert_von=excluded.geaendert_von"]))
    with _SPERRE:
        with _dbwrap.db_conn() as conn:
            conn.execute(sql, (name, wert, jetzt, von))
        env[name] = wert
        _GEAENDERT.add(name)
    # Name ja, Wert nur, wenn er nicht geheim ist — das Log liest jeder, der
    # an den Server kommt.
    log.info("Einstellung %s im Deck gesetzt%s (von %s)", name,
             "" if geheim(name) else " auf %r" % wert, von)


def zuruecksetzen(name, env=None):
    """Zeile loeschen; die Umgebung bekommt den Wert aus der .env (oder keinen)."""
    if not gueltiger_name(name) or schutzgrund(name):
        raise Abgelehnt(_t("Diesen Schlüssel verwaltet das Deck nicht."))
    env = os.environ if env is None else env
    datei = _envdatei.lesen(_ZUSTAND["env_pfad"]) if _ZUSTAND["env_pfad"] else {}
    with _SPERRE:
        with _dbwrap.db_conn() as conn:
            conn.execute("DELETE FROM einstellungen WHERE schluessel=?", (name,))
        if name in datei:
            env[name] = datei[name]
        else:
            env.pop(name, None)
        _GEAENDERT.add(name)
    log.info("Einstellung %s im Deck zurueckgesetzt — es gilt wieder %s", name,
             ".env" if name in datei else "die Vorgabe")


def uebernehmen(von="deck"):
    """Alle Werte der .env, die das Deck verwalten darf, einmal in die Tabelle.

    Ueberschreibt nichts, was schon in der Tabelle steht, und laesst leere
    Werte aus (dort gilt die Vorgabe — ein leerer Eintrag in der Tabelle
    wuerde sie still ueberstimmen). -> {"uebernommen", "vorhanden", "geschuetzt"}"""
    datei = _envdatei.lesen(_ZUSTAND["env_pfad"]) if _ZUSTAND["env_pfad"] else {}
    vorhanden = set(db_werte())
    aus = {"uebernommen": 0, "vorhanden": 0, "geschuetzt": 0}
    for name, wert in sorted(datei.items()):
        if not gueltiger_name(name) or schutzgrund(name):
            aus["geschuetzt"] += 1
        elif name in vorhanden:
            aus["vorhanden"] += 1
        elif wert != "":
            try:
                pruefen(name, wert)
            except Abgelehnt as e:
                log.warning("Einstellung %s nicht uebernommen: %s", name, e)
                continue
            setzen(name, wert, von)
            aus["uebernommen"] += 1
    log.info("Einstellungen aus der .env uebernommen: %(uebernommen)d neu, "
             "%(vorhanden)d schon im Deck, %(geschuetzt)d geschuetzt (bleiben in der .env)", aus)
    return aus


def uebersicht(env=None):
    """Alles fuer das Deck — ohne einen einzigen geheimen Wert.

    quelle: "datenbank" (im Deck gesetzt), "env" (aus der .env), "vorgabe"."""
    env = os.environ if env is None else env
    kat = katalog(_ZUSTAND["beispiel_pfad"])
    db = db_werte()
    datei = _envdatei.lesen(_ZUSTAND["env_pfad"]) if _ZUSTAND["env_pfad"] else {}
    bekannt = {k["name"] for k in kat}
    # Was in DB oder .env steht, aber in keiner Vorlage: trotzdem zeigen.
    for name in sorted((set(db) | set(datei)) - bekannt):
        if gueltiger_name(name):
            kat.append({"name": name, "gruppe": "SONSTIGE", "vorgabe": "", "beschreibung": ""})
    eintraege = []
    for k in kat:
        n = k["name"]
        grund = schutzgrund(n)
        quelle = "datenbank" if n in db and not grund else ("env" if n in datei else "vorgabe")
        e = {"name": n, "gruppe": k["gruppe"], "beschreibung": k["beschreibung"],
             "vorgabe": "" if geheim(n) else k["vorgabe"], "quelle": quelle,
             "geheim": geheim(n), "gesetzt": bool(env.get(n)),
             "geschuetzt": bool(grund), "schutz": SCHUTZ_TEXT[grund] if grund else "",
             "geaendert_um": db.get(n, {}).get("geaendert_um") if quelle == "datenbank" else None}
        if not geheim(n):
            e["wert"] = env.get(n, "")
        eintraege.append(e)
    zahl = {q: sum(1 for e in eintraege if e["quelle"] == q) for q in ("datenbank", "env", "vorgabe")}
    return {"eintraege": eintraege, "zahl": zahl,
            "geschuetzt": sum(1 for e in eintraege if e["geschuetzt"]),
            "neustart": sorted(_GEAENDERT), "start": _ZUSTAND["start"],
            "backend": _dbwrap.DB_BACKEND}
