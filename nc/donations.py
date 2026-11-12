"""nc.donations — Multi-Plattform-Donation-Normalisierung (rein, bot-frei).

Jede Plattform liefert Spenden in einer eigenen "Währung":
  Kick      → Subs/Gifts (kein Betrag im Event)
  Twitch    → Bits ("100 Bits"), Subs/Resubs/Gift-Subs
  YouTube   → Superchats ("5,00 €", "$5.00", "R$ 10,00"), Memberships
  TikTok    → Coins/Diamanten (nackte Zahl)

Ohne Normalisierung scheitert die Spendenziel-Summe still: float("100 Bits")
wirft, der Betrag zählt als 0. Dieses Modul übersetzt alles nach EUR — die
Kurse kommen per configure() aus der Bot-.env, das Modul selbst bleibt frei
von Bot-Abhängigkeiten und ist damit isoliert testbar.
"""

import re

# ---- konfigurierbare Kurse (Defaults = Bot-Defaults) ------------------------
_USD_EUR = 0.92
_BITS_EUR = 0.01           # 100 Bits ≈ 1 USD
_TWITCH_SUB_EUR = 2.50     # Tier-1-Streameranteil
_KICK_SUB_EUR = 2.50
_YT_MEMBER_EUR = 2.50
_TIKTOK_COIN_EUR = 0.01    # 1 Diamant ≈ 0,01 €

# Währungssymbole/-codes → Faktor auf EUR. Nur die realistisch auftretenden;
# alles Unbekannte wird als EUR behandelt (besser zu wenig raten als falsch).
_CUR = {
    "€": 1.0, "eur": 1.0,
    "$": None, "us$": None, "usd": None,       # None → _USD_EUR zur Laufzeit
    "£": 1.17, "gbp": 1.17,
    "r$": 0.16, "brl": 0.16,
    "ca$": 0.68, "cad": 0.68,
    "a$": 0.60, "aud": 0.60,
    "₹": 0.011, "inr": 0.011,
    "¥": 0.0059, "jpy": 0.0059,
}


def configure(usd_eur=None, bits_eur=None, twitch_sub_eur=None,
              kick_sub_eur=None, yt_member_eur=None, tiktok_coin_eur=None):
    """Kurse aus der Bot-.env injizieren (alles optional)."""
    global _USD_EUR, _BITS_EUR, _TWITCH_SUB_EUR, _KICK_SUB_EUR
    global _YT_MEMBER_EUR, _TIKTOK_COIN_EUR
    if usd_eur is not None: _USD_EUR = float(usd_eur)
    if bits_eur is not None: _BITS_EUR = float(bits_eur)
    if twitch_sub_eur is not None: _TWITCH_SUB_EUR = float(twitch_sub_eur)
    if kick_sub_eur is not None: _KICK_SUB_EUR = float(kick_sub_eur)
    if yt_member_eur is not None: _YT_MEMBER_EUR = float(yt_member_eur)
    if tiktok_coin_eur is not None: _TIKTOK_COIN_EUR = float(tiktok_coin_eur)


def parse_number(s: str):
    """Zahl aus einem Geld-String, tolerant gegenüber DE/US-Formaten.

    Regel: kommen '.' UND ',' vor, ist das LETZTE das Dezimaltrennzeichen
    ("1.234,56" → 1234.56 | "1,234.56" → 1234.56). Steht nur eines da, gilt es
    als Dezimaltrenner, wenn genau 1-2 Ziffern folgen ("5,00" → 5.0), sonst
    als Tausendertrenner ("1.234" → 1234).
    """
    m = re.search(r"\d[\d.,\s]*", s or "")
    if not m:
        return None
    raw = m.group(0).replace(" ", "").rstrip(".,")
    if not raw:
        return None
    has_dot, has_com = "." in raw, "," in raw
    if has_dot and has_com:
        dec = "." if raw.rfind(".") > raw.rfind(",") else ","
        thou = "," if dec == "." else "."
        raw = raw.replace(thou, "").replace(dec, ".")
    elif has_com:
        raw = raw.replace(",", "." if len(raw.split(",")[-1]) in (1, 2) else "")
    elif has_dot:
        if len(raw.split(".")[-1]) not in (1, 2):
            raw = raw.replace(".", "")
    try:
        return float(raw)
    except ValueError:
        return None


def _currency_factor(s: str):
    """Währungsfaktor aus dem String; None wenn keine Währung erkennbar."""
    low = (s or "").lower()
    # längere Codes zuerst, damit "r$" nicht als "$" durchgeht
    for sym in sorted(_CUR, key=len, reverse=True):
        if sym in low:
            f = _CUR[sym]
            return _USD_EUR if f is None else f
    return None


