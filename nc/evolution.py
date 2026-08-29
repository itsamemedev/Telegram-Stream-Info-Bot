"""nc.evolution — B167: Selbstanalyse-Kern (aus bot._evolution_analyze extrahiert).

Der KERN des Lern-/Evolutions-Subsystems: liest Betriebsdaten (recording_attempts,
learned_params …) und leitet Erkenntnisse + Vorschläge + gelernte Parameter ab.
Log-only, unkritisch — berührt keinen Aufnahme-/Restream-/Mod-Pfad.

Verbatim aus dem Monolithen gelöst: die Analyse-Logik ist UNVERÄNDERT; nur die
drei Bot-Abhängigkeiten (db_conn, _evolution_llm_note, EVOLUTION_WINDOW_DAYS)
werden als Parameter hereingereicht. _parse_iso kommt aus nc.textmore, die
Outcome-Mengen und der learned_params-Leser wandern mit hierher.
"""

import json
import os
from datetime import datetime, timedelta, timezone

from nc.dbwrap import db_conn
from nc.persona import _learn_param
from nc.textmore import _parse_iso  # bereits bot-freies nc/-Modul

# Outcomes die WEDER Erfolg NOCH Aufnahme-Fehler sind (nicht in den Nenner).
_EVO_NEUTRAL_OUTCOMES = ("running", "cancelled")
_EVO_SUCCESS_OUTCOMES = ("ok", "stall_killed_partial")


def _evo_prev_param(conn, key, default=None):
    row = conn.execute("SELECT v FROM learned_params WHERE k=?", (key,)).fetchone()
    if not row or row["v"] is None:
        return default
    try:
        return json.loads(row["v"])
    except Exception:
        return default


