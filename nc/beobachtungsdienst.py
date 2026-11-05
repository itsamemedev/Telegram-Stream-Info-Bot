"""nc.beobachtungsdienst — Prometheus und Grafana verwalten (bot-frei, stdlib).

v4.2-W148. Der Betreiber am 05.11.: „wenn grafana und Prometheus installiert
sind auch diese 2 extra agenten/Wächter bekommen und grafana / Prometheus
vollständig verwalten / steuern." Bis hierher richtete tools/observability.sh
beides ein, und danach sah niemand mehr nach: fiel Prometheus aus, hörten die
Alarme auf, ohne dass ein Alarm kam — der Wächter, den man braucht, um den
Wächter zu bemerken.

Zwei Hälften:

  * LESEN — prometheus_lage() / grafana_lage() fragen die HTTP-APIs der
    beiden Dienste ab. Rein lesend, mit kurzem Zeitlimit, ohne Bot.
  * STEUERN — steuern() führt GENAU einen von drei festen systemd-Befehlen
    aus, per `sudo -n` (nie mit Passwortabfrage). Kein Teil des Befehls kommt
    aus einer Eingabe: der Aufrufer wählt nur einen Schlüssel aus STEUERUNG.
    Erlaubt sind die drei Befehle durch die sudoers-Regel, die
    tools/observability.sh anlegt — sonst nichts. Fehlt die Regel, sagt die
    Antwort, wie man sie bekommt, statt still zu scheitern.

Beide Wächter (brain/agents.py: PrometheusAgent, GrafanaAgent) und das Deck
(System → „Prometheus & Grafana") benutzen dieselben Funktionen.
"""

import base64
import json
import logging
import os
import subprocess
import urllib.parse
import urllib.request

log = logging.getLogger("TikTokBot")

ZEITLIMIT_S = 4
PROM_DIENST = "nightcrawler-prometheus.service"
GRAFANA_DIENST = "grafana-server.service"
DATENQUELLE_UID = "nightcrawler-prometheus"
DASHBOARD_UID = "nightcrawler"

# Die einzigen Befehle, die dieses Modul ausfuehrt. Die sudoers-Regel aus
# tools/observability.sh erlaubt genau diese — eine Zeile mehr hier wirkt
# ohne passende Regel nicht, und das ist Absicht.
STEUERUNG = {
    ("prometheus", "neu_laden"): ["systemctl", "reload", PROM_DIENST],
    ("prometheus", "neu_starten"): ["systemctl", "restart", PROM_DIENST],
    ("grafana", "neu_starten"): ["systemctl", "restart", GRAFANA_DIENST],
}


def installiert(env=None) -> dict:
    """Welche der beiden sind eingerichtet? Massgeblich ist die .env:
    tools/observability.sh traegt PROMETHEUS_URL und GRAFANA_URL erst ein,
    wenn der Dienst laeuft (W144)."""
    env = os.environ if env is None else env
    return {"prometheus": bool((env.get("PROMETHEUS_URL") or "").strip()),
            "grafana": bool((env.get("GRAFANA_URL") or "").strip())}


def _holen(url, kopf=None, zeitlimit=ZEITLIMIT_S):
    """(status, text) — wirft bei Netzfehlern; der Aufrufer nennt den Grund."""
    req = urllib.request.Request(url, headers=kopf or {})
    try:
        with urllib.request.urlopen(req, timeout=zeitlimit) as r:   # noqa: S310 — eigene Konfiguration
            return r.status, r.read(262144).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # Ein 401/404 ist eine Antwort, kein Ausfall — der Dienst lebt.
        log.debug("Beobachtung: %s -> HTTP %s", url.split("?")[0], e.code)
        return e.code, e.read(4096).decode("utf-8", "replace")


def _json(holen, url, kopf=None):
    status, text = holen(url, kopf) if kopf else holen(url)
    try:
        return status, json.loads(text)
    except ValueError:
        log.debug("Beobachtung: keine JSON-Antwort von %s (HTTP %s)", url.split("?")[0], status)
        return status, None


# ── Prometheus ──────────────────────────────────────────────────────────────

