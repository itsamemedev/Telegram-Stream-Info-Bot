"""test_nc_modules — die aus bot_v37.py extrahierten nc-Module laufen
eigenstaendig gegen das ECHTE Bot-Schema.

Das Schema wird zur Laufzeit AUS bot_v37.py gezogen (Klammer-Zaehlung, keine
Regex-Naeherung) und die f-String-Platzhalter werden mit den SQLite-Werten
aufgeloest. So kann der Test nicht gegen ein ausgedachtes Schema gruen werden —
genau der Fehler, der beim Bauen dieser Module mehrfach passiert ist.

Hintergrund: db_conn() ist nach nc.dbwrap gewandert. Das war der Schluessel zur
weiteren Modularisierung — ueber 100 Bot-Funktionen hingen AUSSCHLIESSLICH an
diesem einen Symbol und sind seitdem frei von Bot-Globals.
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nc.dbwrap import db_conn, configure_db          # noqa: E402
import nc.archive as archive                          # noqa: E402
import nc.notes as notes                              # noqa: E402
import nc.stats as stats                              # noqa: E402

TABLES = ["recording_notes", "bookmarks", "recording_annotations", "recordings",
          "trackings", "recording_attempts", "archive", "stream_chapters",
          "ai_conversations"]

# Werte aus dem SQLite-Zweig von _init_db() (bot_v37.py)
PLACEHOLDERS = {"txt_idx": "TEXT", "txt_long": "TEXT", "txt_big": "TEXT",
                "ts": "TEXT",   # v4.0-W79: indizierter Timestamp (SQLite=TEXT, MariaDB=VARCHAR(64))
                "iv": "INTEGER", "tbl_opts": "",
                "pk": "INTEGER PRIMARY KEY AUTOINCREMENT"}

PASS = 0


def ok(msg):
    global PASS
    PASS += 1
    print("  \u2713 " + msg)


def _extract_schema():
    """CREATE TABLE aus bot_v37.py ziehen — Klammern zaehlen, nicht raten."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(here, "nc", "schema.py")).read()  # B164: Schema extrahiert
    out = []
    for t in TABLES:
        i = src.find("CREATE TABLE IF NOT EXISTS " + t + " (")
        if i < 0:
            continue
        j = src.index("(", i)
        depth, k = 0, j
        while k < len(src):
            if src[k] == "(":
                depth += 1
            elif src[k] == ")":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        out.append(src[i:k + 1])
    sql = ";\n".join(out)
    for a, b in PLACEHOLDERS.items():
        sql = sql.replace("{" + a + "}", b)
    left = re.findall(r"\{[^}]*\}", sql)
    assert not left, "unaufgeloeste Platzhalter: %s" % left
    assert len(out) >= 5, "Schema unvollstaendig: nur %d Tabellen" % len(out)
    return sql





