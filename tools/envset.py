#!/usr/bin/env python3
"""envset — Werte in einer .env setzen, lesen und Platzhalter heilen.

WARUM ES DAS GIBT
tools/install.bat muss dieselbe .env schreiben wie tools/installer.sh. In
Batch ist das nicht sicher hinzubekommen: cmd.exe kennt kein sed, und ein
Wert mit Leerzeichen, Prozentzeichen oder Anfuehrungszeichen zerlegt jede
For-Schleife. Deshalb macht es hier Python — der Interpreter steht zu diesem
Zeitpunkt ohnehin schon, sonst waere die Installation nicht so weit gekommen.

Der Wert kommt bewusst NICHT ueber die Kommandozeile, sondern ueber die
Umgebungsvariable NC_V: Kommandozeilen stehen in der Prozessliste, und dort
haben Bot-Token und Stream-Keys nichts verloren.

    set NC_V=123456:AAF...
    python tools/envset.py --file .env BOT_TOKEN      # setzen
    python tools/envset.py --file .env --get BOT_TOKEN
    python tools/envset.py --file .env --heal         # Platzhalter leeren

--heal raeumt Zeilen der Form  NAME=   # (Geheimnis - hier eintragen)  auf.
Die sehen wie ein Kommentar aus, sind aber der WERT: python-dotenv liest bei
einem unquotierten Wert den Rest der Zeile mit. Wer die alte .env.example
kopiert hat, hatte rund 40 solcher Variablen — der Bot hielt Discord, Twitch
und YouTube fuer eingerichtet und meldete "Token abgelehnt" statt "kein Token".
"""
import os
import sys


def _key_of(line):
    """Schluessel einer Zeile — auch wenn sie auskommentiert ist."""
    text = line.strip()
    if text.startswith("#"):
        text = text.lstrip("#").strip()
    if "=" not in text:
        return ""
    return text.split("=", 1)[0].strip()


def lade(pfad):
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as fh:
        return fh.read().splitlines()


def schreibe(pfad, zeilen):
    with open(pfad, "w", encoding="utf-8") as fh:
        fh.write("\n".join(zeilen).rstrip("\n") + "\n")
    try:
        os.chmod(pfad, 0o600)      # unter Windows wirkungslos, schadet aber nicht
    except OSError:
        pass


def setzen(pfad, schluessel, wert):
    zeilen = [z for z in lade(pfad) if _key_of(z) != schluessel]
    # Werte mit Leerzeichen oder Raute gehoeren in Anfuehrungszeichen, sonst
    # liest dotenv nur bis zum ersten Trennzeichen.
    if any(c in wert for c in ' \t#"'):
        wert = '"%s"' % wert.replace('"', '\\"')
    zeilen.append("%s=%s" % (schluessel, wert))
    schreibe(pfad, zeilen)


def lesen(pfad, schluessel):
    for zeile in lade(pfad):
        if zeile.strip().startswith("#"):
            continue
        if _key_of(zeile) == schluessel:
            wert = zeile.split("=", 1)[1].strip()
            if len(wert) > 1 and wert[0] == wert[-1] and wert[0] in "\"'":
                wert = wert[1:-1]
            return wert
    return ""


def heilen(pfad):
    zeilen = lade(pfad)
    geheilt = 0
    for i, zeile in enumerate(zeilen):
        if zeile.strip().startswith("#") or "=" not in zeile:
            continue
        name, _, wert = zeile.partition("=")
        if wert.strip().startswith("#"):
            zeilen[i] = "%s=" % name.strip()
            geheilt += 1
    if geheilt:
        schreibe(pfad, zeilen)
    return geheilt


def main():
    argumente = sys.argv[1:]
    pfad = os.environ.get("NC_ENV", ".env")
    if "--file" in argumente:
        i = argumente.index("--file")
        pfad = argumente[i + 1]
        del argumente[i:i + 2]
    if "--heal" in argumente:
        print(heilen(pfad))
        return 0
    if "--get" in argumente:
        i = argumente.index("--get")
        print(lesen(pfad, argumente[i + 1]))
        return 0
    if not argumente:
        print(__doc__.strip())
        return 2
    setzen(pfad, argumente[0], os.environ.get("NC_V", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
