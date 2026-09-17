"""nc.archiverules — v4.1-W24: die Auto-Archiv-Regeln, Datenzugriff und Anwendung.

Vier Funktionen, die im Monolithen zwei Aufrufergruppen hatten: die drei
Routen unter `/api/auto-archive-rules` und den Regel-Lauf aus dem
Wartungspfad. Beim Herauslösen der Routen wäre `run_archive_rules` sonst
kopiert worden — eine Funktion, die **Dateien anfasst und Datenbankstände
fortschreibt**, ist der schlechteste Kandidat für ein Duplikat.

Die eigentliche Bedingungsauswertung liegt schon seit W110 in
nc/archive.py (`evaluate_archive_rule`). Dieses Modul klammert sie mit dem
Datenzugriff zusammen.

════════════════════════════════════════════════════════════════════════
KOPIE UND EINTRAG SIND EIN VORGANG — v4.2-W89
════════════════════════════════════════════════════════════════════════
`_archiviere_eine` kopiert erst und schreibt dann die Datenbankzeile. Diese
Reihenfolge ist notwendig — die Zeile traegt die Groesse der Kopie —, und sie
hatte bis W89 einen Dauerschaden im Fehlerfall:

Schlug der INSERT fehl (UNIQUE, Platte voll, Datenbank weg), blieb die Kopie
**ohne Zeile** im Archiv liegen. Beim naechsten Lauf griff dann
`os.path.exists(target)` -> `skipped += 1`. Damit war die Aufnahme **nie
wieder** archivierbar: eine Datei, die es gibt, die in keiner Ansicht
auftaucht und die kein Lauf mehr einsammelt. Der Betreiber sieht nur eine
Regel, die dauerhaft „uebersprungen" meldet, und keinen Grund dafuer.

Deshalb nimmt der Fehlerpfad die Kopie zurueck. Misslingt auch das, ist das
eine ERROR-Zeile mit dem Pfad — dann liegt die Datei wirklich im Weg und muss
von Hand weg, und das muss dastehen, statt in einem `except: pass` zu
verschwinden.

════════════════════════════════════════════════════════════════════════
DER PFAD-RIEGEL
════════════════════════════════════════════════════════════════════════
Bis v4.2-W89 war es `nc.textmore._safe_archive_filename` — ein reiner
Namensfilter, dessen Ergebnis danach per `os.path.join` zusammengesetzt wurde,
ohne den fertigen Pfad noch einmal zu pruefen. Entschaerft war damit nur der
Name, nicht das Ergebnis; ein Symlink im Archivverzeichnis
(`archiv/raus -> /etc`) besteht jede Namenspruefung. Seit W89 laeuft es ueber
`nc.sicherpfad.sicher_join`, den einen Riegel des Bestands: Name bereinigen
UND den fertigen Pfad per `realpath`/`commonpath` gegen das Archiv halten.

**`archive_dir` und `log_event` kommen als Argument herein**, nicht aus einer
Modul-Konstante: das Archivverzeichnis ist eine .env-Einstellung des
Monolithen, und das Ereignisprotokoll kann nur der laufende Bot schreiben.
Ohne `log_event` läuft der Regel-Lauf trotzdem — er protokolliert dann nur
nicht, statt zu scheitern.

Im Fehlertext und im Kommentar steht weiterhin **ARCHIVE_DIR**, obwohl der
Parameter `archive_dir` heisst: der Betreiber sucht die .env-Variable, nicht
den Python-Namen. Ein blindes Umbenennen hätte genau das zerlegt (die Falle
aus W22, dort per ast.parse gefangen).
"""

import json
import logging
import os
import shutil
from datetime import datetime, timezone
from typing import Optional

from nc.archive import add_archive_entry, evaluate_archive_rule
from nc.dbwrap import db_conn
from nc.sicherpfad import sicher_join

log = logging.getLogger("TikTokBot")


def list_archive_rules() -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, name, condition_json, action_json, enabled, "
                "       last_run, last_match_count, created_at "
                "FROM auto_archive_rules ORDER BY id DESC").fetchall()
    except Exception:
        return []

