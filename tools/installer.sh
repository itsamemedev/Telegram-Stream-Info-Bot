#!/usr/bin/env bash
#
# NIGHTCRAWLER v37 — gefuehrte Installation
#
#     bash tools/installer.sh              gefuehrt, erklaert jeden Schritt
#     bash tools/installer.sh --express    nur Pflichtfragen, Rest per Vorgabe
#     bash tools/installer.sh --unattended gar keine Fragen (fuer Skripte)
#     bash tools/installer.sh --dry-run    Plan und .env-Diff zeigen, nichts schreiben
#     bash tools/installer.sh --help       alle Schalter
#
# Ziele: Debian/Ubuntu/Raspberry Pi OS (apt), Fedora/RHEL (dnf), Arch (pacman),
# openSUSE (zypper), Alpine (apk), macOS (brew). Fuer Windows liegt daneben
# tools/install.bat.
#
# WARUM ES DAS GIBT
# Die Anleitung im README ist richtig, aber sie ist eine Anleitung: zehn
# Schritte, drei Fussnoten, und der haeufigste Ausgang war ein Bot, der beim
# ersten Start ueber eine fehlende .env-Variable stolpert oder unter Python
# 3.11 schon beim Parsen von bot.py stirbt (PEP 701, f-string mit Backslash —
# das ist keine Empfehlung, das ist eine harte Grenze).
#
# AUFBAU SEIT v4.2-W124: ERST FRAGEN, DANN HANDELN.
# Bis W123 waren Fragen und Eingriffe verzahnt: wer bei Frage sieben merkte,
# dass Frage drei falsch beantwortet war, hatte schon Pakete installiert und
# eine .env geschrieben. Jetzt laeuft es in vier Phasen:
#
#   A  Erkennung      liest nur — System, Paketmanager, Init, Bestand
#   B  Fragen         fuellt den PLAN, schreibt nichts
#   C  Zusammenfassung  jeder Punkt einzeln aenderbar; dazu der Diff der .env
#                     gegen die bestehende (Geheimnisse maskiert)
#   D  Ausfuehrung    nur was sich unterscheidet: fehlende Pakete, geaenderte
#                     .env-Zeilen, Unit/nginx/start.sh nur bei Abweichung
#
# --dry-run endet nach C. Ein zweiter Lauf auf einem unveraenderten Bestand
# aendert nichts — auch nicht die Geheimnisse: bis W123 erzeugte --unattended
# bei JEDEM Lauf einen neuen DASHBOARD_TOKEN, und jeder gespeicherte
# ?token=-Link war danach tot.
#
# Was es NICHT tut: Geheimnisse erfinden, die von aussen kommen (Bot-Token,
# Stream-Keys). Wo ein Passwort dagegen frei waehlbar ist — Dashboard-Token,
# Dashboard-PIN, Datenbank-Passwort — bietet es an, eines zu erzeugen.

set -euo pipefail

NC_INSTALLER_VERSION="2.0"
REPO_URL="${REPO_URL:-https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git}"
PY_MIN_MAJOR=3
PY_MIN_MINOR=12

# ── Betriebsarten ────────────────────────────────────────────
MODUS="gefuehrt"          # gefuehrt | express | unattended
ZIEL=""                   # --dir
BRANCH="${BRANCH:-main}"
SKIP_SYSTEM=0
FARBE=1
TROCKEN=0                 # --dry-run

# ── Ausgabe ──────────────────────────────────────────────────
setze_farben(){
  if [ "$FARBE" = 1 ] && [ -t 1 ]; then
    B=$'\033[1m'; R=$'\033[0m'
    BR=$'\033[38;5;179m'; DIM=$'\033[38;5;136m'; TXT=$'\033[38;5;187m'
    FNT=$'\033[38;5;101m'; OK=$'\033[38;5;107m'; WRN=$'\033[38;5;173m'; ERR=$'\033[38;5;167m'
  else
    B=""; R=""; BR=""; DIM=""; TXT=""; FNT=""; OK=""; WRN=""; ERR=""
  fi
}
setze_farben

SCHRITT=0
SCHRITTE_GESAMT=8
kopf(){ SCHRITT=$((SCHRITT+1))
  printf '\n%s%s[%d/%d] %s%s\n' "$BR" "$B" "$SCHRITT" "$SCHRITTE_GESAMT" "$(t "$1")" "$R"
  printf '%s%s%s\n' "$DIM" "$(printf '─%.0s' $(seq 1 66))" "$R"; }
# v4.1-W17: Mehrsprachigkeit AN DER SENKE. Jede dieser Funktionen schickt ihren
# Text durch tf (lib/i18n.sh): der Text ist der Schluessel, Laufzeitwerte
# kommen als weitere Argumente. Fehlt eine Uebersetzung, bleibt Deutsch stehen.
# v4.2-W123: tf (Format mit Laufzeitwerten) und tz (Heredoc zeilenweise) kommen
# aus derselben Datei. Fehlt sie, muessen alle drei weiter funktionieren —
# deutsch, aber vollstaendig; ein fehlendes tf waere "command not found" mitten
# in der Installation.
# shellcheck source=lib/i18n.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/i18n.sh" 2>/dev/null || {
  t(){ printf '%s' "$*"; }
  # shellcheck disable=SC2059
  tf(){ if [ $# -le 1 ]; then printf '%s' "${1:-}"; else _f="$1"; shift; printf -- "$_f" "$@"; fi; }
  tz(){ cat; }
}
# v4.2-W124: die Erkennung (Paketmanager, Init, MOTD-Weg, Paketnamen) teilt
# sich der Installer mit tools/update.sh. Ohne sie gibt es keinen Installer —
# zwei Kopien derselben Erkennung liefen auseinander (W98, W100).
# shellcheck source=lib/system.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/system.sh" || {
  printf '%s\n' "$(t 'tools/lib/system.sh fehlt — Quelltext unvollstaendig.')" >&2; exit 2; }

info(){ printf '  %s▸%s %s\n' "$DIM" "$R" "$(tf "$@")"; }
gut(){  printf '  %s✔%s %s\n' "$OK" "$R" "$(tf "$@")"; }
warn(){ printf '  %s▲%s %s\n' "$WRN" "$R" "$(tf "$@")"; }
fehler(){ printf '  %s✘%s %s\n' "$ERR" "$R" "$(tf "$@")" >&2; }
# Erklaerungen sind der halbe Zweck dieses Skripts — deshalb bekommen sie ein
# eigenes, ruhiges Format und werden auf 72 Zeichen umbrochen.
erklaere(){ printf '%s' "$FNT"; printf '%s\n' "$(tf "$@")" | fold -s -w 72 | sed 's/^/    /'; printf '%s' "$R"; }
# Zwischenueberschrift innerhalb eines Schritts.
abschnitt(){ printf '\n  %s%s%s%s\n' "$B" "$TXT" "$(t "$1")" "$R"; }

MERKZETTEL=""
# Auch der Merkzettel geht durch tf — er steht im Bericht und in der Notiz.
merke(){ MERKZETTEL="${MERKZETTEL}$(tf "$@")"$'\n'; }

abbruch(){
  local rc=$?
  printf '\n'
  fehler "Abbruch in Schritt %s (Rueckgabewert %s)." "$SCHRITT" "$rc"
  erklaere "Was bereits geschrieben wurde, bleibt liegen — ein erneuter Lauf setzt dort auf, ohne Schaden anzurichten."
  [ -n "${ZIEL:-}" ] && info "Zielverzeichnis: %s" "$ZIEL"
  exit "$rc"
}
trap abbruch ERR

# ── Eingaben ─────────────────────────────────────────────────
# Auch wenn das Skript per Pipe kommt (curl ... | bash) muss die Tastatur
# erreichbar bleiben — sonst laufen alle Fragen ins Leere und der Nutzer
# bekaeme stumm die Vorgaben. /dev/tty muss sich auch OEFFNEN lassen: in
# Containern existiert es oft, ohne dass es ein Terminal dahinter gibt.
TTY=""
if [ -t 0 ]; then TTY="/dev/stdin"; elif [ -r /dev/tty ] && (: < /dev/tty) 2>/dev/null; then TTY="/dev/tty"; fi

lies(){ # lies VARIABLE [-s]
  local __v="$1" __still="${2:-}" __in=""
  if [ -z "$TTY" ]; then printf -v "$__v" '%s' ""; return 0; fi
  if [ "$__still" = "-s" ]; then
    read -r -s __in < "$TTY" || true; printf '\n'
  else
    read -r __in < "$TTY" || true
  fi
  printf -v "$__v" '%s' "$__in"
}

frage_ja(){ # frage_ja "Frage" [J|N]   -> 0 = ja
  local f="$1" vor="${2:-J}" a
  if [ "$MODUS" = "unattended" ]; then [ "$vor" = "J" ]; return; fi
  while :; do
    if [ "$vor" = "J" ]; then printf '  %s?%s %s %s%s%s ' "$BR" "$R" "$(t "$f")" "$FNT" "$(t '[J/n]')" "$R"
    else                      printf '  %s?%s %s %s%s%s ' "$BR" "$R" "$(t "$f")" "$FNT" "$(t '[j/N]')" "$R"; fi
    lies a
    a=$(printf '%s' "$a" | tr 'A-Z' 'a-z')
    case "$a" in
      j|ja|y|yes) return 0;;
      n|nein|no)  return 1;;
      "") [ "$vor" = "J" ]; return;;
      *) warn "Bitte j oder n.";;
    esac
  done
}

frage_text(){ # frage_text VARIABLE "Frage" "Vorgabe"
  local __v="$1" f="$2" vor="${3:-}" a
  if [ "$MODUS" = "unattended" ]; then printf -v "$__v" '%s' "$vor"; return 0; fi
  if [ -n "$vor" ]; then printf '  %s?%s %s %s[%s]%s ' "$BR" "$R" "$(t "$f")" "$FNT" "$vor" "$R"
  else                   printf '  %s?%s %s ' "$BR" "$R" "$(t "$f")"; fi
  lies a
  [ -z "$a" ] && a="$vor"
  printf -v "$__v" '%s' "$a"
}

# frage_wahl VARIABLE "Frage" VORGABE schl1 "Text 1" schl2 "Text 2" …
# v4.2-W124: Auswahl statt einer Kette von Ja/Nein-Fragen. "Dashboard im Netz
# erreichbar?" + "Reverse-Proxy einrichten?" waren zwei Fragen fuer EINE
# Entscheidung, und die Kombination "beides ja" war moeglich und falsch.
# Gefragt wird nur im gefuehrten Lauf — eine Auswahl ist nie Pflicht, im
# Express- und unbeaufsichtigten Lauf gilt die Vorgabe.
frage_wahl(){
  local __v="$1" f="$2" vor="$3" a i=1 n vorn=1
  shift 3
  local -a _schl=() _text=()
  while [ $# -ge 2 ]; do _schl+=("$1"); _text+=("$2"); shift 2; done
  n=${#_schl[@]}
  for i in $(seq 1 "$n"); do [ "${_schl[$((i-1))]}" = "$vor" ] && vorn=$i; done
  if [ "$MODUS" != "gefuehrt" ] || [ -z "$TTY" ]; then printf -v "$__v" '%s' "$vor"; return 0; fi
  printf '  %s?%s %s\n' "$BR" "$R" "$(t "$f")"
  for i in $(seq 1 "$n"); do
    printf '      %s%d)%s %s\n' "$TXT" "$i" "$R" "$(t "${_text[$((i-1))]}")"
  done
  while :; do
    printf '    %s%s [%d]:%s ' "$FNT" "$(t 'Auswahl')" "$vorn" "$R"
    lies a
    [ -z "$a" ] && a="$vorn"
    if [[ "$a" =~ ^[0-9]+$ ]] && [ "$a" -ge 1 ] && [ "$a" -le "$n" ]; then
      printf -v "$__v" '%s' "${_schl[$((a-1))]}"; return 0
    fi
    warn "Bitte eine Zahl von 1 bis %s." "$n"
  done
}

erzeuge_passwort(){ # erzeuge_passwort [laenge] [nur_ziffern]
  local n="${1:-32}" ziffern="${2:-0}"
  if [ "$ziffern" = 1 ]; then
    if have python3; then python3 -c "import secrets;print(''.join(secrets.choice('0123456789') for _ in range($n)))"
    else LC_ALL=C tr -dc '0-9' < /dev/urandom | head -c "$n"; echo; fi
    return
  fi
  if have openssl; then openssl rand -base64 48 | LC_ALL=C tr -dc 'A-Za-z0-9' | head -c "$n"; echo
  elif have python3; then python3 -c "import secrets;print(secrets.token_urlsafe($n)[:$n])"
  else LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c "$n"; echo; fi
}

frage_geheimnis(){ # frage_geheimnis VARIABLE "Beschreibung" erzeugbar laenge [nur_ziffern] [bisher]
  # Genau der vom Betreiber gewuenschte Ablauf: erst fragen, ob erzeugt werden
  # soll — sonst auf die Eingabe WARTEN (verdeckt, mit Wiederholung).
  #
  # v4.2-W124: ein BESTEHENDES Geheimnis bleibt. Bis hierher erzeugte der
  # unbeaufsichtigte Lauf bei jedem Aufruf ein neues — ein zweiter Lauf machte
  # jeden gespeicherten ?token=-Link und jede PWA-Anmeldung ungueltig.
  local __v="$1" was="$2" erzeugbar="${3:-1}" laenge="${4:-32}" ziffern="${5:-0}" bisher="${6:-}"
  local a b
  if [ -n "$bisher" ]; then
    if [ "$MODUS" != "gefuehrt" ] || frage_ja "$(tf '%s ist gesetzt — behalten?' "$(t "$was")")" J; then
      printf -v "$__v" '%s' "$bisher"; return 0
    fi
  fi
  if [ "$MODUS" = "unattended" ]; then
    if [ "$erzeugbar" = 1 ]; then printf -v "$__v" '%s' "$(erzeuge_passwort "$laenge" "$ziffern")"
    else printf -v "$__v" '%s' ""; fi
    return 0
  fi
  if [ "$erzeugbar" = 1 ] && frage_ja "$(tf '%s: sicheres Passwort erzeugen lassen?' "$(t "$was")")" J; then
    a="$(erzeuge_passwort "$laenge" "$ziffern")"
    printf '    %s%s%s %s%s%s\n' "$FNT" "$(t 'erzeugt:')" "$R" "$B" "$a" "$R"
    erklaere "Notieren oder im Passwortmanager ablegen. Es steht ausserdem in der .env (chmod 600) und laesst sich dort jederzeit nachlesen."
    printf -v "$__v" '%s' "$a"
    return 0
  fi
  while :; do
    printf '  %s?%s %s %s%s%s: ' "$BR" "$R" "$(tf '%s eingeben' "$(t "$was")")" "$FNT" "$(t '(leer = spaeter selbst eintragen)')" "$R"
    lies a -s
    [ -z "$a" ] && { printf -v "$__v" '%s' ""; return 0; }
    printf '  %s?%s %s ' "$BR" "$R" "$(t 'Zur Sicherheit wiederholen:')"
    lies b -s
    [ "$a" = "$b" ] && { printf -v "$__v" '%s' "$a"; return 0; }
    warn "Die Eingaben waren nicht gleich — noch einmal."
  done
}

have(){ command -v "$1" >/dev/null 2>&1; }

# ── Ausfuehren ───────────────────────────────────────────────
# EIN Weg fuer jeden Eingriff ins System: der Befehl wird gezeigt und dann
# ausgefuehrt. Wer liest, was passiert, kann es nachvollziehen und
# wiederholen — und ein Fehler nennt den Befehl, der ihn ausgeloest hat.
lauf(){ printf '    %s$ %s%s\n' "$FNT" "$*" "$R"; "$@"; }
als_root(){ if [ -n "$SUDO" ]; then lauf "$SUDO" "$@"; else lauf "$@"; fi; }

# schreibe_systemdatei ZIEL QUELLE — nur bei Abweichung, mit Diff.
# v4.2-W124: Unit, nginx-Datei und OpenRC-Skript wurden bei jedem Lauf
# ueberschrieben, auch unveraendert — und ein `daemon-reload` samt Neustart
# hing daran. Jetzt: gleich -> nichts; anders -> Diff zeigen, dann schreiben.
# Rueckgabe 0 = geschrieben, 1 = war schon so.
schreibe_systemdatei(){
  local ziel="$1" quelle="$2"
  if [ -f "$ziel" ] && cmp -s "$ziel" "$quelle"; then
    info "unveraendert: %s" "$ziel"; return 1
  fi
  if [ -f "$ziel" ]; then
    info "geaendert: %s" "$ziel"
    diff -u "$ziel" "$quelle" | sed '1,2d; s/^/      /' || true
  else
    info "neu: %s" "$ziel"
  fi
  als_root mkdir -p "$(dirname "$ziel")"
  if [ -n "$SUDO" ]; then "$SUDO" tee "$ziel" < "$quelle" >/dev/null; else cat "$quelle" > "$ziel"; fi
  return 0
}

# ── Schalter ─────────────────────────────────────────────────
# Vorgaben VOR der Auswertung: das Skript laeuft mit set -u, und --set haengt
# an OPT_SETZEN an — ohne Vorbelegung starb schon der erste --set daran.
OPT_PROFIL=""; OPT_SETZEN=""; OPT_EXPERTE=0; OPT_BEOBACHTUNG="${OPT_BEOBACHTUNG:-}"
while [ $# -gt 0 ]; do
  case "$1" in
    --express)     MODUS="express";;
    --unattended|-y) MODUS="unattended";;
    --dry-run)     TROCKEN=1;;
    --dir)         ZIEL="${2:-}"; shift;;
    --dir=*)       ZIEL="${1#*=}";;
    --branch)      BRANCH="${2:-main}"; shift;;
    --branch=*)    BRANCH="${1#*=}";;
    --skip-system) SKIP_SYSTEM=1;;
    --observability) OPT_BEOBACHTUNG="prometheus";;
    --profile)     OPT_PROFIL="${2:-}"; shift;;
    --profile=*)   OPT_PROFIL="${1#*=}";;
    --set)         OPT_SETZEN="${OPT_SETZEN}${2:-}"$'\n'; shift;;
    --set=*)       OPT_SETZEN="${OPT_SETZEN}${1#*=}"$'\n';;
    --expert)      OPT_EXPERTE=1;;
    --observability=grafana) OPT_BEOBACHTUNG="grafana";;
    --pkg)         NC_PKG="${2:-}"; shift;;
    --pkg=*)       NC_PKG="${1#*=}";;
    --no-color)    FARBE=0; setze_farben;;
    --version)     printf 'NIGHTCRAWLER installer %s\n' "$NC_INSTALLER_VERSION"; exit 0;;
    --help|-h)
      # v4.2-W123: tz statt cat — die Hilfe war das Erste, was ein englischer
      # Nutzer sah, und sie war komplett deutsch.
      tz <<'HILFE'
