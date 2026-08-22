"""nc.ledger — Einnahmen-Journal fuer die Steuer-Auswertung (rein, bot-frei).

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL NICHT AUF overlay_events AUFSETZT
════════════════════════════════════════════════════════════════════════
Naheliegend waere: die vorhandenen 'donation'-Events summieren und als
Jahreseinnahme ausgeben. Das waere FALSCH, und zwar aus drei Gruenden:

1. overlay_events enthaelt SCHAETZWERTE. nc.donations rechnet Bits, Subs
   und Superchats ueber feste Kurse (_BITS_EUR = 0.01, _TWITCH_SUB_EUR =
   2.50, _USD_EUR = 0.92) in Euro um. Das sind Anzeigewerte fuers
   Overlay, keine Zahlungsbelege.

2. Der ANGEZEIGTE Betrag ist nicht der ausgezahlte. Twitch, YouTube und
   Kick behalten ihren Anteil ein (bei Subs typischerweise ~50 %,
   Superchats ~30 %). Was beim Finanzamt zaehlt, ist was auf dem Konto
   ankommt — plus die einbehaltene Gebuehr als Betriebsausgabe, wenn
   sie belegt ist.

3. Der ZUFLUSSZEITPUNKT ist ein anderer. Ein Superchat im Dezember wird
   im Januar/Februar ausgezahlt. Bei Einnahmen-Ueberschuss-Rechnung
   (§ 4 Abs. 3 EStG) zaehlt das Zuflussprinzip — also der Monat der
   Gutschrift, nicht der Monat des Chats.

DESHALB: Dieses Journal fuehrt AUSZAHLUNGEN (payout) als Wahrheit. Die
overlay_events dienen nur als Plausibilitaets-Gegenprobe ("laut Overlay
kamen im Q3 ~X EUR rein, ausgezahlt wurden Y" — grosse Abweichung =
Hinweis auf eine vergessene Abrechnung).

TikTok kommt hier ueberhaupt nicht vor: TikTok-Gifts gehen an den
getrackten Streamer, nicht an unsere Kanaele. Fremdes Geld ist keine
Einnahme (siehe REVENUE_PLATFORMS in bot_v37).

════════════════════════════════════════════════════════════════════════
GoBD-NAEHE (kein Zertifikat, aber die Grundsaetze)
════════════════════════════════════════════════════════════════════════
* UNVERAENDERBARKEIT: Eintraege werden nie geaendert oder geloescht.
  Korrekturen laufen als Storno-Gegenbuchung mit Verweis (storno_of).
* NACHVOLLZIEHBARKEIT: fortlaufende, lueckenlose Nummer je Jahr.
* VOLLSTAENDIGKEIT: jeder Eintrag traegt Beleg-Referenz und Quelle.
* Ein Pruefsummen-Feld (row_hash) verkettet die Eintraege, sodass eine
  nachtraegliche Manipulation in der DB auffaellt.

════════════════════════════════════════════════════════════════════════
WICHTIG — GRENZE DIESES WERKZEUGS
════════════════════════════════════════════════════════════════════════
Das hier ist eine strukturierte Einnahmen-Aufstellung, KEINE
Steuerberatung und kein Ersatz fuer eine Buchhaltung. Was fuer dich
gilt — Kleinunternehmerregelung, Umsatzsteuerpflicht, Reverse-Charge
bei Auszahlungen aus dem EU-Ausland oder den USA (Twitch/Google sitzen
in Irland bzw. den USA), Gewerbeanmeldung, Liebhaberei-Abgrenzung —
haengt an deiner konkreten Situation. Diese Aufstellung ist als
VORARBEIT fuer eine Steuerberaterin gedacht, damit die nicht bei Null
anfaengt. Die Zahlen musst du gegen deine Kontoauszuege und die
Plattform-Abrechnungen pruefen.
"""

import csv
import hashlib
import io
import json
import re
from datetime import datetime, timezone

# Plattformen, die Geld an EIGENE Kanaele auszahlen. Deckungsgleich mit
# REVENUE_PLATFORMS in bot_v37 — bewusst hier gespiegelt, damit das Modul
# bot-frei bleibt und isoliert testbar ist.
PLATFORMS = ("twitch", "youtube", "kick", "sonstige")

