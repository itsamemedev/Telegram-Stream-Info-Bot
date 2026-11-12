#!/usr/bin/env bash
#
# NIGHTCRAWLER — lokales LLM: ik_llama.cpp mit Qwen3-14B-Uncensored (v5.1-W181)
#
#     sudo bash tools/ikllama.sh               gefuehrt: altes llama.cpp weg, bauen, Modell, Dienst
#     bash tools/ikllama.sh --check            nur pruefen; Exit 1, wenn etwas fehlt
#     bash tools/ikllama.sh --dry-run          zeigen, was liefe — nichts ausfuehren
#     bash tools/ikllama.sh --zustand          ein Wort: fertig | alt | teilweise | fehlt
#     sudo bash tools/ikllama.sh --neu-bauen   Quellen holen und neu bauen
#     bash tools/ikllama.sh --help             alle Schalter
#
# WARUM ES DAS GIBT
# Der Betreiber am 11.11.: „Dann steigen wir um von llama.cpp auf ik_llama.cpp
# mit Qwen3-14B-Uncensored ... Wenn llama.cpp vorhanden, erst deinstallieren,
# bevor ik_llama.cpp mit Qwen3-14B-Uncensored installiert wird." Bis hierher
# stand die Einrichtung des lokalen LLM als Abschnitt IM Installer (Release-
# ZIP von ggml-org, Qwen2.5-1.5B) und nirgends sonst — update.sh kannte sie
# gar nicht. Jetzt ist es EIN Werkzeug, das Installer und update.sh rufen,
# wie observability.sh: zwei Kopien derselben Einrichtung laufen auseinander
# (W100).
#
# DIE REIHENFOLGE IST DIE SICHERUNG
#   1. Vorpruefung: RAM, Platte, Bauwerkzeuge, Modell-Angaben. Faellt hier
#      etwas, ist NICHTS veraendert — das alte llama.cpp laeuft weiter. Ein
#      Umstieg, der das Alte abbaut und dann am RAM scheitert, liesse den Bot
#      ohne lokales LLM zurueck, obwohl vorher eines lief.
#   2. Altes llama.cpp entfernen (Wunsch des Betreibers: ERST deinstallieren):
#      Dienste llamacpp/llama-server stoppen und abmelden, Unit-Dateien,
#      Programmdateien und Bauverzeichnis weg. Port 8080 muss frei sein,
#      sonst startet der neue Server nicht.
#   3. ik_llama.cpp klonen und bauen (CPU, GGML_NATIVE, nur das Ziel
#      llama-server, mit nice und halber Kernzahl — die Box nimmt dabei auf).
#   4. Modell laden: Wiederaufnahme nach Abbruch (.teil), Groesse und SHA-256
#      gegen die Angaben von Hugging Face, GGUF-Kennung.
#   5. Unit llama-server.service schreiben (gleicher Port wie bisher, damit
#      BRAIN_LLAMACPP_URL weiter passt), starten, /health abwarten.
#
# ALTE MODELLDATEIEN BLEIBEN — mit Begruendung. Programmdateien des alten
# llama.cpp sind ohne das alte Programm wertlos und werden entfernt. Ein altes
# GGUF dagegen laeuft auch unter ik_llama.cpp und ist der Rueckweg, falls das
# 14B-Modell fuer die Box zu gross ist (LLM_MODELL_DATEI darauf zeigen lassen).
# Es kostet rund 1 GB gegen 9 GB des neuen; reicht die Platte nicht, bricht
# die Vorpruefung ab und NENNT die alten Dateien samt --altes-modell-loeschen.
# Geloescht wird nur, was ausdruecklich verlangt ist.
#
# IDEMPOTENT. Ein zweiter Lauf auf fertigem Bestand baut nicht, laedt nicht und
# startet nichts neu. Neu gebaut wird nur mit --neu-bauen.
#
# WERTE (Umgebung > .env > Vorgabe — die .env wird GELESEN, nie geschrieben):
#   LLM_MODELL_REPO     mradermacher/Qwen3-14B-Uncensored-GGUF
#   LLM_MODELL_DATEI    Qwen3-14B-Uncensored.Q4_K_M.gguf   (rund 9 GB)
#   LLM_MODELL_QUANT    Q4_K_M  (Rueckfall, falls die Datei anders heisst)
#   LLM_MODELL_SHA256   leer = von Hugging Face; gesetzt = gegen diesen Wert
#   LLM_MODELL_VERZ     /opt/models
#   LLM_THREADS         4       (Aufnahmen haben Vorrang — siehe nc-ki-backends)
#   LLM_THREADS_BATCH   leer = wie LLM_THREADS; Threads nur fuers EINLESEN des Prompts
#   LLM_KONTEXT         8192
#   IK_LLAMA_DIR        /opt/ik_llama.cpp
#   IK_LLAMA_REPO       https://github.com/ikawrakow/ik_llama.cpp
#   IK_LLAMA_REF        main
#   IK_LLAMA_JOBS       leer = halbe Kernzahl
#   BRAIN_LLAMACPP_URL  daraus der Port (Vorgabe 8080)
#
# EXITCODES — dieselbe Trennung wie update.sh und observability.sh:
#   0  eingerichtet bzw. vollstaendig
#   1  es fehlt etwas (nach --check), Vorpruefung oder ein Schritt gescheitert
#   2  Aufruf- oder Umgebungsfehler (unbekannter Schalter, ungueltiger Wert)

set -uo pipefail

NC_IK_VERSION="1.0"
SKRIPT="$(cd "$(dirname "$0")" && pwd)"

# shellcheck source=lib/i18n.sh
. "$SKRIPT/lib/i18n.sh"
# shellcheck source=lib/ausgabe.sh
. "$SKRIPT/lib/ausgabe.sh"
# shellcheck source=lib/system.sh
. "$SKRIPT/lib/system.sh"

have(){ command -v "$1" >/dev/null 2>&1; }

# Die Kennung in jeder Unit, die dieses Werkzeug schreibt. An ihr — nicht am
# Dateinamen — unterscheidet die Erkennung den eigenen Dienst vom alten: beide
# heissen llama-server.service.
MARKE="# NIGHTCRAWLER-IK-LLAMA"

# ── Schalter ─────────────────────────────────────────────────
NC_MODUS="gefuehrt"
NUR_PRUEFEN=0; TROCKEN=0; NUR_ZUSTAND=0; NEU_BAUEN=0; ALT_MODELL_WEG=0; TROTZ_RAM=0
ZIEL="$(cd "$SKRIPT/.." && pwd)"
# Fuer die Vertraege: alle Systempfade unter einer anderen Wurzel. Auf einem
# Server bleibt das leer.
W="${NC_IK_WURZEL:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --express)        NC_MODUS="express";;
    --unattended|-y)  NC_MODUS="unattended";;
    --check)          NUR_PRUEFEN=1;;
    --dry-run)        TROCKEN=1;;
    --zustand)        NUR_ZUSTAND=1;;
    --neu-bauen|--rebuild) NEU_BAUEN=1;;
    --altes-modell-loeschen) ALT_MODELL_WEG=1;;
    --trotz-ram)      TROTZ_RAM=1;;
    --dir)            ZIEL="${2:-}"; shift;;
    --dir=*)          ZIEL="${1#*=}";;
    --no-color)       export NC_FARBE=0; nc_farben;;
    --version)        printf 'NIGHTCRAWLER ikllama %s\n' "$NC_IK_VERSION"; exit 0;;
    --help|-h)
      tz <<'HILFE'
