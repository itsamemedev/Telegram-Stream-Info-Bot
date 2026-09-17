"""pruefhilfen.py — v4.2-W90: temporaere Verzeichnisse und Attrappen-Dateien
fuer die vier Vertragssuiten.

════════════════════════════════════════════════════════════════════════
WARUM DIESE DATEI
════════════════════════════════════════════════════════════════════════
Die Suiten legten 35 temporaere Verzeichnisse mit `tempfile.mkdtemp()` an
und raeumten drei davon weg. Der Rest blieb liegen — pro Lauf. Auf der
Maschine, auf der W89 entstand, waren nach einem Tag Arbeit **5093
Verzeichnisse mit rund 30 GB** aufgelaufen, und die Pruefkette brach
mitten im Lauf mit `ENOSPC` ab: `df` meldete 1,1 MB frei bei 38 GB
belegt. Kein Vertrag war rot, keine Sperre fiel — es ging nur nichts mehr.

In der CI faellt das nicht auf: ein Lauf, frischer Container, danach ist
die Maschine weg. Genau deshalb konnte es wachsen.

Der Kostentreiber war dabei nicht die Zahl der Verzeichnisse, sondern
**eine einzige Zeile**. `_test_v42_w11_videoteil` brauchte eine Aufnahme
von 300 MB, weil `nc/videoteil.kopier_teilen()` aus Dateigroesse und
Laufzeit die Bitrate rechnet (300 MB / 600 s = 0,5 MB/s -> 81 s je
Segment). Sie stand als:

    f.write(b"\\0" * (300 * 1024 * 1024))    # 300 MB (sparse)

Der Kommentar sagt „sparse", der Code ist das Gegenteil: `b"\\0" * 300MB`
legt erst ein 300-MB-`bytes`-Objekt im RAM an und schreibt dann 300 MB
echte Nullen auf die Platte. Gemessen 0,31 s und +300 MB RSS-Spitze, je
Lauf, fuer eine Zahl, die `os.path.getsize()` auch von einer leeren Datei
mit gesetzter Groesse bekommt.

Dieses Modul stellt beides bereit: Verzeichnisse, die sich selbst
wegraeumen, und Attrappen, die nur so gross *aussehen*. `tools/testmuell.py`
haelt die Suiten darauf fest.
"""

import atexit
import os
import shutil
import tempfile

# Das Verzeichnis, aus dem der Lauf gestartet wurde. `test_smoke.py` wechselt
# absichtlich in ein leeres Verzeichnis, damit der Import von `bot.py` nichts
# ins Repo schreibt — liegt das cwd beim Aufraeumen unter einem Pfad, den wir
# gerade loeschen, braucht es einen Ort zum Zurueckwechseln.
_START = os.getcwd()

_ANGELEGT = []


def verzeichnis(praefix="nc-pruef-"):
    """Ein temporaeres Verzeichnis, das am Prozessende wieder verschwindet.

    Ersatz fuer `tempfile.mkdtemp()` in den Suiten. Der Praefix macht die
    Herkunft im Dateisystem sichtbar: wer `nc-pruef-*` in `/tmp` findet,
    weiss, dass ein Lauf abgebrochen ist, statt zu raten.
    """
    d = tempfile.mkdtemp(prefix=praefix)
    _ANGELEGT.append(d)
    return d


def attrappe(pfad, bytes_):
    """Eine Datei, die `bytes_` gross *ist*, ohne `bytes_` zu kosten.

    `truncate()` setzt die Groesse in den Metadaten; die Bloecke werden erst
    beim Schreiben belegt. `os.path.getsize()` und `st.st_size` liefern
    danach denselben Wert wie bei einer echt geschriebenen Datei — und
    genau die beiden liest der Produktionscode, der hier geprueft wird
    (`nc/videoteil` sechsmal `getsize`, `nc/storage` zweimal `st_size`,
    `nc/archiverules` einmal `getsize`). Wer stattdessen `st_blocks` oder
    `du` auswerten wuerde, saehe einen Unterschied — dann ist eine echte
    Datei noetig und diese Funktion die falsche Wahl.

    Gemessen fuer 300 MB: 0,000 s statt 0,31 s, 0 statt 614.400 Bloecke,
    und die 300-MB-Spitze im RAM entfaellt ganz.
    """
    with open(pfad, "wb") as f:
        f.truncate(bytes_)
    return pfad


def aufraeumen():
    """Alles wegraeumen, was `verzeichnis()` angelegt hat.

    Laeuft per `atexit` und ist damit auch nach einem gefallenen Vertrag
    noch dran — ein `finally` je Vertrag waere 35-mal dieselbe Zeile und
    genau die, die 32-mal vergessen wurde.
    """
    # Liegt das Arbeitsverzeichnis unter einem der Pfade, die jetzt fallen,
    # erst heraus: unter Linux gelingt das Loeschen zwar trotzdem (das cwd
    # wird nur ungueltig), unter Windows nicht.
    try:
        hier = os.getcwd()
    except OSError:
        hier = None                      # cwd schon weg — dann sowieso wechseln
    if hier is None or any(hier == d or hier.startswith(d + os.sep)
                           for d in _ANGELEGT):
        try:
            os.chdir(_START)
        except OSError:
            pass                         # nicht zu retten; rmtree versucht es dennoch
    # Zwei Durchgaenge, und der zweite ist nicht Zierde: `test_smoke.py`
    # importiert `bot.py`, und dieser Import startet Waechter-Threads, die
    # beim Prozessende noch leben. SQLite legt seine `-wal`/`-shm` neben der
    # Datenbank NEU an, sobald einer davon schreibt — entsteht das zwischen
    # dem Listing von rmtree und dem abschliessenden rmdir, faellt rmdir mit
    # ENOTEMPTY, und `ignore_errors` verschluckt es. Genau so blieb hier ein
    # Verzeichnis mit `tiktok_bot.db-shm` und `-wal` zurueck, waehrend die
    # Datenbank selbst schon weg war.
    uebrig = []
    while _ANGELEGT:
        d = _ANGELEGT.pop()
        shutil.rmtree(d, ignore_errors=True)
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)
        if os.path.exists(d):
            uebrig.append(d)
    if uebrig:
        # Nicht still: ein Aufraeumer, der lautlos nichts tut, ist genau der
        # Grund, aus dem hier 30 GB aufgelaufen sind.
        import sys
        print("pruefhilfen: %d Verzeichnis(se) liessen sich nicht raeumen, "
              "vermutlich schreibt noch ein Thread hinein: %s"
              % (len(uebrig), ", ".join(uebrig)), file=sys.stderr)


atexit.register(aufraeumen)
