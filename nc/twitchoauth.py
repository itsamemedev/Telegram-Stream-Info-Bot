"""nc.twitchoauth — Twitch-OAuth ohne manuellen Token-Tanz.

WARUM DAS EXISTIERT:
Der EventSub-Follower-Zaehler brauchte bisher einen von Hand erzeugten
User-Token (TWITCH_EVENTSUB_TOKEN), der
  1. an die richtige Client-ID gebunden sein muss (haeufigste Fehlerquelle:
     Token vom Generator gehoert zu DESSEN Client-ID, nicht zur eigenen),
  2. den Scope moderator:read:followers tragen muss,
  3. nach ~60 Tagen ablaeuft und dann still den Zaehler einfrieren laesst.

Dieser Flow ersetzt das durch: EINMAL im Browser autorisieren, danach hat der
Bot einen Refresh-Token und erneuert den Access-Token selbst — dauerhaft. Der
Nutzer gibt nur Client-ID + Secret an; die Bindung ist automatisch korrekt,
weil die Autorisierung gegen genau diese App laeuft.

Zwei Teile:
  - authorize_url() / exchange_code(): der einmalige Browser-Flow.
  - access_token(): liefert zur Laufzeit einen gueltigen Access-Token, erneuert
    ihn per Refresh-Token, wenn er ablaeuft. Das ist das Gegenstueck zu
    _yt_access_token() fuer YouTube.

Der Refresh-Token wird in einer Datei unter RECORDINGS_DIR persistiert (die .env
kann zur Laufzeit nicht geschrieben werden). Nur der Refresh-Token, keine
Access-Token — die sind kurzlebig und werden nie gespeichert.
"""
import json
import logging
import os
import time
import urllib.parse

log = logging.getLogger("TikTokBot")

# Scopes, die der Flow anfragt:
#   moderator:read:followers   — Follower-Zähler (EventSub)
#   chat:read / chat:edit       — AZRAEL liest UND schreibt im Twitch-Chat (IRC)
#   moderator:manage:banned_users — SENTINEL kann auf Twitch timeouten/bannen
# Ein Token trägt alle; damit deckt EINE Autorisierung Follower, Chat UND
# Moderation ab.
SCOPES = ["moderator:read:followers", "chat:read", "chat:edit",
          "moderator:manage:banned_users",
          # B142: erlaubt Titel + Kategorie (game_id) via Helix PATCH /channels
          "channel:manage:broadcast"]
AUTHORIZE = "https://id.twitch.tv/oauth2/authorize"
TOKEN = "https://id.twitch.tv/oauth2/token"
VALIDATE = "https://id.twitch.tv/oauth2/validate"

_state = {
    "store_path": None,
    "redirect_uri": "http://localhost:3000",
    "access": "",
    "access_exp": 0.0,
    "refresh": "",
    "csrf": "",
    "login": "",
}


def configure(store_path, redirect_uri=None):
    """Beim Start aufrufen: wo der Refresh-Token liegt, welche Redirect-URI gilt."""
    _state["store_path"] = store_path
    if redirect_uri:
        _state["redirect_uri"] = redirect_uri.strip()
    _load()


def _client():
    cid = (os.getenv("TWITCH_CLIENT_ID", "") or "").strip()
    csec = (os.getenv("TWITCH_CLIENT_SECRET", "") or "").strip()
    return cid, csec


def _load():
    p = _state.get("store_path")
    if not p or not os.path.exists(p):
        return
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        _state["refresh"] = (d.get("refresh_token") or "").strip()
    except Exception as e:
        log.debug("twitchoauth: Store nicht lesbar: %s", e)


def _save():
    p = _state.get("store_path")
    if not p:
        return
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"refresh_token": _state["refresh"]}, f)
        os.replace(tmp, p)
        try:
            os.chmod(p, 0o600)     # Refresh-Token ist ein Geheimnis
        except OSError:
            pass
    except Exception as e:
        log.warning("twitchoauth: Store nicht schreibbar: %s", e)


def status():
    """Fuers Dashboard: was ist konfiguriert, ist der Flow abgeschlossen?"""
    cid, csec = _client()
    return {
        "has_client_id": bool(cid),
        "has_secret": bool(csec),
        "has_refresh": bool(_state["refresh"]),
        "ready": bool(cid and csec and _state["refresh"]),
        "redirect_uri": _state["redirect_uri"],
        "scopes": SCOPES,
    }


