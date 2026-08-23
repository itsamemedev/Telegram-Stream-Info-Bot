"""nc.intel.reel — Feature B: KI-Auto-Highlight-Reel.

Wählt aus den Transkript-Segmenten einer Aufnahme (nc.intel.transcripts) die
stärksten Momente und baut einen REEL-PLAN: eine geordnete, nicht überlappende
Cut-Liste mit Untertiteln + optionalem KI-Titel. Die eigentliche ffmpeg-Montage
macht ein dünner Adapter im Bot — hier NUR die Auswahllogik (pure, testbar).

Signale je Moment:
  • Inhalts-Salienz  — Länge/Wortreichtum des Segments (kurze „ja"/„okay" raus).
  • Hot-Marker       — Nähe zu injizierten „heißen" Zeitpunkten (Chat-Ausschläge
                       aus dem Highlight-Radar bzw. Audio-Energie).
  • Keyword-Boost    — optionale Reizwörter (Gewinn, krass, Drama, …).

Abhängigkeiten (LLM für Untertitel/Titel) werden injiziert → ohne Bot testbar.
"""
from __future__ import annotations

import re
from typing import Callable, Optional

from . import transcripts as T

# leichte, sprachneutrale Reizwörter; per annotate/DI erweiterbar
DEFAULT_KEYWORDS = (
    "gewonnen", "gewinn", "krass", "wahnsinn", "unglaublich", "endlich", "achtung",
    "drama", "skandal", "wow", "nein", "oh mein gott", "omg", "rekord", "world record",
    "insane", "clutch", "let's go", "lets go", "no way", "boom",
)

_WORD = re.compile(r"\w+", re.UNICODE)


def _content_score(text: str) -> float:
    """Wortreiche, ganze Sätze > Füllwörter. 0..~1.4."""
    words = _WORD.findall(text or "")
    n = len(words)
    if n < 3:
        return 0.0
    # sättigt bei ~18 Wörtern; Satzzeichen (?, !) geben einen kleinen Bonus
    base = min(1.0, n / 18.0)
    if any(c in (text or "") for c in "!?"):
        base += 0.15
    return base


def _keyword_boost(text: str, keywords) -> float:
    low = (text or "").lower()
    hits = sum(1 for kw in keywords if kw in low)
    return min(0.9, 0.3 * hits)


def _hot_boost(t_start: float, t_end: float, hot_ts, radius: float = 8.0) -> float:
    """Nähe zu einem heißen Zeitpunkt (Chat-Explosion/Energie). 0..1."""
    if not hot_ts:
        return 0.0
    best = 0.0
    mid = (t_start + t_end) / 2.0
    for ht in hot_ts:
        d = abs(mid - float(ht))
        if d <= radius:
            best = max(best, 1.0 - d / radius)
    return best


def score_moments(segments, hot_ts=None, keywords=None) -> list:
    """Jedes Segment bewerten. Rückgabe absteigend sortiert:
       [{t_start, t_end, text, score, parts:{content,keyword,hot}}]."""
    kw = tuple(keywords) if keywords else DEFAULT_KEYWORDS
    out = []
    for s in segments or []:
        text = (s.get("text") or "").strip()
        cs = _content_score(text)
        if cs <= 0:
            continue
        kb = _keyword_boost(text, kw)
        hb = _hot_boost(s.get("start", 0), s.get("end", 0), hot_ts or [])
        score = round(cs + kb + 1.2 * hb, 4)   # Hot-Marker wiegen am schwersten
        out.append({"t_start": float(s.get("start") or 0),
                    "t_end": float(s.get("end") or 0),
                    "text": text, "score": score,
                    "parts": {"content": round(cs, 3), "keyword": round(kb, 3),
                              "hot": round(hb, 3)}})
    out.sort(key=lambda m: m["score"], reverse=True)
    return out


