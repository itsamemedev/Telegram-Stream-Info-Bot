"""nc.streamsel — v4.0-W29: TikTok-Stream-URL-Auswahl (Resolver-Chokepoint).

Der codec-bewusste Kern des Restream-Resolvers, aus bot_v37 herausgelöst — die
Logik, die aus TikToks liveCoreSDKData die beste Quelle (H.264 vor HEVC, sonst
kaputte Aufnahme) wählt. VERBATIM übernommen: Verhalten ist bitgenau identisch
zum Monolithen, inklusive der bestehenden latenten Kanten (z. B. ein Crash, wenn
`quality["main"]` ausnahmsweise kein dict ist) — hier wird NICHTS „nebenbei
gefixt", damit der kritischste Pfad garantiert unverändert bleibt.

Einzige externe Abhängigkeit: _stream_vcodec (bereits in nc.ffdiag). Das früher
globale PREFER_H264 ist jetzt ein Parameter (der Bot reicht seinen env-Wert rein).
"""

import json
from typing import Optional

from nc.ffdiag import _stream_vcodec

_HEVC_TOKENS = ("bytevc1", "hevc", "h265", "h.265", "hvc1", "hev1")


def is_hevc(vcodec: str) -> bool:
    """True wenn der Codec-String auf HEVC/H.265 hindeutet (das was ffmpegs
       FLV-Demuxer als 'codec id 12 / unknown codec' ablehnt)."""
    vc = (vcodec or "").lower()
    return any(tok in vc for tok in _HEVC_TOKENS)


def select_stream_from_data_section(data_section: dict,
                                    prefer_h264: bool = True) -> Optional[dict]:
    """B64: Wählt aus TikTok stream_data['data'] die beste Quelle — CODEC-BEWUSST.

       Hintergrund (Production-Bug 2026-05-29, @dramsell): TikTok liefert die
       `origin`-Qualität zunehmend als HEVC (`bytevc1`, FLV-codec-id 12). ffmpeg
       6.1.1 kann das im FLV-Container NICHT demuxen → 'Video codec is not
       implemented' / 'unknown codec' → kein Header, 0-Byte-Datei. Die NIEDRIGEREN
       Qualitäten (hd/sd/ld) sind fast immer H.264 und nehmen problemlos auf.

       Darum: lieber eine funktionierende H.264-SD-Aufnahme als eine kaputte
       HEVC-'origin'. Returns {hls_url, flv_url, vcodec, quality} oder None.

       Strategie:
         1. Alle Qualitäten mit (Quality-Rang, Codec, hls, flv) sammeln.
         2. prefer_h264=True → H.264-Kandidaten zuerst (beste Quality zuerst),
            HEVC nur als letzter Ausweg (damit wenigstens etwas versucht wird
            und die Diagnose den Codec sieht).
       Über PREFER_H264=0 (env) abschaltbar — sinnvoll nach ffmpeg-Upgrade ≥7.x.
    """
    if not isinstance(data_section, dict):
        return None
    order = ("origin", "uhd", "hd", "sd", "ld")
    cands = []   # (rank, is_hevc, quality, hls, flv, vcodec)
    for rank, quality in enumerate(order):
        q = data_section.get(quality)
        if not isinstance(q, dict):
            continue
        main = q.get("main")
        if not isinstance(main, dict):
            # v4.0-W30-FIX: früher `q.get("main") or {}` — bei einem WAHREN
            # Nicht-dict (z. B. String) crashte der Resolver an main.get(). Jetzt
            # wird eine kaputte Qualität übersprungen statt den ganzen Pull-URL-
            # Resolver zu reißen. Für dict/None/leer identisch zum alten Verhalten.
            continue
        hls = main.get("hls") or None
        flv = main.get("flv") or None
        if not hls and not flv:
            continue
        vc = _stream_vcodec(main)
        cands.append((rank, is_hevc(vc), quality, hls, flv, vc))
    if not cands:
        return None
    if prefer_h264:
        # H.264 (is_hevc False) zuerst, dann nach Quality-Rang (origin=0=beste)
        cands.sort(key=lambda c: (c[1], c[0]))
    else:
        cands.sort(key=lambda c: c[0])
    rank, hev, quality, hls, flv, vc = cands[0]
    return {"hls_url": hls, "flv_url": flv,
            "vcodec": vc or None, "quality": quality}


