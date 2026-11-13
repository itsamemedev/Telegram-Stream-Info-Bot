#!/usr/bin/env sh
# NIGHTCRAWLER — gemeinsame System-Erkennung fuer die Shell-Werkzeuge (v4.2-W123)
#
# WARUM ES DAS GIBT
# installer.sh erkannte bis hierher genau zwei Paketmanager (apt, brew) und
# schrieb die Paketnamen fest in seine Zweige. tools/update.sh braucht dieselbe
# Antwort — und zwei Kopien derselben Erkennung laufen auseinander; das ist die
# Lehre aus W98 (zwei Ordner-Aufloesungen) und W100 (zwei Ausschlusslisten).
# Deshalb steht sie hier, EINMAL, und beide Werkzeuge sourcen sie.
#
# POSIX-sh, keine Arrays, kein local: die Datei laeuft auch unter dash, und
# installer.sh sourct sie, bevor ueberhaupt feststeht, was installiert ist.
#
# PRUEFBAR OHNE ROOT UND OHNE PAKETMANAGER. Drei Stellschrauben, alle fuer die
# Vertraege und fuer den Trockenlauf:
#   NC_OS_RELEASE   statt /etc/os-release (Distribution vorgeben)
#   NC_PKG          Paketmanager erzwingen (apt|dnf|pacman|zypper|apk|brew|keiner)
#   NC_UNAME        statt uname -s
# Eine Erkennung, die man nur auf echter Hardware pruefen kann, prueft niemand.

# Die NC_*-Variablen sind die Schnittstelle: gelesen werden sie von den
# Werkzeugen, die diese Datei sourcen — shellcheck sieht das von hier aus nicht.
# shellcheck disable=SC2034
true

# ── Erkennung ────────────────────────────────────────────────
# Setzt NC_OS (Linux|Darwin|…), NC_DISTRO (ID aus os-release), NC_DISTRO_NAME,
# NC_PKG (apt|dnf|pacman|zypper|apk|brew|keiner) und NC_IST_PI (0|1).
#
# Entschieden wird an ID und ID_LIKE aus os-release, nicht am Vorhandensein
# eines Binaries: auf einer Fedora-Maschine kann ein apt-get herumliegen (aus
# einem Container-Werkzeug), und dann haette die Binary-Suche Debian-Pakete
# installieren wollen. Erst wenn os-release nichts sagt, wird nach dem Binary
# gesucht — und dann in einer festen Reihenfolge, damit zwei Laeufe auf
# derselben Maschine dasselbe Ergebnis liefern.
nc_system_erkennen(){
  NC_OS="${NC_UNAME:-$(uname -s 2>/dev/null || echo unbekannt)}"
  NC_DISTRO=""; NC_DISTRO_NAME=""; NC_IST_PI=0
  _rel="${NC_OS_RELEASE:-/etc/os-release}"
  _id=""; _like=""
  if [ "$NC_OS" = "Linux" ] && [ -r "$_rel" ]; then
    # Nicht sourcen: os-release ist eine Datei des Systems, und ein `.` darauf
    # fuehrt sie als Code aus. Gelesen werden genau drei Schluessel.
    _id="$(sed -n 's/^ID=//p' "$_rel" | tr -d '"' | head -1)"
    _like="$(sed -n 's/^ID_LIKE=//p' "$_rel" | tr -d '"' | head -1)"
    NC_DISTRO_NAME="$(sed -n 's/^PRETTY_NAME=//p' "$_rel" | tr -d '"' | head -1)"
  fi
  NC_DISTRO="${_id:-$NC_OS}"
  [ -n "$NC_DISTRO_NAME" ] || NC_DISTRO_NAME="$NC_DISTRO"
  if [ "$NC_OS" = "Linux" ]; then
    grep -qi 'raspberry' /proc/device-tree/model 2>/dev/null && NC_IST_PI=1
    [ "$NC_DISTRO" = "raspbian" ] && NC_IST_PI=1
  fi

  if [ -n "${NC_PKG:-}" ]; then
    return 0          # ausdruecklich vorgegeben — Vertraege und --pkg
  fi
  NC_PKG="keiner"
  case "$NC_OS" in
    Darwin)
      command -v brew >/dev/null 2>&1 && NC_PKG="brew"
      return 0;;
    Linux) ;;
    *) return 0;;
  esac
  # Reihenfolge ist Absicht: die eigene ID zuerst, dann die Verwandtschaft.
  # "rocky" traegt ID_LIKE="rhel centos fedora" — ohne die zweite Stufe
  # bliebe RHEL-Abkoemmlingen der Paketmanager verborgen.
  for _x in $_id $_like; do
    case "$_x" in
      debian|ubuntu|raspbian|linuxmint|pop) NC_PKG="apt"; return 0;;
      fedora|rhel|centos|rocky|almalinux|ol|amzn) NC_PKG="dnf"; return 0;;
      arch|manjaro|endeavouros|artix) NC_PKG="pacman"; return 0;;
      opensuse*|suse|sles|sled) NC_PKG="zypper"; return 0;;
      alpine) NC_PKG="apk"; return 0;;
    esac
  done
  for _x in apt-get dnf pacman zypper apk; do
    if command -v "$_x" >/dev/null 2>&1; then
      case "$_x" in apt-get) NC_PKG="apt";; *) NC_PKG="$_x";; esac
      return 0
    fi
  done
  return 0
}

