"""nc.topicumzug — die alten @name-Themen in das EINE Upload-Thema umziehen (rein, bot-frei).

v4.2-W168. Bis hierher legte der Bot je getrackter Person ein eigenes
Forum-Thema an (`@anna`, `@ben`, …). Entschieden vom Betreiber am 07.11.:
„Uploads die schon vorhanden sind in einem Topic nachziehen und alle anderen
Channel loeschen" — gewaehlt: neu hochladen, DANN loeschen.

Die Reihenfolge ist die Sicherung: ein Thema zu loeschen loescht in Telegram
jede Nachricht darin, also jedes Video. Geloescht wird deshalb erst, wenn
JEDE noch vorhandene Aufnahme dieses Nutzers nachweislich im Upload-Thema
angekommen ist. Was nicht mehr auf der Platte liegt, kann nicht nachgezogen
werden — das sagt das Log, statt es still zu verlieren.

Der Fortschritt steht in einer Datei: ein Neustart mitten im Umzug darf
nichts doppelt hochladen, und ein gescheitertes Loeschen (fehlendes Recht
„Themen verwalten") wird beim naechsten Start wiederholt, ohne die Videos
ein zweites Mal zu senden.
"""

import json
import os


def alte_themen(themen) -> list:
    """[(chat_id, nutzer, thread_id)] aller @name-Themen aus tg_topics.json.

    Schluessel ohne '#' sind Nutzer-Themen; '#live-notices' und '#uploads'
    gehoeren keinem Nutzer und bleiben. Ein Schluessel, dessen Chat keine Zahl
    ist, stammt nicht von `_topic_key` und wird nicht angefasst."""
    aus = []
    for schluessel, tid in sorted((themen or {}).items()):
        chat, _, nutzer = str(schluessel).partition(":")
        ziffern = chat[1:] if chat.startswith("-") else chat
        if not nutzer or nutzer.startswith("#") or not ziffern.isdigit():
            continue
        aus.append((int(chat), nutzer, int(tid)))
    return aus


def lade(pfad) -> dict:
    """Fortschritt lesen. Fehlt die Datei, beginnt der Umzug von vorn —
    eine kaputte Datei ist dagegen ein Fehler (der Aufrufer meldet ihn),
    sonst wuerde nach einem halben Umzug alles ein zweites Mal hochgeladen."""
    if not os.path.exists(pfad):
        return {"gesendet": {}}
    with open(pfad, encoding="utf-8") as fh:
        daten = json.load(fh)
    if not isinstance(daten, dict) or not isinstance(daten.get("gesendet", {}), dict):
        raise ValueError("%s hat nicht das Format des Topic-Umzugs" % pfad)
    daten.setdefault("gesendet", {})
    return daten


def speichere(pfad, zustand) -> None:
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(zustand, fh, ensure_ascii=False)
    os.replace(tmp, pfad)


def schluessel(chat_id, nutzer) -> str:
    return "%s:%s" % (int(chat_id), str(nutzer).lower())


def offen(dateien, zustand, chat_id, nutzer) -> list:
    """Die Dateien, die fuer dieses Thema noch nicht nachgezogen sind —
    in der gegebenen Reihenfolge, ohne Doppel."""
    schon = set(zustand.get("gesendet", {}).get(schluessel(chat_id, nutzer), ()))
    aus = []
    for d in dateien or ():
        if d not in schon and d not in aus:
            aus.append(d)
    return aus


def gesendet(zustand, chat_id, nutzer, datei) -> None:
    zustand.setdefault("gesendet", {}).setdefault(schluessel(chat_id, nutzer), []).append(datei)


def erledigt(zustand, chat_id, nutzer) -> None:
    """Thema geloescht — die Liste wird nicht mehr gebraucht."""
    zustand.setdefault("gesendet", {}).pop(schluessel(chat_id, nutzer), None)


def angekommen(ergebnis) -> bool:
    """Hat split_and_send_video die Datei vollstaendig gesendet?
    Mindestens ein Teil und kein Fehler — ein leeres Ergebnis heisst, dass
    gar nichts gesendet wurde (toter Chat, Datei leer), und das ist KEIN
    Erfolg: danach wuerde das alte Thema mit dem einzigen Exemplar geloescht."""
    return bool(ergebnis) and ergebnis.get("gesendet", 0) > 0 and not ergebnis.get("fehler", 0)
