#!/usr/bin/env bash
#
# NIGHTCRAWLER — Nachinstallation und Abgleich (v4.2-W123)
#
#     bash tools/update.sh                  gefuehrt: Systempakete + Python-Pflichtpakete
#     bash tools/update.sh --check          nur pruefen; Exit 1, wenn etwas fehlt
#     bash tools/update.sh --dry-run        zeigen, was liefe — nichts ausfuehren
#     bash tools/update.sh --python-deps --optional --unattended
#     bash tools/update.sh --mariadb        SQLite -> MariaDB umziehen (v4.2-W143)
#     bash tools/update.sh --ik-llama       lokales LLM: llama.cpp -> ik_llama.cpp (v5.1-W181)
#     bash tools/update.sh --mysqlclient    MariaDB: C-Treiber statt PyMySQL (v5.2-W193)
#     bash tools/update.sh --mariadb-konf   MariaDB: eigene Server-Einstellungen (v5.2-W193)
#     bash tools/update.sh --help           alle Schalter
#
# WARUM ES DAS GIBT
# Der Installer ist fuer den ERSTEN Lauf gebaut. Danach gab es fuer die Frage
# "fehlt auf dieser Maschine etwas?" keinen Weg ausser ihn erneut laufen zu
# lassen — mit elf Schritten, .env-Fragen und Dienst-Einrichtung, obwohl nur
# yt-dlp fehlte. Und die Update-Funktion (nc/updater.py) spielt Code ein, aber
# keine Abhaengigkeiten: ein neuer Eintrag in requirements.txt kam damit nie
# auf dem Server an, bis jemand von Hand pip aufrief.
#
# Dieses Skript beantwortet genau diese Frage, und nur sie:
#   * was fehlt (Systemwerkzeuge, Python-Pakete aus requirements.txt),
#   * was es dafuer tun wuerde (der Befehl, woertlich),
#   * und danach, ob es jetzt da ist — gemessen, nicht angenommen.
#
# IDEMPOTENT. Ein zweiter Lauf auf einem vollstaendigen Bestand fuehrt KEINEN
# Installationsbefehl aus. Es installiert nur, was fehlt, und es fasst nie die
# .env, die Datenbank, Aufnahmen oder einen Dienst an. Systempakete werden nie
# aktualisiert, nur ergaenzt — ein Upgrade von ffmpeg mitten im Betrieb ist eine
# Entscheidung des Betreibers, keine Nebenwirkung eines Abgleichs.
#
# EXITCODES — dieselbe Trennung wie bei den Sperren (W83):
#   0  vollstaendig (oder: --dry-run ohne Befund)
#   1  es fehlt etwas — nach --check, oder weil die Installation es nicht
#      geschafft hat
#   2  Aufruf- oder Umgebungsfehler (unbekannter Schalter, kein Python)
#
# Prometheus/Grafana: --observability reicht an tools/observability.sh weiter
# (v4.2-W127) — dasselbe Werkzeug, das der Installer aufruft, mit denselben
# Wie-Schaltern. Eine zweite Einrichtung hier liefe auseinander (W100).

set -euo pipefail

NC_UPDATE_VERSION="1.0"
SKRIPT="$(cd "$(dirname "$0")" && pwd)"

# ── Bibliotheken ─────────────────────────────────────────────
# shellcheck source=lib/i18n.sh
. "$SKRIPT/lib/i18n.sh"
# shellcheck source=lib/ausgabe.sh
. "$SKRIPT/lib/ausgabe.sh"
# shellcheck source=lib/system.sh
. "$SKRIPT/lib/system.sh"

have(){ command -v "$1" >/dev/null 2>&1; }

# ── Schalter ─────────────────────────────────────────────────
NC_MODUS="gefuehrt"
NUR_PRUEFEN=0
TROCKEN=0
UPGRADE=0
W_SYSTEM=0; W_PYTHON=0; W_OPTIONAL=0; W_BEOBACHTUNG=""; W_MARIADB=0; W_IKLLAMA=0
W_MYSQLC=0; W_MKONF=0
ZIEL="$(cd "$SKRIPT/.." && pwd)"

while [ $# -gt 0 ]; do
  case "$1" in
    --express)        NC_MODUS="express";;
    --unattended|-y)  NC_MODUS="unattended";;
    --check)          NUR_PRUEFEN=1;;
    --dry-run)        TROCKEN=1;;
    --upgrade)        UPGRADE=1;;
    --system)         W_SYSTEM=1;;
    --python-deps)    W_PYTHON=1;;
    --optional)       W_PYTHON=1; W_OPTIONAL=1;;
    --all)            W_SYSTEM=1; W_PYTHON=1; W_OPTIONAL=1;;
    --observability)  W_BEOBACHTUNG="--no-grafana";;
    --observability=grafana) W_BEOBACHTUNG="--grafana";;
    --mariadb)        W_MARIADB=1;;
    --ik-llama)       W_IKLLAMA=1;;
    --mysqlclient)    W_MYSQLC=1;;
    --mariadb-konf)   W_MKONF=1;;
    --ik-llama-neu)   W_IKLLAMA=2;;
    --dir)            ZIEL="${2:-}"; shift;;
    --dir=*)          ZIEL="${1#*=}";;
    --pkg)            NC_PKG="${2:-}"; shift;;
    --pkg=*)          NC_PKG="${1#*=}";;
    --no-color)       export NC_FARBE=0; nc_farben;;   # gelesen in lib/ausgabe.sh
    --version)        printf 'NIGHTCRAWLER update %s\n' "$NC_UPDATE_VERSION"; exit 0;;
    --help|-h)
      # tz: zeilenweise uebersetzt (lib/i18n.sh). Die Hilfe ist das Erste,
      # was ein englischer Nutzer sieht.
      tz <<'HILFE'
NIGHTCRAWLER — Nachinstallation und Abgleich

  bash tools/update.sh [Schalter]

Was (ohne Auswahl: --system und --python-deps):
  --system         Systemwerkzeuge: ffmpeg streamlink yt-dlp git curl sqlite3
  --python-deps    Pflichtpakete aus requirements.txt in .venv
  --optional       zusaetzlich die als [optional] markierten Pakete
  --all            alles oben
  --observability  Prometheus einrichten bzw. abgleichen (=grafana: mit Grafana)
  --mariadb        Datenbank von SQLite nach MariaDB umziehen und .env umstellen
  --ik-llama       lokales LLM: altes llama.cpp entfernen, ik_llama.cpp mit Qwen3-14B-Uncensored
  --ik-llama-neu   wie --ik-llama, und ik_llama.cpp neu bauen
  --mysqlclient    MariaDB: C-Treiber mysqlclient einrichten (PyMySQL bleibt Rueckweg)
  --mariadb-konf   MariaDB: skip_name_resolve und Commit-fsync je Sekunde, Server neu starten

