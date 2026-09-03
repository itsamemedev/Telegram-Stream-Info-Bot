"""nc.modstats — v4.1-W18: was als Moderations-Aktion an den Betreiber geht.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Der ToxicityAgent meldet dem Betreiber „Chat-Toxizität steigt: N
Moderations-Aktionen letzte Stunde". Seine Zahl kam aus einem blanken
``SELECT ... FROM kick_mod_log`` — **jede** Zeile zählte.

In dieser Tabelle liegt aber deutlich mehr als Moderation:

    _modlog("reaction",  "azrael", …)   AZRAELs Live-Reaktion auf einen
                                        TikTok-Stream — im Sekundentakt
    _modlog("highlight", "radar",  …)   Chat-Ausschlag, auch aus TikTok
    _modlog("send"/"reply", "bot", …)   was der Bot selbst gesagt hat
    _modlog("learn",     "ai",     …)   neu gelernte Schimpfwort-Kandidaten

Ein einziger aktiver TikTok-Live-React-Worker schreibt so pro Stunde
mühelos die sechs Zeilen, ab denen `spike_min` greift — und der Betreiber
bekam eine Toxizitäts-Warnung für einen Chat, den er **gar nicht
moderiert**. TikTok-Gifts gehen an den getrackten Streamer, nicht an
eigene Kanäle; für TikTok-Kommentare gilt dasselbe: es gibt dort keine
Moderationsbefugnis, also auch nichts zu melden. Dieselbe Trennlinie wie
bei REVENUE_PLATFORMS in bot.py.

Deshalb hier zwei Fragen, getrennt beantwortbar und ohne DB testbar:

  1. Ist diese Zeile überhaupt eine **Moderations-Aktion**?  (`ist_moderation`)
  2. Auf **welcher Plattform** fand sie statt?                (`plattform`)

Gezählt wird nur, was beides beantwortet UND in der Auswahl des Betreibers
liegt. `PLATTFORMEN` ist die harte Obergrenze dieser Auswahl — TikTok steht
absichtlich NICHT darin, es lässt sich also auch per Konfiguration nicht
hineinschreiben.

Wichtig für den Trend: die Vorstunde muss durch **dieselbe** Regel laufen.
Wird nur die aktuelle Stunde gefiltert und die Vorstunde roh gezählt,
vergleicht der Agent zwei verschiedene Grössen und meldet Wellen, die es
nie gab.
"""

# Die Plattformen, auf denen der Bot eigene Moderationsbefugnis hat. TikTok
# fehlt hier bewusst und dauerhaft (siehe Modul-Kopf).
PLATTFORMEN = ("kick", "twitch", "youtube", "discord")

# Was ohne ausdrückliche Konfiguration an den Betreiber gemeldet wird: die drei
# Stream-Chats. Discord ist eine eigene Welt (Community statt Livestream) und
# wird nur gemeldet, wenn der Betreiber es einträgt.
STANDARD_QUELLEN = ("kick", "twitch", "youtube")

# Nur diese Arten sind ein Durchgreifen gegen einen Nutzer. "send", "reply",
# "reaction", "highlight" und "learn" sind Bot-Aktivität, keine Moderation.
MOD_ARTEN = ("timeout", "warn", "ban", "delete", "flag")

# Aktor → Plattform für Zeilen ohne ausdrückliche Markierung. Deckt den
# Bestand ab, der vor W18 geschrieben wurde; neue Zeilen tragen
# meta["platform"] und brauchen diese Tabelle nicht.
_AKTOR_PLATTFORM = {
    "auto-mod-kick": "kick",
    "filter": "kick",
    "spam": "kick",
    "ai": "kick",
    "auto-mod-twitch": "twitch",
    "auto-mod-youtube": "youtube",
    "ai-discord": "discord",
}


def ist_moderation(kind) -> bool:
    """Ist diese kick_mod_log-Art ein Durchgreifen gegen einen Nutzer?"""
    return str(kind or "").strip().lower() in MOD_ARTEN


def plattform(actor, meta=None):
    """Plattform einer Log-Zeile, oder None wenn nicht zuzuordnen.

    Die ausdrückliche Markierung schlägt die Aktor-Tabelle. Das ist nicht
    Kosmetik: "sentinel-shield" schreibt sowohl aus dem Kick-Moderator als
    auch aus dem Discord-Automod: über den Aktor allein ist die Zeile nicht
    unterscheidbar. Ohne Markierung bleibt sie unzuordenbar und zählt nicht
    mit — lieber eine Zeile zu wenig als eine falsch zugeordnete Warnung.
    """
    if isinstance(meta, dict):
        p = str(meta.get("platform") or "").strip().lower()
        if p in PLATTFORMEN:
            return p
    return _AKTOR_PLATTFORM.get(str(actor or "").strip().lower())


def quellen(roh=None):
    """Konfigurierte Quellen als Tupel. Unbekannte Namen — TikTok
       eingeschlossen — fallen still raus; leer heisst STANDARD_QUELLEN."""
    if roh is None:
        return STANDARD_QUELLEN
    if isinstance(roh, str):
        teile = roh.replace(";", ",").replace(" ", ",").split(",")
    else:
        teile = list(roh)
    aus = tuple(dict.fromkeys(
        p for p in (str(t or "").strip().lower() for t in teile) if p in PLATTFORMEN))
    return aus or STANDARD_QUELLEN


def zaehlt(kind, actor, meta=None, erlaubt=None) -> bool:
    """Zählt diese Zeile als gemeldete Moderations-Aktion?"""
    if not ist_moderation(kind):
        return False
    p = plattform(actor, meta)
    return p is not None and p in (erlaubt if erlaubt is not None else STANDARD_QUELLEN)


def verdichte(zeilen, vorzeilen=(), erlaubt=None):
    """Der Schnappschuss für den ToxicityAgent.

    `zeilen`/`vorzeilen` sind Folgen von (kind, actor, meta-dict). Beide
    laufen durch dieselbe Regel — sonst vergleicht der Agent eine gefilterte
    Stunde mit einer ungefilterten und meldet eine Welle, die es nie gab.

    avg_toxic_1h bleibt None, wenn keine gezählte Zeile einen toxic-Wert
    trägt: 0.0 wäre eine Aussage ("nicht toxisch"), die niemand gemessen hat.
    """
    erlaubt = tuple(erlaubt) if erlaubt is not None else STANDARD_QUELLEN
    tox = []
    n = 0
    je_plattform = {}
    for kind, actor, meta in zeilen:
        if not zaehlt(kind, actor, meta, erlaubt):
            continue
        n += 1
        p = plattform(actor, meta)
        je_plattform[p] = je_plattform.get(p, 0) + 1
        if isinstance(meta, dict) and "toxic" in meta:
            try:
                tox.append(float(meta["toxic"]))
            except (TypeError, ValueError):
                pass
    vor = sum(1 for k, a, m in vorzeilen if zaehlt(k, a, m, erlaubt))
    return {"actions_1h": n, "actions_prev_1h": vor,
            "avg_toxic_1h": round(sum(tox) / len(tox), 3) if tox else None,
            "platforms": je_plattform, "quellen": list(erlaubt)}