# ── Paketnamen ───────────────────────────────────────────────
# nc_paketname WERKZEUG [PKG] -> Kandidaten, durch Leerzeichen getrennt, in
# Vorzugsreihenfolge. Leer heisst: dieser Paketmanager fuehrt das Werkzeug
# nicht — dann ist pip der Weg (streamlink, yt-dlp) oder es gibt keinen.
#
# Zwei Faelle, die nicht offensichtlich sind und deshalb hier stehen:
#   * ffmpeg auf Fedora: das Paket "ffmpeg" liegt in RPM Fusion, in den
#     Fedora-Quellen steht nur "ffmpeg-free" (ohne x264). Fuer die Aufnahme
#     (-c copy) reicht das, fuer den Transcode-Restream nicht — deshalb steht
#     "ffmpeg" vorn, und update.sh sagt, welches es geworden ist.
#   * sqlite3 heisst ausser auf Debian und openSUSE "sqlite".
nc_paketname(){
  _w="$1"; _p="${2:-$NC_PKG}"
  case "$_p:$_w" in
    *:git|*:curl)          printf '%s' "$_w";;
    dnf:ffmpeg)            printf 'ffmpeg ffmpeg-free';;
    *:ffmpeg)              printf 'ffmpeg';;
    apt:sqlite3|zypper:sqlite3) printf 'sqlite3';;
    *:sqlite3)             printf 'sqlite';;
    apt:streamlink|dnf:streamlink|pacman:streamlink|apk:streamlink|brew:streamlink)
                           printf 'streamlink';;
    zypper:streamlink)     printf 'python3-streamlink';;
    *:streamlink)          printf '';;
    apt:yt-dlp|dnf:yt-dlp|pacman:yt-dlp|zypper:yt-dlp|apk:yt-dlp|brew:yt-dlp)
                           printf 'yt-dlp';;
    *:yt-dlp)              printf '';;
    # v4.2-W124: was der Installer ueber die Werkzeuge hinaus braucht.
    *:unzip|*:nginx|*:ca-certificates) printf '%s' "$_w";;
    apt:mariadb|dnf:mariadb) printf 'mariadb-server';;
    *:mariadb)             printf 'mariadb';;
    apt:certbot-nginx|dnf:certbot-nginx|zypper:certbot-nginx)
                           printf 'certbot python3-certbot-nginx';;
    pacman:certbot-nginx|apk:certbot-nginx) printf 'certbot certbot-nginx';;
    *:certbot-nginx)       printf '';;
    # CrowdSec liegt nur bei Debian/Ubuntu in den Quellen des Projekts, die
    # der Installer kennt. Ueberall sonst: docs/CROWDSEC.md, nicht raten.
    apt:crowdsec)          printf 'crowdsec';;
    *:crowdsec)            printf '';;
    # v4.2-W127: nur, was nachgesehen ist (apt-cache policy auf Ubuntu 24.04:
    # prometheus 2.45). Grafana liegt bei Debian/Ubuntu NICHT in den Quellen —
    # dafuer traegt observability.sh auf Wunsch apt.grafana.com ein. Fuer die
    # anderen Manager stehen hier keine Namen, bis jemand sie nachgesehen hat:
    # ein geratener Name scheitert erst beim Installieren.
    apt:prometheus)        printf 'prometheus';;
    *:prometheus)          printf '';;
    *:grafana)             printf '';;
    # Python >= 3.12 — Kandidaten in Vorzugsreihenfolge. Auf Arch, Alpine
    # und Fedora ist "das" Python aktuell genug; Debian/openSUSE fuehren
    # Fassungen nebeneinander. Das venv-Paket ist ein apt-Sonderfall (siehe
    # nc_venvpaket).
    apt:python)            printf 'python3.13 python3.12';;
    dnf:python)            printf 'python3.13 python3.12 python3';;
    pacman:python)         printf 'python';;
    zypper:python)         printf 'python313 python312';;
    apk:python)            printf 'python3';;
    brew:python)           printf 'python@3.13';;
    *)                     printf '';;
  esac
}

