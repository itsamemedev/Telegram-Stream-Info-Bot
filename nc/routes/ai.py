"""nc.routes.ai — die Routen unter /api/ai als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot_v37.
"""

from datetime import datetime, timedelta, timezone
import asyncio
import json
import os
import re
from flask import Blueprint, Response, jsonify, request
from nc.textmore import _parse_iso
from nc.dbwrap import db_conn
import threading
import time as _time_mod
from nc import claude as _nc_claude
import nc.freeai as _nc_freeai
from nc import sqlguard as _nc_sqlguard
from nc.claude import (api_key as _anthropic_key, model as _anthropic_model,
                       model_raw as _anthropic_model_raw)
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set
from nc.aidb import conv_messages as _conv_messages, add_log_entry as add_ai_log_entry
from nc.notes import _conv_list
from nc.sqlutil import _rule_based_sql
from nc.fmt import _sse, _partial_tag_hold
from nc.util import _ai_err_msg
from nc.stats import _streamer_health

from nc import ctx as _ctx

bp = Blueprint("ai", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()




def _llm_list_models(force_refresh=False):
    """Sync + 60s-gecacht (Ersatz der alten _ollama_list_models): Brain-Backend
       zuerst, sonst freeai. Für Flask-Routen, die schnell antworten müssen."""
    now = _time_mod.monotonic()
    if not force_refresh and _c().cfg["_LLM_MODELS_CACHE"]["models"] and \
            now - _c().cfg["_LLM_MODELS_CACHE"]["ts"] < 60:
        return _c().cfg["_LLM_MODELS_CACHE"]["models"]
    models = _c().check_ai_models_sync(timeout=4.0) or []
    if models:
        _c().cfg["_LLM_MODELS_CACHE"].update(ts=now, models=models)
    return models or _c().cfg["_LLM_MODELS_CACHE"]["models"]


def llm_chat_stream_sync(messages, model=None):
    """Synchrones Streaming für SSE-Routen: yielded Text-Deltas.
       V37: streamt über freeai (SSE); wenn der Stream leer bleibt, einmalig
       nicht-streamend nachziehen, damit der Aufrufer IMMER Text bekommt."""
    import queue as _q
    out = _q.Queue()
    def _pump():
        async def _run():
            got = False
            # v4.0-W65: Claude zuerst (Einmalantwort in einen Chunk), sonst freeai-SSE.
            _akey = _anthropic_key()
            if _akey and not any(m.get("images") for m in messages):
                _ct, _ce = await asyncio.to_thread(
                    _nc_claude.chat_sync, messages, _akey, _anthropic_model(model),
                    _c().cfg["AI_STREAM_TIMEOUT"])
                if _ct:
                    out.put(_ct)
                    return
                if _ce == "auth":
                    return
            async for delta in _nc_freeai.chat_stream(messages, model=model,
                                                      timeout=_c().cfg["AI_STREAM_TIMEOUT"]):
                got = True
                out.put(delta)
            if not got:
                txt, _err = await _nc_freeai.chat(messages, model=model,
                                                  timeout=_c().cfg["AI_TIMEOUT"])
                if txt:
                    out.put(txt)
            out.put(None)
        try:
            asyncio.run(_run())
        except Exception:
            out.put(None)
    threading.Thread(target=_pump, daemon=True).start()
    # <think>-Filter (Reasoning-Modelle): Blöcke rausfiltern, über Chunk-Grenzen
    # zerteilte Tags via _partial_tag_hold zurückhalten (Verhalten der alten
    # Stream-Funktion 1:1 erhalten).
    buf, thinking = "", False
    while True:
        item = out.get()
        if item is None:
            break
        buf += item
        emit = ""
        while buf:
            if thinking:
                j = buf.find("</think>")
                if j < 0:
                    hold = _partial_tag_hold(buf, "</think>")
                    buf = buf[len(buf)-hold:] if hold else ""
                    break
                buf = buf[j+len("</think>"):]
                thinking = False
            else:
                i = buf.find("<think>")
                if i < 0:
                    hold = _partial_tag_hold(buf, "<think>")
                    emit += buf[:len(buf)-hold] if hold else buf
                    buf = buf[len(buf)-hold:] if hold else ""
                    break
                emit += buf[:i]
                buf = buf[i+len("<think>"):]
                thinking = True
        if emit:
            yield emit
    if buf and not thinking:
        yield buf


def _conv_create(title=None):
    """Erstellt eine neue Conversation, returnt id."""
    now = datetime.now(timezone.utc).isoformat()
    with db_conn() as conn:
        cur = conn.execute(
            "INSERT INTO ai_conversations (title, created_at, updated_at) "
            "VALUES (?, ?, ?)",
            (title or "Neue Konversation", now, now))
        conn.commit()
        return cur.lastrowid


def _conv_add_message(conv_id, role, content, model=None, duration_ms=None, error=None):
    """Neue Message anhängen + Conversation updaten. Returnt message-id.
       Wenn die Conversation noch keinen echten Titel hat und das hier die
       erste User-Message ist, generieren wir einen Titel aus dem Inhalt."""
    now = datetime.now(timezone.utc).isoformat()
    with db_conn() as conn:
        cur = conn.execute(
            "INSERT INTO ai_messages (conversation_id, role, content, created_at, model, duration_ms, error) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (conv_id, role, content, now, model, duration_ms, error))
        msg_id = cur.lastrowid
        # Conversation-Meta updaten
        # Title-Gen: wenn aktueller Titel noch der default ist UND das die
        # erste user-message ist → neuer Titel aus den ersten 60 Zeichen.
        if role == "user":
            existing = conn.execute(
                "SELECT title FROM ai_conversations WHERE id = ?",
                (conv_id,)).fetchone()
            if existing and (
                not existing["title"]
                or existing["title"] == "Neue Konversation"
                or existing["title"].startswith("Konversation #")
            ):
                # Erste sinnvolle Zeile als Titel
                first_line = content.strip().split("\n")[0]
                if len(first_line) > _c().cfg["AI_CHAT_TITLE_MAX"]:
                    first_line = first_line[:_c().cfg["AI_CHAT_TITLE_MAX"] - 1].rstrip() + "…"
                conn.execute(
                    "UPDATE ai_conversations SET title = ? WHERE id = ?",
                    (first_line, conv_id))
        conn.execute(
            "UPDATE ai_conversations SET updated_at = ?, "
            "  message_count = COALESCE(message_count, 0) + 1 "
            "WHERE id = ?",
            (now, conv_id))
        conn.commit()
        return msg_id


def _conv_archive(conv_id):
    """Soft-Delete einer Conversation (archived=1)."""
    with db_conn() as conn:
        conn.execute(
            "UPDATE ai_conversations SET archived = 1 WHERE id = ?", (conv_id,))
        conn.commit()


def _conv_rename(conv_id, title):
    """Titel manuell setzen."""
    title = (title or "").strip()[:_c().cfg["AI_CHAT_TITLE_MAX"]] or "(leer)"
    with db_conn() as conn:
        conn.execute(
            "UPDATE ai_conversations SET title = ? WHERE id = ?",
            (title, conv_id))
        conn.commit()


def _build_context_for_llm(conv_id, new_user_message):
    """Baut die Nachrichten-Liste für Ollama. Sliding window:
       letzte N Messages bis max M Zeichen Gesamt-Budget.
       Ältere Messages werden weggelassen (vom Anfang her, jüngste behalten)."""
    history = _conv_messages(conv_id)
    # Wir hängen den neuen User-Prompt schon mal an damit er garantiert dabei ist
    candidate = history + [{"role": "user", "content": new_user_message}]
    # Letzte N
    candidate = candidate[-_c().cfg["AI_CHAT_CONTEXT_MESSAGES"]:]
    # Char-Budget: vom NEUESTEN her aufaddieren bis Limit, älteres droppen
    budget = _c().cfg["AI_CHAT_CONTEXT_CHARS"]
    keep_reversed = []
    for m in reversed(candidate):
        c = m.get("content", "") or ""
        if len(c) > budget and keep_reversed:
            break    # passt nicht mehr rein und wir haben schon was
        keep_reversed.append(m)
        budget -= len(c)
    keep = list(reversed(keep_reversed))
    # Format für Ollama: nur role + content
    return [{"role": m["role"], "content": m["content"]} for m in keep]


def _ai_dashboard_rate_check() -> bool:
    """True = ok, False = limit erreicht. Thread-safe."""
    now = _time_mod.monotonic()
    with _c().cfg["_AI_DASHBOARD_LOCK"]:
        # Älter als 60s rauswerfen
        cutoff = now - 60
        _c().cfg["_AI_DASHBOARD_RATE"][:] = [t for t in _c().cfg["_AI_DASHBOARD_RATE"] if t > cutoff]
        if len(_c().cfg["_AI_DASHBOARD_RATE"]) >= _c().cfg["_AI_DASHBOARD_MAX_PER_MIN"]:
            return False
        _c().cfg["_AI_DASHBOARD_RATE"].append(now)
        return True


def _safe_select(sql, limit=200):
    """Fuehrt EINE read-only SELECT-Abfrage aus (KI-Frage -> LLM -> SQL).

    SEC-AUDIT v4.0-W14: die alte Wortliste mit Leerzeichen-Padding war
    umgehbar — SQLite erlaubt `WITH ... DELETE`, und mit TABS oder /**/
    stand nie " delete " im String. Bewiesen: echte Datenloeschung. Jetzt
    ZWEI Linien:
      1. nc.sqlguard: normalisiert (Kommentare raus, alle Whitespaces zu
         Leerzeichen) und prueft mit Wortgrenzen + kein Statement-Stacking.
      2. Bei SQLite zusaetzlich eine READ-ONLY-Verbindung (mode=ro) — dann
         kann selbst eine Filterluecke nichts mehr schreiben.
    """
    s, err = _nc_sqlguard.check_readonly(sql, _c().cfg["_B71_TABLES"])
    if err:
        return None, err
    s = _nc_sqlguard.with_limit(s, limit)
    try:
        if _c().cfg["DB_BACKEND"] != "mariadb" and os.path.exists(_c().cfg["DB_PATH"]):
            import sqlite3 as _sq
            con = _sq.connect(f"file:{os.path.abspath(_c().cfg["DB_PATH"])}?mode=ro",
                              uri=True, timeout=15)
            try:
                con.row_factory = _sq.Row
                rows = [dict(r) for r in con.execute(s).fetchall()]
            finally:
                con.close()
            return rows, None
        with db_conn() as conn:
            rows = [dict(r) for r in conn.execute(s).fetchall()]
        return rows, None
    except Exception as e:
        return None, f"SQL-Fehler: {e}"


def _nl_to_sql(question):
    """Übersetzt eine natürlichsprachige Frage in eine SELECT-Abfrage.
       Bevorzugt die LLM (Ollama), fällt sonst auf Regeln zurück."""
    if _c().cfg["EVOLUTION_USE_LLM"]:
        try:
            sys_prompt = ("Du bist ein SQLite-Experte. Wandle die Frage in GENAU EINE "
                          "read-only SELECT-Abfrage um. Gib NUR die SQL aus, ohne Erklärung, "
                          "ohne Markdown, ohne Semikolon.\n\n" + _c().cfg["_B71_SCHEMA_DOC"])
            text, err = _c().llm_chat_sync(
                [{"role": "system", "content": sys_prompt},
                 {"role": "user", "content": question}],
                timeout=30)
            if text:
                sql = text.strip()
                if "```" in sql:
                    m = re.search(r"```(?:sql)?\s*(.*?)```", sql, re.DOTALL)
                    if m:
                        sql = m.group(1).strip()
                sql = sql.split(";")[0].strip()
                if sql.lower().startswith(("select", "with")):
                    return sql, "llm"
        except Exception:
            pass
    rb = _rule_based_sql(question)
    return (rb, "rule") if rb else (None, None)


@bp.route("/api/ai/models")
def api_ai_models():
    """Verfügbare LLM-Modelle (Brain-Runtime zuerst, sonst freeai-Basen).
       Frontend nutzt das für den Dropdown im Chat."""
    refresh = request.args.get("refresh") == "1"
    models = _llm_list_models(force_refresh=refresh)
    return jsonify({
        "ok": True,
        "models": models,
        "default": _c().cfg["AI_MODEL"],
        "available": len(models),
        "backend": ("brain" if os.getenv("AI_PROVIDER","").strip().lower()=="brain"
                    else "freeai"),
    })


@bp.route("/api/ai/conversations", methods=["GET"])
def api_ai_conversations_list():
    """Liste aller (nicht-archivierten) Conversations."""
    try:
        limit = _c().arg_int("limit", 50, 1, 200)
    except (TypeError, ValueError):
        limit = 50
    convs = _conv_list(limit=limit)
    return jsonify({"ok": True, "conversations": convs})


@bp.route("/api/ai/conversations", methods=["POST"])
def api_ai_conversations_create():
    """Neue (leere) Conversation. POST ohne Body = leere Conversation.
       Optionaler Body: {"title": "..."}"""
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip() or None
    conv_id = _conv_create(title=title)
    return jsonify({"ok": True, "id": conv_id})


@bp.route("/api/ai/conversations/<int:conv_id>", methods=["GET"])
def api_ai_conversation_get(conv_id):
    """Conversation mit allen Messages."""
    with db_conn() as conn:
        meta = conn.execute(
            "SELECT id, title, created_at, updated_at, message_count, last_model "
            "FROM ai_conversations WHERE id = ? AND COALESCE(archived, 0) = 0",
            (conv_id,)).fetchone()
    if not meta:
        return jsonify(ok=False, error="conversation not found"), 404
    messages = _conv_messages(conv_id)
    return jsonify({
        "ok": True,
        "id": meta["id"],
        "title": meta["title"],
        "created_at": meta["created_at"],
        "updated_at": meta["updated_at"],
        "message_count": meta["message_count"] or 0,
        "last_model": meta["last_model"] or "",   # F78: pre-select in dropdown
        "messages": messages,
    })


@bp.route("/api/ai/conversations/<int:conv_id>", methods=["DELETE"])
def api_ai_conversation_delete(conv_id):
    """Archiviert die Conversation (soft delete — Daten bleiben in der DB)."""
    _conv_archive(conv_id)
    return jsonify({"ok": True})


@bp.route("/api/ai/conversations/<int:conv_id>", methods=["PATCH"])
def api_ai_conversation_patch(conv_id):
    """Titel ändern. Body: {"title": "..."}"""
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    if title is None:
        return jsonify(ok=False, error="title field required"), 400
    _conv_rename(conv_id, title)
    return jsonify({"ok": True})


@bp.route("/api/ai/conversations/<int:conv_id>/messages", methods=["POST"])
def api_ai_conversation_send(conv_id):
    """Neue User-Message hinzufügen, Ollama mit voller History befragen,
       Assistant-Response speichern und zurückgeben.
       Body: {"prompt": "..."}
       Returns: {"ok": True, "user_message": {...}, "assistant_message": {...}}"""
    # Rate limit (B5 wiederverwendet, gilt auch hier)
    if not _ai_dashboard_rate_check():
        return jsonify(ok=False,
                       error=f"Rate-Limit erreicht ({_c().cfg["_AI_DASHBOARD_MAX_PER_MIN"]}/min)"), 429

    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify(ok=False, error="prompt darf nicht leer sein"), 400
    if len(prompt) > _c().cfg["AI_TEXT_MAX_CHARS"]:
        return jsonify(ok=False, error=f"prompt zu lang (max {_c().cfg["AI_TEXT_MAX_CHARS"]} Zeichen)"), 400

    # Conversation existence-Check
    with db_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM ai_conversations WHERE id = ? AND COALESCE(archived, 0) = 0",
            (conv_id,)).fetchone()
    if not exists:
        return jsonify(ok=False, error="conversation not found"), 404

    # F78: Per-Conversation Model-Wahl (mit Validierung gegen INSTALLIERTE
    # Ollama-Modelle). Vorher: B9 hartcodiert auf AI_MODEL — sicher,
    # aber unflexibel. Jetzt: Operator kann pro Konversation wählen,
    # ABER nur aus der Liste die Ollama tatsächlich installed hat
    # (keine arbitrary downloads via Dashboard).
    requested = (payload.get("model") or "").strip()
    if requested:
        installed = _llm_list_models()
        if requested in installed:
            model = requested
        else:
            # ungültig → fallback auf Server-Default. Frontend zeigt's an.
            log.info(f"F78: requested model '{requested}' not installed "
                     f"→ fallback to {_c().cfg["AI_MODEL"]}")
            model = _c().cfg["AI_MODEL"]
    else:
        # Kein Model im Request → check ob Conversation 'last_model' gespeichert hat
        with db_conn() as conn:
            row = conn.execute(
                "SELECT last_model FROM ai_conversations WHERE id = ?",
                (conv_id,)).fetchone()
        last = (row and row["last_model"]) or ""
        if last and last in _llm_list_models():
            model = last
        else:
            model = _c().cfg["AI_MODEL"]

    # Conversation 'last_model' updaten falls Operator gewechselt hat
    with db_conn() as conn:
        conn.execute(
            "UPDATE ai_conversations SET last_model = ? WHERE id = ?",
            (model, conv_id))
        conn.commit()

    # User-Message speichern (für DB-Persistence + Title-Gen)
    user_msg_id = _conv_add_message(conv_id, "user", prompt)

    # Context aufbauen + an Ollama
    messages = _build_context_for_llm(conv_id, "")
    # _build_context appended uns die new-message — wir wollen den User-Prompt
    # aber NICHT zweimal, da er schon in messages drin ist via DB-Lese.
    # Korrektur: _build_context lies aus DB (inkl. unserer just-inserted message)
    # und appended dann eine LEERE user-message. Wir lassen die weg:
    if messages and messages[-1]["role"] == "user" and not messages[-1]["content"]:
        messages.pop()

    started = _time_mod.monotonic()
    # V37-B104: Deckel MUSS mit — sonst erbt der Call AI_TIMEOUT (0 = im Code
    # 3600s) und blockiert einen Flask-Worker bis zu einer Stunde.
    response, err_kind = _c().llm_chat_sync(messages, model=model,
                                       timeout=_c().cfg["AI_FLASK_TIMEOUT"])
    duration_ms = int((_time_mod.monotonic() - started) * 1000)

    # B11: response cappen
    if response and len(response) > _c().cfg["AI_TEXT_MAX_CHARS"]:
        response = (response[:_c().cfg["AI_TEXT_MAX_CHARS"]]
                    + f"\n\n…[gekürzt, originale Länge: {len(response):,} Zeichen]")

    if err_kind or not response:
        err_msg = {
            "model_missing": f"Modell '{model}' nicht installiert",
            "timeout":       f"Ollama Timeout nach {_c().cfg["AI_TIMEOUT"]}s",
            "unreachable":   "Ollama nicht erreichbar (Service läuft nicht?)",
            "http":          "Ollama HTTP-Fehler",
            "other":         "Unerwarteter Fehler",
        }.get(err_kind, "Keine Antwort vom LLM")
        # Assistant-Error als message speichern (so dass es im UI sichtbar ist)
        asst_msg_id = _conv_add_message(conv_id, "assistant", "",
                                        model=model, duration_ms=duration_ms,
                                        error=err_msg)
        # Auch in ai_log für globalen Stream
        try:
            add_ai_log_entry(0, 0, prompt, None, model, duration_ms, err_msg, None, None)
        except Exception as e:
            log.warning(f"ai_log dashboard-chat write failed: {e}")
        return jsonify(ok=False, error=err_msg, error_kind=err_kind,
                       conversation_id=conv_id, user_message_id=user_msg_id,
                       assistant_message_id=asst_msg_id,
                       model=model, duration_ms=duration_ms), 502

    asst_msg_id = _conv_add_message(conv_id, "assistant", response,
                                    model=model, duration_ms=duration_ms)
    # Globaler AI-Stream bekommt auch einen Eintrag
    try:
        add_ai_log_entry(0, 0, prompt, response, model, duration_ms, None, None, None)
    except Exception as e:
        log.warning(f"ai_log dashboard-chat write failed: {e}")

    # Return: beide neuen Messages (UI muss sie nicht re-fetchen)
    return jsonify({
        "ok": True,
        "conversation_id": conv_id,
        "user_message": {
            "id": user_msg_id,
            "role": "user",
            "content": prompt,
        },
        "assistant_message": {
            "id": asst_msg_id,
            "role": "assistant",
            "content": response,
            "model": model,
            "duration_ms": duration_ms,
        },
    })


@bp.route("/api/ai/conversations/<int:conv_id>/stream", methods=["POST"])
def api_ai_conversation_stream(conv_id):
    """Wie .../messages, aber als Live-Stream (SSE): kein Timeout-Abbruch während
       Laden/Denken; Frontend zeigt Reasoning + Tokens live. Speichert die
       Assistant-Antwort am Ende wie der normale Endpoint."""
    if not _ai_dashboard_rate_check():
        return jsonify(ok=False, error=f"Rate-Limit erreicht ({_c().cfg["_AI_DASHBOARD_MAX_PER_MIN"]}/min)"), 429
    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify(ok=False, error="prompt darf nicht leer sein"), 400
    if len(prompt) > _c().cfg["AI_TEXT_MAX_CHARS"]:
        return jsonify(ok=False, error=f"prompt zu lang (max {_c().cfg["AI_TEXT_MAX_CHARS"]} Zeichen)"), 400
    with db_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM ai_conversations WHERE id = ? AND COALESCE(archived, 0) = 0",
            (conv_id,)).fetchone()
    if not exists:
        return jsonify(ok=False, error="conversation not found"), 404

    # Model-Auflösung (wie im Nicht-Stream-Endpoint)
    requested = (payload.get("model") or "").strip()
    if requested and requested in _llm_list_models():
        model = requested
    else:
        with db_conn() as conn:
            row = conn.execute("SELECT last_model FROM ai_conversations WHERE id = ?",
                               (conv_id,)).fetchone()
        last = (row and row["last_model"]) or ""
        model = last if (last and last in _llm_list_models()) else _c().cfg["AI_MODEL"]
    with db_conn() as conn:
        conn.execute("UPDATE ai_conversations SET last_model = ? WHERE id = ?", (model, conv_id))
        conn.commit()

    user_msg_id = _conv_add_message(conv_id, "user", prompt)
    messages = _build_context_for_llm(conv_id, "")
    if messages and messages[-1]["role"] == "user" and not messages[-1]["content"]:
        messages.pop()

    def gen():
        yield _sse("start", {"user_message_id": user_msg_id, "model": model})
        started = _time_mod.monotonic()
        answer_parts, think_parts, err = [], [], None
        try:
            for ev in llm_chat_stream_sync(messages, model=model):
                if "error" in ev:
                    err = ev["error"]
                    yield _sse("error", {"error": _ai_err_msg(err, model), "error_kind": err})
                    break
                if ev.get("thinking"):
                    think_parts.append(ev["thinking"])
                    yield _sse("thinking", {"delta": ev["thinking"]})
                if ev.get("content"):
                    chunk = ev["content"]
                    if not answer_parts:
                        chunk = chunk.lstrip()      # Antwort nicht mit Leerzeilen beginnen
                        if not chunk:
                            continue
                    answer_parts.append(chunk)
                    yield _sse("token", {"delta": chunk})
                if ev.get("done"):
                    break
        except GeneratorExit:
            return
        except Exception as e:
            log.warning(f"AI-Stream gen Fehler: {e}")
            err = err or "other"
            yield _sse("error", {"error": _ai_err_msg(err, model), "error_kind": err})

        duration_ms = int((_time_mod.monotonic() - started) * 1000)
        answer = "".join(answer_parts).strip()
        if answer and len(answer) > _c().cfg["AI_TEXT_MAX_CHARS"]:
            answer = answer[:_c().cfg["AI_TEXT_MAX_CHARS"]] + f"\n\n…[gekürzt, {len(answer):,} Zeichen]"
        thinking = "".join(think_parts).strip()

        if err or not answer:
            emsg = _ai_err_msg(err or "other", model)
            aid = _conv_add_message(conv_id, "assistant", "", model=model,
                                    duration_ms=duration_ms, error=emsg)
            try: add_ai_log_entry(0, 0, prompt, None, model, duration_ms, emsg, None, None)
            except Exception: pass
            yield _sse("done", {"ok": False, "error": emsg, "assistant_message_id": aid,
                                "model": model, "duration_ms": duration_ms})
        else:
            aid = _conv_add_message(conv_id, "assistant", answer, model=model,
                                    duration_ms=duration_ms)
            try: add_ai_log_entry(0, 0, prompt, answer, model, duration_ms, None, None, None)
            except Exception: pass
            yield _sse("done", {"ok": True, "assistant_message_id": aid, "content": answer,
                                "thinking": thinking, "model": model, "duration_ms": duration_ms})

    resp = Response(gen(), mimetype="text/event-stream")
    resp.headers["Cache-Control"] = "no-cache"
    resp.headers["X-Accel-Buffering"] = "no"      # kein Proxy-Buffering (nginx)
    resp.headers["Connection"] = "keep-alive"
    return resp


