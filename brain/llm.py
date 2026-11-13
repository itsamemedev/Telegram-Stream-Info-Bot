# brain/llm.py — M6: Eigene LLM-Runtime (llama.cpp; V37: ollama-frei;
#                 v5.1-W181: ik_llama.cpp mit Qwen3-14B-Uncensored)
#
# ARCHITEKTUR-ENTSCHEIDUNG (ehrlich begründet): Die "eigene Runtime"
# ist llama.cpp (llama-server, GGUF INT4) statt einer Python-Eigenbau-
# Inferenz (tokenizer.py/attention.py/kv_cache.py). WARUM:
#   - llama.cpp liefert GQA, Sliding-Window-Attention, Streaming-KV-Cache
#     und INT4/INT3-Quantisierung produktionsreif und CPU-optimiert (AVX2).
#   - Eine Pure-Python-Attention wäre auf 8 Cores 10-50x langsamer und
#     monatelange Arbeit ohne Mehrwert — Verstoß gegen die v37-Kernregel
#     "niemals nur für mehr KI optimieren".
#   - Ollama fällt trotzdem weg: llama-server ist EIN statisches Binary
#     + EIN GGUF-File, kein Go-Daemon, kein Model-Registry-Overhead.
#
# BUDGET-PRINZIP: Das LLM ist Tier 4 — die LETZTE Instanz. Begrenzt wird
# es ueber die Inferenz-PLAETZE (so viele, wie llama-server mit --parallel
# hat; die Unit laeuft mit Nice=10/CPUWeight=50, Aufnahmen haben Vorrang).
# Ein Stundendeckel (BRAIN_LLM_MAX_CALLS_H) ist seit v5.9-W202 nur noch
# Option: der alte Deckel 30/h lag beim Betreiber mit 800 Mitgliedern bei
# 894 Ablehnungen — er schuetzte nicht die Kerne, er schaltete die KI ab.
# Budget erschöpft ⇒ der Router bekommt Unhandled und antwortet ehrlich
# "kein Tier konnte".
#
# WARUM stdlib-urllib statt aiohttp: brain/ ist thread-basiert (M1) und
# dependency-frei. Blocking-HTTP ist bei Concurrency 1 kein Nachteil.

from __future__ import annotations

import json
import logging
import os
import threading
import time
import urllib.error
import urllib.request
from typing import Optional

from nc.envnum import env_float, env_int  # v4.0-W78/W81: leer-gesetzte .env robust

log = logging.getLogger("brain.llm")

# B-M6-1: Konfig als Laufzeit-Lookup statt Modul-Konstante. WARUM:
# bot_v36 lädt .env teils NACH den ersten Imports — Konstanten würden
# die Defaults einfrieren, bevor die echten Werte existieren (gleiche
# Bug-Klasse wie BRAIN_DB in M1, dort bereits gefixt).
def _backend_conf() -> str:
    return os.getenv("BRAIN_LLM_BACKEND", "auto")   # auto|llamacpp|off (V37: ollama entfernt)


def _llamacpp_url() -> str:
    return os.getenv("BRAIN_LLAMACPP_URL", "http://127.0.0.1:8080").rstrip("/")


def _max_calls_h() -> int:
    """Stundendeckel fuer lokale Antworten. 0 (Vorgabe seit v5.9-W202) = keiner.

    Die Kerne schuetzen die Plaetze und die Unit (Nice/CPUWeight), nicht eine
    Zahl je Stunde: bei rund 46 s je Antwort schafft EIN Platz ohnehin nur
    rund 78 Antworten in der Stunde — 30 war weniger als die Haelfte davon."""
    return max(0, env_int("BRAIN_LLM_MAX_CALLS_H", 0))


def _plaetze_conf() -> str:
    """BRAIN_LLM_PLAETZE: auto (Vorgabe) = so viele, wie llama-server meldet
    (/props total_slots, also sein --parallel); eine Zahl erzwingt sie."""
    return os.getenv("BRAIN_LLM_PLAETZE", "auto").strip().lower()


MAX_PLAETZE = 16
# So viele duerfen je Platz anstehen; wer danach kommt, bekommt sofort „belegt".
WARTESCHLANGE_JE_PLATZ = 3


def _timeout_s() -> float:
    # V37-LLMBUDGET: CPU-Inferenz ohne GPU braucht Zeit — 60s war zu knapp und
    # riss Requests mitten in der Antwort ab. Auf 300s angehoben (deckt lange
    # Antworten auf 8 Cores). Über BRAIN_LLM_TIMEOUT_S weiter frei einstellbar.
    return env_float("BRAIN_LLM_TIMEOUT_S", 300)


