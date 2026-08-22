"""nc.textutil — reine Text-/Format-Helfer (keine Bot-Abhängigkeiten).

Extrahiert aus bot_v37.py. Nur re+html. clean_username härtet gegen jede
TikTok-URL-Variante (B76-Serie); fmt_number/safe/short sind Anzeige-Helfer.
"""

import html
import re


def is_valid_tiktok_username(value: str) -> bool:
    """TikTok-Handle-Regeln: 2-24 Zeichen, nur a-z A-Z 0-9 _ . und kein Punkt
    am Ende. Ein '@' oder '/' kommt in einem Handle NIE vor."""
    v = (value or "").strip()
    return bool(re.fullmatch(r"[A-Za-z0-9_.]{2,24}", v)) and not v.endswith(".")


def clean_username(value: str) -> str:
    """URL -> Handle. Ein bereits sauberer Handle bleibt UNVERAENDERT.

    B125-FIX — hier lag ein echter Datenzerstoerer:
    Die Vorgaengerfassung schnitt bei JEDEM Vorkommen von "tiktok.com" alles
    davor weg. Damit wurde aus dem voellig legitimen Handle
    "www.tiktok.comrabi1978" der Phantom-User "rabi1978".

    Und dieser Name ist gueltig: 22 Zeichen, nur Buchstaben, Ziffern und
    Punkte — TikTok erlaubt Punkte im Handle. Er ist offensichtlich genau
    deshalb so gewaehlt, um automatische URL-Erkennung in die Irre zu
    fuehren. Genau das ist gelungen.

    Die neue Regel unterscheidet sauber, weil ein Handle bestimmte Zeichen
    per Definition nicht enthalten kann:

      1. Schema (http/https) ODER ein "/" vorhanden -> es IST eine URL.
         Handles enthalten nie einen Slash. Also Pfad zerlegen und das
         Segment hinter "/@" nehmen.
      2. Sonst ein "@" vorhanden -> das ist entweder das fuehrende
         Handle-Zeichen (@name) oder URL-Userinfo-Muell
         ("www.tiktok.com@name", vom Mobil-Keyboard verschluckter Slash,
         der B76c-Fall). Ein Handle enthaelt selbst nie ein "@", also ist
         alles bis zum LETZTEN "@" wegwerfbar.
      3. Sonst: LITERAL LASSEN. Kein "/" und kein "@" bedeutet, dass es
         gar keine URL sein KANN — auch dann nicht, wenn "tiktok.com"
         zufaellig im Namen steckt.

    Fall 1 aus dem Beispiel oben landet damit in Regel 3 und bleibt heil.
    """
    value = (value or "").strip()
    if not value:
        return ""

    low = value.lower()
    if low.startswith(("http://", "https://")) or "/" in value:
        # Regel 1 — echte URL. Schema abschneiden, dann Pfadsegmente.
        rest = value.split("://", 1)[1] if "://" in value else value
        rest = rest.split("?", 1)[0].split("#", 1)[0]
        parts = [p for p in rest.split("/") if p]
        handle = ""
        for p in parts[1:] if len(parts) > 1 else []:
            if p.startswith("@"):
                handle = p[1:]
                break
        if not handle:
            # kein /@segment — letztes Segment probieren (…/user oder
            # host@name ohne Slash nach dem Schema)
            tail = parts[-1] if parts else ""
            handle = tail.split("@")[-1] if "@" in tail else (
                tail if len(parts) > 1 else "")
        value = handle
    elif "@" in value:
        # Regel 2 — fuehrendes @ oder Userinfo-Muell.
        value = value.split("@")[-1]
    # Regel 3: alles andere bleibt, wie es ist.

    value = value.strip("/ ").split("?")[0]
    return re.sub(r"[^a-zA-Z0-9_.\-]", "", value)[:64]


def fmt_number(value) -> str:
    try:    return f"{int(value):,}".replace(",", ".")
    except Exception: return "Unbekannt"

def safe(value, fallback="Unbekannt") -> str:
    if value is None: return fallback
    v = str(value).strip()
    return html.escape(v) if v else fallback

def short(value: str, length=80) -> str:
    if not value: return "Unbekannt"
    return value if len(value) <= length else value[:length] + "..."