def prometheus_lage(url, holen=_holen) -> dict:
    """Alles, was ein Betreiber ueber den laufenden Prometheus wissen muss.

    erreichbar   /-/ready antwortet 200
    liest_bot    up{job="nightcrawler"} = 1 (None: noch kein Abruf)
    ziele_aus    Scrape-Ziele mit health != up — mit lastError
    regeln_aus   Regelgruppen/-regeln mit health != ok
    config_ok    der letzte Reload hat die Konfiguration angenommen
    alarme       feuernde Alarme: [{"name", "schwere", "text"}]
    serien       Kopfserien der TSDB (Groesse)"""
    aus = {"url": url, "erreichbar": False, "liest_bot": None, "ziele_aus": [],
           "regeln_aus": [], "config_ok": None, "alarme": [], "serien": None,
           "fehler": None}
    if not url:
        aus["fehler"] = "PROMETHEUS_URL fehlt"
        return aus
    basis = url.rstrip("/")
    try:
        status, _ = holen(basis + "/-/ready")
    except Exception as e:
        # debug, nicht warning: der Waechter macht daraus einen crit-Befund
        # (Entscheidungslog + Alarm) — eine zweite Zeile je Runde waere Laerm.
        log.debug("Prometheus %s nicht erreichbar: %s", basis, e)
        aus["fehler"] = "%s: %s" % (type(e).__name__, e)
        return aus
    aus["erreichbar"] = status == 200
    if not aus["erreichbar"]:
        aus["fehler"] = "HTTP %s auf /-/ready" % status
        return aus
    # Ab hier ist er da; einzelne Abfragen duerfen scheitern, ohne dass der
    # Rest verloren geht — jede Teilantwort fuer sich.
    try:
        _, d = _json(holen, basis + "/api/v1/query?" + urllib.parse.urlencode(
            {"query": 'up{job="nightcrawler"}'}))
        werte = [r["value"][1] for r in ((d or {}).get("data") or {}).get("result") or []]
        aus["liest_bot"] = (True if "1" in werte else False) if werte else None
        _, d = _json(holen, basis + "/api/v1/targets?state=active")
        for z in ((d or {}).get("data") or {}).get("activeTargets") or []:
            if z.get("health") != "up":
                aus["ziele_aus"].append({"job": (z.get("labels") or {}).get("job") or "?",
                                         "fehler": (z.get("lastError") or "")[:200]})
        _, d = _json(holen, basis + "/api/v1/rules")
        for g in ((d or {}).get("data") or {}).get("groups") or []:
            for r in g.get("rules") or []:
                if r.get("health") not in (None, "ok"):
                    aus["regeln_aus"].append({"regel": r.get("name") or "?",
                                              "fehler": (r.get("lastError") or "")[:200]})
        _, d = _json(holen, basis + "/api/v1/status/runtimeinfo")
        info = (d or {}).get("data") or {}
        if "reloadConfigSuccess" in info:
            aus["config_ok"] = bool(info["reloadConfigSuccess"])
        _, d = _json(holen, basis + "/api/v1/alerts")
        for a in ((d or {}).get("data") or {}).get("alerts") or []:
            if a.get("state") == "firing":
                lab, ann = a.get("labels") or {}, a.get("annotations") or {}
                aus["alarme"].append({"name": lab.get("alertname") or "?",
                                      "schwere": lab.get("severity") or "warning",
                                      "text": (ann.get("summary") or "")[:200]})
        _, d = _json(holen, basis + "/api/v1/status/tsdb")
        kopf = ((d or {}).get("data") or {}).get("headStats") or {}
        if "numSeries" in kopf:
            aus["serien"] = int(kopf["numSeries"])
    except Exception as e:
        log.info("Prometheus-Lage: Teilabfrage fehlgeschlagen: %s: %s", type(e).__name__, e)
        aus["fehler"] = "Teilabfrage: %s: %s" % (type(e).__name__, e)
    return aus


# ── Grafana ─────────────────────────────────────────────────────────────────

def _basic(nutzer, passwort):
    roh = ("%s:%s" % (nutzer, passwort)).encode("utf-8")
    return {"Authorization": "Basic " + base64.b64encode(roh).decode("ascii")}


def grafana_lage(url, nutzer="admin", passwort="", holen=_holen) -> dict:
    """erreichbar · db_ok · anmeldung_ok · quelle_ok · dashboard_da.
    Das Passwort verlaesst diese Funktion nie — nur, ob es passt."""
    aus = {"url": url, "erreichbar": False, "db_ok": None, "anmeldung_ok": None,
           "quelle_ok": None, "dashboard_da": None, "fehler": None}
    if not url:
        aus["fehler"] = "GRAFANA_URL fehlt"
        return aus
    basis = url.rstrip("/")
    try:
        status, d = _json(holen, basis + "/api/health")
    except Exception as e:
        log.debug("Grafana %s nicht erreichbar: %s", basis, e)
        aus["fehler"] = "%s: %s" % (type(e).__name__, e)
        return aus
    aus["erreichbar"] = status == 200
    if not aus["erreichbar"]:
        aus["fehler"] = "HTTP %s auf /api/health" % status
        return aus
    aus["db_ok"] = (d or {}).get("database") == "ok"
    if not passwort:
        return aus
    kopf = _basic(nutzer or "admin", passwort)
    try:
        status, _ = holen(basis + "/api/user", kopf)
        aus["anmeldung_ok"] = status == 200
        if aus["anmeldung_ok"]:
            status, d = _json(holen, basis + "/api/datasources/uid/%s/health" % DATENQUELLE_UID, kopf)
            aus["quelle_ok"] = status == 200 and (d or {}).get("status") == "OK"
            status, _ = holen(basis + "/api/dashboards/uid/%s" % DASHBOARD_UID, kopf)
            aus["dashboard_da"] = status == 200
    except Exception as e:
        log.info("Grafana-Lage: Teilabfrage fehlgeschlagen: %s: %s", type(e).__name__, e)
        aus["fehler"] = "Teilabfrage: %s: %s" % (type(e).__name__, e)
    return aus


