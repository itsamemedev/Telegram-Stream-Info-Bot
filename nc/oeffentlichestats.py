"""nc.oeffentlichestats — die oeffentlichen Metriken der Website (stats.json), bot-frei.

v5.6-W197 aus bot.py geloest (173 Zeilen). Der Erzeuger hing nur an zwei
Namen des Monolithen — der Fassung und der Schleifen-Meldung —, alles andere
liest er ohnehin aus nc/ und der Datenbank. Beide kommen per configure().

DIE REGEL bleibt die aus v4.0: NIE Aufnahmen, nur Live-Begleitung und
Moderation. `live_7d` zaehlt, wie viele getrackte Creator je Tag live waren.
"""

import logging
import time as _time_mod
from datetime import datetime, timedelta, timezone

from nc import crypto as _nc_crypto
from nc import meldetakt as _nc_meldetakt
from nc import news as _nc_news
from nc import qrsvg as _nc_qrsvg
from nc import spendeninfo as _nc_spendeninfo
from nc import spendenziel as _nc_spendenziel
from nc import usage as _nc_usage
from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")


def _loop_fehler_ersatz(name, exc):
    log.error("%s: %s: %s", name, type(exc).__name__, exc)


_KONF = {"version": "?", "loop_fehler": _loop_fehler_ersatz}


def _teil_melden(teil, exc):
    """Ein Teil der oeffentlichen Zahlen fiel aus — die Seite zeigt dann eine
    leere Reihe oder eine Null.

    v5.6-W197: diese Auffaenge waren still (`except Exception: pass`), solange
    sie im Monolithen standen. Eine Null auf der Website sah damit genauso aus
    wie „heute war niemand live", und im Log stand nichts. Die Schleife laeuft
    alle fuenf Minuten — deshalb ueber nc.meldetakt: erste Meldung sofort, ein
    neuer Grund sofort, sonst hoechstens alle 15 Minuten."""
    laut, weg = _nc_meldetakt.melden("oeffentliche-stats", teil + ":" + type(exc).__name__,
                                     _time_mod.monotonic())
    if laut:
        log.warning("Oeffentliche Zahlen (stats.json): Teil %s fiel aus — %s: %s. Die "
                    "Website zeigt dort eine Null bzw. leere Reihe.%s", teil,
                    type(exc).__name__, exc, _nc_meldetakt.zusatz(weg))


def _loop_fehler(name, exc):
    """Die Schleifen-Meldung des Bots (erste sofort auf error, dann gedrosselt) —
    per configure() hereingereicht, ohne configure() der eigene Logger."""
    _KONF["loop_fehler"](name, exc)


def configure(*, version=None, loop_fehler=None):
    """Fassung und Schleifen-Meldung des Bots. Ohne configure() meldet das
    Modul ueber den eigenen Logger — nie still."""
    if version is not None:
        _KONF["version"] = version
    if loop_fehler is not None:
        _KONF["loop_fehler"] = loop_fehler


