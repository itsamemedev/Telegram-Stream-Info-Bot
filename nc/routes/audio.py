"""nc.routes.audio — die Routen unter /api/audio als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix).

v4.1-W20: Zwei Routen, **null neue Kontext-Eintraege**. Geloest wurde vorweg:

* **nc/audiocue.py** — die sechs .env-Vorgaben und der Zugriff auf den
  gespeicherten Wert. Der Bot loest die Vorgaben auf und reicht sie hinein;
  das Modul friert nichts ein.
* **nc/channels.RESTREAM_TTS** — die laufenden Stimmkanaele je Restream, als
  Alias. Das ist der Punkt des Testtons: er muss in den LIVE-Mix, nicht in
  eine Kopie. Eine Kopie hiesse "0 Warteschlangen" bei laufendem Restream —
  eine Fehlanzeige, die wie ein kaputter Ton aussieht.
"""

from flask import Blueprint, jsonify, request

from nc import audio_cue as _nc_audio
from nc import audiocue as _nc_audiocue
from nc import cfgstore as _nc_cfgstore
from nc import channels as _nc_channels
from nc import i18n as _nc_i18n

bp = Blueprint("audio", __name__)

# Das PCM-Format des Restream-Tonmischers. Der Signalton muss bitgenau dazu
# passen, sonst rauscht er im Sendebild statt zu piepen.
_TTS_SR, _TTS_CH = 44100, 2


def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


@bp.route("/api/audio/config", methods=["GET", "POST"])
def api_audio_config():
    """v4.0-W12: Signalton + Ducking im Dashboard einstellen (ohne .env/Neustart)."""
    if request.method == "GET":
        c = _nc_audiocue.config()
        c["duck_percent"] = round((1.0 - c["duck"]) * 100)
        c["hinweis"] = _t("Ton wirkt sofort; Ducking greift beim naechsten "
                          "Restream-Start (steckt in der ffmpeg-Kette).")
        return jsonify(ok=True, **c)
    d = request.get_json(silent=True) or {}
    new = dict(_nc_audiocue.config())
    if "tone" in d:
        new["tone"] = bool(d["tone"])
    for key, lo, hi in (("freq", 100.0, 4000.0), ("vol", 0.0, 1.0), ("duck", 0.1, 1.0)):
        if key in d:
            try:
                new[key] = max(lo, min(hi, float(d[key])))
            except (TypeError, ValueError):
                return jsonify(ok=False, error=f"{key} " + _t("ungueltig")), 400
    for key, lo, hi in (("ms", 20, 1000), ("gap_ms", 0, 1000)):
        if key in d:
            try:
                new[key] = max(lo, min(hi, int(d[key])))
            except (TypeError, ValueError):
                return jsonify(ok=False, error=f"{key} " + _t("ungueltig")), 400
    _nc_cfgstore.set_("audio.cue", new)
    return jsonify(ok=True, **new)


@bp.route("/api/audio/testtone", methods=["POST"])
def api_audio_testtone():
    """Spielt den Signalton EINMAL in den laufenden Restream — zum Abhoeren."""
    c = _nc_audiocue.config()
    try:
        pcm = _nc_audio.cue_pcm(freq=c["freq"], ms=c["ms"], volume=c["vol"],
                                gap_ms=c["gap_ms"], sr=_TTS_SR, ch=_TTS_CH)
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:140]), 200
    queues = [v.get("queue") for v in _nc_channels.RESTREAM_TTS.values()
              if v.get("queue") is not None]
    if not queues:
        return jsonify(ok=False,
                       error=_t("kein laufender Restream mit Stimm-Kanal "
                                "— Ton kann nur im Live-Mix hoerbar sein")), 200
    for q in queues:
        q.append(pcm)
    return jsonify(ok=True, queues=len(queues), bytes=len(pcm))