NIGHTCRAWLER v37 — Installation

  bash tools/installer.sh [Schalter]

  --express        nur die Pflichtfragen, alles andere per Vorgabe
  --unattended,-y  keine Fragen; Passwoerter werden erzeugt, optionale
                   Bausteine bleiben aus. Fuer Provisionierung/CI.
  --dry-run        Plan und Aenderungen an der .env zeigen, nichts schreiben
  --dir <Pfad>     Zielverzeichnis (Vorgabe: ~/nightcrawler)
  --branch <Name>  Git-Zweig beim Klonen (Vorgabe: main)
  --skip-system    Systempakete nicht anfassen (wenn schon vorhanden)
  --profile <Name> Nutzungsprofil: minimal | restream | ki (deploy/profile/)
  --set NAME=WERT  einen .env-Wert setzen (mehrfach; nur Namen aus .env.example)
  --expert         zusaetzlich jede Variable aus .env.example aenderbar (gefuehrt)
  --observability  Prometheus mit einrichten (Verlauf und Alarme, nur lokal);
                   =grafana zusaetzlich Grafana. Ohne den Schalter: nur gefuehrt gefragt
  --pkg <Name>     Paketmanager erzwingen: apt dnf pacman zypper apk brew
  --no-color       ohne Farben
  --help           diese Hilfe

Unterstuetzt: Debian, Ubuntu, Raspberry Pi OS, Fedora, RHEL, Arch, openSUSE, Alpine, macOS.
Ein zweiter Lauf zeigt den Unterschied zur bestehenden Installation und aendert nur diesen.
Windows: install.bat im selben Ordner
HILFE
      exit 0;;
    *) fehler "Unbekannter Schalter: %s  (--help)" "$1"; exit 1;;
  esac
  shift
done
[ "$MODUS" != "unattended" ] && [ -z "$TTY" ] && MODUS="unattended"
case "${NC_PKG:-}" in
  ""|apt|dnf|pacman|zypper|apk|brew|keiner) ;;
  *) fehler "Unbekannter Paketmanager: %s (apt dnf pacman zypper apk brew)" "$NC_PKG"; exit 1;;
esac

# Arbeitsdateien des Plans. Raeumen sich selbst weg — auch bei Abbruch.
ARBEIT="$(mktemp -d)"
trap 'rm -rf "$ARBEIT"' EXIT

# ═══════════════════════════════════════════════════════════════════════════
kopf "Willkommen"
printf '  %s%sNIGHTCRAWLER v37%s %s%s%s\n\n' "$BR" "$B" "$R" "$FNT" \
  "$(t '— TikTok-Live-Ueberwachung, Aufnahme, Multi-Ziel-Restream und KI-Moderation (AZRAEL).')" "$R"
erklaere "Dieses Skript richtet den Bot vollstaendig ein und erklaert dabei, was es tut und warum. Es fragt vor jedem Eingriff. Abbrechen mit Strg+C ist jederzeit gefahrlos."
erklaere "Erst wird gefragt, dann zusammengefasst — jeder Punkt laesst sich dort noch aendern —, und erst danach wird etwas installiert oder geschrieben."
printf '\n  %s%s%s\n' "$DIM" "$(t 'Der Weg in acht Schritten:')" "$R"
tz <<'WILLKOMMEN'
    1  Willkommen              5  Ausfuehrung: System und Python
    2  Erkennung               6  Ausfuehrung: Konfiguration und Bausteine
    3  Fragen                  7  Selbsttest und Autostart
    4  Zusammenfassung         8  Bericht
WILLKOMMEN
case "$MODUS" in
  express)    info "Betriebsart: %s — nur Pflichtfragen." "${B}express${R}";;
  unattended) info "Betriebsart: %s — keine Fragen, Vorgaben und erzeugte Passwoerter." "${B}unattended${R}";;
  *)          info "Betriebsart: %s — mit Erklaerungen. Fuer weniger Text: --express" "${B}$(t 'gefuehrt')${R}";;
esac
[ "$TROCKEN" = 1 ] && info "Trockenlauf — Befehle werden gezeigt, nicht ausgefuehrt."
if [ "$MODUS" = "gefuehrt" ]; then
  frage_ja "Loslegen?" J || { info "Abgebrochen — nichts veraendert."; exit 0; }
fi

# ═══════════════════════════════════════════════════════════════════════════
# PHASE A — ERKENNUNG (liest nur)
# ═══════════════════════════════════════════════════════════════════════════
kopf "Erkennung"

nc_system_erkennen
nc_init_erkennen
nc_motd_weg
OS="$NC_OS"; PKG="$NC_PKG"; IST_PI="$NC_IST_PI"
ARCH="$(uname -m)"
info "System:    %s (%s)" "${NC_DISTRO_NAME:-$(t 'unbekannt')}" "$ARCH"
[ "$IST_PI" = 1 ] && info "Erkannt:   Raspberry Pi"
info "Paketmanager: %s" "$PKG"
info "Autostart-Weg: %s" "$NC_INIT"

# Rechte
SUDO=""
if [ "$(id -u)" -ne 0 ] && nc_braucht_root; then
  if have sudo; then SUDO="sudo"; else
    warn "Weder root noch sudo — Systempakete koennen nicht installiert werden."
    SKIP_SYSTEM=1
  fi
fi
if [ "$PKG" = "keiner" ] && [ "$SKIP_SYSTEM" = 0 ]; then
  if [ "$OS" = "Darwin" ]; then
    warn "Homebrew fehlt. Es ist auf macOS der einzige vernuenftige Weg zu ffmpeg."
    # shellcheck disable=SC2016  # der Befehl wird angezeigt, nicht ausgefuehrt
    erklaere "Installation (dauert ein paar Minuten): %s" '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  else
    warn "Paketmanager nicht erkannt (apt, dnf, pacman, zypper, apk, brew)."
    erklaere "Der Bot laeuft trotzdem — du musst ffmpeg, streamlink und yt-dlp dann selbst installieren. Schritt 5 wird uebersprungen."
  fi
  SKIP_SYSTEM=1
fi

# Arbeitsspeicher und Platte: der haeufigste Pi-Ausgang ist ein OOM-Kill
# mitten in der ersten Aufnahme. Lieber jetzt sagen als spaeter suchen.
RAM_MB=0
# NC_RAM_MB: fuer die Vertraege — die kleine Maschine ist der Fall, in dem
# der Installer faster-whisper von sich aus weglaesst (W129b).
if [ -n "${NC_RAM_MB:-}" ]; then RAM_MB="$NC_RAM_MB"
elif [ -r /proc/meminfo ]; then RAM_MB=$(awk '/^MemTotal:/{printf "%d", $2/1024}' /proc/meminfo)
elif [ "$OS" = "Darwin" ]; then RAM_MB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1048576 )); fi
KERNE=$( (nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 1) )
FREI_GB=$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2{printf "%d", $4/1048576}')
info 'Kerne:     %s   RAM: %s MB   frei in $HOME: %s GB' "$KERNE" "$RAM_MB" "${FREI_GB:-?}"
[ "${RAM_MB:-0}" -lt 2000 ] && warn "Unter 2 GB RAM: Transkription (Whisper) und lokales LLM bitte auslassen."
[ "${RAM_MB:-0}" -ge 2000 ] && [ "${RAM_MB:-0}" -lt 4000 ] && warn "Unter 4 GB RAM: Aufnahme und ein Restream-Ziel gehen, mehreres wird eng."
[ "${FREI_GB:-99}" -lt 5 ] && warn "Unter 5 GB frei — Aufnahmen fuellen die Platte sehr schnell."
if [ "$IST_PI" = 1 ]; then
  erklaere "Auf einem Raspberry Pi gilt: Aufnahme und EIN Restream-Ziel ohne Transcode sind realistisch. Transcode (mehrere Ziele gleichzeitig) rechnet die CPU in Software und ueberfordert jeden Pi. Aufnahmen gehoeren auf eine USB-SSD, nicht auf die SD-Karte — Dauerschreiben killt SD-Karten binnen Wochen."
fi

