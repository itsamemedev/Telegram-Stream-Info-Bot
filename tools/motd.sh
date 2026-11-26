#!/usr/bin/env bash
#
# NIGHTCRAWLER — Message of the Day (Login-Statusbild)
#
#   ./motd.sh                  Vorschau (aendert nichts)
#   sudo ./motd.sh --install   als /etc/update-motd.d/99-nightcrawler einhaengen
#   sudo ./motd.sh --uninstall wieder entfernen
#   ./motd.sh --doctor         zeigt, WAS erkannt wurde und woher
#   ./motd.sh --configure      Einstellungen aendern, mit Live-Vorschau
#   ./motd.sh --configure --set WIDTH=60 [--dry-run]   dasselbe ohne Rueckfrage
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
# NEU IN v3.0 (v5.11.1-W210) — der Betreiber am 14.11.: „Kannst du mir die
# motd.sh anpassen, dass es aussieht wie die Uebersicht im Dashboard? Zumal die
# aktuelle mir 2x untereinander angezeigt wird."
#   * LEITSTAND. Kopf, Kennzahl-Kacheln, Lieferkette und die neun Tafeln wie
#     in der Uebersicht des Decks — und aus DERSELBEN Quelle: /api/leitstand
#     ueber Loopback (das Deck laesst lokale Anfragen ohne Token durch, W149).
#     Bis hierher las die MOTD ihre Zahlen selbst aus SQLite; der Betrieb
#     laeuft aber auf MariaDB, und dort stand nur „Zahlen nur im Dashboard".
#     Antwortet das Deck nicht, sagt die Tafel-Zeile das und warum — nichts
#     geladen ist nicht dasselbe wie nichts da (W99).
#   * DOPPELT. Das Skript laeuft EINMAL; gezeigt wird es auf fuenf bekannten
#     Wegen zweimal (Verweis /etc/motd -> /run/motd.dynamic, statische Kopie,
#     zweites Stueck in update-motd.d, Shell-Startdatei, pam_motd zweimal).
#     --install raeumt weg, was der MOTD gehoert, --doctor nennt jeden Fund
#     mit Ort, und das Statusbild selbst sagt es im Hinweisblock.
#   * VERALTET. Die installierte Kopie ist ein Schnappschuss — die
#     Update-Funktion erreicht sie nie. Sie meldet jetzt, wenn im Bestand
#     eine andere Fassung liegt, statt still alt zu bleiben.
#   * FASSUNG. Der Kopf las BUILD_STAMP als Literal aus bot.py; dort steht
#     seit v5 ein Funktionsaufruf, und der Kopf war wieder versionslos.
#
# Grundregel: eine MOTD darf NIE einen Login blockieren. Deshalb kein set -e,
# kein Kommando ohne Zeitdeckel und jedes externe Werkzeug nur nach have().

LC_ALL=C
export LC_ALL

# 3.1 (v5.11.4): die installierte Kopie laedt i18n.sh nicht mehr aus BOT_DIR.
# Der Sprung ist Absicht — eine 3.0 unter /etc/update-motd.d meldet sich damit
# als "veraltet" und nennt den Befehl, der sie ersetzt.
NC_MOTD_VERSION="3.1"

# v4.2-W100: Momentaufnahme der WIRKLICH von aussen gesetzten Variablen —
# noch VOR dem Vorgabenblock. Das ist der Kern: `WIDTH="${WIDTH:-54}"` setzt
# WIDTH, und eine Pruefung auf "ist gesetzt" danach ist fuer jede Variable
# wahr. Der erste Entwurf dieser Reparatur stand hinter den Vorgaben und
# liess damit die motd.conf NIE mehr wirken — gefangen hat das der eigene
# Vertrag (Datei 216 == Vorgabe 216), nicht das Nachdenken.
#
# Warum es das ueberhaupt gibt: der Kopf sagt seit je "per
# /etc/nightcrawler/motd.conf ODER Umgebung ueberschreibbar", der Code lud die
# Datei aber NACH den Vorgaben und gewann damit immer. Gemessen, nachdem
# tools/installer.sh die Datei angelegt hatte (SERVICE=''):
#
#     SERVICE=ausdruecklich  ohne conf -> SERVICE=[ausdruecklich]
#     SERVICE=ausdruecklich  mit  conf -> SERVICE=[]
#
# Reihenfolge jetzt: Umgebung > motd.conf > Vorgabe.
_MOTD_ENV_GESETZT=""
for _v in SERVICE BOT_DIR DASH_PORT DB DISK_TARGET WIDTH BARW SHOW_REC \
          REC_CACHE_TTL CPU_SAMPLE COLOR_MODE DEST; do
  # `+gesetzt` und nicht `-n`: ein ausdruecklich LEERES SERVICE= ist eine
  # Aussage ("nicht automatisch suchen") und keine fehlende Angabe.
  if [ -n "${!_v+gesetzt}" ]; then
    _MOTD_ENV_GESETZT="$_MOTD_ENV_GESETZT $_v=$(printf '%q' "${!_v}")"
  fi
done

# ── Vorgaben (jede per /etc/nightcrawler/motd.conf oder Umgebung ueberschreibbar)
SERVICE="${SERVICE:-}"          # leer = automatisch suchen
BOT_DIR="${BOT_DIR:-}"          # leer = automatisch suchen
DASH_PORT="${DASH_PORT:-}"      # leer = aus .env (DASHBOARD_PORT), sonst 8050
DB="${DB:-}"                    # leer = tiktok_bot.db im BOT_DIR, sonst groesste *.db
DISK_TARGET="${DISK_TARGET:-/}"
# v5.11.1-W210: 62 statt 54 — fuenf Kennzahl-Kacheln zu je zwoelf Spalten
# nebeneinander, wie die Kopfreihe des Decks. Wer per Handy einloggt, setzt
# WIDTH=50 (--configure); die Kacheln brechen dann in zwei Reihen um.
WIDTH="${WIDTH:-62}"
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

# v5.11.4 (OPS-1): die Ablage der installierten Kopie haengt am Verzeichnis
# von CONF, und zwar VOR dem Laden der Datei — CONF kommt nur aus Umgebung oder
# Vorgabe (/etc/nightcrawler), nie aus einer Datei. Was motd.conf danach
# setzt, verschiebt diese Ablage nicht.
NC_MOTD_ABLAGE="$(dirname "$CONF")/motd"

# shellcheck source=/dev/null
[ -r "$CONF" ] && . "$CONF"

# Und die Momentaufnahme wieder darueber — damit gewinnt, was der Aufrufer
# ausdruecklich gesagt hat. Siehe die Begruendung oben am Schnappschuss.
[ -n "$_MOTD_ENV_GESETZT" ] && eval "$_MOTD_ENV_GESETZT"
unset _MOTD_ENV_GESETZT _v

# v4.1-W17: Mehrsprachigkeit. Der Katalog liegt neben dem Werkzeug; ist er nicht
# erreichbar (die installierte Kopie unter /etc/update-motd.d/ hat kein
# locales/ daneben), bleibt alles deutsch statt zu scheitern.
#
# v5.11.4 (OPS-1): WOHER i18n.sh kommt, entscheidet der eigene Pfad. Neben
# sich (tools/lib/) hat es nur der Lauf aus dem Bestand; die installierte Kopie
# unter /etc/update-motd.d/ laeuft bei JEDEM Login als root und laedt NUR aus
# der root-eigenen Ablage, die --install anlegt. Bis 3.0 stand hier ein
# Rueckweg auf ${BOT_DIR}/tools/lib/i18n.sh — eine Datei, die der Bot-Nutzer
# schreiben darf und die nc/updater.py aus GitHub ueberschreibt. Gemessen mit
# einer praeparierten i18n.sh: "AUSGEFUEHRT als uid=0". Genau den Weg Bot →
# root schliesst W210 fuer motd.sh selbst aus; ueber den Katalog stand er offen.
# Fehlt die Ablage, bleibt die Ausgabe deutsch — das ist der kleinere Schaden.
_motd_root_eigen(){ # $1 = Datei; als root nur, wenn sie und ihr Ordner root
  # gehoeren und fuer niemanden sonst schreibbar sind. Eine falsch angelegte
  # Ablage waere sonst derselbe Weg zu root, nur einen Ordner weiter.
  [ "$(id -u)" -ne 0 ] && return 0
  [ -O "$1" ] && [ -O "$(dirname "$1")" ] || return 1
  [ -z "$(find "$1" "$(dirname "$1")" -maxdepth 0 -perm /022 2>/dev/null)" ]
}
# shellcheck source=lib/i18n.sh
if [ -r "$(dirname "$0")/lib/i18n.sh" ]; then
  . "$(dirname "$0")/lib/i18n.sh"
elif [ -r "$NC_MOTD_ABLAGE/tools/lib/i18n.sh" ] && _motd_root_eigen "$NC_MOTD_ABLAGE/tools/lib/i18n.sh"; then
  # i18n.sh sucht den Katalog relativ zu SICH SELBST (../../locales/), also
  # unter $NC_MOTD_ABLAGE/locales/ — dieselbe Form wie im Bestand.
  # shellcheck source=/dev/null
  . "$NC_MOTD_ABLAGE/tools/lib/i18n.sh"
