"""nc.tiktokcheck — v4.1-W5: existiert dieser TikTok-Account noch?

Aus bot.py geloest, damit nc/routes/streamer.py die Pruefung direkt importieren
kann statt sie sich durch nc.ctx reichen zu lassen — der Kontext steht an seiner
Obergrenze, und die Reihenfolge aus W117 lautet: erst den Kern loesen, dann die
Routen. Der Koerper ist woertlich uebernommen.

BEWUSST KONSERVATIV, und das ist der ganze Punkt des Moduls: "gone" nur bei
eindeutigem Signal. Die Server-IP ist bei TikTok geblockt; ein blindes "nicht
gefunden" wuerde echte Accounts in der Oberflaeche loeschbar machen.
"""

from nc.proxyutil import get_random_proxy


class _Conf(dict):
    """Wirft laut statt einen nackten KeyError zu liefern — ein fehlender
       Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler."""

    def __missing__(self, key):
        raise RuntimeError(
            "nc.tiktokcheck ist nicht konfiguriert (%r fehlt) — "
            "nc.tiktokcheck.configure(...) fehlt im Startpfad von bot.py" % key)


_conf = _Conf()


def configure(*, get_ai_session, pick_proxy, live_resolver_headers):
    """Vom Bot genau einmal beim Start gerufen.

    Alle drei haengen am Laufzeitkern des Bots: die gepoolte aiohttp-Session,
    die Just-in-Time-Proxy-Wahl und die Kopfzeilen, mit denen auch die
    Live-Aufloesung spricht. Sie bleiben dort — hier kommt nur, was gebraucht
    wird, damit die Pruefung ueber denselben Weg laeuft wie der Resolver.
    """
    _conf.update(get_ai_session=get_ai_session, pick_proxy=pick_proxy,
                 live_resolver_headers=live_resolver_headers)


async def account_exists(username):
    """Prüft, ob @username auf TikTok noch existiert.
    Return ("exists"|"gone"|"unknown", http_status, detail).

    BEWUSST KONSERVATIV: „gone" nur bei eindeutigem Signal (HTTP 404 oder TikToks
    „Account nicht auffindbar"). Bei Block/Captcha/Rate-Limit/Netzfehler → „unknown",
    damit die Oberfläche KEIN Löschen anbietet — die OVH-IP ist bei TikTok geblockt,
    ein blindes „nicht gefunden" würde sonst echte Accounts löschbar machen. Läuft
    deshalb über denselben Pull-Proxy wie die Live-Auflösung."""
    import aiohttp
    username = (username or "").lstrip("@").strip()
    if not username:
        return ("unknown", 0, "leerer Name")
    # v4.2-W89: die drei Startwerte werden VOR dem Auffangen geholt.
    #
    # `_Conf.__missing__` wirft ausdruecklich laut ("Verdrahtungsfehler im
    # Bot, kein Datenfehler") — und genau dieser RuntimeError lief bis hier
    # in ein `except Exception: proxy = None`. Eine fehlende
    # `configure(...)`-Zeile im Startpfad sah damit aus wie "Proxy nicht
    # verfuegbar": die Pruefung lief ungeproxyt von der Server-IP weiter,
    # TikTok blockt die, und der Betreiber bekam "kein eindeutiges Signal"
    # statt der Wahrheit. Der lauteste Fehler des Moduls war der
    # unsichtbarste.
    #
    # Der Zugriff steht deshalb ausserhalb des try, der AUFRUF darin: eine
    # gescheiterte Proxy-Wahl ist ein Betriebsfall und darf still auf den
    # Zufallsproxy zurueckfallen; eine fehlende Verdrahtung ist keiner.
    waehler = _conf["pick_proxy"]
    sitzung = _conf["get_ai_session"]
    kopfzeilen = _conf["live_resolver_headers"]

    proxy = None
    try:
        proxy = await waehler(username=username)
    except Exception:
        proxy = None
    if not proxy:
        try:
            proxy = get_random_proxy()
        except Exception:
            proxy = None
    url = f"https://www.tiktok.com/@{username}"
    # v4.2-W89: `st` vorher gesetzt. Im except unten stand eine harte 0,
    # obwohl der Status zu diesem Zeitpunkt schon gelesen sein kann — ein
    # Abbruch beim Lesen des Rumpfes (Verbindung weg nach den Kopfzeilen)
    # warf den Status weg und meldete "HTTP 0". Damit war nicht mehr
    # unterscheidbar, ob TikTok geantwortet hat oder ob die Verbindung nie
    # zustande kam, und genau diese Unterscheidung entscheidet, ob die
    # Oberflaeche ein Loeschen anbieten darf.
    st = 0
    try:
        sess = await sitzung()
        _to = aiohttp.ClientTimeout(total=15)
        async with sess.get(url, headers=kopfzeilen, proxy=proxy,
                            allow_redirects=True, timeout=_to) as r:
            st = r.status
            if st == 404:
                return ("gone", 404, "TikTok liefert 404 für das Profil")
            if st in (403, 429):
                return ("unknown", st, f"TikTok blockt/limitet ({st}) — später erneut")
            body = await r.text(errors="ignore")
    except Exception as e:
        return ("unknown", st, f"Abfrage fehlgeschlagen: {str(e)[:80]}")
    low = body.lower()
    if ('"statuscode":10221' in low or '"statuscode":10202' in low
            or "couldn't find this account" in low
            or "couldn\u2019t find this account" in low):
        return ("gone", st, "TikTok: Account nicht auffindbar")
    if ('"uniqueid":"' + username.lower() + '"' in low
            or "__universal_data_for_rehydration__" in low
            or '"userinfo"' in low):
        return ("exists", st, "Profil vorhanden")
    if "captcha" in low or "verify to continue" in low:
        return ("unknown", st, "TikTok-Captcha/Block — später erneut prüfen")
    return ("unknown", st, "kein eindeutiges Signal (evtl. Block) — später erneut")