def _test_dbexport():
    """V37-DBX: SQL-Export/Import fuer den SQLite<->MariaDB-Umstieg."""
    from nc.dbexport import (db_export_sql, db_import_sql, parse_header,
                             export_summary, _lit, _split_statements)

    # --- Der Dialekt-Fallstrick: Backslash ist in MySQL ein Escape ---
    p = "C:\\rec\\live.mp4"
    assert _lit(p, "sqlite") == "'C:\\rec\\live.mp4'", _lit(p, "sqlite")
    assert _lit(p, "mariadb") == "'C:\\\\rec\\\\live.mp4'", _lit(p, "mariadb")
    ok("dbexport: Backslash nur fuer mariadb verdoppelt (sonst still zerstoert)")

    assert _lit(None, "sqlite") == "NULL"
    assert _lit(True, "sqlite") == "1" and _lit(False, "sqlite") == "0"
    assert _lit(b"\x00\xff", "sqlite") == "X'00ff'"
    assert _lit("it's", "sqlite") == "'it''s'"
    ok("dbexport: NULL/bool/BLOB/Quote-Literale")

    # --- Splitter: Semikolon im Wert darf nicht trennen ---
    assert len(_split_statements(
        "INSERT INTO t VALUES ('a; b');\nINSERT INTO t VALUES ('c');")) == 2
    assert len(_split_statements("INSERT INTO t VALUES ('it''s; x');")) == 1
    assert len(_split_statements("-- komm; entar\nINSERT INTO t VALUES (1);")) == 1
    ok("dbexport: Splitter respektiert Strings, Quotes und Kommentare")

    # --- Roundtrip mit allen Fiesheiten ---
    rows = [("C:\\rec\\x.mp4", "hallo; welt", 1024, 1.5, b"\x00\xff"),
            ("/srv/a'b.mp4", "it's; ok?", None, None, None),
            ("/rec/\u00fcn\u00efcode.mp4", "Zeilen\numbruch", 7, 0.1, b"xyz")]
    with db_conn() as c:
        cur = c.cursor()
        cur.execute("CREATE TABLE dbx_t (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "p TEXT, n TEXT, i INTEGER, f REAL, b BLOB)")
        for r in rows:
            cur.execute("INSERT INTO dbx_t (p,n,i,f,b) VALUES (?,?,?,?,?)", r)

    sql = "".join(db_export_sql(dialect="sqlite"))
    h = parse_header(sql)
    assert h.get("dialect") == "sqlite" and h.get("rows", 0) >= 3, h
    ok("dbexport: Header traegt Dialekt + Kennzahlen (%d Zeilen)" % h["rows"])

    with db_conn() as c:
        c.cursor().execute("DELETE FROM dbx_t")
    rep = db_import_sql(sql, expect_dialect="sqlite")
    assert rep["ok"], rep["errors"]
    with db_conn() as c:
        cur = c.cursor()
        cur.execute("SELECT p,n,i,f,b FROM dbx_t ORDER BY id")
        got = [tuple(r[k] for k in ("p", "n", "i", "f", "b"))
               for r in cur.fetchall()]
    assert got == rows, "Roundtrip nicht bitgenau:\n%s\n%s" % (rows, got)
    ok("dbexport: Roundtrip bitgenau (Backslash/Semikolon/Quote/Unicode/NULL/BLOB)")

    # --- dry_run schreibt NICHTS ---
    with db_conn() as c:
        c.cursor().execute("DELETE FROM dbx_t")
    rep = db_import_sql(sql, expect_dialect="sqlite", dry_run=True)
    assert rep["ok"] and rep["applied"] == 0 and rep["statements"] > 0, rep
    with db_conn() as c:
        cur = c.cursor()
        cur.execute("SELECT COUNT(*) AS n FROM dbx_t")
        assert cur.fetchone()["n"] == 0, "dry_run hat geschrieben!"
    ok("dbexport: dry_run prueft, ohne zu schreiben")

    # --- Falscher Dialekt wird abgelehnt (sonst stiller Datenverlust) ---
    my = "".join(db_export_sql(dialect="mariadb"))
    rep = db_import_sql(my, expect_dialect="sqlite")
    assert not rep["ok"] and rep["errors"], "mariadb-Dump in sqlite durchgelassen!"
    ok("dbexport: falscher Dialekt wird abgelehnt")

    try:
        list(db_export_sql(dialect="quatsch"))
        raise AssertionError("ungueltiger Dialekt nicht abgelehnt")
    except ValueError:
        pass
    ok("dbexport: ungueltiger Dialekt wirft ValueError")

    s = export_summary()
    assert isinstance(s, dict) and "dbx_t" in s
    ok("dbexport: export_summary liefert Zeilen je Tabelle")


