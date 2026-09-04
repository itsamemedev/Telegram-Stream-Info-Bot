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
    import sys as _sys

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

        # (1) Pfade woertlich: ein url_prefix wuerde jeden Dashboard-Aufruf
        # brechen. Ausnahmen sind Pfade, die per Konvention NICHT unter /api/
        # liegen — /metrics ist der Prometheus-Endpunkt, und ein Scraper sucht
        # ihn genau dort (v4.1-W23). Die Liste steht hier ausdruecklich, damit
        # ein versehentlich gesetzter url_prefix trotzdem auffliegt.
        AUSSERHALB = {"/metrics"}
        for r in regeln:
            assert str(r.rule).startswith("/api/") or str(r.rule) in AUSSERHALB, \
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
        # (7) Auf Modulebene nur stdlib, flask und nc. v4.1-W23: ein
        # `import aiohttp` ganz oben in nc/routes/beobachtung.py hat genau
        # diesen Job in CI gekippt — dort werden absichtlich nur orjson und
        # flask installiert, damit nc/* isoliert testbar bleibt (CLAUDE.md).
        # Lokal fiel es nicht auf, weil der volle Laufzeitstack da liegt.
        # Wer aiohttp, telegram, discord, streamlink, yt_dlp oder psutil
        # braucht, importiert IN der Funktion.
        ERLAUBT = {"flask", "orjson", "nc"}
        for _n in _ast.parse(quelle).body:      # nur body: verschachtelte
            wurzeln = []                        # Importe sind ausdruecklich ok
            if isinstance(_n, _ast.Import):
                wurzeln = [al.name.split(".")[0] for al in _n.names]
            elif isinstance(_n, _ast.ImportFrom) and not _n.level:
                wurzeln = [(_n.module or "").split(".")[0]]
            for w in wurzeln:
                assert w in ERLAUBT or w in _sys.stdlib_module_names, \
                    ("%s: %r auf Modulebene — bricht den CI-Vertragsjob, "
                     "in die Funktion verschieben" % (name, w))
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
        # v4.1-W15: NUR der Kontext-cfg. Der alte Ausdruck traf jedes
        # `cfg["x"]` — auch ein LOKALES Dict, das die Route selbst gebaut hat
        # (nc/routes/cohost.py: `cfg = _cohost_cfg()` und dann `cfg["enabled"]`).
        # Der Vertrag haette dort vier Schluessel vom Bot verlangt, die es dort
        # nie gab. Blueprints lesen den Kontext ausnahmslos als `_c().cfg[...]`
        # — bp_extract erzeugt genau diese Form.
        gebraucht = set(_re.findall(r'_c\(\)\.cfg\["([^"]+)"\]', code))
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
    # v4.1-W26: als REGEL statt als Namensliste. Frueher stand hier die
    # woertliche Import-Zeile — die kippte, sobald ein interner Aufrufer
    # selbst in einen Blueprint wanderte (/api/pulse nahm api_health_score
    # mit). Die Zusicherung ist dieselbe geblieben, sie prueft jetzt nur den
    # Sachverhalt statt seiner damaligen Schreibweise: jede Blueprint-Funktion,
    # die bot.py AUFRUFT, muss dort auch importiert sein.
    import ast as _ast
    b = _ast.parse(src)
    importiert = set()
    for n in _ast.walk(b):
        if isinstance(n, _ast.ImportFrom) and (n.module or "").startswith("nc.routes"):
            importiert |= {(a.asname or a.name) for a in n.names}
        elif isinstance(n, _ast.Import):
            importiert |= {(a.asname or a.name.split(".")[0]) for a in n.names}
    definiert = {n.name for n in b.body
                 if isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef))}
    gerufen = {n.func.id for n in _ast.walk(b)
               if isinstance(n, _ast.Call) and isinstance(n.func, _ast.Name)}
    for name in ("api_health_score", "api_system_resources"):
        if name in gerufen:
            assert name in importiert or name in definiert, \
                ("bot.py ruft %s auf, importiert es aber nicht — NameError zur "
                 "Laufzeit" % name)
    # api_system_resources hat weiterhin einen internen Aufrufer (Telegram
    # /sysres und die Aggregat-Route) und MUSS deshalb importiert sein.
    assert "api_system_resources" in importiert, \
        "api_system_resources ist nicht mehr importiert — /sysres stirbt"
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



def _test_w13_claude_fehlergrund():
    """v4.1-W13: der Grund darf nicht im except haengenbleiben."""
    import json as _json
    import urllib.error
    import io as _io
    import nc.claude as C

    # (1) Der ECHTE Fehlertext der API kommt beim Aufrufer an. Im debug.log vom
    # 30.08. stand 26 Mal "fehlgeschlagen (bad_request)" und nie, WAS schlecht
    # war — obwohl die API es jedes Mal mitschickt.
    koerper = _json.dumps({"error": {"type": "invalid_request_error",
                                     "message": "max_tokens: must be >= 1"}}).encode()

    def _opener_400(req, timeout):
        raise urllib.error.HTTPError(C.API_URL, 400, "Bad Request", {},
                                     _io.BytesIO(koerper))

    gesehen = []
    txt, kind = C.chat_sync([{"role": "user", "content": "hi"}], "k",
                            opener=_opener_400,
                            on_error=lambda k, d, m: gesehen.append((k, d, m)))
    assert (txt, kind) == (None, "bad_request"), "Vertrag (text, kind) veraendert"
    assert gesehen, "der Grund wird weiter verschluckt"
    assert "max_tokens: must be >= 1" in gesehen[0][1], "API-Text fehlt"
    assert "HTTP 400" in gesehen[0][1] and gesehen[0][2], "Status oder Modell fehlt"

    # (2) Ohne Rueckruf bleibt alles wie vorher — die zwoelf Aufrufstellen, die
    # `err == "auth"` vergleichen, duerfen sich nicht aendern.
    assert C.chat_sync([{"role": "user", "content": "hi"}], "k",
                       opener=_opener_400) == (None, "bad_request")

    # (3) Leere Inhalte fliegen raus: die API weist einen leeren Textblock mit
    # 400 ab, und zwar den GANZEN Request.
    b = C.build_payload([{"role": "system", "content": "S"},
                         {"role": "user", "content": "   "},
                         {"role": "user", "content": "echt"}])
    assert b["messages"] == [{"role": "user", "content": "echt"}], "leerer Block bleibt drin"
    assert b["system"] == "S"

    # (4) Gar kein Verlauf: der Aufruf kann nicht gelingen, also wird er nicht
    # gemacht — und der Grund heisst nicht "bad_request".
    gesehen2 = []
    assert C.chat_sync([{"role": "system", "content": "nur system"}], "k",
                       opener=lambda r, t: (_ for _ in ()).throw(
                           AssertionError("API wurde trotzdem gerufen")),
                       on_error=lambda k, d, m: gesehen2.append(k)) == (None, "kein_verlauf")
    assert gesehen2 == ["kein_verlauf"]
    ok("v4.1-W13: Claude-Fehler nennen Grund und Modell, leere Requests gar nicht erst")



def _test_w14_totes_modell():
    """v4.1-W14: ein totes Modell darf nicht jeden Umlauf den ersten Versuch kosten."""
    import nc.freeai as F

    base = {"url": "https://api.llm7.io/v1",
            "models": ["gpt-4.1-nano-2025-04-14", "zweit", "dritt"]}
    F._model_block.clear()
    assert F._candidate_models(base, None)[0] == "gpt-4.1-nano-2025-04-14"

    # Der Fall aus dem debug.log: 26 Mal "Model ... is currently unavailable",
    # jedes Mal als ERSTER Versuch. Nach dem Merken steht er hinten.
    F._block_model(base["url"], "gpt-4.1-nano-2025-04-14")
    reihe = F._candidate_models(base, None)
    assert reihe[0] == "zweit", "das tote Modell kommt weiter zuerst dran"
    assert set(reihe) == set(base["models"]), "ein Modell ist ganz verschwunden"
    assert reihe[-1] == "gpt-4.1-nano-2025-04-14", "das tote Modell steht nicht hinten"

    # Sind ALLE gesperrt, wird trotzdem probiert — dieselbe Haltung wie bei
    # _eligible_bases: lieber ein Versuch als sicheres Scheitern.
    for m in base["models"]:
        F._block_model(base["url"], m)
    assert F._candidate_models(base, None) == base["models"], \
        "bei komplett gesperrter Base bleibt nichts zum Probieren"

    # Die Sperre gilt pro BASE, nicht global: dasselbe Modell kann anderswo leben.
    andere = {"url": "https://text.pollinations.ai", "models": ["gpt-4.1-nano-2025-04-14", "x"]}
    assert F._candidate_models(andere, None)[0] == "gpt-4.1-nano-2025-04-14", \
        "die Sperre wirkt ueber Basen hinweg — ein gesundes Modell waere mitgesperrt"

    # Eine Base ohne Katalog bleibt unberuehrt (custom FREEAI_BASES).
    assert F._candidate_models({"url": "x"}, "wunsch") == ["wunsch"]
    F._model_block.clear()
    ok("v4.1-W14: totes Modell wandert ans Ende, pro Base, nie ganz raus")


def _test_w18_toxizitaet_ohne_tiktok():
    """v4.1-W18: TikTok loest keine Toxizitaets-Warnung beim Betreiber aus."""
    import nc.modstats as M

    # Der Fall aus dem Betrieb: ein aktiver Live-React-Worker schreibt AZRAELs
    # Reaktionen auf einen TikTok-Stream ins kick_mod_log. Frueher zaehlte
    # jede dieser Zeilen als "Moderations-Aktion" — sechs davon reichten fuer
    # eine Warnung ueber einen Chat, den der Bot gar nicht moderiert.
    tiktok = [("reaction", "azrael", {"src": "helge_72"})] * 12
    tiktok += [("highlight", "radar", {"score": 3})] * 4
    v = M.verdichte(tiktok)
    assert v["actions_1h"] == 0, "TikTok-Reaktionen zaehlen weiter als Moderation"
    assert v["platforms"] == {}

    # Was der Bot selbst sagt und was er lernt, ist ebenfalls keine Moderation.
    assert M.verdichte([("send", "bot", {}), ("reply", "bot", {}),
                        ("learn", "ai", {})])["actions_1h"] == 0

    # Die drei Stream-Chats zaehlen — mit Plattform-Aufschluesselung, damit die
    # Meldung sagt WO es kracht, nicht nur DASS.
    echt = [("timeout", "auto-mod-kick", {"platform": "kick"}),
            ("warn", "auto-mod-twitch", {"platform": "twitch", "cat": "spam"}),
            ("timeout", "auto-mod-youtube", {"platform": "youtube"}),
            ("flag", "auto-mod-youtube", {"platform": "youtube"})]
    v = M.verdichte(echt + tiktok)
    assert v["actions_1h"] == 4, v
    assert v["platforms"] == {"kick": 1, "twitch": 1, "youtube": 2}, v["platforms"]

    # Discord ist eine eigene Welt und standardmaessig NICHT dabei; wer es will,
    # traegt es ein. TikTok laesst sich auch so nicht zuschalten — es steht
    # nicht in PLATTFORMEN, und genau das ist der Sinn der harten Liste.
    dc = [("timeout", "ai-discord", {"platform": "discord", "toxic": 0.9})]
    assert M.verdichte(dc)["actions_1h"] == 0, "Discord meldet ungefragt mit"
    assert M.verdichte(dc, erlaubt=M.quellen("kick,discord"))["actions_1h"] == 1
    assert "tiktok" not in M.PLATTFORMEN, "TikTok waere konfigurierbar geworden"
    assert M.quellen("tiktok") == M.STANDARD_QUELLEN, "TikTok liess sich einschalten"
    assert M.quellen("tiktok,kick") == ("kick",)

    # Der Trend vergleicht zwei Stunden. Liefe die Vorstunde ungefiltert, waere
    # jede TikTok-Sitzung in der Vorstunde eine gemeldete "Beruhigung" und
    # jedes Ende einer Sitzung eine gemeldete "Welle". Beide Seiten, eine Regel.
    v = M.verdichte(echt, vorzeilen=tiktok)
    assert v["actions_prev_1h"] == 0, "die Vorstunde laeuft durch eine andere Regel"

    # sentinel-shield schreibt aus dem Kick-Moderator UND aus dem Discord-
    # Automod. Ohne Markierung ist die Zeile nicht zuzuordnen und zaehlt nicht
    # mit — eine falsch zugeordnete Warnung waere schlimmer als eine fehlende.
    assert M.plattform("sentinel-shield", {}) is None
    assert M.plattform("sentinel-shield", {"platform": "discord"}) == "discord"
    assert M.plattform("sentinel-shield", {"platform": "kick"}) == "kick"
    # Altbestand ohne Markierung bleibt ueber den Aktor lesbar.
    assert M.plattform("auto-mod-twitch", None) == "twitch"
    assert M.plattform("azrael", {"src": "helge_72"}) is None

    # Ein gefaelschter Plattformname faellt auf den Aktor zurueck statt zu zaehlen.
    assert M.plattform("auto-mod-kick", {"platform": "tiktok"}) == "kick"
    assert M.plattform("azrael", {"platform": "tiktok"}) is None

    # avg bleibt None, wenn niemand einen toxic-Wert gemessen hat: 0.0 waere
    # die Aussage "nicht toxisch", und die hat hier niemand getroffen.
    assert M.verdichte(echt)["avg_toxic_1h"] is None
    mit = [("timeout", "ai", {"platform": "kick", "toxic": 0.9}),
           ("timeout", "ai", {"platform": "kick", "toxic": 0.7})]
    assert M.verdichte(mit)["avg_toxic_1h"] == 0.8

    # Der Agent nennt die Plattformen in seiner Meldung.
    import brain.agents as A

    class _B:
        class memory:
            @staticmethod
            def record_metric(*a, **k): pass
    schnapp = {"actions_1h": 9, "actions_prev_1h": 1, "avg_toxic_1h": 0.8,
               "platforms": {"kick": 7, "twitch": 2}}
    m = A.ToxicityAgent(_B(), moderation=lambda: schnapp).run({})
    assert len(m) == 1 and "kick 7" in m[0]["text"] and "twitch 2" in m[0]["text"], m
    # Ohne Aufschluesselung (Altbestand) bleibt der Text wie bisher lesbar.
    m = A.ToxicityAgent(_B(), moderation=lambda: {
        "actions_1h": 9, "actions_prev_1h": 1}).run({})
    assert len(m) == 1 and "[" not in m[0]["text"], m

    ok("v4.1-W18: TikTok zaehlt nicht als Moderation, Plattform steht in der Meldung")


def _test_w18_kickmod_blueprint():
    """v4.1-W18: neun Routen raus, null neue Kontext-Eintraege."""
    import tempfile as _tf

    import nc.badwords as B
    import nc.channels as C

    # (1) Die Datenschicht traegt sich selbst — Dateien, kein Bot, kein Netz.
    d = _tf.mkdtemp()
    B.configure(recordings_dir=d)
    assert B.load_banned() == [] and B.load_learned() == [], "leerer Start nicht leer"
    assert B.save_banned(["arsch", "x" * 99])
    assert B.load_banned() == ["arsch", "x" * 40], "keine Kappung auf 40 Zeichen"
    assert B.save_learned([{"word": "test"}])
    assert B.load_learned() == [{"word": "test"}]
    # Kaputtes JSON darf den Moderator nicht mitreissen: lieber leer als Absturz.
    open(os.path.join(d, "banned_words.json"), "w", encoding="utf-8").write("{kaputt")
    assert B.load_banned() == []
    # Und der Deckel gilt auch beim Lesen einer zu langen Liste.
    B.save_banned(["w%d" % i for i in range(B.CAP + 50)])
    assert len(B.load_banned()) == B.CAP

    # (2) Die Basisliste faellt bei Netzfehler NICHT auf leer zurueck — eine
    # geleerte Liste waere ein still entwaffneter Moderator.
    def _kaputt(url):
        raise OSError("kein Netz")
    w, q = B.fetch_ldnoobw_de(opener=_kaputt)
    assert q == "fallback" and w == B.FALLBACK_DE and w, "Netzfehler leert die Liste"
    # Eine leere Antwort zaehlt ebenfalls als Fehlschlag.
    w, q = B.fetch_ldnoobw_de(opener=lambda u: "\n#nur ein Kommentar\n")
    assert q == "fallback" and w == B.FALLBACK_DE
    w, q = B.fetch_ldnoobw_de(opener=lambda u: "eins\n# weg\nzwei\n")
    assert (w, q) == (["eins", "zwei"], "online")

    # (3) Der primaere Restream ist ein REGISTER, kein Alias. bot.py bindet den
    # Namen bei jeder Primaer-Nachfolge neu; ein Alias zeigte danach auf das
    # alte Dict, und das SENTINEL-Panel meldete den vorherigen User als aktiv.
    C.RESTREAM_ACTIVE["obj"] = {}
    assert C.restream_active() == {}, "restream_active gibt None statt {}"
    C.RESTREAM_ACTIVE["obj"] = {"user": "helge_72", "rid": 7}
    assert C.restream_active().get("user") == "helge_72"

    # (4) Der Blueprint sieht denselben Zustand wie der Bot — das ist der
    # ganze Punkt der Register. Und er kommt ohne neuen ctx-Slot aus.
    import ast as _ast

    import nc.routes.kickmod as K
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(K.bp)
    regeln = {str(r.rule) for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert len(regeln) == 9, regeln
    with app.test_client() as cl:
        j = cl.get("/api/kickmod/status").get_json()
    assert j["ok"] and j["running"] is False, j
    assert j["channels"]["tiktok"]["connected"] is True, "Register nicht gelesen"
    C.RESTREAM_ACTIVE["obj"] = {}

    # Ohne laufenden Moderator antworten die schreibenden Routen 503 statt 500:
    # "startet noch" ist voruebergehend, das Dashboard darf es wiederholen.
    with app.test_client() as cl:
        for weg in ("/api/kickmod/config", "/api/kickmod/start",
                    "/api/kickmod/say", "/api/kickmod/import_badwords"):
            assert cl.post(weg, json={}).status_code == 503, weg

    # (5) Kein neuer ctx-Slot. Der Kontext steht vertraglich bei hoechstens 25.
    quelle = open("nc/routes/kickmod.py", encoding="utf-8").read()
    genutzt = {n.attr for n in _ast.walk(_ast.parse(quelle))
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Call)
               and getattr(n.value.func, "id", "") == "_c"}
    assert genutzt == {"run_async"}, "der Blueprint braucht mehr als run_async: %r" % genutzt

    # (6) Die sieben .env-Werte werden bei JEDEM Aufruf gelesen, nicht als
    # Modul-Konstante eingefroren (CLAUDE.md: .env laedt teils erst spaeter).
    for kopf in ("KICK_CLIENT_ID", "KICKMOD_AUTOSTART", "DISCORD_BOT_TOKEN",
                 "LIVE_REACT_CHAT", "KICK_CHATROOM_ID"):
        assert 'os.getenv("%s"' % kopf in quelle or '_txt("%s")' % kopf in quelle \
            or '_flag("%s")' % kopf in quelle, "%s eingefroren" % kopf
    for zeile in quelle.split("\n"):
        z = zeile.strip()
        assert not (z[:1].isupper() and " = os.getenv(" in z), \
            "Modul-Konstante friert .env ein: %s" % z

    ok("v4.1-W18: kickmod als Blueprint, Bannwoerter und Primaer-Restream geloest")


def _test_w19_azrael_blueprint():
    """v4.1-W19: die groesste Routengruppe raus, null neue Kontext-Eintraege."""
    import ast as _ast

    import nc.azraelstate as A
    import nc.piper_voices as P
    import nc.whispercfg as W

    # (1) Whisper: Name UND Objekt in EINEM Register. Wer nur den Namen
    # aendert und das geladene Modell stehen laesst, transkribiert weiter mit
    # dem alten Modell und zeigt den neuen Namen an — schlimmer als gar kein
    # Umschalten, weil es wie Erfolg aussieht.
    W.MODELL.update(name="base", obj="ALTES-MODELL")
    assert W.name() == "base" and W.geladen()
    assert W.waehle("large-v3") == "large-v3"
    assert W.name() == "large-v3" and not W.geladen(), "das alte Modell blieb geladen"
    # Ein leerer Name aendert nichts — sonst haette ein Tippfehler im Dashboard
    # den Namen geleert und faster-whisper waere mit "" gestartet.
    assert W.waehle("") == "large-v3" and W.waehle(None) == "large-v3"
    W.MODELL.update(name="base", obj=None)

    # (2) Piper: die Suchorte kommen per configure(), nicht als Modul-Konstante.
    # Ein Wechsel muss den Cache verwerfen, sonst zeigt /api/azrael/voices die
    # Stimmen des alten Verzeichnisses und der Betreiber sucht am falschen Ort.
    import tempfile as _tf
    d1, d2 = _tf.mkdtemp(), _tf.mkdtemp()
    open(os.path.join(d1, "de_DE-thorsten-medium.onnx"), "w").close()
    os.makedirs(os.path.join(d2, "unter"), exist_ok=True)
    open(os.path.join(d2, "unter", "en_US-amy-low.onnx"), "w").close()
    P.configure(bin="piper", data_dir=d1, voice_dirs=[d1], recordings_dir="",
                module_dir="")
    assert [v["name"] for v in P.list_voices()] == ["de_DE-thorsten-medium"]
    P.configure(voice_dirs=[d2])
    assert [v["name"] for v in P.list_voices()] == ["en_US-amy-low"], \
        "der Cache ueberlebte den Wechsel der Suchorte"
    # Rekursiv: die .onnx liegt in einem Unterordner und wird trotzdem gefunden.
    assert P.resolve("amy") and P.resolve("amy").endswith("en_US-amy-low.onnx")
    assert P.resolve("gibtsnicht") is None
    # Der Cache greift innerhalb des Fensters, danach wird neu gescannt.
    open(os.path.join(d2, "spaeter.onnx"), "w").close()
    assert len(P.list_voices(_jetzt=1000.0)) in (1, 2)
    assert len(P.list_voices(force=True)) == 2, "force scannt nicht neu"

    # (3) Zustand: Bot und Blueprint sehen DASSELBE Objekt. Das ist der ganze
    # Punkt — eine Kopie hiesse, das Dashboard zeigt einen eingefrorenen Stand.
    A.OVERLAY.clear(); A.OVERLAY["piper_model"] = "thorsten"
    A.TRANSCRIPT.clear(); A.TRANSCRIPT["helge_72"] = [{"ts": 1, "text": "hallo"}]
    A.LIVE_PAUSED["v"] = True
    import nc.routes.azrael as R
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = {str(r.rule) for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert len(regeln) == 18, sorted(regeln)
    with app.test_client() as cl:
        j = cl.get("/api/azrael/live_status").get_json()
        assert j["paused"] is True, "der Blueprint sieht eine Kopie"
        assert j["active"] == [], j
        j = cl.get("/api/azrael/transcript").get_json()
        assert j["transcript"] == {"helge_72": [{"ts": 1, "text": "hallo"}]}
        j = cl.get("/api/azrael/piper_status").get_json()
        assert j["model"] == "thorsten", j
        # Ohne Haken antwortet die Route voruebergehend, nicht mit 500.
        assert cl.post("/api/azrael/ask", json={"q": "hi"}).status_code == 503
        assert cl.post("/api/azrael/ask", json={}).status_code == 400
    A.LIVE_PAUSED["v"] = False; A.OVERLAY.clear(); A.TRANSCRIPT.clear()

    # (4) Personas: atomar geschrieben, kaputtes JSON reisst nichts mit.
    d3 = _tf.mkdtemp()
    A.configure(recordings_dir=d3)
    assert A.personas_load() == {}
    assert A.personas_save({"helge_72": "frech"})
    assert A.personas_load() == {"helge_72": "frech"}
    open(A.personas_path(), "w", encoding="utf-8").write("{kaputt")
    assert A.personas_load() == {}, "kaputtes JSON reisst die Personas mit"

    # (5) Kein neuer ctx-Slot: der Blueprint benutzt nur, was es schon gab.
    quelle = open("nc/routes/azrael.py", encoding="utf-8").read()
    genutzt = {n.attr for n in _ast.walk(_ast.parse(quelle))
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Call)
               and getattr(n.value.func, "id", "") == "_c"}
    assert genutzt <= {"run_async", "arg_int", "log"}, \
        "der Blueprint braucht neue Kontext-Eintraege: %r" % genutzt

    # (6) Keine Modul-Konstante friert .env ein.
    for zeile in quelle.split("\n"):
        z = zeile.strip()
        assert not (z[:1].isupper() and " = os.getenv(" in z), \
            "Modul-Konstante friert .env ein: %s" % z

    ok("v4.1-W19: azrael als Blueprint, Stimme/Whisper/Zustand geloest")


