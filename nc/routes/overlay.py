"""nc.routes.overlay — die Routen unter /api/overlay als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W20: Drei Routen, **null neue Kontext-Eintraege**. Geloest wurde vorweg:

* **nc/revenue.py** — das Einnahmen-Gate (B120). Es lag als Konstantenpaar im
  Monolithen und wurde von money.py bereits ueber einen ctx.cfg-Eintrag
  gespiegelt; jetzt hat es EINE Quelle. TikTok gehoert nicht dazu, und im
  Modul-Kopf steht, warum das keine Geschmacksfrage ist.
* **nc/azraelstate.OVERLAY / REACTION / OVERLAY_SESSION** — die Overlay-
  Konfiguration, die letzte Reaktion und der Nullpunkt der Spendensumme.
  Aliase, wie in W19.

`_overlay_push` bleibt im Bot: es hat zwoelf weitere Aufrufer dort und setzt
den transienten Alert-Zustand des Restreams. Es kommt als **Haken** aus
nc/azraelstate.PUSH — dasselbe Muster wie in W19.

Die Textkuerzung fuers Sendebild (`_ov_clip_text`) ist mit umgezogen: sie hat
ausserhalb dieser Routen keinen Aufrufer mehr.
"""

import logging
import os
import time

from flask import Blueprint, jsonify, request

from nc import azraelstate as _nc_azrael
from nc import channels as _nc_channels
from nc import i18n as _nc_i18n
from nc import revenue as _nc_revenue
from nc import einstellungen as _nc_einst
from nc import fehlertext as _nc_fehlertext
from nc import spendenziel as _nc_spendenziel  # v4.2-W173: ein Ziel fuer alle Anzeigen
from nc import overlaytext as _nc_ovtext       # BH-2: was gehoert in welches Sendebild
from nc import restreamstate as _nc_rsstate    # BH-2: Registry aller aktiven Restreams
from nc.dbwrap import db_conn
from nc.textutil import clean_username
from nc import donations as _nc_donations

_log = logging.getLogger("TikTokBot")

bp = Blueprint("overlay", __name__)


def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _zahl(name, default, lo=None, hi=None):
    """.env bei JEDEM Aufruf lesen, nie als Modul-Konstante einfrieren
       (CLAUDE.md: .env laedt teils erst nach den ersten Imports)."""
    try:
        v = int((os.getenv(name, "") or "").strip() or default)
    except (TypeError, ValueError):
        v = default
    if lo is not None:
        v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v


def _ov_clip_text(t, maxlen=None):
    """Text auf Overlay-Länge kürzen — an der letzten Satzgrenze, sonst hart."""
    t = " ".join(str(t or "").split())
    n = int(maxlen or _zahl("AZRAEL_OVERLAY_MAXLEN", 400, 60, 600))
    if len(t) <= n:
        return t
    cut = t[:n]
    for sep in (". ", "! ", "? ", "; "):
        p = cut.rfind(sep)
        if p > n * 0.55:
            return cut[:p + 1]
    p = cut.rfind(" ")
    return (cut[:p] if p > n * 0.6 else cut).rstrip(" ,;:") + " …"


def _azrael_overlay_state(nutzer=None):
    """Zustand des AZRAEL-Avatars fürs Overlay: an/aus, ob gerade eine Reaktion
       live ist (active), und der Reaktionstext. 'active' verfällt nach
       AZRAEL_REACTION_HOLD_S — der Avatar leuchtet nur kurz beim Reagieren auf.

       BH-2: mit `nutzer` (Seite mit ?rid=) zaehlt nur eine Reaktion auf DIESEN
       Quellnutzer — sonst sprach AZRAEL im Sendebild von A ueber B.
       nutzer=None ist die OBS-Seite ohne rid: alles wie bisher."""
    if not _nc_azrael.OVERLAY.get("azrael_show"):
        return {"show": False, "active": False, "text": "", "statement": ""}
    r = dict(_nc_azrael.REACTION)
    halt = _zahl("AZRAEL_REACTION_HOLD_S", 18, 5, 120)
    active = (bool(r.get("text")) and (time.time() - r.get("ts", 0)) < halt
              and _nc_ovtext.gehoert_zu(r.get("source"), nutzer))
    return {"show": True, "active": active,
            # V37-B101: gekappt fürs Sendebild (Textwand vermeiden)
            "text": _ov_clip_text(r.get("text", "")) if active else "",
            "text_full": r.get("text", "") if active else "",
            "statement": _ov_clip_text(r.get("statement", ""), 120) if active else "",
            "audio": r.get("audio", "") if active else "",
            "source": r.get("source", "") if active else ""}


