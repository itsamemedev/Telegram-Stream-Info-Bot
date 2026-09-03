"""nc.piper_voices — B166: reine Piper-Stimm-/Modell-Auflösung (aus bot.py extrahiert).

Die zwei zustandslosen Kerne der Piper-TTS-Stimmwahl:
  voice_roots()        — baut die Liste der Suchwurzeln (dedupliziert, Reihenfolge)
  resolve_model_path() — löst einen Modellnamen gegen die gefundenen Stimmen auf

Beide sind rein (kein Cache, kein Log, kein Bot-Zustand) → testbar und bitgenau.

v4.1-W19: Dazugekommen ist das **Scannen** samt Cache und die Frage, ob die
Piper-CLI ueberhaupt da ist. Grund: die drei Routen `/api/azrael/voices`,
`/api/azrael/piper_status` und `/api/azrael/tts_test` haetten dafuer sonst
sieben nc.ctx-Eintraege gekostet (vier Funktionen, drei Modul-Globals) — bei
24 von vertraglich 25 belegten Plaetzen unbezahlbar. Erst die Schicht loesen,
dann sind die Routen umsonst; dieselbe Reihenfolge wie W117.

Die Suchorte kommen per `configure(...)` statt als Modul-Konstante: `.env` ist
beim Import teils noch nicht geladen (CLAUDE.md). Das eigentliche Sprechen
(`_piper_say`) bleibt im Bot — es haengt an asyncio, am Overlay-Zustand und am
Restream-Tonmischer. Es wird als Haken registriert, nicht hierher kopiert.

TTS ist ein unkritisches Nebenfeature — diese Extraktion berührt keinen
Aufnahme-/Restream-Pfad.
"""

import os
import time


def voice_roots(base_dirs, *, recordings_dir: str = "", module_dir: str = ""):
    """Alle Wurzeln, in denen nach Piper-Stimmen gesucht wird — in Reihenfolge,
       dedupliziert. base_dirs zuerst (PIPER_VOICE_DIRS), dann die üblichen Orte,
       dann <recordings_dir>/voices und <module_dir>/voices.
       Identisch zur bisherigen bot._piper_voice_roots-Reihenfolge."""
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


# ---- v4.1-W19: Scannen, Cache und Verfuegbarkeit ---------------------------
# Bis W18 lagen diese vier Funktionen und drei Modul-Globals im Monolithen.
# Die Konfiguration kommt per configure(), nicht als Modul-Konstante — .env
# wird teils erst nach den ersten Imports geladen.

_CONF = {"bin": "piper", "data_dir": "", "voice_dirs": [],
         "recordings_dir": "", "module_dir": ""}
_CACHE = {"ts": 0.0, "voices": []}
CACHE_S = 60.0

# Register fuer das eigentliche Sprechen. Der Bot traegt seine Coroutine ein;
# die Routen rufen sie ueber den Kontext auf. Warum nicht hierher kopiert:
# _piper_say haengt an asyncio, am Overlay-Zustand und am Restream-Tonmischer —
# das waere kein Modul mehr, das waere der halbe Bot. Dasselbe Muster wie
# TWITCH_SEND/YT_SEND in nc/channels.py.
SAY = {"fn": None}


def configure(*, bin=None, data_dir=None, voice_dirs=None,
              recordings_dir=None, module_dir=None):
    if bin is not None:
        _CONF["bin"] = str(bin).strip() or "piper"
    if data_dir is not None:
        _CONF["data_dir"] = str(data_dir).strip()
    if voice_dirs is not None:
        _CONF["voice_dirs"] = [d for d in voice_dirs if d]
    if recordings_dir is not None:
        _CONF["recordings_dir"] = str(recordings_dir)
    if module_dir is not None:
        _CONF["module_dir"] = str(module_dir)
    _CACHE.update(ts=0.0, voices=[])      # geaenderte Suchorte -> neu scannen


def bin_pfad() -> str:
    return _CONF["bin"]


def data_dir() -> str:
    return _CONF["data_dir"]


def voice_dirs():
    return list(_CONF["voice_dirs"])


def roots():
    """Alle Wurzeln, in denen nach Stimmen gesucht wird."""
    return voice_roots(_CONF["voice_dirs"],
                       recordings_dir=_CONF["recordings_dir"],
                       module_dir=_CONF["module_dir"])


def list_voices(force=False, _jetzt=None):
    """Alle Wurzeln REKURSIV nach .onnx absuchen. -> [{name, path}], 60 s gecacht.

    Der Cache ist kein Luxus: das Dashboard fragt den Piper-Status im Takt des
    Control-Tabs ab, und ein os.walk ueber mehrere Verzeichnisbaeume je Aufruf
    kostet auf einer Box, die nebenher transkodiert, echte Zeit.
    """
    now = _jetzt if _jetzt is not None else time.time()
    if not force and _CACHE["voices"] and now - _CACHE["ts"] < CACHE_S:
        return _CACHE["voices"]
    gefunden, gesehen = [], set()
    for root in roots():
        try:
            if not (root and os.path.isdir(root)):
                continue
            for dirpath, _dirs, files in os.walk(root):
                for f in files:
                    if f.endswith(".onnx"):
                        p = os.path.abspath(os.path.join(dirpath, f))
                        if p not in gesehen:
                            gesehen.add(p)
                            gefunden.append({"name": f[:-5], "path": p})
        except OSError:
            pass
    gefunden.sort(key=lambda v: v["name"])
    _CACHE.update(ts=now, voices=gefunden)
    return gefunden


def resolve(model):
    """Modellname/-pfad zur konkreten .onnx aufloesen (oder None)."""
    return resolve_model_path(model, list_voices())


def available() -> bool:
    """Ist die Piper-CLI da? Ein absoluter Pfad zaehlt auch ohne PATH-Eintrag."""
    import shutil
    b = _CONF["bin"]
    return bool(shutil.which(b) or os.path.isfile(b))
