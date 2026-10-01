"""nc.tunnelwacht — v4.2-W105: prueft von selbst, ob der Egress wirklich steht.

DER ANLASS. Der Betreiber am 01.10.: „anscheinend gibt's Probleme das der bot
nicht mehr automatisch mit dem Polen vps verbindet". Nachgesehen, und der
Befund war nicht der Tunnel, sondern dass ihn nichts beobachtet:
`_TUNNEL["last_test"]` wurde AUSSCHLIESSLICH von der Dashboard-Route
`/api/tunnel/test` geschrieben. Es gab keine Schleife. Ein toter Polen-VPS
sah damit genauso aus wie ein gesunder — es ging nur nichts, und das in der
Klasse Fehler, die dieses Projekt am teuersten bezahlt hat (W81, W92, W104:
es faellt nichts, es meldet sich nichts).

VIER LAGEN, und drei davon sind KEIN Alarm. Das ist der Teil, der die Meldung
brauchbar macht:

    ok      Proxy gesetzt, TikTok antwortet darueber   -> still
    direkt  kein Proxy konfiguriert                    -> still (Normalfall
            fuer jeden Bestand ohne VPS; eine Meldung, die auf jeder zweiten
            Installation rot ist, erzieht zum Wegsehen — Begruendung aus W85)
    aus     forced_off: der Betreiber hat den Knopf im Deck gedrueckt
            -> INFO, gedrosselt. Absichtlich NICHT still: genau „ich habe das
            vor drei Wochen abgeschaltet" ist die Lage, die als Stoerung
            gemeldet wird.
    fehler  der Weg, der benutzt WIRD, traegt nicht    -> ERROR mit Abhilfe

DIE MASKE IST PFLICHT, nicht Kosmetik. Ein Proxy darf `user:pass@host`
enthalten, und das Ergebnis dieser Probe geht in eine API-Antwort UND ins Log.
Deshalb laeuft nicht nur `via` durch `_tunnel_mask`, sondern auch die
Fehlerausgabe von curl: sie zitiert die Adresse, die sie nicht erreicht hat.
"""

import subprocess
from datetime import datetime, timezone

from nc.fehlertext import nach_aussen, saeubern
from nc.proxyutil import _tunnel_mask

LAGE_OK = "ok"
LAGE_DIREKT = "direkt"
LAGE_AUS = "aus"
LAGE_FEHLER = "fehler"

# Wogegen geprueft wird. tiktok.com und nicht ein neutrales ip-echo: die Frage
# ist nicht „habe ich Internet", sondern „komme ich bei TikTok an" — ein Proxy,
# dessen IP TikTok sperrt, ist fuer diesen Bot genauso kaputt wie ein toter.
ZIEL = "https://www.tiktok.com/"
TIMEOUT_CURL = 10
TIMEOUT_PROZESS = 14

TEXTE = {
    LAGE_FEHLER: (
        "EGRESS DEFEKT: TikTok antwortet ueber %(via)s nicht (%(code)s%(err)s). "
        "Folge: Aufnahme, Resolver und Chat laufen alle ueber diesen Weg — "
        "was jetzt noch durchkommt, kommt zufaellig durch. Abhilfe: den Proxy "
        "pruefen (RECORD_PROXY in der .env), oder im Deck unter Tunnel auf "
        "direkt stellen, bis der VPS wieder laeuft."),
    LAGE_AUS: (
        "Tunnel ist im Deck ABGESCHALTET (forced_off) — Aufnahme und Chat "
        "laufen ueber die Server-IP, obwohl ein Proxy konfiguriert ist. Das "
        "ist bei einer Datacenter-IP der haeufigste Grund fuer 403 und fuer "
        "\u201elive, aber keine Stream-URL\u201c. Abhilfe: im Deck unter Tunnel "
        "wieder einschalten."),
}


def probe_cmd(eff):
    """Die curl-Zeile fuer die Erreichbarkeitsprobe.

    EINE Fassung fuer Deck-Knopf und Waechter. Vorher stand sie nur in
    `/api/tunnel/test`; eine zweite daneben waere der Fehler aus W98 (zwei
    Listen fuer denselben Zweck) an einer Stelle, an der beide Seiten
    behaupten, dasselbe zu messen.
    """
    cmd = ["curl", "--max-time", str(TIMEOUT_CURL), "-sS", "-o", "/dev/null",
           "-w", "%{http_code} %{time_total}", "-A", "Mozilla/5.0", ZIEL]
    if eff:
        cmd = cmd[:1] + ["-x", eff] + cmd[1:]
    return cmd


