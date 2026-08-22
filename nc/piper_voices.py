"""nc.piper_voices — B166: reine Piper-Stimm-/Modell-Auflösung (aus bot_v37 extrahiert).

Die zwei zustandslosen Kerne der Piper-TTS-Stimmwahl:
  voice_roots()        — baut die Liste der Suchwurzeln (dedupliziert, Reihenfolge)
  resolve_model_path() — löst einen Modellnamen gegen die gefundenen Stimmen auf

Beide sind rein (kein Cache, kein Log, kein Bot-Zustand) → testbar und bitgenau.
Das Scannen/Cachen der .onnx-Dateien, die Auto-Stimme-Wahl und der Piper-Aufruf
bleiben im Bot (dort sitzt der Zustand). TTS ist ein unkritisches Nebenfeature —
diese Extraktion berührt keinen Aufnahme-/Restream-Pfad.
"""

import os


def voice_roots(base_dirs, *, recordings_dir: str = "", module_dir: str = ""):
    """Alle Wurzeln, in denen nach Piper-Stimmen gesucht wird — in Reihenfolge,
       dedupliziert. base_dirs zuerst (PIPER_VOICE_DIRS), dann die üblichen Orte,
       dann <recordings_dir>/voices und <module_dir>/voices.
       Identisch zur bisherigen bot_v37._piper_voice_roots-Reihenfolge."""
    roots = list(base_dirs)
    extras = [
        os.path.expanduser("~/.local/share/piper"),
        os.path.expanduser("~/piper/voices"),
        "/usr/share/piper/voices",
        "/usr/local/share/piper/voices",
        "/opt/piper",
    ]
    if recordings_dir:
        extras.append(os.path.join(recordings_dir, "voices"))
    if module_dir:
        extras.append(os.path.join(module_dir, "voices"))
    for extra in extras:
        if extra and extra not in roots:
            roots.append(extra)
    return roots


def resolve_model_path(model: str, voices):
    """Löst Modellname/-pfad zur konkreten .onnx auf (absoluter Pfad) oder None.
       voices = [{"name","path"}] (bereits gefundene Stimmen). Reihenfolge exakt
       wie bisher: absoluter Pfad → exakter Modellname → exakter Dateiname →
       Teilstring (case-insensitiv). So greift 'thorsten' auch auf
       'de_DE-thorsten-medium.onnx' in einem Unterordner."""
    model = (model or "").strip()
    if not model:
        return None
    for c in (model, model + ".onnx"):                       # 1) voller/abs. Pfad
        if os.path.isabs(c) and os.path.isfile(c):
            return os.path.abspath(c)
    base = os.path.basename(model)
    want = (base[:-5] if base.endswith(".onnx") else base).lower()
    for v in voices:                                         # 2) exakter Modellname
        if v["name"].lower() == want:
            return v["path"]
    for v in voices:                                         # 3) exakter Dateiname
        if os.path.basename(v["path"]).lower() == base.lower():
            return v["path"]
    for v in voices:                                         # 4) Teilstring
        if want and want in v["name"].lower():
            return v["path"]
    return None
