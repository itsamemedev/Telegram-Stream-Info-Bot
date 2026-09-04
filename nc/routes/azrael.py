"""nc.routes.azrael — die achtzehn Routen unter /api/azrael als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W19: Die groesste Gruppe, die noch im Monolithen stand — und **null neue
Kontext-Eintraege**. Roh haette sie 35 gekostet, bei 24 von vertraglich 25
belegten Plaetzen. Vorweg geloest, in der Reihenfolge aus W117:

* **nc/azraelstate.py** — die acht Zustands-Container (Overlay-Konfiguration,
  Stream-Kontext, letzte Reaktion, Aufruf-Budget, Pause-Schalter,
  Live-Transkript, laufende Worker, Agenten-Rollen) plus die Personas auf
  Platte. Alles Aliase: bot.py bindet keinen dieser Namen je neu.
* **nc/piper_voices.py** — Suchorte, Scannen samt Cache, Verfuegbarkeit.
* **nc/whispercfg.py** — Modellname und geladenes Modell als Register. Der
  Laufzeit-Umschalter tat das im Monolithen mit `global`; hier waere das der
  Namensraum DIESER Datei gewesen, die Route haette Erfolg gemeldet und der
  naechste Transkript-Lauf das alte Modell benutzt.

Drei Dinge kann nur der Bot: eine Coroutine auf seinem Loop sprechen lassen
(_piper_say), den zentralen KI-Aufruf fahren (azrael_chat) und sagen, was
NIGHTCRAWLER gerade tut (_azrael_live_state). Sie kommen als **Haken** aus den
Registern, nicht aus dem Kontext — siehe nc/azraelstate.py, wo auch steht,
warum das Kopplung ist und trotzdem der richtige Ort.

Die .env-Werte werden bei JEDEM Aufruf gelesen statt als Modul-Konstante
eingefroren (CLAUDE.md: .env laedt teils erst nach den ersten Imports).

Benutzertexte laufen durch `_nc_i18n.t(...)` — an der Quelle, nicht im
Browser. Fehlertexte einer API erreichen das DOM meist verkettet
("Fehler: " + error); ein Katalogeintrag fuer den blossen Text traefe dort
nie. Uebersetzt wird deshalb hier, wo der Text entsteht.
"""

