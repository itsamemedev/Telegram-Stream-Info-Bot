#!/usr/bin/env bash
#
# NIGHTCRAWLER — Prometheus und Grafana einrichten (v4.2-W127)
#
#     sudo bash tools/observability.sh             gefuehrt
#     sudo bash tools/observability.sh --check     nur pruefen; Exit 1, wenn etwas fehlt
#     bash tools/observability.sh --dry-run        zeigen, was liefe — nichts ausfuehren
#     sudo bash tools/observability.sh --remove    eigene Dienste und Dateien entfernen
#     bash tools/observability.sh --help           alle Schalter
#
# WARUM ES DAS GIBT
# Der Bot liefert seit W122 alle Kennzahlen unter /metrics — gelesen hat sie
# niemand. "Wie lief es heute Nacht?" hatte als Antwort nur die Lagezeile im
# Journal, und einen Alarm, der jemanden weckt, gab es fuer keinen der
# Zustaende, die das Deck kennt (Loop haengt, Deskriptoren voll, Neustart im
# Kreis).
#
# WAS ES TUT, UND WAS NICHT
#   * Prometheus als EIGENER Dienst (nightcrawler-prometheus), nur auf
#     127.0.0.1. Der Dienst des Pakets lauscht ab Werk auf *:9090 ohne
#     Anmeldung; hat ERST dieser Lauf das Paket gebracht, wird er wieder
#     abgeschaltet. Lief er schon vorher, bleibt er unangetastet — dann gehoert
#     er jemandem.
#   * Grafana nur, wenn gewollt (--grafana). Auf Debian/Ubuntu liegt es nicht in
#     den Paketquellen; die offizielle Quelle wird nur mit --grafana-repo oder
#     nach ausdruecklicher Rueckfrage eingetragen. Grafana lauscht danach nur
#     auf 127.0.0.1 (Drop-in), Zugang per SSH-Tunnel.
#   * Geschrieben wird nur, was sich unterscheidet; ein zweiter Lauf auf einem
#     fertigen Bestand fasst nichts an und startet nichts neu.
#   * Prometheus braucht keinen DASHBOARD_TOKEN: er fragt 127.0.0.1, und das
#     Deck laesst Loopback ohne Anmeldung durch. Kein Geheimnis wird kopiert.
#   * Die .env, die Datenbank und der Bot-Dienst werden nie angefasst.
#
# EXITCODES — dieselbe Trennung wie update.sh:
#   0  eingerichtet bzw. vollstaendig
#   1  es fehlt etwas (nach --check) oder ein Schritt ist gescheitert
#   2  Aufruf- oder Umgebungsfehler (kein systemd, unbekannter Schalter)

set -uo pipefail

NC_OBS_VERSION="1.0"
SKRIPT="$(cd "$(dirname "$0")" && pwd)"

# shellcheck source=lib/i18n.sh
. "$SKRIPT/lib/i18n.sh"
# shellcheck source=lib/ausgabe.sh
. "$SKRIPT/lib/ausgabe.sh"
# shellcheck source=lib/system.sh
. "$SKRIPT/lib/system.sh"

have(){ command -v "$1" >/dev/null 2>&1; }

