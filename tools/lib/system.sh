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