import json
import os
import time
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from nc import azraelstate as _nc_azrael
from nc import fehlertext as _nc_fehlertext
from nc import channels as _nc_channels
from nc import i18n as _nc_i18n
from nc import piper_voices as _nc_piper
from nc import whispercfg as _nc_whisper
from nc.dbwrap import db_conn
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("azrael", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    return _nc_i18n.t(s)


def _zahl(name, default):
    try:
        return int((os.getenv(name, "") or "").strip() or default)
    except (TypeError, ValueError):
        return default


def _mod():
    return _nc_channels.KICK_MOD["obj"]


def _fehler(e, code=500):
    """Einheitlicher Ausgang fuer die zwei Faelle, die jede Route hat: der
       Bot-Loop laeuft noch nicht (voruebergehend, 503) oder etwas ging
       wirklich schief. Der Fehlertext erreicht das Dashboard absichtlich —
       ohne ihn ist 'AZRAEL antwortet nicht' nicht diagnostizierbar."""
    if isinstance(e, RuntimeError) and _loop_not_ready(e):
        return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
    return jsonify(ok=False, error=_fehler_text(e, "_fehler")), code


# ---- Identitaet, Telemetrie, Rollen -----------------------------------------

@bp.route("/api/azrael/ask", methods=["POST"])
def api_azrael_ask():
    """v37: AZRAEL direkt aus dem Dashboard testen (dieselbe eine KI-Identität)."""
    d = request.get_json(silent=True) or {}
    q = (d.get("q") or "").strip()[:2000]   # v37: Längen-Cap gegen Missbrauch
    if not q:
        return jsonify(ok=False, error=_t("leere Frage")), 400
    chat = _nc_azrael.haken("chat")
    if chat is None:
        return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
    try:
        txt, err = _c().run_async(chat("Dashboard-Test", q, timeout=30), timeout=35)
        if err == "budget":
            return jsonify(ok=False, error=_t("KI-Budget erreicht — gleich nochmal"))
        return jsonify(ok=bool(txt), answer=txt or "", error=(err or None))
    except RuntimeError as e:
        return _fehler(e)
    except Exception as e:
        return _fehler(e)


@bp.route("/api/azrael/core")
def api_azrael_core():
    """F90: Live-Zustand + KI-Telemetrie (letzte 24h) für das AZRAEL-Panel.
       Zeigt, dass alle Kanäle EINE KI mit einem Budget/Gedächtnis sind."""
    live = _nc_azrael.haken("live_state")
    out = {"ok": True, "state": (live() if live else ""),
           "budget_used": len(_nc_azrael.CALL_TS),
           "budget_max": _zahl("AZRAEL_MAX_CALLS_MIN", 20),
           "calls_24h": 0, "ok_rate": None, "avg_ms": None, "by_purpose": [], "recent": [],
           "memories": 0, "chapters_24h": 0}
    try:
        since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        with db_conn() as conn:
            agg = conn.execute("SELECT COUNT(*) AS n, AVG(ms) AS avg_ms, "
                               "SUM(CASE WHEN ok=1 THEN 1 ELSE 0 END) AS oks "
                               "FROM ai_interactions WHERE created_at >= ?", (since,)).fetchone()
            n = (agg["n"] if agg else 0) or 0
            out["calls_24h"] = n
            if n:
                out["avg_ms"] = int(agg["avg_ms"] or 0)
                out["ok_rate"] = round(100.0 * (agg["oks"] or 0) / n, 1)
            out["by_purpose"] = [{"purpose": r["purpose"] or "?", "n": r["n"],
                                  "avg_ms": int(r["avg_ms"] or 0)}
                                 for r in conn.execute(
                                     "SELECT purpose, COUNT(*) AS n, AVG(ms) AS avg_ms "
                                     "FROM ai_interactions WHERE created_at >= ? "
                                     "GROUP BY purpose ORDER BY n DESC LIMIT 8", (since,)).fetchall()]
            out["recent"] = [{"purpose": r["purpose"] or "?", "ms": r["ms"] or 0,
                              "ok": bool(r["ok"]), "chars": r["answer_chars"] or 0,
                              "at": (r["created_at"] or "")[11:19]}
                             for r in conn.execute(
                                 "SELECT purpose, ms, ok, answer_chars, created_at "
                                 "FROM ai_interactions ORDER BY id DESC LIMIT 12").fetchall()]
            out["memories"] = conn.execute(
                "SELECT COUNT(*) AS c FROM stream_memories").fetchone()["c"]
            out["chapters_24h"] = conn.execute(
                "SELECT COUNT(*) AS c FROM stream_chapters WHERE created_at >= ?",
                (since,)).fetchone()["c"]
    except Exception as e:
        out["db_error"] = _fehler_text(e, "azrael")
    return jsonify(out)


@bp.route("/api/azrael/agents")
def api_azrael_agents():
    """v37: die AZRAEL-Agenten (je Rolle ein Agent)."""
    active = (_nc_channels.restream_active().get("user") or "")
    items = [{"key": k, "name": a["name"], "role": a["role"], "persona": a["persona"],
              "channels": list(a["match"])} for k, a in _nc_azrael.AGENTS.items()]
    return jsonify(ok=True, agents=items,
                   model=(os.getenv("AI_MODEL", "openai") or "openai"),
                   restream_user=active or None)


@bp.route("/api/azrael/memories")
def api_azrael_memories():
    """AZRAELs destillierte Stream-Erinnerungen einsehen."""
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT username, summary, created_at FROM stream_memories "
                                "ORDER BY id DESC LIMIT 20").fetchall()
        mems = [{"username": r["username"], "summary": r["summary"],
                 "at": (r["created_at"] or "")[:16].replace("T", " ")} for r in rows]
        return jsonify(ok=True, memories=mems, total=len(mems))
    except Exception as e:
        return _fehler(e)


# ---- Reaktion und Kontext ---------------------------------------------------

@bp.route("/api/azrael/react", methods=["POST"])
def api_azrael_react():
    """AZRAEL erzeugt eine Live-Reaktion (Ollama) auf eine Aussage/Behauptung.
       Optional direkt in den Chat posten. Die Reaktion erscheint im Overlay."""
    d = request.get_json(silent=True) or {}
    statement = (d.get("statement") or "").strip()
    if not statement:
        return jsonify(ok=False, error=_t("statement fehlt")), 400
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
    ctx = d.get("context")
    if ctx is not None:   # mitgeschickter Kontext wird auch als aktueller gespeichert
        _nc_azrael.CONTEXT.update(text=str(ctx)[:400], ts=time.time())
    try:
        text, err = _c().run_async(mod.react(statement, context=ctx),
                                   timeout=_zahl("AI_FLASK_TIMEOUT", 300))
    except RuntimeError as e:
        return _fehler(e)
    except Exception as e:
        return _fehler(e)
    if err or not text:
        return jsonify(ok=False,
                       error=err or _t("keine Antwort (Ollama erreichbar?)")), 502
    if d.get("push_chat"):
        try:
            _c().run_async(mod.send_message(_nc_i18n.t(f"AZRAEL: {text}")), timeout=15)
        except Exception:
            pass
    return jsonify(ok=True, reaction=text)


