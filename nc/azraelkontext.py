"""nc.azraelkontext — v4.2-W177: AZRAEL bekommt, was das Brain weiss.

WARUM DIESES MODUL
==================
Der Betreiber: "die Gehirn-Strukturen sind nicht miteinander verwoben". Das
stimmte woertlich. Das Brain leitet aus jeder Sendung Fakten ab
(brain/knowledge.py: duration_class, peak_hour_utc, sessions_per_week), der
Bot schreibt nach jeder Aufnahme eine Zusammenfassung (stream_memories) —
und AZRAELs Antwortpfade (KickModerator.react/_reply) fragten keins von
beiden. AZRAEL plauderte ueber einen Streamer, ueber den das System seit
Wochen Buch fuehrt, als saehe es ihn zum ersten Mal.

Dieses Modul baut daraus EINE kurze System-Nachricht (hoechstens
`MAX_ZEICHEN`). Kurz, weil jede Zeile Kontext auf der 8-Kern-Box Rechenzeit
der lokalen Inferenz kostet und weil ein langer Block die Persona
ueberstimmt.

Bot-frei (kein Import aus bot.py): Brain und Datenbank-Zugang kommen als
Argumente. Ein Fehler darf die Antwort NIE verhindern — `sicher()` faengt
alles, meldet gedrosselt (nc.meldetakt, Schluessel = Kanal) und gibt None
zurueck; AZRAEL antwortet dann eben ohne Kontext.
"""
from __future__ import annotations

import logging
import time
from typing import Callable, Iterable, Optional

from . import meldetakt as _meldetakt

log = logging.getLogger("nc.azraelkontext")

KANAL = "azrael-kontext"
MAX_ZEICHEN = 300
_DAUER = {"short": "kurz (unter 15 min)", "medium": "mittel (15–60 min)",
          "long": "lang (über 1 h)"}
_LAUFEND = ("live", "running", "starting")


def streamer_waehlen(source: Optional[str],
                     restream_quellen: Iterable[str] = ()) -> Optional[str]:
    """Welcher Streamer ist gemeint?

    `source` ist bei der Live-Reaktion der verfolgte Nutzer. Bei einer
    Chat-Antwort steht dort "plattform:zuschauer" — der Zuschauer ist kein
    Streamer, ueber den das Brain etwas weiss; ebenso "cohost". Dann ist der
    gemeint, dessen Sendung gerade restreamt wird (erste laufende Quelle)."""
    s = (source or "").strip().lstrip("@")
    direkt = [s] if s and ":" not in s and s.lower() != "cohost" else []
    kandidaten = direkt + [q for q in ((x or "").strip().lstrip("@")
                                       for x in restream_quellen) if q]
    # "Kein Streamer bestimmbar" ist kein Fehler (kein Restream, Testknopf
    # im Deck) — dann gibt es schlicht keinen Kontext.
    return next(iter(kandidaten), None)


def restream_quellen(brain) -> list:
    """Quellen der laufenden Restreams aus dem Brain-Zustand."""
    out = []
    for e in brain.state.query("restream"):
        if e.get("state") in _LAUFEND:
            q = (e.get("attrs") or {}).get("source")
            if q and q not in out:
                out.append(q)
    return out


def fakten(knowledge, user: str) -> dict:
    """Die drei Fakten aus dem Wissensgraphen, die fuer ein Gespraech taugen."""
    out = {}
    for f in knowledge.query(s=user):
        if f["p"] in ("duration_class", "peak_hour_utc", "sessions_per_week") \
                and f["p"] not in out:
            out[f["p"]] = f["o"]
    return out


def letzte_erinnerung(db_conn: Callable, user: str) -> str:
    with db_conn() as conn:
        r = conn.execute(
            "SELECT summary FROM stream_memories WHERE username=? "
            "ORDER BY id DESC LIMIT 1", (user,)).fetchone()
    return str(r["summary"] or "").strip() if r else ""


def block(user: str, f: dict, erinnerung: str = "",
          max_zeichen: int = MAX_ZEICHEN) -> Optional[str]:
    """Den Kontextblock bauen — None, wenn es nichts zu sagen gibt (ein
    leerer Block waere nur ein Rauschen im Prompt)."""
    teile = []
    if "peak_hour_utc" in f:
        teile.append(f"sendet meist um {f['peak_hour_utc']} Uhr UTC")
    if "sessions_per_week" in f:
        teile.append(f"etwa {f['sessions_per_week']} Sendungen pro Woche")
    if f.get("duration_class") in _DAUER:
        teile.append(f"Sendungen meist {_DAUER[f['duration_class']]}")
    erinnerung = " ".join((erinnerung or "").split())
    text = f"Was du über @{user} weisst (nur bei Bedarf erwähnen):"
    if teile:
        text += " " + "; ".join(teile) + "."
    if erinnerung:
        rest = max_zeichen - len(text) - len(" Letzte Sendung: ") - 1
        if rest > 20:
            if len(erinnerung) > rest:
                erinnerung = erinnerung[:rest - 1].rstrip() + "…"
            text += " Letzte Sendung: " + erinnerung
    # Ein Kopf ohne Inhalt waere nur Rauschen im Prompt — dann kein Block.
    return text[:max_zeichen] if (teile or erinnerung) else None


def nachricht(brain, db_conn: Optional[Callable], source: Optional[str]) -> Optional[dict]:
    """Die fertige System-Nachricht oder None. Wirft bei Fehlern — der
    Aufrufer im Bot geht ueber `sicher()`."""
    user = streamer_waehlen(source, restream_quellen(brain))
    text = None
    if user:
        f = fakten(brain.knowledge, user)
        erinnerung = letzte_erinnerung(db_conn, user) if db_conn else ""
        text = block(user, f, erinnerung)
    return {"role": "system", "content": text} if text else None


def ausfall(grund: str, detail: str = "") -> None:
    """Gedrosselt melden, dass AZRAEL ohne Brain-Kontext antwortet."""
    laut, unterdrueckt = _meldetakt.melden(KANAL, grund, time.time())
    if laut:
        log.warning("AZRAEL antwortet ohne Brain-Kontext (%s%s) — die Antwort "
                    "selbst laeuft weiter. Pruefen: brain.db lesbar, Tabelle "
                    "stream_memories vorhanden.%s",
                    grund, f": {detail}" if detail else "",
                    _meldetakt.zusatz(unterdrueckt))


def sicher(brain_holen: Callable, db_conn: Optional[Callable],
           source: Optional[str]) -> Optional[dict]:
    """`nachricht()` ohne Ausnahme: Fehler → gedrosselte Meldung, None."""
    try:
        m = nachricht(brain_holen(), db_conn, source)
    except Exception as e:  # noqa: BLE001 — darf die Antwort nie verhindern
        ausfall(type(e).__name__, str(e)[:160])
        return None
    _meldetakt.zuruecksetzen(KANAL)
    return m
