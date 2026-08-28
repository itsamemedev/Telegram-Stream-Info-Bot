"""nc.donationsdb — die manuell erfassten Spenden aus der Datenbank lesen.

Warum ein eigenes Modul und nicht nc/donations.py: dort steht die *reine*
Normalisierung (Bits, Coins, Superchats → EUR), ausdrücklich ohne
Datenbank. Diese drei hier lesen `overlay_events` und gehören deshalb neben
nc/recdb.py — Datenzugriff einer Domäne, gebündelt.

Warum vor dem Blueprint (Welle W116, siehe docs/MODULARISIERUNG.md): die
/api/donations-Routen sind ihre Hauptnutzer, aber `manual_total` wird auch von
der Statistik-Route gebraucht. Blieben sie im Monolithen, kostete das drei
Einträge in nc/ctx.py; hier kosten sie null, weil beide Seiten importieren
können.

Verbatim übernommen, inklusive des stillen `except`. Das ist hier Absicht: das
Spendenpanel soll bei einer klemmenden Tabelle leer bleiben statt das ganze
Dashboard mit einem 500er zu quittieren — und die Ursache steht im DB-Log.

**Geldregel aus CLAUDE.md gilt weiter:** das hier sind *manuell erfasste*
Spenden (platform='manual'), bewusst getrennt von Plattform-Trinkgeldern und
von den gebuchten Auszahlungen in nc/ledger.py. Nichts davon darf aus dem
anderen abgeleitet werden.
"""

import logging

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")


def parse_eur(raw):
    """'12,50' / '12.50' / '€12' → float, sonst None. Robust gegen Komma & Symbol."""
    if raw is None:
        return None
    s = str(raw).strip().replace("€", "").replace(" ", "")
    if not s:
        return None
    s = s.replace(",", ".")
    # nur letzte Punkt-Gruppe als Dezimaltrenner (Tausenderpunkte ignorieren)
    if s.count(".") > 1:
        head, _, tail = s.rpartition(".")
        s = head.replace(".", "") + "." + tail
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None


def manual_rows(limit=200):
    """Manuell im Dashboard erfasste Spenden (overlay_events platform='manual').
       Bewusst getrennt von Plattform-Trinkgeldern; werden aus den Plattform-
       Summen gefiltert (kein Doppelzählen)."""
    rows = []
    try:
        with db_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, ts, name, amount, message FROM overlay_events "
                        "WHERE kind='donation' AND platform='manual' "
                        "ORDER BY ts DESC LIMIT ?", (int(limit),))
            for r in cur.fetchall():
                amt = parse_eur(r["amount"])
                rows.append({"id": r["id"], "ts": r["ts"], "note": r["name"] or "",
                             "amount_eur": round(amt, 2) if amt is not None else 0.0,
                             "message": r["message"] or ""})
    except Exception as e:
        log.debug("manual donations read: %s", e)
    return rows


def manual_total():
    """Summe aller manuell erfassten Spenden in EUR (backend-agnostisch)."""
    return round(sum(r["amount_eur"] for r in manual_rows(limit=100000)), 2)