# ── Schalter ─────────────────────────────────────────────────
NC_MODUS="gefuehrt"
NUR_PRUEFEN=0; TROCKEN=0; ENTFERNEN=0
GRAFANA="frage"          # frage | ja | nein
GRAFANA_QUELLE=0         # 1 = offizielle Grafana-Paketquelle eintragen duerfen
PROM_PORT=9099
AUFBEWAHRUNG="30d"
ZIEL="$(cd "$SKRIPT/.." && pwd)"
# Fuer die Vertraege: alle Zielpfade unter einer anderen Wurzel. Auf einem
# Server bleibt das leer.
W="${NC_OBS_WURZEL:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --express)        NC_MODUS="express";;
    --unattended|-y)  NC_MODUS="unattended";;
    --check)          NUR_PRUEFEN=1;;
    --dry-run)        TROCKEN=1;;
    --remove)         ENTFERNEN=1;;
    --grafana)        GRAFANA="ja";;
    --no-grafana)     GRAFANA="nein";;
    --grafana-repo)   GRAFANA="ja"; GRAFANA_QUELLE=1;;
    --port)           PROM_PORT="${2:-}"; shift;;
    --port=*)         PROM_PORT="${1#*=}";;
    --retention)      AUFBEWAHRUNG="${2:-}"; shift;;
    --retention=*)    AUFBEWAHRUNG="${1#*=}";;
    --dir)            ZIEL="${2:-}"; shift;;
    --dir=*)          ZIEL="${1#*=}";;
    --no-color)       export NC_FARBE=0; nc_farben;;
    --version)        printf 'NIGHTCRAWLER observability %s\n' "$NC_OBS_VERSION"; exit 0;;
    --help|-h)
      tz <<'HILFE'
NIGHTCRAWLER — Prometheus und Grafana einrichten

  sudo bash tools/observability.sh [Schalter]

Was:
  (ohne)           Prometheus einrichten; nach Grafana wird gefragt
  --grafana        Grafana mit einrichten (Datenquelle, Dashboard, nur lokal)
  --grafana-repo   wie --grafana, und die offizielle Grafana-Paketquelle eintragen
  --no-grafana     Grafana nicht anfassen
  --remove         eigene Dienste und Dateien entfernen (Pakete bleiben)

Wie:
  --check          nur pruefen und berichten; Exitcode 1, wenn etwas fehlt
  --dry-run        die Schritte zeigen, die liefen — nichts ausfuehren
  --express        eine Rueckfrage fuer den ganzen Plan
  --unattended,-y  keine Rueckfragen
  --port <N>       Port von Prometheus auf 127.0.0.1 (Vorgabe 9099)
  --retention <D>  wie lange Prometheus Daten haelt (Vorgabe 30d)
  --dir <Pfad>     Installation des Bots (Vorgabe: der Ordner ueber tools/)
  --no-color       ohne Farben

Zugang: ssh -L 3001:127.0.0.1:3000 -L 9099:127.0.0.1:9099 server
Exitcodes: 0 eingerichtet · 1 es fehlt etwas · 2 Aufruffehler
HILFE
      exit 0;;
    *) fehler "Unbekannter Schalter: %s  (--help)" "$1"; exit 2;;
  esac
  shift
done
[ -z "$NC_TTY" ] && [ "$NC_MODUS" != "unattended" ] && NC_MODUS="unattended"

# Eingaben pruefen, BEVOR sie in eine Unit oder Konfiguration wandern.
case "$PROM_PORT" in ''|*[!0-9]*) fehler "Port ist keine Zahl: %s" "$PROM_PORT"; exit 2;; esac
if [ "$((10#$PROM_PORT))" -lt 1024 ] || [ "$((10#$PROM_PORT))" -gt 65535 ]; then
  fehler "Port ausserhalb von 1024 bis 65535: %s" "$PROM_PORT"; exit 2
fi
case "$AUFBEWAHRUNG" in
  [0-9]*[smhdwy]) case "${AUFBEWAHRUNG%?}" in *[!0-9]*) fehler "Aufbewahrung ungueltig: %s (z. B. 30d)" "$AUFBEWAHRUNG"; exit 2;; esac;;
  *) fehler "Aufbewahrung ungueltig: %s (z. B. 30d)" "$AUFBEWAHRUNG"; exit 2;;
esac
[ -d "$ZIEL" ] || { fehler "Verzeichnis gibt es nicht: %s" "$ZIEL"; exit 2; }
ZIEL="$(cd "$ZIEL" && pwd)"
VORLAGEN="$ZIEL/deploy/observability"
[ -d "$VORLAGEN" ] || { fehler "Vorlagen fehlen: %s" "$VORLAGEN"; exit 2; }