else
  t(){ printf '%s' "$*"; }
  # v4.2-W123: tf muss es auch ohne Katalog geben, sonst stirbt --install
  # an "command not found" statt deutsch weiterzulaufen.
  # shellcheck disable=SC2059
  tf(){ if [ $# -le 1 ]; then printf '%s' "${1:-}"; else _f="$1"; shift; printf -- "$_f" "$@"; fi; }
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
# v5.11.1-W210: die Farben des Deck-Themas „Leitstand" (W207) statt Messing —
# Leuchtblau als Akzent, Violett als Zweitakzent, die Ampel wie im Deck:
#   --neon #5CD6FF  --neon-dim #4BA3D9  --text #DCE8FF  --text-faint #8296C2
#   --ok #7DF2C4    --amber #FFC25A     --red #FF7A86   --magenta #C8A2FF
if [ -z "$e" ]; then
  BR=""; DIM=""; TXT=""; FNT=""; OK=""; WRN=""; ERR=""; MAG=""; B=""; R=""
elif [ "$_tc" != 1 ] && [ "$_pal" = 16 ]; then
  # Die 16 Basisfarben. Haesslicher als das Leuchtblau, aber sichtbar —
  # und sichtbar schlaegt schoen, wenn es die Statusanzeige eines Servers ist.
  # Warnungen fett: Gelb und Cyan liegen in manchen Handy-Apps nah beieinander.
  BR="${e}[1;36m"; DIM="${e}[36m"; TXT="${e}[37m"
  FNT="${e}[90m"; OK="${e}[32m"; WRN="${e}[1;33m"
  ERR="${e}[31m"; MAG="${e}[35m"
  B="${e}[1m"; R="${e}[0m"
elif [ "$_tc" = 1 ]; then
  BR="${e}[38;2;92;214;255m"; DIM="${e}[38;2;75;163;217m"; TXT="${e}[38;2;220;232;255m"
  FNT="${e}[38;2;130;150;194m"; OK="${e}[38;2;125;242;196m"; WRN="${e}[38;2;255;194;90m"
  ERR="${e}[38;2;255;122;134m"; MAG="${e}[38;2;200;162;255m"
  B="${e}[1m"; R="${e}[0m"
else
  BR="${e}[38;5;81m"; DIM="${e}[38;5;74m"; TXT="${e}[38;5;189m"
  FNT="${e}[38;5;103m"; OK="${e}[38;5;122m"; WRN="${e}[38;5;221m"
  ERR="${e}[38;5;210m"; MAG="${e}[38;5;183m"
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
    # Ergaenzen, nicht ueberschreiben: ein zweites --install fand nur noch
    # die NEU hinzugekommenen Stuecke, schrieb nur sie in die Liste — und
    # --uninstall holte danach die vom ersten Lauf nie mehr zurueck.
    { cat "$NC_STATE" 2>/dev/null; printf '%s\n' $s; } | sort -u > "$NC_STATE.neu" \
      && mv -f "$NC_STATE.neu" "$NC_STATE"
    printf "  ${FNT}%s${R}%s\n" "$(t "Standard-MOTD gedaempft:")" "$s"
  else
    printf "  ${FNT}%s${R}\n" "$(t "Standard-MOTD war bereits still")"
  fi
  # Die STATISCHE /etc/motd laeuft nicht ueber run-parts und blieb deshalb
  # sichtbar, egal was hier gedaempft wurde. Auf Debian/Ubuntu steht dort das
  # Willkommens-Geschwafel des Images. Beiseitelegen statt loeschen — sie kommt
  # bei --uninstall zurueck.
  if [ -s /etc/motd ]; then
    mkdir -p "$(dirname "$NC_MOTD_SAVED")" 2>/dev/null
    if mv /etc/motd "$NC_MOTD_SAVED" 2>/dev/null; then
      : > /etc/motd 2>/dev/null || true
      printf "  ${FNT}%s${R} → %s\n" "$(t "statische /etc/motd beiseitegelegt")" "$NC_MOTD_SAVED"
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
      printf "  ${WRN}%s${R} ${FNT}— %s %s${R}\n" \
           "$(t "/etc/motd wurde seither neu beschrieben")" \
           "$(t "Sicherung bleibt unter")" "$NC_MOTD_SAVED"
    fi
  fi
  [ "$wieder" = 1 ] && printf "  ${FNT}%s${R}\n" "$(t "Standard-MOTD wiederhergestellt")"
  return 0
}

# ── Doppelte Anzeige (v5.11.1-W210) ──────────────────────────
# Der Betreiber am 14.11.: „die aktuelle wird mir 2x untereinander angezeigt".
# Das Skript laeuft dabei EINMAL — GEZEIGT wird es zweimal, und dafuer gibt es
# fuenf bekannte Wege. Jeder wird einzeln erkannt, weil jeder eine andere
# Abhilfe hat; ein „irgendwas ist doppelt" waere dieselbe Art Meldung wie ein
# blankes „HTTP 403".
NC_MARKE="NIGHTCRAWLER — Message of the Day"
NC_KOPIEN="/etc/nightcrawler/motd-kopien"
# NC_WURZEL setzt nur der Vertrag: er baut die Lage in einem Verzeichnis nach,
# statt auf der Pruefmaschine /etc anzufassen.

pam_motd_laeufe(){ # $1 = PAM-Datei -> Zahl der pam_motd-Zeilen OHNE noupdate
  # Nur diese rechnen die MOTD neu UND zeigen sie. Die Vorgabe von Ubuntu und
  # Debian ist genau EINE (motd=/run/motd.dynamic) und eine mit noupdate fuer
  # /etc/motd. Eine Ebene @include, weil common-session dort mitlaufen kann.
  local f="$1" inc w="${NC_WURZEL:-}"
  [ -r "$f" ] || { echo 0; return 0; }
  { grep -E '^[[:space:]]*session[[:space:]].*pam_motd\.so' "$f" 2>/dev/null
    for inc in $(sed -n 's/^[[:space:]]*@include[[:space:]]\{1,\}\([^[:space:]]*\).*/\1/p' "$f" 2>/dev/null); do
      case "$inc" in */*|"") continue;; esac
      grep -E '^[[:space:]]*session[[:space:]].*pam_motd\.so' "$w/etc/pam.d/$inc" 2>/dev/null
    done; } | grep -vc 'noupdate'
  return 0
}

doppelt_befunde(){ # -> je Befund eine Zeile "art|ort"
  [ "$OS" = "Linux" ] || return 0     # macOS: der Shell-rc-Block IST der Weg
  local f z n eigen w="${NC_WURZEL:-}"; eigen="$(basename "$DEST")"
  # (1) /etc/motd verweist auf die dynamische MOTD. pam_motd zeigt erst
  #     /run/motd.dynamic, danach /etc/motd (die noupdate-Zeile) — zweimal
  #     dieselbe Datei. Auf hochgezogenen Ubuntus steht der Verweis von Haus
  #     aus da. Mit -L geprueft und nicht mit -s: ein Verweis, dessen Ziel beim
  #     --install gerade fehlte, blieb sonst stehen.
  if [ -L "$w/etc/motd" ]; then
    z="$(readlink "$w/etc/motd" 2>/dev/null)"
    case "$z" in *motd.dynamic*|*run/motd*) printf 'verweis|/etc/motd -> %s\n' "$z";; esac
  fi
  # (2) eine STATISCHE Kopie des Statusbilds (motd.sh > /etc/motd, oder eine
  #     Datei in motd.d) — sie steht unter dem echten und veraltet still.
  for f in "$w"/etc/motd "$w"/run/motd "$w"/etc/motd.d/* "$w"/run/motd.d/*; do
    [ -f "$f" ] && [ ! -L "$f" ] || continue
    grep -qs "NIGHTCRAWLER" "$f" && printf 'kopie|%s\n' "$f"
  done
  # (3) ein zweites Stueck in update-motd.d, das ebenfalls das Statusbild
  #     zeichnet (eine alte Kopie unter anderem Namen).
  for f in "$w"/etc/update-motd.d/*; do
    [ -f "$f" ] && [ -x "$f" ] || continue
    case "$(basename "$f")" in "$eigen"|.*) continue;; esac
    grep -qs -e "$NC_MARKE" -e 'motd\.sh' "$f" && printf 'stueck|%s\n' "$f"
  done
  # (4) eine Shell-Startdatei ruft das Statusbild bei jedem Login noch einmal.
  #     Kommentare und alias-Zeilen zaehlen nicht: die laufen beim Login nicht.
  for f in "$w"/etc/profile "$w"/etc/bash.bashrc "$w"/etc/zsh/zshrc "$w"/etc/zsh/zprofile \
           "$w"/etc/profile.d/*.sh "$w"/root/.bashrc "$w"/root/.profile "$w"/root/.bash_profile \
           "$w"/root/.zshrc "$w"/home/*/.bashrc "$w"/home/*/.profile "$w"/home/*/.bash_profile \
           "$w"/home/*/.zshrc; do
    [ -f "$f" ] && [ -r "$f" ] || continue
    n="$(grep -n -e 'motd\.sh' -e 'update-motd\.d' -e 'motd\.dynamic' -e '99-nightcrawler' "$f" 2>/dev/null \
         | grep -v -e '^[0-9]*:[[:space:]]*#' -e '^[0-9]*:[[:space:]]*alias[[:space:]]' | head -1 | cut -d: -f1)"
    [ -n "$n" ] && printf 'startdatei|%s:%s\n' "$f" "$n"
  done
  # (5) pam_motd rechnet und zeigt das Bild zweimal.
  n="$(pam_motd_laeufe "$w/etc/pam.d/sshd")"
  [ "${n:-0}" -ge 2 ] 2>/dev/null && printf 'pam|%s/etc/pam.d/sshd\n' "$w"
  return 0
}

doppelt_text(){ # $1 = art -> was es ist (uebersetzt)
  case "$1" in
    verweis)    t "/etc/motd verweist auf die dynamische MOTD";;
    kopie)      t "statische Kopie des Statusbilds";;
    stueck)     t "zweites Statusbild in /etc/update-motd.d";;
    startdatei) t "Shell-Startdatei ruft das Statusbild noch einmal";;
    pam)        t "pam_motd laeuft zweimal mit Aktualisierung";;
    *)          printf '%s' "$1";;
  esac
}

doppelt_abhilfe(){ # $1 = art, $2 = ort -> was zu tun ist (uebersetzt)
  case "$1" in
    startdatei) tf "Zeile %s in %s entfernen" "${2##*:}" "${2%:*}";;
    pam)        t "eine der pam_motd-Zeilen in /etc/pam.d/sshd mit noupdate versehen";;
    *)          printf 'sudo %s --install' "$(motd_pfad)";;
  esac
}
motd_pfad(){
  if [ -n "$BOT_DIR" ]; then printf '%s/tools/motd.sh' "$BOT_DIR"; else printf 'tools/motd.sh'; fi
}

doppelt_beheben(){
  # Nur was der MOTD gehoert, wird angefasst: Verweise und Kopien des eigenen
  # Bilds. Fremde Startdateien und PAM bleiben unberuehrt und werden genannt —
  # eine falsche PAM-Zeile sperrt den SSH-Zugang, und das laesst sich aus der
  # Ferne nicht mehr beheben.
  local art ort f ziel w="${NC_WURZEL:-}"
  doppelt_befunde > "${TMPDIR:-/tmp}/nc-motd-doppelt.$$" 2>/dev/null
  while IFS='|' read -r art ort; do
    case "$art" in
      verweis)
        mkdir -p "$(dirname "$NC_MOTD_SAVED")" 2>/dev/null
        ziel="$NC_MOTD_SAVED"; [ -e "$ziel" ] || [ -L "$ziel" ] && ziel="$NC_MOTD_SAVED.verweis"
        if mv "$w/etc/motd" "$ziel" 2>/dev/null; then
          : > "$w/etc/motd" 2>/dev/null || true
          printf "  ${OK}✔${R} ${FNT}%s → %s${R}\n" "$(t "Verweis /etc/motd beiseitegelegt")" "$ziel"
        fi;;
      kopie|stueck)
        f="${ort}"; mkdir -p "$NC_KOPIEN" 2>/dev/null
        if [ "$art" = stueck ]; then
          chmod -x "$f" 2>/dev/null && printf '%s\n' "$(basename "$f")" >> "$NC_STATE" \
            && printf "  ${OK}✔${R} ${FNT}%s %s${R}\n" "$(t "zweites Statusbild gedaempft:")" "$f"
        elif mv "$f" "$NC_KOPIEN/$(basename "$f").$(date +%Y%m%d%H%M%S)" 2>/dev/null; then
          [ "$f" = "$w/etc/motd" ] && { : > "$f" 2>/dev/null || true; }
          printf "  ${OK}✔${R} ${FNT}%s %s → %s${R}\n" "$(t "alte Kopie beiseitegelegt:")" "$f" "$NC_KOPIEN"
        fi;;
      *)
        printf "  ${WRN}▲${R} %s ${FNT}(%s)${R}\n    ${TXT}%s${R}\n" \
               "$(doppelt_text "$art")" "$ort" "$(doppelt_abhilfe "$art" "$ort")";;
    esac
  done < "${TMPDIR:-/tmp}/nc-motd-doppelt.$$"
  rm -f "${TMPDIR:-/tmp}/nc-motd-doppelt.$$"
  return 0
}

# v4.2-W126: der Inhalt steht getrennt vom Schreiben, weil --configure ihn
# vorher mit der vorhandenen Datei vergleicht. WIDTH und BARW stehen jetzt mit
# drin: --configure bietet sie an, und ein Wert, den --install beim naechsten
# Lauf nicht wieder hineinschreibt, waere danach still weg.
konf_inhalt(){ # $1 = wer schreibt (--install | --configure)
  printf '# %s\n' "$(tf 'NIGHTCRAWLER MOTD — erzeugt von motd.sh %s am %s' "$1" "$(date '+%F %T')")"
  printf '# %s\n' "$(t 'Von Hand aenderbar; --install und --configure ueberschreiben die Datei.')"
  printf 'SERVICE=%s\n'     "$(qq "$SERVICE")"
  printf 'BOT_DIR=%s\n'     "$(qq "$BOT_DIR")"
  printf 'DASH_PORT=%s\n'   "$(qq "$DASH_PORT")"
  printf 'DB=%s\n'          "$(qq "$DB")"
  printf 'DISK_TARGET=%s\n' "$(qq "$DISK_TARGET")"
  printf 'SHOW_REC=%s\n'    "$(qq "$SHOW_REC")"
  printf 'CPU_SAMPLE=%s\n'  "$(qq "$CPU_SAMPLE")"
  printf 'COLOR_MODE=%s\n'  "$(qq "$COLOR_MODE")"
  printf 'WIDTH=%s\n'       "$(qq "$WIDTH")"
  printf 'BARW=%s\n'        "$(qq "$BARW")"
}

write_conf(){ # [$1 = wer schreibt, Vorgabe --install]
  # Die erkannten Pfade festschreiben. Ohne das raet die installierte Kopie bei
  # jedem Login neu — und raet als root anders als du beim Testen.
  mkdir -p "$(dirname "$CONF")" 2>/dev/null || return 1
  # Erst daneben, dann umbenennen: ein Login, der mitten im Schreiben die
  # halbe Datei sourct, saehe sonst Vorgaben statt der Konfiguration.
  konf_inhalt "${1:---install}" > "$CONF.neu" && mv -f "$CONF.neu" "$CONF" || return 1
  chmod 644 "$CONF" 2>/dev/null
  printf "${OK}✔ %s${R} → %s\n" "$(t "Konfiguration")" "$CONF"
}
qq(){ printf "'%s'" "$(printf '%s' "${1:-}" | sed "s/'/'\\\\''/g")"; }

need_root(){ [ "$(id -u)" -eq 0 ] || { printf "${WRN}%s${R} sudo %s %s\n" "$(t "Bitte mit sudo:")" "$0" "$1"; exit 1; }; }

# v5.11.4 (OPS-1): Uebersetzung fuer die installierte Kopie. KOPIERT, nicht
# verwiesen: die Kopie liest bei jedem Login als root, und alles, was sie dabei
# laedt, muss root gehoeren (root:root 0644). Wie motd.sh selbst ist das ein
# Schnappschuss — die Update-Funktion erreicht ihn nie, --install erneuert ihn.
i18n_ablegen(){ # $1 = Ordner von motd.sh im Bestand, $2 = Ablage
  local quelle="$1" ziel="$2" k
  [ -r "$quelle/lib/i18n.sh" ] || return 0     # Lauf aus einer Kopie: nichts mitzunehmen
  ( umask 022
    mkdir -p "$ziel/tools/lib" "$ziel/locales" &&
    cp "$quelle/lib/i18n.sh" "$ziel/tools/lib/i18n.sh" &&
    for k in "$quelle"/../locales/tools.*.tsv; do
      [ -f "$k" ] && cp "$k" "$ziel/locales/"
    done ) || { printf "${WRN}%s${R} %s\n" "$(t "Uebersetzung nicht abgelegt — Ausgabe bleibt deutsch:")" "$ziel"; return 0; }
  [ "$(id -u)" -eq 0 ] && chown -R root:root "$ziel" 2>/dev/null
  chmod 755 "$ziel" "$ziel/tools" "$ziel/tools/lib" "$ziel/locales" 2>/dev/null
  find "$ziel" -type f -exec chmod 644 {} + 2>/dev/null
  printf "${OK}✔ %s${R} → %s\n" "$(t "Uebersetzung abgelegt")" "$ziel"
}

install_linux(){
  local src; src="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  [ -d /etc/update-motd.d ] || mkdir -p /etc/update-motd.d
  cp "$src" "$DEST" && chmod +x "$DEST" || { printf "${ERR}✘ %s${R}\n" "$(t "Installation fehlgeschlagen")"; exit 1; }
  printf "${OK}✔ %s${R} → %s\n" "$(t "installiert")" "$DEST"
  i18n_ablegen "$(dirname "$src")" "$NC_MOTD_ABLAGE"
  write_conf
  silence_defaults
  doppelt_beheben
  printf "  ${FNT}%s  sudo run-parts /etc/update-motd.d/${R}\n" "$(t "Vorschau:")"
  printf "  ${FNT}%s${R}\n" "$(t "'Last login' kommt von SSH — optional 'PrintLastLog no' in sshd_config")"
  if ! grep -rqs 'pam_motd' /etc/pam.d/sshd 2>/dev/null; then
    printf "  ${WRN}%s${R} ${FNT}%s${R}\n" "$(t "Hinweis:")" \
           "$(t "/etc/pam.d/sshd laedt pam_motd nicht — dann bleibt der Login still.")"
  fi
}

install_darwin(){
  # macOS kennt weder /etc/update-motd.d noch pam_motd. Sauberster Weg ist ein
  # markierter Block in der Shell-rc des Nutzers — idempotent und rueckbaubar.
  local src rc; src="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  rc="${SHELLRC:-$HOME/.zshrc}"; [ -n "${BASH_VERSION:-}" ] && [ ! -f "$rc" ] && rc="$HOME/.bash_profile"
  if grep -qs "$RC_MARK_A" "$rc"; then
    printf "${FNT}%s${R}\n" "$(tf "bereits eingetragen in %s" "$rc")"
  else
    { printf '\n%s\n' "$RC_MARK_A"
      printf '[ -t 1 ] && [ -z "$NC_MOTD_SHOWN" ] && export NC_MOTD_SHOWN=1 && "%s"\n' "$src"
      printf '%s\n' "$RC_MARK_E"; } >> "$rc"
    printf "${OK}✔ %s${R} → %s\n" "$(t "eingetragen")" "$rc"
  fi
  write_conf
  printf "  ${FNT}%s  exec \$SHELL -l${R}\n" "$(t "Wirksam nach:")"
}

uninstall_darwin(){
  local rc; rc="${SHELLRC:-$HOME/.zshrc}"
  for rc in "$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc"; do
    [ -f "$rc" ] && grep -qs "$RC_MARK_A" "$rc" || continue
    sed -i.nc-bak "/$(printf '%s' "$RC_MARK_A" | sed 's/[][\.*^$\/]/\\&/g')/,/$(printf '%s' "$RC_MARK_E" | sed 's/[][\.*^$\/]/\\&/g')/d" "$rc"
    printf "${OK}✔ %s${R} %s ${FNT}(%s %s.nc-bak)${R}\n" \
             "$(t "entfernt aus")" "$rc" "$(t "Sicherung:")" "$rc"
  done
}

# ── --configure (v4.2-W126) ──────────────────────────────────
# Bis hierher hiess "anpassen": die Datei von Hand bearbeiten und danach per
# Login nachsehen, ob es so aussieht wie gedacht. Ein falscher Wert (WIDTH=abc,
# COLOR_MODE=farbig) faellt dabei nicht auf — die MOTD rechnet still mit
# Unsinn oder der Vorgabe weiter. Jetzt: jeder Wert wird geprueft, bevor er
# irgendwo landet, und die Vorschau laeuft sofort mit dem neuen Wert.
KONF_FELDER="SHOW_REC COLOR_MODE WIDTH BARW DISK_TARGET CPU_SAMPLE SERVICE BOT_DIR DASH_PORT DB"

konf_hilfe(){ # $1 = Name -> eine Zeile Erklaerung
  case "$1" in
    SHOW_REC)    t "Aufnahmen-Block zeigen (1) oder weglassen (0)";;
    COLOR_MODE)  t "Farben: always | auto | truecolor | 256 | 16 | off";;
    WIDTH)       t "Breite des Rahmens in Zeichen (40-120)";;
    BARW)        t "Breite der Balken in Zeichen (8-60)";;
    DISK_TARGET) t "Welche Platte gezeigt wird (ein Verzeichnis darauf)";;
    CPU_SAMPLE)  t "Messfenster fuer CPU und Netz in Sekunden (0 = aus, hoechstens 2)";;
    SERVICE)     t "Name des systemd-Dienstes (leer = selbst suchen)";;
    BOT_DIR)     t "Verzeichnis des Bots (dort liegt bot.py)";;
    DASH_PORT)   t "Port des Dashboards";;
    DB)          t "SQLite-Datei fuer die Zahlen (leer = selbst suchen)";;
  esac
}

# 0 = gueltig. Sonst steht der Grund auf stdout — der Aufrufer zeigt ihn.
konf_pruefen(){ # $1 = Name, $2 = Wert
  local n="$1" v="$2"
  case "$n" in
    SHOW_REC)   case "$v" in 0|1) return 0;; esac; t "erlaubt sind 0 und 1";;
    COLOR_MODE) case "$v" in always|auto|truecolor|256|16|off) return 0;; esac
                t "erlaubt sind always, auto, truecolor, 256, 16, off";;
    WIDTH|BARW|DASH_PORT)
      local lo hi
      case "$n" in WIDTH) lo=40; hi=120;; BARW) lo=8; hi=60;; *) lo=1; hi=65535;; esac
      case "$v" in ''|*[!0-9]*) tf "keine ganze Zahl: %s" "$v"; return 1;; esac
      # 10# gegen fuehrende Nullen: "08" waere fuer bash sonst Oktal und ungueltig.
      if [ "$((10#$v))" -ge "$lo" ] && [ "$((10#$v))" -le "$hi" ]; then return 0; fi
      tf "ausserhalb von %s bis %s" "$lo" "$hi";;
    CPU_SAMPLE)
      if printf '%s' "$v" | grep -Eq '^([0-1](\.[0-9]+)?|2(\.0+)?)$'; then return 0; fi
      t "eine Zahl von 0 bis 2, z. B. 0.20";;
    DISK_TARGET|BOT_DIR)
      if [ -d "$v" ]; then
        [ "$n" = BOT_DIR ] && ! is_botdir "$v" && { tf "kein bot.py in %s" "$v"; return 1; }
        return 0
      fi
      tf "kein Verzeichnis: %s" "$v";;
    DB)
      # Leer heisst "selbst suchen" — dieselbe Regel wie in der Erkennung oben.
      # Eine falsch erkannte Datenbank (brain.db, eine alte Kopie) ist genau der
      # Fall, fuer den man hier etwas eintraegt.
      [ -z "$v" ] || [ -f "$v" ] && return 0
      tf "keine Datei: %s" "$v";;
    SERVICE)
      # Leer ist erlaubt (= selbst suchen). Leerzeichen und Anfuehrungszeichen
      # nicht: der Wert geht als Name an systemctl.
      case "$v" in *[[:space:]\'\"\;\$\`]*) t "Name ohne Leer- und Sonderzeichen";; *) return 0;; esac;;
    *) tf "unbekannte Einstellung: %s" "$n";;
  esac
  return 1
}

konf_wert(){ eval "printf '%s' \"\${$1}\""; }

konf_vorschau(){
  # Die Vorschau ist DIESELBE Datei, als eigener Prozess und mit den neuen
  # Werten aus der Umgebung — die gewinnt seit W100 vor der motd.conf. Ein
  # nachgebauter Ausschnitt waere eine zweite Wahrheit.
  printf "\n  ${FNT}── %s ──${R}\n" "$(t "Vorschau")"
  env SERVICE="$SERVICE" BOT_DIR="$BOT_DIR" DASH_PORT="$DASH_PORT" DB="$DB" \
      DISK_TARGET="$DISK_TARGET" SHOW_REC="$SHOW_REC" CPU_SAMPLE="$CPU_SAMPLE" \
      COLOR_MODE="$COLOR_MODE" WIDTH="$WIDTH" BARW="$BARW" \
      "${BASH:-bash}" "$0" 2>&1
}

# Nur die Wertzeilen vergleichen: der Kopf traegt Datum und Urheber und waere
# bei jedem Lauf "geaendert".
konf_werte(){ grep -v '^#' "$1" 2>/dev/null; }

konf_speichern(){ # $1 = 1: nur zeigen (--dry-run)
  local neu; neu="$(mktemp 2>/dev/null || echo "/tmp/nc-motd-konf.$$")"
  konf_inhalt --configure > "$neu"
  if [ -r "$CONF" ] && [ "$(konf_werte "$CONF")" = "$(konf_werte "$neu")" ]; then
    printf "  ${FNT}%s${R} %s\n" "$(t "Unveraendert — nichts geschrieben:")" "$CONF"
    rm -f "$neu"; return 0
  fi
  printf "\n  ${B}%s${R} %s\n" "$(t "Aenderungen an")" "$CONF"
  if [ -r "$CONF" ]; then
    diff <(konf_werte "$CONF") <(konf_werte "$neu") | sed -n 's/^</  -/p; s/^>/  +/p'
  else
    konf_werte "$neu" | sed 's/^/  + /'
  fi
  if [ "${1:-0}" = 1 ]; then
    printf "  ${FNT}%s${R}\n" "$(t "Probelauf — nichts geschrieben.")"
    rm -f "$neu"; return 0
  fi
  # Schreibrecht VORHER pruefen: ein "Permission denied" nach der Fragerei
  # waere die ganze Arbeit fuer nichts.
  local ziel_dir; ziel_dir="$(dirname "$CONF")"
  if { [ -e "$CONF" ] && [ ! -w "$CONF" ]; } || { [ ! -e "$CONF" ] && [ -d "$ziel_dir" ] && [ ! -w "$ziel_dir" ]; } \
     || { [ ! -d "$ziel_dir" ] && [ "$(id -u)" -ne 0 ]; }; then
    printf "  ${WRN}%s${R} sudo %s --configure\n" "$(tf "Keine Schreibrechte fuer %s — bitte mit:" "$CONF")" "$0"
    rm -f "$neu"; return 1
  fi
  rm -f "$neu"
  write_conf --configure
}

konfigurieren(){
  local setzen="" probe=0 a n v grund
  while [ $# -gt 0 ]; do
    case "$1" in
      --set|--set=*)
        if [ "$1" = --set ]; then shift; a="${1:-}"; else a="${1#--set=}"; fi
        # Ein leeres --set ist ein Bedienfehler, kein "nichts setzen": sonst
        # schriebe der Lauf die erkannten Vorgaben und meldete Erfolg
        # (Codex-Befund, PR #165).
        [ -n "$a" ] || { printf "${ERR}✘ %s${R}\n" "$(t "--set ohne NAME=WERT")"; return 2; }
        setzen="$setzen
$a";;
      --dry-run) probe=1;;
      *) printf "${ERR}%s${R}\n" "$(tf "Unbekannte Option: %s" "$1")"; return 2;;
    esac
    shift
  done

  # ── Ohne Rueckfrage: --set NAME=WERT ... (fuer Skripte und den Installer)
  if [ -n "$setzen" ]; then
    while IFS= read -r a; do
      [ -n "$a" ] || continue
      n="${a%%=*}"; v="${a#*=}"
      case " $KONF_FELDER " in *" $n "*) ;; *)
        printf "${ERR}✘ %s${R}\n" "$(tf "unbekannte Einstellung: %s" "$n")"; return 2;; esac
      [ "$a" = "$n" ] && { printf "${ERR}✘ %s${R}\n" "$(tf "Wert fehlt: %s=..." "$n")"; return 2; }
      if ! grund="$(konf_pruefen "$n" "$v")"; then
        # Abbrechen statt ueberspringen: ein Skript, das drei Werte setzt und
        # zwei davon wirken, meldet sonst Erfolg fuer eine halbe Konfiguration.
        printf "${ERR}✘ %s=%s${R} — %s\n" "$n" "$v" "$grund"; return 2
      fi
      printf -v "$n" '%s' "$v"
    done <<< "$setzen"
    konf_speichern "$probe"; return $?
  fi

  # ── Gefuehrt
  local i nr w
  while :; do
    printf "\n${BR}${B}NIGHTCRAWLER MOTD — %s${R}  ${FNT}%s${R}\n\n" "$(t "Einstellungen")" "$CONF"
    i=0
    for n in $KONF_FELDER; do
      i=$((i+1)); w="$(konf_wert "$n")"
      printf "  ${B}%2d${R}  %-12s ${TXT}%-18s${R} ${FNT}%s${R}\n" "$i" "$n" "${w:-—}" "$(konf_hilfe "$n")"
    done
    printf "\n  ${FNT}%s${R}\n" "$(t "Nummer = aendern · v = Vorschau · s = speichern · q = verwerfen")"
    printf "  > "
    IFS= read -r a || { printf '\n'; return 1; }
    case "$a" in
      q|Q) printf "  ${FNT}%s${R}\n" "$(t "Verworfen — nichts geschrieben.")"; return 0;;
      v|V) konf_vorschau; continue;;
      s|S) konf_speichern "$probe"; return $?;;
      ''|*[!0-9]*) continue;;
    esac
    nr=0; n=""
    for w in $KONF_FELDER; do nr=$((nr+1)); [ "$nr" = "$a" ] && n="$w"; done
    [ -n "$n" ] || continue
    printf "  %s %s [%s]: " "$n" "$(t "neuer Wert, Enter = behalten")" "$(konf_wert "$n")"
    IFS= read -r v || { printf '\n'; return 1; }
    [ -z "$v" ] && continue
    if ! grund="$(konf_pruefen "$n" "$v")"; then
      printf "  ${ERR}✘ %s${R}\n" "$grund"; continue
    fi
    printf -v "$n" '%s' "$v"
    # Die Live-Vorschau: gleich nach jeder Aenderung, nicht erst auf Zuruf —
    # ob 60 Zeichen auf das Handy passen, sieht man, nicht liest man.
    konf_vorschau
  done
}

doctor(){
  printf "\n${BR}${B}NIGHTCRAWLER MOTD — %s${R}  ${FNT}v%s${R}\n\n" "$(t "Erkennung")" "$NC_MOTD_VERSION"
  printf "  %-12s %s\n" "$(t "System")"    "$OS $(uname -r 2>/dev/null)"
  printf "  %-12s %s\n" "$(t "Konfig")"    "$([ -r "$CONF" ] && echo "$CONF" || echo "— $(t "keine, alles erkannt")")"
  printf "  %-12s %s\n" "$(t "Dienst")"    "${SERVICE:-— $(t "nicht gefunden")}"
  printf "  %-12s %s\n" "BOT_DIR"   "${BOT_DIR:-— $(t "nicht gefunden")}"
  printf "  %-12s %s\n" ".env"      "$([ -f "$ENVF" ] && echo "$ENVF" || echo "— $(t "fehlt")")"
  printf "  %-12s %s\n" "$(t "Datenbank")" "${DB:-— $(t "keine gefunden")}${DB_BACKEND:+  (DB_BACKEND=$DB_BACKEND)}"
  printf "  %-12s %s\n" "$(t "Log")"       "$([ -f "$LOGF" ] && echo "$LOGF" || echo "— $(t "fehlt")")"
  printf "  %-12s %s\n" "$(t "Aufnahmen")" "$([ -d "$RECDIR" ] && echo "$RECDIR" || echo "— $(t "fehlt")")"
  printf "  %-12s %s\n" "Dashboard" ":$DASH_PORT"
  _ni="$(detect_netif)"
  printf "  %-12s %s\n" "$(t "Netz")"      "${_ni:-— $(t "keine Schnittstelle erkannt")}"
  printf "  %-12s %s\n" "$(t "Werkzeuge")" "$(for t in systemctl ss curl sqlite3 python3 free df find du; do have $t && printf '%s ' "$t"; done)"
  # v5.11.1-W210: woher die Tafeln kommen — und wenn nicht, warum nicht.
  if ! have curl || ! have python3; then
    _lq="— $(t "curl oder python3 fehlt")"
  elif tmo 4 curl -s -k --max-time 3 "http://127.0.0.1:${DASH_PORT}/api/leitstand" 2>/dev/null | grep -q '"tafeln"' \
    || tmo 4 curl -s -k --max-time 3 "https://127.0.0.1:${DASH_PORT}/api/leitstand" 2>/dev/null | grep -q '"tafeln"'; then
    _lq="/api/leitstand :${DASH_PORT}"
  else
    _lq="— $(t "Deck antwortet nicht, Zahlen aus der Datenbank")"
  fi
  printf "  %-12s %s\n" "$(t "Tafeln")" "$_lq"
  _fv=""; [ -n "$BOT_DIR" ] && [ -r "$BOT_DIR/tools/motd.sh" ] && \
    _fv=$(sed -n 's/^NC_MOTD_VERSION="\([^"]*\)".*/\1/p' "$BOT_DIR/tools/motd.sh" | head -1)
  printf "  %-12s %s\n" "$(t "Fassung")" "$NC_MOTD_VERSION${_fv:+  ($(t "im Bestand") $_fv)}"
  # Die doppelte Anzeige: jeder Fund mit Ort und Abhilfe — oder ausdruecklich
  # keiner, mit den PAM-Zeilen, an denen man es selbst nachsehen kann.
  printf "\n  ${BR}${B}%s${R}\n" "$(t "Doppelte Anzeige")"
  _dop="$(doppelt_befunde)"
  if [ -n "$_dop" ]; then
    printf '%s\n' "$_dop" | while IFS='|' read -r _a _o; do
      printf "  ${WRN}▲${R} %s ${FNT}(%s)${R}\n    ${TXT}%s${R}\n" \
             "$(doppelt_text "$_a")" "$_o" "$(doppelt_abhilfe "$_a" "$_o")"
    done
  else
    printf "  ${OK}●${R} %s\n" "$(t "keine bekannte Ursache gefunden")"
    [ -r /etc/pam.d/sshd ] && grep -n 'pam_motd' /etc/pam.d/sshd 2>/dev/null | sed 's/^/    /'
  fi
  printf "\n  ${FNT}%s %s %s${R}\n\n" "$(t "Falsch erkannt? Werte in")" "$CONF" \
         "$(t "eintragen (oder als Umgebung setzen).")"
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
    if [ -f "$DEST" ]; then rm -f "$DEST" && printf "${OK}✔ %s${R} → %s\n" "$(t "entfernt")" "$DEST"
    else printf "${FNT}%s${R}\n" "$(t "nicht installiert")"; fi
    restore_defaults
    case "$NC_MOTD_ABLAGE" in */motd) [ -d "$NC_MOTD_ABLAGE" ] && rm -rf "$NC_MOTD_ABLAGE";; esac
    printf "  ${FNT}%s %s${R}\n" "$CONF" "$(t "bleibt liegen (harmlos, enthaelt nur Pfade)")"
    exit 0;;
  --doctor)  doctor;;
  --configure) shift; konfigurieren "$@"; exit $?;;
  --version) printf 'NIGHTCRAWLER MOTD %s\n' "$NC_MOTD_VERSION"; exit 0;;
  --help|-h)
    printf "NIGHTCRAWLER MOTD %s\n\n" "$NC_MOTD_VERSION"
    printf "  %s\n" "$(t "(ohne Argument)  Vorschau — aendert nichts")"
    printf "  --install        %s\n" "$(t "einhaengen + Standard-MOTD daempfen (sudo; macOS: Shell-rc)")"
    printf "  --uninstall      %s\n" "$(t "entfernen + Standard-MOTD wiederherstellen")"
    printf "  --doctor         %s\n" "$(t "zeigt, was erkannt wurde und woher")"
    printf "  --configure      %s\n" "$(t "Einstellungen aendern, mit Vorschau (--set NAME=WERT, --dry-run)")"
    printf "  --version        %s\n\n" "$(t "Fassung")"
    printf "%s %s %s\n" "$(t "Anpassen ueber")" "$CONF" "$(t "oder Umgebung:")"
    printf "  SERVICE BOT_DIR DASH_PORT DB DISK_TARGET SHOW_REC CPU_SAMPLE COLOR_MODE\n"
    printf "  COLOR_MODE: always (%s) | auto | truecolor | 256 | 16 | off\n" "$(t "Vorgabe")"
    printf "%s  BOT_DIR=~/mein-bot COLOR_MODE=16 ./motd.sh\n" "$(t "Beispiel:")"
    exit 0;;
  "") ;;
  *) printf "${WRN}%s${R}  (--help)\n" "$(tf "Unbekannte Option: %s" "$1")"; exit 1;;