# Python
py_ok(){ "$1" -c "import sys;raise SystemExit(0 if sys.version_info>=($PY_MIN_MAJOR,$PY_MIN_MINOR) else 1)" >/dev/null 2>&1; }
finde_python(){
  local c
  for c in python3.14 python3.13 python3.12 python3 python; do
    have "$c" && py_ok "$c" && { command -v "$c"; return 0; }
  done
  for c in "$HOME/.local/share/uv/python"/*/bin/python3 /usr/local/bin/python3.1[2-9] /opt/homebrew/bin/python3.1[2-9]; do
    [ -x "$c" ] && py_ok "$c" && { printf '%s' "$c"; return 0; }
  done
  return 1
}
PY="$(finde_python || true)"
if [ -n "$PY" ]; then
  gut "Python gefunden: %s (%s)" "$PY" "$("$PY" -V 2>&1)"
else
  AKT="$( (python3 -V 2>&1) || t 'keins')"
  warn "Kein Python >= %s.%s gefunden (vorhanden: %s)." "$PY_MIN_MAJOR" "$PY_MIN_MINOR" "$AKT"
fi

# Quelltext und Ziel
SKRIPT="$(cd "$(dirname "$0")" && pwd)"
QUELLE=""
[ -f "$SKRIPT/../bot.py" ] && QUELLE="$(cd "$SKRIPT/.." && pwd)"
if [ -n "$QUELLE" ]; then
  info "Quelltext liegt bereits hier: %s" "$QUELLE"
  VORGABE="$QUELLE"
else
  info "Kein Quelltext neben dem Skript — er wird von GitHub geholt."
  VORGABE="$HOME/nightcrawler"
fi
[ -n "$ZIEL" ] || frage_text ZIEL "In welches Verzeichnis soll NIGHTCRAWLER?" "$VORGABE"
ZIEL="${ZIEL/#\~/$HOME}"
ENVF="$ZIEL/.env"
VENV="$ZIEL/.venv"
VPY="$VENV/bin/python"

BESTAND=0
[ -f "$ZIEL/bot.py" ] && BESTAND=1
if [ -f "$ENVF" ]; then
  gut "Bestehende Installation gefunden."
  info "Bestehende Werte bleiben; nur was du jetzt beantwortest, wird ueberschrieben."
fi

# ── Die .env als PLAN ────────────────────────────────────────
# v4.2-W124: env_set schreibt nicht mehr in die .env, sondern in den Plan
# (Schluessel<TAB>Wert, der letzte gewinnt). Geschrieben wird in Phase D —
# und nur, wenn das Ergebnis sich von der bestehenden Datei unterscheidet.
# Erst dadurch gibt es VOR dem Schreiben einen Diff, und eine geaenderte
# Antwort in der Zusammenfassung ueberschreibt die erste, statt ihr zu folgen.
PLAN_ENV="$ARBEIT/plan.env"
: > "$PLAN_ENV"
# Grundlage: die bestehende .env, sonst die Vorlage. Die Vorlage dokumentiert
# jede Variable mit ihrer Vorgabe — als Ausgangspunkt ist das Gold wert.
ENV_BASIS=""
if [ -f "$ENVF" ]; then ENV_BASIS="$ENVF"
elif [ -f "$ZIEL/.env.example" ]; then ENV_BASIS="$ZIEL/.env.example"
elif [ -n "$QUELLE" ] && [ -f "$QUELLE/.env.example" ]; then ENV_BASIS="$QUELLE/.env.example"; fi

env_set(){ # env_set SCHLUESSEL WERT — in den Plan, nicht in die Datei
  local k="$1" v="$2" tmp
  [ -z "$k" ] && return 0
  tmp="$ARBEIT/plan.tmp"
  awk -F '\t' -v k="$k" '$1!=k' "$PLAN_ENV" > "$tmp" && mv "$tmp" "$PLAN_ENV"
  printf '%s\t%s\n' "$k" "$v" >> "$PLAN_ENV"
}
env_aus_datei(){ # env_aus_datei DATEI SCHLUESSEL -> erster unkommentierter Wert
  [ -n "$1" ] && [ -f "$1" ] || return 0
  awk -F= -v k="$2" '/^[[:space:]]*#/{next} {key=$1;gsub(/[[:space:]]/,"",key)}
           key==k{v=$2;for(i=3;i<=NF;i++)v=v"="$i;gsub(/^[[:space:]"]+|[[:space:]"]+$/,"",v);print v;exit}' "$1" 2>/dev/null
}
env_get(){ # Plan vor Bestand: was gerade beantwortet wurde, gilt.
  local v
  if v="$(awk -F '\t' -v k="$1" '$1==k{w=$2; f=1} END{if(f) print w; else exit 1}' "$PLAN_ENV")"; then
    printf '%s' "$v"; return 0
  fi
  env_aus_datei "$ENV_BASIS" "$1"
}
env_bisher(){ env_aus_datei "${ENVF}" "$1"; }
VORLAGE=""
for _v in "$ZIEL/.env.example" "${QUELLE:+$QUELLE/.env.example}"; do
  [ -n "$_v" ] && [ -f "$_v" ] && { VORLAGE="$_v"; break; }
done
plan_weg(){ local tmp="$ARBEIT/plan.tmp"; awk -F '\t' -v k="$1" '$1!=k' "$PLAN_ENV" > "$tmp" && mv "$tmp" "$PLAN_ENV"; }
# env_zuruecksetzen SCHLUESSEL… — eine Wahl rueckgaengig machen.
# v4.2-W124: ohne das wirkte eine Aenderung in der Zusammenfassung nur in EINE
# Richtung — wer "sparsam" waehlte und zurueck auf "Vorgaben" ging, behielt
# die sparsamen Werte im Plan. Steht der Wert ausdruecklich in der
# bestehenden .env, kommt die Vorgabe aus der Vorlage (# NAME=wert) zurueck;
# sonst faellt der Schluessel einfach aus dem Plan.
env_zuruecksetzen(){
  local k vorgabe
  for k in "$@"; do
    plan_weg "$k"
    if [ -n "$(env_bisher "$k")" ]; then
      vorgabe="$( [ -n "$VORLAGE" ] && sed -n "s/^[#[:space:]]*${k}=//p" "$VORLAGE" | head -1)"
      env_set "$k" "$vorgabe"
    fi
  done
}

# env_bauen BASIS AUSGABE — Basis + Plan -> fertige .env. Ersetzt die Zeile,
# auch die auskommentierte; Werte mit Leerzeichen oder # werden gequotet.
# Ausserdem die Altlast "NAME=   # (Geheimnis — hier eintragen)": das sieht wie
# ein Kommentar aus, ist aber der WERT — python-dotenv liest bei unquotierten
# Werten den Rest der Zeile mit. Wer .env.example je kopiert hatte, hatte rund
# 40 Variablen mit genau diesem Text als Inhalt: der Bot hielt Discord, Twitch,
# YouTube und Anthropic fuer eingerichtet und meldete "Token abgelehnt" statt
# "kein Token".
env_bauen(){
  local basis="$1" aus="$2"
  if [ -n "$basis" ] && [ -f "$basis" ]; then
    sed -E 's/^([A-Za-z_][A-Za-z0-9_]*)=[[:space:]]*#.*$/\1=/' "$basis" > "$aus"
  else
    : > "$aus"
  fi
  awk -F '\t' 'NR==FNR{ if ($1!="") { plan[$1]=$2; reihe[++n]=$1 }; next }
    { t=$0; sub(/^[[:space:]]*#[[:space:]]*/,"",t)
      p=index(t,"="); key=(p?substr(t,1,p-1):""); gsub(/[[:space:]]/,"",key)
      if (key in plan) {
        if (!(key in gesetzt)) { gesetzt[key]=1; print zeile(key, plan[key]) }
        next }
      print }
    END{ for(i=1;i<=n;i++){ k=reihe[i]; if(!(k in gesetzt)){ gesetzt[k]=1; print zeile(k, plan[k]) } } }
    function zeile(k, v){ return (v ~ /[[:space:]#]/) ? k "=\"" v "\"" : k "=" v }
  ' "$PLAN_ENV" "$aus" > "$aus.neu" && mv "$aus.neu" "$aus"
}

# Geheimnisse im Diff maskieren — der Diff steht auf dem Bildschirm und im
# Scrollback, die .env hat Rechte 600 aus gutem Grund.
GEHEIM_MUSTER='(TOKEN|KEY|PASSWORD|PASSWORT|SECRET|PIN|COOKIE|WEBHOOK)'
env_diff(){ # env_diff ALT NEU -> maskierter Diff, nur die Zeilen
  local alt="$1" neu="$2"
  [ -f "$alt" ] || alt=/dev/null
  diff -u "$alt" "$neu" 2>/dev/null | sed '1,2d' | grep -E '^[-+]' | grep -vE '^[-+][[:space:]]*(#|$)' \
    | sed -E "s/^([-+][A-Za-z_]*${GEHEIM_MUSTER}[A-Za-z_]*=).+$/\1***/" || true
}

# Bestehender Dienst?
VORHANDEN=""
if [ "$NC_INIT" = "systemd" ]; then
  for u in nightcrawler tiktok-bot; do
    systemctl list-unit-files --no-legend "${u}.service" 2>/dev/null | grep -q . && VORHANDEN="$u" && break
  done
elif [ "$NC_INIT" = "openrc" ]; then
  [ -f /etc/init.d/nightcrawler ] && VORHANDEN="nightcrawler"
fi
[ -n "$VORHANDEN" ] && info "Vorhandener Dienst gefunden: %s" "$VORHANDEN"

# ═══════════════════════════════════════════════════════════════════════════
# PHASE B — FRAGEN (fuellt den Plan, schreibt nichts)
#
# Jeder Punkt ist eine Funktion f_<punkt>, damit die Zusammenfassung ihn
# einzeln erneut stellen kann, und hat eine Beschreibung z_<punkt> fuer die
# Zeile darin. Vorgaben kommen aus dem Plan bzw. dem Bestand — ein erneut
# gestellter Punkt beginnt dort, wo die letzte Antwort war.
# ═══════════════════════════════════════════════════════════════════════════
kopf "Fragen"

P_PYWEG="vorhanden"
f_python(){
  [ -n "$PY" ] && { P_PYWEG="vorhanden"; return 0; }
  erklaere "bot.py braucht mindestens Python %s.%s. Das ist keine Empfehlung: die Datei benutzt f-strings mit Backslash (PEP 701), unter 3.11 scheitert bereits das Einlesen mit einem SyntaxError. Debian 12 und Raspberry Pi OS bookworm liefern 3.11 — dort muss ein neuerer Interpreter dazu." "$PY_MIN_MAJOR" "$PY_MIN_MINOR"
  # Vorgabe "paket" nur, wenn die Quellen ein passendes Python TRAGEN.
  # Debian 12 und Raspberry Pi OS bookworm haben nur 3.11 — dort war "paket"
  # die Vorgabe, die Installation von python3.13 scheiterte, und der
  # Installer brach ab, statt uv zu nehmen (Codex-Befund, PR #163). Leere
  # Paketlisten heissen "unbekannt": dann wird nach dem Auffrischen gewaehlt,
  # und der Rueckfall auf uv steht in der Ausfuehrung.
  local vor="uv" _k
  if [ "$SKIP_SYSTEM" = 0 ] && [ -n "$(nc_paketname python)" ]; then
    if nc_quellen_leer; then vor="paket"
    else
      for _k in $(nc_paketname python); do nc_paket_verfuegbar "$_k" && { vor="paket"; break; }; done
    fi
    [ "$vor" = "uv" ] && [ "$PKG" = "apt" ] && [ "$NC_DISTRO" = "ubuntu" ] && vor="deadsnakes"
  fi
  frage_wahl P_PYWEG "Wie soll Python dazukommen?" "$vor" \
    paket "aus den Paketquellen des Systems" \
    deadsnakes "Ubuntu: Zusatzquelle deadsnakes (PPA)" \
    uv "uv: eigenstaendiges Python im Home, ohne root" \
    keiner "gar nicht — Abbruch"
  if [ "$P_PYWEG" = "keiner" ]; then
    fehler "Ohne Python >= %s.%s geht es nicht weiter." "$PY_MIN_MAJOR" "$PY_MIN_MINOR"
    info "Wege: %s" "apt install python3.13  |  dnf install python3.13  |  brew install python@3.13  |  https://astral.sh/uv"
    exit 1
  fi
}
z_python(){
  case "$P_PYWEG" in
    vorhanden) printf '%s' "$PY";;
    paket)     tf 'installieren: %s' "$(nc_paketname python)";;
    *)         tf 'installieren ueber %s' "$P_PYWEG";;
  esac
}

P_SYSTEM="N"
f_system(){
  if [ "$SKIP_SYSTEM" = 1 ]; then P_SYSTEM="N"; return 0; fi
  erklaere "Vier Dinge kommen NICHT ueber pip, weil es Programme sind und keine Bibliotheken: ffmpeg schneidet, kodiert und sendet; streamlink loest die TikTok-Quelle auf; yt-dlp ist der Rueckfall, wenn TikTok mit 403 blockt; sqlite3 ist die Kommandozeile zur Datenbank (fuer Diagnose, nicht fuer den Betrieb)."
  if frage_ja "Fehlende Systempakete installieren?" J; then P_SYSTEM="J"; else P_SYSTEM="N"; fi
}
z_system(){
  if [ "$SKIP_SYSTEM" = 1 ]; then t 'uebersprungen (--skip-system oder kein Paketmanager)'
  elif [ "$P_SYSTEM" = "J" ]; then tf 'fehlende ergaenzen ueber %s' "$PKG"
  else t 'nicht anfassen'; fi
}

OPT_AUS=""
opt_frage(){ # opt_frage <Paket> <Vorgabe J|N> <Erklaerung>
  local paket="$1" vorgabe="$2" text="$3"
  erklaere "$text"
  if ! frage_ja "$(tf '  → %s installieren?' "$paket")" "$vorgabe"; then
    OPT_AUS="$OPT_AUS $paket"
  fi
}
f_pypakete(){
  OPT_AUS=""
  local whisper=J
  [ "$IST_PI" = 1 ] && whisper=N
  [ "${RAM_MB:-0}" -lt 3000 ] && whisper=N
  # Per .env eingeschaltete Bausteine brauchen ihr Paket (Review #162): wer
  # DB_BACKEND=mariadb gesetzt hat, bekommt PyMySQL auch ohne Rueckfrage.
  local mysql=N discord=J
  [ "$(env_get DB_BACKEND | tr 'A-Z' 'a-z')" = "mariadb" ] && mysql=J
  if [ "$MODUS" = "gefuehrt" ]; then
    opt_frage "discord.py"     "$discord" "Discord: zweite Bedienoberflaeche mit 45 Slash-Commands, Moderation und Community-Funktionen. Ohne Discord-Server unnoetig."
    opt_frage "faster-whisper" "$whisper" "Transkription: schreibt mit, was im Stream gesagt wird (Grundlage fuer Clips, Highlights und die KI-Auswertung). Braucht rund 300 MB und deutlich CPU."
    opt_frage "PyMySQL"        "$mysql"   "MariaDB-Treiber: nur noetig, wenn du die Daten in MariaDB statt in SQLite haelst. SQLite reicht bis weit in den sechsstelligen Zeilenbereich."
    opt_frage "redis"          N  "Redis-Cache: entlastet bei sehr vielen gleichzeitigen Dashboard-Zugriffen. Fuer eine Ein-Personen-Installation ohne Nutzen."
    opt_frage "boto3"          N  "S3-Backup: schiebt Aufnahmen automatisch in einen S3-Speicher."
  else
    OPT_AUS="faster-whisper redis boto3"
    [ "$mysql" = "N" ] && OPT_AUS="$OPT_AUS PyMySQL"
    [ "$MODUS" = "unattended" ] && [ -z "$(env_get DISCORD_BOT_TOKEN)" ] && OPT_AUS="$OPT_AUS discord.py"
  fi
  # uvloop gibt es auf exotischen Plattformen nicht als fertiges Rad; es ist
  # reine Beschleunigung und darf fehlen.
  case "$ARCH" in x86_64|amd64|aarch64|arm64) ;; *) OPT_AUS="$OPT_AUS uvloop";; esac
  pakete_nach_plan
  return 0
}
# v4.2-W129b (Codex, PR #168): ein Paket, das eine EINSTELLUNG verlangt, darf
# nicht an der Reihenfolge der Fragen haengen. f_pypakete laeuft vor dem
# Nutzungsprofil; mit --profile ki stand LIVE_REACT_ENABLED=1 im Plan, und
# faster-whisper war schon ausgelassen. Dieselbe Regel wie in tools/update.sh
# (konfig_grund), aufgerufen am Ende JEDES Punkts, der sie aendern kann:
# Paketfrage, Nutzungsprofil, Einzelwerte. Fragt die Aenderungsschleife
# Punkt 3 neu, nachdem das Profil schon stand, korrigiert f_pypakete sich
# damit selbst — ein zweiter Aufruf vor der Installation waere ein Riegel
# ohne eigene Wirkung (W98).
pakete_nach_plan(){
  case "$(env_get LIVE_REACT_ENABLED | tr 'A-Z' 'a-z')" in 1|true|yes|ja|on)
    case "$(env_get LIVE_REACT_SPEECH | tr 'A-Z' 'a-z')" in 0|false|no|nein|off) ;;
      *) OPT_AUS="$(printf '%s' "$OPT_AUS" | sed 's/[[:space:]]*faster-whisper//')";; esac;; esac
  return 0
}
z_pypakete(){ if [ -n "$OPT_AUS" ]; then tf 'Pflicht + optionale, ausgelassen:%s' "$OPT_AUS"; else t 'Pflicht + alle optionalen'; fi; }

f_telegram(){
  erklaere "NIGHTCRAWLER wird ueber Telegram bedient. Ohne Bot-Token startet dieser Teil nicht. Den Token gibt dir @BotFather in Telegram: /newbot, Namen vergeben, fertig — er sieht aus wie 123456789:AAF... Er ist ein Geheimnis und laesst sich nicht erzeugen, nur holen."
  local tok
  frage_geheimnis tok "Telegram Bot-Token (von @BotFather)" 0 32 0 "$(env_get BOT_TOKEN)"
  if [ -n "$tok" ]; then env_set BOT_TOKEN "$tok"
  else warn "Kein Token — der Telegram-Teil bleibt still, bis du BOT_TOKEN in der .env eintraegst."; fi
  erklaere "Ohne Freigabeliste darf JEDER, der deinen Bot findet, ihn bedienen. ALLOWED_USER_IDS ist diese Liste (Zahlen, per Komma getrennt). Deine eigene ID sagt dir @userinfobot in Telegram."
  local ids
  frage_text ids "Deine Telegram-Nutzer-ID (mehrere per Komma, leer = keine Sperre)" "$(env_get ALLOWED_USER_IDS)"
  [ -n "$ids" ] && env_set ALLOWED_USER_IDS "$ids"
  [ -z "$ids" ] && warn "Keine Freigabeliste — jeder Telegram-Nutzer kann den Bot bedienen."
  return 0
}
z_telegram(){
  if [ -n "$(env_get BOT_TOKEN)" ]; then printf 'BOT_TOKEN ✔'; else printf 'BOT_TOKEN —'; fi
  if [ -n "$(env_get ALLOWED_USER_IDS)" ]; then tf ' · Freigabeliste: %s' "$(env_get ALLOWED_USER_IDS)"
  else t ' · ohne Freigabeliste'; fi
}