def analyze(*, db_conn, _evolution_llm_note, EVOLUTION_WINDOW_DAYS):
    """Der KERN des Lernens. Liest Betriebsdaten, baut Wissen auf und leitet
       Erkenntnisse + Vorschläge ab. Gibt dict(insights, proposals, learned).
       'learned' = {key: (value, confidence, samples, category)}."""
    insights = []
    proposals = []
    learned = {}
    with db_conn() as conn:
        # ---- Outcome-Verteilung ----
        # B67: Zwei Sichten — FENSTER (aktuelle Gesundheit) und ALL-TIME (Kontext).
        # Neutral (running/cancelled) zählt in KEINEN Nenner, da weder Erfolg noch
        # Aufnahme-Fehler. So spiegelt die Quote echte Aufnahme-Zuverlässigkeit.
        rows = conn.execute("SELECT outcome, COUNT(*) AS n FROM recording_attempts "
                            "GROUP BY outcome").fetchall()
        by_all = {(r["outcome"] or "?"): int(r["n"]) for r in rows}

        win_cut = (datetime.now(timezone.utc) - timedelta(days=EVOLUTION_WINDOW_DAYS)).isoformat()
        wrows = conn.execute("SELECT outcome, COUNT(*) AS n FROM recording_attempts "
                            "WHERE started_at >= ? GROUP BY outcome", (win_cut,)).fetchall()
        by = {(r["outcome"] or "?"): int(r["n"]) for r in wrows}
        if not by:                       # Fenster leer → all-time als Fallback
            by = by_all

        def _rate(counts):
            succ = sum(counts.get(k, 0) for k in _EVO_SUCCESS_OUTCOMES)
            neu = sum(counts.get(k, 0) for k in _EVO_NEUTRAL_OUTCOMES)
            denom = sum(counts.values()) - neu        # abgeschlossene Versuche
            return (round(100.0 * succ / denom, 1) if denom > 0 else 0.0, succ, denom)

        win_rate, win_ok, win_done = _rate(by)
        all_rate, all_ok, all_done = _rate(by_all)
        total = sum(by.values())            # Fenster-Versuche (inkl. neutral) für Konfidenz
        total_all = sum(by_all.values())
        conf_total = min(1.0, win_done / 40.0)
        learned["global.success_rate"] = (win_rate, conf_total, win_done, "reliability")
        learned["global.success_rate_alltime"] = (all_rate, min(1.0, all_done / 200.0),
                                                   all_done, "reliability")

        if total < 3:
            insights.append(f"Erst {total} Aufnahmeversuche im {EVOLUTION_WINDOW_DAYS}-Tage-"
                            f"Fenster — die KI sammelt noch Daten.")
        else:
            insights.append(
                f"Erfolgsquote (letzte {EVOLUTION_WINDOW_DAYS} Tage): {win_rate}% "
                f"über {win_done} abgeschlossene Versuche. "
                f"All-time {all_rate}% ({all_done} Versuche, inkl. Altlasten).")
            if total_all >= 100 and (win_rate - all_rate) >= 15:
                insights.append(f"Aktuelle Leistung deutlich besser als der All-time-Schnitt "
                                f"(+{round(win_rate-all_rate,1)} Punkte) — alte Fehlversuche "
                                f"ziehen nur die Lebenszeit-Zahl runter, nicht den Ist-Zustand.")

        # ---- Fehler-Aufschlüsselung (im Fenster; welche Kategorie dominiert?) ----
        if total >= 5:
            fails = {k: v for k, v in by.items()
                     if k not in _EVO_SUCCESS_OUTCOMES and k not in _EVO_NEUTRAL_OUTCOMES}
            fail_total = sum(fails.values())
            top_fails = sorted(fails.items(), key=lambda kv: kv[1], reverse=True)[:4]
            learned["outcomes.breakdown"] = (
                {k: round(100.0 * v / total, 1) for k, v in by.items()},
                conf_total, total, "reliability")
            if fail_total > 0 and top_fails:
                brk = ", ".join(f"{k} {round(100.0*v/win_done)}%" for k, v in top_fails) \
                    if win_done else ", ".join(f"{k} {v}×" for k, v in top_fails)
                insights.append(f"Fehler-Aufschlüsselung ({EVOLUTION_WINDOW_DAYS}d): {brk} "
                                f"(von {fail_total} Fehlversuchen).")
                dom_cat, dom_n = top_fails[0]
                dom_pct = round(100.0 * dom_n / fail_total)
                # Aktionable Diagnose je nach dominanter Fehlerkategorie
                _diag = {
                    "early_disconnect": ("CDN-/Netzwerk-Abbruch direkt nach Stream-Start. "
                                         "Meist Retry-Stürme auf nicht-aufnehmbaren Streamern; "
                                         "Cookies erneuern, Proxy testen, und chronische Versager "
                                         "pausieren (siehe unten) reduziert das drastisch."),
                    "forbidden_403":   ("403/Forbidden vom CDN — fast immer abgelaufene/fehlende "
                                        "Cookies. Im System-Tab frische TikTok-Cookies einspielen."),
                    "stream_dead":     ("Stream-URL liefert 404 — Auflösung/Resolver-Problem oder "
                                        "der Live war schon vorbei. URL-Refresh & Resolver prüfen."),
                    "codec_header_fail": ("ffmpeg konnte Codec-Parameter nicht lesen — Input-/"
                                          "Codec-Problem (oft HEVC-nah). Selten bei PREFER_H264; "
                                          "wenn gehäuft, ffmpeg-Upgrade ≥7.x erwägen."),
                    "hevc_unsupported": ("HEVC/bytevc1 — ffmpeg <7.x kann das nicht demuxen. "
                                         "PREFER_H264 prüfen bzw. ffmpeg ≥7.x."),
                    "offline_or_protected": ("Stream war offline/geschützt beim Aufnahmeversuch — "
                                             "oft Live-Detection-Timing; weniger kritisch."),
                    "stall_killed":    ("Watchdog killte hängende Aufnahme ohne Daten — meist "
                                        "abgelaufene Stream-URL; URL-Refresh-Margin prüfen."),
                }.get(dom_cat)
                if _diag:
                    proposals.append({
                        "category": "diagnosis",
                        "title": f"Hauptfehler: {dom_cat} ({dom_pct}% aller Fehlversuche)",
                        "rationale": (f"{dom_n} von {fail_total} Fehlversuchen (letzte "
                                      f"{EVOLUTION_WINDOW_DAYS}d) sind '{dom_cat}'. " + _diag),
                        "confidence": round(conf_total, 2),
                        "impact": "Zuverlässigkeit",
                    })

        # ---- Codec / HEVC ----
        hevc = by.get("hevc_unsupported", 0)
        hevc_rate = round(100.0 * hevc / total, 1) if total else 0.0
        if total >= 5:
            learned["codec.hevc_failure_rate"] = (hevc_rate, conf_total, total, "codec")
            if hevc_rate >= 5:
                insights.append(f"HEVC-Codec-Fehler bei {hevc_rate}% der Versuche — "
                                f"H.264-Bevorzugung ist gerechtfertigt.")
                proposals.append({
                    "category": "codec",
                    "title": f"HEVC-Fehlerrate {hevc_rate}% — ffmpeg-Upgrade erwägen",
                    "rationale": (f"{hevc} von {total} Versuchen scheiterten an HEVC/bytevc1 "
                                  f"(FLV codec-id 12). PREFER_H264 fängt das ab (niedrigere "
                                  f"Auflösung). Für volle origin-Qualität ffmpeg ≥7.x "
                                  f"installieren und dann PREFER_H264=0 setzen."),
                    "confidence": round(conf_total, 2),
                    "impact": "Qualität",
                })
            else:
                insights.append(f"HEVC-Fehler niedrig ({hevc_rate}%) — Codec-Strategie greift.")
                learned["codec.prefer_h264.confirmed"] = (True, conf_total, total, "codec")

        # ---- Verbindungs-/403-Abbrüche ----
        disc = by.get("early_disconnect", 0) + by.get("forbidden_403", 0)
        disc_rate = round(100.0 * disc / total, 1) if total else 0.0
        if total >= 5 and disc_rate >= 25:
            insights.append(f"{disc_rate}% früh abgebrochen/403 — evtl. Cookies veraltet "
                            f"oder Proxy nötig.")
            proposals.append({
                "category": "connectivity",
                "title": f"Hohe Abbruchrate ({disc_rate}%) — Cookies/Proxy prüfen",
                "rationale": (f"{disc} Versuche endeten mit early_disconnect/403. Häufigste "
                              f"Ursachen: abgelaufene Cookies (im System-Tab aktualisieren) "
                              f"oder fehlende Proxy-Rotation bei Geo-/Rate-Limits."),
                "confidence": round(conf_total, 2),
                "impact": "Zuverlässigkeit",
            })

        # ---- Trend: jüngste 7 Tage vs. davor ----
        try:
            now = datetime.now(timezone.utc)
            cutoff = (now - timedelta(days=7)).isoformat()
            recent = conn.execute(
                "SELECT COUNT(*) AS t, SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS o "
                "FROM recording_attempts WHERE started_at >= ?", (cutoff,)).fetchone()
            older = conn.execute(
                "SELECT COUNT(*) AS t, SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS o "
                "FROM recording_attempts WHERE started_at < ?", (cutoff,)).fetchone()
            rt, ro = int(recent["t"] or 0), int(recent["o"] or 0)
            ot, oo = int(older["t"] or 0), int(older["o"] or 0)
            if rt >= 3 and ot >= 3:
                r_rate = 100.0 * ro / rt
                o_rate = 100.0 * oo / ot
                delta = round(r_rate - o_rate, 1)
                learned["global.trend_delta"] = (delta, min(1.0, (rt + ot) / 40.0), rt + ot, "trend")
                if delta >= 5:
                    insights.append(f"Trend positiv: Erfolgsquote zuletzt +{delta} Punkte.")
                elif delta <= -5:
                    insights.append(f"Trend negativ: Erfolgsquote zuletzt {delta} Punkte — Regression.")
                    proposals.append({
                        "category": "trend",
                        "title": f"Verschlechterung {delta} Punkte in 7 Tagen",
                        "rationale": ("Die Erfolgsquote ist gegenüber dem Vorzeitraum gefallen. "
                                      "Logs der letzten Tage prüfen (Log-Tail im Lab-Tab) und "
                                      "Codec/Cookies/Proxy gegenchecken."),
                        "confidence": round(min(1.0, (rt + ot) / 40.0), 2),
                        "impact": "Zuverlässigkeit",
                    })
        except Exception:
            pass

        # ---- Chronisch scheiternde Streamer ----
        try:
            worst = conn.execute(
                "SELECT username, COUNT(*) AS t, SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS o "
                "FROM recording_attempts WHERE started_at >= ? "
                "GROUP BY username HAVING COUNT(*) >= 4", (win_cut,)).fetchall()
            bad = []
            for w in worst:
                t, o = int(w["t"]), int(w["o"] or 0)
                rate = 100.0 * o / t
                if rate < 20:
                    # Dominanten Fehlergrund dieses Streamers ermitteln (im Fenster)
                    dr = conn.execute(
                        "SELECT outcome, COUNT(*) AS n FROM recording_attempts "
                        "WHERE username=? AND started_at >= ? "
                        "AND outcome NOT IN ('ok','stall_killed_partial','running','cancelled') "
                        "GROUP BY outcome ORDER BY n DESC LIMIT 1", (w["username"], win_cut)).fetchone()
                    reason = dr["outcome"] if dr else "?"
                    bad.append((w["username"], round(rate, 0), t, reason))
            if bad:
                names = ", ".join(f"@{u}" for u, _, _, _ in bad[:5])
                insights.append(f"{len(bad)} chronisch scheiternde Streamer: {names}.")
                proposals.append({
                    "category": "reliability",
                    "title": f"{len(bad)} Streamer scheitern >80% — prüfen oder pausieren",
                    "rationale": ("Diese Konten liefern fast nur fehlgeschlagene Aufnahmen — "
                                  "mit Hauptfehler je Streamer (Retries blähen die Gesamt-"
                                  "Erfolgsquote auf): " + "; ".join(
                                      f"@{u} {r:.0f}% ok / {t}× / {reason}"
                                      for u, r, t, reason in bad[:8])),
                    "confidence": 0.7,
                    "impact": "Ressourcen",
                })
                learned["reliability.chronic_failers"] = (
                    [{"user": u, "ok_rate": r, "attempts": t, "main_error": reason}
                     for u, r, t, reason in bad],
                    0.7, len(bad), "reliability")
        except Exception:
            pass

        # ---- Speicher-Trend (cross-cycle gelernt) ----
        try:
            srow = conn.execute("SELECT SUM(file_size) AS b FROM recordings "
                               "WHERE deleted_at IS NULL").fetchone()
            cur_gb = round((srow["b"] or 0) / 1024 / 1024 / 1024, 2)
            prev = _evo_prev_param(conn, "storage.total_gb")
            learned["storage.total_gb"] = (cur_gb, 1.0, 1, "storage")
            if isinstance(prev, (int, float)) and cur_gb - prev >= 1.0:
                growth = round(cur_gb - prev, 2)
                insights.append(f"Speicher seit letztem Zyklus +{growth} GB (jetzt {cur_gb} GB).")
                if cur_gb >= 50:
                    proposals.append({
                        "category": "storage",
                        "title": f"Speicher wächst (+{growth} GB/Zyklus) — Retention setzen",
                        "rationale": (f"Aktuell {cur_gb} GB belegt und steigend. Eine Aufbewahrungs-"
                                      f"Regel (RECORDINGS_RETAIN_DAYS) oder Auto-Archiv-Regeln "
                                      f"verhindern ein Volllaufen der Platte."),
                        "confidence": 0.8,
                        "impact": "Speicher",
                    })
        except Exception:
            pass

        # ---- Beste Aufnahmezeit — Top-5 aktivste Streamer (nicht nur Nr. 1) ----
        try:
            top_rows = conn.execute(
                "SELECT username, COUNT(*) AS n FROM recording_attempts "
                "WHERE outcome='ok' GROUP BY username ORDER BY n DESC LIMIT 5").fetchall()
            for top in top_rows:
                if not top or int(top["n"]) < 4:
                    continue
                u = top["username"]
                hrows = conn.execute(
                    "SELECT started_at FROM recording_attempts WHERE username=? AND outcome='ok'",
                    (u,)).fetchall()
                buckets = [0] * 24
                for hr in hrows:
                    dt = _parse_iso(hr["started_at"])
                    if dt:
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        buckets[dt.hour] += 1
                best_h = max(range(24), key=lambda h: buckets[h])
                conf = min(1.0, int(top["n"]) / 20.0)
                learned[f"timing.best_hour.{u}"] = (best_h, conf, int(top["n"]), "timing")
            if top_rows:
                u = top_rows[0]["username"]
                bh = learned.get(f"timing.best_hour.{u}", (None,))[0]
                if bh is not None:
                    insights.append(f"Aktivster Streamer @{u} ist am häufigsten gegen "
                                    f"{bh:02d}:00 Uhr live.")
        except Exception:
            pass

        # ---- Resolver-Performance tracken (neu: lernt welcher Resolver am besten klappt) ----
        try:
            # log_event speichert 'via' im detail JSON bei jedem erfolgreichen Resolve
            via_rows = conn.execute(
                "SELECT detail FROM event_log WHERE kind='stream.resolve.ok' "
                "AND ts >= ? LIMIT 200", (win_cut,)).fetchall()
            via_counts: dict = {}
            for row in via_rows:
                try:
                    d = json.loads(row["detail"] or "{}")
                    via = d.get("via") or "unknown"
                    via_counts[via] = via_counts.get(via, 0) + 1
                except Exception:
                    pass
            if via_counts:
                total_via = sum(via_counts.values())
                best_via = max(via_counts, key=via_counts.get)
                learned["resolver.best_path"] = (
                    best_via, min(1.0, total_via / 30.0), total_via, "resolver")
                if total_via >= 10:
                    breakdown = ", ".join(
                        f"{v}:{round(100*c/total_via)}%"
                        for v, c in sorted(via_counts.items(), key=lambda x: -x[1]))
                    insights.append(f"Resolver-Wege ({total_via} Resolves): {breakdown}.")
                    if best_via.startswith("html_") and via_counts.get(best_via, 0) / total_via > 0.5:
                        proposals.append({
                            "category": "resolver",
                            "title": f"HTML-Fallback dominiert ({best_via}) — API-Probleme?",
                            "rationale": ("Mehr als 50% aller Resolves laufen über den langsamen "
                                          "HTML-Scraping-Pfad. Das deutet auf API-Blockierung hin. "
                                          "Cookies prüfen, ggf. frischer UA oder Proxy-Pool nötig."),
                            "confidence": min(1.0, total_via / 30.0),
                            "impact": "Latenz",
                        })
        except Exception:
            pass

    return {"insights": insights, "proposals": proposals, "learned": learned}