esac

# ── Zeichen-Helfer ───────────────────────────────────────────
col4(){ local p=${1:-0}; if [ "$p" -ge 90 ]; then printf '%s' "$ERR"
        elif [ "$p" -ge 70 ]; then printf '%s' "$WRN"; else printf '%s' "$OK"; fi; }
rule(){ printf "${DIM}"; awk -v n="$WIDTH" 'BEGIN{while(n-->0)printf "━"}'; printf "${R}\n"; }
# v4.2-W14: die Senken uebersetzen. motd.sh band lib/i18n.sh seit v4.1-W17
# ein und rief t() KEIN EINZIGES MAL auf — jede Zeile war ein printf mit
# deutschem Literal. Und tools/i18n_tools.py sammelte nur aus den Senken
# von installer.sh, die es hier gar nicht gibt, und meldete deshalb 100 %
# Abdeckung fuer eine Datei, die zu 0 % uebersetzt war.
# v5.11.1-W210: sichtbare Breite — ohne Farbfolgen, und ein UTF-8-Zeichen als
# EINES. Unter LC_ALL=C zaehlt ${#s} Bytes: „◆" waere drei, und jede
# rechtsbuendige Angabe stuende um so viele Spalten zu weit links. Reines
# bash ohne Unterprozess — die Funktion laeuft je Login dutzendfach.
_ANSI=$'\033''\[[0-9;]*m'
vb(){ local s="$1"
  while [[ $s =~ $_ANSI ]]; do s="${s/"${BASH_REMATCH[0]}"/}"; done
  s="${s//[$'\200'-$'\277']/}"; VB=${#s}; }
linie(){ # $1 = Zeichen, $2 = Spalten -> LN
  local n="${2:-0}"; [ "$n" -lt 0 ] 2>/dev/null && n=0
  printf -v LN '%*s' "$n" ''; LN="${LN// /$1}"; }
bis(){ # $1 = bisherige Zeile, $2 = Zielspalte -> LN (mindestens ein Leerzeichen)
  vb "$1"; local n=$(( $2 - VB )); [ "$n" -lt 1 ] && n=1; linie " " "$n"; }
# Links und rechts in einer Zeile, rechts buendig auf WIDTH. Passt beides
# nicht, steht das Rechte in einer eigenen Zeile — eine Zeile, die das
# Terminal umbricht, zerreisst den Kopf mehr als eine zusaetzliche.
zwei(){ local l="$1" r="$2" nl
  vb "$l"; nl=$VB; vb "$r"
  if [ $(( nl + VB + 2 )) -le "$WIDTH" ]; then
    linie " " $(( WIDTH - nl - VB )); printf '%s%s%s\n' "$l" "$LN" "$r"
  else
    printf '%s\n' "$l"; linie " " $(( WIDTH - VB )); printf '%s%s\n' "$LN" "$r"
  fi; }
# Der Tafelkopf des Leitstands: Titel links, die Lage rechts IN der Linie, wie
# im Deck. Der Titel laeuft an der Senke durch t(), das Abzeichen kommt fertig.
sect(){ local _ti; _ti="$(t "$1")"; local _ab="${2:-}" _n
  vb "$_ti"; _n=$VB
  if [ -n "$_ab" ]; then
    vb "$_ab"; linie "─" $(( WIDTH - 8 - _n - VB ))
    printf '%s── %s%s%s%s %s%s%s %s %s──%s\n' "$DIM" "$R" "$BR$B" "$_ti" "$R" "$DIM" "$LN" "$R" "$_ab" "$DIM" "$R"
  else
    linie "─" $(( WIDTH - 4 - _n ))
    printf '%s── %s%s%s%s %s%s%s\n' "$DIM" "$R" "$BR$B" "$_ti" "$R" "$DIM" "$LN" "$R"
  fi; }
# Die Lagen des Leitstands (nc/leitstand.LAGEN) — Zeichen UND Farbe, weil
# Farbe allein nichts traegt (16-Farben-Handy, COLOR_MODE=off). Dazu drei fuer
# die Kacheln: „live" (rot wie die Live-Zahl im Deck), „wert" (Leuchtblau) und
# „zweit" (Violett, der Zweitakzent des Decks — fuer den Restream).
lage_an(){ # $1 = Lage -> LF (Farbe), LZ (Zeichen)
  case "$1" in
    fehler) LF="$ERR"; LZ="✘";;  warn) LF="$WRN"; LZ="▲";;
    aktiv)  LF="$BR";  LZ="◉";;  ok)   LF="$OK";  LZ="●";;
    live)   LF="$ERR"; LZ="●";;  wert) LF="$BR";  LZ="●";;
    zweit)  LF="$MAG"; LZ="●";;
    aus)    LF="$FNT"; LZ="○";;  *)    LF="$FNT"; LZ="?";;
  esac; }