@bp.route("/api/azrael/context", methods=["GET", "POST"])
def api_azrael_context():
    """Aktuellen Stream-Kontext für emotionale AZRAEL-Reaktionen setzen/lesen."""
    if request.method == "POST":
        d = request.get_json(silent=True) or {}
        _nc_azrael.CONTEXT.update(text=(d.get("context") or "").strip()[:400], ts=time.time())
    return jsonify(ok=True, context=_nc_azrael.CONTEXT.get("text", ""))


@bp.route("/api/azrael/reaction")
def api_azrael_reaction():
    """Letzte Live-Reaktion (für Overlay-Polling, falls separat genutzt)."""
    r = _nc_azrael.REACTION
    halt = _zahl("AZRAEL_REACTION_HOLD_S", 18)
    active = bool(r.get("text")) and (time.time() - r.get("ts", 0)) < halt
    return jsonify(ok=True, active=active, text=r.get("text", "") if active else "",
                   statement=r.get("statement", "") if active else "",
                   audio=r.get("audio", "") if active else "",
                   emotion=r.get("emotion", "neutral") if active else "neutral")


@bp.route("/api/azrael/reactions")
def api_azrael_reactions():
    """UPGRADE: Verlauf der AZRAEL-Reaktionen (aus kick_mod_log)."""
    limit = _c().arg_int("limit", 50, 1, 200)
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT ts, content, meta FROM kick_mod_log WHERE kind='reaction' "
                                "ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
        out = []
        for r in rows:
            meta = {}
            try:
                meta = json.loads(r["meta"] or "{}")
            except Exception:
                pass
            out.append({"ts": r["ts"], "text": r["content"],
                        "on": meta.get("on", ""), "src": meta.get("src", "")})
        return jsonify(ok=True, reactions=out)
    except Exception as e:
        return _fehler(e)


# ---- Stimme (Piper) ---------------------------------------------------------

@bp.route("/api/azrael/voices")
def api_azrael_voices():
    """Listet die tatsächlich installierten Piper-Stimmen (rekursiv aus den Verzeichnissen)
       + Diagnose: welches Modell konfiguriert ist und ob es auflösbar ist."""
    vs = _nc_piper.list_voices(force=(request.args.get("rescan") == "1"))
    cur = (_nc_azrael.OVERLAY.get("piper_model") or "").strip()
    resolved = _nc_piper.resolve(cur) if cur else None
    return jsonify(ok=True,
                   piper_installed=_nc_piper.available(),
                   current=cur, resolved=resolved,
                   voices=[{"name": v["name"], "path": v["path"]} for v in vs],
                   roots=_nc_piper.roots())


@bp.route("/api/azrael/tts_test", methods=["POST"])
def api_azrael_tts_test():
    """Test: erzeugt mit Piper Audio aus Text und gibt die URL zurück."""
    if not _nc_piper.available():
        return jsonify(ok=False,
                       error=_t("Piper-CLI nicht gefunden — `pip install piper-tts`")), 502
    d = request.get_json(silent=True) or {}
    text = (d.get("text") or _t("Friede sei mit dir. Ich bin AZRAEL.")).strip()[:300]
    # optionales Override fürs Testen, ohne die Config zu speichern
    if d.get("piper_model"):
        _nc_azrael.OVERLAY["piper_model"] = str(d["piper_model"]).strip()[:300]
    if d.get("piper_length") is not None:
        try:
            _nc_azrael.OVERLAY["piper_length"] = max(0.5, min(2.0, float(d["piper_length"])))
        except (TypeError, ValueError):
            pass
    if not (_nc_azrael.OVERLAY.get("piper_model") or "").strip():
        return jsonify(ok=False, error=_t("Kein Piper-Modell gesetzt")), 400
    say = _nc_piper.SAY["fn"]
    if say is None:
        return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
    try:
        url = _c().run_async(say(text), timeout=35)
    except RuntimeError as e:
        return _fehler(e)
    except Exception as e:
        return _fehler(e)
    if not url:
        return jsonify(ok=False,
                       error=_t("Piper fehlgeschlagen (Modell vorhanden? Logs prüfen)")), 502
    return jsonify(ok=True, url=url)


@bp.route("/api/azrael/piper_status")
def api_azrael_piper_status():
    """DASHBOARD: Piper-TTS-Status (Binary, Engine, Stimm-Modell)."""
    model = (_nc_azrael.OVERLAY.get("piper_model") or "").strip()
    mp = _nc_piper.resolve(model)
    return jsonify(ok=True, available=_nc_piper.available(), bin=_nc_piper.bin_pfad(),
                   engine=(_nc_azrael.OVERLAY.get("voice_engine") or "browser"),
                   voice_enabled=bool(_nc_azrael.OVERLAY.get("voice_enabled")),
                   model=model, model_exists=bool(mp), resolved=mp,
                   data_dir=_nc_piper.data_dir(), voice_dirs=_nc_piper.voice_dirs())


