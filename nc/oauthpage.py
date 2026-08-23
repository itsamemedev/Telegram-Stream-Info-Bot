"""nc.oauthpage — v4.0-W49: die OAuth-Rückmeldeseiten, aus bot.py gelöst.

Reine HTML-Bauer: Ergebnis (ok/Fehler) und Meldung rein, fertige Browser-Seite
raus. Kein Zustand, kein I/O ausser html.escape. Bitgenau gegen den Monolithen
geprüft — die Nutzer-Meldung wird escaped (kein HTML-Injection über den Flow).
"""

import html


def twitch(ok, msg):
    """Kleine Rueckmeldeseite nach dem Twitch-Flow — kein rohes JSON im Browser."""
    color = "#0f9d76" if ok else "#e11d48"
    icon = "\u2713" if ok else "\u2717"
    page = (
        "<!doctype html><meta charset=utf-8>"
        "<title>Twitch-Verbindung</title>"
        "<body style='background:#04060a;color:#c8f7e4;font-family:system-ui;"
        "display:flex;align-items:center;justify-content:center;height:100vh;margin:0'>"
        f"<div style='text-align:center;max-width:520px;padding:32px'>"
        f"<div style='font-size:56px;color:{color};margin-bottom:16px'>{icon}</div>"
        f"<div style='font-size:18px;line-height:1.5'>{html.escape(msg)}</div>"
        "<div style='margin-top:24px;font-size:13px;color:#5d8a78'>"
        "Dieses Fenster kann geschlossen werden.</div></div></body>")
    return page


def kick(ok, msg):
    """Kick-OAuth-Rückmeldeseite. Verbatim übernommen — MANUELLES Escaping
       (nur &<>, in dieser Reihenfolge, keine Quotes), bewusst so belassen."""
    esc = (str(msg).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    color = "#8FB98F" if ok else "#E0A0A0"
    icon = "✓" if ok else "✕"
    return ("<!DOCTYPE html><html lang=\"de\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>Kick OAuth</title><style>body{background:#0C0B09;color:#E8C86A;"
            "font-family:system-ui,sans-serif;display:flex;align-items:center;"
            "justify-content:center;min-height:100vh;margin:0}.box{text-align:center;"
            "padding:2rem;max-width:32rem}.i{font-size:3rem;color:" + color + "}"
            "h2{font-weight:600}p{color:#B9A96A}</style></head><body><div class=\"box\">"
            "<div class=\"i\">" + icon + "</div><h2>" + esc + "</h2>"
            "<p>Dieses Fenster kann geschlossen werden.</p></div></body></html>")
