"""nc.raumkennung — v5.1-W184: eine TikTok-Room-ID, bevor sie jemand benutzt.

Gemessen am 11.11. (debug.log 18:39): der Chat-Listener @chrissyxd11 brach
sechsmal in einer halben Stunde nach einer Sekunde ab, jedesmal mit

    Verbindung fehlgeschlagen (invalid literal for int() with base 10: '')

Der Bot-Pfad (`_fetch_tiktok_room_id`) fand keine Room-ID; der Listener
ueberliess die Beschaffung dann TikTokLive, und dessen Abfrage
`api-live/user/room/` lieferte fuer diesen Raum ein LEERES `roomId` — die
Bibliothek ruft darauf `int('')`. Im Log stand ein Python-Wortlaut, der auf
einen Programmfehler zeigt, und die Abhilfe daneben („Sign-Server, Tunnel,
User nicht live") passte nicht: TikTok gibt die Raumkennung dieses Nutzers
fuer diese Sitzung nicht heraus (Abo-/18+-Raum, Region, oder gerade beendet)
— derselbe Fall wie „live ohne Stream-Adresse" (W51), eine Schicht weiter.

Zwei Dinge hier: eine Room-ID wird nur injiziert, wenn sie eine ist (Ziffern,
groesser null — `int()` auf etwas anderem waere derselbe Absturz im eigenen
Code), und der Wortlaut der Bibliothek wird in den Grund uebersetzt.
Bot-frei, rein.
"""

import re

# `int('')` und `int('None')` — die beiden Formen, in denen eine fehlende
# Kennung aus der Bibliothek kommt. Der Wortlaut ist der von CPython.
_LEER = re.compile(r"invalid literal for int\(\) with base 10: '(|None|null|0)'")

GRUND_LEER = ("TikTok gibt fuer diesen Raum keine Room-ID heraus (roomId leer) — "
              "meist ein Abo-/18+-Raum, eine Regionssperre fuer diese Sitzung, oder "
              "der Live ist gerade zu Ende. Kein Programmfehler und kein Sign-Server-"
              "Problem; der Chat versucht es mit wachsendem Abstand weiter.")


def gueltig(rid):
    """-> Room-ID als int, oder None, wenn `rid` keine ist.

    Akzeptiert int und Ziffernfolgen (TikTok liefert die ID als String, sie
    passt nicht in ein JS-Number und wird deshalb nie als Zahl geschickt).
    0 ist keine Kennung: die Bibliothek wertet sie als „nicht live"."""
    # Ueber die Zeichenkette: None, True ("True") und ein negatives int
    # ("-5") fallen damit alle an isdigit() — eine Sonderbehandlung je Typ
    # waere ein zweiter Riegel ohne Wirkung (die Mutationsprobe entwischte).
    s = str(rid).strip()
    n = int(s) if s.isascii() and s.isdigit() else 0
    return n if n > 0 else None


def grund(exc) -> str:
    """-> Klartext fuer eine Ausnahme der Chat-Verbindung: die bekannte Lage
    als Satz, sonst der Wortlaut der Ausnahme."""
    bekannt = isinstance(exc, ValueError) and bool(_LEER.search(str(exc)))
    return GRUND_LEER if bekannt else str(exc)
