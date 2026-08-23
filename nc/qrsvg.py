"""nc.qrsvg — QR-Codes als Inline-SVG (v4.0-W95).

Nutzt das eingebettete, dependency-freie 'segno' (nc/_vendor/segno, MIT) — kein
pip-Install nötig, kein externer Request, korrekte QR-Kodierung (kein selbst
geschriebener Codec, denn ein falscher QR = verlorene Spende). Ergebnisse werden
gecacht (Adressen sind statisch). Wirft nie: bei Problemen leerer String.
"""
import os
import sys

_CACHE = {}
_READY = None


def _ensure():
    global _READY
    if _READY is not None:
        return _READY
    try:
        vend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor")
        if vend not in sys.path:
            sys.path.insert(0, vend)
        import segno
        _READY = segno.make is not None
    except Exception:
        _READY = False
    return _READY


def qr_svg(data, dark="#0a0f12", light="#ffffff", scale=4, border=3):
    """Inline-SVG-String für den QR von `data` (leer bei Fehler/ohne segno).

    v4.0-W102: dunkle Module auf HELLEM Grund (vorher grün auf transparent →
    auf dem dunklen Seiten-Hintergrund kontrastarm & invertiert = viele Scanner
    lasen ihn nicht). Standard-QR (dunkel-auf-hell) + Quiet-Zone (border) scannt
    zuverlässig; die Seite rahmt die weiße Kachel im Cyberpunk-Look."""
    if not data:
        return ""
    key = (data, dark, light, scale, border)
    if key in _CACHE:
        return _CACHE[key]
    out = ""
    if _ensure():
        try:
            import segno
            q = segno.make(str(data), error="m")
            out = q.svg_inline(scale=scale, dark=dark, light=light, border=border)
        except Exception:
            out = ""
    _CACHE[key] = out
    return out
