"""nc.overlaytext — die kleinen Bausteine der Sendebild-Texte (v4.2-W22).

Fuenf Helfer, die aus bot.py heraus sind: Text kappen und glaetten, einen
Fortschrittsbalken zeichnen, eine Datei atomar schreiben, den neuesten
Follower-Wert lesen, und entscheiden ob ein Event ins Overlay darf. Zusammen
14+6+2+9+... Aufrufstellen quer durch die Restream-Sendebild-Logik — und
KEINE davon war je einzeln aufrufbar, weil sie mitten in bot.py standen.

Der atomare Schreib-Weg (`ov_atomic_write`) ist der Grund, warum drawtext nie
eine halb geschriebene Datei sieht: `os.replace` ist auf demselben Dateisystem
atomar, ein direktes `open(path, "w")` waere es nicht — ffmpeg koennte mitten
im Schreiben lesen und fuer einen Frame Muell zeigen.

`overlay_src_ok` liest, ob Events von einer Quelle (kick|tiktok) ins Overlay
duerfen. Default ist 'kick': beim Restream sitzt das Publikum auf Kick, ein
TikTok-Gift kommt vom FREMDEN Publikum des Quell-Streamers und wuerde im
Sendebild wie ein eigener Zufluss aussehen.
"""

import os

from nc import schriftzeichen as _schriftzeichen

# v4.2-W22: aus .env, einmal beim Start gesetzt — siehe configure(). Als
# Modul-Konstante statt Parameter, weil overlay_src_ok() an vielen Stellen
# mit nur einem Argument aufgerufen wird; eine Signaturaenderung an allen
# Aufrufstellen haette das Risiko dieser Welle unnoetig vergroessert.
_OVERLAY_GIFT_SOURCE = "kick"
# v5.9-W203: die Schrift, mit der drawtext die Overlay-Dateien zeichnet — als
# Aufrufbares, weil sie zur Laufzeit gesucht wird (nc.restreamcmd.schriftart).
_SCHRIFT = None


def configure(gift_source=None, schrift=None):
    """Der Bot reicht die .env-Vorgabe einmal beim Start herein."""
    global _OVERLAY_GIFT_SOURCE, _SCHRIFT
    if gift_source is not None:
        _OVERLAY_GIFT_SOURCE = gift_source
    if schrift is not None:
        _SCHRIFT = schrift


def ov_oneline(s, maxlen):
    """Eine Zeile, kein Zeilenumbruch — drawtext mag reload nicht mit \\n."""
    return " ".join((s or "").split())[:maxlen]


def ov_bar(cur, tgt, width=12):
    """Unicode-Fortschrittsbalken als TEXT (reloadbar — kein starres drawbox)."""
    if not tgt or float(tgt) <= 0:
        return ""
    frac = max(0.0, min(1.0, float(cur) / float(tgt)))
    filled = int(round(width * frac))
    return "█" * filled + "░" * (width - filled)


def ov_atomic_write(path, text):
    """Schreibt `text` nach `path` — atomar, damit drawtext nie eine halb
    geschriebene Datei sieht (`os.replace` statt direktem `open(..., "w")`).

    Schluckt jeden Fehler: ein Overlay-Textfeld, das nicht schreibt, darf die
    Aufnahme oder den Restream nicht mitreissen — leer bleibt drawtext einfach
    unsichtbar.

    v5.9-W203: jede Datei hier liest drawtext, und drawtext zeichnet fuer jedes
    Zeichen, das die Schrift nicht hat, ein Kaestchen (die Emoji im Chat).
    Deshalb an DIESER Stelle gefiltert — alle Overlay-Felder laufen hier durch."""
    try:
        schrift = _schriftzeichen.schrift_von(_SCHRIFT) if _SCHRIFT else None
        if schrift:
            _schriftzeichen.vorbereiten(schrift)
        text = _schriftzeichen.zeichenbar(text, schrift)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        pass


def latest_popularity(conn, username):
    """Neuester follower_count für einen User aus profile_snapshots (oder 0)."""
    row = conn.execute(
        "SELECT follower_count FROM profile_snapshots WHERE username=? "
        "ORDER BY captured_at DESC LIMIT 1", (username,)).fetchone()
    return int(row["follower_count"]) if row and row["follower_count"] else 0


def overlay_src_ok(src):
    """True wenn Events von 'src' (kick|tiktok) ins Overlay dürfen. Default 'kick' —
       beim Restream sitzt das Publikum auf Kick, TikTok-Gifts sind das fremde Publikum."""
    return _OVERLAY_GIFT_SOURCE == "both" or _OVERLAY_GIFT_SOURCE == src