@bp.route("/api/ai/diagnose", methods=["POST"])
def api_ai_diagnose():
    """AI-gestützte Diagnose der aktuellen Bot-Probleme.
       Sammelt: letzte Errors, recent Outcomes, Health-Components.
       Liefert: LLM-Vorschläge zu möglichen Ursachen + Fixes (TEXT, kein Code-Apply!)."""
    if not _ai_dashboard_rate_check():
        return jsonify(ok=False,
                       error=f"Rate-Limit erreicht ({_c().cfg["_AI_DASHBOARD_MAX_PER_MIN"]}/min)"), 429

    context_parts = []

    # 1. Recent ERROR lines (filtered against scanner-noise B41)
    try:
        log_path = os.path.join(_c().cfg["LOG_DIR"], "error.log")
        if os.path.isfile(log_path):
            with open(log_path, "r", errors="ignore") as f:
                lines = f.readlines()[-300:]
            errs = [l.strip() for l in lines if "| ERROR |" in l]
            # B41 noise-Filter
            noise_re = re.compile(r"bad request version|jdwp-handshake|jrmi|rtsp/1\.0|giop|amqp|mssqlserver", re.I)
            errs = [l for l in errs if not noise_re.search(l)][-25:]
            if errs:
                context_parts.append("=== RECENT ERRORS (last 25) ===\n" + "\n".join(errs))
    except Exception as e:
        log.warning(f"diagnose error-log read failed: {e}")

    # 2. Outcomes last 24h
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT outcome, COUNT(*) AS c FROM recording_attempts "
                "WHERE started_at >= ? GROUP BY outcome ORDER BY c DESC",
                (cutoff,)).fetchall()
        outs = [f"{r['outcome'] or 'unknown'}: {r['c']}" for r in rows]
        if outs:
            context_parts.append("=== OUTCOMES LAST 24H ===\n" + "\n".join(outs))
    except Exception as e:
        log.warning(f"diagnose outcomes read failed: {e}")

    # 3. Backoff state
    try:
        if _c().cfg["_STREAM_DEAD_BACKOFF_UNTIL"]:
            count = sum(1 for u in list(_c().cfg["_STREAM_DEAD_BACKOFF_UNTIL"].values())
                        if u > _time_mod.monotonic())   # BUG-FIX: list()-Snapshot (Race)
            if count > 0:
                context_parts.append(f"=== B45 BACKOFF ACTIVE ===\n{count} trackings in stream-dead backoff")
    except Exception:
        pass

    # 4. Disk
    try:
        st = _c().get_storage_stats()
        pct = (st.get("disk") or {}).get("used_percent")
        if pct is not None:
            context_parts.append(f"=== DISK ===\n{pct:.0f}% used")
    except Exception:
        pass

    if not context_parts:
        return jsonify(ok=True,
                       diagnosis="Keine auffälligen Daten verfügbar (kein Error-Log, keine Aufnahme-History).",
                       model="(none)", duration_ms=0)

    prompt = (
        "Du bist ein erfahrener Senior Engineer der einen TikTok-Live-Recording-Bot "
        "diagnostiziert. Analysiere die folgenden Daten knapp + konkret. Identifiziere:\n"
        "1) das wichtigste aktuelle Problem (falls eines existiert)\n"
        "2) wahrscheinliche Ursache\n"
        "3) konkrete Handlungsempfehlung (1-3 Sätze)\n"
        "Wenn alles in Ordnung aussieht: sage das. Antworte auf DEUTSCH, max 200 Wörter.\n\n"
        + "\n\n".join(context_parts) +
        "\n\nDeine Analyse:"
    )

    started = _time_mod.monotonic()
    response, err_kind = _c().llm_chat_sync(
        [{"role": "user", "content": prompt}], model=_c().cfg["AI_MODEL"],
        timeout=_c().cfg["AI_FLASK_TIMEOUT"])     # V37-B104: Flask-Worker nicht verhungern lassen
    duration_ms = int((_time_mod.monotonic() - started) * 1000)

    if err_kind or not response:
        return jsonify(ok=False, error=err_kind or "no response from LLM"), 502

    return jsonify({
        "ok": True,
        "diagnosis": response.strip(),
        "model": _c().cfg["AI_MODEL"],
        "duration_ms": duration_ms,
        "context_chars": sum(len(p) for p in context_parts),
        "sections": len(context_parts),
    })


