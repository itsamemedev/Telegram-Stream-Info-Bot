"""nc.bandbreite — v4.1-W26: wie schnell wachsen die laufenden Aufnahmen.

Aus dem Monolithen geloest. Die Rechnung ist ein Vergleich zweier Messpunkte
derselben Datei; der Zustand dazu liegt hier, nicht im Blueprint — sonst
haette jede Route ihre eigene Messreihe und damit ihre eigene Wahrheit ueber
dieselbe Aufnahme.

SAMPLES raeumt am Ende jedes Durchlaufs auf: Messpunkte von Aufnahmen, die
nicht mehr laufen, fliegen raus. Das stand schon so im Monolithen und ist
mitgewandert — ohne diese vier Zeilen wuechse der Zustand mit jeder je
gestarteten Aufnahme.
"""

import os
import time

from nc.dbwrap import db_conn

# tracking_id -> [(monotonic_ts, file_size), ...]
SAMPLES = {}


def messen() -> list:
    """Pollt die file_size aller laufenden Aufnahmen, vergleicht mit
       vorigem Sample → berechnet B/s. Wird vom Dashboard alle paar
       Sekunden aufgerufen. State pro tracking_id."""
    out = []
    now = time.monotonic()
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, username, output_file, pid FROM trackings "
                "WHERE recording=1 AND output_file IS NOT NULL "
                "  AND output_file != ''"
            ).fetchall()
    except Exception:
        return []
    for r in rows:
        tid = r["id"]
        fp = r["output_file"]
        try:
            sz = os.path.getsize(fp) if os.path.exists(fp) else 0
        except OSError:
            sz = 0
        samples = SAMPLES.setdefault(tid, [])
        samples.append((now, sz))
        # Nur die letzten 10s behalten — für die Rate-Berechnung
        cutoff = now - 10
        samples[:] = [(t, s) for (t, s) in samples if t >= cutoff]
        rate_bps = 0
        if len(samples) >= 2:
            t0, s0 = samples[0]
            t1, s1 = samples[-1]
            dt = t1 - t0
            if dt > 0.5:
                rate_bps = max(0, (s1 - s0) / dt)
        out.append({
            "tracking_id": tid,
            "username": r["username"],
            "filename": os.path.basename(fp) if fp else "",
            "size_mb": round(sz / 1024 / 1024, 2),
            "rate_kbps": round(rate_bps * 8 / 1000, 1),    # kilobits/s
        })
    # Cleanup state für Trackings die nicht mehr aufnehmen
    active_tids = {r["id"] for r in rows}
    stale = [k for k in SAMPLES if k not in active_tids]
    for k in stale: SAMPLES.pop(k, None)
    return out