Wie:
  --check          nur pruefen und berichten; Exitcode 1, wenn etwas fehlt
  --dry-run        die Befehle zeigen, die liefen — nichts ausfuehren
  --upgrade        Python-Pakete auf die neueste zulaessige Fassung heben
  --express        eine Rueckfrage fuer den ganzen Plan statt einer je Schritt
  --unattended,-y  keine Rueckfragen (fuer Skripte und Zeitplaene)
  --dir <Pfad>     Installation (Vorgabe: der Ordner ueber tools/)
  --pkg <Name>     Paketmanager erzwingen: apt dnf pacman zypper apk brew
  --no-color       ohne Farben

Exitcodes: 0 vollstaendig · 1 es fehlt etwas · 2 Aufruffehler
Systempakete werden nur ergaenzt, nie aktualisiert.
HILFE
      exit 0;;
    *) fehler "Unbekannter Schalter: %s  (--help)" "$1"; exit 2;;
  esac
  shift
done
if [ -n "$W_BEOBACHTUNG" ]; then
  # Weiterreichen, nicht nachbauen: --check, --dry-run und der Modus gelten
  # dort genauso. Ohne weitere Was-Schalter ist das der ganze Lauf.
  _w=("$W_BEOBACHTUNG" --dir "$ZIEL")
  [ "$NUR_PRUEFEN" = 1 ] && _w+=(--check)
  [ "$TROCKEN" = 1 ] && _w+=(--dry-run)
  case "$NC_MODUS" in express) _w+=(--express);; unattended) _w+=(--unattended);; esac
  [ "${NC_FARBE:-1}" = 0 ] && _w+=(--no-color)
  if [ "$W_SYSTEM$W_PYTHON" = "00" ]; then exec bash "$SKRIPT/observability.sh" "${_w[@]}"; fi
  # Zusammen mit anderen Schaltern ZUERST: der Rest dieses Skripts endet an
  # mehreren Stellen vorzeitig (nichts zu tun, --check, --dry-run), und dort
  # waere die Beobachtung still ausgefallen (Codex, PR #166). Ihr Ergebnis
  # zaehlt beim Exitcode mit — ueber die EXIT-Falle, damit jeder Ausgang es
  # sieht und keiner es vergisst.
  OBS_RC=0
  bash "$SKRIPT/observability.sh" "${_w[@]}" || OBS_RC=$?
  # shellcheck disable=SC2154  # _rc entsteht in der Falle selbst
  trap '_rc=$?; if [ "$_rc" = 0 ] && [ "$OBS_RC" != 0 ]; then exit "$OBS_RC"; fi' EXIT
fi
[ "$W_SYSTEM$W_PYTHON" = "00" ] && { W_SYSTEM=1; W_PYTHON=1; }
# Ohne Tastatur gibt es keine Rueckfragen — dann ehrlich unbeaufsichtigt.
[ -z "$NC_TTY" ] && [ "$NC_MODUS" != "unattended" ] && NC_MODUS="unattended"

case "${NC_PKG:-}" in
  ""|apt|dnf|pacman|zypper|apk|brew|keiner) ;;
  *) fehler "Unbekannter Paketmanager: %s (apt dnf pacman zypper apk brew)" "$NC_PKG"; exit 2;;
esac
[ -d "$ZIEL" ] || { fehler "Verzeichnis gibt es nicht: %s" "$ZIEL"; exit 2; }
ZIEL="$(cd "$ZIEL" && pwd)"

# Befehl ausfuehren oder — im Trockenlauf — nur zeigen. EIN Weg fuer beides:
# der Trockenlauf zeigt woertlich, was der echte Lauf ausfuehrt.
lauf(){
  if [ "$TROCKEN" = 1 ]; then
    printf '    %s$%s %s\n' "$FNT" "$R" "$*"
    return 0
  fi
  printf '    %s$ %s%s\n' "$FNT" "$*" "$R"
  "$@"
}

BEFUND=0     # 1, sobald nach allem noch etwas fehlt

# mariadb_umzug -> 0 umgezogen; sonst 1 und der Bot laeuft weiter auf SQLite.
#
# v4.2-W143. Die Reihenfolge ist die Sicherung: erst Server, Datenbank und
# Nutzer, dann den Bot stoppen (was er nach dem Export schriebe, fehlte
# sonst), dann tools/zu_mariadb.py — das zaehlt nach und stellt die .env nur
# bei Gleichstand um. Gestartet wird der Dienst danach IMMER wieder, auch
# nach einem Abbruch: dann eben auf SQLite, unveraendert. Ein Umzug, der den
# Bot gestoppt zuruecklaesst, waere schlimmer als keiner.
# v5.2-W193: C-Treiber fuer MariaDB. Scheitert ein Schritt, bleibt PyMySQL —
# deshalb ist das hier nie ein Grund, den Bot anzuhalten.
mysqlclient_einrichten(){
  local _s=(); [ -n "$SUDO" ] && [ "$SUDO" != "-" ] && _s=("$SUDO")
  abschnitt "mysqlclient"
  local _p; _p="$(nc_mysqlclient_pakete)"
  if [ -n "$_p" ]; then
    # shellcheck disable=SC2046  # Paketliste aus lib/system.sh, feste Woerter
    lauf ${_s[@]+"${_s[@]}"} $(nc_installbefehl "$_p") \
      || { warn "Bau-Pakete fuer mysqlclient liessen sich nicht installieren — PyMySQL bleibt."; return 1; }
  else
    info "Fuer %s sind die Bau-Pakete nicht hinterlegt — falls pip scheitert: MariaDB-C-Header und Compiler von Hand." "${NC_PKG:-?}"
  fi
  lauf "$VPY" -m pip install "mysqlclient>=2.2" \
    || { warn "mysqlclient liess sich nicht bauen — PyMySQL bleibt (laeuft unveraendert)."; return 1; }
  gut "mysqlclient eingerichtet — wirkt nach dem naechsten Neustart des Bots (MARIADB_TREIBER=auto)."
}

