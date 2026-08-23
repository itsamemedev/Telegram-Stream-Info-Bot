"""nc.flapguard — v4.0-W116: flatternde Dauerverbindungen sichtbar machen.

════════════════════════════════════════════════════════════════════════
DAS PROBLEM
════════════════════════════════════════════════════════════════════════
Kick-WebSocket, Twitch-EventSub und Twitch-Chat melden ihre Trennung mit
`log.warning`. In einem ERROR-Log erscheint davon NICHTS — und genau das
ist das Muster, das den Discord-Gateway-Tod monatelang verdeckt hat.

Eine einzelne Trennung ist auch voellig normal: Plattformen rotieren ihre
Gateways, Netze haben Aussetzer, ein Reconnect nach fuenf Sekunden ist
kein Vorfall. Deshalb waere "jede Trennung auf error" genauso falsch wie
"jede Trennung auf warning": im ersten Fall verschwindet das Signal im
Rauschen, im zweiten gibt es gar keins.

Was zaehlt, ist der VERLAUF. Vier Trennungen in einer Viertelstunde sind
kein Zufall mehr — dann stimmt etwas mit Token, Netz oder Plattform nicht,
und der Betreiber muss es erfahren, waehrend es passiert.

════════════════════════════════════════════════════════════════════════
WARUM BOT-FREI
════════════════════════════════════════════════════════════════════════
Die Entscheidung "ist das Flattern oder Alltag" ist die heikle Stelle:
zu empfindlich erzeugt sie Alarm-Muedigkeit, zu traege meldet sie nie.
Hier steht sie als reine Funktion ohne Logger, ohne Uhr, ohne Netz —
`now` wird hereingereicht, damit ein Test Stunden in Millisekunden
durchspielen kann.

════════════════════════════════════════════════════════════════════════
DIE VIER REGELN
════════════════════════════════════════════════════════════════════════
1. NUR EIN FENSTER ZAEHLT. Trennungen aelter als `fenster_s` fallen raus.
   Sonst summiert sich ueber Tage jede noch so gesunde Verbindung zum
   Daueralarm.
2. EIN LANGER HALT LOESCHT DIE AKTE. Hielt die Verbindung `ruhe_s` durch,
   war sie gesund; die naechste Trennung faengt bei eins an. Ohne das
   bliebe eine Nacht mit drei Aussetzern bis zum Neustart "verdaechtig".
3. GEMELDET WIRD HOECHSTENS ALLE `melde_abstand_s`. Ein dauerhaft
   kaputter Token trennt sonst im Minutentakt und schreibt das Log voll —
   dieselbe Drosselung wie in _loop_fehler.
4. DIE ERHOLUNG WIRD EINMAL GEMELDET, aber nur wenn vorher Alarm war.
   Sonst weiss niemand, ob das Problem noch besteht.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FlapConfig:
    fenster_s: float = 900.0          # Beobachtungsfenster (15 min)
    schwelle: int = 4                 # so viele Trennungen darin = Flattern
    ruhe_s: float = 600.0             # so lange gehalten = gesund, Akte leeren
    melde_abstand_s: float = 1800.0   # fruehestens wieder melden (30 min)


@dataclass
class FlapUrteil:
    """Was der Aufrufer tun soll. Kein Logger hier — nur die Entscheidung."""
    melden: bool = False              # jetzt laut werden (error + Alarm)
    erholt: bool = False              # war laut, ist wieder ruhig
    anzahl: int = 0                   # Trennungen im Fenster (inkl. dieser)
    fenster_min: int = 0              # Fensterbreite in Minuten, fuer den Text
    grund: str = ""


@dataclass
class _Kanal:
    zeiten: list = field(default_factory=list)   # Zeitstempel der Trennungen
    zuletzt_gemeldet: float = 0.0
    laut: bool = False                # laeuft gerade eine gemeldete Episode?


class FlapWatch:
    """Ein Zustand je Kanal ("kick-ws", "twitch-chat", …)."""

    def __init__(self, cfg: FlapConfig | None = None):
        self.cfg = cfg or FlapConfig()
        self._kanaele: dict = {}

    def _k(self, kanal: str) -> _Kanal:
        return self._kanaele.setdefault(kanal, _Kanal())

    def trennung(self, kanal: str, gehalten_s: float, now: float) -> FlapUrteil:
        """Eine Verbindung ist weggebrochen. `gehalten_s` = wie lange sie
        stand (0 wenn unbekannt — dann zaehlt sie als kurz, was die
        vorsichtigere Annahme ist)."""
        cfg = self.cfg
        k = self._k(kanal)
        erholt = False

        # Regel 2: ein langer Halt loescht die Akte.
        if gehalten_s >= cfg.ruhe_s:
            if k.laut:
                erholt = True
                k.laut = False
            k.zeiten = []

        # Regel 1: nur das Fenster zaehlt.
        k.zeiten = [t for t in k.zeiten if now - t < cfg.fenster_s]
        k.zeiten.append(now)
        n = len(k.zeiten)

        fenster_min = int(cfg.fenster_s // 60)
        if n < cfg.schwelle:
            return FlapUrteil(melden=False, erholt=erholt, anzahl=n,
                              fenster_min=fenster_min)

        # Regel 3: Meldeabstand einhalten — aber erst AB der zweiten
        # Meldung. `zuletzt_gemeldet == 0` heisst "noch nie gemeldet"; ohne
        # diese Bedingung haengt es an der absoluten Groesse der Uhr, ob die
        # ERSTE Meldung durchkommt (mit time.time() zufaellig ja, mit einer
        # monotonen Uhr kurz nach dem Start nein). Genau so ein Fehler faellt
        # im Betrieb nie auf: es meldet einfach nichts.
        if k.zuletzt_gemeldet and (now - k.zuletzt_gemeldet) < cfg.melde_abstand_s:
            return FlapUrteil(melden=False, erholt=erholt, anzahl=n,
                              fenster_min=fenster_min,
                              grund="Flattern, aber im Meldeabstand")
        k.zuletzt_gemeldet = now
        k.laut = True
        return FlapUrteil(
            melden=True, erholt=erholt, anzahl=n, fenster_min=fenster_min,
            grund=f"{n} Trennungen in {fenster_min} Minuten")

    def snapshot(self) -> dict:
        return {k: {"im_fenster": len(v.zeiten), "laut": v.laut}
                for k, v in self._kanaele.items()}
