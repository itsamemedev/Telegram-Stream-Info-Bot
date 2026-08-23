"""Unit-Tests für nc.intel (Transkript-Substrat + semantisches Archiv).
Läuft ohne den Bot — Embedding-Backend wird gefaked. `python nc/intel/test_intel.py`."""
import math
import sqlite3
import sys

from nc.intel import library as L
from nc.intel import transcripts as T

P = 0


def ok(m):
    global P
    P += 1
    print("  \u2713", m)


class FakeSem:
    """Bag-of-words + Cosinus — spiegelt die SemanticMemory-API."""
    def __init__(self):
        self.rows = []

    def _v(self, t):
        d = {}
        for w in t.lower().replace(".", " ").split():
            d[w] = d.get(w, 0) + 1
        return d

    def index_text(self, kind, user, text, ref="", ts=None):
        self.rows.append((kind, user, ref, text, self._v(text)))
        return True

    def search(self, q, k=8, username=None):
        qv = self._v(q)
        hits = []
        for kind, u, ref, text, v in self.rows:
            keys = set(qv) | set(v)
            dot = sum(qv.get(x, 0) * v.get(x, 0) for x in keys)
            na = math.sqrt(sum(x * x for x in qv.values()))
            nb = math.sqrt(sum(x * x for x in v.values()))
            hits.append({"kind": kind, "username": u, "ref": ref, "text": text,
                         "score": round(dot / (na * nb) if na and nb else 0, 4)})
        hits.sort(key=lambda h: h["score"], reverse=True)
        return {"ok": True, "hits": hits[:k]}

    def stats(self):
        return {"vectors": len(self.rows)}


def main():
    conn = sqlite3.connect(":memory:")
    T.ensure_schema(conn)
    ok("Schema angelegt (idempotent)")
    T.ensure_schema(conn)  # zweimal → kein Fehler

    segs = [
        {"start": 0, "end": 5, "text": "Willkommen, heute kochen wir ein Rezept mit Nudeln."},
        {"start": 5, "end": 9, "text": "ja"},   # zu kurz zum Indexieren
        {"start": 9, "end": 15, "text": "Danach geht es um Politik und Nachrichten."},
    ]
    n = T.save_segments(conn, 7, segs, lang="de")
    assert n == 3, n
    ok("save_segments speichert 3 Segmente")
    assert "Nudeln" in T.full_text(conn, 7)
    ok("full_text zusammengesetzt")
    m = T.get_meta(conn, 7)
    assert m["status"] == T.DONE and m["seg_count"] == 3 and not m["indexed"]
    ok("Meta: status=done, seg_count=3, indexed=false")
    assert sorted(T.pending_ids(conn, [6, 7, 8])) == [6, 8]
    ok("pending_ids: nur nicht-transkribierte (6,8)")

    be = FakeSem()
    ix = L.index_recording(conn, be, 7, username="chef")
    assert ix["ok"] and ix["indexed"] == 2, ix   # 'ja' übersprungen
    ok("index_recording: 2 von 3 Segmenten (Kurz-Segment übersprungen)")
    assert T.get_meta(conn, 7)["indexed"] is True
    ok("Meta indexed-Flag gesetzt")
    assert L.unindexed_ids(conn, [7]) == []
    ok("unindexed_ids leer nach Index")

    r = L.search(conn, be, "Kochen Rezept Nudeln", k=3)
    assert r["ok"] and r["hits"], r
    top = r["hits"][0]
    assert top["recording_id"] == 7 and top["t_start"] == 0, top
    ok("search: Treffer → recording_id + t_start (Rezept @0)")
    assert top.get("context")
    ok("search: Kontext-Snippet vorhanden")

    r2 = L.search(conn, be, "Politik Nachrichten", k=2)
    assert r2["hits"][0]["t_start"] == 9, r2["hits"][0]
    ok("search: 'Politik' → t_start 9")

    assert L.parse_ref("rec:12:345") == (12, 345)
    assert L.parse_ref("kaputt") is None
    ok("parse_ref robust")

    r3 = L.search(conn, be, "", k=3)
    assert not r3["ok"]
    ok("search: leere Anfrage sauber abgelehnt")

    cov = L.coverage(conn, be)
    assert cov["transcribed"] == 1 and cov["indexed"] == 1 and cov["segments"] == 3
    ok("coverage-Kennzahlen korrekt")

    # transcribe_and_store mit injizierter Segment-Funktion (kein echtes Whisper)
    res = T.transcribe_and_store(conn, 9, "/tmp/fake.mp4",
                                 segment_fn=lambda p: [{"start": 0, "end": 2, "text": "Testlauf."}])
    assert res["ok"] and res["segments"] == 1
    ok("transcribe_and_store (DI) speichert Segmente")
    bad = T.transcribe_and_store(conn, 10, "/x",
                                 segment_fn=lambda p: (_ for _ in ()).throw(RuntimeError("boom")))
    assert not bad["ok"] and T.get_meta(conn, 10)["status"] == T.FAILED
    ok("transcribe_and_store: Fehler → Status FAILED, wirft nicht")

    _test_reel(conn)

    print(f"test_intel OK — {P} Checks grün")