@bp.route("/api/ai/ask", methods=["POST"])
def api_ai_ask():
    """Dashboard-Variante von /ai. Single-shot Q&A (kein History-Tracking
       cross-call) — wer Konversation will nimmt Telegram. Trotzdem wird der
       Call ins ai_log geschrieben damit er im AI-Stream auftaucht.
       POST-Body: {"prompt": "..."}  (model-Param wird IGNORIERT — siehe B9)
       Returns:    {"ok": bool, "response": str, "model": str, "duration_ms": int,
                    "error": str (bei Fehler)}

       F49-Bug-Fix B5: Rate-Limit (default 15/min, via AI_DASHBOARD_MAX_PER_MIN).
       F49-Bug-Fix B9: 'model' im Request wird IGNORIERT — sonst könnte ein
       Caller beliebige Modellnamen schicken und Ollama zum Download triggern.
       Wir nutzen immer AI_MODEL (das was der Telegram-/ai auch nimmt)."""
    # B5: Rate-Limit zuerst
    if not _ai_dashboard_rate_check():
        return jsonify(ok=False,
                       error=f"Rate-Limit erreicht ({_c().cfg["_AI_DASHBOARD_MAX_PER_MIN"]}/min)"), 429

    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify(ok=False, error="prompt darf nicht leer sein"), 400
    if len(prompt) > _c().cfg["AI_TEXT_MAX_CHARS"]:
        return jsonify(ok=False, error=f"prompt zu lang (max {_c().cfg["AI_TEXT_MAX_CHARS"]} Zeichen)"), 400
    # B9: model-Param ignorieren — immer Server-Default nehmen
    model = _c().cfg["AI_MODEL"]

    # F49: Special chat_id=0 / user_id=0 markieren das als Dashboard-Quelle.
    # Im AI-Stream sieht man dann "[dashboard]" statt einer Telegram-User-ID.
    DASHBOARD_CHAT_ID = 0
    DASHBOARD_USER_ID = 0

    started = _time_mod.monotonic()
    messages = [{"role": "user", "content": prompt}]
    response, err_kind = _c().llm_chat_sync(messages, model=model,
                                       timeout=_c().cfg["AI_FLASK_TIMEOUT"])   # V37-B104
    duration_ms = int((_time_mod.monotonic() - started) * 1000)

    # F49-Bug-Fix B11: LLM-Response auf AI_TEXT_MAX_CHARS cappen.
    # Manche Modelle geben mehrere MB zurück (z.B. wenn prompt nach "dem
    # ganzen Dokument" fragt). add_ai_log_entry capped schon auf 16k für die
    # DB, aber das API-Response selbst war uncapped → riesiges JSON für den
    # Browser. Wir trunkieren mit klarer Markierung.
    if response and len(response) > _c().cfg["AI_TEXT_MAX_CHARS"]:
        response = (response[:_c().cfg["AI_TEXT_MAX_CHARS"]]
                    + f"\n\n…[gekürzt, originale Länge: {len(response):,} Zeichen]")

    if err_kind or not response:
        # Log auch bei Fehler — damit man im Stream sieht WAS schief lief
        err_msg = {
            "model_missing": f"Modell '{model}' nicht installiert",
            "timeout":       f"Ollama Timeout nach {_c().cfg["AI_TIMEOUT"]}s",
            "unreachable":   "Ollama nicht erreichbar (Service läuft nicht?)",
            "http":          "Ollama HTTP-Fehler",
            "other":         "Unerwarteter Fehler",
        }.get(err_kind, "Keine Antwort vom LLM")
        try:
            add_ai_log_entry(DASHBOARD_CHAT_ID, DASHBOARD_USER_ID, prompt, None,
                             model, duration_ms, err_msg, None, None)
        except Exception as e:
            log.warning(f"ai_log dashboard write failed: {e}")
        return jsonify(ok=False, error=err_msg, error_kind=err_kind,
                       model=model, duration_ms=duration_ms), 502

    try:
        add_ai_log_entry(DASHBOARD_CHAT_ID, DASHBOARD_USER_ID, prompt, response,
                         model, duration_ms, None, None, None)
    except Exception as e:
        log.warning(f"ai_log dashboard write failed: {e}")

    return jsonify(ok=True, response=response, model=model, duration_ms=duration_ms)


