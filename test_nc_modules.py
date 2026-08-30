"""test_nc_modules — die aus bot.py extrahierten nc-Module laufen
eigenstaendig gegen das ECHTE Bot-Schema.

Das Schema wird zur Laufzeit AUS bot.py gezogen (Klammer-Zaehlung, keine
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

# Werte aus dem SQLite-Zweig von _init_db() (bot.py)
PLACEHOLDERS = {"txt_idx": "TEXT", "txt_long": "TEXT", "txt_big": "TEXT",
                "ts": "TEXT",   # v4.0-W79: indizierter Timestamp (SQLite=TEXT, MariaDB=VARCHAR(64))
                "iv": "INTEGER", "tbl_opts": "",
                "pk": "INTEGER PRIMARY KEY AUTOINCREMENT"}

PASS = 0


def ok(msg):
    global PASS
    PASS += 1
    print("  \u2713 " + msg)


def _ist_monolith(modul: str) -> bool:
    """Zeigt der Modulname auf bot.py? Exakt oder als Paket-Praefix.

    Nach der Umbenennung von bot.py zu bot ist ein reiner startswith("bot")
    zu grob — er wuerde jedes Modul treffen, dessen Name so beginnt."""
    return modul == "bot" or modul.startswith("bot.")


def _extract_schema():
    """CREATE TABLE aus bot.py ziehen — Klammern zaehlen, nicht raten."""
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
       nc.procdiag; bot.py hält nur dünne Wrapper. Verhalten muss identisch sein."""
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
    src = open("bot.py").read()
    assert "from nc import procdiag as _nc_procdiag" in src, "procdiag nicht importiert"
    assert "_nc_procdiag.zombie_child_count()" in src, "Wrapper delegiert nicht"
    ok("bot.py delegiert an nc.procdiag")

    # Phase-1-Zerlegung: ffmpeg-Clip-Helfer nach nc.ffdiag konsolidiert
    from nc import ffdiag
    assert ffdiag.ffprobe_duration("/nonexistent_xyz.mp4") == 0.0
    assert ffdiag.clip_caption_escape("a: 'b' 100% \\ c") == "a b 100 c"
    assert len(ffdiag.clip_caption_escape("x" * 200)) == 70
    ok("ffdiag.ffprobe_duration + clip_caption_escape (aus bot.py gelöst)")
    assert "clip_caption_escape as _clip_caption_escape" in src, "Clip-Escape nicht konsolidiert importiert"
    assert "def _clip_caption_escape(s):" not in src, "alter Rumpf noch im Monolith"
    ok("bot.py nutzt konsolidierte ffdiag-Clip-Helfer")

    # Phase-1-Zerlegung: Login-Seite nach nc.loginpage
    from nc import loginpage
    _pg = loginpage.login_page("Falsches PIN.", "/betrieb")
    assert "<form" in _pg and "Falsches PIN." in _pg and "value='/betrieb'" in _pg
    assert "&lt;script&gt;" in loginpage.login_page("<script>", "/"), "Login-Seite escaped nicht"
    assert "login_page as _login_page" in src and "def _login_page(" not in src, "Login-Seite nicht ausgelagert"
    ok("nc.loginpage.login_page (aus bot.py gelöst, XSS-sicher)")


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
       in nc.recdb, bot.py haelt nur noch Delegationen. Geprueft wird beides —
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
    src = open("bot.py", encoding="utf-8").read()
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
    ok("bot.py delegiert an nc.recdb (13 Funktionen, keine Doppel-Logik)")


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
    for f in ("bot.py", "templates/dashboard.html", "website/lafap_index.html"):
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
    src = open("bot.py", encoding="utf-8").read()
    assert "from nc.routes import recordings as _nc_routes_recordings" in src
    assert "dashboard_app.register_blueprint(_nc_routes_recordings.bp)" in src, \
        "Blueprint nicht registriert"
    assert "_nc_ctx.configure(" in src, "Laufzeitkontext nicht verdrahtet"
    for gone in ('@dashboard_app.route("/api/recordings/list")',
                 "def api_recordings_list", "def compute_waveform_peaks",
                 "def build_recording_manifest", "def _find_orphans"):
        assert gone not in src, "Doppel-Logik: %s noch im Monolithen" % gone
    ok("bot.py registriert nur noch — keine Aufnahmen-Route mehr im Monolithen")


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
    src = open("bot.py", encoding="utf-8").read()
    assert "from nc.routes import archive as _nc_routes_archive" in src
    assert "dashboard_app.register_blueprint(_nc_routes_archive.bp)" in src
    for gone in ('@dashboard_app.route("/api/archive")', "def api_archive_upload",
                 "def rename_archive_entry", "def get_archive_aggregate_stats"):
        assert gone not in src, "Doppel-Logik: %s noch im Monolithen" % gone
    ok("bot.py registriert nur noch — keine Archiv-Route mehr im Monolithen")

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
    src = open("bot.py", encoding="utf-8").read()

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
            "%s nicht in bot.py registriert" % name
        # (4) Architektur-Grenze: kein Rueckimport aus dem Monolithen. Geprueft
        # wird ueber den AST, nicht ueber den Text — "aus bot.py geloest" steht
        # voellig zu Recht in jedem Docstring und ist kein Verstoss.
        # Seit der Umbenennung heisst das Modul schlicht "bot": auf Praefix zu
        # pruefen wuerde jedes kuenftige Modul mit diesem Wortanfang faelschlich
        # treffen, deshalb exakt oder als Paket-Praefix "bot.".
        import ast as _ast
        quelle = open("nc/routes/%s.py" % name, encoding="utf-8").read()
        for _n in _ast.walk(_ast.parse(quelle)):
            if isinstance(_n, _ast.Import):
                assert all(not _ist_monolith(al.name) for al in _n.names), \
                    "%s importiert aus bot.py" % name
            elif isinstance(_n, _ast.ImportFrom):
                assert not _ist_monolith(_n.module or ""), \
                    "%s importiert aus bot.py" % name
        # (5) Keine app-weiten Hooks mitgewandert — als Blueprint-Hook wuerden
        # sie nur noch fuer ihr Blueprint gelten, eine stille Verhaltensaenderung.
        for hook in ("@bp.before_request", "@bp.after_request", "@bp.errorhandler"):
            assert hook not in quelle, "%s: %s gehoert auf die App" % (name, hook)
        # (6) Query-Parameter gehaertet, kein rohes int(request.args...).
        assert "int(request.args.get" not in quelle, \
            "%s: roher Query-Parser (Flask-500-Risiko)" % name
    ok("nc/routes: %d Blueprints, %d Routen — Pfade, Endpunkte, Grenze, Hooks, Parser"
       % (len(module), gesamt))

    # (7) Jeder cfg-Schluessel, den ein Blueprint liest, muss auch geliefert
    # werden. Ein fehlender faellt NICHT beim Start auf, sondern erst beim
    # Aufruf der Route — als KeyError im 500er. Genau so ist in W112
    # /api/ai/forecast-storage gestorben.
    import re as _re
    _i = src.index("    cfg={")
    _j = src.index("    },", _i)
    _geliefert = set(_re.findall(r'"([A-Za-z_][A-Za-z0-9_]*)":', src[_i:_j]))
    for name in module:
        quelle = open("nc/routes/%s.py" % name, encoding="utf-8").read()
        # Doc-/Kommentarzeilen raus: dort steht cfg["NAME"] als Platzhalter.
        code = "\n".join(ln for ln in quelle.splitlines()
                         if not ln.lstrip().startswith("#"))
        code = code.split('"""')
        code = "".join(code[0::2]) if len(code) > 1 else quelle
        gebraucht = set(_re.findall(r'cfg\["([^"]+)"\]', code))
        fehlt = gebraucht - _geliefert
        assert not fehlt, "%s liest cfg-Schluessel, die der Bot nicht liefert: %s" % (
            name, sorted(fehlt))
    ok("cfg: jeder gelesene Schluessel wird auch geliefert (%d Schluessel)" % len(_geliefert))

    # url_for bleibt projektweit verboten: es ist der einzige Grund, warum die
    # Endpunkt-Umbenennung durch Blueprints folgenlos ist.
    for f in ("bot.py", "templates/dashboard.html", "website/lafap_index.html"):
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
    src = open("bot.py", encoding="utf-8").read()
    assert "get_bot_start_time=lambda: _BOT_START_TIME" in src, \
        "Bot reicht die Startzeit nicht als Getter durch"

    # (2) Beide Routen ruft der Bot auch INTERN auf (Telegram /sysres und die
    # Aggregat-Route). Nach dem Umzug muessen sie importiert sein, sonst
    # sterben diese Pfade mit NameError — statisch sichtbar, aber leicht zu
    # uebersehen.
    assert "from nc.routes.health import api_health_score, api_system_resources" in src, \
        "interne Aufrufer verlieren die Funktionen"
    ok("routes.health: Startzeit als Getter, interne Aufrufer versorgt")


