"""nc.oauthredirect — v4.1-W8: die Rueckruf-Adressen der OAuth-Flows.

Aus bot.py geloest, damit nc/routes/twitch.py und nc/routes/youtube.py sie
DIREKT importieren koennen statt sie sich durch nc.ctx reichen zu lassen.
`Ctx.__slots__` steht bei 24 von vertraglich 25 — die Reihenfolge aus W117
lautet deshalb: erst die Schicht loesen, dann die Routen. Danach kostet
/api/twitch null neue Kontext-Eintraege statt drei.

Die Koerper sind woertlich uebernommen; die Reihenfolge app_config → .env →
oeffentliche Basis-URL bleibt Wort fuer Wort dieselbe. Wer sie anfasst, aendert
gleichzeitig Kick, Twitch und YouTube — genau dafuer liegt sie an EINER Stelle.

Warum `configure()` und keine Modul-Konstanten: `.env` wird teils erst nach den
ersten Imports geladen (CLAUDE.md, "Modul-Konstanten frieren .env ein").
TRUSTED_PROXIES und DASHBOARD_PORT liest der Bot beim Start ohnehin einmal —
sie kommen von dort, damit hier keine zweite, moeglicherweise abweichende
Lesestelle entsteht. PUBLIC_BASE_URL und die *_REDIRECT_URI werden weiterhin
bei JEDEM Aufruf gelesen, exakt wie im Monolithen: sie sind live aenderbar.
"""

import os

from flask import request

from nc.cfgstore import get as _cfg_get


class _Conf(dict):
    """Wirft laut statt einen nackten KeyError zu liefern — ein fehlender
       Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler."""

    def __missing__(self, key):
        raise RuntimeError(
            "nc.oauthredirect ist nicht konfiguriert (%r fehlt) — "
            "nc.oauthredirect.configure(...) fehlt im Startpfad von bot.py" % key)


_conf = _Conf()


def configure(*, trusted_proxies, loopback, dashboard_port):
    """Vom Bot genau einmal beim Start gerufen."""
    _conf.update(trusted_proxies=trusted_proxies, loopback=loopback,
                 dashboard_port=dashboard_port)


def public_base_url() -> str:
    """Die Basis-URL, unter der dieses Dashboard von aussen erreichbar ist —
       also das, was im Browser steht (z.B. https://example.dev:8050).

       WARUM: Alle OAuth-Rueckrufe laufen ueber den nginx-Proxy. Kick konnte
       seine Redirect-URI im Dashboard setzen, Twitch und YouTube hatten nur
       .env und sonst 'http://localhost:3000' — eine Adresse, die weder Google
       noch der Betreiber je zu Gesicht bekommt. Folge: Google bricht mit
       redirect_uri_mismatch ab, BEVOR die Kontoauswahl erscheint, und weil der
       Flow nie durchlief, gab es auch nie den Trennen-Knopf. Aus einer falschen
       Adresse wurden drei Symptome.

       Reihenfolge: PUBLIC_BASE_URL (.env) → Proxy-Header, aber NUR von einem
       vertrauten Absender (TRUSTED_PROXIES oder Loopback — sonst koennte
       jeder per gefaelschtem X-Forwarded-Host die Rueckruf-Adresse umbiegen)
       → Host-Header → localhost:DASHBOARD_PORT."""
    forced = (os.getenv("PUBLIC_BASE_URL", "") or "").strip().rstrip("/")
    if forced:
        return forced
    try:
        remote = (request.remote_addr or "").strip()
        proto = host = port = ""
        if remote in _conf["trusted_proxies"] or remote in _conf["loopback"]:
            def _h(name):
                return (request.headers.get(name, "") or "").split(",")[0].strip()
            proto, host, port = _h("X-Forwarded-Proto"), _h("X-Forwarded-Host"), _h("X-Forwarded-Port")
        host = host or (request.headers.get("Host", "") or "").strip()
        # nginx setzt in der Regel nur $host — ohne Port. Läuft das Dashboard
        # unter einem anderen Port als 80/443 (hier: 8050), fehlt der in der
        # Rückruf-Adresse, und Google lehnt sie als fremd ab. X-Forwarded-Port
        # schließt die Lücke, wenn der Proxy ihn mitschickt.
        if port and ":" not in host and port not in ("80", "443"):
            host = f"{host}:{port}"
        if host:
            return f"{proto or request.scheme or 'https'}://{host}".rstrip("/")
    except Exception:
        # Kein Request-Kontext (Start, Hintergrund-Task) — dann der Fallback.
        pass
    return f"http://localhost:{_conf['dashboard_port']}"


def redirect_env(platform: str) -> str:
    """Die .env-Vorgabe je Plattform.

       Bewusst ausgeschrieben statt os.getenv(f"{platform.upper()}_REDIRECT_URI"):
       tools/gen_env_example.py findet Variablen nur als Literal. Ein dynamisch
       gebauter Name fehlt danach in der .env-Vorlage — und was dort fehlt,
       existiert fuer den Betreiber nicht."""
    return {
        "kick": os.getenv("KICK_REDIRECT_URI", ""),
        "twitch": os.getenv("TWITCH_REDIRECT_URI", ""),
        "youtube": os.getenv("YOUTUBE_REDIRECT_URI", ""),
    }.get(platform, "").strip()


def redirect_uri(platform: str) -> str:
    """Redirect-URI eines OAuth-Flows. app_config schlaegt .env schlaegt die
       oeffentliche Basis-URL. Damit gilt fuer Kick, Twitch und YouTube
       dieselbe Regel — und hinter dem Proxy stimmt sie ohne Konfiguration."""
    saved = (_cfg_get(f"{platform}.redirect_uri", "") or "").strip()
    if saved:
        return saved
    env = redirect_env(platform)
    if env:
        return env
    return f"{public_base_url()}/api/{platform}/oauth/callback"


def redirect_source(platform: str) -> str:
    """Woher stammt die aktive Redirect-URI? Fuer die Dashboard-Warnung."""
    if (_cfg_get(f"{platform}.redirect_uri", "") or "").strip():
        return "config"
    if redirect_env(platform):
        return "env"
    return "fallback"


def redirect_public(uri) -> bool:
    """False, wenn die URI auf localhost/127.0.0.1 zeigt — dann kann die
       Plattform sie extern NICHT erreichen und der OAuth-Rueckruf schlaegt
       fehl. Hiess in bot.py _kick_redirect_public, galt aber laengst fuer alle
       drei Flows (Twitch und YouTube riefen dieselbe Funktion)."""
    u = (uri or "").lower()
    return not ("localhost" in u or "127.0.0.1" in u or "://0.0.0.0" in u)