@bp.route("/api/ai/config")
def api_ai_config():
    """v37 / v4.0-W77: die EINE KI-Konfiguration fürs Panel.

    BUG-FIX W77: /api/ai/config war versehentlich an api_freeai_status geroutet
    (liefert bases/model/provider — OHNE budget/timeout/style/url), api_ai_config
    hing an KEINER Route. Das Panel las darum d.budget_used/_max/_timeout_s →
    'undefined/undefined'. Jetzt korrekt verdrahtet.

    Zudem Claude-bewusst: sobald ein Anthropic-Key gesetzt ist, ist Claude der
    PRIMÄRE Provider (llm_chat: Claude zuerst). Das Panel zeigt das jetzt an,
    statt den freeai-Fallback als 'aktiv' auszugeben."""
    _akey = _anthropic_key()
    if _akey:
        _eff = _anthropic_model()
        _raw = _anthropic_model_raw()
        return jsonify(ok=True,
                       model=_eff,
                       url="api.anthropic.com/v1/messages",
                       provider="Claude (Anthropic)",
                       style=_c().cfg["AZRAEL_STYLE"],
                       budget_max=_c().cfg["AZRAEL_MAX_CALLS_MIN"],
                       budget_used=len(_c().cfg["_AI_CALL_TS"]),
                       timeout_s=_c().cfg["AI_TIMEOUT"],
                       model_upgraded=(_eff != _raw),    # v4.0-W88: W73-Auto-Heal sichtbar
                       configured_model=_raw)
    _brain = os.getenv("AI_PROVIDER", "").strip().lower() == "brain"
    return jsonify(ok=True,
                   model=_c().cfg["AI_MODEL"],
                   url=(os.getenv("BRAIN_LLAMACPP_URL", "http://127.0.0.1:8080")
                        if _brain else "nc.freeai (keyless)"),
                   provider=("brain (llama.cpp)" if _brain else "freeai (keyless)"),
                   style=_c().cfg["AZRAEL_STYLE"],
                   budget_max=_c().cfg["AZRAEL_MAX_CALLS_MIN"],
                   budget_used=len(_c().cfg["_AI_CALL_TS"]),
                   timeout_s=_c().cfg["AI_TIMEOUT"])


