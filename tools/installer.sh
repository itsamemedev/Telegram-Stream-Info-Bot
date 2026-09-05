#!/usr/bin/env bash
#
# NIGHTCRAWLER v37 — gefuehrte Installation
#
#     bash tools/installer.sh              gefuehrt, erklaert jeden Schritt
#     bash tools/installer.sh --express    nur Pflichtfragen, Rest per Vorgabe
#     bash tools/installer.sh --unattended gar keine Fragen (fuer Skripte)
#     bash tools/installer.sh --help       alle Schalter
#
# Ziele: Ubuntu, Debian, Raspberry Pi OS, macOS. Fuer Windows liegt daneben
# tools/install.bat.
#
# WARUM ES DAS GIBT
# Die Anleitung im README ist richtig, aber sie ist eine Anleitung: zehn
# Schritte, drei Fussnoten, und der haeufigste Ausgang war ein Bot, der beim
# ersten Start ueber eine fehlende .env-Variable stolpert oder unter Python
# 3.11 schon beim Parsen von bot.py stirbt (PEP 701, f-string mit Backslash —
# das ist keine Empfehlung, das ist eine harte Grenze).
#
# Dieses Skript nimmt genau die Entscheidungen ab, die man nur einmal trifft,
# und ERKLAERT jede davon, statt sie zu verstecken. Es fragt vor jedem Eingriff,
# es schreibt nichts ausserhalb des Zielverzeichnisses ohne Rueckfrage, und es
# ist wiederholbar: ein zweiter Lauf erkennt den Bestand und aktualisiert ihn,
# statt ihn zu ueberbuegeln.
#
# Was es NICHT tut: Geheimnisse erfinden, die von aussen kommen (Bot-Token,
# Stream-Keys). Wo ein Passwort dagegen frei waehlbar ist — Dashboard-Token,
# Dashboard-PIN, Datenbank-Passwort — bietet es an, eines zu erzeugen.

set -euo pipefail

NC_INSTALLER_VERSION="1.0"
REPO_URL="${REPO_URL:-https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git}"
PY_MIN_MAJOR=3
PY_MIN_MINOR=12

# ── Betriebsarten ────────────────────────────────────────────
MODUS="gefuehrt"          # gefuehrt | express | unattended
ZIEL=""                   # --dir
BRANCH="${BRANCH:-main}"
SKIP_SYSTEM=0
FARBE=1

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
SCHRITTE_GESAMT=11
kopf(){ SCHRITT=$((SCHRITT+1))
  printf '\n%s%s[%d/%d] %s%s\n' "$BR" "$B" "$SCHRITT" "$SCHRITTE_GESAMT" "$1" "$R"
  printf '%s%s%s\n' "$DIM" "$(printf '─%.0s' $(seq 1 66))" "$R"; }
# v4.1-W17: Mehrsprachigkeit AN DER SENKE. Jede dieser vier Funktionen (und
# erklaere/frage_ja weiter unten) schickt ihren Text durch t(); damit sind alle
# 112 Ausgabestellen erfasst, ohne eine einzige davon anzufassen. Fehlt eine
# Uebersetzung, bleibt Deutsch stehen — dieselbe Regel wie in nc/i18n.py.
# shellcheck source=lib/i18n.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/i18n.sh" 2>/dev/null || t(){ printf '%s' "$*"; }

info(){ printf '  %s▸%s %s\n' "$DIM" "$R" "$(t "$*")"; }
gut(){  printf '  %s✔%s %s\n' "$OK" "$R" "$(t "$*")"; }
warn(){ printf '  %s▲%s %s\n' "$WRN" "$R" "$(t "$*")"; }
fehler(){ printf '  %s✘%s %s\n' "$ERR" "$R" "$(t "$*")" >&2; }
# Erklaerungen sind der halbe Zweck dieses Skripts — deshalb bekommen sie ein
# eigenes, ruhiges Format und werden auf 72 Zeichen umbrochen.
erklaere(){ printf '%s' "$FNT"; printf '%s\n' "$(t "$*")" | fold -s -w 72 | sed 's/^/    /'; printf '%s' "$R"; }

MERKZETTEL=""
merke(){ MERKZETTEL="${MERKZETTEL}${1}"$'\n'; }

abbruch(){
  local rc=$?
  printf '\n'
  fehler "Abbruch in Schritt ${SCHRITT} (Rueckgabewert ${rc})."
  printf '  %sWas bereits geschrieben wurde, bleibt liegen — ein erneuter Lauf%s\n' "$FNT" "$R"
  printf '  %ssetzt dort auf, ohne Schaden anzurichten.%s\n' "$FNT" "$R"
  [ -n "${ZIEL:-}" ] && printf '  %sZielverzeichnis: %s%s\n' "$FNT" "$ZIEL" "$R"
  exit "$rc"
}
trap abbruch ERR

# ── Eingaben ─────────────────────────────────────────────────
# Auch wenn das Skript per Pipe kommt (curl ... | bash) muss die Tastatur
# erreichbar bleiben — sonst laufen alle Fragen ins Leere und der Nutzer
# bekaeme stumm die Vorgaben.
TTY=""
if [ -t 0 ]; then TTY="/dev/stdin"; elif [ -r /dev/tty ]; then TTY="/dev/tty"; fi
[ -z "$TTY" ] && [ "$MODUS" != "unattended" ] && MODUS="unattended"

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
    if [ "$vor" = "J" ]; then printf '  %s?%s %s %s[J/n]%s ' "$BR" "$R" "$(t "$f")" "$FNT" "$R"
    else                      printf '  %s?%s %s %s[j/N]%s ' "$BR" "$R" "$(t "$f")" "$FNT" "$R"; fi
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

frage_geheimnis(){ # frage_geheimnis VARIABLE "Beschreibung" erzeugbar laenge [nur_ziffern]
  # Genau der vom Betreiber gewuenschte Ablauf: erst fragen, ob erzeugt werden
  # soll — sonst auf die Eingabe WARTEN (verdeckt, mit Wiederholung).
  local __v="$1" was="$2" erzeugbar="${3:-1}" laenge="${4:-32}" ziffern="${5:-0}"
  local a b
  if [ "$MODUS" = "unattended" ]; then
    if [ "$erzeugbar" = 1 ]; then printf -v "$__v" '%s' "$(erzeuge_passwort "$laenge" "$ziffern")"
    else printf -v "$__v" '%s' ""; fi
    return 0
  fi
  if [ "$erzeugbar" = 1 ] && frage_ja "${was}: sicheres Passwort erzeugen lassen?" J; then
    a="$(erzeuge_passwort "$laenge" "$ziffern")"
    printf '    %serzeugt:%s %s%s%s\n' "$FNT" "$R" "$B" "$a" "$R"
    erklaere "Notieren oder im Passwortmanager ablegen. Es steht ausserdem in der .env (chmod 600) und laesst sich dort jederzeit nachlesen."
    printf -v "$__v" '%s' "$a"
    return 0
  fi
  while :; do
    printf '  %s?%s %s eingeben %s(leer = spaeter selbst eintragen)%s: ' "$BR" "$R" "$was" "$FNT" "$R"
    lies a -s
    [ -z "$a" ] && { printf -v "$__v" '%s' ""; return 0; }
    printf '  %s?%s Zur Sicherheit wiederholen: ' "$BR" "$R"
    lies b -s
    [ "$a" = "$b" ] && { printf -v "$__v" '%s' "$a"; return 0; }
    warn "Die Eingaben waren nicht gleich — noch einmal."
  done
}

have(){ command -v "$1" >/dev/null 2>&1; }

# ── Schalter ─────────────────────────────────────────────────
while [ $# -gt 0 ]; do
  case "$1" in
    --express)     MODUS="express";;
    --unattended|-y) MODUS="unattended";;
    --dir)         ZIEL="${2:-}"; shift;;
    --dir=*)       ZIEL="${1#*=}";;
    --branch)      BRANCH="${2:-main}"; shift;;
    --branch=*)    BRANCH="${1#*=}";;
    --skip-system) SKIP_SYSTEM=1;;
    --no-color)    FARBE=0; setze_farben;;
    --version)     printf 'NIGHTCRAWLER installer %s\n' "$NC_INSTALLER_VERSION"; exit 0;;
    --help|-h)
      cat <<'HILFE'
NIGHTCRAWLER v37 — Installation

  bash tools/installer.sh [Schalter]

  --express        nur die Pflichtfragen, alles andere per Vorgabe
  --unattended,-y  keine Fragen; Passwoerter werden erzeugt, optionale
                   Bausteine bleiben aus. Fuer Provisionierung/CI.
  --dir <Pfad>     Zielverzeichnis (Vorgabe: ~/nightcrawler)
  --branch <Name>  Git-Zweig beim Klonen (Vorgabe: main)
  --skip-system    Systempakete nicht anfassen (wenn schon vorhanden)
  --no-color       ohne Farben
  --help           diese Hilfe