# ── v5.1-W181: Bauwerkzeuge fuer ik_llama.cpp ────────────────
# nc_baupakete [PKG] -> ALLE Pakete, die ein C++-Bau mit cmake braucht.
# Bewusst NICHT ueber nc_paketname: dort sind mehrere Namen KANDIDATEN
# ("ffmpeg ffmpeg-free" = das erste, das es gibt), hier gehoeren alle
# zusammen — ein Compiler ohne make baut genauso wenig wie keiner. Leer heisst:
# fuer diesen Paketmanager nicht nachgesehen; dann selbst bereitstellen.
nc_baupakete(){
  case "${1:-$NC_PKG}" in
    apt)           printf 'build-essential cmake git';;
    dnf|zypper)    printf 'gcc-c++ make cmake git';;
    pacman)        printf 'base-devel cmake git';;
    apk)           printf 'build-base cmake git';;
    *)             printf '';;
  esac
}

# ── Paket verfuegbar? ────────────────────────────────────────
# nc_paket_verfuegbar PAKET -> 0, wenn der Paketmanager es kennt. Ohne diese
# Frage wuerde "ffmpeg ffmpeg-free" auf Fedora ohne RPM Fusion am ersten
# Kandidaten scheitern und den zweiten nie versuchen.
nc_paket_verfuegbar(){
  case "$NC_PKG" in
    apt)    apt-cache show "$1" >/dev/null 2>&1;;
    dnf)    dnf -q info "$1" >/dev/null 2>&1;;
    pacman) pacman -Si "$1" >/dev/null 2>&1;;
    zypper) zypper --non-interactive info "$1" 2>/dev/null | grep -q '^Name';;
    apk)    apk search -e "$1" 2>/dev/null | grep -q .;;
    brew)   brew info "$1" >/dev/null 2>&1;;
    *)      return 1;;
  esac
}

# ── Installationsbefehl ──────────────────────────────────────
# nc_installbefehl PAKET… -> die Kommandozeile, die installieren WUERDE.
# Als Text, nicht als Aufruf: der Trockenlauf zeigt sie, der echte Lauf fuehrt
# genau sie aus. Zwei Wege fuer dasselbe waeren zwei Befehle, die
# auseinanderlaufen koennen — und dann zeigt der Trockenlauf etwas anderes,
# als der echte Lauf tut.
#
# pacman bewusst OHNE -y: "pacman -Sy paket" ist ein Teil-Upgrade, das Arch
# ausdruecklich nicht unterstuetzt und das Bibliotheken zerreissen kann.
nc_installbefehl(){
  case "$NC_PKG" in
    apt)    printf 'apt-get install -y %s' "$*";;
    dnf)    printf 'dnf install -y %s' "$*";;
    pacman) printf 'pacman -S --needed --noconfirm %s' "$*";;
    zypper) printf 'zypper --non-interactive install %s' "$*";;
    apk)    printf 'apk add %s' "$*";;
    brew)   printf 'brew install %s' "$*";;
    *)      return 1;;
  esac
}

# Paketquellen auffrischen, wo der Manager das vor einer Installation braucht.
# apt ohne update scheitert auf einem frischen Image an leeren Listen; apk
# ebenso. dnf/zypper/pacman/brew frischen selbst auf (pacman -S tut es nicht,
# aber -Sy waere das Teil-Upgrade von oben — dort bleibt es beim Hinweis).
nc_auffrischbefehl(){
  case "$NC_PKG" in
    apt) printf 'apt-get update -qq';;
    apk) printf 'apk update -q';;
    *)   return 1;;
  esac
}

# Sind die Paketlisten leer? Nur apt und apk halten sie getrennt vom
# Installieren; dort heisst ein leerer Abgleich "nie aufgefrischt", nicht
# "Paket gibt es nicht". NC_APT_LISTEN/NC_APK_CACHE: fuer die Vertraege.
nc_quellen_leer(){
  case "$NC_PKG" in
    apt) _muster="${NC_APT_LISTEN:-/var/lib/apt/lists}/*_Packages*";;
    apk) _muster="${NC_APK_CACHE:-/var/cache/apk}/APKINDEX*";;
    *)   return 1;;
  esac
  # Ein Glob, der nichts trifft, bleibt woertlich stehen — daher der -e-Test.
  for _f in $_muster; do [ -e "$_f" ] && return 1; done
  return 0
}

