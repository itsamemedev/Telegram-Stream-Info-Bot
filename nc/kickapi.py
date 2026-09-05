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
              client_id, client_secret,
              cfg_get=None, cfg_set=None, follower_count=None):
    """Vom Bot genau einmal beim Start gerufen.

    `get_session` ist die gepoolte aiohttp-Session des Bots — sie haengt am
    Laufzeitkern und bleibt dort. `broadcaster_id_env` kommt als WERT, nicht
    als os.getenv-Aufruf: der Bot friert KICK_BROADCASTER_ID beim Import
    ohnehin ein, und eine zweite Lesestelle koennte einen anderen Wert sehen.
    """
    _conf.update(log=log, get_session=get_session, time_mod=time_mod,
                 broadcaster_id_env=broadcaster_id_env,
                 client_id=client_id, client_secret=client_secret)
    # v4.2-W12: was der Bot fuer die REST-Aufrufe zusaetzlich stellen muss.
    # cfg_get/cfg_set sind der app_config-Speicher (der User-Token liegt dort,
    # nicht in der .env — er wird zur Laufzeit erneuert). follower_count haengt
    # an einem ANDEREN Session-Pool des Bots als get_session; deshalb kommt es
    # als Rueckruf und nicht als eigener Aufruf hier.
    _conf.setdefault("cfg_get", None)
    _conf.setdefault("cfg_set", None)
    _conf.setdefault("follower_count", None)
    for name, wert in (("cfg_get", cfg_get), ("cfg_set", cfg_set),
                       ("follower_count", follower_count)):
        if wert is not None:
            _conf[name] = wert


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


# ══════════════════════════════════════════════════════════════════════
# v4.2-W12: die Kick-REST-Aufrufe. Woertlich aus KickModerator geloest.
# ══════════════════════════════════════════════════════════════════════
# Was hier steht, spricht mit api.kick.com und sonst mit niemandem. Was NICHT
# hier steht: der Moderations-Logeintrag und `last_spoken` — das ist Zustand
# des Bots, und er bleibt dort. Der Aufrufer bekommt das Ergebnis und
# entscheidet selbst, was er damit protokolliert.
#
# WARUM DIE TOKENFRAGE ZWEIGETEILT IST (v4.0-W17): Kick kennt zwei Tokens, und
# der Unterschied hat Wochen gekostet. Der APP-Token (client_credentials) darf
# LESEN, aber weder im Chat schreiben noch moderieren noch den Kanal aendern —
# dort antwortet Kick mit einem nackten 401, das nach einem kaputten Schluessel
# aussieht und in Wahrheit "falsche Token-Art" heisst. Schreibende Wege nehmen
# deshalb zuerst den USER-Token und fallen nur zurueck, damit die Fehlermeldung
# den Grund nennen kann.

CHAT_URL = "https://api.kick.com/public/v1/chat"
BANS_URL = "https://api.kick.com/public/v1/moderation/bans"
CHANNELS_URL = "https://api.kick.com/public/v1/channels"
CATEGORIES_URL = "https://api.kick.com/public/v1/categories"

# App-Token, modulweit statt je Objekt: es gibt genau einen Kick-Zugang.
# Lag der Cache am KickModerator, holte jede Neuanlage des Objekts einen
# frischen Token — bei Kick ein zusaetzlicher OAuth-Aufruf pro Neustart der
# Chat-Schleife.
APP_TOKEN = {"token": "", "exp": 0.0}