NIGHTCRAWLER — lokales LLM: ik_llama.cpp mit Qwen3-14B-Uncensored

  sudo bash tools/ikllama.sh [Schalter]

Was:
  (ohne)           altes llama.cpp entfernen, ik_llama.cpp bauen, Modell laden, Dienst starten
  --neu-bauen      Quellen von ik_llama.cpp holen und neu bauen
  --altes-modell-loeschen  auch die GGUF-Dateien der alten Installation loeschen
  --trotz-ram      auch mit zu wenig Arbeitsspeicher einrichten

Wie:
  --check          nur pruefen und berichten; Exitcode 1, wenn etwas fehlt
  --zustand        ein Wort ausgeben: fertig, alt, teilweise oder fehlt
  --dry-run        die Schritte zeigen, die liefen — nichts ausfuehren
  --express        eine Rueckfrage fuer den ganzen Plan
  --unattended,-y  keine Rueckfragen
  --dir <Pfad>     Installation des Bots (Vorgabe: der Ordner ueber tools/)
  --no-color       ohne Farben

Modell und Bau: LLM_MODELL_REPO, LLM_MODELL_DATEI, LLM_THREADS, LLM_KONTEXT,
IK_LLAMA_DIR, IK_LLAMA_REF — in der Umgebung oder in der .env.
Exitcodes: 0 eingerichtet · 1 es fehlt etwas · 2 Aufruffehler
HILFE
      exit 0;;
    *) fehler "Unbekannter Schalter: %s  (--help)" "$1"; exit 2;;
  esac
  shift
done
[ -z "$NC_TTY" ] && [ "$NC_MODUS" != "unattended" ] && NC_MODUS="unattended"
[ -d "$ZIEL" ] || { fehler "Verzeichnis gibt es nicht: %s" "$ZIEL"; exit 2; }
ZIEL="$(cd "$ZIEL" && pwd)"

# ── Werte ────────────────────────────────────────────────────
ENVF="$ZIEL/.env"
env_wert(){ # letzter unkommentierter Wert, ohne Anfuehrungszeichen — gelesen, nie gesourct
  [ -f "$ENVF" ] || return 0
  awk -F= -v k="$1" '/^[[:space:]]*#/{next} {g=$1; gsub(/[[:space:]]/,"",g)}
    g==k {v=substr($0, index($0,"=")+1); sub(/[[:space:]]+#.*$/,"",v);
          gsub(/^[[:space:]"'"'"']+|[[:space:]"'"'"']+$/,"",v); w=v} END{if(w!="")print w}' "$ENVF"
}
# wert NAME VORGABE — Umgebung > .env > Vorgabe. Die Umgebung wird VOR jeder
# Zuweisung gelesen: ein ${X:-…} weiter oben haette X gesetzt, und dann waere
# die Frage "kommt das aus der Umgebung?" fuer jede Variable wahr (W101, motd).
wert(){
  local _v="${!1:-}"
  [ -n "$_v" ] || _v="$(env_wert "$1")"
  printf '%s' "${_v:-$2}"
}
MODELL_REPO="$(wert LLM_MODELL_REPO mradermacher/Qwen3-14B-Uncensored-GGUF)"
MODELL_DATEI="$(wert LLM_MODELL_DATEI Qwen3-14B-Uncensored.Q4_K_M.gguf)"
MODELL_QUANT="$(wert LLM_MODELL_QUANT Q4_K_M)"
# v5.2-W190: klein geschrieben — sha256sum liefert Kleinbuchstaben, und ein
# gross kopierter Wert aus dem Browser loeschte sonst das fertige Modell als
# "Pruefsumme stimmt nicht".
MODELL_SHA="$(wert LLM_MODELL_SHA256 "" | tr 'A-F' 'a-f')"
MODELL_VERZ_E="$(wert LLM_MODELL_VERZ /opt/models)"
THREADS="$(wert LLM_THREADS 4)"
# v5.5-W196: Threads fuers Einlesen getrennt einstellbar. Gemessen beim
# Betreiber mit -t 4: 7,8 Token/s beim Einlesen, 3,4 beim Erzeugen. Einlesen
# ist reine Rechenarbeit und verteilt sich gut; Erzeugen haengt am Speicher.
# Vorgabe leer = unveraendert — die Kerne gehoeren Aufnahme und Restream, und
# wie viel mehr Threads hier helfen, misst der Betreiber an SEINER Box.
THREADS_BATCH="$(wert LLM_THREADS_BATCH "")"
KONTEXT="$(wert LLM_KONTEXT 8192)"
# v5.2-W193: KV-Cache quantisieren. Qwen3-14B: 40 Schichten x 8 KV-Koepfe x 128
# x 2 Byte x (K+V) = 160 KiB je Token, bei 8192 Token Kontext 1,34 GB in f16,
# mit q8_0 rund 0,71 GB. f16 = aus (wie bis v5.2.1).
KV_CACHE="$(wert LLM_KV_CACHE q8_0)"
IK_DIR_E="$(wert IK_LLAMA_DIR /opt/ik_llama.cpp)"
IK_REPO="$(wert IK_LLAMA_REPO https://github.com/ikawrakow/ik_llama.cpp)"
IK_REF="$(wert IK_LLAMA_REF main)"
JOBS="$(wert IK_LLAMA_JOBS "")"
HF="${NC_IK_HF:-https://huggingface.co}"
LLM_URL="$(wert BRAIN_LLAMACPP_URL http://127.0.0.1:8080)"

# Eingaben pruefen, BEVOR sie in eine Unit oder einen Befehl wandern.
PORT="$(printf '%s' "$LLM_URL" | sed -n 's#^https\{0,1\}://\(127\.0\.0\.1\|localhost\|\[::1\]\):\([0-9]*\).*#\2#p')"
if [ -z "$PORT" ]; then
  case "$LLM_URL" in
    http://127.0.0.1|http://127.0.0.1/|http://localhost|http://localhost/) PORT=80;;
    *) fehler "BRAIN_LLAMACPP_URL zeigt nicht auf diese Maschine: %s" "$LLM_URL"
       erklaere "Dieses Werkzeug richtet den Server lokal ein (127.0.0.1). Laeuft das LLM auf einem anderen Rechner, gehoert es dort eingerichtet — oder BRAIN_LLAMACPP_URL auf http://127.0.0.1:8080 setzen."
       exit 2;;
  esac
fi
zahl(){ case "$2" in ''|*[!0-9]*) fehler "%s ist keine Zahl: %s" "$1" "$2"; exit 2;; esac; }
zahl "Port" "$PORT"; zahl LLM_THREADS "$THREADS"; zahl LLM_KONTEXT "$KONTEXT"
[ -z "$THREADS_BATCH" ] || zahl LLM_THREADS_BATCH "$THREADS_BATCH"
[ -z "$JOBS" ] || zahl IK_LLAMA_JOBS "$JOBS"
if [ "$((10#$PORT))" -lt 1024 ] || [ "$((10#$PORT))" -gt 65535 ]; then
  fehler "Port ausserhalb von 1024 bis 65535: %s" "$PORT"; exit 2