# v5.2-W193: eigene Server-Einstellungen. skip_name_resolve nur, wenn das Konto
# des Bots auch fuer 127.0.0.1 existiert — sonst stuende er vor 1045/1130.
mariadb_konf_schreiben(){
  local _s=(); [ -n "$SUDO" ] && [ "$SUDO" != "-" ] && _s=("$SUDO")
  local nu cli skip=1 _tmp
  nu="$(env_wert MARIADB_USER)"; nu="${nu:-nightcrawler}"
  cli="$(command -v mariadb || command -v mysql || printf 'mariadb')"
  abschnitt "MariaDB-Einstellungen"
  [ -n "$MKONF_PFAD" ] || { warn "Kein Konfigurationsverzeichnis gefunden."; return 1; }
  if [ "$TROCKEN" = 0 ] && ! nc_mariadb_tcp_konto "$nu" ${_s[@]+"${_s[@]}"} "$cli"; then
    warn "Nutzer %s hat kein Konto fuer 127.0.0.1 — skip_name_resolve bleibt aus (sonst verweigert MariaDB den Bot). Abhilfe: bash tools/update.sh --mariadb legt die Konten an." "$nu"
    skip=0
  fi
  _tmp="$(mktemp)"; nc_mariadb_konf_text "$skip" "$_tmp"
  if [ -f "$MKONF_PFAD" ] && cmp -s "$_tmp" "$MKONF_PFAD"; then
    rm -f "$_tmp"; gut "Unveraendert: %s" "$MKONF_PFAD"; return 0
  fi
  lauf ${_s[@]+"${_s[@]}"} install -m 644 "$_tmp" "$MKONF_PFAD" \
    || { rm -f "$_tmp"; warn "%s nicht schreibbar." "$MKONF_PFAD"; return 1; }
  rm -f "$_tmp"
  if have systemctl; then
    lauf ${_s[@]+"${_s[@]}"} systemctl restart mariadb \
      || { warn "MariaDB startete nicht neu — %s pruefen, notfalls loeschen und neu starten." "$MKONF_PFAD"; return 1; }
  else
    info "Kein systemd — MariaDB von Hand neu starten, damit %s wirkt." "$MKONF_PFAD"
  fi
  gut "MariaDB-Einstellungen geschrieben: %s" "$MKONF_PFAD"
}

mariadb_umzug(){
  local db nu host port pw cli rc=0 gestoppt=""
  db="$(env_wert MARIADB_DB)"; db="${db:-nightcrawler}"
  nu="$(env_wert MARIADB_USER)"; nu="${nu:-nightcrawler}"
  host="$(env_wert MARIADB_HOST)"; host="${host:-127.0.0.1}"
  port="$(env_wert MARIADB_PORT)"; port="${port:-3306}"
  pw="$(env_wert MARIADB_PASSWORD)"
  if [ -z "$pw" ]; then
    pw="$("${VPY:-python3}" -c 'import secrets;print(secrets.token_urlsafe(24))' 2>/dev/null \
          || python3 -c 'import secrets;print(secrets.token_urlsafe(24))')"
  fi
  local _s=(); [ -n "$SUDO" ] && [ "$SUDO" != "-" ] && _s=("$SUDO")
  abschnitt "MariaDB"
  if ! have mariadb && ! have mysql; then
    # shellcheck disable=SC2046  # Paketliste aus lib/system.sh, feste Woerter
    lauf ${_s[@]+"${_s[@]}"} $(nc_installbefehl "$(nc_paketname mariadb)") \
      || { warn "MariaDB-Server liess sich nicht installieren — Umzug abgebrochen, nichts veraendert."; return 1; }
    if [ "$TROCKEN" = 0 ] && have systemctl; then
      lauf ${_s[@]+"${_s[@]}"} systemctl enable --now mariadb || true
    fi
  fi
  cli="$(command -v mariadb || command -v mysql || printf 'mariadb')"
  if [ "$TROCKEN" = 1 ]; then
    # Das Passwort steht nie in einer Befehlszeile, auch nicht im Trockenlauf.
    printf '    %s$%s nc_mariadb_sql %s %s *** | %s\n' "$FNT" "$R" "$db" "$nu" "$cli"
  elif nc_mariadb_sql "$db" "$nu" "$pw" | ${_s[@]+"${_s[@]}"} "$cli"; then
    gut "Datenbank %s und Nutzer %s angelegt bzw. abgeglichen." "$db" "$nu"
  else
    warn "Datenbank/Nutzer liessen sich nicht anlegen — Umzug abgebrochen, nichts veraendert."
    return 1
  fi
  # PyMySQL VOR dem Stopp: scheitert es, laeuft der Bot unveraendert weiter.
  if [ "$TROCKEN" = 1 ]; then
    { [ -x "$VPY" ] && "$VPY" -c 'import pymysql' 2>/dev/null; } \
      || printf '    %s$%s %s -m pip install PyMySQL>=1.1.1\n' "$FNT" "$R" "$VPY"
  elif ! "$VPY" -c 'import pymysql' 2>/dev/null; then
    lauf "$VPY" -m pip install "PyMySQL>=1.1.1" \
      || { warn "PyMySQL liess sich nicht installieren — Umzug abgebrochen, nichts veraendert."; return 1; }
  fi
  nc_dienst_finden
  if [ -n "$NC_DIENST" ] && systemctl is-active --quiet "$NC_DIENST" 2>/dev/null; then
    if [ "$NC_MODUS" = "gefuehrt" ] && [ "$TROCKEN" = 0 ] && ! frage_ja "Bot-Dienst fuer den Umzug kurz stoppen?" J; then
      info "Umzug uebersprungen — der Bot laeuft weiter auf SQLite."
      return 1
    fi
    lauf ${_s[@]+"${_s[@]}"} systemctl stop "$NC_DIENST" && gestoppt="$NC_DIENST"
  fi
  # Hat dieses Skript den Dienst selbst gestoppt und systemd bestaetigt das,
  # ist das die staerkere Aussage als jede Handle-Suche: mit eingeschraenktem
  # /proc (LXC, hidepid) entschiede zu_mariadb.py sonst nach der
  # Aenderungszeit — und die ist direkt nach dem Stopp frisch (Checkpoint
  # beim Schliessen), der Umzug verweigerte genau den sicheren Fall.
  local _tz=()
  if [ -n "$gestoppt" ] && ! systemctl is-active --quiet "$gestoppt" 2>/dev/null; then
    _tz=(--trotzdem)
  fi
  if [ "$TROCKEN" = 1 ]; then
    printf '    %s$%s NC_MARIADB_PASSWORD=*** %s %s --dir %s\n' "$FNT" "$R" "$VPY" "$SKRIPT/zu_mariadb.py" "$ZIEL"
  else
    printf '    %s$ NC_MARIADB_PASSWORD=*** %s %s --dir %s%s%s\n' "$FNT" "$VPY" "$SKRIPT/zu_mariadb.py" "$ZIEL" "${_tz[*]:+ ${_tz[*]}}" "$R"
    NC_MARIADB_PASSWORD="$pw" "$VPY" "$SKRIPT/zu_mariadb.py" --dir "$ZIEL" \
      --host "$host" --port "$port" --db "$db" --user "$nu" ${_tz[@]+"${_tz[@]}"} || rc=$?
  fi
  if [ -n "$gestoppt" ]; then
    lauf ${_s[@]+"${_s[@]}"} systemctl start "$gestoppt" \
      || warn "Dienst %s liess sich nicht wieder starten — bitte von Hand: systemctl start %s" "$gestoppt" "$gestoppt"
  fi
  if [ "$rc" = 0 ] && [ "$TROCKEN" = 0 ]; then
    gut "Umzug abgeschlossen — der Bot laeuft jetzt auf MariaDB."
  elif [ "$rc" != 0 ]; then
    warn "Umzug abgebrochen (siehe Grund oben) — der Bot laeuft unveraendert auf SQLite."
  fi
  return "$rc"
}

