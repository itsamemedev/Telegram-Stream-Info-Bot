"""nc.crypto — Krypto-Spendenadressen + optionaler Live-Empfang (v4.0-W94).

Adressen kommen ausschließlich aus der env (DONATION_<COIN>_ADDRESS) — hier wird
NICHTS erfunden; ist keine gesetzt, erscheint auch nichts. Für BTC kann der
insgesamt empfangene Betrag best-effort über einen öffentlichen Explorer
(blockstream.info, kostenlos, kein Key) geholt werden — SERVER-seitig, damit der
Browser keinen Fremd-Request macht (DSGVO). Gecacht, wirft nie nach außen.
"""
import json
import os
import time
import urllib.parse
import urllib.request

from nc import qrsvg as _qrsvg   # v4.0-W95: QR-Codes (Inline-SVG, vendored segno)

# (coin-code, Anzeige, env-Variable) — nur gesetzte erscheinen.
_COINS = [
    ("btc", "Bitcoin", "DONATION_BTC_ADDRESS"),
    ("bch", "Bitcoin Cash", "DONATION_BCH_ADDRESS"),
    ("eth", "Ethereum", "DONATION_ETH_ADDRESS"),
    ("ltc", "Litecoin", "DONATION_LTC_ADDRESS"),
    ("xmr", "Monero", "DONATION_XMR_ADDRESS"),
    ("sol", "Solana", "DONATION_SOL_ADDRESS"),
]

_CACHE = {"btc_sats": None, "ts": 0.0}
_TTL = 600.0                       # 10 min — Explorer schonen


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


def snapshot(fetch_live=False):
    """Für stats.json: {addresses:[…], btc_received_btc?: float}.
       fetch_live=True holt den BTC-Empfang best-effort (gecacht)."""
    addrs = addresses()
    out = {"addresses": addrs}
    btc = next((a for a in addrs if a["coin"] == "btc"), None)
    if btc and fetch_live:
        now = time.time()
        if _CACHE["btc_sats"] is None or (now - _CACHE["ts"]) > _TTL:
            try:
                _CACHE["btc_sats"] = _fetch_btc_sats(btc["address"])
                _CACHE["ts"] = now
            except Exception:
                pass                # Netzfehler → letzter Cache/aus, nie werfen
        if _CACHE["btc_sats"] is not None:
            out["btc_received_btc"] = round(_CACHE["btc_sats"] / 1e8, 8)
    return out