# ---------------------------------------------------------------------------
# v4.1-W3: der GANZE Evolution-Core, nicht mehr nur die Analyse.
#
# Bis hierher stand nur analyze() ausserhalb des Monolithen; Versionszaehler,
# build/-Schreiber, LLM-Notiz und der Zyklus selbst blieben in bot.py — und
# damit auch die acht /api/evolution-Routen, die sie brauchen. Erst der Kern,
# dann die Routen (die Reihenfolge aus W117): so kostet das Blueprint
# nc/routes/evolution.py KEINEN einzigen neuen nc.ctx-Slot.
#
# Die Koerper sind woertlich aus bot.py uebernommen. Ersetzt wurden nur die
# Namen, die im Monolithen Modul-Globals waren; sie kommen jetzt aus _conf.
# ---------------------------------------------------------------------------

_EVOLUTION_VERSION_TAG = "v37"


class _Conf(dict):
    """Wirft laut statt einen KeyError zu liefern.

    Ein fehlender Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler
    der Route — und er soll den Namen nennen, der fehlt, statt als nackter
    KeyError im naechsten except-Block zu verschwinden.
    """

    def __missing__(self, key):
        raise RuntimeError(
            "nc.evolution ist nicht konfiguriert (%r fehlt) — "
            "nc.evolution.configure(...) fehlt im Startpfad von bot.py" % key)