# ═══════════════════════════════════════════════════════════════════════════
kopf "Erkennung"
nc_system_erkennen
info "System:    %s (%s)" "$NC_DISTRO_NAME" "$(uname -m 2>/dev/null || echo '?')"
info "Paketmanager: %s" "$NC_PKG"
info "Installation: %s" "$ZIEL"
case "$NC_MODUS" in
  express)    info "Betriebsart: %s — eine Rueckfrage fuer den ganzen Plan." "express";;
  unattended) info "Betriebsart: %s — keine Rueckfragen." "unattended";;
  *)          info "Betriebsart: %s — Rueckfrage je Schritt. Fuer weniger: --express" "$(t 'gefuehrt')";;
esac
[ "$NUR_PRUEFEN" = 1 ] && info "Nur Pruefung — es wird nichts installiert."
[ "$TROCKEN" = 1 ] && info "Trockenlauf — Befehle werden gezeigt, nicht ausgefuehrt."

SUDO=""
if nc_braucht_root && [ "$(id -u)" -ne 0 ]; then
  if have sudo; then SUDO="sudo"; else SUDO="-"; fi
fi

# ═══════════════════════════════════════════════════════════════════════════
# Systemwerkzeuge
# ═══════════════════════════════════════════════════════════════════════════
WERKZEUGE="ffmpeg streamlink yt-dlp git curl sqlite3"
SYS_FEHLT=""        # Werkzeuge, die fehlen
SYS_PAKETE=""       # Pakete, die der Paketmanager dafuer installiert
PIP_STATT=""        # Werkzeuge ohne Systempaket — pip in .venv ist der Weg
SYS_OHNE=""         # weder Paket noch pip: selbst bereitstellen

if [ "$W_SYSTEM" = 1 ]; then
  kopf "Systemwerkzeuge"
  erklaere "Programme, keine Bibliotheken: ffmpeg nimmt auf und sendet, streamlink und yt-dlp loesen die TikTok-Quelle auf, sqlite3 ist die Kommandozeile zur Datenbank. Vorhandene werden nicht angefasst."
  for w in $WERKZEUGE; do
    # Ein yt-dlp/streamlink im venv zaehlt: der Bot ruft sie von dort, weil
    # .venv/bin im PATH des Dienstes vorn steht.
    if have "$w" || [ -x "$ZIEL/.venv/bin/$w" ]; then
      _wo="$(command -v "$w" 2>/dev/null || printf '%s' "$ZIEL/.venv/bin/$w")"
      gut "%s: %s" "$w" "$_wo"
      continue
    fi
    SYS_FEHLT="$SYS_FEHLT $w"
    _paket=""
    for _k in $(nc_paketname "$w"); do
      # Im Trockenlauf und bei --check wird trotzdem nachgesehen: die Frage
      # an den Paketmanager liest nur, und ohne sie zeigte der Trockenlauf
      # einen Befehl, der so nie liefe.
      if nc_paket_verfuegbar "$_k"; then _paket="$_k"; break; fi
    done
    # Leere Paketlisten sind kein "gibt es nicht". Auf einem frischen Image
    # ohne apt-get update findet apt-cache NICHTS — gemessen in W123: sqlite3
    # galt als "kein Paket fuer apt", obwohl es in jeder Debian-Quelle liegt.
    # Auffrischen ist ein Schreibzugriff und gehoert nicht in --check; also
    # den ersten Kandidaten nehmen und es sagen. Die Nachpruefung am Ende
    # misst, ob er wirklich kam.
    if [ -z "$_paket" ] && [ -n "$(nc_paketname "$w")" ] && nc_quellen_leer; then
      _paket="$(nc_paketname "$w" | cut -d' ' -f1)"
      info "Paketquellen noch nicht aufgefrischt — %s wird beim Installieren geklaert." "$_paket"
    fi
    if [ -n "$_paket" ]; then
      warn "%s fehlt — Paket: %s" "$w" "$_paket"
      SYS_PAKETE="$SYS_PAKETE $_paket"
      [ "$w:$_paket" = "ffmpeg:ffmpeg-free" ] && \
        erklaere "ffmpeg-free ist die Fedora-Fassung ohne x264: Aufnahme geht, Restream mit Umkodierung nicht. Die volle Fassung kommt aus RPM Fusion (rpmfusion.org)."
    else
      case "$w" in
        streamlink|yt-dlp)
          warn "%s fehlt — kein Systempaket, wird per pip in .venv ergaenzt." "$w"
          PIP_STATT="$PIP_STATT $w";;
        *)
          warn "%s fehlt — kein Paket fuer %s gefunden. Bitte selbst bereitstellen." "$w" "$NC_PKG"
          SYS_OHNE="$SYS_OHNE $w";;
      esac
    fi
  done
fi

# ═══════════════════════════════════════════════════════════════════════════
# Python-Pakete
# ═══════════════════════════════════════════════════════════════════════════
VPY="$ZIEL/.venv/bin/python"
REQ="$ZIEL/requirements.txt"
PY_FEHLT=""          # Anforderungen (name+spec), die fehlen oder zu alt sind
PY_VENV_NEU=0

finde_python(){
  local c
  for c in python3.14 python3.13 python3.12 python3; do
    if have "$c" && "$c" -c 'import sys;raise SystemExit(0 if sys.version_info>=(3,12) else 1)' 2>/dev/null; then
      command -v "$c"; return 0
    fi
  done
  return 1
}

