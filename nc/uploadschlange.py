"""nc.uploadschlange — wann ein aufgeschobener Upload fertig ist (rein, bot-frei).

v4.2-W175. Die Warteschlange `pending_uploads.json` (bot.py,
`_upload_window_loop`) hat bis hier jeden Eintrag nach EINEM Versuch
entfernt: `split_and_send_video` wirft nie — jeder Fehlschlag (Netz, toter
Chat, Split gescheitert) endet ordentlich mit `return`, und der Aufrufer
hielt das fuer Erfolg. Ein Upload, der nachts im Fenster an einem Timeout
scheiterte, war damit still verloren; der `except`-Zweig mit „NICHT
entfernen → nächster Durchlauf versucht erneut" lief nie.

Entschieden wird jetzt am Ergebnis, das `split_and_send_video` seit W168 in
ein mitgegebenes `ergebnis`-Woerterbuch zaehlt: mindestens ein Teil
gesendet und kein Fehler. Sonst bleibt der Eintrag mit wachsender Pause
liegen und wird nach `MAX_VERSUCHE` laut aufgegeben — ein Chat, den es
nicht mehr gibt, darf die Schlange nicht fuer immer belegen.
"""

MAX_VERSUCHE = 5
PAUSE_S = 600.0          # 10 min nach dem ersten Fehlschlag, dann verdoppelt
PAUSE_MAX_S = 6 * 3600.0


def angekommen(ergebnis) -> bool:
    """Hat der Versand die Datei vollstaendig gesendet?

    Mindestens ein Teil und kein Fehler. Ein leeres Ergebnis heisst, dass gar
    nichts gesendet wurde (toter Chat, Split gescheitert, Platte voll) — und
    das ist KEIN Erfolg, sonst verschwindet der Eintrag mit der einzigen
    Erinnerung daran, dass die Aufnahme noch raus muss."""
    return bool(ergebnis) and ergebnis.get("gesendet", 0) > 0 and not ergebnis.get("fehler", 0)


def faellig(eintrag, jetzt: float) -> bool:
    """Ist der Eintrag jetzt dran? Ohne Zeitstempel (Bestand vor W175) oder
    mit einem, der keine Zahl ist: ja — ein kaputtes Feld darf den Upload
    nicht fuer immer zurueckhalten."""
    wann = eintrag.get("naechster_versuch")
    if isinstance(wann, bool) or not isinstance(wann, (int, float)):
        return True
    return wann <= jetzt


def pause_s(versuche: int) -> float:
    """Pause nach dem n-ten Fehlschlag: 10, 20, 40 … Minuten, hoechstens 6 h."""
    return min(PAUSE_MAX_S, PAUSE_S * (2 ** max(0, int(versuche) - 1)))


def nach_versuch(eintrag, ergebnis, jetzt: float, max_versuche: int = MAX_VERSUCHE):
    """-> (lage, eintrag_neu) mit lage in "fertig", "wieder", "aufgeben".

    `eintrag_neu` ist eine Kopie mit hochgezaehltem `versuche`, dem Grund des
    letzten Fehlschlags und dem Zeitpunkt des naechsten Versuchs — der
    Aufrufer schreibt sie an die Stelle des alten Eintrags."""
    if angekommen(ergebnis):
        return "fertig", dict(eintrag)
    neu = dict(eintrag)
    neu["versuche"] = int(eintrag.get("versuche") or 0) + 1
    neu["letzter_fehler"] = str((ergebnis or {}).get("grund")
                                or ("nichts gesendet" if not (ergebnis or {}).get("gesendet")
                                    else "%s Teil(e) gescheitert" % (ergebnis or {}).get("fehler")))[:300]
    if neu["versuche"] >= max_versuche:
        return "aufgeben", neu
    neu["naechster_versuch"] = jetzt + pause_s(neu["versuche"])
    return "wieder", neu