# Buchungsarten.
#   payout      = Plattform-Auszahlung auf das Konto (der Regelfall)
#   direct      = Direktspende (PayPal/Ueberweisung) ohne Plattform dazwischen
#   correction  = Storno/Korrektur einer frueheren Buchung
KINDS = ("payout", "direct", "correction")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS revenue_entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    seq_year      INTEGER NOT NULL,
    seq_no        INTEGER NOT NULL,
    booked_on     TEXT    NOT NULL,
    platform      TEXT    NOT NULL,
    kind          TEXT    NOT NULL,
    gross_eur     REAL    NOT NULL,
    fee_eur       REAL    NOT NULL DEFAULT 0,
    net_eur       REAL    NOT NULL,
    currency      TEXT    NOT NULL DEFAULT 'EUR',
    fx_rate       REAL,
    original_amount REAL,
    doc_ref       TEXT    NOT NULL DEFAULT '',
    note          TEXT    NOT NULL DEFAULT '',
    storno_of     INTEGER,
    created_at    TEXT    NOT NULL,
    prev_hash     TEXT    NOT NULL DEFAULT '',
    row_hash      TEXT    NOT NULL DEFAULT ''
)
"""
_IDX = (
    "CREATE INDEX IF NOT EXISTS idx_rev_booked ON revenue_entries(booked_on)",
    "CREATE INDEX IF NOT EXISTS idx_rev_year   ON revenue_entries(seq_year, seq_no)",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_rev_seq ON revenue_entries(seq_year, seq_no)",
)

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class LedgerError(ValueError):
    """Fachlicher Fehler — Aufrufer zeigt die Meldung dem Operator."""


# ───────────────────────────────────────────────────────────── Setup

def ensure_schema(conn):
    conn.execute(_SCHEMA)
    for stmt in _IDX:
        try:
            conn.execute(stmt)
        except Exception:
            pass


# ─────────────────────────────────────────────────────── Hash-Kette

def _hash_row(prev_hash, payload: dict) -> str:
    """Verkettete Pruefsumme. Aendert jemand einen alten Betrag direkt in
    der DB, passt ab dort keine Kette mehr — verify_chain() findet die
    Stelle. Kein Schutz gegen komplettes Neuschreiben, aber genau das
    unterscheidet 'versehentlich veraendert' von 'bewusst gefaelscht'."""
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))
    return hashlib.sha256((prev_hash + "|" + blob).encode("utf-8")).hexdigest()


def _last_row(conn):
    return conn.execute(
        "SELECT id, row_hash FROM revenue_entries ORDER BY id DESC LIMIT 1"
    ).fetchone()


def verify_chain(conn) -> dict:
    """Prueft die Hash-Kette. {ok, checked, broken_at}."""
    rows = conn.execute(
        "SELECT * FROM revenue_entries ORDER BY id ASC").fetchall()
    prev = ""
    for r in rows:
        expect = _hash_row(prev, _payload_of(r))
        if expect != (r["row_hash"] or ""):
            return {"ok": False, "checked": len(rows), "broken_at": r["id"]}
        prev = r["row_hash"]
    return {"ok": True, "checked": len(rows), "broken_at": None}


def _payload_of(r) -> dict:
    return {"seq_year": r["seq_year"], "seq_no": r["seq_no"],
            "booked_on": r["booked_on"], "platform": r["platform"],
            "kind": r["kind"], "gross_eur": round(float(r["gross_eur"]), 2),
            "fee_eur": round(float(r["fee_eur"]), 2),
            "net_eur": round(float(r["net_eur"]), 2),
            "currency": r["currency"], "doc_ref": r["doc_ref"] or "",
            "storno_of": r["storno_of"]}


# ────────────────────────────────────────────────────────── Buchen

def _norm_amount(v, field) -> float:
    try:
        f = float(str(v).replace("\u20ac", "").replace(",", ".").strip())
    except (TypeError, ValueError):
        raise LedgerError(f"{field}: '{v}' ist keine Zahl") from None
    return round(f, 2)


def add_entry(conn, booked_on, platform, gross_eur, *, kind="payout",
              fee_eur=0.0, currency="EUR", fx_rate=None,
              original_amount=None, doc_ref="", note="", storno_of=None):
    """Eine Buchung anlegen. Append-only — es gibt bewusst kein update().

    booked_on: ISO-Datum der GUTSCHRIFT (Zuflussprinzip), nicht des Streams.
    gross_eur: was die Plattform als Bruttoertrag ausweist.
    fee_eur:   einbehaltene Plattformgebuehr (Betriebsausgabe, wenn belegt).
    net_eur    wird als gross - fee berechnet und mitgespeichert, damit eine
               spaetere Kursaenderung alte Buchungen nicht rueckwirkend
               veraendert.
    """
    if not _DATE_RE.match(str(booked_on or "")):
        raise LedgerError("booked_on muss YYYY-MM-DD sein (Datum der Gutschrift)")
    p = (platform or "").strip().lower()
    if p not in PLATFORMS:
        raise LedgerError(f"platform muss eine von {PLATFORMS} sein — "
                          f"TikTok ist bewusst nicht dabei (fremdes Geld)")
    k = (kind or "payout").strip().lower()
    if k not in KINDS:
        raise LedgerError(f"kind muss eine von {KINDS} sein")

    gross = _norm_amount(gross_eur, "gross_eur")
    fee = _norm_amount(fee_eur or 0, "fee_eur")
    if k != "correction" and gross < 0:
        raise LedgerError("Negative Betraege nur als kind='correction' "
                          "(Storno) — eine Einnahme wird nie nachtraeglich "
                          "kleiner gebucht, sie wird gegengebucht.")
    if k == "correction" and not storno_of:
        raise LedgerError("Storno braucht storno_of (ID der Ursprungsbuchung)")
    net = round(gross - fee, 2)

    ensure_schema(conn)
    year = int(str(booked_on)[:4])
    row = conn.execute(
        "SELECT COALESCE(MAX(seq_no), 0) AS m FROM revenue_entries "
        "WHERE seq_year=?", (year,)).fetchone()
    seq_no = int(row["m"]) + 1

    last = _last_row(conn)
    prev_hash = (last["row_hash"] if last else "") or ""
    payload = {"seq_year": year, "seq_no": seq_no, "booked_on": booked_on,
               "platform": p, "kind": k, "gross_eur": gross, "fee_eur": fee,
               "net_eur": net, "currency": (currency or "EUR").upper(),
               "doc_ref": doc_ref or "", "storno_of": storno_of}
    row_hash = _hash_row(prev_hash, payload)

    conn.execute(
        "INSERT INTO revenue_entries (seq_year, seq_no, booked_on, platform, "
        "kind, gross_eur, fee_eur, net_eur, currency, fx_rate, "
        "original_amount, doc_ref, note, storno_of, created_at, prev_hash, "
        "row_hash) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (year, seq_no, booked_on, p, k, gross, fee, net,
         (currency or "EUR").upper(),
         (float(fx_rate) if fx_rate else None),
         (float(original_amount) if original_amount else None),
         doc_ref or "", note or "", storno_of,
         datetime.now(timezone.utc).isoformat(), prev_hash, row_hash))
    return {"seq_year": year, "seq_no": seq_no, "net_eur": net,
            "belegnr": f"{year}-{seq_no:04d}"}


# ─────────────────────────────────────────────────────── Auswertung

def summary(conn, year: int) -> dict:
    """Jahresaufstellung: Summen je Plattform, je Quartal, je Monat."""
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM revenue_entries WHERE booked_on >= ? AND booked_on <= ? "
        "ORDER BY booked_on ASC, seq_no ASC",
        (f"{year}-01-01", f"{year}-12-31")).fetchall()

    by_platform, by_month, by_quarter = {}, {}, {}
    tot_g = tot_f = tot_n = 0.0
    for r in rows:
        g, f, n = float(r["gross_eur"]), float(r["fee_eur"]), float(r["net_eur"])
        tot_g += g; tot_f += f; tot_n += n
        for bucket, key in ((by_platform, r["platform"]),
                            (by_month, str(r["booked_on"])[:7]),
                            (by_quarter, f"Q{(int(str(r['booked_on'])[5:7]) - 1) // 3 + 1}")):
            d = bucket.setdefault(key, {"gross": 0.0, "fee": 0.0,
                                        "net": 0.0, "count": 0})
            d["gross"] += g; d["fee"] += f; d["net"] += n; d["count"] += 1

    def _round(d):
        return {k: {kk: (round(vv, 2) if isinstance(vv, float) else vv)
                    for kk, vv in v.items()} for k, v in sorted(d.items())}

    return {"year": year, "entries": len(rows),
            "total": {"gross": round(tot_g, 2), "fee": round(tot_f, 2),
                      "net": round(tot_n, 2)},
            "by_platform": _round(by_platform),
            "by_quarter": _round(by_quarter),
            "by_month": _round(by_month),
            "chain": verify_chain(conn)}


def entries(conn, year: int) -> list:
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM revenue_entries WHERE booked_on >= ? AND booked_on <= ? "
        "ORDER BY booked_on ASC, seq_no ASC",
        (f"{year}-01-01", f"{year}-12-31")).fetchall()
    return [{"belegnr": f"{r['seq_year']}-{r['seq_no']:04d}",
             "id": r["id"], "booked_on": r["booked_on"],
             "platform": r["platform"], "kind": r["kind"],
             "gross_eur": round(float(r["gross_eur"]), 2),
             "fee_eur": round(float(r["fee_eur"]), 2),
             "net_eur": round(float(r["net_eur"]), 2),
             "currency": r["currency"], "fx_rate": r["fx_rate"],
             "original_amount": r["original_amount"],
             "doc_ref": r["doc_ref"] or "", "note": r["note"] or "",
             "storno_of": r["storno_of"]} for r in rows]


def export_csv(conn, year: int) -> str:
    """CSV fuer die Steuerberaterin. Semikolon + UTF-8-BOM, weil Excel in
    deutscher Lokalisierung sonst alles in eine Spalte kippt. Betraege mit
    Komma als Dezimaltrenner."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", quoting=csv.QUOTE_MINIMAL,
                   lineterminator="\r\n")
    w.writerow(["Belegnr", "Datum_Gutschrift", "Plattform", "Art",
                "Brutto_EUR", "Gebuehr_EUR", "Netto_EUR", "Waehrung",
                "Kurs", "Originalbetrag", "Belegreferenz", "Notiz",
                "Storno_zu"])
    de = lambda v: ("%.2f" % float(v)).replace(".", ",")   # noqa: E731
    for e in entries(conn, year):
        w.writerow([e["belegnr"], e["booked_on"], e["platform"], e["kind"],
                    de(e["gross_eur"]), de(e["fee_eur"]), de(e["net_eur"]),
                    e["currency"],
                    (de(e["fx_rate"]) if e["fx_rate"] else ""),
                    (de(e["original_amount"]) if e["original_amount"] else ""),
                    e["doc_ref"], e["note"],
                    (e["storno_of"] or "")])
    s = summary(conn, year)
    w.writerow([])
    w.writerow(["SUMME", year, "", "", de(s["total"]["gross"]),
                de(s["total"]["fee"]), de(s["total"]["net"]), "EUR"])
    return "\ufeff" + buf.getvalue()


