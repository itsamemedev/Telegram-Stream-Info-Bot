"""nc.restream_guard — Soll-Zustand und ehrliche Zielpruefung fuer Restreams.

════════════════════════════════════════════════════════════════════════
ZWEI PROBLEME, DIE HIER GELOEST WERDEN
════════════════════════════════════════════════════════════════════════

PROBLEM 1 — "laeuft" hiess bisher nur "Prozess existiert".
RestreamManager.status() meldete `"live": True` fuer jeden Eintrag in
self._procs. Das ist die Antwort auf die Frage "laeuft ffmpeg?", nicht
auf "kommt das Bild bei Kick/Twitch/YouTube an?".

Der Unterschied ist bei Multistream systematisch, nicht zufaellig: der
tee-Muxer bekommt fuer die ZUSATZ-Ziele (Twitch, YouTube) bewusst
`onfail=ignore`, damit ein klemmendes Twitch nicht den Kick-Stream
mitreisst. Genau deshalb bleibt der Prozess aber am Leben, wenn Twitch
oder YouTube wegbrechen — ffmpeg schreibt weiter an Kick, meldet keinen
Fehler, und das Panel zeigt drei gruene Ziele, waehrend auf zwei
Plattformen nichts ankommt. Das ist exakt das beobachtete Bild.

ACHTUNG, seit B137 stimmt das fuer Kick NICHT mehr: auch der Primaerpfad
traegt jetzt onfail=ignore (kick_hard=False, siehe nc/restream_targets.py).
Der Prozess ueberlebt eine Kick-Ablehnung also — _monitor greift NICHT
mehr, und dieser Waechter ist die einzige Instanz, die einen toten
Kick-Ausgang noch bemerken kann. Der alte Absatz behauptete das Gegenteil
und hat die Fehlersuche zum "Input/output error" in die falsche Richtung
geschickt. Nur im Modus RESTREAM_MULTI_MODE=independent gibt es keinen tee:
dort laeuft Kick im eigenen Prozess, kick_hard ist wirkungslos und der
Ausfall ist wieder hart.

LOESUNG: nicht ffmpeg fragen, sondern die PLATTFORM. Fuer alle drei gibt
es bereits Statusabfragen (Kick keyless, Twitch Helix, YouTube Data API).
Ein Ziel gilt erst als live, wenn die Plattform selbst sagt, dass sie
sendet.

PROBLEM 2 — nach Neustart/Absturz kam nicht alles zurueck.
auto_start_due() startete nur Restreams mit `auto_restream=1`, und auch
die nur, wenn die Quelle zufaellig im richtigen Moment live war. Ein von
Hand gestarteter Restream war nach einem Neustart weg, ohne Spur.

LOESUNG: Soll-Zustand persistieren. Wer laufen SOLL, laeuft nach dem
Neustart wieder — unabhaengig davon, wie er gestartet wurde. Ein
ausdrueckliches Stop setzt den Soll-Zustand auf 0; ein Absturz nicht.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL BOT-FREI IST
════════════════════════════════════════════════════════════════════════
Die Entscheidungslogik ist der heikle Teil: Karenzzeiten, Hysterese,
Backoff. Falsch gebaut erzeugt sie eine Neustart-Schleife, die schlimmer
ist als das Problem. Deshalb steckt sie hier in reinen Funktionen ohne
DB, ohne asyncio, ohne ffmpeg — vollstaendig testbar.

════════════════════════════════════════════════════════════════════════
DIE VIER REGELN, DIE EINE NEUSTART-SCHLEIFE VERHINDERN
════════════════════════════════════════════════════════════════════════
1. KARENZ NACH START (startup_grace_s). RTMP braucht 20-60s, bis die
   Plattform den Stream als live fuehrt — YouTube ist am langsamsten.
   Vor Ablauf der Karenz wird gar nicht bewertet. Ohne das wuerde jeder
   frische Restream sofort wieder abgeschossen.
2. HYSTERESE (misses_before_action). Eine einzelne fehlgeschlagene
   Abfrage beweist nichts: Rate-Limit, Timeout, kurzer API-Aussetzer.
   Erst N aufeinanderfolgende Fehlanzeigen zaehlen als Ausfall.
3. UNBEKANNT IST NICHT OFFLINE. Antwortet die Plattform-API gar nicht
   (Netzfehler, Quota), ist das KEIN Beweis fuer einen toten Stream.
   Solche Antworten setzen den Zaehler nicht hoch — sonst wuerde ein
   API-Ausfall reihenweise gesunde Streams neu starten.
4. BACKOFF (restart_backoff_s, verdoppelnd bis max). Hilft ein Neustart
   nicht, liegt es nicht am Neustart. Immer schneller neu zu starten
   macht es schlimmer.

Zusaetzlich: ist die QUELLE offline, ist ein totes Ziel der Normalfall
und kein Fehler — dann wird nichts unternommen.
"""

