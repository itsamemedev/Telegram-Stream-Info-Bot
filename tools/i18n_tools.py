#!/usr/bin/env python3
"""i18n_tools — Abdeckung des Shell-Katalogs pruefen (v4.1-W17, scharf seit v4.2-W123).

Das Gegenstueck zu tools/i18n_extract.py, nur fuer die SHELL-Werkzeuge. Es
sammelt die Texte, die durch die uebersetzenden Senken von installer.sh,
update.sh, motd.sh, tools/lib/*.sh und install.bat laufen, und vergleicht sie
mit locales/tools.<lang>.tsv.

    python3 tools/i18n_tools.py --liste          was gefunden wurde
    python3 tools/i18n_tools.py --check en       Abdeckung pruefen (CI-Tor)

SEIT v4.2-W123 SCHEITERT --check AUCH AN FEHLENDEN EINTRAEGEN. Bis dahin galt
"fehlend ist nur eine Luecke". Zur LAUFZEIT stimmt das weiter — eine fehlende
Zeile bleibt deutsch, nie ein nackter Schluessel (lib/i18n.sh). Als Pruefung
war es aber genau die Zahl, die niemand liest: eine Luecke, die die CI nicht
rot macht, waechst.

UND DIE 100 % WAREN GESCHOENT. Gemessen vor W123: der Sammler meldete 373 von
373, waehrend im englischen Lauf rund 150 Zeilen deutsch blieben. Fuenf blinde
Flecken, jeder davon steht unten an seinem Ausdruck:

  * einfach gequotete printf-Formate ('  %sZielverzeichnis: %s%s\\n'),
  * Senken-Texte mit Laufzeitwert ("Python gefunden: $PY") — t() schlaegt den
    ZUSAMMENGESETZTEN Text nach und trifft nie; 45 Stellen in installer.sh,
  * Heredocs (--help, Willkommen),
  * merke, kopf und Durchreich-Helfer (opt_frage, restream_ziel), die ihren
    Text an eine Senke weitergeben, deren Aufrufer aber nie eingesammelt wurden,
  * Dateien, die der Betreiber LIEST (Installationsnotiz, start.bat).

Die Antwort auf den zweiten Fleck ist tf FORMAT ARG… (lib/i18n.sh): der
Schluessel ist das Format mit %s, der Wert kommt erst danach hinein. Die
Senken nehmen dieselbe Form an (info "Python gefunden: %s" "$PY").
"""

import glob
import io
import os
import re
import shlex
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLEN = ("tools/installer.sh", "tools/motd.sh", "tools/update.sh")
# v4.2-W123: tools/lib/ mit. Die Bibliotheken werden von allen Werkzeugen
# gesourct und geben selbst aus (Paketwahl, i18n-Status) — eine deutsche
# Zeile dort erscheint in JEDEM Werkzeug.
QUELLEN_LIB = "tools/lib/*.sh"
# v4.2-W8: der Windows-Installer. Er stand bis hierher nicht einmal in dieser
# Liste — der Prüfer meldete deshalb 100 % Abdeckung für ein Werkzeug, das er
# gar nicht ansah. Batch hat eine eigene Aufrufform (`call :senke "text"`) und
# braucht deshalb einen eigenen Ausdruck; dieselbe Datei tools.en.tsv trägt
# beide Installer.
QUELLEN_BAT = ("tools/install.bat",)


def shell_quellen():
    """Alle Shell-Quellen, die es gibt — feste Liste plus tools/lib/."""
    raus = [q for q in QUELLEN if os.path.exists(os.path.join(ROOT, q))]
    for p in sorted(glob.glob(os.path.join(ROOT, QUELLEN_LIB))):
        raus.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return raus


# Ein Literal in einer der beiden Quote-Formen. Doppelt gequotet: ohne $, `
# und Backslash — alles davon ist zur Laufzeit zusammengesetzt bzw. maskiert
# und taugt nicht als Schluessel. Einfach gequotet ist in der Shell IMMER
# woertlich; bis W123 sah der Sammler diese Form gar nicht.
_DQ = r'"([^"\\$`]{%d,})"'
_SQ = r"'([^'\n]{%d,})'"


def _beide(vorne, mindest):
    """Ausdruck fuer `vorne` + Literal in "…" oder '…' -> zwei Gruppen."""
    return re.compile(vorne + r"(?:" + (_DQ % mindest) + r"|" + (_SQ % mindest) + r")", re.M)