_conf = _Conf()


class _LazyLog:
    """Der Logger des Bots, erst beim Zugriff geholt.

    Als Modul-Konstante waere er beim Import None: nc.evolution wird bei den
    ersten Imports geladen, configure() laeuft erst am Dateiende von bot.py.
    """

    def __getattr__(self, name):
        return getattr(_conf["log"], name)


log = _LazyLog()


def configure(*, log, log_event, llm_chat_sync, bot_file, db_path,
              enabled, interval_hours, use_llm, window_days):
    """Vom Bot genau einmal beim Start gerufen.

    bot_file ist bewusst ein Parameter und kein __file__: der Snapshot-Schreiber
    in write_build() sichert die QUELLE DES BOTS. Innerhalb dieses Moduls waere
    __file__ nc/evolution.py — build/bot_v{N}.py haette ab dem Umzug still das
    falsche, 330 Zeilen kurze File enthalten, und niemand haette es gemerkt,
    weil der ganze Snapshot-Pfad in einem `except: pass` haengt.
    """
    _conf.update(log=log, log_event=log_event, llm_chat_sync=llm_chat_sync,
                 bot_file=bot_file, db_path=db_path, enabled=bool(enabled),
                 interval_hours=interval_hours, use_llm=use_llm,
                 window_days=window_days)


