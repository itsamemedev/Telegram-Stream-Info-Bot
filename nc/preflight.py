"""nc.preflight — Stream-URL-Preflight (CDN-404-Schutz, V37-B91).

Extrahiert aus bot_v37.py. Prüft eine Stream-URL vor dem ffmpeg-Spawn auf 404
und testet _hd/_uhd/_sd-Suffix-Fallbacks (TikTok-CDN-Quirk). Nutzt die Zähler
_PREFLIGHT_STATS/_PREFLIGHT_DEAD_STREAK, die die Bridge als Metriken spiegelt.

`log` und `RECORD_PROXY` werden von bot_v37.py via configure() injiziert, damit
das Modul keine Rückabhängigkeit auf den Monolithen hat.
"""

import logging

log = logging.getLogger("nc.preflight")
RECORD_PROXY = ""


def configure(logger=None, record_proxy=None):
    """bot_v37.py reicht seinen Logger + Proxy rein (identisches Verhalten)."""
    global log, RECORD_PROXY
    if logger is not None:
        log = logger
    if record_proxy is not None:
        RECORD_PROXY = record_proxy


_PREFLIGHT_CACHE = {}
# V37-B91c: Preflight-Telemetrie — die Bridge spiegelt diese Zähler als
# Metriken (preflight_ok/fallback/dead), damit im Dashboard/Report sichtbar
# wird, wie oft der CDN-404-Quirk zuschlägt und der Fallback rettet.
_PREFLIGHT_STATS = {"ok": 0, "fallback": 0, "dead": 0}
# V37-B91d: aufeinanderfolgende Tot-Treffer pro Quelle (who → streak). Jeder
# Erfolg (ok/fallback) setzt zurück; die Bridge exponiert das an eine
# Brain-Regel, die chronisch tote Quellen zum Untracken vorschlägt.
_PREFLIGHT_DEAD_STREAK = {}

async def _preflight_url(u, who="?"):
    if not u:
        return u
    def _variants(x):
        out, seen = [x], {x}
        for sfx in ("_hd", "_uhd", "_sd", "_ld"):
            for v in (x.replace(sfx + ".flv", ".flv"),
                      x.replace(sfx + "/index.m3u8", "/index.m3u8"),
                      x.replace(sfx + ".m3u8", ".m3u8")):
                if v not in seen:
                    seen.add(v); out.append(v)
        pref = _PREFLIGHT_CACHE.get(who)
        if pref and pref in x:
            pv = x.replace(pref, "")
            if pv in out and out.index(pv) > 0:
                out.remove(pv); out.insert(0, pv)
        return out
    try:
        import aiohttp as _ah
        tmo = _ah.ClientTimeout(total=6)
        _pxy = RECORD_PROXY or None
        async with _ah.ClientSession(timeout=tmo) as _s:
            for cand in _variants(u):
                try:
                    async with _s.get(cand, proxy=_pxy,
                                      headers={"Range": "bytes=0-1023",
                                               "User-Agent": "Mozilla/5.0"},
                                      allow_redirects=True) as r:
                        if r.status == 404:
                            continue
                        if cand != u:
                            for _sfx in ("_hd", "_uhd", "_sd", "_ld"):
                                if _sfx in u and _sfx not in cand:
                                    _PREFLIGHT_CACHE[who] = _sfx
                                    if len(_PREFLIGHT_CACHE) > 300:
                                        _PREFLIGHT_CACHE.pop(next(iter(_PREFLIGHT_CACHE)))
                                    break
                            log.info("%s: B91-Preflight — %s 404, Fallback greift",
                                     who, u.split("?")[0].rsplit("/", 1)[-1])
                            _PREFLIGHT_STATS["fallback"] += 1
                        else:
                            if who in _PREFLIGHT_CACHE:
                                _PREFLIGHT_CACHE.pop(who, None)
                            _PREFLIGHT_STATS["ok"] += 1
                        _PREFLIGHT_DEAD_STREAK.pop(who, None)   # V37-B91d
                        return cand
                except Exception:
                    return u          # Netzfehler → fail-open mit Original
        log.warning("%s: B91-Preflight — alle URL-Varianten 404 (tot/Battle-Stage)", who)
        _PREFLIGHT_STATS["dead"] += 1
        _PREFLIGHT_DEAD_STREAK[who] = _PREFLIGHT_DEAD_STREAK.get(who, 0) + 1  # V37-B91d
        if len(_PREFLIGHT_DEAD_STREAK) > 300:
            _PREFLIGHT_DEAD_STREAK.pop(next(iter(_PREFLIGHT_DEAD_STREAK)))
        return None
    except Exception:
        return u