# Braucht dieser Paketmanager root? brew verweigert sich unter root sogar.
nc_braucht_root(){ [ "$NC_PKG" != "brew" ]; }

# ── v4.2-W124: was der Installer ueber den Paketmanager hinaus wissen muss ──

# nc_venvpaket PYTHON-FASSUNG -> Paket, das "python -m venv" moeglich macht.
# Nur Debian trennt ensurepip ab; ohne das passende Paket scheitert venv mit
# "ensurepip is not available" — die haeufigste Sackgasse auf Debian.
nc_venvpaket(){
  case "$NC_PKG" in
    apt) printf 'python%s-venv' "$1";;
    *)   printf '';;
  esac
}

# nc_init_erkennen -> NC_INIT: systemd | launchd | openrc | keiner
#
# Entschieden wird am LAUFENDEN Init, nicht am installierten Werkzeug:
# systemctl liegt in vielen Containern herum, ohne dass systemd PID 1 ist —
# ein Dienst, den dort niemand startet, ist schlimmer als keiner.
# NC_INIT von aussen ueberstimmt alles (Vertraege, --no-service).
nc_init_erkennen(){
  if [ -n "${NC_INIT:-}" ]; then return 0; fi
  NC_INIT="keiner"
  case "${NC_OS:-$(uname -s 2>/dev/null)}" in
    Darwin) command -v launchctl >/dev/null 2>&1 && NC_INIT="launchd";;
    Linux)
      if [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
        NC_INIT="systemd"
      elif command -v openrc-run >/dev/null 2>&1 || [ -x /sbin/openrc-run ]; then
        NC_INIT="openrc"
      fi;;
  esac
  return 0
}

# nc_motd_weg -> NC_MOTD_WEG: update-motd | shellrc | keiner
# update-motd: Debian/Ubuntu (pam_motd + /etc/update-motd.d); shellrc: macOS.
# Ueberall sonst gibt es keinen Mechanismus, den motd.sh --install kennt — dort
# wird nichts eingerichtet und es auch so gesagt.
nc_motd_weg(){
  if [ -n "${NC_MOTD_WEG:-}" ]; then return 0; fi
  NC_MOTD_WEG="keiner"
  case "${NC_OS:-$(uname -s 2>/dev/null)}" in
    Darwin) NC_MOTD_WEG="shellrc";;
    Linux)  [ -d /etc/update-motd.d ] && NC_MOTD_WEG="update-motd";;
  esac
  return 0
}

# nc_nginx_ziel -> Pfad der Server-Datei fuer nginx. Debian aktiviert ueber
# sites-enabled (Verweis), Alpine liest http.d/, der Rest conf.d/.
nc_nginx_ziel(){
  case "$NC_PKG" in
    apt) printf '/etc/nginx/sites-available/nightcrawler';;
    apk) printf '/etc/nginx/http.d/nightcrawler.conf';;
    *)   printf '/etc/nginx/conf.d/nightcrawler.conf';;
  esac
}

# nc_firewall_hinweis PORT -> der Befehl, der den Port fuer EINE Adresse
# oeffnet. ufw auf Debian/Ubuntu, firewalld auf Fedora/RHEL/openSUSE. Ein
# ufw-Befehl auf Fedora ist eine Anleitung, die nicht laeuft.
nc_firewall_hinweis(){
  case "$NC_PKG" in
    dnf|zypper) printf "firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=<DEINE-IP> port port=%s protocol=tcp accept' && firewall-cmd --reload" "$1";;
    *)          printf 'ufw allow from <DEINE-IP> to any port %s' "$1";;
  esac
}