P_ZUGANG="lokal"; P_DOMAIN=""; P_CERT="J"
f_dashboard(){
  erklaere "Das Dashboard ist die Weboberflaeche: Sendeleiste, Aufnahmen, Statistiken, Abwehr. Es bindet standardmaessig NUR auf 127.0.0.1 — also nicht im Netz erreichbar. Der sichere Zugang ist ein SSH-Tunnel; alles andere sperrt man ueber Token oder Firewall auf."
  local port
  frage_text port "Port fuers Dashboard" "$(env_get DASHBOARD_PORT || true)"
  [ -z "$port" ] && port=8050
  env_set DASHBOARD_PORT "$port"
  local vor="lokal"
  [ "$(env_bisher WEB_HOST)" = "0.0.0.0" ] && vor="netz"
  [ -n "$(env_get PUBLIC_BASE_URL)" ] && vor="proxy"
  frage_wahl P_ZUGANG "Wie soll das Dashboard erreichbar sein?" "$vor" \
    lokal "nur lokal (127.0.0.1) — Zugang per SSH-Tunnel, empfohlen" \
    proxy "ueber nginx mit HTTPS (Reverse-Proxy, Domain noetig)" \
    netz  "direkt im Netz (0.0.0.0) — nur mit Token UND Firewall"
  case "$P_ZUGANG" in
    netz)
      env_set WEB_HOST 0.0.0.0
      warn "Der Port wird oeffentlich. Token ist damit Pflicht (kommt gleich).";;
    proxy)
      env_set WEB_HOST 127.0.0.1
      erklaere "Reverse-Proxy: nginx nimmt Port 443 mit einem echten Zertifikat entgegen und reicht nach 127.0.0.1 durch. Damit bleibt der Dashboard-Port zu, die Verbindung ist verschluesselt, und die OAuth-Rueckrufe von Kick, Twitch und YouTube funktionieren ohne SSH-Tunnel — die brauchen eine oeffentlich erreichbare HTTPS-Adresse. Das Zertifikat holt certbot von Let's Encrypt und erneuert es selbst."
      local alt_dom
      alt_dom="$(env_get PUBLIC_BASE_URL | sed 's#^https\?://##; s#/.*$##')"
      frage_text P_DOMAIN "Domain, die auf diese Maschine zeigt (z.B. bot.example.dev)" "${P_DOMAIN:-$alt_dom}"
      if [ -z "$P_DOMAIN" ]; then
        warn "Ohne Domain kein Zertifikat — uebersprungen."
        P_ZUGANG="lokal"
      else
        if frage_ja "Zertifikat von Let's Encrypt holen (certbot)?" J; then P_CERT=J; else P_CERT=N; fi
        # Der Bot muss seine oeffentliche Adresse kennen: sonst baut er die
        # OAuth-Rueckrufe auf localhost, und kein Anbieter erreicht die.
        # https NUR mit Zertifikat: die Vorlage lauscht allein auf Port 80,
        # eine https-Adresse ohne TLS waere eine Rueckruf-Adresse, die es nicht
        # gibt (Codex-Befund, PR #163). Scheitert certbot spaeter, setzt die
        # Ausfuehrung die Adresse zurueck auf http.
        if [ "$P_CERT" = "J" ]; then env_set PUBLIC_BASE_URL "https://${P_DOMAIN}"
        else
          env_set PUBLIC_BASE_URL "http://${P_DOMAIN}"
          warn "Ohne Zertifikat nur http — OAuth-Anbieter (Google, Twitch, Kick) verlangen HTTPS fuer ihre Rueckrufe."
        fi
        env_set TRUSTED_PROXIES "127.0.0.1"
      fi;;
    *)
      env_set WEB_HOST 127.0.0.1;;
  esac
  [ "$P_ZUGANG" = "proxy" ] || env_zuruecksetzen PUBLIC_BASE_URL TRUSTED_PROXIES
  erklaere "Der Dashboard-Token schuetzt den Zugriff von aussen (Aufruf einmal mit ?token=..., danach haelt ein Cookie). Loopback und SSH-Tunnel bleiben immer frei. Das ist ein frei waehlbares Geheimnis — hier ist Erzeugen die bessere Wahl als Ausdenken."
  local tok
  frage_geheimnis tok "Dashboard-Token" 1 40 0 "$(env_get DASHBOARD_TOKEN)"
  [ -n "$tok" ] && env_set DASHBOARD_TOKEN "$tok"
  [ -z "$tok" ] && [ "$P_ZUGANG" = "netz" ] && warn "Ohne Token und oeffentlich gebunden — bitte wenigstens die Firewall zumachen."
  if [ "$MODUS" = "gefuehrt" ]; then
    erklaere "Zusaetzlich gibt es einen PIN-Login fuer die Weboberflaeche und die PWA auf dem Handy — bequemer als ein 40-Zeichen-Token im Browser. Token und PIN duerfen parallel gelten."
    local pin bisher_pin
    bisher_pin="$(env_get DASHBOARD_PIN)"
    if [ -n "$bisher_pin" ] || frage_ja "PIN-Login einrichten?" N; then
      frage_geheimnis pin "Dashboard-PIN (Ziffern)" 1 6 1 "$bisher_pin"
      [ -n "$pin" ] && env_set DASHBOARD_PIN "$pin"
    fi
  fi
  return 0
}
z_dashboard(){
  local wie
  case "$P_ZUGANG" in
    netz)  wie="$(t '0.0.0.0 (offen)')";;
    proxy) wie="$(tf 'https://%s (nginx)' "$P_DOMAIN")";;
    *)     wie="$(t 'nur lokal')";;
  esac
  tf '%s · Port %s · Token %s' "$wie" "$(env_get DASHBOARD_PORT)" "$( [ -n "$(env_get DASHBOARD_TOKEN)" ] && printf '✔' || printf '—')"
}

f_discord(){
  if printf '%s' "$OPT_AUS" | grep -qi 'discord'; then return 0; fi
  erklaere "Optional: dieselben Funktionen als Slash-Commands in deinem Discord-Server, dazu Moderation und Community-Features. Token aus dem Discord Developer Portal (Bot → Reset Token). Ohne Token bleibt der Discord-Teil einfach still — der Bot startet trotzdem."
  local alt; alt="$(env_get DISCORD_BOT_TOKEN)"
  if [ -n "$alt" ] || { [ "$MODUS" = "gefuehrt" ] && frage_ja "Discord jetzt einrichten?" N; }; then
    local tok gid rolle
    frage_geheimnis tok "Discord Bot-Token" 0 32 0 "$alt"
    [ -n "$tok" ] && env_set DISCORD_BOT_TOKEN "$tok"
    frage_text gid "Discord-Server-ID (Guild-ID, Rechtsklick auf den Server → ID kopieren)" "$(env_get DISCORD_GUILD_ID || true)"
    [ -n "$gid" ] && env_set DISCORD_GUILD_ID "$gid"
    frage_text rolle "Name der Admin-Rolle (fuer /ban, /timeout, /setup_*)" "$(env_get DISCORD_ADMIN_ROLE || echo Admin)"
    [ -n "$rolle" ] && env_set DISCORD_ADMIN_ROLE "$rolle"
  fi
  return 0
}
z_discord(){ if [ -n "$(env_get DISCORD_BOT_TOKEN)" ]; then t 'eingerichtet'; else t 'aus'; fi; }

restream_ziel(){ # restream_ziel <PRAEFIX> <Klarname> <Hinweis>
  local p="$1" name="$2" hinweis="$3" key alt
  alt="$(env_get "${p}_STREAM_KEY")"
  if [ -n "$alt" ] || frage_ja "$(tf '%s als Restream-Ziel einrichten?' "$name")" N; then
    erklaere "$hinweis"
    frage_geheimnis key "$(tf '%s Stream-Key' "$name")" 0 32 0 "$alt"
    if [ -n "$key" ]; then
      env_set "${p}_STREAM_KEY" "$key"; env_set "${p}_ENABLED" 1
    else
      env_set "${p}_ENABLED" 0
      warn "%s ohne Key — ausgeschaltet gelassen." "$name"
    fi
  else
    env_set "${p}_ENABLED" 0
  fi
}
f_restream(){
  erklaere "Restream heisst: der TikTok-Stream wird gleichzeitig auf deine eigenen Kanaele gesendet. Der Stream-Key kommt von der jeweiligen Plattform (Kick: Creator-Dashboard → Stream Key; Twitch: Creator Dashboard → Einstellungen → Stream; YouTube: Studio → Livestream). Er ist ein Geheimnis und laesst sich nicht erzeugen. Ohne Key bleibt das Ziel aus."
  if [ "$MODUS" = "gefuehrt" ]; then
    erklaere "Wichtig zur Last: sobald ein zweites Ziel dazukommt, muss ffmpeg umkodieren (Transcode) — das kostet ein Vielfaches an CPU. Ein Ziel ohne Transcode laeuft selbst auf schwacher Hardware."
    restream_ziel KICK    "Kick"    "Kick ist das primaere Ziel: kein Transcode noetig, wenn es allein laeuft."
    restream_ziel TWITCH  "Twitch"  "Twitch begrenzt die Bitrate haerter als Kick — bei Problemen RESTREAM_BITRATE_K senken."
    restream_ziel YOUTUBE "YouTube" "YouTube braucht am laengsten, bis es 'live' meldet (bis zu einer Minute). Das ist normal und kein Fehler."
  else
    # Ein Ziel ohne Key bleibt aus — eines MIT Key wird nicht angefasst.
    for p in KICK TWITCH YOUTUBE; do [ -n "$(env_get "${p}_STREAM_KEY")" ] || env_set "${p}_ENABLED" 0; done
  fi
  return 0
}
z_restream(){
  local an="" p
  for p in KICK TWITCH YOUTUBE; do [ "$(env_get "${p}_ENABLED")" = 1 ] && an="$an $p"; done
  if [ -n "$an" ]; then printf '%s' "${an# }"; else t 'keine'; fi
}

P_PROFIL="bleibt"
f_profil(){
  # Vorgabe bei bestehender .env: NICHTS anfassen. Ein zweiter Lauf, der
  # handgestellte Werte (RESTREAM_BITRATE_K=4500) auf "Vorgaben" zuruecksetzt,
  # weil niemand gefragt wurde, waere genau der stille Schaden, den ein
  # unbeaufsichtigter Lauf nie anrichten darf.
  local vor="bleibt"
  [ -f "$ENVF" ] || vor="vorgabe"
  if [ ! -f "$ENVF" ] && { [ "$IST_PI" = 1 ] || [ "${RAM_MB:-0}" -lt 4000 ] || [ "${KERNE:-8}" -lt 4 ]; }; then
    vor="sparsam"
    erklaere "Diese Maschine ist klein. Die Vorgaben des Bots sind auf einen 8-Kern-Server gemuenzt; unveraendert fuehrt das hier zu abgebrochenen Aufnahmen und stotternden Restreams. Das sparsame Profil setzt: nur ein Restream-Ziel, 3500 kbit statt 6000, je ein ffmpeg-Thread fuer Aufnahme und Hintergrund, hoechstens eine Transkription gleichzeitig."
  fi
  frage_wahl P_PROFIL "Leistungsprofil?" "$vor" \
    bleibt  "unveraendert lassen (was in der .env steht, bleibt)" \
    vorgabe "Vorgaben des Bots (Server mit 4+ Kernen)" \
    sparsam "sparsam (Pi, kleine VPS: ein Ziel, 3500 kbit, je ein Thread)"
  if [ "$P_PROFIL" = "sparsam" ]; then
    env_set RESTREAM_SINGLE 1
    env_set RESTREAM_MAX_CONCURRENT 1
    env_set RESTREAM_BITRATE_K 3500
    env_set FFMPEG_THREADS_RECORD 1
    env_set FFMPEG_THREADS_BG 1
    env_set WHISPER_MAX_CONCURRENT 1
    env_set WORKER_COUNT 2
  elif [ "$P_PROFIL" = "bleibt" ]; then
    for _k in RESTREAM_SINGLE RESTREAM_MAX_CONCURRENT RESTREAM_BITRATE_K \
      FFMPEG_THREADS_RECORD FFMPEG_THREADS_BG WHISPER_MAX_CONCURRENT WORKER_COUNT; do plan_weg "$_k"; done
  else
    env_zuruecksetzen RESTREAM_SINGLE RESTREAM_MAX_CONCURRENT RESTREAM_BITRATE_K \
      FFMPEG_THREADS_RECORD FFMPEG_THREADS_BG WHISPER_MAX_CONCURRENT WORKER_COUNT
  fi
  return 0
}
z_profil(){
  case "$P_PROFIL" in sparsam) t 'sparsam';; vorgabe) t 'Vorgaben';; *) t 'unveraendert';; esac
}

P_DB="sqlite"
f_datenbank(){
  local vor="sqlite"
  [ "$(env_get DB_BACKEND | tr 'A-Z' 'a-z')" = "mariadb" ] && vor="mariadb"
  [ "$MODUS" = "gefuehrt" ] && erklaere "Datenbank: standardmaessig SQLite — eine Datei, kein Dienst, kein Passwort, und bis in den sechsstelligen Zeilenbereich schnell genug. MariaDB lohnt erst, wenn mehrere Rechner auf dieselben Daten sollen."
  frage_wahl P_DB "Welche Datenbank?" "$vor" \
    sqlite  "SQLite (eine Datei, empfohlen)" \
    mariadb "MariaDB (lokaler Server, wird eingerichtet)"
  if [ "$P_DB" = "mariadb" ]; then
    local pw
    frage_geheimnis pw "Passwort fuer den Datenbank-Nutzer 'nightcrawler'" 1 24 0 "$(env_get MARIADB_PASSWORD)"
    [ -z "$pw" ] && pw="$(erzeuge_passwort 24)"
    env_set DB_BACKEND mariadb
    env_set MARIADB_HOST 127.0.0.1
    env_set MARIADB_DB nightcrawler
    env_set MARIADB_USER nightcrawler
    env_set MARIADB_PASSWORD "$pw"
    OPT_AUS="$(printf '%s' "$OPT_AUS" | sed 's/[[:space:]]*PyMySQL//')"
  else
    # Zurueck auf SQLite: die MariaDB-Zugangsdaten bleiben in der .env stehen
    # (sie schaden dort nicht und sind beim Zurueckwechseln wieder da) —
    # entscheidend ist DB_BACKEND.
    plan_weg MARIADB_HOST; plan_weg MARIADB_DB; plan_weg MARIADB_USER; plan_weg MARIADB_PASSWORD
    env_zuruecksetzen DB_BACKEND
  fi
  return 0
}
z_datenbank(){ if [ "$P_DB" = "mariadb" ]; then t 'MariaDB (lokal)'; else printf 'SQLite'; fi; }

P_CROWDSEC="N"
f_crowdsec(){
  P_CROWDSEC="N"
  [ "$MODUS" = "gefuehrt" ] && [ "$SKIP_SYSTEM" = 0 ] && [ -n "$(nc_paketname crowdsec)" ] || return 0
  erklaere "CrowdSec ist die Abwehr: es liest Logs mit, erkennt Angriffsmuster und sperrt IPs. Das Dashboard zeigt Sperren und Angriffswellen an; der sentinel-Agent meldet Spitzen. Sinnvoll, sobald die Maschine aus dem Netz erreichbar ist."
  frage_ja "CrowdSec installieren?" N && P_CROWDSEC="J"
  return 0
}
z_crowdsec(){
  if [ -z "$(nc_paketname crowdsec)" ]; then t 'nicht ueber diesen Paketmanager — docs/CROWDSEC.md'
  elif [ "$P_CROWDSEC" = "J" ]; then t 'installieren'; else t 'aus'; fi
}

P_LLM="N"
llm_moeglich(){ [ "${RAM_MB:-0}" -ge 3000 ] && [ "$ARCH" = "x86_64" ] && [ "$OS" = "Linux" ] && [ "$PKG" != "apk" ]; }
f_llm(){
  P_LLM="N"
  [ "$MODUS" = "gefuehrt" ] || return 0
  erklaere "KI (AZRAEL): ohne jede Einrichtung laeuft sie ueber keylose freie Backends — das kostet nichts und braucht keinen Schluessel, ist aber langsamer und nicht immer erreichbar. Ein lokales llama.cpp antwortet in Millisekunden, kostet nichts und verlaesst die Maschine nie; es braucht rund 1 GB Platte und 2 GB RAM."
  if llm_moeglich; then
    frage_ja "llama.cpp lokal einrichten (Download ca. 1 GB)?" N && P_LLM="J"
  else
    info "Lokales LLM ausgelassen (nur fuer x86_64-Linux mit >= 3 GB RAM vorbereitet)."
    erklaere "Auf allen anderen Maschinen bleibt es bei den keylosen Backends. Ein Schluessel von enter.pollinations.ai (POLLINATIONS_API_KEY) macht sie spuerbar zuverlaessiger — eintragen laesst er sich jederzeit in der .env."
  fi
  return 0
}
z_llm(){ if [ "$P_LLM" = "J" ]; then t 'llama.cpp einrichten'; else t 'keylose Backends'; fi; }

P_AUTOSTART="keiner"; DIENST=""
f_autostart(){
  local vor="$NC_INIT"
  # Ohne root kein systemd-/OpenRC-Dienst; launchd ist Sache des Nutzers.
  case "$NC_INIT" in systemd|openrc) [ -n "$SUDO" ] || [ "$(id -u)" -eq 0 ] || vor="keiner";; esac
  case "$NC_INIT" in
    systemd) erklaere "Ein systemd-Dienst startet den Bot beim Booten, startet ihn nach einem Absturz neu und schreibt alles ins Journal (journalctl). Ohne ihn laeuft der Bot nur, solange deine SSH-Sitzung offen ist.";;
    openrc)  erklaere "Alpine startet Dienste mit OpenRC. Ein Dienst mit supervise-daemon startet den Bot beim Booten und nach einem Absturz neu.";;
    launchd) erklaere "macOS hat kein systemd. Das Gegenstueck heisst launchd: eine Datei in ~/Library/LaunchAgents, die den Bot beim Anmelden startet und neu startet, wenn er stirbt.";;
  esac
  if [ "$NC_INIT" = "keiner" ]; then
    P_AUTOSTART="keiner"
  else
    frage_wahl P_AUTOSTART "Autostart?" "$vor" \
      "$NC_INIT" "$(tf 'als Dienst (%s)' "$NC_INIT")" \
      keiner     "keiner — Start von Hand mit start.sh"
  fi
  if [ "$P_AUTOSTART" = "systemd" ] || [ "$P_AUTOSTART" = "openrc" ]; then
    frage_text DIENST "Name des Dienstes" "${DIENST:-${VORHANDEN:-nightcrawler}}"
    [ -n "$DIENST" ] || P_AUTOSTART="keiner"
  fi
  return 0
}
z_autostart(){
  case "$P_AUTOSTART" in
    systemd|openrc) tf '%s-Dienst %s' "$P_AUTOSTART" "$DIENST";;
    launchd) printf 'launchd';;
    *) t 'keiner (start.sh)';;
  esac
}