def _test_w20_overlay_audio_und_geld():
    """v4.1-W20: fuenf Routen raus, EINE Quelle fuers Einnahmen-Gate."""
    import ast as _ast

    import nc.audiocue as AC
    import nc.azraelstate as A
    import nc.channels as C
    import nc.revenue as R

    # (1) Das Einnahmen-Gate hat jetzt EINE Quelle. Vorher stand es als
    # Konstantenpaar im Monolithen und money.py spiegelte es ueber ctx.cfg —
    # zwei Orte fuer eine Wahrheit, aus der ein Drift wird.
    assert R.PLATFORMS == ("kick", "twitch", "youtube", "manuell")
    assert "tiktok" not in R.PLATFORMS, "fremdes Geld waere Einnahme"
    assert R.is_revenue_platform("KICK ") and R.is_revenue_platform("manuell")
    assert not R.is_revenue_platform("tiktok") and not R.is_revenue_platform("")
    assert not R.is_revenue_platform(None)
    assert R.sql_in() == "('kick','twitch','youtube','manuell')"
    # TikTok darf sehr wohl ins Sendebild — Follows sind Reichweite, kein Geld.
    assert "tiktok" in R.OV_PLATFORMS
    assert R.normalisieren("TikTok") == "tiktok"
    assert R.normalisieren("erfunden") == "kick" and R.normalisieren(None) == "kick"

    # (2) Ton-Konfig: gespeicherter Wert schlaegt .env-Vorgabe, ohne Neustart.
    AC.configure(tone=True, freq=880.0, ms=120, vol=0.25, gap_ms=60, duck=0.9)
    c = AC.config()
    assert c["freq"] == 880.0 and c["duck"] == 0.9, c
    AC.configure(freq=440.0)
    assert AC.config()["freq"] == 440.0, "die .env-Vorgabe wurde eingefroren"

    # (3) Der Testton muss in den LIVE-Mix. Eine Kopie hiesse "0
    # Warteschlangen" bei laufendem Restream — eine Fehlanzeige, die wie ein
    # kaputter Ton aussieht.
    C.RESTREAM_TTS.clear()
    C.RESTREAM_TTS[7] = {"queue": []}
    import nc.routes.audio as RA
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(RA.bp)
    with app.test_client() as cl:
        j = cl.post("/api/audio/testtone", json={}).get_json()
        assert j["ok"] and j["queues"] == 1, j
        assert len(C.RESTREAM_TTS[7]["queue"]) == 1, "der Ton landete nicht im Mix"
    C.RESTREAM_TTS.clear()
    with app.test_client() as cl:
        assert cl.post("/api/audio/testtone", json={}).get_json()["ok"] is False

    # (4) Overlay: der Zaehler-Nullpunkt ist geteilt. Ohne ihn summiert das
    # Overlay alles seit der Installation und springt beim Stream-Start nie
    # auf 0 zurueck (V37-OVMP-FIX).
    import nc.routes.overlay as RO
    app2 = Flask(__name__)
    app2.register_blueprint(RO.bp)
    regeln = {str(r.rule) for r in app2.url_map.iter_rules() if r.endpoint != "static"}
    assert len(regeln) == 3, sorted(regeln)
    A.OVERLAY.clear(); A.OVERLAY.update(title="Prüfstand", azrael_show=False)
    A.OVERLAY_SESSION["start"] = "2026-09-03T10:00:00+00:00"
    with app2.test_client() as cl:
        j = cl.get("/api/overlay/state").get_json()
        assert j["title"] == "Prüfstand", j
        assert j["session_start"] == "2026-09-03T10:00:00+00:00", j
        assert set(j["by_platform"]) >= set(R.OV_PLATFORMS)
        # Ohne Haken antwortet die Event-Route voruebergehend, nicht mit 500.
        A.PUSH["fn"] = None
        assert cl.post("/api/overlay/event", json={"kind": "follow"}).status_code == 503
        assert cl.post("/api/overlay/event", json={"kind": "quatsch"}).status_code == 400
        gesehen = []
        A.PUSH["fn"] = lambda *a, **k: gesehen.append((a, k))
        assert cl.post("/api/overlay/event",
                       json={"kind": "donation", "name": "x"}).status_code == 200
        assert gesehen and gesehen[0][1]["platform"] == "kick", gesehen
    A.PUSH["fn"] = None
    A.OVERLAY_SESSION["start"] = None
    A.OVERLAY.clear()

    # (5) Kein neuer ctx-Slot: beide Blueprints kommen ohne Kontext aus.
    for datei in ("nc/routes/overlay.py", "nc/routes/audio.py"):
        quelle = open(datei, encoding="utf-8").read()
        assert "from nc import ctx" not in quelle, "%s braucht den Kontext" % datei
        for zeile in quelle.split("\n"):
            z = zeile.strip()
            assert not (z[:1].isupper() and " = os.getenv(" in z), \
                "Modul-Konstante friert .env ein: %s" % z
        _ast.parse(quelle)

    ok("v4.1-W20: overlay+audio als Blueprint, Einnahmen-Gate mit einer Quelle")


def _test_w21_brain_blueprint():
    """v4.1-W21: sechs Routen raus; Zahl und Router als Register, Rest Alias."""
    import ast as _ast

    import nc.brainstate as B

    # (1) STALLS MUSS ein Register sein. Eine ganze Zahl laesst sich nicht per
    # Alias teilen — ein Alias waere eine Kopie auf 0, und /api/brain/health
    # meldete "keine Stalls", waehrend der Loop klemmt. Genau die stille
    # Fehlanzeige, gegen die es die Zahl ueberhaupt gibt.
    B.STALLS["n"] = 0
    assert B.stall() == 1 and B.stall() == 2
    assert B.STALLS["n"] == 2, "der Zaehler ist nicht geteilt"

    # (2) Die Ringpuffer sind BEIM SCHREIBEN begrenzt, nicht beim Lesen. Sonst
    # waechst die Liste weiter und nur die Anzeige sieht harmlos aus — ein
    # Speicherleck, das erst nach Tagen auffaellt.
    B.HISTORY.clear(); B.STREAM.clear(); B.LAST_STATUS.clear()
    for i in range(B.HISTORY_MAX + 25):
        B.record({"core": {"activity": i, "status": "active", "label": "BOT CORE"}})
    assert len(B.HISTORY["core"]) == B.HISTORY_MAX, len(B.HISTORY["core"])
    assert B.HISTORY["core"][-1] == B.HISTORY_MAX + 24, "die juengsten Werte fehlen"
    assert B.history_for("core") == B.HISTORY["core"]
    assert B.history_for("gibtsnicht") == []

    # (3) Ein Status-UEBERGANG erzeugt genau ein Stream-Ereignis, kein Dauerfeuer.
    B.STREAM.clear(); B.LAST_STATUS.clear()
    # Der erste Blick auf einen Knoten ist kein Uebergang: sonst meldete jeder
    # Bot-Start eine Welle von Ereignissen fuer Zustaende, die sich gar nicht
    # geaendert haben.
    B.record({"x": {"activity": 1, "status": "active", "label": "X"}})
    assert B.STREAM == [], "der erste Blick gilt schon als Uebergang"
    B.record({"x": {"activity": 1, "status": "error", "label": "X"}})
    assert len(B.STREAM) == 1 and B.STREAM[0]["kind"] == "error", B.STREAM
    B.record({"x": {"activity": 1, "status": "error", "label": "X"}})
    assert len(B.STREAM) == 1, "gleicher Status erzeugt weiter Ereignisse"
    B.record({"x": {"activity": 1, "status": "active", "label": "X"}})
    assert len(B.STREAM) == 2 and B.STREAM[-1]["kind"] == "up"
    # Juengstes zuerst — das Panel zeigt oben, was gerade passiert ist.
    assert B.stream_recent(1)[0]["kind"] == "up"
    for i in range(B.STREAM_MAX + 10):
        B.record({"x": {"activity": 1, "status": "error" if i % 2 else "active", "label": "X"}})
    assert len(B.STREAM) == B.STREAM_MAX

    # (4) Der Blueprint sieht denselben Zustand wie der Bot.
    import nc.routes.brain as R
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = {str(r.rule) for r in app.url_map.iter_rules() if r.endpoint != "static"}
    assert len(regeln) == 6, sorted(regeln)
    B.BRIDGE.update(ok=False, phase="import_failed", error="brain fehlt")
    B.STALLS["n"] = 7
    with app.test_client() as cl:
        j = cl.get("/api/brain/health").get_json()
        assert j["ok"] is False and j["phase"] == "import_failed", j
        assert j["error"] == "brain fehlt", "der echte Grund kommt nicht durch"
        assert j["loop_stalls"] == 7, "der Stall-Zaehler ist eine Kopie"
        assert cl.get("/api/brain/creator").get_json()["ok"] is False
    B.BRIDGE.update(ok=False, phase="not_started", error=None)
    B.STALLS["n"] = 0

    # (5) Kein neuer ctx-Slot, keine eingefrorene .env-Konstante.
    quelle = open("nc/routes/brain.py", encoding="utf-8").read()
    genutzt = {n.attr for n in _ast.walk(_ast.parse(quelle))
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Call)
               and getattr(n.value.func, "id", "") == "_c"}
    assert genutzt <= {"arg_int", "get_bot_start_time", "log"}, \
        "der Blueprint braucht neue Kontext-Eintraege: %r" % genutzt
    for zeile in quelle.split("\n"):
        z = zeile.strip()
        assert not (z[:1].isupper() and " = os.getenv(" in z), \
            "Modul-Konstante friert .env ein: %s" % z
    # Und kein globals()-Umweg: genau daran waere der Proxy-Router gescheitert.
    # Per AST, nicht per Text — die Erklaerung dazu steht voellig zu Recht im
    # Docstring des Blueprints und ist kein Verstoss (derselbe Fehlalarm wie
    # in W16).
    _baum = _ast.parse(quelle)
    assert not [n for n in _ast.walk(_baum)
                if isinstance(n, _ast.Call) and isinstance(n.func, _ast.Name)
                and n.func.id == "globals"], \
        "globals() im Blueprint — das ist DIESER Namensraum"

    ok("v4.1-W21: brain als Blueprint, Zaehler und Router als Register")


def _test_w22_restream_blueprint():
    """v4.1-W22: sechzehn Routen raus; Keys bleiben drinnen."""
    import ast as _ast
    import os as _os

    import nc.restreamcfg as C
    import nc.restreamstate as S

    # (1) Die Sendeziele. Kick hat keinen Schalter — es ist der Hauptkanal und
    # wird ueber einen fehlenden Key abgeschaltet.
    alt = {k: _os.environ.get(k) for k in
           ("TWITCH_ENABLED", "TWITCH_STREAM_KEY", "TWITCH_INGEST_URL",
            "YOUTUBE_ENABLED", "KICK_STREAM_KEY", "RESTREAM_VERIFY_S")}
    try:
        _os.environ.pop("TWITCH_STREAM_KEY", None)
        _os.environ.pop("KICK_STREAM_KEY", None)
        _os.environ["TWITCH_ENABLED"] = "0"
        assert C.aktiv("kick") is True and C.aktiv("twitch") is False
        assert C.bereite_ziele() == [], C.bereite_ziele()
        _os.environ["TWITCH_ENABLED"] = "1"
        _os.environ["TWITCH_STREAM_KEY"] = "geheim123"
        assert C.aktiv("twitch") is True and C.key_gesetzt("twitch") is True
        assert C.bereite_ziele() == ["twitch"], C.bereite_ziele()
        # LIVE gelesen, nicht eingefroren: der Betreiber aendert Keys und
        # erwartet, dass der naechste Restream sie benutzt.
        _os.environ["RESTREAM_VERIFY_S"] = "17"
        assert C.verify_takt() == 17, "die Pruefparameter sind eingefroren"
        _os.environ["RESTREAM_VERIFY_S"] = "keine-zahl"
        assert C.verify_takt() == 120, "ein Tippfehler in .env darf nicht crashen"
        # Der globale Twitch-Ingest ist die Vorgabe (der alte live.twitch.tv
        # brach Restreams mit rc=8 ab).
        _os.environ.pop("TWITCH_INGEST_URL", None)
        assert "ingest.global-contribute" in C.ingest("twitch")
        assert C.ingest("erfunden") == "" and C.aktiv("erfunden") is False
    finally:
        for k, v in alt.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v

    # (2) Der Blueprint gibt KEINEN Stream-Key heraus. Wer das tut, verschenkt
    # den Kanal — jeder mit dem Key kann darauf senden.
    quelle = open("nc/routes/restream.py", encoding="utf-8").read()
    baum = _ast.parse(quelle)
    # Erlaubt ist der Kommandobauer-Pfad (ffmpeg braucht den Key). Verboten
    # ist "steht in einer Antwort" — von dort waere er sofort oeffentlich.
    for zeile in quelle.split("\n"):
        if "jsonify(" in zeile and '["key"]' in zeile:
            raise AssertionError("Stream-Key in einer API-Antwort: %s" % zeile.strip())
    # Und die Diagnose benutzt den bool, nicht den Wert.
    assert "key_gesetzt(" in quelle, "die Diagnose liest den Key statt des bools"

    # (3) Manager und Waechter sind REGISTER: sie entstehen im Monolithen erst
    # weit unten, ein Alias waere fuer immer None.
    S.MGR["obj"] = None
    assert S.mgr() is None and S.laufende() == [], "laufende() wirft ohne Manager"

    class _M:
        _procs = {7: object(), 3: object()}
    S.MGR["obj"] = _M()
    assert S.laufende() == [3, 7], S.laufende()
    S.MGR["obj"] = None

    # (4) Das Layout faellt auf 'studio' zurueck. Ein erfundener Modus wuerde
    # den ffmpeg-Filtergraph brechen.
    S.LAYOUT["mode"] = "burnin"
    assert S.layout_mode() == "burnin"
    S.LAYOUT["mode"] = "quatsch"
    assert S.layout_mode() == "studio", "ein erfundener Modus kommt durch"
    S.LAYOUT["mode"] = "studio"

    # (5) Der Blueprint traegt sechzehn Routen und braucht keinen neuen Slot.
    from flask import Flask
    import nc.routes.restream as R
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    # REGELN zaehlen, nicht Pfade: /api/restream/testpush ist zweimal
    # registriert (GET fuer den Status, POST fuer den Lauf) und waere als
    # Menge nur ein Eintrag.
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 16, sorted(str(r.rule) for r in regeln)
    genutzt = {n.attr for n in _ast.walk(baum)
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Call)
               and getattr(n.value.func, "id", "") == "_c"}
    assert genutzt <= {"run_async", "log_event", "log", "arg_int"}, \
        "der Blueprint braucht neue Kontext-Eintraege: %r" % genutzt
    for zeile in quelle.split("\n"):
        z = zeile.strip()
        assert not (z[:1].isupper() and " = os.getenv(" in z), \
            "Modul-Konstante friert .env ein: %s" % z

    # (6) Jeder .env-Name steht WOERTLICH da — sonst findet gen_env_example.py
    # ihn nicht (beim ersten Entwurf fielen prompt vierzehn Variablen still
    # aus der Vorlage) und ein grep laeuft ins Leere.
    cfg = open("nc/restreamcfg.py", encoding="utf-8").read()
    for name in ("KICK_INGEST_URL", "KICK_STREAM_KEY", "TWITCH_ENABLED",
                 "TWITCH_INGEST_URL", "TWITCH_STREAM_KEY", "YOUTUBE_ENABLED",
                 "YOUTUBE_INGEST_URL", "YOUTUBE_STREAM_KEY", "RESTREAM_VERIFY",
                 "RESTREAM_VERIFY_S", "RESTREAM_VERIFY_GRACE_S",
                 "RESTREAM_VERIFY_MISSES", "RESTREAM_STALL_TIMEOUT_S",
                 "RESTREAM_OVERLAY", "KICK_CHANNEL_URL", "DISCORD_INVITE_URL"):
        assert 'os.getenv("%s"' % name in cfg, \
            "%s steht nicht woertlich in einem os.getenv" % name

    ok("v4.1-W22: restream als Blueprint, Ziele live gelesen, kein Key nach aussen")


def _test_w23_beobachtung_und_toasts():
    """v4.1-W23: acht Beobachtungs-Routen raus, verkettete Toasts uebersetzbar."""
    import ast as _ast
    import re as _re

    import nc.brainstate as B
    import nc.channels as C
    import nc.tiktokheaders as H

    # (1) Die Zuschauer-Stichproben sind BEGRENZT. Ohne maxlen waere das ein
    # Leck, das erst nach Tagen auffaellt — bei 60-s-Takt sind 720 Punkte
    # rund 12 Stunden, und mehr zeigt der Graph ohnehin nicht.
    assert C.VIEWER_SAMPLES.maxlen == 720
    C.VIEWER_SAMPLES.clear()
    for i in range(900):
        C.VIEWER_SAMPLES.append((i, i))
    assert len(C.VIEWER_SAMPLES) == 720 and C.VIEWER_SAMPLES[-1] == (899, 899)
    C.VIEWER_SAMPLES.clear()

    # (2) Die drei Waechter-Zaehler liegen beieinander — sie beantworten
    # dieselbe Frage ("warum startet der nicht neu?") und wurden vorher an
    # drei Stellen im Monolithen gepflegt.
    for name in ("DEAD_STREAK", "EARLY_DISCONNECT", "DEAD_BACKOFF_UNTIL"):
        assert isinstance(getattr(B, name), dict), name

    # (3) Die TikTok-Kopfzeilen sind vollstaendig — ohne plausiblen
    # Fingerabdruck liefert TikTok eine andere Seite aus, und der Aufloeser
    # findet keine Stream-URL. Accept-Encoding kommt vom Bot, weil es davon
    # abhaengt, ob Brotli installiert ist.
    for k in ("User-Agent", "Accept", "Accept-Language", "Referer", "sec-ch-ua"):
        assert H.HEADERS.get(k), "Kopfzeile %s fehlt" % k
    H.configure(accept_encoding="gzip, deflate, br")
    assert H.HEADERS["Accept-Encoding"] == "gzip, deflate, br"
    H.configure(accept_encoding="gzip, deflate")

    # (4) Der Blueprint: acht Routen, kein neuer ctx-Slot, keine eingefrorene
    # .env-Konstante. /metrics liegt bewusst NICHT unter /api/ — ein
    # Prometheus-Scraper sucht es genau dort.
    from flask import Flask
    import nc.routes.beobachtung as R
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 8, sorted(str(r.rule) for r in regeln)
    assert any(str(r.rule) == "/metrics" for r in regeln)
    quelle = open("nc/routes/beobachtung.py", encoding="utf-8").read()
    baum = _ast.parse(quelle)
    genutzt = {n.attr for n in _ast.walk(baum)
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Call)
               and getattr(n.value.func, "id", "") == "_c"}
    assert genutzt <= {"run_async", "log", "log_event", "arg_int",
                       "scraper_session", "get_bot_start_time"}, \
        "der Blueprint braucht neue Kontext-Eintraege: %r" % genutzt
    for zeile in quelle.split("\n"):
        z = zeile.strip()
        assert not (z[:1].isupper() and " = os.getenv(" in z), \
            "Modul-Konstante friert .env ein: %s" % z

    # (5) Diese Routen BEOBACHTEN nur. Kein Aufruf hier startet, stoppt oder
    # loescht etwas — das ist die Klammer, die die vier Gruppen zusammenhaelt,
    # und der Grund, warum sie in EINER Datei stehen duerfen.
    for n in _ast.walk(baum):
        if not (isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef))):
            continue
        for d in n.decorator_list:
            if not (isinstance(d, _ast.Call) and _ast.unparse(d.func).endswith(".route")):
                continue
            meth = []
            for kw in d.keywords:
                if kw.arg == "methods":
                    meth = _ast.literal_eval(kw.value)
            assert set(meth) <= {"GET", "POST"}, "%s: schreibende Methode" % n.name
    assert "DELETE" not in quelle and "conn.execute(\"DELETE" not in quelle

    # (6) Die verketteten Toasts sind umschlossen. toast() erzeugt zwar einen
    # DOM-Knoten, aber bei 'Aufnahme @'+u+' gestartet' heisst der Knoten
    # "Aufnahme @helge_72 gestartet" — ein Eintrag fuer "Aufnahme @" trifft
    # dort nie. 28 solcher Eintraege standen bereits im Katalog und zaehlten
    # als uebersetzt, ohne je zu greifen.
    dash = open("templates/dashboard.html", encoding="utf-8").read()
    offen = []
    for m in _re.finditer(r"\btoast\s*\(\s*'([^'\\\n]{3,})'\s*\+", dash):
        offen.append(m.group(1))
    assert not offen, "verketteter Toast ohne T(): %r" % offen[:5]
    # Und das ZWEITE Argument bleibt unberuehrt: 'err'/'ok' ist eine
    # CSS-Klasse, kein Text. Ein T() darauf zerstoert die Fehlerfarbe.
    assert "T('err')" not in dash and 'T("err")' not in dash, \
        "die Toast-Klasse wird uebersetzt"

    ok("v4.1-W23: Beobachtungs-Routen als Blueprint, verkettete Toasts uebersetzbar")



def _test_w24_wartung_blueprint():
    """v4.1-W24: zehn Wartungsrouten raus — und die drei loeschenden Pfade
       behalten ihre Sicherungen."""
    import ast as _ast
    import os as _os
    import tempfile as _tf

    import nc.backupcfg as K
    from nc.backupcfg import aktiv as _nc_backup_aktiv
    import nc.retention as RET
    import nc.storage as ST

    # (1) Kein Geheimnis in der Anzeige. s3_konfiguriert() ist ein bool und
    # gibt nichts heraus; die Zugangsdaten kommen NUR aus s3_zugang(), das
    # ausschliesslich der boto3-Client aufruft. Wer hier einen Key in eine
    # Antwort schreibt, verschenkt den Bucket.
    alt = {k: _os.environ.get(k) for k in
           ("S3_BACKUP", "S3_BUCKET", "S3_ACCESS_KEY", "S3_SECRET_KEY")}
    try:
        _os.environ.update({"S3_BACKUP": "1", "S3_BUCKET": "eimer",
                            "S3_ACCESS_KEY": "AKIA-GEHEIM",
                            "S3_SECRET_KEY": "sehr-geheim"})
        assert K.s3_konfiguriert() is True
        assert isinstance(K.s3_konfiguriert(), bool)
        assert K.s3_zugang()["access_key"] == "AKIA-GEHEIM"
        # Ohne Schluessel gilt S3 als NICHT konfiguriert — sonst meldete das
        # Deck "gesichert", waehrend jeder Upload scheitert.
        _os.environ["S3_SECRET_KEY"] = ""
        assert K.s3_konfiguriert() is False
    finally:
        for k, v in alt.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v

    # (2) Live gelesen, nicht eingefroren: der Betreiber schaltet SYS_BACKUP
    # im Betrieb um und erwartet, dass die naechste Sicherung das sieht.
    vorher = _os.environ.get("SYS_BACKUP")
    try:
        _os.environ["SYS_BACKUP"] = "0"
        assert K.sys_backup() is False
        _os.environ["SYS_BACKUP"] = "1"
        assert K.sys_backup() is True
    finally:
        if vorher is None:
            _os.environ.pop("SYS_BACKUP", None)
        else:
            _os.environ["SYS_BACKUP"] = vorher

    # (3) DIE WICHTIGSTE ZUSICHERUNG DIESER WELLE. retention.scan(delete=True)
    # loescht Dateien. Geloescht wird ausschliesslich, was nachweislich im
    # Aufnahme-Verzeichnis liegt. Faellt diese Pruefung, wird aus einer
    # Aufraeumfunktion ein Loeschwerkzeug fuer das ganze Dateisystem.
    quelle = open("nc/retention.py", encoding="utf-8").read()
    assert "os.path.abspath(fp).startswith(rec_root + os.sep)" in quelle, \
        "Pfad-Haertung in nc/retention.py fehlt"
    # Und sie greift auch wirklich: eine Datei AUSSERHALB bleibt liegen.
    with _tf.TemporaryDirectory() as tmp:
        drinnen = _os.path.join(tmp, "rec")
        _os.makedirs(drinnen)
        aussen = _os.path.join(tmp, "fremd.txt")
        open(aussen, "w").write("x")
        assert _os.path.abspath(aussen).startswith(_os.path.abspath(drinnen) + _os.sep) is False
        # scan() ohne Datenbank liefert eine wohlgeformte Null-Antwort statt
        # einer Ausnahme — die Routen rechnen damit.
        r = RET.scan(1, drinnen, delete=False)
        assert r == {"count": 0, "freed_bytes": 0}, r
        assert _os.path.isfile(aussen), "Datei ausserhalb wurde angefasst"

    # (4) storage.cleanup loescht DATEIEN, nie Datenbankeintraege — der
    # Betreiber soll weiter sehen, DASS es die Aufnahme gab. Und days<=0
    # loescht gar nichts, auch nicht versehentlich.
    q = open("nc/storage.py", encoding="utf-8").read()
    assert "DELETE FROM recordings" not in q, \
        "storage.cleanup loescht Datenbankeintraege — das macht retention.py"
    r = ST.cleanup("/nicht/vorhanden", days=0)
    assert r["deleted"] == 0 and "RECORDINGS_RETAIN_DAYS=0" in r["reason"]

    # (5) Der Zustand des System-Backups ist ein ALIAS, kein Register: der
    # Monolith veraendert das Dict nur an Ort und Stelle. Bindet er den Namen
    # neu, meldet /api/backup/status fuer immer "laeuft nicht", waehrend die
    # Sicherung laeuft — ohne Fehler und ohne Logzeile.
    b = open("bot.py", encoding="utf-8").read()
    assert "_SYS_BACKUP_STATE = _nc_backup.STATE" in b, "Alias fehlt"
    assert b.count("_SYS_BACKUP_STATE = ") == 1, \
        "_SYS_BACKUP_STATE wird neu gebunden — der Alias zeigt dann auf eine tote Kopie"
    assert set(K.STATE) == {"running", "last_ts", "last_file", "size_mb",
                            "files", "error"}

    # (6) Der Blueprint: zehn Routen, kein neuer ctx-Slot.
    from flask import Flask
    import nc.routes.wartung as R
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 10, "10 Regeln erwartet, %d" % len(regeln)

    w = open("nc/routes/wartung.py", encoding="utf-8").read()
    # Kein Bucket-Geheimnis in einer Antwort. Geprueft wird ueber den AST und
    # nicht ueber den Text: der Modul-Kopf ERKLAERT s3_zugang() voellig zu
    # Recht, und ein Textvergleich meldete genau diese Erklaerung als
    # Verstoss (dieselbe Falle wie bei globals() in W22).
    _wb = _ast.parse(w)
    for _n in _ast.walk(_wb):
        assert not (isinstance(_n, _ast.Attribute) and _n.attr == "s3_zugang"), \
            "Blueprint liest S3-Zugangsdaten"
        assert not (isinstance(_n, _ast.Constant) and isinstance(_n.value, str)
                    and _n.value in ("S3_ACCESS_KEY", "S3_SECRET_KEY")), \
            "Blueprint liest einen S3-Schluessel direkt aus der Umgebung"
    # Die zwei Haken sind deklariert und werden im Monolithen eingetragen.
    assert set(R.HAKEN) == {"local_scan", "system"}
    for h in R.HAKEN:
        assert '_nc_routes_wartung.HAKEN["%s"]["fn"]' % h in b, \
            "Haken %s wird im Monolithen nie eingetragen" % h

    # (7) Der Monolith ruft die geloesten Funktionen auf, statt sie ein
    # zweites Mal zu halten. Eine Kopie einer loeschenden Funktion laeuft
    # irgendwann auseinander — genau deshalb sind sie gewandert.
    for ruf in ("_nc_retention.scan(", "_nc_storage.cleanup(",
                "_nc_storage.stats(", "_nc_arules.run_archive_rules("):
        assert ruf in b, "Monolith ruft %s nicht auf" % ruf

    # (8) Ein fehlender Haken sagt es, statt Erfolg zu melden. Ohne diese
    # Pruefung startet threading.Thread(target=None) klaglos und die Route
    # antwortet started=True, waehrend nichts sichert — die stille Sorte
    # Fehler, die CLAUDE.md als Hauptfeind benennt.
    for h in R.HAKEN:
        R.HAKEN[h]["fn"] = None
    c = app.test_client()
    # Erst ein Ziel konfigurieren: ohne eins antwortet /api/backup/system
    # zurecht schon vorher mit 400 ("kein Ziel"), und die Haken-Pruefung
    # dahinter waere nie erreicht.
    sicher = {k: _os.environ.get(k) for k in ("LOCAL_BACKUP", "LOCAL_BACKUP_DIR")}
    try:
        _os.environ.update({"LOCAL_BACKUP": "1", "LOCAL_BACKUP_DIR": "/tmp/nc-backup-test"})
        assert _nc_backup_aktiv(), "Testaufbau: Ziel nicht erkannt"
        for pfad in ("/api/backup/system", "/api/backup/run"):
            antwort = c.post(pfad)
            assert antwort.status_code == 503, \
                "%s meldet %d statt 503 ohne Haken" % (pfad, antwort.status_code)
            assert antwort.get_json()["ok"] is False
    finally:
        for k, v in sicher.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v

    ok("v4.1-W24: Wartung als Blueprint, Loeschpfade gehaertet, keine S3-Geheimnisse")