def _bilanz(zeilen, by_platform):
    """Spenden und Follows je Plattform ab Sende-Start (V37-OVMP).

    v4.2-W173 herausgeloest: api_overlay_state lag mit dem gemeinsamen
    Spendenziel ueber 100 Zeilen. Betraege liest nc.donations.zeile_eur —
    dieselbe Lesart wie das Spendenziel, statt einer zweiten eigenen (bis
    v4.2-W178 parse_eur: Bits, Dollar und Subs zaehlten dort 0 €)."""
    _nc_donations.kurse_aus_env()
    for r in zeilen:
        p = (r["platform"] or "kick")
        if p not in by_platform:
            by_platform[p] = {"donations": 0, "amount": 0.0, "follows": 0}
        if r["kind"] == "donation":
            a = _nc_donations.zeile_eur(r)
            by_platform[p]["donations"] += 1
            by_platform[p]["amount"] = round(by_platform[p]["amount"] + a, 2)
        else:
            by_platform[p]["follows"] += 1


_CHATBILD_SEITE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               os.pardir, os.pardir, "templates", "chatbild.html")


@bp.route("/overlay/chat")
def overlay_chatbild():
    """v5.9-W205: der Chat-Kasten des Studio-Sendebilds, gezeichnet von Chromium.

    Roh ausgeliefert (kein Jinja: CSS und JS tragen geschweifte Klammern).
    Der Bot ruft sie ueber 127.0.0.1 — Loopback braucht keinen Token. Fuer
    OBS ist sie nicht gedacht und steht deshalb NICHT bei den Ausnahmen."""
    try:
        with open(_CHATBILD_SEITE, "r", encoding="utf-8") as f:
            return f.read(), 200, {"Content-Type": "text/html; charset=utf-8",
                                   "Cache-Control": "no-store"}
    except OSError as e:
        return _t("Chat-Kasten fehlt: ") + _nc_fehlertext.nach_aussen(e, "overlay_chatbild"), 404


@bp.route("/overlay/chat.json")
def overlay_chatbild_daten():
    """Die juengsten Chat-Eintraege fuer EIN Sendebild (?user=<TikTok-Quelle>).

    Ungefiltert, also MIT Emoji — der Text-Chat fuer drawtext nimmt sie heraus
    (nc/schriftzeichen.py), hier zeichnet Chromium sie farbig."""
    nutzer = clean_username(request.args.get("user") or "")
    return jsonify(ok=True, zeilen=_nc_channels.chat_eintraege(source_user=nutzer or None))


def _quelle_fuer(rid):
    """BH-2: Quellnutzer und Label des Restreams `rid` aus der Registry, sonst None.

    Die Registry fuehrt den rid als Zahl, die Anfrage bringt Text. Ein
    unbekannter rid (Restream gerade beendet, Tippfehler) ist KEIN Grund, das
    Sendebild eines anderen zu zeigen — der Aufrufer filtert dann auf
    „kanalweit" (leerer Nutzer)."""
    alle = _nc_rsstate.ACTIVE_ALL
    info = alle.get(rid) or (alle.get(int(rid)) if rid.isdigit() else None)
    return ({"user": info.get("user") or "", "label": info.get("label") or ""}
            if info else None)