@bp.route("/api/ai/claude/status")
def api_claude_status():
    """v4.0-W64: Status der Claude-Anbindung (Key gesetzt? maskiert, Modell, Quelle)."""
    stored = _cfg_get("ai.anthropic_key", None)
    env_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    key = (stored.strip() if isinstance(stored, str) and stored.strip() else env_key)
    masked = (key[:7] + "…" + key[-4:]) if len(key) >= 14 else ("gesetzt" if key else "")
    raw_model = _anthropic_model_raw()
    eff_model = _nc_claude.resolve_model(raw_model)
    return jsonify(ok=True, configured=bool(key), masked=masked,
                   source=("dashboard" if isinstance(stored, str) and stored.strip()
                           else ("env" if env_key else "keine")),
                   model=eff_model, configured_model=raw_model,
                   model_upgraded=(eff_model != raw_model),
                   model_note=('Modell „%s“ ist abgeschaltet — automatisch auf '
                               '„%s“ angehoben. .env/ANTHROPIC_MODEL aktualisieren.'
                               % (raw_model, eff_model)) if eff_model != raw_model else "",
                   default_model=_nc_claude.DEFAULT_MODEL)


@bp.route("/api/ai/claude/save", methods=["POST"])
def api_claude_save():
    """Key und/oder Modell speichern (in app_config). Key wird nie zurückgegeben."""
    payload = request.get_json(silent=True) or {}
    saved = {}
    if "key" in payload:
        k = str(payload.get("key") or "").strip()
        if k and not k.startswith("sk-"):
            return jsonify(ok=False, error="Kein gültiger Anthropic-Key (erwartet 'sk-…')."), 400
        _cfg_set("ai.anthropic_key", k)   # leerer String = entfernt
        saved["key"] = bool(k)
    if "model" in payload:
        m = str(payload.get("model") or "").strip()
        _cfg_set("ai.anthropic_model", m)
        saved["model"] = m or _nc_claude.DEFAULT_MODEL
    return jsonify(ok=True, saved=saved)


