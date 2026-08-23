"""nc.schema — B164: DB-Schema-Erzeugung (aus bot_v37.init_db extrahiert).

Rein mechanisch aus dem Monolithen herausgelöst: der komplette CREATE-TABLE-/
Index-/Migrations-Block. Die backend-abhängigen Platzhalter (pk, txt_idx …) und
die zwei Helfer (_create_index_safe, _migrate_columns) werden vom Bot als
Parameter hereingereicht — so ändert sich KEINE Schema-Zeile beim Umzug, und
das Modul bleibt frei von Bot-Globals. Aufruf: bot_v37.init_db() öffnet die
Verbindung und ruft create_schema(conn, …).

43 Tabellen + Indizes + Spalten-Migrationen. Idempotent (CREATE … IF NOT EXISTS).
"""

from nc.textutil import clean_username  # bereits bot-freies nc/-Modul


def create_schema(conn, *, pk, txt_idx, txt_long, txt_big, iv, tbl_opts, is_my,
                  _create_index_safe, _migrate_columns, log, ts=None):
    """Legt das vollständige Schema auf der offenen Verbindung `conn` an.
       Alle Platzhalter/Helfer kommen als Parameter (backend-agnostisch).

       v4.0-W79: `ts` ist der Typ für INDIZIERTE ISO-Timestamp-Spalten
       (created_at/updated_at/started_at/...). Vorher `txt_long`=TEXT — eine
       indizierte TEXT-Spalte sprengt in MariaDB/InnoDB unter utf8mb4 die
       3072-Byte-Schlüsselgrenze (Fehler 1071) und ließ die Migration crashen.
       Bounded VARCHAR(64) passt für jeden ISO-Timestamp und in jeden Index."""
    if ts is None:
        ts = txt_idx  # backward-compat: nie TEXT für indizierte Timestamps
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS tiktok_checks (
        id {pk},
        telegram_user_id BIGINT,
        username {txt_idx},
        data {txt_big},
        created_at {ts}
    ){tbl_opts}""")
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS trackings (
        id {pk},
        group_id BIGINT NOT NULL,
        username {txt_idx} NOT NULL,
        added_by BIGINT,
        created_at {ts},
        last_live INT DEFAULT 0,
        recording INT DEFAULT 0,
        output_file {txt_long},
        pid INT,
        paused INT DEFAULT 0
    ){tbl_opts}""")
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS recordings (
        id {pk},
        username {txt_idx} NOT NULL,
        filepath {txt_long} NOT NULL,
        created_at {ts}
    ){tbl_opts}""")
    # F16: AI-Log für Dashboard-Stream + Audit
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS ai_log (
        id {pk},
        chat_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        prompt {txt_big} NOT NULL,
        response {txt_big},
        model {txt_long},
        duration_ms INT,
        error {txt_long},
        file_kind {txt_long},
        file_size BIGINT,
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    # F73: Persistent AI-Chat-Conversations für das Dashboard.
    # Wie ChatGPT/Claude: jede Conversation hat eine Historie aus Messages
    # (user + assistant + optional system). Bei jedem neuen User-Message
    # senden wir die letzten N Messages als context an Ollama → echtes
    # Multi-Turn-Chat statt Single-Shot wie F49.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS ai_conversations (
        id {pk},
        title {txt_long},
        created_at {ts} NOT NULL,
        updated_at {ts} NOT NULL,
        archived INT DEFAULT 0,
        message_count INT DEFAULT 0
    ){tbl_opts}""")
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS ai_messages (
        id {pk},
        conversation_id INT NOT NULL,
        role {txt_long} NOT NULL,
        content {txt_big} NOT NULL,
        created_at {ts} NOT NULL,
        model {txt_long},
        duration_ms INT,
        error {txt_long}
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_ai_msg_conv ON ai_messages(conversation_id, id)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_ai_conv_upd ON ai_conversations(archived, updated_at)")
    # F78: Per-Conversation Model-Wahl. Wenn Operator im Chat ein anderes
    # Modell wählt, wird's hier gespeichert → beim nächsten Öffnen wieder
    # vorausgewählt. NULL = use AI_MODEL default.
    _migrate_columns(conn, "ai_conversations", {
        "last_model": txt_long,
    })
    # F19: Recording-Attempts — jeder Versuch wird hier festgehalten,
    # auch fehlgeschlagene. Damit ist nachvollziehbar warum keine
    # Videos rauskommen (cookies down? recorder broken? ffmpeg-crash?).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS recording_attempts (
        id {pk},
        tracking_id INT,
        username {txt_idx} NOT NULL,
        recorder {txt_long},
        started_at {ts} NOT NULL,
        ended_at {ts},
        duration_secs INT,
        returncode INT,
        file_path {txt_long},
        file_size BIGINT,
        outcome {txt_long},
        stderr_tail {txt_big},
        error {txt_big}
    ){tbl_opts}""")
    # F21: Manuelles Archiv (separat von recordings/)
    # filepath UNIQUE → muss VARCHAR sein, nicht TEXT
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS archive (
        id {pk},
        filename {txt_idx} NOT NULL,
        filepath VARCHAR(500) NOT NULL UNIQUE,
        title {txt_long},
        notes {txt_big},
        size_bytes BIGINT,
        mime_type {txt_long},
        source_url {txt_long},
        created_at {ts} NOT NULL
    ){tbl_opts}""")

    # F26: Schema-Migration für Upgrades von alten Bot-Versionen.
    # CREATE TABLE IF NOT EXISTS lässt existierende Tabellen unverändert →
    # neue Spalten fehlen, Queries crashen "no such column". ALTER TABLE
    # ergänzt fehlende Spalten ohne Daten zu verlieren.
    _migrate_columns(conn, "trackings", {
        "added_by":    "BIGINT" if is_my else "INTEGER",
        "created_at":  ts,
        "last_live":   "INT DEFAULT 0",
        "recording":   "INT DEFAULT 0",
        "output_file": txt_long,
        "pid":         "INT",
        # F53: Pause-Toggle. paused=1 → Worker skipt diesen User komplett
        # (kein Live-Check, kein Recording). Default 0 = aktiv wie bisher.
        "paused":      "INT DEFAULT 0",
        # F60: Freitext-Label für Operator-Notizen ("VIP", "streams 2am",
        # "test account"). Sichtbar in Dashboard (inline editable) und
        # in /list-Output. Max 200 Zeichen (Endpoint-validiert).
        "notes":       txt_long,
        # B54: Circuit-Breaker State. auto_disabled_at = ISO-Timestamp wann
        # automatisches Disable triggerte. auto_disabled_reason = welche
        # Bedingung (z.B. "10× stall_killed"). Beim /resume vom Operator
        # werden beide auf NULL gesetzt.
        "auto_disabled_at":     txt_long,
        "auto_disabled_reason": txt_long,
    })
    _migrate_columns(conn, "tiktok_checks", {
        "telegram_user_id": "BIGINT" if is_my else "INTEGER",
        "data":             txt_big,
        "created_at":       ts,
    })
    _migrate_columns(conn, "recordings", {
        "created_at": ts,
    })

    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_trackings_username ON trackings(username)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_trackings_group_id ON trackings(group_id)")
    _create_index_safe(conn,
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_trackings_unique ON trackings(group_id, username)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_tiktok_checks_username ON tiktok_checks(username)")
    # B122-PERF: ohne diesen Index waere das Retention-DELETE unten selbst
    # ein Full-Scan — also genau das, was es beseitigen soll.
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_tiktok_checks_created ON tiktok_checks(created_at DESC)",
        "CREATE INDEX idx_tiktok_checks_created ON tiktok_checks(created_at)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_ai_log_created ON ai_log(created_at DESC)",
        "CREATE INDEX idx_ai_log_created ON ai_log(created_at)")     # MariaDB ignores DESC in index spec
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_rec_attempts_started ON recording_attempts(started_at DESC)",
        "CREATE INDEX idx_rec_attempts_started ON recording_attempts(started_at)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_archive_created ON archive(created_at DESC)",
        "CREATE INDEX idx_archive_created ON archive(created_at)")

    # ====================================================================
    # X-Series Tables (30 new features, build 2026.06)
    # ====================================================================
    # X-tags: Tags per Tracking. Composite PK (tracking_id, tag) prevents
    # duplicate tag assignments. Cascade-delete handled in remove_tracking.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS tracking_tags (
        tracking_id INT NOT NULL,
        tag {txt_idx} NOT NULL,
        created_at {ts},
        PRIMARY KEY (tracking_id, tag)
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_tracking_tags_tag ON tracking_tags(tag)")
    # F82: Indizes für die heißesten Query-Pfade. recordings wächst unbegrenzt
    # (jede Aufnahme eine Row) — created_at wird von Digest/Retention/Dashboard
    # gefiltert (6 Queries), username von /stats,/clips,/topstreamers + Digest-
    # GROUP BY. profile_snapshots: Timeline pro User. discord_*: COTW-Fenster,
    # Warn-Zähler, XP-Leaderboard. Alles Grundschema-Spalten (keine Migrations-
    # Abhängigkeit), IF NOT EXISTS → einmaliger Build beim ersten Start.
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_recordings_created ON recordings(created_at)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_recordings_user ON recordings(username, created_at)")
    # B82-Fix: Die Discord-/Community-Indizes standen hier VOR ihren Tabellen
    # (discord_clips/warns/xp/daily, community_events, profile_snapshots werden
    # erst später erstellt). Auf einer FRISCHEN DB crashte init_db reihenweise
    # ('no such table'). Vom F104-Selfcheck gefangen. Alle diese Indizes sind
    # jetzt ans ENDE von init_db verschoben (nach allen CREATE TABLE).
    # F102: Community — tägliche Streaks (/daily) + geplante Events/Countdowns
    # B138-Fix: vorher rohes SQLite-DDL ohne Platzhalter — auf MariaDB nie
    # angelegt (AUTOINCREMENT ist dort schon Syntaxfehler). Jetzt aufs
    # backend-aware Muster gezogen (f-String + {pk}/{txt_*}/{iv}/{tbl_opts}).
    # Discord-guild_id/user_id/created_by sind Snowflakes (64-bit) → BIGINT,
    # nicht {iv}: MariaDB-INT ist 32-bit und würde die IDs überlaufen lassen
    # (gleiche Begründung wie telegram_user_id BIGINT oben). Auf SQLite ist
    # BIGINT INTEGER-Affinität — die erzeugte SQLite-DDL bleibt verhaltensgleich.
    # starts_at ist über idx_events_when indiziert → {txt_idx} (VARCHAR(255)).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS discord_daily (
        guild_id BIGINT, user_id BIGINT,
        last_claim {txt_long}, streak {iv} DEFAULT 0, best_streak {iv} DEFAULT 0,
        total_claims {iv} DEFAULT 0,
        PRIMARY KEY (guild_id, user_id)
    ){tbl_opts}""")
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS community_events (
        id {pk},
        guild_id BIGINT, title {txt_long}, description {txt_long},
        starts_at {txt_idx}, created_by BIGINT, created_at {ts},
        announced {iv} DEFAULT 0, done {iv} DEFAULT 0
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_when ON community_events(starts_at, done)")

    # X-priority: VIP-Markierung + Custom-Interval pro Tracking
    # priority_level: 0=normal, 1=high (15s poll), 2=vip (10s poll)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS tracking_priority (
        tracking_id INT PRIMARY KEY,
        priority_level INT DEFAULT 0,
        custom_interval_secs INT,
        updated_at {ts}
    ){tbl_opts}""")

    # X-notes: Notes pro Recording (auch nach Telegram-Upload behaltbar)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS recording_notes (
        recording_id INT PRIMARY KEY,
        note {txt_big},
        created_at {ts},
        updated_at {ts}
    ){tbl_opts}""")

    # X-annotations: Timestamps in Aufnahmen ("interessanter Moment bei 02:34")
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS recording_annotations (
        id {pk},
        recording_id INT NOT NULL,
        timestamp_secs INT NOT NULL,
        label {txt_long},
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_rec_annot_rec ON recording_annotations(recording_id, timestamp_secs)")

    # X-bookmarks: Favorit-Markierung
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS bookmarks (
        recording_id INT PRIMARY KEY,
        created_at {ts} NOT NULL
    ){tbl_opts}""")

    # X-events: Chronologischer Event-Log (Sources: recording-events, system-events, manual)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS event_log (
        id {pk},
        ts {txt_long} NOT NULL,
        kind {txt_idx} NOT NULL,
        severity {txt_long} DEFAULT 'info',
        summary {txt_long},
        payload {txt_big}
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_event_log_ts ON event_log(ts DESC)",
        "CREATE INDEX idx_event_log_ts ON event_log(ts)")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_event_log_kind ON event_log(kind)")

    # X-archive-rules: Auto-Archive-Regeln. condition+action als JSON.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS auto_archive_rules (
        id {pk},
        name {txt_long} NOT NULL,
        condition_json {txt_big} NOT NULL,
        action_json {txt_big} NOT NULL,
        enabled INT DEFAULT 1,
        last_run {txt_long},
        last_match_count INT DEFAULT 0,
        created_at {ts} NOT NULL
    ){tbl_opts}""")

    # X-inspect: ffprobe-Cache für recordings (vermeidet bei jedem Hover
    # ffprobe-Subprocess-Call)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS recording_inspect_cache (
        recording_id INT PRIMARY KEY,
        inspect_json {txt_big},
        file_hash {txt_long},
        inspected_at {txt_long} NOT NULL
    ){tbl_opts}""")

    # X-snapshots: Profile-Snapshots pro Username (Follower-History etc.)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS profile_snapshots (
        id {pk},
        username {txt_idx} NOT NULL,
        payload {txt_big} NOT NULL,
        follower_count INT,
        heart_count BIGINT,
        video_count INT,
        captured_at {txt_long} NOT NULL
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_prof_snap_user ON profile_snapshots(username, captured_at DESC)",
        "CREATE INDEX idx_prof_snap_user ON profile_snapshots(username, captured_at)")

    # X-manual: Manuelle Ad-hoc-Aufnahmen
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS manual_recordings (
        id {pk},
        username {txt_idx} NOT NULL,
        max_duration_secs INT NOT NULL,
        started_at {ts} NOT NULL,
        ended_at {ts},
        recorder_pid INT,
        output_file {txt_long},
        status {txt_long} DEFAULT 'running',
        file_size BIGINT,
        triggered_by {txt_long} DEFAULT 'dashboard'
    ){tbl_opts}""")

    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_manual_rec_status ON manual_recordings(status, started_at DESC)",
        "CREATE INDEX idx_manual_rec_status ON manual_recordings(status, started_at)")

    # Restream-Ziele: relayt einen (autorisierten) Stream nach Kick.
    # source_username = getrackter Streamer (Quelle wird via Resolver geholt).
    # status: idle | starting | live | error | stopped
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS restreams (
        id {pk},
        created_at {ts} NOT NULL,
        label {txt_long},
        source_username {txt_long},
        ingest_url {txt_long},
        stream_key {txt_long},
        transcode {iv} DEFAULT 0,
        enabled {iv} DEFAULT 1,
        status {txt_long} DEFAULT 'idle',
        pid {iv},
        started_at {ts},
        last_error {txt_big}
    ){tbl_opts}""")
    # Moderator-Log: was der KI-Mod gesendet/moderiert hat (für Dashboard-Anzeige).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS kick_mod_log (
        id {pk},
        ts {txt_long} NOT NULL,
        kind {txt_long},
        actor {txt_long},
        content {txt_big},
        meta {txt_big}
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_modlog_ts ON kick_mod_log(ts DESC)",
        "CREATE INDEX idx_modlog_ts ON kick_mod_log(ts)")

    # Overlay-Events (Follower/Donations) für die On-Screen-Grafik.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS overlay_events (
        id {pk},
        ts {txt_long} NOT NULL,
        kind {txt_long},
        name {txt_long},
        amount {txt_long},
        message {txt_big}
    ){tbl_opts}""")
    _create_index_safe(conn,
        "CREATE INDEX IF NOT EXISTS idx_overlay_ts ON overlay_events(ts DESC)",
        "CREATE INDEX idx_overlay_ts ON overlay_events(ts)")
    # V37-OVMP: Multi-Plattform-Overlay. Bestandszeilen haben keine
    # Herkunft — sie bekommen 'kick' (bis hier war Kick die einzige
    # Quelle, die Follows/Donations ins Overlay schrieb).
    _migrate_columns(conn, "overlay_events", {"platform": f"{txt_long} DEFAULT 'kick'"})
    # V37-OV: Multi-Plattform-Donations/Follower. platform = kick|twitch|
    # youtube|tiktok|manuell; amount_eur = auf EUR normalisierter Betrag
    # (Bits/Subs/Superchats/Coins sind sonst nicht summierbar).
    _migrate_columns(conn, "overlay_events", {
        "platform": f"{txt_long}",
        "amount_eur": "REAL DEFAULT 0",
    })
    # Discord-Community: XP/Level-Ranking pro Guild+User
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS discord_xp (
        guild_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        xp INT DEFAULT 0,
        level INT DEFAULT 0,
        last_ts {txt_long},
        PRIMARY KEY (guild_id, user_id)
    ){tbl_opts}""")
    # V37-LOYALTY: persistente Punkte fuer Stammzuschauer (Stream-Treue,
    # getrennt vom Discord-Chat-XP). key = 'platform:username'.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS loyalty_points (
        k {txt_idx} NOT NULL,
        name {txt_long},
        points INT DEFAULT 0,
        updated {txt_long},
        PRIMARY KEY (k)
    ){tbl_opts}""")
    # V37-BRAINVIZ: Zeitreihe des Brain-Wachstums (Wissen/Vektoren/Nutzer über
    # Zeit) — fuer die Lern-/Wachstumskurve im Dashboard. Ein Snapshot je Stunde.
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS brain_growth (
        ts {txt_long} NOT NULL,
        triples INT DEFAULT 0,
        vectors INT DEFAULT 0,
        users INT DEFAULT 0,
        sessions INT DEFAULT 0
    ){tbl_opts}""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_brain_growth_ts ON brain_growth(ts)")
    # Discord-Community: persistenter Key-Value-State (z.B. Live-Board-Message-ID)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS discord_state (
        k {txt_idx} NOT NULL,
        v {txt_long},
        PRIMARY KEY (k)
    ){tbl_opts}""")
    # Discord-Community: Verwarnungen (Warn-System mit Eskalation)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS discord_warns (
        id {pk},
        guild_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        moderator {txt_long},
        reason {txt_big},
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    # Discord-Community: gepostete Clips (für Clip-of-the-Week Reaction-Voting)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS discord_clips (
        id {pk},
        guild_id BIGINT NOT NULL,
        channel_id BIGINT NOT NULL,
        message_id BIGINT NOT NULL,
        username {txt_long},
        filepath {txt_big},
        stars_pushed INTEGER DEFAULT 0,
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    # F84: Migration falls die Tabelle auf dem Server schon ohne die neuen
    # Spalten existiert (Feature kam nach dem ersten Deploy).
    for _coldef in ("filepath TEXT", "stars_pushed INTEGER DEFAULT 0"):
        try:
            conn.execute(f"ALTER TABLE discord_clips ADD COLUMN {_coldef}")
        except Exception:
            pass
    # v37 W3b: Backup-Status-Spalte für Aufnahmen (idempotent)
    try:
        conn.execute("ALTER TABLE recordings ADD COLUMN backed_up INTEGER DEFAULT 0")
    except Exception:
        pass
    # B82: Die Discord-/Community-Indizes JETZT anlegen — hier existieren alle
    # referenzierten Tabellen garantiert (discord_clips/warns/xp/daily,
    # profile_snapshots). Vorher standen sie irrtümlich VOR den Tabellen und
    # ließen init_db auf frischer DB crashen. Alle IF NOT EXISTS → idempotent.
    for _ix in (
        "CREATE INDEX IF NOT EXISTS idx_snapshots_user ON profile_snapshots(username, captured_at)",
        "CREATE INDEX IF NOT EXISTS idx_discord_clips_created ON discord_clips(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_discord_warns_gu ON discord_warns(guild_id, user_id)",
        "CREATE INDEX IF NOT EXISTS idx_discord_xp_gx ON discord_xp(guild_id, xp)",
    ):
        try:
            conn.execute(_ix)
        except Exception as _e:
            log.debug("index build skipped: %s", _e)
    # B76c: Alt-Einträge in restreams heilen — source_username enthielt teils
    # komplette TikTok-URLs (mit UND ohne Slash vor dem @). Der Chat-Listener
    # scheiterte daran an Phantom-Usern. Idempotent: saubere Handles bleiben
    # unverändert, nur Müll-Formen werden normalisiert.
    try:
        for _r in conn.execute("SELECT id, source_username FROM restreams").fetchall():
            _raw = _r["source_username"] or ""
            _cu = clean_username(_raw)
            if _cu and _cu != _raw:
                conn.execute("UPDATE restreams SET source_username=? WHERE id=?",
                             (_cu, _r["id"]))
                log.info("B76c: Restream #%s source_username '%s' → '%s' normalisiert.",
                         _r["id"], _raw, _cu)
    except Exception:
        pass
    # F86: AZRAEL ORACLE — destilliertes Langzeit-Gedächtnis pro Streamer
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS stream_memories (
        id {pk},
        username {txt_long},
        summary {txt_big},
        lines INTEGER,
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_mem ON stream_memories(username, created_at)")
    # F87: AUTO-DIRECTOR — markierte Hype-Momente (Kapitel) pro Aufnahme
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS stream_chapters (
        id {pk},
        username {txt_long},
        recfile {txt_long},
        offset_secs REAL,
        reason {txt_long},
        title {txt_long},
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_chap ON stream_chapters(username, created_at)")
    # F90: KI-Telemetrie — jede AZRAEL-Interaktion (Zweck, Dauer, ok/err)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS ai_interactions (
        id {pk},
        purpose {txt_long},
        prompt_chars INTEGER,
        answer_chars INTEGER,
        ms INTEGER,
        ok INTEGER DEFAULT 1,
        err {txt_long},
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ai_inter ON ai_interactions(created_at)")
    # v37 Welle 1: Preflight-Historie (Health über Zeit)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS preflight_history (
        id {pk},
        overall {txt_long},
        fails INTEGER,
        warns INTEGER,
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_preflight_hist ON preflight_history(created_at)")
    # v37 Welle 1: Audit-Log (wer hat im Dashboard was geschaltet)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS audit_log (
        id {pk},
        method {txt_long},
        path {txt_long},
        ip {txt_long},
        status INTEGER,
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit ON audit_log(created_at)")
    # v37 Welle 2: Scheduler — geplante Aufgaben zu festen Uhrzeiten
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS scheduled_tasks (
        id {pk},
        kind {txt_long} NOT NULL,
        at_hhmm {txt_long} NOT NULL,
        payload {txt_long},
        enabled INTEGER DEFAULT 1,
        last_run_date {txt_long},
        created_at {ts} NOT NULL
    ){tbl_opts}""")
    # Restream: auto_restream (Auto-Start bei Go-Live) nachrüsten
    _migrate_columns(conn, "restreams", {
        "auto_restream": "INTEGER DEFAULT 0",
        # B123: SOLL-Zustand. Bisher gab es nur den IST-Zustand (status/pid).
        # Nach einem Absturz war damit nicht mehr feststellbar, ob ein
        # Restream laufen SOLLTE — ein von Hand gestarteter war schlicht weg.
        # desired=1 setzt start(), desired=0 nur ein ausdrueckliches stop().
        # Ein Absturz fasst die Spalte nicht an, deshalb ueberlebt der
        # Soll-Zustand ihn.
        "desired": "INTEGER DEFAULT 0",
        "desired_since": "TEXT",
        # v4.0-W77: PRO-PLATTFORM-Overrides je Restream (B). Kick nutzt weiter
        # ingest_url/stream_key; Twitch/YouTube bekommen eigene Override-Spalten.
        # Leer → globale Env-Ziele. So kann ein einzelner Restream z. B. auf einen
        # anderen Twitch-Kanal gehen, ohne die globale Konfiguration zu ändern.
        "tw_ingest": txt_long,
        "tw_key": txt_long,
        "yt_ingest": txt_long,
        "yt_key": txt_long,
    })

    # Migration: recordings.file_size (für Quality-Score + Bandwidth-Calc)
    _migrate_columns(conn, "recordings", {
        "file_size":      "BIGINT",
        "duration_secs":  "INT",
        "fingerprint":    txt_long,    # SHA256 von ersten 1MB
        "quality_score":  "INT",       # 0-100
        "deleted_at":     ts,    # Soft-delete für trash/restore
        "tracking_id":    "INT",       # Backlink für analytics
    })

    # =====================================================================
    # B65: 30-Module-Pack — Schema (Insights/Kuratierung/Collections/
    #      Webhooks/Notif/Ops). Alles idempotent + cross-dialect.
    # =====================================================================
    # Key-Value-Config für Retention, Quiet-Hours etc. (statt vieler Mini-
    # Tabellen — ein zentraler, leicht erweiterbarer Store).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS app_config (
        k {txt_idx} NOT NULL,
        v {txt_big},
        updated_at {ts}
    ){tbl_opts}""")
    try:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_app_config_k "
                     "ON app_config(k)")
    except Exception:
        pass
    # Webhooks (Outbound-Integrationen: Discord/n8n/eigener Endpoint).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS webhooks (
        id {pk},
        url {txt_long} NOT NULL,
        events {txt_idx},
        enabled INT DEFAULT 1,
        created_at {ts},
        last_status {txt_idx},
        last_fired_at {txt_long},
        fail_count INT DEFAULT 0
    ){tbl_opts}""")
    # Benannte Streamer-Collections (Gruppierung über group_id hinaus).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS tracking_collections (
        id {pk},
        name {txt_idx} NOT NULL,
        color {txt_idx},
        created_at {ts}
    ){tbl_opts}""")
    # Neue recordings-Spalten: starred/rating/label (Kuratierung)
    _migrate_columns(conn, "recordings", {
        "starred":   "INT DEFAULT 0",
        "rating":    "INT",            # 1-5
        "label":     txt_idx,          # frei wählbares Label
    })
    # Neue trackings-Spalten: Collection-Zuordnung + Dauer-Override
    _migrate_columns(conn, "trackings", {
        "collection_id":         "BIGINT",
        "max_duration_override": "INT",   # Sekunden; NULL = globaler Default
    })

    # =====================================================================
    # B66: Self-Learning Evolution Core — Schema
    # =====================================================================
    # Gelerntes Wissen (key-value mit Konfidenz + Sample-Größe + Kategorie).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS learned_params (
        k {txt_idx} NOT NULL,
        v {txt_big},
        confidence REAL DEFAULT 0,
        samples INT DEFAULT 0,
        category {txt_idx},
        updated_at {ts}
    ){tbl_opts}""")
    try:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_learned_params_k "
                     "ON learned_params(k)")
    except Exception:
        pass
    # Protokoll jedes Lern-Zyklus (versioniert).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS evolution_log (
        id {pk},
        version INT,
        ts {txt_long},
        summary {txt_big},
        insights INT DEFAULT 0,
        proposals INT DEFAULT 0,
        files INT DEFAULT 0,
        trigger {txt_idx}
    ){tbl_opts}""")
    # Generierte Weiterentwicklungs-Vorschläge (zum Review).
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS evolution_proposals (
        id {pk},
        version INT,
        ts {txt_long},
        category {txt_idx},
        title {txt_long},
        rationale {txt_big},
        detail {txt_big},
        confidence REAL DEFAULT 0,
        impact {txt_idx},
        status {txt_idx} DEFAULT 'proposed'
    ){tbl_opts}""")

    conn.commit()