nc_system_erkennen
nc_init_erkennen
if [ "$NC_INIT" != "systemd" ]; then
  # Ehrlich statt halb: ohne systemd gibt es hier keinen Dienst, der Prometheus
  # nach einem Neustart wieder hochholt — und ein Monitoring, das nach dem
  # ersten Reboot fehlt, meldet genau dann nichts, wenn es zaehlt.
  fehler "Ohne systemd richtet dieses Werkzeug nichts ein (gefunden: %s)." "$NC_INIT"
  erklaere "Prometheus laesst sich trotzdem betreiben: die Vorlagen in deploy/observability/ sind gewoehnliche Dateien, die @@…@@-Stellen von Hand einsetzen."
  exit 2
fi

# ── Zielpfade ────────────────────────────────────────────────
ETC="$W/etc/nightcrawler/observability"
REGELN="$ETC/rules"
UNIT="$W/etc/systemd/system/nightcrawler-prometheus.service"
GF_PROV="$W/etc/grafana/provisioning"
GF_DASH="$W/var/lib/grafana/dashboards/nightcrawler"
GF_DROPIN="$W/etc/systemd/system/grafana-server.service.d/nightcrawler.conf"

SUDO=""
if [ -n "${NC_OBS_SUDO+gesetzt}" ]; then
  # Fuer die Vertraege, wie NC_OBS_WURZEL: sudo setzt den PATH zurueck
  # (secure_path) und landete beim ECHTEN systemctl statt bei der Attrappe —
  # so geschehen in der CI, die nicht als root laeuft.
  SUDO="$NC_OBS_SUDO"
elif [ "$(id -u)" -ne 0 ]; then
  if have sudo; then SUDO="sudo"; else SUDO="-"; fi
fi

# ── Werte aus der Installation ───────────────────────────────
ENVF="$ZIEL/.env"
env_wert(){ # letzter unkommentierter Wert, ohne Anfuehrungszeichen
  [ -f "$ENVF" ] || return 0
  awk -F= -v k="$1" '/^[[:space:]]*#/{next} {g=$1; gsub(/[[:space:]]/,"",g)}
    g==k {v=substr($0, index($0,"=")+1); sub(/[[:space:]]+#.*$/,"",v);
          gsub(/^[[:space:]"'"'"']+|[[:space:]"'"'"']+$/,"",v); w=v} END{if(w!="")print w}' "$ENVF"
}
DASH_PORT="$(env_wert DASHBOARD_PORT)"; DASH_PORT="${DASH_PORT:-8050}"
case "$DASH_PORT" in ''|*[!0-9]*) fehler "DASHBOARD_PORT in der .env ist keine Zahl: %s" "$DASH_PORT"; exit 2;; esac
SCHEMA="http"; [ -n "$(env_wert DASHBOARD_TLS_CERT)" ] && SCHEMA="https"
WEB_HOST="$(env_wert WEB_HOST)"
case "${WEB_HOST:-127.0.0.1}" in
  127.*|localhost|0.0.0.0|::|"[::]"|::1) ;;
  *)
    # Bindet das Deck an EINE fremde Adresse, ist 127.0.0.1 nicht erreichbar
    # — und von dort kaeme die Abfrage ohne Anmeldung. Statt den Token in eine
    # zweite Datei zu kopieren: sagen, was zu aendern ist.
    fehler "WEB_HOST=%s — das Deck ist auf 127.0.0.1 nicht erreichbar." "$WEB_HOST"
    erklaere "Prometheus fragt 127.0.0.1 ohne Anmeldung ab. Mit WEB_HOST=0.0.0.0 (alle Adressen, inklusive 127.0.0.1) oder 127.0.0.1 in der .env geht es — danach den Bot neu starten."
    exit 2;;
esac

# ── Helfer ───────────────────────────────────────────────────
lauf(){
  if [ "$TROCKEN" = 1 ]; then printf '    %s$%s %s\n' "$FNT" "$R" "$*"; return 0; fi
  printf '    %s$ %s%s\n' "$FNT" "$*" "$R"
  if [ -n "$SUDO" ] && [ "$SUDO" != "-" ]; then sudo "$@"; else "$@"; fi
}
dienst(){ # systemctl, gezeigt und — ausser im Trockenlauf — ausgefuehrt
  lauf systemctl "$@"
}

