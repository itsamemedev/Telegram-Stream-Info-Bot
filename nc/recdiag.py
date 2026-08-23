"""nc.recdiag — warum enden Aufnahmen? Auswertung von recording_attempts.

Die Tabelle protokolliert seit jeher JEDEN Aufnahmeversuch mit Dauer,
Returncode, Outcome und den letzten 1500 Zeichen ffmpeg-stderr. Nur ausgewertet
hat das nie jemand — also wurde ueber Disconnect-Ursachen geraten, statt sie
abzulesen.

Dieses Modul beantwortet die Fragen, die zaehlen:
  - Welche Abbruchgruende dominieren, und bei WELCHEM User?
  - Wie lange haelt eine Aufnahme typischerweise?
  - Welche ffmpeg-Fehler stehen wirklich im stderr?

Braucht nur db_conn — keine Bot-Globals.
"""
import logging
import re
from collections import Counter
from dataclasses import dataclass

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")

# Outcome -> (Klartext, ist_das_ein_problem)
OUTCOMES = {
    "ok": ("sauber beendet", False),
    "early_disconnect": ("Abbruch in den ersten Sekunden", True),
    "stall_killed_partial": ("Watchdog hat einen haengenden ffmpeg gekillt", True),
    "resolve_failed": ("Stream-URL nicht aufloesbar", True),
    "start_failed": ("ffmpeg startete nicht", True),
    "post_spawn_fail": ("Fehler direkt nach dem Start", True),
    "offline_or_protected": ("User offline oder Stream geschuetzt", False),
    "hevc_unsupported": ("HEVC-Codec, nicht unterstuetzt", True),
}

# Signaturen, die im ffmpeg-stderr die ECHTE Ursache verraten.
# Reihenfolge zaehlt: die spezifischste zuerst.
STDERR_SIGNS = [
    (r"HTTP error 403", "403 Forbidden — TikTok blockt die IP (Datacenter/VPS) "
                        "oder die URL-Signatur passt nicht"),
    (r"HTTP error 404", "404 — Stream-URL abgelaufen oder Raum beendet"),
    (r"Connection timed out|Connection reset|Broken pipe",
     "Netzwerk-Abbruch zur CDN (Tunnel/Proxy instabil?)"),
    (r"Server returned 5\d\d", "CDN-Serverfehler (5xx)"),
    (r"Invalid data found|moov atom not found|Invalid NAL",
     "kaputter Stream-Bitstream von TikTok"),
    (r"No such file or directory", "Pfad-/Schreibfehler"),
    (r"Immediate exit requested|Exiting normally",
     "geplanter Stopp (SIGTERM — z.B. URL-Refresh)"),
    (r"non-monotonic|Non-monotonous|pts has no value",
     "Timestamp-Chaos im Quellstream"),
    (r"Protocol not found|Unknown protocol", "URL-Schema/Protokoll-Problem"),
    (r"Operation not permitted|Permission denied", "Rechteproblem"),
]


def _classify_stderr(text):
    """Erste passende Signatur — oder None."""
    if not text:
        return None
    for pat, meaning in STDERR_SIGNS:
        if re.search(pat, text, re.I):
            return meaning
    return None


def _rows(days, username=None, limit=4000):
    where = ["started_at >= datetime('now', ?)"]
    params = ["-%d days" % int(days)]
    if username:
        where.append("username = ?")
        params.append(username)
    sql = ("SELECT username, duration_secs, returncode, outcome, stderr_tail, "
           "started_at FROM recording_attempts WHERE " + " AND ".join(where)
           + " ORDER BY id DESC LIMIT %d" % int(limit))
    with db_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchall()
        except Exception:
            # MariaDB kennt datetime('now', ...) nicht — dort ohne Zeitfilter
            # und in Python schneiden waere teuer; stattdessen INTERVAL.
            sql2 = sql.replace("started_at >= datetime('now', ?)",
                               "started_at >= (NOW() - INTERVAL %d DAY)" % int(days))
            params2 = [p for p in params if not str(p).startswith("-")]
            cur.execute(sql2, params2)
            return cur.fetchall()