def _test_cfgstore_und_claude():
    """W111: Vorarbeit fuer das /api/ai-Blueprint. Fuenf Funktionen, die reiner
       app_config-Zugriff bzw. Anthropic-Belang sind, lagen im Monolithen und
       waeren dort zu fuenf Kontext-Eintraegen geworden. Sie liegen jetzt in
       den Modulen, die genau dafuer da sind."""
    import sqlite3, tempfile, os as _os
    from nc import cfgstore, claude, dbwrap

    db = _os.path.join(tempfile.mkdtemp(), "cfg.sqlite")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE app_config (k TEXT UNIQUE, v TEXT, updated_at TEXT)")
    con.commit(); con.close()
    dbwrap.configure_db(db_path=db, backend="sqlite")

    assert cfgstore.get("fehlt", "vorgabe") == "vorgabe"
    cfgstore.set_("ai.x", {"a": 1})
    assert cfgstore.get("ai.x") == {"a": 1}
    cfgstore.set_("ai.x", {"a": 2})                     # Upsert-Pfad
    assert cfgstore.get("ai.x") == {"a": 2}, "Upsert hat nicht aktualisiert"
    ok("cfgstore: get/set_ inkl. Upsert gegen echtes SQLite")

    # Anthropic: app_config hat Vorrang vor der Umgebung.
    _os.environ["ANTHROPIC_MODEL"] = "claude-aus-der-env"
    assert claude.model_raw() == "claude-aus-der-env"
    cfgstore.set_("ai.anthropic_model", "claude-aus-der-db")
    assert claude.model_raw() == "claude-aus-der-db", "app_config hat keinen Vorrang"
    # Ein abgeschalteter Pin wird angehoben, statt still auf 404 zu laufen.
    assert claude.model("claude-3-5-haiku-latest") == claude.DEFAULT_MODEL
    _os.environ.pop("ANTHROPIC_MODEL", None)
    ok("claude: Modellwahl (app_config > env > Default) + Retired-Anhebung")

    # Und der Monolith delegiert, statt eine zweite Kopie zu halten.
    src = open("bot.py", encoding="utf-8").read()
    for fn, ziel in (("_cfg_get", "_nc_cfgstore.get(key, default)"),
                     ("_cfg_set", "_nc_cfgstore.set_(key, value)"),
                     ("_anthropic_key", "_nc_claude.api_key()"),
                     ("_anthropic_model", "_nc_claude.model(override)")):
        assert ("return " + ziel) in src, "%s delegiert nicht" % fn
    assert "_ANTHROPIC_MODEL_WARNED" not in src, "alter Warn-Cache noch im Monolithen"
    # model_raw braucht der Bot selbst nicht mehr — es wanderte mit den
    # /api/ai-Routen ins Blueprint und wird dort direkt aus nc.claude
    # importiert, statt ueber eine zweite Huelle zu laufen.
    assert "model_raw as _anthropic_model_raw" in open(
        "nc/routes/ai.py", encoding="utf-8").read(), "Blueprint importiert model_raw nicht direkt"
    ok("bot.py delegiert cfg-Zugriff und Anthropic-Modellwahl")


