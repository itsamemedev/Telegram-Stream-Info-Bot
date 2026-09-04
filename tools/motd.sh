#!/usr/bin/env bash
#
# NIGHTCRAWLER — Message of the Day (Login-Statusbild)
#
#   ./motd.sh                  Vorschau (aendert nichts)
#   sudo ./motd.sh --install   als /etc/update-motd.d/99-nightcrawler einhaengen
#   sudo ./motd.sh --uninstall wieder entfernen
#   ./motd.sh --doctor         zeigt, WAS erkannt wurde und woher
#
# WARUM DIESE FASSUNG
# Die erste Version hatte alle Pfade fest verdrahtet (/home/ubuntu/tiktok-bot,
# bot_v37.py, Dienst "tiktok-bot"). Auf jeder anderen Maschine — und seit W119
# auch auf dieser, weil bot_v37.py zu bot.py wurde — zeigte sie stumm einen
# leeren Rahmen: kein Fehler, nur keine Daten. Diese Fassung erkennt die
# Installation selbst, schreibt das Ergebnis beim --install in eine Konfig
# (/etc/nightcrawler/motd.conf) und ist damit auf jeder Box richtig.
#
# Weitere Unterschiede, jeder aus einem konkreten Fehlbild:
#   * Plattform-Chips lasen JEDEN .env-Schluessel, der "KICK" enthielt. Ein
#     gesetztes KICK_INGEST_URL machte Kick gruen, obwohl KICK_ENABLED=0 war.
#     Jetzt entscheidet <PLAT>_ENABLED, danach erst ein echter Stream-Key.
#   * "BARW=10 bar ..." — Zuweisung vor einem FUNKTIONSaufruf bleibt in bash
#     nach der Rueckkehr stehen. Die Breite war ab da global kaputt. Jetzt
#     nimmt bar() die Breite als zweites Argument.
#   * du/find ueber eine 400-GB-Aufnahmebibliothek lief bei JEDEM Login. Das
#     Ergebnis wird jetzt 15 Minuten zwischengespeichert.
#   * Dashboard galt als "auf", sobald der Port lauschte. Ein haengender Flask
#     lauscht auch. Jetzt wird /healthz wirklich gefragt.
#   * Laeuft auf bash 3.2 (macOS) mit: keine assoziativen Arrays, /proc-Zugriffe
#     sind eingezaeunt, fuer Darwin gibt es eigene Zweige.
#
# NEU IN v2.1 (v4.2-W7) — vier Anzeigen, jede aus einer Frage, die die alte
# Fassung nicht beantwortet hat:
#   * GESAMTAMPEL im Kopf. Acht Bloecke sind zu viel fuer einen Blick; per
#     Handy-SSH sieht man drei, ohne zu scrollen. Der schlimmste Befund steht
#     jetzt in Zeile zwei. Dafuer laufen die Proben fuer Dienst und Dashboard
#     VOR dem Kopf statt mitten in der Ausgabe — dieselben Aufrufe, nur
#     frueher, die Anzeige kostet keine Millisekunde mehr.
#   * NETZDURCHSATZ. "Bot laeuft" und "es geht wirklich etwas raus" sind zwei
#     verschiedene Fragen; die zweite blieb bisher offen. Gemessen im SELBEN
#     Fenster wie die CPU — ein eigener sleep waere der teuerste Posten der
#     ganzen MOTD geworden.
#   * FEHLERVERLAUF ueber sieben Tage. Eine nackte 4 sagt nichts: vier Fehler
#     hinter sechs stillen Tagen sind ein Ausbruch, vier hinter sechs Tagen mit
#     je dreissig sind eine Verbesserung.
#   * VERLAUFSBALKEN in Truecolor. Jede Zelle traegt die Farbe ihrer Position,
#     der Balken liest sich als Thermometer — 85 % sind sichtbar heiss, bevor
#     die 90er-Schwelle reisst. In 256 und 16 Farben gaebe das Bandenbildung
#     statt Verlauf; dort bleibt es bei der einen Farbe.
#
# Grundregel: eine MOTD darf NIE einen Login blockieren. Deshalb kein set -e,
# kein Kommando ohne Zeitdeckel und jedes externe Werkzeug nur nach have().

LC_ALL=C
export LC_ALL

NC_MOTD_VERSION="2.1"

# ── Vorgaben (jede per /etc/nightcrawler/motd.conf oder Umgebung ueberschreibbar)
SERVICE="${SERVICE:-}"          # leer = automatisch suchen
BOT_DIR="${BOT_DIR:-}"          # leer = automatisch suchen
DASH_PORT="${DASH_PORT:-}"      # leer = aus .env (DASHBOARD_PORT), sonst 8050
DB="${DB:-}"                    # leer = tiktok_bot.db im BOT_DIR, sonst groesste *.db
DISK_TARGET="${DISK_TARGET:-/}"
WIDTH="${WIDTH:-54}"
BARW="${BARW:-22}"
SHOW_REC="${SHOW_REC:-1}"       # Aufnahmen-Block (0 = aus)
REC_CACHE_TTL="${REC_CACHE_TTL:-900}"   # Sekunden; der Scan ist der teuerste Teil
CPU_SAMPLE="${CPU_SAMPLE:-0.20}"        # Messfenster; 0 = ueberspringen
# v4.1-W17: 'always' ist die neue Vorgabe und das, was --install festschreibt.
# Grund: 'auto' waehlt ohne COLORTERM die 256-Farben-Palette — viele
# Handy-SSH-Apps (Termius, JuiceSSH, Blink) melden aber nur TERM=xterm und
# stellen 256er-Codes teils gar nicht oder falsch dar. Der Betreiber sah dann
# eine graue Wand statt der Ampel, fuer die die MOTD gebaut ist.
# 'always' faellt deshalb bis auf die 16 BASISFARBEN durch, die wirklich jedes
# Terminal kann — nie auf farblos. Reihenfolge: truecolor > 256 > 16.
COLOR_MODE="${COLOR_MODE:-always}"      # always | auto | truecolor | 256 | 16 | off
DEST="${DEST:-/etc/update-motd.d/99-nightcrawler}"

OS="$(uname -s 2>/dev/null || echo unknown)"
# macOS hat kein /etc/update-motd.d und der Login laeuft ohne root — die
# Konfiguration liegt dort im Home, sonst systemweit unter /etc.
if [ -z "${CONF:-}" ]; then
  if [ "$OS" = "Darwin" ] && [ ! -r /etc/nightcrawler/motd.conf ]; then
    CONF="$HOME/.nightcrawler-motd.conf"
  else
    CONF="/etc/nightcrawler/motd.conf"
  fi
fi

# shellcheck source=/dev/null
[ -r "$CONF" ] && . "$CONF"

# v4.1-W17: Mehrsprachigkeit. Der Katalog liegt neben dem Werkzeug; ist er nicht
# erreichbar (die installierte Kopie unter /etc/update-motd.d/ hat kein
# locales/ daneben), bleibt alles deutsch statt zu scheitern.
# shellcheck source=lib/i18n.sh
if [ -r "$(dirname "$0")/lib/i18n.sh" ]; then
  . "$(dirname "$0")/lib/i18n.sh"
elif [ -n "${BOT_DIR:-}" ] && [ -r "${BOT_DIR}/tools/lib/i18n.sh" ]; then
  # Die INSTALLIERTE Kopie unter /etc/update-motd.d/ hat kein locales/ neben
  # sich. i18n.sh findet den Katalog trotzdem: es sucht ueber BASH_SOURCE
  # relativ zu SICH SELBST, also unter ${BOT_DIR}/locales/.
  . "${BOT_DIR}/tools/lib/i18n.sh"
else
  t(){ printf '%s' "$*"; }
fi

# ── Farben ───────────────────────────────────────────────────
# Bewusst OHNE TTY-Test: die MOTD laeuft unter run-parts ohne TTY, ein Gate
# haette sie dauerhaft farblos gemacht. Wer es roh braucht: COLOR_MODE=off.
e=$'\033'
_tc=0
_pal=256
case "$COLOR_MODE" in
  off)       e=""; ;;
  16)        _pal=16 ;;
  256)       _tc=0 ;;
  truecolor) _tc=1 ;;
  always)
    # Nie farblos. Die reichste Palette, die die Umgebung wirklich zusagt —
    # und im Zweifel 16, weil das jede Handy-App darstellt.
    case "${COLORTERM:-}" in
      *[Tt]ruecolor*|*24bit*) _tc=1 ;;
      *) case "${TERM:-}" in
           *256color*|*direct*) _pal=256 ;;
           ""|dumb)             _pal=16 ;;
           *)                   _pal=16 ;;
         esac ;;
    esac ;;
  *)         case "${COLORTERM:-}" in *[Tt]ruecolor*|*24bit*) _tc=1 ;; esac ;;