def crosscheck(conn, year: int, revenue_sql_in: str) -> dict:
    """Gegenprobe Overlay-Schaetzung vs. gebuchte Auszahlung.

    Bewusst KEINE automatische Uebernahme: die Overlay-Summe ist eine
    Schaetzung aus Anzeigewerten (siehe Modul-Docstring). Sie taugt nur
    als Warnlampe — weicht sie stark ab, fehlt vermutlich eine
    Plattform-Abrechnung im Journal."""
    est = 0.0
    try:
        rows = conn.execute(
            "SELECT amount FROM overlay_events WHERE kind='donation' "
            "AND COALESCE(platform,'kick') IN " + revenue_sql_in +
            " AND ts >= ? AND ts <= ?",
            (f"{year}-01-01", f"{year}-12-31T23:59:59")).fetchall()
        for r in rows:
            try:
                est += float(str(r["amount"]).replace("\u20ac", "")
                             .replace(",", ".").strip() or 0)
            except (TypeError, ValueError):
                pass
    except Exception:
        return {"available": False}
    booked = summary(conn, year)["total"]["gross"]
    diff = round(booked - est, 2)
    return {"available": True, "overlay_estimate_eur": round(est, 2),
            "booked_gross_eur": booked, "diff_eur": diff,
            "hint": ("Overlay-Schaetzung und gebuchte Auszahlungen liegen weit "
                     "auseinander — fehlt eine Plattform-Abrechnung im Journal?"
                     if est > 0 and abs(diff) > max(50.0, est * 0.5)
                     else "unauffaellig")}


DISCLAIMER = (
    "Diese Aufstellung ist eine strukturierte Vorarbeit, keine "
    "Steuerberatung. Gebucht wird der ZUFLUSS (Datum der Gutschrift), "
    "nicht der Zeitpunkt des Streams. Die Zahlen sind gegen Kontoauszuege "
    "und die Abrechnungen von Twitch/YouTube/Kick zu pruefen. Ob "
    "Kleinunternehmerregelung, Umsatzsteuerpflicht oder Reverse-Charge auf "
    "Auszahlungen aus dem Ausland greifen, entscheidet dein Steuerbuero."
)
