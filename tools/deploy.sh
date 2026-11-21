#!/usr/bin/env bash
#
# NIGHTCRAWLER — Auslieferung mit Vorabpruefung.
#
# WARUM ES DAS GIBT
# Der bisherige Weg war: Dienst stoppen, entpacken, Dienst starten. Zwischen
# "stoppen" und "starten" prueft nichts, ob der neue Build ueberhaupt
# importiert. Ein Syntax- oder Importfehler nimmt den Bot herunter, und die
# einzige Rettung ist das Tarball-Backup — bemerkt wird das erst, wenn jemand
# hinschaut. Dieses Skript dreht die Reihenfolge um: erst pruefen, dann
# umschwenken. Der laufende Bot wird nicht angefasst, solange nicht alles
# gruen ist.
#
# BENUTZUNG
#     bash tools/deploy.sh ~/NIGHTCRAWLER_v37_B138.zip
#
# Anpassbar per Umgebungsvariable:
#     BOT_DIR=~/tiktok-bot  SERVICE=tiktok-bot  PORT=8050  bash tools/deploy.sh <zip>
#
# Bricht bei jedem Fehler ab (set -e) und sagt, in welchem Schritt.

set -euo pipefail

ZIP="${1:-}"
BOT_DIR="${BOT_DIR:-$HOME/tiktok-bot}"
SERVICE="${SERVICE:-tiktok-bot}"
PORT="${PORT:-8050}"
STAGING="${STAGING:-${BOT_DIR}.staging}"
PY="${PY:-python3}"

rot()  { printf '\033[31m%s\033[0m\n' "$*"; }
gruen(){ printf '\033[32m%s\033[0m\n' "$*"; }
info() { printf '\033[36m▸ %s\033[0m\n' "$*"; }

schritt=0
kopf() { schritt=$((schritt+1)); printf '\n\033[1m[%d/8] %s\033[0m\n' "$schritt" "$1"; }

abbruch() {
  rot ""
  rot "ABBRUCH in Schritt ${schritt}."
  if [ "${UMGESCHWENKT:-0}" = "1" ]; then
    rot "Der Umschwenk war bereits erfolgt — spiele das Backup zurueck."
    sudo systemctl stop "$SERVICE" || true
    tar xzf "$BACKUP" -C "$BOT_DIR"
    sudo systemctl start "$SERVICE" || true
    rot "Backup zurueckgespielt: $BACKUP"
    rot "Zurueckgespielt sind nur die ersetzten Code-Dateien. Datenbank, Aufnahmen,"
    rot "Cookies und .env standen nie im Backup und sind auf dem Stand von eben."
  else
    gruen "Der laufende Bot wurde NICHT angefasst — er laeuft unveraendert weiter."
  fi
  exit 1
}
trap abbruch ERR

# ── Vorbedingungen ───────────────────────────────────────────────────────
kopf "Vorbedingungen pruefen"
[ -n "$ZIP" ]      || { rot "Kein Archiv angegeben. Aufruf: bash tools/deploy.sh <zip>"; exit 1; }
[ -f "$ZIP" ]      || { rot "Archiv nicht gefunden: $ZIP"; exit 1; }
[ -d "$BOT_DIR" ]  || { rot "Bot-Verzeichnis nicht gefunden: $BOT_DIR (BOT_DIR= setzen)"; exit 1; }
command -v unzip >/dev/null || { rot "unzip fehlt: sudo apt install unzip"; exit 1; }
systemctl list-unit-files | grep -q "^${SERVICE}.service" \
  || { rot "Dienst '${SERVICE}' unbekannt. Finden mit: systemctl list-units | grep -i tiktok"; exit 1; }
info "Archiv:  $ZIP"
info "Ziel:    $BOT_DIR   Dienst: $SERVICE"

# ── Staging ──────────────────────────────────────────────────────────────
kopf "Neuen Build in ein Nebenverzeichnis entpacken"
rm -rf "$STAGING"
mkdir -p "$STAGING"
unzip -q -o "$ZIP" -d "$STAGING"