def to_eur(amount, platform="", message="") -> float:
    """Beliebigen Plattform-Betrag → EUR (0.0 wenn nicht bestimmbar).

    Reihenfolge: Bits → explizite Währung → Sub/Gift/Member-Pauschale →
    TikTok-Coins → nackte Zahl als EUR.
    """
    s = str(amount if amount is not None else "").strip()
    plat = (platform or "").strip().lower()
    msg = (message or "").strip().lower()
    blob = f"{s} {msg}".lower()

    # Beide Schreibweisen aus dem Docstring: "100 Bits" und "bits: 500".
    # Die zweite stand dort seit jeher und passte auf kein Muster.
    bits_re = r"(\d[\d.,]*)\s*bits?\b|\bbits?\s*:\s*(\d[\d.,]*)"

    # 1) Twitch-Bits im Betrag selbst ("100 Bits")
    m = re.search(bits_re, s.lower())
    if m:
        n = parse_number(m.group(1) or m.group(2))
        return round((n or 0) * _BITS_EUR, 2)

    # 2) Expliziter Geldbetrag mit Währung ("€5,00", "$5.00", "R$ 10")
    if s:
        f = _currency_factor(s)
        if f is not None:
            n = parse_number(s)
            if n is not None:
                return round(n * f, 2)

    # 1b) Bits nur in der Nachricht ("bits: 500"). Steht NACH der Waehrung:
    # bis v4.2-W149 lief die Suche ueber Betrag UND Nachricht zuerst, und ein
    # Superchat "$50.00" mit dem Text "fuer 100 bits Spass" zaehlte 1 € statt
    # 46 € — die Nachricht schreibt der Zuschauer, den Betrag die Plattform.
    m = re.search(bits_re, msg)
    if m:
        n = parse_number(m.group(1) or m.group(2))
        return round((n or 0) * _BITS_EUR, 2)

    # 3) Pauschalen für betragslose Events (Subs/Gifts/Memberships)
    has_digit = bool(re.search(r"\d", s))
    if not has_digit:
        if "member" in blob or "sponsor" in blob:
            return _YT_MEMBER_EUR
        if "sub" in blob or "gift" in blob:
            if plat == "twitch":
                return _TWITCH_SUB_EUR
            if plat == "kick":
                return _KICK_SUB_EUR
            if plat == "youtube":
                return _YT_MEMBER_EUR
            return _KICK_SUB_EUR
        return 0.0

    # 4) TikTok-Coins/Diamanten (nackte Zahl)
    n = parse_number(s)
    if n is None:
        return 0.0
    if plat == "tiktok":
        return round(n * _TIKTOK_COIN_EUR, 2)

    # 5) Nackte Zahl sonst = EUR (manuelle Einträge im Dashboard)
    return round(n, 2)


# v4.2-W178: die Kurse standen als OVERLAY_*-Variablen in der .env-Vorlage und
# in bot.py — gelesen wurden sie dort, an configure() gingen sie nie. Wer
# OVERLAY_USD_EUR setzte, aenderte damit nichts. Jetzt bei jeder Summe frisch
# aus der Umgebung (Funktion statt Modul-Konstante: .env und Deck-Einstellungen
# kommen erst nach den Importen).
def kurse_aus_env() -> None:
    from nc import envnum as _envnum
    f = _envnum.env_float
    # Woertlich je Name: tools/gen_env_example.py findet nur Literale.
    configure(usd_eur=max(0.0, f("OVERLAY_USD_EUR", 0.92)),
              bits_eur=max(0.0, f("OVERLAY_TWITCH_BITS_EUR", 0.01)),
              twitch_sub_eur=max(0.0, f("OVERLAY_TWITCH_SUB_EUR", 2.50)),
              kick_sub_eur=max(0.0, f("OVERLAY_KICK_SUB_EUR", 2.50)),
              yt_member_eur=max(0.0, f("OVERLAY_YT_MEMBER_EUR", 2.50)),
              tiktok_coin_eur=max(0.0, f("OVERLAY_TIKTOK_COIN_EUR", 0.01)))


def zeile_eur(r) -> float:
    """Eine overlay_events-Zeile (amount, platform, message) in EUR, nie negativ.

    v4.2-W178: Spendenziel, Overlay-Bilanz und Steuer-Gegenprobe lasen den
    Betrag mit parse_eur/float. Der kennt nur nackte Zahlen — „100 Bits",
    „$5.00" und „R$ 10,00" ergaben None, eine Twitch-Sub oder YouTube-
    Mitgliedschaft hat gar keinen Betrag (amount NULL). Alles zaehlte 0 €,
    waehrend to_eur() genau dafuer existierte und keinen Aufrufer hatte."""
    if hasattr(r, "keys"):
        ks = r.keys()
        amount = r["amount"]
        plat = r["platform"] if "platform" in ks else ""
        msg = r["message"] if "message" in ks else ""
    else:
        amount, plat, msg = (tuple(r) + (None, None, None))[:3]
    v = to_eur(amount, plat or "", msg or "")
    return v if v > 0 else 0.0


def summe_eur(zeilen) -> float:
    kurse_aus_env()
    return round(sum(zeile_eur(r) for r in zeilen), 2)


def fmt_eur(v) -> str:
    try:
        return f"{float(v):.2f} €".replace(".", ",")
    except (TypeError, ValueError):
        return "0,00 €"


def unknown_count(conn, days=30):
    """v4.0-W59 (conn-injiziert): Wie viele Spenden-Zeilen haben keine verwertbare
       Herkunft (Plattform leer/NULL) im Zeitfenster? Damit der Betreiber eine
       gesunkene Summe einordnen kann — die Zeilen sind nicht weg, zählen nur nicht
       mehr als eigene Einnahme. Enthält den SQLite-/andere-DB-Fallback und den
       robusten Row-Zugriff. Jeder Fehler → 0."""
    try:
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) n FROM overlay_events "
                        "WHERE kind='donation' AND (platform IS NULL OR platform='') "
                        "AND ts >= datetime('now', ?)", ("-%d days" % days,))
        except Exception:
            cur.execute("SELECT COUNT(*) n FROM overlay_events "
                        "WHERE kind='donation' AND (platform IS NULL OR platform='') "
                        "AND ts >= (NOW() - INTERVAL %d DAY)" % days)
        r = cur.fetchone()
        return int((r["n"] if hasattr(r, "keys") else r[0]) or 0)
    except Exception:
        return 0