def _median(xs):
    if not xs:
        return 0
    s = sorted(xs)
    return s[len(s) // 2]


def disconnect_analysis(days=7, username=None):
    """Die Gesamtsicht: was bricht ab, wie oft, bei wem, und warum wirklich."""
    rows = _rows(days, username)
    total = len(rows)
    out = {"window_days": int(days), "total": total, "username": username,
           "by_outcome": [], "by_user": [], "stderr_causes": [],
           "duration": {}, "problem_share_pct": 0.0}
    if not total:
        return out

    oc = Counter()
    per_user = {}
    causes = Counter()
    durs = []
    short = 0

    for r in rows:
        o = (r["outcome"] or "unbekannt")
        oc[o] += 1
        u = r["username"] or "?"
        pu = per_user.setdefault(u, {"total": 0, "problems": 0, "durs": [],
                                     "outcomes": Counter()})
        pu["total"] += 1
        pu["outcomes"][o] += 1
        d = r["duration_secs"]
        if d is not None and d >= 0:
            durs.append(d)
            pu["durs"].append(d)
            if d < 60:
                short += 1
        _, is_problem = OUTCOMES.get(o, ("", True))
        if is_problem:
            pu["problems"] += 1
        c = _classify_stderr(r["stderr_tail"])
        if c:
            causes[c] += 1

    problems = sum(n for o, n in oc.items()
                   if OUTCOMES.get(o, ("", True))[1])
    out["problem_share_pct"] = round(problems * 100.0 / total, 1)
    out["by_outcome"] = [
        {"outcome": o, "n": n, "pct": round(n * 100.0 / total, 1),
         "meaning": OUTCOMES.get(o, ("unbekannter Outcome", True))[0],
         "problem": OUTCOMES.get(o, ("", True))[1]}
        for o, n in oc.most_common()]
    out["stderr_causes"] = [{"cause": c, "n": n} for c, n in causes.most_common(8)]
    out["duration"] = {
        "median_s": _median(durs), "shortest_s": min(durs) if durs else 0,
        "longest_s": max(durs) if durs else 0,
        "under_60s": short,
        "under_60s_pct": round(short * 100.0 / total, 1),
    }
    out["by_user"] = sorted(
        ({"username": u, "total": v["total"], "problems": v["problems"],
          "problem_pct": round(v["problems"] * 100.0 / max(1, v["total"]), 1),
          "median_s": _median(v["durs"]),
          "top_outcome": v["outcomes"].most_common(1)[0][0] if v["outcomes"] else "?"}
         for u, v in per_user.items()),
        key=lambda x: (-x["problems"], -x["total"]))[:15]
    return out


def url_refresh_stats(days=7):
    """Wie oft wird wegen URL-Ablauf planmaessig neu gestartet?

    Diese Restarts sind KEIN Fehler (die TikTok-URL traegt ein expire=-Token,
    ~30min TTL), aber jeder kostet eine Luecke in der Aufnahme. Die Zahl zeigt,
    wie viel eine Verkuerzung dieser Luecke ueberhaupt bringt.
    """
    rows = _rows(days)
    refresh = [r for r in rows
               if r["outcome"] == "ok" and r["duration_secs"]
               and 1500 <= (r["duration_secs"] or 0) <= 2100]
    return {"window_days": int(days),
            "likely_url_refresh_cuts": len(refresh),
            "median_segment_s": _median([r["duration_secs"] for r in refresh]),
            "note": "Segmente um ~25-35min sind typisch fuer den URL-Refresh-Schnitt"}


# ══════════════════════════════════════════════════════════════════════════
# v4.0-W116 · RATEN-EINBRUCH WAEHREND DER AUFNAHME
# ══════════════════════════════════════════════════════════════════════════
# Der Stillstands-Waechter in handle_recording_finished misst genau eine
# Sache: waechst die Datei? Das faengt den toten Stream — aber nicht den
# HALBTOTEN. Faellt bei einer TikTok-Uebertragung die Videospur weg und der
# Ton laeuft weiter, waechst die Datei munter im Kilobyte-Takt: der Waechter
# sieht Fortschritt, die Aufnahme laeuft stundenlang weiter, und am Ende
# liegt eine Datei mit Standbild auf der Platte. Dasselbe Bild bei einem
# Netz-Einbruch, bei dem die Quelle auf eine Notbitrate faellt.
#
# Erkennbar ist das an der RATE, nicht am Wachstum: die Datenrate bricht auf
# einen Bruchteil dessen ein, was dieselbe Aufnahme vorher hatte.
#
# WARUM DAS NUR MELDET UND NICHT ABBRICHT:
# Ein H.264-Stream mit -c copy gibt die Quelle 1:1 weiter, und eine wirklich
# statische Szene (Standbild-Intro, jemand haelt die Kamera auf eine Wand)
# druckt die Bitrate voellig legitim um mehr als 85 % nach unten. Eine
# Aufnahme deswegen abzubrechen wuerde echtes Material vernichten — und
# Material zurueckholen kann man nicht. Der Nullwachstums-Waechter darf
# killen, weil "0 Bytes in 45 Sekunden" keine harmlose Lesart hat; dieser
# hier darf es nicht. Er meldet, und der Betreiber entscheidet.


@dataclass(frozen=True)
class RateConfig:
    warmlauf_s: float = 60.0            # so lange nur Grundlinie sammeln
    einbruch_anteil: float = 0.15       # unter 15 % der Grundlinie = Einbruch
    einbruch_dauer_s: float = 90.0      # so lange muss er anhalten
    min_grundlinie_bps: float = 40000.0 # darunter ist keine Aussage moeglich


@dataclass
class RateSpur:
    """Verlauf EINER Aufnahme. Reine Rechnung: keine Uhr, keine Datei —
    der Aufrufer reicht Zuwachs und Zeitspanne herein."""
    grundlinie_bps: float = 0.0
    laufzeit_s: float = 0.0
    seit_einbruch_s: float = 0.0
    gemeldet: bool = False
    letzte_rate_bps: float = 0.0

    def beobachte(self, zuwachs_bytes: float, dt_s: float,
                  cfg: RateConfig | None = None):
        """Gibt "einbruch", "erholt" oder None zurueck — hoechstens einmal
        je Episode, damit der Aufrufer nicht drosseln muss."""
        cfg = cfg or RateConfig()
        if dt_s <= 0:
            return None
        rate = max(0.0, float(zuwachs_bytes)) / dt_s
        self.letzte_rate_bps = rate
        self.laufzeit_s += dt_s

        # Warmlauf: nur Grundlinie bilden, nie urteilen. Die ersten Sekunden
        # einer Aufnahme sind kein Massstab — Header, Probe, erster Keyframe.
        if self.laufzeit_s < cfg.warmlauf_s:
            self.grundlinie_bps = max(self.grundlinie_bps, rate)
            return None
        if self.grundlinie_bps < cfg.min_grundlinie_bps:
            self.grundlinie_bps = max(self.grundlinie_bps, rate)
            return None

        schwelle = self.grundlinie_bps * cfg.einbruch_anteil
        if rate >= schwelle:
            # Gesunde Messung: Grundlinie langsam nachfuehren. Nur hier —
            # waehrend eines Einbruchs mitzuziehen wuerde die Grundlinie
            # nach unten schleifen, und der Einbruch verschwaende von selbst.
            self.grundlinie_bps = 0.9 * self.grundlinie_bps + 0.1 * rate
            war = self.gemeldet
            self.seit_einbruch_s = 0.0
            self.gemeldet = False
            return "erholt" if war else None

        self.seit_einbruch_s += dt_s
        if self.seit_einbruch_s >= cfg.einbruch_dauer_s and not self.gemeldet:
            self.gemeldet = True
            return "einbruch"
        return None

    def bericht(self) -> str:
        """Eine Zeile fuer das Log — kbit/s statt Bytes, weil der Betreiber
        die Bitrate seiner Quelle in kbit/s kennt."""
        return ("%.0f kbit/s gegen %.0f kbit/s Grundlinie, seit %.0f s"
                % (self.letzte_rate_bps * 8 / 1000,
                   self.grundlinie_bps * 8 / 1000, self.seit_einbruch_s))