def _test_routes_ai():
    """W112: die 24 /api/ai-Routen als Blueprint — der groesste Einzelumzug
       (1.125 Zeilen). Die generischen Zusicherungen deckt
       _test_routes_alle_blueprints ab; hier stehen die Besonderheiten."""
    from flask import Flask
    from nc.routes import ai as rt

    app = Flask(__name__)
    app.register_blueprint(rt.bp)
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 24, "24 Regeln erwartet, %d" % len(regeln)
    ok("routes.ai: 24 Regeln registriert")

    q = open("nc/routes/ai.py", encoding="utf-8").read()

    # (1) Der SQL-Wachhund und die Read-only-Verbindung MUESSEN mitgewandert
    # sein — /api/ai/query fuehrt vom Nutzer erzeugtes SQL aus. Ohne beides
    # waere die Zerlegung ein Sicherheitsrueckschritt.
    assert "_nc_sqlguard.check_readonly(" in q, "SQL-Wachhund fehlt im Blueprint"
    assert "?mode=ro" in q and "uri=True" in q, "keine Read-only-Verbindung"

    # (2) Vier Namen kommen direkt aus nc/, nicht ueber den Laufzeitkontext.
    # Sie waeren sonst vier Slots gewesen, obwohl sie reiner Modulzugriff sind.
    for imp in ("from nc.claude import", "from nc.cfgstore import get as _cfg_get",
                "from nc.aidb import conv_messages", "from nc.notes import _conv_list"):
        assert imp in q, "Direktimport fehlt: " + imp
    assert "_c().cfg[" in q, "Konfiguration laeuft nicht ueber ctx.cfg"

    # (3) Und der Monolith haelt keine zweite Kopie der KI-Routen.
    src = open("bot.py", encoding="utf-8").read()
    for gone in ('@dashboard_app.route("/api/ai/ask")', "def api_ai_ask",
                 "def llm_chat_stream_sync", "def _nl_to_sql", "def _safe_select"):
        assert gone not in src, "Doppel-Logik: %s noch im Monolithen" % gone
    ok("routes.ai: SQL-Wachhund + Read-only mitgewandert, Direktimporte statt ctx")


