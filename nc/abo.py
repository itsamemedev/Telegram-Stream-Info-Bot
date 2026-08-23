"""nc.abo — v4.0-W26: Abo-/Subscriber-only-Erkennung im TikTok-liveRoom-JSON.

Verbatim aus bot.py herausgelöst (B148). Rein und ohne Bot-Kopplung: bekommt
das Room-Dict herein, scannt defensiv nach dem 'sub_only'-Gating und gibt True
nur bei einem echten Sub-only-Signal zurück. Bitgenau gegen den Monolithen
geprüft.
"""


def room_is_abo(room):
    """B148: Erkennt Abo-/Subscriber-only Lives im TikTok-liveRoom-JSON.
       TikTok benennt das Gating 'live_sub_only' (Feldkonvention aus der
       offiziellen Room/Proto-Struktur, z.B. live_sub_only_tier/_month).
       Wir scannen defensiv nach diesem Marker (Key-Varianten + Schachtelung),
       damit die Erkennung nicht an EINEM exakten Pfad hängt und robust bleibt,
       wenn TikTok das Feld verschiebt. Positiv nur bei echtem Sub-only-Signal."""
    if not isinstance(room, dict):
        return False
    for k in ("live_sub_only", "liveSubOnly", "sub_only", "subOnly"):
        v = room.get(k)
        if v is True or (isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0):
            return True

    def _scan(node, depth):
        if depth > 4:
            return False
        if isinstance(node, dict):
            for kk, vv in node.items():
                kl = str(kk).lower()
                if "sub_only" in kl or "subonly" in kl:
                    if vv is True or (isinstance(vv, (int, float)) and not isinstance(vv, bool) and vv > 0):
                        return True
                    if isinstance(vv, str) and vv.strip().lower() not in ("", "0", "false", "none", "null"):
                        return True
                if isinstance(vv, (dict, list)) and _scan(vv, depth + 1):
                    return True
        elif isinstance(node, list):
            for it in node[:50]:
                if isinstance(it, (dict, list)) and _scan(it, depth + 1):
                    return True
        return False
    try:
        return _scan(room, 0)
    except Exception:
        return False