def conf():
    """Die .env-Startwerte des Cores — fuer die Anzeige-Routen.

    Als Funktion, nicht als Modul-Konstante: gefuellt wird erst beim Start.
    """
    return {"enabled": _conf["enabled"], "interval_hours": _conf["interval_hours"],
            "use_llm": _conf["use_llm"], "window_days": _conf["window_days"]}


def build_dir():
    """Pfad zum build/-Ordner (neben der DB / im Bot-Verzeichnis)."""
    override = os.getenv("BUILD_DIR")
    if override:
        return override
    base = os.path.dirname(os.path.abspath(_conf["db_path"])) or "."
    return os.path.join(base, "build")


def next_version():
    """Aktuelle Evolutions-Version (Anzahl bisheriger Zyklen + 1)."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT MAX(version) AS m FROM evolution_log").fetchone()
        return int((row["m"] or 0)) + 1
    except Exception:
        return 1


def engineering_note(insights, proposals):
    """Optional: lokales LLM (Ollama) für eine Klartext-Engineering-Notiz.
       Gibt Text oder None (graceful wenn Ollama offline / deaktiviert)."""
    if not _conf["use_llm"]:
        return None
    try:
        sys_p = ("Du bist ein Senior-Engineer der einen TikTok-Live-Recording-Bot betreut. "
                 "Fasse die folgenden automatisch erkannten Erkenntnisse in 2-4 knappen "
                 "Sätzen zusammen und nenne die EINE wichtigste nächste Maßnahme. Deutsch, "
                 "technisch-präzise, keine Floskeln.")
        body = "ERKENNTNISSE:\n" + "\n".join(f"- {i}" for i in insights[:12])
        if proposals:
            body += "\n\nVORSCHLÄGE:\n" + "\n".join(f"- {p['title']}" for p in proposals[:8])
        text, err = _conf["llm_chat_sync"](
            [{"role": "system", "content": sys_p},
             {"role": "user", "content": body}],
            timeout=30)
        return text if text and not err else None
    except Exception as e:
        log.debug(f"evolution LLM note failed: {e}")
        return None


def write_build(version, summary, insights, proposals, learned, llm_note):
    """Schreibt die Weiterentwicklung in den build/-Ordner: README.md (überschrieben),
       CHANGELOG.md (neueste Version oben), proposals/vN.md, learned_state.json.
       Gibt die Anzahl geschriebener Dateien zurück."""
    bdir = build_dir()
    pdir = os.path.join(bdir, "proposals")
    os.makedirs(pdir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    files = 0

    def _fmt_props(props):
        if not props:
            return "_Keine offenen Vorschläge in diesem Zyklus._\n"
        out = ""
        for p in props:
            out += (f"- **{p['title']}**  \n"
                    f"  _Kategorie:_ {p['category']} · _Impact:_ {p.get('impact','—')} · "
                    f"_Konfidenz:_ {int(p.get('confidence',0)*100)}%  \n"
                    f"  {p['rationale']}\n")
        return out

    # README.md
    learned_lines = ""
    for k, tup in sorted(learned.items()):
        val = tup[0] if isinstance(tup, (list, tuple)) else tup
        conf = int((tup[1] if isinstance(tup, (list, tuple)) and len(tup) > 1 else 0) * 100)
        learned_lines += f"- `{k}` = {val}  _(Konfidenz {conf}%)_\n"
    readme = f"""# 🧬 Self-Learning Evolution Core — build/

