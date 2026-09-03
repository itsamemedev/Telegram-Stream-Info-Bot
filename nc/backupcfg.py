"""nc.backupcfg — v4.1-W24: Sicherung und Aufbewahrung, an einer Stelle.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die zehn Wartungsrouten (`/api/storage`, `/api/retention`, `/api/backup`,
`/api/auto-archive-rules`) lesen fünfzehn .env-Werte des Monolithen. Als
nc.ctx-Einträge wären das fünfzehn der 25 vertraglichen Plätze — bei 24
belegten unmöglich. Dieselbe Auflösung wie in nc/restreamcfg.py (W22): erst
die Datenschicht herauslösen, dann kostet die Route nichts.

**Gelesen wird bei JEDEM Aufruf, nie als Modul-Konstante** (CLAUDE.md). Hier
ist das nicht nur Formsache: der Betreiber schaltet `LOCAL_BACKUP` oder
`SYS_BACKUP` im laufenden Betrieb um und erwartet, dass die nächste Sicherung
das sieht. Eine eingefrorene Konstante hätte weiter ins Leere gesichert.

════════════════════════════════════════════════════════════════════════
S3-ZUGANGSDATEN SIND GEHEIMNISSE
════════════════════════════════════════════════════════════════════════
`S3_ACCESS_KEY` und `S3_SECRET_KEY` sind vollwertige Bucket-Zugänge — wer sie
hat, kann lesen, schreiben und löschen. Deshalb dieselbe Trennung wie bei den
Stream-Keys in nc/restreamcfg.py:

* `s3_zugang()` gibt sie heraus und ist **nur für den boto3-Client**.
* Für Anzeige und Diagnose gibt es `s3_konfiguriert()` — ein bool.
  Die Routen benutzen ausschliesslich das.

Die .env-Namen stehen überall WÖRTLICH in `os.getenv(...)`, nie dynamisch
zusammengesetzt: sonst findet tools/gen_env_example.py sie nicht (in W22 fielen
so prompt vierzehn Variablen still aus der Vorlage) und ein `grep S3_BUCKET`
liefe ins Leere.
"""

import os

_WAHR = ("1", "true", "yes", "on", "y")


def _flag(wert) -> bool:
    return (wert or "").strip().lower() in _WAHR


def _zahl(wert, default):
    try:
        return int((wert or "").strip() or default)
    except (TypeError, ValueError):
        return default


# ---- System-Backup (das ganze Verzeichnis, täglich) -------------------------

def sys_backup() -> bool:
    return _flag(os.getenv("SYS_BACKUP", "1"))


def sys_hour() -> int:
    """Volle Stunde in LOKALER Serverzeit, nicht UTC — der Betreiber legt sie
       in die Nacht, und 'Nacht' meint seine."""
    return _zahl(os.getenv("SYS_BACKUP_HOUR", "4"), 4)


def sys_keep() -> int:
    return _zahl(os.getenv("SYS_BACKUP_KEEP", "14"), 14)


def sys_max_file_mb() -> int:
    """Einzeldatei-Limit im Archiv. Ohne das zieht eine einzige grosse
       Aufnahme das Systemarchiv auf Stunden."""
    return _zahl(os.getenv("SYS_BACKUP_MAX_FILE_MB", "256"), 256)


# ---- Lokales Sicherungsziel -------------------------------------------------

def lokal() -> bool:
    return _flag(os.getenv("LOCAL_BACKUP", "0"))


def lokal_dir() -> str:
    return (os.getenv("LOCAL_BACKUP_DIR", "") or "").strip()


# ---- S3 / Backblaze B2 ------------------------------------------------------

def s3() -> bool:
    return _flag(os.getenv("S3_BACKUP", "0"))


def s3_bucket() -> str:
    return (os.getenv("S3_BUCKET", "") or "").strip()


def s3_endpoint() -> str:
    """Leer heisst AWS-Standard. B2 und andere setzen hier ihre Adresse."""
    return (os.getenv("S3_ENDPOINT", "") or "").strip()


def s3_region() -> str:
    return (os.getenv("S3_REGION", "us-east-1") or "us-east-1").strip()


def s3_zugang():
    """Die beiden Zugangsdaten. EINZIGE Funktion hier, die sie herausgibt —
       siehe Modul-Kopf. Nur für den boto3-Client, nie für eine Antwort."""
    return {"access_key": (os.getenv("S3_ACCESS_KEY", "") or "").strip(),
            "secret_key": (os.getenv("S3_SECRET_KEY", "") or "").strip()}


def s3_konfiguriert() -> bool:
    """Für Anzeige und Diagnose: ist S3 vollständig eingerichtet? Gibt keine
       Zugangsdaten heraus."""
    z = s3_zugang()
    return bool(s3() and s3_bucket() and z["access_key"] and z["secret_key"])


# ---- Ist überhaupt ein Ziel da? ---------------------------------------------

def aktiv() -> bool:
    """Mindestens ein Sicherungsziel konfiguriert — lokal oder S3."""
    return bool(lokal() and lokal_dir()) or s3_konfiguriert()


def fehlgrund() -> str:
    """Warum ist kein Ziel da? Der häufigste Support-Fall war 'Backup tut
       nichts' ohne Begründung — dieselbe Überlegung wie bei
       nc.restreamcfg.enabled()."""
    if aktiv():
        return ""
    return ("Kein Backup-Ziel konfiguriert (.env: LOCAL_BACKUP=1 + "
            "LOCAL_BACKUP_DIR und/oder S3_BACKUP=1 + "
            "S3_BUCKET/S3_ACCESS_KEY/S3_SECRET_KEY)")


# ---- Aufbewahrung -----------------------------------------------------------

def retention_days() -> int:
    """Auto-Löschung von Aufnahmen älter als N Tage. 0 = aus, und 0 ist der
       Standard: eine Voreinstellung, die ungefragt löscht, gibt es nicht."""
    return _zahl(os.getenv("RETENTION_DAYS", "0"), 0)


def recordings_retain_days() -> int:
    """Getrennt von RETENTION_DAYS: hiermit räumt der Aufnahme-Pfad selbst
       auf. Beide auf 0 heisst 'nie automatisch löschen'."""
    return _zahl(os.getenv("RECORDINGS_RETAIN_DAYS", "0"), 0)


# ---- Laufzeitzustand des System-Backups (Alias) -----------------------------

# Alias, kein Register: bot.py verändert das Dict nur an Ort und Stelle
# (STATE["running"] = True) und bindet den Namen nie neu. Ein Vertrag hält das
# fest — kippt es, meldet /api/backup/status für immer "läuft nicht", während
# die Sicherung läuft.
STATE = {"running": False, "last_ts": None, "last_file": None,
         "size_mb": None, "files": 0, "error": None}
