"""nc.routes.settings — die Routen unter /api/config,/api/schedule,/api/db,/api/cookies als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
import json
import os
import shutil
from flask import Blueprint, Response, jsonify, request

from nc import fehlertext as _nc_fehlertext

from nc import i18n as _nc_i18n
from nc.dbwrap import db_conn
from http.cookiejar import MozillaCookieJar
from typing import Optional
import time as _time_mod
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set
from nc.cookies import _cookies_input_to_netscape, _dedupe_cookie_text
from nc.dbexport import db_export_sql as _dbx_export, db_import_sql as _dbx_import, export_summary as _dbx_summary

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

       Body: {"cookies": "<text>"} — der Inhalt ist entweder das Netscape-
       Format (Extension 'Get cookies.txt LOCALLY') ODER ein JSON-Array
       (Extension 'Cookie-Editor' / 'EditThisCookie'). Format wird automatisch
       erkannt.

       Ablauf (defensiv — alte Cookies gehen NIE kaputt):
         1. Input nach Netscape konvertieren.
         2. In <COOKIE_FILE>.new schreiben und mit MozillaCookieJar validieren.
         3. Prüfen dass ein Auth-Cookie (sessionid_ss/sessionid) drin ist —
            sonst Abbruch (User war im Browser nicht eingeloggt). Alte Datei
            bleibt unangetastet.
         4. Alte Datei nach <COOKIE_FILE>.bak sichern.
         5. Atomar ersetzen (os.replace) + Cache leeren → sofort live.

       Keine Zusatz-Software auf dem Server nötig.
    """
    payload = request.get_json(silent=True) or {}
    raw = (payload.get("cookies") or "").strip()
    if not raw:
        return jsonify(ok=False, error=_t("Keine Cookie-Daten übergeben.")), 400
    if len(raw) > 2_000_000:
        return jsonify(ok=False, error=_t("Eingabe zu groß (>2 MB).")), 400

    # 1) Konvertieren
    try:
        netscape, n_parsed = _cookies_input_to_netscape(raw)
    except json.JSONDecodeError as e:
        return jsonify(ok=False, error=f"JSON nicht lesbar: {_fehler_text(e, 'api_cookies_update')}"), 400
    except Exception as e:
        return jsonify(ok=False, error=f"Cookies nicht verarbeitbar: {_fehler_text(e, 'api_cookies_update')}"), 400
    if n_parsed == 0:
        return jsonify(ok=False,
                       error=_t("Keine gültigen Cookies erkannt. Erwartet wird das "
                                "Netscape-Format (cookies.txt) oder ein JSON-Array.")), 400
    # 1b) Doppelte Namen (z.B. msToken unter mehreren Domains) automatisch
    #     bereinigen → verhindert die 'mehrfach unter verschiedenen Domains'-Warnung.
    try:
        netscape, n_dupes = _dedupe_cookie_text(netscape)
    except Exception:
        n_dupes = 0

    # 2) Temp schreiben + validieren
    tmp = _c().cfg["COOKIE_FILE"] + ".new"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(netscape)
        cj = MozillaCookieJar(tmp)
        cj.load(ignore_discard=True, ignore_expires=True)
        names = {c.name for c in cj}
    except Exception as e:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return jsonify(ok=False, error=f"Validierung fehlgeschlagen: {_fehler_text(e, 'api_cookies_update')}"), 400

    # 3) Auth-Cookie verlangen — sonst nicht überschreiben
    if "sessionid_ss" not in names and "sessionid" not in names:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return jsonify(
            ok=False,
            error=_t("Kein Auth-Cookie (sessionid_ss/sessionid) gefunden. Bist du im "
                     "Browser bei TikTok eingeloggt? Update abgebrochen — die alten "
                     "Cookies bleiben erhalten."),
            parsed=n_parsed,
            found=sorted(names)[:20],
        ), 400

    # 4) Backup
    backed_up = False
    if os.path.exists(_c().cfg["COOKIE_FILE"]):
        try:
            shutil.copy2(_c().cfg["COOKIE_FILE"], _c().cfg["COOKIE_FILE"] + ".bak")
            backed_up = True
        except Exception as e:
            log.warning(f"Cookie-Backup fehlgeschlagen (fahre fort): {e}")

    # 5) Atomar ersetzen
    try:
        os.replace(tmp, _c().cfg["COOKIE_FILE"])
    except Exception as e:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return jsonify(ok=False, error=f"Schreiben fehlgeschlagen: {_fehler_text(e, 'api_cookies_update')}"), 500

    # Cache invalidieren → _load_cookies_dict() lädt beim nächsten Zugriff neu
    try:
        _c().cfg["_COOKIES_CACHE"].pop("v", None)
    except Exception:
        pass

    health = _c().get_cookie_health()
    try:
        log.info(
            f"Cookies via Dashboard aktualisiert: {n_parsed} Cookies geschrieben, "
            f"status={health.get('status')}, critical_present={health.get('critical_present')}, "
            f"backup={'ja' if backed_up else 'nein'}"
        )
    except Exception:
        pass
    return jsonify(ok=True, parsed=n_parsed, backed_up=backed_up,
                   deduped=n_dupes,
                   auth_cookie=("sessionid_ss" if "sessionid_ss" in names else "sessionid"),
                   health=health)


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