Dieser Ordner wird **automatisch** vom Evolution Core des TikTok-Bots erzeugt
und gepflegt. Die KI lernt kontinuierlich aus den Betriebsdaten des Bots und
legt hier ihre Erkenntnisse und Weiterentwicklungs-Vorschläge ab.

- **Aktuelle Version:** v{version}
- **Letzter Lern-Zyklus:** {ts}
- **Modell-Tag:** {_EVOLUTION_VERSION_TAG}

## Wie es funktioniert
1. Alle {_conf["interval_hours"]}h (oder manuell) analysiert die KI Aufnahme-
   Outcomes, Codec-Fehler, Zuverlässigkeit pro Streamer, Trends und Speicher.
2. Sie baut **versioniertes Wissen** auf (`learned_state.json`, mit Konfidenz).
3. Sie generiert **datengestützte Vorschläge** (`proposals/`), priorisiert nach
   Impact und Konfidenz.
4. Jeder Zyklus wird in `CHANGELOG.md` dokumentiert.

> ⚠️ **Sicherheit:** Die KI deployt **keinen** Code eigenmächtig in den laufenden
> Bot. Sie justiert nur risikofreies Wissen automatisch und legt Code-/Config-
> Änderungen als **prüfbare Vorschläge** hier ab. Anwenden entscheidet ein Mensch.

## Letzte Zusammenfassung
{summary}

{("### 🧠 Engineering-Notiz (LLM)\n" + llm_note + "\n") if llm_note else ""}
## Aktueller Wissensstand
{learned_lines or "_noch kein Wissen gelernt_"}

## Offene Vorschläge (v{version})
{_fmt_props(proposals)}
---
_Automatisch generiert — nicht manuell editieren, wird beim nächsten Zyklus überschrieben._
"""
    with open(os.path.join(bdir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    files += 1

    # proposals/vN.md
    pmd = f"""# Vorschläge — Evolution v{version}
_{ts}_

## Zusammenfassung
{summary}

## Erkenntnisse
{chr(10).join('- ' + i for i in insights) or '- keine'}