def _fehlerausgabe(roh):
    """curl-stderr fuer Log und API: maskiert und entschaerft.

    `_tunnel_mask` zuerst — die Ausgabe zitiert die Proxy-Adresse, die sie
    nicht erreicht hat, und die kann user:pass tragen. `saeubern` danach fuer
    Pfade und lange Geheimnisse.

    EINE Maske, nicht zwei. Der erste Entwurf ersetzte zusaetzlich die
    Proxy-Zeichenkette woertlich im Text — das sah nach doppelter Sicherheit
    aus und war keine: eine Mutationsprobe, die diese Zeile entfernte, blieb
    gruen, weil `_tunnel_mask` denselben Fall schon abdeckt. Zwei Riegel, von
    denen einer wirkt, sind ein Riegel und eine falsche Gewissheit (W98).
    Die Probe hat dabei das eigentliche Loch gezeigt: `_tunnel_mask` verlangte
    `://` und liess ein schemaloses `nutzer:pass@host` durch — behoben in
    nc/proxyutil.py, also an der Stelle, an der ALLE elf Aufrufer davon haben.

    EIN Ausgang (wie nc/ytdlpurl.py seit W102, nc/livecache.py seit W103): ein
    frueher `return None` in einem reinen Abbild ohne Logger ist fuer
    tools/blindstellen.py ein stummer Fehlerpfad.
    """
    text = (roh or "").strip()
    sauber = saeubern(_tunnel_mask(text) or "")[:200] if text else ""
    return sauber or None


def probe(eff, jetzt_ms=None):
    """TikTok ueber `eff` anfragen -> Ergebnis-Woerterbuch wie bisher.

    Die Form ist bewusst bitgenau die der alten Route ({ok, http_code, via,
    ms, err, at}) — das Deck liest sie, und ein stiller Formwechsel waere ein
    leeres Feld im Lagebild statt einer Fehlermeldung.
    """
    import time as _t
    t0 = _t.time()
    maske = _tunnel_mask(eff) or "direkt"
    try:
        r = subprocess.run(probe_cmd(eff), capture_output=True, text=True,
                           timeout=TIMEOUT_PROZESS)
        out = (r.stdout or "").strip()
        code = out.split(" ")[0] if out else "0"
        ok = code.startswith(("2", "3"))
        err = _fehlerausgabe(r.stderr) if not ok else None
    except Exception as e:
        code, ok = "0", False
        err = saeubern(nach_aussen(e, "tunnelwacht"))[:200]
    return {"ok": ok, "http_code": code, "via": maske,
            "ms": int((_t.time() - t0) * 1000) if jetzt_ms is None else jetzt_ms,
            "err": err,
            "at": datetime.now(timezone.utc).strftime("%H:%M:%S")}


def _code_text(code) -> str:
    """„HTTP 403" oder „keine Antwort" — curl liefert bei Verbindungsfehlern
    `000`, nicht `0`. Eine Meldung „HTTP 000" sieht nach einem Statuscode aus
    und ist keiner; gemessen gegen curl 8.x beim Fehlschlag auf einen toten
    Proxy."""
    roh = str(code or "").strip()
    if not roh or set(roh) <= {"0"}:
        return "keine Antwort"
    return "HTTP %s" % roh


def lage(res, hat_proxy, forced_off) -> str:
    """Welche der vier Lagen ist das? -> LAGE_*

    Die Reihenfolge ist die Aussage: `forced_off` gewinnt vor dem Messwert,
    weil „abgeschaltet" die Erklaerung IST und nicht zusaetzlich als Defekt
    gemeldet werden soll. Und ein Bestand ohne Proxy ist nie ein Fehler,
    auch wenn die Probe scheitert — dann ist TikTok nicht erreichbar, und das
    meldet der Resolver bereits laut genug (W102).
    """
    if forced_off and hat_proxy:
        return LAGE_AUS
    if not hat_proxy:
        return LAGE_DIREKT
    return LAGE_OK if (res or {}).get("ok") else LAGE_FEHLER


def meldung(lg, res):
    """-> (stufe, text) oder (None, None), wenn diese Lage still ist."""
    aus = (None, None)            # EIN Ausgang, Begruendung wie oben
    if lg == LAGE_FEHLER:
        r = res or {}
        err = r.get("err")
        aus = ("error", TEXTE[LAGE_FEHLER] % {
            "via": r.get("via") or "direkt",
            "code": _code_text(r.get("http_code")),
            "err": ": %s" % err if err else "",
        })
    elif lg == LAGE_AUS:
        aus = ("info", TEXTE[LAGE_AUS])
    return aus