def _test_restream_stability():
    """v4.0-W113: die Wiederanlauf-Regeln des Restreams.

    Diese Logik lag vorher in RestreamManager._monitor und war damit nur mit
    laufendem ffmpeg, laufender DB und laufendem Event-Loop erreichbar — also
    faktisch ungeprueft. Zwei der fuenf Regeln waren nachweislich falsch
    gesetzt; genau die stehen hier zuerst.
    """
    import nc.restream_stability as rs

    pol = rs.ReconnectPolicy()

    # 1) Budget-Rueckgabe — DER Befund. Vorher wanderte `attempts` von
    #    Reconnect zu Reconnect weiter; ein Restream, der stundenlang lief und
    #    fuenfmal stolperte, galt danach als aufgegeben.
    assert rs.budget_after_run(4, 3600.0, pol) == 0
    assert rs.budget_after_run(4, 10.0, pol) == 4
    assert rs.budget_after_run(0, 10.0, pol) == 0
    # Lang gelaufen, aber nichts gesendet (Stillstands-Kill): KEIN Nachschlag,
    # sonst haemmert der Bot gegen einen toten Ingest ewig im Grundtakt.
    assert rs.budget_after_run(4, 3600.0, pol, progressed=False) == 4
    assert rs.budget_exhausted(5, pol) and not rs.budget_exhausted(4, pol)
    ok("restream_stability: Reconnect-Budget kommt nach gesundem Lauf zurueck")

    # 2) Backoff — exponentiell, gedeckelt, gestreut. Ohne Streuung kehren
    #    alle gleichzeitig gestorbenen Restreams im Gleichschritt zurueck.
    for n in range(0, 12):
        d = rs.reconnect_delay(n, pol)
        assert 1.0 <= d <= pol.max_delay_s, (n, d)
    fest = rs.ReconnectPolicy(jitter=0.0)
    assert rs.reconnect_delay(0, fest) == 8.0
    assert rs.reconnect_delay(1, fest) == 16.0
    assert rs.reconnect_delay(2, fest) == 32.0
    assert rs.reconnect_delay(9, fest) == 60.0          # Deckel greift
    gestreut = {rs.reconnect_delay(1, pol) for _ in range(40)}
    assert len(gestreut) > 1, "Backoff streut nicht — Gleichschritt bleibt"
    ok("restream_stability: Backoff exponentiell, gedeckelt und gestreut")

    # 3) Ablauf der Quell-URL — schnell bleiben beim Normalfall, bremsen bei
    #    der Schleife. Vorher: 2s, kein Fehlversuch, ohne jede Untergrenze.
    assert rs.expired_streak(5, 400.0, pol) == 0        # Minuten gelaufen = normal
    assert rs.expired_streak(0, 0.4, pol) == 1
    assert rs.expired_streak(3, 0.4, pol) == 4
    assert rs.expired_delay(0, pol) == 2.0
    assert rs.expired_delay(99, pol) == pol.expired_delays_s[-1]
    assert not rs.expired_is_spinning(0, pol)
    assert rs.expired_is_spinning(len(pol.expired_delays_s), pol)
    # Die Verzoegerung waechst monoton — nie schneller werden.
    folge = [rs.expired_delay(i, pol) for i in range(len(pol.expired_delays_s))]
    assert folge == sorted(folge), folge
    ok("restream_stability: Ablauf-Pfad bremst erst, wenn er sich dreht")

    # 4) Codec-Fallback — die schwachen Marker duerfen nicht mehr auf
    #    Netzfehler anspringen (transcode kostet CPU, die dem Bild fehlt).
    assert rs.is_codec_failure("Unable to find a suitable output format")
    assert rs.is_codec_failure("No such codec: h265")
    assert rs.is_codec_failure("Invalid data found when processing input")
    assert not rs.is_codec_failure("Failed to resolve hostname pull-flv.tiktokcdn.com")
    assert not rs.is_codec_failure("Unable to open resource: Connection refused")
    assert not rs.is_codec_failure(
        "Could not write header (incorrect codec parameters ?): Input/output error")
    assert not rs.is_codec_failure("")
    # Starke Marker gelten trotz Netz-Rauschen in derselben Kachel.
    assert rs.is_codec_failure(
        "Will reconnect at 123... Codec does not support this pixel format")
    ok("restream_stability: Codec-Fallback springt nicht mehr auf Netzfehler an")

    # 5) Stillstand — Karenz, Blindheit, Abschuss.
    v = rs.stall_verdict(10.0, 0.0, pol)
    assert v.state == rs.STALL_GRACE and not v.stalled
    v = rs.stall_verdict(600.0, 5.0, pol)
    assert v.state == rs.STALL_OK and not v.stalled
    v = rs.stall_verdict(600.0, 200.0, pol)
    assert v.state == rs.STALL_DEAD and v.stalled and v.reason
    # Blind heisst nicht tot — Unwissen ist kein Beweis (Regel aus dem Guard).
    v = rs.stall_verdict(600.0, 200.0, pol, reader_alive=False)
    assert v.state == rs.STALL_BLIND and not v.stalled
    v = rs.stall_verdict(600.0, None, pol)
    assert v.state == rs.STALL_BLIND and not v.stalled
    ok("restream_stability: Stillstand erkannt, Karenz und Blindheit geachtet")

    # Das Modul bleibt bot-frei — sonst waere es nicht ohne Laufzeitstack
    #  pruefbar, und genau das war der Grund fuer diese Extraktion.
    quelle = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "nc", "restream_stability.py"), encoding="utf-8").read()
    import ast as _ast
    for _n in _ast.walk(_ast.parse(quelle)):
        if isinstance(_n, _ast.Import):
            _mods = [a.name.split(".")[0] for a in _n.names]
        elif isinstance(_n, _ast.ImportFrom):
            _mods = [(_n.module or "").split(".")[0]]
        else:
            continue
        assert set(_mods) <= {"random", "dataclasses", "__future__"}, _mods
    ok("restream_stability: bot-frei und stdlib-only")


