"""nc.discordstate — v4.1-W16: Discords Zustand, persistiert und laufend.

Aus bot.py geloest, damit nc/routes/discord.py ihn direkt importieren kann.
`Ctx.__slots__` steht bei 24 von vertraglich 25 — die Reihenfolge aus W117
gilt weiter: erst die Schicht, dann die Routen. Ohne diesen Schritt haette
/api/discord acht Kontext-Eintraege gekostet.

Warum beides in EINEM Modul liegt, obwohl das eine aus der Datenbank kommt und
das andere aus dem Arbeitsspeicher: es beantwortet dieselbe Frage — "wie steht
es gerade um Discord?". Das Dashboard-Panel liest in einem Aufruf den
gespeicherten Wochenstand UND den laufenden Verbindungszustand. Sie zu trennen
haette zwei Module fuer eine Ansicht ergeben.

CLIENT und SESSION sind GETEILTER Zustand, keine Kopien. Der Supervisor im Bot
schreibt sie fort (Reconnects, Fehlergrund, Verbindungszeitpunkt), die Route
liest sie. Eine zweite Kopie, und das Panel meldete "nie verbunden", waehrend
der Bot seit Stunden im Server sitzt.
"""

import os

from nc.cfgstore import get as _cfg_get
from nc.dbwrap import db_conn

# Der laufende discord.py-Client. Register statt Modul-Global, weil der Bot ihn
# NEU BINDET (bei Reconnect und beim Aufraeumen) — ein direkter Alias zeigte
# danach auf den alten Client. Dieselbe Falle wie bei KICK_MOD in W9.
CLIENT = {"obj": None}

# Verbindungs-Buchfuehrung des Supervisors. Anders als CLIENT wird dieses Dict
# nur IN PLACE veraendert, nie neu gebunden — deshalb reicht hier das Dict.
SESSION = {"attempt": 0, "connected_since": None, "last_error": None,
           "last_disconnect": None, "reconnects": 0}


def state_get(k):
    """Ein Wert aus der Tabelle discord_state (Wochenstaende der Digests)."""
    try:
        with db_conn() as conn:
            r = conn.execute("SELECT v FROM discord_state WHERE k=?", (k,)).fetchone()
        return r["v"] if r else None
    except Exception:
        return None


def invite() -> str:
    """v4.0-W35: die EINE Wahrheit für den Community-Invite. Reihenfolge:
       gespeicherter (einmalig erzeugter) app_config-Wert → .env-Fallback. So
       nutzen Announcer, Marketing UND die Website denselben Link, sobald er
       einmal existiert.

       v4.1-W16: DISCORD_INVITE_URL wird hier bei jedem Aufruf gelesen statt
       als Modul-Konstante eingefroren. Das ist die Regel aus CLAUDE.md — und
       hier zusaetzlich richtig: der gespeicherte Wert schlaegt ihn ohnehin,
       sobald der Flow einmal lief, also aendert sich am Ergebnis nichts
       ausser dem Fall "Betreiber traegt die Variable nach".
    """
    try:
        stored = (_cfg_get("discord.invite_url", "") or "").strip()
    except Exception:
        stored = ""
    return stored or os.getenv("DISCORD_INVITE_URL", "").strip()