# nc_mariadb_sql DB NUTZER PASSWORT -> das SQL fuer Datenbank und Nutzer
#
# v4.2-W143: EINE Stelle fuer Installer und update.sh. Vorher stand der Block
# nur im Installer; ein zweiter Weg (der Umzug in update.sh) haette ihn
# abgeschrieben, und zwei Fassungen laufen auseinander (W100). Gedacht fuer
# eine Pipe in den Client — das Passwort ueber die Standardeingabe, nie in
# argv (dort stuende es in der Prozessliste). IF NOT EXISTS + ALTER USER: ein
# zweiter Lauf gleicht nur an.
#
# DREI Hosts, nicht einer (Codex, PR #191): der Bot verbindet per TCP auf
# MARIADB_HOST=127.0.0.1. MariaDB ordnet 127.0.0.1 dem Konto @'localhost' nur
# zu, wenn es den Namen aufloest — mit skip-name-resolve (auf Servern und in
# Containern ueblich) kommt "Host '127.0.0.1' is not allowed" (1130), gemessen
# gegen MariaDB 10.11. @'localhost' bleibt fuer den Socket, ::1 fuer IPv6.
#
# Maskiert werden Backslash UND Anfuehrungszeichen: ohne NO_BACKSLASH_ESCAPES
# liest MariaDB '\' in einem Literal als Escape — ein Passwort mit Backslash
# kaeme veraendert an, und der Bot stuende mit dem Wert aus der .env vor 1045.
nc_mariadb_sql(){
  _db="$1"; _nu="$2"; _pw="$(printf '%s' "$3" | sed -e 's/\\/\\\\/g' -e "s/'/''/g")"
  printf 'CREATE DATABASE IF NOT EXISTS `%s` CHARACTER SET utf8mb4 COLLATE utf8mb4_nopad_bin;\n' "$_db"
  # v4.2-W151: bytegenau wie SQLite (siehe nc/schema.py KOLLATION). Eine schon
  # bestehende Datenbank behaelt ihre Vorgabe — die Tabellen gleicht der Bot an.
  printf 'ALTER DATABASE `%s` CHARACTER SET utf8mb4 COLLATE utf8mb4_nopad_bin;\n' "$_db"
  for _h in localhost 127.0.0.1 ::1; do
    printf "CREATE USER IF NOT EXISTS '%s'@'%s' IDENTIFIED BY '%s';\n" "$_nu" "$_h" "$_pw"
    printf "ALTER USER '%s'@'%s' IDENTIFIED BY '%s';\n" "$_nu" "$_h" "$_pw"
    printf "GRANT ALL PRIVILEGES ON \`%s\`.* TO '%s'@'%s';\n" "$_db" "$_nu" "$_h"
  done
  printf 'FLUSH PRIVILEGES;\n'
}

# ── v5.2-W193: MariaDB-Feinschliff (Installer und update.sh) ──────────────
# nc_mysqlclient_pakete [Paketmanager] -> Systempakete zum Bauen von mysqlclient
# Nur, was nachgesehen ist (Ubuntu 24.04: libmariadb-dev 1:10.11). Fuer andere
# Manager steht hier nichts — ein geratener Name scheitert erst beim
# Installieren, und PyMySQL bleibt dann ohnehin der Treiber (W127-Regel).
nc_mysqlclient_pakete(){
  case "${1:-$NC_PKG}" in
    apt) printf 'libmariadb-dev pkg-config build-essential python3-dev';;
    *)   printf '';;
  esac
}

# nc_mariadb_konf_pfad -> Pfad der eigenen Konfigurationsdatei (leer = kein
# bekanntes Verzeichnis). Debian/Ubuntu lesen mariadb.conf.d, RHEL my.cnf.d.
nc_mariadb_konf_pfad(){
  for _d in /etc/mysql/mariadb.conf.d /etc/my.cnf.d; do
    [ -d "${W:-}$_d" ] && { printf '%s/90-nightcrawler.cnf' "$_d"; return 0; }
  done
  printf ''
}

# nc_mariadb_konf_text SKIP DATEI -> schreibt die Datei. SKIP=1: skip_name_resolve.
# Ohne Konto fuer 127.0.0.1 (von Hand angelegt, nur @'localhost') faende der
# Bot sich damit vor "Access denied" (1045, gemessen gegen MariaDB 10.11) —
# der Aufrufer prueft das vorher (nc_mariadb_tcp_konto) und gibt dann 0.
nc_mariadb_konf_text(){
  _skip=""
  [ "${1:-1}" = 1 ] && _skip="skip_name_resolve = 1"
  cat > "$2" <<KONF
# NIGHTCRAWLER (v5.2-W193) — geschrieben von tools/installer.sh bzw.
# tools/update.sh --mariadb-konf; der naechste Lauf gleicht sie an.
[mysqld]
# skip_name_resolve: kein Namens-Nachschlag je neuer Verbindung — kostet
# einen DNS-Rundgang und haengt, wenn DNS haengt. Die Konten des Bots stehen
# auf localhost, 127.0.0.1 und ::1 (nc_mariadb_sql).
$_skip
# Wie SQLite mit synchronous=NORMAL: das Protokoll wird je Commit
# geschrieben, aber nur einmal je Sekunde auf die Platte gezwungen. Ein
# Absturz von MariaDB verliert nichts, ein Stromausfall hoechstens die letzte
# Sekunde — und die Platte bekommt keinen fsync je Commit mehr.
innodb_flush_log_at_trx_commit = 2
KONF
}

