"""nc.tagesbericht — der Tagesbericht (/summary, Autopost, /api/…/tagesbericht), bot-frei.

v5.6-W197 aus bot.py geloest (88 Zeilen). Er las nur die Datenbank und zwei
Lagen des Bots — Speicher und Cookie-Gesundheit; die kommen per configure()
als Funktionen (nicht als Werte: beide aendern sich zur Laufzeit).

Synchron und blockierend (DB, Plattenstatistik): aus dem Event-Loop nur per
asyncio.to_thread aufrufen — ein Vertrag (W176) haelt das fuer die Schleife fest.
"""

from datetime import datetime, timedelta, timezone

from nc.dbwrap import db_conn
from nc.textutil import safe


def _nicht_konfiguriert():
    raise RuntimeError("nc.tagesbericht: configure(storage=..., cookies=...) fehlt "
                       "im Startpfad von bot.py")


_KONF = {"storage": _nicht_konfiguriert, "cookies": _nicht_konfiguriert}


def configure(*, storage, cookies):
    """storage() -> dict wie get_storage_stats, cookies() -> dict wie get_cookie_health."""
    _KONF.update(storage=storage, cookies=cookies)


def bauen() -> str:
    """Baut den Summary-Text. Synchron — alles aus DB. Wird auch von
       /summary command + autopost benutzt."""
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=24)).isoformat()
    with db_conn() as conn:
        # Aktuelle Status-Zahlen
        n_track = conn.execute("SELECT COUNT(*) AS c FROM trackings").fetchone()["c"]
        n_paused = conn.execute(
            "SELECT COUNT(*) AS c FROM trackings WHERE COALESCE(paused,0)=1"
        ).fetchone()["c"]
        n_live = conn.execute(
            "SELECT COUNT(*) AS c FROM trackings WHERE last_live=1").fetchone()["c"]
        n_rec_active = conn.execute(
            "SELECT COUNT(*) AS c FROM trackings WHERE recording=1").fetchone()["c"]

        # Last-24h-Aktivität
        rec_24h = conn.execute(
            "SELECT COUNT(*) AS c FROM recordings WHERE created_at >= ?", (cutoff,)
        ).fetchone()["c"]
        att_24h_total = conn.execute(
            "SELECT COUNT(*) AS c FROM recording_attempts WHERE started_at >= ?",
            (cutoff,)).fetchone()["c"]
        att_24h_ok = conn.execute(
            "SELECT COUNT(*) AS c FROM recording_attempts WHERE started_at >= ? "
            "AND outcome IN ('ok', 'stall_killed_partial')", (cutoff,)
        ).fetchone()["c"]
        att_24h_ed = conn.execute(
            "SELECT COUNT(*) AS c FROM recording_attempts WHERE started_at >= ? "
            "AND outcome = 'early_disconnect'", (cutoff,)).fetchone()["c"]

        # Top 3 User der letzten 24h nach Aufnahmen
        top_rows = conn.execute(
            "SELECT username, COUNT(*) AS n FROM recordings "
            "WHERE created_at >= ? GROUP BY username ORDER BY n DESC LIMIT 3",
            (cutoff,)).fetchall()

    success_pct = int(att_24h_ok / att_24h_total * 100) if att_24h_total else 0

    # Storage
    storage = _KONF["storage"]()
    disk = storage.get("disk", {}) or {}
    rec_size_mb = (storage.get("recordings_dir", {}).get("total_bytes") or 0) / 1024 / 1024
    disk_pct = None
    if disk.get("total_bytes") and disk.get("used_bytes"):
        disk_pct = int(disk["used_bytes"] / disk["total_bytes"] * 100)

    # Cookie-Health
    ch = _KONF["cookies"]()

    # Bauen
    lines = []
    lines.append(f"<b>📋 DAILY SUMMARY</b> <i>{now.strftime('%d.%m.%Y')}</i>")
    lines.append("")
    lines.append("<b>Status jetzt:</b>")
    lines.append(f"  {n_track} Trackings ({n_live} live, {n_rec_active} aufnehmend"
                 + (f", {n_paused} pausiert" if n_paused else "") + ")")
    lines.append("")
    lines.append("<b>Letzte 24h:</b>")
    if att_24h_total:
        lines.append(f"  {rec_24h} Aufnahmen erfolgreich gespeichert")
        lines.append(f"  {att_24h_total} Versuche · {success_pct}% Erfolg"
                     + (f" · {att_24h_ed} early-disconnects" if att_24h_ed else ""))
    else:
        lines.append("  <i>keine Aufnahme-Aktivität</i>")

    if top_rows:
        lines.append("")
        lines.append("<b>Top User (24h):</b>")
        for i, r in enumerate(top_rows, 1):
            lines.append(f"  {i}. @{safe(r['username'])} — {r['n']} Aufnahmen")

    lines.append("")
    lines.append("<b>Storage:</b>")
    if disk_pct is not None:
        warn = " ⚠️" if disk_pct > 85 else ""
        lines.append(f"  Disk: {disk_pct}% belegt{warn}")
    lines.append(f"  Recordings: {rec_size_mb:.0f} MB")
    if storage.get("retention_days") and storage["retention_days"] > 0:
        lines.append(f"  Auto-Cleanup: nach {storage['retention_days']} Tagen")

    lines.append("")
    lines.append("<b>Cookies:</b>")
    icon = {"ok": "✅", "warning": "⚠️", "critical": "🚨",
            "missing": "❌", "parse_error": "❌"}.get(ch["status"], "❓")
    lines.append(f"  {icon} {ch['headline']}")

    return "\n".join(lines)