def _test_reel(conn):
    from nc.intel import reel as R
    segs = [
        {"start": 0, "end": 3, "text": "ja"},                       # Füllwort → raus
        {"start": 3, "end": 9, "text": "Und dann haben wir tatsächlich das ganze Turnier gewonnen, unglaublich!"},
        {"start": 30, "end": 36, "text": "Jetzt reden wir ruhig über das Wetter und den Alltag heute."},
        {"start": 70, "end": 78, "text": "Achtung, das war der krasseste Moment des Streams, absolut wahnsinn!"},
    ]
    # Hot-Marker nahe Segment 4 (t~74) → soll es zusätzlich anheben
    scored = R.score_moments(segs, hot_ts=[74.0], keywords=None)
    assert scored and scored[0]["t_start"] in (3.0, 70.0)
    assert all(s["text"] != "ja" for s in scored)
    ok("reel.score_moments: Füllwort raus, Reizwort/Hot bewertet")
    # das Hot+Keyword-Segment (70-78) sollte vorn liegen
    assert scored[0]["t_start"] == 70.0, scored[0]
    ok("reel.score_moments: Hot-Marker + Reizwort gewinnt")

    picks = R.select_highlights(scored, max_clips=2, min_gap_s=20, pad_pre=3, pad_post=3)
    assert len(picks) == 2
    assert picks[0]["t_start"] <= picks[1]["t_start"]     # chronologisch
    assert picks[0]["t_start"] >= 0                        # Padding nicht negativ
    ok("reel.select_highlights: nicht überlappend, chronologisch, gepaddet")

    # DI-LLM: liefert deterministische „Untertitel"
    picks2, title = R.annotate([dict(p) for p in picks],
                               llm_fn=lambda prompt: "Turnier gewonnen und gefeiert")
    assert all(p["caption"] for p in picks2) and title
    assert all(len(p["caption"].split()) <= 6 for p in picks2)
    ok("reel.annotate: Untertitel (≤6 Wörter) + Titel per DI-LLM")

    plan = R.build_plan(501, picks2, title=title, source_path="/rec/501.mp4")
    assert plan["ok"] and plan["clip_count"] == 2 and plan["total_s"] > 0
    assert plan["clips"][0]["dur"] > 0 and "start" in plan["clips"][0]
    ok("reel.build_plan: gültige Cut-Liste + Gesamtdauer")

    # End-to-End aus dem Transkript-Store (Segmente von Aufnahme 7 existieren)
    e2e = R.plan_from_transcript(conn, 7, hot_ts=[], max_clips=3,
                                 llm_fn=lambda p: "Kurzer Untertitel hier")
    assert e2e["ok"] and e2e["clip_count"] >= 1
    ok("reel.plan_from_transcript: End-to-End-Plan aus dem Store")

    empty = R.plan_from_transcript(conn, 9999, max_clips=3)
    assert not empty["ok"]
    ok("reel.plan_from_transcript: ohne Transkript sauber abgelehnt")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
