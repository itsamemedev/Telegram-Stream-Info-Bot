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
Einnahme (siehe REVENUE_PLATFORMS in bot.py).

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

from nc import ddlsafe as _ddlsafe

import csv
import hashlib
import io
import json
import logging
import math
import re
import threading
from datetime import datetime, timezone

_log = logging.getLogger("TikTokBot")

# Plattformen, die Geld an EIGENE Kanaele auszahlen. Deckungsgleich mit
# REVENUE_PLATFORMS in bot.py — bewusst hier gespiegelt, damit das Modul
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
# v4.2-W150: dieselbe Tabelle fuer MariaDB. Die SQLite-Fassung oben kann dort
# nicht laufen — `INTEGER PRIMARY KEY AUTOINCREMENT` ist MariaDB-Fehler 1064,
# und ein Index auf `booked_on TEXT` waere 1170. db_conn() uebersetzt nur die
# Platzhalter, kein DDL: das Steuer-Journal liess sich unter DB_BACKEND=mariadb
# deshalb nie anlegen, und der Umzug brach an genau dieser Tabelle ab.
# Typen so gewaehlt, dass der Hash gleich bleibt: Datum als Zeichenkette,
# Betraege als DOUBLE (MariaDB-REAL ist DOUBLE).
_SCHEMA_MARIADB = """
CREATE TABLE IF NOT EXISTS revenue_entries (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    seq_year      INTEGER NOT NULL,
    seq_no        INTEGER NOT NULL,
    booked_on     VARCHAR(10) NOT NULL,
    platform      VARCHAR(32) NOT NULL,
    kind          VARCHAR(32) NOT NULL,
    gross_eur     DOUBLE  NOT NULL,
    fee_eur       DOUBLE  NOT NULL DEFAULT 0,
    net_eur       DOUBLE  NOT NULL,
    currency      VARCHAR(8) NOT NULL DEFAULT 'EUR',
    fx_rate       DOUBLE,
    original_amount DOUBLE,
    doc_ref       TEXT    NOT NULL,
    note          TEXT    NOT NULL,
    storno_of     INTEGER,
    created_at    VARCHAR(64) NOT NULL,
    prev_hash     VARCHAR(64) NOT NULL DEFAULT '',
    row_hash      VARCHAR(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_nopad_bin
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

def ensure_schema(conn, melden=None, backend=None):
    """Tabelle und Indizes anlegen. Idempotent.

    v4.2-W65: die Indizes liefen bis hierher durch `except Exception: pass`.
    „Index existiert bereits" ist der Normalfall ab dem zweiten Start und
    gehoert geschluckt — eine gesperrte Datenbank oder ein Tippfehler im DDL
    aber nicht. DAS HIER IST DAS STEUER-JOURNAL mit Hash-Kette; ein Schema,
    das anders aussieht als der Code annimmt, faellt sonst erst bei der
    Jahresauswertung auf.

    Ohne `melden` wirft nc.ddlsafe.ddl einen unerwarteten Fehler weiter —
    genau richtig fuer ein Modul ohne Logger. Wer das ueberleben will, reicht
    einen Melder herein.
    """
    if backend is None:
        # Ohne Angabe das Backend, auf das db_conn() gerade zeigt — so
        # brauchen die drei Aufrufer in diesem Modul nichts zu wissen.
        from nc import dbwrap as _dbwrap
        backend = _dbwrap.DB_BACKEND
    if backend == "mariadb":
        conn.execute(_SCHEMA_MARIADB)
        # MariaDB kennt IF NOT EXISTS fuer Indizes nicht in jeder Fassung;
        # ein vorhandener Index (1061) schluckt ddlsafe.
        idx = tuple(s.replace("IF NOT EXISTS ", "") for s in _IDX)
    else:
        conn.execute(_SCHEMA)
        idx = _IDX
    for stmt in idx:
        _ddlsafe.ddl(conn, stmt, melden)


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
        ist = r["row_hash"] or ""
        payload = _payload_of(r)
        if _hash_row(prev, payload) != ist and not _altbestand_storno(prev, payload, ist):
            return {"ok": False, "checked": len(rows), "broken_at": r["id"]}
        prev = r["row_hash"]
    return {"ok": True, "checked": len(rows), "broken_at": None}


def _altbestand_storno(prev, payload, ist) -> bool:
    """Bis v4.2-W149 wurde storno_of so gehasht, wie es hereinkam — aus dem
    Deck (JSON) also als Zeichenkette "5". In der Tabelle steht es als
    INTEGER 5 (SQLite-Typaffinitaet), und die Pruefung rechnete mit der 5:
    JEDE ueber das Deck gebuchte Storno-Buchung meldete die Kette als
    gebrochen. Ein Steuer-Journal, das sich selbst als manipuliert ausweist,
    ist schlimmer als keine Pruefung. Fuer den Altbestand gilt deshalb auch
    der Hash ueber die Zeichenkette — Betraege, Datum und Plattform bleiben
    voll gedeckt, nur die Schreibweise der Storno-ID darf abweichen."""
    if payload.get("storno_of") is None:
        return False
    alt = dict(payload, storno_of=str(payload["storno_of"]))
    return _hash_row(prev, alt) == ist


def _payload_of(r) -> dict:
    return {"seq_year": r["seq_year"], "seq_no": r["seq_no"],
            "booked_on": r["booked_on"], "platform": r["platform"],
            "kind": r["kind"], "gross_eur": round(float(r["gross_eur"]), 2),
            "fee_eur": round(float(r["fee_eur"]), 2),
            "net_eur": round(float(r["net_eur"]), 2),
            "currency": r["currency"], "doc_ref": r["doc_ref"] or "",
            "storno_of": r["storno_of"]}


# ────────────────────────────────────────────────────────── Buchen

def _endliche_zahl(v, field) -> float:
    """Eine endliche Zahl aus Deck-/Telegram-Eingabe, UNGERUNDET."""
    try:
        f = float(str(v).replace("\u20ac", "").replace(",", ".").strip())
    except (TypeError, ValueError):
        raise LedgerError(f"{field}: '{v}' ist keine Zahl") from None
    # float("nan") und float("inf") sind fuer Python Zahlen. "nan" lief bis
    # W149 am Negativ-Riegel vorbei (nan < 0 ist falsch) und starb erst am
    # NOT NULL der Tabelle — "inf" wurde gebucht und machte jede Jahressumme
    # unendlich.
    if not math.isfinite(f):
        raise LedgerError(f"{field}: '{v}' ist kein endlicher Betrag")
    return f


def _norm_amount(v, field) -> float:
    """Ein EUR-Betrag — auf Cent gerundet."""
    return round(_endliche_zahl(v, field), 2)


def _norm_optional(v, field):
    """Kurs und Originalbetrag: leer oder 0 -> None, sonst eine endliche Zahl > 0.

    v4.2-W162: beide gingen roh durch float(). "abc" wurde ein ValueError,
    den die Route als HTTP 500 meldete statt als Eingabefehler; "nan" und
    "inf" wurden gebucht und standen als "nan" in der CSV fuer das
    Steuerbuero. Sie stehen nicht im Hash — gerade deshalb faellt ein
    unsinniger Wert spaeter niemandem auf."""
    # Review #207: NICHT auf Cent runden — ein Kurs 1,2345 ist nicht 1,23, und
    # der Originalbetrag steht in seiner eigenen Waehrung.
    f = 0.0 if v in (None, "") else _endliche_zahl(v, field)
    if f < 0:
        raise LedgerError(f"{field}: '{v}' muss groesser als 0 sein")
    return f or None                # leer und 0 heissen „kein Kurs", wie bisher


def _norm_storno(v):
    """storno_of als Ganzzahl — so steht es in der Tabelle, so muss es in
    den Hash. Siehe _altbestand_storno(). Nur fuer gesetzte Werte; "keine
    Storno-Buchung" entscheidet der Aufrufer."""
    try:
        n = int(str(v).strip())
    except (TypeError, ValueError):
        raise LedgerError(f"storno_of: '{v}' ist keine Buchungs-ID") from None
    if n <= 0:
        raise LedgerError(f"storno_of: '{v}' ist keine Buchungs-ID")
    return n


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

    Seit v4.2-W178 committet add_entry selbst (unter Sperre, siehe unten);
    ein conn.commit() des Aufrufers danach ist harmlos.
    """
    if not _DATE_RE.match(str(booked_on or "")):
        raise LedgerError("booked_on muss YYYY-MM-DD sein (Datum der Gutschrift)")
    # Das Muster allein liess "2026-13-45" durch — gebucht, im Quartal "Q5"
    # summiert und von keiner Monatsauswertung je gefunden.
    try:
        datetime.strptime(str(booked_on), "%Y-%m-%d")
    except ValueError:
        raise LedgerError(f"booked_on: '{booked_on}' ist kein gueltiges Datum") from None
    p = (platform or "").strip().lower()
    if p not in PLATFORMS:
        raise LedgerError(f"platform muss eine von {PLATFORMS} sein — "
                          f"TikTok ist bewusst nicht dabei (fremdes Geld)")
    k = (kind or "payout").strip().lower()
    if k not in KINDS:
        raise LedgerError(f"kind muss eine von {KINDS} sein")

    gross = _norm_amount(gross_eur, "gross_eur")
    fee = _norm_amount(fee_eur or 0, "fee_eur")
    storno_of = None if storno_of in (None, "") else _norm_storno(storno_of)
    fx_rate = _norm_optional(fx_rate, "fx_rate")
    original_amount = _norm_optional(original_amount, "original_amount")
    if k != "correction" and fee < 0:
        raise LedgerError("Eine negative Gebuehr wuerde den Nettobetrag ueber "
                          "den Bruttobetrag heben — Korrekturen als "
                          "kind='correction' buchen.")
    if k != "correction" and gross < 0:
        raise LedgerError("Negative Betraege nur als kind='correction' "
                          "(Storno) — eine Einnahme wird nie nachtraeglich "
                          "kleiner gebucht, sie wird gegengebucht.")
    if k == "correction" and not storno_of:
        raise LedgerError("Storno braucht storno_of (ID der Ursprungsbuchung)")
    net = round(gross - fee, 2)

    ensure_schema(conn)
    # v4.2-W178: Lesen (MAX(seq_no), letzter row_hash) und Schreiben waren
    # nicht verbunden. Zwei Buchungen gleichzeitig (Deck und /einnahmen, oder
    # zwei Tabs) lasen dieselbe Folgenummer — UNIQUE-Fehler, HTTP 500 — oder,
    # bei verschiedenen Jahren, denselben prev_hash: zwei Zeilen haengen am
    # selben Vorgaenger, und verify_chain meldet die Kette ab da fuer immer als
    # gebrochen. Ein Steuer-Journal, das sich selbst als manipuliert ausweist,
    # ist wertlos. Deshalb: Prozess-Sperre, dazu eine Datenbank-Sperre VOR dem
    # Lesen (andere Prozesse, z. B. tools/), und der Commit gehoert hier hinein
    # — eine Sperre, die vor dem Commit faellt, schuetzt nichts.
    from nc import dbwrap as _dbwrap
    backend = _dbwrap.DB_BACKEND
    with _BUCHUNG_LOCK:
        gesperrt = _db_sperren(conn, backend)
        try:
            res = _buchung_schreiben(conn, booked_on, p, k, gross, fee, net,
                                     currency, fx_rate, original_amount,
                                     doc_ref, note, storno_of)
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            if gesperrt:
                _db_entsperren(conn)
    return res


# Prozessweit: eine Buchung nach der anderen. Modul-global, nicht am conn —
# jede Buchung bringt ihre eigene Verbindung mit.
_BUCHUNG_LOCK = threading.Lock()
_MARIADB_SPERRE = "nc_ledger_buchung"


def _db_sperren(conn, backend) -> bool:
    """Schreibsperre VOR dem ersten Lesen. True = benannte Sperre (MariaDB)
    muss wieder freigegeben werden."""
    if backend == "mariadb":
        # GET_LOCK statt SELECT ... FOR UPDATE: Lueckensperren zweier
        # Transaktionen vertragen sich in InnoDB, beide INSERTs liefen dann
        # in einen Deadlock. Die benannte Sperre serialisiert sauber, auch
        # ueber Prozesse.
        r = conn.execute("SELECT GET_LOCK(?, 30) AS ok", (_MARIADB_SPERRE,)).fetchone()
        if not r or int(r["ok"] or 0) != 1:
            raise LedgerError("Journal ist gerade von einer anderen Buchung belegt "
                              "— in einer halben Minute erneut versuchen.")
        return True
    # SQLite: BEGIN IMMEDIATE nimmt die Schreibsperre sofort; eine zweite
    # Verbindung wartet hier (busy_timeout), bis die erste committet hat, und
    # liest danach die neue Folgenummer. Laeuft schon eine Transaktion mit
    # Schreibzugriff, haelt sie die Sperre bereits.
    if not conn.in_transaction:
        conn.execute("BEGIN IMMEDIATE")
    return False


def _db_entsperren(conn) -> None:
    try:
        conn.execute("SELECT RELEASE_LOCK(?)", (_MARIADB_SPERRE,)).fetchone()
    except Exception as e:
        # Bleibt die Sperre an einer Pool-Verbindung haengen, wartet jede
        # folgende Buchung 30 s und scheitert — das muss im Fehlerlog stehen.
        _log.error("Ledger: benannte Sperre %s nicht freigegeben (%s: %s)",
                   _MARIADB_SPERRE, type(e).__name__, e)


def _buchung_schreiben(conn, booked_on, p, k, gross, fee, net, currency,
                       fx_rate, original_amount, doc_ref, note, storno_of):
    if storno_of is not None and conn.execute(
            "SELECT 1 FROM revenue_entries WHERE id=?", (storno_of,)).fetchone() is None:
        raise LedgerError(f"storno_of: Buchung {storno_of} existiert nicht")
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
         fx_rate, original_amount,
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
    from nc import donations as _donations
    try:
        rows = conn.execute(
            "SELECT amount, platform, message FROM overlay_events WHERE kind='donation' "
            # Kein COALESCE(platform,'kick'): eine Zeile ohne Plattform ist
            # Altbestand aus der Zeit, als TikTok-Gifts als 'donation' mit
            # leerer Plattform geschrieben wurden (B138-GELD). Ueberall sonst
            # war das seit B138 behoben — hier blaehte es die Gegenprobe auf
            # und liess eine fehlende Abrechnung wie eine zu viel gebuchte
            # aussehen.
            "AND platform IN " + revenue_sql_in +
            " AND ts >= ? AND ts <= ?",
            (f"{year}-01-01", f"{year}-12-31T23:59:59")).fetchall()
        # v4.2-W178: war float(amount) mit stillem pass — „100 Bits", „$5.00"
        # und Subs ohne Betrag zaehlten 0, die Gegenprobe meldete dann eine
        # zu viel gebuchte Auszahlung, wo in Wahrheit Einnahmen fehlten.
        est = _donations.summe_eur(rows)
    except Exception as e:
        _log.error("Ledger-Gegenprobe: overlay_events nicht lesbar (%s: %s)",
                   type(e).__name__, e)
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