# rendern VORLAGE -> stdout. Unbekannte Platzhalter brechen ab: ein @@X@@, das
# in eine Unit wandert, macht daraus einen Befehl, den es nicht gibt.
rendern(){
  sed -e "s#@@DASH_PORT@@#$DASH_PORT#g" -e "s#@@SCHEMA@@#$SCHEMA#g" \
      -e "s#@@PROM_PORT@@#$PROM_PORT#g" -e "s#@@AUFBEWAHRUNG@@#$AUFBEWAHRUNG#g" \
      -e "s#@@PROMETHEUS@@#$PROM_BIN#g" -e "s#@@ETC@@#${ETC#"$W"}#g" \
      -e "s#@@REGELN@@#${REGELN#"$W"}#g" -e "s#@@DASHBOARDS@@#${GF_DASH#"$W"}#g" "$1"
}

GEAENDERT=""             # Liste der Ziele, die dieser Lauf geschrieben hat
# schreibe ZIEL VORLAGE [modus] — nur bei Abweichung; zeigt, was sich aendert.
schreibe(){
  local ziel="$1" vorlage="$2" modus="${3:-644}" neu
  neu="$(mktemp)" || return 1
  rendern "$vorlage" > "$neu"
  if grep -q '@@[A-Z_]*@@' "$neu"; then
    fehler "Unbekannter Platzhalter in %s: %s" "$vorlage" "$(grep -o '@@[A-Z_]*@@' "$neu" | head -1)"
    rm -f "$neu"; return 1
  fi
  if [ -f "$ziel" ] && cmp -s "$neu" "$ziel"; then
    rm -f "$neu"; return 0
  fi
  if [ -f "$ziel" ]; then
    info "geaendert: %s" "${ziel#"$W"}"
    diff -u "$ziel" "$neu" | sed -n '3,$p' | head -20 | sed 's/^/      /'
  else
    info "neu: %s" "${ziel#"$W"}"
  fi
  GEAENDERT="$GEAENDERT ${ziel#"$W"}"
  # Im Trockenlauf zeigt lauf() die Befehle nur — EIN Riegel fuer alles.
  lauf mkdir -p "$(dirname "$ziel")" || { rm -f "$neu"; return 1; }
  lauf install -m "$modus" "$neu" "$ziel" || { rm -f "$neu"; return 1; }
  rm -f "$neu"
}
geaendert(){ case " $GEAENDERT " in *" ${1#"$W"} "*) return 0;; esac; return 1; }

unit_da(){ systemctl list-unit-files --no-legend "$1" 2>/dev/null | grep -q .; }
unit_aktiv(){ systemctl is-active --quiet "$1" 2>/dev/null; }

# ═══════════════════════════════════════════════════════════════════════════
if [ "$ENTFERNEN" = 1 ]; then
  kopf "Entfernen"
  erklaere "Entfernt werden nur die Dateien und Dienste dieses Werkzeugs. Die Pakete prometheus und grafana bleiben installiert, die gesammelten Daten unter /var/lib/nightcrawler-prometheus ebenfalls (systemd raeumt sie mit dem Dienst nicht weg)."
  # Entschieden an der EIGENEN Unit-Datei, nicht an systemctl list-unit-files:
  # die Datei ist das, was dieses Werkzeug angelegt hat und hier wegnimmt.
  [ -f "$UNIT" ] && dienst disable --now nightcrawler-prometheus.service
  _gf=0
  for f in "$GF_DROPIN" "$W/etc/systemd/system/grafana.service.d/nightcrawler.conf" \
           "$GF_PROV/datasources/nightcrawler.yml" \
           "$GF_PROV/dashboards/nightcrawler.yml" "$GF_DASH/nightcrawler.json"; do
    [ -e "$f" ] && { lauf rm -f "$f"; _gf=1; }
  done
  for f in "$UNIT" "$REGELN/nightcrawler.yml" "$ETC/prometheus.yml"; do
    [ -e "$f" ] && lauf rm -f "$f"
  done
  dienst daemon-reload
  # Grafana nur neu starten, wenn ihm hier etwas weggenommen wurde — sonst
  # stoesst --remove einen Dienst an, der mit NIGHTCRAWLER nichts zu tun hat.
  if [ "$_gf" = 1 ]; then
    for u in grafana-server.service grafana.service; do
      if unit_aktiv "$u"; then dienst restart "$u"; fi
    done
  fi
  gut "Entfernt."
  exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Bestand"