def _denken() -> bool:
    """v5.1-W181: darf das lokale Modell vor der Antwort „denken"?

    Qwen3 schreibt ab Werk erst einen <think>…</think>-Block und dann die
    Antwort. Auf 8 CPU-Kernen sind das hunderte Token, bevor das erste Wort
    der Antwort kommt — bei max_tokens 1024 bleibt fuer die Antwort oft
    nichts, und der Chat sah leer aus. Vorgabe deshalb AUS."""
    return os.getenv("BRAIN_LLM_DENKEN", "0").strip().lower() in ("1", "true", "ja", "yes", "on")


_DENK_AUF, _DENK_ZU = "<think>", "</think>"


def ohne_denkblock(text) -> str:
    """Den Denkblock eines Reasoning-Modells (Qwen3) aus der Antwort nehmen.

    v5.1-W181. Drei Formen kommen vor, und jede landete sonst woertlich im
    Telegram-Chat, im Overlay und in der Sprachausgabe:
      * ``<think>…</think>Antwort`` — der Normalfall ohne --jinja,
      * ``…</think>Antwort`` — die Vorlage hat ``<think>`` selbst gesetzt
        (thinking_forced_open), nur das Ende steht in der Ausgabe,
      * ``<think>…`` ohne Ende — max_tokens riss mitten im Denken ab. Dann
        gibt es KEINE Antwort, und ``""`` sagt das; der Aufrufer faellt auf das
        naechste Backend, statt halbe Gedanken als Antwort auszugeben.
    Gross-/Kleinschreibung egal; mehrere Bloecke werden alle entfernt."""
    t = str(text or "")
    klein = t.lower()
    if _DENK_ZU in klein:
        # Alles bis zum LETZTEN Ende ist Denken — auch ein zweiter Block, der
        # vor der Antwort steht. Was danach kommt, ist die Antwort.
        t = t[klein.rindex(_DENK_ZU) + len(_DENK_ZU):]
    elif _DENK_AUF in klein:
        t = t[:klein.index(_DENK_AUF)]
    return t.strip()


def _max_tokens() -> int:
    # V37-LLMBUDGET: 512 schnitt längere Antworten ab. Auf 1024 verdoppelt —
    # genug für ausführliche Antworten, ohne den CPU-Aufwand zu sprengen.
    return env_int("BRAIN_LLM_MAX_TOKENS", 1024)


def _reserve() -> int:
    """v5.5-W196: so viele Aufrufe der Stunde bleiben Gespraechen vorbehalten.
    Eigeninitiative (Vorrang „nebenbei") darf sie nicht verbrauchen — sonst
    plaudert AZRAEL das Budget leer, und wer ihn anspricht, bekommt die Cloud."""
    return max(0, env_int("BRAIN_LLM_RESERVE", 8))


# v5.5-W196: Rang je Vorrang — kleiner kommt zuerst.
RANG = {"gespraech": 0, "reaktion": 1, "nebenbei": 2}