abzeichen(){ # $1 = Lage, $2 = Text (fertig uebersetzt) -> AZ
  lage_an "$1"; AZ="${LF}${LZ} ${2}${R}"; }
# Der Grund einer Tafel als Wort. Die Schluessel stehen in nc/leitstand.py;
# ein neuer, den es hier nicht gibt, erscheint roh statt gar nicht.
grundtext(){
  case "$1" in
    ruht) t "ruht";;                     sendet) t "sendet";;
    gestoert) t "gestoert";;             langsam) t "langsam";;
    live) t "live";;                     niemand_live) t "niemand live";;
    discord_getrennt) t "getrennt";;     discord_aus) t "aus";;
    chat_hype) t "Chat-Hype";;           verbunden) t "verbunden";;
    platte_voll) t "Platte voll";;       platte_knapp) t "Platte knapp";;
    ueberlast) t "Ueberlast";;           last_hoch) t "Last hoch";;
    speicher_voll) t "Speicher voll";;   speicher_knapp) t "Speicher knapp";;
    swap_hoch) t "Swap hoch";;           drosselung) t "Drosselung";;
    ruhig) t "ruhig";;                   bruecke) t "Bruecke steht";;
    waechter_fehler) t "Waechter-Fehler";;
    waechter_ueberfaellig) t "Waechter ueberfaellig";;
    lokal_aus) t "lokale KI aus";;       denkt) t "denkt";;
    patrouille) t "patrouilliert";;      wach) t "wach";;
    quote_niedrig) t "Quote niedrig";;   quote) t "Quote";;
    neustart_noetig) t "Neustart noetig";;
    aktuell) t "aktuell";;               keine_server) t "keine Server";;
    webui_fehlt) t "Oberflaeche fehlt";; bereit) t "bereit";;
    nicht_geladen) t "nicht geladen";;
    *:*) printf '%s: %s' "${1%%:*}" "${1#*:}";;   # Betrieb: dienst:grund
    *) printf '%s' "$1";;
  esac; }