fi
# Genau ein Schraegstrich, beidseits ein Name: das Repo landet in einer URL.
case "$MODELL_REPO" in
  */*/*|*[!A-Za-z0-9._/-]*|[!A-Za-z0-9]*|*/[!A-Za-z0-9]*|*/) _repo_ok=0;;
  */*) _repo_ok=1;;
  *) _repo_ok=0;;
esac
[ "$_repo_ok" = 1 ] || { fehler "LLM_MODELL_REPO ungueltig: %s (Form: besitzer/name)" "$MODELL_REPO"; exit 2; }
case "$MODELL_DATEI" in
  */*|.*|*[!A-Za-z0-9._-]*) fehler "LLM_MODELL_DATEI ungueltig: %s" "$MODELL_DATEI"; exit 2;;
  *.gguf) ;;
  *) fehler "LLM_MODELL_DATEI ist keine .gguf-Datei: %s" "$MODELL_DATEI"; exit 2;;
esac
# v5.2-W190: 64 Hex-Zeichen, nicht 64 beliebige — ein Tippfehler fiel sonst
# erst nach dem Download von 9 GB auf.
case "$KV_CACHE" in f16|q8_0|q4_0) ;;
  *) fehler "LLM_KV_CACHE muss f16, q8_0 oder q4_0 sein: %s" "$KV_CACHE"; exit 2;; esac
case "$MODELL_SHA" in
  '') ;;
  *[!0-9a-f]*) fehler "LLM_MODELL_SHA256 ist kein SHA-256 (nur 0-9a-f): %s" "$MODELL_SHA"; exit 2;;
  ????????????????????????????????????????????????????????????????) ;;
  *) fehler "LLM_MODELL_SHA256 ist kein SHA-256 (64 Zeichen): %s" "$MODELL_SHA"; exit 2;; esac
