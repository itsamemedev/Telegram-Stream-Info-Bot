#!/usr/bin/env python3
"""tools/kickchat.py — v4.2-W171: kommt der Kick-Chat ueber Centrifugo an?

Kick hat den Chat im Oktober 2026 von Pusher auf Centrifugo umgestellt
(nc/kickzentrifugo.py). Das Protokoll ist nicht dokumentiert, sondern aus
den Umbauten anderer Chat-Clients nachgelesen. Dieses Werkzeug geht genau
den Weg, den der Bot geht — Anmeldung, Websocket, Abo — und druckt, was
ankommt. Auf dem Server laufen lassen, dort ist das Netz des Bots:

    venv/bin/python tools/kickchat.py                 # Raum aus KICK_CHATROOM_ID
    venv/bin/python tools/kickchat.py --raum 123456   # anderer Raum
    venv/bin/python tools/kickchat.py --sekunden 120

Exitcode 0: Abo bestaetigt (Nachrichten kommen, sobald jemand schreibt).
Exitcode 1: Aufbau gescheitert, der Grund steht in der letzten Zeile.
"""
import argparse
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nc import kickzentrifugo as kz  # noqa: E402


def _raum_aus_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), ".env"))
    except ImportError:
        print("Hinweis: python-dotenv fehlt — es zaehlt nur die Umgebung.")
    return int(os.getenv("KICK_CHATROOM_ID", "0") or 0)


async def lauf(raum, sekunden):
    import aiohttp
    async with aiohttp.ClientSession() as s:
        cid = kz.neue_client_id()
        url, token = await kz.zugang(s, cid)
        print("Websocket:", url)
        print("Gast-Token: erhalten (%d Zeichen)" % len(token))
        async with s.ws_connect(url, headers=kz.KOPF) as ws:
            await ws.send_str(kz.connect_cmd(token))
            await ws.send_str(kz.subscribe_cmd(raum))
            abo, ende = False, time.monotonic() + sekunden
            while time.monotonic() < ende:
                msg = await ws.receive(timeout=kz.STILLE_S)
                if msg.type != aiohttp.WSMsgType.TEXT:
                    print("Verbindung beendet (Code %s)" % ws.close_code)
                    break
                for n in kz.zerlegen(msg.data):
                    if kz.ist_ping(n):
                        await ws.send_str("{}")
                        continue
                    if kz.antwort_fehler(n):
                        raise kz.KickZentrifugoFehler("abgelehnt: " + kz.antwort_fehler(n))
                    if n.get("id") == kz.ID_SUBSCRIBE:
                        abo = True
                        print("Abo bestaetigt: %s — warte auf Nachrichten …" % kz.kanal(raum))
                    elif "connect" in n:
                        print("Verbunden, Token-Laufzeit %d s" % kz.ttl_aus(n))
                    f = kz.als_frame(n)
                    if f:
                        try:
                            d = json.loads(f["data"])
                        except ValueError:
                            d = {}
                        wer = ((d.get("sender") or {}).get("username")) or "?"
                        print("%-40s %s: %s" % (f["event"], wer, (d.get("content") or "")[:120]))
            return abo


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raum", type=int, default=0, help="Kick-Chatroom-ID (Vorgabe: KICK_CHATROOM_ID)")
    ap.add_argument("--sekunden", type=int, default=60)
    a = ap.parse_args()
    raum = a.raum or _raum_aus_env()
    if not raum:
        print("Keine Chatroom-ID: --raum angeben oder KICK_CHATROOM_ID in der .env setzen.")
        return 1
    try:
        ok = asyncio.run(lauf(raum, a.sekunden))
    except Exception as e:
        print("FEHLER: %s: %s" % (type(e).__name__, e))
        return 1
    print("OK — der Kick-Chat kommt ueber Centrifugo an." if ok
          else "Kein Abo bestaetigt — der Weg steht nicht.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