def _test_updater():
    """v4.0-W115: Selbst-Update — die drei Zusagen, ohne Netz und ohne Bot.

    Ein Update schreibt Code unter einen laufenden Dienst. Genau drei Dinge
    duerfen dabei nie passieren, und alle drei sind hier reine Funktionen:
    Betriebsdaten anfassen, aus der Wurzel ausbrechen, lokale Dateien
    loeschen. Der Rest (Download, Backup, Schreiben) haengt daran.
    """
    import nc.updater as up

    # ── Zusage 1: Betriebsdaten sind unantastbar ─────────────────────────
    # Die Liste ist der einzige Schutz der .env mit ihren 352 Variablen —
    # ein Update, das sie mit .env.example ueberschreibt, kostet den Betrieb.
    for pfad in (".env", "logs/debug.log", "nc/logs/x.log", "recordings/a.mp4",
                 "bot.db", "bot.db-wal", "archive/x.mp4", "backups/x.zip",
                 ".git/HEAD", "build/README.md", "nc/__pycache__/x.pyc",
                 "website/news.json", ".nc_update.json"):
        assert up.is_protected(pfad), pfad
    for pfad in ("bot.py", "nc/updater.py", "brain/router.py",
                 "templates/dashboard.html", "website/lafap_index.html",
                 ".claude/skills/nightcrawler/SKILL.md", "requirements.txt",
                 ".env.example"):
        assert not up.is_protected(pfad), pfad
    ok("updater: Betriebsdaten geschuetzt, Quelltext aktualisierbar")

    # website/news.json schreibt der News-Agent im Betrieb. Kaeme sie aus dem
    # Archiv zurueck, stuende die Website schlagartig auf dem Stand des
    # letzten Commits — mit verschwundenen News.
    assert up.is_protected("website/news.json")
    assert not up.is_protected("website/lafap_index.html")
    ok("updater: news.json geschuetzt, die Seite selbst nicht")

    # ── Zusage 2: kein Ausbruch aus der Wurzel (Zip-Slip) ────────────────
    for bose in ("../etc/passwd", "/etc/passwd", "a/../../b", "C:/x",
                 "./../x", "", "..", "nc/../../boom"):
        assert up.normalize(bose) == "", bose
    assert up.normalize("nc/updater.py") == "nc/updater.py"
    assert up.normalize("nc\\updater.py") == "nc/updater.py"
    # Ein unbrauchbarer Pfad gilt zugleich als geschuetzt — doppelter Riegel,
    # damit kein Zweig ihn versehentlich doch schreibt.
    assert up.is_protected("../etc/passwd")
    ok("updater: Zip-Slip abgeriegelt, unbrauchbare Pfade gelten als geschuetzt")

    # GitHub packt alles unter <repo>-<branch>/ — diese Ebene faellt weg.
    assert up.strip_archive_root("Telegram-Stream-Info-Bot-main/nc/x.py") == "nc/x.py"
    assert up.strip_archive_root("Telegram-Stream-Info-Bot-main/") == ""
    assert up.strip_archive_root("nurwurzel") == ""
    ok("updater: Archiv-Wurzel wird abgestreift")

    # ── Zusage 3: nur hinzufuegen und ersetzen, nie loeschen ─────────────
    eintraege = [("bot.py", 10, "neu"), ("nc/neu.py", 5, "x"),
                 ("gleich.py", 3, "same"), (".env", 1, "y"),
                 ("../boom", 1, "z"), ("riesig.bin", up.MAX_FILE_BYTES + 1, "w")]
    lokal = {"bot.py": "alt", "gleich.py": "same", "nur_lokal.sh": "meins"}
    plan = up.build_plan(eintraege, lambda r: lokal.get(r))
    assert plan.changed == ["bot.py"], plan.changed
    assert plan.new == ["nc/neu.py"], plan.new
    assert plan.same == 1
    assert plan.protected == [".env"], plan.protected
    assert sorted(plan.rejected) == ["../boom", "riesig.bin"], plan.rejected
    # Die lokale Datei, die im Archiv fehlt, taucht in keiner Liste auf —
    # sie bleibt liegen. Sonst raeumt ein Update eigene Skripte weg.
    for liste in (plan.new, plan.changed, plan.protected, plan.rejected):
        assert "nur_lokal.sh" not in liste
    assert plan.as_dict()["count"] == 2
    ok("updater: Plan trennt neu/geaendert/geschuetzt, loescht nie")

    # ── Ehrlichkeit der Auskunft ────────────────────────────────────────
    # Ohne bekannten lokalen Stand ist "es gibt ein Update" eine Behauptung.
    assert "unbekannt" in up.describe({"ok": True, "update_available": False,
                                       "local_known": False}).lower()
    assert "aktuell" in up.describe({"ok": True, "update_available": False,
                                     "local_known": True}).lower()
    assert "fehlgeschlagen" in up.describe({"ok": False, "error": "kaputt"}).lower()
    assert up.short_sha("a1b2c3d4e5f6") == "a1b2c3d"
    ok("updater: Auskunft nennt einen unbekannten Stand auch so")

    # ── bot-frei und stdlib-only ────────────────────────────────────────
    hier = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(hier, "nc", "updater.py"), encoding="utf-8").read()
    # Ueber den AST, nicht ueber den Text: "bot" steckt seit der Umbenennung
    # in jedem zweiten Wort des Moduls ("bot-frei"), eine Textsuche waere ein
    # Dauer-Fehlalarm.
    import ast as _ast
    for _n in _ast.walk(_ast.parse(src)):
        if isinstance(_n, _ast.Import):
            assert all(not _ist_monolith(a.name) for a in _n.names), "importiert bot.py"
        elif isinstance(_n, _ast.ImportFrom):
            assert not _ist_monolith(_n.module or ""), "importiert bot.py"
    assert "import requests" not in src and "aiohttp" not in src, "Fremd-Bibliothek"
    assert "urllib.request" in src
    # Der Token darf nie in einer API-Antwort landen.
    up.configure(root=hier, token="geheim")
    st = up.settings()
    assert "geheim" not in repr(st) and st["has_token"] is True, st
    ok("updater: bot-frei, stdlib-only, Token nie in der Auskunft")


