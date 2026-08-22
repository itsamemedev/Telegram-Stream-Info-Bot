"""nc.cookies — Cookie-Format-Verarbeitung (keine Bot-Abhängigkeiten).

Extrahiert aus bot_v37.py: beliebige Cookie-Eingaben (Header-String, JSON-
Export, Netscape) → Netscape-Format, Dedupe, Alarm-Stufen-Bewertung."""

import json


def _cookies_input_to_netscape(raw: str):
    """B63: Konvertiert beliebigen Cookie-Input nach Netscape-Format (das was
       MozillaCookieJar / yt-dlp lesen). Akzeptiert zwei Formate:

         1) Netscape-Text  — wie ihn die Extension 'Get cookies.txt LOCALLY'
            exportiert (tab-getrennt, '# Netscape HTTP Cookie File'-Header).
         2) JSON-Array     — wie ihn 'Cookie-Editor' / 'EditThisCookie' liefert:
            [{"name","value","domain","path","secure","expirationDate"}, ...]

       Returns (netscape_text, anzahl_cookies). Wirft bei kaputtem JSON.

       Wichtig:
         - HttpOnly-Cookies: manche Tools schreiben '#HttpOnly_<domain>' an den
           Zeilenanfang. MozillaCookieJar würde die als Kommentar werfen → die
           kritischen Auth-Cookies (sessionid_ss) gingen verloren. Wir strippen
           den Marker, damit sie geparst werden.
         - Tabs-zu-Spaces: Copy-Paste macht aus Tabs oft Spaces. Wir reparieren
           solche Zeilen, damit MozillaCookieJar sie wieder versteht.
    """
    s = (raw or "").lstrip()
    if not s:
        return "# Netscape HTTP Cookie File\n", 0

    # ── Format 1: JSON (Cookie-Editor / EditThisCookie) ──────────────────────
    if s[:1] in ("[", "{"):
        data = json.loads(s)
        if isinstance(data, dict):
            # manche Tools wrappen: {"cookies":[...]} oder {"data":[...]}
            data = data.get("cookies") or data.get("data") or []
        if not isinstance(data, list):
            return "# Netscape HTTP Cookie File\n", 0
        out = ["# Netscape HTTP Cookie File",
               "# Aktualisiert via TikTokBot-Dashboard", ""]
        count = 0
        for c in data:
            if not isinstance(c, dict):
                continue
            name = c.get("name")
            if not name:
                continue
            value = c.get("value", "")
            domain = c.get("domain") or ".tiktok.com"
            include_sub = "TRUE" if str(domain).startswith(".") else "FALSE"
            path = c.get("path") or "/"
            secure = "TRUE" if c.get("secure") else "FALSE"
            exp = (c.get("expirationDate") or c.get("expires")
                   or c.get("expiry") or 0)
            try:
                exp = int(float(exp))
            except (TypeError, ValueError):
                exp = 0
            # Tabs/Newlines in name/value sind im Netscape-Format illegal
            name = str(name).replace("\t", "").replace("\n", "").replace("\r", "")
            value = str(value).replace("\t", "").replace("\n", "").replace("\r", "")
            out.append(f"{domain}\t{include_sub}\t{path}\t{secure}\t{exp}\t{name}\t{value}")
            count += 1
        return "\n".join(out) + "\n", count

    # ── Format 2: Netscape-Text ──────────────────────────────────────────────
    lines = raw.splitlines()
    has_header = any(l.lstrip().startswith("# Netscape") for l in lines[:3])
    out = []
    if not has_header:
        out.append("# Netscape HTTP Cookie File")
    count = 0
    for l in lines:
        ls = l.strip()
        # HttpOnly-Marker entfernen, damit der Cookie nicht als Kommentar verschwindet
        if ls.startswith("#HttpOnly_"):
            ls = ls[len("#HttpOnly_"):]
            l = ls
        if not ls:
            out.append(l)
            continue
        if ls.startswith("#"):
            out.append(l)
            continue
        # gültige Datenzeile: >= 7 tab-getrennte Felder
        if len(ls.split("\t")) >= 7:
            out.append(l)
            count += 1
        else:
            # evtl. mit Spaces statt Tabs (Copy-Paste-Schaden)? reparieren
            parts = ls.split()
            if len(parts) >= 7:
                # Felder 1-6 sind feldlos, ab 7 ist der Value (kann theoretisch
                # Spaces enthalten — bei TikTok aber nie, daher rejoin per Space)
                out.append("\t".join(parts[:6]) + "\t" + " ".join(parts[6:]))
                count += 1
            # sonst: Müll-Zeile überspringen
    return "\n".join(out) + "\n", count

def _dedupe_cookie_text(netscape_text: str):
    """Entfernt doppelte Cookie-NAMEN (z.B. msToken unter .tiktok.com UND
       www.tiktok.com) und behält pro Name nur die beste Variante — exakt nach
       derselben Regel wie _load_cookies_dict(): spezifischere Domain (ohne
       führenden Punkt) gewinnt, bei Gleichstand die längere Expiry. So
       verschwindet die 'mehrfach unter verschiedenen Domains'-Warnung und der
       Bot sendet garantiert den Wert, den auch die Health-Anzeige sieht.
       Werte werden NICHT verändert — nur die unterlegene Zeile entfällt.
       Returns (bereinigter_text, anzahl_entfernt)."""
    lines = netscape_text.splitlines()
    best = {}                  # name -> (spec, expiry, idx)
    is_data = set()
    for i, l in enumerate(lines):
        ls = l.strip()
        if not ls or ls.startswith("#"):
            continue
        parts = ls.split("\t")
        if len(parts) < 7:
            continue
        is_data.add(i)
        domain, name = parts[0], parts[5]
        try: expiry = int(parts[4])
        except (ValueError, IndexError): expiry = 0
        spec = 0 if domain.startswith(".") else 1
        prev = best.get(name)
        if prev is None or (spec, expiry) > (prev[0], prev[1]):
            best[name] = (spec, expiry, i)
    keep = {v[2] for v in best.values()}
    out, removed = [], 0
    for i, l in enumerate(lines):
        if i in is_data and i not in keep:
            removed += 1
            continue
        out.append(l)
    return "\n".join(out) + "\n", removed

def _cookie_alarm_level(h):
    """get_cookie_health() → (level, telegram_html). level: ok|warn|crit.
       Nutzt das bereits berechnete status/headline aus get_cookie_health()."""
    status = h.get("status")
    head = h.get("headline") or "Cookie-Problem"
    if status in ("missing", "parse_error", "critical"):
        return "crit", ("🚨 <b>COOKIE-ALARM</b>\n\n" + head +
                        "\n\nOhne gültige Auth-Cookies scheitern Aufnahmen (TikTok 403). "
                        "Bitte <code>cookies.txt</code> neu exportieren.")
    if status == "warning":
        od = h.get("oldest_expiry_days")
        extra = (f"\nKritischer Cookie noch ~{od}d gültig." if (od is not None and od >= 0) else "")
        return "warn", ("⚠️ <b>COOKIE-WARNUNG</b>\n\n" + head + extra +
                        "\n\nVor Ablauf neu exportieren — sonst brechen Aufnahmen still ab.")
    return "ok", ""
