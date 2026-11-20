"""nc.crypto — Krypto-Spendenadressen + optionaler Live-Empfang (v4.0-W94).

Adressen kommen ausschließlich aus der env (DONATION_<COIN>_ADDRESS) — hier wird
NICHTS erfunden; ist keine gesetzt, erscheint auch nichts. Für BTC kann der
insgesamt empfangene Betrag best-effort über einen öffentlichen Explorer
(blockstream.info, kostenlos, kein Key) geholt werden — SERVER-seitig, damit der
Browser keinen Fremd-Request macht (DSGVO). Gecacht, wirft nie nach außen.
"""
import json
import logging
import os
import threading
import time
import urllib.parse
import urllib.request

from nc import meldetakt as _meldetakt
from nc import qrsvg as _qrsvg   # v4.0-W95: QR-Codes (Inline-SVG, vendored segno)

_log = logging.getLogger(__name__)

# (coin-code, Anzeige, env-Variable) — nur gesetzte erscheinen.
_COINS = [
    ("btc", "Bitcoin", "DONATION_BTC_ADDRESS"),
    ("bch", "Bitcoin Cash", "DONATION_BCH_ADDRESS"),
    ("eth", "Ethereum", "DONATION_ETH_ADDRESS"),
    ("ltc", "Litecoin", "DONATION_LTC_ADDRESS"),
    ("xmr", "Monero", "DONATION_XMR_ADDRESS"),
    ("sol", "Solana", "DONATION_SOL_ADDRESS"),
]

_CACHE = {"btc_sats": None, "ts": 0.0, "fehl_ts": 0.0}
_TTL = 600.0                       # 10 min — Explorer schonen
# v5.11.3-WEB-2: auch ein FEHLSCHLAG wird gemerkt. snapshot() laeuft ueber
# /api/public/stats ohne Anmeldung im waitress-Thread; ohne diese Frist rief
# bei gestoertem blockstream.info JEDE Anfrage urlopen(timeout=8) — acht
# gleichzeitige Aufrufe genuegten, um den ganzen Thread-Pool des Decks zu
# belegen. Kuerzer als _TTL: ein kurzer Ausfall soll die Zahl nicht zehn
# Minuten lang verstecken.
_FEHL_TTL = 300.0
# Nur EIN Thread fragt gleichzeitig. Die Fehlerfrist greift erst, wenn der
# erste Versuch nach bis zu 8 s gescheitert ist — bis dahin waeren alle
# parallelen Anfragen ebenfalls ins Netz gegangen.
_ABRUF = threading.Lock()
_KANAL = "crypto-btc-explorer"


def gesetzte():
    """v4.2-W172: [(Bezeichnung, Adresse)] — nur die gesetzten, ohne QR-Code.
    Fuer /spenden: ein Chat-Text braucht keine SVG, und die Lesestelle bleibt
    hier, wo tools/gen_env_example.py die Liste _COINS aufloesen kann."""
    aus = []
    for _coin, label, env in _COINS:
        a = (os.getenv(env, "") or "").strip()
        if a:
            aus.append((label, a))
    return aus


def addresses():
    """Konfigurierte Adressen (nur die gesetzten), Reihenfolge wie _COINS,
       je mit QR-Code als Inline-SVG (BIP21 'bitcoin:' für BTC, sonst roh)."""
    out = []
    for coin, label, env in _COINS:
        a = (os.getenv(env, "") or "").strip()
        if a:
            payload = ("bitcoin:" + a) if coin == "btc" else a
            out.append({"coin": coin, "label": label, "address": a,
                        "qr": _qrsvg.qr_svg(payload)})
    return out