from dataclasses import dataclass, field

# Ergebnis einer Plattform-Abfrage.
LIVE = "live"          # Plattform bestaetigt: sendet
OFFLINE = "offline"    # Plattform sagt ausdruecklich: sendet nicht
UNKNOWN = "unknown"    # keine belastbare Antwort (Fehler, Quota, nicht konfiguriert)

# Was der Aufrufer tun soll.
ACT_NONE = "none"
ACT_START = "start"        # soll laufen, laeuft aber nicht
ACT_RESTART = "restart"    # laeuft, aber ein Ziel ist nachweislich tot
ACT_STOP = "stop"          # laeuft, soll aber nicht


@dataclass
class GuardConfig:
    startup_grace_s: float = 90.0      # YouTube meldet am spaetesten
    misses_before_action: int = 3      # bei 120s-Takt: ~6 Minuten Gewissheit
    restart_backoff_s: float = 60.0
    restart_backoff_max_s: float = 900.0
    verify_interval_s: float = 120.0
    # v5.9-W206: so oft darf EIN totes Ziel den ganzen Restream neu aufbauen,
    # solange ein anderes Ziel nachweislich sendet. Danach gilt es als
    # aufgegeben (bis zum naechsten Start von aussen) — siehe evaluate().
    neuaufbau_je_ziel: int = 1


@dataclass
class TargetState:
    """Zustand EINER Plattform innerhalb eines Restreams."""
    misses: int = 0
    last_result: str = UNKNOWN
    last_seen_live: float = 0.0
    confirmed: bool = False        # war seit dem Start mindestens einmal live
    neuaufbauten: int = 0          # v5.9-W206: Neuaufbauten, die DIESES Ziel ausloeste
    aufgegeben: bool = False       # v5.9-W206: kein Neuaufbau mehr wegen dieses Ziels


@dataclass
class RestreamState:
    """Zustand eines Restreams ueber alle seine Ziele."""
    rid: int
    started_at: float = 0.0
    targets: dict = field(default_factory=dict)      # platform -> TargetState
    restarts: int = 0
    last_restart: float = 0.0
    backoff_s: float = 0.0

    def target(self, platform: str) -> TargetState:
        return self.targets.setdefault(platform, TargetState())


