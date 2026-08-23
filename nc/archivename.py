"""nc.archivename — v4.0-W62: kollisionsfreies, atomares Anlegen, aus bot.py gelöst.

open_unique kapselt die Namensfolge (filename, dann base_2, base_3, … vor der
Extension) und die Retry-Schleife. Das eigentliche Öffnen wird injiziert
(opener(full) → fd, wirft FileExistsError bei Kollision), damit die Logik ohne
echtes Dateisystem testbar ist. Atomik (O_CREAT|O_EXCL) liegt beim Aufrufer:
zwei parallele Uploads können denselben Pfad nicht überschreiben.
"""

import os


def open_unique(directory, filename, opener, join=os.path.join, max_attempts=10000):
    """(fd, full_path) für einen frisch angelegten, kollisionsfreien Pfad.
       opener(full) legt die Datei atomar an und wirft FileExistsError, falls sie
       schon existiert; dann wird das nächste Suffix probiert. Nach max_attempts
       Kollisionen → RuntimeError."""
    base, ext = os.path.splitext(filename)
    for attempt in range(0, max_attempts):
        candidate = filename if attempt == 0 else f"{base}_{attempt + 1}{ext}"
        full = join(directory, candidate)
        try:
            return opener(full), full
        except FileExistsError:
            continue
    raise RuntimeError("zu viele Kollisionen im Archive-Ordner")
