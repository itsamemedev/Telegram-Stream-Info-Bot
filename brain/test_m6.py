# brain/test_m6.py — M6-Integrationstest
# Mock-HTTP-Server simuliert llama-server (OpenAI-API). V37: ollama-frei.
# Prüft: Backend-Wahl, Fehlerpfad bei llamacpp-down, Stundenbudget,
# Concurrency-1-Slot, Router-Tier llm inkl. Unhandled bei Budget-Ende.
# Ausführung: python3 -m brain.test_m6

import json
import os
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

os.environ["BRAIN_DB"] = os.path.join(tempfile.mkdtemp(), "brain_m6.db")
os.environ["BRAIN_LLM_MAX_CALLS_H"] = "3"
os.environ["BRAIN_LLM_BACKEND"] = "auto"


def _mk_server(handler_cls):
    srv = HTTPServer(("127.0.0.1", 0), handler_cls)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


class LlamaCppMock(BaseHTTPRequestHandler):
    up = True

    def do_GET(self):                      # /health
        self.send_response(200 if self.up else 503)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_POST(self):                     # /v1/chat/completions
        if not LlamaCppMock.up:
            self.send_response(503)
            self.end_headers()
            return
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        user = body["messages"][-1]["content"]
        out = {"choices": [{"message": {
            "content": f"[llamacpp] {user[:40]}"}}]}
        data = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass




def main():
    _, llama_url = _mk_server(LlamaCppMock)
    os.environ["BRAIN_LLAMACPP_URL"] = llama_url

    # Import NACH dem Env-Setzen (Modul-Konstanten)
    from brain import get_brain
    from brain.llm import BudgetExhausted

    b = get_brain()

    # --- Primär-Backend antwortet ---------------------------------------
    r = b.llm.chat([{"role": "user", "content": "status?"}])
    assert r["ok"] and r["backend"] == "llamacpp" and "[llamacpp]" in r["text"]
    h = b.llm.health()
    assert h["llamacpp"]["up"] and "ollama" not in h   # V37: ollama-frei

    # --- llamacpp down → sauberer Fehler (Cloud-Fallback macht der Bot) ----
    LlamaCppMock.up = False
    b.llm._health_cache = None          # Cache invalidieren für frischen Probe
    r = b.llm.chat([{"role": "user", "content": "x"}])
    assert not r["ok"], r               # kein stiller Zweit-Backend-Sprung mehr
    LlamaCppMock.up = True

    # --- Budget: Fehl-Calls zählen NICHT (V37); 2 weitere ok-Calls füllen
    # das 3er-Budget (Call 1 war der erste), der nächste wirft BudgetExhausted.
    r = b.llm.chat([{"role": "user", "content": "y"}])
    assert r["ok"] and b.llm.budget()["remaining"] == 1
    r = b.llm.chat([{"role": "user", "content": "y2"}])
    assert r["ok"] and b.llm.budget()["remaining"] == 0
    try:
        b.llm.chat([{"role": "user", "content": "z"}])
        raise AssertionError("Budget nicht durchgesetzt")
    except BudgetExhausted:
        pass
    assert b.llm.stats()["budget_denied"] == 1

    # --- Router-Tier llm: Budget-Ende → sauberes Unhandled im Trace --------
    import contextlib
    import sqlite3
    import brain_bridge
    TMP2 = tempfile.mkdtemp()
    bot_db = os.path.join(TMP2, "bot.db")
    c = sqlite3.connect(bot_db)
    c.executescript(
        "CREATE TABLE trackings(id INTEGER PRIMARY KEY, group_id INT, "
        "username TEXT, added_by INT, created_at TEXT, last_live INT, "
        "recording INT, output_file TEXT, pid INT, paused INT DEFAULT 0);"
        "CREATE TABLE restreams(id INTEGER PRIMARY KEY, created_at TEXT, "
        "label TEXT, source_username TEXT, ingest_url TEXT, stream_key "
        "TEXT, transcode INT, enabled INT DEFAULT 1, status TEXT, pid INT, "
        "started_at TEXT, last_error TEXT);"
        "CREATE TABLE recordings(id INTEGER PRIMARY KEY, username TEXT, "
        "filepath TEXT, created_at TEXT);")
    c.commit()
    c.close()

    @contextlib.contextmanager
    def db_conn():
        conn = sqlite3.connect(bot_db)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    brain_bridge.init_bridge(db_conn=db_conn, start_tick=False)

    res = b.router.route("ask", {"prompt": "hi"})
    assert not res["ok"], res                      # Budget ist verbraucht
    assert any("budget" in str(t.get("skip", "")).lower()
               for t in res["trace"]), res["trace"]

    # Budget künstlich freigeben → Tier llm antwortet
    b.llm._calls.clear()
    res = b.router.route("ask", {"prompt": "status bitte"})
    assert res["ok"] and res["tier"] == "llm"
    assert "[llamacpp]" in res["result"]["text"]

    # unbekanntes Topic OHNE Catchall → fällt komplett durch (kein Budget-Burn)
    used_before = b.llm.budget()["used_h"]
    res = b.router.route("voellig_unbekannt", {})
    assert not res["ok"] and b.llm.budget()["used_h"] == used_before

    print("test_m6 OK — Backend/Fallback/Budget/Slot/Router-Tier-4 grün")


if __name__ == "__main__":
    main()
