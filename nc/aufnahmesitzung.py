"""nc.aufnahmesitzung — was zusammengehoert, gehoert zusammen (v4.2-W44).

Ein dreistuendiger TikTok-Stream liegt bei uns als sechs bis zehn Dateien auf
der Platte. Das ist kein Fehler, sondern Absicht: die signierte Stream-URL
laeuft nach rund 30 Minuten ab, und B58 beendet ffmpeg lieber ein paar Sekunden
vorher sauber, als auf den 404 zu warten. Dazu kommt je eine Datei nach jedem
403, Stall oder Abriss.

Was fehlte, war die Klammer. Die Tabelle kannte nur

    recordings(id, username, filepath, created_at, …)

und nichts darin sagte, dass sieben dieser Zeilen EIN Stream von 20:00 bis
23:30 sind. Der Betreiber konnte den Stream deshalb nicht von Anfang bis Ende
sehen — nicht weil das Material fehlte, sondern weil es unsortiert herumlag.

Dieses Modul rechnet, und zwar nur: keine Datenbank, kein Prozess, keine Uhr
aus dem Modul. Zeiten kommen als Parameter herein. Damit laesst sich die
Sitzungslogik pruefen, ohne einen Stream aufzunehmen.
"""
from __future__ import annotations

import datetime as _dt
import re

from nc import ffbuild as _ffbuild

# Ab dieser Pause zwischen Segment-Ende und naechstem Segment-Start gilt der
# Stream als beendet und es beginnt eine neue Sitzung. Grosszuegig gewaehlt:
# ein 403 mit Backoff kann Minuten kosten, und dann ist es immer noch derselbe
# Stream. Erst wenn jemand wirklich offline geht, soll die Klammer brechen.
SITZUNG_MAX_LUECKE_S = 900


def _dateisicher(text: str, vorgabe: str = "unbenannt") -> str:
    """Ein Stueck fremder Text, das gefahrlos in einen Dateinamen darf.

    Der Punkt bleibt erlaubt — TikTok-Namen wie "helge.72" sollen lesbar
    bleiben —, aber eine FOLGE von Punkten wird eingedampft. Grund: eine
    Kennung, die aus dem URL-Pfad der Join-Route kommt, kann ".." tragen.
    Ausbrechen kann ein solcher Name nach dem Ersetzen der Schraegstriche
    zwar nicht mehr, aber "sitzung_.._.._x.mp4" wird von jedem spaeteren
    normpath-Schritt wieder als Aufstieg gelesen — das gar nicht erst
    entstehen zu lassen ist billiger als jede spaetere Pruefung.
    """
    t = re.sub(r"[^A-Za-z0-9_.@-]", "_", text or "")
    t = re.sub(r"\.{2,}", "_", t).strip("._")
    return t or vorgabe


def _stempel(iso: str) -> str:
    """ISO-Zeit → kompakter Stempel fuer die Sitzungs-ID (20260911T2000)."""
    roh = re.sub(r"[^0-9T]", "", (iso or "").replace(" ", "T"))
    return (roh[:13] or "unbekannt")


def sitzung_id(username: str, start_iso: str) -> str:
    """Lesbare, stabile ID: @user_20260911T2000.

    Bewusst sprechend statt UUID — sie steht im Dashboard und in Dateinamen,
    und dort ist "@helge_72_20260911T2000" beim Suchen mehr wert als ein Hash.
    """
    u = _dateisicher((username or "").lstrip("@"), "unbekannt")
    return f"@{u}_{_stempel(start_iso)}"


def gehoert_dazu(vorheriges_ende, neuer_start, *, max_luecke_s=None) -> bool:
    """Setzt das neue Segment die laufende Sitzung fort?

    Beide Zeiten als Sekunden (float). None beim vorherigen Ende heisst: es
    gibt keine laufende Sitzung.
    """
    if vorheriges_ende is None or neuer_start is None:
        return False
    grenze = SITZUNG_MAX_LUECKE_S if max_luecke_s is None else max_luecke_s
    luecke = neuer_start - vorheriges_ende
    # Negative Luecke = Ueberlappung. Das ist keine neue Sitzung, sondern ein
    # nahtloser Schnitt (oder eine Uhr, die gesprungen ist) — dazugehoerig.
    return luecke <= grenze


def luecken(segmente):
    """Wo sind die Loecher, und wie gross?

    segmente: Liste von (start_s, ende_s), beliebige Reihenfolge.
    Rueckgabe: (liste_der_luecken_s, summe_s, brutto_s, netto_s)

    brutto = erste Startzeit bis letztes Ende (die Wanduhr des Streams)
    netto  = tatsaechlich aufgenommene Sekunden

    Ueberlappungen zaehlen NICHT als negative Luecke — sonst rechnet sich eine
    saubere Naht die echten Loecher schoen.
    """
    paare = sorted((s, e) for s, e in segmente if s is not None and e is not None)
    if not paare:
        return [], 0.0, 0.0, 0.0
    lst = []
    for (_s_vor, e_vor), (s_next, _e) in zip(paare, paare[1:]):
        d = s_next - e_vor
        if d > 0:
            lst.append(d)
    brutto = paare[-1][1] - paare[0][0]
    netto = sum(max(0.0, e - s) for s, e in paare)
    return lst, float(sum(lst)), float(brutto), float(netto)