esac
if [ -z "$e" ]; then
  BR=""; DIM=""; TXT=""; FNT=""; OK=""; WRN=""; ERR=""; B=""; R=""
elif [ "$_tc" != 1 ] && [ "$_pal" = 16 ]; then
  # Die 16 Basisfarben. Haesslicher als die Messing-Palette, aber sichtbar —
  # und sichtbar schlaegt schoen, wenn es die Statusanzeige eines Servers ist.
  BR="${e}[1;33m"; DIM="${e}[33m"; TXT="${e}[37m"
  FNT="${e}[90m"; OK="${e}[32m"; WRN="${e}[33m"
  ERR="${e}[31m"
  B="${e}[1m"; R="${e}[0m"
elif [ "$_tc" = 1 ]; then
  BR="${e}[38;2;232;200;106m"; DIM="${e}[38;2;201;162;39m"; TXT="${e}[38;2;239;231;214m"
  FNT="${e}[38;2;138;129;114m"; OK="${e}[38;2;127;168;107m"; WRN="${e}[38;2;224;154;60m"
  ERR="${e}[38;2;212;85;63m"
  B="${e}[1m"; R="${e}[0m"
else
  BR="${e}[38;5;179m"; DIM="${e}[38;5;136m"; TXT="${e}[38;5;187m"
  FNT="${e}[38;5;101m"; OK="${e}[38;5;107m"; WRN="${e}[38;5;173m"
  ERR="${e}[38;5;167m"
  B="${e}[1m"; R="${e}[0m"
fi

have(){ command -v "$1" >/dev/null 2>&1; }

# Zeitdeckel um alles, was haengen kann. Ohne timeout(1) (macOS ohne coreutils)
# wird das Kommando roh ausgefuehrt — dort sind die Kandidaten lokal und schnell.
tmo(){ local s="$1"; shift; if have timeout; then timeout "$s" "$@"; else "$@"; fi; }

# ── Installation erkennen ────────────────────────────────────
detect_service(){
  [ -n "$SERVICE" ] && { printf '%s' "$SERVICE"; return; }
  have systemctl || return
  local u
  for u in tiktok-bot nightcrawler nightcrawler-bot tiktok_bot; do
    if systemctl list-unit-files --no-legend "${u}.service" 2>/dev/null | grep -q .; then
      printf '%s' "$u"; return
    fi
  done
  # Letzter Versuch: irgendeine Unit, die nach dem Bot aussieht.
  systemctl list-unit-files --no-legend --type=service 2>/dev/null \
    | awk '{print $1}' | grep -iE '^(tiktok|nightcrawler)' | head -1 | sed 's/\.service$//'
}

is_botdir(){ [ -f "$1/bot.py" ] || [ -f "$1/bot_v37.py" ]; }

# v4.2-W7: Welche Schnittstelle traegt den Upstream? Als FUNKTION und nicht
# inline in der Messung, weil --doctor sie ebenfalls zeigen muss — und
# --doctor laeuft VOR der Messung. Eine zweite Kopie waere die zweite
# Wahrheit, die genau dann auseinanderlaeuft, wenn man sie braucht.
detect_netif(){
  [ -n "${NET_IF:-}" ] && { printf '%s' "$NET_IF"; return; }
  [ -r /proc/net/dev ] || return
  local i=""
  have ip && i=$(tmo 2 ip route show default 2>/dev/null | awk '{print $5; exit}')
  # Ohne Standardroute (Container, reines LAN): die erste Schnittstelle, die
  # nicht loopback ist und schon Daten gesehen hat.
  [ -z "$i" ] && i=$(awk -F'[: ]+' 'NR>2 && $2!="lo" && $3+0>0 {print $2; exit}' /proc/net/dev 2>/dev/null)
  printf '%s' "$i"
}

detect_botdir(){
  [ -n "$BOT_DIR" ] && is_botdir "$BOT_DIR" && { printf '%s' "$BOT_DIR"; return; }
  local d
  # 1. Der Dienst weiss es am besten.
  if [ -n "$SERVICE" ] && have systemctl; then
    d=$(systemctl show -p WorkingDirectory --value "$SERVICE" 2>/dev/null)
    [ -n "$d" ] && is_botdir "$d" && { printf '%s' "$d"; return; }
  fi
  # 2. Uebliche Orte, inklusive aller Home-Verzeichnisse (MOTD laeuft als root).
  for d in "$HOME/nightcrawler" "$HOME/tiktok-bot" /opt/nightcrawler /opt/tiktok-bot \
           /srv/nightcrawler /home/*/nightcrawler /home/*/tiktok-bot \
           /Users/*/nightcrawler /Users/*/tiktok-bot; do
    is_botdir "$d" && { printf '%s' "$d"; return; }
  done
}

envget(){ # $1=Schluessel — erster unkommentierter Treffer aus der .env
  [ -f "$ENVF" ] || return
  awk -F= -v k="$1" '
    /^[[:space:]]*#/ {next}
    {key=$1; gsub(/[[:space:]]/,"",key)}
    key==k {v=$2; for(i=3;i<=NF;i++) v=v"="$i
            sub(/[[:space:]]*#.*$/,"",v); gsub(/^[[:space:]"'"'"']+|[[:space:]"'"'"']+$/,"",v)
            print v; exit}' "$ENVF" 2>/dev/null
}

SERVICE="$(detect_service)"
BOT_DIR="$(detect_botdir)"
ENVF="${ENVF:-$BOT_DIR/.env}"
LOGF="${LOGF:-$BOT_DIR/logs/error.log}"
RECDIR="${RECDIR:-$BOT_DIR/recordings}"
if [ -z "$DASH_PORT" ]; then DASH_PORT="$(envget DASHBOARD_PORT)"; fi
[ -z "$DASH_PORT" ] && DASH_PORT=8050
DB_BACKEND="$(envget DB_BACKEND)"
if [ -z "$DB" ]; then
  if [ -f "$BOT_DIR/tiktok_bot.db" ]; then DB="$BOT_DIR/tiktok_bot.db"
  else
    # brain.db ist die KI-Ablage, nicht die Bot-Datenbank — sie waere auf
    # manchen Boxen die groessere und wuerde die Zahlen unten leer lassen.
    _big=0
    for _f in "$BOT_DIR"/*.db; do
      [ -f "$_f" ] || continue
      case "$_f" in */brain.db) continue;; esac
      _sz=$(wc -c < "$_f" 2>/dev/null || echo 0)
      [ "$_sz" -gt "$_big" ] 2>/dev/null && { _big=$_sz; DB=$_f; }
    done
  fi
fi

# ── Install / Uninstall ──────────────────────────────────────
NC_STATE="/etc/update-motd.d/.nc-silenced"
NC_MOTD_SAVED="/etc/nightcrawler/motd-static.bak"
# v4.1-W17: Die feste Liste war der Fehler. Sie kannte Ubuntus Standardstuecke —
# aber nicht das, was Hoster, Images und Distributionen sonst noch einhaengen
# (00-hoster-banner, 10-uname, 98-reboot-required, neofetch-Schnipsel, das
# figlet-Logo des Anbieters). Nach --install standen die alle WEITER da, und
# die NIGHTCRAWLER-MOTD hing unten an einer fremden Wand aus Text.
# Jetzt wird ALLES ausser dem eigenen Stueck gedaempft — und jede gedaempfte
# Datei namentlich vermerkt, damit --uninstall exakt sie zurueckholt und nichts
# anderes. Die Liste bleibt nur noch als Erklaerung stehen, wofuer sie stand.
RC_MARK_A="# >>> NIGHTCRAWLER MOTD >>>"
RC_MARK_E="# <<< NIGHTCRAWLER MOTD <<<"

