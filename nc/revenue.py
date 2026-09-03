"""nc.revenue — v4.1-W20: welche Plattform Geld auf EIGENE Kanaele bringt.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die Trennlinie stand als Konstantenpaar im Monolithen und wird von den
Overlay-, Spenden- und Finanzamt-Routen gebraucht. Als nc.ctx-Eintraege waeren
das drei der 25 vertraglichen Plaetze — fuer vier Zeilen Wahrheit.

**TikTok gehoert nicht dazu, und das ist kein Versehen.** TikTok-Gifts gehen an
den GETRACKTEN Streamer, nicht an unsere eigenen Kanaele. Sie sind fremdes
Geld, das wir beim Mitschneiden nur vorbeifliegen sehen. Sie im Spenden-Panel,
im Spendenziel oder gar in der Finanzamt-Auswertung mitzuzaehlen wuerde
Einnahmen erfinden, die es nie gegeben hat (B120). Dieselbe Trennlinie wie in
nc/modstats.py fuer die Moderation.

`sql_in()` ist bewusst eine Funktion und keine Konstante: sie wird direkt in
SQL eingesetzt, und ein eingefrorener String waere nach einer Aenderung an
PLATFORMS still veraltet.

**Warum hier kein `COALESCE(platform,'kick')` steht** (B138-GELD): frueher
lauteten die Abfragen so. Damit wurde jede Zeile OHNE Plattform-Angabe
stillschweigend zu Kick erklaert und als eigene Einnahme gezaehlt — betroffen
sind Altbestaende aus der Zeit, als TikTok-Gifts noch als 'donation' mit leerer
Plattform geschrieben wurden. Im Panel tauchten dann TikTok-Namen unter KICK
auf und blaehten die Summe auf. Jetzt steht dort schlicht `platform IN (…)`:
`NULL IN (…)` ergibt NULL, also nicht TRUE, und die Zeile faellt heraus.
"Herkunft unbekannt" ist eben KEINE Einnahme.

Nicht zu verwechseln mit `nc.ledger.PLATFORMS`: das sind BUCHUNGS-Kategorien
fuer die Steuer (dort heisst der Sammelposten "sonstige"), hier stehen
EINNAHME-Quellen (dort "manuell"). Die beiden Listen sehen aehnlich aus und
sind es nicht — der Kommentar in nc/ledger.py, sie seien deckungsgleich, ist
falsch. Anzeigewert ≠ Auszahlung, siehe CLAUDE.md.
"""

# Plattformen, deren Geld auf UNSERE Kanaele einzahlt.
PLATFORMS = ("kick", "twitch", "youtube", "manuell")

# Woher ein Overlay-Ereignis kommen kann. TikTok steht hier sehr wohl drin:
# Follows von dort sind Reichweite und duerfen ins Sendebild — nur Geld nicht.
OV_PLATFORMS = ("kick", "twitch", "youtube", "tiktok")


def is_revenue_platform(platform) -> bool:
    """Zaehlt Geld von dieser Plattform auf UNSERE Kanaele ein?"""
    return (platform or "").strip().lower() in PLATFORMS


def normalisieren(platform) -> str:
    """Overlay-Plattform normalisieren; Unbekanntes wird 'kick' (der Default,
       der alte Aufrufer ohne Plattform-Angabe kompatibel haelt)."""
    p = (platform or "kick").strip().lower()
    return p if p in OV_PLATFORMS else "kick"


def sql_in() -> str:
    """Die IN-Liste fuer SQL. Funktion statt Konstante — siehe Modul-Kopf."""
    return "('" + "','".join(PLATFORMS) + "')"
