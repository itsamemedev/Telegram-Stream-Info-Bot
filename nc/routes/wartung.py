"""nc.routes.wartung — was den Bestand in Ordnung haelt.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W24: Zehn Routen, eine Klammer — Speicherplatz, Aufbewahrung, Sicherung
und Archivregeln. Alle vier Gruppen tun dasselbe: **sie halten den Bestand in
Ordnung.** Und drei von ihnen LOESCHEN oder KOPIEREN, sind also die
gefaehrlichste Gruppe dieser Zerlegung.

**Null neue Kontext-Eintraege.** Vorweg geloest:

* **nc/backupcfg.py** — die fuenfzehn .env-Werte fuer Sicherung und
  Aufbewahrung, jeder Name woertlich in einem os.getenv(...). Die
  S3-Zugangsdaten gibt nur `s3_zugang()` heraus; die Routen benutzen
  ausschliesslich `s3_konfiguriert()` (bool).
* **nc/retention.py** — der Aufbewahrungs-Scan mitsamt seiner Haertung. Er
  hatte im Monolithen zwei Aufrufer (Dauerschleife und Route); eine Kopie
  einer loeschenden Funktion war keine Option.
* **nc/archiverules.py** — die vier Regel-Funktionen, aus demselben Grund.

Was hier NICHT hineingehoert: die eigentliche Sicherung (`_local_backup_scan`,
`_system_backup`). Die haengen an boto3, tar und dem Aufnahme-Pfad und
bleiben vorerst im Monolithen — sie kommen als Haken herein.
"""

import json
import os
import threading

from flask import Blueprint, jsonify, request

from nc import archiverules as _nc_arules
from nc import backupcfg as _nc_backup
from nc import i18n as _nc_i18n
from nc import retention as _nc_retention
from nc import storage as _nc_storage
from nc.dbwrap import db_conn

from nc import ctx as _ctx

