"""nc.sqldialekt — SQL-Bausteine, die SQLite und MariaDB verschieden schreiben (rein).

v4.2-W143. Beim ersten Umzug gegen einen echten MariaDB-Server fiel auf, dass
zwei Schreibstellen des Bestands reines SQLite sprachen:

    INSERT … ON CONFLICT(k) DO UPDATE SET …      (Treuepunkte, bot.py)
    INSERT … ON CONFLICT(guild_id,user_id) …     (Discord-Tagesbonus)

MariaDB kennt `ON CONFLICT` nicht; dort heisst dasselbe
`ON DUPLICATE KEY UPDATE`, und `excluded.spalte` heisst `VALUES(spalte)`.
Beide Stellen fingen den Fehler ab — auf MariaDB waeren Punkte und Bonus
still nie gebucht worden. Der Baustein steht hier EINMAL, damit eine dritte
Stelle nicht die dritte Schreibweise erfindet.

Voraussetzung in beiden Dialekten: auf `schluessel` liegt ein PRIMARY KEY oder
UNIQUE-Index — MariaDB entscheidet ueber JEDEN eindeutigen Schluessel der
Tabelle, nicht nur ueber den genannten.
"""

import re

_EXCLUDED = re.compile(r"\bexcluded\.(\w+)")


def bei_konflikt(backend, schluessel, zuweisungen):
    """Die Upsert-Klausel fuer `backend` ("sqlite" | "mariadb").

    schluessel:  "k" oder "guild_id,user_id"
    zuweisungen: ["points=points+?", "name=excluded.name", …] — in SQLite-
                 Schreibweise; fuer MariaDB wird excluded.x zu VALUES(x).
                 Platzhalter (?) bleiben, wo sie sind: die Parameterreihe ist
                 in beiden Dialekten dieselbe.
    """
    setzen = ", ".join(zuweisungen)
    if backend == "mariadb":
        return "ON DUPLICATE KEY UPDATE " + _EXCLUDED.sub(r"VALUES(\1)", setzen)
    return "ON CONFLICT(%s) DO UPDATE SET %s" % (schluessel, setzen)