def _test_flapguard_und_rate():
    """v4.0-W116: die beiden Verlaufs-Urteile, jeweils ohne Bot und ohne Uhr.

    Beide entscheiden ueber die ZEIT, und beide sind in der falschen
    Richtung teuer: zu empfindlich erzeugt Alarm-Muedigkeit, zu traege
    meldet nie. Genau deshalb stehen sie als reine Funktionen hier, wo
    Stunden in Millisekunden durchgespielt werden koennen.
    """
    import nc.flapguard as fg
    import nc.recdiag as rd

    # ── Flattern ──────────────────────────────────────────────────────────
    cfg = fg.FlapConfig(fenster_s=900, schwelle=4, ruhe_s=600,
                        melde_abstand_s=1800)
    w = fg.FlapWatch(cfg)
    t = 1000.0
    # Drei kurze Trennungen: noch kein Alarm.
    for i in range(3):
        u = w.trennung("kick", 30, t + i * 60)
        assert not u.melden, i
    # Die vierte im Fenster ist es.
    u = w.trennung("kick", 30, t + 180)
    assert u.melden and u.anzahl == 4 and "4 Trennungen" in u.grund, u
    ok("flapguard: vier Trennungen im Fenster schlagen an, drei nicht")

    # Regel 3: im Meldeabstand bleibt es still, danach nicht mehr.
    u = w.trennung("kick", 30, t + 240)
    assert not u.melden and u.anzahl == 5, u
    u = w.trennung("kick", 30, t + 1900)     # Abstand + Fenster vorbei
    assert not u.melden, "Fenster haette sich leeren muessen"
    ok("flapguard: Meldeabstand gedrosselt, altes Fenster faellt raus")

    # Regel 2: ein langer Halt loescht die Akte und meldet die Erholung.
    w2 = fg.FlapWatch(cfg)
    for i in range(4):
        w2.trennung("tw", 10, 100 + i)
    assert w2.snapshot()["tw"]["laut"] is True
    u = w2.trennung("tw", 3600, 5000)        # eine Stunde gehalten
    assert u.erholt and u.anzahl == 1 and not u.melden, u
    assert w2.snapshot()["tw"]["laut"] is False
    ok("flapguard: langer Halt loescht die Akte und meldet die Erholung")

    # Regel 1: ueber das Fenster hinaus summiert sich nichts auf.
    w3 = fg.FlapWatch(cfg)
    for i in range(10):
        u = w3.trennung("yt", 10, i * 1000.0)   # je 1000s auseinander
        assert not u.melden, i
    ok("flapguard: verteilte Trennungen summieren sich nicht zum Daueralarm")

    # ── Raten-Einbruch ────────────────────────────────────────────────────
    rc = rd.RateConfig(warmlauf_s=60, einbruch_anteil=0.15,
                       einbruch_dauer_s=90, min_grundlinie_bps=40000)
    sp = rd.RateSpur()
    NORM = 500_000            # 500 kB/s ~ 4 Mbit/s
    # Warmlauf: nie urteilen, nur Grundlinie bilden.
    for _ in range(4):
        assert sp.beobachte(NORM * 15, 15, rc) is None
    assert sp.grundlinie_bps >= 40000
    # Gesund weiter: still.
    for _ in range(4):
        assert sp.beobachte(NORM * 15, 15, rc) is None
    # Bild weg, Ton laeuft (5 % der Rate): erst nach der Mindestdauer melden.
    LEISE = int(NORM * 0.05)
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # 15s
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # 30s
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # 45s
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # 60s
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # 75s
    assert sp.beobachte(LEISE * 15, 15, rc) == "einbruch"  # 90s
    assert sp.beobachte(LEISE * 15, 15, rc) is None      # nur EINMAL je Episode
    ok("recdiag.RateSpur: Einbruch erst nach Mindestdauer, dann genau einmal")

    # Erholung wird gemeldet, danach ist wieder Ruhe.
    assert sp.beobachte(NORM * 15, 15, rc) == "erholt"
    assert sp.beobachte(NORM * 15, 15, rc) is None
    ok("recdiag.RateSpur: Erholung genau einmal")

    # Der Einbruch darf die Grundlinie NICHT nach unten schleifen — sonst
    # normalisiert sich jeder Ausfall von selbst weg.
    sp2 = rd.RateSpur()
    for _ in range(8):
        sp2.beobachte(NORM * 15, 15, rc)
    basis = sp2.grundlinie_bps
    for _ in range(20):
        sp2.beobachte(LEISE * 15, 15, rc)
    assert sp2.grundlinie_bps == basis, "Grundlinie ist mitgewandert"
    ok("recdiag.RateSpur: Grundlinie wandert waehrend des Einbruchs nicht mit")

    # Eine statische Szene mit MASSVOLLEM Rueckgang loest nicht aus.
    sp3 = rd.RateSpur()
    for _ in range(8):
        sp3.beobachte(NORM * 15, 15, rc)
    for _ in range(20):
        assert sp3.beobachte(int(NORM * 0.4) * 15, 15, rc) != "einbruch"
    ok("recdiag.RateSpur: massvoller Rueckgang (40 %) ist kein Einbruch")

    # Beide Module bleiben bot-frei.
    import ast as _ast, os as _os
    for datei, erlaubt in (("flapguard.py", {"dataclasses", "__future__"}),):
        quelle = open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                    "nc", datei), encoding="utf-8").read()
        for _n in _ast.walk(_ast.parse(quelle)):
            if isinstance(_n, _ast.Import):
                mods = [a.name.split(".")[0] for a in _n.names]
            elif isinstance(_n, _ast.ImportFrom):
                mods = [(_n.module or "").split(".")[0]]
            else:
                continue
            assert set(mods) <= erlaubt, (datei, mods)
    ok("flapguard: bot-frei und stdlib-only")