def public_stats() -> dict:
    """v4.0: SICHERE oeffentliche Metriken fuer die Website (stats.json).
       NIE Aufnahmen — nur Live-Begleitung/Moderation. live_7d = wie viele
       getrackte Creator je Tag live waren (intern aus dem Live-Erkennungs-Log,
       oeffentlich als 'live' formuliert)."""
    facts = _nc_news.collect_facts()
    stats = {
        "version": _KONF["version"],
        "generated_at": _time_mod.time(),
        "tracked": facts.get("tracked", 0),
        "live_today": facts.get("live_today_count", 0),
        "platforms": facts.get("platforms", []),
        "agents_active": facts.get("agents_active", 0),
        "kg_facts": facts.get("kg_facts", 0),
        "live_7d": [],
    }
    try:
        with db_conn() as c:
            days = []
            for i in range(6, -1, -1):
                d0 = (datetime.now(timezone.utc) - timedelta(days=i)).date()
                lo = datetime(d0.year, d0.month, d0.day, tzinfo=timezone.utc).isoformat()
                hi = (datetime(d0.year, d0.month, d0.day, tzinfo=timezone.utc)
                      + timedelta(days=1)).isoformat()
                n = c.execute(
                    "SELECT COUNT(DISTINCT username) AS n FROM recording_attempts "
                    "WHERE started_at >= ? AND started_at < ?", (lo, hi)).fetchone()["n"]
                days.append({"day": d0.isoformat(), "live": int(n or 0)})
            stats["live_7d"] = days
    except Exception as e:
        _teil_melden("live_7d", e)
    # v4.0: abgeleitete + aggregierte Zusatz-Metriken (weiter aufnahmefrei).
    _lv = [d.get("live", 0) for d in stats.get("live_7d", [])]
    stats["total_live_7d"] = sum(_lv)
    stats["peak_live"] = max(_lv) if _lv else 0
    stats["moderation_7d"] = 0
    try:
        with db_conn() as c:
            _cut7 = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            stats["moderation_7d"] = int(c.execute(
                "SELECT COUNT(*) AS n FROM kick_mod_log WHERE ts >= ?",
                (_cut7,)).fetchone()["n"] or 0)
    except Exception as e:
        _teil_melden("moderation_7d", e)
    # v4.0-W4: LIVE-Agentenliste (Name + aktiv) für die Website-Flotte.
    # v4.0-W74: agents_known trennt „Brain gerade nicht erreichbar" (Liste leer,
    # weil die Bridge im schreibenden Prozess nicht hochkam oder status() warf)
    # von „Brain sagt 0 aktiv". Ohne dieses Flag zeigte die Website stur
    # „0 von 12 aktiv", obwohl in Wahrheit nur der Snapshot leer war.
    stats["agents"] = []
    stats["agents_known"] = False
    try:
        from brain import get_brain
        _b = get_brain()
        _fleet = (_b.agents.status() or []) if _b else []
        for _a in _fleet:
            stats["agents"].append({"name": _a.get("name", ""),
                                    "active": bool(_a.get("enabled", False))})
        stats["agents_known"] = bool(_fleet)
    except Exception as e:
        # agents_known bleibt False: die Website sagt dann „Status nicht
        # verfuegbar" statt „0 aktiv" (W74) — und das Log sagt, warum.
        _teil_melden("agents", e)
    stats["agents_total"] = len(stats["agents"])
    stats["agents_active"] = sum(1 for _a in stats["agents"] if _a.get("active")) or stats.get("agents_active", 0)
    # v4.0-W4: Moderations-Aktivität je Tag (7 Tage) für einen zweiten Chart.
    stats["mod_7d"] = []
    try:
        with db_conn() as c:
            _md = []
            for i in range(6, -1, -1):
                d0 = (datetime.now(timezone.utc) - timedelta(days=i)).date()
                lo = datetime(d0.year, d0.month, d0.day, tzinfo=timezone.utc).isoformat()
                hi = (datetime(d0.year, d0.month, d0.day, tzinfo=timezone.utc)
                      + timedelta(days=1)).isoformat()
                n = c.execute(
                    "SELECT COUNT(*) AS n FROM kick_mod_log WHERE ts >= ? AND ts < ? "
                    "AND kind IN ('timeout','ban','flag','delete','warn')", (lo, hi)).fetchone()["n"]
                _md.append({"day": d0.isoformat(), "n": int(n or 0)})
            stats["mod_7d"] = _md
    except Exception as e:
        _teil_melden("mod_7d", e)

    # v4.0-W92: LLM-Token-/Kostenverbrauch (aus nc.usage) — für die 3D-Statistik.
    try:
        stats["usage"] = _nc_usage.snapshot()
    except Exception as e:
        _teil_melden("usage", e)
        stats["usage"] = {}

    # v4.0-W92: Live-Spendenpanel — PayPal-Ziel. Der aktuelle Betrag ist
    # betreiber-gepflegt (DONATION_CURRENT_EUR): PayPal bietet keine öffentliche
    # Live-Summe ohne API/IPN. Ziel + Adresse sind per env übersteuerbar.
    try:
        # v4.2-W173: Ziel und Stand aus nc/spendenziel.py — dieselben Zahlen wie
        # Overlay, Sendebild und /spenden. Bis W172 zaehlte die Website nur
        # manuell erfasste Spenden, seit Installation; eine Kick-Spende kam
        # hier nie an.
        with db_conn() as _conn:
            _ziel = _nc_spendenziel.stand(_conn)
        # v4.2-W172: eine Quelle fuer Website, Deck und /spenden.
        _pp = _nc_spendeninfo.paypal()
        _pp_url = _nc_spendeninfo.paypal_url(_pp)
        stats["donation"] = {
            "goal_eur": _ziel["ziel_eur"],
            "current_eur": _ziel["aktuell_eur"],
            "pct": _ziel["prozent"],
            "paypal": _pp,
            "paypal_url": _pp_url,
            "paypal_qr": _nc_qrsvg.qr_svg(_pp_url) if _pp_url else "",
            "period": _ziel["zeitraum"],
            "label": _ziel["label"],
            "purpose": _ziel["zweck"],
            "currency": "EUR",
        }
    except Exception as e:
        # War ein stiller Auffang: der Block verschwand von der Website, und
        # „nichts konfiguriert" sah aus wie „Datenbank weg" (W99).
        _loop_fehler("spendenziel-website", e)
        stats["donation"] = {}

    # v4.0-W94: Krypto-Spenden — Adressen aus env, BTC-Empfang best-effort live.
    try:
        stats["crypto"] = _nc_crypto.snapshot(fetch_live=True)
    except Exception as e:
        # v4.2-W99: war ein stiller Auffang. Eine leere Adressliste ist auf
        # der oeffentlichen Seite nicht von "nichts konfiguriert" zu
        # unterscheiden — der Spendenblock verschwindet in beiden Faellen —,
        # und im Log stand dazu keine Zeile. Gedrosselt, weil die Schleife
        # alle fuenf Minuten laeuft.
        stats["crypto"] = {"addresses": [], "grund": "fehler"}
        laut, unterdrueckt = _nc_meldetakt.melden(
            "crypto-snapshot", type(e).__name__, _time_mod.monotonic())
        if laut:
            log.error("Krypto-Spendenadressen nicht ermittelbar: %s: %s — der "
                      "Spendenblock auf der oeffentlichen Seite sagt bis dahin "
                      "'derzeit nicht abrufbar'.%s",
                      type(e).__name__, e, _nc_meldetakt.zusatz(unterdrueckt))
    else:
        _nc_meldetakt.zuruecksetzen("crypto-snapshot")
        # Der haeufigere Fall ist nicht der Fehler, sondern die leere .env.
        # Auch das gehoert gesagt — einmal und gedrosselt, mit den NAMEN, die
        # gesucht wurden. Ein "keine Adressen" ohne die Namen ist dieselbe Art
        # Auskunft wie ein blankes "HTTP 403".
        if not stats["crypto"].get("addresses"):
            laut, unterdrueckt = _nc_meldetakt.melden(
                "crypto-leer", "keine_adresse", _time_mod.monotonic())
            if laut:
                log.warning(
                    "Keine Krypto-Spendenadresse gesetzt — der Spendenblock auf "
                    "der oeffentlichen Seite steht (v4.2-W101), nennt aber nur "
                    "PayPal. Gesucht wird in der .env nach: %s%s",
                    ", ".join(_nc_crypto.erwartete_namen()),
                    _nc_meldetakt.zusatz(unterdrueckt))
        else:
            _nc_meldetakt.zuruecksetzen("crypto-leer")
            # v4.2-W101: der dritte Zustand, der bis hierher gar keinen
            # hatte. Zwei von sechs Wallets gesetzt sah im Log genauso aus
            # wie alle sechs — und die oeffentliche Seite zeigt nur, was da
            # ist, nie was fehlt. Einmal auf INFO mit den fehlenden Namen;
            # das ist kein Fehler, sondern eine Lage, die man kennen will.
            _fehlend = stats["crypto"].get("fehlend") or []
            if _fehlend:
                laut, unterdrueckt = _nc_meldetakt.melden(
                    "crypto-teil", ",".join(_fehlend), _time_mod.monotonic())
                if laut:
                    log.info(
                        "Krypto-Spenden: %d von %d Adressen gesetzt. Ohne "
                        "Eintrag in der .env: %s%s",
                        len(stats["crypto"].get("addresses") or []),
                        len(_nc_crypto.erwartete_namen()),
                        ", ".join(_fehlend),
                        _nc_meldetakt.zusatz(unterdrueckt))
            else:
                _nc_meldetakt.zuruecksetzen("crypto-teil")
    return stats
