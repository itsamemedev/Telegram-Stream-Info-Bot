"""nc.kickapi — v4.1-W9: Kanal-Slug, Broadcaster-ID und der letzte Sendeversuch.

Aus bot.py geloest, damit nc/routes/kick.py die Kick-Diagnose direkt
importieren kann. `Ctx.__slots__` steht bei 24 von vertraglich 25 — die
Reihenfolge aus W117 gilt weiter: erst die Schicht, dann die Routen. Ohne
diesen Schritt haette /api/kick elf Kontext-Eintraege gekostet.

Die Koerper sind woertlich uebernommen.

`SEND_LAST` ist GETEILTER Zustand, kein Cache: der Kick-Sendepfad im Bot
schreibt hinein, die Diagnose-Route liest daraus. Zwei Kopien, und
/api/kick/sendcheck meldete ewig "noch kein Sendeversuch", waehrend der Chat
in Wahrheit seit Stunden mit 401 abgewiesen wird — genau die stille
Fehlanzeige, gegen die die Route ueberhaupt gebaut wurde (v4.0-W10).
"""

import os


class _Conf(dict):
    """Wirft laut statt einen nackten KeyError zu liefern — ein fehlender
       Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler."""

    def __missing__(self, key):
        raise RuntimeError(
            "nc.kickapi ist nicht konfiguriert (%r fehlt) — "
            "nc.kickapi.configure(...) fehlt im Startpfad von bot.py" % key)


_conf = _Conf()

# v4.0-W9: Broadcaster-ID, einmal aufgeloest, 1 h gecacht.
BID_CACHE = {"id": 0, "ts": 0.0}
# v4.0-W10: letzter Kick-Sendeversuch — damit ein stummer Kick-Chat nicht mehr
# still scheitert, sondern im Dashboard mit KLARTEXT-Grund sichtbar wird.
SEND_LAST = {"ts": 0.0, "ok": None, "error": "", "status": 0, "bid": 0}


def configure(*, log, get_session, time_mod, broadcaster_id_env,
              client_id, client_secret):
    """Vom Bot genau einmal beim Start gerufen.

    `get_session` ist die gepoolte aiohttp-Session des Bots — sie haengt am
    Laufzeitkern und bleibt dort. `broadcaster_id_env` kommt als WERT, nicht
    als os.getenv-Aufruf: der Bot friert KICK_BROADCASTER_ID beim Import
    ohnehin ein, und eine zweite Lesestelle koennte einen anderen Wert sehen.
    """
    _conf.update(log=log, get_session=get_session, time_mod=time_mod,
                 broadcaster_id_env=broadcaster_id_env,
                 client_id=client_id, client_secret=client_secret)


def slug():
    u = (os.getenv("KICK_CHANNEL_URL", "") or "").strip().rstrip("/")
    return u.rsplit("/", 1)[-1] if "/" in u else u


async def broadcaster_id():
    """v4.0-W9: Broadcaster-User-ID fuer den Kick-Chat-/Moderations-POST. Nutzt
       KICK_BROADCASTER_ID wenn gesetzt, sonst wird sie EINMALIG aus dem Kanal-Slug
       aufgeloest (kick.com/api/v2/channels/<slug> -> user_id) und 1h gecacht.
       OHNE sie lehnt Kick den Bot-POST ab (HTTP 400) -> AZRAEL bliebe auf Kick
       stumm und Kick-Timeouts wuerden still scheitern."""
    log = _conf["log"]
    _time_mod = _conf["time_mod"]
    if _conf["broadcaster_id_env"]:
        return _conf["broadcaster_id_env"]
    c = BID_CACHE
    if c["id"] and (_time_mod.time() - c["ts"] < 3600):
        return c["id"]
    s = slug()
    if not s:
        return 0
    try:
        import aiohttp
        session = await _conf["get_session"]()
        async with session.get(f"https://kick.com/api/v2/channels/{s}",
                               timeout=aiohttp.ClientTimeout(total=8),
                               headers={"User-Agent": "Mozilla/5.0"}) as r:
            if r.status != 200:
                return 0
            j = await r.json(content_type=None)
        bid = int(j.get("user_id") or (j.get("user") or {}).get("id") or 0)
        if bid:
            c.update(id=bid, ts=_time_mod.time())
            log.info("Kick-Broadcaster-ID aus Kanal aufgeloest: %s", bid)
        return bid
    except Exception as e:
        log.debug("kick broadcaster-id: %s", e)
        return 0


async def oauth_exchange(code, pending):
    """Autorisierungs-Code gegen ein Token-Paar tauschen (PKCE) und ablegen.

    Liegt hier und nicht im Blueprint, weil es die gepoolte Session und die
    Zugangsdaten braucht — beides ist schon konfiguriert. Im Blueprint waeren
    daraus zwei nc.ctx-Eintraege geworden, obwohl es reine Kick-API-Arbeit ist.
    """
    import aiohttp
    from nc import kick_oauth as _ko
    from nc.cfgstore import set_ as _cfg_set
    from nc.oauthredirect import redirect_uri as _redirect_uri

    payload = _ko.token_exchange_payload(
        _conf["client_id"], _conf["client_secret"],
        pending.get("redirect") or _redirect_uri("kick"), code, pending.get("verifier"))
    session = await _conf["get_session"]()
    async with session.post(_ko.TOKEN_URL, data=payload,
                            timeout=aiohttp.ClientTimeout(total=20)) as r:
        data = await r.json(content_type=None)
    tok, err = _ko.parse_token_response(data, _conf["time_mod"].time())
    if not tok:
        return {"ok": False, "error": str(err)}
    _cfg_set("kick.user_token", tok)
    _conf["log"].info("Kick-User-OAuth verbunden (Scope: %s)", tok.get("scope", ""))
    return {"ok": True, "scope": tok.get("scope", "")}