async def app_token(session):
    """Der APP-Token (client_credentials). None, wenn nicht konfiguriert.

    30 s Sicherheitsabstand vor dem Ablauf: ein Token, der waehrend des
    Requests verfaellt, kommt als 401 zurueck und sieht aus wie ein
    Rechteproblem.
    """
    log = _conf["log"]
    _time_mod = _conf["time_mod"]
    if APP_TOKEN["token"] and _time_mod.monotonic() < APP_TOKEN["exp"] - 30:
        return APP_TOKEN["token"]
    cid, csec = _conf["client_id"], _conf["client_secret"]
    if not (cid and csec):
        return None
    try:
        import aiohttp
        async with session.post(
                "https://id.kick.com/oauth/token",
                data={"grant_type": "client_credentials",
                      "client_id": cid, "client_secret": csec},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status != 200:
                log.warning("Kick OAuth HTTP %s", resp.status)
                return None
            d = await resp.json()
            APP_TOKEN["token"] = d.get("access_token")
            APP_TOKEN["exp"] = _time_mod.monotonic() + int(d.get("expires_in", 3600))
            return APP_TOKEN["token"]
    except Exception as e:
        log.warning("Kick OAuth Fehler: %s", e)
        return None


async def user_token(session=None):
    """Der USER-Token (channel:write / chat:write / moderation:ban) oder None.

    Liegt im app_config-Speicher, nicht in der .env: er wird zur Laufzeit
    erneuert. Laesst sich der Refresh nicht durchfuehren, wird der ALTE Token
    zurueckgegeben statt None — dann entscheidet Kicks 401, ob er noch gilt.
    Ein vorschnelles None waere der schlechtere Weg: es faellt still auf den
    App-Token zurueck, und der darf nicht schreiben.
    """
    log = _conf["log"]
    _time_mod = _conf["time_mod"]
    cfg_get, cfg_set = _conf.get("cfg_get"), _conf.get("cfg_set")
    if not cfg_get:
        return None
    from nc import kick_oauth as _oauth
    tok = cfg_get("kick.user_token", None) or {}
    if not tok.get("access_token"):
        return None
    if not _oauth.is_expired(tok, _time_mod.time()):
        return tok["access_token"]
    rt = tok.get("refresh_token")
    cid, csec = _conf["client_id"], _conf["client_secret"]
    if not (rt and cid and csec):
        return tok.get("access_token")
    import aiohttp
    own = session is None
    if own:
        session = aiohttp.ClientSession()
    try:
        payload = _oauth.token_refresh_payload(cid, csec, rt)
        async with session.post(_oauth.TOKEN_URL, data=payload,
                                timeout=aiohttp.ClientTimeout(total=15)) as r:
            data = await r.json(content_type=None)
        neu, err = _oauth.parse_token_response(data, _time_mod.time())
        if neu:
            if cfg_set:
                cfg_set("kick.user_token", neu)
            log.info("Kick-User-Token erneuert (Scope: %s)", neu.get("scope", ""))
            return neu["access_token"]
        log.warning("Kick-Token-Refresh abgelehnt: %s", err)
        return tok.get("access_token")
    except Exception as e:
        log.debug("Kick-Token-Refresh Fehler: %s", e)
        return tok.get("access_token")
    finally:
        if own:
            await session.close()


async def _schreib_token(session):
    """Token fuer einen SCHREIBENDEN Aufruf. -> (token, war_user_token)"""
    ut = await user_token(session)
    return (ut or await app_token(session)), bool(ut)


async def send_message(content, session=None):
    """In den eigenen Kick-Chat schreiben. -> (ok, fehlertext oder None)

    SEND_LAST wird IMMER gesetzt, auch im Fehlerfall — das ist die einzige
    Stelle, an der ein stummer Kick-Chat sichtbar wird (v4.0-W10). Ohne sie
    meldete die Diagnose ewig "noch kein Sendeversuch", waehrend Kick seit
    Stunden mit 401 abweist.
    """
    import aiohttp
    _time_mod = _conf["time_mod"]
    own = False
    if session is None:
        session = aiohttp.ClientSession()
        own = True
    try:
        tok, ist_user = await _schreib_token(session)
        if not tok:
            SEND_LAST.update(ts=_time_mod.time(), ok=False, status=0, bid=0,
                             error="kein Token — KICK_CLIENT_ID/SECRET pruefen "
                                   "bzw. Kick im Dashboard verbinden")
            return False, "kein Token (client id/secret?)"
        payload = {"type": "user" if ist_user else "bot", "content": content[:480]}
        bid = _conf["broadcaster_id_env"] or await broadcaster_id()
        if bid:
            payload["broadcaster_user_id"] = bid
        async with session.post(
                CHAT_URL, json=payload,
                headers={"Authorization": "Bearer %s" % tok},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            ok = 200 <= resp.status < 300
            # Kicks ANTWORTTEXT mitnehmen: "HTTP 400" allein sagt nicht, ob
            # Broadcaster-ID, Scope oder Inhalt schuld ist.
            detail = ""
            if not ok:
                try:
                    detail = (await resp.text())[:180].replace("\n", " ").strip()
                except Exception:
                    detail = ""
                if not bid:
                    detail = (detail + " · keine Broadcaster-ID aufloesbar "
                              "(KICK_BROADCASTER_ID setzen)").strip()
                if resp.status in (401, 403) and not ist_user:
                    detail = (detail + " · App-Token darf nicht chatten — Kick im "
                              "Dashboard verbinden (Scope chat:write)").strip()
            SEND_LAST.update(
                ts=_time_mod.time(), ok=ok, status=resp.status, bid=bid,
                error=("" if ok else "HTTP %s" % resp.status
                       + (": %s" % detail if detail else "")))
            return ok, (None if ok else SEND_LAST["error"])
    except Exception as e:
        SEND_LAST.update(ts=_time_mod.time(), ok=False, status=0,
                         error=str(e)[:180])
        return False, str(e)
    finally:
        if own:
            await session.close()


async def timeout_user(user_id, minutes, reason, session):
    """Einen Zuschauer stummschalten. -> bool

    Die Dauer wird auf 1 Minute bis 7 Tage geklemmt: Kick lehnt alles
    ausserhalb ab, und eine abgelehnte Moderation sieht im Log aus wie eine
    durchgefuehrte.
    """
    import aiohttp
    try:
        tok, _ = await _schreib_token(session)
        if not tok:
            return False
        payload = {"user_id": user_id,
                   "duration": max(1, min(minutes, 10080)),
                   "reason": reason[:100]}
        bid = _conf["broadcaster_id_env"] or await broadcaster_id()
        if bid:
            payload["broadcaster_user_id"] = bid
        async with session.post(
                BANS_URL, json=payload,
                headers={"Authorization": "Bearer %s" % tok},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


async def channel_info(session=None):
    """Kanalzustand: live, Zuschauer, Titel, Kategorie, Follower.

    -> (dict, None) oder (None, fehlertext). Nur LESEND, deshalb reicht der
    App-Token.
    """
    import aiohttp
    own = False
    if session is None:
        session = aiohttp.ClientSession()
        own = True
    try:
        tok = await app_token(session)
        if not tok:
            return None, "kein Token"
        params = {}
        bid = _conf["broadcaster_id_env"] or await broadcaster_id()
        if bid:
            params["broadcaster_user_id"] = bid
        async with session.get(
                CHANNELS_URL, params=params,
                headers={"Authorization": "Bearer %s" % tok},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if not (200 <= resp.status < 300):
                return None, "HTTP %s" % resp.status
            d = await resp.json()
        row = (d.get("data") or [None])
        row = row[0] if isinstance(row, list) and row else d
        stream = (row or {}).get("stream") or {}
        # B138: followers_count steht in der v1-Antwort NICHT drin — deshalb
        # blieb die Anzeige auf "—", obwohl Zuschauer und Titel ankamen.
        # Rueckfall auf den keylosen v2-Endpunkt, den der Bot stellt.
        fol = (row or {}).get("followers_count")
        if fol is None and _conf.get("follower_count"):
            fol = await _conf["follower_count"](session)
        return {
            "slug": (row or {}).get("slug"),
            "title": (row or {}).get("stream_title") or stream.get("title"),
            "category": ((row or {}).get("category") or {}).get("name"),
            "is_live": bool(stream.get("is_live")),
            "viewers": stream.get("viewer_count"),
            "followers": fol,
        }, None
    except Exception as e:
        return None, str(e)
    finally:
        if own:
            await session.close()


async def update_channel(title=None, category_id=None, session=None):
    """Titel und/oder Kategorie setzen. -> (ok, fehlertext oder None)"""
    import aiohttp
    own = False
    if session is None:
        session = aiohttp.ClientSession()
        own = True
    try:
        tok, ist_user = await _schreib_token(session)
        if not tok:
            return False, "kein Token"
        payload = {}
        if title is not None:
            payload["stream_title"] = title[:140]
        if category_id:
            payload["category_id"] = int(category_id)
        if not payload:
            return False, "nichts zu ändern"
        async with session.patch(
                CHANNELS_URL, json=payload,
                headers={"Authorization": "Bearer %s" % tok},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if 200 <= resp.status < 300:
                return True, None
            # B164: Klartext statt nacktem "HTTP 401" — der App-Token darf
            # einen Kanal nicht editieren, und das sieht man ihm nicht an.
            if resp.status in (401, 403):
                return False, ("Kick: App-Token darf Titel/Kategorie nicht setzen — "
                               "User-OAuth mit Scope channel:write nötig")
            return False, "HTTP %s" % resp.status
    except Exception as e:
        return False, str(e)
    finally:
        if own:
            await session.close()


async def search_category(query, session=None):
    """B142: Kategorie per Name suchen. -> (id, name) oder (None, None).

    Ein exakter Namenstreffer schlaegt den ersten Treffer: Kick sortiert nach
    Beliebtheit, und "Just Chatting" waere sonst die Antwort auf fast alles.
    """
    import aiohttp
    log = _conf["log"]
    q = (query or "").strip()
    if not q:
        return None, None
    own = False
    if session is None:
        session = aiohttp.ClientSession()
        own = True
    try:
        tok = await app_token(session)
        if not tok:
            return None, None
        async with session.get(
                CATEGORIES_URL, params={"q": q},
                headers={"Authorization": "Bearer %s" % tok},
                timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if not (200 <= resp.status < 300):
                return None, None
            j = await resp.json(content_type=None)
        data = j.get("data") if isinstance(j, dict) else j
        data = data or []
        if not data:
            return None, None
        exakt = next((d for d in data
                      if (d.get("name") or "").strip().lower() == q.lower()), None)
        treffer = exakt or data[0]
        return treffer.get("id"), treffer.get("name")
    except Exception as e:
        log.debug("Kick search_category: %s", e)
        return None, None
    finally:
        if own:
            await session.close()