PROM_BIN="$(command -v prometheus || true)"
PROMTOOL="$(command -v promtool || true)"
PROM_PAKET="$(nc_paketname prometheus)"
PAKET_DIENST_VORHER=0; unit_da prometheus.service && PAKET_DIENST_VORHER=1
if [ -n "$PROM_BIN" ]; then gut "prometheus: %s" "$PROM_BIN"
elif [ -n "$PROM_PAKET" ]; then info "prometheus fehlt — Paket: %s" "$PROM_PAKET"
else warn "prometheus fehlt, und fuer %s ist kein Paket bekannt." "${NC_PKG:-?}"; fi
info "Bot-Dashboard: %s://127.0.0.1:%s/metrics" "$SCHEMA" "$DASH_PORT"

GF_DA=0; GF_DIENST=""
for u in grafana-server.service grafana.service; do
  if unit_da "$u"; then GF_DA=1; GF_DIENST="$u"; break; fi
done
[ "$GF_DA" = 1 ] && gut "grafana: %s" "$GF_DIENST" || info "grafana: nicht installiert"

if [ "$GRAFANA" = "frage" ]; then
  if [ "$NC_MODUS" = "unattended" ]; then
    # Unbeaufsichtigt nur, was schon da ist: eine Paketquelle einzutragen ist
    # keine Entscheidung, die ein Skript nebenbei trifft.
    [ "$GF_DA" = 1 ] && GRAFANA="ja" || GRAFANA="nein"
  elif frage_ja "Grafana mit einrichten (Diagramme im Browser)?" J; then GRAFANA="ja"
  else GRAFANA="nein"; fi
fi

# ── --check ──────────────────────────────────────────────────
if [ "$NUR_PRUEFEN" = 1 ]; then
  BEFUND=0
  [ -n "$PROM_BIN" ] || { warn "prometheus ist nicht installiert."; BEFUND=1; }
  for f in "$ETC/prometheus.yml" "$REGELN/nightcrawler.yml" "$UNIT"; do
    [ -f "$f" ] || { warn "fehlt: %s" "${f#"$W"}"; BEFUND=1; }
  done
  if unit_aktiv nightcrawler-prometheus.service; then gut "nightcrawler-prometheus laeuft."
  else warn "nightcrawler-prometheus laeuft nicht."; BEFUND=1; fi
  if [ "$GRAFANA" = "ja" ]; then
    [ "$GF_DA" = 1 ] || { warn "grafana ist nicht installiert."; BEFUND=1; }
    for f in "$GF_PROV/datasources/nightcrawler.yml" "$GF_DASH/nightcrawler.json"; do
      [ -f "$f" ] || { warn "fehlt: %s" "${f#"$W"}"; BEFUND=1; }
    done
  fi
  [ "$BEFUND" = 0 ] && gut "Vollstaendig." || warn "Unvollstaendig — ohne --check wird es eingerichtet."
  exit "$BEFUND"
fi

if [ "$SUDO" = "-" ] && [ "$TROCKEN" = 0 ]; then
  fehler "Weder root noch sudo — Dienste lassen sich so nicht einrichten."
  exit 2
