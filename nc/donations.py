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

    # 1) Twitch-Bits ("100 Bits", "bits: 500")
    m = re.search(r"(\d[\d.,]*)\s*bits?\b", blob)
    if m:
        n = parse_number(m.group(1))
        return round((n or 0) * _BITS_EUR, 2)

    # 2) Expliziter Geldbetrag mit Währung ("€5,00", "$5.00", "R$ 10")
    if s:
        f = _currency_factor(s)
        if f is not None:
            n = parse_number(s)
            if n is not None:
                return round(n * f, 2)

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


def fmt_eur(v) -> str:
    try:
        return f"{float(v):.2f} €".replace(".", ",")
    except (TypeError, ValueError):
        return "0,00 €"


def source_allowed(conf: str, platform: str) -> bool:
    """Darf ein Event dieser Plattform ins Overlay?

    conf: "all" | "both" (= kick+tiktok, Altwert) | einzelne Plattform |
          Komma-Liste ("kick,twitch"). Leer/unbekannt → nur kick (Altverhalten).
    """
    c = (conf or "kick").strip().lower()
    p = (platform or "").strip().lower()
    if not p:
        return True                      # unmarkierte Alt-Events nicht blocken
    if c in ("all", "*"):
        return True
    if c == "both":
        return p in ("kick", "tiktok")
    allowed = {x.strip() for x in c.split(",") if x.strip()}
    return p in allowed


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
