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

Seit BH-1/BH-2 (Bughunt v5.11) steht hier auch, welches Sendebild-Feld
kanalweit ist und welches je Restream (`ziele`, `*_fuer`, `overlay_url`) —
die Begruendung je Feld steht am Abschnitt unten.

`overlay_src_ok` liest, ob Events von einer Quelle (kick|tiktok) ins Overlay
duerfen. Default ist 'kick': beim Restream sitzt das Publikum auf Kick, ein
TikTok-Gift kommt vom FREMDEN Publikum des Quell-Streamers und wuerde im
Sendebild wie ein eigener Zufluss aussehen.
"""

import os
import urllib.parse as _urlparse

from nc import schriftzeichen as _schriftzeichen
from nc import textutil as _textutil

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


# ---- BH-1/BH-2 (Bughunt v5.11): was gehoert in WELCHES Sendebild ----------
#
# Bis hierher fuellte der Overlay-Schreiber den Wurzelordner aus dem zuletzt
# GESTARTETEN Restream (_restream_active()) und kopierte Titel, Reaktion, Ziel,
# Follower, Alert, Caption und Brand von dort in jeden weiteren rid-Ordner;
# die HTML-Seite kannte gar keinen Restream. Mit zwei Restreams brannte A
# AZRAELs Reaktion auf B, Bs Follower-Zahl und Bs TikTok-Gifts ins Bild.
#
# Die Regel je Feld — kanalweit heisst: EINE Quelle fuer alle Sendebilder:
#
#   title    kanalweit  der Sendername (OVERLAY_TITLE / Deck): EIN Konfigwert,
#                       es gibt keinen je Restream. Quelle und Label des
#                       Restreams stehen in `source`.
#   goal     kanalweit  das EINE Spendenziel (nc/spendenziel.py, seit W173
#                       dasselbe fuer Website, Sendebild und /spenden).
#   caption  kanalweit  Legende der Chat-Quellen — Konfiguration, kein Stream.
#   brand    kanalweit  Adressen der EIGENEN Kanaele (Kick, Discord).
#   source   je rid     @Quellnutzer · Label.
#   react    je rid     react() stempelt source=<Quellnutzer>. Eine Reaktion
#                       ohne Quelle gilt allen; AZRAELs Zeile im EIGENEN
#                       Kick-Chat (last_spoken) bleibt kanalweiter Rueckfall.
#   follow   je rid     die ZAHL ist die des Quellnutzers (profile_snapshots);
#                       der Name des letzten Followers ist kanalweit
#                       (overlay_events traegt keine Herkunft).
#   alert    je rid     Events der eigenen Kanaele (kick/twitch/youtube) gelten
#                       allen; ein TikTok-Gift/-Follow kommt aus dem Raum EINES
#                       Quellnutzers und traegt seit BH-1 origin=.
#   chat     je rid     seit V37-P6.


def gehoert_zu(herkunft, nutzer) -> bool:
    """Gehoert etwas mit dieser Herkunft ins Sendebild von `nutzer`?

    nutzer=None heisst „keine Zuordnung verlangt" — die OBS-Seite ohne rid,
    der Weg wie bisher. Leere Herkunft heisst kanalweit: gilt fuer alle.
    Verglichen wird der bereinigte Handle ohne Gross/klein, wie beim
    Chat-Filter (nc.channels.chat_eintraege) — sonst faellt „@Anna" gegen
    „anna" durch und A sieht seine eigene Reaktion nicht."""
    if nutzer is None:
        return True
    h = _textutil.clean_username(str(herkunft or "")).lower()
    return (not h) or h == _textutil.clean_username(str(nutzer or "")).lower()


