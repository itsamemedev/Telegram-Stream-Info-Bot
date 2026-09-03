#!/usr/bin/env sh
# NIGHTCRAWLER — Mehrsprachigkeit fuer die Shell-Werkzeuge (v4.1-W17)
#
# Dieselbe Regel wie in nc/i18n.py: DER DEUTSCHE TEXT IST DER SCHLUESSEL.
# Fehlt eine Uebersetzung, bleibt Deutsch stehen — nie ein nackter Schluessel,
# nie eine leere Zeile. Ein halb uebersetzter Installer ist unangenehm; einer,
# der bei einer fehlenden Zeile gar nichts sagt, ist gefaehrlich.
#
# UEBERSETZT WIRD AN DER SENKE, nicht an der Aufrufstelle. installer.sh hat 112
# Ausgabe-Aufrufe und motd.sh noch einmal so viele; jeden einzeln zu umschliessen
# waere ein Diff von 250 Zeilen gewesen, bei dem eine vergessene Stelle
# unsichtbar bleibt. Stattdessen laufen info/gut/warn/fehler/erklaere durch t()
# — genau wie _safe_send() im Bot seit v4.1-W7.
#
# Der Katalog ist eine TSV-Datei (deutsch<TAB>englisch), damit er ohne Werkzeug
# lesbar und mit jedem Editor erweiterbar ist. Kein JSON: die Shell haette dafuer
# python3 gebraucht, und der Installer laeuft, BEVOR python3 sichergestellt ist.

NC_TOOLS_I18N_VERSION="1"      # wird von nc_i18n_status ausgegeben (--doctor)

# ── Sprache bestimmen ────────────────────────────────────────
# Reihenfolge: NC_LANG (ausdruecklich) → UI_LANG aus der .env (dieselbe
# Variable, die der Bot benutzt) → LC_ALL/LANG des Systems → Deutsch.
nc_i18n_sprache(){
  _l="${NC_LANG:-}"
  if [ -z "$_l" ] && [ -n "${NC_ENV_FILE:-}" ] && [ -r "${NC_ENV_FILE}" ]; then
    _l="$(sed -n 's/^[[:space:]]*UI_LANG[[:space:]]*=[[:space:]]*//p' "$NC_ENV_FILE" 2>/dev/null | tr -d '"'"'"' \r' | tail -1)"
  fi
  [ -z "$_l" ] && _l="${UI_LANG:-}"
  [ -z "$_l" ] && _l="${LC_ALL:-${LANG:-}}"
  # 'de_DE.UTF-8' → 'de'
  _l="$(printf '%s' "$_l" | cut -c1-2 | tr 'A-Z' 'a-z')"
  case "$_l" in
    en) printf 'en' ;;
    *)  printf 'de' ;;          # alles Unbekannte faellt auf die Quellsprache
  esac
}

NC_LANG_EFF="$(nc_i18n_sprache)"

# Katalog neben locales/ suchen — relativ zum Werkzeug, nicht zum Arbeitsverzeichnis.
# Gesucht wird an drei Orten, in dieser Reihenfolge: neben DIESER Datei (bash
# verraet das ueber BASH_SOURCE), neben dem AUFRUFENDEN Skript, und zuletzt im
# Arbeitsverzeichnis. Der erste Weg ist der verlaessliche — $0 ist beim Sourcen
# aus einer Subshell heraus nicht das, was man erwartet, und genau daran waere
# die Suche sonst still gescheitert.
if [ -z "${NC_I18N_KATALOG:-}" ]; then
  _selbst=""
  [ -n "${BASH_SOURCE:-}" ] && _selbst="$(cd "$(dirname "${BASH_SOURCE%% *}")" 2>/dev/null && pwd)"
  _ruf="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
  for _k in "$_selbst/../../locales/tools.$NC_LANG_EFF.tsv" \
            "$_ruf/../locales/tools.$NC_LANG_EFF.tsv" \
            "$_ruf/../../locales/tools.$NC_LANG_EFF.tsv" \
            "./locales/tools.$NC_LANG_EFF.tsv"; do
    [ -n "$_k" ] && [ -r "$_k" ] && { NC_I18N_KATALOG="$_k"; break; }
  done
fi

# ── t: uebersetzen oder unveraendert durchreichen ────────────
# Bewusst ohne Cache-Datei und ohne assoziatives Array: der Installer laeuft
# einmal, und POSIX-sh hat keine Arrays. Ein grep je Zeile ist bei ~250 Zeilen
# nicht messbar — und diese Loesung laeuft auch in der dash, mit der Debian
# /bin/sh besetzt.
t(){
  _s="$*"
  [ "$NC_LANG_EFF" = "de" ] && { printf '%s' "$_s"; return; }
  [ -n "${NC_I18N_KATALOG:-}" ] && [ -r "$NC_I18N_KATALOG" ] || { printf '%s' "$_s"; return; }
  _tr="$(awk -v k="$_s" -F '\t' '$1==k {print $2; found=1; exit} END{if(!found) exit 1}' \
         "$NC_I18N_KATALOG" 2>/dev/null)" || { printf '%s' "$_s"; return; }
  [ -n "$_tr" ] && printf '%s' "$_tr" || printf '%s' "$_s"
}

# Wie viel ist abgedeckt? Fuer tools/i18n_tools.py --check und den --doctor.
nc_i18n_status(){
  printf 'i18n:    Fassung %s\n' "$NC_TOOLS_I18N_VERSION"
  printf 'Sprache: %s\n' "$NC_LANG_EFF"
  if [ -n "${NC_I18N_KATALOG:-}" ] && [ -r "$NC_I18N_KATALOG" ]; then
    printf 'Katalog: %s (%s Eintraege)\n' "$NC_I18N_KATALOG" \
      "$(grep -cv '^[[:space:]]*\(#\|$\)' "$NC_I18N_KATALOG" 2>/dev/null || echo 0)"
  else
    printf 'Katalog: keiner geladen — Ausgabe bleibt deutsch\n'
  fi
}