@bp.route("/api/overlay/state")
def api_overlay_state():
    """Live-Zustand fürs Overlay: Name, Ziel, letzter Follower, Donations, Moderator.

    BH-2: ?rid=<rid> ist die Seite EINES Restreams (der Bot oeffnet sie je rid
    in Chromium, bot._htmlov_url). Dann kommt `quelle` dazu, und AZRAELs
    Reaktion zaehlt nur, wenn sie diesem Quellnutzer gilt. Kanalweit bleiben,
    mit Grund in nc/overlaytext.py: Sendername (ein Konfigwert), Spendenziel,
    Donations und Follower der EIGENEN Kanaele, die Zeile im eigenen Kick-Chat.
    Ohne rid (OBS) bleibt alles wie bisher."""
    rid = (request.args.get("rid") or "").strip()
    quelle = _quelle_fuer(rid) if rid else None
    nutzer = ((quelle or {}).get("user") or "") if rid else None
    latest_follower = None
    followers = []
    donations = []
    ziel = None
    by_platform = {p: {"donations": 0, "amount": 0.0, "follows": 0}
                   for p in _nc_revenue.OV_PLATFORMS}
    # V37-OVMP-FIX: Zaehler-Nullpunkt ist der Sende-Start. Ohne ihn summierte
    # das Overlay alles seit der Installation und sprang beim Stream-Start nie
    # auf 0 zurueck.
    _sess = _nc_azrael.OVERLAY_SESSION.get("start")
    _and_sess = " AND ts >= ?" if _sess else ""
    _sp = (_sess,) if _sess else ()

    try:
        with db_conn() as conn:
            fr = conn.execute("SELECT name, ts, platform FROM overlay_events "
                              "WHERE kind='follow'" + _and_sess +
                              " ORDER BY id DESC LIMIT 1", _sp).fetchone()
            if fr:
                latest_follower = {"name": fr["name"], "ts": (fr["ts"] or "")[:19],
                                   "platform": fr["platform"] or "kick"}
            # V37-OVMP: letzte Follower ALLER Plattformen (fürs Ticker-Panel)
            frows = conn.execute("SELECT name, ts, platform FROM overlay_events "
                                 "WHERE kind='follow'" + _and_sess +
                                 " ORDER BY id DESC LIMIT 8", _sp).fetchall()
            followers = [{"name": r["name"], "ts": (r["ts"] or "")[:19],
                          "platform": r["platform"] or "kick"} for r in frows]
            drows = conn.execute("SELECT name, amount, message, ts, platform FROM overlay_events "
                                 "WHERE kind='donation' "
                                 # B120: nur eigene Kanaele (siehe nc/revenue.py)
                                 "AND platform IN" + _nc_revenue.sql_in() + " " + _and_sess +
                                 " ORDER BY id DESC LIMIT 10", _sp).fetchall()
            donations = [{"name": r["name"], "amount": r["amount"], "message": r["message"],
                          "ts": (r["ts"] or "")[:19],
                          "platform": r["platform"] or "kick"} for r in drows]
            # Ziel-Fortschritt + Plattform-Bilanz über ALLE Session-Events
            # (nicht nur die letzten 10) — ab Sende-Start.
            allrows = conn.execute("SELECT kind, amount, platform, message FROM overlay_events "
                                   "WHERE (kind='follow' OR (kind='donation' AND "
                                   "platform IN" + _nc_revenue.sql_in() + ")) " + _and_sess,
                                   _sp).fetchall()
            _bilanz(allrows, by_platform)
            # v4.2-W173: das Ziel kommt aus nc/spendenziel.py — dasselbe wie auf
            # Website, Sendebild und /spenden. Die Bilanz je Plattform oben zaehlt
            # weiter ab Sende-Start; das ist die Sendung, nicht das Ziel.
            ziel = _nc_spendenziel.stand(conn)
    except Exception as e:
        # War `pass`: das Overlay zeigte dann 0 € und leere Ticker, als waere
        # nichts passiert. Die Antwort bleibt (OBS darf nicht leer werden).
        _log.error("overlay/state: Datenbank nicht lesbar (%s: %s) — das Overlay "
                   "zeigt bis dahin kein Spendenziel.", type(e).__name__, e)

    ov = _nc_azrael.OVERLAY
    mod = _nc_channels.KICK_MOD["obj"]
    last_spoken = getattr(mod, "last_spoken", {}) or {}
    spoken_age = time.monotonic() - last_spoken.get("ts", 0)
    return jsonify(
        ok=True,
        title=ov.get("title", ""),
        goal=({"current": ziel["aktuell_eur"], "target": ziel["ziel_eur"],
               "label": ziel["label"], "purpose": ziel["zweck"],
               "period": ziel["zeitraum"], "pct": ziel["prozent"]} if ziel else {}),
        latest_follower=latest_follower,
        followers=followers,             # V37-OVMP: Multi-Plattform-Ticker
        donations=donations,
        by_platform=by_platform,         # V37-OVMP: Bilanz je Plattform
        session_start=_sess,             # V37-OVMP-FIX: Zähler-Nullpunkt (Sende-Start)
        test=_test_ereignis(),           # GELD-1: nur anzeigen, in keiner Summe
        mod={
            "running": bool(getattr(mod, "running", False)),
            "connected": (getattr(mod, "stats", {}) or {}).get("connected"),
            "speaking": spoken_age < 7,
            "last_line": last_spoken.get("text", "") if spoken_age < 30 else "",
            "stats": getattr(mod, "stats", {}) or {},
        },
        azrael=_azrael_overlay_state(nutzer),
        quelle=quelle,                   # BH-2: nur mit ?rid= gesetzt
        voice={
            "enabled": bool(ov.get("voice_enabled")),
            "engine": ov.get("voice_engine", "browser"),
            "lang": ov.get("voice_lang", "de-DE"),
            "name": ov.get("voice_name", ""),
            "rate": ov.get("voice_rate", 1.0),
            "pitch": ov.get("voice_pitch", 1.0),
            "volume": ov.get("voice_volume", 1.0),
            "reactions": bool(ov.get("voice_reactions", True)),
            "mod": bool(ov.get("voice_mod", False)),
        })


