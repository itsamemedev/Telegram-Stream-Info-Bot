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


def client_optionen() -> dict:
    """Schluesselwoerter fuer discord.Client(...)."""
    n = puffer()
    return {"chunk_guilds_at_startup": _an("DISCORD_MITGLIEDER_LADEN", "0"),
            "max_messages": n if n > 0 else None}


def anzeige(mitglied, user_id) -> str:
    """Name aus dem Speicher, sonst eine Erwaehnung (<@id>) — Discord zeigt sie
    als Namen an. Der Aufrufer sendet mit AllowedMentions.none(), sonst
    pingte die Rangliste zehn Leute an."""
    if mitglied is not None:
        return mitglied.display_name
    return "<@%d>" % int(user_id)
