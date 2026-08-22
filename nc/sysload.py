"""nc.sysload — v4.0-W30: reine Parser für den CPU/Speicher-Snapshot.

Aus _cpu_load_snapshot herausgelöst: das I/O (os.getloadavg, /proc/meminfo,
`ps`) bleibt im Bot, die reine Auswertung wandert hierher — Load-Klassifikation,
meminfo-Parsing samt Swap-Rechnung, ps-Tabelle mit Top-Verbrauchern und
ffmpeg-Zählung. Text/Zahlen rein, dict raus. Bitgenau gegen den Monolithen
geprüft.
"""


def classify_load(la1, la5, la15, cores):
    """Load-Mittel + Auslastung pro Kern + Zustand (ok/busy/overloaded)."""
    cores = cores or 1
    return {
        "avg": {"1m": round(la1, 2), "5m": round(la5, 2), "15m": round(la15, 2)},
        "per_core": round(la1 / cores, 2),
        "state": ("ok" if la1 < cores * 0.8 else
                  "busy" if la1 < cores * 1.5 else "overloaded"),
    }


def parse_meminfo(text):
    """/proc/meminfo-Text → Speicher/Swap-Kennzahlen (GB/MB/%)."""
    mem = {}
    for line in (text or "").splitlines():
        k, _, v = line.partition(":")
        if k in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
            mem[k] = int(v.split()[0]) * 1024
    st, sf = mem.get("SwapTotal", 0), mem.get("SwapFree", 0)
    return {
        "mem_total_gb": round(mem.get("MemTotal", 0) / 1e9, 1),
        "mem_available_gb": round(mem.get("MemAvailable", 0) / 1e9, 1),
        "swap_total_mb": round(st / 1e6),
        "swap_used_mb": round((st - sf) / 1e6),
        "swap_pct": round((st - sf) * 100.0 / st, 1) if st else 0.0,
    }


def parse_ps(stdout):
    """Ausgabe von `ps -eo comm,pid,pcpu,rss,nlwp --sort=-pcpu` → Top-Verbraucher
       (CPU > 1 %) + Anzahl/Threads der ffmpeg-Prozesse."""
    rows = []
    for line in (stdout or "").splitlines()[1:12]:
        p = line.split(None, 4)
        if len(p) < 5:
            continue
        try:
            rows.append({"comm": p[0], "pid": int(p[1]), "cpu": float(p[2]),
                         "rss_mb": round(int(p[3]) / 1024), "threads": int(p[4])})
        except ValueError:
            continue
    ff = [x for x in rows if x["comm"].startswith("ffmpeg")]
    return {
        "top": [x for x in rows if x["cpu"] > 1.0][:8],
        "ffmpeg_procs": len(ff),
        "ffmpeg_threads_total": sum(x["threads"] for x in ff),
    }
