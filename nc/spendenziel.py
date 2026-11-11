"""nc.spendenziel — v4.2-W173: EIN Spendenziel fuer Website, Overlay, Sendebild und Chat.

Gemeldet am 11.11.: „Die Spendenziele sind noch nicht miteinander verknuepft.
Es ist ja immer dasselbe, egal ob Website, Stream oder Telegram/Discord."

Bis hier gab es drei Ziele, die sich nie trafen:

    Website      DONATION_GOAL_EUR (500)    Stand: DONATION_CURRENT_EUR + NUR
                                            manuell erfasste Spenden, seit Installation
    Overlay      DONATION_GOAL_TARGET (0)   Stand: Kick/Twitch/YouTube/manuell,
    Sendebild    oder das Deck-Feld         aber NUR seit Stream-Start
    /spenden     DONATION_GOAL_EUR          Stand: keiner

Dieselbe Spende auf Kick erschien damit im Overlay, aber nie auf der Website;
eine im Deck eingetragene PayPal-Spende auf der Website, im Overlay aber nur,
solange der Stream lief, in dem sie eingetragen wurde. Und mit der Vorgabe 0
war das Overlay-Ziel auf jeder frischen Installation aus, waehrend die Website
500 € zeigte.

Jetzt gilt EINE Rechnung:

* Ziel: DONATION_GOAL_EUR. DONATION_GOAL_TARGET bleibt als alter Name lesbar,
  wenn DONATION_GOAL_EUR nicht gesetzt ist — bestehende .env-Dateien verlieren
  ihr Ziel nicht.
* Stand: DONATION_CURRENT_EUR (von Hand gepflegter Sockel, z. B. PayPal ohne
  API) plus jede Spende auf einem EIGENEN Kanal (nc.revenue.PLATFORMS: Kick,
  Twitch, YouTube, im Deck erfasst) im Zeitraum. TikTok-Gifts zaehlen nie —
  sie gehen an den getrackten Streamer (CLAUDE.md, „Geld — nicht vermischen").
* Zeitraum: DONATION_PERIOD. „monatlich" (Vorgabe) zaehlt ab dem Ersten des
  laufenden Monats (UTC — so stehen die Zeitstempel in overlay_events),
  alles andere seit Beginn.

Das ist Telemetrie aus Schaetzwerten, keine Buchhaltung: das Steuer-Journal
(nc/ledger.py) bleibt davon getrennt und wird hieraus nie abgeleitet.

Bot-frei; die Datenbank kommt ueber nc.dbwrap.
"""

import os
from datetime import datetime, timezone

from nc import envnum as _envnum
from nc import revenue as _revenue
from nc.donationsdb import parse_eur as _parse_eur


def ziel_eur() -> float:
    """Das Ziel in EUR, 0 = kein Ziel."""
    if (os.getenv("DONATION_GOAL_EUR") or "").strip():
        return max(0.0, _envnum.env_float("DONATION_GOAL_EUR", 500.0))
    alt = _envnum.env_float("DONATION_GOAL_TARGET", 0.0)
    return max(0.0, alt) if alt > 0 else 500.0


def zeitraum() -> str:
    return (os.getenv("DONATION_PERIOD", "monatlich") or "monatlich").strip()


def ist_monatlich(zr=None) -> bool:
    return (zeitraum() if zr is None else zr).lower() in ("monatlich", "monthly", "mensual")


def fenster_start(jetzt=None, zr=None):
    """ISO-Datum des Fensterbeginns, oder None (= seit Beginn).

    Als Datum ohne Uhrzeit: '2026-11-01' ist kleiner als jeder Zeitstempel
    desselben Tages in ISO-Form, der Vergleich in SQL ist damit ein reiner
    Zeichenkettenvergleich und laeuft unter SQLite wie unter MariaDB gleich."""
    seit = None        # None heisst „seit Beginn" — kein Fehlerfall
    if ist_monatlich(zr):
        j = jetzt or datetime.now(timezone.utc)
        seit = "%04d-%02d-01" % (j.year, j.month)
    return seit


def summe(zeilen) -> float:
    """Betraege aus overlay_events-Zeilen addieren; Unlesbares zaehlt 0."""
    s = 0.0
    for r in zeilen:
        v = _parse_eur(r[0] if not hasattr(r, "keys") else r["amount"])
        s += v if v is not None and v > 0 else 0.0
    return round(s, 2)


def eingang(conn, seit) -> float:
    """Spenden auf eigenen Kanaelen im Fenster — aus EINER Abfrage."""
    sql = ("SELECT amount FROM overlay_events WHERE kind='donation' AND platform IN"
           + _revenue.sql_in() + (" AND ts >= ?" if seit else ""))
    return summe(conn.execute(sql, ((seit,) if seit else ())).fetchall())


def stand(conn, jetzt=None) -> dict:
    """Ziel, Stand und Fortschritt — fuer jede Anzeige dieselben Zahlen."""
    zr = zeitraum()
    seit = fenster_start(jetzt, zr)
    ziel = ziel_eur()
    aktuell = round(_envnum.env_float("DONATION_CURRENT_EUR", 0.0) + eingang(conn, seit), 2)
    pct = round(max(0.0, min(100.0, aktuell / ziel * 100.0)), 1) if ziel > 0 else 0.0
    return {
        "ziel_eur": round(ziel, 2), "aktuell_eur": aktuell, "prozent": pct,
        "zeitraum": zr, "seit": seit,
        "label": (os.getenv("DONATION_GOAL_LABEL", "Spendenziel") or "Spendenziel").strip(),
        "zweck": (os.getenv("DONATION_GOAL_PURPOSE", "") or "").strip(),
    }