# Die Senken, die durch t()/tf() laufen. Nicht am Zeilenanfang verankert: die
# Senken stehen oft hinter && oder || ("... && gut "..." || warn "...""
# ueber zwei Zeilen). Ein Anker auf ^ hat genau die uebersehen — und sie
# tauchten dann als "verwaist" auf, obwohl sie im Quelltext stehen.
# v4.2-W123: kopf und merke dazu. kopf gab seine Schrittnamen roh aus, merke
# schrieb den Merkzettel roh — beide standen im englischen Lauf deutsch da.
# Was vor einem Senken-Aufruf stehen darf. v4.2-W123: `)` dazu — ein
# Aufruf direkt im case-Zweig (`express) info "…";;`) fiel durch, und die
# Betriebsart stand im englischen Lauf deutsch da. Gefunden hat das der echte
# Installer-Lauf mit NC_LANG=en, nicht die Quote.
_VOR_SENKE = r'(?:^|&&|\|\||[;{()]|\bthen|\belse|\bdo)\s*'
_SENKEN_NAMEN = r"(?:info|gut|warn|fehler|erklaere|merke|kopf|abschnitt|nz)"
_SENKEN = _beide(_VOR_SENKE + _SENKEN_NAMEN + r'\s+', 4)
_FRAGEN = _beide(r'(?:frage_ja|frage_text|frage_geheimnis|frage_wahl)\s+(?:\w+\s+)?', 4)

# v4.2-W14: motd.sh hat EIGENE Senken (sect/row/gauge) und umschliesst den Rest
# ausdruecklich mit t(). Die Senken von installer.sh gibt es dort nicht — und
# genau deshalb sammelte der Pruefer bisher NICHTS aus motd.sh und meldete
# trotzdem 100 % Abdeckung. Eine Zahl, die nur zaehlt, was sie ohnehin kennt.
_MOTD_SENKEN = re.compile(r'(?:^|\s)(?:sect|row|gauge)\s+"([^"\\$`]{2,})"', re.M)
# lage_setz traegt den Text der Gesamtampel. Er wird erst beim Zeichnen
# uebersetzt ($(t "$LAGE_TEXT")), muss aber hier eingesammelt werden —
# sonst fehlt genau die Zeile im Katalog, die als erste ins Auge faellt.
_LAGE = re.compile(r'(?:^|\s)lage_setz\s+(?:err|warn)\s+"([^"\\$`]{2,})"', re.M)
# Ausdrueckliche Umschliessung, in allen Schreibweisen: t "…", t '…', $(t …),
# und seit W123 tf mit Format als erstem Argument.
_T_AUFRUF = _beide(r'(?:\$\(|(?:^|\s))tf?\s+', 2)

# v4.2-W123: Helfer, die ein Argument an eine Senke DURCHREICHEN. Ihre
# Aufrufer tragen den Text — ohne diese Tabelle sammelt niemand ihn ein, und
# die Zeile bleibt deutsch, waehrend die Quote 100 % meldet. Name -> Position
# (1-basiert) des Textarguments. Ein neuer Durchreicher gehoert hierher; der
# Vertrag _test_v42_w123_* faellt, wenn eine Senke "$var" aus einem
# Positionsparameter bekommt, dessen Helfer hier fehlt.
DURCHREICHER = {"opt_frage": 3, "restream_ziel": 3, "baustein": 3}

# Heredocs, die zeilenweise uebersetzt werden: tz <<'MARKE' … MARKE.
_TZ_HEREDOC = re.compile(r"\btz\s+<<-?\s*'?(\w+)'?\s*\n(.*?)\n\s*\1\s*$", re.M | re.S)

# Die Senken von tools/install.bat. Erfasst wird das ERSTE Argument — ausser
# bei :wert_gut, wo der Wert vorne steht und der feste Text hinten.
# Kein %: was einen Wert traegt, kann kein Schluessel sein (der Wert steht erst
# zur Laufzeit fest). Genau dafuer gibt es die *_wert-Senken.
_BAT_SENKEN = re.compile(
    r'\bcall :(?:kopf|info|info_wert|gut|gut_wert|warn|fehler|fehler_wert|'
    r'erklaere|merken|merken_wert|zeile|zeile2|zeile_wert|zeile_wert2|'
    r'zeile2_wert|punkt|t|notiz|notiz_wert)\s+"([^"%]{3,})"')
