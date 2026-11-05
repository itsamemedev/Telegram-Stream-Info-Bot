"""nc.beobachtungslage — liest Prometheus den Bot wirklich, und ist Grafana da? (rein)

v4.2-W144. tools/observability.sh traegt PROMETHEUS_URL und GRAFANA_* in die
.env ein. Gelesen hat sie bis hierher niemand — und „eingerichtet" sagt
nichts darueber, ob Prometheus den Bot auch ABFRAGT: ein falscher
DASHBOARD_PORT, ein Deck auf einer fremden Adresse, und Prometheus sammelt
still `up=0`. Das Deck fragt deshalb Prometheus selbst nach `up` fuer den
Bot und sagt, was es fand — mit Abhilfe, nicht als blankes „nicht erreichbar".

Gemessen wird nur auf Abruf (Knopf im Deck), nie in /healthz: der Endpunkt
haengt an UptimeRobot und darf nicht auf ein Netz warten (W105).
Das Grafana-Passwort verlaesst diese Funktion nie — nur, OB es hinterlegt ist.

Die Gruende sind Benutzertext: `_t` uebersetzt die VORLAGE, bevor die Werte
eingesetzt werden — ein Katalogeintrag fuer den fertigen Satz traefe nie.
tools/i18n_extract.py sammelt die `_t("…")` dieser Datei ein (MARKIERT).
"""

import json
import logging
import os
import urllib.parse
import urllib.request

ZEITLIMIT_S = 3
log = logging.getLogger("TikTokBot")
TUNNEL_BEFEHL = "ssh -L 3001:127.0.0.1:3000 <server>   →   http://localhost:3001"


def _holen(url, zeitlimit=ZEITLIMIT_S):
    """(status, text) — wirft bei Netzfehlern; der Aufrufer nennt den Grund."""
    with urllib.request.urlopen(url, timeout=zeitlimit) as r:   # noqa: S310 — eigene Konfiguration
        return r.status, r.read(65536).decode("utf-8", "replace")


def _ohne(s):
    return s


def prometheus(url, holen=_holen, _t=_ohne):
    aus = {"url": url, "konfiguriert": bool(url), "erreichbar": False,
           "liest_bot": None, "grund": ""}
    if not url:
        aus["grund"] = _t("PROMETHEUS_URL fehlt in der .env — einrichten mit "
                           "sudo bash tools/observability.sh")
        return aus
    q = url.rstrip("/") + "/api/v1/query?" + urllib.parse.urlencode(
        {"query": 'up{job="nightcrawler"}'})
    try:
        status, text = holen(q)
    except Exception as e:
        # Auf Knopfdruck im Deck, nicht im Takt — eine Zeile je Fehlschlag
        # flutet nichts und steht im Log, wenn jemand spaeter nachsieht.
        log.info("Beobachtung: Prometheus %s nicht erreichbar: %s", url, e)
        aus["grund"] = _t("Prometheus antwortet nicht (%s: %s) — systemctl status "
                           "nightcrawler-prometheus") % (type(e).__name__, e)
        return aus
    aus["erreichbar"] = status == 200
    try:
        werte = [r["value"][1] for r in json.loads(text)["data"]["result"]]
    except (ValueError, KeyError, TypeError, IndexError) as e:
        log.info("Beobachtung: Antwort von Prometheus nicht lesbar: %s", e)
        aus["grund"] = _t("Antwort von Prometheus nicht lesbar (%s)") % type(e).__name__
        return aus
    if not werte:
        aus["grund"] = _t("Prometheus kennt den Bot noch nicht — kurz nach dem Start normal "
                           "(erster Abruf nach 30 s), sonst fehlt der Job in prometheus.yml.")
    elif "1" in werte:
        aus["liest_bot"] = True
    else:
        aus["liest_bot"] = False
        aus["grund"] = _t("Prometheus erreicht den Bot nicht (up=0) — stimmt DASHBOARD_PORT, "
                           "lauscht das Deck auf 127.0.0.1? bash tools/observability.sh --check")
    return aus


def grafana(url, passwort_gesetzt, holen=_holen, _t=_ohne):
    aus = {"url": url, "konfiguriert": bool(url), "erreichbar": False,
           "passwort_hinterlegt": bool(passwort_gesetzt), "grund": "",
           "tunnel": TUNNEL_BEFEHL}
    if not url:
        aus["grund"] = _t("Grafana nicht eingerichtet — sudo bash tools/observability.sh --grafana")
        return aus
    try:
        status, _ = holen(url.rstrip("/") + "/api/health")
        aus["erreichbar"] = status == 200
    except Exception as e:
        log.info("Beobachtung: Grafana %s nicht erreichbar: %s", url, e)
        aus["grund"] = _t("Grafana antwortet nicht (%s) — systemctl status grafana-server") % type(e).__name__
        return aus
    if not passwort_gesetzt:
        aus["grund"] = _t("GRAFANA_ADMIN_PASSWORD fehlt in der .env — Grafana steht womoeglich "
                           "noch auf admin/admin. sudo bash tools/observability.sh --grafana setzt eins.")
    return aus


def lage(holen=_holen, _t=_ohne):
    """Beides zusammen, fuer /api/beobachtung/lage.

    Woertlich os.getenv("NAME"): tools/gen_env_example.py findet die Namen
    nur so — sonst fehlten sie in der Vorlage (W99)."""
    return {
        "prometheus": prometheus((os.getenv("PROMETHEUS_URL") or "").strip(), holen, _t),
        "grafana": grafana((os.getenv("GRAFANA_URL") or "").strip(),
                           bool((os.getenv("GRAFANA_ADMIN_PASSWORD") or "").strip()), holen, _t),
    }