# nc_mariadb_tcp_konto NUTZER CLI... -> 0, wenn NUTZER ein Konto fuer
# 127.0.0.1, ::1 oder % hat (dann ist skip_name_resolve sicher).
nc_mariadb_tcp_konto(){
  _nu="$(printf '%s' "$1" | sed "s/'/''/g")"; shift
  _n="$(printf "SELECT COUNT(*) FROM mysql.user WHERE User='%s' AND Host IN ('127.0.0.1','::1','%%');\n" "$_nu" \
        | "$@" -N 2>/dev/null | tr -d '[:space:]')"
  [ -n "$_n" ] && [ "$_n" != "0" ]
}

# nc_dienst_finden -> NC_DIENST: Name der Bot-Unit (nightcrawler | tiktok-bot) oder leer
# Dieselben zwei Namen wie im Installer; die Doku nennt tiktok-bot, der
# Installer legt nightcrawler an.
nc_dienst_finden(){
  NC_DIENST=""
  command -v systemctl >/dev/null 2>&1 || return 0
  for _u in nightcrawler tiktok-bot; do
    if systemctl list-unit-files --no-legend "${_u}.service" 2>/dev/null | grep -q .; then
      NC_DIENST="$_u"; return 0
    fi
  done
  return 0
}

# v5.4-W195: Warum die TikTok-Werkzeuge in der venv erneuert werden muessen —
# leer, wenn nichts zu tun ist. EINE Regel fuer Installer und update.sh: der
# Installer rief pip bei jedem Lauf (nicht idempotent), update.sh nur mit
# Grund. Geprueft ohne Netz; das Datum steckt in der yt-dlp-Fassung.
#   nc_tt_grund <venv-python>
nc_tt_grund(){
  [ -x "$1" ] || return 0
  "$1" - 2>/dev/null <<'PY'
import datetime, importlib.util
g = []
try:
    import yt_dlp.version as v
    alter = (datetime.date.today() - datetime.date(*map(int, v.__version__.split(".")[:3]))).days
    if alter > 30:
        g.append("yt-dlp %s ist %d Tage alt" % (v.__version__, alter))
except (ImportError, ValueError, TypeError):
    g.append("yt-dlp fehlt in der venv")
if importlib.util.find_spec("curl_cffi") is None:
    g.append("curl_cffi fehlt (yt-dlp kann keinen Browser nachahmen)")
if importlib.util.find_spec("streamlink") is None:
    g.append("streamlink fehlt in der venv")
print("; ".join(g))
PY
}


# nc_emoji_pakete [Paketmanager] -> Schriftpakete, die fuer Emoji fehlen (je Zeile)
#
# v5.9-W205. Zwei Wege zeichnen Emoji, und jeder braucht eine andere Schrift:
#   * der Chat-Kasten im Sendebild (Chromium) eine FARB-Schrift
#     -> fonts-noto-color-emoji;
#   * der eingebrannte Chat in Aufnahmen (libass) eine UMRISS-Schrift — libass
#     ueberspringt Bitmap-Schriften wie Noto Color Emoji -> fonts-symbola.
# Ohne sie steht fuer jedes Emoji ein Kaestchen da. Geprueft wird an U+1F339
# (Rose): DejaVu Sans fuehrt U+1F600 bis U+1F64F selbst und haette eine
# Pruefung an 😀 bestanden, ohne dass eine Rose oder ein Krankenhaus ginge.
# Nur apt: die Paketnamen der anderen Verwalter sind nicht nachgesehen.
nc_emoji_pakete(){
  _p="${1:-$NC_PKG}"
  [ "$_p" = "apt" ] || return 0
  if ! command -v fc-list >/dev/null 2>&1; then
    printf '%s\n' fonts-noto-color-emoji fonts-symbola
    return 0
  fi
  fc-list 2>/dev/null | grep -qi "Noto Color Emoji" || printf '%s\n' fonts-noto-color-emoji
  fc-list ':charset=1f339:outline=true' 2>/dev/null | grep -q . || printf '%s\n' fonts-symbola
  return 0
}
