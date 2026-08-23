"""nc.intel.transcripts — Transkript-Segmente je Aufnahme (gemeinsames Substrat).

Speichert zeitgestempelte Segmente ([start, end, text]) pro recording_id in einer
Seiten-Tabelle — die bestehende `recordings`-Tabelle wird NICHT angefasst
(Monolith-schonend, rückwärtskompatibel). Alle drei Flaggschiff-Features bauen
darauf auf: das Archiv indiziert die Segmente semantisch, das Reel wählt
Segmente aus, der Copilot füttert Live-Segmente ein.

DB-agnostisch: Funktionen bekommen eine DBAPI-Connection. Platzhalterstil wird
über `paramstyle` gewählt ("qmark" → ?, "format" → %s), Default sqlite.
Kein Import aus bot.py — dadurch ohne den Bot testbar.
"""
from __future__ import annotations

import time
from typing import Callable, Iterable, Optional

# ---- Status-Konstanten -------------------------------------------------------
PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"


def _ph(paramstyle: str) -> str:
    return "%s" if paramstyle == "format" else "?"


def _q(sql: str, paramstyle: str) -> str:
    """Übersetzt ?-Platzhalter in den Zielstil (nur wenn 'format' gewünscht)."""
    return sql.replace("?", "%s") if paramstyle == "format" else sql


def ensure_schema(conn, paramstyle: str = "qmark") -> None:
    """Legt die beiden Seiten-Tabellen an (idempotent). AUTOINCREMENT-frei, damit
       sqlite und MariaDB dieselbe DDL vertragen."""
    cur = conn.cursor()
    is_my = paramstyle == "format"
    pk = "BIGINT AUTO_INCREMENT PRIMARY KEY" if is_my else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur.execute(
        "CREATE TABLE IF NOT EXISTS intel_transcript_meta ("
        " recording_id BIGINT PRIMARY KEY,"
        " status VARCHAR(16) NOT NULL,"
        " lang VARCHAR(8),"
        " seg_count INTEGER DEFAULT 0,"
        " duration_s DOUBLE DEFAULT 0,"
        " indexed INTEGER DEFAULT 0,"
        " error TEXT,"
        " updated_at DOUBLE)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS intel_transcript_seg ("
        " id " + pk + ","
        " recording_id BIGINT NOT NULL,"
        " seg_index INTEGER NOT NULL,"
        " t_start DOUBLE NOT NULL,"
        " t_end DOUBLE NOT NULL,"
        " text TEXT NOT NULL)")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_intel_seg_rec "
                "ON intel_transcript_seg(recording_id)")
    conn.commit()


def set_status(conn, recording_id: int, status: str, *, lang: str = None,
               seg_count: int = None, duration_s: float = None,
               error: str = None, indexed: int = None,
               paramstyle: str = "qmark") -> None:
    """Upsert der Meta-Zeile. Nur übergebene Felder werden gesetzt."""
    now = time.time()
    cur = conn.cursor()
    row = cur.execute(_q("SELECT recording_id FROM intel_transcript_meta "
                         "WHERE recording_id=?", paramstyle),
                      (recording_id,)).fetchone()
    if row is None:
        cur.execute(_q("INSERT INTO intel_transcript_meta"
                       "(recording_id,status,lang,seg_count,duration_s,indexed,error,updated_at)"
                       " VALUES(?,?,?,?,?,?,?,?)", paramstyle),
                    (recording_id, status, lang or "", seg_count or 0,
                     duration_s or 0, indexed or 0, error, now))
    else:
        sets, args = ["status=?", "updated_at=?"], [status, now]
        if lang is not None:
            sets.append("lang=?"); args.append(lang)
        if seg_count is not None:
            sets.append("seg_count=?"); args.append(seg_count)
        if duration_s is not None:
            sets.append("duration_s=?"); args.append(duration_s)
        if error is not None:
            sets.append("error=?"); args.append(error)
        if indexed is not None:
            sets.append("indexed=?"); args.append(indexed)
        args.append(recording_id)
        cur.execute(_q("UPDATE intel_transcript_meta SET " + ",".join(sets) +
                       " WHERE recording_id=?", paramstyle), args)
    conn.commit()