class RestreamGuard:
    """Haelt den Zustand aller ueberwachten Restreams. Reine Logik."""

    def __init__(self, cfg: GuardConfig = None):
        self.cfg = cfg or GuardConfig()
        self._states: dict = {}

    def state(self, rid: int) -> RestreamState:
        return self._states.setdefault(rid, RestreamState(rid=rid))

    def note_started(self, rid: int, now: float):
        """Nach einem (Neu-)Start aufrufen: Karenz beginnt, Zaehler auf 0."""
        st = self.state(rid)
        st.started_at = now
        for t in st.targets.values():
            t.misses = 0
            t.confirmed = False
            t.last_result = UNKNOWN

    def forget(self, rid: int):
        self._states.pop(rid, None)

    # ─────────────────────────────────────────────────────── Bewertung

    def evaluate(self, rid, *, running, desired, source_live,
                 platform_results: dict, now: float) -> dict:
        """Eine Entscheidung fuer EINEN Restream.

        platform_results: {"kick": LIVE|OFFLINE|UNKNOWN, "twitch": ..., ...}
                          Nur konfigurierte Ziele uebergeben.
        Rueckgabe: {"action", "reason", "dead": [...], "detail": {...}}
        """
        st = self.state(rid)

        if not desired:
            return self._r(ACT_STOP if running else ACT_NONE,
                           "Soll-Zustand ist aus", st)

        if not running:
            # Soll laufen, laeuft nicht: Absturz oder Neustart des Bots.
            if not source_live:
                return self._r(ACT_NONE, "Quelle nicht live — kein Start", st)
            if st.last_restart and now - st.last_restart < st.backoff_s:
                wait = round(st.backoff_s - (now - st.last_restart))
                return self._r(ACT_NONE, f"Backoff aktiv ({wait}s)", st)
            return self._r(ACT_START, "soll laufen, laeuft nicht", st)

        # Laeuft. Jetzt die ehrliche Frage: kommt es auch an?
        if now - st.started_at < self.cfg.startup_grace_s:
            left = round(self.cfg.startup_grace_s - (now - st.started_at))
            return self._r(ACT_NONE, f"Anlaufkarenz ({left}s)", st)

        if not source_live:
            # Quelle weg -> Ziele sind zu Recht leer. Zaehler zuruecksetzen,
            # damit nach der Rueckkehr der Quelle nicht sofort neu gestartet
            # wird, nur weil waehrend der Pause Fehlanzeigen aufliefen.
            for t in st.targets.values():
                t.misses = 0
            return self._r(ACT_NONE, "Quelle offline — Ziele erwartet leer", st)

        dead = []
        for platform, result in platform_results.items():
            t = st.target(platform)
            t.last_result = result
            if result == LIVE:
                t.misses = 0
                t.confirmed = True
                t.last_seen_live = now
                # Sendet ein aufgegebenes Ziel wieder (Betreiber hat den
                # Schluessel getauscht), bekommt es seine Versuche zurueck.
                t.aufgegeben = False
                t.neuaufbauten = 0
            elif result == OFFLINE:
                t.misses += 1
                if t.misses >= self.cfg.misses_before_action:
                    dead.append(platform)
            # UNKNOWN: Regel 3 — kein Beweis, Zaehler bleibt unveraendert.

        # v5.9-W206: ein totes Ziel reisst die anderen nicht endlos mit.
        # Bei tee laesst sich kein einzelnes Ziel neu verbinden — ein
        # Neuaufbau beendet ALLE. Beim Betreiber am 13.11.: YouTube ging nicht
        # live, der Waechter baute siebenmal im Sechs-Minuten-Takt neu auf,
        # und jedes Mal brach Kick mit ab (Broken pipe, Pausenbild, Neustart
        # unter Volllast). Sendet ein anderes Ziel nachweislich, bekommt das
        # tote `neuaufbau_je_ziel` Versuche; danach ist es aufgegeben, und
        # die Ziele, die laufen, bleiben in Ruhe. Erst wenn KEIN Ziel mehr
        # sendet, wird wie bisher neu aufgebaut.
        lebende = [p for p, r in platform_results.items() if r == LIVE]
        neu_aufgegeben = []
        if lebende:
            for p in list(dead):
                t = st.target(p)
                if t.aufgegeben:
                    dead.remove(p)
                elif t.neuaufbauten >= self.cfg.neuaufbau_je_ziel:
                    t.aufgegeben = True
                    neu_aufgegeben.append(p)
                    dead.remove(p)
        aufgegeben = sorted(p for p, t in st.targets.items() if t.aufgegeben)

        if not dead:
            if aufgegeben:
                return self._r(ACT_NONE,
                               "%s aufgegeben — %s senden weiter"
                               % (", ".join(aufgegeben), ", ".join(sorted(lebende)) or "keins"),
                               st, aufgegeben=aufgegeben, neu_aufgegeben=neu_aufgegeben)
            return self._r(ACT_NONE, "alle Ziele bestaetigt", st)

        if st.last_restart and now - st.last_restart < st.backoff_s:
            wait = round(st.backoff_s - (now - st.last_restart))
            return self._r(ACT_NONE,
                           f"{', '.join(dead)} tot, aber Backoff aktiv ({wait}s)",
                           st, dead=dead)

        return self._r(ACT_RESTART,
                       f"{', '.join(dead)} meldet offline trotz laufendem Prozess",
                       st, dead=dead)

    def note_restart(self, rid: int, now: float, dead=None):
        """Nach einem ausgeloesten Neustart aufrufen: Backoff hochsetzen.

        `dead` (v5.9-W206): die Ziele, deretwegen neu aufgebaut wurde — ihre
        Versuche zaehlen fuer die Regel „ein totes Ziel reisst die anderen
        nicht endlos mit"."""
        st = self.state(rid)
        for p in dead or ():
            st.target(p).neuaufbauten += 1
        st.restarts += 1
        st.last_restart = now
        st.backoff_s = (self.cfg.restart_backoff_s if not st.backoff_s
                        else min(st.backoff_s * 2, self.cfg.restart_backoff_max_s))
        self.note_started(rid, now)

    def note_healthy(self, rid: int):
        """Laeuft ein Restream wieder laenger sauber, Backoff zuruecksetzen —
        sonst bleibt eine einmalige Stoerung ewig als Strafe haengen."""
        st = self.state(rid)
        st.backoff_s = 0.0

    def _r(self, action, reason, st, dead=None, aufgegeben=None, neu_aufgegeben=None):
        return {"action": action, "reason": reason, "dead": dead or [],
                "aufgegeben": aufgegeben or [], "neu_aufgegeben": neu_aufgegeben or [],
                "detail": {p: {"result": t.last_result, "misses": t.misses,
                               "confirmed": t.confirmed, "aufgegeben": t.aufgegeben}
                           for p, t in st.targets.items()},
                "restarts": st.restarts,
                "backoff_s": round(st.backoff_s)}

    def snapshot(self) -> dict:
        """Fuer Dashboard/Diagnose."""
        return {rid: {"restarts": s.restarts, "backoff_s": round(s.backoff_s),
                      "started_at": s.started_at,
                      "targets": {p: {"result": t.last_result,
                                      "misses": t.misses,
                                      "confirmed": t.confirmed,
                                      "aufgegeben": t.aufgegeben,
                                      "last_seen_live": t.last_seen_live}
                                  for p, t in s.targets.items()}}
                for rid, s in self._states.items()}