_BAT_WERT_GUT = re.compile(r'\bcall :wert_gut\s+"[^"]*"\s+"([^"%]{3,})"')
_BAT_FRAGEN = re.compile(
    r'\bcall :(?:frage_ja|frage_text|frage_geheimnis|frage_wahl)\s+(?:[JN0-9]\s+)?"([^"%]{3,})"')


def _durchreicher_texte(text):
    raus = set()
    for zeile in text.split("\n"):
        st = zeile.strip()
        if not st or st.startswith("#"):
            continue
        name = st.split(None, 1)[0]
        pos = DURCHREICHER.get(name)
        if not pos or st.startswith(name + "(){"):
            continue
        try:
            teile = shlex.split(st, comments=True)
        except ValueError:
            continue
        if len(teile) > pos:
            wert = teile[pos]
            if wert and "$" not in wert and "`" not in wert:
                raus.add(wert)
    return raus


def _wahl_texte(text):
    """Die Beschriftungen von frage_wahl — jedes zweite Argument ab dem fuenften.

    v4.2-W124: frage_wahl VAR "Frage" VORGABE schl1 "Text 1" schl2 "Text 2" …
    Die Frage faengt _FRAGEN; die Beschriftungen stehen hinter Schluesseln und
    oft ueber Fortsetzungszeilen verteilt. Ohne diesen Sammler blieben genau
    die Zeilen deutsch, zwischen denen ein englischer Nutzer waehlen soll.
    """
    raus = set()
    logisch = re.sub(r"\\\n\s*", " ", text)
    for zeile in logisch.split("\n"):
        st = zeile.strip()
        if not st.startswith("frage_wahl ") or st.startswith("frage_wahl(){"):
            continue
        try:
            teile = shlex.split(st, comments=True)
        except ValueError:
            continue
        for wert in teile[5::2]:
            if wert and "$" not in wert and "`" not in wert:
                raus.add(wert)
    return raus


def _zwei(treffer):
    return {a or b for a, b in treffer if (a or b)}


def sammeln_shell(text):
    # Der Kommentar hinter einer Funktionskopfzeile beschreibt die Aufrufform
    # (`frage_geheimnis(){ # frage_geheimnis VARIABLE "Beschreibung" …`) und
    # ist kein Ausgabetext — ohne das landete "Beschreibung" im Katalog.
    text = re.sub(r"\(\)\s*\{\s*#.*$", "(){", text, flags=re.M)
    # Ebenso ganze Kommentarzeilen: lib/ausgabe.sh beschreibt dort die
    # Aufrufform (# info "Gefunden: %s" "$pfad") — das ist Doku, keine Ausgabe.
    text = re.sub(r"^[ \t]*#.*$", "", text, flags=re.M)
    raus = set()
    raus |= _zwei(_SENKEN.findall(text))
    raus |= _zwei(_FRAGEN.findall(text))
    raus |= set(_MOTD_SENKEN.findall(text))
    raus |= set(_LAGE.findall(text))
    for wert in _zwei(_T_AUFRUF.findall(text)):
        # "$LAGE_TEXT" ist eine Variable, kein Schluessel — ihre Werte
        # stehen an den lage_setz-Aufrufstellen und werden dort erfasst.
        if not wert.startswith("$"):
            raus.add(wert)
    raus |= _durchreicher_texte(text)
    raus |= _wahl_texte(text)
    for _marke, rumpf in _TZ_HEREDOC.findall(text):
        for z in rumpf.split("\n"):
            if z.strip():
                raus.add(z.strip())
    return raus


def sammeln():
    raus = set()
    for rel in shell_quellen():
        raus |= sammeln_shell(io.open(os.path.join(ROOT, rel), encoding="utf-8").read())
    for rel in QUELLEN_BAT:
        pfad = os.path.join(ROOT, rel)
        if not os.path.exists(pfad):
            continue
        text = io.open(pfad, encoding="utf-8").read()
        raus |= set(_BAT_SENKEN.findall(text))
        raus |= set(_BAT_WERT_GUT.findall(text))
        raus |= set(_BAT_FRAGEN.findall(text))
        # v4.2-W124: die Optionen von :frage_wahl — alle Literale der Zeile.
        for zeile in text.split("\n"):
            m = re.search(r"\bcall :frage_wahl\s", zeile)
            if m:
                # Erst AB dem Aufruf: davor steht oft ein if "%A%"=="11", und
                # zwischen dessen Anfuehrungszeichen laege sonst " call … 1 ".
                raus |= set(re.findall(r'"([^"%]{3,})"', zeile[m.end():]))
    return raus


