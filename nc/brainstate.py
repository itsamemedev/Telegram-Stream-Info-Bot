"""nc.brainstate — v4.1-W21: der Zustand hinter dem Brain-Panel.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die sechs Routen unter `/api/brain` lesen fünfzehn Modul-Globals des
Monolithen. Als nc.ctx-Einträge wären das fünfzehn der 25 vertraglichen
Plätze — bei 24 belegten schlicht nicht vorhanden.

Der Kontext ist auch hier der falsche Ort: das ist **geteilter Zustand**, den
Bot und Oberfläche gemeinsam sehen müssen, keine Fähigkeit, die nur der
Monolith hat. Dieselbe Unterscheidung wie in nc/azraelstate.py (W19).

Zwei Sorten, und der Unterschied entscheidet über Alias oder Register:

* **Aliase** sind alle Sammlungen und der Lock. bot.py verändert sie nur an
  Ort und Stelle (`.append`, `[k] = v`, `del hist[:-N]`), bindet sie nie neu.
* **STALLS ist ein Register**, weil `_LOOP_STALL_COUNT` eine ganze Zahl war
  und mit `+= 1` unter `global` hochgezählt wurde. Eine Zahl lässt sich nicht
  teilen — ein Alias wäre eine Kopie, die für immer auf 0 stehen bliebe, und
  `/api/brain/health` meldete "keine Stalls", während der Loop klemmt. Genau
  die stille Fehlanzeige, gegen die es die Zahl überhaupt gibt.

Die Ringpuffer sind bewusst begrenzt: das Panel pollt im Sekundentakt, und
ein unbegrenzter Verlauf wäre ein Speicherleck, das erst nach Tagen auffällt.
Gekappt wird beim Schreiben, nicht beim Lesen — sonst wächst die Liste
trotzdem und nur die Anzeige sieht harmlos aus.
"""

import threading
from datetime import datetime, timezone

# ---- Ringpuffer und Übergangs-Gedächtnis (Aliase) --------------------------

HISTORY = {}            # node_key -> list[int]  (Ring, letzte N activity-Werte)
HISTORY_MAX = 40
STREAM = []             # list[{ts, node, kind, text}]  (Ring)
STREAM_MAX = 50
LAST_STATUS = {}        # node_key -> letzter status (für Übergangs-Events)
LOCK = threading.Lock()

# Zustand der Brücke zum brain/-Kern. Der Bot trägt hier ein, was beim
# Hochfahren passiert ist; das Panel zeigt es an. Ohne diesen Zustand meldet
# ein nicht gestartetes Brain nur "keine Daten" statt des echten Grundes.
BRIDGE = {"ok": False, "phase": "not_started", "error": None}

# F49-B5: Sende-Bremse für den Dashboard-Chat (Schutz vor Browser-Bug/Spam).
AI_RATE = []            # monotonic-Zeitstempel der letzten Aufrufe
AI_LOCK = threading.Lock()

# ---- Register (Zahlen lassen sich nicht teilen) ----------------------------

# Erkannte Loop-Stalls seit Boot. Register und NICHT Alias: eine ganze Zahl
# ist unteilbar, ein Alias wäre eine Kopie auf 0 — siehe Modul-Kopf.
STALLS = {"n": 0}

# Der Proxy-Router. Register und nicht Alias, obwohl bot.py ihn nur einmal
# erzeugt: er entsteht erst weit unten in der Datei, waehrend frueherer Code
# ihn schon braucht. Im Monolithen stand dafuer
# `router_getter=lambda: globals().get("PROXY_ROUTER")` — in einem Blueprint
# waere globals() dessen eigener Namensraum und das Brain-Panel meldete den
# Proxy fuer immer als "idle".
PROXY = {"obj": None}


# ---- Wächter-Zustand des Check-Loops (Aliase) -------------------------------
# Beide gehören zum Gesundheitsbild, das /api/brain/health zeigt: wann der
# nächste Check ansteht und welche Trackings gerade in einer Rückfall-Sperre
# sitzen. Der Bot trägt ein und räumt auf, bindet aber keinen der beiden
# Namen neu — Aliase reichen.
NEXT_CHECK_AT = {}          # tracking_id -> monotonic-Zeitstempel
DEAD_BACKOFF_UNTIL = {}     # tracking_id -> monotonic ts, ab wann wieder erlaubt


def stall():
    """Einen erkannten Loop-Stall zählen. Gibt den neuen Stand zurück."""
    STALLS["n"] += 1
    return STALLS["n"]


def record(nodes: dict):
    """Schreibt aktuelle Activity-Werte in die Historie + erzeugt Stream-Events
       bei Status-Übergängen. Thread-safe, bounded."""
    nowiso = datetime.now(timezone.utc).isoformat()
    with LOCK:
        for key, n in nodes.items():
            hist = HISTORY.setdefault(key, [])
            hist.append(int(n.get("activity", 0)))
            if len(hist) > HISTORY_MAX:
                del hist[:-HISTORY_MAX]
            prev = LAST_STATUS.get(key)
            cur = n.get("status")
            if prev is not None and prev != cur:
                # Status-Übergang → Stream-Event
                kind = "error" if cur == "error" else (
                    "up" if cur in ("active", "working") else "down")
                STREAM.append({
                    "ts": nowiso, "node": n.get("label", key),
                    "kind": kind, "text": f"{n.get('label', key)}: {prev} → {cur}",
                })
                if len(STREAM) > STREAM_MAX:
                    del STREAM[:-STREAM_MAX]
            LAST_STATUS[key] = cur


def history_for(key):
    with LOCK:
        return list(HISTORY.get(key, []))


def stream_recent(limit=20):
    with LOCK:
        return list(reversed(STREAM[-limit:]))
