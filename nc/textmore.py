"""nc.textmore — weitere reine Text-/Parse-Helfer.

Extrahiert aus bot_v37.py: Telegram-Nachrichten-Splitting, Text-Kompaktierung,
ISO-Datums-Parsing, sichere Archiv-Dateinamen, Video-Captions, Overlay-Umbruch."""

import os
import re
from datetime import datetime
from typing import List

from nc.fmt import fmt_duration, fmt_size_mb
from nc.textutil import safe

def split_for_telegram(text: str, limit: int = 4000) -> List[str]:
    """Splittet Text in Telegram-sichere Stücke (max 4096 chars), bevorzugt
       an Newline-Grenzen."""
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        if len(text) <= limit:
            chunks.append(text); break
        cut = text.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = limit
        chunks.append(text[:cut])
        text = text[cut:].lstrip()
    return chunks

def _compact_text(t, max_chars=3000):
    """V6: Whisper-Transkripte deduplizieren (aufeinanderfolgende Wiederholungen
       raus) und kappen — schärfere Prompts, weniger Rauschen/Token."""
    out, prev = [], None
    for line in (t or "").splitlines():
        s = " ".join(line.split())
        if s and s != prev:
            out.append(s)
            prev = s
    return "\n".join(out)[-max_chars:]

def _parse_iso(s):
    """Robustes ISO-8601-Parsing (mit 'Z'/Offset/Mikrosekunden). None bei Fehler."""
    if not s or not isinstance(s, str):
        return None
    t = s.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(t)
    except Exception:
        # Fallback: nur das Datum/Sekunden-Präfix versuchen
        try:
            return datetime.fromisoformat(t[:19])
        except Exception:
            return None

def _safe_archive_filename(orig: str) -> str:
    """Sanitize filename for safe filesystem use; preserve extension.
       Strip path components, control chars, problematic chars."""
    if not orig:
        return "upload.bin"
    base = os.path.basename(orig).strip()
    # Erlaubte Zeichen: alphanumerisch, ASCII-Punkt, Space, Bindestrich, Unterstrich, Klammern
    base = re.sub(r'[^\w. \-()]', '_', base, flags=re.ASCII)
    base = re.sub(r'_+', '_', base).strip('._- ')
    return base or "upload.bin"

def _video_caption(username: str, started_at, ended_at, size_mb,
                   part: int = None, total_parts: int = None) -> str:
    title = f"🎥 <b>@{safe(username)}</b>"
    if part and total_parts:
        title += f" · Teil {part}/{total_parts}"

    duration_secs = None
    if started_at and ended_at:
        duration_secs = (ended_at - started_at).total_seconds()

    bits = []
    if duration_secs is not None:
        bits.append(f"⏱ {fmt_duration(duration_secs)}")
    if size_mb is not None:
        bits.append(f"💾 {fmt_size_mb(size_mb)}")
    line2 = "  ·  ".join(bits)

    line3 = ""
    if started_at:
        line3 = f"<code>{started_at.strftime('%Y-%m-%d %H:%M')} UTC</code>"

    parts = [title]
    if line2: parts.append(f"<i>{line2}</i>")
    if line3: parts.append(line3)
    return "\n".join(parts)

def _ov_wrap(s, width=42, maxlines=2, ellipsis=False):
    """Wort-Umbruch in mehrere Zeilen — drawtext rendert \\n als echte Zeilen, sonst
       würde langer Text am rechten Rand abgeschnitten (Hochkant ist schmal).

       ellipsis=True: passt der Text NICHT in maxlines, endet die letzte Zeile
       mit »…« statt den Rest still wegzuwerfen. Ohne das sah der Zuschauer im
       Sendebild einen mitten im Satz abgeschnittenen Text mit hängendem Komma —
       er konnte nicht erkennen, dass da noch etwas fehlte. Ein sichtbares »…«
       sagt: hier geht es weiter, nur nicht im Overlay.
    """
    s = " ".join((s or "").split())
    if not s:
        return ""
    # Woerter, die breiter als eine ganze Zeile sind (URL, langer Name), hart
    # zerteilen — sonst zeichnet drawtext sie ueber den Bildrand hinaus. Bei
    # normalen AZRAEL-Antworten passiert das nie, aber ein durchgereichter Link
    # soll das Sendebild nicht sprengen.
    words = []
    for w in s.split(" "):
        while len(w) > width:
            words.append(w[:width])
            w = w[width:]
        words.append(w)
    lines, cur, truncated = [], "", False
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur); cur = w
            if len(lines) >= maxlines:
                # Es folgen noch Wörter, die nicht mehr passen
                truncated = True
                cur = ""
                break
    if cur and len(lines) < maxlines:
        lines.append(cur)
    lines = lines[:maxlines]

    if ellipsis and truncated and lines:
        last = lines[-1].rstrip(" ,;:—-")
        # Platz fürs »…« schaffen: notfalls das letzte Wort kürzen
        if len(last) + 1 > width:
            last = last[:max(0, width - 1)].rstrip(" ,;:—-")
        lines[-1] = last + "…"
    return "\n".join(lines)


_BANNED_CAP = 300


def configure_banned_cap(cap):
    global _BANNED_CAP
    _BANNED_CAP = int(cap)


def _merge_banned_words(existing, incoming):
    """Case-insensitive Dedup-Union (Reihenfolge: bestehende zuerst, dann neue), gekappt."""
    seen, out = set(), []
    for w in list(existing) + list(incoming):
        w = (str(w) or "").strip()[:40]
        if not w:
            continue
        k = w.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(w)
    return out[:_BANNED_CAP]