kettenname(){
  case "$1" in
    erfassen) t "ERFASSEN";;  live) t "LIVE";;          aufnahme) t "AUFNAHME";;
    kodieren) t "KODIEREN";;  versand) t "VERSAND";;    restream) t "RESTREAM";;
    archiv) t "ARCHIV";;      *) printf '%s' "$1";;
  esac; }
# Die Kennzahl-Kacheln aus dem Kopf des Leitstands. Jede ist KB Spalten breit,
# je Zeile so viele, wie WIDTH traegt; die Unterkante traegt die Lage.
KB=12; KZ_B=""; KZ_W=""; KZ_U=""; KZ_N=0
kachel(){ local _b; _b="$(t "$1")"; local _w="${2:-—}"
  lage_an "${3:-unbekannt}"
  _b="${_b:0:$(( KB - 2 ))}"; _w="${_w:0:$(( KB - 2 ))}"
  vb "$_b"; linie " " $(( KB - VB )); KZ_B="${KZ_B}${FNT}${_b}${R}${LN}"
  vb "$_w"; linie " " $(( KB - VB )); KZ_W="${KZ_W}${LF}${B}${_w}${R}${LN}"
  linie "━" $(( KB - 2 )); KZ_U="${KZ_U}${LF}${LN}${R}  "
  KZ_N=$(( KZ_N + 1 ))
  [ $(( (KZ_N + 1) * KB + 2 )) -gt "$WIDTH" ] && kacheln_aus
  return 0; }
kacheln_aus(){ [ "$KZ_N" -gt 0 ] || return 0
  printf '  %s\n  %s\n  %s\n' "$KZ_B" "$KZ_W" "$KZ_U"
  KZ_B=""; KZ_W=""; KZ_U=""; KZ_N=0; }