def _fetch_btc_sats(address, timeout=8):
    """Insgesamt je empfangene Satoshis für eine BTC-Adresse (blockstream
       Esplora: chain_stats.funded_txo_sum + mempool)."""
    url = "https://blockstream.info/api/address/" + urllib.parse.quote(address, safe="")
    req = urllib.request.Request(url, headers={"user-agent": "nightcrawler-crypto"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8", "ignore"))
    cs = d.get("chain_stats") or {}
    ms = d.get("mempool_stats") or {}
    return int(cs.get("funded_txo_sum") or 0) + int(ms.get("funded_txo_sum") or 0)


def erwartete_namen():
    """Die env-Namen, unter denen Adressen gesucht werden.

    v4.2-W99: gibt es, damit der Bot sie NENNEN kann. Steht keine Adresse in
    der .env, ist der Spendenblock auf der oeffentlichen Seite leer — und bis
    W99 sagte nichts, ob nichts konfiguriert ist oder etwas kaputt. Genau das
    hat einen Nachmittag gekostet: die Vorlage `.env.example` kannte diese
    sechs Namen naemlich selbst nicht (tools/gen_env_example.py sah nur
    woertliche `os.getenv("NAME")`, hier steht der Name in einer
    Schleifenvariablen). Wer seine .env aus der Vorlage neu aufbaute, verlor
    damit saemtliche Wallet-Adressen, ohne es erfahren zu koennen.
    """
    return tuple(env for _coin, _label, env in _COINS)


def fehlende_namen():
    """Die env-Namen, unter denen KEINE Adresse steht.

    v4.2-W101: `erwartete_namen()` sagt, wonach gesucht wird — nicht, was
    fehlt. Der Betreiber wollte wissen, welche der sechs Wallets leer ist,
    ohne die Liste von Hand gegen die `.env` zu halten; das ist genau die
    Frage, die eine Teilkonfiguration stellt.
    """
    return tuple(env for _coin, _label, env in _COINS
                 if not (os.getenv(env, "") or "").strip())


def snapshot(fetch_live=False):
    """Für stats.json: {addresses:[…], grund, gesucht, fehlend,
       btc_received_btc?}. fetch_live=True holt den BTC-Empfang best-effort.

       `grund` sagt bei leerer Liste WARUM — "keine_adresse_konfiguriert" ist
       eine Aussage, eine leere Liste ohne Grund ist keine.

       v4.2-W101: `gesucht` trägt jetzt IMMER alle sechs Namen und `fehlend`
       die nicht gesetzten. Bis dahin war `gesucht` bei einem Treffer leer
       ("bei Treffern braucht niemand die Namen") — und damit sah eine
       Konfiguration mit einer von sechs Adressen genauso aus wie eine
       vollständige. Eine Teilkonfiguration ist der Normalfall, nicht die
       Ausnahme: wer nur Bitcoin annimmt, hat fünf leere Namen, und die
       sollen nachlesbar sein statt erraten."""
    addrs = addresses()
    fehlend = list(fehlende_namen())
    out = {"addresses": addrs,
           "grund": "" if addrs else "keine_adresse_konfiguriert",
           "gesucht": list(erwartete_namen()),
           "fehlend": fehlend}
    btc = next((a for a in addrs if a["coin"] == "btc"), None)
    if btc and fetch_live:
        _btc_auffrischen(btc["address"])
        if _CACHE["btc_sats"] is not None:
            out["btc_received_btc"] = round(_CACHE["btc_sats"] / 1e8, 8)
    return out


def _btc_auffrischen(address):
    """Den BTC-Empfang neu holen, wenn er faellig ist — hoechstens ein Netzaufruf
    je Frist, auch im Fehlerfall (WEB-2). Wirft nie: die oeffentliche Seite
    zeigt dann den letzten Stand oder keinen.

    Der Fehler bleibt nicht still (bis v5.11.3 `except Exception: pass`): er
    geht gedrosselt durch nc/meldetakt, Kanal statt Adresse als Schluessel."""
    now = time.time()
    if _CACHE["btc_sats"] is not None and (now - _CACHE["ts"]) <= _TTL:
        return
    if (now - _CACHE["fehl_ts"]) < _FEHL_TTL:
        return
    if not _ABRUF.acquire(blocking=False):
        return                      # ein anderer Thread fragt gerade
    try:
        try:
            sats = _fetch_btc_sats(address)
        except Exception as e:
            # Uhr beim Schreiben, nicht beim Beginn: ein Timeout von 8 s
            # verkuerzte die Frist sonst um genau diese 8 s.
            _CACHE["fehl_ts"] = time.time()
            laut, weg = _meldetakt.melden(_KANAL, type(e).__name__, time.monotonic())
            if laut:
                _log.warning("BTC-Empfang: Explorer blockstream.info nicht erreichbar "
                             "(%s: %s) — naechster Versuch in %d min, bis dahin %s%s. "
                             "Abhilfe: ausgehendes HTTPS zu blockstream.info pruefen "
                             "(Firewall/Proxy).", type(e).__name__, e, int(_FEHL_TTL // 60),
                             "der letzte Stand" if _CACHE["btc_sats"] is not None
                             else "keine Anzeige", _meldetakt.zusatz(weg))
            return
        _CACHE["btc_sats"] = sats
        _CACHE["ts"] = time.time()
        _CACHE["fehl_ts"] = 0.0
        _meldetakt.zuruecksetzen(_KANAL)
    finally:
        _ABRUF.release()
