"""nc.restreamcfg — v4.1-W22: die Sendeziele und die Prüf-Parameter.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die sechzehn Routen unter `/api/restream` lesen siebzehn .env-Werte des
Monolithen: die drei Sendeziele, die Parameter der Sendeprüfung, den
Stall-Zeitgeber und zwei öffentliche Links. Als nc.ctx-Einträge wären das
siebzehn der 25 vertraglichen Plätze — bei 24 belegten unmöglich.

**Gelesen wird bei JEDEM Aufruf, nie als Modul-Konstante.** Das ist hier nicht
nur die Regel aus CLAUDE.md, sondern hat einen konkreten Betriebsgrund: der
Betreiber ändert Stream-Keys im Dashboard und erwartet, dass der nächste
Restream sie benutzt — ohne Neustart. Eine eingefrorene Konstante hätte
stillschweigend den alten Key gesendet.

════════════════════════════════════════════════════════════════════════
STREAM-KEYS SIND GEHEIMNISSE
════════════════════════════════════════════════════════════════════════
`ziel(name)["key"]` ist ein echter Sendeschlüssel. Wer ihn in ein Log oder
eine API-Antwort schreibt, verschenkt den Kanal — jeder mit dem Key kann auf
ihm senden.

Deshalb:

* Für Anzeige und Diagnose gibt es `key_gesetzt(name)` — ein bool, kein Wert.
  Die Routen benutzen ausschliesslich das.
* Für Logzeilen gibt es `nc/logsafe.py` (F4), das die Kommandozeilen von
  streamlink und ffmpeg redigiert. Dieser Pfad darf bei Änderungen an der
  Kommandozeile nicht umgangen werden (CLAUDE.md).
* `ziel(...)` ist die EINZIGE Funktion hier, die einen Key herausgibt, und
  heisst deshalb bewusst nicht wie ein Getter. Sie ist für den Kommandobauer.

Die .env-Namen stehen überall WÖRTLICH in `os.getenv(...)`, nie dynamisch
zusammengesetzt. Sonst findet `tools/gen_env_example.py` sie nicht — beim
ersten Entwurf dieses Moduls fielen prompt vierzehn Variablen still aus der
Vorlage — und ein `grep KICK_STREAM_KEY` liefe ins Leere.
"""

import os

# Die drei eigenen Sendeziele. TikTok ist keins: von dort wird empfangen.
ZIELE = ("kick", "twitch", "youtube")

_WAHR = ("1", "true", "yes", "on", "y")



# Die Helfer nehmen den WERT, nicht den Namen: so steht jeder .env-Name
# woertlich in einem os.getenv(...) und ist fuer gen_env_example.py wie fuer
# ein grep sichtbar.

def _flag(wert) -> bool:
    return (wert or "").strip().lower() in _WAHR


def _zahl(wert, default):
    try:
        return int((wert or "").strip() or default)
    except (TypeError, ValueError):
        return default


# ---- Sendeziele -------------------------------------------------------------

# Die .env-Namen stehen hier WOERTLICH, nicht als "%s_INGEST_URL" % ziel.upper().
# Zwei Gruende, beide praktisch: tools/gen_env_example.py findet dynamisch
# gebaute Namen nicht — vierzehn Variablen waeren stillschweigend aus der
# Vorlage verschwunden. Und der Betreiber muss "wo kommt KICK_STREAM_KEY her?"
# mit einem grep beantworten koennen; das ist in diesem Bestand die halbe
# Arbeitsgrundlage (CLAUDE.md, Navigation).

def _kick():
    return {"aktiv": True,          # Hauptkanal: kein Schalter, nur der Key
            "ingest": os.getenv("KICK_INGEST_URL", "").strip(),
            "key": os.getenv("KICK_STREAM_KEY", "").strip()}


def _twitch():
    return {"aktiv": _flag(os.getenv("TWITCH_ENABLED", "1")),
            # Bewusst EINE lange Zeile: ein Umbruch zwischen os.getenv und dem
            # Namen macht die Variable fuer ein `grep os.getenv("TWITCH_...` 
            # unsichtbar. gen_env_example.py sieht sie seit W22 zwar auch
            # umbrochen — der Betreiber greppt aber ohne das Werkzeug.
            "ingest": os.getenv("TWITCH_INGEST_URL", "rtmp://ingest.global-contribute.live-video.net/app").strip(),
            "key": os.getenv("TWITCH_STREAM_KEY", "").strip()}


def _youtube():
    return {"aktiv": _flag(os.getenv("YOUTUBE_ENABLED", "1")),
            "ingest": os.getenv("YOUTUBE_INGEST_URL",
                                "rtmp://a.rtmp.youtube.com/live2").strip(),
            "key": os.getenv("YOUTUBE_STREAM_KEY", "").strip()}


_LESER = {"kick": _kick, "twitch": _twitch, "youtube": _youtube}


def ziel(name):
    """Ingest und Key eines Sendeziels. Die einzige Funktion hier, die einen
       Schlüssel herausgibt — siehe Modul-Kopf. Nur für den Kommandobauer."""
    leser = _LESER.get((name or "").strip().lower())
    return leser() if leser else {"ingest": "", "key": "", "aktiv": False}