# Elemente nebeneinander, mit Trenner, umgebrochen an WIDTH (Lieferkette,
# Kanaele). Je Zeile auf stdin ein fertig gefaerbtes Element.
fluss(){ local _s="$1" _z="" _e
  while IFS= read -r _e; do
    [ -n "$_e" ] || continue
    if [ -z "$_z" ]; then _z="  $_e"; continue; fi
    vb "$_z$_s$_e"
    if [ "$VB" -gt "$WIDTH" ]; then printf '%s\n' "$_z"; _z="  $_e"
    else _z="$_z$_s$_e"; fi
  done
  [ -n "$_z" ] && printf '%s\n' "$_z"
  return 0; }
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
        if (i >= fill) { printf "%s[38;2;34;57;107m▒", esc; continue }
        q = (w > 1) ? (i * 100.0 / (w - 1)) : 0
        # v5.11.1-W210: Leitstand — Gruen 125,242,196 → Bernstein 255,194,90
        # bei 70 % → Rot 255,122,134; leere Zellen im Rasterblau 34,57,107.
        if (q < 70) { r=125+(255-125)*q/70;      g=242+(194-242)*q/70;      b=196+(90-196)*q/70 }
        else        { r=255;                     g=194+(122-194)*(q-70)/30; b=90+(134-90)*(q-70)/30 }
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
gauge(){ printf "  ${DIM}%-6s${R} %b ${FNT}%s${R}\n" "$(t "$1")" "$(bar "$2")" "$3"; }
dot(){ case "$1" in ok) printf "${OK}●${R}";; warn) printf "${WRN}●${R}";;
                    err) printf "${ERR}●${R}";; *) printf "${FNT}●${R}";; esac; }
# Nur die BESCHRIFTUNG laeuft durch t(): das dritte Argument traegt
# Farbcodes und Laufzeitwerte und kann deshalb kein Schluessel sein —
# dort wird an der Quelle uebersetzt.
row(){ printf "  ${DIM}%-11s${R}%b %b\n" "$(t "$1")" "$2" "$3"; }
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
# Das Schema muss zum Dienst passen. Laeuft das Dashboard mit
# DASHBOARD_TLS_CERT/-KEY, spricht es TLS — ein http://-Probe bekommt dann
# NICHTS zurueck, faellt auf den ss-Zweig durch und meldet "Port offen, keine
# Antwort", waehrend das Dashboard in Wahrheit sauber 200er liefert. Genau
# dieser Fehlalarm stand am 10.09. in der MOTD. Deshalb: Schema aus der .env
# bestimmen und im Zweifel BEIDE probieren.
# -k ist hier richtig und keine Nachlaessigkeit: das Zertifikat lautet auf den
# Domainnamen, geprobt wird gegen 127.0.0.1 — die Pruefung MUSS scheitern.
dash_probe(){ # $1=Schema — leere Ausgabe heisst "keine Antwort"
  tmo 2 curl -s -k --max-time 1.5 "$1://127.0.0.1:${DASH_PORT}/healthz" 2>/dev/null
}
if have curl; then
  DASH_SCHEMES="http https"
  if [ -n "$(envget DASHBOARD_TLS_CERT)" ] && [ -n "$(envget DASHBOARD_TLS_KEY)" ]; then
    DASH_SCHEMES="https http"
  fi
  for _sch in $DASH_SCHEMES; do
    DASH_JSON=$(dash_probe "$_sch")
    [ -n "$DASH_JSON" ] && break
  done
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

# ── Leitstand: dieselbe Quelle wie die Uebersicht (v5.11.1-W210) ──
# Antwortet das Deck, kommen Kennzahlen, Lieferkette, Tafeln und Ereignisse
# aus /api/leitstand — EIN Abruf, dieselben Zahlen wie im Browser, und unter
# MariaDB die einzigen, die die MOTD ueberhaupt bekommt. Loopback ohne
# Weiterleitungskopf gilt dem Deck als lokal (nc/clientip, W149): kein Token,
# die MOTD liest dafuer nichts Geheimes aus der .env.
#
# python3 liest das JSON, weil sed an verschachteltem JSON raet. Es reinigt
# jeden Text von Steuerzeichen: Nutzernamen und Ereignistexte kommen von
# aussen, und eine ESC-Folge darin liefe sonst als root ins Terminal. Und es
# kuerzt nach SICHTBARER Breite — ein Emoji in einem Ereignistext ist zwei
# Spalten breit, ein Schnitt nach Bytes zerhackte es.
LS_PY='
import json, re, sys, time, unicodedata
try:
    W = int(sys.argv[1])
except Exception:
    W = 62
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
except Exception:
    sys.exit(0)
if not isinstance(d, dict) or d.get("ok") is not True:
    sys.exit(0)
STEUER = re.compile(r"[\x00-\x1f\x7f-\x9f|]")
def rein(x):
    return STEUER.sub(" ", "" if x is None else str(x)).strip()
def breite(s):
    b = 0
    for c in s:
        if not unicodedata.combining(c):
            b += 2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
    return b
def kurz(x, n):
    s = rein(x)
    if n < 2:
        return ""
    if breite(s) <= n:
        return s
    aus, b = "", 0
    for c in s:
        if b + breite(c) > n - 1:
            break
        aus, b = aus + c, b + breite(c)
    return aus + "…"
def wert(x):
    return "" if x is None else rein(x)
tafeln = [t for t in (d.get("tafeln") or ()) if isinstance(t, dict)]
tab = {t.get("tab"): t for t in tafeln}
for g in d.get("kette") or ():
    if isinstance(g, dict):
        print("K|%s|%s|%s" % (rein(g.get("name")), wert(g.get("wert")), rein(g.get("lage"))))
for t in tafeln:
    da = t.get("daten") or {}
    w = t.get("wert")
    if t.get("tab") in ("system", "insights") and isinstance(w, (int, float)):
        w = "%d%%" % round(w)
    namen, mehr = [], 0
    if t.get("tab") in ("restream", "wall"):
        liste = da.get("spuren") if t.get("tab") == "restream" else da.get("namen")
        namen = [rein(x.get("name")) for x in (liste or ()) if isinstance(x, dict) and x.get("name")]
        mehr = int(da.get("weitere") or 0)
    det = " ".join("@" + n for n in namen[:2])
    rest = max(0, len(namen) - 2) + mehr
    if det and rest:
        det += " +%d" % rest
    ws = wert(w)
    print("T|%s|%s|%s|%s|%s|%s" % (rein(t.get("nr")), rein(t.get("kennung")), rein(t.get("lage")),
                                   rein(t.get("grund")), ws, kurz(det, W - 48 - breite(ws))))
def bekannt(t, x):
    return "" if (t or {}).get("lage", "unbekannt") == "unbekannt" else wert(x)
wall, rs, br = tab.get("wall") or {}, tab.get("restream") or {}, tab.get("brain") or {}
wd = wall.get("daten") or {}
print("Z|%s|%s|%s|%s|%s|%s" % (bekannt(wall, wd.get("live")), wert(wd.get("getrackt")),
      bekannt(wall, wd.get("aufnahme")), bekannt(rs, rs.get("wert")),
      bekannt(br, br.get("wert")), rein(br.get("lage"))))
for e in (d.get("ereignisse") or ())[:3]:
    if not isinstance(e, dict):
        continue
    ts, hm = e.get("ts"), ""
    if isinstance(ts, (int, float)):
        hm = time.strftime("%H:%M", time.localtime(ts))
    else:
        m = re.search(r"(\d{2}:\d{2})", str(ts or ""))
        hm = m.group(1) if m else ""
    art = kurz(e.get("kind"), 22)
    print("E|%s|%s|%s|%s" % (hm, rein(e.get("ton")), art, kurz(e.get("summary"), W - 12 - breite(art))))
'
LS=""; LS_GRUND=""
if [ -z "$DASH_JSON" ]; then LS_GRUND=deck
elif ! have python3; then LS_GRUND=python
else
  LS=$(tmo 4 curl -s -k --max-time 3 "${_sch}://127.0.0.1:${DASH_PORT}/api/leitstand" 2>/dev/null \
       | tmo 3 python3 -I -c "$LS_PY" "$WIDTH" 2>/dev/null)
  [ -z "$LS" ] && LS_GRUND=leer
fi
KETTE=""; TAFELN=""; EREIGNISSE=""; ZAHLEN=""
while IFS= read -r _z; do
  case "$_z" in
    K\|*) KETTE="${KETTE}${_z#K|}"$'\n';;
    T\|*) TAFELN="${TAFELN}${_z#T|}"$'\n';;
    E\|*) EREIGNISSE="${EREIGNISSE}${_z#E|}"$'\n';;
    Z\|*) ZAHLEN="${_z#Z|}";;
  esac
done <<EOF
$LS
EOF

# Ohne Deck die Zahlen aus der Datenbank, streng lesend — wie bis v3.0. Unter
# MariaDB gibt es diesen Rueckweg nicht: die MOTD liest keine Zugangsdaten.
dbq(){ # $1 = SQL, liefert eine Zeile mit |-getrennten Spalten
  if have sqlite3; then tmo 3 sqlite3 -readonly -separator '|' "$DB" "$1" 2>/dev/null
  elif have python3; then tmo 5 python3 -I -c '
import sqlite3, sys
try:
    c = sqlite3.connect("file:" + sys.argv[1] + "?mode=ro", uri=True)
    print("|".join(str(x) for x in c.execute(sys.argv[2]).fetchone()))
except Exception:
    pass' "$DB" "$1" 2>/dev/null
  fi; }
K_LIVE=""; K_TRK=""; K_REC=""; K_RS=""; K_WA=""; K_WAL=""
if [ -n "$ZAHLEN" ]; then
  IFS='|' read -r K_LIVE K_TRK K_REC K_RS K_WA K_WAL <<EOF
$ZAHLEN
EOF
elif [ -n "$DB" ] && [ -f "$DB" ] && { have sqlite3 || have python3; }; then
  case "$DB_BACKEND" in
    mariadb|mysql) ;;
    *)
    # EIN Aufruf statt vier: jeder oeffnet die Datei, sperrt kurz und kostet
    # Zeit — bei jedem Login. restreams gibt es erst ab v37, deshalb der
    # Rueckfall auf die schmale Abfrage.
    STATS=$(dbq "SELECT (SELECT COUNT(*) FROM trackings),
                        (SELECT COUNT(*) FROM trackings WHERE last_live=1),
                        (SELECT COUNT(*) FROM trackings WHERE recording=1),
                        (SELECT COUNT(*) FROM restreams WHERE status='live')")
    [ -z "$STATS" ] && STATS=$(dbq "SELECT (SELECT COUNT(*) FROM trackings),
                        (SELECT COUNT(*) FROM trackings WHERE last_live=1),
                        (SELECT COUNT(*) FROM trackings WHERE recording=1), -1")
    if [ -n "$STATS" ]; then
      IFS='|' read -r K_TRK K_LIVE K_REC K_RS <<EOF
$STATS
EOF
      [ "${K_RS:--1}" -lt 0 ] 2>/dev/null && K_RS=""
    fi;;
  esac
fi
# Eine Kennzahl ohne Wert ist „unbekannt", nie 0 — eine 0 laese sich wie
# „niemand live" (W99: nichts geladen ist nicht dasselbe wie nichts da).
kz_lage(){ # $1 = Wert -> KL
  case "$1" in "") KL=unbekannt;; *) if [ "$1" -gt 0 ] 2>/dev/null; then KL=aktiv; else KL=ok; fi;; esac; }
if [ -z "$KETTE" ]; then
  for _g in "erfassen:$K_TRK" "live:$K_LIVE" "aufnahme:$K_REC" "kodieren:" "versand:" \
            "restream:$K_RS" "archiv:"; do
    _n="${_g%%:*}"; _v="${_g#*:}"; kz_lage "$_v"
    [ "$_n" = erfassen ] && [ "$KL" = aktiv ] && KL=ok
    KETTE="${KETTE}${_n}|${_v}|${KL}"$'\n'
  done
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
[ "$DPCT" -ge 90 ] 2>/dev/null && lage_setz err "Platte fast voll"
[ -n "$THROTTLE" ] && lage_setz warn "Drosselung gemeldet"
# v5.11.1-W210: die Tafeln des Leitstands reden mit — NACH den eigenen
# Befunden, damit die Ursache (Bot steht) die Folge schlaegt.
while IFS='|' read -r _nr _ken _lage _grund _rest; do
  case "$_lage" in
    fehler) lage_setz err  "$_ken: $(grundtext "$_grund")";;
    warn)   lage_setz warn "$_ken: $(grundtext "$_grund")";;
  esac