# GELD-1: Plattformen, von denen eine Spende ueber diese Route kommen darf —
# Einnahme (nc/revenue.PLATFORMS) UND im Overlay darstellbar. "manual" faellt
# heraus: manuelle Spenden erfasst /api/donations/add, hier wuerde
# _overlay_push sie zu Kick machen.
_SPENDE_VON = tuple(p for p in _nc_revenue.PLATFORMS if p in _nc_revenue.OV_PLATFORMS)

# GELD-1: das letzte Test-Ereignis aus dem Deck. Es wird nur angezeigt und
# NIE in overlay_events gespeichert — dort waere eine Test-Spende Einnahme.
_TEST = {"id": 0, "ts": 0.0, "ereignis": None}
_TEST_SICHTBAR_S = 30.0


def _test_ereignis():
    """Das Test-Ereignis fuer /api/overlay/state, solange es frisch ist —
    sonst None: kein Test gedrueckt, das ist der Normalfall, kein Fehler."""
    frisch = bool(_TEST["ereignis"]) and time.monotonic() - _TEST["ts"] <= _TEST_SICHTBAR_S
    return dict(_TEST["ereignis"], id=_TEST["id"]) if frisch else None


@bp.route("/api/overlay/event", methods=["POST"])
def api_overlay_event():
    """Event pushen (Follower/Donation) — für StreamElements-Webhook o.ä. oder manuell.
       Body: {kind: 'follow'|'donation', name, amount?, message?, platform?, test?}

       GELD-1: eine echte Spende braucht eine ausdrueckliche Erloesplattform.
       Bis hier wurde jede ohne Angabe eine Kick-Spende, und der Test-Knopf des
       Decks buchte so 5 € erfundene Einnahme. test=true zeigt nur an."""
    d = request.get_json(silent=True) or {}
    kind = (d.get("kind") or "").strip()
    if kind not in ("follow", "donation"):
        return jsonify(ok=False, error=_t("kind muss 'follow' oder 'donation' sein")), 400
    test = d.get("test") in (True, 1, "1", "true")
    platform = str(d.get("platform") or "").strip().lower()
    if kind == "donation" and not test and platform not in _SPENDE_VON:
        return jsonify(ok=False, error=_t(
            "Spende ohne gültige Plattform — platform muss kick, twitch oder youtube "
            "sein. Manuelle Spenden erfasst das Deck unter Spenden.")), 400
    push = _nc_azrael.haken("push")
    if push is None:
        return jsonify(ok=False, error=_t("Bot startet noch — gleich erneut"),
                       transient=True), 503
    name, amount, message = d.get("name") or "?", d.get("amount"), d.get("message")
    platform = platform or "kick"      # Follows: nur das Badge, kein Geld
    if test:
        _TEST.update(id=_TEST["id"] + 1, ts=time.monotonic(), ereignis={
            "kind": kind, "name": str(name)[:120], "platform": platform,
            "amount": (str(amount)[:40] if amount is not None else None),
            "message": str(message or "")[:200]})
    push(kind, name, amount, message, platform=platform, test=test)
    return jsonify(ok=True, test=test, gespeichert=not test)


