"""nc.profildetail — aus einem TikTok-Profil eine Auskunft machen (rein).

v4.2-W138. Der Betreiber am 05.11.: „das dashboard kann die tiktok Profile
nicht laden. Und selbst wenn ist es nicht detailliert genug, dies gilt auch
für discord und telegram."

Dashboard, Telegram-`/tiktok` und Discord zeigen dasselbe Profil. Bis hierher
rechnete jede Oberfläche für sich — oder gar nicht: Follower, Likes und Videos
standen als drei nackte Zahlen da, ohne Verhältnis und ohne Verlauf. Was eine
Zahl *bedeutet*, entscheidet jetzt dieses Modul einmal für alle drei.

Kein Netz, keine Datenbank: die Schnappschüsse reicht der Aufrufer herein.
"""

import logging
import re
from datetime import datetime, timezone

log = logging.getLogger("TikTokBot")

# Welche Felder des Scrapers an eine Oberfläche gehen. Ausdrücklich eine
# Liste: `sec_uid` und die rohe Nutzer-ID sind für das Popup Rauschen, und
# eine Oberfläche, die „alles" durchreicht, wächst mit jedem TikTok-Feld mit.
FELDER = (
    "nickname", "signature", "avatar", "verified", "private",
    "follower_count", "following_count", "heart_count", "video_count",
    "friend_count", "digg_count", "user_id", "create_time",
    "language", "region", "bio_link", "commerce", "category", "seller",
    "organization", "room_id", "nickname_modify_time",
    "unique_id_modify_time",
)


_GANZZAHL = re.compile(r"-?\d+")


def _zahl(v):
    """Ganzzahl oder None. Ohne try: TikTok liefert Zahl oder Ziffernkette,
    und alles andere (bool, leer, "1.2K") ist hier kein Zaehlerwert."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str) and _GANZZAHL.fullmatch(v.strip()):
        return int(v.strip())
    return None


def felder(roh):
    """Die Felder aus FELDER; Wahrheitswerte als bool, der Rest unverändert."""
    roh = roh or {}
    aus = {k: roh.get(k) for k in FELDER}
    for k in ("verified", "private", "commerce", "seller", "organization"):
        aus[k] = bool(aus.get(k))
    return aus


def kontotyp(p):
    """Ein Wort für die Art des Kontos — oder None, wenn nichts dafür spricht."""
    if p.get("organization"):
        return "Organisation"
    if p.get("seller"):
        return "Shop"
    if p.get("commerce"):
        return "Business" + (f" · {p['category']}" if p.get("category") else "")
    return None


def kennzahlen(p):
    """Verhältnisse, die drei nackte Zahlen nicht zeigen.

    Jede Kennzahl ist None, wenn ein Teil fehlt oder null ist — eine 0 wäre
    eine Aussage („keine Likes pro Video"), ein fehlender Wert ist keine.
    """
    fol, fng = _zahl(p.get("follower_count")), _zahl(p.get("following_count"))
    herz, vid = _zahl(p.get("heart_count")), _zahl(p.get("video_count"))
    return {
        "likes_pro_video": round(herz / vid) if herz is not None and vid else None,
        "likes_pro_follower": round(herz / fol, 1) if herz is not None and fol else None,
        "follower_pro_folgt": round(fol / fng, 1) if fol is not None and fng else None,
    }


def _ts(iso):
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError as e:
        # captured_at schreibt nc/routes/beobachtung selbst per isoformat().
        # Ein unlesbarer Wert ist also ein Befund an unseren Daten, keiner
        # an TikTok — und faellt sonst still aus dem Verlauf.
        log.warning("Profil-Verlauf: captured_at %r unlesbar (%s)", iso, e)
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t.timestamp()


def verlauf(schnappschuesse, p, jetzt=None):
    """Follower-Veränderung gegen den jüngsten Schnappschuss, der mindestens
    1 bzw. 7 Tage alt ist.

    Bewusst „mindestens so alt" und nicht „der nächstgelegene": ein
    Schnappschuss von vor zehn Minuten als Tageswert ausgegeben wäre eine
    falsche Zahl mit richtigem Etikett. Gibt es keinen alten genug, steht
    None da — und die Oberfläche sagt „noch kein Verlauf".
    """
    jetzt = jetzt if jetzt is not None else datetime.now(timezone.utc).timestamp()
    fol = _zahl(p.get("follower_count"))
    aus = {"tag": None, "woche": None, "messpunkte": 0}
    if fol is None:
        return aus
    punkte = []
    for s in schnappschuesse or ():
        t, f = _ts(s.get("captured_at")), _zahl(s.get("follower_count"))
        if t is not None and f is not None:
            punkte.append((t, f))
    aus["messpunkte"] = len(punkte)
    for name, alter in (("tag", 86400), ("woche", 7 * 86400)):
        alt_genug = [(t, f) for t, f in punkte if jetzt - t >= alter]
        if alt_genug:
            _, f = max(alt_genug)            # der juengste davon
            aus[name] = fol - f
    return aus


def datum(epoch):
    """Unix-Zeit als JJJJ-MM-TT, oder None."""
    z = _zahl(epoch)
    # Bereich statt try: TikTok-Zeiten sind Sekunden seit 1970; ausserhalb
    # davon (0, Millisekunden, Unsinn) gibt es kein Datum, das stimmt.
    if z is None or not 0 < z < 32503680000:
        return None
    return datetime.fromtimestamp(z, timezone.utc).strftime("%Y-%m-%d")