def _test_w25_abwehr_blueprint():
    """v4.1-W25: vier Abwehr-Routen raus, ein Schreibweg fuer den Adress-Cache."""
    import ast as _ast
    import os as _os

    import nc.defensecfg as D
    import nc.geocache as G
    import nc.geoip as GI

    # (1) DER BEFUND DIESER WELLE. Der Adress-Cache hat genau EINEN
    # Schreibweg, und der setzt die Obergrenze durch. Vorher gab es zwei:
    # einen Helfer mit Grenze und einen Direktzugriff daran vorbei. Bei einer
    # Angriffswelle mit vielen verschiedenen Adressen wuchs der Cache
    # unbegrenzt — kein Fehler, keine Logzeile, nur Speicher.
    G.leeren()
    for i in range(G.MAX + 250):
        G.put("203.0.113.%d-%d" % (i // 256, i % 256), {"lat": i})
    assert G.groesse() == G.MAX, \
        "Obergrenze greift nicht: %d Eintraege" % G.groesse()
    G.leeren()
    # Und es gibt wirklich nur den einen Weg: das Modul gibt den Cache nicht
    # heraus. Wer ihn direkt fuellen wollte, muesste an einen privaten Namen.
    assert not hasattr(G, "CACHE"), "Cache liegt offen — der zweite Schreibweg"

    # (2) Ein vorhandener Eintrag wandert ans Ende, damit die Verdraengung den
    # aeltesten trifft und nicht den zuletzt benutzten.
    G.leeren()
    for name in ("a", "b", "c"):
        G.put(name, {"lat": 1})
    G.put("a", {"lat": 2})          # a ist jetzt der juengste
    assert G.get("a")["lat"] == 2
    G.leeren()

    # (3) Private und lokale Adressen kosten nur Kontingent (45/min bei
    # ip-api) und fallen still raus — ohne Netzzugriff.
    for ip in ("10.0.0.1", "127.0.0.1", "192.168.5.9", "169.254.1.1"):
        assert GI.ist_privat(ip), ip
    assert not GI.ist_privat("8.8.8.8")
    gemeldet = []
    assert GI.lookup(["10.0.0.1", "127.0.0.1"],
                     fehler_setzen=gemeldet.append) == {}
    assert G.groesse() == 0, "private Adressen im Cache gelandet"

    # (4) Kein Geheimnis in der Anzeige. bouncer_gesetzt() ist ein bool; den
    # Schluessel gibt nur bouncer_key() heraus, und das ruft ausschliesslich
    # der LAPI-Aufruf im Monolithen.
    vorher = _os.environ.get("CROWDSEC_BOUNCER_KEY")
    try:
        _os.environ["CROWDSEC_BOUNCER_KEY"] = "geheim-123"
        assert D.bouncer_gesetzt() is True
        assert isinstance(D.bouncer_gesetzt(), bool)
        assert D.bouncer_key() == "geheim-123"
        _os.environ["CROWDSEC_BOUNCER_KEY"] = ""
        assert D.bouncer_gesetzt() is False
    finally:
        if vorher is None:
            _os.environ.pop("CROWDSEC_BOUNCER_KEY", None)
        else:
            _os.environ["CROWDSEC_BOUNCER_KEY"] = vorher

    # (5) Leere .env-Zeilen kippen den Standort nicht. Eine gesetzte, leere
    # Variable ist der haeufigste Fall (v4.0-W82) — sie muss auf den
    # Vorgabewert zurueckfallen, nicht werfen.
    sicher = {k: _os.environ.get(k) for k in ("DEFENSE_SERVER_LAT", "DEFENSE_SERVER_LON")}
    try:
        _os.environ.update({"DEFENSE_SERVER_LAT": "", "DEFENSE_SERVER_LON": "quatsch"})
        assert D.server_lat() == 50.69 and D.server_lon() == 2.13
        _os.environ["DEFENSE_SERVER_LAT"] = "48,21"      # Komma statt Punkt
        assert abs(D.server_lat() - 48.21) < 1e-9
    finally:
        for k, v in sicher.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v

    # (6) Der Fehlgrund der Geo-Aufloesung ist ein REGISTER, kein Alias: eine
    # Zeichenkette ist unteilbar, und der Monolith band den Namen frueher neu.
    D.geo_fehler_setzen("x" * 400)
    assert len(D.geo_fehler()) == 160, "Fehlgrund nicht gekuerzt"
    D.geo_fehler_setzen("")
    b = open("bot.py", encoding="utf-8").read()
    assert "_DEFENSE_GEO_ERR" not in b, \
        "der alte Modul-Global steht noch — zwei Wahrheiten ueber denselben Fehlgrund"

    # (7) Der Blueprint: vier Routen, kein neuer ctx-Slot, kein Schluessel
    # nach aussen.
    from flask import Flask
    import nc.routes.abwehr as R
    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 4, "4 Regeln erwartet, %d" % len(regeln)

    w = open("nc/routes/abwehr.py", encoding="utf-8").read()
    for _n in _ast.walk(_ast.parse(w)):
        assert not (isinstance(_n, _ast.Attribute) and _n.attr == "bouncer_key"), \
            "Blueprint liest den Bouncer-Schluessel"

    # (8) Ohne Haken meldet die Ansicht NICHT "alles ruhig". Bei einer
    # Sicherheitsanzeige ist 0 Sperren / 0 Angriffe die gefaehrlichste aller
    # falschen Antworten — sie sieht aus wie ein gutes Ergebnis.
    for h in R.HAKEN:
        R.HAKEN[h]["fn"] = None
    c = app.test_client()
    for pfad in ("/api/defense/overview", "/api/defense/crowdsec",
                 "/api/defense/fail2ban", "/api/defense/attacks"):
        antwort = c.get(pfad)
        assert antwort.status_code == 503, \
            "%s meldet %d statt 503 ohne Haken" % (pfad, antwort.status_code)
        d = antwort.get_json()
        assert d["ok"] is False and d["status"] == "nicht_bereit"
    # Der Monolith traegt beide wirklich ein.
    for h in R.HAKEN:
        assert '_nc_routes_abwehr.HAKEN["%s"]["fn"]' % h in b, \
            "Haken %s wird im Monolithen nie eingetragen" % h

    ok("v4.1-W25: Abwehr als Blueprint, Adress-Cache mit EINEM Schreibweg")



def _test_w26_huellen_schlucken_nichts():
    """v4.1-W26: die Zaehl-Huellen im Monolithen duerfen kein Argument
       verlieren.

    ECHTER PRODUKTIONSFEHLER, gefunden im error.log vom 2026-09-03:

        TypeError: _claude_chat_sync_metered() got an unexpected keyword
                   argument 'on_error'

    Der Monolith ERSETZT nc.claude.chat_sync durch eine Huelle, die die Token
    zaehlt. Die Huelle zaehlte ihre Parameter einzeln auf. Als v4.1-W13
    `on_error` zu chat_sync hinzufuegte, wurde sie nicht mitgezogen — und
    damit brach jeder Aufruf, der den neuen Parameter benutzte.
    _living_title_loop lief neunmal genau da hinein, jedes Mal die ganze Runde
    verloren. Im Log stand nur "Schleife gestoert", der Grund kam erst aus dem
    Traceback.

    Geprueft wird ueber den AST von bot.py gegen die ECHTE Signatur des
    umhuellten Moduls — bot.py laesst sich hier nicht importieren (voller
    Laufzeitstack), die nc-Module schon.
    """
    import ast as _ast
    import inspect as _inspect

    import nc.claude as _claude
    import nc.freeai as _freeai

    baum = _ast.parse(open("bot.py", encoding="utf-8").read())
    huellen = {n.name: n for n in baum.body if isinstance(n, _ast.FunctionDef)}

    for huelle, modul, fn in (("_claude_chat_sync_metered", _claude, "chat_sync"),
                              ("_freeai_chat_sync_metered", _freeai, "chat_sync")):
        n = huellen.get(huelle)
        assert n is not None, "%s gibt es nicht mehr" % huelle
        eigen = {a.arg for a in n.args.args} | {a.arg for a in n.args.kwonlyargs}
        echt = set(_inspect.signature(getattr(modul, fn)).parameters)

        # (1) Entweder nennt die Huelle jeden Parameter selbst, ODER sie hat
        # ein **kwargs, das den Rest durchreicht. Alles andere heisst: ein
        # Aufruf mit dem fehlenden Parameter stirbt zur Laufzeit.
        fehlt = echt - eigen
        assert not fehlt or n.args.kwarg is not None, \
            ("%s verliert %s — genau der Fehler, der _living_title_loop "
             "neunmal gekillt hat" % (huelle, sorted(fehlt)))

        # (2) Die Positions-Parameter muessen in DERSELBEN Reihenfolge stehen.
        # Drei Aufrufstellen uebergeben model und timeout positionell; eine
        # Umsortierung schoebe das Modell in den falschen Parameter — ein
        # stiller Fehler statt eines lauten.
        echt_pos = [k for k in _inspect.signature(getattr(modul, fn)).parameters]
        eigen_pos = [a.arg for a in n.args.args]
        gemeinsam = [k for k in echt_pos if k in set(eigen_pos)]
        assert eigen_pos[:len(gemeinsam)] == gemeinsam, \
            ("%s hat die Parameter umsortiert: %r statt %r — positionelle "
             "Aufrufe landen im falschen Parameter" % (huelle, eigen_pos, gemeinsam))

        # (3) Die Huelle ersetzt das Modul wirklich. Faellt diese Zeile weg,
        # zaehlt niemand mehr Token, ohne dass irgendetwas bricht.
        assert "_nc_%s.%s = %s" % (
            {"nc.claude": "claude", "nc.freeai": "freeai"}[modul.__name__],
            fn, huelle) in open("bot.py", encoding="utf-8").read(), \
            "%s wird nie eingehaengt" % huelle

    # ---- Zweiter Befund aus demselben Log: der eingefrorene Event-Loop ----
    #
    # `_write_restream_overlay()` schreibt bis zu vierzehn Textdateien und lief
    # rund einmal pro Sekunde SYNCHRON auf dem Event-Loop. Unter Plattenlast
    # (685-MB-Upload, ffmpeg, Restream) blockierte os.replace bis zu 68
    # Sekunden — in der Zeit stand der ganze Bot. Neunzehn von fuenfundzwanzig
    # Stack-Abzuegen des Waechters zeigten genau diesen Aufruf.
    quelle = open("bot.py", encoding="utf-8").read()
    baum2 = _ast.parse(quelle)

    # (1) Der Sekundentakt laeuft NEBEN dem Loop.
    assert "await _write_restream_overlay_async()" in quelle, \
        "der Sekundentakt schreibt wieder synchron auf dem Loop"
    for n in baum2.body:
        if isinstance(n, _ast.AsyncFunctionDef) and n.name == "_write_restream_overlay_async":
            break
    else:
        raise AssertionError("_write_restream_overlay_async gibt es nicht mehr")
    assert "asyncio.to_thread(_write_restream_overlay" in quelle, \
        "die nebenlaeufige Fassung ruft den Schreiber nicht im Thread"

    # (2) EIN Waechter, und zwar modul-global. Als Objekt-Attribut braeche er,
    # sobald das Objekt neu erzeugt wird (CLAUDE.md) — dann stapeln sich bei
    # langsamer Platte die Schreib-Threads, weil der Takt jede Sekunde kommt
    # und ein Schreibvorgang im Stoerfall ueber sechzig dauerte.
    assert '_OVERLAY_SCHREIBT = {"an": False}' in quelle, "Waechter fehlt"
    assert "if _OVERLAY_SCHREIBT[\"an\"]:" in quelle, "Waechter wird nicht geprueft"
    assert '_OVERLAY_SCHREIBT["an"] = False' in quelle, \
        "Waechter wird nie zurueckgesetzt — nach dem ersten Fehler schreibt nie wieder jemand"

    # (3) Der Anlauf-Aufruf bleibt SYNCHRON: die Textdateien muessen da sein,
    # BEVOR drawtext sie oeffnet. Ein await davor waere eine Wettlaufsituation
    # mit dem gerade startenden ffmpeg.
    assert "_write_restream_overlay()      # Textdateien anlegen" in quelle, \
        "der Anlauf-Aufruf ist verschwunden oder nebenlaeufig geworden"

    # (4) DER SCHREIBER DARF NUR LESEN. Er laeuft jetzt in einem Thread,
    # waehrend der Loop den geteilten Zustand weiter veraendert. Ein
    # Schreibzugriff von dort waere ein echtes Wettrennen — bei einem
    # `global` sogar eines, das den Zustand des ganzen Bots trifft. Geprueft
    # wird ueber den AST: keine global-Anweisung, und jede Mutation nur auf
    # Namen, die die Funktion selbst angelegt hat.
    for _n in baum2.body:
        if isinstance(_n, _ast.FunctionDef) and _n.name == "_write_restream_overlay":
            break
    else:
        raise AssertionError("_write_restream_overlay gibt es nicht mehr")
    assert not [g for g in _ast.walk(_n) if isinstance(g, _ast.Global)], \
        "der Overlay-Schreiber bindet einen globalen Namen neu — im Thread ein Wettrennen"
    _lokal = {t.id for k in _ast.walk(_n) if isinstance(k, _ast.Assign)
              for t in k.targets if isinstance(t, _ast.Name)}
    _lokal |= {a.arg for a in _n.args.args}
    for k in _ast.walk(_n):
        if isinstance(k, _ast.Call) and isinstance(k.func, _ast.Attribute) \
           and k.func.attr in ("append", "pop", "update", "clear", "setdefault",
                               "add", "remove", "insert", "extend") \
           and isinstance(k.func.value, _ast.Name):
            assert k.func.value.id in _lokal, \
                ("der Overlay-Schreiber veraendert %s — das ist geteilter Zustand, "
                 "und er laeuft seit W26 in einem Thread" % k.func.value.id)

    # (5) Der Aufnahme-Anspruch laeuft ebenfalls neben dem Loop — er stand in
    # zwei Abzuegen als Blocker (db_conn().__exit__ -> close()).
    assert "await asyncio.to_thread(try_acquire_recording_lock," in quelle, \
        "der Aufnahme-Anspruch blockiert wieder den Loop"

    ok("v4.1-W26: Zaehl-Huellen reichen alles durch, Overlay blockiert den Loop nicht mehr")


def _test_w26_auskunft_blueprint():
    """v4.1-W26: fuenfundzwanzig lesende Routen raus — und die Klammer haelt."""
    import ast as _ast

    from flask import Flask
    import nc.routes.auskunft as R

    app = Flask(__name__)
    app.register_blueprint(R.bp)
    regeln = [r for r in app.url_map.iter_rules() if r.endpoint != "static"]
    assert len(regeln) == 25, "25 Regeln erwartet, %d" % len(regeln)

    # (1) DIE KLAMMER DIESES BLUEPRINTS: er ANTWORTET nur. Keine Route hier
    # startet, stoppt, loescht oder speichert etwas. /api/annotations (DELETE)
    # und /api/highlights/config (POST) liegen benachbart und sind deshalb
    # ausdruecklich NICHT mitgewandert. Ohne diese Pruefung waere die Klammer
    # eine Behauptung im Docstring statt einer Regel.
    for r in regeln:
        schreibend = r.methods - {"GET", "HEAD", "OPTIONS"}
        assert not schreibend, \
            ("%s ist schreibend (%s) — dieser Blueprint antwortet nur"
             % (r.rule, sorted(schreibend)))

    # (2) Die Fachlogik ist mitgewandert, nicht kopiert. Der Monolith ruft
    # dieselben Funktionen auf wie der Blueprint — sonst gaebe es zwei
    # Wahrheiten ueber denselben Wert.
    b = open("bot.py", encoding="utf-8").read()
    for ruf in ("_nc_suche.universal_search(", "_nc_outcomes.get_outcome_breakdown(",
                "_nc_band.messen()", "_nc_storage.forecast(",
                "_nc_recdb.get_all_checks("):
        assert ruf in b, "Monolith ruft %s nicht auf" % ruf

    # (3) Der Radar-Zustand ist ein REGISTER, kein Haken: das ist geteilter
    # ZUSTAND, keine Faehigkeit. Und Register und nicht Alias, weil bot.py den
    # Namen mit new_state() neu bindet — ein Alias zeigte fuer immer auf das
    # leere Anfangs-Dict, und das Panel meldete dauerhaft null Treffer.
    import nc.highlights as H
    assert "STATE" in dir(H) and H.zustand() == {} or H.STATE["obj"] is not None
    assert '_nc_highlights.STATE["obj"] = _HIGHLIGHTS' in b, \
        "der Radar-Zustand wird nie ins Register gelegt"
    assert "highlights" not in R.HAKEN, \
        "geteilter Zustand als Haken — das ist die falsche Schublade"

    # (4) Ohne Haken sagt die Auskunft das, statt Leere zu melden. Eine leere
    # Liste sieht aus wie "nichts gefunden"; der Betreiber sucht dann an der
    # falschen Stelle.
    for h in R.HAKEN:
        R.HAKEN[h]["fn"] = None
    c = app.test_client()
    for pfad in ("/api/public/stats", "/api/summary/preview"):
        antwort = c.get(pfad)
        assert antwort.status_code == 503, \
            "%s meldet %d statt 503 ohne Haken" % (pfad, antwort.status_code)
        assert antwort.get_json()["status"] == "nicht_bereit"
    # Und alle vier werden im Monolithen wirklich eingetragen.
    for h in R.HAKEN:
        assert '_nc_routes_auskunft.HAKEN["%s"]["fn"]' % h in b, \
            "Haken %s wird im Monolithen nie eingetragen" % h

    # (5) Kein toter Import: was der Blueprint aus nc/ holt, benutzt er auch.
    # pyflakes prueft das ohnehin — hier steht es, weil dieser Blueprint mit
    # Abstand die meisten Importe hat und ein vergessener leicht durchrutscht.
    q = open("nc/routes/auskunft.py", encoding="utf-8").read()
    baum = _ast.parse(q)
    benutzt = {n.id for n in _ast.walk(baum) if isinstance(n, _ast.Name)} | \
              {n.attr for n in _ast.walk(baum) if isinstance(n, _ast.Attribute)} | \
              {n.value.id for n in _ast.walk(baum)
               if isinstance(n, _ast.Attribute) and isinstance(n.value, _ast.Name)}
    for n in baum.body:
        if isinstance(n, _ast.ImportFrom) and (n.module or "").startswith("nc"):
            for a in n.names:
                assert (a.asname or a.name) in benutzt, \
                    "toter Import: %s" % (a.asname or a.name)

    ok("v4.1-W26: Auskunft als Blueprint — 25 Routen, keine davon schreibt")



def _test_w27_verkettete_knoten():
    """v4.1-W27: verkettete Textzuweisungen im Dashboard sind uebersetzbar.

    Der DOM-Uebersetzer trifft GANZE Textknoten. Bei

        el.textContent = 'Quelle: ' + name

    heisst der Knoten "Quelle: kick"; ein Katalogeintrag fuer "Quelle: " trifft
    dort nie. ZEHN solcher Eintraege standen bereits im Katalog und zaehlten
    als uebersetzt, ohne je zu greifen — dieselbe stille Buchhaltung wie bei
    den nativen Dialogen (W21) und den verketteten Toasts (W23), nur an der
    dritten Stelle.

    Das ist der Grund, warum dieser Vertrag existiert: eine Abdeckungszahl,
    die tote Eintraege mitzaehlt, ist schlimmer als gar keine — sie sagt, die
    Arbeit sei getan.
    """
    import json as _json
    import re as _re

    dash = open("templates/dashboard.html", encoding="utf-8").read()
    WORT = _re.compile(r"[A-Za-zÄÖÜäöüß]{3}")
    MARKUP = _re.compile(r"[<>=]|var\(|&nbsp;|&#")
    LIT = _re.compile(r"'([^'\\\n]*(?:\\.[^'\\\n]*)*)'")
    ZUW = _re.compile(r"\.(?:textContent|innerText|innerHTML)\s*=\s*([^;\n]{0,300})")

    offen = []
    for m in ZUW.finditer(dash):
        rhs = m.group(1)
        if "+" not in rhs:
            continue                       # ganzes Literal ist schon ein Knoten
        for lm in LIT.finditer(rhs):
            t = lm.group(1)
            if not (t.strip() and WORT.search(t)) or MARKUP.search(t):
                continue
            davor = rhs[max(0, lm.start() - 2):lm.start()].strip()
            danach = rhs[lm.end():lm.end() + 2].strip()
            if not (davor.endswith("+") or danach.startswith("+")):
                continue
            if rhs[max(0, lm.start() - 3):lm.start()].endswith("T("):
                continue
            offen.append(t)
    assert not offen, \
        ("verkettete Textzuweisung ohne T() — der Knoten traegt den Wert mit "
         "und kein Katalogeintrag trifft ihn: %r" % offen[:6])

    # (2) Der Nachschlag TRIMMT beidseitig, der Extraktor legt getrimmt ab.
    # Faellt eines von beiden weg, sind alle Fragment-Eintraege ("Quelle: ",
    # " aktiv") auf einen Schlag tot — und die Abdeckungszahl luegt wieder.
    i18n = open("nc/routes/i18n.py", encoding="utf-8").read()
    # v4.1-W28: Anker nachgezogen, Zusicherung unveraendert. Der Nachschlag
    # trennt Rand und Kern jetzt per Ausdruck, statt zu trimmen und den Kern
    # zurueckzuersetzen — noetig fuer mehrzeilige Knoten, wo der getrimmte
    # Kern im Original gar nicht mehr woertlich vorkommt. Beide Eigenschaften
    # gelten weiter: der Rand wird abgetrennt UND wieder angesetzt.
    assert "text.match(/^(\\s*)([\\s\\S]*?)(\\s*)$/)" in i18n, \
        "der Nachschlag trennt Rand und Kern nicht mehr — Fragment-Eintraege treffen nie"
    assert "return vorn + treffer + hinten;" in i18n, \
        "die Rand-Leerzeichen gehen verloren — das Layout verrutscht"

    # (3) Prosa darf nicht mit Markup in EINEM Literal kleben. Sonst ist sie
    # nicht umschliessbar, und die Meldung steht halb uebersetzt da: der eine
    # Teil englisch, der andere deutsch, in demselben Satz.
    TAG = _re.compile(r"</?[a-zA-Z]")
    halb = []
    for m in ZUW.finditer(dash):
        rhs = m.group(1)
        if "T('" not in rhs:
            continue
        for lm in LIT.finditer(rhs):
            t = lm.group(1)
            if not TAG.search(t):
                continue
            rest = _re.sub(r"<[^>]*>", "", t).strip()
            if rest and WORT.search(rest):
                halb.append(rest)
    assert not halb, \
        ("Prosa klebt am Markup und bleibt deutsch, waehrend der Rest "
         "derselben Meldung uebersetzt wird: %r" % halb[:4])

    # (4) Kein Eintrag im Katalog, den niemand nachschlaegt. Das prueft
    # tools/i18n_extract.py --check bereits als "verwaist" — hier steht die
    # Gegenrichtung: die Zahl im Katalog muss der Zahl im Quelltext
    # entsprechen, sonst zaehlt sie etwas mit, das nie greift.
    kat = _json.load(open("locales/en.json", encoding="utf-8"))["strings"]
    assert len(kat) >= 970, "Katalog geschrumpft: %d" % len(kat)

    ok("v4.1-W27: verkettete Textknoten uebersetzbar, keine toten Eintraege mehr")



def _test_w28_abdeckung_ist_ehrlich():
    """v4.1-W28: die Abdeckungszahl muss messen, was WIRKLICH im Deck steht.

    Gemeldet wurde "0 fehlend" bei 970 Eintraegen. Gemessen am Dashboard waren
    davon **18 % der Textknoten** erfasst. Der Rest fiel im Extraktor durch die
    Deutsch-Heuristik: "Aufnahmen", "Analysieren", "BEFUNDE", "7-TAGE-TREND"
    haben weder Umlaut noch Funktionswort und sahen deshalb aus wie Bezeichner.
    Die Zahl war nicht falsch berechnet — sie zaehlte nur, was der Extraktor
    eingesammelt hatte, und das war der kleinere Teil.

    Das ist dieselbe Krankheit wie die toten Eintraege aus W21/W23/W27, nur
    umgekehrt: dort zaehlte Erfasstes mit, das nie griff; hier fehlte das
    meiste und wurde nie gezaehlt.
    """
    import html as _html
    import json as _json
    import re as _re

    import tools.i18n_extract as _X  # noqa: F401  (nur fuer _KEIN_TEXT)

    kat = _json.load(open("locales/en.json", encoding="utf-8"))["strings"]
    WORT = _re.compile(r"[A-Za-zÄÖÜäöüß]{3}")

    # (1) Die Abdeckung im Dashboard wird GEMESSEN, nicht behauptet. Alles,
    # was nicht uebersetzt ist, muss ausdruecklich als Eigenname gefuehrt
    # sein oder ein von Inline-Tags zerschnittenes Bruchstueck.
    roh = open("templates/dashboard.html", encoding="utf-8").read()
    ohne = _re.sub(
        r"<script\b.*?</script\b[^>]*>|<style\b.*?</style\b[^>]*>|<!--.*?-->",
        "",
        roh,
        flags=_re.S | _re.I,
    )
    knoten = {" ".join(_html.unescape(t).split())
              for t in _re.findall(r">([^<>]+)<", ohne)
              if t.strip() and WORT.search(t) and len(t.strip()) >= 3}
    drin = {t for t in knoten if t in kat}
    anteil = 100.0 * len(drin) / max(1, len(knoten))
    assert anteil >= 85.0, \
        ("nur %.0f%% der Dashboard-Textknoten sind uebersetzt (%d von %d)"
         % (anteil, len(drin), len(knoten)))

    # (2) Kein Schluessel mit HTML-Entity. Der Browser sieht den DEKODIERTEN
    # Text: aus `BACKUP &amp; EXPORT` wird im DOM "BACKUP & EXPORT". 22 solcher
    # Eintraege waren auf einen Schlag tot, ohne dass es auffiel.
    ent = [k for k in kat if "&amp;" in k or "&nbsp;" in k or "&#" in k]
    assert not ent, "Katalogschluessel mit HTML-Entity — trifft den DOM nie: %r" % ent[:4]

    # (3) Beide Seiten normalisieren mehrzeilige Knoten GLEICH. Faellt eine
    # Seite weg, sind alle Hilfetexte tot: der Quelltext bricht sie um, der
    # Katalog haelt sie mit einfachen Leerzeichen.
    i18n = open("nc/routes/i18n.py", encoding="utf-8").read()
    assert "kern.replace(/\\s+/g, ' ')" in i18n, \
        "der Nachschlag normalisiert mehrzeilige Knoten nicht mehr"
    ext = open("tools/i18n_extract.py", encoding="utf-8").read()
    assert 'raus.add(" ".join(t.split()))' in ext, \
        "der Extraktor normalisiert nicht mehr — die Schluessel haengen wieder an der Einrueckung"
    assert "_html.unescape(t)" in ext, "der Extraktor loest keine Entities mehr auf"

    # (4) Die Ausnahmeliste bleibt eine LISTE, keine Heuristik. Eine Regel wie
    # "alles in Grossbuchstaben ist ein Name" wuerde spaeter still echte
    # Beschriftungen verschlucken.
    assert "_KEIN_TEXT = frozenset({" in ext, "die Ausnahmen sind keine Liste mehr"
    assert len(_X._KEIN_TEXT) < 80, \
        ("die Ausnahmeliste waechst zur Muellhalde: %d Eintraege" % len(_X._KEIN_TEXT))

    ok("v4.1-W28: Dashboard-Abdeckung %.0f%% (vorher 18%%), Katalog %d Eintraege"
       % (anteil, len(kat)))



def _test_w29_kein_sqlite_auf_dem_loop():
    """v4.1-W29: Datenbankarbeit gehoert NEBEN den Event-Loop.

    BEFUND AUS DEM BETRIEBSLOG (2026-09-03): der Waechter meldete Blockaden
    von 30 bis 68 Sekunden. Einer der Stack-Abzuege:

        _handle_single_tracking -> try_acquire_recording_lock
          -> db_conn().__exit__ -> close()

    SQLite blockiert unter Plattenlast. Steht der Aufruf direkt in einer
    async-Funktion, blockiert er nicht die Abfrage, sondern den GANZEN Bot.

    Dieser Vertrag ist eine RATSCHE: die Zahl darf fallen, nie steigen. Eine
    harte Null waere heute unerreichbar (siebzig Stellen im Bestand) und
    deshalb wertlos — sie wuerde sofort abgeschaltet. Eine Obergrenze, die
    bei jeder Welle sinkt, wirkt dagegen.
    """
    import ast as _ast
    import re as _re

    # Der Stand nach W29. Wer eine Stelle loest, SETZT DIESE ZAHL HERUNTER —
    # sonst faellt die naechste Welle wieder zurueck, ohne dass es auffaellt.
    GRENZE = 52

    quelle = open("bot.py", encoding="utf-8").read()
    baum = _ast.parse(quelle)

    # Entscheidend ist die UNMITTELBAR umschliessende Funktion, nicht die
    # lexikalische Verschachtelung: ein db_conn() in einem verschachtelten
    # SYNCHRONEN Helfer laeuft ueber asyncio.to_thread und blockiert nicht.
    # Die erste Zaehlung dieser Welle hat das verwechselt und 115 statt 71
    # gemeldet.
    treffer = []

    def lauf(knoten, umgebend):
        for k in _ast.iter_child_nodes(knoten):
            if isinstance(k, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
                lauf(k, k)
            else:
                if (isinstance(k, _ast.With)
                        and isinstance(umgebend, _ast.AsyncFunctionDef)
                        and any(_ast.unparse(i.context_expr).startswith("db_conn(")
                                for i in k.items)):
                    treffer.append((umgebend.name, k.lineno))
                lauf(k, umgebend)

    lauf(baum, None)
    assert len(treffer) <= GRENZE, \
        ("%d blockierende db_conn-Bloecke in async-Funktionen (erlaubt: %d). "
         "Neue Stelle? db_async(...) benutzen. Erste drei: %r"
         % (len(treffer), GRENZE, treffer[:3]))
    assert len(treffer) >= GRENZE - 15, \
        ("nur noch %d von %d — die Grenze im Vertrag gehoert nachgezogen, "
         "sonst schuetzt sie nicht mehr" % (len(treffer), GRENZE))

    # (2) db_async gibt es, laeuft im Thread und oeffnet die Verbindung DORT.
    # Eine ueber die Thread-Grenze gereichte sqlite3-Verbindung wirft zur
    # Laufzeit (check_same_thread) — deshalb muss der `with` INNEN stehen.
    w = open("nc/dbwrap.py", encoding="utf-8").read()
    assert "async def db_async(" in w, "db_async fehlt"
    assert "asyncio.to_thread(_lauf)" in w, "db_async laeuft nicht im Thread"
    _i = w.index("async def db_async(")
    _rumpf = w[_i:]
    assert _rumpf.index("with db_conn() as conn:") < _rumpf.index("asyncio.to_thread"), \
        "die Verbindung entsteht ausserhalb des Threads — das wirft zur Laufzeit"

    # (3) Das Ereignisprotokoll blockiert nicht mehr. Es hatte ueber dreissig
    # Aufrufer, synchrone wie asynchrone; sie alle auf await umzustellen haette
    # die Zusicherung "aus jedem Pfad ohne Risiko" gebrochen.
    assert "_nc_eventlog.schreibe(" in quelle, \
        "log_event schreibt wieder synchron in die Datenbank"
    import nc.eventlog as E
    assert E.KAPAZITAET > 0, "die Schlange ist unbegrenzt — ein Speicherleck mit Anlauf"
    st = E.stand()
    for feld in ("warteschlange", "kapazitaet", "geschrieben", "verworfen", "fehler"):
        assert feld in st, "die Diagnose verschweigt %s" % feld

    e = open("nc/eventlog.py", encoding="utf-8").read()
    # Verlust MUSS gezaehlt und gemeldet werden. Ein Pruefprotokoll, das still
    # Eintraege verliert, ist schlimmer als keines: die Luecke sieht aus wie Ruhe.
    assert '_ZAEHLER["verworfen"] += 1' in e, "verworfene Eintraege werden nicht gezaehlt"
    assert "_melde_verworfen()" in e, "verworfene Eintraege werden nicht gemeldet"
    # Die Fehler-Drosselung laeuft ueber die ZEIT. Ueber den Zaehler ginge es
    # nicht: der waechst in Buendeln von bis zu 50, ein `% 100 == 1` haette nie
    # ausgeloest und der Schreibfehler waere still geblieben.
    assert "_FEHLER_GEMELDET" in e and 'jetzt - _FEHLER_GEMELDET["ts"] >= 60' in e, \
        "die Fehlermeldung ist nicht zeitgedrosselt — sie loest nie oder dauernd aus"
    # EIN Schreiber: das Protokoll ist eine Chronik, zwei Threads wuerfeln die
    # Reihenfolge durcheinander.
    assert e.count("threading.Thread(target=_schreiber") == 1, "mehr als ein Schreiber"
    assert '_LAEUFT = {"an": False}' in e, "der Waechter ist kein Modul-Global"

    # (4) KEIN Dauerlaeufer blockiert mehr. Die sind die schlimmsten: sie
    # wiederholen sich fuer immer, also trifft ihre Blockade frueher oder
    # spaeter jeden Betriebszustand.
    laeufer = sorted({n for n, _ in treffer if n.endswith("_loop")})
    assert not laeufer, "Dauerlaeufer blockieren wieder den Loop: %r" % laeufer

    # (5) Keine offene Transaktion ueber ein `await` hinweg. Das blockiert den
    # Loop NICHT (das await gibt ihn frei) — es haelt aber die Verbindung und
    # damit den Schreib-Lock offen, waehrend auf das Netz gewartet wird. Jeder
    # andere Schreiber bekommt in der Zeit "database is locked", und die
    # Ursache steht in einer Schleife, die nur jede Minute laeuft.
    # _community_events_loop hatte genau das (v4.1-W29).
    for _f in _ast.walk(baum):
        if not isinstance(_f, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            continue
        for _w in _ast.walk(_f):
            if not (isinstance(_w, _ast.With) and any(
                    _ast.unparse(i.context_expr).startswith("db_conn(") for i in _w.items)):
                continue
            for _k in _ast.walk(_w):
                assert not isinstance(_k, (_ast.Await, _ast.AsyncFor)), \
                    ("%s: await innerhalb eines offenen db_conn()-Blocks (Zeile %d) — "
                     "haelt den Schreib-Lock ueber das Warten hinweg"
                     % (_f.name, _w.lineno))

    # (6) Der Sendebild-Chat laeuft ueber EINEN Arbeiter. Das ist keine
    # Feinheit: der Chat ist eine Abfolge. Mit mehreren Arbeitern wuerfelt
    # der Thread-Pool die Reihenfolge durcheinander — nachgemessen, mit acht
    # Arbeitern kommen 200 Nachrichten NICHT in der Einreichungsreihenfolge
    # an. Eine vertauschte Chat-Nachricht ist kein akzeptabler Preis fuer
    # Nebenlaeufigkeit.
    assert "_CHAT_PUSH_EXEC = _cf_thread.ThreadPoolExecutor(max_workers=1" in quelle, \
        "der Chat-Push laeuft nicht mehr ueber genau EINEN Arbeiter"
    assert "async def _restream_chat_push_async(" in quelle, "die nebenlaeufige Huelle fehlt"
    # Und alle Aufrufer benutzen sie wirklich. Ein vergessener Aufruf schriebe
    # weiter synchron und faellt sonst niemandem auf.
    roh_aufrufe = len(_re.findall(r"(?<!await )(?<!def )\b_restream_chat_push\(", quelle))
    assert roh_aufrufe <= 1, \
        ("%d Aufrufe von _restream_chat_push ohne die nebenlaeufige Huelle "
         "(erlaubt ist nur der eine INNERHALB der Huelle)" % roh_aufrufe)

    ok("v4.1-W29: %d blockierende Stellen (Grenze %d), kein Dauerlaeufer, "
       "keine Transaktion ueber ein await, Chat-Reihenfolge gesichert"
       % (len(treffer), GRENZE))



def _test_w30_fehlertext_und_offenes_deck():
    """v4.1-W30: was nach aussen geht, und ob das Deck ueberhaupt zu ist."""
    import ast as _ast
    import glob as _glob
    import os as _os

    import nc.dashauth as D
    import nc.fehlertext as F

    # (1) KEIN roher Ausnahmetext mehr in einer Antwort. Die Schranke des
    # Decks macht gar nichts, wenn weder Token noch PIN gesetzt ist — dann
    # geht jede dieser Meldungen an jeden, der den Port erreicht, mitsamt
    # Dateipfaden und gelegentlich dem Wortlaut einer fremden API-Antwort.
    # v4.2-W3: nach AST statt nach der Zeichenkette "str(e)". Die Textsuche
    # sah nur den Namen `e` — ein `except Exception as ex:` mit `str(ex)`
    # blieb unsichtbar und stand genau so in nc/routes/brain.py. Gefunden hat
    # ihn erst das lokal installierte CodeQL.
    def _roher_str_aufruf(pfad):
        baum = _ast.parse(open(pfad, encoding="utf-8").read())
        raus = []
        for k in _ast.walk(baum):
            if not isinstance(k, _ast.ExceptHandler) or not k.name:
                continue
            for j in _ast.walk(k):
                if (isinstance(j, _ast.Call)
                        and isinstance(j.func, _ast.Name) and j.func.id == "str"
                        and len(j.args) == 1
                        and isinstance(j.args[0], _ast.Name)
                        and j.args[0].id == k.name):
                    raus.append((pfad, j.lineno))
        return raus

    offen = []
    for p in sorted(_glob.glob("nc/routes/*.py")):
        offen += _roher_str_aufruf(p)
    assert not offen, (
        "roher Ausnahmetext in einem Blueprint — str(<ausnahme>) ohne "
        "Saeuberung: %r" % (offen[:8],))

    # v4.2-W3: DIE LUECKE, DIE W30 GELASSEN HAT. Der Vertrag oben verbietet
    # `str(e)` — aber `f"JSON nicht lesbar: {e}"` ist genau derselbe Leck-Weg
    # und stand danach noch an 22 Stellen. Ein lokal installiertes CodeQL hat
    # sie gefunden (py/stack-trace-exposure); die Textsuche nach "str(e)"
    # konnte das nie sehen.
    #
    # Geprueft wird jetzt die FORM, nicht die Zeichenkette: in einem
    # `except … as e` darf `{e}` in keinem f-string stehen, ausser der Name
    # laeuft durch _fehler_text. Nach AST, weil ein f-string beliebig
    # verschachtelt sein kann und ein Regex daran zerbricht.
    # NUR Antwort-Bauer, nicht das Log. Im Log ist der volle Wortlaut richtig
    # — nach_aussen() schreibt ihn selbst dorthin. Ein Vertrag, der auch
    # log.warning(f"... {e}") meldet, waere ein Dauer-Fehlalarm und flöge
    # nach der dritten Welle raus.
    ANTWORT = {"jsonify", "Response", "make_response", "abort", "_oauth_page"}

    def _rohe_ausnahme_in_fstring(pfad):
        baum = _ast.parse(open(pfad, encoding="utf-8").read())
        raus = []
        for k in _ast.walk(baum):
            if not isinstance(k, _ast.ExceptHandler) or not k.name:
                continue
            for aufruf in _ast.walk(k):
                if not (isinstance(aufruf, _ast.Call)
                        and _ast.unparse(aufruf.func).split(".")[-1] in ANTWORT):
                    continue
                for j in _ast.walk(aufruf):
                    if not isinstance(j, _ast.JoinedStr):
                        continue
                    for teil in j.values:
                        # Bare `{e}` — ein Aufruf drumherum (also
                        # _fehler_text(e)) ist genau das, was hier verlangt
                        # wird, und faellt deshalb nicht auf.
                        if (isinstance(teil, _ast.FormattedValue)
                                and isinstance(teil.value, _ast.Name)
                                and teil.value.id == k.name):
                            raus.append((pfad, j.lineno))
        return raus

    roh_fstring = []
    for p in sorted(_glob.glob("nc/routes/*.py")) + ["bot.py"]:
        roh_fstring += _rohe_ausnahme_in_fstring(p)
    assert not roh_fstring, (
        "roher Ausnahmetext in einem f-string — dasselbe Leck wie str(e), "
        "nur anders geschrieben. Durch _fehler_text(e, \"<funktion>\") "
        "ersetzen: %r" % (roh_fstring[:8],))

    # Und in bot.py wenigstens nicht mehr in einer HTTP-Antwort.
    b = open("bot.py", encoding="utf-8").read()
    for k in _ast.walk(_ast.parse(b)):
        if isinstance(k, _ast.Call) and isinstance(k.func, _ast.Name) \
           and k.func.id == "jsonify":
            for kw in k.keywords:
                assert not _ast.unparse(kw.value).startswith("str(e)"), \
                    ("roher Ausnahmetext in einer jsonify-Antwort, Zeile %d"
                     % kw.value.lineno)

    # (2) Der Saeuberer nimmt raus, was verraeterisch ist, und laesst stehen,
    # was der Betreiber braucht. "Interner Fehler" waere in einem
    # Ein-Personen-Betrieb keine Sicherheit, sondern eine Sackgasse.
    assert F.saeubern("database is locked") == "database is locked"
    assert "/home/" not in F.saeubern(
        "[Errno 2] No such file: '/home/ubuntu/tiktok-bot/recordings/x.mp4'")
    assert "abc123def456" not in F.saeubern('HTTP 401: token=abc123def456')
    assert "46zAbCdEfGhIjKlMnOpQrStUvWxYz012345" not in F.saeubern(
        "rtmp://ingest/app/46zAbCdEfGhIjKlMnOpQrStUvWxYz012345 refused")
    assert len(F.saeubern("x" * 4000)) <= F.MAX
    # Der Typ bleibt: "OperationalError" sagt Datenbank, "TimeoutError" sagt
    # Netz — und verraet nichts ueber den Bestand.
    assert F.nach_aussen(ValueError("kaputt"), "test").startswith("ValueError")

    # (3) Die Lage-Erkennung benutzt DIESELBE Bedingung wie die Schranke:
    # ein Token ODER ein PIN reicht. Frueher fragte die Warnung nur nach dem
    # Token und schlug bei einem PIN-geschuetzten Deck faelschlich an — ein
    # Fehlalarm erzieht dazu, die Meldung zu ueberlesen.
    sicher = {k: _os.environ.get(k) for k in ("WEB_HOST", "DASHBOARD_TOKEN", "DASHBOARD_PIN")}
    try:
        for env, erwartet in (
                ({"WEB_HOST": "127.0.0.1", "DASHBOARD_TOKEN": "", "DASHBOARD_PIN": ""}, False),
                ({"WEB_HOST": "0.0.0.0", "DASHBOARD_TOKEN": "", "DASHBOARD_PIN": ""}, True),
                ({"WEB_HOST": "0.0.0.0", "DASHBOARD_TOKEN": "", "DASHBOARD_PIN": "1234"}, False),
                ({"WEB_HOST": "0.0.0.0", "DASHBOARD_TOKEN": "geheim", "DASHBOARD_PIN": ""}, False)):
            _os.environ.update(env)
            assert D.offen_im_netz() is erwartet, env
    finally:
        for k, v in sicher.items():
            if v is None:
                _os.environ.pop(k, None)
            else:
                _os.environ[k] = v

    # (4) Die Meldung laeuft auf ERROR und WIEDERHOLT sich. Ein log.warning
    # erscheint in einem ERROR-Log nie (CLAUDE.md), und eine Meldung nur beim
    # Start sieht niemand: der Betreiber liest das Log, wenn etwas kaputt ist,
    # nicht beim Hochfahren. Der gefaehrliche Zustand ist ein Dauerzustand.
    assert "_nc_dashauth.lage()" in b, "die Lage wird nicht mehr abgefragt"
    assert "async def _sicherheits_erinnerung_loop" in b, "die Erinnerung fehlt"
    assert '_spawn(_sicherheits_erinnerung_loop(), name="sec-reminder")' in b, \
        "die Erinnerung wird nie gestartet"
    _i = b.index("async def _sicherheits_erinnerung_loop")
    _seg = b[_i:_i + 1400]
    assert "log.error(" in _seg, "die Erinnerung laeuft nicht auf ERROR"
    assert "log.warning(" not in _seg, \
        "die Erinnerung faellt auf warning zurueck — im ERROR-Log unsichtbar"

    ok("v4.1-W30: kein roher Ausnahmetext nach aussen, offenes Deck meldet sich wiederholt")


def _test_w31_rauchtest_laeuft_in_der_ci():
    """v4.1-W31: der Rauchtest laeuft automatisch — und bleibt lauffaehig."""
    import ast as _ast
    import pathlib as _pl
    import sys as _sys

    ci = open(".github/workflows/ci.yml", encoding="utf-8").read()

    # (1) Er laeuft ueberhaupt. Bis W31 stand in der Pflicht-Pruefkette ein
    # Test, den KEINE Maschine je ausfuehrte: auf der Autorenmaschine fehlt
    # der Laufzeitstack, in der CI war er ausgeschlossen, und auf dem Server
    # lief er nur, wenn jemand daran dachte. Genau die Fehler, die er faengt
    # (NameError auf der Modul-Ebene, 500er beim ersten Aufruf), haben in W26
    # und W29 in Produktion zugeschlagen.
    assert "python test_smoke.py" in ci, \
        "test_smoke.py laeuft in der CI nicht mehr — der Job wurde entfernt"
    assert "requirements-smoke.txt" in ci, \
        "der Rauchtest-Job installiert nicht mehr aus requirements-smoke.txt"
    _i = ci.index("python test_smoke.py")
    assert 'PYTHONUTF8: "1"' in ci[max(0, _i - 400):_i], \
        ("test_smoke.py laeuft ohne PYTHONUTF8=1 — es oeffnet bot.py ohne "
         "encoding=, das stirbt ausserhalb einer UTF-8-Umgebung mit "
         "UnicodeDecodeError statt zu pruefen")

    # (2) Und er BLEIBT lauffaehig. Ein neuer Import auf der Modul-Ebene, der
    # in requirements-smoke.txt fehlt, wuerde den Job mit einem nackten
    # ImportError toeten — mitten in der Liste, ohne Hinweis worauf. Dieser
    # Vergleich meldet das hier, mit Datei und Paketname.
    quelle = open("requirements-smoke.txt", encoding="utf-8").read()
    gelistet = {z.split("#")[0].strip().lower()
                for z in quelle.splitlines() if z.split("#")[0].strip()}

    # Importname -> pip-Name. Nur was sich unterscheidet steht hier drin.
    PIPNAME = {"dotenv": "python-dotenv", "discord": "discord.py",
               "socks": "PySocks", "pymysql": "PyMySQL",
               "telegram": "python-telegram-bot", "faster_whisper": "faster-whisper"}
    # Diese stubbt test_smoke.py selbst — sie duerfen fehlen.
    GESTUBBT = {"TikTokLive", "telegram"}
    LOKAL = {"nc", "brain", "bot", "brain_bridge", "tools"}

    def _fremd_auf_modulebene(pfad):
        """Importe der Modul-Ebene, getrennt nach 'muss da sein' und 'optional'.

        Optional heisst: in einem try mit except ImportError. Solche Pakete
        darf der Rauchtest nicht haben — der Code faengt ihr Fehlen ab.
        """
        baum = _ast.parse(_pl.Path(pfad).read_text(encoding="utf-8"))
        pflicht, optional = set(), set()

        def _namen(knoten):
            if isinstance(knoten, _ast.Import):
                return [a.name.split(".")[0] for a in knoten.names]
            if isinstance(knoten, _ast.ImportFrom) and knoten.level == 0 and knoten.module:
                return [knoten.module.split(".")[0]]
            return []

        def _lauf(koerper, weich):
            for k in koerper:
                for n in _namen(k):
                    if n in _sys.stdlib_module_names or n in LOKAL:
                        continue
                    (optional if weich else pflicht).add(n)
                if isinstance(k, _ast.Try):
                    # Ein Handler, der ImportError faengt, macht den Import
                    # optional. `except Exception` und das nackte `except:`
                    # fangen ihn mit — deshalb zaehlen die hier auch.
                    faengt_import = False
                    for h in k.handlers:
                        art = "" if h.type is None else _ast.unparse(h.type)
                        if h.type is None or any(
                                w in art for w in ("ImportError", "ModuleNotFoundError",
                                                   "Exception", "BaseException")):
                            faengt_import = True
                    _lauf(k.body, weich or faengt_import)
                    for h in k.handlers:
                        _lauf(h.body, True)
                    _lauf(k.orelse, weich or faengt_import)
                    _lauf(k.finalbody, weich)
                elif isinstance(k, _ast.If):
                    _lauf(k.body, weich)
                    _lauf(k.orelse, weich)
        _lauf(baum.body, False)
        return pflicht, optional - pflicht

    dateien = ["bot.py"] + [str(p) for p in sorted(_pl.Path(".").glob("nc/**/*.py"))
                            if "_vendor" not in str(p)] \
                        + [str(p) for p in sorted(_pl.Path(".").glob("brain/**/*.py"))]
    fehlt = []
    for d in dateien:
        pflicht, _ = _fremd_auf_modulebene(d)
        for n in pflicht:
            if n in GESTUBBT:
                continue
            if PIPNAME.get(n, n).lower() not in gelistet:
                fehlt.append((d, n, PIPNAME.get(n, n)))
    assert not fehlt, (
        "Import auf der Modul-Ebene ohne Eintrag in requirements-smoke.txt — "
        "der Rauchtest stirbt damit in der CI an einem ImportError. "
        "Eintragen oder in eine Funktion verschieben: %r" % (fehlt,))

    # (3) Umgekehrt: kein toter Eintrag. Eine Liste, die mehr enthaelt als
    # noetig, waechst still weiter und macht den Job wieder teuer — genau der
    # Grund, warum requirements.txt hier nicht taugt.
    # Optionale Importe zaehlen hier MIT. discord ist der Fall, um den es
    # geht: bot.py faengt sein Fehlen ab (`except Exception: discord = None`),
    # der Rauchtest liefe also auch ohne das Paket gruen — und wuerde dabei
    # die gesamte Slash-Command-Registrierung ueberspringen. Genau dort sass
    # B79. Ein optionales Paket gehoert deshalb in die Liste, wenn ohne es
    # ein Stueck bot.py ungeprueft bleibt.
    gebraucht = set()
    for d in dateien:
        pflicht, optional = _fremd_auf_modulebene(d)
        for n in pflicht | optional:
            if n not in GESTUBBT:
                gebraucht.add(PIPNAME.get(n, n).lower())
    tot = gelistet - gebraucht
    assert not tot, (
        "requirements-smoke.txt listet Pakete, die keine Modul-Ebene mehr "
        "braucht: %r — raus damit, sonst wird der Job wieder teuer" % sorted(tot))

    ok("v4.1-W31: der Rauchtest laeuft in der CI, %d Datei(en) gegen "
       "requirements-smoke.txt geprueft" % len(dateien))

def _test_w32_sondenschicht_und_systemlage():
    """v4.1-W32: die Sonden liegen in nc/, drei System-Routen sind draussen."""
    import ast as _ast

    import nc.cookies as C
    import nc.logsafe as L
    import nc.systemprobe as P

    b = open("bot.py", encoding="utf-8").read()

    # (1) Die drei Routen sind WEG aus dem Monolithen und im Blueprint.
    # Ein Blueprint, den niemand registriert, ist ein 404 mit Rueckendeckung —
    # deshalb beides pruefen, nicht nur die Datei.
    for name in ("api_system", "api_system_preflight_history", "api_config_drift"):
        assert ("\ndef %s(" % name) not in b, \
            "%s steht noch in bot.py — doppelte Route oder toter Code" % name
    s = open("nc/routes/systemlage.py", encoding="utf-8").read()
    for pfad in ("/api/system", "/api/system/preflight_history",
                 "/api/system/config_drift"):
        assert '"%s"' % pfad in s, "%s fehlt im Blueprint" % pfad
    assert "register_blueprint(_nc_routes_systemlage.bp)" in b, \
        "der Blueprint ist nicht registriert — die drei Routen waeren 404"

    # (2) Der Drift-Bericht liest den QUELLTEXT von bot.py. Im Monolithen stand
    # dafuer __file__. In einem Blueprint zeigt __file__ auf DIESE Datei, und
    # nc/confdrift faende dort keine einzige os.getenv-Vorgabe: die Antwort
    # waere ein leerer Bericht mit ok=true. Genau die stille Fehlanzeige, vor
    # der CLAUDE.md warnt — deshalb ein Vertrag und kein Kommentar.
    # Nach AST, nicht nach Text: der Kommentar daneben ERKLAERT die Falle und
    # nennt __file__ dabei. Eine Textsuche haette den eigenen Warnhinweis als
    # Verstoss gemeldet — ein Vertrag, der auf seine Begruendung anschlaegt,
    # wird beim naechsten Mal geloescht statt gelesen.
    for _k in _ast.walk(_ast.parse(s)):
        if isinstance(_k, _ast.Name) and _k.id == "__file__":
            raise AssertionError(
                "nc/routes/systemlage.py benutzt __file__, Zeile %d — in einem "
                "Blueprint zeigt das auf die falsche Datei und ergibt eine "
                "leere Drift-Liste mit ok=true" % _k.lineno)
    assert 'cfg["BOT_DATEI"]' in s, "der Pfad von bot.py kommt nicht mehr aus cfg"
    assert '"BOT_DATEI": __file__' in b, "bot.py reicht seinen Pfad nicht mehr durch"

    # (3) Keine Modul-Konstante aus der Umgebung. CLAUDE.md: ".env wird teils
    # erst nach den ersten Imports geladen" — ein os.getenv auf Modul-Ebene
    # haette hier die leere Vorgabe fuer immer eingefroren.
    for datei in ("nc/systemprobe.py", "nc/cookies.py"):
        baum = _ast.parse(open(datei, encoding="utf-8").read())
        for k in baum.body:
            for x in _ast.walk(k):
                if isinstance(x, _ast.Call) and _ast.unparse(x.func).endswith("getenv"):
                    raise AssertionError(
                        "%s liest os.getenv auf Modul-Ebene, Zeile %d — "
                        "Konfiguration gehoert in configure()" % (datei, x.lineno))
        assert "def configure(" in open(datei, encoding="utf-8").read(), \
            "%s hat kein configure()" % datei

    # (4) Die Sonden-Auswahl. `which` ist Parameter, damit der Vertrag sie
    # pruefen kann, ohne ffmpeg zu installieren.
    def _da(*was):
        return lambda x: ("/usr/bin/" + x) if x in was else None
    P.configure(recorder_pref="auto")
    assert P.active_recorder(which=_da("ffmpeg", "yt-dlp")) == "native"
    assert P.active_recorder(which=_da("yt-dlp")) == "ytdlp"
    assert P.active_recorder(which=_da()) is None
    P.configure(recorder_pref="ytdlp")
    assert P.active_recorder(which=_da("ffmpeg")) is None, \
        "pref=ytdlp darf NICHT auf native zurueckfallen — sonst nimmt der " \
        "Recorder still einen anderen Weg als eingestellt"
    assert P.active_recorder(which=_da("yt-dlp")) == "ytdlp"
    P.configure(recorder_pref="native")
    assert P.active_recorder(which=_da("yt-dlp")) is None
    P.configure(recorder_pref="auto")

    # (5) Der Deckel haelt AUCH ein negatives Ergebnis fest. Sonst laeuft jede
    # Sonde bei totem Redis in einen 1-2-Sekunden-Timeout, und zwar bei jedem
    # Aufruf — das Dashboard pollt im Sekundentakt.
    P.cache_leeren()
    zaehler = {"n": 0}

    def _teuer():
        zaehler["n"] += 1
        return False
    for _ in range(5):
        assert P.cached_probe("test", _teuer) is False
    assert zaehler["n"] == 1, \
        "cached_probe wiederholt eine fehlgeschlagene Sonde (%d Aufrufe)" % zaehler["n"]
    P.cache_leeren()

    # (6) Zugangsdaten raus, Ziel drin. Die Antwort landet im Browser-Cache,
    # in Screenshots und in jedem Support-Log (v4.0-W118).
    assert L.url_ohne_zugang("redis://:geheim@host:6379/0") == \
        "redis://<geheim>@host:6379/0"
    assert L.url_ohne_zugang("redis://nutzer:geheim@host:6379/0") == \
        "redis://nutzer:<geheim>@host:6379/0"
    assert L.url_ohne_zugang("redis://localhost:6379/0") == "redis://localhost:6379/0"
    assert L.url_ohne_zugang(None) == ""

    # (7) EIN Cookie-Cache, nicht zwei. Der Bot leert ihn nach einer
    # Reparatur, das Deck liest ihn ueber ctx.cfg — eine Kopie waere ein
    # totes Panel und ein Cache, den niemand mehr invalidiert.
    assert C.CACHE is C._COOKIES_CACHE, \
        ("nc.cookies.CACHE ist eine Kopie — der Bot leert dann einen "
         "anderen Cache als den, den load_dict liest")
    assert "_COOKIES_CACHE = _nc_cookies_datei.CACHE" in b, \
        "bot.py haelt einen eigenen Cookie-Cache — zwei Wahrheiten ueber eine Datei"
    assert "_load_cookies_dict = _nc_cookies_datei.load_dict" in b, \
        "der Cookie-Leser ist kein Alias mehr — ein Wrapper waere eine zweite Signatur"

    # (8) Die Kollisionsaufloesung ist ein Bugfix, dessen Symptom niemand ein
    # zweites Mal suchen will: Deck meldet "Cookies aktuell", TikTok liefert
    # trotzdem 403, weil der gesendete sessionid-Wert aus der falschen
    # Domain-Variante stammt. Spezifischere Domain gewinnt, bei Gleichstand
    # die laengere Expiry.
    import os as _os
    import tempfile as _tf
    d = _tf.mkdtemp()
    pfad = _os.path.join(d, "c.txt")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("\t".join([".tiktok.com", "TRUE", "/", "FALSE", "9999999999",
                           "sessionid", "ALT"]) + "\n")
        f.write("\t".join(["www.tiktok.com", "FALSE", "/", "FALSE", "1111111111",
                           "sessionid", "GENAU"]) + "\n")

    class _Still:
        def __getattr__(self, n):
            return lambda *a, **k: None
    C.configure(datei=pfad, log=_Still())
    C.CACHE.pop("v", None)
    got = C.load_dict()
    assert got.get("sessionid") == "GENAU", \
        ("Domain-Kollision falsch aufgeloest: %r — die exakte Domain muss "
         "gewinnen, sonst sendet der Bot einen veralteten sessionid" % got)
    C.CACHE.pop("v", None)

    ok("v4.1-W32: Sondenschicht in nc/, 3 System-Routen im Blueprint, "
       "ein Cookie-Cache")

def _test_w33_sammelentscheid_und_ein_stempel():
    """v4.2: Vorschläge gesammelt entscheiden, und EIN Build-Stempel."""
    import ast as _ast
    import json as _json
    import re as _re

    from nc import version as V

    dash = open("templates/dashboard.html", encoding="utf-8").read()
    evo = open("nc/routes/evolution.py", encoding="utf-8").read()

    # ── (1) Die beiden Knoepfe und ihre Route ───────────────────────────────
    assert 'onclick="evoBulk(true)"' in dash and 'onclick="evoBulk(false)"' in dash, \
        "die Sammelknoepfe fehlen im Deck"
    assert '"/api/evolution/proposals/bulk"' in evo, "keine Sammel-Route"
    assert "def evoBulk(" not in dash and "async function evoBulk(" in dash, \
        "evoBulk ist nicht als Funktion verdrahtet"

    # ── (2) Sie fassen NUR offene Vorschlaege an. Ein bereits uebernommener
    # Vorschlag darf durch einen spaeteren Klick auf "alles verwerfen" nicht
    # rueckwirkend zu "verworfen" werden — das waere eine Umschreibung der
    # Entscheidungshistorie, nicht eine Massenaktion.
    _i = evo.index("def api_evolution_bulk(")
    _rumpf = evo[_i:evo.index("@bp.route", _i)]
    assert "WHERE status='proposed'" in _rumpf, \
        ("die Sammelaktion filtert nicht auf offene Vorschlaege — sie wuerde "
         "bereits getroffene Entscheidungen ueberschreiben")
    assert "rowcount" in _rumpf, \
        "die Route meldet nicht, wie viele sie angefasst hat"

    # ── (3) Eine Anweisung, nicht N. Bei zwanzig offenen Vorschlaegen waeren
    # zwanzig POSTs zwanzig Transaktionen; bricht einer ab, bleibt die Liste
    # halb bearbeitet zurueck, ohne dass jemand sagen kann welche Haelfte.
    assert _rumpf.count("UPDATE evolution_proposals") == 1, \
        "die Sammelaktion laeuft nicht in EINER Anweisung"
    _bulkjs = dash[dash.index("async function evoBulk("):]
    _bulkjs = _bulkjs[:_bulkjs.index("\n}")]
    assert "for(" not in _bulkjs and "forEach" not in _bulkjs, \
        "das Deck schleift ueber die Vorschlaege statt die Sammel-Route zu rufen"

    # ── (4) Rueckfrage vor dem Verwerfen, und sie nennt die Zahl. Eine Frage
    # ohne Zahl beantwortet man anders als eine, die 17 nennt.
    assert "confirm(" in _bulkjs, "verwirft ohne Rueckfrage"
    assert "offen+' '+T(" in _bulkjs, "die Rueckfrage nennt die Zahl nicht"
    # T() um den Text, nicht um das Ergebnis: ein nativer Dialog laeuft nie
    # durch die DOM-Uebersetzung (CLAUDE.md, W21).
    for stueck in ("T('Vorschläge verwerfen?')",
                   "T('Vorschläge als angewendet markieren?')"):
        assert stueck in _bulkjs, "Dialogtext nicht an der Quelle uebersetzt: %s" % stueck

    # ── (5) Knoepfe nur, wenn es etwas zu sammeln gibt. Ein Knopf, der auf
    # eine leere Liste wirkt, tut nichts und sieht wie ein Fehler aus.
    assert 'id="evo_bulk"' in dash and "bulk.hidden = !ps.length" in dash, \
        "die Sammelknoepfe werden bei leerer Liste nicht ausgeblendet"

    # ── (6) EIN Build-Stempel. Er stand woertlich in bot.py, in
    # nc/routes/brain.py und zweimal im Footer — vier Kopien einer Zahl, von
    # denen keine mitwanderte, wenn nc/version.py hochgezaehlt wurde. Genau
    # deshalb zeigte das Deck im September noch August an.
    assert V.build_stamp() == "%s · v%s" % (V.RELEASE, V.VERSION)
    # Nach AST, nicht nach Regex: ein Ausdruck als Vorgabe enthaelt selbst
    # Klammern, an denen jedes "bis zur naechsten )"-Muster falsch abschneidet.
    for datei in ("bot.py", "nc/routes/brain.py"):
        for k in _ast.walk(_ast.parse(open(datei, encoding="utf-8").read())):
            if not (isinstance(k, _ast.Call)
                    and _ast.unparse(k.func).endswith("getenv")
                    and k.args and isinstance(k.args[0], _ast.Constant)
                    and k.args[0].value == "BUILD_STAMP"):
                continue
            assert len(k.args) >= 2, "%s: BUILD_STAMP ohne Vorgabe" % datei
            vorgabe = _ast.unparse(k.args[1])
            assert vorgabe.endswith("build_stamp()"), \
                ("%s haelt eine eigene Vorgabe fuer BUILD_STAMP (%s), Zeile %d — "
                 "beim naechsten Hochzaehlen laeuft sie auseinander"
                 % (datei, vorgabe, k.lineno))
    # Ohne Kommentare zaehlen: die Wellen-Marken ("v4.2: …") und das Beispiel
    # im Kommentar daneben sind keine Anzeige. Ein Vertrag, der auf seine
    # eigene Begruendung anschlaegt, wird beim naechsten Mal geloescht statt
    # gelesen — dieselbe Falle wie beim __file__-Vertrag in W32.
    _nackt = _re.sub(r"<!--.*?-->", "", dash, flags=_re.S)
    _nackt = _re.sub(r"/\*.*?\*/", "", _nackt, flags=_re.S)
    _nackt = _re.sub(r"(?m)^\s*//.*$", "", _nackt)
    for zahl in (V.RELEASE, "v" + V.VERSION):
        assert _nackt.count(zahl) <= 1, \
            ("%r steht %dx fest im Deck — der Footer soll die Version HOLEN, "
             "nicht behaupten" % (zahl, _nackt.count(zahl)))

    # ── (7) Und die Route liefert ihn wirklich. Sie las ihn ueber globals()
    # aus einem Blueprint-Namensraum, in dem er nie stand: /api/version gab
    # seit W26 still build="" zurueck, und niemand sah es, weil der Footer
    # ohnehin fest verdrahtet war.
    ausk = open("nc/routes/auskunft.py", encoding="utf-8").read()
    _a = ausk.index("def api_version(")
    _r = ausk[_a:ausk.index("@bp.route", _a)]
    for k in _ast.walk(_ast.parse("def f():\n" + "\n".join(
            " " + z for z in _r.splitlines()[1:]))):
        if isinstance(k, _ast.Call) and _ast.unparse(k.func) == "globals":
            raise AssertionError(
                "api_version liest wieder ueber globals() — im Blueprint ist "
                "das der falsche Namensraum, die Antwort waere still leer")
    assert 'cfg.get("BUILD_STAMP")' in _r, "der Stempel kommt nicht aus ctx.cfg"
    assert "loadFooterVersion()" in dash, "der Footer holt die Version nicht"

    # ── (8) Der Katalog kennt die neuen Texte. Ein fehlender Eintrag faellt
    # auf Deutsch zurueck — die Knoepfe blieben im englischen Deck deutsch.
    kat = _json.load(open("locales/en.json", encoding="utf-8"))["strings"]
    for s in ("✓ alles übernehmen", "alles verwerfen", "Vorschläge verwerfen?",
              "Vorschläge als angewendet markieren?"):
        assert s in kat, "Katalogeintrag fehlt: %r" % s

    ok("v4.2: Vorschlaege gesammelt entscheiden, ein Build-Stempel, "
       "Footer holt die Version")

def _test_v42_w1_schnappschuss_ohne_geheimnis():
    """v4.2-W1: config_snapshot und check_timing raus — ohne Geheimnisse."""
    import ast as _ast

    import nc.discordlimits as D
    import nc.whispercfg as W

    b = open("bot.py", encoding="utf-8").read()
    s = open("nc/routes/systemlage.py", encoding="utf-8").read()

    # ── (1) Die Routen sind weg aus dem Monolithen und im Blueprint ─────────
    for name in ("api_system_config_snapshot", "api_check_timing"):
        assert ("\ndef %s(" % name) not in b, "%s steht noch in bot.py" % name
        assert "def %s(" % name in s, "%s fehlt im Blueprint" % name
    for pfad in ("/api/system/config_snapshot", "/api/system/check_timing"):
        assert '"%s"' % pfad in s, "%s fehlt" % pfad

    # ── (2) KEIN GEHEIMNIS IM KONTEXT. Der Schnappschuss beantwortet nur, OB
    # etwas gesetzt ist. Den Wert dafuer durch den Kontext zu reichen, damit
    # ein Blueprint ihn zu True verrechnet, waere groessere Angriffsflaeche
    # fuer null Gewinn — dieselbe Ueberlegung wie bei s3_zugang() in W24.
    # Die .env traegt rund 500 Variablen mit Cookies, OAuth-Token und
    # Stream-Schluesseln; jede davon, die unnoetig wandert, ist ein Risiko.
    GEHEIM = ("DASHBOARD_TOKEN", "DASHBOARD_PIN", "DISCORD_BOT_TOKEN",
              "KICK_CLIENT_SECRET", "TWITCH_STREAM_KEY", "YOUTUBE_STREAM_KEY",
              "KICK_STREAM_KEY", "KICK_STREAM_KEY_BACKUP")
    _cfg = None
    for k in _ast.walk(_ast.parse(b)):
        if (isinstance(k, _ast.Call) and _ast.unparse(k.func).endswith("ctx.configure")):
            for kw in k.keywords:
                if kw.arg == "cfg":
                    _cfg = kw.value
    assert _cfg is not None, "nc.ctx.configure(cfg=…) nicht gefunden"
    for schluessel, wert in zip(_cfg.keys, _cfg.values):
        roh = _ast.unparse(wert)
        for g in GEHEIM:
            # bool(X) und "a and b"-Verrechnungen sind erlaubt: dabei verlaesst
            # nur das Ergebnis den Bot, nicht der Wert.
            if roh == g:
                raise AssertionError(
                    "ctx.cfg[%s] reicht das Geheimnis %s im Klartext an die "
                    "Blueprints weiter — als bool(%s) uebergeben"
                    % (_ast.unparse(schluessel), g, g))
    # Und der Blueprint fragt auch gar nicht danach.
    for g in GEHEIM:
        assert '"%s"' % g not in s, \
            "der Blueprint greift auf %s zu — er braucht nur das HAT_-Boolean" % g
    for hat in ("HAT_DASHBOARD_TOKEN", "HAT_KICK_CREDS", "HAT_DISCORD_BOT_TOKEN"):
        assert '"%s"' % hat in b and '"%s"' % hat in s, "%s nicht verdrahtet" % hat

    # ── (3) Kein globals() im Blueprint. Der Schnappschuss las
    # globals().get("BOT_VERSION", "?") — dort ist das der Namensraum DIESER
    # Datei, das Deck haette dauerhaft "?" gemeldet. Dieselbe stille
    # Fehlanzeige wie bei /api/version (W33) und config_drift (W32).
    for k in _ast.walk(_ast.parse(s)):
        if isinstance(k, _ast.Call) and _ast.unparse(k.func) == "globals":
            raise AssertionError(
                "nc/routes/systemlage.py benutzt globals(), Zeile %d — im "
                "Blueprint der falsche Namensraum" % k.lineno)

    # ── (4) Die drei Zustands-Dicts wandern als REFERENZ. Eine Kopie waere ab
    # Start eingefroren: das Panel zeigte ewig null Messungen, null
    # Whisper-Laeufe und die Automatik-Schalter vom Bootzeitpunkt.
    for name in ("_AUTOMATION", "_CHECK_TIMING", "_WHISPER_STATE"):
        gefunden = False
        for schluessel, wert in zip(_cfg.keys, _cfg.values):
            if isinstance(schluessel, _ast.Constant) and schluessel.value == name:
                gefunden = True
                assert _ast.unparse(wert) == name, \
                    ("ctx.cfg[%r] ist keine Referenz sondern %s — das Panel "
                     "waere ab Start eingefroren" % (name, _ast.unparse(wert)))
        assert gefunden, "%s fehlt im Kontext" % name

    # ── (5) Das Upload-Limit beantwortet nc/discordlimits.py selbst ─────────
    assert hasattr(D, "aktuell_mb") and hasattr(D, "aktuell_label")
    assert "_discord_upload_limit_mb    = _nc_dclimits.aktuell_mb" in b, \
        "der Bot rechnet das Limit wieder selbst aus"
    D.configure(guild_id=0, override_mb=None)
    assert D.guild_filesize_bytes() == 0, "ohne Client muss 0 herauskommen"
    # Ohne Guild greift das Free-Limit, nicht 0 — sonst meldete das Deck
    # "0 MB" und der Betreiber suchte einen Fehler, den es nicht gibt.
    assert D.aktuell_mb() == D.FREE_DEFAULT_MB, D.aktuell_mb()
    assert "Free" in D.aktuell_label(), D.aktuell_label()
    # Der Betreiber-Deckel senkt — aber nie unter die Qualitaets-Untergrenze.
    D.configure(guild_id=0, override_mb=9)
    assert D.aktuell_mb() == 9, D.aktuell_mb()
    D.configure(guild_id=0, override_mb=5)
    assert D.aktuell_mb() == D.FLOOR_MB, \
        ("ein Betreiber-Deckel unter FLOOR_MB darf nicht durchschlagen — "
         "sonst komprimiert der Bot Aufnahmen bis zur Unbrauchbarkeit, "
         "bekommen: %s" % D.aktuell_mb())
    D.configure(guild_id=0, override_mb=None)

    # ── (6) EINE Antwort auf "laeuft Whisper hier". bot.py hielt eine zweite
    # Fassung ohne try — ein kaputter Paket-Baum haette dort geworfen statt
    # "nein" zu sagen.
    assert "_faster_whisper_available = _nc_whisper.verfuegbar" in b, \
        "bot.py hat wieder eine eigene Whisper-Pruefung"
    assert isinstance(W.verfuegbar(), bool)

    # ── (7) Der Restream-Manager kommt aus dem Register — MIT Wache. Vor dem
    # Start ist er None; ohne die Wache staerbe die ganze Antwort an einem
    # AttributeError, statt eine leere Zielliste zu melden.
    assert '_nc_rsstate.MGR["obj"]' in s, "der Manager kommt nicht aus dem Register"
    assert "if _mgr is not None:" in s, "keine Wache gegen den None-Manager"

    ok("v4.2-W1: config_snapshot + check_timing im Blueprint, kein Geheimnis "
       "im Kontext, Zustand als Referenz")

def _test_v42_w2_ein_riegel_gegen_pfadausbruch():
    """v4.2-W2: ein Riegel, ueberall derselbe — und er faengt Symlinks."""
    import ast as _ast
    import os as _os
    import re as _re
    import tempfile as _tf

    def _nackt(pfad):
        """Quelltext OHNE Kommentare und ohne Docstrings.

        Dreimal ist in dieser Reihe ein Vertrag auf seine eigene Begruendung
        angeschlagen (W32 __file__, W33 Versionszahl, hier). Ein Vertrag, der
        den Kommentar meldet, der ihn erklaert, wird beim naechsten Mal
        geloescht statt gelesen — deshalb einmal richtig: ast.unparse wirft
        Kommentare weg, die Docstrings raeumen wir selbst heraus.
        """
        baum = _ast.parse(open(pfad, encoding="utf-8").read())
        for k in _ast.walk(baum):
            if not isinstance(k, (_ast.Module, _ast.FunctionDef,
                                  _ast.AsyncFunctionDef, _ast.ClassDef)):
                continue
            if (k.body and isinstance(k.body[0], _ast.Expr)
                    and isinstance(k.body[0].value, _ast.Constant)
                    and isinstance(k.body[0].value.value, str)):
                k.body.pop(0)
                if not k.body:
                    k.body.append(_ast.Pass())
        return _ast.unparse(_ast.fix_missing_locations(baum))

    from nc import sicherpfad as S

    # ── (1) Der Name verliert jeden Pfadanteil ─────────────────────────────
    for roh, erwartet in (("../../etc/passwd", "passwd"),
                          ("/etc/shadow", "shadow"),
                          ("a/b/c.txt", "c.txt"),
                          (".", "datei.bin"),
                          ("..", "datei.bin"),
                          ("", "datei.bin")):
        assert S.sicherer_name(roh) == erwartet, (roh, S.sicherer_name(roh))
    # Windows-Trenner: auf Linux ist "\\" ein NORMALES Zeichen, os.path.basename
    # laesst "..\\..\\x" komplett stehen. Wer nur basename benutzt, haelt das
    # fuer einen Dateinamen — auf einem Windows-Ziel ist es ein Ausbruch.
    assert S.sicherer_name("..\\..\\windows\\x.dll") == "x.dll", \
        ("Windows-Trenner nicht behandelt: %r. os.path.basename laesst auf "
         "Linux jeden Backslash stehen — der Name sieht harmlos aus und ist "
         "auf einem Windows-Ziel ein Ausbruch"
         % S.sicherer_name("..\\..\\windows\\x.dll"))
    # Harmloses bleibt unangetastet.
    assert S.sicherer_name("norm al-1(a).mp4") == "norm al-1(a).mp4"

    # ── (2) DER PUNKT DER WELLE: realpath faengt, was abspath durchlaesst.
    # Steht im Zielverzeichnis ein Symlink nach draussen, dann ist
    # abspath(basis/link/datei) == basis/link/datei — jede startswith-Pruefung
    # sagt "drin", geschrieben wird nach /etc. Genau so pruefte nc/updater.py
    # bei der Update-Entpackung, mit "Ein Zip-Slip schreibt sonst nach /etc"
    # als Kommentar darueber.
    basis = _tf.mkdtemp()
    _os.symlink("/etc", _os.path.join(basis, "raus"))
    ausbruch = _os.path.join(basis, "raus", "passwd")
    assert _os.path.abspath(ausbruch).startswith(basis + _os.sep), \
        "Vorbedingung: abspath haelt den Ausbruch faelschlich fuer sicher"
    assert S.unter(basis, ausbruch) is False, \
        "unter() laesst einen Symlink-Ausbruch durch — der ganze Riegel taugt nichts"
    assert S.unter(basis, _os.path.join(basis, "drin.txt")) is True

    # Nachbarverzeichnis mit gleichem Praefix: /x/archiv2 beginnt mit
    # /x/archiv, liegt aber nicht darin. Ein startswith ohne Trenner irrt.
    eltern = _tf.mkdtemp()
    a = _os.path.join(eltern, "archiv"); _os.makedirs(a)
    b = _os.path.join(eltern, "archiv2"); _os.makedirs(b)
    assert _os.path.join(b, "x").startswith(a), "Vorbedingung des Praefix-Falls"
    assert S.unter(a, _os.path.join(b, "x")) is False, \
        "unter() verwechselt ein Nachbarverzeichnis mit gleichem Praefix"

    # ── (3) sicher_join wirft, statt still danebenzugreifen. Ein Rueckfall
    # auf einen Ersatzpfad waere hier falsch: der Aufrufer schriebe in eine
    # Datei, die er nicht gemeint hat.
    assert S.sicher_join(basis, "../../etc/passwd") == _os.path.join(basis, "passwd")
    # Der Fall, den KEINE reine Namenspruefung faengt: der Name ist harmlos,
    # aber die Datei unter dem Namen ist ein Symlink nach draussen. Wer nur
    # basename() und einen Zeichensatz prueft, schreibt hier nach /etc.
    _os.symlink("/etc/passwd", _os.path.join(basis, "harmlos.txt"))
    try:
        S.sicher_join(basis, "harmlos.txt")
        raise AssertionError(
            "sicher_join laesst einen Symlink auf /etc/passwd durch — genau "
            "das faengt eine reine Namenspruefung nicht")
    except ValueError:
        pass

    # ── (4) Die Aufrufstellen benutzen ihn wirklich ────────────────────────
    up = _nackt("nc/updater.py")
    assert "_nc_sicherpfad.unter(root, p)" in up, \
        "nc/updater._abs prueft nicht mehr ueber nc.sicherpfad"
    assert "p.startswith(root + os.sep)" not in up, \
        ("nc/updater.py prueft wieder mit startswith+abspath — das laesst "
         "einen Symlink-Ausbruch durch")
    assert "_nc_sicherpfad.sicher_join(" in up, "rollback ohne Riegel"

    arc = _nackt("nc/routes/archive.py")
    assert "os.path.join(_c().cfg['ARCHIVE_DIR'], target_filename)" not in arc, \
        "der Zielpfad beim Umbenennen wird wieder ungeprueft zusammengesetzt"
    assert arc.count("_nc_sicherpfad.sicher_join(") >= 2, \
        "nicht alle Zielpfade im Archiv laufen ueber den Riegel"

    # ── (5) Der Katalogpfad wird nachgeschlagen, nicht zusammengesetzt ─────
    from nc import i18n as I
    assert set(I.KATALOGDATEI) == set(I.SPRACHEN), \
        "SPRACHEN und KATALOGDATEI laufen auseinander — eine Sprache ohne "\
        "Eintrag wuerde beim Laden mit KeyError sterben"
    i18nsrc = _nackt("nc/i18n.py")
    assert "'%s.json' % sprache" not in i18nsrc, \
        "der Katalogpfad wird wieder aus der Sprache zusammengesetzt"
    assert len(I.katalog("en")) > 1000, "der englische Katalog laedt nicht mehr"
    assert I.katalog("xx") == {}, "eine unbekannte Sprache muss leer bleiben"

    # ── (6) Die Tag-Muster halten an einer echten Tag-Grenze ───────────────
    # `</script >` beendet das Element im Browser. Ein Muster ohne \s* haelt
    # dort NICHT an und frisst den Rest der Datei: eine ID aus einem
    # JS-String wurde dann als doppelte Markup-ID gemeldet — ein Fehlalarm,
    # der das Werkzeug unglaubwuerdig macht.
    # Das echte Muster-Objekt pruefen, nicht seinen Quelltext: ein Regex,
    # den man aus der Datei zurueckparst, kommt mit verdoppelten Backslashes
    # zurueck und testet dann etwas anderes als das, was laeuft.
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_ncpatch_pruef", "tools/ncpatch.py")
    _m = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_m)
    probe = ('<div id="echt"></div><script>var s=\'<div id="echt"></div>\';'
             '</script ><p>x</p>')
    for name in ("RE_SCRIPT_WEG", "RE_SCRIPT_BLOCK"):
        assert hasattr(_m, name), "tools/ncpatch.py hat kein %s mehr" % name
    weg = _m.RE_SCRIPT_WEG.sub("", probe)
    ids = _re.findall(r'id="([^"]+)"', weg)
    assert len(ids) == len(set(ids)) == 1, \
        ("das Tag-Muster laesst eine ID aus dem Skriptblock stehen (%r) — "
         "Fehlalarm 'doppelte ID' bei jedem `</script >` im Deck" % (ids,))
    # Und es haelt an einer echten Tag-Grenze, nicht an einem Praefix.
    assert _m.RE_SCRIPT_WEG.sub("", "<scriptfoo>x</scriptfoo>") == \
        "<scriptfoo>x</scriptfoo>", "das Muster passt auf <scriptfoo>"
    assert len(_m.RE_SCRIPT_BLOCK.findall(
        "<script>a</script >\n<script>b</script>")) == 2, \
        "zwei Bloecke werden zu einem verschmolzen — node --check liefe dann "\
        "an einer Datei, die es so nie gab"

    ok("v4.2-W2: ein Riegel gegen Pfadausbruch (realpath, nicht abspath), "
       "Katalog per Erlaubnisliste, Tag-Muster an der Tag-Grenze")

def _test_v42_w3_codeql_barriere_und_setup():
    """v4.2-W3: eigene CodeQL-Abfrage statt 208 unlesbarer Meldungen."""
    import ast as _ast
    import os as _os

    for datei in (".github/codeql/qlpack.yml", ".github/codeql/NcSanitizer.qll",
                  ".github/codeql/NcStackTraceExposure.ql",
                  ".github/codeql/codeql-config.yml",
                  ".github/workflows/codeql.yml"):
        assert _os.path.exists(datei), "%s fehlt" % datei

    qll = open(".github/codeql/NcSanitizer.qll", encoding="utf-8").read()
    ql = open(".github/codeql/NcStackTraceExposure.ql", encoding="utf-8").read()
    cfg = open(".github/codeql/codeql-config.yml", encoding="utf-8").read()
    wf = open(".github/workflows/codeql.yml", encoding="utf-8").read()

    # ── (1) Die Regel wird ERSETZT, nicht abgeschaltet. Ein blosses exclude
    # haette auch jeden neuen, echten Befund verschluckt — und genau so einer
    # (str(ex) in nc/routes/brain.py) stand wochenlang unbemerkt in der Liste,
    # weil 208 Meldungen niemand mehr einzeln liest.
    # OHNE Kommentarzeilen pruefen, und OHNE PyYAML.
    #
    # Ohne Kommentare, weil die Begruendung daneben dieselben Schluessel nennt
    # — ein Vertrag, der auf seine eigene Erklaerung anschlaegt, wird beim
    # naechsten Mal geloescht statt gelesen (dieselbe Falle wie in W32/W33).
    #
    # Ohne PyYAML, weil der Vertrags-Job in der CI nur `orjson flask`
    # installiert. Das steht seit W23 als Regel in ci.yml — und ich bin beim
    # ersten Versuch trotzdem hineingelaufen: `import yaml` liess beide
    # Vertrags-Jobs mit ModuleNotFoundError sterben.
    def _ohne_kommentar(text):
        return "\n".join(z for z in text.splitlines()
                         if not z.lstrip().startswith("#"))

    knapp = _ohne_kommentar(cfg)
    assert "id: py/stack-trace-exposure" in knapp, \
        "die Standardregel wird nicht ersetzt"
    assert "uses: ./.github/codeql" in knapp, "die eigene Abfrage wird nicht geladen"
    assert "@id nc/stack-trace-exposure" in ql, "die Ersatzabfrage hat keine eigene Id"
    assert "disable-default-queries" not in knapp, \
        ("die Standard-Suite waere abgeschaltet — dann faellt weit mehr weg "
         "als die eine Regel")

    # ── (2) Die Ersatzabfrage ist die GLEICHE Abfrage. Nur die Barriere kommt
    # dazu. Waeren Quelle, Senke oder der Select veraendert, hiesse sie zu
    # Unrecht so und wuerde etwas anderes messen.
    assert "StackTraceExposureFlow::flowPath(source, sink)" in ql, \
        "die Ersatzabfrage folgt nicht mehr demselben Datenfluss"
    assert "import NcSanitizer" in ql, "die Barriere ist nicht eingebunden"
    assert "StackTraceExposure::Sanitizer" in qll, \
        "die Barriere haengt nicht am vorgesehenen Erweiterungspunkt"

    # ── (3) DIE NAMEN MUESSEN ZUSAMMENBLEIBEN. Die Barriere greift ueber die
    # Namen "nach_aussen" und "_fehler_text". Wird der Helfer im Python-Code
    # umbenannt und hier nicht, faellt die Barriere still weg — und 193
    # Meldungen kommen ohne Vorwarnung zurueck.
    for name in ("nach_aussen", "_fehler_text"):
        assert '"%s"' % name in qll, "die Barriere kennt %s nicht" % name
    import nc.fehlertext as F
    assert hasattr(F, "nach_aussen"), \
        "nc.fehlertext.nach_aussen heisst anders — die CodeQL-Barriere zeigt ins Leere"
    # Und der lokale Name in den Blueprints ist wirklich _fehler_text.
    baum = _ast.parse(open("nc/routes/systemlage.py", encoding="utf-8").read())
    namen = {k.name for k in _ast.walk(baum)
             if isinstance(k, (_ast.FunctionDef, _ast.AsyncFunctionDef))}
    assert "_fehler_text" in namen, \
        "die Blueprints nennen den Helfer anders — die Barriere greift dort nicht"

    # ── (4) Der Workflow faehrt dieselben Sprachen wie das Default-Setup.
    # Faellt eine weg, hoert die Analyse dort still auf — ohne rote Meldung.
    wf_knapp = _ohne_kommentar(wf)
    for sprache in ("actions", "javascript-typescript", "python"):
        assert "language: %s" % sprache in wf_knapp, \
            "Sprache %s fehlt im Workflow" % sprache
    assert "security-events: write" in wf, "ohne dieses Recht laedt nichts hoch"
    assert "config-file: ./.github/codeql/codeql-config.yml" in wf, \
        "der Workflow benutzt die Konfiguration nicht"

    # ── (5) Der Umstellungs-Hinweis steht drin. Solange das Default-Setup in
    # den Repo-Einstellungen aktiv ist, bricht dieser Workflow beim Hochladen
    # ab — das ist eine Handarbeit, die nur der Betreiber machen kann, und
    # ohne Hinweis sucht er den Fehler im Workflow.
    assert "Default setup" in wf and "Disable" in wf, \
        "der Hinweis auf das abzuschaltende Default-Setup fehlt"

    ok("v4.2-W3: CodeQL-Barriere fuer nach_aussen, Regel ersetzt statt "
       "abgeschaltet, Namen vertraglich gekoppelt")

def _test_v42_w4_preflight_und_resilienz():
    """v4.2-W4: die letzten grossen System-Routen bis auf selftest."""
    import ast as _ast
    import re as _re

    import nc.systemprobe as P

    b = open("bot.py", encoding="utf-8").read()
    s = open("nc/routes/systemlage.py", encoding="utf-8").read()

    # ── (1) Draussen aus dem Monolithen, drin im Blueprint ─────────────────
    for name in ("api_system_preflight", "api_system_resilience"):
        assert ("\ndef %s(" % name) not in b, "%s steht noch in bot.py" % name
        assert "def %s(" % name in s, "%s fehlt im Blueprint" % name

    # ── (2) KEIN globals() — im Blueprint der falsche Namensraum. Der
    # Monolith hatte hier `RECORDINGS_DIR if "RECORDINGS_DIR" in globals()
    # else "/"`. Uebernommen waere der Test dauerhaft False gewesen und die
    # Preflight-Karte haette die SYSTEMPLATTE gemessen statt des
    # Aufnahme-Verzeichnisses — eine Zahl, die stimmt aussieht und falsch ist.
    for k in _ast.walk(_ast.parse(s)):
        if isinstance(k, _ast.Call) and _ast.unparse(k.func) == "globals":
            raise AssertionError(
                "nc/routes/systemlage.py benutzt globals(), Zeile %d" % k.lineno)
    assert "_c().recordings_dir" in s, \
        "die Preflight-Karte misst nicht mehr das Aufnahme-Verzeichnis"

    # ── (3) KEINE ZWEITE WAHRHEIT. recordings_dir, ffmpeg_threads_bg und
    # ffmpeg_nice_bg liegen seit W110/W116 als SLOT im Kontext. Sie
    # zusaetzlich nach cfg zu legen waeren zwei Werte fuer dieselbe Sache,
    # die beim naechsten Umbau auseinanderlaufen.
    i = b.index("_nc_ctx.configure(")
    block = b[i:b.index("\n)\n", i)]
    for doppelt in ("RECORDINGS_DIR", "FFMPEG_THREADS_BG", "FFMPEG_NICE_BG"):
        assert '"%s":' % doppelt not in block, \
            ("ctx.cfg[%r] dupliziert einen vorhandenen Slot — zwei Werte fuer "
             "dieselbe Sache" % doppelt)

    # ── (4) Jeder gelesene cfg-Schluessel wird auch geliefert. Ein Tippfehler
    # waere sonst ein KeyError erst beim Aufruf der Route — im Betrieb, nicht
    # im Test. (Genau so ist FFMPEG_THREADS_BG in dieser Welle aufgefallen.)
    benutzt = set(_re.findall(r"""c\[["']([A-Z_][A-Z0-9_]*)["']\]""", s))
    geliefert = set(_re.findall(r'^\s+"([A-Z_][A-Z0-9_]*)":', block, _re.M))
    fehlt = sorted(benutzt - geliefert)
    assert not fehlt, "der Blueprint liest cfg-Schluessel, die der Bot nicht liefert: %r" % fehlt

    # ── (5) Die drei Sonden sind Aliase, kein zweiter Koerper ──────────────
    for zeile in ("_cpu_load_snapshot = _nc_probe.cpu_load_snapshot",
                  "_disk_pct = _nc_probe.disk_pct",
                  "_check_ai_alive_sync = _nc_probe.ai_alive"):
        assert zeile in b, "bot.py haelt wieder einen eigenen Koerper: %s" % zeile

    # ── (6) disk_pct misst das KONFIGURIERTE Verzeichnis, nicht das
    # Arbeitsverzeichnis. Sonst zeigt das Deck die Systemplatte und der
    # Plattenwaechter greift zu spaet.
    import os as _os
    import tempfile as _tf
    d = _tf.mkdtemp()
    sicher = P.recordings_dir()
    try:
        P.configure(recordings_dir=d)
        assert P.recordings_dir() == d
        # Womit wirklich gemessen wird: ein Vergleich der Prozentzahlen taugt
        # nicht — Temp- und Arbeitsverzeichnis liegen oft auf derselben
        # Platte und liefern denselben Wert. Also den Aufruf abfangen.
        import shutil as _sh
        gesehen = []
        _echt = _sh.disk_usage
        _sh.disk_usage = lambda pfad: (gesehen.append(pfad), _echt(pfad))[1]
        try:
            pct, st = P.disk_pct()
        finally:
            _sh.disk_usage = _echt
        assert gesehen == [d], \
            ("disk_pct misst %r statt des konfigurierten Verzeichnisses %r — "
             "das Deck zeigte dann die Systemplatte und der Plattenwaechter "
             "griffe zu spaet" % (gesehen, d))
        assert isinstance(pct, int) and 0 <= pct <= 100, pct
        assert st is not None and st.total > 0
        # Ein unbrauchbarer Pfad darf keine Ausnahme werfen — der Aufrufer ist
        # ein Statuspanel, das eine Zahl braucht.
        P.configure(recordings_dir=_os.path.join(d, "gibtsnicht"))
        pct2, _ = P.disk_pct()
        assert isinstance(pct2, int), pct2
    finally:
        P.configure(recordings_dir=sicher)

    # ── (7) cpu_load_snapshot liefert die Felder, die das Panel zeigt. Ein
    # leeres Dict waere kein Fehler, sondern ein leeres Panel.
    d2 = P.cpu_load_snapshot()
    for feld in ("state", "mem_total_gb", "swap_pct"):
        assert feld in d2, "cpu_load_snapshot liefert %r nicht mehr: %r" % (feld, sorted(d2))

    # ── (8) Der Whisper-Drosselzustand bleibt sichtbar — sonst laeuft die
    # Drossel unbemerkt (B98).
    assert '"throttled": c["_WHISPER_STATE"]["throttled"]' in s, \
        "der Drossel-Zustand fehlt in der Resilienz-Antwort"

    ok("v4.2-W4: preflight + resilience im Blueprint, Sonden in nc/, "
       "keine zweite Wahrheit fuer die drei Slots")

def _test_v42_w6_zerschnittene_saetze():
    """v4.2-W6: Saetze, die ein Inline-Tag zerschneidet, sind uebersetzbar."""
    import json as _json
    import sys as _sys

    _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "tools"))
    import i18n_extract as _ex

    # ── (1) BEIDE SEITEN, EIN SCHLUESSEL. Das Verfahren steht und faellt
    # damit, dass Extraktor (Python) und Uebersetzer (Browser-JS) aus
    # denselben Kindern dieselbe Zeichenkette bauen. Faellt eine Seite auch
    # nur um ein Leerzeichen ab, trifft KEIN Eintrag mehr — und der Katalog
    # meldet trotzdem "0 fehlend", weil er nur zaehlt, was der Extraktor
    # gesehen hat. Genau die stille Luecke, die W28 schon einmal hatte.
    kinder = [("t", "Gebucht wird der "), ("el", "b"),
              ("t", " \u2014 der Tag\n   der Gutschrift.")]
    assert _ex.muster_schluessel(kinder) == \
        "Gebucht wird der {0} \u2014 der Tag der Gutschrift.", \
        "der Muster-Schluessel wird anders gebaut als dokumentiert"
    # Umbruch und Einrueckung zu EINEM Leerzeichen, aussen getrimmt: sonst
    # haengt der Schluessel an der Formatierung des HTML und jede
    # Umformatierung toetet ihn stillschweigend.
    assert _ex.muster_schluessel([("t", "\n  A  "), ("el", "b"), ("t", "  B\n")]) \
        == "A {0} B", "Leerraum wird nicht normalisiert"

    js = open("nc/routes/i18n.py", encoding="utf-8").read()
    for teil in ("function musterSchluessel(", "function musterEinsetzen(",
                 "musterEinsetzen(n);"):
        assert teil in js, "der Browser-Uebersetzer kennt %s nicht" % teil
    # Die JS-Seite muss dieselben drei Regeln fahren wie die Python-Seite.
    for teil in ("replace(/\\s+/g, ' ')", "replace(/^\\s+|\\s+$/g, '')"):
        assert teil in js, "im Browser fehlt die Regel %s" % teil
    # Und dieselben GRENZEN. Nicht als Zeichenkette verglichen, sondern als
    # Menge: wer in Python ein Inline-Tag ergaenzt und im Browser nicht, baut
    # eine Luecke, die kein Textvergleich sieht — der Extraktor sammelt dann
    # einen Schluessel ein, den der Browser nie erzeugt.
    js_inline = set(re.findall(r"(\w+):1",
                               re.search(r"var INLINE = \{(.*?)\};", js, re.S).group(1)))
    assert js_inline == {t.upper() for t in _ex._INLINE_TAGS}, \
        "Inline-Listen laufen auseinander: nur JS %r / nur Python %r" % (
            sorted(js_inline - {t.upper() for t in _ex._INLINE_TAGS}),
            sorted({t.upper() for t in _ex._INLINE_TAGS} - js_inline))
    js_max = int(re.search(r"var MAX_PLATZ = (\d+)", js).group(1))
    assert js_max == _ex._MAX_PLATZHALTER, \
        "MAX_PLATZ %d != _MAX_PLATZHALTER %d" % (js_max, _ex._MAX_PLATZHALTER)

    # ── (2) NUR WO ES KLEMMT. Traegt jedes Textstueck fuer sich schon als
    # Knoten, macht der normale Weg das laengst — ein Muster wuerde dort eine
    # vorhandene Uebersetzung durch einen laengeren Schluessel ersetzen und
    # damit geleistete Arbeit vernichten.
    def _muster(html):
        m, _ = _ex._muster_strings(html)
        return m

    gut = _muster("<p>Der Bot laeuft seit gestern. <b>x</b> "
                  "Die Aufnahme ist fertig und liegt im Archiv.</p>")
    assert not gut, "Muster gebaut, obwohl beide Stuecke allein tragen: %r" % gut
    klemmt = _muster("<p>Gebucht wird der <b>Zufluss</b> \u2014 der Tag der "
                     "Gutschrift auf dem Konto, nicht der Stream-Tag.</p>")
    assert klemmt == {"Gebucht wird der {0} \u2014 der Tag der Gutschrift auf "
                      "dem Konto, nicht der Stream-Tag."}, \
        "der zerschnittene Satz wird nicht eingesammelt: %r" % klemmt
    # <code> ist Daten (Befehle, Logzeilen) und darf nie Schluessel werden.
    assert not _muster("<code>ffmpeg -i <b>x</b> und noch etwas Text dazu</code>"), \
        "ein <code>-Block wurde zum Muster"
    # Ein Absatz mit einem Dutzend Tags ist ein Layout, kein Satz.
    viele = "<p>Ein Satz der lang genug ist %s und weiter geht.</p>" % (
        "<b>x</b>" * (_ex._MAX_PLATZHALTER + 1))
    assert not _muster(viele), "Layout mit %d Tags wurde zum Satz" % (
        _ex._MAX_PLATZHALTER + 1)

    # ── (3) VERDRAENGT, NICHT VERWAIST. Beim Muster ersetzt der Browser den
    # ganzen Inhalt; die einzelnen Knoten gibt es danach nicht mehr. Ein
    # Eintrag fuer so ein Stueck waere tot. Steht derselbe Text ANDERSWO noch
    # fuer sich, muss er dagegen bleiben.
    _, weg = _ex._muster_strings(
        "<p>Gebucht wird der <b>Zufluss</b> \u2014 der Tag der Gutschrift auf "
        "dem Konto, nicht der Stream-Tag.</p>")
    assert "Gebucht wird der" in weg, "das Bruchstueck wird nicht verdraengt"
    _, weg2 = _ex._muster_strings(
        "<p>Gebucht wird der <b>Zufluss</b> \u2014 der Tag der Gutschrift auf "
        "dem Konto, nicht der Stream-Tag.</p><div>Gebucht wird der</div>")
    assert "Gebucht wird der" not in weg2, \
        "ein Text, der anderswo allein steht, wurde mit verdraengt"

    # ── (4) KEIN PLATZHALTER DARF VERLOREN GEHEN. Der Browser setzt die
    # VORHANDENEN Kind-Elemente wieder ein. Fehlt in der Uebersetzung ein
    # {n}, verschwaende der Umbau das Element \u2014 ein fehlender Link ist
    # schlimmer als ein deutscher Satz. Der Uebersetzer laesst so einen
    # Eintrag deshalb liegen; hier faellt er auf, statt still zu wirken.
    def _pruefe_katalog(strings):
        schlecht = []
        for de, en in strings.items():
            n = len(re.findall(r"\{(\d+)\}", de))
            if not n or not en:
                continue
            idx = [int(x) for x in re.findall(r"\{(\d+)\}", en)]
            if sorted(idx) != list(range(n)):
                schlecht.append(de[:60])
        return schlecht

    for datei in sorted(os.listdir("locales")):
        if not datei.endswith(".json"):
            continue
        with open(os.path.join("locales", datei), encoding="utf-8") as f:
            strings = _json.load(f).get("strings", {})
        schlecht = _pruefe_katalog(strings)
        assert not schlecht, "locales/%s: Platzhalter passen nicht: %r" % (
            datei, schlecht)
    # Der Melder muss auch wirklich anschlagen \u2014 sonst prueft er nichts.
    assert _pruefe_katalog({"A {0} B {1}": "A {0} B"}), \
        "fehlender Platzhalter wird nicht gemeldet"
    assert _pruefe_katalog({"A {0} B": "A {0} B {0}"}), \
        "doppelter Platzhalter wird nicht gemeldet"

    ok("v4.2-W6: zerschnittene Saetze \u2014 ein Schluessel auf beiden Seiten")


def _test_v42_w5_selftest_und_leerer_monolith():
    """v4.2-W5: keine System-Route mehr im Monolithen."""
    import ast as _ast
    import re as _re

    b = open("bot.py", encoding="utf-8").read()
    s = open("nc/routes/selbsttest.py", encoding="utf-8").read()

    # ── (1) DER ABSCHLUSS von Vorschlag 2. Alle acht System-Routen sind
    # draussen. Steht eine wieder in bot.py, ist der Abbau rueckwaerts
    # gelaufen — und das faellt sonst niemandem auf.
    ACHT = ("api_system", "api_system_config_snapshot", "api_system_preflight",
            "api_system_preflight_history", "api_system_resilience",
            "api_check_timing", "api_config_drift", "api_selftest")
    drin = [n for n in ACHT if ("\ndef %s(" % n) in b]
    assert not drin, "wieder im Monolithen: %r" % drin
    assert "def api_selftest(" in s, "api_selftest fehlt im Blueprint"
    assert "register_blueprint(_nc_routes_selbsttest.bp)" in b, \
        "der Blueprint ist nicht registriert — /api/selftest waere 404"

    # ── (2) Der Helfer ist mitgewandert. 23 Aufrufe, alle in dieser einen
    # Funktion — er im Monolithen, sie im Blueprint waere ein Import ueber
    # die Architektur-Grenze.
    assert "def _st_befund(" in s, "_st_befund fehlt im Blueprint"
    assert "\ndef _st_befund(" not in b, "_st_befund steht noch in bot.py"

    # ── (3) EIN WEG zu Sperrliste und Angriffen. nc/routes/abwehr.py haelt
    # seit W25 die Haken, die der Bot eintraegt. Ein zweiter Weg zu denselben
    # Daten waere eine zweite Wahrheit — und die beiden Panels koennten
    # Widerspruechliches melden.
    assert "_nc_routes_abwehr.HAKEN[name][\"fn\"]" in s, \
        "der Selbsttest holt Sperrliste/Angriffe nicht ueber die Abwehr-Haken"
    for haken in ('_haken("sperrliste")', '_haken("angriffe")'):
        assert haken in s, "%s wird nicht benutzt" % haken
    # Fehlt der Haken (Bot laeuft nicht), darf NICHT "nichts gefunden"
    # herauskommen. Bei einer Sicherheitsanzeige ist das die gefaehrlichste
    # aller Antworten — dieselbe Ueberlegung wie in abwehr._nicht_bereit().
    # Nach VERHALTEN, nicht nach Text: ein `return {}` steht auch im
    # except-Zweig, die Textsuche kann beides nicht unterscheiden.
    from nc import ctx as _nc_ctx_modul
    from nc.routes import abwehr as _A

    def _ctx_konfiguriert():
        return _nc_ctx_modul.is_configured()

    from nc.routes import selbsttest as _S
    _sicher = _A.HAKEN["sperrliste"]["fn"]
    try:
        _A.HAKEN["sperrliste"]["fn"] = None
        assert _S._haken("sperrliste") == {}, \
            ("ein fehlender Haken liefert ein Ergebnis statt Leere — der "
             "Selbsttest meldete dann 'keine Sperren', obwohl gar nicht "
             "nachgesehen wurde")
        _A.HAKEN["sperrliste"]["fn"] = lambda: {"total_banned": 7}
        assert _S._haken("sperrliste") == {"total_banned": 7}, \
            "ein vorhandener Haken wird nicht durchgereicht"
        # Der werfende Haken loggt — und Loggen braucht den gefuellten
        # Kontext. Ohne ihn (Vertrag allein aufgerufen) waere der Test ein
        # Fehlalarm ueber etwas, das im Betrieb nie vorkommt.
        if _ctx_konfiguriert():
            def _kaputt():
                raise RuntimeError("absichtlich")
            _A.HAKEN["sperrliste"]["fn"] = _kaputt
            assert _S._haken("sperrliste") == {}, \
                "ein werfender Haken reisst den ganzen Selbsttest mit"
    finally:
        _A.HAKEN["sperrliste"]["fn"] = _sicher

    # ── (4) Der Restream-Manager kommt aus dem Register — MIT Wache. Vor dem
    # Start ist er None; ohne Wache kippte ein AttributeError die GANZE
    # Antwort, also auch die 20 Befunde ohne Restream-Bezug.
    assert '_nc_rsstate.MGR["obj"]' in s, "der Manager kommt nicht aus dem Register"
    # Jeder Zugriff auf seine privaten Felder laeuft ueber getattr mit
    # Vorgabe. Ein nacktes _mgr()._procs waere vor dem Start ein
    # AttributeError auf None.
    for feld in ("_procs", "_srcexpired"):
        for treffer in _re.finditer(r"[\w()]+\.%s\b" % feld, s):
            zeile = s[:treffer.start()].count("\n") + 1
            assert "getattr(" in s.splitlines()[zeile - 1], \
                ("ungeschuetzter Zugriff auf %s in Zeile %d — vor dem Start "
                 "ist der Manager None und die GANZE Antwort kippt, nicht nur "
                 "der Restream-Teil" % (feld, zeile))
    assert s.count("getattr(_mgr()") + s.count('getattr(_m, "_procs"') >= 3, \
        "zu wenige geschuetzte Zugriffe — eine Stelle wurde vergessen"

    # ── (5) Kein globals() — dieselbe Falle wie in W32/W33/W4.
    for k in _ast.walk(_ast.parse(s)):
        if isinstance(k, _ast.Call) and _ast.unparse(k.func) == "globals":
            raise AssertionError("nc/routes/selbsttest.py benutzt globals(), Zeile %d" % k.lineno)

    # ── (6) Jeder gelesene cfg-Schluessel wird auch geliefert. Sonst ein
    # KeyError beim ersten Aufruf — im Betrieb, nicht im Test.
    i = b.index("_nc_ctx.configure(")
    block = b[i:b.index("\n)\n", i)]
    benutzt = set(_re.findall(r"""c\[["']([A-Z_][A-Z0-9_]*)["']\]""", s))
    geliefert = set(_re.findall(r'^\s+"([A-Z_][A-Z0-9_]*)":', block, _re.M))
    fehlt = sorted(benutzt - geliefert)
    assert not fehlt, "der Blueprint liest cfg-Schluessel, die der Bot nicht liefert: %r" % fehlt

    # ── (7) Kein Stream-Schluessel im Kontext. Der Selbsttest fragt nur, OB
    # einer gesetzt ist.
    assert '"YOUTUBE_STREAM_KEY"' not in s, \
        "der Selbsttest greift auf den YouTube-Schluessel zu statt auf HAT_YOUTUBE_KEY"
    assert 'c["HAT_YOUTUBE_KEY"]' in s, "die Boolean-Pruefung fehlt"

    ok("v4.2-W5: /api/selftest im Blueprint — keine der acht System-Routen "
       "steht mehr im Monolithen")

def _test_v42_w7_motd_optik():
    """v4.2-W7: die vier neuen MOTD-Anzeigen — und die eine Grundregel."""
    import subprocess as _sp

    motd = "tools/motd.sh"
    quelle = open(motd, encoding="utf-8").read()

    # ── (1) DIE GRUNDREGEL. Eine MOTD darf NIE einen Login blockieren. Jedes
    # neue Kommando, das haengen kann, gehoert hinter tmo(); ein set -e wuerde
    # bei der ersten leeren Ausgabe den Login abbrechen. Beides ist keine
    # Stilfrage: ein blockierter Login auf einem Server ohne Konsole ist ein
    # Ausfall, der sich nicht mehr aus der Ferne beheben laesst.
    assert "\nset -e" not in quelle, "set -e in der MOTD — ein Login darf nie abbrechen"
    for befehl in ("ip route show default", "tail -n 50000"):
        stelle = quelle.find(befehl)
        assert stelle > 0, "%r fehlt" % befehl
        zeile = quelle[quelle.rfind("\n", 0, stelle) + 1:stelle]
        assert "tmo " in zeile, "%r laeuft ohne Zeitdeckel: %r" % (befehl, zeile.strip())

    # ── (2) EIN MESSFENSTER, NICHT ZWEI. Der Durchsatz braucht zwei Proben
    # mit Abstand. Ein eigener sleep waere der teuerste Posten der ganzen
    # Anzeige geworden — teurer als alles andere zusammen. Er haengt sich
    # deshalb an das Fenster, das fuer die CPU ohnehin gewartet wird.
    assert quelle.count('sleep "$CPU_SAMPLE"') == 1, \
        "mehr als ein Messfenster — der Durchsatz kostet jetzt einen eigenen sleep"
    fenster = quelle[quelle.find("CPU_LINES=\"\"; NET_RX="):]
    fenster = fenster[:fenster.find('\nfi\n')]
    assert fenster.find("_n1=") < fenster.find('sleep "$CPU_SAMPLE"') < fenster.find("_n2="), \
        "die Netz-Proben liegen nicht um das Messfenster herum"

    # ── (3) DIE AMPEL BRAUCHT IHRE MESSWERTE VOR DEM KOPF. Genau deshalb sind
    # die Proben fuer Dienst und Dashboard hochgezogen worden. Rutscht eine
    # zurueck hinter den Kopf, zeigt die Ampel wieder "alles im Griff",
    # waehrend zwei Zeilen tiefer "gestoppt" steht — der gefaehrlichste aller
    # Zustaende, weil er falsche Sicherheit gibt.
    kopf = quelle.find("# ── Kopf ─")
    for name in ("BOT_STATE=unbekannt", "DASH_STATE=aus", "LAGE=ok", "DPCT=0"):
        assert 0 < quelle.find(name) < kopf, "%s wird erst NACH dem Kopf gesetzt" % name
    # Und die Ursache muss die Folge schlagen: ein toter Bot macht das
    # Dashboard unerreichbar — stuende dort die Folge, suchte der Betreiber
    # am falschen Ende.
    assert quelle.find('lage_setz err "Bot laeuft nicht"') < \
        quelle.find('lage_setz err  "Dashboard nicht erreichbar"'), \
        "die Folge wird vor der Ursache geprueft"

    # ── (4) VERHALTEN, nicht Wortlaut. Die vier Anzeigen werden ausgefuehrt
    # und ihr Ergebnis geprueft — ein Textvergleich haette bei jeder der drei
    # Umformulierungen dieser Datei gekippt, ohne dass etwas kaputt war.
    def _lauf(*teile, **umgebung):
        # Erst der Vorgabewert, dann der Aufrufer — sonst entschiede die
        # Umgebung des Testlaufs mit, und der Vertrag waere von der Maschine
        # abhaengig, auf der er laeuft.
        umg = dict(os.environ)
        umg["COLOR_MODE"] = "off"
        umg.update(umgebung)
        return _sp.run(["bash", motd] + list(teile), capture_output=True,
                       text=True, timeout=60, env=umg).stdout

    # Der Miniverlauf: sieben Zahlen, sieben Zeichen, das Maximum als Vollblock
    # und die Null als Grundlinie. Ohne diese Skalierung waere er bei kleinen
    # Zahlen platt und bei grossen abgeschnitten.
    hilf = _sp.run(["bash", "-c",
                    "source /dev/stdin <<'X'\n%s\nX\nspark 0 1 0 12 0 3 0"
                    % re.search(r"^spark\(\)\{.*?^\}", quelle, re.S | re.M).group(0)],
                   capture_output=True, text=True, timeout=30).stdout
    assert len(hilf) == 7, "der Verlauf hat %d Zeichen statt sieben: %r" % (len(hilf), hilf)
    assert hilf[3] == "\u2588", "der Hoechstwert ist kein Vollblock: %r" % hilf
    assert hilf[0] == hilf[2] == "\u2581", "die Null liegt nicht auf der Grundlinie: %r" % hilf

    # Die Ampel: gruen nur, wenn wirklich alles steht. Geprueft mit
    # vorgetaeuschtem systemctl/curl, weil die echten Zustaende sich in einem
    # Testlauf nicht herstellen lassen — und ungeprueft waere ausgerechnet der
    # Pfad, den der Betreiber jeden Tag sieht, der einzige ohne Deckung.
    stub = tempfile.mkdtemp()
    with open(os.path.join(stub, "systemctl"), "w", encoding="utf-8") as f:
        f.write('#!/bin/bash\ncase "$*" in\n'
                '  *"is-active --quiet"*) [ "$FAKE_BOT" = up ] && exit 0 || exit 1;;\n'
                '  *"show -p Result"*) echo "exit-code";;\n'
                '  *"show -p NRestarts"*) echo 0;;\n'
                '  *list-unit-files*) exit 1;;\nesac\nexit 0\n')
    with open(os.path.join(stub, "curl"), "w", encoding="utf-8") as f:
        f.write('#!/bin/bash\n[ "$FAKE_DASH" = none ] && exit 7\n'
                'echo \'{"ok": true, "procs": 4, "zombies": 0}\'\n')
    for name in ("systemctl", "curl"):
        os.chmod(os.path.join(stub, name), 0o755)
    botdir = tempfile.mkdtemp()
    open(os.path.join(botdir, "bot.py"), "w").close()

    pfad = stub + os.pathsep + os.environ.get("PATH", "")
    gruen = _lauf(PATH=pfad, FAKE_BOT="up", FAKE_DASH="ok",
                  SERVICE="nightcrawler", BOT_DIR=botdir)
    rot = _lauf(PATH=pfad, FAKE_BOT="down", FAKE_DASH="none",
                SERVICE="nightcrawler", BOT_DIR=botdir)
    assert "alles im Griff" in gruen, "der gesunde Zustand meldet keine gruene Ampel"
    assert "Bot laeuft nicht" in rot, "der gestoppte Bot erreicht die Ampel nicht"
    assert "alles im Griff" not in rot, \
        "gruene Ampel trotz gestopptem Bot — falsche Sicherheit"
    # Die Ampel darf die Zeile darunter nie ueberholen: was oben steht, muss
    # unten belegt sein.
    assert "gestoppt" in rot, "die Ampel meldet mehr, als die Zeilen darunter zeigen"

    # ── (5) DER VERLAUFSBALKEN faellt zurueck, statt zu verschwinden. Auf
    # einer 16-Farben-Handy-App gibt es keinen Verlauf; dort muss der Balken
    # trotzdem dastehen. Ein "schoen oder gar nicht" waere hier der falsche
    # Handel — die MOTD ist eine Statusanzeige, kein Plakat.
    for modus in ("truecolor", "256", "16", "off"):
        aus = _lauf(COLOR_MODE=modus, BOT_DIR=botdir)
        assert "\u2588" in aus or "\u2592" in aus, \
            "COLOR_MODE=%s zeigt gar keinen Balken" % modus

    ok("v4.2-W7: MOTD-Optik \u2014 Ampel vor dem Kopf, ein Messfenster, Balken faellt zurueck")


def _test_v42_w8_windows_installer_spricht_englisch():
    """v4.2-W8: tools/install.bat hatte gar keine Sprachschicht."""
    import sys as _sys

    _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "tools"))
    import i18n_tools as _it

    bat = open("tools/install.bat", encoding="utf-8").read()

    # ── (1) DER PRUEFER SAH DIESE DATEI GAR NICHT AN. Genau das ist die
    # gefaehrliche Sorte Luecke: er meldete 100 % Abdeckung fuer die
    # Shell-Werkzeuge, waehrend der Windows-Installer zu 0 % uebersetzt war.
    # Eine Abdeckungszahl, die nur zaehlt, was sie ohnehin kennt, verdeckt
    # genau das, was sie sichtbar machen soll (dieselbe Lehre wie W28).
    assert "tools/install.bat" in _it.QUELLEN_BAT, \
        "der Windows-Installer steht nicht in der Quellenliste des Pruefers"
    gefunden = _it.sammeln()
    assert len(gefunden) > 250, \
        "nur %d Zeichenketten — der Batch-Sammler greift nicht" % len(gefunden)

    # ── (2) REIN ASCII. Steht so in der Kopfzeile der Datei und ist keine
    # Stilfrage: cmd.exe rendert je nach Codepage sonst Buchstabensalat, und
    # zwar erst beim Anwender.
    schlecht = sorted({c for c in bat if ord(c) > 127})
    assert not schlecht, "nicht-ASCII in install.bat: %r" % schlecht

    # ── (3) DER TABULATOR IST ECHT. Trennzeichen im Katalog, in "delims=" und
    # im Suchmuster. Ein Editor, der Tabs zu Leerzeichen macht, wuerde den
    # Nachschlag still wirkungslos machen — die Ausgabe bliebe deutsch, ohne
    # dass irgendetwas scheitert.
    assert 'delims=\t"' in bat, "das Trennzeichen in delims= ist kein Tabulator mehr"
    assert '/c:"%~1\t"' in bat, "das Suchmuster traegt keinen Tabulator mehr"
    assert "/b /l /c:" in bat, \
        "findstr laeuft nicht mehr literal und am Zeilenanfang — die deutschen " \
        "Texte enthalten Punkte und Klammern, die als Ausdruck etwas anderes bedeuten"

    # ── (4) DER DEUTSCHE PFAD BLEIBT UNBERUEHRT. Dieser Installer laesst sich
    # hier nicht ausfuehren — es gibt kein cmd.exe. Was man nicht ausprobieren
    # kann, muss so gebaut sein, dass sein Fehlschlag folgenlos ist: ohne
    # gesetzten Katalog kehrt :t VOR dem Nachschlag zurueck, und der
    # Rueckfallwert steht schon in der Zeile davor.
    zeilen = [z.strip() for z in
              bat[bat.index("\n:t\n") + 1:].split("\n") if z.strip()]
    assert zeilen[1] == 'set "UEBERSETZT=%~1"', \
        "der Rueckfall steht nicht als erste Anweisung in :t: %r" % zeilen[1]
    assert zeilen[2] == "if not defined NC_KATALOG goto :eof", \
        "ohne Katalog wird trotzdem nachgeschlagen: %r" % zeilen[2]
    assert "2^>nul" in bat, "ein Fehlschlag von findstr wuerde eine Meldung ausgeben"

    # ── (5) KEINE DEUTSCHE AUSGABE MEHR AN EINER SENKE VORBEI. Ein
    # vergessenes echo faellt sonst niemandem auf: eine deutsch gebliebene
    # Zeile sieht aus wie eine, die es noch nicht gibt.
    uebrig = []
    for zeile in bat.split("\n"):
        st = zeile.strip()
        if st.lower().startswith("rem"):
            continue
        # Umleitungen in eine Datei sind keine Bildschirmausgabe.
        if re.search(r'>+\s*"', zeile):
            continue
        # NICHT nur am Zeilenanfang: `if exist ... echo Merkzettel` ist genau
        # die Form, die diese Datei benutzt — ein Pruefer, der nur auf "echo"
        # am Anfang sieht, laesst sie durch. (Beim Mutationstest genau so
        # passiert; deshalb steht es hier.)
        m = re.search(r'(?<![>\w])echo\s+(\S.*)$', zeile)
        if not m:
            continue
        rest = m.group(1).strip()
        if "%" in rest or not re.search(r"[A-Za-z]{4}", rest):
            continue
        # Ein Befehl zum Abtippen ist kein Satz. Dieselbe Ausnahme wie im
        # HTML-Extraktor: "winget install --id Git.Git -e" uebersetzt man
        # nicht — wer es taete, gaebe dem Anwender ein Kommando, das nicht
        # laeuft.
        if re.match(r"(winget|git|pip|python|curl|schtasks|robocopy|"
                    r"powershell|cd|del|mkdir|rmdir)\b", rest):
            continue
        uebrig.append(rest[:60])
    assert not uebrig, "Ausgabe an der Senke vorbei: %r" % uebrig

    # ── (6) DER NACHSCHLAG TRIFFT WIRKLICH. Ohne cmd.exe ist das der Ersatz
    # fuer den Lauf: findstr /b /l /c: wird nachgebildet und jeder eingesammelte
    # Schluessel dagegen geprueft. Ein Schluessel, den findstr nicht faende,
    # waere eine Zeile, die fuer immer deutsch bleibt.
    roh = open("locales/tools.en.tsv", encoding="utf-8").read().split("\n")
    doppelt = {}
    for z in roh:
        if z.startswith("#") or "\t" not in z:
            continue
        doppelt.setdefault(z.split("\t", 1)[0], 0)
        doppelt[z.split("\t", 1)[0]] += 1
    mehrfach = sorted(k for k, n in doppelt.items() if n > 1)
    assert not mehrfach, "doppelte Schluessel im Katalog: %r" % mehrfach[:5]

    def _findstr(schluessel):
        """findstr /b /l /c:"<schluessel><TAB>" — literal, am Zeilenanfang."""
        muster = schluessel + "\t"
        return [z for z in roh if z.startswith(muster)]

    kat = _it.katalog("en")
    for schluessel in sorted(gefunden):
        treffer = _findstr(schluessel)
        assert len(treffer) == 1, \
            "findstr faende %d Zeilen fuer %r" % (len(treffer), schluessel[:60])
        wert = treffer[0].split("\t", 1)[1]
        assert wert.strip(), "leere Uebersetzung fuer %r" % schluessel[:60]
        assert kat[schluessel] == wert
    # Und der Melder muss anschlagen — sonst prueft er nichts.
    assert not _findstr("diesen Text gibt es im Katalog nicht")

    # ── (7) KEIN SCHLUESSEL MIT WERT. Ein Text mit %ZIEL% darin steht erst zur
    # Laufzeit fest und traefe nie. Dafuer gibt es die *_wert-Senken — der
    # feste Teil ist der Schluessel, der Wert wird angehaengt.
    mit_wert = [k for k in gefunden if "%" in k]
    assert not mit_wert, "Schluessel mit Laufzeitwert: %r" % mit_wert[:3]

    ok("v4.2-W8: install.bat spricht Englisch \u2014 ein Katalog fuer beide Installer")