# ── Optional, aber per .env eingeschaltet ───────────────────
# "[optional]" heisst: der Bot startet ohne. Das stimmt nur, solange der
# zugehoerige Schalter aus ist. Mit DB_BACKEND=mariadb ist PyMySQL Pflicht —
# fehlte es, meldete --python-deps "vollstaendig", und der Bot starb beim
# ersten db_conn() am Import (Befund Codex-Review, PR #162). Dieselbe Klasse
# wie W110: eine Bedingung, deren Abhaengigkeit niemand prueft.
#
# Nur Pakete mit einem AUSDRUECKLICHEN Einschalter stehen hier. redis und
# faster-whisper haben keinen: redis wird mit Rueckfall versucht, Whisper
# laeuft nur, wenn es installiert ist. Sie bleiben optional.
#
# Die .env wird GELESEN, nicht gesourct — sie enthaelt Geheimnisse und
# beliebige Werte, ein `.` darauf fuehrt sie als Code aus.
env_wert(){ # env_wert SCHLUESSEL -> letzter unkommentierter Wert, ohne Quotes
  [ -r "$ZIEL/.env" ] || return 0
  sed -n "s/^[[:space:]]*$1[[:space:]]*=[[:space:]]*//p" "$ZIEL/.env" \
    | tail -1 | sed 's/[[:space:]]*#.*$//' | tr -d '"'"'"'\r' | sed 's/[[:space:]]*$//'
}
normiert(){ printf '%s' "$1" | tr 'A-Z' 'a-z' | tr '_.' '--'; }
KONFIG_PFLICHT=""     # "normname=Grund" je Zeile
[ "$(env_wert DB_BACKEND | tr 'A-Z' 'a-z')" = "mariadb" ] && \
  KONFIG_PFLICHT="${KONFIG_PFLICHT}pymysql=DB_BACKEND=mariadb"$'\n'
case "$(env_wert S3_BACKUP | tr 'A-Z' 'a-z')" in 1|true|yes|ja|on)
  KONFIG_PFLICHT="${KONFIG_PFLICHT}boto3=S3_BACKUP=1"$'\n';; esac
[ -n "$(env_wert DISCORD_BOT_TOKEN)" ] && \
  KONFIG_PFLICHT="${KONFIG_PFLICHT}discord-py=DISCORD_BOT_TOKEN"$'\n'
# v4.2-W129: die Sprachreaktion (Nutzungsprofil "ki") zapft das Stream-Audio
# und laesst faster-whisper mitschreiben. Ohne das Paket meldet der Selbsttest
# "LIVE_REACT_SPEECH=1, aber faster-whisper fehlt" — erst NACH dem Start.
# LIVE_REACT_SPEECH ist ab Werk an; nur ein ausdrueckliches Aus nimmt es weg.
case "$(env_wert LIVE_REACT_ENABLED | tr 'A-Z' 'a-z')" in 1|true|yes|ja|on)
  case "$(env_wert LIVE_REACT_SPEECH | tr 'A-Z' 'a-z')" in 0|false|no|nein|off) ;;
    *) KONFIG_PFLICHT="${KONFIG_PFLICHT}faster-whisper=LIVE_REACT_ENABLED=1"$'\n';; esac;; esac
konfig_grund(){ # konfig_grund NAME -> Grund, falls per .env Pflicht
  printf '%s' "$KONFIG_PFLICHT" | sed -n "s/^$(normiert "$1")=//p" | head -1
}

abgleich_lesen(){ # -> setzt PY_FEHLT, gibt die Tabelle aus
  local status name ist spec art grund
  PY_FEHLT=""
  while IFS="$(printf '\t')" read -r status name ist spec art; do
    [ -n "$status" ] || continue
    # v5.2-W193: mysqlclient braucht Header und Compiler — ein pip-Lauf ueber
    # alle Pakete fiele daran ganz. Es hat einen eigenen Schritt (--mysqlclient).
    [ "$(normiert "$name")" = "mysqlclient" ] && continue
    if [ "$art" = "optional" ] && [ "$W_OPTIONAL" = 0 ]; then
      grund="$(konfig_grund "$name")"
      [ -n "$grund" ] || continue
      info "%s ist optional, wird hier aber gebraucht: %s" "$name" "$grund"
    fi
    case "$status" in
      ok)        gut "%s %s" "$name" "$ist";;
      entfaellt) info "%s: entfaellt auf dieser Plattform" "$name";;
      fehlt)     warn "%s fehlt (%s)" "$name" "$spec"
                 PY_FEHLT="$PY_FEHLT ${name}${spec/\*/}";;
      alt)       warn "%s %s ist zu alt (%s)" "$name" "$ist" "$spec"
                 PY_FEHLT="$PY_FEHLT ${name}${spec}";;
    esac
  done
}

if [ "$W_PYTHON" = 1 ]; then
  kopf "Python-Pakete"
  [ -r "$REQ" ] || { fehler "requirements.txt fehlt in %s" "$ZIEL"; exit 2; }
  if [ ! -x "$VPY" ]; then
    warn "Keine virtuelle Umgebung unter %s/.venv." "$ZIEL"
    PY_VENV_NEU=1
    BASIS_PY="$(finde_python || true)"
    if [ -z "$BASIS_PY" ]; then
      fehler "Kein Python >= 3.12 gefunden — erst tools/installer.sh laufen lassen."
      exit 2
    fi
    info "Wird angelegt mit %s" "$BASIS_PY"
  else
    # Der Abgleich laeuft mit dem venv-Python: nur so sieht er dessen Pakete.
    # Exit 2 von anforderungen.py heisst "kann nicht pruefen" — das ist ein
    # Befund, kein "alles fehlt" und kein "alles da".
    _tab="$("$VPY" "$SKRIPT/anforderungen.py" --datei "$REQ")" || {
      fehler "Abgleich gegen requirements.txt fehlgeschlagen (siehe Meldung oben)."; exit 2; }
    abgleich_lesen <<< "$_tab"
  fi
  [ "$W_OPTIONAL" = 0 ] && info "Optionale Pakete nicht geprueft, ausser per .env eingeschaltete (alle: --optional)."
fi

# ═══════════════════════════════════════════════════════════════════════════
# Zusatzfunktionen (v4.2-W143)
# ═══════════════════════════════════════════════════════════════════════════
# Der Betreiber am 05.11.: „update.sh sollte interaktiv alle fehlenden
# Funktionen, plugins, Software nach installieren. Also Prometheus grafana und
# Co." Alles hier war schon da — nur nie GEFRAGT: Prometheus/Grafana hingen an
# --observability, die optionalen Pakete an --optional, und wer die Schalter
# nicht kannte, bekam „Nichts zu tun". Gefragt wird nur im gefuehrten Modus;
# unbeaufsichtigt und mit --express gilt weiter nur, was per Schalter gewaehlt
# ist — ein Zeitplan darf nie still einen Datenbank-Umzug ausloesen.
#
# Nichts davon ist ein Befund fuer --check: ein Bot ohne Prometheus oder auf
# SQLite ist vollstaendig. Gemeldet wird es trotzdem, damit man es weiss.
Z_PROM=0; Z_GRAF=0; Z_MARIA=0
_fragen(){ [ "$NC_MODUS" = "gefuehrt" ] && [ "$NUR_PRUEFEN" = 0 ] && [ -n "$NC_TTY" ]; }
kopf "Zusatzfunktionen"
if [ -z "$W_BEOBACHTUNG" ]; then
  if have prometheus || { have systemctl && systemctl list-unit-files --no-legend \
       nightcrawler-prometheus.service 2>/dev/null | grep -q .; }; then
    gut "Prometheus: eingerichtet"
  else
    info "Prometheus: nicht eingerichtet — Kennzahlen unter /metrics und Alarme bleiben ungelesen."
    if _fragen && frage_ja "Prometheus jetzt einrichten?" N; then
      Z_PROM=1
      frage_ja "Grafana dazu (Diagramme im Browser, nur ueber SSH-Tunnel)?" N && Z_GRAF=1
    fi
  fi