Unterstuetzt: Ubuntu, Debian, Raspberry Pi OS, macOS.
Windows: tools\install.bat
HILFE
      exit 0;;
    *) fehler "Unbekannter Schalter: $1  (--help)"; exit 1;;
  esac
  shift
done
[ "$MODUS" != "unattended" ] && [ -z "$TTY" ] && MODUS="unattended"

# ═══════════════════════════════════════════════════════════════════════════
kopf "Willkommen"
cat <<WILLKOMMEN
  ${BR}${B}NIGHTCRAWLER v37${R} ${FNT}— TikTok-Live-Ueberwachung, Aufnahme,
  Multi-Ziel-Restream und KI-Moderation (AZRAEL).${R}

  Dieses Skript richtet den Bot vollstaendig ein und erklaert dabei, was
  es tut und warum. Es fragt vor jedem Eingriff. Abbrechen mit Strg+C ist
  jederzeit gefahrlos.

  ${DIM}Der Weg in elf Schritten:${R}
    1  Willkommen              7  Konfiguration (.env)
    2  System pruefen          8  Optionale Bausteine
    3  Python sicherstellen    9  Selbsttest
    4  Zielverzeichnis        10  Autostart, MOTD, Totmann-Meldung
    5  Systempakete           11  Zusammenfassung
    6  Python-Pakete
WILLKOMMEN
case "$MODUS" in
  express)    info "Betriebsart: ${B}express${R} — nur Pflichtfragen.";;
  unattended) info "Betriebsart: ${B}unattended${R} — keine Fragen, Vorgaben und erzeugte Passwoerter.";;
  *)          info "Betriebsart: ${B}gefuehrt${R} — mit Erklaerungen. Fuer weniger Text: --express";;
esac
if [ "$MODUS" = "gefuehrt" ]; then
  frage_ja "Loslegen?" J || { info "Abgebrochen — nichts veraendert."; exit 0; }
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "System pruefen"

OS="$(uname -s)"
ARCH="$(uname -m)"
DISTRO=""; DISTRO_NAME=""; PKG=""; IST_PI=0
case "$OS" in
  Linux)
    if [ -r /etc/os-release ]; then
      # shellcheck source=/dev/null
      . /etc/os-release
      DISTRO="${ID:-linux}"; DISTRO_NAME="${PRETTY_NAME:-$DISTRO}"
      case "${ID:-}${ID_LIKE:-}" in *debian*|*ubuntu*|*raspbian*) PKG="apt";; esac
    fi
    grep -qi 'raspberry' /proc/device-tree/model 2>/dev/null && IST_PI=1
    [ "$DISTRO" = "raspbian" ] && IST_PI=1
    ;;
  Darwin)
    DISTRO="macos"; DISTRO_NAME="macOS $(sw_vers -productVersion 2>/dev/null)"
    have brew && PKG="brew"
    ;;
  *) DISTRO="$OS"; DISTRO_NAME="$OS";;
esac

info "System:    ${DISTRO_NAME:-unbekannt} (${ARCH})"
[ "$IST_PI" = 1 ] && info "Erkannt:   Raspberry Pi"

# Rechte
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if have sudo; then SUDO="sudo"; else
    warn "Weder root noch sudo — Systempakete koennen nicht installiert werden."
    SKIP_SYSTEM=1
  fi
fi

# Paketmanager
if [ -z "$PKG" ] && [ "$SKIP_SYSTEM" = 0 ]; then
  if [ "$OS" = "Darwin" ]; then
    warn "Homebrew fehlt. Es ist auf macOS der einzige vernuenftige Weg zu ffmpeg."
    erklaere "Installation (dauert ein paar Minuten): /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    if frage_ja "Homebrew jetzt installieren?" J; then
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      for p in /opt/homebrew/bin/brew /usr/local/bin/brew; do
        [ -x "$p" ] && eval "$("$p" shellenv)" && PKG="brew" && break
      done
    else SKIP_SYSTEM=1; fi
  else
    warn "Paketmanager nicht erkannt (weder apt noch brew)."
    erklaere "Der Bot laeuft trotzdem — du musst ffmpeg, streamlink und yt-dlp dann selbst installieren. Schritt 5 wird uebersprungen."
    SKIP_SYSTEM=1
  fi
fi

# Arbeitsspeicher und Platte: der haeufigste Pi-Ausgang ist ein OOM-Kill
# mitten in der ersten Aufnahme. Lieber jetzt sagen als spaeter suchen.
RAM_MB=0
if [ -r /proc/meminfo ]; then RAM_MB=$(awk '/^MemTotal:/{printf "%d", $2/1024}' /proc/meminfo)
elif [ "$OS" = "Darwin" ]; then RAM_MB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1048576 )); fi
KERNE=$( (nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 1) )
FREI_GB=$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2{printf "%d", $4/1048576}')
info "Kerne:     ${KERNE}   RAM: ${RAM_MB} MB   frei in \$HOME: ${FREI_GB:-?} GB"
[ "${RAM_MB:-0}" -lt 2000 ] && warn "Unter 2 GB RAM: Transkription (Whisper) und lokales LLM bitte auslassen."
[ "${RAM_MB:-0}" -ge 2000 ] && [ "${RAM_MB:-0}" -lt 4000 ] && warn "Unter 4 GB RAM: Aufnahme und ein Restream-Ziel gehen, mehreres wird eng."
[ "${FREI_GB:-99}" -lt 5 ] && warn "Unter 5 GB frei — Aufnahmen fuellen die Platte sehr schnell."
if [ "$IST_PI" = 1 ]; then
  erklaere "Auf einem Raspberry Pi gilt: Aufnahme und EIN Restream-Ziel ohne Transcode sind realistisch. Transcode (mehrere Ziele gleichzeitig) rechnet die CPU in Software und ueberfordert jeden Pi. Aufnahmen gehoeren auf eine USB-SSD, nicht auf die SD-Karte — Dauerschreiben killt SD-Karten binnen Wochen."
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Python sicherstellen"
erklaere "bot.py braucht mindestens Python ${PY_MIN_MAJOR}.${PY_MIN_MINOR}. Das ist keine Empfehlung: die Datei benutzt f-strings mit Backslash (PEP 701), unter 3.11 scheitert bereits das Einlesen mit einem SyntaxError. Debian 12 und Raspberry Pi OS bookworm liefern 3.11 — dort muss ein neuerer Interpreter dazu."

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
  gut "Python gefunden: $PY ($("$PY" -V 2>&1))"
else
  AKT="$( (python3 -V 2>&1) || echo 'keins')"
  warn "Kein Python >= ${PY_MIN_MAJOR}.${PY_MIN_MINOR} gefunden (vorhanden: ${AKT})."
  INSTALLIERT=0
  if [ "$PKG" = "apt" ] && [ "$SKIP_SYSTEM" = 0 ]; then
    if $SUDO apt-cache show python3.13 >/dev/null 2>&1 || $SUDO apt-cache show python3.12 >/dev/null 2>&1; then
      if frage_ja "python3.12/3.13 aus den Paketquellen installieren?" J; then
        $SUDO apt-get update -qq
        $SUDO apt-get install -y python3.13 python3.13-venv || $SUDO apt-get install -y python3.12 python3.12-venv
        INSTALLIERT=1
      fi
    elif [ "$DISTRO" = "ubuntu" ]; then
      erklaere "Diese Ubuntu-Fassung hat kein 3.12 in den Quellen. Das Zusatz-Repository deadsnakes ist der uebliche Weg dorthin."
      if frage_ja "deadsnakes-PPA hinzufuegen und python3.12 installieren?" J; then
        $SUDO apt-get update -qq && $SUDO apt-get install -y software-properties-common
        $SUDO add-apt-repository -y ppa:deadsnakes/ppa
        $SUDO apt-get update -qq && $SUDO apt-get install -y python3.12 python3.12-venv
        INSTALLIERT=1
      fi
    fi
  elif [ "$PKG" = "brew" ]; then
    frage_ja "python@3.13 per Homebrew installieren?" J && { brew install python@3.13; INSTALLIERT=1; }
  fi
  if [ "$INSTALLIERT" = 0 ]; then
    erklaere "Rueckfallweg ohne Paketquellen: uv (astral.sh) laedt eine fertige, eigenstaendige CPython-Fassung in dein Home — ohne root, ohne das System-Python anzufassen. Genau der Weg fuer Debian 12 und Raspberry Pi OS."
    if frage_ja "uv installieren und darueber Python 3.13 holen?" J; then
      curl -LsSf https://astral.sh/uv/install.sh | sh
      export PATH="$HOME/.local/bin:$PATH"
      uv python install 3.13
      INSTALLIERT=1
    fi
  fi
  PY="$(finde_python || true)"
  if [ -z "$PY" ]; then
    fehler "Ohne Python >= ${PY_MIN_MAJOR}.${PY_MIN_MINOR} geht es nicht weiter."
    printf '  %sWege: apt install python3.13  |  brew install python@3.13  |  https://astral.sh/uv%s\n' "$FNT" "$R"
    exit 1
  fi
  gut "Python bereit: $PY ($("$PY" -V 2>&1))"
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Zielverzeichnis und Quelltext"