def _test_w10_diagnose_und_pfadschutz():
    """v4.1-W10: die Befunde aus dem error.log und von CodeQL — als reine Logik
       geprueft, dort wo sie liegt."""
    import os
    from nc.restream_util import (betroffene_ziele, fenstergroesse, http_url,
                                  url_host)
    from nc.util import datei_in

    # (1) Wer steht wirklich im stderr-Auszug? Kick und Twitch liegen BEIDE auf
    # live-video.net — deshalb wird auf den vollen Host verglichen. Genau daran
    # scheiterte die alte Diagnose: sie nannte kategorisch Kick.
    ziele = [("kick", "rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/K1"),
             ("twitch", "rtmp://ingest.global-contribute.live-video.net/app/K2"),
             ("youtube", "rtmp://a.rtmp.youtube.com/live2/K3")]
    nur_twitch = ("[tee] Slave '[f=flv]rtmp://ingest.global-contribute."
                  "live-video.net/app/<KEY>': error opening: I/O error")
    assert betroffene_ziele(nur_twitch, ziele) == ["twitch"], \
        "Twitch-Ausfall wuerde weiter als Kick gemeldet"
    beide = nur_twitch + "\nSlave 'rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/<KEY>' failed"
    assert betroffene_ziele(beide, ziele) == ["kick", "twitch"], "Reihenfolge/Menge falsch"
    assert betroffene_ziele("All tee outputs failed.", ziele) == [], \
        "ohne Host im Text darf kein Ziel behauptet werden"
    assert betroffene_ziele("", ziele) == [] and betroffene_ziele("x", []) == []
    assert url_host("rtmps://h.example:443/app/k") == "h.example"
    assert url_host("kaputt") == ""
    ok("v4.1-W10: Abbruch-Diagnose nennt das Ziel, das wirklich im stderr steht")

    # (2) Was auf eine Kommandozeile darf. Die Uebergabe ist eine Liste, es gibt
    # keine Shell — ein zweites Argument waere trotzdem ein zweites Argument.
    assert fenstergroesse("1080,1920") == "1080,1920"
    assert fenstergroesse(" 1920 x 1080 ") == "1920,1080", "x als Trenner nicht erkannt"
    assert fenstergroesse("800,600 --dump-dom", "9,9") == "9,9", "Flag-Anhang kommt durch"
    assert fenstergroesse("auto", "9,9") == "9,9" and fenstergroesse(None, "9,9") == "9,9"
    assert fenstergroesse("0,600", "9,9") == "9,9", "Nullbreite akzeptiert"
    assert fenstergroesse("999999,10", "9,9") == "9,9", "unbegrenzte Groesse akzeptiert"
    assert http_url("https://a.example/x") == "https://a.example/x"
    for boese in ("file:///etc/shadow", "--dump-dom", "javascript:1", ""):
        assert http_url(boese, "FB") == "FB", "%s kommt auf die Kommandozeile" % boese
    ok("v4.1-W10: Fenstergroesse und Overlay-URL koennen kein Argument schmuggeln")

    # (3) Pfad-Zusage statt Verbotsliste. Geprueft wird das ERGEBNIS: liegt die
    # aufgeloeste Datei wirklich unter der Basis?
    assert datei_in("/daten/clips", "a.mp4", ".mp4") == os.path.realpath("/daten/clips/a.mp4")
    for boese in ("../etc/passwd.mp4", "../../x.mp4", "/etc/shadow.mp4",
                  "", None):
        assert datei_in("/daten/clips", boese, ".mp4") is None, "%r kommt durch" % boese
    # Der Rueckwaertsschraegstrich ist unter POSIX ein ganz normales Zeichen in
    # einem Dateinamen — er traegt dort NICHT aus dem Verzeichnis heraus. Die
    # alte Pruefung verbot ihn trotzdem; das war nicht falsch, aber es war eine
    # Aussage ueber Zeichen statt ueber das Ziel. Entscheidend ist, dass der
    # aufgeloeste Pfad in der Basis liegt — und das tut er hier.
    if os.sep == "/":
        assert datei_in("/daten/clips", "..\\x.mp4", ".mp4") == \
            os.path.realpath("/daten/clips/..\\x.mp4")
    assert datei_in("/daten/clips", "a.wav", ".mp4") is None, "Endung nicht erzwungen"
    assert datei_in("/daten/clips", "unterordner/a.mp4", ".mp4") == \
        os.path.realpath("/daten/clips/unterordner/a.mp4"), \
        "ein Unterordner INNERHALB der Basis ist erlaubt — die Zusage ist die Basis"
    # Der Praefix-Nachbar: /daten/clips2 faengt mit /daten/clips an, liegt aber
    # nicht darin. Genau das macht ein startswith-Vergleich falsch.
    assert datei_in("/daten/clips", "../clips2/a.mp4", ".mp4") is None, \
        "Praefix-Nachbar gilt faelschlich als innerhalb"
    ok("v4.1-W10: Ausliefer-Pfade weisen Zugehoerigkeit nach, statt Zeichen zu verbieten")

    # (4) Der Sprachkatalog liest nur bekannte Sprachen — der Name wird sonst
    # zum Dateipfad, und katalog() haengt an /api/i18n/katalog?lang=…
    import nc.i18n as I18N
    assert I18N.katalog("../../etc/passwd") == {}, "Sprachname wandert in den Pfad"
    assert I18N.katalog("fr") == {}, "unbekannte Sprache wird geladen"
    assert I18N.katalog("de") == {}, "Quellsprache braucht keinen Katalog"
    assert isinstance(I18N.katalog("en"), dict)
    ok("v4.1-W10: Katalog laedt nur Sprachen aus der Positivliste")



