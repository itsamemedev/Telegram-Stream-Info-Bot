"""nc.fmt — reine Format-/Stream-Helfer (keine Bot-Abhängigkeiten).

Extrahiert aus bot_v37.py:
- _sse: Server-Sent-Events-Frame (json).
- _partial_tag_hold: hält am Chunk-Ende zurück, was Anfang eines <think>-Tags
  sein könnte (Stream-Parsing).
- _fmt_offset: Sekunden → H:MM:SS / MM:SS.
"""

import json
from datetime import datetime, timezone


def _sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _partial_tag_hold(buf, tag):
    """Wie viele Zeichen am Ende von buf könnten der Anfang von tag sein
       (damit ein über Chunks zerteiltes <think>/</think> nicht durchrutscht)."""
    for h in range(min(len(tag) - 1, len(buf)), 0, -1):
        if tag.startswith(buf[-h:]):
            return h
    return 0


def _fmt_offset(secs):
    s = max(0, int(secs or 0))
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return (f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}")


def fmt_duration(secs) -> str:
    if not secs or secs < 0:
        return "—"
    secs = int(secs)
    h, r = divmod(secs, 3600)
    m, s = divmod(r, 60)
    if h: return f"{h}h {m:02d}m"
    if m: return f"{m}m {s:02d}s"
    return f"{s}s"


def fmt_size_mb(mb) -> str:
    try:
        v = float(mb)
    except (TypeError, ValueError):
        return "—"
    if v < 1024:
        return f"{v:.1f} MB"
    return f"{v/1024:.2f} GB"


def utc_clock() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")

def pre_table(rows, label_w=10, align='right') -> str:
    """Baut eine Key-Value-Tabelle für <pre>-Block.
       align='right' für Zahlen (default), 'left' für Text-Identifier."""
    if not rows:
        return ""
    label_w = max(label_w, max(len(str(k)) for k, _ in rows))
    if align == 'right':
        val_w = max(len(str(v)) for _, v in rows)
        return "\n".join(
            f"{str(k).ljust(label_w)}  {str(v).rjust(val_w)}" for k, v in rows
        )
    return "\n".join(
        f"{str(k).ljust(label_w)}  {str(v)}" for k, v in rows
    )

