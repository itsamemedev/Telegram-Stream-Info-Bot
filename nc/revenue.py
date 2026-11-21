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
EINNAHME-Quellen (dort "manual"). Die beiden Listen sehen aehnlich aus und
sind es nicht — der Kommentar in nc/ledger.py, sie seien deckungsgleich, ist
falsch. Anzeigewert ≠ Auszahlung, siehe CLAUDE.md.
"""

# Plattformen, deren Geld auf UNSERE Kanaele einzahlt.
# v4.2-W164: "manual" statt "manuell". Gespeichert werden manuell erfasste
# Spenden seit W102 als platform='manual' (nc/routes/money.py) — "manuell"
# kam in keiner einzigen Zeile vor. Der Eintrag war damit tot, und eine
# PayPal- oder Krypto-Spende, die der Betreiber im Deck eintrug, fehlte im
# Spendenziel des Overlays, in den Spendenlisten und in der Gegenprobe des
# Steuer-Journals. Doppelt gezaehlt wird dadurch nichts: der Fortschritt der
# Website rechnet getrennt (DONATION_CURRENT_EUR + nc.donationsdb.manual_total)
# und benutzt diese Liste nicht.
PLATFORMS = ("kick", "twitch", "youtube", "manual")

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


def tiktok_geschenk(ev) -> tuple:
    """LIVE-5: (fertig, diamanten) eines TikTokLive-GiftEvent.

    Ein Combo-Geschenk (Rose x 30) kommt NICHT als ein Ereignis. TikTokLive 6.x
    feuert je Streak-Schritt ein GiftEvent mit wachsendem `repeat_count`, und
    erst das letzte traegt `repeat_end` — die Bibliothek fasst das als
    Eigenschaft `streaking` zusammen (TikTokLive/events/proto_events.py,
    6.6.5: `not gift.streakable -> False`, sonst `not repeat_end`) und rechnet
    ihren eigenen `value` aus genau diesem Grund nur am Ende („Prevent
    double-count"). Wir zaehlten jeden Schritt: aus 30 Rosen wurden
    1+2+…+30 = 465 Diamanten, je Schritt ein clip_moment, eine
    Sendebild-Zeile und (bei OVERLAY_GIFT_SOURCE=tiktok) eine overlay_events-
    Zeile.

    `fertig` ist False fuer einen Zwischenschritt — der Aufrufer wertet ihn
    gar nicht. Defensiv ueber getattr: eine Fassung ohne `streaking` gilt als
    fertig — lieber einmal zu viel gezaehlt als ein Geschenk verschluckt.
    Das gilt auch fuer ein GiftEvent ohne Gift-Objekt: dort scheitert die
    Eigenschaft selbst an `None.streakable`, und das ist ein AttributeError,
    den getattr mit Vorgabe schon abfaengt. Ein eigenes try/except darum war
    in der ersten Fassung ein zweiter Riegel, den die Mutationsprobe als
    wirkungslos entlarvt hat (dieselbe Lehre wie W98/W105).
    Der Wert bleibt fremdes Geld (Modulkopf): er landet nie in einer Summe."""
    laeuft = bool(getattr(ev, "streaking", False))
    gift = getattr(ev, "gift", None)
    dia = getattr(gift, "diamond_count", None) or getattr(ev, "diamond_count", None) or 0
    cnt = getattr(ev, "repeat_count", None) or getattr(ev, "combo_count", None) or 1
    # Ziffern statt int()-Versuch: protobuf liefert int, eine kaputte Angabe
    # ist 0 Diamanten — ohne except, das hier nur einen Grund verschluckte.
    wert = (int(dia) * int(cnt)
            if str(dia).isdigit() and str(cnt).isdigit() else 0)
    return (not laeuft, wert)
