"""conftest.py — v4.2-W86: die Verträge einzeln fahrbar machen.

════════════════════════════════════════════════════════════════════════
WARUM DIESE DATEI
════════════════════════════════════════════════════════════════════════
`test_nc_modules.py` und `test_restream.py` sind zusammen 22.000 Zeilen mit
rund 100 Vertragsfunktionen, und bis hierher gab es genau **einen** Weg, sie
zu fahren: `python test_nc_modules.py`, alles oder nichts. Das kostet bei
jedem Befund eine volle Minute, um eine einzige Zeile zu prüfen — und es
verhindert jede Messung, die je Vertrag arbeitet.

Der Grund war kein Vorsatz, sondern ein Nebeneffekt: der Aufbau der
Testdatenbank stand mitten in `main()`. Wer einen einzelnen Vertrag aufrief,
bekam keine konfigurierte Datenbank; `db_conn()` fiel auf den Vorgabepfad
zurück und legte ein `tiktok_bot.db` **im Arbeitsverzeichnis** an. Beim
zweiten Lauf stirbt `_test_dbexport` dann an „table dbx_t already exists",
und im Repo liegt eine Datenbankdatei, die niemand bestellt hat.

Seit v4.2-W86 steht der Aufbau als `richte_testdatenbank_ein()` neben den
Verträgen, und diese Datei ruft ihn für pytest genauso auf wie `main()` für
den alten Weg. **Beide Wege bleiben.** `python test_nc_modules.py` ist und
bleibt das, was die CI fährt und was in der Prüfkette steht — pytest kommt
daneben, für die Arbeit am einzelnen Vertrag und für die Überdeckung.

════════════════════════════════════════════════════════════════════════
WAS HIER NICHT PASSIERT
════════════════════════════════════════════════════════════════════════
Keine Umschreibung der bestehenden Verträge auf pytest-Idiome, kein
`assert`-Rewriting-Zauber, keine Fixtures, die Verträge sich teilen. Die
Funktionen bleiben, wie sie sind; sie bekommen nur eine Umgebung, in der sie
einzeln laufen. Eine Suite dieser Größe umzuschreiben wäre ein Quartal und
ein unprüfbarer Diff — dieselbe Überlegung, aus der die Ratschen in W65/W66
den Bestand dulden und nur sein Wachstum sperren.
"""

import os
import sys

import pytest

WURZEL = os.path.dirname(os.path.abspath(__file__))
if WURZEL not in sys.path:
    sys.path.insert(0, WURZEL)


@pytest.fixture(scope="session", autouse=True)
def testdatenbank():
    """Dieselbe Umgebung, die `main()` aufbaut — einmal je pytest-Lauf.

    session-scoped und autouse: die Verträge holen sie sich nicht per
    Parameter (sie haben keine), sie setzen sie voraus. Genau wie unter
    `main()`.

    `configure_db` ist prozessweit; eine Fixture je Vertrag hiesse, die
    Datenbank hundertmal neu aufzubauen, und die Verträge sind darauf gar
    nicht ausgelegt — `_test_dbexport` legt seine Tabellen selbst an und
    erwartet, dass sie danach stehen.
    """
    import test_nc_modules as T
    tmp, rid = T.richte_testdatenbank_ein()
    yield {"tmp": tmp, "rid": rid}


def pytest_collection_modifyitems(items):
    """Die Verträge in Dateireihenfolge fahren, nicht in Sammelreihenfolge.

    pytest sammelt je Datei in Definitionsreihenfolge — das entspricht der
    Reihenfolge, in der `main()` sie aufruft, und darauf sind sie gemessen
    lauffaehig. Ohne diese Zusicherung waere ein Umsortieren durch ein Plugin
    (pytest-randomly etwa) ein Vertragsbruch, der nichts mit dem Code zu tun
    hat.
    """
    items.sort(key=lambda i: (str(getattr(i, "fspath", "")),
                              getattr(i.function, "__code__",
                                      None).co_firstlineno
                              if getattr(i, "function", None) else 0))
