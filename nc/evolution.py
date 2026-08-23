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
from datetime import datetime, timedelta, timezone

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