def _test_w12_einzel_slot():
    """v4.1-W12: zwei Restreams duerfen sich keinen Kick-Key teilen."""
    from nc.restream_util import slot_belegt

    # Der Fall vom 30.08.: #60 stirbt, wird aus _procs genommen, der Scheduler
    # vergibt den Slot an #6 — und 20 Sekunden spaeter feuert der geplante
    # Reconnect von #60. Genau hier muss die Antwort "belegt" lauten.
    assert slot_belegt(True, [6], 60) == 6, "Reconnect laeuft in den fremden Slot"
    assert slot_belegt(True, [], 60) is None, "freier Slot wird verweigert"
    # Der eigene Wiederanlauf ist kein Fremdbeleger — sonst koennte sich ein
    # Restream nach einem Abbruch nie mehr selbst neu aufbauen.
    assert slot_belegt(True, [60], 60) is None, "Restream blockiert sich selbst"
    # Multi-Modus heisst: eigene Keys je Ziel, also kein Slot.
    assert slot_belegt(False, [6, 43], 60) is None, "Multi-Modus kennt keinen Slot"
    # Mehrere Fremde: es genuegt, EINEN zu nennen — die Meldung soll knapp sein.
    assert slot_belegt(True, [6, 43], 60) in (6, 43)
    ok("v4.1-W12: Einzel-Slot wird beim START geprueft, nicht bei der Planung")


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

    _test_cfgstore_und_claude()

    _test_routes_ai()

    _test_restream_stability()

    _test_flapguard_und_rate()

    _test_updater()

    _test_w10_diagnose_und_pfadschutz()

    _test_w12_einzel_slot()

    print("test_nc_modules OK \u2014 %d Vertraege gruen" % PASS)


if __name__ == "__main__":
    main()