# Deutsche Marker — dieselbe Idee wie in tools/i18n_extract.py.
# v4.2-W123: ohne Gross-/Kleinschreibung ("BEDIENUNG", "WEITERLESEN" standen
# in der Installationsnotiz und fielen durch) und um die Woerter erweitert, die
# der verschaerfte Lauf in den Werkzeugen gefunden hat. Ein Marker-Satz, den
# man nicht nachzieht, wird blind — deshalb steht jede Erweiterung mit ihrem
# Fund im Vertrag.
_DEUTSCH = re.compile(
    r"[ÄÖÜäöüß]|\b(?:der|die|das|den|dem|des|ein|eine|einen|und|oder|nicht|kein|"
    r"keine|keinen|wird|wurde|werden|ist|sind|war|hat|haben|kann|koennen|muss|"
    r"muessen|soll|noch|schon|nur|auch|mehr|alle|alles|jede|jeder|beim|vom|zum|"
    r"zur|fuer|mit|ohne|nach|vor|ueber|unter|seit|bitte|wenn|dann|"
    r"fehler|datei|dateien|grund|stand|wert|seite|gefunden|laeuft|fehlt|fehlen|"
    r"unbekannt|unbekannte|unbekannter|gestoppt|aktiv|inaktiv|"
    # v4.2-W14: Beschriftungen der MOTD, die keinen der Marker oben tragen.
    r"kerne|netz|platte|werkzeuge|aufnahmen|erkennung|sicherung|vorschau|"
    # v4.2-W123: Funde aus Installer, Notiz und MOTD-Hilfe.
    r"verzeichnis|dienst|dienste|konfiguration|bedienung|weiterlesen|schritte|"
    r"merkzettel|eingeben|sicherheit|wiederholen|erzeugt|wege|meist|ziele|"
    r"leistungsprofil|handstart|selbsttest|einstieg|ausliefern|abwehr|"
    r"mitlesen|starten|anschreiben|oeffnen|gedaempft|beiseitegelegt|"
    r"wiederhergestellt|aenderbar|fehlgeschlagen|installiert|eingetragen|"
    r"entfernt|einhaengen|daempfen|fassung|vorgabe|beispiel|getrackt|gesamt|"
    r"datenbank|willkommen|schalter|zweig|pfad|unterstuetzt|bereits|erkannt|"
    r"neustart|zusammenfassung|pakete|paket|rechte|geheimnisse|zuschauen|"
    r"aktualisieren|beendet|fenster|schliessen|taste|beliebigen|"
    r"pflichtteil|uebersicht|funktionen|betriebsart|fragen|weg|schritt|"
    r"pruefen|sicherstellen|zielverzeichnis|quelltext|systempakete|"
    r"bausteine|optionale|ausgelassen|nachinstalliert|aktuell|vorhanden)\b",
    re.I)
# Was wie deutscher Text aussieht und keiner ist.
_KEIN_TEXT = ("NIGHTCRAWLER", "CROWDSEC", "DASHBOARD")

# Aufrufe, deren erstes Literal ohnehin durch t()/tf() laeuft.
_UMSCHLOSSEN = (
    r'(?:info|gut|warn|fehler|erklaere|merke|merken|kopf|abschnitt|nz|sect|row|gauge|'
    r'frage_ja|frage_text|frage_geheimnis|frage_wahl|tz|' +
    "|".join(DURCHREICHER) + r')\s+(?:\w+\s+)?')


def _literale(roh):
    """Beide Quote-Formen; Inhalt jedes Literals."""
    return [a or b for a, b in re.findall(r'"([^"]{4,})"|\'([^\'\n]{4,})\'', roh)]


def _klar(lit):
    # v4.2-W123: Vorgabewerte ${X:-Text} sind Ausgabe. Vorher fiel die ganze
    # Ersetzung weg — und mit ihr "— nicht gefunden" aus dem --doctor.
    lit = re.sub(r"\$\{\w+:?[-=?+]([^}]*)\}", r" \1 ", lit)
    klar = re.sub(r"\$\{[^}]*\}|\$\([^)]*\)|\$\w+|%[-0-9.]*[a-zA-Z]|\\[ntre]|\\033\[[0-9;]*m",
                  " ", lit)
    return " ".join(klar.split())