def add_archive_rule(name: str, condition: dict, action: dict) -> Optional[int]:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "INSERT INTO auto_archive_rules "
                "(name, condition_json, action_json, enabled, created_at) "
                "VALUES (?,?,?,1,?)",
                (name[:200],
                 json.dumps(condition, ensure_ascii=False)[:2000],
                 json.dumps(action, ensure_ascii=False)[:2000],
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        log.warning(f"add_archive_rule: {e}")
        return None

def delete_archive_rule(rule_id: int) -> bool:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "DELETE FROM auto_archive_rules WHERE id=?", (rule_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception:
        return False


def _archiviere_eine(src: str, archive_dir: str, rule_name: str,
                     rec_id) -> bool:
    """Eine Aufnahme ins Archiv kopieren UND eintragen. -> archiviert ja/nein

    Steht als eigene Funktion da, weil sie der einzige Teil des Regel-Laufs
    ist, der Dateien anfasst — und weil sie im Fehlerfall aufraeumen muss
    (siehe KOPIE UND EINTRAG SIND EIN VORGANG oben).
    """
    # sicher_join statt join(dir, _safe_archive_filename(...)): bereinigt den
    # Namen UND prueft den fertigen Pfad gegen das Archiv, realpath also auch
    # gegen Symlinks. Wirft ValueError, wenn das Ergebnis ausbrechen wuerde —
    # kein stiller Rueckfall auf einen Ersatzpfad, denn dann schriebe der Lauf
    # in eine Datei, die niemand gemeint hat.
    try:
        target = sicher_join(archive_dir, os.path.basename(src),
                             "aufnahme.bin")
        # Schon eingespielt? Dann NICHT ueberschreiben — copy2 fragt nicht,
        # und der zweite Lauf schriebe jede Archivfassung mit der aktuellen
        # Quelle zu. Der Betreiber merkt das nie, die Datei ist ja da.
        if os.path.exists(target):
            return False
        shutil.copy2(src, target)
    except Exception as e:
        log.warning(f"archive rule '{rule_name}' on rec#{rec_id}: {e}")
        return False

    # Ab hier liegt die Kopie im Archiv. Schlaegt der Eintrag fehl, MUSS sie
    # wieder weg — sonst blockiert sie jeden weiteren Versuch.
    try:
        add_archive_entry(
            filename=os.path.basename(target), filepath=target,
            title=None, notes=f"auto-archive von rule '{rule_name}'",
            size=os.path.getsize(target), mime=None,
            source_url=f"recording/{rec_id}")
        return True
    except Exception as e:
        log.error("archive rule '%s' on rec#%s: Eintrag fehlgeschlagen "
                  "(%s: %s) — die Kopie wird zurueckgenommen, damit der "
                  "naechste Lauf es erneut versucht.",
                  rule_name, rec_id, type(e).__name__, e)
        try:
            os.remove(target)
        except OSError as e2:
            # NICHT still: bleibt die Kopie liegen, ist der Dauerschaden
            # zurueck, gegen den die Ruecknahme gebaut ist.
            log.error("archive rule '%s': die Kopie %s liess sich nicht "
                      "zurueckholen (%s). Sie liegt jetzt ohne Datenbankzeile "
                      "im Archiv und blockiert jeden weiteren Versuch fuer "
                      "rec#%s — von Hand loeschen.",
                      rule_name, target, e2, rec_id)
        return False


def run_archive_rules(rule_id: Optional[int] = None, archive_dir: str = "",
                      log_event=None) -> dict:
    """Wendet eine oder alle aktiven Regeln an. Action: 'copy_to_archive'
       (zur Zeit einzige supported action)."""
    if not archive_dir:
        return {"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}
    rules = list_archive_rules()
    if rule_id is not None:
        rules = [r for r in rules if r["id"] == rule_id]
    if not rules:
        return {"ok": True, "processed": 0, "results": []}
    try:
        with db_conn() as conn:
            recs = conn.execute(
                "SELECT id, username, filepath, file_size, duration_secs, created_at "
                "FROM recordings WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 5000"
            ).fetchall()
    except Exception as e:
        return {"ok": False, "error": str(e)}

    results = []
    for rule in rules:
        if not rule["enabled"]: continue
        try:
            cond = json.loads(rule["condition_json"] or "{}")
            act = json.loads(rule["action_json"] or "{}")
        except Exception:
            continue
        action_kind = (act.get("action") or "").lower()
        matched = []
        archived = 0
        skipped = 0
        for r in recs:
            row_dict = {"id": r["id"], "username": r["username"],
                        "filepath": r["filepath"], "file_size": r["file_size"],
                        "duration_secs": r["duration_secs"]}
            if not evaluate_archive_rule(cond, row_dict):
                continue
            matched.append(r["id"])
            if action_kind != "copy_to_archive":
                continue
            # Copy zu ARCHIVE_DIR — nur wenn noch nicht da
            src = r["filepath"]
            if not src or not os.path.isfile(src):
                skipped += 1; continue
            if _archiviere_eine(src, archive_dir, rule["name"], r["id"]):
                archived += 1
            else:
                skipped += 1
        try:
            with db_conn() as conn:
                conn.execute(
                    "UPDATE auto_archive_rules SET last_run=?, last_match_count=? WHERE id=?",
                    (datetime.now(timezone.utc).isoformat(), len(matched), rule["id"]))
                conn.commit()
        except Exception as e:
            # v4.2-W89: war `except Exception: pass`. `last_run` ist die
            # einzige Spur, dass eine Regel ueberhaupt laeuft; bleibt sie
            # stehen, sieht das Deck eine Regel, die nie gelaufen ist, obwohl
            # sie gerade Dateien kopiert hat. Genau die Verwechslung, die man
            # ohne Logzeile nicht aufloesen kann.
            log.warning("archive rule '%s': last_run liess sich nicht "
                        "fortschreiben (%s: %s) — die Regel LIEF, das Deck "
                        "zeigt sie aber weiter als nie gelaufen.",
                        rule["name"], type(e).__name__, e)
        results.append({
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "matched": len(matched),
            "archived": archived,
            "skipped": skipped,
        })
        # Ohne laufenden Bot gibt es kein Ereignisprotokoll — das ist kein
        # Grund, den Regel-Lauf scheitern zu lassen.
        if log_event:
            log_event("archive.rule.run", "info",
                      f"Rule '{rule['name']}': matched={len(matched)} "
                      f"archived={archived}",
                      {"rule_id": rule["id"], "matched": len(matched),
                       "archived": archived})
    return {"ok": True, "processed": len(results), "results": results}
