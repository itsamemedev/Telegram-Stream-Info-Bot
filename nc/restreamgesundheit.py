"""nc.restreamgesundheit — die Buchfuehrung hinter der Sendeanzeige.

v4.2-W13. Aus RestreamManager (1418 Zeilen) geloest. Was hier steht, rechnet
mit Zahlen und Woerterbuechern und kennt weder ffmpeg noch einen Prozess:
Fortschrittsmarke, Blind-Markierung, Verfall der tee-Ziel-Fehler.

WARUM AUSGERECHNET DIESE DREI: sie beantworten die Frage, ob eine Anzeige noch
etwas MISST oder nur noch etwas ZEIGT. Das ist die gefaehrlichere Haelfte jedes
Befunds — nicht dass die Messung aufhoert, sondern dass ihr letzter Wert
weiter als Messung gilt. Drei Fehler dieser Art stecken in der Vorgeschichte
(W113, W116, v4.1-W10), und alle drei waren Rechenfehler, keine ffmpeg-Fehler.
Genau deshalb gehoeren sie an einen Ort, an dem man sie ohne laufenden Stream
nachrechnen kann.

Die Zeit kommt als ARGUMENT herein, nicht aus time.monotonic(). Ohne das
liesse sich Verfall nicht pruefen, ohne im Test zu warten — und ein Verfall,
den man nicht pruefen kann, ist genau der, der jahrelang nicht stattfindet.
"""


def marke_setzen(eintrag, health, progress, jetzt):
    """Fortschrittsmarke fuer den Stillstands-Waechter fortschreiben.

    W113/W115: Es zaehlt NICHT, dass ein progress-Block ankam — ffmpeg
    schreibt seine Schnappschuesse auch dann weiter, wenn der Ausgang
    blockiert und frame/total_size stehenbleiben. Beweis fuer eine lebende
    Sendung ist nur der ZUWACHS an Bild oder Bytes.

    -> True, wenn sich wirklich etwas bewegt hat.
    """
    if eintrag is None:
        return False
    w = eintrag.setdefault("watch", {"frame": -1, "bytes": -1, "advanced": jetzt})
    vorwaerts = False
    try:
        fr = int((health or {}).get("frame") or 0)
        if fr > w["frame"]:
            w["frame"], vorwaerts = fr, True
    except (TypeError, ValueError):
        pass
    try:
        by = int((progress or {}).get("total_size"))
        if by > w["bytes"]:
            w["bytes"], vorwaerts = by, True
    except (TypeError, ValueError):
        pass
    if vorwaerts:
        w["advanced"] = jetzt
    return vorwaerts


def blind_markieren(info, grund, jetzt):
    """Die Health-Werte dieses Laufs sind ab jetzt Vergangenheit.

    v4.1-W10: Ohne diese Markierung bleibt im Dashboard die letzte Bitrate
    stehen — und eine stehende Bitrate liest sich wie ein gesunder Stream.

    -> True beim ERSTEN Mal, danach False. Der Aufrufer meldet nur beim
    ersten; eine Blindheit, die im Log dauerfeuert, wird weggeblendet wie
    jede Wiederholung.
    """
    # `is None` und NICHT `not info`: ein LEERER Eintrag ist ein gueltiger
    # Eintrag, der nur noch nichts enthaelt — und genau dann ist die
    # Blind-Markierung wichtig. Im Monolithen fiel der Unterschied nicht auf,
    # weil _eintrag() dort immer ein gefuelltes Woerterbuch liefert; als
    # allgemeine Funktion waere die Falsch-Pruefung ein stiller Ausfall.
    if info is None:
        return False
    h = info.setdefault("health", {})
    if h.get("blind"):
        return False
    h["blind"] = True
    h["blind_reason"] = grund
    h["blind_ts"] = jetzt
    return True


def frische_tee_fehler(roh, ttl, jetzt):
    """Die tee-Ziel-Fehler, die JETZT noch gelten. -> (frisch, verfallen)

    W116: _tee_fail wurde an fuenf Stellen gelesen — Deck, Verify-Schleife,
    Sentinel-Alarm, status() und Selbsttest — und an keiner geleert. Eine
    einmalige Ablehnung von YouTube stand damit bis zum Bot-Neustart im Panel,
    im Alarm und im Selbsttest, auch wenn das Ziel seit Stunden wieder sendet.
    Bei der Fehlersuche jagt man dann einem Zustand von vorgestern hinterher.

    ttl <= 0 schaltet den Verfall ab; dann gilt wieder alles. Das ist kein
    Versehen, sondern die Notbremse fuer den Fall, dass die Verfallszeit selbst
    zum Problem wird — sie muss abschaltbar sein, ohne den Code zu aendern.
    """
    roh = roh or {}
    if ttl <= 0:
        return dict(roh), False
    frisch = {k: v for k, v in roh.items()
              if (jetzt - (v.get("ts") or 0)) < ttl}
    # Verfallene gleich entsorgen, nicht nur ausblenden — sonst waechst das
    # Woerterbuch ueber Wochen mit toten Zielen voll.
    return frisch, len(frisch) != len(roh)
