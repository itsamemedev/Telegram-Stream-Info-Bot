"""nc.routes.money — die Routen unter /api/donations,/api/finanzamt als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
from flask import Blueprint, Response, jsonify, request
from nc.dbwrap import db_conn
from nc import i18n as _nc_i18n
from nc import revenue as _nc_revenue
from nc import ledger as _nc_ledger
from nc import donations as _nc_donations
from nc.donationsdb import parse_eur as _parse_eur, manual_rows as _manual_donations_rows, manual_total as _manual_donations_total

from nc import ctx as _ctx

bp = Blueprint("money", __name__)

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


def _donations_unknown_count(conn, days=30):
    """Wie viele Spenden-Zeilen haben keine verwertbare Herkunft?
       v4.0-W59: nach nc/donations.py extrahiert (conn-injiziert, gegen SQLite bewiesen)."""
    return _nc_donations.unknown_count(conn, days)


@bp.route("/api/donations/reset", methods=["POST"])
def api_donations_reset():
    """v4.0-W65: Spenden-DB leeren. Löscht alle overlay_events mit kind='donation'
       (die bisherigen Einträge sind durch Bugs entstanden, es gab real keine
       Spenden). Der Ziel-Fortschritt wird live aus genau diesen Zeilen summiert
       und geht dadurch automatisch auf 0 zurück. Follows/Reaktionen bleiben."""
    try:
        with db_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM overlay_events WHERE kind='donation'")
            removed = cur.rowcount if (cur.rowcount is not None and cur.rowcount >= 0) else 0
            conn.commit()
        log.info("Spenden-DB geleert: %s Zeilen entfernt (Dashboard)", removed)
        return jsonify(ok=True, removed=int(removed))
    except Exception as e:
        log.error("Spenden-Reset fehlgeschlagen: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/donations/add", methods=["POST"])
def api_donations_add():
    """v4.0-W102: manuelle Spende erfassen (Dashboard). Betreiber-gepflegt, weil
       PayPal/Krypto keine öffentliche Live-Summe liefern. Fließt in den
       Website-Fortschritt (current_eur = env-Basis + Summe manuell)."""
    src = request.get_json(silent=True) or request.form or request.values
    amount = _parse_eur(src.get("amount"))
    if amount is None or amount <= 0:
        return jsonify(ok=False, error=_t("Betrag fehlt oder ungültig (z. B. 12,50).")), 400
    if amount > 1_000_000:
        return jsonify(ok=False, error=_t("Betrag unplausibel groß.")), 400
    note = (str(src.get("note") or src.get("source") or "").strip())[:120] or "manuell"
    msg = (str(src.get("message") or "").strip())[:500]
    ts_in = str(src.get("date") or src.get("ts") or "").strip()
    try:
        ts = (datetime.fromisoformat(ts_in).astimezone(timezone.utc).isoformat()
              if ts_in else datetime.now(timezone.utc).isoformat())
    except Exception:
        ts = datetime.now(timezone.utc).isoformat()
    try:
        with db_conn() as conn:
            conn.execute("INSERT INTO overlay_events (ts, kind, name, amount, message, platform) "
                         "VALUES (?,?,?,?,?, 'manual')",
                         (ts, "donation", note, ("%.2f" % amount), msg))
            conn.commit()
        log.info("Manuelle Spende erfasst: %.2f EUR (%s)", amount, note)
        return jsonify(ok=True, amount_eur=round(amount, 2),
                       total_eur=_manual_donations_total())
    except Exception as e:
        log.error("Manuelle Spende fehlgeschlagen: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/donations/manual")
def api_donations_manual():
    """v4.0-W102: Liste + Summe der manuell erfassten Spenden fürs Dashboard."""
    rows = _manual_donations_rows(limit=_c().arg_int("limit", 100, 1, 1000))
    return jsonify(ok=True, total_eur=round(sum(r["amount_eur"] for r in rows), 2),
                   count=len(rows), items=rows)


@bp.route("/api/donations/manual/<int:rid>/delete", methods=["POST"])
def api_donations_manual_delete(rid):
    """v4.0-W102: eine manuelle Spende wieder entfernen (Korrektur)."""
    try:
        with db_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM overlay_events WHERE id=? AND kind='donation' "
                        "AND platform='manual'", (int(rid),))
            removed = cur.rowcount if (cur.rowcount and cur.rowcount > 0) else 0
            conn.commit()
        return jsonify(ok=bool(removed), removed=int(removed),
                       total_eur=_manual_donations_total())
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/donations/summary")
def api_donations_summary():
    """V37-DON: Donations aus overlay_events, nach Plattform aufgeschluesselt.

    Alle vier Plattformen schreiben ueber _overlay_push('donation', ...) mit
    platform-Tag in dieselbe Tabelle — Kick/TikTok/Twitch (Bits/Subs)/YouTube
    (Superchat). Dieses Panel macht sie erstmals sichtbar. ?days=30 begrenzt.
    """
    try:
        days = _c().arg_int("days", 30, 1, 365)
    except ValueError:
        days = 30
    out = {"ok": True, "window_days": days, "by_platform": [], "recent": [],
           "total_count": 0}
    try:
        with db_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "SELECT platform, COUNT(*) n FROM overlay_events "
                    "WHERE kind='donation' AND platform IN"
                    + _nc_revenue.sql_in() +
                    " AND ts >= datetime('now', ?) "
                    "GROUP BY platform", ("-%d days" % days,))
            except Exception:
                cur.execute(
                    "SELECT platform, COUNT(*) n FROM overlay_events "
                    "WHERE kind='donation' AND platform IN"
                    + _nc_revenue.sql_in() +
                    (" AND ts >= (NOW() - INTERVAL %d DAY) "
                     "GROUP BY platform" % days))
            rows = cur.fetchall()
            # Alle vier Plattformen zeigen, auch mit 0 — macht sichtbar, was
            # verbunden ist und was (noch) nicht.
            counts = {r["platform"] or "?": r["n"] for r in rows}
            # V37-DON: TikTok bewusst NICHT im Panel — auf Wunsch entfernt.
            # (Die Erfassung läuft weiter, nur die Anzeige zeigt TikTok nicht.)
            for p in ("kick", "twitch", "youtube"):
                out["by_platform"].append({"platform": p, "count": counts.get(p, 0)})
                out["total_count"] += counts.get(p, 0)
            # Letzte 15 Donations (ohne TikTok — auf Wunsch aus dem Panel)
            try:
                cur.execute(
                    "SELECT ts, name, amount, message, platform FROM overlay_events "
                    "WHERE kind='donation' AND platform IN"
                    + _nc_revenue.sql_in() +
                    " ORDER BY id DESC LIMIT 15")
            except Exception:
                pass
            for r in cur.fetchall():
                out["recent"].append({
                    "ts": r["ts"], "name": r["name"] or "?",
                    "amount": r["amount"] or "", "message": r["message"] or "",
                    "platform": r["platform"] or "?"})
            # B138: Zeilen ohne Herkunft mitzaehlen — sie sind nicht weg, sie
            # gelten nur nicht mehr als eigene Einnahme. Ohne diese Zahl wirkt
            # die (korrekt) gesunkene Summe wie Datenverlust.
            out["unknown_count"] = _donations_unknown_count(conn, days)
        return jsonify(out)
    except Exception as e:
        log.warning("api_donations_summary: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/finanzamt/entries")
def api_finanzamt_entries():
    try:
        year = _c().arg_int("year", datetime.now(timezone.utc).year)
    except ValueError:
        return jsonify(ok=False, error=_t("year muss eine Jahreszahl sein")), 400
    try:
        with db_conn() as conn:
            return jsonify(ok=True, year=year,
                           entries=_nc_ledger.entries(conn, year),
                           summary=_nc_ledger.summary(conn, year),
                           crosscheck=_nc_ledger.crosscheck(conn, year, _nc_revenue.sql_in()),
                           platforms=list(_nc_ledger.PLATFORMS),
                           kinds=list(_nc_ledger.KINDS),
                           disclaimer=_nc_ledger.DISCLAIMER)
    except Exception as e:
        log.warning("api_finanzamt_entries: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/finanzamt/entry", methods=["POST"])
def api_finanzamt_add():
    """Auszahlung buchen. Append-only — es gibt bewusst kein PUT/DELETE.
    Korrektur = neue Buchung mit kind='correction' + storno_of."""
    d = request.get_json(silent=True) or {}
    try:
        with db_conn() as conn:
            res = _nc_ledger.add_entry(
                conn,
                d.get("booked_on"), d.get("platform"), d.get("gross_eur"),
                kind=(d.get("kind") or "payout"),
                fee_eur=d.get("fee_eur") or 0,
                currency=(d.get("currency") or "EUR"),
                fx_rate=d.get("fx_rate"),
                original_amount=d.get("original_amount"),
                doc_ref=(d.get("doc_ref") or ""),
                note=(d.get("note") or ""),
                storno_of=d.get("storno_of"))
            conn.commit()
        return jsonify(ok=True, **res)
    except _nc_ledger.LedgerError as e:
        return jsonify(ok=False, error=str(e)), 400
    except Exception as e:
        log.warning("api_finanzamt_add: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/finanzamt/export.csv")
def api_finanzamt_csv():
    """CSV fuer die Steuerberaterin (Semikolon + BOM, DE-Dezimalkomma)."""
    try:
        year = _c().arg_int("year", datetime.now(timezone.utc).year)
    except ValueError:
        return Response("year muss eine Jahreszahl sein", status=400)
    try:
        with db_conn() as conn:
            body = _nc_ledger.export_csv(conn, year)
        return Response(body, mimetype="text/csv; charset=utf-8",
                        headers={"Content-Disposition":
                                 f'attachment; filename="einnahmen_{year}.csv"'})
    except Exception as e:
        log.warning("api_finanzamt_csv: %s", e)
        return Response(f"Export fehlgeschlagen: {e}", status=500)
