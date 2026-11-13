"""nc.tgantwort — v5.8-W200: wann AZRAEL in Telegram antwortet (bot-frei).

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber: „In Telegram antwortet das Brain nicht auf Antwort-Nachrichten."
Drei Ursachen, jede still:

1. Eine Antwort auf eine Bot-Nachricht lief nur, wenn fuer genau diesen
   Chat und diesen Nutzer ein Verlauf in Redis lag (F19). Ohne Redis gibt
   ai_history_load() immer [] — dann wurde JEDE Antwort verworfen. Mit Redis
   nach einer Stunde (AI_HISTORY_TTL), und immer, wenn jemand anderes auf
   AZRAELs Antwort antwortete: der hat keinen eigenen Verlauf.
2. Themen-Gruppen (der Bot legt seit W168 je Tracking ein Thema an): dort
   traegt Telegram an JEDER Nachricht einen Antwort-Bezug auf die
   Eroeffnungsnachricht des Themas — und die stammt vom Bot. Damit galt jede
   Nachricht als „Antwort auf den Bot", scheiterte am Verlauf, und die
   Ansprache „@Azrael …" (die nur Nicht-Antworten nimmt) kam nie dran.
3. Eine Antwort auf die Nachricht eines ANDEREN Nutzers mit „@Azrael …" fiel
   durch beide Filter: keine Antwort auf den Bot, aber eine Antwort.

Hier steht die Entscheidung als reine Funktion — ohne python-telegram-bot,
die Nachricht wird nur ueber Attribute gelesen, damit sie sich mit einer
Attrappe pruefen laesst.
"""

import collections
import re
import threading

# Der Fuss, den _run_ai_call an jede KI-Antwort haengt:
#   "\n\n— 3.2s · <modell>[ · datei]"
# Daran ist eine KI-Antwort auch ohne Verlauf und nach einem Neustart zu
# erkennen. Bei einer langen Antwort traegt nur das LETZTE Stueck den Fuss —
# dafuer die gemerkten Kennungen unten.
_FUSS = re.compile(r"\n\n— \d+(?:\.\d+)?s · \S[^\n]*$")
_NAME = re.compile(r"(?<![\w@])@?azrael\b", re.I)

# Kennungen der Nachrichten, die eine KI-Antwort tragen (je Chat). Begrenzt:
# ein Bot in vielen Gruppen soll hier keinen Speicher sammeln. Nach einem
# Neustart leer — dann traegt der Fuss die Erkennung allein.
MAX_GEMERKT = 4000
_GEMERKT = collections.OrderedDict()      # (chat_id, message_id) -> None
_SPERRE = threading.Lock()

FOLGE = "folge"          # Antwort auf AZRAEL: weiterreden, mit Zusammenhang
ANSPRACHE = "ansprache"  # neue Frage an AZRAEL


def merken(chat_id, message_id):
    """Eine Nachricht als KI-Antwort merken (aufgerufen von _run_ai_call)."""
    if chat_id is None or message_id is None:
        return
    with _SPERRE:
        _GEMERKT[(chat_id, message_id)] = None
        _GEMERKT.move_to_end((chat_id, message_id))
        while len(_GEMERKT) > MAX_GEMERKT:
            _GEMERKT.popitem(last=False)


def gemerkt(chat_id, message_id) -> bool:
    with _SPERRE:
        return (chat_id, message_id) in _GEMERKT


def echte_antwort(msg):
    """Die Nachricht, auf die `msg` wirklich antwortet — oder None.

    In Themen-Gruppen setzt Telegram reply_to_message auch ohne Antwort: auf
    die Eroeffnungsnachricht des Themas (forum_topic_created), deren Kennung
    gleich message_thread_id ist. Das ist keine Antwort, sondern der Ort."""
    bezug = getattr(msg, "reply_to_message", None)
    if bezug is None:
        return None
    if getattr(bezug, "forum_topic_created", None):
        return None
    thema = getattr(msg, "message_thread_id", None)
    if (getattr(msg, "is_topic_message", False) and thema is not None
            and getattr(bezug, "message_id", None) == thema):
        return None
    return bezug


def ist_ki_antwort(chat_id, bezug) -> bool:
    """Traegt `bezug` (eine Bot-Nachricht) eine KI-Antwort?"""
    if bezug is None:
        return False
    if gemerkt(chat_id, getattr(bezug, "message_id", None)):
        return True
    return bool(_FUSS.search(getattr(bezug, "text", None) or ""))


def ohne_fuss(text) -> str:
    """Der Text einer KI-Antwort ohne den Fuss — als Zusammenhang fuer die Folgefrage."""
    return _FUSS.sub("", text or "").strip()


def angesprochen(text) -> bool:
    """Steht der Name im Text? „Azrael", „@Azrael", „azrael," — nicht „Mazrael"."""
    return bool(_NAME.search(text or ""))


def frage_ohne_namen(text) -> str:
    """Den Namen aus der Frage nehmen, sonst antwortet die KI auf sich selbst."""
    frage = re.sub(r"(?<![\w@])@?azrael\b[:,]?\s*", "", text or "", flags=re.I).strip()
    return frage or (text or "").strip()


def entscheiden(text, privat, antwort_auf_bot, ki_antwort, verlauf_da):
    """FOLGE, ANSPRACHE oder None (nicht antworten).

    antwort_auf_bot: die Nachricht antwortet wirklich auf eine Bot-Nachricht
    (echte_antwort(), nicht der Themen-Kopf).

    - Befehle haben Vorrang: „/…" nie.
    - Antwort auf eine KI-Antwort: immer weiterreden — auch ohne Verlauf und
      auch von jemand anderem. Dafuer antwortet man darauf.
    - Antwort auf eine ANDERE Bot-Nachricht (Live-Meldung, Aufnahme, Alarm):
      nur mit Ansprache, im Privatchat oder bei laufendem Gespraech — sonst
      schriebe AZRAEL unter jede Live-Meldung, auf die jemand „geil" antwortet.
    - Alles andere (auch die Antwort auf einen anderen Nutzer): Ansprache mit
      Namen, oder Privatchat."""
    t = (text or "").strip()
    if not t or t.startswith("/"):
        return None
    if antwort_auf_bot:
        if ki_antwort or verlauf_da or privat or angesprochen(t):
            return FOLGE
        return None
    if privat or angesprochen(t):
        return ANSPRACHE
    return None