def save_segments(conn, recording_id: int, segments: Iterable[dict],
                  lang: str = None, paramstyle: str = "qmark") -> int:
    """Ersetzt die Segmente einer Aufnahme und setzt den Status auf DONE.
       segments: iterable von {"start","end","text"}. Leere Texte werden
       verworfen. Gibt die Anzahl gespeicherter Segmente zurück."""
    cur = conn.cursor()
    cur.execute(_q("DELETE FROM intel_transcript_seg WHERE recording_id=?", paramstyle),
                (recording_id,))
    n, dur = 0, 0.0
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        st = float(seg.get("start") or 0)
        en = float(seg.get("end") or st)
        cur.execute(_q("INSERT INTO intel_transcript_seg"
                       "(recording_id,seg_index,t_start,t_end,text) VALUES(?,?,?,?,?)",
                       paramstyle),
                    (recording_id, n, st, en, text[:2000]))
        n += 1
        dur = max(dur, en)
    conn.commit()
    set_status(conn, recording_id, DONE, lang=lang, seg_count=n,
               duration_s=dur, error="", paramstyle=paramstyle)
    return n


def get_segments(conn, recording_id: int, paramstyle: str = "qmark") -> list:
    cur = conn.cursor()
    rows = cur.execute(_q("SELECT seg_index,t_start,t_end,text FROM intel_transcript_seg"
                          " WHERE recording_id=? ORDER BY seg_index", paramstyle),
                       (recording_id,)).fetchall()
    return [{"i": r[0], "start": r[1], "end": r[2], "text": r[3]} for r in rows]


def full_text(conn, recording_id: int, paramstyle: str = "qmark") -> str:
    return " ".join(s["text"] for s in get_segments(conn, recording_id, paramstyle))


def get_meta(conn, recording_id: int, paramstyle: str = "qmark") -> Optional[dict]:
    cur = conn.cursor()
    r = cur.execute(_q("SELECT recording_id,status,lang,seg_count,duration_s,indexed,error,updated_at"
                       " FROM intel_transcript_meta WHERE recording_id=?", paramstyle),
                    (recording_id,)).fetchone()
    if not r:
        return None
    return {"recording_id": r[0], "status": r[1], "lang": r[2], "seg_count": r[3],
            "duration_s": r[4], "indexed": bool(r[5]), "error": r[6], "updated_at": r[7]}


def pending_ids(conn, candidate_ids: Iterable[int], paramstyle: str = "qmark") -> list:
    """Aus einer Kandidatenliste (z. B. neueste Aufnahmen) die zurückgeben, die
       noch KEIN abgeschlossenes Transkript haben — die Arbeitsliste des
       Hintergrund-Transkribierers."""
    cand = [int(x) for x in candidate_ids]
    if not cand:
        return []
    cur = conn.cursor()
    done = set()
    # in Blöcken, um IN-Listen-Limits zu meiden
    for i in range(0, len(cand), 400):
        chunk = cand[i:i + 400]
        marks = ",".join([_ph(paramstyle)] * len(chunk))
        rows = cur.execute(
            "SELECT recording_id FROM intel_transcript_meta "
            "WHERE status=" + _ph(paramstyle) + " AND recording_id IN (" + marks + ")",
            [DONE] + chunk).fetchall()
        done.update(r[0] for r in rows)
    return [x for x in cand if x not in done]


def stats(conn, paramstyle: str = "qmark") -> dict:
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM intel_transcript_meta").fetchone()[0]
    done = cur.execute(_q("SELECT COUNT(*) FROM intel_transcript_meta WHERE status=?",
                          paramstyle), (DONE,)).fetchone()[0]
    indexed = cur.execute("SELECT COUNT(*) FROM intel_transcript_meta WHERE indexed=1").fetchone()[0]
    segs = cur.execute("SELECT COUNT(*) FROM intel_transcript_seg").fetchone()[0]
    return {"recordings": total, "transcribed": done, "indexed": indexed, "segments": segs}


def transcribe_and_store(conn, recording_id: int, path: str,
                         segment_fn: Callable[[str], list],
                         lang: str = None, paramstyle: str = "qmark") -> dict:
    """Orchestrierung (synchron, DI): segment_fn(path) -> [{"start","end","text"}].
       Der Bot reicht seinen Whisper-Segment-Adapter rein. Fehler werden als
       Status FAILED persistiert und als dict zurückgegeben (wirft nicht)."""
    set_status(conn, recording_id, RUNNING, paramstyle=paramstyle)
    try:
        segs = segment_fn(path) or []
    except Exception as e:  # noqa: BLE001
        set_status(conn, recording_id, FAILED, error=str(e)[:400], paramstyle=paramstyle)
        return {"ok": False, "error": str(e)[:400], "recording_id": recording_id}
    n = save_segments(conn, recording_id, segs, lang=lang, paramstyle=paramstyle)
    return {"ok": True, "recording_id": recording_id, "segments": n}