class _Vorrangslot:
    """Die Inferenz-Plaetze, mit Warteschlange nach Vorrang.

    v5.9-W202: bis dahin genau EIN Platz („Concurrency 1"), und jeder zweite
    /brain-Aufruf in einer Gruppe mit 800 Mitgliedern bekam „Slot belegt"
    (22-mal gezaehlt). Jetzt so viele Plaetze, wie llama-server hat
    (`erwerben(..., kapazitaet=n)`); die Regel bleibt dieselbe: frei wird ein
    Platz fuer den Besten, der wartet. Mit n=1 verhaelt sich alles wie vorher.

    Bis W196 war der Platz ein Lock mit `acquire(blocking=False)`: wer kam,
    waehrend Qwen rechnete, flog sofort raus und ging in die Cloud. Auf der
    CPU rechnet ein 14B-Modell eine Antwort in zehn bis hundert Sekunden —
    der Platz war also fast immer belegt, und AZRAEL sprach meistens mit
    fremder Stimme. Jetzt darf ein Aufrufer bis `warten_s` warten, und frei
    wird der Platz fuer den mit dem besten Rang, der gerade wartet: ein
    Gespraech ueberholt eine Live-Reaktion, die ueberholt die Eigeninitiative.
    Wer nicht warten will (warten_s=0), verhaelt sich wie vorher."""

    def __init__(self):
        self._bed = threading.Condition()
        self._belegt = 0
        self._wartend: list[int] = []

    def erwerben(self, rang: int, warten_s: float, kapazitaet: int = 1,
                 max_wartend: Optional[int] = None) -> bool:
        """max_wartend (v5.9-W202): stehen schon so viele an, wird nicht mehr
        angestellt, sondern sofort abgewiesen. Jeder Wartende haelt einen
        Thread fest — 800 Mitglieder, die /brain fragen, duerfen den Bot nicht
        mit wartenden Threads zustellen (W47: dieselben Threads braucht DNS)."""
        frist = time.monotonic() + max(0.0, warten_s)
        kap = max(1, int(kapazitaet or 1))
        with self._bed:
            if (max_wartend is not None and warten_s > 0
                    and len(self._wartend) >= max_wartend):
                warten_s, frist = 0.0, time.monotonic()
            self._wartend.append(rang)
            try:
                # Frei ist ein Platz fuer MICH erst, wenn nach allen Besseren,
                # die gerade warten, noch einer uebrig bleibt.
                while self._belegt + sum(1 for r in self._wartend if r < rang) >= kap:
                    rest = frist - time.monotonic()
                    if rest <= 0:
                        return False
                    self._bed.wait(rest)
                self._belegt += 1
                return True
            finally:
                self._wartend.remove(rang)
                # Wer aufgibt, kann einen schlechter Gerangten blockiert haben,
                # der nur auf IHN gewartet hat — also alle wecken.
                self._bed.notify_all()

    def freigeben(self):
        with self._bed:
            self._belegt = max(0, self._belegt - 1)
            self._bed.notify_all()

    def lage(self) -> dict:
        with self._bed:
            return {"belegt": self._belegt > 0, "in_arbeit": self._belegt,
                    "wartend": len(self._wartend)}


def _ohne_denken_bitten(messages: list) -> list:
    """Qwen3s Schalter ``/no_think`` an die LETZTE Nutzernachricht haengen.

    Eine Kopie — die Liste des Aufrufers bleibt unveraendert (bot.py haelt
    damit den Verlauf, und dort darf der Schalter nicht landen). Nur
    Text-Inhalte: ein Bild-Inhalt (Liste) bleibt, wie er ist."""
    raus = [dict(m) if isinstance(m, dict) else m for m in (messages or [])]
    for m in reversed(raus):
        if isinstance(m, dict) and m.get("role") == "user":
            if isinstance(m.get("content"), str) and "/no_think" not in m["content"]:
                m["content"] = m["content"].rstrip() + " /no_think"
            break
    return raus


class BudgetExhausted(Exception):
    """Stundenbudget verbraucht — Aufrufer (Router-Tier) reicht als
    Unhandled weiter statt zu warten: Warten würde den Router-Pfad
    blockieren, und Tier-4-Antworten sind nie zeitkritisch genug dafür."""