bp = Blueprint("wartung", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    """v4.1-W24: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _rec_dir() -> str:
    """Das Aufnahme-Verzeichnis. Als Funktion und nicht als Konstante: .env
       wird teils erst nach den ersten Imports geladen (CLAUDE.md)."""
    return (os.getenv("RECORDINGS_DIR", "recordings") or "recordings").strip()


def _archiv_dir() -> str:
    """Das Archivverzeichnis. Leer heisst: kein Archiv konfiguriert."""
    return (os.getenv("ARCHIVE_DIR", "") or "").strip()



# Zwei Bruecken, weil die Signatur sich geaendert hat: nc/retention.py und
# nc/archiverules.py nehmen jetzt entgegen, was der Monolith frueher aus
# Modul-Konstanten las (Aufnahme- bzw. Archivverzeichnis, Ereignisprotokoll).
# Die Routen bleiben dadurch woertlich wie vorher.

def _nc_retention_scan(days, delete=False):
    return _nc_retention.scan(days, _rec_dir(), delete=delete)


def _nc_storage_stats():
    return _nc_storage.stats(_rec_dir(), _archiv_dir(),
                             _nc_backup.recordings_retain_days())


def _nc_storage_cleanup(days=0, dry_run=False):
    return _nc_storage.cleanup(_rec_dir(), days=days, dry_run=dry_run)


def _nc_run_archive_rules(rule_id=None):
    return _nc_arules.run_archive_rules(
        rule_id, archive_dir=_archiv_dir(),
        log_event=_c().log_event)


# Die eigentliche Sicherung bleibt im Monolithen (boto3, tar, Aufnahme-Pfad)
# und wird beim Start hier eingetragen. Sichtbare Kopplung statt versteckter
# im Kontext, dessen 25 Plaetze eine andere Frage beantworten — dieselbe
# Begruendung wie in nc/azraelstate.py und nc/restreamstate.py.
HAKEN = {"local_scan": {"fn": None},   # (limit) -> dict
         "system": {"fn": None}}       # () -> None, laeuft im Daemon-Thread


def _nc_backup_haken(name):
    """Der eingetragene Haken. None, wenn der Bot ihn nie gesetzt hat —
       die Aufrufer pruefen das und sagen es, statt Erfolg zu melden."""
    return HAKEN[name]["fn"]


@bp.route("/api/storage")
def api_storage():
    """Disk-Usage, Recording-Verzeichnis und Archive im Überblick."""
    return jsonify(_nc_storage_stats())


@bp.route("/api/storage/cleanup", methods=["POST"])
def api_storage_cleanup():
    """Cleanup nach Alter. POST-Body: {"days": N, "dry_run": bool}.
       Defaults: days = RECORDINGS_RETAIN_DAYS, dry_run = True.
       Schutz: ohne explizites dry_run:false wird NICHT wirklich gelöscht."""
    payload = request.get_json(silent=True) or {}
    try:
        days = int(payload.get("days", _nc_backup.recordings_retain_days()))
    except (TypeError, ValueError):
        return jsonify(ok=False, error=_t("days muss eine Zahl sein")), 400
    # F47: Safety — explizit dry_run:false setzen muss der Caller
    dry_run = payload.get("dry_run", True)
    if days <= 0 and not payload.get("force"):
        return jsonify(ok=False, error=_t("days <= 0 hat keinen Effekt")), 400
    result = _nc_storage_cleanup(days=days, dry_run=bool(dry_run))
    return jsonify(ok=True, **result)


@bp.route("/api/retention/preview")
def api_retention_preview():
    auto = _nc_backup.retention_days()
    days = request.args.get("days", type=int) or (auto if auto > 0 else 30)
    if days < 1:
        return jsonify(ok=False, error=_t("days muss mindestens 1 sein")), 400
    res = _nc_retention_scan(days, delete=False)
    return jsonify(ok=True, days=days, auto=auto, **res)


@bp.route("/api/retention/run", methods=["POST"])
def api_retention_run():
    d = request.get_json(silent=True) or {}
    auto = _nc_backup.retention_days()
    days = int(d.get("days") or (auto if auto > 0 else 30))
    if days < 1:
        return jsonify(ok=False, error=_t("days muss mindestens 1 sein")), 400
    res = _nc_retention_scan(days, delete=True)
    _c().log.info("Retention manuell: %d Aufnahmen > %d Tage gelöscht (%.1f GB).",
                  res["count"], days, res["freed_bytes"] / 1024**3)
    return jsonify(ok=True, days=days, **res)


@bp.route("/api/backup/system", methods=["POST"])
def api_backup_system():
    """F94: System-Backup sofort anstoßen (läuft im Daemon-Thread — Flask-Route
       kehrt sofort zurück, Fortschritt via /api/backup/status → sys.running)."""
    if _nc_backup.STATE["running"]:
        return jsonify(ok=False, error=_t("System-Backup läuft bereits")), 409
    if not _nc_backup.aktiv():
        return jsonify(ok=False, error=_t("Kein Backup-Ziel konfiguriert (LOCAL_BACKUP_DIR / S3)")), 400
    haken = _nc_backup_haken("system")
    if haken is None:
        # threading.Thread(target=None) startet klaglos und tut nichts —
        # die Route haette started=True gemeldet, ohne dass etwas laeuft.
        return jsonify(ok=False, error=_t("Sicherung nicht bereit — Bot laeuft nicht")), 503
    threading.Thread(target=haken, name="sys-backup-manual", daemon=True).start()
    return jsonify(ok=True, started=True)


@bp.route("/api/backup/status")
def api_backup_status():
    import shutil as _sh
    import importlib.util as _il
    out = {"ok": True, "enabled": _nc_backup.lokal(), "dir": _nc_backup.lokal_dir() or None,
           "pending": 0, "done": 0, "backup_free_gb": None, "dir_ok": False,
           "s3_enabled": _nc_backup.s3(), "s3_bucket": _nc_backup.s3_bucket() or None,
           "s3_endpoint": (_nc_backup.s3_endpoint() or "AWS-Standard") if _nc_backup.s3() else None,
           "boto3": (_il.find_spec("boto3") is not None) if _nc_backup.s3() else None,
           # F94: System-Backup-Status (täglich SYS_BACKUP_HOUR Uhr)
           "sys": {"enabled": _nc_backup.sys_backup(), "hour": _nc_backup.sys_hour(), "keep": _nc_backup.sys_keep(),
                   "running": _nc_backup.STATE["running"],
                   "last_ts": _nc_backup.STATE["last_ts"], "last_file": _nc_backup.STATE["last_file"],
                   "size_mb": _nc_backup.STATE["size_mb"], "files": _nc_backup.STATE["files"],
                   "error": _nc_backup.STATE["error"]}}
    try:
        if _nc_backup.lokal_dir():
            out["dir_ok"] = os.path.isdir(_nc_backup.lokal_dir())
            if out["dir_ok"]:
                du = _sh.disk_usage(_nc_backup.lokal_dir())
                out["backup_free_gb"] = round(du.free / 1024**3, 1)
    except Exception:
        pass
    try:
        with db_conn() as conn:
            out["done"] = conn.execute("SELECT COUNT(*) AS c FROM recordings "
                                       "WHERE COALESCE(backed_up,0)=1").fetchone()["c"]
            out["pending"] = conn.execute("SELECT COUNT(*) AS c FROM recordings "
                                          "WHERE COALESCE(backed_up,0)=0").fetchone()["c"]
    except Exception:
        pass
    return jsonify(out)


@bp.route("/api/backup/run", methods=["POST"])
def api_backup_run():
    haken = _nc_backup_haken("local_scan")
    if haken is None:
        return jsonify(ok=False, error=_t("Sicherung nicht bereit — Bot laeuft nicht")), 503
    return jsonify(haken(50))


@bp.route("/api/auto-archive-rules", methods=["GET", "POST"])
def api_archive_rules():
    if request.method == "GET":
        rows = _nc_arules.list_archive_rules()
        return jsonify(ok=True, rules=[{
            "id": r["id"], "name": r["name"],
            "condition": json.loads(r["condition_json"] or "{}"),
            "action": json.loads(r["action_json"] or "{}"),
            "enabled": bool(r["enabled"]),
            "last_run": r["last_run"],
            "last_match_count": r["last_match_count"],
            "created_at": r["created_at"],
        } for r in rows])
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    condition = data.get("condition") or {}
    action = data.get("action") or {}
    if not name or not isinstance(condition, dict) or not isinstance(action, dict):
        return jsonify(ok=False, error=_t("name, condition und action sind Pflicht")), 400
    rid = _nc_arules.add_archive_rule(name, condition, action)
    if rid is None:
        return jsonify(ok=False, error=_t("Anlegen fehlgeschlagen")), 500
    return jsonify(ok=True, id=rid)


@bp.route("/api/auto-archive-rules/<int:rule_id>", methods=["DELETE"])
def api_archive_rule_delete(rule_id):
    return jsonify(ok=_nc_arules.delete_archive_rule(rule_id))


@bp.route("/api/auto-archive-rules/run", methods=["POST"])
def api_archive_rules_run():
    data = request.get_json(silent=True) or {}
    rule_id = data.get("rule_id")
    result = _nc_run_archive_rules(rule_id)
    code = 200 if result.get("ok") else 400
    return jsonify(result), code