P_MOTD="N"
f_motd(){
  P_MOTD="N"
  [ -f "${QUELLE:-$ZIEL}/tools/motd.sh" ] || [ -f "$ZIEL/tools/motd.sh" ] || return 0
  [ "$NC_MOTD_WEG" = "keiner" ] && return 0
  erklaere "Die MOTD zeigt bei jedem SSH-Login den Zustand in einem Bild: Last, RAM, Platte, Dienst, Dashboard, Fehler heute, wie viele Streamer live sind und ob wirklich aufgenommen wird. Kostet einen Sekundenbruchteil pro Login. Sie ersetzt dabei die Standard-MOTD der Distribution — die kommt bei 'tools/motd.sh --uninstall' vollstaendig zurueck."
  # v4.1-W17: gehoert zur Standard-Einrichtung. Im gefuehrten Lauf weiterhin
  # eine Frage (mit Vorgabe J), im Express- und im unbeaufsichtigten Lauf
  # kommentarlos AN — vorher blieb sie dort ganz aus, obwohl sie nichts kostet
  # und das erste ist, was der Betreiber nach einem Login sieht.
  if [ "$MODUS" != "gefuehrt" ] || frage_ja "Status-MOTD beim Login einrichten?" J; then P_MOTD="J"; fi
  return 0
}
z_motd(){
  if [ "$NC_MOTD_WEG" = "keiner" ]; then t 'auf diesem System nicht moeglich'
  elif [ "$P_MOTD" = "J" ]; then tf 'einrichten (%s)' "$NC_MOTD_WEG"; else t 'aus'; fi
}

P_TOTMANN="N"
f_totmann(){
  P_TOTMANN="N"
  [ "$P_AUTOSTART" = "systemd" ] || return 0
  erklaere "Stirbt der Prozess ganz — OOM-Killer, kaputter Build, Absturz beim Start — sagt dir das sonst NIEMAND. Die Totmann-Meldung schickt bei jedem Ausfall die letzten Logzeilen per Telegram oder Discord."
  frage_ja "Totmann-Meldung einrichten?" J && P_TOTMANN="J"
  return 0
}
z_totmann(){
  if [ "$P_AUTOSTART" != "systemd" ]; then t 'nur mit systemd-Dienst'
  elif [ "$P_TOTMANN" = "J" ]; then t 'einrichten'; else t 'aus'; fi
}

# v4.2-W127: Prometheus/Grafana. Nur auf Nachfrage oder per Schalter: es
# bringt Pakete und einen weiteren Dienst mit, und das ist keine
# Nebenwirkung, die eine Installation ungefragt haben darf.
OPT_BEOBACHTUNG="${OPT_BEOBACHTUNG:-}"
P_BEOBACHTUNG="N"; P_GRAFANA="N"
f_beobachtung(){
  P_BEOBACHTUNG="N"; P_GRAFANA="N"
  [ "$P_AUTOSTART" = "systemd" ] || return 0
  [ -f "${QUELLE:-$ZIEL}/tools/observability.sh" ] || [ -f "$ZIEL/tools/observability.sh" ] || return 0
  if [ -n "$OPT_BEOBACHTUNG" ]; then
    P_BEOBACHTUNG="J"; [ "$OPT_BEOBACHTUNG" = "grafana" ] && P_GRAFANA="J"
    return 0
  fi
  [ "$MODUS" = "gefuehrt" ] || return 0
  erklaere "Prometheus sammelt die Kennzahlen des Bots (/metrics) und haelt sie 30 Tage — Verlauf statt Momentaufnahme — und prueft zehn Alarmregeln: Bot weg, Neustart im Kreis, Platte voll, Event-Loop haengt. Laeuft nur auf 127.0.0.1. Grafana zeigt das als Diagramme im Browser; auf Debian/Ubuntu wird dafuer die offizielle Paketquelle apt.grafana.com eingetragen."
  frage_ja "Prometheus einrichten (Verlauf und Alarme)?" N && P_BEOBACHTUNG="J"
  [ "$P_BEOBACHTUNG" = "J" ] && frage_ja "Grafana dazu (Diagramme im Browser)?" N && P_GRAFANA="J"
  return 0
}
z_beobachtung(){
  if [ "$P_AUTOSTART" != "systemd" ]; then t 'nur mit systemd-Dienst'
  elif [ "$P_GRAFANA" = "J" ]; then t 'Prometheus und Grafana'
  elif [ "$P_BEOBACHTUNG" = "J" ]; then printf 'Prometheus'; else t 'aus'; fi
}

# ── v4.2-W129: Nutzungsprofil und Expertenmodus ──────────────
# Ein Nutzungsprofil ist eine Datei unter deploy/profile/ mit Schaltern, die
# es im Bot gibt (der Vertrag haelt jeden Namen gegen .env.example). Es steht
# NEBEN dem Leistungsprofil oben: das regelt, wie viel die Maschine traegt,
# dieses, was der Bot tun soll — ihre Schalter ueberschneiden sich nicht.
#
# Beim Wechsel zaehlt nur das gewaehlte Profil: was ein ANDERES Profil setzt,
# kommt auf die Vorgabe des Bots zurueck. Sonst behielte, wer von "minimal" auf
# "ki" wechselt, CLIP_ENABLED=0 aus dem alten Profil — und fragte sich, warum
# keine Clips kommen.
PROFILE_DIR=""
for _p in "$ZIEL/deploy/profile" "${QUELLE:+$QUELLE/deploy/profile}"; do
  [ -n "$_p" ] && [ -d "$_p" ] && { PROFILE_DIR="$_p"; break; }