@bp.route("/api/ai/claude/test", methods=["POST"])
def api_claude_test():
    """Den gespeicherten (oder mitgeschickten) Key mit einem Mini-Call prüfen.
       v4.0-W70: gibt den ECHTEN Grund zurück (HTTP-Status + Anthropic-Fehlertext
       oder konkreter Netzfehler), damit ein Fehlschlag diagnostizierbar ist."""
    payload = request.get_json(silent=True) or {}
    key = str(payload.get("key") or "").strip() or _anthropic_key()
    if not key:
        return jsonify(ok=False, error="Kein Key gesetzt.",
                       message="Kein Key im Feld und keiner gespeichert."), 400
    ok_, kind, detail = _nc_claude.probe(key, model=_anthropic_model())
    hint = {"auth": " — Key falsch/gesperrt oder Guthaben leer.",
            "unreachable": " — der Server erreicht api.anthropic.com nicht "
                           "(Egress/Firewall, Port 443, DNS oder Proxy prüfen).",
            "bad_request": " — meist ein ungültiger Modellname.",
            "http_404": " — Modell nicht gefunden (Modellname prüfen)."}.get(kind, "")
    return jsonify(ok=bool(ok_), detail=kind, message=detail + hint)


@bp.route("/api/ai/skills")
def api_ai_skills():
    """Meta: welche Fähigkeiten die KI über das Selbstlernen hinaus hat."""
    return jsonify(ok=True, skills=[
        {"id": "ask", "name": "Daten-Fragen (NL→SQL)", "endpoint": "/api/ai/query",
         "desc": "Stellt natürlichsprachige Fragen an die eigene Datenbank."},
        {"id": "predict", "name": "Go-Live-Vorhersage", "endpoint": "/api/ai/predict-golive/<user>",
         "desc": "Schätzt wann ein Streamer wahrscheinlich live geht."},
        {"id": "anomalies", "name": "Anomalie-Erkennung", "endpoint": "/api/ai/anomalies",
         "desc": "Erkennt Fehler-/Storage-/Volumen-Spikes."},
        {"id": "segments", "name": "Streamer-Segmentierung", "endpoint": "/api/ai/segments",
         "desc": "Gruppiert Streamer nach Verhalten."},
        {"id": "recommend", "name": "Handlungsempfehlungen", "endpoint": "/api/ai/recommendations",
         "desc": "Schlägt konkrete Aktionen vor."},
        {"id": "report", "name": "Klartext-Report", "endpoint": "/api/ai/report",
         "desc": "Fasst die Aktivität in Klartext zusammen."},
        {"id": "retry", "name": "Retry-Beratung", "endpoint": "/api/ai/retry-advice/<user>",
         "desc": "Empfiehlt Retry-Strategie aus dem Fehlermuster."},
        {"id": "forecast", "name": "Speicher-Prognose", "endpoint": "/api/ai/forecast-storage",
         "desc": "Schätzt wann die Platte voll ist."},
        {"id": "health", "name": "Streamer-Scorecard", "endpoint": "/api/ai/health-score/<user>",
         "desc": "Composite-Gesundheitswert je Streamer."},
    ])


@bp.route("/api/ai/query", methods=["POST"])
def api_ai_query():
    """KI-Fähigkeit: natürlichsprachige Frage → sichere SELECT → Antwort.
       Body: {"q": "welcher streamer scheitert am häufigsten diese woche?"}"""
    data = request.get_json(silent=True) or {}
    q = (data.get("q") or data.get("question") or "").strip()
    if not q:
        return jsonify(ok=False, error="q (Frage) erforderlich"), 400
    sql, source = _nl_to_sql(q)
    if not sql:
        return jsonify(ok=False, error="Konnte die Frage nicht in SQL übersetzen "
                       "(LLM offline? Versuch eine einfachere Formulierung).",
                       question=q), 200
    rows, err = _safe_select(sql)
    if err:
        return jsonify(ok=False, question=q, sql=sql, source=source, error=err), 200
    return jsonify(ok=True, question=q, sql=sql, source=source,
                   row_count=len(rows), rows=rows[:200])


@bp.route("/api/ai/predict-golive/<username>")
def api_ai_predict_golive(username):
    """Schätzt die wahrscheinlichsten Live-Zeiten eines Streamers aus der
       Historie (Stunde × Wochentag). Datenquelle: recording_attempts."""
    username = username.lstrip("@")
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT started_at FROM recording_attempts WHERE username=? "
                "AND outcome IN ('ok','stall_killed_partial') ORDER BY started_at DESC LIMIT 500",
                (username,)).fetchall()
        if not rows:
            # Fallback: alle Versuche (auch fehlgeschlagene zeigen Live-Zeiten)
            with db_conn() as conn:
                rows = conn.execute(
                    "SELECT started_at FROM recording_attempts WHERE username=? "
                    "ORDER BY started_at DESC LIMIT 500", (username,)).fetchall()
        by_hour = [0] * 24
        by_dow = [0] * 7
        n = 0
        for r in rows:
            dt = _parse_iso(r["started_at"])
            if not dt:
                continue
            # BUG-FIX: naive datetimes als UTC behandeln (konsistent mit _streamer_health)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            by_hour[dt.hour] += 1
            by_dow[dt.weekday()] += 1
            n += 1
        if n < 3:
            return jsonify(ok=True, username=username, samples=n,
                           note="Zu wenig Historie für eine Vorhersage.",
                           top_hours=[], top_days=[])
        top_hours = sorted(range(24), key=lambda h: by_hour[h], reverse=True)[:3]
        dow_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        top_days = sorted(range(7), key=lambda d: by_dow[d], reverse=True)[:3]
        return jsonify(ok=True, username=username, samples=n,
                       top_hours=[{"hour": h, "score": by_hour[h],
                                   "pct": round(100.0 * by_hour[h] / n)} for h in top_hours if by_hour[h] > 0],
                       top_days=[{"day": dow_names[d], "score": by_dow[d],
                                  "pct": round(100.0 * by_dow[d] / n)} for d in top_days if by_dow[d] > 0],
                       histogram_hours=by_hour, histogram_days=by_dow)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/anomalies")