def unumschlossen(rel):
    """Deutscher Ausgabetext, der an KEINER Senke haengt. -> [(zeile, text)]

    Das ist die ehrliche Haelfte der Abdeckung. Die Quote oben sagt nur, wie
    viel von dem uebersetzt ist, was der Sammler FINDET — sie kann 100 %
    melden, waehrend eine ganze Datei deutsch bleibt. Genau das war bis
    v4.2-W14 der Fall: motd.sh band lib/i18n.sh ein und rief t() nie auf.
    Und bis v4.2-W123 noch einmal: dieser Melder sah nur "…", nie '…'.
    """
    pfad = os.path.join(ROOT, rel)
    if not os.path.exists(pfad):
        return []
    if rel.endswith(".bat"):
        return _unumschlossen_bat(pfad)
    raus = []
    zeilen = io.open(pfad, encoding="utf-8").read().split("\n")
    heredoc = None          # (marke, ist_ausgabe)
    for nr, zeile in enumerate(zeilen, 1):
        roh = zeile.strip()
        if heredoc:
            if roh == heredoc[0]:
                heredoc = None
            elif heredoc[1] and roh and _DEUTSCH.search(_klar(roh)):
                raus.append((nr, _klar(roh)[:70]))
            continue
        if roh.startswith("#") or not roh:
            continue
        # v4.2-W123: Heredocs. `cat <<X` ohne Umleitung ist Bildschirmausgabe
        # (--help, Willkommen) und stand komplett deutsch da. In eine Datei
        # (cat > f <<X, tee f <<X) gehen Units und Konfiguration — Kommentare
        # darin sind fuer systemd/nginx, nicht fuer den Betreiber im Dialog.
        # Die Marke beginnt mit einem Buchstaben: `$((1<<2))` ist eine
        # Verschiebung, kein Heredoc — sonst verschluckte der Melder den Rest
        # der Datei bis zu einer Zeile "2".
        m = re.search(r"<<-?\s*'?([A-Za-z_]\w*)'?", roh)
        if m and "<<<" not in roh:
            ausgabe = bool(re.search(r"\bcat\s+<<", roh)) and ">" not in roh.split("<<")[0]
            heredoc = (m.group(1), ausgabe)
            continue
        # Was ist Ausgabe? Drei Merkmale, und alle drei sind noetig:
        #   * printf/echo — der offensichtliche Fall;
        #   * lage_setz — die Gesamtampel, die ihren Text erst spaeter zeichnet;
        #   * ein FARBCODE im Literal. Eine Zeichenkette mit ${FNT} darin ist
        #     per Bauart Anzeige, egal ob sie in eine Variable geht.
        _farbe = re.search(r'"\s*[^"]*\$\{(?:FNT|TXT|WRN|ERR|OK|DIM|BR|B)\}', roh)
        if not (re.search(r"\b(?:printf|echo|lage_setz)\b", roh) or _farbe):
            continue
        # Umschliessungen ZUERST herausschneiden. Sonst zieht der Melder die
        # innere Zeichenkette aus $(t "…") heraus und meldet ausgerechnet das
        # als unumschlossen — ein Melder mit Fehlalarm wird nicht gelesen,
        # und dann faellt der echte Befund mit durch.
        ohne_t = re.sub(r'\$\(tf?\s+(?:"[^"]*"|\'[^\']*\')', "\x00", roh)
        ohne_t = re.sub(r'(?:^|\s)tf?\s+(?:"[^"]*"|\'[^\']*\')', "\x00", ohne_t)
        # Und die Senken mit ihrem ersten Argument: die laufen ohnehin durch
        # t(). Ohne das meldet jede Zeile, die zufaellig ein `echo` als
        # Vorgabewert traegt, ihren Fragetext als unumschlossen.
        ohne_t = re.sub(r'(?:^|\s)' + _UMSCHLOSSEN + r'(?:"[^"]*"|\'[^\']*\')', "\x00", ohne_t)
        ohne_t = re.sub(r'lage_setz\s+(?:err|warn)\s+"[^"]*"', "\x00", ohne_t)
        # awk-/sed-Programme sind Code, kein Text.
        ohne_t = re.sub(r"\b(?:awk|sed)\b.*$", "\x00", ohne_t)
        for lit in _literale(ohne_t):
            klar = _klar(lit)
            if len(klar) < 4 or klar in _KEIN_TEXT:
                continue
            if _DEUTSCH.search(klar):
                raus.append((nr, klar[:70]))
    return raus