fi
if [ "$NC_MODUS" = "express" ] && [ "$TROCKEN" = 0 ]; then
  if [ "$GRAFANA" = "ja" ]; then _f="Prometheus und Grafana einrichten?"; else _f="Prometheus einrichten?"; fi
  frage_ja "$_f" J || { info "Abgebrochen — nichts veraendert."; exit 1; }
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Prometheus"
BEFUND=0
PROM_NEU=0               # 1 = DIESER Lauf hat das Paket installiert
if [ -z "$PROM_BIN" ]; then
  if [ -z "$PROM_PAKET" ]; then
    fehler "Prometheus bitte selbst installieren (https://prometheus.io/download/), dann erneut aufrufen."
    exit 1
  fi
  if [ "$NC_MODUS" = "gefuehrt" ] && [ "$TROCKEN" = 0 ] && ! frage_ja "Paket jetzt installieren?" J; then
    info "Abgebrochen — nichts veraendert."; exit 1
  fi
  if _af="$(nc_auffrischbefehl)"; then
    # shellcheck disable=SC2086  # feste Woerter aus lib/system.sh
    lauf $_af || warn "Paketquellen liessen sich nicht auffrischen — versuche es trotzdem."
  fi
  # shellcheck disable=SC2046,SC2086
  lauf env DEBIAN_FRONTEND=noninteractive $(nc_installbefehl $PROM_PAKET) || { fehler "Installation gescheitert."; exit 1; }
  PROM_NEU=1
  PROM_BIN="$(command -v prometheus || true)"
  PROMTOOL="$(command -v promtool || true)"
  # Im Trockenlauf gibt es das Programm noch nicht — der Pfad des Pakets.
  [ -z "$PROM_BIN" ] && [ "$TROCKEN" = 1 ] && PROM_BIN="/usr/bin/prometheus"
  [ -n "$PROM_BIN" ] || { fehler "prometheus nach der Installation nicht gefunden."; exit 1; }
fi

schreibe "$ETC/prometheus.yml" "$VORLAGEN/prometheus.yml" || exit 1
schreibe "$REGELN/nightcrawler.yml" "$VORLAGEN/rules/nightcrawler.yml" || exit 1
schreibe "$UNIT" "$VORLAGEN/systemd/nightcrawler-prometheus.service" || exit 1

# promtool VOR dem Start: eine Konfiguration, die Prometheus ablehnt, liesse
# den Dienst mit Restart=on-failure im Kreis laufen — der W100-Befund, eine
# Schicht weiter. Ohne promtool wird es gesagt, nicht uebersprungen.
if [ "$TROCKEN" = 0 ]; then
  if [ -n "$PROMTOOL" ]; then
    if ! "$PROMTOOL" check config "$ETC/prometheus.yml" >/dev/null 2>&1 \
       || ! "$PROMTOOL" check rules "$REGELN/nightcrawler.yml" >/dev/null 2>&1; then
      fehler "promtool lehnt die Konfiguration ab — Dienst wird nicht (neu) gestartet:"
      "$PROMTOOL" check config "$ETC/prometheus.yml" 2>&1 | sed 's/^/      /' | tail -8
      exit 1
    fi
    gut "promtool: Konfiguration und Regeln gueltig."
  else
    warn "promtool fehlt — Konfiguration ungeprueft."
  fi
fi

geaendert "$UNIT" && dienst daemon-reload
if ! unit_aktiv nightcrawler-prometheus.service; then
  dienst enable --now nightcrawler-prometheus.service || BEFUND=1
elif geaendert "$UNIT"; then
  dienst restart nightcrawler-prometheus.service || BEFUND=1
elif geaendert "$ETC/prometheus.yml" || geaendert "$REGELN/nightcrawler.yml"; then
  # Konfiguration und Regeln liest Prometheus auf SIGHUP neu — ohne Luecke in
  # den Daten, anders als ein Neustart.
  dienst reload nightcrawler-prometheus.service || BEFUND=1
else
  gut "nightcrawler-prometheus: unveraendert, laeuft."
fi

# Den Paket-Dienst nur abschalten, wenn ERST dieser Lauf ihn gebracht hat.
# Lief er schon vorher, gehoert er jemandem — dann bleibt er, wie er ist.
if [ "$PROM_NEU" = 1 ] && [ "$PAKET_DIENST_VORHER" = 0 ] && { unit_da prometheus.service || [ "$TROCKEN" = 1 ]; }; then
  info "Der Dienst des Pakets lauscht auf *:9090 ohne Anmeldung — er wird abgeschaltet."
  dienst disable --now prometheus.service || warn "prometheus.service liess sich nicht abschalten — Port 9090 pruefen."