def _test_procdiag():
    """Phase-1-Zerlegung: die Prozess-/Thread-Diagnose (W83/W88) liegt jetzt in
       nc.procdiag; bot_v37 hält nur dünne Wrapper. Verhalten muss identisch sein."""
    import tempfile, os as _os, glob as _glob
    from nc import procdiag
    assert isinstance(procdiag.zombie_child_count(), int)
    ok("procdiag.zombie_child_count")

    d = tempfile.mkdtemp()
    for i in range(12):
        open(_os.path.join(d, "loop_stall_%d.txt" % i), "w").close()
    procdiag.prune_stall_dumps(d, keep=10)
    assert len(_glob.glob(_os.path.join(d, "loop_stall_*.txt"))) == 10
    ok("procdiag.prune_stall_dumps (12→10)")

    p = procdiag.dump_all_threads(d, "unittest")
    assert p and _os.path.exists(p) and "THREAD-DUMP" in open(p).read()
    ok("procdiag.dump_all_threads schreibt Dump")

    # Monolith delegiert (Wrapper vorhanden, Logik ausgelagert)
    src = open("bot_v37.py").read()
    assert "from nc import procdiag as _nc_procdiag" in src, "procdiag nicht importiert"
    assert "_nc_procdiag.zombie_child_count()" in src, "Wrapper delegiert nicht"
    ok("bot_v37 delegiert an nc.procdiag")

    # Phase-1-Zerlegung: ffmpeg-Clip-Helfer nach nc.ffdiag konsolidiert
    from nc import ffdiag
    assert ffdiag.ffprobe_duration("/nonexistent_xyz.mp4") == 0.0
    assert ffdiag.clip_caption_escape("a: 'b' 100% \\ c") == "a b 100 c"
    assert len(ffdiag.clip_caption_escape("x" * 200)) == 70
    ok("ffdiag.ffprobe_duration + clip_caption_escape (aus bot_v37 gelöst)")
    assert "clip_caption_escape as _clip_caption_escape" in src, "Clip-Escape nicht konsolidiert importiert"
    assert "def _clip_caption_escape(s):" not in src, "alter Rumpf noch im Monolith"
    ok("bot_v37 nutzt konsolidierte ffdiag-Clip-Helfer")

    # Phase-1-Zerlegung: Login-Seite nach nc.loginpage
    from nc import loginpage
    _pg = loginpage.login_page("Falsches PIN.", "/betrieb")
    assert "<form" in _pg and "Falsches PIN." in _pg and "value='/betrieb'" in _pg
    assert "&lt;script&gt;" in loginpage.login_page("<script>", "/"), "Login-Seite escaped nicht"
    assert "login_page as _login_page" in src and "def _login_page(" not in src, "Login-Seite nicht ausgelagert"
    ok("nc.loginpage.login_page (aus bot_v37 gelöst, XSS-sicher)")


def _test_shield_harden():
    """V37-SHIELD-HARDEN: Umgehungstricks (Homoglyphen, Zero-Width, Akzente,
    Trennzeichen) müssen gefangen werden — OHNE harmlose Nachrichten zu treffen.
    False Positives sind bei Moderation das größere Übel."""
    import os as _os
    _os.environ["SENTINEL_SHIELD"] = "1"
    import nc.shield as S

    evasions = [
        "s\u200bieg h\u200beil",
        "\u0455\u0456\u0435g h\u0435\u0456l",
        "s.i.e.g h.e.i.l",
        "s\u00ed\u00e9g h\u00e9\u00edl",
        "h-e-i-l h-i-t-l-e-r",
        "k\u200by\u200bs",
    ]
    for e in evasions:
        assert S._sentinel_screen(e) is not None, f"Umgehung nicht gefangen: {e!r}"
    ok("shield: Umgehungen (Homoglyph/ZeroWidth/Akzent/Trenner) gefangen")

    safe = [
        "hey wie gehts euch heute", "der stream ist mega geil danke",
        "ich hei\u00dfe Sieglinde und wohne in Berlin",
        "das kostet 1488 euro glaube ich", "heiliger strohsack war das knapp",
        "gut gemacht leute weiter so", "meine e-mail steht im profil",
        "schau mal 3.5 sterne daf\u00fcr", "super-cool das ganze",
    ]
    for s in safe:
        r = S._sentinel_screen(s)
        assert r is None, f"FALSE POSITIVE bei harmloser Nachricht: {s!r} → {r}"
    ok("shield: 0 False Positives bei harmlosen Nachrichten")

    assert " " in S._shield_normalize("gut gemacht leute"), \
        "normale Leerzeichen dürfen nicht verschwinden"
    ok("shield: normale Wortgrenzen bleiben erhalten")