def reaktion_fuer(reaktion, gesprochen, nutzer, frisch_s, wand, mono):
    """AZRAELs Zeile fuer das Sendebild von `nutzer` (eine Zeile, max. 140), sonst "".

    V37-B99: Primaerquelle ist die Reaktion (nc.azraelstate.REACTION, setzt
    react() selbst, Wanduhr). KickModerator.last_spoken wird NUR gesetzt, wenn
    der Bot in den Kick-Chat schreibt — als einzige Quelle tauchten AZRAELs
    Live-Reaktionen im Sendebild nie auf. Es bleibt der Rueckfall (monotonic).

    BH-1: eine Reaktion auf einen ANDEREN Quellnutzer zaehlt hier nicht als
    vorhanden — dann greift der Rueckfall, wie ohne Reaktion."""
    r = reaktion or {}
    txt, alter = "", 1e9
    if r.get("text") and gehoert_zu(r.get("source"), nutzer):
        txt = ov_oneline(r.get("text") or "", 140)
        alter = wand - (r.get("ts") or 0.0)
    if not txt:
        ls = gesprochen or {}
        txt = ov_oneline(ls.get("text") or "", 140)
        alter = mono - (ls.get("ts") or 0.0)
    return txt if (txt and alter <= frisch_s) else ""


def alert_fuer(ereignis, nutzer, mono, halt_s=8.0):
    """Transienter Alert (letztes Event der letzten `halt_s` s) fuers Sendebild von `nutzer`."""
    ev = ereignis or {}
    zeile = ""
    if ev.get("name") and (mono - (ev.get("ts") or 0.0)) <= halt_s \
            and gehoert_zu(ev.get("origin"), nutzer):
        if ev.get("kind") == "follow":
            zeile = "▲▲ FOLLOWER  " + ov_oneline(ev["name"], 30)
        else:
            amt = ev.get("amount") or ""
            extra = ((": " + str(amt)) if amt
                     else ((" · " + str(ev.get("message"))) if ev.get("message") else ""))
            zeile = "◆ " + ov_oneline(ev["name"], 30) + extra
    return zeile


def follow_zeile(zahl, name):
    """Follower-Zeile: Zahl des Quellnutzers und/oder Name des letzten Followers."""
    zeile = ""
    if zahl and name:
        zeile = f"▲ {_textutil.fmt_number(zahl)}  · +{ov_oneline(name, 22)}"
    elif zahl:
        zeile = f"▲ {_textutil.fmt_number(zahl)} FOLLOWER"
    elif name:
        zeile = "▲ FOLLOWER  " + ov_oneline(name, 32)
    return zeile


def quelle_zeile(info, laeuft):
    """„└ @nutzer · Label" — nur solange der Restream wirklich sendet."""
    info = info or {}
    zeile = ""
    if laeuft and info.get("user"):
        zeile = "└ @" + str(info["user"])
        if info.get("label"):
            zeile += "  · " + str(info["label"])
    return zeile


def ziele(aktiv_alle, primaer, wurzel):
    """[(rid, info)] — jedes Sendebild, das in diesem Takt beschrieben wird.

    Jeder Registry-Eintrag mit seinem eingefrorenen Ordner (V37-P6). Gehoert
    der Wurzelordner keinem davon, kommt er mit rid=None und dem primaeren
    Restream dazu — der Weg der Aufrufer ohne rid, exakt wie bisher."""
    aus = [(rid, dict(info or {})) for rid, info in list((aktiv_alle or {}).items())]
    if not any(i.get("ovdir") == wurzel for _rid, i in aus):
        aus.insert(0, (None, dict(primaer or {})))
    return aus


def overlay_url(basis, rid):
    """BH-2: die Overlay-Seite fuer EINEN Restream — `rid=<rid>` an `basis`.

    Eine vorhandene Query bleibt Zeichen fuer Zeichen stehen (kein
    parse_qsl/urlencode, das kodierte sie um), ein altes rid= wird ersetzt,
    ein Fragment bleibt hinten. rid=None laesst die Adresse unveraendert."""
    if rid is None:
        return basis
    teile = _urlparse.urlsplit(basis)
    stuecke = [s for s in teile.query.split("&") if s and s.split("=", 1)[0] != "rid"]
    stuecke.append("rid=" + _urlparse.quote(str(rid), safe=""))
    return _urlparse.urlunsplit(teile._replace(query="&".join(stuecke)))
