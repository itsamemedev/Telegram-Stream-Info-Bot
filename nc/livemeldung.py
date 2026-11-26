"""nc.livemeldung — v4.2-W176: globale Live-/Offline-Aktionen einmal je Nutzer.

Derselbe TikTok-Nutzer darf aus mehreren Telegram-Chats verfolgt werden; jeder
Chat ist ein eigenes Tracking mit eigenem `claim_live_transition`. Das ist fuer
die Telegram-Meldung richtig — jeder Chat will seine eigene. Fuer alles, was
NICHT an einem Chat haengt, war es ein Fehler, und zwar ein lauter:

    zwei Discord-LIVE-Embeds fuer denselben Stream,
    ein zweiter Discord-Live-Thread (der erste wurde nie archiviert),
    _oracle_memorize und _director_finalize doppelt,
    und `_LIVE_SESSION_START.pop` liess dem zweiten Offline `None` —
    die Sitzungsbilanz des zweiten Embeds war leer.

Die Regel hier: ein Nutzer hat einen von drei Zustaenden, und nur ein
WECHSEL loest die globalen Aktionen aus.

    (fehlt)  unbekannt — nach einem Neustart. Ein Offline zaehlt dann als
             Wechsel (der erste Chat meldet, der zweite nicht mehr), ein
             Live ebenso.
    "live"   die Live-Aktionen sind gelaufen; ein zweites Live schweigt.
    "aus"    die Offline-Aktionen sind gelaufen; ein zweites Offline schweigt.

Bewusst KEINE Menge von Tracking-IDs („beim letzten Offline raeumen"): ein
Tracking, das waehrend des Streams pausiert oder entfernt wird, meldet sein
Offline nie, und die Menge wuerde nie leer — die Offline-Bilanz fiele dann
ganz aus. Es ist derselbe Nutzer; das ERSTE bestaetigte Offline ist die
Wahrheit fuer alle Chats.

Aufgerufen wird nur aus dem Event-Loop, zwischen Pruefen und Setzen steht kein
await — damit ist der Wechsel atomar, auch wenn zwei Worker denselben Nutzer
gleichzeitig bearbeiten.
"""
from __future__ import annotations

from typing import Dict

LIVE = "live"
AUS = "aus"

# username -> LIVE | AUS. Klein (ein Eintrag je verfolgtem Nutzer), daher
# ohne Deckel.
STAND: Dict[str, str] = {}


def _schluessel(username: str) -> str:
    """LIVE-6: TikTok-Handles sind gross/klein-unabhaengig, gespeichert wird
    der Name aber so, wie er eingegeben wurde. „MaxMuster" in einem Chat und
    „maxmuster" im zweiten waren hier zwei Nutzer — zwei Discord-LIVE-Embeds
    und zwei Live-Threads fuer EINEN Stream, genau der Befund aus W176."""
    return (username or "").lower()


def live_an(username: str) -> bool:
    """Ein Tracking hat den Wechsel auf LIVE beansprucht.
    -> True, wenn die globalen Live-Aktionen jetzt laufen sollen."""
    k = _schluessel(username)
    if STAND.get(k) == LIVE:
        return False
    STAND[k] = LIVE
    return True


def live_aus(username: str) -> bool:
    """Ein Tracking hat den Wechsel auf OFFLINE beansprucht.
    -> True, wenn die globalen Offline-Aktionen jetzt laufen sollen."""
    k = _schluessel(username)
    if STAND.get(k) == AUS:
        return False
    STAND[k] = AUS
    return True