# ---- Live-Reaction-Engine ---------------------------------------------------

@bp.route("/api/azrael/live_status")
def api_azrael_live_status():
    """Status der Live-Reaction-Engine (für Dashboard/Diagnose)."""
    return jsonify(ok=True,
                   enabled=_nc_azrael.flag("LIVE_REACT_ENABLED", "0"),
                   paused=_nc_azrael.LIVE_PAUSED["v"],
                   speech=_nc_azrael.flag("LIVE_REACT_SPEECH", "1"),
                   chat=_nc_azrael.flag("LIVE_REACT_CHAT", "1"),
                   whisper_ready=_nc_whisper.verfuegbar(),
                   proxy_set=bool((os.getenv("PROXY_LIST", "") or "").strip()),
                   record_proxy=bool((os.getenv("RECORD_PROXY", "") or "").strip()),
                   active=sorted(_nc_azrael.WORKERS.keys()))


@bp.route("/api/azrael/live_pause", methods=["POST"])
def api_azrael_live_pause():
    """Reaction-Engine zur Laufzeit pausieren/fortsetzen (ohne Neustart)."""
    d = request.get_json(silent=True) or {}
    _nc_azrael.LIVE_PAUSED["v"] = bool(d.get("paused", not _nc_azrael.LIVE_PAUSED["v"]))
    return jsonify(ok=True, paused=_nc_azrael.LIVE_PAUSED["v"])


@bp.route("/api/azrael/live_test", methods=["POST"])
def api_azrael_live_test():
    """Test-Reaktion durch die volle Kette (react → Overlay/Stimme) ohne echten Live-User."""
    d = request.get_json(silent=True) or {}
    statement = (d.get("statement")
                 or _t("Jemand im Chat behauptet etwas Zweifelhaftes.")).strip()[:500]
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
    try:
        text, err = _c().run_async(
            mod.react(statement, context=_t("Manuell ausgelöste Test-Reaktion:")),
            timeout=_zahl("AI_FLASK_TIMEOUT", 300))
    except RuntimeError as e:
        return _fehler(e)
    except Exception as e:
        return _fehler(e)
    if err or not text:
        return jsonify(ok=False, error=err or _t("keine Antwort")), 502
    return jsonify(ok=True, text=text)


@bp.route("/api/azrael/transcript")
def api_azrael_transcript():
    """DASHBOARD: aktuelles Live-Transkript (was Whisper hoert), je User."""
    out = {u: buf[-20:] for u, buf in _nc_azrael.TRANSCRIPT.items()}
    return jsonify(ok=True, transcript=out)


@bp.route("/api/azrael/whisper_model", methods=["GET", "POST"])
def api_azrael_whisper_model():
    """DASHBOARD: Whisper-Modell lesen / zur Laufzeit umschalten.
       POST {model} -> setzt Namen + leert Cache (Reload beim naechsten Transkript)."""
    if request.method == "POST":
        d = request.get_json(silent=True) or {}
        m = (d.get("model") or "").strip()
        if not m:
            return jsonify(ok=False, error=_t("model fehlt")), 400
        _c().log.info("Whisper-Modell zur Laufzeit umgeschaltet -> %s", _nc_whisper.waehle(m))
        return jsonify(ok=True, model=_nc_whisper.name(), presets=_nc_whisper.PRESETS)
    return jsonify(ok=True, model=_nc_whisper.name(), presets=_nc_whisper.PRESETS,
                   loaded=_nc_whisper.geladen(),
                   available=_nc_whisper.verfuegbar())


# ---- Pro-Streamer-Persona ---------------------------------------------------

@bp.route("/api/azrael/personas")
def api_azrael_personas():
    """UPGRADE: Liste der pro-Streamer-Persona-Overrides."""
    try:
        return jsonify(ok=True, personas=_nc_azrael.personas_load())
    except Exception as e:
        return _fehler(e)


@bp.route("/api/azrael/persona", methods=["POST"])
def api_azrael_persona_set():
    """UPGRADE: setzt/loescht die AZRAEL-Persona fuer einen Streamer.
       Body {username, persona}; leere persona entfernt den Override."""
    d = request.get_json(silent=True) or {}
    user = (d.get("username") or "").strip().lstrip("@").lower()
    persona = (d.get("persona") or "").strip()
    if not user:
        return jsonify(ok=False, error=_t("username fehlt")), 400
    try:
        m = _nc_azrael.personas_load()
        if persona:
            m[user] = persona
        else:
            m.pop(user, None)
        _nc_azrael.personas_save(m)
        return jsonify(ok=True, personas=m)
    except Exception as e:
        return _fehler(e)