done
profil_schalter(){ # profil_schalter NAME -> "KEY=WERT" je Zeile, ohne Kommentare
  grep -E '^[A-Z][A-Z0-9_]*=' "$PROFILE_DIR/$1.env" | sed -E 's/[[:space:]]+#.*$//'
}
P_NUTZUNG="keins"
f_nutzung(){
  P_NUTZUNG="keins"
  if [ -z "$PROFILE_DIR" ]; then
    # Ohne Checkout neben dem Installer gibt es die Profile in DIESER Phase
    # noch nicht — der Klon kommt spaeter. Still uebergehen hiesse: der
    # Betreiber haelt das Profil fuer gesetzt (Codex, PR #168).
    if [ -n "$OPT_PROFIL" ]; then
      fehler "--profile braucht deploy/profile/ — den Installer aus einem Checkout starten: git clone …, dann bash tools/installer.sh --profile %s" "$OPT_PROFIL"
      exit 1
    fi
    return 0
  fi
  if [ -n "$OPT_PROFIL" ]; then
    P_NUTZUNG="$OPT_PROFIL"
  elif [ "$MODUS" = "gefuehrt" ]; then
    erklaere "Ein Nutzungsprofil setzt eine Handvoll Schalter auf einmal — was der Bot von sich aus tut. Es laesst alles andere stehen, und im naechsten Schritt bleibt jeder Wert einzeln aenderbar."
    frage_wahl P_NUTZUNG "Nutzungsprofil?" keins \
      keins    "keins — die Schalter bleiben, wie sie sind" \
      minimal  "minimal — nur ueberwachen und aufnehmen, kein Restream, keine KI" \
      restream "voller Restream — Kick, Twitch, YouTube, mit Overlay" \
      ki       "viel KI — AZRAEL hoert mit, antwortet und moderiert"
  fi
  [ "$P_NUTZUNG" = "keins" ] && return 0
  if [ ! -f "$PROFILE_DIR/$P_NUTZUNG.env" ]; then
    fehler "Unbekanntes Nutzungsprofil: %s (minimal, restream, ki)" "$P_NUTZUNG"
    exit 1
  fi
  local f k v alle=""
  for f in "$PROFILE_DIR"/*.env; do
    [ "$f" = "$PROFILE_DIR/$P_NUTZUNG.env" ] && continue
    alle="$alle $(profil_schalter "$(basename "$f" .env)" | cut -d= -f1)"
  done
  # Erst die fremden auf die Vorgabe, dann die eigenen setzen — ein Schalter,
  # der in beiden steht, endet so auf dem Wert des gewaehlten Profils.
  # shellcheck disable=SC2086  # Namen ohne Leerzeichen
  env_zuruecksetzen $alle
  while IFS='=' read -r k v; do
    [ -n "$k" ] && env_set "$k" "$v"
  done < <(profil_schalter "$P_NUTZUNG")
  pakete_nach_plan
  return 0
}
z_nutzung(){
  case "$P_NUTZUNG" in
    minimal) t 'minimal';; restream) t 'voller Restream';; ki) t 'viel KI';;
    *) t 'keins (Schalter unveraendert)';;
  esac
}

# Expertenmodus: jede Variable aus .env.example, nicht nur die abgefragten.
# --set NAME=WERT geht immer (auch unbeaufsichtigt); --expert oeffnet dazu
# eine Suche im gefuehrten Lauf. Nur Namen aus der Vorlage — ein Tippfehler
# im Namen landete sonst als Zeile in der .env, die der Bot nie liest, und
# der Betreiber hielte die Einstellung fuer gesetzt.
P_EXPERTE=0
experte_bekannt(){ [ -n "$VORLAGE" ] && grep -qE "^#? ?$1=" "$VORLAGE"; }
experte_zeigen(){ # experte_zeigen NAME -> "NAME  jetzt  (Vorgabe)" maskiert
  local k="$1" w vor
  w="$(env_get "$k")"; vor="$(sed -n "s/^[#[:space:]]*${k}=//p" "$VORLAGE" | head -1)"
  if [ -n "$w" ] && printf '%s' "$k" | grep -qE "$GEHEIM_MUSTER"; then w="***"; fi
  printf '%-34s %s%s%s  %s(%s: %s)%s' "$k" "$TXT" "${w:-—}" "$R" "$FNT" "$(t 'Vorgabe')" "${vor:-—}" "$R"
}
f_experte(){
  P_EXPERTE=0
  local a k v
  if [ -z "$VORLAGE" ] && { [ -n "$OPT_SETZEN" ] || [ "$OPT_EXPERTE" = 1 ]; }; then
    # Ohne .env.example laesst sich kein Name pruefen — und jeder --set
    # scheiterte sonst mit "Tippfehler?", obwohl der Name stimmt.
    fehler "--set und --expert brauchen .env.example — den Installer aus einem Checkout starten (git clone …, dann bash tools/installer.sh)."
    exit 1
  fi
  while IFS= read -r a; do
    [ -n "$a" ] || continue
    k="${a%%=*}"; v="${a#*=}"
    if [ "$k" = "$a" ] || ! printf '%s' "$k" | grep -qE '^[A-Z][A-Z0-9_]*$'; then
      fehler "--set erwartet NAME=WERT: %s" "$a"; exit 1
    fi
    if ! experte_bekannt "$k"; then
      fehler "%s steht nicht in .env.example — Tippfehler? Der Bot liest diesen Namen nicht." "$k"; exit 1
    fi
    env_set "$k" "$v"; P_EXPERTE=$((P_EXPERTE+1))
  done <<< "$OPT_SETZEN"
  # Auch ohne --expert: ein --set LIVE_REACT_ENABLED=1 verlangt sein Paket.
  [ "$OPT_EXPERTE" = 1 ] && [ "$MODUS" = "gefuehrt" ] && [ -n "$VORLAGE" ] || { pakete_nach_plan; return 0; }
  # Eigene Namen fuer die Antworten (_ex_*): frage_text schreibt per
  # printf -v in die genannte Variable, hat aber selbst ein lokales "a" — ein
  # Aufruf "frage_text a" traf DESSEN a, und jede Eingabe ging verloren
  # (gefunden im Terminaltest W129).
  local _ex_such _ex_nr _ex_wert
  erklaere "Expertenmodus: jede Variable aus .env.example. Einen Namen oder ein Stichwort eingeben (z. B. WHISPER oder BITRATE), dann die Nummer. Leere Eingabe beendet."
  local -a treffer=()
  while :; do
    frage_text _ex_such "Variable oder Stichwort" ""
    [ -n "$_ex_such" ] || break
    mapfile -t treffer < <(grep -oE "^#? ?[A-Z][A-Z0-9_]*=" "$VORLAGE" | sed -E 's/^#? ?//; s/=$//' \
                           | grep -i -- "$_ex_such" | head -15)
    if [ "${#treffer[@]}" -eq 0 ]; then warn "Kein Treffer fuer %s." "$_ex_such"; continue; fi
    local i=0
    for k in "${treffer[@]}"; do i=$((i+1)); printf '   %s%2d%s  %s\n' "$TXT" "$i" "$R" "$(experte_zeigen "$k")"; done
    frage_text _ex_nr "Nummer (Enter = neue Suche)" ""
    [[ "$_ex_nr" =~ ^[0-9]+$ ]] && [ "$_ex_nr" -ge 1 ] && [ "$_ex_nr" -le "${#treffer[@]}" ] || continue
    k="${treffer[$((_ex_nr-1))]}"
    info "%s" "$(experte_zeigen "$k")"
    frage_text _ex_wert "Neuer Wert (- = Vorgabe, Enter = behalten)" ""
    case "$_ex_wert" in
      "") ;;
      -)  env_zuruecksetzen "$k"; P_EXPERTE=$((P_EXPERTE+1));;
      *)  env_set "$k" "$_ex_wert"; P_EXPERTE=$((P_EXPERTE+1));;
    esac
  done
  pakete_nach_plan
  return 0
}
z_experte(){
  if [ "$P_EXPERTE" -gt 0 ]; then tf '%s Wert(e) von Hand' "$P_EXPERTE"
  else t 'keine'; fi
}

# Die Reihenfolge ist die der Zusammenfassung. Abschnitte mit Ueberschrift.
# Neue Punkte kommen ans ENDE: die Nummern der bestehenden sind die Eingabe
# der Aenderungsschleife, und wer "8" fuer das Leistungsprofil kennt, soll
# nach einem Update nicht ploetzlich die Datenbank aendern.
PUNKTE=(python system pypakete telegram dashboard discord restream profil datenbank crowdsec llm autostart motd totmann beobachtung nutzung experte)
punkt_titel(){
  case "$1" in
    python) t 'Python';; system) t 'Systempakete';; pypakete) t 'Python-Pakete';;
    telegram) printf 'Telegram';; dashboard) printf 'Dashboard';; discord) printf 'Discord';;
    restream) t 'Restream-Ziele';; profil) t 'Leistungsprofil';; datenbank) t 'Datenbank';;
    crowdsec) printf 'CrowdSec';; llm) t 'Lokales LLM';; autostart) printf 'Autostart';;
    motd) printf 'MOTD';; totmann) t 'Totmann-Meldung';;
    beobachtung) t 'Beobachtung';; nutzung) t 'Nutzungsprofil';; experte) t 'Einzelwerte';;
  esac
}
punkt_fragen(){
  case "$1" in
    telegram)  abschnitt "Telegram — der Pflichtteil";;
    dashboard) abschnitt "Dashboard";;
    discord)   printf '%s' "$OPT_AUS" | grep -qi discord || abschnitt "Discord";;
    restream)  abschnitt "Restream-Ziele";;
    profil)    abschnitt "Leistungsprofil";;
  esac
  "f_$1"
}
for p in "${PUNKTE[@]}"; do punkt_fragen "$p"; done

# ═══════════════════════════════════════════════════════════════════════════
# PHASE C — ZUSAMMENFASSUNG (jeder Punkt aenderbar, dazu der .env-Diff)
# ═══════════════════════════════════════════════════════════════════════════
kopf "Zusammenfassung"
zusammenfassung(){
  local i=0 p
  info "Zielverzeichnis: %s" "$ZIEL"
  for p in "${PUNKTE[@]}"; do
    i=$((i+1))
    printf '   %s%2d%s  %-18s %s\n' "$TXT" "$i" "$R" "$(punkt_titel "$p")" "$("z_$p")"
  done
  env_bauen "$ENV_BASIS" "$ARBEIT/env.neu"
  # Neu angelegt: verglichen wird mit der VORLAGE — gegen eine leere Datei
  # stuende hier jede der rund 500 Vorgabezeilen.
  local d; d="$(env_diff "${ENVF}" "$ARBEIT/env.neu")"
  [ -f "$ENVF" ] || d="$(env_diff "$ENV_BASIS" "$ARBEIT/env.neu")"
  printf '\n'
  if [ ! -f "$ENVF" ]; then
    info ".env wird neu angelegt — gegenueber der Vorlage gesetzt (Geheimnisse maskiert):"
  elif [ -z "$d" ]; then
    gut ".env: keine Aenderung."
  else
    info ".env-Aenderungen gegenueber dem Bestand (Geheimnisse maskiert):"
  fi
  [ -n "$d" ] && printf '%s\n' "$d" | sed 's/^/      /'
  return 0
}
trocken_ende(){ printf '\n'; info "Trockenlauf beendet — nichts wurde veraendert."; exit 0; }
while :; do
  zusammenfassung
  # Im Trockenlauf ist die Aenderungsschleife im gefuehrten Lauf trotzdem da:
  # sie ist genau das, was man vor dem echten Lauf ausprobieren will. Nur
  # "Enter" fuehrt dann nicht aus, sondern endet.
  [ "$MODUS" = "unattended" ] && { [ "$TROCKEN" = 1 ] && trocken_ende; break; }
  if [ "$MODUS" = "express" ]; then
    [ "$TROCKEN" = 1 ] && trocken_ende
    frage_ja "So ausfuehren?" J && break
    info "Abgebrochen — nichts veraendert."; exit 0
  fi
  printf '\n  %s?%s %s ' "$BR" "$R" "$(t 'Nummer zum Aendern, Enter = ausfuehren, a = abbrechen:')"
  wahl=""; lies wahl
  case "$wahl" in
    "") [ "$TROCKEN" = 1 ] && trocken_ende; break;;
    a|A|q|Q) info "Abgebrochen — nichts veraendert."; exit 0;;
    *)
      if [[ "$wahl" =~ ^[0-9]+$ ]] && [ "$wahl" -ge 1 ] && [ "$wahl" -le "${#PUNKTE[@]}" ]; then
        punkt_fragen "${PUNKTE[$((wahl-1))]}"
      else
        warn "Bitte eine Zahl von 1 bis %s." "${#PUNKTE[@]}"
      fi;;
  esac
done

# ═══════════════════════════════════════════════════════════════════════════
# PHASE D — AUSFUEHRUNG
# ═══════════════════════════════════════════════════════════════════════════
python_ueber_uv(){
  erklaere "Rueckfallweg ohne Paketquellen: uv (astral.sh) laedt eine fertige, eigenstaendige CPython-Fassung in dein Home — ohne root, ohne das System-Python anzufassen. Genau der Weg fuer Debian 12 und Raspberry Pi OS."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  lauf uv python install 3.13
}
kopf "Ausfuehrung: System und Python"

# ── Python ───────────────────────────────────────────────────
if [ "$P_PYWEG" != "vorhanden" ]; then
  case "$P_PYWEG" in
    paket)
      # Erst auffrischen, DANN waehlen: auf einem frischen Image kennt apt
      # ohne update kein einziges Paket, und die Wahl davor waere geraten.
      if _af="$(nc_auffrischbefehl)"; then
        # shellcheck disable=SC2086  # fester Befehl aus lib/system.sh
        als_root $_af || true
      fi
      _pp=""
      for _k in $(nc_paketname python); do nc_paket_verfuegbar "$_k" && { _pp="$_k"; break; }; done
      if [ -n "$_pp" ]; then
        _venvp=""; [ "$PKG" = "apt" ] && _venvp="$(nc_venvpaket "${_pp#python}")"
        # shellcheck disable=SC2046,SC2086
        als_root $(nc_installbefehl $_pp $_venvp) || warn "Mindestens ein Paket liess sich nicht installieren."
      fi
      if [ -z "$_pp" ] || [ -z "$(finde_python || true)" ]; then
        warn "Kein Python >= %s.%s aus den Paketquellen — weiter mit uv." "$PY_MIN_MAJOR" "$PY_MIN_MINOR"
        python_ueber_uv
      fi;;
    deadsnakes)
      als_root apt-get update -qq && als_root apt-get install -y software-properties-common
      als_root add-apt-repository -y ppa:deadsnakes/ppa
      als_root apt-get update -qq && als_root apt-get install -y python3.12 python3.12-venv;;
    uv)
      python_ueber_uv;;
  esac
  PY="$(finde_python || true)"
  if [ -z "$PY" ]; then
    fehler "Ohne Python >= %s.%s geht es nicht weiter." "$PY_MIN_MAJOR" "$PY_MIN_MINOR"
    info "Wege: %s" "apt install python3.13  |  dnf install python3.13  |  brew install python@3.13  |  https://astral.sh/uv"
    exit 1
  fi
  gut "Python bereit: %s (%s)" "$PY" "$("$PY" -V 2>&1)"
fi

# ── Quelltext ────────────────────────────────────────────────
if [ "$ZIEL" = "$QUELLE" ]; then
  gut "Installation direkt im vorhandenen Verzeichnis — nichts zu kopieren."
elif [ -n "$QUELLE" ]; then
  mkdir -p "$ZIEL"
  info "Kopiere Quelltext nach %s" "$ZIEL"
  erklaere ".env, Datenbanken, Aufnahmen und Logs werden dabei NIE angefasst — sie gehoeren dir, nicht dem Build."
  # v4.2-W100: die Liste stand zweimal da (rsync und tar) und wich von der
  # des Auslieferungsarchivs ab. Gemessen an einer Installation aus einem
  # Arbeitsbaum: .coverage, .pytest_cache/, .ruff_cache/ und ein 4-MB-
  # Release-ZIP wanderten mit. Nichts davon ist falsch, aber nichts davon
  # gehoert in einen Bestand, der ausgeliefert laeuft — und ein zweiter
  # Caches-Satz mit fremden mtimes ist der Stoff, aus dem die .pyc-Falle aus
  # CLAUDE.md gemacht ist.
  #
  # EINE Liste, von beiden Wegen benutzt. Dieselbe Lehre wie bei den zwei
  # Ordner-Aufloesungen in W98: zwei Listen fuer denselben Zweck laufen
  # auseinander, und die Abweichung faellt erst im Bestand auf.
  AUS_KOPIE=(
    '.git' '.venv' 'recordings' 'logs' '*.db' '.env'
    '__pycache__' '.pytest_cache' '.ruff_cache' '.mypy_cache' '.coverage'
    '*.zip' '*.pyc' 'AUSLIEFERUNG.json'
  )
  if have rsync; then
    RS_ARGS=(); for m in "${AUS_KOPIE[@]}"; do RS_ARGS+=(--exclude "$m"); done
    rsync -a "${RS_ARGS[@]}" "$QUELLE"/ "$ZIEL"/
  else
    TAR_ARGS=(); for m in "${AUS_KOPIE[@]}"; do TAR_ARGS+=(--exclude="$m"); done
    (cd "$QUELLE" && tar cf - "${TAR_ARGS[@]}" .) | (cd "$ZIEL" && tar xf -)
  fi
  gut "Quelltext liegt in %s" "$ZIEL"
else
  if [ "$BESTAND" = 1 ]; then
    if [ -d "$ZIEL/.git" ] && frage_ja "Auf den neuesten Stand bringen (git pull)?" J; then
      git -C "$ZIEL" pull --ff-only || warn "git pull fehlgeschlagen — lokale Aenderungen? Quelltext bleibt wie er ist."
    fi
  else
    have git || { fehler "git fehlt und wird zum Holen des Quelltexts gebraucht."; exit 1; }
    info "Klone %s (Zweig %s)" "$REPO_URL" "$BRANCH"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$ZIEL"
    gut "Quelltext geholt."
  fi
fi
cd "$ZIEL"
# Nach einem frischen Klon gibt es die Vorlage erst jetzt.
[ -n "$ENV_BASIS" ] || { [ -f "$ZIEL/.env.example" ] && ENV_BASIS="$ZIEL/.env.example"; }

# ── Systempakete: nur was fehlt ──────────────────────────────
abschnitt "Systempakete"
if [ "$P_SYSTEM" = "J" ]; then
  SYS_PAKETE=""
  for w in ffmpeg streamlink yt-dlp git curl sqlite3 unzip; do
    have "$w" && continue
    for _k in $(nc_paketname "$w"); do
      if nc_paket_verfuegbar "$_k" || nc_quellen_leer; then SYS_PAKETE="$SYS_PAKETE $_k"; break; fi
    done
  done
  # Das venv-Paket muss zur GEWAEHLTEN Python-Fassung passen — sonst
  # scheitert python -m venv mit "ensurepip is not available", und das
  # ist die mit Abstand haeufigste Sackgasse auf Debian.
  if [ "$PKG" = "apt" ] && ! "$PY" -c 'import ensurepip' 2>/dev/null; then
    PYV="$("$PY" -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
    SYS_PAKETE="$SYS_PAKETE $(nc_venvpaket "$PYV")"
  fi
  if [ -n "$SYS_PAKETE" ]; then
    if _af="$(nc_auffrischbefehl)"; then
      # shellcheck disable=SC2086
      als_root $_af || warn "Paketquellen liessen sich nicht auffrischen — versuche es trotzdem."
    fi
    # yt-dlp/streamlink aus alten Quellen sind oft zu alt; fehlen sie, holt
    # der pip-Schritt die aktuelle Fassung ins venv. Deshalb kein Abbruch.
    # shellcheck disable=SC2046,SC2086
    als_root $(nc_installbefehl $SYS_PAKETE) || warn "Mindestens ein Paket fehlte in den Quellen — es wird spaeter im venv ergaenzt."
  else
    gut "Nichts zu tun — alles vorhanden."
  fi
elif [ "$SKIP_SYSTEM" = 1 ]; then
  warn "Uebersprungen (--skip-system oder kein Paketmanager)."
  info "Bitte selbst bereitstellen: ffmpeg streamlink yt-dlp git curl sqlite3"
fi
for prog in ffmpeg streamlink yt-dlp; do
  if have "$prog"; then gut "%s: %s" "$prog" "$(command -v "$prog")"
  elif [ "$prog" = ffmpeg ]; then warn "%s fehlt — ohne ihn laeuft KEINE Aufnahme und kein Restream." "$prog"
  else warn "%s fehlt — wird spaeter im venv ergaenzt." "$prog"; fi
done

# ── Python-Pakete: nur was fehlt ─────────────────────────────
abschnitt "Python-Pakete"
erklaere "Alles Weitere lebt in einer virtuellen Umgebung unter .venv/ — ein eigener Ordner mit eigenem Python und eigenen Bibliotheken. Damit kann keine Installation hier das System-Python beschaedigen und umgekehrt."
if [ -x "$VPY" ] && "$VPY" -c 'import sys;raise SystemExit(0 if sys.version_info>=(3,12) else 1)' 2>/dev/null; then
  gut "Vorhandene Umgebung wird weiterbenutzt: %s" "$VENV"
else
  [ -d "$VENV" ] && { warn "Vorhandenes .venv passt nicht (zu altes Python) — wird neu angelegt."; rm -rf "$VENV"; }
  info "Lege virtuelle Umgebung an (%s)" "$PY"
  "$PY" -m venv "$VENV" || {
    fehler "venv liess sich nicht anlegen."
    info "Meist fehlt das Paket python3-venv:  %s" "sudo apt install python3-venv"; exit 1; }
  gut "Umgebung angelegt."
fi

REQ_TMP="$ARBEIT/requirements.txt"
# Paketnamen aus requirements.txt loesen: Kommentare weg, Leerzeilen weg,
# abgewaehlte Pakete weg (Vergleich case-insensitiv, - und _ gleichwertig).
NC_AUS="$OPT_AUS" awk '
  { line=$0; sub(/#.*/,"",line); gsub(/^[[:space:]]+|[[:space:]]+$/,"",line)
    if (line=="") next
    name=line; sub(/[;<>=!~[].*/,"",name); gsub(/[[:space:]]/,"",name)   # ; trennt den Umgebungsmarker ab
    key=tolower(name); gsub(/_/,"-",key)
    if (!(key in aus)) print line }
  BEGIN{ n=split(tolower(ENVIRON["NC_AUS"]), a, /[[:space:]]+/)
         for(i=1;i<=n;i++){ k=a[i]; gsub(/_/,"-",k); if(k!="") aus[k]=1 } }
' requirements.txt > "$REQ_TMP"
# v4.2-W124: erst abgleichen, dann installieren. Ein zweiter Lauf auf einem
# vollstaendigen venv rief bisher pip ueber alle Pakete auf — Minuten fuer
# nichts, und mit Netz als Voraussetzung. tools/anforderungen.py ist derselbe
# Abgleich, den tools/update.sh benutzt.
_fehlt=""
if _tab="$("$VPY" "$ZIEL/tools/anforderungen.py" --datei "$REQ_TMP" 2>/dev/null)"; then
  _fehlt="$(printf '%s\n' "$_tab" | awk -F '\t' '$1=="fehlt"||$1=="alt"{print $2}' | tr '\n' ' ')"
  if [ -z "${_fehlt// /}" ]; then
    gut "Python-Pakete vollstaendig — nichts zu installieren."
  fi
else
  _fehlt="(Abgleich nicht moeglich)"
fi
if [ -n "${_fehlt// /}" ]; then
  _anzahl="$(wc -l < "$REQ_TMP" | tr -d ' ')"
  if [ -n "$OPT_AUS" ]; then info "%s Pakete werden installiert, ausgelassen:%s" "$_anzahl" "$OPT_AUS"
  else info "%s Pakete werden installiert" "$_anzahl"; fi
  "$VPY" -m pip install --upgrade pip wheel >/dev/null 2>&1 || warn "pip liess sich nicht aktualisieren — weiter mit der vorhandenen Fassung."
  info "pip install laeuft — das dauert je nach Verbindung 1 bis 15 Minuten."
  if ! "$VPY" -m pip install -r "$REQ_TMP"; then
    fehler "Mindestens ein Paket liess sich nicht installieren."
    erklaere "Haeufigste Ursachen: kein Compiler fuer ein Paket ohne fertiges Rad (dann: sudo apt install build-essential python3-dev), oder eine abgerissene Verbindung. Wiederholen ist gefahrlos: .venv/bin/pip install -r requirements.txt"
    exit 1
  fi
fi
# streamlink/yt-dlp aus den Systemquellen sind oft zu alt fuer TikTok. Im venv
# sind sie immer aktuell und haben Vorrang, weil .venv/bin frueher im PATH steht.
have streamlink || [ -x "$VENV/bin/streamlink" ] || "$VPY" -m pip install streamlink || warn "streamlink liess sich nicht nachinstallieren."
have yt-dlp     || [ -x "$VENV/bin/yt-dlp" ]     || "$VPY" -m pip install yt-dlp     || warn "yt-dlp liess sich nicht nachinstallieren."
gut "Python-Pakete stehen."

# ═══════════════════════════════════════════════════════════════════════════
kopf "Ausfuehrung: Konfiguration und Bausteine"

# ── .env: nur bei Abweichung schreiben, vorher sichern ───────
erklaere "Alle Einstellungen leben in einer einzigen Datei: .env. Sie enthaelt Bot-Token, Stream-Keys und Cookies — deshalb bekommt sie Rechte 600 (nur du darfst lesen) und gehoert NIE in ein Archiv oder ein Repository."
env_bauen "$ENV_BASIS" "$ARBEIT/env.neu"
if [ -f "$ENVF" ] && cmp -s "$ENVF" "$ARBEIT/env.neu"; then
  gut ".env: keine Aenderung."
else
  if [ -f "$ENVF" ]; then
    SICHERUNG="$ENVF.bak.$(date +%Y%m%d-%H%M%S)"
    cp -p "$ENVF" "$SICHERUNG"
    gut "Vorhandene .env gesichert: %s" "$(basename "$SICHERUNG")"
  fi
  # Erst Rechte, dann Inhalt: die Datei ist keinen Augenblick lesbar.
  ( umask 077; cat "$ARBEIT/env.neu" > "$ENVF.neu" ) && mv "$ENVF.neu" "$ENVF"
  gut "Konfiguration geschrieben: %s (Rechte 600)" "$ENVF"
fi
chmod 600 "$ENVF"
[ -z "$(env_bisher BOT_TOKEN)" ] && merke "OFFEN: BOT_TOKEN in %s eintragen (von @BotFather)" "$ENVF"
[ -n "$(env_bisher DASHBOARD_TOKEN)" ] && merke "Dashboard-Token: steht in .env (DASHBOARD_TOKEN)"
[ "$P_ZUGANG" = "netz" ] && merke "SICHERHEIT: Dashboard lauscht auf 0.0.0.0 — Firewall setzen: %s" "$(nc_firewall_hinweis "$(env_bisher DASHBOARD_PORT)")"
[ "$P_PROFIL" = "sparsam" ] && merke "Leistungsprofil: sparsam (RESTREAM_SINGLE=1, Bitrate 3500)"
DASH_PORT="$(env_bisher DASHBOARD_PORT)"; DASH_PORT="${DASH_PORT:-8050}"

