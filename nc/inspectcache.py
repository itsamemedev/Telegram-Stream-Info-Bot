"""nc.inspectcache — v4.0-W54: (De-)Serialisierung des Recording-Inspect-Caches.

Die reinen Teile aus get_or_compute_inspect_sync / store_inspect: eine
Cache-Zeile robust zu einem dict parsen (fehlend/kaputt → None, damit der
Aufrufer lazy neu berechnet) und ein Inspect-dict mit hartem Grössendeckel
serialisieren. DB-Lesen/Schreiben bleibt beim Aufrufer. Bitgenau gegen den
Monolithen geprüft.
"""

import json

INSPECT_JSON_CAP = 200000     # max. Zeichen im Cache — schützt vor Riesen-Payloads


def parse_row(row):
    """Aus einer recording_inspect_cache-Zeile das inspect_json parsen. Kein
       Eintrag oder kaputtes JSON → None (Aufrufer triggert dann eine frische
       Inspection)."""
    if row and row["inspect_json"]:
        try:
            return json.loads(row["inspect_json"])
        except Exception:
            return None
    return None


def serialize(data):
    """Inspect-dict → JSON-String, ensure_ascii=False (Unicode bleibt lesbar),
       hart auf INSPECT_JSON_CAP Zeichen begrenzt."""
    return json.dumps(data, ensure_ascii=False)[:INSPECT_JSON_CAP]