done <<EOF
$TAFELN
EOF

# ── Kopf ─────────────────────────────────────────────────────
# v5.11.1-W210: der Kopf des Leitstands — Name, Gesamtampel, Sendezustand.
# Die Fassung kam bis hierher aus BUILD_STAMP in bot.py; dort steht seit v5
# `_nc_version.build_stamp()` statt eines Literals, und der sed fand nichts —
# der Kopf war versionslos, dieselbe Falle wie nach W119. Die eine Quelle der
# Fassung ist nc/version.py.
VER="$(envget BUILD_STAMP)"
if [ -z "$VER" ] && [ -f "$BOT_DIR/nc/version.py" ]; then
  VER=$(sed -n 's/^VERSION *= *"\([^"]*\)".*/\1/p' "$BOT_DIR/nc/version.py" | head -1)
  _cn=$(sed -n 's/^CODENAME *= *"\([^"]*\)".*/\1/p' "$BOT_DIR/nc/version.py" | head -1)
  [ -n "$VER" ] && VER="v${VER}${_cn:+ · ${_cn}}"
fi
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

case "$LAGE" in
  ok)   LAGE_BADGE="${OK}●${R} ${OK}$(t "$LAGE_TEXT")${R}";;
  warn) LAGE_BADGE="${WRN}▲${R} ${WRN}$(t "$LAGE_TEXT")${R}";;
  *)    LAGE_BADGE="${ERR}✘${R} ${B}${ERR}$(t "$LAGE_TEXT")${R}";;
esac
# ON AIR wie die Pille oben links im Deck: sendet gerade ein Restream?
if [ "${K_RS:-0}" -gt 0 ] 2>/dev/null; then AIR="${ERR}${B}● ON AIR${R}"
else AIR="${FNT}○ OFF AIR${R}"; fi

printf "\n"; rule
zwei "  ${BR}${B}◆ NIGHTCRAWLER${R} ${DIM}·${R} ${TXT}${B}$(t "LEITSTAND")${R}" "$AIR"
zwei "  $LAGE_BADGE" "${DIM}${VER:-—}${R}${GITREF:+ ${FNT}· ${GITREF}${R}}"
zwei "  ${FNT}$(hostname 2>/dev/null)${R}" "${FNT}$(t "up") ${UP} · $(date +%H:%M)${R}"
rule

# ── Kennzahlen und Lieferkette ───────────────────────────────
# Die Kopfreihe des Decks: was laeuft gerade, in fuenf Zahlen. Live in Rot
# wie im Deck, Restream im Violett des Zweitakzents, der Rest Leuchtblau; ein Waechter mit Befund faerbt seine
# Kachel. Unbekanntes bleibt „—" in Grau.
kz_lage "$K_LIVE"; case "$KL" in aktiv) KL=live;; ok) KL=wert;; esac
kachel "LIVE JETZT" "$K_LIVE" "$KL"
kz_lage "$K_TRK";  [ "$KL" = unbekannt ] || KL=wert
kachel "GETRACKT" "$K_TRK" "$KL"
kz_lage "$K_REC";  [ "$KL" = unbekannt ] || KL=wert
kachel "AUFNAHMEN" "$K_REC" "$KL"
kz_lage "$K_RS";   [ "$KL" = unbekannt ] || KL=zweit
kachel "RESTREAM" "$K_RS" "$KL"
case "$K_WAL" in fehler|warn) KL="$K_WAL";; *) KL=wert;; esac
[ -z "$K_WA" ] && KL=unbekannt
kachel "WAECHTER" "$K_WA" "$KL"
kacheln_aus
# Die Lieferkette einer Sendung, links nach rechts wie im Deck. Jedes Glied
# traegt die Farbe seiner Lage; „—" heisst: diese Stufe kennt nur das Deck.
_kz=""; _i=0
while IFS='|' read -r _n _v _l; do
  [ -n "$_n" ] || continue
  _i=$(( _i + 1 )); lage_an "$_l"
  [ "$_l" = ok ] && LF="$TXT"
  _kz="${_kz}${FNT}0${_i}${R} ${DIM}$(kettenname "$_n")${R} ${LF}${B}${_v:-—}${R}"$'\n'
done <<EOF
$KETTE
EOF
printf '%s' "$_kz" | fluss " ${DIM}▸${R} "

# ── System ───────────────────────────────────────────────────
# Die Lage nach denselben Grenzen wie die Tafel kern.last (nc/leitstand.py:
# Platte 85/95, Speicher 85/95, Swap 80) — hier gemessen und nicht aus dem
# Deck gelesen, damit die Tafel auch steht, wenn das Deck nicht antwortet.
MEMP=$(pct "$MEM_U" "$MEM_T"); SWPP=$(pct "$SWP_U" "$SWP_T")
SYS_LAGE=ok; SYS_GRUND=ruhig
sys_setz(){ case "$1" in
              fehler) [ "$SYS_LAGE" = fehler ] || { SYS_LAGE=fehler; SYS_GRUND="$2"; };;
              warn)   [ "$SYS_LAGE" = ok ] && { SYS_LAGE=warn; SYS_GRUND="$2"; };;
            esac; return 0; }
[ "$DPCT" -ge 95 ] 2>/dev/null && sys_setz fehler platte_voll
[ "$MEMP" -ge 95 ] 2>/dev/null && sys_setz fehler speicher_voll
[ "$DPCT" -ge 85 ] 2>/dev/null && sys_setz warn platte_knapp
[ "$MEMP" -ge 85 ] 2>/dev/null && sys_setz warn speicher_knapp
[ "$SWPP" -ge 80 ] 2>/dev/null && sys_setz warn swap_hoch
[ -n "$THROTTLE" ] && sys_setz warn drosselung
abzeichen "$SYS_LAGE" "$(grundtext "$SYS_GRUND")"
sect "SYSTEM" "$AZ"
gauge "CPU" "$CPU_ALL" "${CPU_ALL}% · ${NPC} $(t "Kerne")"
if [ -n "$CPU_LINES" ]; then
  # Ein Zeichen je Kern: sieht sofort, ob EIN ffmpeg einen Kern festhaelt oder
  # ob wirklich alle unter Last stehen.
  EQ="  ${FNT}$(t "Kerne")  ${R}"
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
  gauge "Disk" "$DPCT" "$(human $((DISK_U*1024)))/$(human $((DISK_T*1024)))  ${DPCT}% · $(human $((DISK_A*1024))) $(t "frei")"
  [ "$DPCT" -ge 90 ] && warn_add "$(t "Platte fast voll") (${DPCT}%) — $(t "Aufnahmen brechen ab"): ${TXT}/cleanup${R}${FNT} $(t "oder alte Dateien loeschen")${R}"
fi
# v4.2-W7: Der Upstream ist bei einer Restream-Box die Zahl, die "laeuft" von
# "sendet wirklich" trennt. Rauf zuerst und hervorgehoben — runter ist bei
# diesem Geraet die Nebensache.
if [ -n "$NET_TX" ]; then
  printf "  ${DIM}%-6s${R} ${TXT}↑ %s/s${R}   ${FNT}↓ %s/s${R}   ${FNT}%s${R}\n" \
    "$(t "Netz")" "$(human "$NET_TX")" "$(human "${NET_RX:-0}")" "$NET_IF"
fi
[ -n "$THROTTLE" ] && warn_add "$(t "Pi meldet Drosselung") (get_throttled=${THROTTLE}) — $(t "Netzteil pruefen, sonst bricht ffmpeg weg")"

# ── Dienst: Bot, Deck, Abwehr, Fehler, Aufnahmen ─────────────
case "$BOT_STATE" in
  gestoppt|tot) abzeichen fehler "$(t "Bot steht")";;
  laeuft|prozess)
    case "$DASH_STATE" in
      gesund)           abzeichen ok     "$(t "laeuft")";;
      degradiert|stumm) abzeichen warn   "$(t "Deck stockt")";;
      *)                abzeichen fehler "$(t "Deck aus")";;
    esac;;
  *) abzeichen unbekannt "$(t "nicht gefunden")";;
esac
sect "DIENST" "$AZ"
if [ -z "$BOT_DIR" ]; then
  row "Installation" "$(dot warn)" "${WRN}$(t "nicht gefunden")${R} ${FNT}— $(t "BOT_DIR in der Konfiguration setzen") (${CONF}, ./motd.sh --doctor)${R}"
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
      warn_add "$(t "Dienst wurde neu gestartet") (${BOT_NRS}x) — $(t "Grund"): ${TXT}journalctl -u ${SERVICE} -p err -n 50${R}"
    fi
    row "Bot" "$(dot ok)" "${TXT}$(t "laeuft")${R} ${FNT}${_extra}${R}";;
  gestoppt)
    row "Bot" "$(dot err)" "${ERR}$(t "gestoppt")${R} ${FNT}${BOT_RES:+(${BOT_RES})}${R}"
    warn_add "$(t "Bot laeuft nicht"): ${TXT}sudo systemctl start ${SERVICE}${R}${FNT} — $(t "Grund"): journalctl -u ${SERVICE} -n 80${R}";;
  prozess)
    row "Bot" "$(dot ok)" "${TXT}$(t "laeuft")${R} ${FNT}($(t "Prozess, kein systemd-Dienst"))${R}";;
  tot)
    row "Bot" "$(dot err)" "${ERR}$(t "kein Prozess")${R} ${FNT}($(t "kein systemd-Dienst gefunden"))${R}";;
esac

case "$DASH_STATE" in
  gesund)
    row "Dashboard" "$(dot ok)" "${TXT}$(t "gesund")${R} ${FNT}:${DASH_PORT}${DASH_PROCS:+ · ${DASH_PROCS} $(t "Kindprozesse")}${R}";;
  degradiert)
    row "Dashboard" "$(dot warn)" "${WRN}$(t "degradiert")${R} ${FNT}:${DASH_PORT} — $(t "/healthz meldet ok=false")${R}"
    warn_add "$(t "Dashboard degradiert (DB oder Dauerschleifen)"): ${TXT}curl -s localhost:${DASH_PORT}/api/selftest${R}";;
  stumm)
    row "Dashboard" "$(dot warn)" "${WRN}$(t "Port offen, keine Antwort")${R} ${FNT}:${DASH_PORT}${R}";;
  *)
    row "Dashboard" "$(dot err)" "${ERR}$(t "kein Listener")${R} ${FNT}:${DASH_PORT}${R}";;
esac
[ -n "$DASH_ZOMB" ] && [ "$DASH_ZOMB" -gt 0 ] 2>/dev/null && \
  warn_add "${DASH_ZOMB} $(t "Zombie-Kindprozesse — ffmpeg/streamlink werden nicht abgeraeumt")"

