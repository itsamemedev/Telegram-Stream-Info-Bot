# brain/semantic.py — V37-W-PLUS: semantisches Gedächtnis.
# Embeddings über die vorhandene lokale Infrastruktur (llama.cpp /embedding,
# alternativ llama.cpp /embedding), Vektoren als BLOB in brain.db, Suche als
# Pure-Python-Cosine (bei wenigen zehntausend Einträgen auf 8 Cores völlig
# ausreichend — kein numpy, keine neue Abhängigkeit).
#
# Env:
#   BRAIN_EMBED_BACKEND = llamacpp | off   (default llamacpp; V37: ollama entfernt)
#   BRAIN_EMBED_URL     = http://127.0.0.1:8089      (llama-server --embedding)
#   BRAIN_EMBED_MAX     = 20000                      (Vektor-Obergrenze, FIFO)

from __future__ import annotations

import array
import json
import logging
import math
import os
import threading
import time
import urllib.request

log = logging.getLogger("brain.semantic")


def _env(k: str, d: str) -> str:
    return (os.getenv(k, d) or d).strip()


def _aus() -> bool:
    return _env("BRAIN_EMBED_BACKEND", "llamacpp").lower() in ("off", "none", "0")


# v4.2-W177: Meldedrossel des Embedding-Kanals. Der Server auf :8089 wird
# nicht mitgeliefert, und jeder Fehler stand bis hierher auf log.debug — der
# Ingest der Stream-Erinnerungen brach jede Runde still ab, "Frag dein
# Archiv" fand nichts, und im Log stand nichts. Erste Meldung und jeder neue
# Grund sofort, sonst hoechstens alle 15 min (nc.meldetakt, Schluessel =
# Kanal). Der Erfolgspfad setzt zurueck.
_KANAL = "brain-embed"
ABHILFE = ("Abhilfe: einen Embedding-Server auf BRAIN_EMBED_URL starten "
           "(llama-server --embedding -m <embedding-modell.gguf> --port 8089) "
           "oder BRAIN_EMBED_BACKEND=off setzen — dann bleibt das semantische "
           "Gedaechtnis bewusst aus und meldet nichts.")


def _embed_fehler(grund: str, detail: str, url: str) -> None:
    from nc import meldetakt as _mt      # lokal: brain/ bleibt ohne nc importierbar
    laut, unterdrueckt = _mt.melden(_KANAL, grund, time.time())
    if laut:
        log.warning("Embedding fehlgeschlagen (%s) unter %s: %s. %s%s",
                    grund, url, detail, ABHILFE, _mt.zusatz(unterdrueckt))