elif [ "$PAKET_DIENST_VORHER" = 1 ] && unit_aktiv prometheus.service; then
  info "prometheus.service lief schon vorher und bleibt unangetastet."
fi

# ═══════════════════════════════════════════════════════════════════════════
if [ "$GRAFANA" = "ja" ]; then
  kopf "Grafana"
  if [ "$GF_DA" = 0 ]; then
    GF_PAKET="$(nc_paketname grafana)"
    if [ "$NC_PKG" = "apt" ] && [ -z "$GF_PAKET" ]; then
      if [ "$GRAFANA_QUELLE" = 0 ] && { [ "$NC_MODUS" = "unattended" ] || ! frage_ja "Grafana liegt nicht in den Paketquellen. Offizielle Quelle apt.grafana.com eintragen?" N; }; then
        warn "Grafana nicht eingerichtet: es fehlt die Paketquelle."
        erklaere "Mit --grafana-repo traegt dieses Werkzeug https://apt.grafana.com ein (signiert, Schluessel unter /etc/apt/keyrings/grafana.gpg) und installiert das Paket grafana."
        BEFUND=1; GRAFANA="nein"
      else
        lauf mkdir -p /etc/apt/keyrings
        if [ "$TROCKEN" = 1 ]; then
          printf '    %s$%s curl -fsSL https://apt.grafana.com/gpg.key | gpg --dearmor -o /etc/apt/keyrings/grafana.gpg\n' "$FNT" "$R"
        else
          curl -fsSL https://apt.grafana.com/gpg.key | ${SUDO:+sudo} gpg --dearmor --yes -o /etc/apt/keyrings/grafana.gpg \
            || { fehler "Schluessel von apt.grafana.com nicht erhalten."; exit 1; }
        fi
        _liste="deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main"
        if [ "$TROCKEN" = 1 ]; then
          printf '    %s$%s echo "%s" > /etc/apt/sources.list.d/grafana.list\n' "$FNT" "$R" "$_liste"
        else
          printf '%s\n' "$_liste" | ${SUDO:+sudo} tee /etc/apt/sources.list.d/grafana.list >/dev/null
        fi
        GF_PAKET="grafana"
      fi
    fi
    if [ "$GRAFANA" = "ja" ]; then
      if [ -z "$GF_PAKET" ]; then
        warn "Fuer %s ist kein Grafana-Paket bekannt — bitte selbst installieren und erneut aufrufen." "${NC_PKG:-?}"
        BEFUND=1; GRAFANA="nein"
      else
        if _af="$(nc_auffrischbefehl)"; then
          # shellcheck disable=SC2086
          lauf $_af || true
        fi
        # shellcheck disable=SC2046,SC2086
        lauf env DEBIAN_FRONTEND=noninteractive $(nc_installbefehl $GF_PAKET) || { fehler "Installation gescheitert."; exit 1; }
        GF_DIENST="grafana-server.service"
        unit_da grafana.service && ! unit_da grafana-server.service && GF_DIENST="grafana.service"
      fi
    fi
  fi