## Vorschläge
{_fmt_props(proposals)}
"""
    with open(os.path.join(pdir, f"v{version}.md"), "w", encoding="utf-8") as f:
        f.write(pmd)
    files += 1

    # CHANGELOG.md (neueste Version oben)
    header = ("# Changelog — Evolution Core\n\n"
              "Automatisch generiert. Jeder Eintrag = ein Lern-Zyklus.\n\n")
    entry = (f"## v{version} — {ts}\n\n"
             f"{summary}\n\n"
             f"**Erkenntnisse:** {len(insights)} · **Vorschläge:** {len(proposals)}\n\n"
             + "".join(f"- {i}\n" for i in insights)
             + ("\n**Neue Vorschläge:**\n" + "".join(f"- {p['title']}\n" for p in proposals)
                if proposals else "")
             + "\n")
    chpath = os.path.join(bdir, "CHANGELOG.md")
    old_body = ""
    if os.path.exists(chpath):
        try:
            with open(chpath, "r", encoding="utf-8") as f:
                content = f.read()
            idx = content.find("## v")
            old_body = content[idx:] if idx != -1 else ""
        except Exception:
            old_body = ""
    with open(chpath, "w", encoding="utf-8") as f:
        f.write(header + entry + old_body)
    files += 1

    # learned_state.json
    try:
        dump = {k: {"value": (t[0] if isinstance(t, (list, tuple)) else t),
                    "confidence": (t[1] if isinstance(t, (list, tuple)) and len(t) > 1 else None),
                    "samples": (t[2] if isinstance(t, (list, tuple)) and len(t) > 2 else None),
                    "category": (t[3] if isinstance(t, (list, tuple)) and len(t) > 3 else None)}
                for k, t in learned.items()}
        with open(os.path.join(bdir, "learned_state.json"), "w", encoding="utf-8") as f:
            json.dump({"version": version, "generated": ts, "params": dump}, f,
                      ensure_ascii=False, indent=2)
        files += 1
    except Exception:
        pass

    # Self-Reproduction: versionierten Snapshot der eigenen Quelldatei schreiben.
    # BUG-FIX (Trim): Vorher wurde find(_HEADER_MARK_E) genutzt — trifft den Marker
    # im Header (erste Fundstelle), aber _HEADER_MARK_E erscheint auch als String-Literal
    # im Funktionskörper selbst. rfind() findet den letzten Treffer und landet damit
    # immer korrekt am Ende des Headers, nie mittendrin im Code.
    _HEADER_MARK_S = "# [EVOLUTION SNAPSHOT"
    _HEADER_MARK_E = "# [END EVOLUTION SNAPSHOT]"
    try:
        bdir = build_dir()
        with open(_conf["bot_file"], "r", encoding="utf-8") as _src:
            src_lines = _src.read()

        # BUG-FIX: Vorher griff der Trim, sobald die Marker IRGENDWO im File
        # vorkamen — aber _HEADER_MARK_S/_E stehen als String-Literale in genau
        # dieser Funktion (snap_header-Template). __file__ (die laufende Quelle)
        # hat NIE einen echten Header oben; trotzdem fand rfind/find den Literal
        # bei ~Z.16279 und schnitt ~80% der Datei weg → bot_v{N}.py war
        # abgeschnitten + nicht lauffähig (SyntaxError, mitten im String-Literal).
        # Korrekt: nur trimmen wenn die Datei WIRKLICH mit einem Header BEGINNT
        # (der wird immer oben angefügt). Dann ist der ERSTE End-Marker (find)
        # das Header-Ende. Pristine Quelle → startswith False → kein Trim → volle
        # Datei wird sauber gesnapshottet.
        if src_lines.lstrip().startswith(_HEADER_MARK_S):
            e = src_lines.find(_HEADER_MARK_E)
            if e != -1:
                src_lines = src_lines[e + len(_HEADER_MARK_E):].lstrip("\n")

        # Erkenntnisse als Kommentar-Zeilen
        if insights:
            ins_text = "".join(
                "#   %02d. %s\n" % (i + 1, line)
                for i, line in enumerate(insights)
            )
        else:
            ins_text = "#   (keine Erkenntnisse in diesem Zyklus)\n"

        # Vorschlaege als Kommentar-Zeilen
        if proposals:
            prop_lines = []
            for i, p in enumerate(proposals):
                title    = p.get("title", "?")
                cat      = p.get("category", "")
                impact   = p.get("impact", "")
                conf_pct = int(p.get("confidence", 0) * 100)
                rat      = p.get("rationale", "")
                prop_lines.append(
                    "#   %02d. [%s] %s\n"
                    "#       Impact: %s  Konfidenz: %d%%\n"
                    "#       %s\n" % (i + 1, cat, title, impact, conf_pct, rat)
                )
            prop_text = "".join(prop_lines)
        else:
            prop_text = "#   (keine Vorschlaege in diesem Zyklus)\n"

        # Gelerntes Wissen als Kommentar-Zeilen
        if learned:
            learn_lines = []
            for k, tup in sorted(learned.items()):
                val  = tup[0] if isinstance(tup, (list, tuple)) else tup
                conf = int(
                    (tup[1] if isinstance(tup, (list, tuple)) and len(tup) > 1 else 0) * 100
                )
                learn_lines.append("#   %s = %s  (Konfidenz %d%%)\n" % (k, val, conf))
            learn_text = "".join(learn_lines)
        else:
            learn_text = "#   (kein Wissen in diesem Zyklus)\n"

        snap_header = (
            "# [EVOLUTION SNAPSHOT v%d]\n"
            "# Erzeugt:     %s\n"
            "# Zusammenfassung: %s\n"
            "#\n"
            "# ERKENNTNISSE (%d)\n"
            "%s"
            "#\n"
            "# VORSCHLAEGE (%d)\n"
            "%s"
            "#\n"
            "# GELERNTES WISSEN\n"
            "%s"
            "# [END EVOLUTION SNAPSHOT]\n"
            "\n"
        ) % (version, ts, summary,
             len(insights), ins_text,
             len(proposals), prop_text,
             learn_text)

        snapshot_src  = snap_header + src_lines
        snapshot_name = "bot_v%d.py" % version
        latest_name   = "bot_latest.py"

        with open(os.path.join(bdir, snapshot_name), "w", encoding="utf-8") as _out:
            _out.write(snapshot_src)
        with open(os.path.join(bdir, latest_name), "w", encoding="utf-8") as _out:
            _out.write(snapshot_src)
        files += 2

        # Manifest (snapshots.json)
        manifest_path = os.path.join(bdir, "snapshots.json")
        try:
            with open(manifest_path, "r", encoding="utf-8") as mf:
                manifest = json.load(mf)
        except Exception:
            manifest = []
        manifest.insert(0, {
            "version":   version,
            "ts":        ts,
            "file":      snapshot_name,
            "size_kb":   round(len(snapshot_src.encode("utf-8")) / 1024, 1),
            "insights":  len(insights),
            "proposals": len(proposals),
            "learned":   len(learned),
            "summary":   summary,
        })
        manifest = manifest[:20]
        with open(manifest_path, "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, ensure_ascii=False, indent=2)

    except Exception:
        pass   # Self-Repro optional — kein Crash wenn Permissions fehlen

    return files


def cycle(trigger="auto"):
    """Ein kompletter Lern-Zyklus (SYNC — wird von der Loop via to_thread und vom
       Flask-Thread aufgerufen). Analysiert, lernt, schreibt build/, loggt.
       Gibt ein Summary-dict zurück."""
    version = next_version()
    result = analyze(db_conn=db_conn, _evolution_llm_note=engineering_note,
                     EVOLUTION_WINDOW_DAYS=_conf["window_days"])
    insights = result["insights"]
    proposals = result["proposals"]
    learned = result["learned"]

    # Wissen persistieren
    try:
        with db_conn() as conn:
            for k, tup in learned.items():
                if isinstance(tup, (list, tuple)):
                    val, conf, samples, cat = (tup + (0, 0, "general"))[:4]
                else:
                    val, conf, samples, cat = tup, 0.5, 0, "general"
                _learn_param(conn, k, val, conf, samples, cat)
            conn.commit()
    except Exception as e:
        log.warning(f"evolution: learned_params persist failed: {e}")

    # Vorschläge persistieren (dedupliziert auf (category,title) bei status='proposed')
    saved_props = 0
    try:
        with db_conn() as conn:
            now = datetime.now(timezone.utc).isoformat()
            for p in proposals:
                dup = conn.execute(
                    "SELECT 1 FROM evolution_proposals WHERE category=? AND title=? "
                    "AND status='proposed'", (p["category"], p["title"])).fetchone()
                if dup:
                    continue
                conn.execute(
                    "INSERT INTO evolution_proposals (version, ts, category, title, rationale, "
                    "detail, confidence, impact, status) VALUES (?,?,?,?,?,?,?,?,'proposed')",
                    (version, now, p["category"], p["title"], p.get("rationale", ""),
                     json.dumps(p, ensure_ascii=False), float(p.get("confidence", 0.5)),
                     p.get("impact", "")))
                saved_props += 1
            conn.commit()
    except Exception as e:
        log.warning(f"evolution: proposals persist failed: {e}")

    summary = (f"Zyklus v{version}: {len(insights)} Erkenntnisse, {saved_props} neue "
               f"Vorschläge (von {len(proposals)} erkannt). Erfolgsquote-Wissen aktualisiert.")
    if not insights:
        summary = f"Zyklus v{version}: noch zu wenig Daten für belastbare Erkenntnisse."

    llm_note = engineering_note(insights, proposals)

    files = 0
    try:
        files = write_build(version, summary, insights, proposals, learned, llm_note)
    except Exception as e:
        log.warning(f"evolution: build write failed: {e}")

    # Zyklus loggen
    try:
        with db_conn() as conn:
            conn.execute(
                "INSERT INTO evolution_log (version, ts, summary, insights, proposals, files, "
                "trigger) VALUES (?,?,?,?,?,?,?)",
                (version, datetime.now(timezone.utc).isoformat(), summary,
                 len(insights), saved_props, files, trigger))
            conn.commit()
    except Exception as e:
        log.warning(f"evolution: log write failed: {e}")

    try:
        _conf["log_event"]("evolution.cycle", "info", summary,
                  {"version": version, "insights": len(insights),
                   "proposals": saved_props, "trigger": trigger})
    except Exception:
        pass
    log.info(f"🧬 Evolution {summary} (build: {files} Dateien, trigger={trigger})")

    return {"ok": True, "version": version, "summary": summary,
            "insights": insights, "proposals": saved_props, "files": files,
            "llm_note": llm_note, "build_dir": build_dir()}