# Die Liste der Dateien, die der Umschwenk schreibt — und NUR diese sichert
# das Backup. Bis v5.11.4 packte es das ganze BOT_DIR, also auch recordings/,
# die laufende Datenbank samt -wal/-shm, tiktok_cookies.txt und .nc_update.json.
# Brach die Nachkontrolle ab, spielte abbruch() das komplett zurueck: alles,
# was der Bot zwischen Backup und Abbruch geschrieben hatte, war weg, die
# Cookies waren wieder die alten, und eine SQLite-Datei aus einem tar mitten
# im Betrieb ist kein konsistenter Stand. Dazu belegte jede Auslieferung den
# Aufnahmebestand ein zweites Mal auf derselben Platte.
# Ausgeschlossen wird mit DERSELBEN Schutzliste wie in der Update-Funktion
# (nc/updater.is_protected) — zwei Listen fuer denselben Zweck sind in diesem
# Bestand schon dreimal auseinandergelaufen (CLAUDE.md W100). Damit faehrt
# auch website/news.json nicht mehr ueber den Bestand: der News-Agent schreibt
# sie im Betrieb, und das Archiv brachte den Stand des Build-Rechners zurueck.
# Die Liste entsteht VOR der Vorabpruefung: die Suiten legen im Nebenverzeichnis
# eigene Dateien an, und die gehoeren nicht in den Bestand.
LISTE="${STAGING}.liste"
BESTAND_LISTE="${STAGING}.bestand"
"$PY" - "$STAGING" "$BOT_DIR" "$LISTE" "$BESTAND_LISTE" <<'PYEOF'
import os, sys
quelle, ziel, liste, bestand = sys.argv[1:5]
sys.path.insert(0, quelle)
from nc.updater import is_protected
alle, vorhanden = [], []
for wurzel, _dirs, dateien in os.walk(quelle):
    for name in dateien:
        rel = os.path.relpath(os.path.join(wurzel, name), quelle).replace(os.sep, "/")
        if is_protected(rel):
            continue
        alle.append(rel)
        if os.path.lexists(os.path.join(ziel, rel)):
            vorhanden.append(rel)
for pfad, eintraege in ((liste, alle), (bestand, vorhanden)):
    with open(pfad, "wb") as f:
        f.write(b"".join(e.encode("utf-8") + b"\0" for e in sorted(eintraege)))
print("  %d Dateien im Archiv, %d davon ersetzen eine bestehende" % (len(alle), len(vorhanden)))
PYEOF

# ── Backup ───────────────────────────────────────────────────────────────
kopf "Backup anlegen (Rettungsanker, nur die Dateien, die ersetzt werden)"
BACKUP="$HOME/nightcrawler_backup_$(date +%F_%H%M%S).tgz"
tar czf "$BACKUP" -C "$BOT_DIR" --null -T "$BESTAND_LISTE"
gruen "Backup: $BACKUP ($(du -h "$BACKUP" | cut -f1))"
# Der laufende Bestand bleibt unberuehrt. Geprueft wird ausschliesslich hier.
# .env wird BEWUSST NICHT kopiert: test_smoke.py wechselt selbst in ein
# Temp-Verzeichnis und erzwingt DB_BACKEND=sqlite — es braucht keine
# Geheimnisse und fasst die Produktionsdatenbank nicht an.
info "$(find "$STAGING" -name '*.py' | wc -l) Python-Dateien entpackt"

# ── Vorabpruefung ────────────────────────────────────────────────────────
kopf "Vorabpruefung im Nebenverzeichnis (der Bot laeuft weiter)"
cd "$STAGING"

info "py_compile ueber alle Python-Dateien"
find . -name '*.py' -print0 | xargs -0 "$PY" -m py_compile