def api_ai_anomalies():
    """Erkennt Auffälligkeiten: Fehler-Spike (jüngstes Fenster vs Baseline),
       Storage-Spike, Versuchs-Volumen-Spike, plötzlich stille Streamer.
       Wird im Dashboard angezeigt — KEINE Push-Benachrichtigung."""
    out = []
    try:
        now = datetime.now(timezone.utc)
        d1 = (now - timedelta(days=1)).isoformat()
        d7 = (now - timedelta(days=7)).isoformat()
        with db_conn() as conn:
            def rate(since_a, since_b):
                row = conn.execute(
                    "SELECT SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok, "
                    "SUM(CASE WHEN outcome NOT IN ('running','cancelled') THEN 1 ELSE 0 END) AS done "
                    "FROM recording_attempts WHERE started_at >= ? AND started_at < ?",
                    (since_a, since_b)).fetchone()
                ok_n, done = int(row["ok"] or 0), int(row["done"] or 0)
                return (100.0 * ok_n / done if done else None), done
            r24, n24 = rate(d1, now.isoformat())
            r_base, n_base = rate(d7, d1)
            if r24 is not None and r_base is not None and n24 >= 5 and (r_base - r24) >= 25:
                out.append({"type": "failure_spike", "severity": "high",
                            "title": "Fehler-Spike letzte 24h",
                            "detail": f"Erfolgsquote fiel auf {r24:.0f}% (Baseline {r_base:.0f}%).",
                            "metric": {"current": round(r24, 1), "baseline": round(r_base, 1)}})
            # Storage-Spike: Tagesvolumen vs 7d-Schnitt
            day_mb = conn.execute(
                "SELECT COALESCE(SUM(file_size),0)/1048576.0 AS mb FROM recordings WHERE created_at >= ?",
                (d1,)).fetchone()["mb"]
            wk_mb = conn.execute(
                "SELECT COALESCE(SUM(file_size),0)/1048576.0 AS mb FROM recordings WHERE created_at >= ?",
                (d7,)).fetchone()["mb"]
            avg_day = wk_mb / 7.0 if wk_mb else 0
            if avg_day > 50 and day_mb > avg_day * 2.5:
                out.append({"type": "storage_spike", "severity": "medium",
                            "title": "Speicher-Spike heute",
                            "detail": f"{day_mb:.0f} MB heute vs Ø {avg_day:.0f} MB/Tag.",
                            "metric": {"today_mb": round(day_mb), "avg_mb": round(avg_day)}})
            # Volumen-Spike: viele Versuche, wenige Erfolge (Retry-Sturm)
            if n24 >= 50 and r24 is not None and r24 < 15:
                out.append({"type": "retry_storm", "severity": "high",
                            "title": "Möglicher Retry-Sturm",
                            "detail": f"{n24} Versuche/24h bei nur {r24:.0f}% Erfolg — ein paar "
                                      f"nicht-aufnehmbare Streamer hämmern.",
                            "metric": {"attempts_24h": n24, "success_pct": round(r24, 1)}})
            # Stille Streamer: aktiv getrackt, aber lange kein Versuch
            silent = conn.execute(
                "SELECT t.username, MAX(a.started_at) AS last FROM trackings t "
                "LEFT JOIN recording_attempts a ON a.username=t.username "
                "WHERE t.paused=0 GROUP BY t.username HAVING last IS NULL OR last < ?",
                ((now - timedelta(days=14)).isoformat(),)).fetchall()
            if silent:
                names = ", ".join("@" + s["username"] for s in silent[:6])
                out.append({"type": "dormant_streamers", "severity": "low",
                            "title": f"{len(silent)} stille Streamer (>14 Tage)",
                            "detail": f"Lange kein Aufnahmeversuch: {names}. Evtl. inaktiv/pausieren.",
                            "metric": {"count": len(silent)}})
        return jsonify(ok=True, count=len(out), anomalies=out,
                       checked_at=now.isoformat())
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/segments")
def api_ai_segments():
    """Segmentiert Streamer nach Verhalten: reliable / sporadic / chronic_fail /
       dormant / high_volume. Einfaches, transparentes Regelmodell."""
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        seg = {"reliable": [], "sporadic": [], "chronic_fail": [], "dormant": [], "high_volume": []}
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT t.username, "
                " COUNT(a.id) AS attempts, "
                " SUM(CASE WHEN a.outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok, "
                " MAX(a.started_at) AS last "
                "FROM trackings t LEFT JOIN recording_attempts a "
                "  ON a.username=t.username AND a.started_at >= ? "
                "GROUP BY t.username", (cut,)).fetchall()
        for r in rows:
            u = r["username"]
            att = int(r["attempts"] or 0)
            ok_n = int(r["ok"] or 0)
            last = r["last"]
            rate = (100.0 * ok_n / att) if att else 0
            entry = {"user": u, "attempts": att, "ok_rate": round(rate, 1), "last": last}
            if att == 0:
                seg["dormant"].append(entry)
            elif rate >= 70 and att >= 3:
                # BUG-FIX: high_volume (att>=40) wurde vorher zuerst geprüft — ein Streamer
                # mit 40+ Versuchen und 95% Erfolg landete als "high_volume" statt "reliable".
                # Inhaltliche Segmente schlagen das Volumen-Label.
                seg["reliable"].append(entry)
            elif rate < 20 and att >= 4:
                seg["chronic_fail"].append(entry)
            elif att >= 40:
                seg["high_volume"].append(entry)
            else:
                seg["sporadic"].append(entry)
        summary = {k: len(v) for k, v in seg.items()}
        return jsonify(ok=True, summary=summary, segments=seg)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/recommendations")
def api_ai_recommendations():
    """Leitet konkrete Handlungsempfehlungen aus den Daten ab."""
    recs = []
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
        with db_conn() as conn:
            # chronische Versager → pausieren
            chronic = conn.execute(
                "SELECT username, COUNT(*) AS n, "
                "SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok "
                "FROM recording_attempts WHERE started_at >= ? GROUP BY username "
                "HAVING n >= 5 AND (100.0*ok/n) < 15 ORDER BY n DESC", (cut,)).fetchall()
            for c in chronic[:8]:
                recs.append({"action": "pause_or_check", "priority": "high",
                             "target": c["username"],
                             "title": f"@{c['username']} pausieren oder prüfen",
                             "reason": f"{c['n']} Versuche, <15% Erfolg — verbrennt Ressourcen."})
            # dominanter 403 → Cookies
            forb = conn.execute(
                "SELECT COUNT(*) AS n FROM recording_attempts WHERE outcome='forbidden_403' "
                "AND started_at >= ?", (cut,)).fetchone()["n"]
            tot = conn.execute(
                "SELECT COUNT(*) AS n FROM recording_attempts WHERE started_at >= ?",
                (cut,)).fetchone()["n"]
            if tot and forb / tot > 0.2:
                recs.append({"action": "refresh_cookies", "priority": "high", "target": None,
                             "title": "TikTok-Cookies erneuern",
                             "reason": f"{round(100.0*forb/tot)}% der Versuche sind 403/Forbidden."})
            # reliable high-value → priorisieren (VIP)
            top = conn.execute(
                "SELECT username, COUNT(*) AS n, "
                "SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok "
                "FROM recording_attempts WHERE started_at >= ? GROUP BY username "
                "HAVING n >= 5 AND (100.0*ok/n) >= 80 ORDER BY ok DESC LIMIT 3", (cut,)).fetchall()
            for t in top:
                recs.append({"action": "prioritize", "priority": "low", "target": t["username"],
                             "title": f"@{t['username']} als VIP priorisieren",
                             "reason": f"Sehr zuverlässig ({t['ok']}/{t['n']} ok) — schnelleres Polling lohnt."})
        if not recs:
            recs.append({"action": "none", "priority": "info", "target": None,
                         "title": "Keine dringenden Empfehlungen",
                         "reason": "Das System läuft im erwarteten Rahmen."})
        return jsonify(ok=True, count=len(recs), recommendations=recs)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/report")