silence_defaults(){
  local s="" f b
  # ALLES ausser dem eigenen Stueck. Der Name des eigenen kommt aus DEST,
  # nicht fest verdrahtet — wer DEST umsetzt, daempft sich sonst selbst.
  local eigen; eigen="$(basename "$DEST")"
  for f in /etc/update-motd.d/*; do
    [ -e "$f" ] || continue                  # leeres Verzeichnis: das Glob bleibt stehen
    b="$(basename "$f")"
    [ "$b" = "$eigen" ] && continue
    case "$b" in .*) continue ;; esac        # .nc-silenced und Konsorten
    [ -x "$f" ] || continue                  # schon still
    chmod -x "$f" 2>/dev/null && s="$s $b"
  done
  if [ -n "$s" ]; then
    printf '%s\n' $s > "$NC_STATE"
    printf "  ${FNT}Standard-MOTD gedaempft:${R}%s\n" "$s"
  else
    printf "  ${FNT}Standard-MOTD war bereits still${R}\n"
  fi
  # Die STATISCHE /etc/motd laeuft nicht ueber run-parts und blieb deshalb
  # sichtbar, egal was hier gedaempft wurde. Auf Debian/Ubuntu steht dort das
  # Willkommens-Geschwafel des Images. Beiseitelegen statt loeschen — sie kommt
  # bei --uninstall zurueck.
  if [ -s /etc/motd ]; then
    mkdir -p "$(dirname "$NC_MOTD_SAVED")" 2>/dev/null
    if mv /etc/motd "$NC_MOTD_SAVED" 2>/dev/null; then
      : > /etc/motd 2>/dev/null || true
      printf "  ${FNT}statische /etc/motd beiseitegelegt${R} → %s\n" "$NC_MOTD_SAVED"
    fi
  fi
}
restore_defaults(){
  local f wieder=0
  if [ -f "$NC_STATE" ]; then
    while read -r f; do
      [ -n "$f" ] || continue
      [ -e "/etc/update-motd.d/$f" ] && chmod +x "/etc/update-motd.d/$f" && wieder=1
    done < "$NC_STATE"
    rm -f "$NC_STATE"
  fi
  # Die beiseitegelegte statische MOTD zurueck — aber nur, wenn seither nichts
  # Neues an ihre Stelle geschrieben wurde. Fremdes Zeug zu ueberbuegeln waere
  # schlimmer als eine Datei zu viel.
  if [ -f "$NC_MOTD_SAVED" ]; then
    if [ ! -s /etc/motd ]; then
      mv "$NC_MOTD_SAVED" /etc/motd 2>/dev/null && wieder=1
    else
      printf "  ${WRN}/etc/motd wurde seither neu beschrieben${R} ${FNT}— Sicherung bleibt unter %s${R}\n" "$NC_MOTD_SAVED"
    fi
  fi
  [ "$wieder" = 1 ] && printf "  ${FNT}Standard-MOTD wiederhergestellt${R}\n"
  return 0
}

write_conf(){
  # Die erkannten Pfade festschreiben. Ohne das raet die installierte Kopie bei
  # jedem Login neu — und raet als root anders als du beim Testen.
  mkdir -p "$(dirname "$CONF")" 2>/dev/null || return 1
  {
    printf '# NIGHTCRAWLER MOTD — erzeugt von motd.sh --install am %s\n' "$(date '+%F %T')"
    printf '# Von Hand aenderbar; --install ueberschreibt die Datei.\n'
    printf 'SERVICE=%s\n'     "$(qq "$SERVICE")"
    printf 'BOT_DIR=%s\n'     "$(qq "$BOT_DIR")"
    printf 'DASH_PORT=%s\n'   "$(qq "$DASH_PORT")"
    printf 'DB=%s\n'          "$(qq "$DB")"
    printf 'DISK_TARGET=%s\n' "$(qq "$DISK_TARGET")"
    printf 'SHOW_REC=%s\n'    "$(qq "$SHOW_REC")"
    printf 'CPU_SAMPLE=%s\n'  "$(qq "$CPU_SAMPLE")"
    printf 'COLOR_MODE=%s\n'  "$(qq "$COLOR_MODE")"
  } > "$CONF"
  chmod 644 "$CONF" 2>/dev/null
  printf "${OK}✔ Konfiguration${R} → %s\n" "$CONF"
}
qq(){ printf "'%s'" "$(printf '%s' "${1:-}" | sed "s/'/'\\\\''/g")"; }

need_root(){ [ "$(id -u)" -eq 0 ] || { printf "${WRN}Bitte mit sudo:${R} sudo %s %s\n" "$0" "$1"; exit 1; }; }

install_linux(){
  local src; src="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  [ -d /etc/update-motd.d ] || mkdir -p /etc/update-motd.d
  cp "$src" "$DEST" && chmod +x "$DEST" || { printf "${ERR}✘ Installation fehlgeschlagen${R}\n"; exit 1; }
  printf "${OK}✔ installiert${R} → %s\n" "$DEST"
  write_conf
  silence_defaults
  printf "  ${FNT}Vorschau:  sudo run-parts /etc/update-motd.d/${R}\n"
  printf "  ${FNT}'Last login' kommt von SSH — optional 'PrintLastLog no' in sshd_config${R}\n"
  if ! grep -rqs 'pam_motd' /etc/pam.d/sshd 2>/dev/null; then
    printf "  ${WRN}Hinweis:${R} ${FNT}/etc/pam.d/sshd laedt pam_motd nicht — dann bleibt der Login still.${R}\n"
  fi
}

install_darwin(){
  # macOS kennt weder /etc/update-motd.d noch pam_motd. Sauberster Weg ist ein
  # markierter Block in der Shell-rc des Nutzers — idempotent und rueckbaubar.
  local src rc; src="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  rc="${SHELLRC:-$HOME/.zshrc}"; [ -n "${BASH_VERSION:-}" ] && [ ! -f "$rc" ] && rc="$HOME/.bash_profile"
  if grep -qs "$RC_MARK_A" "$rc"; then
    printf "${FNT}bereits eingetragen in %s${R}\n" "$rc"
  else
    { printf '\n%s\n' "$RC_MARK_A"
      printf '[ -t 1 ] && [ -z "$NC_MOTD_SHOWN" ] && export NC_MOTD_SHOWN=1 && "%s"\n' "$src"
      printf '%s\n' "$RC_MARK_E"; } >> "$rc"
    printf "${OK}✔ eingetragen${R} → %s\n" "$rc"
  fi
  write_conf
  printf "  ${FNT}Wirksam nach:  exec \$SHELL -l${R}\n"
}

uninstall_darwin(){
  local rc; rc="${SHELLRC:-$HOME/.zshrc}"
  for rc in "$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc"; do
    [ -f "$rc" ] && grep -qs "$RC_MARK_A" "$rc" || continue
    sed -i.nc-bak "/$(printf '%s' "$RC_MARK_A" | sed 's/[][\.*^$\/]/\\&/g')/,/$(printf '%s' "$RC_MARK_E" | sed 's/[][\.*^$\/]/\\&/g')/d" "$rc"
    printf "${OK}✔ entfernt aus${R} %s ${FNT}(Sicherung: %s.nc-bak)${R}\n" "$rc" "$rc"
  done
}

doctor(){
  printf "\n${BR}${B}NIGHTCRAWLER MOTD — Erkennung${R}  ${FNT}v%s${R}\n\n" "$NC_MOTD_VERSION"
  printf "  %-12s %s\n" "System"    "$OS $(uname -r 2>/dev/null)"
  printf "  %-12s %s\n" "Konfig"    "$([ -r "$CONF" ] && echo "$CONF" || echo "— (keine, alles erkannt)")"
  printf "  %-12s %s\n" "Dienst"    "${SERVICE:-— nicht gefunden}"
  printf "  %-12s %s\n" "BOT_DIR"   "${BOT_DIR:-— nicht gefunden}"
  printf "  %-12s %s\n" ".env"      "$([ -f "$ENVF" ] && echo "$ENVF" || echo "— fehlt")"
  printf "  %-12s %s\n" "Datenbank" "${DB:-— keine gefunden}${DB_BACKEND:+  (DB_BACKEND=$DB_BACKEND)}"
  printf "  %-12s %s\n" "Log"       "$([ -f "$LOGF" ] && echo "$LOGF" || echo "— fehlt")"
  printf "  %-12s %s\n" "Aufnahmen" "$([ -d "$RECDIR" ] && echo "$RECDIR" || echo "— fehlt")"
  printf "  %-12s %s\n" "Dashboard" ":$DASH_PORT"
  _ni="$(detect_netif)"
  printf "  %-12s %s\n" "Netz"      "${_ni:-— keine Schnittstelle erkannt}"
  printf "  %-12s %s\n" "Werkzeuge" "$(for t in systemctl ss curl sqlite3 python3 free df find du; do have $t && printf '%s ' "$t"; done)"
  printf "\n  ${FNT}Falsch erkannt? Werte in %s eintragen (oder als Umgebung setzen).${R}\n\n" "$CONF"
  exit 0
}

case "${1:-}" in
  --install)
    need_root --install
    if [ "$OS" = "Darwin" ]; then install_darwin; else install_linux; fi
    exit 0;;
  --uninstall)
    if [ "$OS" = "Darwin" ]; then uninstall_darwin; exit 0; fi
    need_root --uninstall
    if [ -f "$DEST" ]; then rm -f "$DEST" && printf "${OK}✔ entfernt${R} → %s\n" "$DEST"
    else printf "${FNT}nicht installiert${R}\n"; fi
    restore_defaults
    printf "  ${FNT}%s bleibt liegen (harmlos, enthaelt nur Pfade)${R}\n" "$CONF"
    exit 0;;
  --doctor)  doctor;;
  --version) printf 'NIGHTCRAWLER MOTD %s\n' "$NC_MOTD_VERSION"; exit 0;;
  --help|-h)
    printf "NIGHTCRAWLER MOTD %s\n\n" "$NC_MOTD_VERSION"
    printf "  (ohne Argument)  Vorschau — aendert nichts\n"
    printf "  --install        einhaengen + Standard-MOTD daempfen (sudo; macOS: Shell-rc)\n"
    printf "  --uninstall      entfernen + Standard-MOTD wiederherstellen\n"
    printf "  --doctor         zeigt, was erkannt wurde und woher\n"
    printf "  --version        Fassung\n\n"
    printf "Anpassen ueber %s oder Umgebung:\n" "$CONF"
    printf "  SERVICE BOT_DIR DASH_PORT DB DISK_TARGET SHOW_REC CPU_SAMPLE COLOR_MODE\n"
    printf "  COLOR_MODE: always (Vorgabe) | auto | truecolor | 256 | 16 | off\n"
    printf "Beispiel:  BOT_DIR=~/mein-bot COLOR_MODE=16 ./motd.sh\n"
    exit 0;;
  "") ;;
  *) printf "${WRN}Unbekannte Option: %s${R}  (--help)\n" "$1"; exit 1;;
esac

# ── Zeichen-Helfer ───────────────────────────────────────────
col4(){ local p=${1:-0}; if [ "$p" -ge 90 ]; then printf '%s' "$ERR"
        elif [ "$p" -ge 70 ]; then printf '%s' "$WRN"; else printf '%s' "$OK"; fi; }
rule(){ printf "${DIM}"; awk -v n="$WIDTH" 'BEGIN{while(n-->0)printf "━"}'; printf "${R}\n"; }
sect(){ printf "  ${DIM}${B}%s${R}\n" "$1"; }
bar(){  # bar <prozent> [breite]  — Breite als ARGUMENT: eine Zuweisung vor dem
        # Funktionsaufruf (BARW=10 bar 50) bleibt in bash danach stehen und
        # verstellte in der Vorfassung alle folgenden Balken.
  local p=${1:-0} w=${2:-$BARW} i fill col out=""
  [ "$p" -lt 0 ] 2>/dev/null && p=0; [ "$p" -gt 100 ] 2>/dev/null && p=100
  fill=$(( (p*w+50)/100 ))
  # v4.2-W7: Verlauf statt einer Farbe — aber NUR in Truecolor. Jede Zelle
  # traegt die Farbe IHRER Position, der Balken liest sich damit wie ein
  # Thermometer: eine RAM-Anzeige bei 85 % ist sichtbar heiss, bevor sie die
  # 90er-Schwelle reisst. In der 256er- und erst recht in der 16er-Palette
  # gaebe das Bandenbildung statt Verlauf; dort bleibt die eine Farbe.
  #
  # In EINEM awk gebaut und nicht in einer Shell-Schleife: 22 Zellen waeren
  # 22 Rechenschritte je Balken und fuenf Balken je Login.
  if [ "$_tc" = 1 ] && [ -n "$e" ]; then
    awk -v fill="$fill" -v w="$w" -v esc="$e" 'BEGIN{
      for (i = 0; i < w; i++) {
        if (i >= fill) { printf "%s[38;2;138;129;114m▒", esc; continue }
        q = (w > 1) ? (i * 100.0 / (w - 1)) : 0
        # Gruen 127,168,107 → Bernstein 224,154,60 bei 70 % → Rot 212,85,63
        if (q < 70) { r=127+(224-127)*q/70;      g=168+(154-168)*q/70;      b=107+(60-107)*q/70 }
        else        { r=224+(212-224)*(q-70)/30; g=154+(85-154)*(q-70)/30;  b=60+(63-60)*(q-70)/30 }
        printf "%s[38;2;%d;%d;%dm█", esc, r+0.5, g+0.5, b+0.5
      }
      printf "%s[0m", esc }'
    return
  fi
  col=$(col4 "$p"); out="${col}"
  i=0; while [ "$i" -lt "$w" ]; do
    if [ "$i" -lt "$fill" ]; then out="${out}█"; else out="${out}${FNT}▒${col}"; fi
    i=$((i+1))
  done
  printf "%b" "${out}${R}"
}
# v4.2-W7: Miniverlauf. Sieben Zahlen als sieben Blockzeichen — die Frage bei
# einer Fehlerzahl ist nie "wie viele", sondern "mehr als sonst?". Eine 4 sagt
# nichts; eine 4 hinter sechs Nullen sagt alles.
# Skaliert auf das Maximum der Reihe, nicht auf einen festen Deckel: sonst
# waere der Verlauf bei kleinen Zahlen platt und bei grossen abgeschnitten.
spark(){
  awk -v vals="$*" 'BEGIN{
    n = split(vals, v, " "); if (!n) exit
    max = 0; for (i = 1; i <= n; i++) if (v[i] + 0 > max) max = v[i] + 0
    n8 = split("▁ ▂ ▃ ▄ ▅ ▆ ▇ █", g, " ")
    for (i = 1; i <= n; i++) {
      if (max <= 0) { printf "%s", g[1]; continue }
      k = int(v[i] * (n8 - 1) / max + 0.5) + 1; if (k > n8) k = n8
      printf "%s", g[k]
    } }'
}
gauge(){ printf "  ${DIM}%-6s${R} %b ${FNT}%s${R}\n" "$1" "$(bar "$2")" "$3"; }
dot(){ case "$1" in ok) printf "${OK}●${R}";; warn) printf "${WRN}●${R}";;
                    err) printf "${ERR}●${R}";; *) printf "${FNT}●${R}";; esac; }
row(){ printf "  ${DIM}%-11s${R}%b %b\n" "$1" "$2" "$3"; }
human(){ awk -v b="${1:-0}" 'BEGIN{s="B K M G T P";n=split(s,u," ");x=b+0;i=1;
         while(x>=1024&&i<n){x/=1024;i++} printf (x<10?"%.1f%s":"%.0f%s"),x,u[i]}'; }
ago(){ local d=$(( $(date +%s) - ${1%.*} ))
  [ "$d" -lt 0 ] && d=0
  if   [ "$d" -lt 60 ];    then echo "${d}s"
  elif [ "$d" -lt 3600 ];  then echo "$((d/60))m"
  elif [ "$d" -lt 86400 ]; then echo "$((d/3600))h"
  else echo "$((d/86400))d"; fi; }
onoff(){ [ "${1:-0}" -gt 0 ] 2>/dev/null && echo ok || echo faint; }
pct(){ [ "${2:-0}" -gt 0 ] 2>/dev/null && echo $(( $1*100/$2 )) || echo 0; }

WARN_LINES=""
warn_add(){ WARN_LINES="${WARN_LINES}${1}"$'\n'; }

# ── Messwerte einsammeln ─────────────────────────────────────
# v4.2-W7: Netzdurchsatz im SELBEN Messfenster wie die CPU.
#
# Fuer eine Restream-Box ist der Upstream die aussagekraeftigste Zahl
# ueberhaupt: "Bot laeuft" und "es geht wirklich etwas raus" sind zwei
# verschiedene Fragen, und die zweite beantwortete die MOTD bisher nicht.
# Ein Durchsatz braucht aber zwei Messungen mit Abstand — ein eigener sleep
# waere der teuerste Posten der ganzen Anzeige geworden. Er haengt sich
# deshalb an das Fenster, das fuer die CPU ohnehin schon gewartet wird.
[ "$OS" = "Linux" ] && NET_IF="$(detect_netif)"
_netsnap(){ awk -v i="$NET_IF" '{sub(/:/, " ")} $1==i {print $2, $10; exit}' /proc/net/dev 2>/dev/null; }

CPU_LINES=""; NET_RX=""; NET_TX=""
if [ "$OS" = "Linux" ] && [ "$CPU_SAMPLE" != "0" ]; then
  _snap(){ awk '/^cpu[0-9]*[ \t]/{idle=$5+$6; tot=0; for(i=2;i<=NF;i++) tot+=$i; print $1, idle, tot}' /proc/stat; }
  _s1=""; [ -r /proc/stat ] && _s1=$(_snap)
  _n1=""; [ -n "$NET_IF" ] && _n1=$(_netsnap)
  sleep "$CPU_SAMPLE"
  if [ -n "$_s1" ]; then
    _s2=$(_snap)
    CPU_LINES=$(printf '%s\n%s\n' "$_s1" "$_s2" | awk '
      { if (seen[$1]++) { di=$2-i[$1]; dt=$3-t[$1]; p=(dt>0)?int(100*(dt-di)/dt+0.5):0; print $1, p }
        else { i[$1]=$2; t[$1]=$3 } }')
  fi
  if [ -n "$_n1" ]; then
    _n2=$(_netsnap)
    # Zaehleruberlauf und Schnittstellen-Neustart geben negative Differenzen —
    # dann lieber gar nichts zeigen als eine erfundene Zahl.
    eval "$(awk -v a="$_n1" -v b="$_n2" -v w="$CPU_SAMPLE" 'BEGIN{
      split(a,x," "); split(b,y," "); if (w+0 <= 0) exit
      dr=(y[1]-x[1])/w; dt=(y[2]-x[2])/w
      if (dr>=0 && dt>=0) printf "NET_RX=%d NET_TX=%d", dr, dt }')"
  fi
fi
CPU_ALL=$(printf '%s\n' "$CPU_LINES" | awk '$1=="cpu"{print $2; exit}')
if [ -z "$CPU_ALL" ] && [ "$OS" = "Darwin" ]; then
  # macOS hat kein /proc: Summe der Prozesslast durch Kernzahl. Grob, aber
  # sofort da — top -l 1 kostet eine ganze Sekunde pro Login.
  CPU_ALL=$(ps -A -o %cpu= 2>/dev/null | awk -v n="$(sysctl -n hw.ncpu 2>/dev/null || echo 1)" \
            '{s+=$1} END{p=int(s/n+0.5); print (p>100?100:p)}')
fi
[ -z "$CPU_ALL" ] && CPU_ALL=0

if [ "$OS" = "Darwin" ]; then
  NPC=$(sysctl -n hw.ncpu 2>/dev/null || echo 1)
else
  NPC=$(nproc 2>/dev/null || grep -c '^processor' /proc/cpuinfo 2>/dev/null || echo 1)
fi

# Speicher — auf Linux direkt aus /proc/meminfo (kein free(1) noetig, kein
# Rateraten an dessen Spaltenlayout, das sich zwischen Versionen verschoben hat)
MEM_U=0; MEM_T=0; SWP_U=0; SWP_T=0
if [ -r /proc/meminfo ]; then
  eval "$(awk '/^MemTotal:/{t=$2} /^MemAvailable:/{a=$2} /^SwapTotal:/{st=$2} /^SwapFree:/{sf=$2}
               END{printf "MEM_T=%d MEM_U=%d SWP_T=%d SWP_U=%d", t/1024, (t-a)/1024, st/1024, (st-sf)/1024}' /proc/meminfo)"
elif [ "$OS" = "Darwin" ] && have vm_stat; then
  MEM_T=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1048576 ))
  MEM_U=$(vm_stat 2>/dev/null | awk -v tot="$MEM_T" '
    /page size of/{ps=$8} /Pages free/{f=$3} /Pages speculative/{s=$3}
    END{gsub(/\./,"",f); gsub(/\./,"",s); if(ps=="")ps=4096; printf "%d", tot-((f+s)*ps)/1048576}')
fi

# Platte — POSIX-df (-Pk laeuft auch auf macOS; --output ist GNU-only)
DISK_U=0; DISK_T=0; DISK_A=0
eval "$(tmo 3 df -Pk "$DISK_TARGET" 2>/dev/null | awk 'NR==2{printf "DISK_U=%d DISK_T=%d DISK_A=%d", $3, $2, $4}')"
DPCT=0; [ "$DISK_T" -gt 0 ] 2>/dev/null && DPCT=$(( DISK_U * 100 / DISK_T ))

# Temperatur — Raspberry Pi und alles mit thermal_zone
TEMP=""
if have vcgencmd; then
  TEMP=$(tmo 2 vcgencmd measure_temp 2>/dev/null | tr -dc '0-9.' | cut -d. -f1)
elif [ -r /sys/class/thermal/thermal_zone0/temp ]; then
  TEMP=$(( $(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null || echo 0) / 1000 ))
  [ "$TEMP" = "0" ] && TEMP=""
fi
# Unterspannung/Drosselung: der haeufigste Grund fuer "der Pi nimmt nicht auf"
THROTTLE=""
if have vcgencmd; then
  _tv=$(tmo 2 vcgencmd get_throttled 2>/dev/null | cut -d= -f2)
  case "$_tv" in 0x0|"") ;; *) THROTTLE="$_tv" ;; esac
fi

# ── Lage: Dienst und Dashboard (v4.2-W7) ─────────────────────
# Beide Proben liefen bisher MITTEN in der Ausgabe. Sie stehen jetzt davor,
# weil die Gesamtampel im Kopf ihr Ergebnis braucht — und eine Statusanzeige,
# die ihr Urteil erst am Ende faellt, hilft niemandem, der nach dem Login nur
# einmal kurz hinsieht. Es sind dieselben zwei Aufrufe mit denselben
# Zeitdeckeln, nur frueher; die Anzeige kostet keine Millisekunde mehr.
BOT_STATE=unbekannt; BOT_SINCE=""; BOT_NRS=""; BOT_RES=""
if [ -n "$SERVICE" ] && have systemctl; then
  if systemctl is-active --quiet "$SERVICE" 2>/dev/null; then
    BOT_STATE=laeuft
    BOT_SINCE=$(systemctl show -p ActiveEnterTimestamp --value "$SERVICE" 2>/dev/null | cut -d' ' -f2-3)
    BOT_NRS=$(systemctl show -p NRestarts --value "$SERVICE" 2>/dev/null)
  else
    BOT_STATE=gestoppt
    BOT_RES=$(systemctl show -p Result --value "$SERVICE" 2>/dev/null)
  fi
elif [ -n "$BOT_DIR" ]; then
  # Ohne systemd (macOS, Container, Handstart): am Prozess erkennen.
  # Muster bewusst eng: ein blosses "bot.py" trifft auch einen Editor, ein
  # grep oder ein Deploy-Skript in der Prozessliste — und meldet dann froehlich
  # "laeuft", waehrend der Bot tot ist.
  if tmo 2 pgrep -f "python[0-9.]*[^|]*bot(_v37)?\.py" >/dev/null 2>&1; then
    BOT_STATE=prozess
  else
    BOT_STATE=tot
  fi
fi

# Dashboard: nicht "lauscht der Port", sondern "antwortet die App". Ein
# haengender Flask-Thread haelt den Port offen — die alte Anzeige blieb gruen.
DASH_STATE=aus; DASH_PROCS=""; DASH_ZOMB=""; DASH_JSON=""
if have curl; then
  DASH_JSON=$(tmo 2 curl -s --max-time 1.5 "http://127.0.0.1:${DASH_PORT}/healthz" 2>/dev/null)
fi
if [ -n "$DASH_JSON" ]; then
  _ok=$(printf '%s' "$DASH_JSON" | sed -n 's/.*"ok"[: ]*\([a-z]*\).*/\1/p')
  DASH_PROCS=$(printf '%s' "$DASH_JSON" | sed -n 's/.*"procs"[: ]*\([0-9]*\).*/\1/p')
  DASH_ZOMB=$(printf '%s' "$DASH_JSON" | sed -n 's/.*"zombies"[: ]*\([0-9]*\).*/\1/p')
  if [ "$_ok" = "true" ]; then DASH_STATE=gesund; else DASH_STATE=degradiert; fi
elif have ss && tmo 2 ss -ltn 2>/dev/null | grep -q ":${DASH_PORT} "; then
  DASH_STATE=stumm
elif have lsof && tmo 2 lsof -nP -iTCP:"${DASH_PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  DASH_STATE=stumm
fi

# ── Gesamtampel ──────────────────────────────────────────────
# Ein Urteil in einer Zeile. Die MOTD hat acht Bloecke; wer per Handy-SSH
# einloggt, sieht davon drei, ohne zu scrollen. Genau deshalb steht der
# schlimmste Befund oben und nicht nur unten in den Hinweisen.
#
# Rot schlaegt Gelb, und innerhalb einer Stufe gewinnt der ERSTE Befund:
# "Bot laeuft nicht" ist die Ursache, "Dashboard nicht erreichbar" meist nur
# die Folge — sie darf die Ursache nicht ueberschreiben.
LAGE=ok; LAGE_TEXT="alles im Griff"
lage_setz(){
  case "$1" in
    err)  [ "$LAGE" = err ] || { LAGE=err; LAGE_TEXT="$2"; } ;;
    warn) [ "$LAGE" = ok ] && { LAGE=warn; LAGE_TEXT="$2"; } ;;
  esac
}
if [ -z "$BOT_DIR" ] && [ -z "$SERVICE" ]; then
  lage_setz warn "Installation nicht gefunden"