# ── MariaDB ──────────────────────────────────────────────────
if [ "$P_DB" = "mariadb" ]; then
  abschnitt "Datenbank"
  if ! have mariadb && ! have mysql && [ "$SKIP_SYSTEM" = 0 ]; then
    # shellcheck disable=SC2046
    als_root $(nc_installbefehl "$(nc_paketname mariadb)") || warn "MariaDB-Server liess sich nicht installieren."
    [ "$NC_INIT" = "systemd" ] && { als_root systemctl enable --now mariadb || true; }
    [ "$NC_INIT" = "openrc" ] && { als_root rc-update add mariadb default || true; als_root rc-service mariadb start || true; }
  fi
  if have mariadb || have mysql; then
    MYSQL_CLI="$(command -v mariadb || command -v mysql)"
    DBPW="$(env_bisher MARIADB_PASSWORD)"
    # Passwort ueber die Standardeingabe statt auf der Kommandozeile: ein
    # Passwort in argv steht in der Prozessliste und damit fuer JEDEN Nutzer
    # sichtbar. IF NOT EXISTS + ALTER USER: ein zweiter Lauf gleicht nur an.
    if printf 'CREATE DATABASE IF NOT EXISTS nightcrawler CHARACTER SET utf8mb4;\n%s\n%s\n%s\nFLUSH PRIVILEGES;\n' \
         "CREATE USER IF NOT EXISTS 'nightcrawler'@'localhost' IDENTIFIED BY '$(printf '%s' "$DBPW" | sed "s/'/''/g")';" \
         "ALTER USER 'nightcrawler'@'localhost' IDENTIFIED BY '$(printf '%s' "$DBPW" | sed "s/'/''/g")';" \
         "GRANT ALL PRIVILEGES ON nightcrawler.* TO 'nightcrawler'@'localhost';" \
       | ${SUDO:+$SUDO} "$MYSQL_CLI" 2>/dev/null; then
      gut "MariaDB eingerichtet (Datenbank und Nutzer 'nightcrawler')."
      merke "MariaDB: Nutzer nightcrawler, Passwort in .env (MARIADB_PASSWORD)"
    else
      warn "Datenbank liess sich nicht anlegen — DB_BACKEND steht auf mariadb; vor dem Start pruefen oder auf sqlite zuruecksetzen."
    fi
  else
    warn "Kein MariaDB-Client gefunden — DB_BACKEND steht auf mariadb; vor dem Start pruefen oder auf sqlite zuruecksetzen."
  fi
fi

# ── CrowdSec ─────────────────────────────────────────────────
if [ "$P_CROWDSEC" = "J" ]; then
  abschnitt "CrowdSec"
  if have cscli; then gut "CrowdSec installiert: %s" "$(cscli version 2>/dev/null | head -1)"
  else
    # shellcheck disable=SC2046
    als_root $(nc_installbefehl "$(nc_paketname crowdsec)") || warn "CrowdSec fehlt in den Quellen — siehe docs/CROWDSEC.md."
    have cscli && gut "CrowdSec installiert: %s" "$(cscli version 2>/dev/null | head -1)"
  fi
  merke "CrowdSec: installiert — Feinheiten in docs/CROWDSEC.md"
fi

# ── Reverse-Proxy + HTTPS ────────────────────────────────────
# v4.1-W17: Bis hierher endete der Installer beim Dashboard auf 127.0.0.1 und
# ueberliess den Rest der Anleitung. Genau dort brach der haeufigste Weg ab:
# wer die Oberflaeche von aussen wollte, oeffnete den Port statt einen Proxy
# davorzusetzen — und stand dann ohne TLS und ohne Zertifikat da. Der Log vom
# 30.08. zeigt das Ergebnis: Dashboard auf 0.0.0.0:8050, ohne Token, mit
# Fremdzugriffen im Journal. Der Proxy ist der Weg, der das ueberfluessig macht.
# Pakete: nginx certbot python3-certbot-nginx (apt/dnf/zypper) bzw.
# certbot-nginx (pacman/apk) — siehe nc_paketname in lib/system.sh.
if [ "$P_ZUGANG" = "proxy" ] && [ -n "$P_DOMAIN" ]; then
  abschnitt "Reverse-Proxy"
  if ! have nginx && [ "$SKIP_SYSTEM" = 0 ]; then
    # shellcheck disable=SC2046
    als_root $(nc_installbefehl nginx $(nc_paketname certbot-nginx)) \
      || warn "nginx/certbot liessen sich nicht installieren."
  fi
  if have nginx; then
    NGX="$(nc_nginx_ziel)"
    cat > "$ARBEIT/nginx.conf" <<NGXEOF
# NIGHTCRAWLER — erzeugt von tools/installer.sh
# certbot traegt die TLS-Zeilen selbst nach (--nginx).
server {
    listen 80;
    listen [::]:80;
    server_name ${P_DOMAIN};

    # Der Bot bindet auf 127.0.0.1 — der Port bleibt von aussen zu.
    location / {
        proxy_pass         http://127.0.0.1:${DASH_PORT};
        proxy_http_version 1.1;
        proxy_set_header   Host              \$host;
        proxy_set_header   X-Real-IP         \$remote_addr;
        proxy_set_header   X-Forwarded-For   \$proxy_add_x_forwarded_for;
        # Diese drei liest nc/oauthredirect.py, um die Rueckruf-Adresse zu
        # bauen. Fehlt X-Forwarded-Proto, baut der Bot http:// und Google
        # lehnt den OAuth-Rueckruf ab, BEVOR die Kontoauswahl erscheint.
        proxy_set_header   X-Forwarded-Proto \$scheme;
        proxy_set_header   X-Forwarded-Host  \$host;
        proxy_set_header   X-Forwarded-Port  \$server_port;
        # Server-sent events und lange Antworten (Log-Tail, KI-Streaming).
        proxy_buffering    off;
        proxy_read_timeout 300s;
    }
}
NGXEOF
    # Nach certbot steht in der Datei mehr als in der Vorlage (TLS-Zeilen).
    # Eine bestehende Datei mit "managed by Certbot" wird deshalb NICHT
    # ueberschrieben — das risse das Zertifikat wieder heraus.
    if [ -f "$NGX" ] && grep -q 'managed by Certbot' "$NGX" 2>/dev/null; then
      info "nginx-Datei traegt bereits das Zertifikat — bleibt unveraendert: %s" "$NGX"
    elif schreibe_systemdatei "$NGX" "$ARBEIT/nginx.conf"; then
      [ "$PKG" = "apt" ] && als_root ln -sf "$NGX" /etc/nginx/sites-enabled/nightcrawler
      if ${SUDO:+$SUDO} nginx -t >/dev/null 2>&1; then
        { [ "$NC_INIT" = "openrc" ] && als_root rc-service nginx reload; } \
          || als_root systemctl reload nginx 2>/dev/null || als_root systemctl restart nginx 2>/dev/null || true
        gut "nginx eingerichtet."
      else
        warn "nginx-Konfiguration fehlerhaft — bitte 'sudo nginx -t' pruefen."
      fi
    fi
    if [ "$P_CERT" = "J" ] && have certbot && ! grep -q 'managed by Certbot' "$NGX" 2>/dev/null; then
      erklaere "certbot holt jetzt das Zertifikat. Dafuer muss Port 80 dieser Maschine aus dem Internet erreichbar sein und die Domain hierher zeigen — sonst schlaegt die Pruefung fehl. Die Erneuerung laeuft danach von selbst per systemd-Timer."
      als_root certbot --nginx -d "$P_DOMAIN" --agree-tos --redirect -n \
            --register-unsafely-without-email \
        && gut "Zertifikat aktiv, HTTP leitet auf HTTPS um." \
        || warn "certbot fehlgeschlagen — Port 80 offen? Domain zeigt hierher? Erneut: sudo certbot --nginx -d %s" "$P_DOMAIN"
    fi
    # Steht danach KEIN Zertifikat in der nginx-Datei, darf die Adresse nicht
    # https behaupten — sonst zeigen alle OAuth-Rueckrufe ins Leere.
    if [ "$P_CERT" = "J" ] && ! grep -q 'managed by Certbot' "$NGX" 2>/dev/null; then
      : > "$PLAN_ENV"
      env_set PUBLIC_BASE_URL "http://${P_DOMAIN}"
      ENV_BASIS="$ENVF"; env_bauen "$ENV_BASIS" "$ARBEIT/env.neu"
      cat "$ARBEIT/env.neu" > "$ENVF"; chmod 600 "$ENVF"
      warn "Kein Zertifikat aktiv — PUBLIC_BASE_URL steht auf http://%s, bis certbot gelaufen ist." "$P_DOMAIN"
      merke "OFFEN: Zertifikat holen (sudo certbot --nginx -d %s), dann PUBLIC_BASE_URL auf https://%s setzen" "$P_DOMAIN" "$P_DOMAIN"
    fi
    if grep -q 'managed by Certbot' "$NGX" 2>/dev/null; then
      merke "Reverse-Proxy: https://%s → 127.0.0.1:%s (nginx + certbot)" "$P_DOMAIN" "$DASH_PORT"
      merke "PUBLIC_BASE_URL und TRUSTED_PROXIES sind gesetzt — die OAuth-Rueckrufe stimmen damit ohne weitere Pflege."
    fi
  fi
fi

# ── Lokales LLM ──────────────────────────────────────────────
if [ "$P_LLM" = "J" ]; then
  abschnitt "Lokales LLM"
  LLDIR="${LLDIR:-/opt/llamacpp}"
  als_root mkdir -p "$LLDIR"
  LLBIN="$(find "$LLDIR" -name llama-server -type f 2>/dev/null | head -1)"
  if [ -z "$LLBIN" ]; then
    info "Suche das aktuelle Release-Paket …"
    ASSET="$("$VPY" - <<'PYEOF'
import json, sys, urllib.request
try:
    d = json.load(urllib.request.urlopen(
        "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest", timeout=20))
    for a in d.get("assets", []):
        n = a["name"]
        if "ubuntu" in n and "x64" in n and n.endswith(".zip"):
            print(a["browser_download_url"]); break
except Exception as e:
    # Auf stderr, damit der Installer den Grund zeigt statt nur "nichts gefunden".
    print("Release-Abfrage fehlgeschlagen: %s" % e, file=sys.stderr)
PYEOF
)"
    if [ -n "$ASSET" ]; then
      als_root curl -Lf --progress-bar -o "$LLDIR/llama.zip" "$ASSET" && als_root unzip -oq "$LLDIR/llama.zip" -d "$LLDIR"
      LLBIN="$(find "$LLDIR" -name llama-server -type f 2>/dev/null | head -1)"
      [ -n "$LLBIN" ] && als_root chmod +x "$LLBIN"
    else
      warn "Kein passendes Release gefunden — Handanleitung: docs/SETUP_LLAMACPP.md"
    fi
  fi
  if [ -n "$LLBIN" ] && [ ! -f "$LLDIR/model.gguf" ]; then
    info "Lade das Modell (Qwen2.5-1.5B-Instruct, Q4_K_M, ca. 1 GB) …"
    als_root curl -Lf --progress-bar -o "$LLDIR/model.gguf" \
      "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf" \
      || warn "Modell-Download fehlgeschlagen — Anleitung: docs/SETUP_LLAMACPP.md"
  fi
  if [ -n "$LLBIN" ] && [ -f "$LLDIR/model.gguf" ] && [ "$NC_INIT" = "systemd" ]; then
    # -t 4 ist Absicht, keine Sparsamkeit: Aufnahmen haben Vorrang vor
    # der KI. Nice=10 und CPUWeight=50 verankern das noch einmal.
    cat > "$ARBEIT/llamacpp.service" <<UNIT
[Unit]
Description=llama.cpp Server (NIGHTCRAWLER Brain Tier 4)
After=network.target

[Service]
ExecStart=${LLBIN} -m ${LLDIR}/model.gguf --host 127.0.0.1 --port 8080 -t 4 -c 8192 --no-warmup
Restart=always
RestartSec=5
Nice=10
CPUWeight=50

[Install]
WantedBy=multi-user.target
UNIT
    if schreibe_systemdatei /etc/systemd/system/llamacpp.service "$ARBEIT/llamacpp.service"; then
      als_root systemctl daemon-reload
    fi
    als_root systemctl enable --now llamacpp || warn "llamacpp-Dienst startete nicht — journalctl -u llamacpp -n 50"
    gut "llama.cpp laeuft auf 127.0.0.1:8080."
    merke "Lokales LLM: llamacpp-Dienst, Modell %s/model.gguf" "$LLDIR"
  fi
  # Nachtragen, nicht im Plan: die Werte haengen am Erfolg dieses Schritts.
  if [ -n "$LLBIN" ] && [ -f "$LLDIR/model.gguf" ]; then
    : > "$PLAN_ENV"
    env_set BRAIN_LLM_BACKEND auto
    env_set BRAIN_LLAMACPP_URL "http://127.0.0.1:8080"
    ENV_BASIS="$ENVF"; env_bauen "$ENV_BASIS" "$ARBEIT/env.neu"
    cmp -s "$ENVF" "$ARBEIT/env.neu" || { cat "$ARBEIT/env.neu" > "$ENVF"; chmod 600 "$ENVF"; }
  fi
fi

# ── TikTok-Cookies ───────────────────────────────────────────
if [ "$MODUS" = "gefuehrt" ]; then
  erklaere "TikTok liefert manche Streams nur mit gueltiger Sitzung aus; ohne Cookies bricht die Aufloesung dann mit HTTP 403 ab. Der Bot liest sie aus tiktok_cookies.txt im Netscape-Format (Browser-Erweiterung 'Get cookies.txt'). Ohne die Datei laeuft alles — nur eben nicht bei geschuetzten Streams."
  [ -f "$ZIEL/tiktok_cookies.txt" ] && gut "tiktok_cookies.txt ist vorhanden." \
    || merke "OPTIONAL: tiktok_cookies.txt anlegen (gegen HTTP 403 bei der Stream-Aufloesung)"
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Selbsttest und Autostart"
erklaere "Jetzt wird geprueft, ob das Zusammengestellte wirklich laeuft: bot.py --selfcheck laedt den kompletten Bot, prueft Werkzeuge, Konfiguration und Erreichbarkeiten und beendet sich wieder. Das ist der Unterschied zwischen 'installiert' und 'laeuft'."

SELFCHECK_RC=0
if [ -f "$ZIEL/bot.py" ]; then
  ( cd "$ZIEL" && "$VPY" bot.py --selfcheck ) || SELFCHECK_RC=$?
  case "$SELFCHECK_RC" in
    0) gut "Selbsttest ohne Befund.";;
    1) warn "Der Selbsttest meldet offene Punkte (oben rot). Meist fehlt ein Token oder ein Schluessel — der Bot startet trotzdem."
       merke "Selbsttest hatte Befunde: erneut pruefen mit  .venv/bin/python bot.py --selfcheck";;
    *) warn "Der Selbsttest liess sich nicht ausfuehren (Code %s)." "$SELFCHECK_RC"
       info "Ersatzpruefung: Modul-Import"
       ( cd "$ZIEL" && "$VPY" -c 'import ast,sys; ast.parse(open("bot.py",encoding="utf-8").read()); print("bot.py ist syntaktisch in Ordnung")' ) \
         || { fehler "bot.py laesst sich nicht einmal einlesen — Python-Fassung pruefen."; exit 1; };;
  esac
fi

# ── Startskript (immer, auch mit Dienst) ─────────────────────
cat > "$ARBEIT/start.sh" <<START
#!/usr/bin/env bash
# Von tools/installer.sh erzeugt — Handstart ohne Dienst.
# Der Dienst ist der Normalfall; das hier ist fuer Tests und fuers Zuschauen.
cd "\$(dirname "\$0")" || exit 1
exec .venv/bin/python bot.py "\$@"
START
if [ -f "$ZIEL/start.sh" ] && cmp -s "$ZIEL/start.sh" "$ARBEIT/start.sh"; then
  info "unveraendert: %s" "$ZIEL/start.sh"
else
  cp "$ARBEIT/start.sh" "$ZIEL/start.sh"
fi
chmod +x "$ZIEL/start.sh"
gut "Startskript: %s/start.sh" "$ZIEL"