def select_highlights(scored, max_clips: int = 6, min_gap_s: float = 20.0,
                      pad_pre: float = 3.0, pad_post: float = 3.0,
                      min_len: float = 4.0, max_len: float = 30.0) -> list:
    """Aus den bewerteten Momenten die besten NICHT überlappenden wählen,
       Fenster mit Vor-/Nachlauf padden, chronologisch zurückgeben."""
    picked = []
    for m in scored:
        if len(picked) >= max_clips:
            break
        mid = (m["t_start"] + m["t_end"]) / 2.0
        if any(abs(mid - (p["t_start"] + p["t_end"]) / 2.0) < min_gap_s for p in picked):
            continue
        start = max(0.0, m["t_start"] - pad_pre)
        end = m["t_end"] + pad_post
        if end - start < min_len:
            end = start + min_len
        if end - start > max_len:
            end = start + max_len
        picked.append({"t_start": round(start, 2), "t_end": round(end, 2),
                       "text": m["text"], "score": m["score"]})
    picked.sort(key=lambda p: p["t_start"])
    return picked


def caption_prompt(text: str) -> str:
    return ("Formuliere einen sehr kurzen, packenden deutschen Untertitel (max. 6 Wörter, "
            "kein Emoji, keine Anführungszeichen) für diesen Stream-Moment:\n\"" +
            (text or "")[:300] + "\"")


def title_prompt(texts) -> str:
    joined = " / ".join(t[:120] for t in texts[:6])
    return ("Gib einen kurzen, catchy deutschen Titel (max. 8 Wörter, kein Emoji, keine "
            "Anführungszeichen) für ein Highlight-Reel aus diesen Momenten:\n" + joined)


def _clean_line(s: str, max_words: int) -> str:
    s = (s or "").strip().strip('"').strip("„").strip("“").splitlines()[0] if s else ""
    words = s.split()
    return " ".join(words[:max_words]).strip()


def build_plan(recording_id: int, highlights, title: str = None,
               source_path: str = None) -> dict:
    """Reel-Plan aus gewählten Highlights: Cut-Liste + Gesamtdauer."""
    clips = [{"index": i, "start": h["t_start"], "end": h["t_end"],
              "dur": round(h["t_end"] - h["t_start"], 2),
              "caption": h.get("caption", ""), "text": h.get("text", ""),
              "score": h.get("score")}
             for i, h in enumerate(highlights)]
    return {"ok": bool(clips), "recording_id": recording_id, "title": title or "",
            "source_path": source_path or "",
            "clips": clips, "clip_count": len(clips),
            "total_s": round(sum(c["dur"] for c in clips), 2)}


def annotate(highlights, llm_fn: Optional[Callable[[str], str]] = None,
             make_title: bool = True) -> tuple:
    """Untertitel je Highlight + optional einen Reel-Titel per injiziertem
       llm_fn(prompt)->str erzeugen. Ohne llm_fn: unverändert (leere Captions)."""
    title = ""
    if llm_fn is None:
        return highlights, title
    for h in highlights:
        try:
            h["caption"] = _clean_line(llm_fn(caption_prompt(h.get("text", ""))), 6)
        except Exception:  # noqa: BLE001
            h["caption"] = ""
    if make_title and highlights:
        try:
            title = _clean_line(llm_fn(title_prompt([h.get("text", "") for h in highlights])), 8)
        except Exception:  # noqa: BLE001
            title = ""
    return highlights, title


def plan_from_transcript(conn, recording_id: int, hot_ts=None, keywords=None,
                         max_clips: int = 6, llm_fn=None, source_path: str = None,
                         paramstyle: str = "qmark") -> dict:
    """End-to-End (pure): Transkript → Bewertung → Auswahl → (Untertitel) → Plan."""
    segs = T.get_segments(conn, recording_id, paramstyle)
    if not segs:
        return {"ok": False, "error": "kein Transkript — erst indizieren", "clips": []}
    scored = score_moments(segs, hot_ts=hot_ts, keywords=keywords)
    picks = select_highlights(scored, max_clips=max_clips)
    picks, title = annotate(picks, llm_fn=llm_fn)
    return build_plan(recording_id, picks, title=title, source_path=source_path)