else
  case "$BOT_STATE" in gestoppt|tot) lage_setz err "Bot laeuft nicht";; esac
  case "$DASH_STATE" in
    aus)               lage_setz err  "Dashboard nicht erreichbar";;
    degradiert|stumm)  lage_setz warn "Dashboard antwortet nicht sauber";;
  esac
fi
[ "$DPCT" -ge 90 ] 2>/dev/null && lage_setz err "Platte fast voll (${DPCT}%)"
[ -n "$THROTTLE" ] && lage_setz warn "Drosselung gemeldet"

# ── Kopf ─────────────────────────────────────────────────────
# BUILD_STAMP steht seit v4.0 als Klartext in bot.py ("2026.08 · v4.0"); die
# alte Fassung suchte ein "B<nummer>" in bot_v37.py und fand nach W119 nichts
# mehr — der Kopf war seitdem versionslos.
VER="$(envget BUILD_STAMP)"
if [ -z "$VER" ]; then
  for f in "$BOT_DIR/bot.py" "$BOT_DIR/bot_v37.py"; do
    [ -f "$f" ] || continue
    VER=$(sed -n 's/^BUILD_STAMP *= *os\.getenv("BUILD_STAMP", *"\([^"]*\)").*/\1/p' "$f" | head -1)
    [ -n "$VER" ] && break
  done
