#!/usr/bin/env python3
"""tools/kickpusher.py — v4.2-W136: welcher Pusher-Cluster nimmt den Kick-Key?

Am 31.10. lehnte Pusher den Kick-Chat mit "4001 App key ... not in this
cluster" ab, und das jede Sekunde. Key und Cluster stammen aus dem
oeffentlichen Web-Client von kick.com und koennen sich ohne Ankuendigung
aendern. Dieses Werkzeug probiert die bekannten Pusher-Cluster mit dem Key
aus der .env durch und sagt, welcher ihn annimmt — dann gehoert dieser Wert
als KICK_PUSHER_CLUSTER in die .env.

Es baut nur Verbindungen zum oeffentlichen Pusher-Endpunkt auf, abonniert
nichts und sendet nichts. Auf dem Server laufen lassen (dort ist das Netz,
durch das auch der Bot geht):

    venv/bin/python tools/kickpusher.py
    venv/bin/python tools/kickpusher.py --key <anderer-key>
"""
import argparse
import asyncio
import json
import os
import sys

CLUSTER = ("us2", "us3", "us1", "mt1", "eu", "ap1", "ap2", "ap3", "ap4", "sa1")


def _key_aus_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), ".env"))
    except ImportError:
        print("Hinweis: python-dotenv fehlt — es zaehlt nur die Umgebung.")
    return (os.getenv("KICK_PUSHER_KEY") or "32cbd69e4b950bf97679").strip()


async def _probe(aiohttp, key, cluster):
    url = ("wss://ws-%s.pusher.com/app/%s"
           "?protocol=7&client=js&version=8.4.0&flash=false" % (cluster, key))
    try:
        async with aiohttp.ClientSession(trust_env=True) as s:
            async with s.ws_connect(url, timeout=aiohttp.ClientWSTimeout(ws_close=8)) as ws:
                m = await asyncio.wait_for(ws.receive(), 8)
                text = str(m.data or "")
                try:
                    ev = json.loads(text).get("event", "")
                except ValueError:
                    ev = ""
                if ev == "pusher:connection_established":
                    return cluster, "ok", "angenommen"
                return cluster, "abgelehnt", text[:120] or m.type.name
    except Exception as e:
        # Kein Urteil ueber den Key: Pusher hat gar nicht geantwortet.
        return cluster, "netz", "%s: %s" % (type(e).__name__, str(e)[:100])


async def _alle(key):
    import aiohttp
    return await asyncio.gather(*(_probe(aiohttp, key, c) for c in CLUSTER))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--key", help="anderer Pusher-Key als in der .env")
    a = p.parse_args(argv)
    key = (a.key or _key_aus_env()).strip()
    print("Pusher-Key %s…%s — probiere %d Cluster" % (key[:4], key[-4:], len(CLUSTER)))
    treffer, abgelehnt = [], 0
    for cluster, lage, text in asyncio.run(_alle(key)):
        print("  %-4s %-9s %s" % (cluster, lage, text))
        if lage == "ok":
            treffer.append(cluster)
        elif lage == "abgelehnt":
            abgelehnt += 1
    if treffer:
        print("\nIn die .env:  KICK_PUSHER_CLUSTER=%s   (dann Dienst neu starten)" % treffer[0])
        return 0
    if not abgelehnt:
        # Kein einziger Cluster hat geantwortet — dann sagt dieser Lauf nichts
        # ueber den Key. Den Key zu verdaechtigen waere hier ein falscher Rat.
        print("\nPusher war von hier aus nicht erreichbar (DNS, Proxy oder "
              "Firewall). Ueber den Key sagt dieser Lauf nichts — auf der "
              "Maschine wiederholen, auf der der Bot laeuft.")
        return 2
    print("\nKein Cluster nimmt diesen Key an. Kick hat ihn vermutlich gewechselt: "
          "auf kick.com im Browser die Entwicklerwerkzeuge oeffnen (Netzwerk, "
          "Filter 'pusher'), den Key aus der wss-Adresse lesen und hier mit "
          "--key pruefen.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
