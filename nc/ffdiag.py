"""nc.ffdiag — ffmpeg-Diagnose-Helfer (keine Bot-Abhängigkeiten).

Extrahiert aus bot_v37.py: stderr-Tail/Diagnostik (Banner-Skip, Fehler-
Extraktion), Kommando-Redaktion fürs Log (Cookies raus), Codec-Erkennung,
Aufnahme-Qualitätsstufe."""

import json
import re
import subprocess
from typing import List

def _ffmpeg_stderr_tail(text: str, max_len: int = 1000) -> str:
    """B44: Aus dem Live-Log gesehen: 'ffmpeg split failed: ffmpeg version 6.1.1
       built with gcc 13 (Ubuntu 13.3.0-6ubuntu2~24.04) configuration: --prefix=...'
       Das ist NUR der Banner. Die echte Fehlermeldung steht am ENDE von stderr,
       nach Stream-Info etc. Vorher: stderr.decode()[:500] → wir sehen nur den
       Banner, nicht den Grund warum's geknallt hat. Jetzt: skippt Banner + Config
       + Library-Versionen + Stream-Mapping; gibt den TAIL zurück (die letzten
       max_len Zeichen) wo die eigentliche Error-Meldung steht. Wenn der Text
       eh kürzer ist als max_len, returnen wir alles. Trimmt führende leere Zeilen."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_len:
        return text
    # Skip die typische ffmpeg-Banner-Region. Wir erkennen sie an dem Pattern
    # "configuration: --prefix=...". Wenn vorhanden, suchen wir das ENDE dieser
    # Section (markiert durch die letzte "libXxx" Zeile) und nehmen alles danach.
    # Fallback: einfach den Tail.
    skip_markers = ("configuration:", "  libavutil", "  libavcodec",
                    "  libavformat", "  libavdevice", "  libavfilter",
                    "  libswscale", "  libswresample", "  libpostproc")
    lines = text.splitlines()
    # Finde letzten Index mit Banner-Marker
    last_banner_idx = -1
    for i, line in enumerate(lines):
        if any(line.startswith(m) or m in line[:30] for m in skip_markers):
            last_banner_idx = i
    if last_banner_idx >= 0 and last_banner_idx < len(lines) - 1:
        # Nehme alles NACH dem Banner
        tail = "\n".join(lines[last_banner_idx + 1:]).strip()
        if tail:
            # Falls Tail immer noch zu lang, nimm den letzten Teil
            if len(tail) > max_len:
                tail = "…" + tail[-max_len:]
            return tail
    # Fallback: einfach die letzten max_len Zeichen
    return "…" + text[-max_len:]

def _ffmpeg_stderr_diagnostic(text: str, max_len: int = 2000) -> str:
    """B55: Wenn _ffmpeg_stderr_tail() nichts Useful zurückgibt (das passiert
       wenn ffmpeg NUR den Banner ausgegeben hat = vor jeglichem Stream-Read
       gestorben), geben wir die GANZE stderr zurück (gecappt) damit Operator
       wenigstens den Banner sieht. Banner enthält z.B. die HLS-URL, die wir
       für Debugging brauchen.

       Production-Bug 2026-05-25: @dramsell hatte 25× "empty stderr" — wir
       haben absolut keine Info gehabt warum die Recordings starben. Mit
       diesem Fallback sehen wir wenigstens was ffmpeg PROBIERT hat.

       Algorithmus: erst versuchen post-banner content zu extrahieren.
       Wenn da was steht → das ist die echte Fehlermeldung (B44 Verhalten).
       Wenn NICHTS nach dem Banner kommt = "banner-only" → ganze stderr
       zurück mit explizitem Marker damit Operator weiß was los ist."""
    if not text or not text.strip():
        return "(no stderr — process never wrote output)"
    text = text.strip()
    # Banner-Marker (gleich wie in _ffmpeg_stderr_tail)
    skip_markers = ("configuration:", "  libavutil", "  libavcodec",
                    "  libavformat", "  libavdevice", "  libavfilter",
                    "  libswscale", "  libswresample", "  libpostproc",
                    "ffmpeg version", "built with", "Copyright (c)")
    lines = text.splitlines()
    last_banner_idx = -1
    for i, line in enumerate(lines):
        if any(line.startswith(m) or m in line[:40] for m in skip_markers):
            last_banner_idx = i
    # Post-Banner content extrahieren
    post_banner = ""
    if last_banner_idx >= 0 and last_banner_idx < len(lines) - 1:
        post_banner = "\n".join(lines[last_banner_idx + 1:]).strip()
    elif last_banner_idx < 0:
        # Kein Banner erkannt → alles ist post_banner
        post_banner = text
    if post_banner:
        if len(post_banner) > max_len:
            return "…" + post_banner[-max_len:]
        return post_banner
    # Banner-only case → fallback auf FULL mit explizitem Marker
    prefix = "[banner-only, no stream-output] "
    if len(text) <= max_len:
        return prefix + text
    half = max_len // 2
    return prefix + text[:half] + "\n…[gekürzt]…\n" + text[-half:]

def redact_cmd_for_log(cmd: List[str]) -> List[str]:
    """Cookies aus dem cmd entfernen bevor's ins Log geht.
       Behandelt streamlink (--http-header Cookie=…), yt-dlp (--cookies FILE),
       und ffmpeg (-headers '...Cookie: ...\\r\\n')."""
    out = []
    skip_next = False
    redact_kind = None
    for arg in cmd:
        if skip_next:
            if redact_kind == "cookie_header" and arg.startswith("Cookie="):
                out.append("Cookie=<redacted>")
            elif redact_kind == "cookie_file":
                out.append("<COOKIE_FILE>")
            elif redact_kind == "ffmpeg_headers":
                # bei -headers ist der Wert ein Multi-Line-String mit u.U. Cookie drin
                if "Cookie:" in arg:
                    parts = []
                    for line in arg.splitlines():
                        if line.lower().startswith("cookie:"):
                            parts.append("Cookie: <redacted>")
                        elif line.strip():
                            parts.append(line)
                    out.append("\\r\\n".join(parts) + "\\r\\n")
                else:
                    out.append(arg)
            else:
                out.append(arg)
            skip_next = False; redact_kind = None
            continue
        if arg == "--http-header":
            skip_next = True; redact_kind = "cookie_header"
        elif arg == "--cookies":
            skip_next = True; redact_kind = "cookie_file"
        elif arg == "-headers":
            skip_next = True; redact_kind = "ffmpeg_headers"
        out.append(arg)
    return out

def _stream_vcodec(main: dict) -> str:
    """B64: Aus einem quality.main-Objekt den Video-Codec rausholen (lowercased).
       TikTok packt das in `sdk_params` (meist JSON-String) als Feld 'VCodec'.
       Werte: 'h264' (AVC, ffmpeg-freundlich) | 'bytevc1' (ByteDance-HEVC) |
       'h265'/'hevc'. Fallback: '' wenn nicht ermittelbar."""
    if not isinstance(main, dict):
        return ""
    sp = main.get("sdk_params") or main.get("sdkParams")
    if isinstance(sp, str):
        try:
            sp = json.loads(sp)
        except Exception:
            sp = None
    if isinstance(sp, dict):
        vc = sp.get("VCodec") or sp.get("vcodec") or sp.get("v_codec") or ""
        return str(vc).lower()
    return ""

def _rec_quality(rec):
    """Qualitäts-Score 0-100 aus Größe, Dauer, Bitrate-Schätzung."""
    size_mb = (rec.get("file_size") or 0) / 1048576.0
    dur = rec.get("duration_secs") or 0
    if dur <= 0:
        return {"score": 0, "tier": "unbekannt", "mbps": None}
    mbps = (size_mb * 8) / dur
    # grobe Heuristik: >2.5 Mbps gut, >1 ok, sonst niedrig; Dauer-Bonus
    bitrate_score = min(100, mbps / 3.0 * 100)
    dur_score = min(100, dur / 600.0 * 100)    # 10min → voll
    score = round(0.7 * bitrate_score + 0.3 * dur_score)
    tier = ("hoch" if mbps >= 2.5 else "mittel" if mbps >= 1.0 else "niedrig")
    return {"score": score, "tier": tier, "mbps": round(mbps, 2),
            "size_mb": round(size_mb, 1), "duration_secs": dur}


def ffprobe_duration(path) -> float:
    """Dauer einer Mediendatei in Sekunden (sync, ffprobe). 0.0 bei Fehler/Timeout.
       Phase-1-Zerlegung: verbatim aus bot_v37 (_ffprobe_duration)."""
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", path],
                           capture_output=True, text=True, timeout=15)
        return float((p.stdout or "0").strip() or 0)
    except Exception:
        return 0.0


def clip_caption_escape(s) -> str:
    """Text für ffmpeg drawtext entschärfen (Sonderzeichen) + auf 70 Zeichen kürzen.
       Phase-1-Zerlegung: verbatim aus bot_v37 (_clip_caption_escape)."""
    s = (s or "").replace("\\", " ").replace(":", " ").replace("'", " ").replace("%", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:70]