def _test_recdb():
    """Welle 1 der Zerlegung (v4.0-W104): die Aufnahmen-DB-Zugriffe liegen jetzt
       in nc.recdb, bot_v37 haelt nur noch Delegationen. Geprueft wird beides —
       dass das Modul arbeitet UND dass der Monolith wirklich delegiert, statt
       eine zweite Kopie der Logik zu behalten."""
    import sqlite3, tempfile, os as _os
    from nc import recdb, dbwrap

    db = _os.path.join(tempfile.mkdtemp(), "rec.sqlite")
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE recordings (id INTEGER PRIMARY KEY, username TEXT, filepath TEXT,
            file_size INT, duration_secs INT, created_at TEXT, deleted_at TEXT,
            fingerprint TEXT);
        CREATE TABLE recording_notes (recording_id INT, note TEXT);
        CREATE TABLE recording_annotations (id INTEGER PRIMARY KEY, recording_id INT,
            timestamp_secs INT, label TEXT, created_at TEXT);
        CREATE TABLE bookmarks (recording_id INT, created_at TEXT);
        INSERT INTO recordings (id, username, filepath, deleted_at)
            VALUES (1, 'a', '/x.mp4', NULL), (2, 'b', '/y.mp4', '2026-01-01');
        INSERT INTO recording_notes VALUES (1, 'Notiz');
        INSERT INTO recording_annotations VALUES (1, 1, 42, 'Marke', '2026-01-01');
    """)
    con.commit(); con.close()
    dbwrap.configure_db(db_path=db, backend="sqlite")

    # Soft-Delete-Filter: die geloeschte #2 darf nicht auftauchen
    rows = recdb.get_all_recordings(limit=10)
    assert [r["id"] for r in rows] == [1], [r["id"] for r in rows]
    assert [r["id"] for r in recdb.get_all_recordings(limit=10, include_deleted=True)] == [2, 1]
    ok("recdb.get_all_recordings filtert Soft-Delete")

    assert recdb.get_recording_by_id(1)["username"] == "a"
    assert recdb.get_recording_note(1) == "Notiz"
    assert recdb.get_recording_note(999) is None
    assert len(recdb.get_annotations_for_recording(1)) == 1
    assert [r["id"] for r in recdb.get_trash_recordings()] == [2]
    ok("recdb: by_id, note, annotations, trash")

    # Papierkorb: der Rundlauf muss den Soft-Delete-Zustand wirklich umschalten
    seen = []
    recdb.configure(log_event=lambda *a, **k: seen.append(a[0]))
    assert recdb.soft_delete_recording(1) is True
    assert recdb.get_all_recordings(limit=10) == []
    assert recdb.restore_recording(1) is True
    assert [r["id"] for r in recdb.get_all_recordings(limit=10)] == [1]
    assert recdb.soft_delete_recording(999) is False, "nicht vorhandene ID darf nicht True melden"
    assert seen == ["recording.trashed", "recording.restored"], seen
    ok("recdb: Papierkorb-Rundlauf + log_event-Injection")

    # Ohne Injection darf nichts sterben — der Default ist ein No-Op, keine Ausnahme.
    import importlib
    fresh = importlib.reload(recdb)
    assert fresh.soft_delete_recording(1) is True, "ohne log_event-Injection gestorben"
    fresh.restore_recording(1)
    ok("recdb bleibt ohne log_event-Injection funktionsfaehig")

    # Fehlerpfad: eine fehlende Tabelle gibt [] zurueck, keinen 500er im Dashboard
    assert recdb.get_manual_recordings() == []
    assert recdb.get_bookmarked_recordings(limit=5) == []
    ok("recdb: fehlende Tabelle -> leere Liste statt Ausnahme")

    # --- und der Monolith delegiert wirklich ---
    src = open("bot_v37.py", encoding="utf-8").read()
    assert "from nc import recdb as _nc_recdb" in src, "recdb nicht importiert"
    assert "_nc_recdb.configure(log_event=log_event)" in src, "log_event nicht injiziert"
    for fn in ("get_all_recordings", "get_recording_by_id", "soft_delete_recording",
               "restore_recording", "get_trash_recordings", "get_manual_recordings",
               "get_recording_note", "get_annotations_for_recording",
               "get_bookmarked_recordings", "get_recent_recording_attempts",
               "update_recording_fingerprint", "find_recordings_by_fingerprint",
               "get_or_compute_inspect_sync"):
        assert ("return _nc_recdb.%s(" % fn) in src, "%s delegiert nicht" % fn
    # Kein Rumpf-Rest: die SQL darf nur noch im Modul stehen, sonst laufen die
    # beiden Kopien mit der Zeit auseinander.
    assert "SELECT * FROM recordings WHERE deleted_at IS NULL" not in src, \
        "alte SQL noch im Monolithen — Doppel-Logik"
    ok("bot_v37 delegiert an nc.recdb (13 Funktionen, keine Doppel-Logik)")


def _test_routes_recordings():
    """Welle 2 der Zerlegung (v4.0-W106): die 34 Aufnahmen-Routen liegen als
       Flask-Blueprint in nc/routes/recordings.py. Geprueft wird, dass das
       Blueprint fuer sich allein funktioniert (ohne Bot), dass der Kontext
       laut scheitert statt still None zu liefern, und dass im Monolithen keine
       zweite Kopie zurueckgeblieben ist."""
    import importlib
    from flask import Flask
    from nc import ctx as ncctx
    from nc.routes import recordings as rt

    # (1) Die Pfade muessen WOERTLICH die alten sein — ein url_prefix waere die
    # stille Verhaltensaenderung, die alle Dashboard-Aufrufe bricht.
    app = Flask(__name__)
    app.register_blueprint(rt.bp)
    rules = {str(r.rule) for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert len(rules) == 34, "34 Routen erwartet, %d registriert" % len(rules)
    for want in ("/api/recordings/list", "/api/recordings/daily",
                 "/api/recordings/<int:rid>/manifest", "/api/recordings/trash",
                 "/api/rec/orphans", "/api/rec/quality/<int:rec_id>"):
        assert want in rules, "Pfad fehlt oder umbenannt: %s" % want
    assert not any(r.startswith("/recordings") for r in rules), \
        "url_prefix gesetzt — die Pfade haben sich verschoben"
    ok("routes.recordings: 34 Routen, Pfade woertlich unveraendert")

    # (2) Endpunkt-Namen sind blueprint-qualifiziert. Das ist die EINZIGE
    # erlaubte Aenderung — sie ist folgenlos, weil es im Projekt kein url_for gibt.
    eps = {r.endpoint for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert all(e.startswith("recordings.") for e in eps), sorted(eps)[:3]
    for f in ("bot_v37.py", "templates/dashboard.html", "website/lafap_index.html"):
        assert "url_for(" not in open(f, encoding="utf-8").read(), \
            "%s benutzt url_for — Endpunkt-Umbenennung waere jetzt ein Bruch" % f
    ok("routes.recordings: Endpunkte qualifiziert, weiterhin kein url_for im Projekt")

    # (3) Ohne configure() muss der Kontext LAUT scheitern. Ein stiller
    # None-Kontext waere der CLAUDE.md-Fehler eine Ebene hoeher: die Route
    # liefe, taete aber nichts.
    fresh = importlib.reload(ncctx)
    assert fresh.is_configured() is False
    try:
        fresh.get()
        raise AssertionError("nc.ctx.get() schweigt ohne configure()")
    except RuntimeError as e:
        assert "configure" in str(e), e
    ok("nc.ctx: get() ohne configure() scheitert laut, nicht still")

    # (4) __slots__ ist die Bremse gegen das Sammelbecken — ein vertippter oder
    # neuer Schluessel muss sofort auffliegen, nicht erst beim ersten Aufruf.
    try:
        fresh.configure(gibtsnicht=1)
        raise AssertionError("unbekannter ctx-Schluessel wurde stillschweigend geschluckt")
    except AttributeError:
        pass
    ok("nc.ctx: unbekannter Schluessel fliegt sofort auf (__slots__)")

    # (5) Und der Monolith haelt keine zweite Kopie.
    src = open("bot_v37.py", encoding="utf-8").read()
    assert "from nc.routes import recordings as _nc_routes_recordings" in src
    assert "dashboard_app.register_blueprint(_nc_routes_recordings.bp)" in src, \
        "Blueprint nicht registriert"
    assert "_nc_ctx.configure(" in src, "Laufzeitkontext nicht verdrahtet"
    for gone in ('@dashboard_app.route("/api/recordings/list")',
                 "def api_recordings_list", "def compute_waveform_peaks",
                 "def build_recording_manifest", "def _find_orphans"):
        assert gone not in src, "Doppel-Logik: %s noch im Monolithen" % gone
    ok("bot_v37 registriert nur noch — keine Aufnahmen-Route mehr im Monolithen")


def _test_routes_archive():
    """Welle 3 der Zerlegung (v4.0-W107): elf Archiv-Routen als Blueprint.
       Dieselben Zusicherungen wie fuer recordings — plus die neue cfg-Bruecke,
       die verhindert, dass nc/ctx.py zum Konfigurations-Abladeplatz wird."""
    from flask import Flask
    from nc.routes import archive as rt

    app = Flask(__name__)
    app.register_blueprint(rt.bp)
    rules = {str(r.rule) for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert len(rules) == 11, "11 Routen erwartet, %d registriert" % len(rules)
    for want in ("/api/archive", "/api/archive/upload", "/api/archive/search",
                 "/api/archive/<int:eid>", "/api/archive/duplicates"):
        assert want in rules, "Pfad fehlt oder umbenannt: %s" % want
    assert all(r.endpoint.startswith("archive.")
               for r in app.url_map.iter_rules() if r.endpoint != "static")
    ok("routes.archive: 11 Routen, Pfade woertlich unveraendert")

    # Konfiguration laeuft ueber cfg, NICHT ueber eigene Env-Lesepfade: der Bot
    # friert diese Werte beim Import ein, ein zweiter Lesepfad im Blueprint waere
    # eine stille Verhaltensaenderung gegenueber dem Monolithen.
    src_rt = open("nc/routes/archive.py", encoding="utf-8").read()
    assert 'cfg["ARCHIVE_DIR"]' in src_rt, "ARCHIVE_DIR nicht ueber cfg"
    # GENAU EIN roher Env-Zugriff ist erlaubt, und zwar der, der schon im
    # Monolithen stand (api_archive_duplicates liest ARCHIVE_DIR als Fallback
    # nochmal selbst, obwohl der Bot den Wert oben bereits einfriert). Das ist
    # eine Altlast, kein neuer Lesepfad — sie wurde beim Verschieben bewusst
    # NICHT "nebenbei repariert", weil Verhalten und Ort nie in derselben Welle
    # geaendert werden. Der Zaehler haelt fest, dass nicht mehr dazukommen.
    assert src_rt.count('os.getenv("ARCHIVE') == 1, (
        "neuer roher Env-Lesepfad im Blueprint (%d statt 1)"
        % src_rt.count('os.getenv("ARCHIVE'))
    ok("routes.archive: Konfiguration ueber ctx.cfg, nur die bekannte Altlast bleibt")

    # Und der Monolith haelt keine zweite Kopie.
    src = open("bot_v37.py", encoding="utf-8").read()
    assert "from nc.routes import archive as _nc_routes_archive" in src
    assert "dashboard_app.register_blueprint(_nc_routes_archive.bp)" in src
    for gone in ('@dashboard_app.route("/api/archive")', "def api_archive_upload",
                 "def rename_archive_entry", "def get_archive_aggregate_stats"):
        assert gone not in src, "Doppel-Logik: %s noch im Monolithen" % gone
    ok("bot_v37 registriert nur noch — keine Archiv-Route mehr im Monolithen")

    # Die Obergrenze fuer nc.ctx prueft _test_routes_alle_blueprints zentral.


def _test_routes_alle_blueprints():
    """W108: ab hier gilt der Vertrag GENERISCH fuer jedes Modul in nc/routes/.

       Frueher bekam jedes Blueprint seinen eigenen Testblock — bei dreizehn
       geplanten waere das dreizehnmal dieselbe Zusicherung in leicht anderer
       Schreibweise. Was fuer alle gilt, wird hier einmal geprueft; nur
       Besonderheiten einzelner Module stehen weiter in eigenen Tests."""
    import glob as _glob
    import importlib
    from flask import Flask

    module = sorted(_os_basename(p) for p in _glob.glob("nc/routes/*.py")
                    if not p.endswith("__init__.py"))
    assert module, "keine Blueprints gefunden"
    src = open("bot_v37.py", encoding="utf-8").read()

    gesamt = 0
    for name in module:
        mod = importlib.import_module("nc.routes." + name)
        assert hasattr(mod, "bp"), "%s hat kein bp" % name

        app = Flask(__name__)
        app.register_blueprint(mod.bp)
        regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
        assert regeln, "%s registriert keine Route" % name
        gesamt += len(regeln)

        # (1) Pfade woertlich: ein url_prefix wuerde jeden Dashboard-Aufruf brechen.
        for r in regeln:
            assert str(r.rule).startswith("/api/"), \
                "%s: Pfad nicht mehr unter /api/ — url_prefix gesetzt? %s" % (name, r.rule)
        # (2) Endpunkte blueprint-qualifiziert.
        assert all(r.endpoint.startswith(name + ".") for r in regeln), \
            "%s: Endpunkt nicht qualifiziert" % name
        # (3) Der Bot registriert es wirklich — sonst waere die Route weg.
        assert "register_blueprint(_nc_routes_%s.bp)" % name in src, \
            "%s nicht in bot_v37 registriert" % name
        # (4) Architektur-Grenze: kein Rueckimport aus dem Monolithen. Geprueft
        # wird ueber den AST, nicht ueber den Text — "aus bot_v37 geloest" steht
        # voellig zu Recht in jedem Docstring und ist kein Verstoss.
        import ast as _ast
        quelle = open("nc/routes/%s.py" % name, encoding="utf-8").read()
        for _n in _ast.walk(_ast.parse(quelle)):
            if isinstance(_n, _ast.Import):
                assert all(not al.name.startswith("bot_v37") for al in _n.names), \
                    "%s importiert aus bot_v37" % name
            elif isinstance(_n, _ast.ImportFrom):
                assert not (_n.module or "").startswith("bot_v37"), \
                    "%s importiert aus bot_v37" % name
        # (5) Keine app-weiten Hooks mitgewandert — als Blueprint-Hook wuerden
        # sie nur noch fuer ihr Blueprint gelten, eine stille Verhaltensaenderung.
        for hook in ("@bp.before_request", "@bp.after_request", "@bp.errorhandler"):
            assert hook not in quelle, "%s: %s gehoert auf die App" % (name, hook)
        # (6) Query-Parameter gehaertet, kein rohes int(request.args...).
        assert "int(request.args.get" not in quelle, \
            "%s: roher Query-Parser (Flask-500-Risiko)" % name
    ok("nc/routes: %d Blueprints, %d Routen — Pfade, Endpunkte, Grenze, Hooks, Parser"
       % (len(module), gesamt))

    # url_for bleibt projektweit verboten: es ist der einzige Grund, warum die
    # Endpunkt-Umbenennung durch Blueprints folgenlos ist.
    for f in ("bot_v37.py", "templates/dashboard.html", "website/lafap_index.html"):
        assert "url_for(" not in open(f, encoding="utf-8").read(), \
            "%s benutzt url_for — Blueprint-Umbenennung waere jetzt ein Bruch" % f
    ok("weiterhin kein url_for im Projekt")

    # Der Kontext bleibt klein, sonst ist die Grenze weg, die er sich setzt.
    from nc import ctx as ncctx
    assert len(ncctx.Ctx.__slots__) <= 25, (
        "nc.ctx waechst zum Sammelbecken: %d Slots" % len(ncctx.Ctx.__slots__))
    ok("nc.ctx: %d Slots, Obergrenze eingehalten" % len(ncctx.Ctx.__slots__))


def _os_basename(p):
    import os as _os
    return _os.path.basename(p)[:-3]


def _test_routes_health():
    """W110: /api/health-score und /api/system-resources als ein Blueprint.

       Zwei Praefixe, EIN Thema (Systemzustand) — deshalb ein Modul statt zwei
       Ein-Routen-Dateien. Der Vertrag haelt die zwei Fallen fest, die hier
       zugeschlagen haben."""
    from nc import ctx as ncctx

    # (1) Die Startzeit MUSS spaet gelesen werden. _BOT_START_TIME ist beim
    # Import None und wird erst in main() gesetzt; ein beim Start uebergebener
    # Wert waere fuer immer None und die Uptime staende ewig auf 0.
    assert "get_bot_start_time" in ncctx.Ctx.__slots__, "Startzeit-Getter fehlt im Kontext"
    assert "bot_start_time" not in [x for x in ncctx.Ctx.__slots__ if x != "get_bot_start_time"], \
        "Startzeit wieder als Wert im Kontext — friert beim Import ein"
    q = open("nc/routes/health.py", encoding="utf-8").read()
    assert "_c().get_bot_start_time()" in q, "Blueprint liest die Startzeit nicht als Getter"
    src = open("bot_v37.py", encoding="utf-8").read()
    assert "get_bot_start_time=lambda: _BOT_START_TIME" in src, \
        "Bot reicht die Startzeit nicht als Getter durch"

    # (2) Beide Routen ruft der Bot auch INTERN auf (Telegram /sysres und die
    # Aggregat-Route). Nach dem Umzug muessen sie importiert sein, sonst
    # sterben diese Pfade mit NameError — statisch sichtbar, aber leicht zu
    # uebersehen.
    assert "from nc.routes.health import api_health_score, api_system_resources" in src, \
        "interne Aufrufer verlieren die Funktionen"
    ok("routes.health: Startzeit als Getter, interne Aufrufer versorgt")


def main():
    tmp = tempfile.mkdtemp()
    configure_db(db_path=os.path.join(tmp, "t.db"), backend="sqlite")

    with db_conn() as c:
        cur = c.cursor()
        for stmt in [s.strip() for s in _extract_schema().split(";") if s.strip()]:
            cur.execute(stmt)
        cur.execute("INSERT INTO recordings (username, filepath, created_at) "
                    "VALUES (?,?,?)",
                    ("helge_72", os.path.join(tmp, "x.mp4"),
                     "2026-07-17T02:00:00"))
        rid = cur.lastrowid
    open(os.path.join(tmp, "x.mp4"), "wb").write(b"0" * 5000)
    ok("db_conn aus nc.dbwrap: echtes Schema angelegt, Commit durchgelaufen")

    # --- Rollback-Vertrag: Exception im with-Block darf nichts schreiben ---
    try:
        with db_conn() as c:
            c.cursor().execute("INSERT INTO recordings (username, filepath, "
                               "created_at) VALUES (?,?,?)",
                               ("rollback", "/x", "2026-01-01T00:00:00"))
            raise RuntimeError("absichtlich")
    except RuntimeError:
        pass
    with db_conn() as c:
        cur = c.cursor()
        cur.execute("SELECT COUNT(*) AS n FROM recordings")
        assert cur.fetchone()["n"] == 1, "Rollback fehlgeschlagen"
    ok("db_conn: Rollback bei Exception, Commit bei sauberem Austritt")

    # --- nc.notes ---
    assert notes.set_recording_note(rid, "AZRAEL-Test") is True
    with db_conn() as c:
        cur = c.cursor()
        cur.execute("SELECT note FROM recording_notes WHERE recording_id=?",
                    (rid,))
        assert cur.fetchone()["note"] == "AZRAEL-Test"
    ok("notes.set_recording_note schreibt in recording_notes")

    a = notes.toggle_bookmark(rid)
    b = notes.toggle_bookmark(rid)
    assert a["bookmarked"] is True and b["bookmarked"] is False, (a, b)
    ok("notes.toggle_bookmark schaltet um")

    aid = notes.add_annotation(rid, 42, "AZRAEL reagiert")
    assert aid == 1 and notes.delete_annotation(aid) is True
    ok("notes.add_annotation / delete_annotation")

    assert notes._conv_list(limit=5) is not None
    ok("notes._conv_list")

    # --- nc.stats ---
    d = stats._dir_stats(tmp)
    assert d["exists"] and d["file_count"] >= 1, d
    ok("stats._dir_stats (%d Dateien)" % d["file_count"])

    assert isinstance(stats.get_per_user_stats(), list)
    ok("stats.get_per_user_stats")
    assert isinstance(stats.get_lives_heatmap("helge_72"), dict)
    ok("stats.get_lives_heatmap")
    assert isinstance(stats.get_recordings_heatmap(), dict)
    ok("stats.get_recordings_heatmap")
    assert isinstance(stats.get_activity_pulse(minutes=60), list)
    ok("stats.get_activity_pulse")

    # --- nc.archive ---
    fp = archive.compute_recording_fingerprint(os.path.join(tmp, "x.mp4"))
    assert fp and len(fp) > 16, fp
    ok("archive.compute_recording_fingerprint")

    assert archive.evaluate_archive_rule(
        {"field": "username", "op": "eq", "value": "helge_72"},
        {"username": "helge_72"}) in (True, False)
    ok("archive.evaluate_archive_rule")

    assert archive.get_archive_entries_paged() is not None
    ok("archive.get_archive_entries_paged")

    _test_shield_harden()

    _test_dbexport()

    _test_procdiag()

    _test_recdb()

    _test_routes_recordings()

    _test_routes_archive()

    _test_routes_alle_blueprints()

    _test_routes_health()

    print("test_nc_modules OK \u2014 %d Vertraege gruen" % PASS)


if __name__ == "__main__":
    main()