def authorize_url(csrf, redirect_uri=None):
    """Schritt 1: den Link, den der Nutzer im Browser oeffnet. csrf schuetzt vor
       untergeschobenen Codes (state-Parameter).

       redirect_uri: die Adresse, an die Twitch zurueckschickt. Standard ist der
       konfigurierte Wert, aber das Dashboard uebergibt hier die tatsaechliche
       eigene URL — sonst zeigt der Redirect auf localhost:3000 (= das Geraet mit
       dem Browser, nicht der Server, auf dem der Bot laeuft)."""
    cid, _ = _client()
    if not cid:
        return None
    _state["csrf"] = csrf
    ru = (redirect_uri or _state["redirect_uri"]).strip()
    _state["last_redirect"] = ru      # fuer den Token-Tausch merken (muss gleich sein)
    q = urllib.parse.urlencode({
        "client_id": cid,
        "redirect_uri": ru,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": csrf,
        "force_verify": "true",
    })
    return AUTHORIZE + "?" + q


async def exchange_code(code, state, aiohttp):
    """Schritt 2: den ?code aus dem Redirect gegen Access+Refresh tauschen.
       Gibt (ok, meldung) zurueck."""
    # v4.0-W118 (SEC): frueher `if state and _state["csrf"] and ...` — die
    # Pruefung fiel weg, sobald der Rueckruf GAR KEINEN state mitbrachte. Genau
    # das kann ein Angreifer: er baut den Callback-Aufruf selbst und laesst den
    # Parameter einfach weg. Damit war der CSRF-Schutz mit einem Handgriff
    # abschaltbar. Jetzt gilt: wurde ein state ausgegeben, MUSS er passen.
    if _state["csrf"] and state != _state["csrf"]:
        return False, "state fehlt oder stimmt nicht (CSRF) — Flow neu starten"
    cid, csec = _client()
    if not (cid and csec):
        return False, "TWITCH_CLIENT_ID + TWITCH_CLIENT_SECRET fehlen"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(TOKEN, data={
                    "client_id": cid, "client_secret": csec,
                    "code": code, "grant_type": "authorization_code",
                    # MUSS exakt die Redirect-URI aus dem authorize-Schritt sein,
                    # sonst lehnt Twitch mit "redirect mismatch" ab.
                    "redirect_uri": _state.get("last_redirect") or _state["redirect_uri"]},
                    timeout=aiohttp.ClientTimeout(total=15)) as r:
                j = await r.json(content_type=None)
    except Exception as e:
        return False, f"Netzwerkfehler: {e}"
    rt = j.get("refresh_token")
    at = j.get("access_token")
    if not rt:
        return False, "Twitch gab keinen Refresh-Token (%s)" % j.get("message", j.get("error", "?"))
    _state["refresh"] = rt
    _state["access"] = at or ""
    _state["access_exp"] = time.time() + int(j.get("expires_in", 3600)) - 120
    _save()
    return True, "Twitch verbunden — Refresh-Token gespeichert, Follower-Zaehler aktiv"


async def login_name(aiohttp):
    """Der Login-Name des autorisierten Accounts (fuer den IRC-NICK beim Chat).
       Twitch verlangt, dass NICK = der Account ist, dem der Token gehoert.
       Gecacht, damit nicht jeder Reconnect eine Validate-Anfrage ausloest."""
    if _state.get("login"):
        return _state["login"]
    tok = await access_token(aiohttp)
    if not tok:
        return None
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(VALIDATE,
                             headers={"Authorization": "OAuth " + tok},
                             timeout=aiohttp.ClientTimeout(total=10)) as r:
                j = await r.json(content_type=None)
        _state["login"] = (j.get("login") or "").strip().lower()
        return _state["login"] or None
    except Exception as e:
        log.debug("twitchoauth: login_name-Fehler: %s", e)
        return None