class LLMRuntime:
    def __init__(self):
        # Die Inferenz-Plaetze. Seit v5.5-W196 mit Vorrang und Wartezeit
        # (_Vorrangslot), seit v5.9-W202 so viele, wie llama-server hat.
        self._slot = _Vorrangslot()
        self._server_plaetze = None       # aus /props; None = nicht gemessen
        self._plaetze_t = -1e9            # wann zuletzt gemessen (monotonic)
        self._plaetze_fehler = None
        self._zeiten: dict = {}           # v5.5-W196: timings der letzten lokalen Antwort
        self._calls: list[float] = []
        self._durs: list[float] = []      # V37: letzte Latenzen (ms)      # Timestamps fürs Stundenbudget
        self._stats = {"ok": 0, "errors": 0, "budget_denied": 0,
                       "busy_denied": 0, "by_backend": {},
                       "reserve_denied": 0, "prompt_token": 0, "prompt_gecacht": 0}
        # B-M6-2: RLock, nicht Lock — stats() ruft unter gehaltenem Lock
        # budget() auf, das denselben Lock nimmt. Nicht-reentrant = Deadlock.
        self._stats_lock = threading.RLock()
        self._letzter_fehler: dict = {}   # backend -> letzter Grund (Meldedrossel)

    # ------------------------------------------------------------- API

    def chat(self, messages: list[dict], timeout: Optional[float] = None,
             max_tokens: Optional[int] = None,
             backends: Optional[list] = None,
             vorrang: Optional[str] = None, warten_s: float = 0.0) -> dict:
        """Eine Chat-Vervollständigung über die Backend-Kette.

        Rückgabe: {ok, text|error, backend, ms}. Wirft BudgetExhausted
        bei verbrauchtem Budget (bewusst Exception statt ok=False: der
        Unterschied 'LLM kaputt' vs. 'LLM gedeckelt' muss im Router-Trace
        unterscheidbar sein).

        v4.2-W177 `backends`: schraenkt die konfigurierte Kette ein (nie
        erweitern — BRAIN_LLM_BACKEND=off bleibt aus). bot.py hat fuer Chat,
        AZRAEL und Reaction-Engine einen EIGENEN Cloud-Rueckfall; ohne die
        Einschraenkung fuhr chat() llamacpp UND freeai (bis 2x Timeout), und
        bei ok=False fragte der Aufrufer freeai ein zweites Mal.

        Das Stundenbudget gilt nur fuer llama.cpp: es schuetzt die Kerne
        der Box vor der lokalen Inferenz. Ein Cloud-Aufruf kostet die Box
        nichts — bis W177 zaehlte er trotzdem mit, und nach 30 Cloud-
        Antworten meldete der Router "Budget verbraucht", ohne dass ein
        einziges Mal lokal gerechnet worden war. Ist das Budget weg, faellt
        nur der llamacpp-Schritt aus; BudgetExhausted kommt erst, wenn
        danach nichts mehr in der Kette steht.

        v5.5-W196 `vorrang` (gespraech|reaktion|nebenbei) und `warten_s`: wer
        einen Vorrang nennt, darf auf den Platz warten und wird nach Rang
        bedient; „nebenbei" bekommt die letzten BRAIN_LLM_RESERVE Aufrufe der
        Stunde nicht. Ohne Angabe: wie vorher (Rang „reaktion", kein Warten)."""
        rang = RANG.get(vorrang or "reaktion", RANG["reaktion"])
        kette = self._chain()
        if backends is not None:
            kette = [x for x in kette if x in backends]
        budget_grund = self._deckel_grund(rang) if "llamacpp" in kette else None
        if budget_grund:
            kette = [x for x in kette if x != "llamacpp"]
            if not kette:
                raise BudgetExhausted(budget_grund)
        t0 = time.time()
        gruende = [budget_grund] if budget_grund else []
        gefragt = False
        for backend in kette:
            # v5.9-W202: der Platz gilt NUR dem lokalen Modell — er schuetzt die
            # Kerne. Bis dahin wartete auch der Cloud-Aufruf darauf: war der
            # eine Platz belegt, kam /brain gar nicht erst bei der Cloud an.
            lokal = backend == "llamacpp"
            if lokal:
                kap = self.plaetze(messen=True)
                if not self._slot.erwerben(rang, warten_s, self._plaetze_fuer(rang, kap),
                                           max_wartend=WARTESCHLANGE_JE_PLATZ * kap):
                    with self._stats_lock:
                        self._stats["busy_denied"] += 1
                    gruende.append("alle %d Inferenz-Plaetze belegt%s" % (
                        kap, ", %.0f s gewartet" % warten_s if warten_s > 0 else ""))
                    continue
            gefragt = True
            try:
                text = self._call(backend, messages,
                                  timeout or _timeout_s(),
                                  max_tokens or _max_tokens())
                ms = self._erfolg_buchen(backend, t0)
                return {"ok": True, "text": text,
                        "backend": backend, "ms": ms}
            except Exception as e:
                fehler = f"{backend}: {type(e).__name__}: {e}"
                gruende.append(fehler)
                # v4.2-W110: war log.debug. Antwortet llama-server auf
                # /health, aber nicht auf den Chat (z. B. mit
                # --embeddings gestartet: nur Embeddings), ging JEDE
                # Anfrage still in die Cloud. Gemeldet wird ein WECHSEL
                # des Grundes — ein Dauerfehler steht so einmal im Log.
                if fehler != self._letzter_fehler.get(backend):
                    log.warning("LLM-Backend %s scheitert: %s — die Anfrage "
                                "geht an das naechste Backend der Kette.",
                                backend, e)
                self._letzter_fehler[backend] = fehler
            finally:
                if lokal:
                    self._slot.freigeben()
        if not gefragt and gruende:
            # Niemand wurde gefragt — Deckel oder Plaetze: das ist „gedeckelt",
            # nicht „kaputt" (BudgetExhausted, wie bisher).
            raise BudgetExhausted(" — ".join(gruende))
        with self._stats_lock:
            self._stats["errors"] += 1
        # Alle Gruende nennen: "Cloud scheiterte" allein verschwiege, dass
        # lokal gar nicht erst gefragt wurde (Deckel oder Plaetze).
        return {"ok": False, "error": " — ".join(gruende) or "kein Backend konfiguriert",
                "backend": None, "ms": round((time.time() - t0) * 1000, 1)}

    def _deckel_grund(self, rang: int):
        """Warum lokal NICHT gefragt wird (Stundendeckel oder Reserve) — None,
        wenn es gefragt werden darf. Ohne Deckel (Vorgabe seit W202) immer None."""
        b = self.budget()
        nebenbei = rang == RANG["nebenbei"]
        if not b["max_h"] or not (b["remaining"] <= 0
                                  or (nebenbei and b["remaining"] <= _reserve())):
            return None
        with self._stats_lock:
            self._stats["reserve_denied" if b["remaining"] > 0
                        else "budget_denied"] += 1
        if b["remaining"] <= 0:
            return f"LLM-Stundenbudget verbraucht ({b['used_h']}/{b['max_h']})"
        return (f"Reserve fuer Gespraeche ({b['remaining']} von {b['max_h']} "
                f"uebrig, BRAIN_LLM_RESERVE={_reserve()})")

    def _erfolg_buchen(self, backend: str, t0: float) -> float:
        """Zaehler, Budget (nur lokal) und Latenz einer gelungenen Antwort -> ms."""
        ms = round((time.time() - t0) * 1000, 1)
        with self._stats_lock:
            self._stats["ok"] += 1
            bb = self._stats["by_backend"]
            bb[backend] = bb.get(backend, 0) + 1
            if backend == "llamacpp":         # nur lokal ins Budget
                self._calls.append(time.time())
            # V37: Latenz-Historie für stats()/Metrik/Dashboard
            self._durs.append(ms)
            if len(self._durs) > 50:
                del self._durs[:25]
        self._letzter_fehler.pop(backend, None)   # wieder gesund
        return ms

    # ------------------------------------------------------------ Plaetze

    @staticmethod
    def _plaetze_fuer(rang: int, kap: int) -> int:
        """Eigeninitiative bekommt nie den LETZTEN freien Platz (ab zwei
        Plaetzen): sonst plaudert AZRAEL alle Plaetze voll, und wer ihn
        anspricht, wartet. Das ist die Reserve aus W196, eine Ebene tiefer —
        sie haengt nicht mehr an einem Stundendeckel, den es nicht mehr gibt."""
        return kap - 1 if (rang == RANG["nebenbei"] and kap > 1) else kap

    _PLAETZE_TTL = 60.0

    def plaetze(self, messen: bool = False) -> int:
        """Wie viele Inferenz-Plaetze gelten. BRAIN_LLM_PLAETZE=<n> erzwingt n,
        sonst zaehlt, was llama-server meldet (sein --parallel), sonst 1.

        messen=False misst nie (Anzeigen, /healthz); messen=True fragt den
        Server hoechstens alle 60 s."""
        roh = _plaetze_conf()
        if roh not in ("", "auto"):
            try:
                return max(1, min(MAX_PLAETZE, int(roh)))
            except ValueError:
                if roh != self._plaetze_fehler:
                    log.warning("BRAIN_LLM_PLAETZE=%r ist keine Zahl — es gilt auto "
                                "(so viele Plaetze, wie llama-server meldet).", roh)
                    self._plaetze_fehler = roh
        if messen and time.monotonic() - self._plaetze_t > self._PLAETZE_TTL:
            self._plaetze_t = time.monotonic()
            self._server_plaetze = self._plaetze_messen()
        n = self._server_plaetze
        return max(1, min(MAX_PLAETZE, n)) if n else 1

    def _plaetze_messen(self):
        """total_slots aus /props, ersatzweise die Laenge von /slots; None, wenn
        der Server keines davon sagt (dann gilt 1 — das sichere Mass)."""
        for pfad in ("/props", "/slots"):
            try:
                req = urllib.request.Request(f"{_llamacpp_url()}{pfad}", method="GET")
                with urllib.request.urlopen(req, timeout=3) as r:
                    j = json.loads(r.read(1 << 20).decode("utf-8", "replace"))
            except Exception as e:
                grund = f"{pfad}: {type(e).__name__}"
                if grund != self._plaetze_fehler:
                    log.info("llama-server: Zahl der Plaetze unter %s nicht lesbar (%s) — "
                             "es gilt 1, bis der Server sie nennt.", pfad, type(e).__name__)
                    self._plaetze_fehler = grund
                continue
            if pfad == "/props" and isinstance(j, dict) and isinstance(j.get("total_slots"), int):
                return j["total_slots"]
            if pfad == "/slots" and isinstance(j, list) and j:
                return len(j)
        return None

    _HEALTH_TTL = 15.0

    def health(self) -> dict:
        """Backends anpingen (für Dashboard). Zählt NICHT ins Budget.
        IMP-4: 15s-Cache — bei toten Backends kosten die Probes 2×3s
        Timeout; ungecached blockierte das bei jedem 10s-Dashboard-Poll
        einen Flask-Worker. Budget wird immer frisch berechnet."""
        now = time.time()
        cache = getattr(self, "_health_cache", None)
        if cache and now - cache[0] < self._HEALTH_TTL:
            out = dict(cache[1])
        else:
            out = {"llamacpp": self._probe("llamacpp")}
            if out["llamacpp"].get("up"):
                # v5.1-W181: welches Modell lokal antwortet — das Deck nannte
                # bisher nur "llama.cpp", und nach dem Umstieg auf Qwen3-14B
                # war nicht zu sehen, ob der neue Server oder ein alter laeuft.
                # models() ist 60 s gecacht und kostet bei laufendem Server
                # Millisekunden.
                mods = self.models()
                if mods:
                    out["llamacpp"]["modell"] = mods[0]
                # v5.9-W202: wie viele Antworten gleichzeitig gehen
                out["llamacpp"]["plaetze"] = self.plaetze(messen=True)
            # B120: Cloud-Reserve im Health sichtbar machen. Ohne den
            # Eintrag meldete das Dashboard 'offline', obwohl freeai
            # antwortet — der Operator suchte dann am falschen Ende.
            if "freeai" in self._chain():
                try:
                    from nc import freeai as _freeai
                    basen = _freeai.bases_status()
                    out["freeai"] = {"up": bool(_freeai.alive_sync(3.0)), "bases": basen}
                    # v5.9-W202: „UP" hiess nur, dass die Modellliste antwortet —
                    # beim Betreiber stand UP, und jede Antwort scheiterte mit
                    # auth. Tragen ALLE Basen einen Fehler (ein Erfolg loescht
                    # ihn), ist die Reserve gestoert; auth zuerst, weil ein
                    # Schluessel sie behebt.
                    fehler = [b["last_error"] for b in basen if b.get("last_error")]
                    if basen and len(fehler) == len(basen):
                        arten = [f.get("kind") for f in fehler]
                        art = "auth" if "auth" in arten else max(
                            fehler, key=lambda f: f.get("ts") or 0).get("kind")
                        out["freeai"]["gestoert"] = art
                        out["freeai"]["abhilfe"] = _freeai.abhilfe(art)
                except Exception as e:
                    out["freeai"] = {"up": False, "error": type(e).__name__}
            self._health_cache = (now, dict(out))
        out["backend_conf"] = _backend_conf()
        out["budget"] = self.budget()
        with self._stats_lock:                     # V37: Latenz für die Pill
            out["avg_ms"] = (round(sum(self._durs) / len(self._durs), 1)
                             if self._durs else None)
        return out

    def zuletzt_oben(self):
        """llama-server laut LETZTER Probe: True/False, None = nie gemessen.

        v4.2-W110. Misst NICHT — Anzeigen und /healthz duerfen fragen, ohne
        eine 3-s-Probe auszuloesen. Die Probe selbst laeuft in health()."""
        cache = getattr(self, "_health_cache", None)
        return bool((cache[1].get("llamacpp") or {}).get("up")) if cache else None

    def zuletzt_modell(self):
        """Modell des lokalen Servers laut LETZTER Probe, sonst None.

        v5.1-W181. Misst NICHT (wie zuletzt_oben): die KI-Konfiguration im
        Deck nennt damit "qwen3-14b-uncensored.q4_k_m" statt des Cloud-
        Modellnamens, ohne selbst eine Anfrage auszuloesen."""
        cache = getattr(self, "_health_cache", None)
        return ((cache[1].get("llamacpp") or {}).get("modell") or None) if cache else None

    _MODELS_TTL = 60.0

    def models(self) -> list:
        """Modelle des lokalen Servers (OpenAI-kompatibel: /v1/models).

        v4.2-W110: bot.py rief diese Methode seit V37 — es gab sie nicht. Der
        AttributeError wurde dort still gefangen, und die Modellliste im Deck
        zeigte nie das lokale Modell. 60 s gecacht: das Deck fragt im
        10-s-Takt, und ein toter Server kostete sonst jedes Mal 3 s.
        Leer heisst: kein lokaler Server (oder Backend aus) — der Aufrufer
        nimmt dann die Cloud-Liste."""
        now = time.time()
        cache = getattr(self, "_models_cache", None)
        if cache and now - cache[0] < self._MODELS_TTL:
            return list(cache[1])
        ids = []
        if "llamacpp" in self._chain():
            try:
                req = urllib.request.Request(f"{_llamacpp_url()}/v1/models",
                                             method="GET")
                with urllib.request.urlopen(req, timeout=3) as r:
                    j = json.loads(r.read().decode("utf-8", "replace"))
                ids = [m.get("id") for m in (j.get("data") or [])
                       if isinstance(m, dict) and m.get("id")]
            except Exception as e:
                fehler = f"{type(e).__name__}: {e}"
                if fehler != getattr(self, "_models_fehler", None):
                    # Nur ein WECHSEL meldet: das Deck fragt alle 60 s, ein
                    # dauerhaft abwesender Server waere sonst Rauschen.
                    log.warning("llama-server: Modellliste nicht lesbar (%s) "
                                "unter %s — laeuft `llama-server`?",
                                fehler, _llamacpp_url())
                self._models_fehler = fehler
            else:
                self._models_fehler = None
        self._models_cache = (now, list(ids))
        return ids

    def budget(self) -> dict:
        """used_h zaehlt immer; max_h 0 = kein Deckel, dann remaining None.

        None und nicht eine grosse Zahl: eine erfundene Restmenge saehe im
        Deck aus wie ein Deckel, den es nicht gibt."""
        cutoff = time.time() - 3600
        with self._stats_lock:
            self._calls = [t for t in self._calls if t > cutoff]
            used = len(self._calls)
        deckel = _max_calls_h()
        return {"used_h": used, "max_h": deckel,
                "remaining": max(deckel - used, 0) if deckel else None}

    def stats(self) -> dict:
        with self._stats_lock:
            pt = self._stats["prompt_token"]
            return dict(self._stats, budget=self.budget(),
                        avg_ms=(round(sum(self._durs) / len(self._durs), 1)
                                if self._durs else None),
                        last_ms=(self._durs[-1] if self._durs else None),
                        # v5.5-W196: was die letzte lokale Antwort gekostet hat
                        letzte_zeiten=dict(self._zeiten),
                        slot=dict(self._slot.lage(), plaetze=self.plaetze()),
                        cache_anteil=(round(self._stats["prompt_gecacht"] / pt, 3)
                                      if pt else None),
                        reserve=_reserve())

    # -------------------------------------------------------- Backends

    def _chain(self) -> list[str]:
        """B120: Kette statt Sackgasse.

        Vorher lieferte _chain() AUSSCHLIESSLICH ['llamacpp']. Lief der
        llama-server nicht (Standardfall auf der 8-Kern-Box, wenn kein
        GGUF geladen ist), gab chat() ok=False zurueck, der Router-Tier
        'llm' warf Unhandled — und /brain antwortete strukturell IMMER
        'keine Antwort'. Beim Ollama-Ausbau wurde der Cloud-Fallback
        vergessen; nc.freeai existiert, war hier aber nie verdrahtet.

        Reihenfolge bleibt lokal-zuerst: llama.cpp kostet nichts und
        verlaesst die Box nicht. 'freeai' greift nur, wenn lokal nichts
        antwortet. BRAIN_LLM_BACKEND=llamacpp erzwingt rein lokal."""
        conf = _backend_conf()
        if conf == "off":
            return []
        if conf == "llamacpp":
            return ["llamacpp"]          # bewusst ohne Cloud-Ausweg
        if conf == "freeai":
            return ["freeai"]
        return ["llamacpp", "freeai"]    # auto (Default) + unbekannte Werte

    def _call(self, backend: str, messages, timeout, max_tokens) -> str:
        if backend == "freeai":
            # Cloud-Reserve. Import LOKAL, damit brain/ dependency-frei
            # bleibt und ohne nc/ weiter importierbar ist (M1-Vertrag).
            from nc import freeai as _freeai
            txt, err = _freeai.chat_sync(messages, timeout=timeout)
            if not txt:
                # v5.9-W202: mit Abhilfe — „freeai: auth" allein stand beim
                # Betreiber auf der Brain-Seite und sagte nicht, was zu tun ist.
                hilfe = _freeai.abhilfe(err)
                raise RuntimeError(f"freeai: {err or 'leer'}" + (f" ({hilfe})" if hilfe else ""))
            return txt
        if backend == "llamacpp":
            # llama-server spricht die OpenAI-kompatible API — Vorteil:
            # jeder andere OpenAI-kompatible lokale Server (vllm, etc.)
            # funktioniert ohne Codeänderung über BRAIN_LLAMACPP_URL.
            # v5.5-W196 cache_prompt: llama-server haelt den KV-Cache des
            # letzten Prompts und liest nur den Teil neu ein, der sich
            # unterscheidet. Gemessen beim Betreiber: 7,8 Token/s beim
            # Einlesen — eine Persona von 600 Token kostete ohne das bei
            # JEDER Nachricht rund 80 s, bevor das erste Wort kam.
            body = {"messages": messages, "max_tokens": max_tokens,
                    "temperature": 0.3, "stream": False, "cache_prompt": True}
            if not _denken():
                # v5.1-W181: zwei Riegel gegen den Qwen3-Denkmodus. Der erste
                # wirkt ueber die Chat-Vorlage (ik_llama.cpp/llama.cpp mit
                # --jinja), der zweite ist Qwen3s eigener Schalter im Text —
                # er wirkt auch, wo die Vorlage den Parameter nicht kennt.
                body["chat_template_kwargs"] = {"enable_thinking": False}
                body["messages"] = _ohne_denken_bitten(messages)
            j = self._post(f"{_llamacpp_url()}/v1/chat/completions",
                           body, timeout)
            self._zeiten_merken(j)
            roh = j["choices"][0]["message"].get("content")
            text = ohne_denkblock(roh)
            if not text:
                # Nur Denken, keine Antwort (max_tokens im Denkblock
                # verbraucht): ein Fehler fuer die Kette, kein leerer Erfolg —
                # sonst ginge "" als Antwort an Telegram und an die TTS.
                raise RuntimeError("Antwort leer (nur Denkblock oder nichts) — "
                                   "BRAIN_LLM_MAX_TOKENS heben oder "
                                   "BRAIN_LLM_DENKEN=0 lassen")
            return text
        raise ValueError(f"unbekanntes Backend: {backend}")

    def _zeiten_merken(self, j: dict):
        """Die Messung, die llama-server jeder Antwort beilegt (`timings`),
        plus wie viele Prompt-Token aus dem Cache kamen. Ohne das waere die
        Frage „hilft der Prompt-Cache?" am Server nur von Hand zu beantworten.

        `usage.prompt_tokens` ist der ganze Prompt, `timings.prompt_n` der
        Teil, der wirklich eingelesen wurde — die Differenz kam aus dem Cache.
        Fehlt eines davon (anderer Server), bleibt `gecacht` None, nicht 0:
        eine 0 hiesse „Cache wirkt nicht", und das waere eine Behauptung."""
        t = j.get("timings") if isinstance(j.get("timings"), dict) else {}
        u = j.get("usage") if isinstance(j.get("usage"), dict) else {}
        gesamt, neu = u.get("prompt_tokens"), t.get("prompt_n")
        gecacht = (gesamt - neu) if isinstance(gesamt, int) and isinstance(neu, int) else None
        z = {"prompt_gesamt": gesamt, "prompt_neu": neu, "gecacht": gecacht,
             "einlesen_ms": t.get("prompt_ms"), "erzeugen_n": t.get("predicted_n"),
             "erzeugen_ms": t.get("predicted_ms"),
             "einlesen_tps": t.get("prompt_per_second"),
             "erzeugen_tps": t.get("predicted_per_second")}
        with self._stats_lock:
            self._zeiten = z
            if isinstance(gesamt, int) and isinstance(gecacht, int):
                self._stats["prompt_token"] += gesamt
                self._stats["prompt_gecacht"] += max(0, gecacht)

    def _probe(self, backend: str) -> dict:
        url = f"{_llamacpp_url()}/health"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3) as r:
                r.read(256)
            return {"up": True,
                    "ms": round((time.time() - t0) * 1000, 1)}
        except Exception as e:
            return {"up": False, "error": f"{type(e).__name__}"}

    @staticmethod
    def _post(url: str, body: dict, timeout: float) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            # B120: Body anhaengen. 'HTTPError: 400' allein sagt nicht,
            # ob das Modell fehlt oder der Prompt zu lang war.
            try:
                detail = e.read().decode("utf-8", "ignore")[:200]
            except Exception:
                detail = ""
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None

    # Budget: Pruefung steht seit v4.2-W177 in chat() vor dem llamacpp-Schritt.
