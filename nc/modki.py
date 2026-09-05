"""nc.modki — die zwei KI-Fragen der Chat-Moderation.

v4.2-W13. Aus KickModerator geloest. Hier stehen die Aufforderung an das
Sprachmodell und die Auswertung seiner Antwort — nicht der Aufruf selbst: den
reicht der Bot als `ai_chat` herein, weil er am Router, am Budget und an der
Basen-Rotation haengt (siehe nc/freeai.py, brain/llm.py).

WARUM DAS TRENNBAR IST UND SEIN SOLLTE: die Auswertung ist der Teil, der
schiefgeht. Ein Sprachmodell antwortet mal mit ```json, mal mit nacktem JSON,
mal mit einem Satz davor. Faengt das niemand ab, kippt eine Moderation still
ins Nichts — `None` sieht aus wie "unauffaellig". Diese Faelle lassen sich
hier ohne Modell durchspielen; mit dem Aufruf verwoben ginge das nicht.
"""

import json
import re

# Ein Sprachmodell rahmt JSON gern in einen Codeblock. Ohne das Abstreifen
# scheitert json.loads, und die Moderation faellt aus, ohne es zu sagen.
_ZAUN = re.compile(r"^```(?:json)?|```$", re.MULTILINE)

KLASSIFIKATION = ("Klassifiziere die Chat-Nachricht. Antworte NUR mit JSON: "
                  '{"toxic": <0.0-1.0>, "question": <true|false>}. '
                  "toxic=Wahrscheinlichkeit für Spam/Beleidigung/Hass.")
SCHIMPFWOERTER = ("Extrahiere aus der Chat-Nachricht NUR echte Schimpf-/Hasswörter "
                  "(Beleidigungen, Slurs) — KEINE harmlosen Wörter. Antworte NUR mit JSON-Array "
                  '[{"word":"<wort>","lang":"<ISO-639-1>"}]. Leeres Array [] wenn keines eindeutig.')

MAX_WOERTER = 8


def _entzaunen(text):
    return _ZAUN.sub("", (text or "").strip()).strip()


def frage(system, inhalt, grenze):
    """Die Nachrichtenliste fuer ai_chat. Der Inhalt wird gekuerzt: ein
    Chat-Roman kostet Budget und aendert am Urteil nichts."""
    return [{"role": "system", "content": system},
            {"role": "user", "content": (inhalt or "")[:grenze]}]


def lies_klassifikation(text):
    """-> {"toxic": float, "question": bool} oder None.

    None heisst "keine Antwort", nicht "unauffaellig". Der Aufrufer muss
    beides unterscheiden koennen — sonst gilt ein ausgefallenes Modell als
    Freispruch.
    """
    try:
        d = json.loads(_entzaunen(text))
        return {"toxic": float(d.get("toxic", 0)),
                "question": bool(d.get("question"))}
    except Exception:
        return None


def lies_schimpfwoerter(text):
    """-> [{"word", "lang"}]. Leer bei Unklarheit — nie None.

    Hier ist die leere Liste richtig: ein unlesbares Modellergebnis darf
    keine Sperrliste erweitern. Im Zweifel wird NICHT gelernt.
    """
    raus = []
    try:
        arr = json.loads(_entzaunen(text))
    except Exception:
        return raus
    if not isinstance(arr, list):
        return raus
    for eintrag in arr[:MAX_WOERTER]:
        if not isinstance(eintrag, dict):
            continue
        wort = str(eintrag.get("word", "")).strip()[:40]
        sprache = str(eintrag.get("lang", "")).strip()[:5].lower()
        if wort:
            raus.append({"word": wort, "lang": sprache or "?"})
    return raus
