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

import os
import time

from flask import Blueprint, jsonify, request

from nc import azraelstate as _nc_azrael
from nc import channels as _nc_channels
from nc import i18n as _nc_i18n
from nc import revenue as _nc_revenue
from nc.dbwrap import db_conn

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


def _azrael_overlay_state():
    """Zustand des AZRAEL-Avatars fürs Overlay: an/aus, ob gerade eine Reaktion
       live ist (active), und der Reaktionstext. 'active' verfällt nach
       AZRAEL_REACTION_HOLD_S — der Avatar leuchtet nur kurz beim Reagieren auf."""
    if not _nc_azrael.OVERLAY.get("azrael_show"):
        return {"show": False, "active": False, "text": "", "statement": ""}
    r = _nc_azrael.REACTION
    halt = _zahl("AZRAEL_REACTION_HOLD_S", 18, 5, 120)
    active = bool(r.get("text")) and (time.time() - r.get("ts", 0)) < halt
    return {"show": True, "active": active,
            # V37-B101: gekappt fürs Sendebild (Textwand vermeiden)
            "text": _ov_clip_text(r.get("text", "")) if active else "",
            "text_full": r.get("text", "") if active else "",
            "statement": _ov_clip_text(r.get("statement", ""), 120) if active else "",
            "audio": r.get("audio", "") if active else "",
            "source": r.get("source", "") if active else ""}


@bp.route("/api/overlay/state")
def api_overlay_state():
    """Live-Zustand fürs Overlay: Name, Ziel, letzter Follower, Donations, Moderator."""
    latest_follower = None
    followers = []
    donations = []
    goal_current = 0.0
    by_platform = {p: {"donations": 0, "amount": 0.0, "follows": 0}
                   for p in _nc_revenue.OV_PLATFORMS}
    # V37-OVMP-FIX: Zaehler-Nullpunkt ist der Sende-Start. Ohne ihn summierte
    # das Overlay alles seit der Installation und sprang beim Stream-Start nie
    # auf 0 zurueck.
    _sess = _nc_azrael.OVERLAY_SESSION.get("start")
    _and_sess = " AND ts >= ?" if _sess else ""
    _sp = (_sess,) if _sess else ()

    def _amt(v):
        try:
            return float(str(v).replace(",", ".").replace("€", "").strip())
        except (TypeError, ValueError):
            return 0.0

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
            allrows = conn.execute("SELECT kind, amount, platform FROM overlay_events "
                                   "WHERE (kind='follow' OR (kind='donation' AND "
                                   "platform IN" + _nc_revenue.sql_in() + ")) " + _and_sess,
                                   _sp).fetchall()
            for r in allrows:
                p = (r["platform"] or "kick")
                if p not in by_platform:
                    by_platform[p] = {"donations": 0, "amount": 0.0, "follows": 0}
                if r["kind"] == "donation":
                    a = _amt(r["amount"])
                    goal_current += a
                    by_platform[p]["donations"] += 1
                    by_platform[p]["amount"] = round(by_platform[p]["amount"] + a, 2)
                else:
                    by_platform[p]["follows"] += 1
    except Exception:
        pass

    ov = _nc_azrael.OVERLAY
    mod = _nc_channels.KICK_MOD["obj"]
    last_spoken = getattr(mod, "last_spoken", {}) or {}
    spoken_age = time.monotonic() - last_spoken.get("ts", 0)
    return jsonify(
        ok=True,
        title=ov.get("title", ""),
        goal={"current": round(goal_current, 2), "target": ov.get("goal_target", 0),
              "label": ov.get("goal_label", ""), "purpose": ov.get("goal_purpose", "")},
        latest_follower=latest_follower,
        followers=followers,             # V37-OVMP: Multi-Plattform-Ticker
        donations=donations,
        by_platform=by_platform,         # V37-OVMP: Bilanz je Plattform
        session_start=_sess,             # V37-OVMP-FIX: Zähler-Nullpunkt (Sende-Start)
        mod={
            "running": bool(getattr(mod, "running", False)),
            "connected": (getattr(mod, "stats", {}) or {}).get("connected"),
            "speaking": spoken_age < 7,
            "last_line": last_spoken.get("text", "") if spoken_age < 30 else "",
            "stats": getattr(mod, "stats", {}) or {},
        },
        azrael=_azrael_overlay_state(),
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


@bp.route("/api/overlay/event", methods=["POST"])
def api_overlay_event():
    """Event pushen (Follower/Donation) — für StreamElements-Webhook o.ä. oder manuell.
       Body: {kind: 'follow'|'donation', name, amount?, message?}"""
    d = request.get_json(silent=True) or {}
    kind = (d.get("kind") or "").strip()
    if kind not in ("follow", "donation"):
        return jsonify(ok=False, error=_t("kind muss 'follow' oder 'donation' sein")), 400
    push = _nc_azrael.haken("push")
    if push is None:
        return jsonify(ok=False, error=_t("Bot startet noch — gleich erneut"),
                       transient=True), 503
    push(kind, d.get("name") or "?", d.get("amount"), d.get("message"),
         platform=(d.get("platform") or "kick"))
    return jsonify(ok=True)


@bp.route("/api/overlay/config", methods=["POST"])
def api_overlay_config():
    """Sendername + Spendenziel setzen (persistiert über Laufzeit)."""
    d = request.get_json(silent=True) or {}
    ov = _nc_azrael.OVERLAY
    if "title" in d: ov["title"] = (d["title"] or "Azrael Sentinel")[:60]
    if "goal_label" in d: ov["goal_label"] = (d["goal_label"] or "")[:60]
    if "goal_purpose" in d: ov["goal_purpose"] = (d["goal_purpose"] or "")[:160]
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
    if "goal_target" in d:
        try: ov["goal_target"] = max(0, int(d["goal_target"]))
        except (TypeError, ValueError): pass
    return jsonify(ok=True, overlay=ov)