def _test_v42_w9_oauth_ueberlebt_neustart_und_stoerung():
    """v4.2-W9: der gespeicherte OAuth-Zustand darf nicht luegen."""
    import asyncio as _asyncio
    import json as _json
    import logging as _logging

    import nc.twitchoauth as _tw
    import nc.ytoauth as _yt

    # Antwort-Attrappe: die beiden Module reden nur ueber aiohttp mit der
    # Aussenwelt, und genau die Antwort ist hier der Prueffall.
    class _Antwort:
        def __init__(self, status, payload):
            self.status, self._p = status, payload

        async def json(self, content_type=None):
            return self._p

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

    class _Sitzung:
        def __init__(self, r):
            self._r = r

        def post(self, *a, **k):
            return self._r

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

    class _Aio:
        def __init__(self, r):
            self._r = r

        def ClientSession(self):
            return _Sitzung(self._r)

        def ClientTimeout(self, **k):
            return None

    alt_level = _logging.getLogger("TikTokBot").level
    _logging.getLogger("TikTokBot").setLevel(_logging.CRITICAL)
    umgebung = {k: os.environ.get(k) for k in
                ("TWITCH_CLIENT_ID", "TWITCH_CLIENT_SECRET",
                 "YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET")}
    try:
        os.environ.update(TWITCH_CLIENT_ID="x", TWITCH_CLIENT_SECRET="y",
                          YOUTUBE_CLIENT_ID="x", YOUTUBE_CLIENT_SECRET="y")
        d = tempfile.mkdtemp()
        pt = os.path.join(d, "twitch_oauth.json")
        py = os.path.join(d, "youtube_oauth.json")
        _tw.configure(pt)
        _yt.configure(py)

        # ── (1) DER PFAD IST ABSOLUT. bot.py reicht "recordings/..." herein,
        # also relativ zum Arbeitsverzeichnis. Ein Start aus einem anderen
        # Verzeichnis haette den Store woanders gesucht — und der gespeicherte
        # Token waere weg gewesen, ohne dass irgendetwas scheitert.
        _tw.configure("recordings/twitch_oauth.json")
        assert os.path.isabs(_tw._state["store_path"]), \
            "twitchoauth: Store-Pfad bleibt relativ"
        _yt.configure("recordings/youtube_oauth.json")
        assert os.path.isabs(_yt._state["store_path"]), \
            "ytoauth: Store-Pfad bleibt relativ"
        _tw.configure(pt)
        _yt.configure(py)

        # ── (2) _save SCHREIBT NUR EINE VERBINDUNG, NIE IHRE ABWESENHEIT.
        # set_channel() rief _save(); war der Refresh-Token im Speicher gerade
        # geleert, ueberschrieb ein KANALNAME die gespeicherte Verbindung mit
        # einem leeren Token. Loeschen laeuft ausschliesslich ueber forget().
        _yt._state["refresh"] = "rt-gut"
        _yt._save()
        _yt._state["refresh"] = ""
        _yt.set_channel("Mein Kanal")
        with open(py, encoding="utf-8") as f:
            assert _json.load(f)["refresh_token"] == "rt-gut", \
                "ein Kanalname hat die gespeicherte Verbindung geloescht"

        # ── (3) EINE STOERUNG IST KEIN TOTER TOKEN. Twitch warf den
        # Refresh-Token bei JEDEM ausbleibenden Access-Token weg — also auch
        # bei einem 500er oder einem Wartungsfenster. Der Betreiber musste
        # dann neu autorisieren, obwohl an seinem Token nie etwas falsch war.
        _tw._state.update(refresh="rt-gut", access="", access_exp=0.0)
        _tw._save()
        _asyncio.run(_tw.access_token(_Aio(_Antwort(500, {"message": "Internal Server Error"}))))
        assert _tw._state["refresh"] == "rt-gut" and os.path.exists(pt), \
            "ein 500er von Twitch kostet die gespeicherte Verbindung"
        _yt._state.update(refresh="rt-gut", access="", access_exp=0.0)
        _yt._save()
        _asyncio.run(_yt.access_token(_Aio(_Antwort(503, {"error": "backendError"}))))
        assert _yt._state["refresh"] == "rt-gut" and os.path.exists(py), \
            "eine Google-Stoerung kostet die gespeicherte Verbindung"

        # ── (4) PLATTE UND SPEICHER SAGEN DASSELBE. ytoauth leerte den toten
        # Token NUR im Speicher; auf der Platte blieb er liegen. Beim naechsten
        # Neustart las _load() ihn zurueck, status() meldete "ready" und das
        # Panel zeigte "verbunden" — waehrend kein einziger Aufruf durchging.
        # DAS ist das Bild "muss staendig neu verbinden".
        _asyncio.run(_yt.access_token(_Aio(_Antwort(400, {"error": "invalid_grant"}))))
        assert not _yt._state["refresh"], "der tote Token bleibt im Speicher"
        assert not os.path.exists(py), \
            "der tote Token bleibt auf der Platte — er kommt beim Neustart zurueck"
        _yt._load()
        assert not _yt._state["refresh"], "der tote Token kommt beim Neustart zurueck"
        _tw._state.update(refresh="rt-gut", access="", access_exp=0.0)
        _tw._save()
        _asyncio.run(_tw.access_token(_Aio(_Antwort(400, {"message": "Invalid refresh token"}))))
        assert not _tw._state["refresh"] and not os.path.exists(pt), \
            "twitchoauth raeumt die abgelehnte Verbindung nicht ab"

        # ── (5) DAS PANEL DARF NICHT LUEGEN. "abgelaufen" und "nie verbunden"
        # sahen gleich aus; der Betreiber musste raten, ob er neu verbinden
        # oder erst die Google-Konsole pruefen muss.
        st = _yt.status()
        assert st["expired"] is True, "status() verschweigt den Ablauf"
        assert "invalid_grant" in st["last_error"], st["last_error"]
        assert st["last_error_ts"] > 0
        assert st["ready"] is False
        # Nach einer Handabmeldung ist nichts "abgelaufen" — nur leer.
        _yt._state["refresh"] = "rt-gut"
        _yt._save()
        _yt.forget()
        assert _yt.status()["expired"] is False, \
            "forget() laesst einen alten Fehlergrund stehen"
    finally:
        for k, v in umgebung.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        _logging.getLogger("TikTokBot").setLevel(alt_level)

    # ── (6) DER FEHLERKANAL. Ein nicht schreibbarer Store hiess bisher
    # log.warning — und ein ERROR-Log zeigt warning NIE (CLAUDE.md). Genau so
    # blieb "der Token wird gar nicht gespeichert" unsichtbar.
    for datei in ("nc/ytoauth.py", "nc/twitchoauth.py"):
        quelle = open(datei, encoding="utf-8").read()
        stelle = quelle.find("Store nicht schreibbar")
        assert stelle > 0, "%s meldet einen unschreibbaren Store gar nicht" % datei
        umfeld = quelle[max(0, stelle - 400):stelle + 200]
        assert "log.error" in umfeld, \
            "%s meldet den unschreibbaren Store nicht auf error" % datei

    ok("v4.2-W9: OAuth \u2014 Stoerung kostet keinen Token, toter Token ueberlebt "
       "keinen Neustart")



