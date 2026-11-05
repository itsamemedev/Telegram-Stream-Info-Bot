#!/usr/bin/env python3
"""tools/zu_mariadb.py — die SQLite-Datenbank nach MariaDB umziehen (v4.2-W143).

    venv/bin/python tools/zu_mariadb.py --dry-run     pruefen: Quelle ok, Ziel erreichbar und leer
    venv/bin/python tools/zu_mariadb.py               umziehen, nachzaehlen, .env umstellen

Vorher den Dienst stoppen — was der Bot nach dem Export noch in die SQLite-Datei
schreibt, fehlt sonst in MariaDB. `bash tools/update.sh` fuehrt durch alles:
Server, Datenbank und Nutzer anlegen, Dienst stoppen, umziehen, neu starten.

Zugangsdaten kommen aus der .env (MARIADB_HOST/PORT/DB/USER/PASSWORD) oder aus
den Schaltern; das Passwort nie auf der Kommandozeile (es stuende in der
Prozessliste), sondern aus der .env oder der Umgebungsvariable
NC_MARIADB_PASSWORD.

Was dabei garantiert ist (nc/mariadbumzug.py):
  * die SQLite-Datei wird nur gelesen — der Rueckweg ist DB_BACKEND=sqlite;
  * ein nicht leeres Ziel wird nicht ueberschrieben;
  * die .env wird nur umgestellt, wenn JEDE Tabelle nachgezaehlt stimmt —
    vorher entsteht .env.vor-mariadb-<zeit>.

Exitcodes: 0 umgezogen (oder Trockenlauf ok, oder schon auf MariaDB),
           1 abgebrochen (Grund und Abhilfe stehen da), 2 Aufruf-/Umgebungsfehler.
"""
import argparse
import logging
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WURZEL)

from nc import mariadbumzug as U  # noqa: E402


def _env_lesen(pfad):
    """Die .env LESEN, nicht ausfuehren — sie traegt beliebige Werte."""
    werte = {}
    if not os.path.isfile(pfad):
        return werte
    with open(pfad, encoding="utf-8") as fh:
        for z in fh:
            z = z.strip()
            if not z or z.startswith("#") or "=" not in z:
                continue
            k, v = z.split("=", 1)
            werte[k.strip()] = v.split(" #", 1)[0].strip().strip('"').strip("'")
    return werte


def main(argv=None):
    ap = argparse.ArgumentParser(description="SQLite → MariaDB umziehen")
    ap.add_argument("--dir", default=WURZEL, help="Installation (Vorgabe: Ordner ueber tools/)")
    ap.add_argument("--host")
    ap.add_argument("--port", type=int)
    ap.add_argument("--db")
    ap.add_argument("--user")
    ap.add_argument("--dry-run", action="store_true", help="nur pruefen, nichts schreiben")
    ap.add_argument("--auslassen", default="", help="Tabellen, kommagetrennt, bewusst weglassen")
    ap.add_argument("--trotzdem", action="store_true",
                    help="auch umziehen, wenn die SQLite-Datei gerade geschrieben wurde")
    a = ap.parse_args(argv)

    envpfad = os.path.join(a.dir, ".env")
    env = _env_lesen(envpfad)
    if (env.get("DB_BACKEND") or "").lower() == "mariadb":
        print("DB_BACKEND steht schon auf mariadb — nichts zu tun.")
        return 0
    if not os.path.isfile(envpfad):
        print("Keine .env unter %s — erst tools/installer.sh." % a.dir, file=sys.stderr)
        return 2
    sqlite_pfad = env.get("DB_PATH") or "tiktok_bot.db"
    if not os.path.isabs(sqlite_pfad):
        sqlite_pfad = os.path.join(a.dir, sqlite_pfad)
    ziel = {
        "host": a.host or env.get("MARIADB_HOST") or "127.0.0.1",
        "port": a.port or int(env.get("MARIADB_PORT") or 3306),
        "db": a.db or env.get("MARIADB_DB") or "nightcrawler",
        "user": a.user or env.get("MARIADB_USER") or "nightcrawler",
        "password": os.environ.get("NC_MARIADB_PASSWORD") or env.get("MARIADB_PASSWORD") or "",
    }
    if not ziel["password"]:
        print("Kein Passwort — MARIADB_PASSWORD in die .env oder NC_MARIADB_PASSWORD "
              "setzen (bash tools/update.sh erzeugt eins).", file=sys.stderr)
        return 2
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    log = logging.getLogger("TikTokBot")
    print("Ziel: mariadb://%s@%s:%s/%s" % (ziel["user"], ziel["host"], ziel["port"], ziel["db"]))
    try:
        U.umziehen(sqlite_pfad=sqlite_pfad, mariadb=ziel, log=log,
                   auslassen=[t for t in a.auslassen.split(",") if t.strip()],
                   trotzdem_aktiv=a.trotzdem, trocken=a.dry_run)
    except U.UmzugAbgebrochen as e:
        print("ABGEBROCHEN: %s" % e, file=sys.stderr)
        return 1
    if a.dry_run:
        return 0
    sicherung = U.env_setzen(envpfad, {
        "DB_BACKEND": "mariadb", "MARIADB_HOST": ziel["host"], "MARIADB_PORT": ziel["port"],
        "MARIADB_DB": ziel["db"], "MARIADB_USER": ziel["user"],
        "MARIADB_PASSWORD": ziel["password"]})
    print(".env umgestellt auf DB_BACKEND=mariadb (vorher gesichert: %s)." % os.path.basename(sicherung))
    print("Die SQLite-Datei bleibt unveraendert liegen — Rueckweg: DB_BACKEND=sqlite in der .env.")
    print("Jetzt den Dienst starten; erst dann laeuft der Bot auf MariaDB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
