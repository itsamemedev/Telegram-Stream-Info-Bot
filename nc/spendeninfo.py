"""nc.spendeninfo — v4.2-W172: /spenden auf Telegram und Discord.

Gemeldet am 11.11.: „Der Bot hat weder in Discord noch in Telegram die
Donation-Funktion." Die Website zeigt PayPal, die Krypto-Adressen und das
Spendenziel seit W92/W99 — im Chat, also dort, wo die Zuschauer sind, gab es
keinen Weg dahin.

Gelesen wird aus denselben Quellen wie Website und Deck, damit nirgends eine
zweite Liste entsteht, die auseinanderlaeuft:

* PayPal: DONATION_PAYPAL (Vorgabe wie im Website-Panel)
* Krypto: nc.crypto._COINS → DONATION_<COIN>_ADDRESS
* Zweck: DONATION_GOAL_PURPOSE, Ziel: DONATION_GOAL_EUR, Zeitraum: DONATION_PERIOD
* Link: DONATION_LINK (optional, z. B. die Spendenseite der Website)

Alles bei JEDEM Aufruf aus der Umgebung — eine Adresse, die im Deck geaendert
wird (nc/einstellungen.py), gilt sofort, ohne Neustart.

Ist gar nichts konfiguriert, sagt der Text das ausdruecklich und nennt die
Variablen. Ein leerer Block sieht aus wie ein Ausfall (W99/W101: „ein leerer
Block ist keine Auskunft").

Bot-frei. Benutzertext ist mit _t markiert und wird beim Gebrauch uebersetzt.
"""

import html
import os
from urllib.parse import quote

import logging

from nc import crypto as _crypto
from nc import dbwrap as _dbwrap
from nc import spendenziel as _spendenziel

_log = logging.getLogger("TikTokBot")

def _t(text):
    """Markiert Benutzertext fuer tools/i18n_extract.py."""
    return text


def paypal() -> str:
    # Vorgabe woertlich: tools/gen_env_example.py liest sie von hier in die Vorlage.
    return (os.getenv("DONATION_PAYPAL", "paypal@voice4you.org") or "").strip()


def paypal_url(pp=None) -> str:
    """Der Spenden-Link — derselbe, den das Website-Panel als QR-Code zeigt."""
    pp = paypal() if pp is None else pp
    url = ""       # leer heisst: kein PayPal eingetragen — kein Fehler
    if pp:
        url = ("https://www.paypal.com/donate/?business=" + quote(pp)
               + "&currency_code=EUR&item_name=" + quote("Azrael Sentinel - Betrieb"))
    return url


def krypto():
    """[(Bezeichnung, Adresse)] — nur die gesetzten, Reihenfolge wie die Website."""
    return _crypto.gesetzte()


def stand():
    """Alles, was der Text braucht, als ein Wert — fuer Vertrag und Aufrufer.

    v4.2-W173: Ziel, Stand und Zeitraum aus nc/spendenziel.py — dieselben
    Zahlen wie Website, Overlay und Sendebild. Liest die Datenbank, also vom
    Bot aus nur neben dem Event-Loop aufrufen (asyncio.to_thread)."""
    try:
        with _dbwrap.db_conn() as conn:
            z = _spendenziel.stand(conn)
    except Exception as e:
        # Ohne Datenbank bleiben Adressen und Ziel richtig; nur der Stand fehlt —
        # und das wird gesagt, statt „0 €" zu behaupten.
        _log.error("/spenden: Spendenstand nicht lesbar (%s: %s) — Antwort ohne Stand.",
                   type(e).__name__, e)
        z = {"ziel_eur": _spendenziel.ziel_eur(), "aktuell_eur": None, "prozent": None,
             "zeitraum": _spendenziel.zeitraum(),
             "zweck": (os.getenv("DONATION_GOAL_PURPOSE", "") or "").strip()}
    return {
        "paypal": paypal(),
        "krypto": krypto(),
        "zweck": z["zweck"],
        "ziel_eur": z["ziel_eur"],
        "aktuell_eur": z["aktuell_eur"],
        "prozent": z["prozent"],
        "zeitraum": z["zeitraum"],
        "link": (os.getenv("DONATION_LINK", "") or "").strip(),
    }


def text(fmt="html", uebersetzen=lambda s: s, s=None):
    """Die Antwort auf /spenden. fmt: "html" (Telegram) oder "md" (Discord)."""
    s = stand() if s is None else s
    u = uebersetzen
    if fmt == "html":
        fett, code = (lambda x: "<b>%s</b>" % html.escape(x)), \
                     (lambda x: "<code>%s</code>" % html.escape(x))
        esc = html.escape
    else:
        fett, code = (lambda x: "**%s**" % x), (lambda x: "`%s`" % x)
        esc = str
    z = ["💸 " + fett(u(_t("Projekt unterstützen")))]
    if s["zweck"]:
        z.append(esc(s["zweck"]))
    if s["ziel_eur"] > 0 and s.get("aktuell_eur") is not None:
        z.append(esc(u(_t("Stand: %s € von %s € (%s %%) · %s")) % (
            "%.0f" % s["aktuell_eur"], "%.0f" % s["ziel_eur"],
            "%.0f" % (s.get("prozent") or 0), s["zeitraum"])))
    elif s["ziel_eur"] > 0:
        z.append(esc(u(_t("Ziel: %s € %s")) % (("%.0f" % s["ziel_eur"]), s["zeitraum"])).strip())
    if s["paypal"]:
        z += ["", fett("PayPal") + ": " + code(s["paypal"]), esc(paypal_url(s["paypal"]))]
    if s["krypto"]:
        z += ["", fett(u(_t("Krypto")))]
        z += ["%s: %s" % (esc(label), code(adr)) for label, adr in s["krypto"]]
    if s["link"]:
        z += ["", esc(s["link"])]
    if not s["paypal"] and not s["krypto"] and not s["link"]:
        z += ["", esc(u(_t("Es ist noch keine Spendenadresse eingetragen. Betreiber: "
                           "DONATION_PAYPAL oder DONATION_<COIN>_ADDRESS in der .env "
                           "oder im Deck unter Einstellungen setzen.")))]
    else:
        z += ["", esc(u(_t("Danke — jede Spende geht in Server, Speicher und KI.")))]
    return "\n".join(z)