class SemanticMemory:
    def __init__(self, conn_factory, db_lock):
        self._conn = conn_factory
        self._lock = db_lock
        self._emb_lock = threading.Lock()   # ein Embed-Call zur Zeit (CPU)
        self.letzter_fehler = None          # v4.2-W177: fuer stats()/Deck
        with self._lock, self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS sem_vectors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL, kind TEXT, username TEXT, ref TEXT,
                text TEXT, dim INTEGER, vec BLOB)""")
            c.execute("CREATE INDEX IF NOT EXISTS ix_sem_user "
                      "ON sem_vectors(username, ts)")
            c.execute("""CREATE TABLE IF NOT EXISTS sem_cursor(
                name TEXT PRIMARY KEY, last_id INTEGER)""")

    # ---------------- Embedding-Backend ----------------
    def aktiv(self) -> bool:
        """False bei BRAIN_EMBED_BACKEND=off — ein gewollter, stiller Zustand."""
        return not _aus()

    def _embed(self, text: str):
        if _aus():
            return None
        text = (text or "").strip()[:2000]
        if not text:
            return None
        url = _env("BRAIN_EMBED_URL", "http://127.0.0.1:8089")
        with self._emb_lock:
            try:
                # V37: nur noch llama.cpp (llama-server --embedding); Ollama entfernt.
                req = urllib.request.Request(
                    url.rstrip("/") + "/embedding",
                    data=json.dumps({"content": text}).encode(),
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    j = json.loads(r.read().decode())
                vec = j.get("embedding") or (j[0].get("embedding")
                                             if isinstance(j, list) else None)
                if not vec:
                    self.letzter_fehler = "leere Antwort"
                    _embed_fehler("leer", "Antwort ohne 'embedding' — laeuft dort "
                                  "ein Chat-Server ohne --embedding?", url)
                    return None
                # llama-server mit --pooling none liefert je Token einen
                # Vektor (Liste von Listen) — dann den ersten nehmen statt an
                # sum(x*x) mit TypeError zu sterben.
                if vec and isinstance(vec[0], list):
                    vec = vec[0]
                # Normieren → Cosine wird zum Skalarprodukt
                n = math.sqrt(sum(x * x for x in vec)) or 1.0
                self.letzter_fehler = None
                from nc import meldetakt as _mt
                _mt.zuruecksetzen(_KANAL)
                return [x / n for x in vec]
            except Exception as e:
                self.letzter_fehler = f"{type(e).__name__}: {e}"
                _embed_fehler(type(e).__name__, str(e)[:200], url)
                return None

    # ---------------- Schreiben ----------------
    def index_text(self, kind: str, username: str, text: str,
                   ref: str = "", ts: float = None) -> bool:
        vec = self._embed(text)
        if vec is None:
            return False
        blob = array.array("f", vec).tobytes()
        with self._lock, self._conn() as c:
            c.execute("INSERT INTO sem_vectors(ts,kind,username,ref,text,dim,vec) "
                      "VALUES(?,?,?,?,?,?,?)",
                      (ts or time.time(), kind, (username or "").lstrip("@").lower(),
                       ref, text[:2000], len(vec), blob))
            # FIFO-Deckel
            cap = int(_env("BRAIN_EMBED_MAX", "20000"))
            n = c.execute("SELECT COUNT(*) FROM sem_vectors").fetchone()[0]
            if n > cap:
                c.execute("DELETE FROM sem_vectors WHERE id IN "
                          "(SELECT id FROM sem_vectors ORDER BY id LIMIT ?)",
                          (n - cap,))
        return True

    def cursor(self, name: str, new_val: int = None) -> int:
        with self._lock, self._conn() as c:
            if new_val is not None:
                c.execute("INSERT INTO sem_cursor(name,last_id) VALUES(?,?) "
                          "ON CONFLICT(name) DO UPDATE SET last_id=excluded.last_id",
                          (name, int(new_val)))
                return int(new_val)
            row = c.execute("SELECT last_id FROM sem_cursor WHERE name=?",
                            (name,)).fetchone()
            return int(row[0]) if row else 0

    # ---------------- Suche ----------------
    def search(self, query: str, k: int = 5, username: str = None) -> dict:
        qv = self._embed(query)
        if qv is None:
            return {"ok": False, "error": "Embedding-Backend nicht erreichbar "
                    "(BRAIN_EMBED_BACKEND/URL/MODEL prüfen; z.B. "
                    "llama-server --embedding auf BRAIN_EMBED_URL starten)", "hits": []}
        sql = "SELECT ts,kind,username,ref,text,dim,vec FROM sem_vectors"
        args = ()
        if username:
            sql += " WHERE username=?"
            args = ((username or "").lstrip("@").lower(),)
        with self._lock, self._conn() as c:
            rows = c.execute(sql, args).fetchall()
        hits = []
        for ts, kind, user, ref, text, dim, blob in rows:
            if dim != len(qv):
                continue
            v = array.array("f")
            v.frombytes(blob)
            score = sum(a * b for a, b in zip(qv, v, strict=True))
            hits.append((score, ts, kind, user, ref, text))
        hits.sort(key=lambda h: h[0], reverse=True)
        return {"ok": True, "hits": [
            {"score": round(s, 4), "ts": ts, "kind": kind, "username": u,
             "ref": ref, "text": t} for s, ts, kind, u, ref, t in hits[:k]]}

    def stats(self) -> dict:
        with self._lock, self._conn() as c:
            n = c.execute("SELECT COUNT(*) FROM sem_vectors").fetchone()[0]
            u = c.execute("SELECT COUNT(DISTINCT username) FROM sem_vectors").fetchone()[0]
        return {"vectors": n, "users": u,
                "backend": _env("BRAIN_EMBED_BACKEND", "llamacpp"),
                # v4.2-W177: "nichts indiziert" und "Backend tot" unterscheiden
                "letzter_fehler": getattr(self, "letzter_fehler", None),
                "model": _env("BRAIN_EMBED_MODEL", "nomic-embed-text")}
