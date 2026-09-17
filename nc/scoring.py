"""nc.scoring — Profil-Qualitäts-Score + Analyse-Report (rein).

Extrahiert aus bot.py: compute_quality_score bewertet ein TikTok-Profil
(Follower/Engagement/Verhältnisse), build_report rendert den Telegram-Report."""

from datetime import datetime

from nc.fmt import pre_table
from nc.textutil import fmt_number, safe, short

def compute_quality_score(inspect_data: dict, file_size: int,
                          duration_secs: float) -> dict:
    """0-100 Score basierend auf Bitrate, Auflösung, Audio-Bitrate,
       und Completeness (returncode + duration vs intended).
       Returns: {score, components: {video: 0-30, audio: 0-20, ...}}"""
    if not inspect_data:
        return {"score": 0, "components": {}, "notes": ["no inspect-data"]}

    notes = []
    components = {"video": 0, "audio": 0, "container": 0, "size": 0}

    streams = inspect_data.get("streams") or []
    fmt = inspect_data.get("format") or {}

    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)

    # VIDEO 0-30
    if video:
        components["video"] = 5    # for existing
        try:
            h = int(video.get("height") or 0)
            if h >= 1080:    components["video"] += 15
            elif h >= 720:   components["video"] += 12
            elif h >= 480:   components["video"] += 8
            elif h > 0:      components["video"] += 4
            else: notes.append("no video dimensions")

            # Codec check
            codec = (video.get("codec_name") or "").lower()
            if codec in ("h264", "hevc", "av1"):
                components["video"] += 5
            elif codec:
                components["video"] += 2

            # Framerate
            fr = video.get("r_frame_rate", "0/1")
            try:
                num, den = fr.split("/")
                fps = float(num) / float(den) if float(den) else 0
                if fps >= 25:    components["video"] += 5
                elif fps >= 15:  components["video"] += 3
            except Exception: pass
        except Exception:
            notes.append("video parse error")
    else:
        notes.append("no video stream")

    # AUDIO 0-20
    if audio:
        components["audio"] = 5
        try:
            br = int(audio.get("bit_rate") or 0)
            if br >= 128000:   components["audio"] += 10
            elif br >= 64000:  components["audio"] += 7
            elif br > 0:       components["audio"] += 4
            ch = int(audio.get("channels") or 0)
            if ch >= 2:        components["audio"] += 5
            elif ch == 1:      components["audio"] += 3
        except Exception:
            notes.append("audio parse error")
    else:
        notes.append("no audio stream")

    # CONTAINER 0-15
    if fmt:
        components["container"] = 5
        try:
            dur = float(fmt.get("duration") or 0)
            if dur > 0:
                components["container"] += 5
                if duration_secs and abs(dur - duration_secs) / max(dur, 1) < 0.05:
                    components["container"] += 5  # well-matched duration
            # v4.2-W89: hier standen zwei Zeilen, die `fmt["bit_rate"]` lasen
            # und im Treffer `pass` machten — mit dem Kommentar "bitrate
            # already factored in video/audio". Sie vergaben also keinen
            # Punkt, konnten aber bei einem unlesbaren Wert die ganze
            # Container-Bewertung in den except-Zweig reissen und die
            # Dauer-Punkte mitnehmen. Ein Lesevorgang, der nur schiefgehen
            # kann, ist schlechter als keiner.
        except Exception:
            # v4.2-W89: war `except Exception: pass` — der einzige der vier
            # Bloecke ohne Notiz. Video und Audio melden ihren Parse-Fehler,
            # der Container schwieg: eine Aufnahme verlor bis zu 10 Punkte,
            # und in `notes` stand nichts, woran der Betreiber das haette
            # sehen koennen.
            notes.append("container parse error")

    # SIZE 0-35 (sanity check — recording shouldn't be tiny)
    mb = (file_size or 0) / 1024 / 1024
    if mb >= 50:     components["size"] = 35
    elif mb >= 10:   components["size"] = 25
    elif mb >= 1:    components["size"] = 15
    elif mb > 0:     components["size"] = 5
    else:
        notes.append("zero file size")

    score = sum(components.values())
    score = max(0, min(100, score))
    return {"score": score, "components": components, "notes": notes}

def build_report(data: dict, live: dict) -> str:
    def _ts(v):
        try: return datetime.fromtimestamp(int(v)).strftime("%Y-%m-%d %H:%M")
        except Exception: return "—"

    handle = safe(data.get("unique_id") or data.get("username"))
    name   = safe(data.get("nickname"), "—")

    flags = []
    if data.get("verified"):     flags.append("✓ verified")
    if data.get("private"):      flags.append("🔒 privat")
    else:                        flags.append("public")
    if live.get("is_live"):      flags.append("🔴 LIVE")

    sec_uid = safe(short(str(data.get("sec_uid") or "—"), 20))
    user_id = safe(data.get("user_id"))

    identity = pre_table([
        ("Name",   name),
        ("ID",     user_id or "—"),
        ("SecUID", sec_uid),
    ], align='left')

    metrics = pre_table([
        ("Follower",  fmt_number(data.get("follower_count"))),
        ("Following", fmt_number(data.get("following_count"))),
        ("Likes",     fmt_number(data.get("heart_count"))),
        ("Videos",    fmt_number(data.get("video_count"))),
        ("Friends",   fmt_number(data.get("friend_count"))),
        ("Diggs",     fmt_number(data.get("digg_count"))),
    ], align='right')

    timeline = pre_table([
        ("Erstellt", _ts(data.get("create_time"))),
        ("Geändert", _ts(data.get("modify_time"))),
    ], align='left')

    parts = [
        f"📊 <b>PROFIL · @{handle}</b>",
        f"<i>{' · '.join(flags)}</i>",
        "",
        f"<pre>{identity}</pre>",
        "",
        "📈 <b>Metriken</b>",
        f"<pre>{metrics}</pre>",
        "",
        "📅 <b>Zeitleiste</b>",
        f"<pre>{timeline}</pre>",
    ]

    bio = data.get("signature")
    if bio and str(bio).strip():
        bio_safe = safe(bio)
        tag = "blockquote expandable" if len(str(bio)) > 180 else "blockquote"
        parts += ["", "📝 <b>Bio</b>", f"<{tag}>{bio_safe}</blockquote>"]

    videos = data.get("recent_videos") or []
    if videos:
        parts += ["", "🎬 <b>Letzte Videos</b>"]
        for i, v in enumerate(videos, 1):
            # v4.2-W89: erst SCHNEIDEN, dann maskieren. Hier stand
            # `short(safe(...), 50)`, also die umgekehrte Reihenfolge — und
            # damit schneidet die 50-Zeichen-Grenze mitten in eine
            # HTML-Entitaet: aus "&amp;" wird "&am", aus "&#39;" wird "&#3".
            # Telegram parst den Report als HTML und lehnt dann die GANZE
            # Nachricht mit "can't parse entities" ab — nicht die eine Zeile.
            # Ein Titel mit "&" oder "<" an der richtigen Stelle genuegt, und
            # der Betreiber bekommt statt des Reports gar nichts. Zwei Zeilen
            # weiter oben (SecUID) stand die Reihenfolge immer richtig; das
            # hier war ein Versehen, keine Absicht.
            roh = str(v.get("desc") or "").strip()
            desc = safe(short(roh, 50) if roh else "Video")
            parts.append(f"  {i}. <a href=\"{safe(v.get('url',''))}\">{desc}</a>")

    return "\n".join(parts)
