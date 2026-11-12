"""nc.routes.settings — die Routen unter /api/config,/api/schedule,/api/db,/api/cookies als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
import json
import os
from flask import Blueprint, Response, jsonify, request

from nc import fehlertext as _nc_fehlertext

from nc import i18n as _nc_i18n
from nc.dbwrap import db_conn
from typing import Optional
import time as _time_mod
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set
from nc import cookiebezug as _nc_cookiebezug
from nc import cookieholen as _nc_cookieholen
from nc.dbexport import db_export_sql as _dbx_export, db_import_sql as _dbx_import, export_summary as _dbx_summary
from nc import dbrestore as _nc_dbrest   # v4.2-W96: Sicherung im Deck einsetzen
from nc import sicherpfad as _nc_sicherpfad

from nc import ctx as _ctx

bp = Blueprint("settings", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def cookies_days_old() -> Optional[float]:
    """Wie viele Tage ist die cookies.txt alt? None wenn nicht da."""
    if not os.path.exists(_c().cfg["COOKIE_FILE"]): return None
    try:
        return (_time_mod.time() - os.path.getmtime(_c().cfg["COOKIE_FILE"])) / 86400
    except Exception:
        return None


@bp.route("/api/cookies/health")
def api_cookies_health():
    """Liefert detaillierten Cookie-Status: welche kritischen fehlen, was
       läuft bald ab, wie alt ist die cookies.txt."""
    return jsonify(_c().get_cookie_health())


@bp.route("/api/cookies/update", methods=["POST"])
def api_cookies_update():
    """B63: Cookies aktualisieren ohne SSH/Datei-Editing.

       Body: {"cookies": "<text>"} — Netscape (cookies.txt), JSON-Array
       (Cookie-Editor / EditThisCookie) oder seit v5.4-W195 ein Header-String
       (`sessionid=…; ttwid=…`, Cookie-Editor „Header String", DevTools). Das
       Deck schickt hierher auch den Inhalt einer hochgeladenen Datei — der
       Browser liest sie, der Server bekommt nur Text.

       Ablauf und Riegel stehen in nc.cookieholen.uebernehmen(), denselben,
       den das Telegram-Dokument nimmt: konvertieren, Doppelte bereinigen,
       Login-Cookie verlangen, .tmp mit 0600 schreiben und LADEN, Backup,
       atomar tauschen — unter DATEI_SPERRE. Die alte Datei bleibt bei jedem
       Fehlschlag unangetastet.
    """
    payload = request.get_json(silent=True) or {}
    datei = _c().cfg["COOKIE_FILE"]
    erg = _nc_cookieholen.uebernehmen(payload.get("cookies") or "", datei)
    if not erg["ok"]:
        art = erg["art"]
        if art == "leer":
            fehler = _t("Keine Cookie-Daten übergeben.")
        elif art == "zu_gross":
            fehler = _t("Eingabe zu groß (>2 MB).")
        elif art == "json":
            fehler = "JSON nicht lesbar: " + erg["detail"]
        elif art == "format":
            fehler = "Cookies nicht verarbeitbar: " + erg["detail"]
        elif art == "keine":
            fehler = _t("Keine gültigen Cookies erkannt. Erwartet wird das Netscape-Format "
                        "(cookies.txt), ein JSON-Array oder ein Header-String "
                        "(name=wert; name2=wert2).")
        elif art == "kein_login":
            fehler = _t("Kein Auth-Cookie (sessionid_ss/sessionid) gefunden. Bist du im "
                        "Browser bei TikTok eingeloggt? Update abgebrochen — die alten "
                        "Cookies bleiben erhalten.")
        else:
            fehler = "Schreiben fehlgeschlagen: " + erg["detail"]
        return jsonify(ok=False, error=fehler, found=erg.get("gefunden") or []), \
            (500 if art == "schreiben" else 400)

    # Cache invalidieren → _load_cookies_dict() lädt beim nächsten Zugriff neu
    _c().cfg["_COOKIES_CACHE"].pop("v", None)
    health = _c().get_cookie_health()
    log.info("Cookies via Dashboard aktualisiert: %d Cookies geschrieben, status=%s, "
             "critical_present=%s, backup=%s", erg["anzahl"], health.get("status"),
             health.get("critical_present"), "ja" if erg["backup"] else "nein")
    return jsonify(ok=True, parsed=erg["anzahl"], backed_up=erg["backup"],
                   deduped=erg["doppelt"], auth_cookie=erg["auth_cookie"], health=health)


@bp.route("/api/cookies/fetch", methods=["POST"])
def api_cookies_fetch():
    """v4.2-W10: Cookies selbst beziehen, ohne Browser-Extension und ohne SSH.

       Body: {"source": "gast"|"browser", "browser": "chrome"}

       'gast'    — ein HTTPS-Aufruf auf tiktok.com holt die rotierenden
                   Anti-Bot-Tokens (ttwid, msToken, tt_chain_token, …). Kein
                   Login noetig, und Auth-Cookies werden dabei NICHT angefasst.
       'browser' — liest das TikTok-Profil eines lokal installierten Browsers.
                   Nur so kommt ein echter sessionid herein. Auf dem Server
                   (kein Browser) scheitert das mit klarer Meldung.

       Warum das nicht einfach /api/cookies/update mitmacht: update erwartet
       einen Text vom Menschen und verlangt ein Auth-Cookie. Der Gast-Bezug
       hat keins und darf trotzdem schreiben — zwei verschiedene Vertraege in
       einer Route waeren die naechste stille Fehlbedienung."""
    payload = request.get_json(silent=True) or {}
    quelle = (payload.get("source") or "gast").strip().lower()
    browser = (payload.get("browser") or "").strip().lower() or None
    if quelle not in ("gast", "guest", "browser"):
        return jsonify(ok=False, error=_t("Unbekannte Quelle.")), 400
    if quelle == "guest":
        quelle = "gast"

    # v4.2-W107: durch den Buchhalter, nicht an ihm vorbei. Vorher rief
    # die Route nc/cookieholen direkt — nach einem erfolgreichen Klick stand
    # im Deck weiter „Auto-Bezug: noch nie gelaufen". holen() leert auch den
    # Cookie-Cache des Recorders.
    bericht = _nc_cookiebezug.holen(quelle, browser, anlass="deck")
    if bericht.get("ok"):
        bericht["health"] = _c().get_cookie_health()
        log.info("Cookies via Deck bezogen (%s): %d neu, %d erneuert",
                 quelle, len(bericht.get("added") or []),
                 len(bericht.get("replaced") or []))
        return jsonify(bericht)
    # Hier wird NICHT nachgesaeubert: der Wortlaut ist schon durch
    # nc.fehlertext.nach_aussen gegangen, dort wo die Ausnahme wirklich
    # anfaellt (nc/cookieholen.aktualisiere). Eine zweite Saeuberung an der
    # Senke waere die zweite Wahrheit ueber dieselbe Meldung.
    # v5.1-W187: „kein Desktop" ist eine Lage dieser Maschine, kein
    # Ausfall eines Gegenuebers — 409 statt 502, damit _log_5xx sie nicht
    # als Serverfehler ins Fehlerlog schreibt (11.11.: KeyError
    # 'DBUS_SESSION_BUS_ADDRESS' als HTTP 502).
    if bericht.get("grund") == "kein_desktop":
        return jsonify(bericht), 409
    return jsonify(bericht), 502


@bp.route("/api/cookies/age")
def api_cookies_age():
    days = cookies_days_old()
    return jsonify(ok=True, days_old=round(days, 1) if days is not None else None,
                   exists=days is not None,
                   warn=(days is not None and days > 7))


@bp.route("/api/db/summary")
def api_db_summary():
    """Tabellen + Zeilenzahlen fuer das Wartungs-Panel."""
    try:
        s = _dbx_summary()
        return jsonify(ok=True, backend=_c().cfg["DB_BACKEND"], tables=s,
                       total=sum(v for v in s.values() if v > 0),
                       other=("mariadb" if _c().cfg["DB_BACKEND"] == "sqlite" else "sqlite"))
    except Exception as e:
        log.warning("api_db_summary: %s", e)
        return jsonify(ok=False, error=_fehler_text(e, "api_db_summary")), 500


@bp.route("/api/db/export")
def api_db_export():
    """Streamt den SQL-Export als Download.

    ?dialect=mariadb|sqlite — fuer welches ZIEL escaped wird. Default ist das
    jeweils ANDERE Backend, weil genau das der Umzugs-Fall ist.
    """
    dialect = (request.args.get("dialect") or
               ("mariadb" if _c().cfg["DB_BACKEND"] == "sqlite" else "sqlite")).strip().lower()
    if dialect not in ("sqlite", "mariadb"):
        return jsonify(ok=False, error=_t("dialect muss sqlite oder mariadb sein")), 400
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    fname = f"nightcrawler-{_c().cfg['DB_BACKEND']}-to-{dialect}-{ts}.sql"

    def _gen():
        try:
            yield from _dbx_export(dialect=dialect)
        except Exception as e:                     # im Stream ist kein 500 mehr moeglich
            log.error("DB-Export abgebrochen: %s", e)
            yield f"\n-- ABBRUCH: {e}\n-- Diese Datei ist UNVOLLSTAENDIG, nicht einspielen!\n"

    log.info("DB-Export gestartet: %s -> %s", _c().cfg["DB_BACKEND"], dialect)
    return Response(_gen(), mimetype="application/sql",
                    headers={"Content-Disposition": f'attachment; filename="{fname}"',
                             "X-Accel-Buffering": "no"})


@bp.route("/api/db/import", methods=["POST"])
def api_db_import():
    """Spielt einen Export ein. Erwartet die .sql-Datei als multipart 'file'
       oder den Text im Body. ?dry_run=1 prueft nur."""
    dry = request.args.get("dry_run") == "1"
    f = request.files.get("file")
    if f is not None:
        raw = f.read()
    else:
        raw = request.get_data() or b""
    if not raw:
        return jsonify(ok=False, error=_t("keine Datei/kein Inhalt")), 400
    if len(raw) > _c().cfg["DB_IMPORT_MAX_MB"] * 1024 * 1024:
        return jsonify(ok=False, error=f"Datei > {_c().cfg['DB_IMPORT_MAX_MB']} MB — "
                                       "DB_IMPORT_MAX_MB anheben oder per CLI einspielen"), 413
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return jsonify(ok=False, error=_t("Datei ist kein UTF-8 — kein gueltiger Export")), 400
    try:
        rep = _dbx_import(text, expect_dialect=_c().cfg["DB_BACKEND"], dry_run=dry)
        # rep enthaelt "ok" bereits — jsonify(ok=…, **rep) waere ein doppeltes
        # Keyword-Argument und wirft TypeError.
        return jsonify(**rep), (200 if rep.get("ok") else 400)
    except Exception as e:
        log.error("DB-Import fehlgeschlagen: %s", e)
        return jsonify(ok=False, error=_fehler_text(e, "api_db_import")), 500


def _sicherungsverzeichnis():
    """Wo liegen die Systemarchive? Als Funktion gelesen, nie als
       Modul-Konstante — .env wird teils erst nach den ersten Imports
       geladen (CLAUDE.md, W67)."""
    basis = (os.getenv("LOCAL_BACKUP_DIR", "") or "").strip()
    return os.path.join(basis, "system") if basis else ""


@bp.route("/api/db/restore/list")
def api_db_restore_list():
    """v4.2-W96: welche Systemarchive stehen zur Wiederherstellung bereit?"""
    try:
        verz = _sicherungsverzeichnis()
        if not verz:
            return jsonify(ok=False, error=_t(
                "LOCAL_BACKUP_DIR ist nicht gesetzt — es gibt kein lokales "
                "Sicherungsverzeichnis."), archive=[]), 400
        return jsonify(ok=True, verzeichnis=verz,
                       archive=_nc_dbrest.archive(verz))
    except Exception as e:
        # Ausdruecklich auf error: ein misslungener Eingriff an der
        # Datenbank ist das, wonach der Betreiber im Log sucht.
        log.error("api_db_restore_list: %s", e, exc_info=True)
        return jsonify(ok=False, error=_fehler_text(e, "api_db_restore_list")), 500


@bp.route("/api/db/restore/prepare", methods=["POST"])
def api_db_restore_prepare():
    """v4.2-W96: ein Archiv zu einer NEUEN, geprueften Datenbankdatei machen.

    Ruehrt die laufende Datenbank nicht an. Das Ergebnis ist eine Datei
    daneben, samt Zeilen je Tabelle — damit der Betreiber VOR dem Einsetzen
    sieht, ob die Zahlen plausibel sind."""
    data = request.get_json(silent=True) or {}
    name = (data.get("archiv") or "").strip()
    if not name:
        return jsonify(ok=False, error=_t("archiv erforderlich")), 400
    try:
        verz = _sicherungsverzeichnis()
        if not verz:
            return jsonify(ok=False, error=_t("LOCAL_BACKUP_DIR nicht gesetzt")), 400
        # Der Name kommt von aussen: ueber nc.sicherpfad, nicht von Hand.
        archiv = _nc_sicherpfad.sicher_join(verz, name, "archiv.tar.gz")
        if not os.path.isfile(archiv):
            return jsonify(ok=False, error=_t("Archiv nicht gefunden")), 404
        db_pfad = _c().cfg["DB_PATH"]
        stempel = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        ziel = os.path.join(os.path.dirname(os.path.abspath(db_pfad)),
                            "wiederhergestellt_%s.db" % stempel)
        ok_, befund, tabellen = _nc_dbrest.vorbereiten(archiv, ziel)
        if not ok_:
            return jsonify(ok=False, error=befund), 400
        return jsonify(ok=True, datei=os.path.basename(ziel), befund=befund,
                       zeilen=sum(n for _n, n in tabellen),
                       tabellen=[{"name": n, "zeilen": c} for n, c in tabellen],
                       hinweis=_t("Zahlen pruefen, dann einsetzen. Danach ist "
                                  "ein Neustart noetig."))
    except Exception as e:
        # Ausdruecklich auf error: ein misslungener Eingriff an der
        # Datenbank ist das, wonach der Betreiber im Log sucht.
        log.error("api_db_restore_prepare: %s", e, exc_info=True)
        return jsonify(ok=False, error=_fehler_text(e, "api_db_restore_prepare")), 500


@bp.route("/api/db/restore/apply", methods=["POST"])
def api_db_restore_apply():
    """v4.2-W96: die vorbereitete Datei an die Stelle der laufenden setzen.

    confirm=true noetig. Legt Hauptdatei UND -wal/-shm zur Seite: bleibt das
    WAL liegen, spielt SQLite es auf die neue Datei und liefert den ALTEN
    Stand zurueck, mit sauberem integrity_check — die Wiederherstellung
    waere lautlos verschwunden."""
    data = request.get_json(silent=True) or {}
    if not data.get("confirm"):
        return jsonify(ok=False, error=_t("confirm=true erforderlich")), 400
    name = (data.get("datei") or "").strip()
    if not name:
        return jsonify(ok=False, error=_t("datei erforderlich")), 400
    try:
        db_pfad = _c().cfg["DB_PATH"]
        verz = os.path.dirname(os.path.abspath(db_pfad))
        neu = _nc_sicherpfad.sicher_join(verz, name, "wiederhergestellt.db")
        if not os.path.isfile(neu):
            return jsonify(ok=False, error=_t("Datei nicht gefunden")), 404
        if os.path.abspath(neu) == os.path.abspath(db_pfad):
            return jsonify(ok=False, error=_t(
                "Das ist die laufende Datenbank selbst.")), 400
        ok_, meldung, weggeraeumt = _nc_dbrest.einsetzen(db_pfad, neu)
        if not ok_:
            log.error("Wiederherstellung fehlgeschlagen: %s", meldung)
            return jsonify(ok=False, error=meldung), 500
        log.warning("Datenbank aus Sicherung eingesetzt (%s). Neustart noetig; "
                    "der vorige Stand liegt unter %s", name,
                    ", ".join(os.path.basename(w) for w in weggeraeumt))
        return jsonify(ok=True, meldung=meldung,
                       weggeraeumt=[os.path.basename(w) for w in weggeraeumt])
    except Exception as e:
        # Ausdruecklich auf error: ein misslungener Eingriff an der
        # Datenbank ist das, wonach der Betreiber im Log sucht.
        log.error("api_db_restore_apply: %s", e, exc_info=True)
        return jsonify(ok=False, error=_fehler_text(e, "api_db_restore_apply")), 500


@bp.route("/api/config/snapshot")
def api_config_snapshot():
    """Exportiert app_config + learned_params als JSON-Snapshot (Backup)."""
    try:
        with db_conn() as conn:
            cfg = {r["k"]: r["v"] for r in conn.execute("SELECT k, v FROM app_config").fetchall()}
            learned = [dict(r) for r in conn.execute(
                "SELECT k, v, confidence, samples, category FROM learned_params").fetchall()]
        return jsonify(ok=True, generated_at=datetime.now(timezone.utc).isoformat(),
                       app_config=cfg, learned_params=learned,
                       counts={"config": len(cfg), "learned": len(learned)})
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_config_snapshot")), 500


@bp.route("/api/config/restore", methods=["POST"])
def api_config_restore():
    """Stellt app_config aus einem Snapshot wieder her. confirm=true nötig.
       Setzt NUR app_config-Schlüssel (keine learned_params, kein Schema)."""
    data = request.get_json(silent=True) or {}
    if not data.get("confirm"):
        return jsonify(ok=False, error=_t("confirm=true erforderlich")), 400
    cfg = data.get("app_config") or {}
    if not isinstance(cfg, dict):
        return jsonify(ok=False, error=_t("app_config muss ein Objekt sein")), 400
    try:
        restored = 0
        failed = 0
        for k, v in cfg.items():
            try:
                _cfg_set(k, json.loads(v) if isinstance(v, str) else v)
                restored += 1
            except Exception:
                # BUG-FIX: vorher wurde auch nach Fehler restored+=1 gezählt
                # weil der äußere except auf _cfg_set(k,v) fiel und ebenfalls
                # restored+=1 ausführte. Jetzt: getrennter Fehler-Zähler.
                try:
                    _cfg_set(k, v)
                    restored += 1
                except Exception:
                    failed += 1
        return jsonify(ok=True, restored=restored, failed=failed)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_config_restore")), 500


@bp.route("/api/schedule/list")
def api_schedule_list():
    """Listet geplante Aufnahmefenster (in app_config gespeichert)."""
    try:
        sched = _cfg_get("scheduled_recordings", []) or []
        return jsonify(ok=True, count=len(sched), schedules=sched)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_schedule_list")), 500


@bp.route("/api/schedule/add", methods=["POST"])
def api_schedule_add():
    """Fügt ein geplantes Aufnahmefenster hinzu.
       Body: {username, weekday(0-6), hour(0-23), duration_min}"""
    data = request.get_json(silent=True) or {}
    u = (data.get("username") or "").lstrip("@")
    if not u:
        return jsonify(ok=False, error=_t("username erforderlich")), 400
    try:
        # BUG-FIX: int(datetime.now().timestamp()) hat Sekunden-Granularität.
        # Zwei Einträge in derselben Sekunde bekommen die gleiche ID →
        # api_schedule_remove löscht beide. Fix: Mikrosekunden-Timestamp.
        uid = int(datetime.now(timezone.utc).timestamp() * 1_000_000)
        entry = {"id": uid,
                 "username": u, "weekday": int(data.get("weekday", 0)) % 7,
                 "hour": int(data.get("hour", 20)) % 24,
                 "duration_min": int(data.get("duration_min", 60))}
        sched = _cfg_get("scheduled_recordings", []) or []
        sched.append(entry)
        _cfg_set("scheduled_recordings", sched)
        return jsonify(ok=True, added=entry, count=len(sched))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_schedule_add")), 500


@bp.route("/api/schedule/remove", methods=["POST"])
def api_schedule_remove():
    """Entfernt ein geplantes Fenster per id."""
    data = request.get_json(silent=True) or {}
    sid = data.get("id")
    try:
        sched = _cfg_get("scheduled_recordings", []) or []
        new = [s for s in sched if str(s.get("id")) != str(sid)]
        _cfg_set("scheduled_recordings", new)
        return jsonify(ok=True, removed=len(sched) - len(new), count=len(new))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_schedule_remove")), 500
