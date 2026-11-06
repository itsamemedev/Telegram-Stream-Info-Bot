"""nc.geschuetzt — live, aber fuer uns verschlossen (rein, bot-frei).

v4.2-W154. Aus dem Log des Betreibers vom 06.11., zwanzig Minuten:

    webcast-api @caro94erlafamilia: status=live ohne Stream-URL
    Starte ytdlp für @caro94erlafamilia …            (55-mal)
    ERROR: [tiktok:live] caro94erlafamilia: The channel is not currently live

Derselbe Weg (Proxy, Cookies, Rechner) lieferte im selben Zeitraum fuer
@tbwpueppi eine Adresse und eine Aufnahme. Es liegt also nicht an der
Server-IP, wie die Meldung „TikTok gibt die Adresse einer Datacenter-IP oft
nicht heraus" riet, sondern an diesem einen Raum: TikTok meldet ihn als live
und gibt die Adresse nur angemeldeten, berechtigten Konten heraus —
Abo-Live oder 18+. yt-dlp sieht ohne solche Cookies keinen laufenden Raum.

Die Folgen waren dreifach:
* Der Recorder startete alle zwanzig Sekunden einen yt-dlp, der sofort starb.
* Der Restream lief ueber den Durchreicher, der aus demselben Grund starb —
  die Sendebruecke zeigte dem Publikum dauerhaft das Pausenbild, ohne Ton.
* Der Rat im Log zeigte auf den Proxy, nicht auf die Cookies.

Hier steht nur die Entscheidung: wie oft das in Folge passiert ist, ab wann
der Bot Ruhe gibt, und was er dazu sagt. Ein gelungener Versuch setzt alles
zurueck — ein Abo-Live kann jederzeit wieder ein offenes werden.
"""

# Ab so vielen Fehlversuchen in Folge gilt der Raum als verschlossen.
SCHWELLE = 3
# Ruhezeiten danach: erst kurz, dann laenger — ein Raum kann aufgehen.
# v4.2-W157: von 5-30 min auf 2-10 min. Beim Betreiber am 06.11. stand
# @tavorbeerchen auf der Liste, der eine Stunde vorher normal aufgenommen
# wurde: eine lange Ruhe kostet dann bis zu einer halben Stunde Aufnahme.
RUHE_S = (120, 300, 600)

# v4.2-W157: die erste Fassung sagte „typisch fuer Abo-Lives und 18+" — eine
# Ursache, die der Bot gar nicht kennt. Am 06.11. traf es drei Raeume, und die
# Abo-Erkennung (nc/abo.py) hatte keinen davon als Abo gemeldet. Der Text
# nennt jetzt beide Moeglichkeiten; was nc/abo.py sagt, haengt der Aufrufer an.
ABHILFE = ("TikTok meldet den Raum als live, gibt die Stream-Adresse aber nicht heraus "
           "(Webcast ohne stream_data, Live-Seite ohne Daten, yt-dlp: „not currently "
           "live\"). Zwei Ursachen sehen gleich aus: ein Abo-/18+-Live, das nur "
           "berechtigte Konten sehen, oder TikTok verweigert die Adresse dieser "
           "Sitzung/IP fuer diesen Raum. Laufen andere Raeume ueber denselben Weg, liegt "
           "es am Raum. Abhilfe in beiden Faellen: in COOKIE_FILE die Cookies eines "
           "angemeldeten TikTok-Kontos (mit sessionid) hinterlegen, das den Stream sehen darf.")

import logging

log = logging.getLogger(__name__)

_STAND = {}     # name -> {"folge": int, "ruhe_bis": float, "runde": int}


def _schluessel(name):
    return (name or "").lstrip("@").lower()


def vermerken(name, jetzt) -> dict:
    """Ein Versuch endete mit „nicht live", obwohl die API live meldet.

    -> {"verschlossen": bool, "neu": bool, "folge": int, "ruhe_s": int}
    `neu` ist wahr genau beim Uebergang in den verschlossenen Zustand — dann
    meldet der Aufrufer laut, danach nicht mehr bei jedem Versuch."""
    s = _STAND.setdefault(_schluessel(name), {"folge": 0, "ruhe_bis": 0.0, "runde": 0})
    s["folge"] += 1
    if s["folge"] < SCHWELLE:
        return {"verschlossen": False, "neu": False, "folge": s["folge"], "ruhe_s": 0}
    ruhe = RUHE_S[min(s["runde"], len(RUHE_S) - 1)]
    s["ruhe_bis"] = jetzt + ruhe
    neu = s["runde"] == 0
    s["runde"] += 1
    return {"verschlossen": True, "neu": neu, "folge": s["folge"], "ruhe_s": ruhe}


def ruhend(name, jetzt) -> bool:
    """Gilt fuer diesen Raum gerade eine Ruhezeit?"""
    s = _STAND.get(_schluessel(name))
    return bool(s) and s["ruhe_bis"] > jetzt


def verschlossen(name) -> bool:
    """Gilt der Raum (noch) als verschlossen — unabhaengig von der Ruhezeit."""
    s = _STAND.get(_schluessel(name))
    return bool(s) and s["folge"] >= SCHWELLE


def zuruecksetzen(name) -> bool:
    """Ein Versuch ist gelungen. -> True, wenn der Raum vorher verschlossen war.

    Meldet den Uebergang selbst: beide Aufrufer (Fehlerpfad mit anderer
    Kategorie, Erfolgspfad mit Datei) sagen sonst dasselbe zweimal, und der
    Erfolgspfad steht in einer Funktion unter Laengen-Sperre (W78)."""
    s = _STAND.pop(_schluessel(name), None)
    war = bool(s) and s["folge"] >= SCHWELLE
    if war:
        log.info("@%s: der Raum ist wieder offen — Aufnahme und Restream laufen "
                 "normal weiter.", _schluessel(name))
    return war


def lage() -> dict:
    """{name: folge} der verschlossenen Raeume — fuer /healthz und das Deck."""
    return {k: v["folge"] for k, v in _STAND.items() if v["folge"] >= SCHWELLE}
