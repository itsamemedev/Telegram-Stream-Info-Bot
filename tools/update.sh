#!/usr/bin/env bash
#
# NIGHTCRAWLER — Nachinstallation und Abgleich (v4.2-W123)
#
#     bash tools/update.sh                  gefuehrt: Systempakete + Python-Pflichtpakete
#     bash tools/update.sh --check          nur pruefen; Exit 1, wenn etwas fehlt
#     bash tools/update.sh --dry-run        zeigen, was liefe — nichts ausfuehren
#     bash tools/update.sh --python-deps --optional --unattended
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
W_SYSTEM=0; W_PYTHON=0; W_OPTIONAL=0; W_BEOBACHTUNG=""
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
konfig_grund(){ # konfig_grund NAME -> Grund, falls per .env Pflicht
  printf '%s' "$KONFIG_PFLICHT" | sed -n "s/^$(normiert "$1")=//p" | head -1
}

abgleich_lesen(){ # -> setzt PY_FEHLT, gibt die Tabelle aus
  local status name ist spec art grund
  PY_FEHLT=""
  while IFS="$(printf '\t')" read -r status name ist spec art; do
    [ -n "$status" ] || continue
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
