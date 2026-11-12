"""nc.raumsperre — v5.4-W195: WARUM ein Raum live ist, aber keine Adresse hat (bot-frei).

DER BEFUND (Betreiber, 12.11.)
  `api-live/user/room` meldet `status=2` ohne `stream_data`, yt-dlp sagt
  „The channel is not currently live", und der Bot riet „Abo-Live oder
  Sitzung/IP". Eine Abfrage von `webcast/room/info` mit derselben room_id
  sagte es woertlich:

      status_code: 4003110   data: {"prompts": ...}

  4003110 ist TikToks Code fuer ein altersbeschraenktes Live (18+): die
  Adresse gibt es nur mit der Anmeldung eines altersbestaetigten Kontos.
  TikTokLive fuehrt denselben Code als AgeRestrictedError. Weder die
  Abo-Erkennung noch yt-dlp konnten das sagen — yt-dlp macht aus jedem
  Status ausser 2 ein „nicht live". Dazu stand in der Cookie-Datei des
  Betreibers kein sessionid, nur die Gast-Tokens des Auto-Bezugs.

DIE REGEL
  Fragen, wo die Antwort steht: einmal `webcast/room/info` je Raum, und das
  nur im Zweig „live ohne Adresse" und hoechstens alle RUHE_S je Raum. Die
  Deutung hier, die Anfrage beim Aufrufer (er hat Sitzung, Proxy, Cookies).
"""

import time

URL = "https://webcast.tiktok.com/webcast/room/info/"
RUHE_S = 600            # je Raum hoechstens alle 10 min fragen
AB18 = 4003110

_STAND = {}             # name -> {"raum": str, "lage": str, "code": int|None, "zeit": float}
_GEFRAGT = {}           # raum -> monotonic


def _name(n):
    return (n or "").lstrip("@").lower()


def faellig(raum, jetzt=None) -> bool:
    """Soll fuer diesen Raum jetzt gefragt werden? Stempelt sofort — zwei
    gleichzeitige Aufloesungen fragen sonst beide (dieselbe Falle wie der
    Live-Cache vor W103)."""
    if not raum:
        return False
    jetzt = time.monotonic() if jetzt is None else jetzt
    if jetzt - _GEFRAGT.get(raum, -1e9) < RUHE_S:
        return False
    _GEFRAGT[raum] = jetzt
    if len(_GEFRAGT) > 500:
        for r in sorted(_GEFRAGT, key=_GEFRAGT.get)[:250]:
            del _GEFRAGT[r]
    return True


def deuten(antwort) -> tuple:
    """Antwort von webcast/room/info -> (lage, code).

    lage: "ab18"          4003110 — Anmeldung eines altersbestaetigten Kontos noetig
          "offen"         status_code 0 und eine stream_url — der Raum gibt sie her
          "ohne_adresse"  status_code 0, aber keine stream_url
          "fehler"        ein anderer Code (steht in `code`)
          "unlesbar"      keine erkennbare Antwort"""
    if not isinstance(antwort, dict):
        return "unlesbar", None
    code = antwort.get("status_code")
    if not isinstance(code, int):
        return "unlesbar", None
    if code == AB18:
        return "ab18", code
    if code != 0:
        return "fehler", code
    daten = antwort.get("data") if isinstance(antwort.get("data"), dict) else {}
    return ("offen" if daten.get("stream_url") else "ohne_adresse"), code


def merken(name, raum, lage, code, jetzt=None):
    _STAND[_name(name)] = {"raum": raum, "lage": lage, "code": code,
                           "zeit": time.time() if jetzt is None else jetzt}


def lage(name):
    """Letzte Deutung fuer diesen Nutzer oder None."""
    return _STAND.get(_name(name))


def vergessen(name):
    """Neues Live, neue Lage — sonst haengt ein altes 18+ am naechsten Raum."""
    _STAND.pop(_name(name), None)


def text(eintrag, hat_login) -> str:
    """Der Satz fuer Log und Telegram — mit Abhilfe, oder '' ohne Befund."""
    if not eintrag:
        return ""
    if eintrag["lage"] == "ab18":
        if not hat_login:
            return ("TikTok meldet 18+ (Code 4003110), und die Cookie-Datei traegt keine "
                    "Anmeldung (kein sessionid). Abhilfe: Cookies eines eingeloggten, "
                    "altersbestaetigten Kontos hinterlegen — /cookies in Telegram nennt die Wege.")
        return ("TikTok meldet 18+ (Code 4003110), obwohl ein sessionid hinterlegt ist: das "
                "Konto ist nicht altersbestaetigt, oder die Anmeldung ist abgelaufen. "
                "Abhilfe: im Browser mit diesem Konto ein 18+-Live oeffnen und neu exportieren.")
    if eintrag["lage"] == "fehler":
        return "webcast/room/info antwortet mit Code %s." % eintrag["code"]
    return ""


def snapshot() -> dict:
    """Fuer /healthz: wer gerade aus welchem Grund verschlossen ist."""
    return {n: {"lage": e["lage"], "code": e["code"]} for n, e in _STAND.items()}