def aktiv(name) -> bool:
    """Ist dieses Ziel eingeschaltet? Kick hat keinen Schalter — es ist der
       Hauptkanal und wird über einen fehlenden Key abgeschaltet."""
    return bool(ziel(name)["aktiv"])


def ingest(name) -> str:
    return ziel(name)["ingest"]


def key_gesetzt(name) -> bool:
    """Für Anzeige und Diagnose: IST ein Key da? Gibt ihn nicht heraus."""
    return bool(ziel(name)["key"])


def bereite_ziele():
    """Die Ziele, die eingeschaltet sind UND einen Key haben — ohne Keys."""
    return [z for z in ZIELE if aktiv(z) and key_gesetzt(z)]


# ---- Sendeprüfung und Zeitgeber ---------------------------------------------

def verify() -> bool:
    return _flag(os.getenv("RESTREAM_VERIFY", "1"))


def verify_takt() -> int:
    """Prüftakt in Sekunden."""
    return _zahl(os.getenv("RESTREAM_VERIFY_S", "120"), 120)


def verify_karenz() -> int:
    """Anlaufkarenz: so lange nach dem Start wird nicht geprüft. Ohne sie
       meldet die Prüfung jeden Start als Fehlschlag, weil die Plattform das
       Signal noch nicht sieht."""
    return _zahl(os.getenv("RESTREAM_VERIFY_GRACE_S", "90"), 90)


def verify_misses() -> int:
    """Hysterese: so viele Fehlschläge in Folge, bevor etwas gemeldet wird.
       Eine einzelne verpasste Prüfung ist bei RTMP normal."""
    return _zahl(os.getenv("RESTREAM_VERIFY_MISSES", "3"), 3)


def stall_timeout() -> int:
    """Ab wann ein Relay ohne Fortschritt als hängend gilt."""
    return _zahl(os.getenv("RESTREAM_STALL_TIMEOUT_S", "75"), 75)


def overlay() -> bool:
    return _flag(os.getenv("RESTREAM_OVERLAY", "0"))


# ---- Öffentliche Links (kein Geheimnis) -------------------------------------

def kick_channel_url() -> str:
    return (os.getenv("KICK_CHANNEL_URL", "") or "").strip().rstrip("/")


def discord_invite() -> str:
    return (os.getenv("DISCORD_INVITE_URL", "") or "").strip()


# ---- Ist Restream ueberhaupt an, und wohin? ---------------------------------

def enabled():
    """Master-Schalter für die Restream-Funktion. -> (an: bool, grund: str).

    "auto" heisst: aktiv, sobald IRGENDEIN Ziel konfiguriert ist. Seit W77
    gibt es keine Kick-Pflicht mehr — Kick, Twitch und YouTube sind
    gleichberechtigt. Der Grund kommt mit zurueck, weil "Restream ist aus"
    ohne Begruendung der haeufigste Support-Fall war.
    """
    from nc import restream_targets as _rst

    v = (os.getenv("RESTREAM_ENABLED", "auto") or "auto").strip().lower()
    if v in ("0", "false", "no", "off", "disabled"):
        return False, "per RESTREAM_ENABLED=0 deaktiviert"
    if v in ("1", "true", "yes", "on", "enabled"):
        return True, ""
    if _rst.active_targets():
        return True, ""
    return False, ("kein Restream-Ziel konfiguriert — mindestens EIN "
                   "*_INGEST_URL + *_STREAM_KEY (kick/twitch/youtube) setzen")


def active_platforms():
    """Welche Plattformen bekommen ueberhaupt Bild? Kick ist der Primaer,
       Twitch/YouTube nur wenn als Multistream-Ziel konfiguriert. Nicht
       konfigurierte Ziele duerfen nie einen Neustart ausloesen."""
    from nc import restream_targets as _rst

    namen = {"kick"}
    for n, _url in _rst.multistream_targets():
        namen.add(n)
    return namen


def chat_src_ok(src) -> bool:
    """Darf diese Quelle in den Sendebild-Chat? (RESTREAM_CHAT_SOURCE)

    V37-W-CHAT: twitch/youtube sind eigene Kanaele wie kick — sie zaehlen zur
    Kick-Klasse und sind bei "both" wie bei "kick" sichtbar. TikTok ist das
    fremde Publikum und hat eine eigene Einstellung.
    """
    v = (os.getenv("RESTREAM_CHAT_SOURCE", "both") or "both").strip().lower()
    if v in ("off", "none", "0"):
        return False
    if src in ("twitch", "youtube"):
        return v in ("both", "kick", src)
    return v == "both" or v == src


def yt_oauth_configured() -> bool:
    """Ist YouTube verbunden — per Flow oder per drei .env-Werten?"""
    from nc import ytoauth as _yt

    try:
        if _yt.status().get("ready"):
            return True
    except Exception:
        pass
    return all((os.getenv(k, "") or "").strip() for k in (
        "YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"))
