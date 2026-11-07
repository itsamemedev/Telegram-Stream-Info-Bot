"""nc.kickzentrifugo — v4.2-W171: der Kick-Chat laeuft ueber Centrifugo, nicht mehr Pusher.

Gemeldet am 07.11.: der Kick-Chat verbindet sich alle drei Sekunden neu,
„4001 App key 32cbd69e4b950bf97679 not in this cluster" — und mit dem
zweiten bekannten Key genauso. Der Betreiber hat im Firefox nachgesehen: der
Web-Client von kick.com oeffnet gar keine Verbindung zu `pusher.com` mehr,
sondern zu `realtime.us-west-2.platform.kick.com`. Kick hat den Chat Mitte
Oktober 2026 auf Centrifugo umgestellt und den Pusher-Key zurueckgezogen.
Damit war W154 (Cluster durchprobieren) und W167 (bekannte Keys
durchprobieren) die Suche an der falschen Stelle: es gibt keinen Key mehr,
der passt.

Der Weg, wie ihn der Web-Client geht (nachgelesen in mehreren unabhaengigen
Umbauten anderer Chat-Clients; Kick dokumentiert davon nichts):

1. POST web.kick.com/api/v1/realtime/connection mit einer Client-ID (UUID)
   und den angenommenen Anbietern. Antwort: data.connections[].provider /
   .credentials.url — die Websocket-Adresse. Die Region steht darin; deshalb
   wird sie gelesen, nicht fest verdrahtet (W136: ein fest verdrahteter
   Cluster liess sich nicht ohne Codeaenderung korrigieren).
2. POST web.kick.com/api/v1/realtime/auth/connection mit derselben ID.
   Antwort: data.token — ein Gast-JWT, rund 45 Minuten gueltig, ohne Login.
3. Websocket, Centrifugo-JSON-Protokoll:
   → {"connect":{"token":…,"name":"js"},"id":1}
   → {"subscribe":{"channel":"chatrooms.<id>.v2"},"id":2}
   ← {"push":{"channel":…,"pub":{"data":{"event":…,"data":"<JSON-Text>"}}}}
   Der Server schickt alle 25 s ein leeres `{}` und erwartet `{}` zurueck,
   sonst schliesst er mit 3012 „no pong". Ein Rahmen kann mehrere
   Nachrichten tragen, durch Zeilenumbrueche getrennt.

Der Inhalt einer Veroeffentlichung ist DERSELBE `{event, data}` wie frueher
der Pusher-Rahmen. `als_frame()` macht daraus genau diese Form, und die
gesamte Verarbeitung im Bot (Moderation, AZRAEL, Overlay, Gifts) bleibt
unberuehrt — sie hat nie Pusher gelesen, nur Kick-Ereignisse.

Bot-frei. Das HTTP laeuft ueber eine hereingereichte aiohttp-Session.
"""

import json
import uuid

VERBINDUNG_URL = "https://web.kick.com/api/v1/realtime/connection"
TOKEN_URL = "https://web.kick.com/api/v1/realtime/auth/connection"

# Der Websocket weist fremde Origins mit 403 ab (gemessen von anderen
# Clients); kick.com selbst und gar keine Origin gehen. Gesendet wird die des
# Web-Clients — wir sprechen mit demselben Dienst wie er.
KOPF = {
    "Origin": "https://kick.com",
    "Referer": "https://kick.com/",
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"),
    "Accept": "application/json",
}

# Erneuern bei drei Vierteln der Laufzeit: ein Token, das waehrend eines
# langen Streams ablaeuft, beendet die Verbindung genau dann, wenn am meisten
# im Chat los ist.
ERNEUERN_ANTEIL = 0.75
TTL_VORGABE_S = 2700

# Der Server pingt alle 25 s. Doppelt so lange plus Luft ohne einen Rahmen
# heisst: tot, auch wenn die TCP-Verbindung das noch nicht gemerkt hat.
STILLE_S = 60

ID_CONNECT = 1
ID_SUBSCRIBE = 2