case "$P_AUTOSTART" in
  systemd)
    cat > "$ARBEIT/dienst.service" <<UNIT
[Unit]
Description=NIGHTCRAWLER v37 — TikTok-Ueberwachung, Aufnahme, Restream
# network-online statt network: ohne echte Adresse scheitern die ersten
# Auflaeufe zu TikTok und der Bot startet in eine Fehlerschleife.
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$(id -un)
Group=$(id -gn)
WorkingDirectory=${ZIEL}
Environment=PYTHONUNBUFFERED=1
ExecStart=${VENV}/bin/python ${ZIEL}/bot.py
Restart=always
RestartSec=10
# v4.2-W118: ohne diese Zeile laeuft der Dienst mit 1024 Dateideskriptoren —
# jede Aufnahme belegt zwei Pipes, jeder Chat einen Socket. Der Bot hebt das
# Soft-Limit zwar selbst an, aber nur bis zum Hard-Limit, das hier steht.
LimitNOFILE=65536
# v4.2-W121: SIGTERM nur an den Bot; er beendet seine Aufnahmen selbst
# (SIGTERM an ffmpeg, Datei eintragen) und raeumt die Hilfsprozesse ab.
# Mit der Vorgabe control-group bekaeme jedes ffmpeg das Signal gleichzeitig
# und unabhaengig davon. Was nach 60 s noch lebt, toetet systemd.
KillMode=mixed
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
UNIT
    if schreibe_systemdatei "/etc/systemd/system/${DIENST}.service" "$ARBEIT/dienst.service"; then
      als_root systemctl daemon-reload || warn "systemctl daemon-reload fehlgeschlagen."
    fi
    als_root systemctl enable "$DIENST" >/dev/null 2>&1 || warn "Dienst liess sich nicht aktivieren."
    merke "Dienst: %s  (Status: systemctl status %s · Log: journalctl -u %s -f)" "$DIENST" "$DIENST" "$DIENST";;
  openrc)
    cat > "$ARBEIT/dienst.openrc" <<ORC
#!/sbin/openrc-run
# NIGHTCRAWLER — erzeugt von tools/installer.sh
name="${DIENST}"
description="NIGHTCRAWLER v37"
command="${VENV}/bin/python"
command_args="${ZIEL}/bot.py"
command_user="$(id -un):$(id -gn)"
directory="${ZIEL}"
supervisor=supervise-daemon
respawn_delay=10
output_log="${ZIEL}/logs/openrc.out.log"
error_log="${ZIEL}/logs/openrc.err.log"
depend() { need net; }
ORC
    mkdir -p "$ZIEL/logs"
    if schreibe_systemdatei "/etc/init.d/${DIENST}" "$ARBEIT/dienst.openrc"; then
      als_root chmod +x "/etc/init.d/${DIENST}"
    fi
    als_root rc-update add "$DIENST" default >/dev/null 2>&1 || warn "Dienst liess sich nicht aktivieren."
    merke "Dienst: %s  (Status: rc-service %s status · Log: %s/logs/openrc.err.log)" "$DIENST" "$DIENST" "$ZIEL";;
  launchd)
    PLIST="$HOME/Library/LaunchAgents/dev.nightcrawler.bot.plist"
    mkdir -p "$(dirname "$PLIST")" "$ZIEL/logs"
    cat > "$ARBEIT/bot.plist" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>dev.nightcrawler.bot</string>
  <key>ProgramArguments</key><array>
    <string>${VENV}/bin/python</string><string>${ZIEL}/bot.py</string></array>
  <key>WorkingDirectory</key><string>${ZIEL}</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>${ZIEL}/logs/launchd.out.log</string>
  <key>StandardErrorPath</key><string>${ZIEL}/logs/launchd.err.log</string>
</dict></plist>
PLISTEOF
    if [ -f "$PLIST" ] && cmp -s "$PLIST" "$ARBEIT/bot.plist"; then
      info "unveraendert: %s" "$PLIST"
    else
      cp "$ARBEIT/bot.plist" "$PLIST"
      launchctl unload "$PLIST" 2>/dev/null || true
      launchctl load "$PLIST" && gut "launchd-Eintrag geladen." || warn "launchctl load fehlgeschlagen."
    fi
    merke "launchd: %s  (stoppen: launchctl unload %s)" "$PLIST" "$PLIST";;
  *)
    # Container, WSL ohne systemd, oder keine Rechte: dann ist der Handstart der
    # ehrliche Weg — ein Dienst, den niemand startet, ist schlimmer als keiner.
    info "Kein systemd/launchd verfuegbar — Start von Hand:  bash %s/start.sh" "$ZIEL"
    erklaere "Soll der Bot dauerhaft laufen, braucht er einen Aufpasser: unter WSL 'wsl --shutdown'-fest per Aufgabenplanung, im Container per Restart-Regel, sonst tmux/screen.";;
esac

# Starten oder neu starten. v4.2-W124: ein laufender Dienst sieht neuen Code,
# neue Pakete und eine geaenderte .env erst nach einem Neustart — der
# Installer hat genau das gerade geliefert. Im unbeaufsichtigten Lauf wird
# trotzdem NICHT neu gestartet: das Abschalten laufender Aufnahmen ist eine
# Entscheidung des Betreibers, keine Nebenwirkung eines Skripts.
dienst_aktiv(){
  case "$P_AUTOSTART" in
    systemd) systemctl is-active --quiet "$DIENST" 2>/dev/null;;
    openrc)  ${SUDO:+$SUDO} rc-service "$DIENST" status >/dev/null 2>&1;;
    *) return 1;;
  esac
}
dienst_start(){
  case "$P_AUTOSTART" in
    systemd) als_root systemctl "$1" "$DIENST";;
    openrc)  als_root rc-service "$DIENST" "$1";;
  esac
}
if [ "$P_AUTOSTART" = "systemd" ] || [ "$P_AUTOSTART" = "openrc" ]; then
  if dienst_aktiv; then
    if [ "$MODUS" = "unattended" ]; then
      info "Dienst %s laeuft — Neustart noetig, damit Aenderungen wirken. Nicht automatisch: %s" "$DIENST" \
        "$( [ "$P_AUTOSTART" = systemd ] && printf 'sudo systemctl restart %s' "$DIENST" || printf 'sudo rc-service %s restart' "$DIENST")"
    elif frage_ja "$(tf 'Dienst %s laeuft — jetzt neu starten (laufende Aufnahmen werden sauber beendet)?' "$DIENST")" J; then
      dienst_start restart || warn "Dienst liess sich nicht aktivieren."
    fi
  elif [ "$MODUS" = "unattended" ] || frage_ja "Dienst aktivieren und starten?" J; then
    dienst_start start || true
    sleep 2
    if dienst_aktiv; then gut "Dienst %s laeuft." "$DIENST"
    else warn "Dienst startete nicht. Grund ansehen:  journalctl -u %s -n 60 --no-pager" "$DIENST"; fi
  else
    info "Spaeter:  sudo systemctl enable --now %s" "$DIENST"
  fi
fi

# ── MOTD ─────────────────────────────────────────────────────
if [ "$P_MOTD" = "J" ] && [ -f "$ZIEL/tools/motd.sh" ]; then
  chmod +x "$ZIEL/tools/motd.sh"
  if [ "$NC_MOTD_WEG" = "shellrc" ]; then
    BOT_DIR="$ZIEL" SERVICE="" DASH_PORT="$DASH_PORT" "$ZIEL/tools/motd.sh" --install || warn "MOTD-Einrichtung fehlgeschlagen."
  else
    ${SUDO:+$SUDO} env BOT_DIR="$ZIEL" SERVICE="${DIENST:-}" DASH_PORT="$DASH_PORT" "$ZIEL/tools/motd.sh" --install \
      || warn "MOTD-Einrichtung fehlgeschlagen."
  fi
  merke "MOTD: aktiv (Vorschau: tools/motd.sh · Erkennung pruefen: tools/motd.sh --doctor)"
fi

# ── Totmann-Meldung ──────────────────────────────────────────
if [ "$P_TOTMANN" = "J" ] && [ -f "$ZIEL/tools/notify_failure.sh" ]; then
  chmod +x "$ZIEL/tools/notify_failure.sh"
  # notify_failure.sh liest TELEGRAM_TOKEN/TELEGRAM_CHAT_ID bzw.
  # DISCORD_WEBHOOK — Namen, die der Bot selbst NICHT benutzt (er hat
  # BOT_TOKEN und ALLOWED_USER_IDS). Ohne diese Spiegelung meldet der
  # Totmann still gar nichts; genau deshalb steht sie hier.
  : > "$PLAN_ENV"
  _tgt="$(env_bisher BOT_TOKEN)"; _tgc="$(printf '%s' "$(env_bisher ALLOWED_USER_IDS)" | cut -d, -f1)"
  [ -n "$_tgt" ] && [ -z "$(env_bisher TELEGRAM_TOKEN)" ]   && env_set TELEGRAM_TOKEN "$_tgt"
  [ -n "$_tgc" ] && [ -z "$(env_bisher TELEGRAM_CHAT_ID)" ] && env_set TELEGRAM_CHAT_ID "$_tgc"
  _dcw="$(env_bisher DISCORD_WEBHOOK_URL)"
  [ -n "$_dcw" ] && [ -z "$(env_bisher DISCORD_WEBHOOK)" ]  && env_set DISCORD_WEBHOOK "$_dcw"
  if [ -s "$PLAN_ENV" ]; then
    ENV_BASIS="$ENVF"; env_bauen "$ENV_BASIS" "$ARBEIT/env.neu"
    cat "$ARBEIT/env.neu" > "$ENVF"; chmod 600 "$ENVF"
  fi
  cat > "$ARBEIT/notify.service" <<UNIT
[Unit]
Description=NIGHTCRAWLER Totmann-Meldung fuer %i

[Service]
Type=oneshot
User=$(id -un)
EnvironmentFile=${ENVF}
ExecStart=${ZIEL}/tools/notify_failure.sh %i
UNIT
  printf '[Unit]\nOnFailure=nightcrawler-notify@%%n.service\n' > "$ARBEIT/onfailure.conf"
  _neu=0
  schreibe_systemdatei /etc/systemd/system/nightcrawler-notify@.service "$ARBEIT/notify.service" && _neu=1
  schreibe_systemdatei "/etc/systemd/system/${DIENST}.service.d/onfailure.conf" "$ARBEIT/onfailure.conf" && _neu=1
  [ "$_neu" = 1 ] && { als_root systemctl daemon-reload || warn "systemctl daemon-reload fehlgeschlagen."; }
  gut "Totmann-Meldung verdrahtet."
  info "Testen (MUSS eine Nachricht ausloesen):  sudo systemctl start nightcrawler-notify@%s.service" "$DIENST"
  merke "Totmann-Meldung: aktiv — Test: sudo systemctl start nightcrawler-notify@%s.service" "$DIENST"
fi

# ── Beobachtung (v4.2-W127) ──────────────────────────────────
# Dasselbe Werkzeug wie spaeter von Hand: eine Einrichtung, zwei Wege dorthin
# — zwei Kopien liefen auseinander (W100).
if [ "$P_BEOBACHTUNG" = "J" ] && [ -f "$ZIEL/tools/observability.sh" ]; then
  _obs=(--unattended --dir "$ZIEL" --no-grafana)
  [ "$P_GRAFANA" = "J" ] && _obs=(--unattended --dir "$ZIEL" --grafana-repo)
  [ "$TROCKEN" = 1 ] && _obs+=(--dry-run)
  if ${SUDO:+$SUDO} bash "$ZIEL/tools/observability.sh" "${_obs[@]}"; then
    merke "Beobachtung: Prometheus auf 127.0.0.1:9099 — pruefen: bash tools/observability.sh --check"
  else
    warn "Beobachtung unvollstaendig — Grund oben; erneut: sudo bash %s/tools/observability.sh" "$ZIEL"
  fi
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Bericht"

NOTIZ="$HOME/nightcrawler-installation.txt"
# v4.2-W123: die Notiz ist eine Datei, die der Betreiber LIEST — sie war bis
# hierher in jeder Sprache deutsch. Jede Zeile geht deshalb durch tf.
nz(){ printf '%s\n' "$(tf "$@")"; }
{
  nz "NIGHTCRAWLER v37 — Installation vom %s" "$(date '+%F %H:%M')"
  printf '%s\n\n' "$(printf '=%.0s' $(seq 1 60))"
  nz "Verzeichnis   %s" "$ZIEL"
  printf 'Python        %s\n' "$("$VPY" -V 2>&1)"
  nz "Konfiguration %s   (Rechte 600 — enthaelt Geheimnisse)" "$ENVF"
  [ -n "${DIENST:-}" ] && nz "Dienst        %s" "$DIENST"
  printf 'Dashboard     http://127.0.0.1:%s\n\n' "$DASH_PORT"
  nz "BEDIENUNG"
  if [ "$P_AUTOSTART" = "systemd" ]; then
    printf '  Status      systemctl status %s\n  Log         journalctl -u %s -f\n' "$DIENST" "$DIENST"
    nz "  Neustart    sudo systemctl restart %s" "$DIENST"
  fi
  nz "  Handstart   bash %s/start.sh" "$ZIEL"
  # v4.2-W100: hier stand '%s/bot.py' — ein Schraegstrich statt eines
  # Leerzeichens, also '.venv/bin/python/bot.py'. Genau DIESE Zeile kopiert
  # der Betreiber aus dem Bericht, und sie kann nicht laufen. Dieselbe Klasse
  # wie die Dashboard-Adresse in W93: die Zeile, die man kopiert, war falsch.
  nz "  Selbsttest  %s bot.py --selfcheck" "$VENV/bin/python"
  nz "  Nachinstallieren  bash %s/tools/update.sh" "$ZIEL"
  printf '  Dashboard   ssh -L 3000:localhost:%s %s@<server-ip>   → http://localhost:3000\n\n' "$DASH_PORT" "$(id -un)"
  if [ -n "$MERKZETTEL" ]; then nz "MERKZETTEL"; printf '%s' "$MERKZETTEL" | sed 's/^/  · /'; printf '\n'; fi
  nz "WEITERLESEN"
  nz "  docs/START_HIER.txt   Einstieg und Alltag"
  nz "  docs/DEPLOY.md        Ausliefern, Rollback, Pruefschritte"
  nz "  docs/CROWDSEC.md      Abwehr"
  nz "  docs/SETUP_*.md       OAuth fuer Twitch und YouTube, llama.cpp"
} > "$NOTIZ"

printf '\n'
gut "NIGHTCRAWLER ist eingerichtet."
printf '\n'
printf '  %s%-13s%s %s\n' "$DIM" "$(t 'Verzeichnis')" "$R" "$ZIEL"
printf '  %s%-13s%s %s\n' "$DIM" "Python" "$R" "$("$VPY" -V 2>&1)"
[ -n "${DIENST:-}" ] && printf '  %s%-13s%s %s\n' "$DIM" "$(t 'Dienst')" "$R" "$DIENST"
printf '  %sDashboard%s     http://127.0.0.1:%s\n' "$DIM" "$R" "$DASH_PORT"
printf '\n'
if [ -n "$MERKZETTEL" ]; then
  printf '  %s%s%s%s\n' "$B" "$TXT" "$(t 'Merkzettel')" "$R"
  printf '%s' "$MERKZETTEL" | sed "s/^/    ${DIM}·${R} /"
  printf '\n'
fi
printf '  %s%s%s%s\n' "$B" "$TXT" "$(t 'Naechste Schritte')" "$R"
if [ "$P_AUTOSTART" = "systemd" ]; then
  printf '    1  %s\n' "$(tf 'Mitlesen, ob er sauber hochkommt:  %s' "${TXT}journalctl -u ${DIENST} -f${R}")"
else
  printf '    1  %s\n' "$(tf 'Starten und zuschauen:  %s' "${TXT}bash ${ZIEL}/start.sh${R}")"
fi
printf '    2  %s\n' "$(tf 'In Telegram deinen Bot anschreiben:  %s, dann %s' "${TXT}/start${R}" "${TXT}/track <tiktok-name>${R}")"
printf '    3  %s\n' "$(tf 'Dashboard per Tunnel oeffnen:  %s' "${TXT}ssh -L 3000:localhost:${DASH_PORT} $(id -un)@<server-ip>${R}")"
printf '\n'
printf '  %s%s%s\n' "$FNT" "$(tf 'Alles davon steht auch in %s' "$NOTIZ")" "$R"
printf '\n'
exit 0