async def timeout_user(aiohttp, login, minutes, reason=""):
    """SENTINEL-Timeout auf Twitch über die Helix-API. Braucht Scope
       moderator:manage:banned_users. broadcaster = moderator = der autorisierte
       Account (Henry ist beides). Gibt (ok, meldung) zurück.

       login: der Twitch-Nutzername, der getimeoutet werden soll.
    """
    cid, _ = _client()
    tok = await access_token(aiohttp)
    if not (cid and tok):
        return False, "kein OAuth-Token"
    try:
        async with aiohttp.ClientSession() as s:
            hdr = {"Client-Id": cid, "Authorization": "Bearer " + tok}
            # broadcaster-ID (= eigener Account) + Ziel-User-ID auflösen
            bid = await _user_id(s, hdr, await login_name(aiohttp))
            tid = await _user_id(s, hdr, login)
            if not (bid and tid):
                return False, "User-ID nicht auflösbar"
            body = {"data": {"user_id": tid,
                             "duration": max(1, min(int(minutes) * 60, 1209600)),
                             "reason": (reason or "")[:500]}}
            async with s.post(
                    "https://api.twitch.tv/helix/moderation/bans",
                    params={"broadcaster_id": bid, "moderator_id": bid},
                    headers=hdr, json=body,
                    timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status in (200, 201):
                    return True, "getimeoutet"
                j = await r.json(content_type=None)
                return False, "Twitch %s: %s" % (r.status, j.get("message", "?"))
    except Exception as e:
        return False, str(e)


async def _user_id(session, hdr, login):
    if not login:
        return None
    try:
        async with session.get("https://api.twitch.tv/helix/users",
                               params={"login": login}, headers=hdr,
                               timeout=session._timeout) as r:
            j = await r.json(content_type=None)
        d = j.get("data") or []
        return d[0]["id"] if d else None
    except Exception:
        return None


async def access_token(aiohttp):
    """Zur Laufzeit: gueltiger Access-Token, bei Bedarf per Refresh erneuert.
       None, wenn nichts konfiguriert ist. Gegenstueck zu _yt_access_token()."""
    now = time.time()
    if _state["access"] and now < _state["access_exp"]:
        return _state["access"]
    cid, csec = _client()
    rt = _state["refresh"]
    if not (cid and csec and rt):
        return None
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(TOKEN, data={
                    "client_id": cid, "client_secret": csec,
                    "refresh_token": rt, "grant_type": "refresh_token"},
                    timeout=aiohttp.ClientTimeout(total=15)) as r:
                j = await r.json(content_type=None)
    except Exception as e:
        log.warning("twitchoauth: Refresh-Netzwerkfehler: %s", e)
        return None
    at = j.get("access_token")
    if not at:
        # Refresh-Token ungueltig geworden (Passwortwechsel, Entzug) → neu autorisieren
        log.warning("twitchoauth: Refresh fehlgeschlagen (%s) — neu autorisieren",
                    j.get("message", j.get("error", "?")))
        _state["refresh"] = ""
        _save()
        return None
    _state["access"] = at
    _state["access_exp"] = now + int(j.get("expires_in", 3600)) - 120
    # Twitch rotiert den Refresh-Token bei jedem Refresh mit
    if j.get("refresh_token"):
        _state["refresh"] = j["refresh_token"]
        _save()
    return at


async def _own_broadcaster_id(session, hdr):
    """B142: Eigene broadcaster_id (= autorisierter Account). GET /helix/users
       ohne login liefert den Token-Inhaber."""
    try:
        async with session.get("https://api.twitch.tv/helix/users",
                               headers=hdr,
                               timeout=session._timeout) as r:
            j = await r.json(content_type=None)
        d = j.get("data") or []
        return d[0]["id"] if d else None
    except Exception:
        return None


async def search_category(aiohttp, query):
    """B142: Twitch-Kategorie (Spiel/IRL) per Name suchen → (game_id, name) oder
       (None, None). Nutzt Helix /search/categories; nimmt bevorzugt einen
       exakten (case-insensitiven) Namenstreffer, sonst den ersten Treffer."""
    q = (query or "").strip()
    if not q:
        return None, None
    tok = await access_token(aiohttp)
    cid, _ = _client()
    if not (tok and cid):
        return None, None
    hdr = {"Authorization": f"Bearer {tok}", "Client-Id": cid}
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.twitch.tv/helix/search/categories",
                             params={"query": q, "first": 20}, headers=hdr,
                             timeout=aiohttp.ClientTimeout(total=15)) as r:
                j = await r.json(content_type=None)
        data = j.get("data") or []
        if not data:
            return None, None
        exact = next((d for d in data
                      if (d.get("name") or "").strip().lower() == q.lower()), None)
        pick = exact or data[0]
        return pick.get("id"), pick.get("name")
    except Exception as e:
        log.debug("twitchoauth: search_category-Fehler: %s", e)
        return None, None


async def update_channel(aiohttp, title=None, game_id=None):
    """B142: Titel und/oder Kategorie (game_id) des eigenen Kanals setzen via
       Helix PATCH /channels. Braucht Scope channel:manage:broadcast — wurde er
       vor dieser Version autorisiert, fehlt er und Twitch antwortet 401; dann
       im Dashboard einmal neu verbinden. Rueckgabe (ok, err)."""
    tok = await access_token(aiohttp)
    cid, _ = _client()
    if not (tok and cid):
        return False, "kein Token"
    hdr = {"Authorization": f"Bearer {tok}", "Client-Id": cid,
           "Content-Type": "application/json"}
    body = {}
    if title is not None:
        body["title"] = str(title)[:140]
    if game_id:
        body["game_id"] = str(game_id)
    if not body:
        return False, "nichts zu ändern"
    try:
        async with aiohttp.ClientSession() as s:
            bid = await _own_broadcaster_id(s, hdr)
            if not bid:
                return False, "broadcaster_id nicht auflösbar"
            async with s.patch("https://api.twitch.tv/helix/channels",
                               params={"broadcaster_id": bid},
                               json=body, headers=hdr,
                               timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 204:
                    return True, None
                txt = (await r.text())[:200]
                if r.status == 401:
                    return False, "401 — Scope channel:manage:broadcast fehlt, Twitch neu verbinden"
                return False, f"HTTP {r.status}: {txt}"
    except Exception as e:
        return False, str(e)