def gleicher(a, b) -> bool:
    """Derselbe Eintrag? Datei, Ziel und Zeitpunkt des Einreihens — dieselben
    drei Felder, an denen `_upload_queue_remove` ihn seit jeher erkennt."""
    return (a.get("file") == b.get("file") and a.get("chat_id") == b.get("chat_id")
            and a.get("ziel") == b.get("ziel") and a.get("queued_at") == b.get("queued_at"))


# ── ARC-5: die Datei streng lesen ───────────────────────────────────────────
# Bis v5.11.3 gab `_upload_queue_load` bei JEDEM Lesefehler `[]` zurueck. Der
# naechste Schreibvorgang (Einreihen, Entfernen, Fortschreiben) schrieb diese
# leere Liste dann zurueck — alle aufgeschobenen Uploads waren weg, und
# `_clip_prune` loeschte mit derselben leeren Schutzmenge die aufgeschobenen
# Meme-Zusammenschnitte. Dieselbe Klasse wie W198/W199 („Lesen mit Vorgabe,
# dann zurueckschreiben"), nur in einer JSON-Datei statt in app_config.

import json as _json
import os as _os
import time as _time


class SchlangeUnlesbar(RuntimeError):
    """Die Warteschlange war nicht zu lesen.

    `inhalt` trennt die beiden Lagen: True heisst „die Datei ist da, aber kein
    JSON / keine Liste" — sie wird nie wieder lesbar und darf beiseitegelegt
    werden. False heisst „das Lesen selbst scheiterte" (Rechte, E/A) — das
    kann voruebergehend sein, also nichts anfassen und nichts schreiben."""

    def __init__(self, text, *, inhalt):
        super().__init__(text)
        self.inhalt = inhalt


def lesen(pfad) -> list:
    """Die Eintraege der Schlange. Fehlende Datei = leere Schlange (Normalfall).

    Alles andere wirft SchlangeUnlesbar statt `[]` — wer danach schreibt,
    wuerde sonst den ganzen Bestand ueberschreiben."""
    roh = b"[]"                      # fehlende Datei = leere Schlange
    if _os.path.exists(pfad):
        try:
            with open(pfad, "rb") as f:
                roh = f.read()
        except OSError as e:
            # Auch ein FileNotFoundError zwischen exists und open landet hier:
            # dann wird in diesem Durchgang nicht geschrieben — harmlos, der
            # naechste sieht die fehlende Datei als leere Schlange.
            raise SchlangeUnlesbar("%s nicht lesbar (%s: %s)"
                                   % (pfad, type(e).__name__, e), inhalt=False) from e
    try:
        data = _json.loads(roh.decode("utf-8"))
    except ValueError as e:          # auch UnicodeDecodeError
        raise SchlangeUnlesbar("%s ist kein gueltiges JSON (%s)" % (pfad, e),
                               inhalt=True) from e
    if not isinstance(data, list):
        raise SchlangeUnlesbar("%s enthaelt keine Liste, sondern %s"
                               % (pfad, type(data).__name__), inhalt=True)
    return data


def beiseite(pfad, jetzt=None) -> str:
    """Die kaputte Datei unter `<pfad>.kaputt-<stempel>` wegstellen. -> neuer Pfad

    Umbenennen statt loeschen: in ihr stehen die aufgeschobenen Uploads, und
    die lassen sich von Hand oft noch retten (abgeschnittenes JSON). Ein
    vorhandener Name wird nie ueberschrieben — zwei Ausfaelle in derselben
    Sekunde bekommen einen Zaehler."""
    stempel = _time.strftime("%Y%m%d-%H%M%S", _time.localtime(jetzt))
    ziel = "%s.kaputt-%s" % (pfad, stempel)
    n = 1
    while _os.path.exists(ziel):
        ziel = "%s.kaputt-%s-%d" % (pfad, stempel, n)
        n += 1
    _os.rename(pfad, ziel)
    return ziel