fi
GITREF=""
if [ -n "$BOT_DIR" ] && [ -d "$BOT_DIR/.git" ] && have git; then
  GITREF=$(tmo 2 git -C "$BOT_DIR" rev-parse --short HEAD 2>/dev/null)
fi
if have uptime; then UP=$(uptime -p 2>/dev/null | sed 's/^up //'); fi
[ -z "${UP:-}" ] && [ -r /proc/uptime ] && UP="$(awk '{d=int($1/86400); h=int(($1%86400)/3600); m=int(($1%3600)/60);
  printf (d? "%dd %dh" : (h? "%dh %dm" : "%dm")), (d?d:(h?h:m)), (d?h:m)}' /proc/uptime)"
[ -z "${UP:-}" ] && UP="—"

printf "\n"; rule
printf "  ${BR}${B}◤ NIGHTCRAWLER${R}${VER:+ ${DIM}${VER}${R}}${GITREF:+ ${FNT}·${R} ${FNT}${GITREF}${R}}   ${TXT}%s${R}\n" "$(hostname 2>/dev/null)"
case "$LAGE" in
  ok)   LAGE_BADGE="${OK}●${R} ${OK}${LAGE_TEXT}${R}";;
  warn) LAGE_BADGE="${WRN}▲${R} ${WRN}${LAGE_TEXT}${R}";;
  *)    LAGE_BADGE="${ERR}✘${R} ${B}${ERR}${LAGE_TEXT}${R}";;