SKRIPT="$(cd "$(dirname "$0")" && pwd)"
QUELLE=""
[ -f "$SKRIPT/../bot.py" ] && QUELLE="$(cd "$SKRIPT/.." && pwd)"

if [ -n "$QUELLE" ]; then
  info "Quelltext liegt bereits hier: $QUELLE"
  VORGABE="$QUELLE"
else
  info "Kein Quelltext neben dem Skript — er wird von GitHub geholt."
  VORGABE="$HOME/nightcrawler"
fi
[ -n "$ZIEL" ] || frage_text ZIEL "In welches Verzeichnis soll NIGHTCRAWLER?" "$VORGABE"
ZIEL="${ZIEL/#\~/$HOME}"

BESTAND=0
if [ -f "$ZIEL/bot.py" ] && [ "$ZIEL" != "$QUELLE" ]; then BESTAND=1; fi

if [ "$ZIEL" = "$QUELLE" ]; then
  gut "Installation direkt im vorhandenen Verzeichnis — nichts zu kopieren."
elif [ -n "$QUELLE" ]; then
  mkdir -p "$ZIEL"
  info "Kopiere Quelltext nach $ZIEL"
  erklaere ".env, Datenbanken, Aufnahmen und Logs werden dabei NIE angefasst — sie gehoeren dir, nicht dem Build."
  if have rsync; then
    rsync -a --exclude '.git' --exclude '.venv' --exclude 'recordings' \
          --exclude 'logs' --exclude '*.db' --exclude '.env' \
          "$QUELLE"/ "$ZIEL"/
  else
    (cd "$QUELLE" && tar cf - --exclude='.git' --exclude='.venv' --exclude='recordings' \
        --exclude='logs' --exclude='*.db' --exclude='.env' .) | (cd "$ZIEL" && tar xf -)
  fi
  gut "Quelltext liegt in $ZIEL"
else
  if [ "$BESTAND" = 1 ]; then
    info "Bestehende Installation gefunden."
    if [ -d "$ZIEL/.git" ] && frage_ja "Auf den neuesten Stand bringen (git pull)?" J; then
      git -C "$ZIEL" pull --ff-only || warn "git pull fehlgeschlagen — lokale Aenderungen? Quelltext bleibt wie er ist."
    fi
  else
    have git || { fehler "git fehlt und wird zum Holen des Quelltexts gebraucht."; exit 1; }
    info "Klone $REPO_URL (Zweig $BRANCH)"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$ZIEL"
    gut "Quelltext geholt."
  fi
fi
cd "$ZIEL"
ENVF="$ZIEL/.env"

# ═══════════════════════════════════════════════════════════════════════════
kopf "Systempakete"
erklaere "Vier Dinge kommen NICHT ueber pip, weil es Programme sind und keine Bibliotheken: ffmpeg schneidet, kodiert und sendet; streamlink loest die TikTok-Quelle auf; yt-dlp ist der Rueckfall, wenn TikTok mit 403 blockt; sqlite3 ist die Kommandozeile zur Datenbank (fuer Diagnose, nicht fuer den Betrieb)."

if [ "$SKIP_SYSTEM" = 1 ]; then
  warn "Uebersprungen (--skip-system oder kein Paketmanager)."
  info "Bitte selbst bereitstellen: ffmpeg streamlink yt-dlp git curl sqlite3"
else
  case "$PKG" in
    apt)
      PAKETE="ffmpeg streamlink yt-dlp git curl unzip sqlite3 ca-certificates"
      # Das venv-Paket muss zur GEWAEHLTEN Python-Fassung passen — sonst
      # scheitert python -m venv mit "ensurepip is not available", und das
      # ist die mit Abstand haeufigste Sackgasse auf Debian.
      PYV="$("$PY" -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
      if $SUDO apt-cache show "python${PYV}-venv" >/dev/null 2>&1; then
        PAKETE="$PAKETE python${PYV}-venv"
      else
        PAKETE="$PAKETE python3-venv"
      fi
      info "apt-get install $PAKETE"
      if frage_ja "Diese Pakete jetzt installieren?" J; then
        $SUDO apt-get update -qq
        # yt-dlp aus alten Debian-Quellen ist oft steinalt; wenn das Paket
        # fehlt oder zu alt ist, holt der pip-Schritt spaeter die aktuelle
        # Fassung ins venv. Deshalb hier kein hartes Scheitern.
        $SUDO apt-get install -y $PAKETE || warn "Mindestens ein Paket fehlte in den Quellen — es wird spaeter im venv ergaenzt."
        gut "Systempakete installiert."
      else
        warn "Uebersprungen. Ohne ffmpeg gibt es weder Aufnahme noch Restream."
      fi;;
    brew)
      info "brew install ffmpeg streamlink yt-dlp git sqlite"
      if frage_ja "Diese Pakete jetzt per Homebrew installieren?" J; then
        brew install ffmpeg streamlink yt-dlp git sqlite || warn "Mindestens ein Paket liess sich nicht installieren."
        gut "Systempakete installiert."
      fi;;
  esac
fi
for prog in ffmpeg streamlink yt-dlp; do
  if have "$prog"; then gut "$prog: $(command -v "$prog")"
  else
    # v4.2-W14: die Begruendung EINZELN uebersetzen. Vorher stand sie in einem
    # printf innerhalb der Ersetzung — der aeussere Text laeuft durch t(),
    # traegt aber einen Laufzeitwert und trifft deshalb nie einen Schluessel.
    if [ "$prog" = ffmpeg ]; then _grund="$(t 'ohne ihn laeuft KEINE Aufnahme und kein Restream')"
    else _grund="$(t 'wird spaeter im venv ergaenzt')"; fi
    warn "$prog $(t 'fehlt') — ${_grund}."
  fi
done

# ═══════════════════════════════════════════════════════════════════════════
kopf "Python-Pakete"
erklaere "Alles Weitere lebt in einer virtuellen Umgebung unter .venv/ — ein eigener Ordner mit eigenem Python und eigenen Bibliotheken. Damit kann keine Installation hier das System-Python beschaedigen und umgekehrt."

VENV="$ZIEL/.venv"
if [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c 'import sys;raise SystemExit(0 if sys.version_info>=(3,12) else 1)' 2>/dev/null; then
  gut "Vorhandene Umgebung wird weiterbenutzt: $VENV"
else
  [ -d "$VENV" ] && { warn "Vorhandenes .venv passt nicht (zu altes Python) — wird neu angelegt."; rm -rf "$VENV"; }
  info "Lege virtuelle Umgebung an ($PY)"
  "$PY" -m venv "$VENV" || {
    fehler "venv liess sich nicht anlegen."
    printf '  %sMeist fehlt das Paket python3-venv:  sudo apt install python3-venv%s\n' "$FNT" "$R"; exit 1; }
  gut "Umgebung angelegt."
fi
VPY="$VENV/bin/python"

# Optionale Pakete — jedes kostet Platz und Zeit, keines ist fuer den Kern
# noetig. Auf einem Pi ist das der Unterschied zwischen 3 und 25 Minuten.
OPT_AUS=""
opt_frage(){ # opt_frage <Paket> <Vorgabe J|N> <Erklaerung>
  local paket="$1" vorgabe="$2" text="$3"
  erklaere "$text"
  if frage_ja "  → ${paket} installieren?" "$vorgabe"; then
    merke "Python-Paket ${paket}: installiert"
  else
    OPT_AUS="$OPT_AUS $paket"
    merke "Python-Paket ${paket}: ausgelassen (spaeter: .venv/bin/pip install ${paket})"
  fi
}
WHISPER_VOR=J; [ "$IST_PI" = 1 ] && WHISPER_VOR=N
[ "${RAM_MB:-0}" -lt 3000 ] && WHISPER_VOR=N
if [ "$MODUS" = "gefuehrt" ]; then
  opt_frage "discord.py"     J  "Discord: zweite Bedienoberflaeche mit 45 Slash-Commands, Moderation und Community-Funktionen. Ohne Discord-Server unnoetig."
  opt_frage "faster-whisper" "$WHISPER_VOR" "Transkription: schreibt mit, was im Stream gesagt wird (Grundlage fuer Clips, Highlights und die KI-Auswertung). Braucht rund 300 MB und deutlich CPU."
  opt_frage "PyMySQL"        N  "MariaDB-Treiber: nur noetig, wenn du die Daten in MariaDB statt in SQLite haelst. SQLite reicht bis weit in den sechsstelligen Zeilenbereich."
  opt_frage "redis"          N  "Redis-Cache: entlastet bei sehr vielen gleichzeitigen Dashboard-Zugriffen. Fuer eine Ein-Personen-Installation ohne Nutzen."
  opt_frage "boto3"          N  "S3-Backup: schiebt Aufnahmen automatisch in einen S3-Speicher."
else
  OPT_AUS="faster-whisper PyMySQL redis boto3"
  [ "$MODUS" = "unattended" ] && OPT_AUS="$OPT_AUS discord.py"
fi
# uvloop gibt es auf exotischen Plattformen nicht als fertiges Rad; es ist
# reine Beschleunigung und darf fehlen.
case "$ARCH" in x86_64|amd64|aarch64|arm64) ;; *) OPT_AUS="$OPT_AUS uvloop";; esac