if "$PY" -c 'import pyflakes' 2>/dev/null; then
  info "pyflakes"
  "$PY" -m pyflakes bot.py brain_bridge.py nc/*.py brain/*.py
else
  info "pyflakes nicht installiert — uebersprungen (pip install pyflakes)"
fi

if "$PY" -c 'import ruff' 2>/dev/null || command -v ruff >/dev/null; then
  info "ruff"
  "$PY" -m ruff check --select F,E9,B --ignore B905 bot.py || \
    ruff check --select F,E9,B --ignore B905 bot.py
else
  info "ruff nicht installiert — uebersprungen"
fi

info "test_smoke.py — fuehrt bot.py wirklich aus"
"$PY" test_smoke.py

info "test_nc_modules.py"
"$PY" test_nc_modules.py

info "test_restream.py"
"$PY" test_restream.py

info "ncpatch check (Templates: doppelte IDs, CSS-Bilanz)"
"$PY" tools/ncpatch.py check

# JavaScript: die Script-Bloecke aus den Templates gegen node pruefen.
if command -v node >/dev/null; then
  info "node --check auf die Script-Bloecke der Templates"
  "$PY" - <<'PYEOF'
import re, subprocess, sys, tempfile, os, glob
fehler = 0
for datei in glob.glob("templates/*.html") + glob.glob("website/*.html"):
    roh = open(datei, encoding="utf-8").read()
    for i, m in enumerate(re.finditer(r"<script([^>]*)>(.*?)</script>", roh, re.S | re.I)):
        attrs, code = m.group(1).lower(), m.group(2)
        # JSON-LD ist JSON, kein JS — als JSON pruefen, nicht mit node --check
        if "ld+json" in attrs or "application/json" in attrs:
            import json
            try:
                json.loads(code)
            except Exception as e:
                print(f"  JSON-LD kaputt in {datei} #{i}: {e}"); fehler += 1
            continue
        if " src=" in attrs:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(code); p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        os.unlink(p)
        if r.returncode:
            print(f"  Syntaxfehler in {datei} Block #{i}:\n{r.stderr.strip()[:400]}")
            fehler += 1
sys.exit(1 if fehler else 0)
PYEOF
else
  rot "  node fehlt — die JS-Bloecke werden NICHT geprueft."
  rot "  Nachholen mit: sudo apt install nodejs"
fi
gruen "Vorabpruefung vollstaendig gruen."

# ── Umschwenken ──────────────────────────────────────────────────────────
kopf "Dienst stoppen und umschwenken"
cd "$HOME"
sudo systemctl stop "$SERVICE"
UMGESCHWENKT=1
# Nur die Dateien aus der Liste (oben). Das Nebenverzeichnis traegt nach der
# Vorabpruefung auch __pycache__/ und was die Suiten dort anlegen; ein
# Kopieren des ganzen Verzeichnisses brachte das mit. Kein --delete: was der
# Bestand zusaetzlich hat, bleibt.
if command -v rsync >/dev/null; then
  rsync -a --from0 --files-from="$LISTE" "$STAGING"/ "$BOT_DIR"/
else
  (cd "$STAGING" && tar cf - --null -T "$LISTE") | (cd "$BOT_DIR" && tar xf -)
fi
gruen "Code uebernommen."

kopf "Dienst starten"
sudo systemctl start "$SERVICE"
sleep 8

# ── Nachkontrolle ────────────────────────────────────────────────────────
kopf "Nachkontrolle: laeuft er wirklich?"
systemctl is-active --quiet "$SERVICE" || {
  rot "Dienst ist nicht aktiv. Letzte Logzeilen:"
  journalctl -u "$SERVICE" -n 40 --no-pager || true
  false
}
gruen "systemd: aktiv"

info "Warte auf das Dashboard (max 60s)"
bereit=0
for _ in $(seq 1 30); do
  if curl -fsS -m 2 -o /dev/null "http://127.0.0.1:${PORT}/" 2>/dev/null; then
    bereit=1; break
  fi
  sleep 2
done
[ "$bereit" = "1" ] || {
  rot "Dashboard antwortet nach 60s nicht auf 127.0.0.1:${PORT}."
  journalctl -u "$SERVICE" -n 40 --no-pager || true
  false
}
gruen "Dashboard antwortet auf 127.0.0.1:${PORT}"

kopf "Selbsttest des laufenden Bots"
# Kein Abbruch mehr — ab hier laeuft der Bot. Das ist eine Meldung, kein Gate.
trap - ERR
URTEIL="$(curl -fsS -m 10 "http://127.0.0.1:${PORT}/api/selftest" 2>/dev/null || true)"
if [ -n "$URTEIL" ]; then
  # Heredoc mit 'PYEOF' in Anfuehrungszeichen: die Shell fasst den Block nicht
  # an, deshalb duerfen hier beliebige Anfuehrungszeichen und $ vorkommen.
  # Das Urteil kommt ueber die UMGEBUNG, nicht ueber eine Pipe. Grund: "python -"
  # liest das PROGRAMM von stdin, und das Heredoc belegt stdin damit bereits —
  # die Pipe lief ins Leere und json.load(sys.stdin) bekam nichts. Aufgefallen
  # ist es nie, weil bei jedem Fehlschlag klaglos der Rueckfall griff und statt
  # des formatierten Urteils rohes JSON zeigte. Genau so sah jede Auslieferung
  # bisher aus.
  URTEIL="$URTEIL" "$PY" - <<'PYEOF' || printf '%s\n' "$URTEIL" | head -c 800
import json, os

d = json.loads(os.environ["URTEIL"])
ZEICHEN = {"rot": "\033[31m✗\033[0m", "gelb": "\033[33m!\033[0m"}
print("  Urteil: %s (%d rot, %d gelb)" % (
    d.get("urteil", "?"), d.get("anzahl_rot", 0), d.get("anzahl_gelb", 0)))
for x in d.get("befunde", []):
    print("  %s [%s] %s" % (ZEICHEN.get(x.get("schwere"), "?"),
                            x.get("bereich", "?"), x.get("befund", "")))
    if x.get("fix"):
        print("      → %s" % x["fix"])
if not d.get("befunde"):
    print("  \033[32mKeine Befunde — der Bot meldet sich gesund.\033[0m")
PYEOF
else
  rot "  /api/selftest antwortet nicht — pruefe das Log manuell."
fi

kopf "Fehlerbild der ersten Minute"
if journalctl -u "$SERVICE" --since '-2min' --no-pager | grep -Ei 'Traceback|CRITICAL|Schleife .* gestoert' | head -20; then
  rot ""
  rot "Es stehen Fehler im Log (oben). Der Bot laeuft, aber sieh sie dir an."
else
  gruen "Keine Tracebacks, keine gestoerten Schleifen."
fi

echo
gruen "════════════════════════════════════════════════════════════"
gruen " Auslieferung abgeschlossen."
gruen "════════════════════════════════════════════════════════════"
echo "  Backup liegt unter : $BACKUP"
echo "  Zurueckrollen      : sudo systemctl stop $SERVICE && \\"
echo "                       tar xzf $BACKUP -C $BOT_DIR && \\"
echo "                       sudo systemctl start $SERVICE"
echo
echo "  Jetzt sinnvoll mitlesen:"
echo "    journalctl -u $SERVICE -f | grep -E 'Kick-Ziel|YouTube-Restream|Schleife'"
rm -rf "$STAGING" "$LISTE" "$BESTAND_LISTE"