esac
printf "  %b   ${FNT}Restream Control Room${R}   ${FNT}up %s${R}\n" "$LAGE_BADGE" "$UP"
rule

# ── System ───────────────────────────────────────────────────
sect "SYSTEM"
gauge "CPU" "$CPU_ALL" "${CPU_ALL}% · ${NPC} Kerne"
if [ -n "$CPU_LINES" ]; then
  # Ein Zeichen je Kern: sieht sofort, ob EIN ffmpeg einen Kern festhaelt oder
  # ob wirklich alle unter Last stehen.
  EQ="  ${FNT}Kerne  ${R}"
  while read -r _n _p; do
    case "$_n" in cpu[0-9]*) ;; *) continue;; esac
    _l=$(( (_p*8+50)/100 )); [ "$_l" -gt 8 ] && _l=8
    case "$_l" in 0|1) _c="▁";; 2) _c="▂";; 3) _c="▃";; 4) _c="▄";;
                  5) _c="▅";; 6) _c="▆";; 7) _c="▇";; *) _c="█";; esac
    EQ="${EQ}$(col4 "$_p")${_c}${R}"
  done <<EOF
$CPU_LINES
EOF
  printf "%b\n" "$EQ"
fi
if [ -r /proc/loadavg ]; then read -r l1 l5 l15 _ < /proc/loadavg
elif have uptime; then eval "$(uptime | sed 's/.*averages*: *//; s/,//g' | awk '{print "l1="$1" l5="$2" l15="$3}')"; fi
LOADLINE="  ${DIM}Load  ${R} ${TXT}${l1:-?}${R} ${FNT}·${R} ${TXT}${l5:-?}${R} ${FNT}·${R} ${TXT}${l15:-?}${R}"
[ -n "$TEMP" ] && LOADLINE="${LOADLINE}   ${DIM}Temp${R} $( [ "$TEMP" -ge 75 ] && printf '%s' "$WRN" || printf '%s' "$TXT" )${TEMP}°C${R}"
printf "%b\n" "$LOADLINE"
[ "$MEM_T" -gt 0 ] && gauge "RAM"  "$(pct "$MEM_U" "$MEM_T")" \
  "$(awk -v u="$MEM_U" -v t="$MEM_T" 'BEGIN{printf "%.1f/%.1fG",u/1024,t/1024}')  $(pct "$MEM_U" "$MEM_T")%"
[ "$SWP_T" -gt 0 ] && gauge "Swap" "$(pct "$SWP_U" "$SWP_T")" \
  "$(awk -v u="$SWP_U" -v t="$SWP_T" 'BEGIN{printf "%.1f/%.1fG",u/1024,t/1024}')  $(pct "$SWP_U" "$SWP_T")%"
if [ "$DISK_T" -gt 0 ]; then
  gauge "Disk" "$DPCT" "$(human $((DISK_U*1024)))/$(human $((DISK_T*1024)))  ${DPCT}% · $(human $((DISK_A*1024))) frei"
  [ "$DPCT" -ge 90 ] && warn_add "Platte zu ${DPCT}% voll — Aufnahmen brechen ab: ${TXT}/cleanup${R}${FNT} oder alte Dateien loeschen${R}"
fi
# v4.2-W7: Der Upstream ist bei einer Restream-Box die Zahl, die "laeuft" von
# "sendet wirklich" trennt. Rauf zuerst und hervorgehoben — runter ist bei
# diesem Geraet die Nebensache.
if [ -n "$NET_TX" ]; then
  printf "  ${DIM}%-6s${R} ${TXT}↑ %s/s${R}   ${FNT}↓ %s/s${R}   ${FNT}%s${R}\n" \
    "Netz" "$(human "$NET_TX")" "$(human "${NET_RX:-0}")" "$NET_IF"
fi
[ -n "$THROTTLE" ] && warn_add "Pi meldet Drosselung (get_throttled=${THROTTLE}) — Netzteil pruefen, sonst bricht ffmpeg weg"
rule

# ── NIGHTCRAWLER: Dienst, Dashboard, Abwehr, Fehler ──────────
sect "NIGHTCRAWLER"
if [ -z "$BOT_DIR" ]; then
  row "Installation" "$(dot warn)" "${WRN}nicht gefunden${R} ${FNT}— BOT_DIR in ${CONF} setzen (./motd.sh --doctor)${R}"
fi