# ── Steuern ─────────────────────────────────────────────────────────────────

def grafana_unit(wurzel="") -> str:
    """Debian/Ubuntu nennen den Dienst grafana-server, Arch grafana.
    observability.sh legt sein Drop-in unter dem echten Namen an — daran
    entschieden, nicht an einer Einstellung: ein Unit-Name aus der .env waere
    ein Befehlsteil aus Fremdeingabe."""
    for u in (GRAFANA_DIENST, "grafana.service"):
        if os.path.isfile(wurzel + "/etc/systemd/system/%s.d/nightcrawler.conf" % u):
            return u
    return GRAFANA_DIENST


def steuern(dienst, aktion, run=subprocess.run, wurzel="") -> dict:
    """Einen der festen Befehle aus STEUERUNG ausfuehren. -> {"ok", "text", "befehl"}"""
    befehl = STEUERUNG.get((dienst, aktion))
    if befehl is not None and dienst == "grafana":
        befehl = befehl[:2] + [grafana_unit(wurzel)]
    if befehl is None:
        return {"ok": False, "befehl": None,
                "text": "Unbekannte Steuerung %s/%s — erlaubt: %s" % (
                    dienst, aktion, ", ".join("%s/%s" % k for k in STEUERUNG))}
    voll = ["sudo", "-n"] + befehl
    try:
        r = run(voll, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        log.warning("Beobachtung: %s scheiterte: %s", " ".join(befehl), e)
        return {"ok": False, "befehl": " ".join(befehl), "text": "%s: %s" % (type(e).__name__, e)}
    if r.returncode == 0:
        log.info("Beobachtung: %s ausgefuehrt", " ".join(befehl))
        return {"ok": True, "befehl": " ".join(befehl), "text": "ausgefuehrt"}
    fehler = (r.stderr or r.stdout or "").strip()[:300]
    if "password is required" in fehler or "a terminal is required" in fehler:
        text = ("sudo verlangt ein Passwort — die Steuerregel fehlt. Einmal ausfuehren: "
                "sudo bash tools/observability.sh (legt /etc/sudoers.d/nightcrawler-beobachtung "
                "fuer genau diese drei Befehle an).")
    else:
        text = "rc=%s: %s" % (r.returncode, fehler or "keine Ausgabe")
    log.warning("Beobachtung: %s nicht ausgefuehrt — %s", " ".join(befehl), text)
    return {"ok": False, "befehl": " ".join(befehl), "text": text}


# ── Fuer Waechter und Deck: mit den Werten von JETZT ────────────────────────
# Als Funktion gelesen, nie als Modul-Konstante: .env und die Einstellungen
# aus dem Deck (W145) stehen beim Import noch nicht fest.

def prometheus_jetzt() -> dict:
    return prometheus_lage((os.getenv("PROMETHEUS_URL") or "").strip())


def grafana_jetzt() -> dict:
    return grafana_lage((os.getenv("GRAFANA_URL") or "").strip(),
                        (os.getenv("GRAFANA_ADMIN_USER") or "admin").strip(),
                        os.getenv("GRAFANA_ADMIN_PASSWORD") or "")


def selbstheilung_erlaubt(dienst: str) -> bool:
    """BRAIN_ACT_PROMETHEUS / BRAIN_ACT_GRAFANA, Vorgabe AN — anders als die
    uebrigen Aktions-Gates. Begruendet: das eigentliche Opt-in ist die
    sudoers-Regel, die nur `sudo bash tools/observability.sh` anlegt; ohne sie
    scheitert jeder Versuch mit einer Meldung, wie man sie bekommt. Und die
    beiden Dienste sind die eigenen Beobachter, nicht der Bot."""
    # Woertlich je Dienst, nicht zusammengesetzt: tools/gen_env_example.py
    # findet nur woertliche Namen, und ein Schalter, der in der Vorlage
    # fehlt, ist fuer den Betreiber nicht vorhanden (W99).
    if dienst == "prometheus":
        wert = os.getenv("BRAIN_ACT_PROMETHEUS")
    elif dienst == "grafana":
        wert = os.getenv("BRAIN_ACT_GRAFANA")
    else:
        return False
    return (wert or "1").strip().lower() in ("1", "true", "ja", "on")
