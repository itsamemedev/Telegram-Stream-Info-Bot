"""nc.loginpage — PIN-Login-Seite im Terminal-Look, aus bot_v37 gelöst.

Reiner HTML-Builder (einzige Abhängigkeit: html.escape). Phase-1-Zerlegung,
verbatim übernommen. Der Bot importiert login_page unter seinem alten Namen,
sodass die Login-Routen unverändert bleiben.
"""

import html


def login_page(error="", nxt="/"):
    """v4.0-W52: PIN-Login-Seite im Terminal-Look (self-contained, auch in der PWA)."""
    err = ("<div class='err'>" + html.escape(error) + "</div>") if error else ""
    nxt_esc = html.escape(nxt or "/")
    return (
        "<!doctype html><html lang=de><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>NIGHTCRAWLER · Login</title>"
        "<link rel=manifest href='/manifest.webmanifest'>"
        "<style>"
        ":root{--neon:#00ff9c;--cyan:#22d3ee;--bg:#04060a;--panel:#0a0f16;--dim:#5d8a78}"
        "*{box-sizing:border-box}"
        "body{background:var(--bg);color:var(--neon);font-family:'JetBrains Mono',ui-monospace,monospace;"
        "display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}"
        ".box{background:var(--panel);border:1px solid #10361f;border-radius:14px;padding:34px 30px;"
        "width:min(92vw,360px);text-align:center;box-shadow:0 0 40px #00ff9c22}"
        ".logo{font-family:Orbitron,sans-serif;font-weight:800;letter-spacing:2px;font-size:20px;"
        "color:var(--neon);margin-bottom:4px}"
        ".sub{color:var(--dim);font-size:12px;margin-bottom:22px}"
        "input{width:100%;background:#04070b;border:1px solid #10361f;color:var(--cyan);"
        "font-family:inherit;font-size:24px;text-align:center;letter-spacing:8px;padding:12px;"
        "border-radius:9px;outline:none}"
        "input:focus{border-color:var(--neon);box-shadow:0 0 0 2px #00ff9c33}"
        "button{width:100%;margin-top:16px;background:var(--neon);color:#04060a;border:0;"
        "font-family:inherit;font-weight:700;font-size:15px;padding:12px;border-radius:9px;cursor:pointer}"
        "button:active{transform:translateY(1px)}"
        ".err{color:#ff5d73;font-size:12px;margin-bottom:14px}"
        ".hint{color:var(--dim);font-size:10.5px;margin-top:18px;line-height:1.5}"
        "</style></head><body>"
        "<form class=box method=post action='/api/login'>"
        "<div class=logo>NIGHTCRAWLER</div><div class=sub>Azrael Sentinel · Kontrollpanel</div>"
        + err +
        "<input name=pin type=password inputmode=numeric autocomplete='current-password' "
        "autofocus placeholder='····' aria-label=PIN>"
        "<input type=hidden name=next value='" + nxt_esc + "'>"
        "<button type=submit>Entsperren</button>"
        "<div class=hint>Zugriff per SSH-Tunnel (localhost) bleibt ohne PIN frei.</div>"
        "</form></body></html>")