REQ_TMP="$(mktemp)"
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
_ausgelassen=""
[ -n "$OPT_AUS" ] && _ausgelassen=", $(t 'ausgelassen:')$OPT_AUS"
info "$(wc -l < "$REQ_TMP" | tr -d ' ') $(t 'Pakete werden installiert')${_ausgelassen}"

"$VPY" -m pip install --upgrade pip wheel >/dev/null 2>&1 || warn "pip liess sich nicht aktualisieren — weiter mit der vorhandenen Fassung."
info "pip install laeuft — das dauert je nach Verbindung 1 bis 15 Minuten."
if ! "$VPY" -m pip install -r "$REQ_TMP"; then
  fehler "Mindestens ein Paket liess sich nicht installieren."
  erklaere "Haeufigste Ursachen: kein Compiler fuer ein Paket ohne fertiges Rad (dann: sudo apt install build-essential python3-dev), oder eine abgerissene Verbindung. Wiederholen ist gefahrlos: .venv/bin/pip install -r requirements.txt"
  exit 1
fi
rm -f "$REQ_TMP"
# streamlink/yt-dlp aus den Systemquellen sind oft zu alt fuer TikTok. Im venv
# sind sie immer aktuell und haben Vorrang, weil .venv/bin frueher im PATH steht.
have streamlink || "$VPY" -m pip install streamlink || warn "streamlink liess sich nicht nachinstallieren."
have yt-dlp     || "$VPY" -m pip install yt-dlp     || warn "yt-dlp liess sich nicht nachinstallieren."
gut "Python-Pakete stehen."

# ═══════════════════════════════════════════════════════════════════════════
kopf "Konfiguration (.env)"
erklaere "Alle Einstellungen leben in einer einzigen Datei: .env. Sie enthaelt Bot-Token, Stream-Keys und Cookies — deshalb bekommt sie Rechte 600 (nur du darfst lesen) und gehoert NIE in ein Archiv oder ein Repository."

if [ -f "$ENVF" ]; then
  SICHERUNG="$ENVF.bak.$(date +%Y%m%d-%H%M%S)"
  cp "$ENVF" "$SICHERUNG"
  gut "Vorhandene .env gesichert: $(basename "$SICHERUNG")"
  info "Bestehende Werte bleiben; nur was du jetzt beantwortest, wird ueberschrieben."
else
  if [ -f "$ZIEL/.env.example" ]; then
    # .env.example ist auto-generiert und dokumentiert ~470 Variablen. Als
    # Ausgangspunkt ist das Gold wert, weil jeder Default dort schwarz auf
    # weiss steht statt nur im Quelltext.
    cp "$ZIEL/.env.example" "$ENVF"
    gut ".env aus der Vorlage angelegt (alle Vorgaben aktiv, nichts gesetzt)."
  else
    : > "$ENVF"
  fi
fi
chmod 600 "$ENVF"

# Altlast aus frueheren Vorlagen: Zeilen der Form "NAME=   # (Geheimnis — hier
# eintragen)". Das sieht wie ein Kommentar aus, ist aber der WERT — python-dotenv
# liest bei unquotierten Werten den Rest der Zeile mit. Wer .env.example je
# kopiert hat, hatte rund 40 Variablen mit genau diesem Text als Inhalt: der Bot
# hielt Discord, Twitch, YouTube und Anthropic fuer eingerichtet und meldete
# "Token abgelehnt" statt "kein Token". Die Vorlage erzeugt das nicht mehr,
# bestehende .env-Dateien muessen aber geheilt werden.
MUELL=$(grep -cE '^[A-Za-z_][A-Za-z0-9_]*=[[:space:]]*#' "$ENVF" 2>/dev/null || true)
if [ "${MUELL:-0}" -gt 0 ]; then
  tmp="$(mktemp)"
  sed -E 's/^([A-Za-z_][A-Za-z0-9_]*)=[[:space:]]*#.*$/\1=/' "$ENVF" > "$tmp" && mv "$tmp" "$ENVF"
  chmod 600 "$ENVF"
  gut "${MUELL} Platzhalter-Werte geleert (sie waeren als echte Werte gelesen worden)."
fi