def find_stream_urls(obj, prefer_h264: bool = True, _depth: int = 0) -> Optional[dict]:
    """Rekursiv durch eine geparste JSON-Struktur laufen und das streamUrl-Node finden.
       Defensiv: TikTok variiert die Pfade zwischen Releases — wir suchen breit.

       v4.0-W31: verbatim aus bot_v37 übernommen; prefer_h264 wird durchgereicht
       (früher las die Blattfunktion das globale PREFER_H264 direkt)."""
    if _depth > 8:
        return None
    if isinstance(obj, dict):
        # Direkter Treffer: dieses Dict IST ein streamUrl-Objekt
        if any(k in obj for k in ("hls_pull_url", "hlsPullUrl",
                                  "liveCoreSDKData", "live_core_sdk_data")):
            r = extract_urls_from_streamurl_node(obj, prefer_h264=prefer_h264)
            if r:
                return r
        # Containing-Node: streamUrl/stream_url als Schlüssel
        for k in ("streamUrl", "stream_url"):
            child = obj.get(k)
            if isinstance(child, dict):
                r = extract_urls_from_streamurl_node(child, prefer_h264=prefer_h264)
                if r:
                    return r
        # Rekursion
        for v in obj.values():
            if isinstance(v, (dict, list)):
                r = find_stream_urls(v, prefer_h264=prefer_h264, _depth=_depth + 1)
                if r:
                    return r
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                r = find_stream_urls(v, prefer_h264=prefer_h264, _depth=_depth + 1)
                if r:
                    return r
    return None


def extract_urls_from_streamurl_node(node: dict,
                                     prefer_h264: bool = True) -> Optional[dict]:
    """Aus einem `streamUrl`-Objekt die HLS/FLV URLs extrahieren.
       Bevorzugt origin-Qualität aus liveCoreSDKData, fällt auf top-level zurück."""
    if not isinstance(node, dict):
        return None
    # Top-Level Felder (gibt's bei vielen Streams direkt)
    hls = node.get("hls_pull_url") or node.get("hlsPullUrl")
    flv = node.get("flv_pull_url") or node.get("flvPullUrl")

    # Bessere Qualität via liveCoreSDKData wenn vorhanden
    sdk = node.get("liveCoreSDKData") or node.get("live_core_sdk_data")
    vcodec = None
    quality = None
    if isinstance(sdk, dict):
        pull_data = sdk.get("pull_data")
        if isinstance(pull_data, dict):
            sd = pull_data.get("stream_data")
            # stream_data ist meistens ein JSON-String
            if isinstance(sd, str):
                try:
                    sd = json.loads(sd)
                except Exception:
                    sd = None
            if isinstance(sd, dict):
                data_section = sd.get("data") or {}
                # B64: codec-bewusste Auswahl (H.264 vor HEVC) statt blind origin
                sel = select_stream_from_data_section(data_section,
                                                      prefer_h264=prefer_h264)
                if sel:
                    # B64-Fix: sel ist codec-bewusst und damit MASSGEBLICH —
                    # nicht mit dem Top-Level mergen. Das Top-Level hls_pull_url
                    # ist oft die HEVC-origin-Variante; ein `or hls` würde bei
                    # einer H.264-flv-only-Auswahl wieder das HEVC-HLS reinholen,
                    # das der Recorder dann bevorzugt → wieder kaputt. Wenn der
                    # gewählte H.264-Stream nur FLV hat, soll hls None bleiben.
                    hls = sel.get("hls_url")
                    flv = sel.get("flv_url")
                    vcodec = sel.get("vcodec")
                    quality = sel.get("quality")

    if not hls and not flv:
        return None
    out = {"hls_url": hls, "flv_url": flv}
    if vcodec:
        out["vcodec"] = vcodec
    if quality:
        out["quality"] = quality
    return out