if have systemctl && systemctl list-unit-files --no-legend 'crowdsec.service' 2>/dev/null | grep -q .; then
  if systemctl is-active --quiet crowdsec 2>/dev/null; then
    CS=$(command -v cscli 2>/dev/null || echo /usr/bin/cscli)
    BANS=""
    [ -x "$CS" ] && BANS=$(tmo 3 "$CS" decisions list -o raw 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    row "CrowdSec" "$(dot ok)" "${TXT}$(t "aktiv")${R} ${FNT}${BANS:+· ${BANS} Bans}${R}"
  else
    row "CrowdSec" "$(dot err)" "${ERR}$(t "inaktiv")${R} ${FNT}— $(t "Abwehr blind")${R}"
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
  if   [ "$ETODAY" -eq 0 ] 2>/dev/null; then row "Fehler" "$(dot ok)"   "${TXT}0${R} ${FNT}$(t "heute")${R}${ESPARK}"
  elif [ "$ETODAY" -lt 5 ] 2>/dev/null; then row "Fehler" "$(dot warn)" "${WRN}${ETODAY}${R} ${FNT}$(t "heute")${ELAST}${R}${ESPARK}"
  else row "Fehler" "$(dot err)" "${ERR}${ETODAY}${R} ${FNT}$(t "heute")${ELAST}${R}${ESPARK}"
       warn_add "${ETODAY} $(t "Fehler heute"): ${TXT}tail -n 40 ${LOGF}${R}"
  fi
fi
# Aufnahmen: der Bestand auf der Platte (zwischengespeichert) und die
# laufenden ffmpeg. Genau die Luecke jagt der recording-Sentinel: die Zahlen
# sagen „nimmt auf", es laeuft aber kein einziges ffmpeg.
FFN=$(tmo 2 pgrep -c ffmpeg 2>/dev/null | tr -d ' '); FFN=${FFN:-0}
if [ "${K_REC:-0}" -gt 0 ] 2>/dev/null && [ "$FFN" -eq 0 ] 2>/dev/null; then
  warn_add "$(t "DB meldet Aufnahmen, es laeuft aber KEIN ffmpeg — Karteileichen") (${K_REC}): ${TXT}/recstatus${R}"
fi
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
  _rz="${TXT}${RC:-0}${R} ${FNT}$(t "Dateien")"
  [ -n "${RKB:-}" ] && _rz="${_rz} · $(human $(( ${RKB:-0} * 1024 ))) $(t "gesamt")"
  [ -n "${RNEW:-}" ] && _rz="${_rz} · $(tf "neuste vor %s" "$(ago "$RNEW")")"
  row "Aufnahmen" "$(dot "$(onoff "$FFN")")" "${_rz} · ${FFN} ffmpeg${R}"
fi

# ── Die neun Tafeln des Leitstands ───────────────────────────
if [ -n "$TAFELN" ]; then
  _tf=0; _tw=0
  while IFS='|' read -r _nr _ken _lage _rest; do
    case "$_lage" in fehler) _tf=$(( _tf + 1 ));; warn) _tw=$(( _tw + 1 ));; esac
  done <<EOF
$TAFELN
EOF
  if   [ "$_tf" -gt 0 ]; then abzeichen fehler "$(tf "%s Stoerung(en)" "$_tf")"
  elif [ "$_tw" -gt 0 ]; then abzeichen warn   "$(tf "%s Warnung(en)" "$_tw")"
  else abzeichen ok "$(t "ruhig")"; fi
  sect "TAFELN" "$AZ"
  # Spalten: Nummer und Kennung wie im Deck (die Kennung ist der Code-Titel
  # der Tafel und bleibt unuebersetzt), Lage mit Grund, Wert, Namen.
  while IFS='|' read -r _nr _ken _lage _grund _wert _det; do
    [ -n "$_ken" ] || continue
    lage_an "$_lage"
    _l="  ${FNT}${_nr}${R} ${TXT}${_ken}${R}"
    bis "$_l" 24; _l="${_l}${LN}${LF}${LZ} $(grundtext "$_grund")${R}"
    if [ -n "$_wert" ]; then bis "$_l" 46; _l="${_l}${LN}${TXT}${B}${_wert}${R}"; fi
    [ -n "$_det" ] && _l="${_l}  ${FNT}${_det}${R}"
    printf '%s\n' "$_l"
  done <<EOF
$TAFELN
EOF
else
  # Nichts geladen ist nicht dasselbe wie nichts da (W99) — und WARUM nichts
  # geladen wurde, entscheidet, was zu tun ist.
  abzeichen unbekannt "$(t "nicht geladen")"
  sect "TAFELN" "$AZ"
  case "$LS_GRUND" in
    deck)   row "Quelle" "$(dot faint)" "${FNT}$(t "Deck antwortet nicht — die Tafeln kommen von /api/leitstand")${R}";;
    python) row "Quelle" "$(dot faint)" "${FNT}$(t "python3 fehlt — es liest die Tafeln aus /api/leitstand")${R}";;
    *)      row "Quelle" "$(dot warn)" "${WRN}$(t "das Deck lieferte keine Tafeln (Fassung vor 5.10?)")${R}";;
  esac
  case "$DB_BACKEND" in
    mariadb|mysql) row "Datenbank" "$(dot faint)" "${FNT}MariaDB — $(t "ohne Deck keine Zahlen")${R}";;
    *) [ -n "$K_TRK" ] && row "Datenbank" "$(dot faint)" "${FNT}$(t "Zahlen oben aus der Datenbank gelesen")${R}";;
  esac
fi

# ── Ereignisstrom ────────────────────────────────────────────
# Die letzten drei Ereignisse — was zuletzt passiert ist, ohne das Deck
# aufzumachen. Nur mit Deck: das Ereignisprotokoll liest die MOTD nicht selbst.
if [ -n "$EREIGNISSE" ]; then
  sect "EREIGNISSE"
  while IFS='|' read -r _hm _ton _art _sum; do
    [ -n "$_art" ] || continue
    case "$_ton" in
      fehler) lage_an fehler;;  warn) lage_an warn;;  gut) lage_an ok;;
      *) LF="$FNT"; LZ="·";;
    esac
    printf '%s\n' "  ${FNT}${_hm:-—}${R} ${LF}${LZ}${R} ${DIM}${_art}${R}  ${TXT}${_sum}${R}"
  done <<EOF
$EREIGNISSE
EOF
fi

# ── Kanaele: Restream-Ziele und Bots (aus der .env) ──────────
if [ -f "$ENVF" ]; then
  truthy(){ case "$(printf '%s' "${1:-}" | tr 'A-Z' 'a-z')" in
              1|true|yes|on|y) return 0;; *) return 1;; esac; }
  chip(){ case "$2" in
            on)   printf "${OK}▣ %s${R}" "$1";;
            halb) printf "${WRN}▨ %s${R}" "$1";;   # eingeschaltet, aber unvollstaendig
            *)    printf "${FNT}▢ %s${R}" "$1";;
          esac; }
  # Die Vorfassung nahm JEDEN Schluessel, der das Stichwort enthielt. Ein
  # gesetztes KICK_INGEST_URL machte Kick gruen, obwohl KICK_ENABLED=0 war.
  # Reihenfolge jetzt: ausdrueckliches ENABLED schlaegt alles, danach zaehlt
  # nur ein echter Stream-Key.
  plat(){ # $1=Praefix  $2=Schluesselvariable
    local en key
    en="$(envget "${1}_ENABLED")"; key="$(envget "$2")"
    if [ -n "$en" ] && ! truthy "$en"; then echo off; return; fi
    if [ -n "$key" ]; then echo on; else echo halb; fi
  }
  _tg=off; [ -n "$(envget BOT_TOKEN)" ] && _tg=on
  _dc=off; [ -n "$(envget DISCORD_BOT_TOKEN)" ] && _dc=on
  _ai=halb   # keylos laeuft AZRAEL immer (nc/freeai), mit Key nur besser
  for k in ANTHROPIC_API_KEY OPENAI_API_KEY POLLINATIONS_API_KEY LLM7_TOKEN; do
    [ -n "$(envget "$k")" ] && { _ai=on; break; }
  done
  sect "KANAELE" "${FNT}$(t "▣ bereit · ▨ ohne Key · ▢ aus")${R}"
  printf '%s\n' "$(chip Kick "$(plat KICK KICK_STREAM_KEY)")" \
                "$(chip Twitch "$(plat TWITCH TWITCH_STREAM_KEY)")" \
                "$(chip YouTube "$(plat YOUTUBE YOUTUBE_STREAM_KEY)")" \
                "$(chip Telegram "$_tg")" "$(chip Discord "$_dc")" "$(chip AZRAEL "$_ai")" \
    | fluss "  "
  [ "$_tg" = off ] && warn_add "$(t "BOT_TOKEN fehlt in der .env — ohne ihn startet der Telegram-Teil nicht")"
elif [ -n "$BOT_DIR" ]; then
  sect "KANAELE"
  row ".env" "$(dot err)" "${ERR}$(t "fehlt")${R} ${FNT}— cp .env.example .env && chmod 600 .env${R}"
fi

# ── Doppelte Anzeige und veraltete Kopie (v5.11.1-W210) ──────
# Beides sieht man nur hier: wer die MOTD zweimal sieht, sieht auch diesen
# Hinweis — und die Abhilfe dazu.
if [ -d /etc/update-motd.d ]; then
  _dop="$(doppelt_befunde | head -1)"
  if [ -n "$_dop" ]; then
    warn_add "$(t "Statusbild erscheint doppelt"): $(doppelt_text "${_dop%%|*}") ${FNT}(${_dop#*|})${R} — ${TXT}$(doppelt_abhilfe "${_dop%%|*}" "${_dop#*|}")${R}"
  fi
fi
# Die installierte Kopie unter /etc/update-motd.d ist ein SCHNAPPSCHUSS: die
# Update-Funktion schreibt tools/motd.sh, erreicht diese Kopie aber nie. Dass
# sie den Bestand nicht einfach AUSFUEHRT, ist Absicht — eine Datei, die der
# Bot-Nutzer schreiben darf, bei jedem Login als root zu starten, waere ein
# Weg vom Bot zu root. Also sagt sie, dass sie alt ist.
if [ -n "$BOT_DIR" ] && [ -r "$BOT_DIR/tools/motd.sh" ]; then
  _bv=$(sed -n 's/^NC_MOTD_VERSION="\([^"]*\)".*/\1/p' "$BOT_DIR/tools/motd.sh" | head -1)
  if [ -n "$_bv" ] && [ "$_bv" != "$NC_MOTD_VERSION" ]; then
    warn_add "$(tf "Statusbild veraltet (installiert %s, im Bestand %s)" "$NC_MOTD_VERSION" "$_bv"): ${TXT}sudo $BOT_DIR/tools/motd.sh --install${R}"
  fi
fi

# ── Hinweise ─────────────────────────────────────────────────
# Nur was WIRKLICH ansteht. Eine MOTD, die immer denselben Absatz zeigt, wird
# nach drei Tagen nicht mehr gelesen — dann faellt auch der echte Befund durch.
if [ -n "$WARN_LINES" ]; then
  abzeichen warn "$(printf '%s' "$WARN_LINES" | grep -c .)"
  sect "HINWEISE" "$AZ"
  printf '%s' "$WARN_LINES" | while IFS= read -r l; do
    [ -n "$l" ] && printf "  ${WRN}▲${R} %b\n" "$l"
  done
fi
rule
printf "\n"
exit 0