def concat_liste(pfade) -> str:
    """Inhalt der concat-Demuxer-Liste fuer ffmpeg.

    Der Demuxer erwartet Zeilen der Form  file 'pfad'  — und ein einfaches
    Anfuehrungszeichen IM Pfad beendet es sonst vorzeitig. ffmpeg will dafuer
    die Form '\\'' (schliessen, escaptes Zeichen, wieder oeffnen). Ohne das
    ist ein Dateiname mit Apostroph nicht nur kaputt, sondern hebelt die
    Argumentgrenze aus.
    """
    zeilen = []
    for p in pfade:
        sicher = str(p).replace("'", "'\\''")
        zeilen.append(f"file '{sicher}'")
    return "\n".join(zeilen) + ("\n" if zeilen else "")


def concat_cmd(listendatei: str, ziel: str, *, threads=None, nice=None):
    """ffmpeg-Befehl, der die Segmente OHNE Neukodierung aneinanderhaengt.

    -c copy ist der ganze Punkt: alle Segmente stammen aus derselben Quelle
    mit demselben Recorder-Kommando, haben also identische Codec-Parameter.
    Damit kostet das Zusammenfuegen praktisch keine CPU — wichtig auf einer
    Box, die schon beim Restream-Transcode nicht hinterherkommt.

    -safe 0, weil die Liste absolute Pfade traegt.

    Der Thread-Deckel wird HIER gesetzt und nicht beim Aufrufer: die Regel
    "jeder rechnende ffmpeg-Pfad laeuft durch ff_cmd" wird in
    test_restream.test_ffmpeg_thread_budget an der Funktion geprueft, die das
    Kommando baut. Ein Deckel eine Ebene hoeher waere korrekt und trotzdem
    unsichtbar — und die naechste Aufrufstelle haette dann gar keinen.
    """
    return _ffbuild.ff_cmd(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-f", "concat", "-safe", "0", "-i", listendatei,
         "-c", "copy", "-movflags", "+faststart", ziel],
        threads=threads, nice=nice)


def zieldatei(verzeichnis: str, sid: str) -> str:
    """Name der zusammengefuegten Datei, garantiert unterhalb `verzeichnis`.

    Praefix 'sitzung_', damit sie sich von den Segmenten unterscheidet und
    beim naechsten Lauf nicht selbst wieder eingesammelt wird.

    Der Pfad-Riegel kommt aus nc.sicherpfad und wird hier NICHT nachgebaut:
    die Sitzungs-ID traegt einen Nutzernamen aus fremder Quelle, und fuer
    genau diesen Fall gibt es im Projekt eine zustaendige Stelle. Ein zweiter
    Riegel danebenzustellen war schon einmal der Grund, warum CodeQL 241
    Befunde meldete, die keiner mehr pruefen konnte.
    """
    from nc.sicherpfad import sicher_join
    flach = _dateisicher(sid, "unbenannt")
    return sicher_join(verzeichnis, f"sitzung_{flach}.mp4",
                       "sitzung_unbenannt.mp4")


def sekunden(iso):
    """ISO-Zeitstempel → Sekunden seit Epoche, oder None.

    Datumswerte liegen in beiden Backends als ISO-Strings in TEXT/VARCHAR,
    nie als natives DATETIME (siehe Skill nc-datenbank). Die Sitzungsrechnung
    braucht aber Zahlen, und zwar VERGLEICHBARE: ein Stempel ohne Zeitzone
    wuerde in Python als lokale Zeit gelesen und stuende dann je nach
    Sommerzeit ein bis zwei Stunden neben einem, der ein "+00:00" traegt.
    Wir schreiben ausschliesslich UTC, also wird ein nackter Stempel hier
    auch als UTC gelesen statt als Ortszeit.
    """
    if iso is None:
        return None
    if isinstance(iso, (int, float)):
        return float(iso)
    t = str(iso).strip()
    if not t:
        return None
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        d = _dt.datetime.fromisoformat(t)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=_dt.timezone.utc)
    return d.timestamp()


def abdeckung(segmente):
    """Wie viel Prozent des Streams liegen wirklich auf der Platte?

    Rueckgabe 0.0-100.0. Ohne Brutto-Zeit (ein einziges Segment der Laenge 0)
    gilt die Aufnahme als vollstaendig — sonst meldete eine Sitzung mit einer
    Datei 0 % und der Betreiber suchte nach einem Loch, das es nicht gibt.
    """
    _l, _s, brutto, netto = luecken(segmente)
    if brutto <= 0:
        return 100.0
    return round(min(100.0, netto / brutto * 100.0), 1)