def classify(status: dict) -> str:
    """Plattform-Statusdict (aus /api/channels/status) -> LIVE/OFFLINE/UNKNOWN.

    Die Unterscheidung OFFLINE vs UNKNOWN ist der Kern von Regel 3: nur ein
    ausdrueckliches "nicht live" darf einen Neustart ausloesen. Fehler,
    fehlende Konfiguration und leere Antworten sind UNKNOWN."""
    if not isinstance(status, dict):
        return UNKNOWN
    if status.get("error") or not status.get("configured", True):
        return UNKNOWN
    v = status.get("is_live")
    if v is None:
        v = status.get("live")
    if v is None:
        return UNKNOWN
    return LIVE if v else OFFLINE


def abhilfe(platform: str) -> str:
    """Was der Betreiber tun kann, wenn ein Ziel trotz Neuaufbau nicht live
    geht (v5.9-W206). Der haeufigste Fall ist kein Fehler des Bots."""
    p = str(platform or "").lower()
    if p == "youtube":
        return ("YouTube nimmt den Strom an, startet die Sendung aber nicht: im "
                "YouTube Studio den Stream-Schluessel pruefen und „Automatisch "
                "starten\" fuer den Stream einschalten — oder YouTube im Deck "
                "(Restream › Ziele) abschalten.")
    if p == "twitch":
        return ("Twitch-Stream-Schluessel pruefen (Twitch › Creator-Dashboard), "
                "oder Twitch im Deck abschalten.")
    if p == "kick":
        return "Kick-Stream-Schluessel und Ingest-Adresse pruefen (Kick › Creator)."
    return "Stream-Schluessel dieses Ziels pruefen oder das Ziel im Deck abschalten."