env_set(){ # env_set SCHLUESSEL WERT — ersetzt die Zeile, auch die auskommentierte
  local k="$1" v="$2" tmp
  [ -z "$k" ] && return 0
  tmp="$(mktemp)"
  NC_K="$k" NC_V="$v" awk '
    BEGIN{ k=ENVIRON["NC_K"]; v=ENVIRON["NC_V"] }
    { t=$0; sub(/^[[:space:]]*#[[:space:]]*/,"",t)
      p=index(t,"="); key=(p?substr(t,1,p-1):"")
      gsub(/[[:space:]]/,"",key)
      if (key==k) next
      print }
    END{ if (v ~ /[[:space:]#]/) printf "%s=\"%s\"\n", k, v; else printf "%s=%s\n", k, v }
  ' "$ENVF" > "$tmp" && mv "$tmp" "$ENVF"
  chmod 600 "$ENVF"
}
env_get(){ awk -F= -v k="$1" '/^[[:space:]]*#/{next} {key=$1;gsub(/[[:space:]]/,"",key)}
           key==k{v=$2;for(i=3;i<=NF;i++)v=v"="$i;gsub(/^[[:space:]"]+|[[:space:]"]+$/,"",v);print v;exit}' "$ENVF" 2>/dev/null; }

# ── Telegram (Pflicht) ───────────────────────────────────────
printf '\n  %s%sTelegram — der Pflichtteil%s\n' "$B" "$TXT" "$R"
erklaere "NIGHTCRAWLER wird ueber Telegram bedient. Ohne Bot-Token startet dieser Teil nicht. Den Token gibt dir @BotFather in Telegram: /newbot, Namen vergeben, fertig — er sieht aus wie 123456789:AAF... Er ist ein Geheimnis und laesst sich nicht erzeugen, nur holen."
ALT_TOKEN="$(env_get BOT_TOKEN)"
if [ -n "$ALT_TOKEN" ] && [ "$MODUS" != "unattended" ]; then
  info "Es ist bereits ein BOT_TOKEN eingetragen."
  frage_ja "Ersetzen?" N && { frage_geheimnis TG_TOKEN "Telegram Bot-Token" 0; [ -n "$TG_TOKEN" ] && env_set BOT_TOKEN "$TG_TOKEN"; }
else
  frage_geheimnis TG_TOKEN "Telegram Bot-Token (von @BotFather)" 0
  if [ -n "${TG_TOKEN:-}" ]; then env_set BOT_TOKEN "$TG_TOKEN"; gut "BOT_TOKEN gesetzt."
  else warn "Kein Token — der Telegram-Teil bleibt still, bis du BOT_TOKEN in der .env eintraegst."
       merke "OFFEN: BOT_TOKEN in $ENVF eintragen (von @BotFather)"; fi
fi

erklaere "Ohne Freigabeliste darf JEDER, der deinen Bot findet, ihn bedienen. ALLOWED_USER_IDS ist diese Liste (Zahlen, per Komma getrennt). Deine eigene ID sagt dir @userinfobot in Telegram."
frage_text TG_IDS "Deine Telegram-Nutzer-ID (mehrere per Komma, leer = keine Sperre)" "$(env_get ALLOWED_USER_IDS)"
if [ -n "${TG_IDS:-}" ]; then env_set ALLOWED_USER_IDS "$TG_IDS"; gut "Freigabeliste gesetzt."
else warn "Keine Freigabeliste — jeder Telegram-Nutzer kann den Bot bedienen."; fi

# ── Dashboard ────────────────────────────────────────────────
printf '\n  %s%sDashboard%s\n' "$B" "$TXT" "$R"
erklaere "Das Dashboard ist die Weboberflaeche mit 359 Routen: Sendeleiste, Aufnahmen, Statistiken, Abwehr. Es bindet standardmaessig NUR auf 127.0.0.1 — also nicht im Netz erreichbar. Der sichere Zugang ist ein SSH-Tunnel; alles andere sperrt man ueber Token oder Firewall auf."
frage_text DASH_PORT "Port fuers Dashboard" "$(env_get DASHBOARD_PORT || true)"
[ -z "${DASH_PORT:-}" ] && DASH_PORT=8050
env_set DASHBOARD_PORT "$DASH_PORT"

WEBHOST="127.0.0.1"
if [ "$MODUS" = "gefuehrt" ]; then
  erklaere "Willst du das Dashboard direkt aus dem Netz erreichen (statt per SSH-Tunnel), muss es auf 0.0.0.0 lauschen. Das ist eine bewusste Oeffnung: wer den Port erreicht, kann Aufnahmen loeschen, Cookies sehen und Logs lesen. Nur mit Token UND Firewall machen."
  if frage_ja "Dashboard im Netz erreichbar machen (0.0.0.0)?" N; then
    WEBHOST="0.0.0.0"
    warn "Der Port wird oeffentlich. Token ist damit Pflicht (kommt gleich)."
    merke "SICHERHEIT: Dashboard lauscht auf 0.0.0.0 — Firewall setzen: ufw allow from <DEINE-IP> to any port ${DASH_PORT}"
  fi
fi
env_set WEB_HOST "$WEBHOST"

erklaere "Der Dashboard-Token schuetzt den Zugriff von aussen (Aufruf einmal mit ?token=..., danach haelt ein Cookie). Loopback und SSH-Tunnel bleiben immer frei. Das ist ein frei waehlbares Geheimnis — hier ist Erzeugen die bessere Wahl als Ausdenken."
frage_geheimnis DASH_TOKEN "Dashboard-Token" 1 40
[ -n "${DASH_TOKEN:-}" ] && { env_set DASHBOARD_TOKEN "$DASH_TOKEN"; gut "DASHBOARD_TOKEN gesetzt."
                              merke "Dashboard-Token: steht in .env (DASHBOARD_TOKEN)"; }
[ -z "${DASH_TOKEN:-}" ] && [ "$WEBHOST" = "0.0.0.0" ] && warn "Ohne Token und oeffentlich gebunden — bitte wenigstens die Firewall zumachen."

if [ "$MODUS" = "gefuehrt" ]; then
  erklaere "Zusaetzlich gibt es einen PIN-Login fuer die Weboberflaeche und die PWA auf dem Handy — bequemer als ein 40-Zeichen-Token im Browser. Token und PIN duerfen parallel gelten."
  if frage_ja "PIN-Login einrichten?" N; then
    frage_geheimnis DASH_PIN "Dashboard-PIN (Ziffern)" 1 6 1
    [ -n "${DASH_PIN:-}" ] && { env_set DASHBOARD_PIN "$DASH_PIN"; gut "DASHBOARD_PIN gesetzt."; }
  fi
fi

# ── Discord ──────────────────────────────────────────────────
if ! printf '%s' "$OPT_AUS" | grep -qi 'discord'; then
  printf '\n  %s%sDiscord%s\n' "$B" "$TXT" "$R"
  erklaere "Optional: dieselben Funktionen als Slash-Commands in deinem Discord-Server, dazu Moderation und Community-Features. Token aus dem Discord Developer Portal (Bot → Reset Token). Ohne Token bleibt der Discord-Teil einfach still — der Bot startet trotzdem."
  if frage_ja "Discord jetzt einrichten?" N; then
    frage_geheimnis DC_TOKEN "Discord Bot-Token" 0
    [ -n "${DC_TOKEN:-}" ] && env_set DISCORD_BOT_TOKEN "$DC_TOKEN"
    frage_text DC_GUILD "Discord-Server-ID (Guild-ID, Rechtsklick auf den Server → ID kopieren)" "$(env_get DISCORD_GUILD_ID || true)"
    [ -n "${DC_GUILD:-}" ] && env_set DISCORD_GUILD_ID "$DC_GUILD"
    frage_text DC_ROLE "Name der Admin-Rolle (fuer /ban, /timeout, /setup_*)" "$(env_get DISCORD_ADMIN_ROLE || echo Admin)"
    [ -n "${DC_ROLE:-}" ] && env_set DISCORD_ADMIN_ROLE "$DC_ROLE"
    gut "Discord konfiguriert."
  fi
fi

# ── Restream ─────────────────────────────────────────────────
printf '\n  %s%sRestream-Ziele%s\n' "$B" "$TXT" "$R"
erklaere "Restream heisst: der TikTok-Stream wird gleichzeitig auf deine eigenen Kanaele gesendet. Der Stream-Key kommt von der jeweiligen Plattform (Kick: Creator-Dashboard → Stream Key; Twitch: Creator Dashboard → Einstellungen → Stream; YouTube: Studio → Livestream). Er ist ein Geheimnis und laesst sich nicht erzeugen. Ohne Key bleibt das Ziel aus."
erklaere "Wichtig zur Last: sobald ein zweites Ziel dazukommt, muss ffmpeg umkodieren (Transcode) — das kostet ein Vielfaches an CPU. Ein Ziel ohne Transcode laeuft selbst auf schwacher Hardware."
restream_ziel(){ # restream_ziel <PRAEFIX> <Klarname> <Hinweis>
  local p="$1" name="$2" hinweis="$3" key
  if frage_ja "${name} als Restream-Ziel einrichten?" N; then
    erklaere "$hinweis"
    frage_geheimnis key "${name} Stream-Key" 0
    if [ -n "$key" ]; then
      env_set "${p}_STREAM_KEY" "$key"; env_set "${p}_ENABLED" 1
      gut "${name} eingerichtet."
    else
      env_set "${p}_ENABLED" 0
      warn "${name} ohne Key — ausgeschaltet gelassen."
    fi
  else
    env_set "${p}_ENABLED" 0
  fi
}
if [ "$MODUS" = "gefuehrt" ]; then
  restream_ziel KICK    "Kick"    "Kick ist das primaere Ziel: kein Transcode noetig, wenn es allein laeuft."
  restream_ziel TWITCH  "Twitch"  "Twitch begrenzt die Bitrate haerter als Kick — bei Problemen RESTREAM_BITRATE_K senken."
  restream_ziel YOUTUBE "YouTube" "YouTube braucht am laengsten, bis es 'live' meldet (bis zu einer Minute). Das ist normal und kein Fehler."
else
  for p in KICK TWITCH YOUTUBE; do [ -n "$(env_get "${p}_STREAM_KEY")" ] || env_set "${p}_ENABLED" 0; done
fi

# ── Leistungsprofil ──────────────────────────────────────────
if [ "$IST_PI" = 1 ] || [ "${RAM_MB:-0}" -lt 4000 ] || [ "${KERNE:-8}" -lt 4 ]; then
  printf '\n  %s%sLeistungsprofil%s\n' "$B" "$TXT" "$R"
  erklaere "Diese Maschine ist klein. Die Vorgaben des Bots sind auf einen 8-Kern-Server gemuenzt; unveraendert fuehrt das hier zu abgebrochenen Aufnahmen und stotternden Restreams. Das sparsame Profil setzt: nur ein Restream-Ziel, 3500 kbit statt 6000, je ein ffmpeg-Thread fuer Aufnahme und Hintergrund, hoechstens eine Transkription gleichzeitig."
  if frage_ja "Sparsames Profil setzen?" J; then
    env_set RESTREAM_SINGLE 1
    env_set RESTREAM_MAX_CONCURRENT 1
    env_set RESTREAM_BITRATE_K 3500
    env_set FFMPEG_THREADS_RECORD 1
    env_set FFMPEG_THREADS_BG 1
    env_set WHISPER_MAX_CONCURRENT 1
    env_set WORKER_COUNT 2
    gut "Sparsames Profil gesetzt (jederzeit in der .env aenderbar)."
    merke "Leistungsprofil: sparsam (RESTREAM_SINGLE=1, Bitrate 3500)"
  fi
fi
gut "Konfiguration geschrieben: $ENVF (Rechte 600)"

# ═══════════════════════════════════════════════════════════════════════════
kopf "Optionale Bausteine"
erklaere "Alles hier ist Zubehoer. Der Bot laeuft ohne jedes davon; er kann mit ihnen mehr. Was du jetzt auslaesst, laesst sich spaeter jederzeit nachruesten."

# ── MariaDB ──────────────────────────────────────────────────
if [ "$MODUS" = "gefuehrt" ] && ! printf '%s' "$OPT_AUS" | grep -qi 'pymysql'; then
  erklaere "Datenbank: standardmaessig SQLite — eine Datei, kein Dienst, kein Passwort, und bis in den sechsstelligen Zeilenbereich schnell genug. MariaDB lohnt erst, wenn mehrere Rechner auf dieselben Daten sollen."
  if frage_ja "Auf MariaDB umstellen?" N; then
    frage_geheimnis DBPW "Passwort fuer den Datenbank-Nutzer 'nightcrawler'" 1 24
    [ -z "${DBPW:-}" ] && DBPW="$(erzeuge_passwort 24)"
    if [ "$PKG" = "apt" ] && [ "$SKIP_SYSTEM" = 0 ] && frage_ja "MariaDB-Server lokal installieren?" J; then
      $SUDO apt-get install -y mariadb-server
      $SUDO systemctl enable --now mariadb || true
    fi
    if have mariadb || have mysql; then
      MYSQL_CLI="$(command -v mariadb || command -v mysql)"
      # Passwort ueber die Umgebung statt auf der Kommandozeile: ein Passwort
      # in argv steht in der Prozessliste und damit fuer JEDEN Nutzer sichtbar.
      if printf 'CREATE DATABASE IF NOT EXISTS nightcrawler CHARACTER SET utf8mb4;\n%s\n%s\nFLUSH PRIVILEGES;\n' \
           "CREATE USER IF NOT EXISTS 'nightcrawler'@'localhost' IDENTIFIED BY '$(printf '%s' "$DBPW" | sed "s/'/''/g")';" \
           "GRANT ALL PRIVILEGES ON nightcrawler.* TO 'nightcrawler'@'localhost';" \
         | $SUDO "$MYSQL_CLI" 2>/dev/null; then
        env_set DB_BACKEND mariadb
        env_set MARIADB_HOST 127.0.0.1
        env_set MARIADB_DB nightcrawler
        env_set MARIADB_USER nightcrawler
        env_set MARIADB_PASSWORD "$DBPW"
        gut "MariaDB eingerichtet (Datenbank und Nutzer 'nightcrawler')."
        merke "MariaDB: Nutzer nightcrawler, Passwort in .env (MARIADB_PASSWORD)"
      else
        warn "Datenbank liess sich nicht anlegen — bleibe bei SQLite."
      fi
    else
      warn "Kein MariaDB-Client gefunden — bleibe bei SQLite."
    fi
  fi
fi

# ── CrowdSec ─────────────────────────────────────────────────
if [ "$MODUS" = "gefuehrt" ] && [ "$PKG" = "apt" ] && [ "$SKIP_SYSTEM" = 0 ]; then
  erklaere "CrowdSec ist die Abwehr: es liest Logs mit, erkennt Angriffsmuster und sperrt IPs. Das Dashboard zeigt Sperren und Angriffswellen an; der sentinel-Agent meldet Spitzen. Sinnvoll, sobald die Maschine aus dem Netz erreichbar ist."
  if frage_ja "CrowdSec installieren?" N; then
    $SUDO apt-get install -y crowdsec || warn "CrowdSec fehlt in den Quellen — siehe docs/CROWDSEC.md."
    have cscli && gut "CrowdSec installiert: $(cscli version 2>/dev/null | head -1)"
    merke "CrowdSec: installiert — Feinheiten in docs/CROWDSEC.md"
  fi
fi

# ── Reverse-Proxy + HTTPS ────────────────────────────────────
# v4.1-W17: Bis hierher endete der Installer beim Dashboard auf 127.0.0.1 und
# ueberliess den Rest der Anleitung. Genau dort brach der haeufigste Weg ab:
# wer die Oberflaeche von aussen wollte, oeffnete den Port statt einen Proxy
# davorzusetzen — und stand dann ohne TLS und ohne Zertifikat da. Der Log vom
# 30.08. zeigt das Ergebnis: Dashboard auf 0.0.0.0:8050, ohne Token, mit
# Fremdzugriffen im Journal. Der Proxy ist der Weg, der das ueberfluessig macht.
if [ "$MODUS" = "gefuehrt" ] && [ "$PKG" = "apt" ] && [ "$SKIP_SYSTEM" = 0 ]; then
  erklaere "Reverse-Proxy: nginx nimmt Port 443 mit einem echten Zertifikat entgegen und reicht nach 127.0.0.1 durch. Damit bleibt der Dashboard-Port zu, die Verbindung ist verschluesselt, und die OAuth-Rueckrufe von Kick, Twitch und YouTube funktionieren ohne SSH-Tunnel — die brauchen eine oeffentlich erreichbare HTTPS-Adresse. Das Zertifikat holt certbot von Let's Encrypt und erneuert es selbst."
  if frage_ja "nginx als Reverse-Proxy mit HTTPS einrichten?" N; then
    frage_text PROXY_DOMAIN "Domain, die auf diese Maschine zeigt (z.B. bot.example.dev)" ""
    if [ -z "${PROXY_DOMAIN:-}" ]; then
      warn "Ohne Domain kein Zertifikat — uebersprungen."
    else
      $SUDO apt-get install -y nginx certbot python3-certbot-nginx \
        || warn "nginx/certbot liessen sich nicht installieren."
      if have nginx; then
        NGX="/etc/nginx/sites-available/nightcrawler"
        $SUDO tee "$NGX" >/dev/null <<NGXEOF
# NIGHTCRAWLER — erzeugt von tools/installer.sh
# certbot traegt die TLS-Zeilen selbst nach (--nginx).
server {
    listen 80;
    listen [::]:80;
    server_name ${PROXY_DOMAIN};

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
        $SUDO ln -sf "$NGX" /etc/nginx/sites-enabled/nightcrawler
        if $SUDO nginx -t >/dev/null 2>&1; then
          $SUDO systemctl reload nginx 2>/dev/null || $SUDO systemctl restart nginx 2>/dev/null || true
          gut "nginx eingerichtet."
        else
          warn "nginx-Konfiguration fehlerhaft — bitte 'sudo nginx -t' pruefen."
        fi
        if have certbot; then
          erklaere "certbot holt jetzt das Zertifikat. Dafuer muss Port 80 dieser Maschine aus dem Internet erreichbar sein und die Domain hierher zeigen — sonst schlaegt die Pruefung fehl. Die Erneuerung laeuft danach von selbst per systemd-Timer."
          if frage_ja "Zertifikat jetzt holen (Let's Encrypt)?" J; then
            $SUDO certbot --nginx -d "$PROXY_DOMAIN" --agree-tos --redirect -n \
                  --register-unsafely-without-email \
              && gut "Zertifikat aktiv, HTTP leitet auf HTTPS um." \
              || warn "certbot fehlgeschlagen — Port 80 offen? Domain zeigt hierher? Erneut: sudo certbot --nginx -d $PROXY_DOMAIN"
          fi
        fi
        # Der Bot muss seine oeffentliche Adresse kennen: sonst baut er die
        # OAuth-Rueckrufe auf localhost, und kein Anbieter erreicht die.
        env_set PUBLIC_BASE_URL "https://${PROXY_DOMAIN}"
        env_set TRUSTED_PROXIES "127.0.0.1"
        merke "Reverse-Proxy: https://${PROXY_DOMAIN} → 127.0.0.1:${DASH_PORT} (nginx + certbot)"
        merke "PUBLIC_BASE_URL und TRUSTED_PROXIES sind gesetzt — die OAuth-Rueckrufe stimmen damit ohne weitere Pflege."
      fi
    fi
  fi
fi

# ── Lokales LLM ──────────────────────────────────────────────
if [ "$MODUS" = "gefuehrt" ]; then
  erklaere "KI (AZRAEL): ohne jede Einrichtung laeuft sie ueber keylose freie Backends — das kostet nichts und braucht keinen Schluessel, ist aber langsamer und nicht immer erreichbar. Ein lokales llama.cpp antwortet in Millisekunden, kostet nichts und verlaesst die Maschine nie; es braucht rund 1 GB Platte und 2 GB RAM."
  if [ "${RAM_MB:-0}" -ge 3000 ] && [ "$ARCH" = "x86_64" ] && [ "$OS" = "Linux" ]; then
    if frage_ja "llama.cpp lokal einrichten (Download ca. 1 GB)?" N; then
      LLDIR="${LLDIR:-/opt/llamacpp}"
      $SUDO mkdir -p "$LLDIR"
      info "Suche das aktuelle Release-Paket …"
      ASSET="$("$VPY" - <<'PYEOF'
import json, urllib.request
try:
    d = json.load(urllib.request.urlopen(
        "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest", timeout=20))
    for a in d.get("assets", []):
        n = a["name"]
        if "ubuntu" in n and "x64" in n and n.endswith(".zip"):
            print(a["browser_download_url"]); break
except Exception:
    pass
PYEOF
)"
      if [ -n "$ASSET" ]; then
        $SUDO curl -Lf --progress-bar -o "$LLDIR/llama.zip" "$ASSET" && $SUDO unzip -oq "$LLDIR/llama.zip" -d "$LLDIR"
        LLBIN="$(find "$LLDIR" -name llama-server -type f 2>/dev/null | head -1)"
        [ -n "$LLBIN" ] && $SUDO chmod +x "$LLBIN"
        if [ -n "$LLBIN" ] && [ ! -f "$LLDIR/model.gguf" ]; then
          info "Lade das Modell (Qwen2.5-1.5B-Instruct, Q4_K_M, ca. 1 GB) …"
          $SUDO curl -Lf --progress-bar -o "$LLDIR/model.gguf" \
            "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf" \
            || warn "Modell-Download fehlgeschlagen — Anleitung: docs/SETUP_LLAMACPP.md"
        fi
        if [ -n "$LLBIN" ] && [ -f "$LLDIR/model.gguf" ]; then
          # -t 4 ist Absicht, keine Sparsamkeit: Aufnahmen haben Vorrang vor
          # der KI. Nice=10 und CPUWeight=50 verankern das noch einmal.
          $SUDO tee /etc/systemd/system/llamacpp.service >/dev/null <<UNIT
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
          $SUDO systemctl daemon-reload
          $SUDO systemctl enable --now llamacpp || warn "llamacpp-Dienst startete nicht — journalctl -u llamacpp -n 50"
          env_set BRAIN_LLM_BACKEND auto
          env_set BRAIN_LLAMACPP_URL "http://127.0.0.1:8080"
          gut "llama.cpp laeuft auf 127.0.0.1:8080."
          merke "Lokales LLM: llamacpp-Dienst, Modell ${LLDIR}/model.gguf"
        fi
      else
        warn "Kein passendes Release gefunden — Handanleitung: docs/SETUP_LLAMACPP.md"
      fi
    fi
  else
    info "Lokales LLM ausgelassen (nur fuer x86_64-Linux mit >= 3 GB RAM vorbereitet)."
    erklaere "Auf allen anderen Maschinen bleibt es bei den keylosen Backends. Ein Schluessel von enter.pollinations.ai (POLLINATIONS_API_KEY) macht sie spuerbar zuverlaessiger — eintragen laesst er sich jederzeit in der .env."
  fi
fi

# ── TikTok-Cookies ───────────────────────────────────────────
if [ "$MODUS" = "gefuehrt" ]; then
  erklaere "TikTok liefert manche Streams nur mit gueltiger Sitzung aus; ohne Cookies bricht die Aufloesung dann mit HTTP 403 ab. Der Bot liest sie aus tiktok_cookies.txt im Netscape-Format (Browser-Erweiterung 'Get cookies.txt'). Ohne die Datei laeuft alles — nur eben nicht bei geschuetzten Streams."
  [ -f "$ZIEL/tiktok_cookies.txt" ] && gut "tiktok_cookies.txt ist vorhanden." \
    || merke "OPTIONAL: tiktok_cookies.txt anlegen (gegen HTTP 403 bei der Stream-Aufloesung)"
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Selbsttest"
erklaere "Jetzt wird geprueft, ob das Zusammengestellte wirklich laeuft: bot.py --selfcheck laedt den kompletten Bot, prueft Werkzeuge, Konfiguration und Erreichbarkeiten und beendet sich wieder. Das ist der Unterschied zwischen 'installiert' und 'laeuft'."

SELFCHECK_RC=0
if [ -f "$ZIEL/bot.py" ]; then
  ( cd "$ZIEL" && "$VPY" bot.py --selfcheck ) || SELFCHECK_RC=$?
  case "$SELFCHECK_RC" in
    0) gut "Selbsttest ohne Befund.";;
    1) warn "Der Selbsttest meldet offene Punkte (oben rot). Meist fehlt ein Token oder ein Schluessel — der Bot startet trotzdem."
       merke "Selbsttest hatte Befunde: erneut pruefen mit  .venv/bin/python bot.py --selfcheck";;
    *) warn "Der Selbsttest liess sich nicht ausfuehren (Code ${SELFCHECK_RC})."
       info "Ersatzpruefung: Modul-Import"
       ( cd "$ZIEL" && "$VPY" -c 'import ast,sys; ast.parse(open("bot.py",encoding="utf-8").read()); print("bot.py ist syntaktisch in Ordnung")' ) \
         || { fehler "bot.py laesst sich nicht einmal einlesen — Python-Fassung pruefen."; exit 1; };;
  esac
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Autostart, MOTD, Totmann-Meldung"

# ── Startskript (immer, auch mit Dienst) ─────────────────────
cat > "$ZIEL/start.sh" <<START
#!/usr/bin/env bash
# Von tools/installer.sh erzeugt — Handstart ohne systemd.
# Der Dienst ist der Normalfall; das hier ist fuer Tests und fuers Zuschauen.
cd "\$(dirname "\$0")" || exit 1
exec .venv/bin/python bot.py "\$@"
START
chmod +x "$ZIEL/start.sh"
gut "Startskript: $ZIEL/start.sh"

DIENST=""
SYSTEMD=0
[ -d /run/systemd/system ] && have systemctl && SYSTEMD=1
if [ "$SYSTEMD" = 1 ] && { [ -n "$SUDO" ] || [ "$(id -u)" -eq 0 ]; }; then
  erklaere "Ein systemd-Dienst startet den Bot beim Booten, startet ihn nach einem Absturz neu und schreibt alles ins Journal (journalctl). Ohne ihn laeuft der Bot nur, solange deine SSH-Sitzung offen ist."
  VORHANDEN=""
  for u in nightcrawler tiktok-bot; do
    systemctl list-unit-files --no-legend "${u}.service" 2>/dev/null | grep -q . && VORHANDEN="$u" && break
  done
  [ -n "$VORHANDEN" ] && info "Vorhandener Dienst gefunden: ${VORHANDEN}"
  frage_text DIENST "Name des Dienstes" "${VORHANDEN:-nightcrawler}"
  if [ -n "${DIENST:-}" ] && frage_ja "Dienst ${DIENST} jetzt einrichten?" J; then
    $SUDO tee "/etc/systemd/system/${DIENST}.service" >/dev/null <<UNIT
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

[Install]
WantedBy=multi-user.target
UNIT
    $SUDO systemctl daemon-reload || warn "systemctl daemon-reload fehlgeschlagen."
    if frage_ja "Dienst aktivieren und starten?" J; then
      $SUDO systemctl enable --now "$DIENST" || warn "Dienst liess sich nicht aktivieren."
      sleep 2
      if systemctl is-active --quiet "$DIENST"; then
        gut "Dienst ${DIENST} laeuft."
      else
        warn "Dienst startete nicht. Grund ansehen:  journalctl -u ${DIENST} -n 60 --no-pager"
      fi
    else
      info "Spaeter:  sudo systemctl enable --now ${DIENST}"
    fi
    merke "Dienst: ${DIENST}  (Status: systemctl status ${DIENST} · Log: journalctl -u ${DIENST} -f)"
  fi
elif [ "$OS" = "Darwin" ]; then
  erklaere "macOS hat kein systemd. Das Gegenstueck heisst launchd: eine Datei in ~/Library/LaunchAgents, die den Bot beim Anmelden startet und neu startet, wenn er stirbt."
  if frage_ja "launchd-Eintrag anlegen?" J; then
    PLIST="$HOME/Library/LaunchAgents/dev.nightcrawler.bot.plist"
    mkdir -p "$(dirname "$PLIST")"
    cat > "$PLIST" <<PLISTEOF
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
    mkdir -p "$ZIEL/logs"
    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load "$PLIST" && gut "launchd-Eintrag geladen." || warn "launchctl load fehlgeschlagen."
    merke "launchd: ${PLIST}  (stoppen: launchctl unload ${PLIST})"
  fi
else
  # Container, WSL ohne systemd, oder keine Rechte: dann ist der Handstart der
  # ehrliche Weg — ein Dienst, den niemand startet, ist schlimmer als keiner.
  info "Kein systemd/launchd verfuegbar — Start von Hand:  bash ${ZIEL}/start.sh"
  erklaere "Soll der Bot dauerhaft laufen, braucht er einen Aufpasser: unter WSL 'wsl --shutdown'-fest per Aufgabenplanung, im Container per Restart-Regel, sonst tmux/screen."
fi

# ── MOTD ─────────────────────────────────────────────────────
if [ -f "$ZIEL/tools/motd.sh" ] && { [ "$OS" = "Darwin" ] || [ -d /etc/update-motd.d ] || [ "$SYSTEMD" = 1 ]; }; then
  erklaere "Die MOTD zeigt bei jedem SSH-Login den Zustand in einem Bild: Last, RAM, Platte, Dienst, Dashboard, Fehler heute, wie viele Streamer live sind und ob wirklich aufgenommen wird. Kostet einen Sekundenbruchteil pro Login. Sie ersetzt dabei die Standard-MOTD der Distribution — die kommt bei 'tools/motd.sh --uninstall' vollstaendig zurueck."
  # v4.1-W17: gehoert zur Standard-Einrichtung. Im gefuehrten Lauf weiterhin
  # eine Frage (mit Vorgabe J), im Express- und im unbeaufsichtigten Lauf
  # kommentarlos AN — vorher blieb sie dort ganz aus, obwohl sie nichts kostet
  # und das erste ist, was der Betreiber nach einem Login sieht.
  if [ "$MODUS" != "gefuehrt" ] || frage_ja "Status-MOTD beim Login einrichten?" J; then
    chmod +x "$ZIEL/tools/motd.sh"
    if [ "$OS" = "Darwin" ]; then
      BOT_DIR="$ZIEL" SERVICE="" DASH_PORT="$DASH_PORT" "$ZIEL/tools/motd.sh" --install || warn "MOTD-Einrichtung fehlgeschlagen."
    else
      $SUDO env BOT_DIR="$ZIEL" SERVICE="${DIENST:-}" DASH_PORT="$DASH_PORT" "$ZIEL/tools/motd.sh" --install \
        || warn "MOTD-Einrichtung fehlgeschlagen."
    fi
    merke "MOTD: aktiv (Vorschau: tools/motd.sh · Erkennung pruefen: tools/motd.sh --doctor)"
  fi
fi

# ── Totmann-Meldung ──────────────────────────────────────────
if [ -n "${DIENST:-}" ] && [ -f "$ZIEL/tools/notify_failure.sh" ]; then
  erklaere "Stirbt der Prozess ganz — OOM-Killer, kaputter Build, Absturz beim Start — sagt dir das sonst NIEMAND. Die Totmann-Meldung schickt bei jedem Ausfall die letzten Logzeilen per Telegram oder Discord."
  if frage_ja "Totmann-Meldung einrichten?" J; then
    chmod +x "$ZIEL/tools/notify_failure.sh"
    # notify_failure.sh liest TELEGRAM_TOKEN/TELEGRAM_CHAT_ID bzw.
    # DISCORD_WEBHOOK — Namen, die der Bot selbst NICHT benutzt (er hat
    # BOT_TOKEN und ALLOWED_USER_IDS). Ohne diese Spiegelung meldet der
    # Totmann still gar nichts; genau deshalb steht sie hier.
    _tgt="$(env_get BOT_TOKEN)"; _tgc="$(printf '%s' "$(env_get ALLOWED_USER_IDS)" | cut -d, -f1)"
    [ -n "$_tgt" ] && [ -z "$(env_get TELEGRAM_TOKEN)" ]   && env_set TELEGRAM_TOKEN "$_tgt"
    [ -n "$_tgc" ] && [ -z "$(env_get TELEGRAM_CHAT_ID)" ] && env_set TELEGRAM_CHAT_ID "$_tgc"
    _dcw="$(env_get DISCORD_WEBHOOK_URL)"
    [ -n "$_dcw" ] && [ -z "$(env_get DISCORD_WEBHOOK)" ]  && env_set DISCORD_WEBHOOK "$_dcw"
    $SUDO tee /etc/systemd/system/nightcrawler-notify@.service >/dev/null <<UNIT
[Unit]
Description=NIGHTCRAWLER Totmann-Meldung fuer %i

[Service]
Type=oneshot
User=$(id -un)
EnvironmentFile=${ENVF}
ExecStart=${ZIEL}/tools/notify_failure.sh %i
UNIT
    $SUDO mkdir -p "/etc/systemd/system/${DIENST}.service.d"
    $SUDO tee "/etc/systemd/system/${DIENST}.service.d/onfailure.conf" >/dev/null <<UNIT
[Unit]
OnFailure=nightcrawler-notify@%n.service
UNIT
    $SUDO systemctl daemon-reload || warn "systemctl daemon-reload fehlgeschlagen."
    gut "Totmann-Meldung verdrahtet."
    info "Testen (MUSS eine Nachricht ausloesen):  sudo systemctl start nightcrawler-notify@${DIENST}.service"
    merke "Totmann-Meldung: aktiv — Test: sudo systemctl start nightcrawler-notify@${DIENST}.service"
  fi
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Zusammenfassung"

NOTIZ="$HOME/nightcrawler-installation.txt"
{
  printf 'NIGHTCRAWLER v37 — Installation vom %s\n' "$(date '+%F %H:%M')"
  printf '%s\n\n' "$(printf '=%.0s' $(seq 1 60))"
  printf 'Verzeichnis   %s\n' "$ZIEL"
  printf 'Python        %s\n' "$("$VPY" -V 2>&1)"
  printf 'Konfiguration %s   (Rechte 600 — enthaelt Geheimnisse)\n' "$ENVF"
  [ -n "${DIENST:-}" ] && printf 'Dienst        %s\n' "$DIENST"
  printf 'Dashboard     http://127.0.0.1:%s\n\n' "$DASH_PORT"
  printf 'BEDIENUNG\n'
  [ -n "${DIENST:-}" ] && printf '  Status      systemctl status %s\n  Log         journalctl -u %s -f\n  Neustart    sudo systemctl restart %s\n' "$DIENST" "$DIENST" "$DIENST"
  printf '  Handstart   bash %s/start.sh\n' "$ZIEL"
  printf '  Selbsttest  %s/bot.py --selfcheck\n' "$VENV/bin/python"
  printf '  Dashboard   ssh -L 3000:localhost:%s %s@<server-ip>   → http://localhost:3000\n\n' "$DASH_PORT" "$(id -un)"
  if [ -n "$MERKZETTEL" ]; then printf 'MERKZETTEL\n'; printf '%s' "$MERKZETTEL" | sed 's/^/  · /'; printf '\n'; fi
  printf 'WEITERLESEN\n'
  printf '  docs/START_HIER.txt   Einstieg und Alltag\n'
  printf '  docs/DEPLOY.md        Ausliefern, Rollback, Pruefschritte\n'
  printf '  docs/CROWDSEC.md      Abwehr\n'
  printf '  docs/SETUP_*.md       OAuth fuer Twitch und YouTube, llama.cpp\n'
} > "$NOTIZ"

printf '\n'
gut "NIGHTCRAWLER ist eingerichtet."
printf '\n'
printf '  %sVerzeichnis%s   %s\n' "$DIM" "$R" "$ZIEL"
printf '  %sPython%s        %s\n' "$DIM" "$R" "$("$VPY" -V 2>&1)"
[ -n "${DIENST:-}" ] && printf '  %sDienst%s        %s\n' "$DIM" "$R" "$DIENST"
printf '  %sDashboard%s     http://127.0.0.1:%s\n' "$DIM" "$R" "$DASH_PORT"
printf '\n'
if [ -n "$MERKZETTEL" ]; then
  printf '  %s%sMerkzettel%s\n' "$B" "$TXT" "$R"
  printf '%s' "$MERKZETTEL" | sed "s/^/    ${DIM}·${R} /"
  printf '\n'
fi
printf '  %s%sNaechste Schritte%s\n' "$B" "$TXT" "$R"
if [ -n "${DIENST:-}" ]; then
  printf '    1  Mitlesen, ob er sauber hochkommt:  %sjournalctl -u %s -f%s\n' "$TXT" "$DIENST" "$R"
else
  printf '    1  Starten und zuschauen:  %sbash %s/start.sh%s\n' "$TXT" "$ZIEL" "$R"
fi
printf '    2  In Telegram deinen Bot anschreiben:  %s/start%s, dann %s/track <tiktok-name>%s\n' "$TXT" "$R" "$TXT" "$R"
printf '    3  Dashboard per Tunnel oeffnen:  %sssh -L 3000:localhost:%s %s@<server-ip>%s\n' "$TXT" "$DASH_PORT" "$(id -un)" "$R"
printf '\n'
printf '  %sAlles davon steht auch in %s%s\n' "$FNT" "$NOTIZ" "$R"
printf '\n'
exit 0