fi
# Nur wenn gefragt wird: ohne Rueckfrage nennt der Abgleich die optionalen
# Pakete bewusst nicht (W129 — wer die Sprachreaktion ausgeschaltet hat, soll
# nicht von faster-whisper lesen).
if _fragen && [ "$W_PYTHON" = 1 ] && [ "$W_OPTIONAL" = 0 ] && [ -n "${_tab:-}" ]; then
  _opt="$(printf '%s\n' "$_tab" | awk -F '\t' '$5=="optional" && ($1=="fehlt" || $1=="alt") {printf " %s", $2}')"
  if [ -n "$_opt" ]; then
    info "Optionale Pakete nicht installiert:%s" "$_opt"
    if frage_ja "Optionale Pakete mitinstallieren?" N; then
      W_OPTIONAL=1
      abgleich_lesen <<< "$_tab" >/dev/null
    fi
  fi
fi
DB_JETZT="$(env_wert DB_BACKEND | tr 'A-Z' 'a-z')"
SQ_PFAD="$(env_wert DB_PATH)"; SQ_PFAD="${SQ_PFAD:-tiktok_bot.db}"
case "$SQ_PFAD" in /*) ;; *) SQ_PFAD="$ZIEL/$SQ_PFAD";; esac
Z_MYSQLC=0; Z_MKONF=0
if [ "$DB_JETZT" = "mariadb" ]; then
  gut "Datenbank: MariaDB"
  [ "$W_MARIADB" = 1 ] && info "DB_BACKEND steht schon auf mariadb — kein Umzug noetig."
  # v5.2-W193: C-Treiber. Kein Befund fuer --check — PyMySQL laeuft.
  if [ -x "$VPY" ] && "$VPY" -c 'import MySQLdb' 2>/dev/null; then
    gut "MariaDB-Treiber: mysqlclient"
  else
    info "MariaDB-Treiber: PyMySQL (reines Python) — mysqlclient braucht rund ein Drittel der CPU je Abfrage."
    if [ "$W_MYSQLC" = 1 ]; then Z_MYSQLC=1
    elif [ "$NC_MODUS" = "express" ] && [ "$NUR_PRUEFEN" = 0 ]; then Z_MYSQLC=1
    elif _fragen; then
      erklaere "Baut den C-Treiber mysqlclient ins venv (Systempakete libmariadb-dev, pkg-config, Compiler). Der Bot nimmt ihn nach dem naechsten Neustart; scheitert der Bau, bleibt PyMySQL."
      frage_ja "C-Treiber mysqlclient einrichten?" J && Z_MYSQLC=1
    fi
  fi
  # v5.2-W193: Server-Einstellungen. Ein Neustart von MariaDB gehoert dem
  # Betreiber — deshalb nie unbeaufsichtigt ohne Schalter.
  MKONF_PFAD="$(nc_mariadb_konf_pfad)"
  if [ -z "$MKONF_PFAD" ]; then
    info "MariaDB-Einstellungen: kein bekanntes Konfigurationsverzeichnis (mariadb.conf.d/my.cnf.d) — uebersprungen."
  elif [ -f "$MKONF_PFAD" ] && grep -q 'innodb_flush_log_at_trx_commit = 2' "$MKONF_PFAD"; then
    gut "MariaDB-Einstellungen: %s" "$MKONF_PFAD"
  else
    info "MariaDB-Einstellungen: Werkseinstellung (Namens-Nachschlag je Verbindung, fsync je Commit)."
    if [ "$W_MKONF" = 1 ]; then Z_MKONF=1
    elif [ "$NC_MODUS" = "express" ] && [ "$NUR_PRUEFEN" = 0 ]; then Z_MKONF=1
    elif _fragen; then
      erklaere "Schreibt %s: kein DNS-Nachschlag je neuer Verbindung, und das Protokoll wird einmal je Sekunde statt je Commit auf die Platte gezwungen (wie SQLite mit synchronous=NORMAL; ein Stromausfall kostet hoechstens die letzte Sekunde). Danach startet MariaDB neu — der Bot verbindet sich von selbst wieder." "$MKONF_PFAD"
      frage_ja "MariaDB-Einstellungen schreiben und MariaDB neu starten?" J && Z_MKONF=1
    fi
  fi
elif [ ! -s "$SQ_PFAD" ]; then
  info "Datenbank: SQLite, noch ohne Datei — ein Umzug lohnt erst mit Daten."
else
  info "Datenbank: SQLite (%s)" "$SQ_PFAD"
  if [ "$W_MARIADB" = 1 ]; then
    Z_MARIA=1
  elif _fragen; then
    erklaere "MariaDB lohnt, wenn die Datenbank gross wird oder mehrere Rechner darauf sollen. Der Umzug stoppt den Bot kurz, legt Server, Datenbank und Nutzer an, zieht jede Tabelle um, zaehlt nach und stellt erst dann die .env um. Die SQLite-Datei bleibt liegen — Rueckweg: DB_BACKEND=sqlite."
    frage_ja "Datenbank nach MariaDB umziehen?" N && Z_MARIA=1
  fi
fi
# ── Lokales LLM (v5.1-W181) ──────────────────────────────────
# Der Betreiber am 11.11.: Umstieg auf ik_llama.cpp mit Qwen3-14B-Uncensored,
# und ein vorhandenes llama.cpp ERST deinstallieren. Die Arbeit macht
# tools/ikllama.sh — dasselbe Werkzeug wie im Installer, gefragt wird hier nur.
# Gefragt wird im gefuehrten Modus; unbeaufsichtigt nur mit --ik-llama: ein
# Zeitplan darf nie still 9 GB laden und eine Viertelstunde bauen (dieselbe
# Regel wie fuer den Datenbank-Umzug). Kein Befund fuer --check — ein Bot mit
# altem llama.cpp oder ganz ohne lokales LLM laeuft (Cloud-Reserve).
Z_IK=0
IK_ZUSTAND="$(bash "$SKRIPT/ikllama.sh" --dir "$ZIEL" --zustand 2>/dev/null | tail -1)"
case "$IK_ZUSTAND" in
  fertig)
    gut "Lokales LLM: ik_llama.cpp eingerichtet"
    [ "$W_IKLLAMA" = 2 ] && Z_IK=1;;
  alt)
    warn "Lokales LLM: altes llama.cpp — Umstieg auf ik_llama.cpp mit Qwen3-14B-Uncensored steht aus."
    if [ "$W_IKLLAMA" != 0 ]; then Z_IK=1
    elif [ "$NC_MODUS" = "express" ] && [ "$NUR_PRUEFEN" = 0 ]; then Z_IK=1
    elif _fragen; then
      erklaere "Das alte llama.cpp wird gestoppt und entfernt (Dienst, Programm, Bau; alte Modelldateien bleiben als Rueckweg), dann ik_llama.cpp gebaut (10 bis 20 Minuten) und Qwen3-14B-Uncensored geladen (rund 9 GB, braucht rund 12 GB RAM). Der Bot bleibt dabei an — die KI laeuft so lange ueber die Cloud."
      frage_ja "Jetzt auf ik_llama.cpp umsteigen?" J && Z_IK=1
    else
      info "Umstieg: bash tools/update.sh --ik-llama  (oder sudo bash tools/ikllama.sh)"
    fi;;
  teilweise)
    warn "Lokales LLM: ik_llama.cpp nur teilweise eingerichtet (abgebrochener Lauf?)."
    if [ "$W_IKLLAMA" != 0 ]; then Z_IK=1
    elif _fragen; then frage_ja "Einrichtung fortsetzen?" J && Z_IK=1
    else info "Fortsetzen: bash tools/update.sh --ik-llama"; fi;;
  fehlt)
    info "Lokales LLM: nicht eingerichtet — die KI laeuft ueber die Cloud."
    if [ "$W_IKLLAMA" != 0 ]; then Z_IK=1
    elif _fragen; then frage_ja "ik_llama.cpp mit Qwen3-14B-Uncensored einrichten (rund 9 GB)?" N && Z_IK=1; fi;;
  *)
    warn "Lokales LLM: Zustand nicht ermittelbar — bash tools/ikllama.sh --check zeigt den Grund."
    [ "$W_IKLLAMA" != 0 ] && Z_IK=1;;
esac
# Der Umzug braucht PyMySQL im venv. Installiert wird es IN mariadb_umzug,
# vor dem Stopp — nicht ueber PY_FEHLT: dieser Weg laeuft nur mit
# --python-deps, und `--mariadb --system` haette die Zeile in den Plan
# geschrieben und nie ausgefuehrt (Codex, PR #191).

# ═══════════════════════════════════════════════════════════════════════════
kopf "Plan"
PLAN=0
if [ -n "$SYS_PAKETE" ]; then
  PLAN=1
  if [ "$SUDO" = "-" ]; then
    warn "Weder root noch sudo — Systempakete koennen nicht installiert werden."
    BEFUND=1
  else
    _ib="$(nc_installbefehl $SYS_PAKETE)"
    info "Systempakete: %s" "${SUDO:+$SUDO }$_ib"
  fi
fi
[ -n "$SYS_OHNE" ] && { warn "Selbst bereitstellen:%s" "$SYS_OHNE"; BEFUND=1; }
[ "$PY_VENV_NEU" = 1 ] && { PLAN=1; info "Virtuelle Umgebung anlegen: %s/.venv" "$ZIEL"; }
if [ "$PY_VENV_NEU" = 1 ]; then
  info "Danach: alle Pflichtpakete aus requirements.txt"
elif [ -n "$PY_FEHLT" ]; then
  PLAN=1; info "Python-Pakete:%s" "$PY_FEHLT"
fi
[ -n "$PIP_STATT" ] && { PLAN=1; info "Per pip in .venv:%s" "$PIP_STATT"; }
[ "$UPGRADE" = 1 ] && [ "$W_PYTHON" = 1 ] && { PLAN=1; info "Python-Pakete auf neueste zulaessige Fassung heben (--upgrade)"; }
[ "$Z_PROM" = 1 ] && { PLAN=1; if [ "$Z_GRAF" = 1 ]; then info "Prometheus und Grafana einrichten"; else info "Prometheus einrichten"; fi; }
[ "$Z_MARIA" = 1 ] && { PLAN=1; info "Datenbank umziehen: SQLite -> MariaDB (Server, Nutzer, Umzug, Nachzaehlen, .env)"; }
[ "$Z_IK" = 1 ] && { PLAN=1; info "Lokales LLM: altes llama.cpp entfernen, ik_llama.cpp bauen, Qwen3-14B-Uncensored laden"; }
[ "$Z_MYSQLC" = 1 ] && { PLAN=1; info "MariaDB: C-Treiber mysqlclient bauen (PyMySQL bleibt Rueckweg)"; }
[ "$Z_MKONF" = 1 ] && { PLAN=1; info "MariaDB: Einstellungen schreiben und MariaDB neu starten"; }

if [ "$PLAN" = 0 ]; then
  if [ "$BEFUND" = 0 ]; then gut "Nichts zu tun — alles vorhanden."
  else warn "Nichts automatisch zu tun — offene Punkte siehe oben."; fi
  exit "$BEFUND"
fi
if [ "$NUR_PRUEFEN" = 1 ]; then
  warn "Es fehlt etwas (siehe Plan). Ohne --check wird es installiert."
  exit 1
fi
if [ "$NC_MODUS" = "express" ] && [ "$TROCKEN" = 0 ]; then
  frage_ja "Plan ausfuehren?" J || { info "Abgebrochen — nichts veraendert."; exit 1; }
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Ausfuehrung"
if [ -n "$SYS_PAKETE" ] && [ "$SUDO" != "-" ]; then
  if [ "$NC_MODUS" != "gefuehrt" ] || [ "$TROCKEN" = 1 ] || frage_ja "Systempakete jetzt installieren?" J; then
    # ${a[@]+"${a[@]}"}: ein leeres Feld unter set -u ist in bash 3.2 (macOS)
    # ein "unbound variable" — und genau dort ist SUDO leer (brew).
    _sudo=(); [ -n "$SUDO" ] && _sudo=("$SUDO")
    if _af="$(nc_auffrischbefehl)"; then
      # Wortweise Zerlegung ist hier Absicht: der Befehl kommt aus lib/system.sh
      # und enthaelt nur feste Woerter.
      # shellcheck disable=SC2086
      lauf ${_sudo[@]+"${_sudo[@]}"} $_af || warn "Paketquellen liessen sich nicht auffrischen — versuche es trotzdem."
    fi
    # shellcheck disable=SC2086,SC2046
    lauf ${_sudo[@]+"${_sudo[@]}"} $(nc_installbefehl $SYS_PAKETE) || warn "Mindestens ein Systempaket liess sich nicht installieren."
  else
    info "Systempakete uebersprungen."
  fi
fi

if [ "$W_PYTHON" = 1 ] || [ -n "$PIP_STATT" ]; then
  if [ "$PY_VENV_NEU" = 1 ]; then
    if [ "$NC_MODUS" != "gefuehrt" ] || [ "$TROCKEN" = 1 ] || frage_ja "Virtuelle Umgebung anlegen und Pakete installieren?" J; then
      lauf "$BASIS_PY" -m venv "$ZIEL/.venv" || { fehler "venv liess sich nicht anlegen."; exit 1; }
      lauf "$VPY" -m pip install -r "$REQ" || BEFUND=1
    fi
  elif [ -n "$PY_FEHLT" ] || [ "$UPGRADE" = 1 ]; then
    if [ "$NC_MODUS" != "gefuehrt" ] || [ "$TROCKEN" = 1 ] || frage_ja "Python-Pakete jetzt installieren?" J; then
      if [ "$UPGRADE" = 1 ]; then
        # Upgrade ueber die Datei: nur so gelten die Untergrenzen UND die
        # Umgebungsmarker (uvloop nicht auf Windows) wie bei der Installation.
        # Optionale nur, wenn sie gewaehlt sind — sonst holte --upgrade still
        # 300 MB faster-whisper auf einen Pi.
        _rq="$(mktemp)"
        if [ "$W_OPTIONAL" = 1 ]; then cp "$REQ" "$_rq"
        else grep -v '\[optional\]' "$REQ" > "$_rq" || true; fi
        lauf "$VPY" -m pip install --upgrade -r "$_rq" || BEFUND=1
        rm -f "$_rq"
      else
        # shellcheck disable=SC2086  # PY_FEHLT: Anforderungen ohne Leerzeichen
        lauf "$VPY" -m pip install $PY_FEHLT || BEFUND=1
      fi
    fi
  fi
  if [ -n "$PIP_STATT" ]; then
    if [ -x "$VPY" ] || [ "$TROCKEN" = 1 ]; then
      # shellcheck disable=SC2086
      lauf "$VPY" -m pip install $PIP_STATT || BEFUND=1
    else
      warn "Ohne .venv kein pip-Weg fuer:%s" "$PIP_STATT"; BEFUND=1
    fi
  fi
fi

if [ "$Z_PROM" = 1 ]; then
  _w=(--no-grafana); [ "$Z_GRAF" = 1 ] && _w=(--grafana)
  _w+=(--dir "$ZIEL"); [ "$TROCKEN" = 1 ] && _w+=(--dry-run)
  [ "$NC_MODUS" = "unattended" ] && _w+=(--unattended)
  _sudo=(); [ -n "$SUDO" ] && [ "$SUDO" != "-" ] && _sudo=("$SUDO")
  lauf ${_sudo[@]+"${_sudo[@]}"} bash "$SKRIPT/observability.sh" "${_w[@]}" \
    || { warn "Prometheus/Grafana: Einrichtung unvollstaendig (siehe oben)."; BEFUND=1; }
fi
[ "$Z_MARIA" = 1 ] && { mariadb_umzug || BEFUND=1; }
[ "$Z_MYSQLC" = 1 ] && { mysqlclient_einrichten || BEFUND=1; }
[ "$Z_MKONF" = 1 ] && { mariadb_konf_schreiben || BEFUND=1; }
if [ "$Z_IK" = 1 ]; then
  # Die Rueckfrage ist oben gestellt (bzw. per Schalter beantwortet) — das
  # Werkzeug laeuft deshalb unbeaufsichtigt und fragt nicht ein zweites Mal.
  _w=(--unattended --dir "$ZIEL"); [ "$TROCKEN" = 1 ] && _w+=(--dry-run)
  [ "$W_IKLLAMA" = 2 ] && _w+=(--neu-bauen)
  [ "${NC_FARBE:-1}" = 0 ] && _w+=(--no-color)
  # Ohne sudo davor: ikllama.sh holt sich root selbst, Schritt fuer Schritt —
  # sudo setzt den PATH zurueck, und die Werkzeuge kaemen aus secure_path.
  # Und ohne lauf(): im Trockenlauf soll es seine Schritte ZEIGEN, nicht
  # selbst nur als eine Zeile erscheinen.
  bash "$SKRIPT/ikllama.sh" "${_w[@]}" \
    || { warn "Lokales LLM: Einrichtung unvollstaendig (Grund oben) — erneut: bash tools/update.sh --ik-llama"; BEFUND=1; }
fi

if [ "$TROCKEN" = 1 ]; then
  info "Trockenlauf beendet — nichts wurde veraendert."
  exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════
# Nachpruefung: gemessen, nicht angenommen. Ein Paketmanager, der mit 0
# endet, hat nicht zwingend das Werkzeug in den PATH gelegt (yt-dlp aus alten
# Quellen heisst mal youtube-dl), und pip kann ein Paket "erfolgreich" in eine
# andere Umgebung installieren.
kopf "Nachpruefung"
for w in $SYS_FEHLT; do
  if have "$w" || [ -x "$ZIEL/.venv/bin/$w" ]; then gut "%s: jetzt vorhanden" "$w"
  else warn "%s fehlt weiterhin." "$w"; BEFUND=1; fi
done
if [ "$W_PYTHON" = 1 ] && [ -x "$VPY" ]; then
  _tab="$("$VPY" "$SKRIPT/anforderungen.py" --datei "$REQ")" || BEFUND=1
  abgleich_lesen <<< "$_tab"
  [ -n "$PY_FEHLT" ] && { warn "Python-Pakete fehlen weiterhin:%s" "$PY_FEHLT"; BEFUND=1; }
fi
if [ "$BEFUND" = 0 ]; then
  gut "Abgleich vollstaendig."
  # Code und Pakete wirken erst nach einem Neustart — dieselbe Lage wie bei
  # der Update-Funktion (nc/laufstand.py). Gesagt wird es, getan nicht:
  # einen Dienst neu zu starten ist eine Entscheidung des Betreibers.
  info "Ein laufender Bot sieht neue Pakete erst nach einem Neustart des Dienstes."
else
  warn "Abgleich unvollstaendig — offene Punkte siehe oben."
fi
exit "$BEFUND"