class KickZentrifugoFehler(ConnectionError):
    """Aufbau gescheitert — mit Klartext und, wo es einen gibt, Code."""

    def __init__(self, text, code=None):
        super().__init__(text)
        self.code = code


def neue_client_id() -> str:
    return str(uuid.uuid4())


def kanal(chatroom_id) -> str:
    return "chatrooms.%d.v2" % int(chatroom_id)


def verbindung_body(client_id) -> dict:
    # Nur Centrifugo anbieten: wer Pusher mitanbietet, bekommt heute zwar
    # trotzdem Centrifugo, aber Pusher ist genau der Weg, der tot ist.
    return {"client": {"id": client_id, "type": "web"},
            "capabilities": {"accepted_providers": [{"provider": "centrifugo"}]}}


def ws_url_aus(antwort) -> str:
    """Die Websocket-Adresse aus der Antwort von VERBINDUNG_URL."""
    verb = ((antwort or {}).get("data") or {}).get("connections") or []
    for v in verb:
        if isinstance(v, dict) and v.get("provider") == "centrifugo":
            url = ((v.get("credentials") or {}).get("url") or "").strip()
            # Nur verschluesselt: ueber die Verbindung geht das Token. ws://
            # ausschliesslich auf Loopback — das ist der Nachbau im Vertrag.
            if url.startswith("wss://") or url.startswith(("ws://127.0.0.1:", "ws://localhost:")):
                return url
            raise KickZentrifugoFehler(
                "Kick nannte eine Centrifugo-Adresse, die nicht verschluesselt ist "
                "oder fehlt (%r) — nicht verbunden, das Token ginge im Klartext." % url[:120])
    anbieter = [v.get("provider") for v in verb if isinstance(v, dict)]
    raise KickZentrifugoFehler(
        "Kick nannte keinen Centrifugo-Websocket (Anbieter: %s) — der "
        "Web-Client von kick.com hat den Weg vermutlich wieder gewechselt. "
        "Abhilfe: in Firefox F12 › Netzwerkanalyse › WebSockets auf einem "
        "Live-Kanal nachsehen, wohin er verbindet." % (anbieter or "keine"))


def token_aus(antwort) -> str:
    tok = (((antwort or {}).get("data") or {}).get("token") or "").strip()
    if not tok:
        raise KickZentrifugoFehler("Kick gab kein Gast-Token heraus (Antwort ohne data.token)")
    return tok


def connect_cmd(token) -> str:
    return json.dumps({"connect": {"token": token, "name": "js"}, "id": ID_CONNECT})


def subscribe_cmd(chatroom_id) -> str:
    return json.dumps({"subscribe": {"channel": kanal(chatroom_id)}, "id": ID_SUBSCRIBE})


def refresh_cmd(token, cmd_id) -> str:
    return json.dumps({"refresh": {"token": token}, "id": int(cmd_id)})


def zerlegen(text):
    """Ein Websocket-Rahmen → Liste der Nachrichten darin.

    Centrifugo buendelt mehrere Antworten in einem Rahmen, eine je Zeile. Wer
    den Rahmen als EIN JSON liest, verliert bei jedem gebuendelten Rahmen
    alle Nachrichten darin — das Fehlerbild waere ein Chat, in dem gerade die
    belebten Momente fehlen. Eine unlesbare Zeile wirft: der Aufrufer
    entscheidet, ob er sie meldet.
    """
    return [json.loads(z) for z in str(text or "").split("\n") if z.strip()]


def ist_ping(nachricht) -> bool:
    """Der Server-Ping ist ein leeres Objekt; die Antwort darauf auch."""
    return nachricht == {}


def antwort_fehler(nachricht) -> str:
    """Klartext einer Fehlerantwort ({"id":…,"error":{code,message}}), sonst ''."""
    err = (nachricht or {}).get("error") if isinstance(nachricht, dict) else None
    text = ""          # leer heisst: keine Fehlerantwort, nicht „Fehler verschluckt"
    if isinstance(err, dict):
        text = ("%s %s" % (err.get("code", ""), err.get("message", ""))).strip() or "Fehler ohne Text"
    elif err:
        text = str(err)[:200]
    return text