for _p in "$MODELL_VERZ_E" "$IK_DIR_E"; do
  case "$_p" in /*) ;; *) fehler "Pfad muss absolut sein: %s" "$_p"; exit 2;; esac
  case "$_p" in *[!A-Za-z0-9._/-]*) fehler "Pfad mit Sonderzeichen: %s" "$_p"; exit 2;; esac
done
case "$IK_REF" in *[!A-Za-z0-9._/-]*|-*) fehler "IK_LLAMA_REF ungueltig: %s" "$IK_REF"; exit 2;; esac
case "$IK_REPO" in https://*) ;; *) fehler "IK_LLAMA_REPO muss eine https-Adresse sein: %s" "$IK_REPO"; exit 2;; esac

# ── Pfade ────────────────────────────────────────────────────
# *_E: so, wie sie in der Unit stehen. Ohne _E: wo dieses Skript sie anfasst.
IK_DIR="$W$IK_DIR_E"
IK_BIN_E="$IK_DIR_E/build/bin/llama-server"
IK_BIN="$W$IK_BIN_E"
STEMPEL="$IK_DIR/.nc_gebaut"
MODELL_VERZ="$W$MODELL_VERZ_E"
UNIT_NAME="llama-server.service"
UNIT="$W/etc/systemd/system/$UNIT_NAME"
# Alles, was die bisherigen Wege angelegt haben: der Installer bis v5.0
# (/opt/llamacpp, Dienst llamacpp), die mitgelieferte Unit (/opt/llama.cpp,
# Dienst llama-server) und ein "make install" (/usr/local/bin).
ALT_DIENSTE="llamacpp llama-server"
ALT_UNIT_ORTE="/etc/systemd/system /lib/systemd/system /usr/lib/systemd/system"
ALT_ORDNER="/opt/llamacpp /opt/llama.cpp"
ALT_PROGRAMME="/usr/local/bin/llama-server"

SUDO=""
if [ -n "${NC_IK_SUDO+gesetzt}" ]; then
  # Fuer die Vertraege: sudo setzt den PATH zurueck und traefe das echte
  # systemctl statt der Attrappe (Lehre aus observability.sh).
  SUDO="$NC_IK_SUDO"
elif [ "$(id -u)" -ne 0 ]; then
  if have sudo; then SUDO="sudo"; else SUDO="-"; fi
fi

lauf(){
  if [ "$TROCKEN" = 1 ]; then printf '    %s$%s %s\n' "$FNT" "$R" "$*"; return 0; fi
  printf '    %s$ %s%s\n' "$FNT" "$*" "$R"
  if [ -n "$SUDO" ] && [ "$SUDO" != "-" ]; then sudo "$@"; else "$@"; fi
}
mb(){ # Bytes -> MB, gerundet
  printf '%s' "$(( ($1 + 524288) / 1048576 ))"
}

# ── Erkennung ────────────────────────────────────────────────
ALT_UNITS=""          # Unit-Dateien des alten llama.cpp (Pfad unter $W)
ALT_DIENST_NAMEN=""   # deren Dienstnamen
ALT_DATEN=""          # Programmordner und -dateien, die entfernt werden
ALT_FREMD=""          # Programme an Orten, die dieses Skript nicht kennt — nur genannt
ALT_MODELLE=""        # GGUF-Dateien der alten Installation
# bekannt_alt PFAD -> 0, wenn PFAD in einem Ort liegt, den dieses Skript
# selbst entfernt (oder im neuen Bau — der ist nicht alt).
bekannt_alt(){
  local _k
  case "$1" in "$IK_DIR_E"/*) return 0;; esac
  for _k in $ALT_ORDNER; do case "$1" in "$_k"/*) return 0;; esac; done
  for _k in $ALT_PROGRAMME; do [ "$1" = "$_k" ] && return 0; done
  return 1
}
alt_erkennen(){
  local _u _d _f _bin _m _o
  ALT_UNITS=""; ALT_DIENST_NAMEN=""; ALT_DATEN=""; ALT_FREMD=""; ALT_MODELLE=""
  for _u in $ALT_DIENSTE; do
    for _d in $ALT_UNIT_ORTE; do
      _f="$W$_d/$_u.service"
      [ -f "$_f" ] || continue
      # Die eigene Unit traegt die Marke — sie ist der NEUE Dienst, nicht der alte.
      grep -q "^$MARKE" "$_f" 2>/dev/null && continue
      ALT_UNITS="$ALT_UNITS $_f"
      case " $ALT_DIENST_NAMEN " in *" $_u "*) ;; *) ALT_DIENST_NAMEN="$ALT_DIENST_NAMEN $_u";; esac
      # Programm und Modell aus ExecStart: nur die erste Zeile mit dem Befehl
      # und ihre Fortsetzungen — ein Kommentar ueber -m ist kein Modell.
      _bin="$(awk '/^[[:space:]]*#/{next} /^ExecStart=/{f=1} f{printf "%s ", $0; if ($0 !~ /\\$/) exit}' "$_f" \
              | sed 's/^ExecStart=//; s/\\//g')"
      _o="${_bin%% *}"
      if [ -n "$_o" ] && [ -e "$W$_o" ] && ! bekannt_alt "$_o"; then
        case " $ALT_FREMD " in *" $_o "*) ;; *) ALT_FREMD="$ALT_FREMD $_o";; esac
      fi
      _m="$(printf '%s' "$_bin" | sed -n 's/.*[[:space:]]\(-m\|--model\)[[:space:]]\{1,\}\([^[:space:]]*\.gguf\).*/\2/p')"
      if [ -n "$_m" ] && [ -f "$W$_m" ] && [ "$_m" != "$MODELL_VERZ_E/$MODELL_DATEI" ]; then
        case " $ALT_MODELLE " in *" $_m "*) ;; *) ALT_MODELLE="$ALT_MODELLE $_m";; esac
      fi
    done
  done
  for _d in $ALT_ORDNER; do
    [ -d "$W$_d" ] || continue
    [ "$_d" = "$IK_DIR_E" ] && continue
    # Liegen nur noch Modelle darin, ist der Umstieg hier erledigt — sonst
    # meldete jeder weitere Lauf "altes llama.cpp gefunden", fuer immer.
    if find "$W$_d" -mindepth 1 -maxdepth 1 ! -name '*.gguf' 2>/dev/null | grep -q .; then
      ALT_DATEN="$ALT_DATEN $_d"
    fi
    for _f in "$W$_d"/*.gguf; do
      [ -f "$_f" ] || continue
      _f="${_f#"$W"}"
      case " $ALT_MODELLE " in *" $_f "*) ;; *) ALT_MODELLE="$ALT_MODELLE $_f";; esac
    done
  done
  for _f in $ALT_PROGRAMME; do
    # Ein Verweis in den neuen Bau ist nicht "alt".
    if [ -f "$W$_f" ] && [ "$(readlink -f "$W$_f" 2>/dev/null)" != "$(readlink -f "$IK_BIN" 2>/dev/null)" ]; then
      ALT_DATEN="$ALT_DATEN $_f"
    fi
  done
}

# Die Unit, wie dieser Lauf sie schreiben wuerde. Der Speicherdeckel folgt der
# Modellgroesse: der alte Deckel von 3 GB haette den 14B-Server beim Laden
# abgeschossen, und -rtr legt das Modell vollstaendig in den Arbeitsspeicher.
# In eine DATEI, nicht auf stdout: die Kommentare darin sind fuer systemd und
# den, der die Unit liest — keine Ausgabe an den Betreiber im Dialog.
# v5.2-W193: die Schalter fuer den quantisierten KV-Cache — nur, wenn das
# gebaute llama-server sie kennt. ik_llama.cpp und llama.cpp schreiben
# Flash-Attention verschieden (-fa gegen -fa on), und ein unbekannter Schalter
# laesst den Dienst gar nicht erst starten. Gefragt wird das Programm selbst.
kv_schalter(){
  [ "$KV_CACHE" = "f16" ] && return 0
  [ -x "$IK_BIN_E" ] || return 0
  local _hilfe; _hilfe="$("$IK_BIN_E" --help 2>&1 || true)"
  printf '%s' "$_hilfe" | grep -q -- '--cache-type-k' || return 0
  printf '%s' "$_hilfe" | grep -q -- '--flash-attn' || return 0
  if printf '%s' "$_hilfe" | grep -Eq -- '--flash-attn[^[:alnum:]]*[^\n]*(\[on|on\|off|<on)'; then
    printf ' -fa on -ctk %s -ctv %s' "$KV_CACHE" "$KV_CACHE"
  else
    printf ' -fa -ctk %s -ctv %s' "$KV_CACHE" "$KV_CACHE"
  fi
}

# v5.5-W196: -tb nur, wenn gesetzt UND das Programm den Schalter kennt — ein
# unbekannter Schalter liesse den Dienst nicht starten (wie bei kv_schalter).
tb_schalter(){
  [ -n "$THREADS_BATCH" ] || return 0
  [ -x "$IK_BIN_E" ] || return 0
  "$IK_BIN_E" --help 2>&1 | grep -q -- '--threads-batch' || return 0
  printf ' -tb %s' "$THREADS_BATCH"
}

unit_text(){ # unit_text GROESSE_BYTES DATEI
  local _gb=$(( ($1 + 1073741823) / 1073741824 + 4 ))
  local _kv; _kv="$(kv_schalter)$(tb_schalter)"
  local _alias; _alias="$(printf '%s' "${MODELL_DATEI%.gguf}" | tr 'A-Z' 'a-z')"
  cat > "$2" <<UNIT
$MARKE — erzeugt von tools/ikllama.sh (v5.1-W181).
# Nicht von Hand aendern: der naechste Lauf schreibt sie neu. Werte ueber die
# .env (LLM_THREADS, LLM_KONTEXT, LLM_MODELL_DATEI, BRAIN_LLAMACPP_URL).
#   -t $THREADS        Aufnahmen und Restreams haben Vorrang vor der KI (Nice, CPUWeight)
#   -ngl 0      reiner CPU-Betrieb; die Vorgabe von ik_llama.cpp ist 999
#   -rtr        Gewichte beim Laden in die verschraenkte Form umpacken (schneller auf CPU)
#   --jinja     Chat-Vorlage aus dem Modell: nur damit wirkt enable_thinking=false
#   KEIN --embeddings: der Schalter beschraenkt den Server auf Embeddings (W110)
#   -ctk/-ctv   KV-Cache quantisiert (LLM_KV_CACHE, v5.2-W193), braucht -fa
#   -tb         Threads nur fuers Einlesen (LLM_THREADS_BATCH, v5.5-W196), leer = wie -t
[Unit]
Description=ik_llama.cpp Server (NIGHTCRAWLER Brain-LLM, ${MODELL_DATEI%.gguf})
After=network.target

[Service]
Type=simple
ExecStart=$IK_BIN_E -m $MODELL_VERZ_E/$MODELL_DATEI -a $_alias --host 127.0.0.1 --port $PORT -t $THREADS -c $KONTEXT -ngl 0 -rtr --jinja --no-warmup$_kv
Nice=10
CPUWeight=50
MemoryMax=${_gb}G
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT
}

MODELL="$MODELL_VERZ/$MODELL_DATEI"
MODELL_OK="$MODELL.sha256"     # geschrieben erst NACH bestandener Pruefung
ik_gebaut(){ [ -x "$IK_BIN" ] && [ -f "$STEMPEL" ]; }
modell_fertig(){ [ -f "$MODELL" ] && [ -s "$MODELL_OK" ]; }
unit_aktuell(){
  local _t _rc
  [ -f "$UNIT" ] && modell_fertig || return 1
  _t="$(mktemp)" || return 1
  unit_text "$(wc -c < "$MODELL" | tr -d ' ')" "$_t"
  cmp -s "$_t" "$UNIT"; _rc=$?
  rm -f "$_t"; return "$_rc"
}

zustand(){   # braucht alt_erkennen vorher — im Elternprozess, nicht in $(…)
  # Die vier Woerter sind Schnittstelle (update.sh, installer.sh), keine
  # Ausgabe an den Betreiber — sie bleiben in jeder Sprache gleich.
  if [ -n "$ALT_UNITS$ALT_DATEN" ]; then echo alt; return; fi
  if ik_gebaut && modell_fertig && unit_aktuell; then echo fertig; return; fi
  if [ -e "$IK_DIR" ] || [ -f "$MODELL" ] || [ -f "$MODELL.teil" ] || [ -f "$UNIT" ]; then
    echo teilweise; return
  fi
  echo fehlt
}

alt_erkennen
if [ "$NUR_ZUSTAND" = 1 ]; then
  zustand; exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Lokales LLM: ik_llama.cpp"
nc_system_erkennen
nc_init_erkennen
info "Modell: %s/%s" "$MODELL_REPO" "$MODELL_DATEI"
info "Server: %s  (127.0.0.1:%s, %s Threads, Kontext %s)" "$IK_BIN_E" "$PORT" "$THREADS" "$KONTEXT"
[ "$TROCKEN" = 1 ] && info "Trockenlauf — Befehle werden gezeigt, nicht ausgefuehrt."

ZST="$(zustand)"
BEFUND=0
if [ -n "$ALT_UNITS$ALT_DATEN" ]; then
  warn "Altes llama.cpp gefunden — wird vor der Einrichtung entfernt:"
  for _x in $ALT_UNITS $ALT_DATEN; do info "  %s" "${_x#"$W"}"; done
fi
for _x in $ALT_FREMD; do
  warn "Altes llama-server an unbekanntem Ort: %s — wird nicht angefasst, bitte selbst entfernen." "$_x"
done
for _x in $ALT_MODELLE; do
  if [ "$ALT_MODELL_WEG" = 1 ]; then info "Altes Modell wird geloescht: %s" "$_x"
  else info "Altes Modell bleibt liegen: %s (loeschen: --altes-modell-loeschen)" "$_x"; fi
done
if ik_gebaut; then gut "ik_llama.cpp gebaut: %s (%s)" "$IK_BIN_E" "$(cat "$STEMPEL" 2>/dev/null)"
else info "ik_llama.cpp: noch nicht gebaut"; fi
if modell_fertig; then gut "Modell geprueft: %s" "$MODELL_VERZ_E/$MODELL_DATEI"
elif [ -f "$MODELL.teil" ]; then info "Modell: Teil-Download liegt vor (%s MB) — wird fortgesetzt." "$(mb "$(wc -c < "$MODELL.teil")")"
else info "Modell: noch nicht geladen"; fi
if unit_aktuell; then gut "Dienst: %s ist aktuell" "$UNIT_NAME"; fi

if [ "$ZST" = "fertig" ] && [ "$NEU_BAUEN" = 0 ]; then
  gut "ik_llama.cpp mit %s ist eingerichtet — nichts zu tun." "$MODELL_DATEI"
  if [ "$NC_INIT" = "systemd" ] && have systemctl && ! systemctl is-active --quiet "$UNIT_NAME" 2>/dev/null; then
    warn "Der Dienst %s laeuft nicht — sudo systemctl start %s; Grund: journalctl -u %s -n 50" "$UNIT_NAME" "$UNIT_NAME" "$UNIT_NAME"
    [ "$NUR_PRUEFEN" = 1 ] && exit 1
  fi
  exit 0
fi
if [ "$NUR_PRUEFEN" = 1 ]; then
  case "$ZST" in
    alt)       warn "Umstieg steht aus: altes llama.cpp statt ik_llama.cpp. Einrichten: sudo bash tools/ikllama.sh";;
    teilweise) warn "Einrichtung unvollstaendig. Fortsetzen: sudo bash tools/ikllama.sh";;
    *)         info "Lokales LLM nicht eingerichtet. Einrichten: sudo bash tools/ikllama.sh";;
  esac
  exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
kopf "Vorpruefung"
# Nichts hier veraendert etwas. Faellt eine Pruefung, laeuft das alte
# llama.cpp unangetastet weiter.

# Modell-Angaben von Hugging Face: Name, Groesse, SHA-256. Ueber die API statt
# geraten — eine falsche Groesse liesse eine abgebrochene Datei als fertig
# durchgehen.
HF_GROESSE=""; HF_SHA=""
hf_lesen(){
  local _json _py
  _py="$ZIEL/.venv/bin/python"; [ -x "$_py" ] || _py="python3"
  # Meldungen auf stderr: die Funktion laeuft in $(…), und stdout ist dort
  # die Liste — eine Warnung darin waere verschluckt und als Datei gelesen.
  have "$_py" || [ -x "$_py" ] || { warn "Kein python3 — Modell-Angaben von Hugging Face nicht lesbar." >&2; return 1; }
  _json="$(curl -fsSL --max-time 30 "$HF/api/models/$MODELL_REPO/tree/main" 2>/dev/null)" || {
    warn "Hugging Face nicht erreichbar (%s/api/models/%s) — Groesse und Pruefsumme ungeprueft." "$HF" "$MODELL_REPO" >&2
    return 1; }
  # Ausgabe: DATEI<TAB>GROESSE<TAB>SHA256 je GGUF. -I: nichts aus dem
  # Arbeitsverzeichnis importieren.
  printf '%s' "$_json" | "$_py" -I -c '
import json, sys
for e in json.load(sys.stdin):
    p = e.get("path") or ""
    if not p.endswith(".gguf"):
        continue
    lfs = e.get("lfs") or {}
    print("%s\t%s\t%s" % (p, lfs.get("size") or e.get("size") or "", lfs.get("oid") or lfs.get("sha256") or ""))
' 2>/dev/null || {
    warn "Antwort von Hugging Face nicht lesbar — Groesse und Pruefsumme ungeprueft." >&2
    return 1; }
}
LISTE="$(hf_lesen)" || LISTE=""
if [ -n "$LISTE" ]; then
  _zeile="$(printf '%s\n' "$LISTE" | awk -F '\t' -v d="$MODELL_DATEI" '$1==d' | head -1)"
  if [ -z "$_zeile" ]; then
    # Rueckfall auf die Quantisierung: die Datei heisst in einem anderen
    # Repo anders (Punkt statt Bindestrich, "i1-"), die Wahl ist dieselbe.
    _treffer="$(printf '%s\n' "$LISTE" | awk -F '\t' -v q="$MODELL_QUANT" 'index($1, q) && $1 !~ /\//')"
    if [ "$(printf '%s\n' "$_treffer" | grep -c .)" = 1 ]; then
      _zeile="$_treffer"
      warn "%s gibt es in %s nicht — nehme %s (gleiche Quantisierung %s)." "$MODELL_DATEI" "$MODELL_REPO" "$(printf '%s' "$_zeile" | cut -f1)" "$MODELL_QUANT"
      MODELL_DATEI="$(printf '%s' "$_zeile" | cut -f1)"
      MODELL="$MODELL_VERZ/$MODELL_DATEI"; MODELL_OK="$MODELL.sha256"
    else
      fehler "%s gibt es in %s nicht." "$MODELL_DATEI" "$MODELL_REPO"
      erklaere "Vorhanden sind (LLM_MODELL_DATEI auf einen davon setzen):"
      printf '%s\n' "$LISTE" | cut -f1,2 | awk -F '\t' '{printf "      %s  (%d MB)\n", $1, ($2+524288)/1048576}'
      exit 1
    fi
  fi
  HF_GROESSE="$(printf '%s' "$_zeile" | cut -f2)"
  HF_SHA="$(printf '%s' "$_zeile" | cut -f3)"
  [ -n "$HF_GROESSE" ] && info "Modell bei Hugging Face: %s MB, SHA-256 %s" "$(mb "$HF_GROESSE")" "${HF_SHA:-unbekannt}"
fi
[ -n "$MODELL_SHA" ] && HF_SHA="$MODELL_SHA"
# Ohne Angabe gilt eine vorsichtige Schaetzung fuer 14B Q4_K_M (rund 9 GB).
GROESSE="${HF_GROESSE:-9663676416}"
if [ -f "$MODELL" ] && ! modell_fertig; then GROESSE="$(wc -c < "$MODELL" | tr -d ' ')"; fi

# Arbeitsspeicher: Modell + Kontext + Puffer. Mit -rtr liegt das Modell
# vollstaendig im RAM, und daneben laufen ffmpeg, Whisper und der Bot.
RAM_MB="${NC_IK_RAM_MB:-}"
[ -n "$RAM_MB" ] || RAM_MB="$(awk '/^MemTotal:/{printf "%d", $2/1024}' /proc/meminfo 2>/dev/null)"
RAM_NOETIG=$(( $(mb "$GROESSE") + 3072 ))
if [ -n "$RAM_MB" ] && [ "$RAM_MB" -lt "$RAM_NOETIG" ]; then
  if [ "$TROTZ_RAM" = 1 ]; then
    warn "Arbeitsspeicher knapp: %s MB vorhanden, rund %s MB noetig — auf Wunsch trotzdem (--trotz-ram)." "$RAM_MB" "$RAM_NOETIG"
  else
    fehler "Zu wenig Arbeitsspeicher: %s MB vorhanden, rund %s MB noetig. Nichts veraendert." "$RAM_MB" "$RAM_NOETIG"
    erklaere "Ein kleineres Modell passt: LLM_MODELL_DATEI=Qwen3-14B-Uncensored.Q3_K_M.gguf (rund 7 GB) oder .Q2_K.gguf (rund 6 GB) in die .env, dann erneut. Wer es trotzdem will: --trotz-ram."
    exit 1
  fi
else
  gut "Arbeitsspeicher: %s MB (noetig rund %s MB)" "${RAM_MB:-?}" "$RAM_NOETIG"
fi

# Platte: was vom Modell noch fehlt, plus rund 2 GB fuer Quellen und Bau.
frei_mb(){ # frei_mb PFAD -> freie MB am naechsten vorhandenen Elternordner
  local _p="$1"
  while [ ! -d "$_p" ] && [ "$_p" != "/" ] && [ -n "$_p" ]; do _p="$(dirname "$_p")"; done
  df -Pk "${_p:-/}" 2>/dev/null | awk 'NR==2{printf "%d", $4/1024}'
}
_schon=0
modell_fertig && _schon="$GROESSE"
[ -f "$MODELL.teil" ] && _schon="$(wc -c < "$MODELL.teil" | tr -d ' ')"
PLATZ_NOETIG=$(( $(mb "$GROESSE") - $(mb "$_schon") + 1024 ))
ik_gebaut || PLATZ_NOETIG=$(( PLATZ_NOETIG + 2048 ))
PLATZ="$(frei_mb "$MODELL_VERZ")"
if [ -n "$PLATZ" ] && [ "$PLATZ" -lt "$PLATZ_NOETIG" ]; then
  fehler "Zu wenig Platz unter %s: %s MB frei, rund %s MB noetig. Nichts veraendert." "$MODELL_VERZ_E" "$PLATZ" "$PLATZ_NOETIG"
  [ -n "$ALT_MODELLE" ] && erklaere "Platz schaffen die Modelle der alten Installation (Liste oben): erneut mit --altes-modell-loeschen."
  exit 1
fi
gut "Platte: %s MB frei (noetig rund %s MB)" "${PLATZ:-?}" "$PLATZ_NOETIG"

# Bauwerkzeuge: fehlen sie und ist kein Paketmanager da, gar nicht erst anfangen.
BAU_FEHLT=""
if ! ik_gebaut || [ "$NEU_BAUEN" = 1 ]; then
  for _w in git cmake make; do have "$_w" || BAU_FEHLT="$BAU_FEHLT $_w"; done
  have c++ || have g++ || BAU_FEHLT="$BAU_FEHLT c++"
fi
BAU_PAKETE=""
if [ -n "$BAU_FEHLT" ]; then
  BAU_PAKETE="$(nc_baupakete)"
  if [ -z "$BAU_PAKETE" ] || [ "$SUDO" = "-" ]; then
    fehler "Zum Bauen fehlt:%s — und dieser Lauf kann es nicht installieren (Paketmanager %s). Nichts veraendert." "$BAU_FEHLT" "$NC_PKG"
    erklaere "Bitte C++-Compiler, make, cmake und git selbst installieren und erneut aufrufen."
    exit 1
  fi
  info "Zum Bauen fehlt:%s — wird installiert: %s" "$BAU_FEHLT" "$BAU_PAKETE"
fi
if [ "$(uname -m 2>/dev/null)" = "x86_64" ] && [ -r /proc/cpuinfo ] && ! grep -qw avx2 /proc/cpuinfo; then
  warn "Die CPU meldet kein AVX2 — ik_llama.cpp laeuft, aber deutlich langsamer."
fi
if [ -d "$IK_DIR" ] && [ ! -d "$IK_DIR/.git" ]; then
  fehler "%s gibt es schon, ist aber kein git-Arbeitsbaum — nicht ueberschrieben. Nichts veraendert." "$IK_DIR_E"
  erklaere "Ordner wegraeumen oder IK_LLAMA_DIR auf einen anderen Ort setzen."
  exit 1
fi
if [ "$SUDO" = "-" ]; then
  fehler "Weder root noch sudo — /opt und der Dienst sind so nicht einzurichten."
  exit 1
fi

# ── Plan ─────────────────────────────────────────────────────
kopf "Plan"
[ -n "$ALT_UNITS$ALT_DATEN" ] && info "1. Altes llama.cpp stoppen und entfernen:%s" "$(for _x in $ALT_DIENST_NAMEN; do printf ' %s.service' "$_x"; done; for _x in $ALT_DATEN; do printf ' %s' "$_x"; done)"
[ -n "$BAU_PAKETE" ] && info "2. Bauwerkzeuge installieren: %s" "$BAU_PAKETE"
if ! ik_gebaut || [ "$NEU_BAUEN" = 1 ]; then info "3. ik_llama.cpp holen (%s, %s) und bauen" "$IK_REPO" "$IK_REF"; fi
modell_fertig || info "4. Modell laden: %s (%s MB)" "$MODELL_DATEI" "$(mb "$GROESSE")"
info "5. Dienst %s auf 127.0.0.1:%s einrichten und auf /health warten" "$UNIT_NAME" "$PORT"
if [ "$NC_MODUS" != "unattended" ] && [ "$TROCKEN" = 0 ]; then
  frage_ja "Plan ausfuehren?" J || { info "Abgebrochen — nichts veraendert."; exit 1; }
fi

# ═══════════════════════════════════════════════════════════════════════════
if [ -n "$ALT_UNITS$ALT_DATEN" ] || { [ "$ALT_MODELL_WEG" = 1 ] && [ -n "$ALT_MODELLE" ]; }; then
  kopf "Altes llama.cpp entfernen"
  for _u in $ALT_DIENST_NAMEN; do
    if [ "$NC_INIT" = "systemd" ] && have systemctl; then
      lauf systemctl disable --now "$_u.service" || warn "%s liess sich nicht stoppen — weiter, der Port wird unten geprueft." "$_u.service"
    fi
  done
  for _f in $ALT_UNITS; do lauf rm -f "$_f" || { fehler "Unit nicht entfernbar: %s" "${_f#"$W"}"; exit 1; }; done
  [ -n "$ALT_UNITS" ] && [ "$NC_INIT" = "systemd" ] && have systemctl && { lauf systemctl daemon-reload || true; }
  for _d in $ALT_DATEN; do
    if [ -d "$W$_d" ]; then
      if [ "$ALT_MODELL_WEG" = 1 ]; then
        lauf rm -rf "$W$_d" || { fehler "Nicht entfernbar: %s" "$_d"; exit 1; }
      else
        # Alles ausser den Modellen: die bleiben der Rueckweg (Kopf der Datei).
        lauf find "$W$_d" -mindepth 1 -maxdepth 1 ! -name '*.gguf' -exec rm -rf {} + \
          || { fehler "Nicht entfernbar: %s" "$_d"; exit 1; }
      fi
    else
      lauf rm -f "$W$_d" || { fehler "Nicht entfernbar: %s" "$_d"; exit 1; }
    fi
  done
  if [ "$ALT_MODELL_WEG" = 1 ]; then
    for _m in $ALT_MODELLE; do [ -f "$W$_m" ] && { lauf rm -f "$W$_m" || warn "Nicht entfernbar: %s" "$_m"; }; done
  fi
  # Nachsehen statt annehmen: belegt noch etwas den Port, startet der neue
  # Server nicht — und /health antwortete dann der ALTE.
  if [ "$TROCKEN" = 0 ] && have curl && curl -s -o /dev/null --max-time 3 "http://127.0.0.1:$PORT/health"; then
    fehler "Auf 127.0.0.1:%s antwortet noch ein Server — ein altes llama-server ausserhalb von systemd?" "$PORT"
    erklaere "Pruefen: ss -ltnp | grep :%s — den Prozess beenden und erneut aufrufen." "$PORT"
    exit 1
  fi
  gut "Altes llama.cpp entfernt."
fi

# ── Bauwerkzeuge ─────────────────────────────────────────────
if [ -n "$BAU_PAKETE" ]; then
  kopf "Bauwerkzeuge"
  if _af="$(nc_auffrischbefehl)"; then
    # shellcheck disable=SC2086  # feste Woerter aus lib/system.sh
    lauf $_af || warn "Paketquellen liessen sich nicht auffrischen — versuche es trotzdem."
  fi
  # shellcheck disable=SC2046,SC2086
  lauf $(nc_installbefehl $BAU_PAKETE) || { fehler "Bauwerkzeuge liessen sich nicht installieren."; exit 1; }
fi

# ── Quellen und Bau ──────────────────────────────────────────
if ! ik_gebaut || [ "$NEU_BAUEN" = 1 ]; then
  kopf "ik_llama.cpp bauen"
  if [ ! -d "$IK_DIR/.git" ]; then
    lauf git clone --depth 1 --branch "$IK_REF" "$IK_REPO" "$IK_DIR" \
      || { fehler "git clone fehlgeschlagen — Netz zu github.com? Erneut aufrufen setzt hier fort."; exit 1; }
  elif [ "$NEU_BAUEN" = 1 ]; then
    lauf git -C "$IK_DIR" fetch --depth 1 origin "$IK_REF" && lauf git -C "$IK_DIR" reset --hard FETCH_HEAD \
      || { fehler "Quellen liessen sich nicht aktualisieren — der vorhandene Bau bleibt."; exit 1; }
  fi
  if [ -z "$JOBS" ]; then
    # Die Haelfte der Kerne: der Bau dauert auf 8 Kernen rund 10 bis 20
    # Minuten, und waehrenddessen nimmt die Box weiter auf.
    JOBS=$(( $(nproc 2>/dev/null || echo 2) / 2 )); [ "$JOBS" -ge 1 ] || JOBS=1
  fi
  # GGML_NATIVE: fuer genau diese CPU (AVX2/AVX-512, was sie kann). CUDA
  # bleibt aus — die Box hat keine GPU.
  lauf cmake -S "$IK_DIR" -B "$IK_DIR/build" -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON \
    || { fehler "cmake-Konfiguration fehlgeschlagen (Ausgabe oben)."; exit 1; }
  lauf nice -n 15 cmake --build "$IK_DIR/build" --config Release -j "$JOBS" --target llama-server \
    || { fehler "Bau fehlgeschlagen (Ausgabe oben). Erneut: sudo bash tools/ikllama.sh --neu-bauen"; exit 1; }
  if [ "$TROCKEN" = 0 ]; then
    [ -x "$IK_BIN" ] || { fehler "Bau ohne Ergebnis: %s fehlt." "$IK_BIN_E"; exit 1; }
    _rev="$(git -C "$IK_DIR" rev-parse --short HEAD 2>/dev/null)"; _rev="${_rev:-?}"
    printf '%s\n' "$_rev" | lauf tee "$STEMPEL" >/dev/null
    gut "ik_llama.cpp gebaut (%s)." "$_rev"
  fi
  NEU_GESTARTET=1
fi

# ── Modell ───────────────────────────────────────────────────
if ! modell_fertig; then
  kopf "Modell"
  lauf mkdir -p "$MODELL_VERZ" || { fehler "Ordner nicht anlegbar: %s" "$MODELL_VERZ_E"; exit 1; }
  _url="$HF/$MODELL_REPO/resolve/main/$MODELL_DATEI"
  # Fertig, aber ohne Pruefvermerk (Abbruch nach dem Laden): erst pruefen,
  # nicht neu laden.
  _teil=0; [ -f "$MODELL.teil" ] && _teil="$(wc -c < "$MODELL.teil" | tr -d ' ')"
  # Vollstaendig geladen, aber nie geprueft: kein zweiter Download — curl -C -
  # bekaeme fuer einen Bereich hinter dem Dateiende HTTP 416 und endete mit
  # einem Fehler, obwohl nichts fehlt.
  if [ ! -f "$MODELL" ] && { [ -z "$HF_GROESSE" ] || [ "$_teil" != "$HF_GROESSE" ]; }; then
    info "Lade %s (%s MB) — ein Abbruch wird beim naechsten Aufruf fortgesetzt." "$MODELL_DATEI" "$(mb "$GROESSE")"
    # -C -: Wiederaufnahme an der Stelle, an der .teil endet. --retry gegen
    # kurze Netzaussetzer; ein dauerhafter Fehler endet mit Exit 1 und laesst
    # .teil fuer den naechsten Lauf liegen.
    lauf curl -fL -C - --retry 5 --retry-delay 10 --progress-bar -o "$MODELL.teil" "$_url" \
      || { fehler "Download abgebrochen — erneut aufrufen setzt fort (%s.teil)." "$MODELL_VERZ_E/$MODELL_DATEI"; exit 1; }
  fi
  if [ "$TROCKEN" = 0 ]; then
    _pruef="$MODELL"; [ -f "$MODELL" ] || _pruef="$MODELL.teil"
    _ist="$(wc -c < "$_pruef" | tr -d ' ')"
    if [ -n "$HF_GROESSE" ] && [ "$_ist" != "$HF_GROESSE" ]; then
      fehler "Groesse stimmt nicht: %s Bytes statt %s. Datei bleibt liegen; erneut aufrufen setzt fort." "$_ist" "$HF_GROESSE"
      exit 1
    fi
    if [ "$(head -c 4 "$_pruef")" != "GGUF" ]; then
      fehler "Keine GGUF-Datei (Kennung fehlt): %s — wird entfernt." "$_pruef"
      lauf rm -f "$_pruef"; exit 1
    fi
    info "Pruefe SHA-256 …"
    _sha="$(sha256sum "$_pruef" | cut -d' ' -f1)"
    if [ -n "$HF_SHA" ] && [ "$_sha" != "$HF_SHA" ]; then
      fehler "SHA-256 stimmt nicht: %s statt %s — Datei wird entfernt, erneut aufrufen laedt neu." "$_sha" "$HF_SHA"
      lauf rm -f "$_pruef"; exit 1
    fi
    [ -n "$HF_SHA" ] || warn "Keine Pruefsumme von Hugging Face — nur Groesse und GGUF-Kennung geprueft (SHA-256 %s)." "$_sha"
    [ "$_pruef" = "$MODELL" ] || lauf mv -f "$MODELL.teil" "$MODELL" || exit 1
    printf '%s  %s\n' "$_sha" "$MODELL_DATEI" | lauf tee "$MODELL_OK" >/dev/null
    gut "Modell geprueft: %s" "$MODELL_VERZ_E/$MODELL_DATEI"
  fi
  NEU_GESTARTET=1
fi

# ── Dienst ───────────────────────────────────────────────────
if [ "$NC_INIT" != "systemd" ]; then
  warn "Ohne systemd (gefunden: %s) wird kein Dienst eingerichtet." "$NC_INIT"
  info "Von Hand starten: %s" "$IK_BIN_E -m $MODELL_VERZ_E/$MODELL_DATEI --host 127.0.0.1 --port $PORT -t $THREADS -c $KONTEXT -ngl 0 -rtr --jinja --no-warmup$(kv_schalter)$(tb_schalter)"
  exit 0
fi
kopf "Dienst"
_groesse="$GROESSE"; [ -f "$MODELL" ] && _groesse="$(wc -c < "$MODELL" | tr -d ' ')"
_neu="$(mktemp)"; unit_text "$_groesse" "$_neu"
UNIT_GEAENDERT=0
if [ -f "$UNIT" ] && cmp -s "$_neu" "$UNIT"; then
  gut "%s unveraendert." "$UNIT_NAME"
else
  UNIT_GEAENDERT=1
  if [ -f "$UNIT" ]; then info "geaendert: %s" "${UNIT#"$W"}"; else info "neu: %s" "${UNIT#"$W"}"; fi
  lauf mkdir -p "$(dirname "$UNIT")" && lauf install -m 644 "$_neu" "$UNIT" \
    || { rm -f "$_neu"; fehler "Unit nicht schreibbar: %s" "${UNIT#"$W"}"; exit 1; }
  lauf systemctl daemon-reload || true
fi
rm -f "$_neu"
if [ "$UNIT_GEAENDERT" = 1 ] || [ "${NEU_GESTARTET:-0}" = 1 ]; then
  lauf systemctl enable "$UNIT_NAME" || warn "%s liess sich nicht aktivieren." "$UNIT_NAME"
  lauf systemctl restart "$UNIT_NAME" || { fehler "%s startete nicht — journalctl -u %s -n 50" "$UNIT_NAME" "$UNIT_NAME"; exit 1; }
elif ! systemctl is-active --quiet "$UNIT_NAME" 2>/dev/null; then
  lauf systemctl enable --now "$UNIT_NAME" || { fehler "%s startete nicht — journalctl -u %s -n 50" "$UNIT_NAME" "$UNIT_NAME"; exit 1; }
fi
if [ "$TROCKEN" = 1 ]; then
  info "Trockenlauf beendet — nichts wurde veraendert."
  exit 0
fi

# /health abwarten: 503 heisst "Modell laedt" — mit -rtr und 9 GB dauert das
# Minuten. 500 oder ein gestorbener Dienst ist ein Fehler, kein Warten.
WARTEN="${NC_IK_WARTEN:-600}"
warte_health(){ # -> 0 = 200, 1 = laeuft nicht an / keine Antwort (Grund in _code)
  info "Warte auf http://127.0.0.1:%s/health (bis %s s; das Modell laedt) …" "$PORT" "$WARTEN"
  local _t=0; _code=""
  while :; do
    _code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:$PORT/health" 2>/dev/null)"
    [ "$_code" = "200" ] && return 0
    if [ "$_code" = "500" ] || systemctl is-failed --quiet "$UNIT_NAME" 2>/dev/null; then
      return 1
    fi
    [ "$_t" -ge "$WARTEN" ] && return 1
    sleep 5; _t=$(( _t + 5 ))
  done
}
if ! warte_health; then
  # v5.2-W193: lief er mit quantisiertem KV-Cache nicht an, einmal ohne —
  # ein Schalter, den diese Fassung anders versteht, darf die KI nicht abschalten.
  if [ "$KV_CACHE" != "f16" ] && grep -q -- ' -ctk ' "$UNIT" 2>/dev/null; then
    warn "%s startet mit quantisiertem KV-Cache nicht (HTTP %s) — schreibe die Unit ohne (LLM_KV_CACHE=f16) und versuche es erneut." "$UNIT_NAME" "${_code:-—}"
    KV_CACHE=f16
    _neu="$(mktemp)"; unit_text "$_groesse" "$_neu"
    lauf install -m 644 "$_neu" "$UNIT" || { rm -f "$_neu"; fehler "Unit nicht schreibbar: %s" "${UNIT#"$W"}"; exit 1; }
    rm -f "$_neu"
    lauf systemctl daemon-reload || true
    lauf systemctl restart "$UNIT_NAME" || true
    warte_health || { fehler "%s laeuft auch ohne KV-Quantisierung nicht an (HTTP %s) — journalctl -u %s -n 50" "$UNIT_NAME" "${_code:-—}" "$UNIT_NAME"; exit 1; }
  else
    fehler "%s laeuft nicht an (HTTP %s) — journalctl -u %s -n 50" "$UNIT_NAME" "${_code:-—}" "$UNIT_NAME"
    exit 1
  fi
fi
gut "ik_llama.cpp antwortet auf 127.0.0.1:%s (%s)." "$PORT" "$MODELL_DATEI"
# Ein Satz durch den Chat — /health gruen heisst noch nicht, dass der Chat
# antwortet (W110: mit --embeddings war genau das der Fall).
_antw="$(curl -s --max-time 180 "http://127.0.0.1:$PORT/v1/chat/completions" -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Sag nur: ok /no_think"}],"max_tokens":16,"chat_template_kwargs":{"enable_thinking":false}}' 2>/dev/null)"
if printf '%s' "$_antw" | grep -q '"choices"'; then
  gut "Chat-Probe beantwortet."
else
  warn "Chat-Probe ohne Antwort — der Bot faellt dann auf die Cloud zurueck. Pruefen: journalctl -u %s -n 50" "$UNIT_NAME"
  BEFUND=1
fi
info "Der Bot nutzt es von selbst (AI_PROVIDER=auto), sobald /health antwortet — kein Neustart noetig."
exit "$BEFUND"