# v4.2-W7: gemessen wurde oben, hier wird nur noch gezeichnet.
case "$BOT_STATE" in
  laeuft)
    _extra=""
    [ -n "$BOT_SINCE" ] && _extra="seit $BOT_SINCE"
    # NRestarts > 0 heisst: der Dienst ist zwar oben, faellt aber. Genau das
    # sieht man an "is-active" NIE — und es ist der wichtigere Befund.
    if [ -n "$BOT_NRS" ] && [ "$BOT_NRS" -gt 0 ] 2>/dev/null; then
      _extra="${_extra} · ${BOT_NRS}x neugestartet"
      warn_add "Dienst wurde ${BOT_NRS}x neu gestartet — Grund: ${TXT}journalctl -u ${SERVICE} -p err -n 50${R}"
    fi
    row "Bot" "$(dot ok)" "${TXT}laeuft${R} ${FNT}${_extra}${R}";;
  gestoppt)
    row "Bot" "$(dot err)" "${ERR}gestoppt${R} ${FNT}${BOT_RES:+(${BOT_RES})}${R}"
    warn_add "Bot laeuft nicht: ${TXT}sudo systemctl start ${SERVICE}${R}${FNT} — Grund: journalctl -u ${SERVICE} -n 80${R}";;
  prozess)
    row "Bot" "$(dot ok)" "${TXT}laeuft${R} ${FNT}(Prozess, kein systemd-Dienst)${R}";;
  tot)
    row "Bot" "$(dot err)" "${ERR}kein Prozess${R} ${FNT}(kein systemd-Dienst gefunden)${R}";;
esac

case "$DASH_STATE" in
  gesund)
    row "Dashboard" "$(dot ok)" "${TXT}gesund${R} ${FNT}:${DASH_PORT}${DASH_PROCS:+ · ${DASH_PROCS} Kindprozesse}${R}";;
  degradiert)
    row "Dashboard" "$(dot warn)" "${WRN}degradiert${R} ${FNT}:${DASH_PORT} — /healthz meldet ok=false${R}"
    warn_add "Dashboard degradiert (DB oder Dauerschleifen): ${TXT}curl -s localhost:${DASH_PORT}/api/selftest${R}";;
  stumm)
    row "Dashboard" "$(dot warn)" "${WRN}Port offen, keine Antwort${R} ${FNT}:${DASH_PORT}${R}";;
  *)
    row "Dashboard" "$(dot err)" "${ERR}kein Listener${R} ${FNT}:${DASH_PORT}${R}";;
esac
[ -n "$DASH_ZOMB" ] && [ "$DASH_ZOMB" -gt 0 ] 2>/dev/null && \
  warn_add "${DASH_ZOMB} Zombie-Kindprozesse — ffmpeg/streamlink werden nicht abgeraeumt"

if have systemctl && systemctl list-unit-files --no-legend 'crowdsec.service' 2>/dev/null | grep -q .; then
  if systemctl is-active --quiet crowdsec 2>/dev/null; then
    CS=$(command -v cscli 2>/dev/null || echo /usr/bin/cscli)
    BANS=""
    [ -x "$CS" ] && BANS=$(tmo 3 "$CS" decisions list -o raw 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    row "CrowdSec" "$(dot ok)" "${TXT}aktiv${R} ${FNT}${BANS:+· ${BANS} Bans}${R}"
  else
    row "CrowdSec" "$(dot err)" "${ERR}inaktiv${R} ${FNT}— Abwehr blind${R}"
  fi
fi

if [ -f "$LOGF" ]; then
  # error.log enthaelt NUR ERROR+ (eigener Handler). Interessant ist deshalb
  # nicht "gibt es Fehler", sondern "wie viele HEUTE und wie alt der letzte".
  #
  # v4.2-W7: und wie viele an den sechs Tagen davor. Eine nackte 4 sagt
  # nichts — vier Fehler hinter sechs stillen Tagen sind ein Ausbruch, vier
  # hinter sechs Tagen mit je dreissig sind eine Verbesserung. Genau diese
  # Frage beantwortete die Anzeige bisher nicht, und ohne sie wird die Zahl
  # nach drei Tagen nicht mehr gelesen.
  #
  # EIN Durchgang ueber das Ende der Datei statt sieben grep-Laeufe: die
  # sieben Tage werden vorab als Datumsliste gebaut und awk zaehlt sie in
  # einem Rutsch. Der Deckel von 50000 Zeilen ist der Preis dafuer, dass eine
  # gewachsene Logdatei den Login nicht ausbremst — bei mehr Fehlern als das
  # ist der Verlauf ohnehin nicht die dringendste Frage.
  ETODAY=$(tmo 3 grep -c "^$(date +%F)" "$LOGF" 2>/dev/null | tr -d ' ')
  ETODAY=${ETODAY:-0}
  ELAST=""
  if [ "$ETODAY" -gt 0 ] 2>/dev/null; then
    _lt=$(tail -n 1 "$LOGF" 2>/dev/null | cut -c1-19)
    [ -n "$_lt" ] && ELAST=$(date -d "$_lt" +%s 2>/dev/null)
    [ -n "$ELAST" ] && ELAST=" · letzter vor $(ago "$ELAST")"
  fi
  ESPARK=""
  _tage=""
  for _i in 6 5 4 3 2 1 0; do
    # GNU date kann -d, BSD/macOS braucht -v. Faellt beides aus, bleibt die
    # Liste leer und der Verlauf entfaellt — er ist Beiwerk, kein Befund.
    _d=$(date -d "-${_i} days" +%F 2>/dev/null || date -v-"${_i}"d +%F 2>/dev/null)
    [ -n "$_d" ] && _tage="${_tage}${_tage:+ }${_d}"
  done
  if [ -n "$_tage" ]; then
    _hist=$(tmo 3 tail -n 50000 "$LOGF" 2>/dev/null | awk -v tage="$_tage" '
      BEGIN{ n = split(tage, d, " "); for (i = 1; i <= n; i++) c[d[i]] = 0 }
      { k = substr($0, 1, 10); if (k in c) c[k]++ }
      END{ for (i = 1; i <= n; i++) printf "%s%d", (i > 1 ? " " : ""), c[d[i]] }')
    # Der Verlauf traegt dieselbe Ampel wie die Zahl daneben — zwei
    # verschiedene Farben fuer denselben Befund liest niemand als einen.
    if   [ "$ETODAY" -eq 0 ] 2>/dev/null; then _sc="$OK"
    elif [ "$ETODAY" -lt 5 ] 2>/dev/null; then _sc="$WRN"
    else _sc="$ERR"; fi
    [ -n "$_hist" ] && ESPARK="  ${_sc}$(spark $_hist)${R} ${FNT}7d${R}"
  fi
  if   [ "$ETODAY" -eq 0 ] 2>/dev/null; then row "Fehler" "$(dot ok)"   "${TXT}0${R} ${FNT}heute${R}${ESPARK}"
  elif [ "$ETODAY" -lt 5 ] 2>/dev/null; then row "Fehler" "$(dot warn)" "${WRN}${ETODAY}${R} ${FNT}heute${ELAST}${R}${ESPARK}"
  else row "Fehler" "$(dot err)" "${ERR}${ETODAY}${R} ${FNT}heute${ELAST}${R}${ESPARK}"
       warn_add "${ETODAY} Fehler heute: ${TXT}tail -n 40 ${LOGF}${R}"
  fi
fi
rule

# ── Tracking (Datenbank, streng lesend) ──────────────────────
dbq(){ # $1 = SQL, liefert eine Zeile mit |-getrennten Spalten
  if have sqlite3; then tmo 3 sqlite3 -readonly -separator '|' "$DB" "$1" 2>/dev/null
  elif have python3; then tmo 5 python3 -c '
import sqlite3, sys
try:
    c = sqlite3.connect("file:" + sys.argv[1] + "?mode=ro", uri=True)
    print("|".join(str(x) for x in c.execute(sys.argv[2]).fetchone()))
except Exception:
    pass' "$DB" "$1" 2>/dev/null
  fi; }

case "$DB_BACKEND" in
  mariadb|mysql)
    sect "TRACKING"
    row "Datenbank" "$(dot faint)" "${FNT}MariaDB — Zahlen nur im Dashboard (:${DASH_PORT})${R}"
    rule;;
  *)
  if [ -n "$DB" ] && [ -f "$DB" ] && { have sqlite3 || have python3; }; then
    # EIN Aufruf statt fuenf: jeder oeffnet die Datei, sperrt kurz und kostet
    # Zeit — bei jedem Login. restreams gibt es erst ab v37, deshalb der
    # Rueckfall auf die schmale Abfrage.
    STATS=$(dbq "SELECT (SELECT COUNT(*) FROM trackings),
                        (SELECT COUNT(*) FROM trackings WHERE last_live=1),
                        (SELECT COUNT(*) FROM trackings WHERE recording=1),
                        (SELECT COUNT(*) FROM trackings WHERE paused=1),
                        (SELECT COUNT(*) FROM restreams WHERE status='live')")
    [ -z "$STATS" ] && STATS=$(dbq "SELECT (SELECT COUNT(*) FROM trackings),
                        (SELECT COUNT(*) FROM trackings WHERE last_live=1),
                        (SELECT COUNT(*) FROM trackings WHERE recording=1),
                        (SELECT COUNT(*) FROM trackings WHERE paused=1), -1")
    if [ -n "$STATS" ]; then
      IFS='|' read -r TT LVN REC PAU RSL <<EOF
$STATS
EOF
      TT=${TT:-0}; LVN=${LVN:-0}; REC=${REC:-0}; PAU=${PAU:-0}; RSL=${RSL:--1}
      FFN=$(tmo 2 pgrep -c ffmpeg 2>/dev/null | tr -d ' '); FFN=${FFN:-0}
      sect "TRACKING"
      row "Getrackt" "$(dot faint)" "${TXT}${TT}${R} ${FNT}Streamer${R}${FNT}$([ "$PAU" -gt 0 ] 2>/dev/null && printf ' · %s pausiert' "$PAU")${R}"
      printf "  ${DIM}%-11s${R}%b ${TXT}%s${R} ${FNT}von %s${R}  %b\n" \
        "Live jetzt" "$(dot "$(onoff "$LVN")")" "$LVN" "$TT" "$(bar "$(pct "$LVN" "$TT")" 10)"
      row "Aufnahme" "$(dot "$(onoff "$REC")")" "${TXT}${REC}${R} ${FNT}aktiv · ${FFN} ffmpeg${R}"
      # Genau diese Luecke jagt der recording-Sentinel: DB sagt "nimmt auf",
      # es laeuft aber kein einziges ffmpeg.
      if [ "$REC" -gt 0 ] 2>/dev/null && [ "$FFN" -eq 0 ] 2>/dev/null; then
        warn_add "DB meldet ${REC} Aufnahmen, es laeuft aber KEIN ffmpeg — Karteileichen: ${TXT}/recstatus${R}"
      fi
      [ "$RSL" -ge 0 ] 2>/dev/null && row "Restream" "$(dot "$(onoff "$RSL")")" "${TXT}${RSL}${R} ${FNT}Ziel(e) live${R}"
      rule
    fi
  fi;;
esac

# ── Plattformen und Kanaele (Chips aus der .env) ─────────────
if [ -f "$ENVF" ]; then
  truthy(){ case "$(printf '%s' "${1:-}" | tr 'A-Z' 'a-z')" in
              1|true|yes|on|y) return 0;; *) return 1;; esac; }
  chip(){ case "$2" in
            on)   printf "${OK}▣ %s${R}  " "$1";;
            halb) printf "${WRN}▨ %s${R}  " "$1";;   # eingeschaltet, aber unvollstaendig
            *)    printf "${FNT}▢ %s${R}  " "$1";;
          esac; }
  # Die Vorfassung nahm JEDEN Schluessel, der das Stichwort enthielt. Ein
  # gesetztes KICK_INGEST_URL machte Kick gruen, obwohl KICK_ENABLED=0 war.
  # Reihenfolge jetzt: ausdrueckliches ENABLED schlaegt alles, danach zaehlt
  # nur ein echter Stream-Key.
  plat(){ # $1=Praefix  $2=Schluesselvariable  ($3 = Vorgabe wenn ENABLED fehlt)
    local en key
    en="$(envget "${1}_ENABLED")"; key="$(envget "$2")"
    if [ -n "$en" ] && ! truthy "$en"; then echo off; return; fi
    if [ -n "$key" ]; then echo on; else echo halb; fi
  }
  sect "RESTREAM"
  printf "  %b%b%b${FNT}  ▣ bereit · ▨ ohne Key · ▢ aus${R}\n" \
    "$(chip Kick    "$(plat KICK    KICK_STREAM_KEY)")" \
    "$(chip Twitch  "$(plat TWITCH  TWITCH_STREAM_KEY)")" \
    "$(chip YouTube "$(plat YOUTUBE YOUTUBE_STREAM_KEY)")"
  sect "KANAELE"
  _tg=off; [ -n "$(envget BOT_TOKEN)" ] && _tg=on
  _dc=off; [ -n "$(envget DISCORD_BOT_TOKEN)" ] && _dc=on
  _ai=halb   # keylos laeuft AZRAEL immer (nc/freeai), mit Key nur besser
  for k in ANTHROPIC_API_KEY OPENAI_API_KEY POLLINATIONS_API_KEY LLM7_TOKEN; do
    [ -n "$(envget "$k")" ] && { _ai=on; break; }
  done
  printf "  %b%b%b\n" "$(chip Telegram "$_tg")" "$(chip Discord "$_dc")" "$(chip AZRAEL "$_ai")"
  [ "$_tg" = off ] && warn_add "BOT_TOKEN fehlt in der .env — ohne ihn startet der Telegram-Teil nicht"
  rule
