"""nc.dcspar — v5.2-W193: Discord ohne volle Mitgliederliste im Speicher (bot-frei).

discord.py laedt mit dem members-Intent beim Verbinden JEDE Gilde vollstaendig
(`chunk_guilds_at_startup`, Vorgabe an) und haelt die letzten 1000 Nachrichten
vor (`max_messages`). Der Bot liest Mitglieder an genau einer Stelle — der
Rangliste — und Nachrichten nur ueber raw-Ereignisse (`on_raw_reaction_add`).
Bei einer Gilde mit zehntausend Mitgliedern liegen sie trotzdem alle im RAM,
und das Abholen beim Verbinden verzoegert jeden Reconnect.

Schalter (als Funktion gelesen):
    DISCORD_MITGLIEDER_LADEN=1   altes Verhalten (volle Liste beim Start)
    DISCORD_NACHRICHTEN_PUFFER   Vorgabe 100 (0 = keiner; discord.py-Vorgabe 1000)

Bot-frei: liefert nur Optionen und den Anzeigenamen; discord.py importiert
der Aufrufer.
"""

import os


def _an(name, vorgabe):
    return os.getenv(name, vorgabe).strip().lower() in ("1", "true", "ja", "yes", "on")


def puffer() -> int:
    roh = os.getenv("DISCORD_NACHRICHTEN_PUFFER", "100").strip()
    return max(0, min(5000, int(roh))) if roh.isdigit() else 100


def client_optionen(erwaehnungen) -> dict:
    """Schluesselwoerter fuer discord.Client(...).

    DC-2: `erwaehnungen` ist `discord.AllowedMentions.none()` des Aufrufers
    (dieses Modul importiert discord nicht) und wird die Vorgabe JEDER
    Nachricht des Clients. Ohne sie pingte jede Antwort, die Nutzereingabe
    wiedergibt: `/stats username:@everyone` -> „📊 **@everyone**" rief den
    ganzen Server, und ein per /track gespeicherter Name tat das bei jedem
    /livenow, /recstatus und /tracklist erneut. Wer bewusst pingt, gibt sein
    eigenes allowed_mentions mit — discord.py fuehrt es mit dieser Vorgabe
    zusammen. Pflicht statt Vorgabe-None: ein Aufrufer, der es vergisst,
    faellt beim Start auf, nicht erst am ersten @everyone.
    """
    if erwaehnungen is None:
        raise ValueError("client_optionen: allowed_mentions fehlt (DC-2)")
    n = puffer()
    return {"chunk_guilds_at_startup": _an("DISCORD_MITGLIEDER_LADEN", "0"),
            "max_messages": n if n > 0 else None,
            "allowed_mentions": erwaehnungen}


def anzeige(mitglied, user_id) -> str:
    """Name aus dem Speicher, sonst eine Erwaehnung (<@id>) — Discord zeigt sie
    als Namen an. Der Aufrufer sendet mit AllowedMentions.none(), sonst
    pingte die Rangliste zehn Leute an."""
    if mitglied is not None:
        return mitglied.display_name
    return "<@%d>" % int(user_id)