def _unumschlossen_bat(pfad):
    """install.bat: echo-Zeilen mit deutschem Text, auch in Dateien.

    v4.2-W123: die Installationsnotiz und start.bat werden per
    `>>"%NOTIZ%" echo …` geschrieben — und gelesen werden sie vom Betreiber.
    Der Vertrag aus W8 ueberspringt Umleitungen (Bildschirm), dieser Melder
    nicht: eine Notiz, die auf Englisch deutsch ist, ist dieselbe Luecke.
    """
    raus = []
    for nr, zeile in enumerate(io.open(pfad, encoding="utf-8"), 1):
        st = zeile.strip()
        if st.lower().startswith("rem") or st.startswith("::"):
            continue
        m = re.search(r'(?<![>\w])echo\s+(\S.*)$', zeile)
        if not m:
            continue
        rest = re.sub(r"%[~\w]*%|%~\d|\^.", " ", m.group(1))
        klar = " ".join(rest.split())
        if len(klar) < 4:
            continue
        if _DEUTSCH.search(klar):
            raus.append((nr, klar[:70]))
    return raus


# v4.2-W123: Senken-Texte, die zur Laufzeit zusammengesetzt werden. t() schlaegt
# den FERTIGEN Text nach — "Python gefunden: /usr/bin/python3" trifft nie
# einen Schluessel, die Zeile bleibt deutsch, und keine Quote zeigt es, weil
# der Sammler Literale mit $ zu Recht nicht einsammelt. 45 solche Stellen
# standen in installer.sh. Erlaubt sind nur zwei Formen ohne Literal-Anteil:
# eine blanke Variable (Durchreichen, der Text steht beim Aufrufer) und eine
# vollstaendige $(t …)/$(tf …)-Umschliessung.
_SENKE_MIT_WERT = re.compile(
    _VOR_SENKE +
    r'(?:info|gut|warn|fehler|erklaere|merke|kopf|abschnitt|nz|sect|row|gauge|'
    r'frage_ja|frage_text\s+\w+|frage_geheimnis\s+\w+|frage_wahl\s+\w+)\s+"((?:[^"\\]|\\.)*)"')


# "$(t …)" / "$(tf …)" als GANZES Argument, mit bis zu zwei Ebenen innerer
# Klammern ("$(tf '%s: …' "$(t "$was")")").
_GANZ_UMSCHLOSSEN = re.compile(
    r'"\$\(tf?\s(?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)"')


def zusammengesetzt(rel):
    """Senken-Aufrufe mit Laufzeitwert im Text -> [(zeile, text)]."""
    pfad = os.path.join(ROOT, rel)
    if not os.path.exists(pfad) or rel.endswith(".bat"):
        return []
    raus = []
    for nr, zeile in enumerate(io.open(pfad, encoding="utf-8"), 1):
        if zeile.strip().startswith("#"):
            continue
        # Vollstaendig umschlossene Argumente vorher herausnehmen. Der
        # Ausdruck darunter endet am ersten inneren Anfuehrungszeichen und
        # saehe in "$(tf '%s eingeben' "$was")" sonst einen halben Text.
        zeile = _GANZ_UMSCHLOSSEN.sub('""', zeile)
        for lit in _SENKE_MIT_WERT.findall(zeile):
            if "$" not in lit and "`" not in lit:
                continue
            if re.fullmatch(r"\$\{?\w+\}?", lit) or re.fullmatch(r"\$\(tf?\s.*\)", lit):
                continue
            raus.append((nr, lit[:70]))
    return raus


def katalog(sprache):
    pfad = os.path.join(ROOT, "locales", "tools.%s.tsv" % sprache)
    aus = {}
    if not os.path.exists(pfad):
        return aus
    for zeile in io.open(pfad, encoding="utf-8"):
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        teile = zeile.rstrip("\n").split("\t")
        if len(teile) >= 2 and teile[0] and teile[1]:
            aus[teile[0]] = teile[1]
    return aus


_PLATZHALTER = re.compile(r"%[-0-9.]*[sdbfx%]")