elif [ -n "$BOT_DIR" ]; then
  row ".env" "$(dot err)" "${ERR}fehlt${R} ${FNT}— cp .env.example .env && chmod 600 .env${R}"
  rule
fi

# ── Aufnahmen (Dateisystem, zwischengespeichert) ─────────────
# du/find ueber eine 400-GB-Bibliothek dauerte bei JEDEM Login mehrere
# Sekunden. Das Ergebnis aendert sich langsam — REC_CACHE_TTL reicht voellig.
if [ "$SHOW_REC" = 1 ] && [ -d "$RECDIR" ]; then
  CACHE="${TMPDIR:-/var/tmp}/nc-motd-rec-$(id -u 2>/dev/null || echo 0).cache"
  cache_age(){ local m
    m=$(stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null) || return 1
    [ -n "$m" ] || return 1; echo $(( $(date +%s) - m )); }
  _age=$(cache_age "$CACHE" 2>/dev/null)
  if [ -n "${_age:-}" ] && [ "$_age" -lt "$REC_CACHE_TTL" ] 2>/dev/null; then
    IFS='|' read -r RC RKB RNEW < "$CACHE"
  else
    RC=$(tmo 8 find "$RECDIR" -type f \( -name '*.ts' -o -name '*.mp4' -o -name '*.mkv' -o -name '*.flv' \) 2>/dev/null | wc -l | tr -d ' ')
    RKB=$(tmo 8 du -sk "$RECDIR" 2>/dev/null | cut -f1)
    if [ "$OS" = "Darwin" ]; then
      RNEW=$(tmo 8 find "$RECDIR" -type f -exec stat -f '%m' {} + 2>/dev/null | sort -n | tail -1)
    else
      RNEW=$(tmo 8 find "$RECDIR" -type f -printf '%T@\n' 2>/dev/null | sort -n | tail -1)
    fi
    printf '%s|%s|%s\n' "${RC:-0}" "${RKB:-0}" "${RNEW:-}" > "$CACHE" 2>/dev/null
  fi
  sect "AUFNAHMEN"
  printf "  ${TXT}%s${R} ${FNT}Dateien${R}   ${TXT}%s${R} ${FNT}gesamt${R}%b   ${FNT}%s${R}\n" \
    "${RC:-0}" \
    "$([ -n "${RKB:-}" ] && human $(( ${RKB:-0} * 1024 )) || echo '—')" \
    "$([ -n "${RNEW:-}" ] && printf "   ${FNT}neuste vor${R} ${TXT}%s${R}" "$(ago "$RNEW")")" \
    "$([ -n "${_age:-}" ] && [ "${_age:-0}" -lt "$REC_CACHE_TTL" ] 2>/dev/null && printf '(Stand: vor %ss)' "$_age")"
  rule
fi

# ── Hinweise ─────────────────────────────────────────────────
# Nur was WIRKLICH ansteht. Eine MOTD, die immer denselben Absatz zeigt, wird
# nach drei Tagen nicht mehr gelesen — dann faellt auch der echte Befund durch.
if [ -n "$WARN_LINES" ]; then
  sect "HINWEISE"
  printf '%s' "$WARN_LINES" | while IFS= read -r l; do
    [ -n "$l" ] && printf "  ${WRN}▲${R} %b\n" "$l"
  done
  rule
fi
printf "\n"
exit 0