def fehler_code(nachricht):
    err = (nachricht or {}).get("error") if isinstance(nachricht, dict) else None
    return err.get("code") if isinstance(err, dict) else None


def ttl_aus(nachricht, vorgabe=TTL_VORGABE_S) -> int:
    """Laufzeit des Tokens aus der connect-/refresh-Antwort, in Sekunden."""
    for teil in ("connect", "refresh"):
        t = ((nachricht or {}).get(teil) or {}).get("ttl") if isinstance(nachricht, dict) else None
        if isinstance(t, (int, float)) and t > 0:
            return int(t)
    return int(vorgabe)


def als_frame(nachricht):
    """Eine Veroeffentlichung → {"event": …, "data": "<JSON-Text>"} wie frueher
    bei Pusher; alles andere → None."""
    # None ist hier der Normalfall (Ping, Abo-Antwort), kein Fehlerpfad.
    frame = None
    pub = (((nachricht.get("push") or {}).get("pub") or {}).get("data")
           if isinstance(nachricht, dict) else None)
    if isinstance(pub, dict) and pub.get("event"):
        data = pub.get("data")
        if not isinstance(data, str):
            # Der Bot liest data mit json.loads — ein schon zerlegtes Objekt wird
            # wieder Text, statt dort in einem TypeError zu verschwinden.
            data = json.dumps(data if data is not None else {})
        frame = {"event": pub["event"], "data": data}
    return frame


# ── Was ein Schliesscode verlangt ────────────────────────────────────────
# Centrifugo teilt die Codes selbst ein: 3000–3499 und 4000–4499 heissen
# „neu verbinden", 3500–3999 und 4500–4999 „nicht unveraendert neu
# verbinden". Fuer diese Lage ist die Pause lang — ein abgelehntes Token
# alle paar Sekunden neu anzufragen war genau der Lärm, den der Betreiber
# gemeldet hat, und eine Sperre der Server-IP waere der naechste Schritt
# (von anderen Clients so beobachtet).
ENDGUELTIG_PAUSE_S = 900
BACKOFF_MAX_S = 120


def lage(code) -> str:
    if isinstance(code, int) and (3500 <= code <= 3999 or 4500 <= code <= 4999):
        return "endgueltig"
    return "gewoehnlich"


def pause(code, folge: int) -> int:
    """Pause vor dem naechsten Versuch; `folge` zaehlt Trennungen derselben
    Lage hintereinander (1 = die erste). Waechst, damit ein Kick-Ausfall
    nicht in eine Neuverbindung je Sekunde muendet (W133: 11975 in 3,5 h)."""
    if lage(code) == "endgueltig":
        return ENDGUELTIG_PAUSE_S
    return int(min(BACKOFF_MAX_S, 5 * 2 ** max(0, int(folge) - 1)))


async def _post(session, url, body, timeout_s):
    import aiohttp
    async with session.post(url, json=body, headers=KOPF,
                            timeout=aiohttp.ClientTimeout(total=timeout_s)) as r:
        text = await r.text()
        if r.status != 200:
            # 403 mit HTML ist Cloudflare, nicht Kicks Antwort auf uns —
            # das gehoert in den Text, sonst sucht man am Token.
            cf = " (Cloudflare-Seite)" if "cloudflare" in text.lower() else ""
            raise KickZentrifugoFehler("%s antwortete HTTP %d%s: %s"
                                       % (url, r.status, cf, text[:160]), code=r.status)
        try:
            return json.loads(text)
        except ValueError as e:
            raise KickZentrifugoFehler("%s lieferte kein JSON: %s" % (url, text[:160])) from e


async def zugang(session, client_id, timeout_s=15):
    """→ (Websocket-Adresse, Gast-Token). Wirft KickZentrifugoFehler."""
    url = ws_url_aus(await _post(session, VERBINDUNG_URL, verbindung_body(client_id), timeout_s))
    tok = await neues_token(session, client_id, timeout_s)
    return url, tok


async def neues_token(session, client_id, timeout_s=15) -> str:
    return token_aus(await _post(session, TOKEN_URL, {"client_id": client_id}, timeout_s))
