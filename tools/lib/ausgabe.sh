#!/usr/bin/env sh
# NIGHTCRAWLER — gemeinsame Ausgabe-Senken fuer die Shell-Werkzeuge (v4.2-W123)
#
# Dieselben Senken wie in installer.sh (info/gut/warn/fehler/erklaere/kopf),
# hier als Bibliothek fuer tools/update.sh und alles, was danach kommt. Jede
# Senke laeuft durch tf (lib/i18n.sh): ein Text ist Schluessel, Laufzeitwerte
# kommen als weitere Argumente (info "Gefunden: %s" "$pfad"). Genau diese Form
# prueft tools/i18n_tools.py — ein Text mit $ im Literal macht die CI rot.
#
# POSIX-sh: die CI prueft tools/lib/ mit `shellcheck -s sh`.
#
# Erwartet: lib/i18n.sh ist bereits gesourct (t, tf).
#
# Steuerung:
#   NC_FARBE=0|1     Farben (Vorgabe: 1 bei Terminal)
#   NC_MODUS=gefuehrt|express|unattended  — bestimmt, ob frage_ja fragt

nc_farben(){
  if [ "${NC_FARBE:-1}" = 1 ] && [ -t 1 ]; then
    _e="$(printf '\033')"
    B="${_e}[1m"; R="${_e}[0m"
    BR="${_e}[38;5;179m"; DIM="${_e}[38;5;136m"; TXT="${_e}[38;5;187m"
    FNT="${_e}[38;5;101m"; OK="${_e}[38;5;107m"; WRN="${_e}[38;5;173m"; ERR="${_e}[38;5;167m"
  else
    B=""; R=""; BR=""; DIM=""; TXT=""; FNT=""; OK=""; WRN=""; ERR=""
  fi
}
nc_farben

info(){ printf '  %s▸%s %s\n' "$DIM" "$R" "$(tf "$@")"; }
gut(){  printf '  %s✔%s %s\n' "$OK" "$R" "$(tf "$@")"; }
warn(){ printf '  %s▲%s %s\n' "$WRN" "$R" "$(tf "$@")"; }
fehler(){ printf '  %s✘%s %s\n' "$ERR" "$R" "$(tf "$@")" >&2; }
erklaere(){ printf '%s' "$FNT"; printf '%s\n' "$(tf "$@")" | fold -s -w 72 | sed 's/^/    /'; printf '%s' "$R"; }
kopf(){ printf '\n%s%s%s%s\n' "$BR" "$B" "$(t "$1")" "$R"; }
abschnitt(){ printf '\n  %s%s%s%s\n' "$B" "$TXT" "$(t "$1")" "$R"; }

# Tastatur auch dann, wenn das Skript per Pipe kommt (curl … | bash). Ohne
# TTY gibt es keine Fragen — dann gilt die Vorgabe, und zwar laut: der
# Aufrufer erfaehrt ueber NC_MODUS=unattended, dass nicht gefragt wurde.
NC_TTY=""
if [ -t 0 ]; then NC_TTY="/dev/stdin"; elif [ -r /dev/tty ] && (: < /dev/tty) 2>/dev/null; then NC_TTY="/dev/tty"; fi

# frage_ja "Frage" [J|N] -> 0 = ja. Ohne Rueckfrage im Modus unattended und
# ohne TTY; dann entscheidet die Vorgabe.
frage_ja(){
  _f="$1"; _vor="${2:-J}"
  if [ "${NC_MODUS:-gefuehrt}" = "unattended" ] || [ -z "$NC_TTY" ]; then [ "$_vor" = "J" ]; return; fi
  while :; do
    if [ "$_vor" = "J" ]; then _k="$(t '[J/n]')"; else _k="$(t '[j/N]')"; fi
    printf '  %s?%s %s %s%s%s ' "$BR" "$R" "$(t "$_f")" "$FNT" "$_k" "$R"
    _a=""; read -r _a < "$NC_TTY" || _a=""
    _a="$(printf '%s' "$_a" | tr 'A-Z' 'a-z')"
    case "$_a" in
      j|ja|y|yes) return 0;;
      n|nein|no)  return 1;;
      "") [ "$_vor" = "J" ]; return;;
      *) warn "Bitte j oder n.";;
    esac
  done
}
