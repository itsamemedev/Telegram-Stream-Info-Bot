"""nc.intel.library — Feature A: Semantisches Stream-Archiv („Frag dein Archiv").

Indiziert Transkript-Segmente (aus nc.intel.transcripts) semantisch und
beantwortet Bedeutungs-Suchen: „Wann ging es um X?" → Trefferliste mit
recording_id + Zeitstempel (Sprung direkt in den Clip).

Nutzt das vorhandene semantische Gedächtnis (brain.semantic.SemanticMemory) über
eine schmale, injizierte Schnittstelle — KEIN harter Import, damit unit-testbar
mit einem Fake-Backend. Erwartete Backend-API:

    backend.index_text(kind, username, text, ref="", ts=None) -> bool
    backend.search(query, k=?, username=None) -> {"ok":bool, "hits":[{ref,text,score,...}]}

Segment-Referenz-Format:  rec:<recording_id>:<t_start_int>
"""
from __future__ import annotations

import re

from . import transcripts as T

KIND = "recording"
_REF = re.compile(r"^rec:(\d+):(\d+)$")


def make_ref(recording_id: int, t_start: float) -> str:
    return "rec:%d:%d" % (int(recording_id), int(t_start or 0))


def parse_ref(ref: str):
    """rec:<id>:<t> -> (recording_id, t_start) oder None."""
    m = _REF.match(ref or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def index_recording(conn, backend, recording_id: int, username: str = "",
                    created_at: float = None, paramstyle: str = "qmark",
                    min_chars: int = 12) -> dict:
    """Alle Segmente einer Aufnahme in den semantischen Index schreiben.
       Sehr kurze Segmente (< min_chars) werden übersprungen (Rauschen wie „ja",
       „okay"). Setzt indexed=1 in der Meta. Gibt Zählwerte zurück."""
    segs = T.get_segments(conn, recording_id, paramstyle)
    if not segs:
        return {"ok": False, "error": "keine Segmente", "indexed": 0}
    done = 0
    for s in segs:
        text = (s["text"] or "").strip()
        if len(text) < min_chars:
            continue
        ref = make_ref(recording_id, s["start"])
        try:
            if backend.index_text(KIND, username or "", text, ref=ref, ts=created_at):
                done += 1
        except Exception:  # noqa: BLE001
            continue
    T.set_status(conn, recording_id, T.DONE, indexed=1, paramstyle=paramstyle)
    return {"ok": True, "indexed": done, "of": len(segs)}


def unindexed_ids(conn, candidate_ids, paramstyle: str = "qmark") -> list:
    """Aufnahmen mit fertigem Transkript, aber noch nicht semantisch indiziert."""
    cand = [int(x) for x in candidate_ids]
    if not cand:
        return []
    cur = conn.cursor()
    ph = "%s" if paramstyle == "format" else "?"
    out = []
    for i in range(0, len(cand), 400):
        chunk = cand[i:i + 400]
        marks = ",".join([ph] * len(chunk))
        rows = cur.execute(
            "SELECT recording_id FROM intel_transcript_meta "
            "WHERE status=" + ph + " AND indexed=0 AND recording_id IN (" + marks + ")",
            [T.DONE] + chunk).fetchall()
        out.extend(r[0] for r in rows)
    return out


def _context_snippet(conn, recording_id: int, t_start: int, paramstyle: str,
                     window: int = 1) -> str:
    """Kleiner Kontext um einen Treffer: das getroffene Segment plus je `window`
       Nachbarn — liest sich im UI besser als ein isolierter Fetzen."""
    segs = T.get_segments(conn, recording_id, paramstyle)
    if not segs:
        return ""
    idx = min(range(len(segs)), key=lambda i: abs(int(segs[i]["start"]) - t_start))
    lo, hi = max(0, idx - window), min(len(segs), idx + window + 1)
    return " ".join(s["text"] for s in segs[lo:hi]).strip()


def search(conn, backend, query: str, k: int = 8, username: str = None,
           paramstyle: str = "qmark", with_context: bool = True) -> dict:
    """Bedeutungs-Suche über alle transkribierten Aufnahmen.
       Rückgabe: {ok, query, hits:[{recording_id, t_start, score, text, context}]}.
       Filtert auf KIND='recording' und parst die Segment-Referenz zurück in
       recording_id + Zeitstempel."""
    q = (query or "").strip()
    if not q:
        return {"ok": False, "error": "leere Anfrage", "hits": []}
    try:
        res = backend.search(q, k=max(k * 3, 12), username=username)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": "Suche fehlgeschlagen: " + str(e)[:200], "hits": []}
    if not res or not res.get("ok"):
        return {"ok": False, "error": (res or {}).get("error", "Backend nicht erreichbar"),
                "hits": []}
    hits = []
    seen = set()
    for h in res.get("hits", []):
        if h.get("kind") and h.get("kind") != KIND:
            continue
        pr = parse_ref(h.get("ref", ""))
        if not pr:
            continue
        rid, t0 = pr
        key = (rid, t0)
        if key in seen:
            continue
        seen.add(key)
        item = {"recording_id": rid, "t_start": t0,
                "score": h.get("score"), "text": h.get("text", ""),
                "username": h.get("username", "")}
        if with_context:
            item["context"] = _context_snippet(conn, rid, t0, paramstyle)
        hits.append(item)
        if len(hits) >= k:
            break
    return {"ok": True, "query": q, "hits": hits}


def coverage(conn, backend=None, paramstyle: str = "qmark") -> dict:
    """Kennzahlen fürs Dashboard: wie viel des Archivs ist transkribiert/indiziert."""
    st = T.stats(conn, paramstyle)
    out = {"transcribed": st["transcribed"], "indexed": st["indexed"],
           "segments": st["segments"]}
    if backend is not None:
        try:
            out["backend"] = backend.stats() if hasattr(backend, "stats") else {}
        except Exception:  # noqa: BLE001
            out["backend"] = {}
    return out