def api_ai_report():
    """Klartext-Zusammenfassung der Aktivität (period=day|week). Nutzt die LLM
       wenn verfügbar, sonst eine Template-Zusammenfassung. Reiner Lesebericht."""
    period = (request.args.get("period") or "day").lower()
    days = 7 if period == "week" else 1
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with db_conn() as conn:
            a = conn.execute(
                "SELECT COUNT(*) AS att, "
                "SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok, "
                "SUM(CASE WHEN outcome NOT IN ('running','cancelled') THEN 1 ELSE 0 END) AS done "
                "FROM recording_attempts WHERE started_at >= ?", (cut,)).fetchone()
            recs = conn.execute(
                "SELECT COUNT(*) AS n, COALESCE(SUM(file_size),0)/1048576.0 AS mb "
                "FROM recordings WHERE created_at >= ?", (cut,)).fetchone()
            topfail = conn.execute(
                "SELECT outcome, COUNT(*) AS n FROM recording_attempts "
                "WHERE outcome NOT IN ('ok','stall_killed_partial','running','cancelled') "
                "AND started_at >= ? GROUP BY outcome ORDER BY n DESC LIMIT 1", (cut,)).fetchone()
        att, ok_n, done = int(a["att"] or 0), int(a["ok"] or 0), int(a["done"] or 0)
        rate = round(100.0 * ok_n / done, 1) if done else 0.0
        stats = {"period": period, "attempts": att, "successes": ok_n,
                 "success_rate": rate, "recordings": int(recs["n"] or 0),
                 "stored_mb": round(recs["mb"] or 0),
                 "top_failure": (topfail["outcome"] if topfail else None)}
        # Template-Text (immer vorhanden)
        zr = "Woche" if days == 7 else "24 Stunden"
        text = (f"In den letzten {zr}: {att} Aufnahmeversuche, davon {ok_n} erfolgreich "
                f"({rate}% der abgeschlossenen). {stats['recordings']} Aufnahmen gespeichert "
                f"(~{stats['stored_mb']} MB).")
        if topfail:
            text += f" Häufigster Fehler: {topfail['outcome']}."
        # Optional: LLM-Verfeinerung
        if _c().cfg["EVOLUTION_USE_LLM"]:
            try:
                t2, err = _c().llm_chat_sync(
                    [{"role": "system", "content": "Formuliere einen knappen, sachlichen "
                      "deutschen Statusbericht (2-3 Sätze) aus diesen Kennzahlen. Keine Floskeln."},
                     {"role": "user", "content": json.dumps(stats, ensure_ascii=False)}],
                    timeout=30)
                if t2 and len(t2.strip()) > 20:
                    text = t2.strip()
            except Exception:
                pass
        return jsonify(ok=True, stats=stats, report=text)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/retry-advice/<username>")
def api_ai_retry_advice(username):
    """Empfiehlt eine Retry-/Backoff-Strategie anhand des Fehlermusters."""
    username = username.lstrip("@")
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT outcome, COUNT(*) AS n FROM recording_attempts "
                "WHERE username=? AND started_at >= ? GROUP BY outcome ORDER BY n DESC",
                (username, cut)).fetchall()
        by = {r["outcome"]: int(r["n"]) for r in rows}
        total = sum(by.values())
        if total < 3:
            return jsonify(ok=True, username=username, samples=total,
                           advice="Zu wenig Historie für eine Empfehlung.")
        dom = max((k for k in by if k not in ("ok", "stall_killed_partial", "running", "cancelled")),
                  key=lambda k: by[k], default=None)
        tips = {
            "early_disconnect": "Aggressive Retries bremsen — Backoff erhöhen; Cookies/Proxy prüfen.",
            "forbidden_403": "Retries bringen nichts ohne frische Cookies — erst Cookies erneuern.",
            "stream_dead": "URL-Refresh-Margin erhöhen; bei 404 schnell aufhören statt zu hämmern.",
            "hevc_unsupported": "PREFER_H264 sicherstellen; sonst dauerhaft chancenlos → pausieren.",
            "codec_header_fail": "Meist Input-Problem — selten lösbar durch Retry; ffmpeg-Upgrade.",
            "offline_or_protected": "Live-Detection-Timing — moderater Backoff reicht.",
        }
        advice = tips.get(dom, "Kein klares Muster — Standard-Backoff beibehalten.")
        return jsonify(ok=True, username=username, samples=total,
                       dominant_failure=dom, breakdown=by, advice=advice)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/forecast-storage")
def api_ai_forecast_storage():
    """Schätzt anhand der jüngsten Wachstumsrate, wann die Platte voll ist."""
    try:
        import shutil as _sh
        rec_dir = _c().recordings_dir if os.path.isdir(_c().recordings_dir) else "."
        usage = _sh.disk_usage(rec_dir)
        free_gb = usage.free / 1024 ** 3
        cut = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        with db_conn() as conn:
            mb7 = conn.execute(
                "SELECT COALESCE(SUM(file_size),0)/1048576.0 AS mb FROM recordings WHERE created_at >= ?",
                (cut,)).fetchone()["mb"]
        per_day_gb = (mb7 / 1024.0) / 7.0
        days_left = round(free_gb / per_day_gb) if per_day_gb > 0.01 else None
        driver = None
        if per_day_gb > 0.01:
            with db_conn() as conn:
                top = conn.execute(
                    "SELECT username, ROUND(SUM(file_size)/1048576.0,1) AS mb FROM recordings "
                    "WHERE created_at >= ? GROUP BY username ORDER BY mb DESC LIMIT 1",
                    (cut,)).fetchone()
            driver = {"username": top["username"], "mb_7d": top["mb"]} if top else None
        return jsonify(ok=True, free_gb=round(free_gb, 1),
                       growth_gb_per_day=round(per_day_gb, 2),
                       days_until_full=days_left, main_driver=driver,
                       note=("Stabil — kaum Wachstum." if days_left is None
                             else f"Bei aktuellem Tempo in ~{days_left} Tagen voll."))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/ai/health-score/<username>")
def api_ai_health_score(username):
    """Streamer-Scorecard (Composite)."""
    username = username.lstrip("@")
    try:
        with db_conn() as conn:
            return jsonify(ok=True, username=username, **_streamer_health(username, conn))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