fi
if [ "$GRAFANA" = "ja" ]; then
  # Das Drop-in heisst nach dem Dienst; Arch nennt ihn grafana.service.
  GF_DROPIN="$W/etc/systemd/system/${GF_DIENST:-grafana-server.service}.d/nightcrawler.conf"
  schreibe "$GF_PROV/datasources/nightcrawler.yml" "$VORLAGEN/grafana/provisioning/datasources/nightcrawler.yml" || exit 1
  schreibe "$GF_PROV/dashboards/nightcrawler.yml" "$VORLAGEN/grafana/provisioning/dashboards/nightcrawler.yml" || exit 1
  schreibe "$GF_DASH/nightcrawler.json" "$VORLAGEN/grafana/dashboards/nightcrawler.json" || exit 1
  schreibe "$GF_DROPIN" "$VORLAGEN/systemd/grafana-server.service.d/nightcrawler.conf" || exit 1
  geaendert "$GF_DROPIN" && dienst daemon-reload
  if ! unit_aktiv "${GF_DIENST:-grafana-server.service}"; then
    dienst enable --now "${GF_DIENST:-grafana-server.service}" || BEFUND=1
  elif [ -n "$GEAENDERT" ] && { geaendert "$GF_DROPIN" || geaendert "$GF_PROV/datasources/nightcrawler.yml" \
         || geaendert "$GF_PROV/dashboards/nightcrawler.yml" || geaendert "$GF_DASH/nightcrawler.json"; }; then
    # Grafana liest die Bereitstellung nur beim Start.
    dienst restart "${GF_DIENST:-grafana-server.service}" || BEFUND=1
  else
    gut "grafana: unveraendert, laeuft."
  fi
fi

if [ "$TROCKEN" = 1 ]; then
  info "Trockenlauf beendet — nichts wurde veraendert."
  exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════
# Nachpruefung: gemessen. "systemctl start" mit 0 heisst nur, dass systemd den
# Prozess gestartet hat — nicht, dass er die Konfiguration angenommen hat und
# den Bot erreicht.
kopf "Nachpruefung"
_bereit=0
# NC_OBS_WARTEN: Sekunden bis "antwortet nicht" (Vorgabe 10; die Vertraege
# setzen 0 — dort laeuft kein Prometheus, und zehn Sekunden je Lauf waeren
# nur Wartezeit).
for _i in $(seq 1 "${NC_OBS_WARTEN:-10}"); do
  if curl -fsS -m 3 "http://127.0.0.1:$PROM_PORT/-/ready" >/dev/null 2>&1; then _bereit=1; break; fi
  sleep 1
done
if [ "$_bereit" = 1 ]; then
  gut "Prometheus bereit: http://127.0.0.1:%s" "$PROM_PORT"
  # Der erste Abruf kommt erst nach scrape_interval — ein frisch gestarteter
  # Prometheus kennt "up" noch nicht. Das ist kein Fehler, nur zu frueh.
  _up="$(curl -fsS -m 5 "http://127.0.0.1:$PROM_PORT/api/v1/query" --data-urlencode 'query=up{job="nightcrawler"}' 2>/dev/null \
         | grep -o '"value":\[[^]]*\]' | grep -o '"[01]"' | tr -d '"' | head -1)"
  case "$_up" in
    1) gut "Der Bot wird abgefragt (up=1).";;
    0) warn "Prometheus erreicht den Bot nicht (up=0): laeuft der Dienst, stimmt DASHBOARD_PORT=%s?" "$DASH_PORT"; BEFUND=1;;
    *) info "Noch kein Abruf erfolgt — in 30 s erneut: bash tools/observability.sh --check";;
  esac
else
  warn "Prometheus antwortet nicht auf 127.0.0.1:%s." "$PROM_PORT"
  erklaere "journalctl -u nightcrawler-prometheus -n 40"
  BEFUND=1
fi
if [ "$GRAFANA" = "ja" ]; then
  if curl -fsS -m 5 "http://127.0.0.1:3000/api/health" >/dev/null 2>&1; then
    gut "Grafana bereit — Zugang per Tunnel: ssh -L 3001:127.0.0.1:3000 <server>, dann http://localhost:3001"
    erklaere "Erste Anmeldung admin/admin; Grafana verlangt dabei ein neues Passwort. Das Dashboard liegt im Ordner NIGHTCRAWLER."
  else
    warn "Grafana antwortet (noch) nicht auf 127.0.0.1:3000 — journalctl -u %s -n 40" "${GF_DIENST:-grafana-server}"
    BEFUND=1
  fi
fi
[ "$BEFUND" = 0 ] && gut "Fertig." || warn "Unvollstaendig — offene Punkte siehe oben."
exit "$BEFUND"