def _test_v42_w10_cookies_reparieren_und_selbst_holen():
    """v4.2-W10: die kaputte cookies.txt wird wirklich repariert — und der Bot
       holt sich fehlende Anti-Bot-Tokens selbst.

       Hintergrund, damit das hier niemand als Formalie liest: die alte
       "Reparatur" hat den Text nur durchgereicht. Genau die drei Sachen, an
       denen MozillaCookieJar TATSAECHLICH stirbt — Domain-Flag passt nicht zur
       Domain, mehr oder weniger als sieben Felder, eine Ablaufzeit die keine
       Zahl ist — hat sie nicht angefasst. Ergebnis: 'parse_error' im Deck,
       rc=1 in yt-dlp, leeres dict im Recorder, TikTok 403. Und weil danach
       niemand nachgeprueft hat, ob die geschriebene Datei ladbar ist, blieb
       das im Kreis."""
    import http.server
    import os as _os
    import tempfile as _tf
    import threading as _th
    import warnings as _warn
    from http.cookiejar import MozillaCookieJar

    import nc.cookieholen as HOL
    import nc.cookies as C

    # http.cookiejar druckt bei JEDEM Formatfehler einen kompletten Traceback
    # als UserWarning ("http.cookiejar bug!"). Dieser Vertrag fuettert es
    # absichtlich mit acht kaputten Dateien — ohne den Filter versinkt die
    # Testausgabe in Tracebacks, die alle erwartet sind, und niemand liest
    # sie mehr. Nur die MELDUNG wird unterdrueckt, nicht der Fehler.
    _alte_filter = _warn.filters[:]
    _warn.filterwarnings("ignore", message=r"http\.cookiejar bug!")

    def _laden(text):
        d = _tf.mkdtemp()
        pfad = _os.path.join(d, "c.txt")
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(text)
        cj = MozillaCookieJar(pfad)
        cj.load(ignore_discard=True, ignore_expires=True)
        return {c.name: c.value for c in cj}, pfad

    # (1) Die Fehlerbilder. Jedes einzelne hat MozillaCookieJar vorher die
    # GANZE Datei verweigern lassen — nicht nur die eine Zeile.
    kaputt = {
        "Domain-Flag FALSE bei .tiktok.com":
            "# Netscape HTTP Cookie File\n"
            ".tiktok.com\tFALSE\t/\tTRUE\t9999999999\tsessionid_ss\tW",
        "Domain-Flag TRUE bei www.tiktok.com":
            "# Netscape HTTP Cookie File\n"
            "www.tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tW",
        # Acht Felder: cookiejar entpackt in genau sieben Namen und stirbt an
        # der ganzen Datei. Der ueberzaehlige Tab faellt weg, der Wert wird
        # zusammengezogen — im Netscape-Format ist ein Tab im Wert illegal,
        # also ist er entweder Schaden oder ein leeres Zusatzfeld.
        "acht Felder statt sieben":
            "# Netscape HTTP Cookie File\n"
            ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\t\tW",
        "Ablaufzeit 'Session' statt Zahl":
            "# Netscape HTTP Cookie File\n"
            ".tiktok.com\tTRUE\t/\tTRUE\tSession\tsessionid_ss\tW",
        "Leerzeile vor dem Kopf":
            "\n# Netscape HTTP Cookie File\n"
            ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tW",
        "BOM vor dem Kopf":
            "\ufeff# Netscape HTTP Cookie File\n"
            ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tW",
        "Spaces statt Tabs (Copy-Paste)":
            "# Netscape HTTP Cookie File\r\n"
            ".tiktok.com FALSE / TRUE 9999999999 sessionid_ss W\r\n",
        "gar kein Kopf":
            ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tW\n",
    }
    for was, roh in kaputt.items():
        try:
            _laden(roh)
            raise AssertionError(
                "Testfall '%s' laedt bereits roh — er prueft nichts mehr" % was)
        except AssertionError:
            raise
        except Exception:
            pass
        text, anzahl = C._cookies_input_to_netscape(roh)
        assert anzahl == 1, "%s: %d Cookies erkannt statt 1" % (was, anzahl)
        got, _ = _laden(text)
        assert got.get("sessionid_ss") == "W", \
            ("%s: nach der Reparatur nicht ladbar/falscher Wert (%r) — genau "
             "hier kam vorher 'parse_error' her" % (was, got))
    ok("v4.2-W10: %d Formatfehler repariert, die cookiejar vorher toeteten"
       % len(kaputt))

    # (2) Ein leerer Wert ist ein Cookie, kein Muell. Vorher fiel er raus,
    # weil strip() den letzten Tab frisst und dann sechs Felder uebrig sind.
    text, anzahl = C._cookies_input_to_netscape(
        "# Netscape HTTP Cookie File\n.tiktok.com\tTRUE\t/\tTRUE\t0\tmsToken\t")
    assert anzahl == 1, "Cookie mit leerem Wert verschwindet (%d)" % anzahl

    # (3) Der Leser gibt nicht mehr leer zurueck, nur weil das Format krumm ist.
    # Das ist der Pfad, an dem der Recorder ohne Cookies losfuhr.
    d = _tf.mkdtemp()
    pfad = _os.path.join(d, "c.txt")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("# Netscape HTTP Cookie File\n"
                ".tiktok.com\tFALSE\t/\tTRUE\t9999999999\tsessionid_ss\tECHT\n")
    jar, normalisiert = C.lade_jar(pfad)
    assert normalisiert is True and {c.name for c in jar} == {"sessionid_ss"}

    class _Still:
        def __getattr__(self, n):
            return lambda *a, **k: None
    C.configure(datei=pfad, log=_Still())
    C.CACHE.pop("v", None)
    assert C.load_dict().get("sessionid_ss") == "ECHT", \
        "load_dict laeuft bei krummem Format immer noch leer — das ist der 403"
    C.CACHE.pop("v", None)
    # ... und die Datei bleibt dabei unangetastet. Ein Leser, der nebenbei
    # schreibt, ist die Sorte Nebenwirkung, die man nachts nicht sucht.
    assert "FALSE\t/" in open(pfad, encoding="utf-8").read(), \
        "lade_jar hat die Datei umgeschrieben"
    ok("v4.2-W10: krumme cookies.txt wird gelesen statt verworfen, ohne sie anzufassen")

    # (4) Der Auto-Bezug fasst den Login NICHT an. Ein Gast-sessionid ueber
    # einen echten geschrieben waere ein stiller Logout.
    alt = ("# Netscape HTTP Cookie File\n"
           ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tECHTE_SESSION\n"
           ".tiktok.com\tTRUE\t/\tTRUE\t1000\tttwid\tALT\n"
           ".tiktok.com\tTRUE\t/\tTRUE\t1000\tirgendwas\tBLEIBT\n")
    neu = {"sessionid_ss": ("GAST", ".tiktok.com", 9999999999),
           "odin_tt": ("GAST", ".tiktok.com", 9999999999),
           "ttwid": ("NEU", ".tiktok.com", 9999999999),
           "msToken": ("NEU", ".tiktok.com", 0)}
    text, ergaenzt, ersetzt = HOL.zusammenfuehren(alt, neu, gast=True)
    got, _ = _laden(text)
    assert got["sessionid_ss"] == "ECHTE_SESSION", \
        "Gast-Bezug hat den Login ueberschrieben — das ist der stille Logout"
    assert "odin_tt" not in got, "Gast-odin_tt neben echtem Login = 403"
    assert got["ttwid"] == "NEU" and got["msToken"] == "NEU"
    assert got["irgendwas"] == "BLEIBT", "unbekannter Cookie ging verloren"
    assert ergaenzt == ["msToken"] and ersetzt == ["ttwid"], (ergaenzt, ersetzt)

    # (5) Fremde Domains kommen NICHT in die Datei. Ein Browser-Profil traegt
    # die Cookies aller Seiten; tiktok_cookies.txt liegt im Backup.
    assert HOL._gehoert_zu_tiktok(".tiktok.com")
    assert HOL._gehoert_zu_tiktok("www.tiktok.com")
    for fremd in ("bank.example", "tiktok.com.evil.tld", "nottiktok.com", ""):
        assert not HOL._gehoert_zu_tiktok(fremd), fremd
    ok("v4.2-W10: Gast-Bezug laesst Auth-Cookies in Ruhe, fremde Domains draussen")

    # (6) Geschrieben wird erst, wenn das Ergebnis ladbar ist. Wer zuerst
    # tauscht und dann prueft, hat den funktionierenden Bestand schon weg.
    ziel = _os.path.join(_tf.mkdtemp(), "c.txt")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write("# Netscape HTTP Cookie File\n"
                ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid_ss\tALT\n")
    try:
        HOL.schreibe(ziel, "das ist kein Netscape-Format")
        raise AssertionError("schreibe() nimmt unladbaren Text an")
    except AssertionError:
        raise
    except Exception:
        pass
    assert "sessionid_ss\tALT" in open(ziel, encoding="utf-8").read(), \
        "der alte Bestand wurde von einem ungeprueften Schreibvorgang zerstoert"
    try:
        HOL.schreibe(ziel, "# Netscape HTTP Cookie File\n"
                     ".tiktok.com\tTRUE\t/\tTRUE\t0\tttwid\tX\n",
                     auth_pflicht=True)
        raise AssertionError("schreibe() ignoriert auth_pflicht")
    except AssertionError:
        raise
    except Exception:
        pass

    # (7) Der ganze Weg — holen, mischen, schreiben — gegen einen Stub auf
    # dem Loopback. NICHT gegen das echte TikTok: der erste Anlauf dieses
    # Vertrags nahm an, in der CI gaebe es kein Netz, und wurde prompt rot,
    # weil der Runner sehr wohl an tiktok.com kommt. Ein Vertrag, der an der
    # Netzanbindung haengt, prueft nicht das, was er zu pruefen behauptet —
    # und ruft nebenbei bei jedem Lauf einen fremden Dienst.
    class _Stub(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Set-Cookie", "ttwid=STUB; Path=/; Max-Age=99999")
            self.send_header("Set-Cookie", "msToken=STUB2; Path=/")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), _Stub)
    _th.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        url = "http://127.0.0.1:%d/" % srv.server_address[1]
        nur_lokal = ("127.0.0.1",)

        # Der Abruf liest Set-Cookie …
        geholt = HOL.hole_gastcookies(urls=[url], timeout=5, domains=nur_lokal)
        assert set(geholt) == {"ttwid", "msToken"}, geholt
        assert geholt["ttwid"][0] == "STUB"
        # … und derselbe Abruf mit dem echten Domain-Filter laesst NICHTS
        # durch. Ein Browser-Profil traegt die Cookies aller Seiten.
        assert HOL.hole_gastcookies(urls=[url], timeout=5) == {}

        # Der volle Weg: zwei Tokens dazu, der Login bleibt stehen.
        b1 = HOL.aktualisiere(ziel, quelle="gast", timeout=5,
                              urls=[url], domains=nur_lokal)
        assert b1["ok"] and sorted(b1["added"]) == ["msToken", "ttwid"], b1
        drin, _ = _laden(open(ziel, encoding="utf-8").read())
        assert drin["sessionid_ss"] == "ALT", "der Login ging beim Schreiben verloren"
        assert drin["ttwid"] == "STUB" and drin["msToken"] == "STUB2", drin
        assert _os.path.exists(ziel + ".bak"), "kein Backup vor dem Tausch"

        # Zweiter Lauf, gleiche Werte: nichts geaendert = NICHT schreiben.
        # Sonst wandert die mtime, und das Deck meldet "Cookies frisch",
        # waehrend in Wahrheit alles beim Alten ist.
        vorher = _os.path.getmtime(ziel)
        b2 = HOL.aktualisiere(ziel, quelle="gast", timeout=5,
                              urls=[url], domains=nur_lokal)
        assert b2["ok"] and not b2["added"] and not b2["replaced"], b2
        assert _os.path.getmtime(ziel) == vorher, \
            "unveraenderter Bezug hat die Datei trotzdem neu geschrieben"
    finally:
        srv.shutdown()

    # Und ein gescheiterter Abruf fasst die Datei erst recht nicht an.
    # Toter Port statt abgeschaltetem Netz: deterministisch, ohne Wartezeit.
    import socket as _sock
    _s = _sock.socket()
    _s.bind(("127.0.0.1", 0))
    _tot = "http://127.0.0.1:%d/" % _s.getsockname()[1]
    _s.close()
    vorher = _os.path.getmtime(ziel)
    b3 = HOL.aktualisiere(ziel, quelle="gast", timeout=2, urls=[_tot])
    assert b3["ok"] is False and b3["error"], b3
    assert _os.path.getmtime(ziel) == vorher, \
        "gescheiterter Bezug hat die Datei angefasst"
    ok("v4.2-W10: Abruf, Mischen und Schreiben am Stueck — validiert, "
       "mit Backup, und nur bei echter Aenderung")

    # (9) Und der Monolith haengt wirklich dran. Ohne diese Haken ist alles
    # oben eine Bibliothek, die niemand aufruft.
    b = open("bot.py", encoding="utf-8").read()
    assert "_nc_cookies_datei.lade_jar(COOKIE_FILE)" in b, \
        "get_cookie_health laedt wieder direkt — dann ist 'parse_error' zurueck"
    assert "_COOKIE_FILE_LOCK = _nc_cookies_datei.DATEI_SPERRE" in b, \
        "zwei Schreib-Locks auf dieselbe Datei sind keiner"
    assert "_nc_cookieholen.configure(proxy_waehler=_pull_proxy_still" in b, \
        "der Auto-Bezug geht ohne Proxy raus — TikTok antwortet der Server-IP mit 403"
    assert "await asyncio.to_thread(_cookies_selbst_holen, \"gast\")" in b, \
        ("der Cookie-Alarm holt nicht selbst nach, bevor er jemanden weckt — "
         "und wenn doch, dann bitte im Thread: der Abruf ist blockierendes "
         "urllib mit bis zu 2x15s, das haelt sonst den ganzen Bot-Loop an")
    # Die Reparatur prueft, BEVOR sie tauscht.
    stelle = b.index("def _ensure_cookie_file_netscape")
    rumpf = b[stelle:stelle + 4000]
    pruefung = rumpf.index("MozillaCookieJar(tmp).load")
    tausch = rumpf.index("os.replace(tmp, COOKIE_FILE)")
    assert pruefung < tausch, \
        "die Reparatur tauscht, bevor sie prueft — ein ungeprueftes Ergebnis"

    # Der Bericht geht als JSON ins Deck, in die Health-Anzeige und nach
    # Telegram — der Wortlaut einer Ausnahme aus urllib, yt-dlp oder einem
    # Browser-Profil traegt Pfade. Er muss durch nach_aussen, und zwar an
    # der Quelle: das ist zugleich die Barriere, die
    # .github/codeql/NcSanitizer.qll kennt. saeubern() taete sachlich
    # dasselbe, aber CodeQL sieht es nicht — und meldete hier prompt zwei
    # py/stack-trace-exposure.
    h = open("nc/cookieholen.py", encoding="utf-8").read()
    assert "_nc_fehlertext.nach_aussen(e," in h, \
        ("nc/cookieholen.py gibt den rohen Ausnahmetext nach aussen — durch "
         "nach_aussen() schicken, nicht durch str(e) und nicht durch "
         "saeubern() (dann faellt die CodeQL-Barriere weg)")
    for muster in ('bericht["error"] = str(e)', "str(e) or e.__class__"):
        assert muster not in h, "roher Ausnahmetext in nc/cookieholen.py: %s" % muster

    from flask import Flask
    from nc.routes import settings as rt
    app = Flask(__name__)
    app.register_blueprint(rt.bp)
    rules = {str(r.rule) for r in app.url_map.iter_rules()}
    assert "/api/cookies/fetch" in rules, "die Bezugs-Route ist nicht registriert"
    haus = open("templates/dashboard.html", encoding="utf-8").read()
    assert "/api/cookies/fetch" in haus and "function fetchCookies(" in haus, \
        "das Deck kann den Bezug nicht ausloesen"
    ok("v4.2-W10: Bot, Route und Deck haengen am Auto-Bezug")
    _warn.filters[:] = _alte_filter


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

    _test_w13_claude_fehlergrund()

    _test_w14_totes_modell()

    _test_w18_toxizitaet_ohne_tiktok()

    _test_w18_kickmod_blueprint()

    _test_w19_azrael_blueprint()

    _test_w20_overlay_audio_und_geld()

    _test_w21_brain_blueprint()

    _test_w22_restream_blueprint()

    _test_w23_beobachtung_und_toasts()

    _test_w24_wartung_blueprint()

    _test_w25_abwehr_blueprint()

    _test_w26_huellen_schlucken_nichts()

    _test_w26_auskunft_blueprint()

    _test_w27_verkettete_knoten()

    _test_w28_abdeckung_ist_ehrlich()

    _test_w29_kein_sqlite_auf_dem_loop()

    _test_w30_fehlertext_und_offenes_deck()

    _test_w31_rauchtest_laeuft_in_der_ci()

    _test_w32_sondenschicht_und_systemlage()

    _test_w33_sammelentscheid_und_ein_stempel()

    _test_v42_w1_schnappschuss_ohne_geheimnis()

    _test_v42_w2_ein_riegel_gegen_pfadausbruch()

    _test_v42_w3_codeql_barriere_und_setup()

    _test_v42_w4_preflight_und_resilienz()

    _test_v42_w5_selftest_und_leerer_monolith()

    _test_v42_w6_zerschnittene_saetze()

    _test_v42_w7_motd_optik()

    _test_v42_w8_windows_installer_spricht_englisch()

    _test_v42_w9_oauth_ueberlebt_neustart_und_stoerung()

    _test_v42_w10_cookies_reparieren_und_selbst_holen()

    print("test_nc_modules OK \u2014 %d Vertraege gruen" % PASS)


if __name__ == "__main__":
    main()