@bp.route("/api/overlay/config", methods=["POST"])
def api_overlay_config():
    """Sendername + Spendenziel setzen (persistiert über Laufzeit)."""
    d = request.get_json(silent=True) or {}
    ov = _nc_azrael.OVERLAY
    if "title" in d: ov["title"] = (d["title"] or "Azrael Sentinel")[:60]
    if "azrael_show" in d: ov["azrael_show"] = bool(d["azrael_show"])
    if "voice_enabled" in d: ov["voice_enabled"] = bool(d["voice_enabled"])
    if "voice_engine" in d: ov["voice_engine"] = (d["voice_engine"] or "browser").strip().lower()
    if "piper_model" in d: ov["piper_model"] = (d["piper_model"] or "").strip()[:300]
    if "piper_length" in d:
        try: ov["piper_length"] = max(0.5, min(2.0, float(d["piper_length"])))
        except (TypeError, ValueError): pass
    if "voice_lang" in d: ov["voice_lang"] = (d["voice_lang"] or "de-DE")[:20]
    if "voice_name" in d: ov["voice_name"] = (d["voice_name"] or "")[:80]
    if "voice_reactions" in d: ov["voice_reactions"] = bool(d["voice_reactions"])
    if "voice_mod" in d: ov["voice_mod"] = bool(d["voice_mod"])
    for _k, _lo, _hi in (("voice_rate", 0.5, 2.0), ("voice_pitch", 0.0, 2.0),
                         ("voice_volume", 0.0, 1.0)):
        if _k in d:
            try: ov[_k] = max(_lo, min(_hi, float(d[_k])))
            except (TypeError, ValueError): pass
    try:
        _ziel_speichern(d)
    except _nc_einst.Abgelehnt as e:
        _log.warning("Overlay: Spendenziel abgelehnt — %s", e)
        return jsonify(ok=False, error=_nc_i18n.t(e.grund)), 400
    except ValueError:
        return jsonify(ok=False, error=_nc_i18n.t("Das Ziel muss eine Zahl sein.")), 400
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_overlay_config")), 503
    return jsonify(ok=True, overlay=ov)


# v4.2-W173: die Ziel-Felder des Overlay-Formulars schreiben das EINE Ziel —
# ueber nc/einstellungen.py, also in dieselbe Tabelle wie der Reiter
# „Einstellungen", und damit sofort fuer Website, Sendebild und /spenden.
# Bis hier lag das Overlay-Ziel nur im Speicher und war nach einem Neustart weg.
_ZIEL_FELDER = (("goal_target", "DONATION_GOAL_EUR", 12),
                ("goal_label", "DONATION_GOAL_LABEL", 60),
                ("goal_purpose", "DONATION_GOAL_PURPOSE", 160))


def _ziel_speichern(d):
    """Leere oder fehlende Felder bleiben unveraendert: das Formular wird nicht
    vorbefuellt, und wer nur den Sendernamen aendert, schickte sonst Ziel 0
    und ein leeres Label — fuer Website und Chat gleich mit."""
    for feld, env, laenge in _ZIEL_FELDER:
        wert = "" if d.get(feld) is None else str(d.get(feld)).strip()[:laenge]
        if not wert:
            continue
        if feld == "goal_target":
            wert = "%g" % max(0.0, float(wert.replace(",", ".")))   # 0 = kein Ziel
        _nc_einst.setzen(env, wert, von="deck-overlay")