def platzhalter_bruch(kat):
    """Eintraege, deren Uebersetzung andere printf-Platzhalter traegt.

    v4.2-W123: mit tf ist der Schluessel ein printf-FORMAT. Eine Uebersetzung
    mit einem %s weniger schiebt jeden Wert eine Stelle nach vorn, eine mit
    einem mehr druckt eine leere Stelle — beides ohne Fehlermeldung. Die
    Reihenfolge muss gleich bleiben; umstellen geht nur ueber den Satzbau.
    """
    return sorted(k for k, v in kat.items()
                  if _PLATZHALTER.findall(k) != _PLATZHALTER.findall(v))


def main():
    args = sys.argv[1:]
    gefunden = sammeln()
    quellen = shell_quellen() + list(QUELLEN_BAT)
    if "--liste" in args:
        for s in sorted(gefunden):
            print(s)
        print("\n%d uebersetzbare Zeichenketten in %d Dateien" % (len(gefunden), len(quellen)))
        return 0
    sprache = "en"
    if "--check" in args:
        i = args.index("--check")
        if i + 1 < len(args):
            sprache = args[i + 1]
    kat = katalog(sprache)
    fehlt = sorted(gefunden - set(kat))
    verwaist = sorted(set(kat) - gefunden)
    quote = (100.0 * (len(gefunden) - len(fehlt)) / len(gefunden)) if gefunden else 100.0
    print("gefunden: %d Zeichenketten in %d Werkzeugen" % (len(gefunden), len(quellen)))
    print("Katalog %s: %d Eintraege | fehlend: %d | verwaist: %d | Abdeckung: %.1f%%"
          % (sprache, len(kat), len(fehlt), len(verwaist), quote))
    # v4.2-W14: die EHRLICHE Haelfte. Die Quote oben sagt nur, wie viel von
    # dem uebersetzt ist, was der Sammler findet — sie kann 100 % melden,
    # waehrend eine ganze Datei deutsch bleibt.
    offen = []
    gebaut = []
    for rel in quellen:
        for nr, txt in unumschlossen(rel):
            offen.append("%s:%d: %s" % (rel, nr, txt))
        for nr, txt in zusammengesetzt(rel):
            gebaut.append("%s:%d: %s" % (rel, nr, txt))
    bruch = platzhalter_bruch(kat)
    print("unumschlossene deutsche Ausgabe: %d" % len(offen))
    print("zur Laufzeit zusammengesetzte Senken-Texte: %d" % len(gebaut))
    print("Platzhalter-Brueche im Katalog: %d" % len(bruch))
    for o in offen:
        print("  unumschlossen: %s" % o)
    for g in gebaut:
        print("  zusammengesetzt: %s" % g)
    for b in bruch[:20]:
        print("  platzhalter: %s" % b[:100])
    for v in verwaist[:20]:
        print("  verwaist: %s" % v[:100])
    for f in fehlt:
        print("  fehlend: %s" % f[:100])
    befund = False
    if verwaist:
        # Ein Eintrag ohne Quelle heisst: der deutsche Text wurde geaendert und
        # der Katalog nicht nachgezogen. Ab jetzt bleibt diese Zeile fuer immer
        # deutsch, ohne dass es jemand merkt — DAS ist der Fehler.
        print("FEHLER: verwaiste Eintraege — deutscher Text geaendert?")
        befund = True
    if offen:
        # Hartes Tor, und zwar bei NULL. Eine Ausnahmeliste "vier bekannte
        # Faelle" verrottet: nach dem fuenften liest niemand mehr hin.
        print("FEHLER: deutsche Ausgabe an keiner Senke — sie bleibt fuer "
              "immer deutsch, ohne dass die Abdeckung es zeigt")
        befund = True
    if gebaut:
        print("FEHLER: Senken-Text mit Laufzeitwert — t() trifft ihn nie. "
              "Form: info \"Text %s\" \"$wert\" (tf, lib/i18n.sh)")
        befund = True
    if bruch:
        print("FEHLER: Uebersetzung traegt andere printf-Platzhalter als der Schluessel")
        befund = True
    if fehlt:
        # v4.2-W123: zur Laufzeit faellt eine fehlende Zeile auf Deutsch
        # zurueck — das bleibt so. Als Pruefung ist sie ein Befund: eine
        # Luecke, die die CI nicht rot macht, waechst.
        print("FEHLER: %d Zeichenketten ohne Uebersetzung (%s)" % (len(fehlt), sprache))
        befund = True
    return 1 if befund else 0


if __name__ == "__main__":
    sys.exit(main())
