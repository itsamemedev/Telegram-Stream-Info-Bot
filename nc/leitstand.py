"""nc.leitstand — v5.10-W207: die Übersicht als Leitstand, jeder Tab ein Live-Panel.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber zeigte ein Video eines dichten Leitstands — viele kleine
Panels, die gleichzeitig leben, Lichtströme zwischen ihnen, Agenten, die
dorthin fliegen, wo sie arbeiten, und ein „Schlüsselmoment", wenn etwas
passiert — und schrieb: „So habe ich mir die Übersicht vorgestellt …
Bedenke, dass alle anderen Tabs integriert werden müssen."

Die Übersicht hatte bis hierher Kennzahlen, das Lagebild und drei Kacheln
mit Links. Von den neun anderen Tabs sah man auf ihr nichts. Jetzt steht
jeder Tab als eigene Tafel da, mit seiner Lage und seinen lebenden Werten,
und ein Klick führt hinein.

════════════════════════════════════════════════════════════════════════
WARUM DIE LAGE HIER ENTSCHIEDEN WIRD UND NICHT IM JAVASCRIPT
════════════════════════════════════════════════════════════════════════
Dieselbe Regel wie beim Lagebild (W112): eine Animation ist eine Aussage.
Ob eine Tafel rot, gelb oder ruhig ist, ob eine Wächter-Drohne zur
System-Tafel oder zum Restream fliegt, ob ein Ereignis als Schlüsselmoment
aufpoppt — das entscheidet dieses Modul, und Verträge halten es fest. Das
JS wählt nur Farbe und Text zu `lage` und `grund` und bewegt, was hier
entschieden wurde.

Und wie dort: **nichts geladen ist nicht dasselbe wie nichts da** (W99).
Eine Quelle, die nicht gelesen werden konnte, macht ihre Tafel
„unbekannt" — nie „ok".

Rein: keine Datenbank, kein Netz, keine Uhr. Die Rohdaten sammelt
nc/routes/leitstand.py.
"""

LAGEN = ("fehler", "warn", "unbekannt", "aktiv", "ok", "aus")

# Die neun Tabs ausser der Übersicht, in der Reihenfolge der Tab-Leiste.
# (Tab, Nummer, Kennung). Die Kennung ist der kleine Code-Titel der Tafel —
# bewusst keine Übersetzung: sie benennt die Datenquelle, nicht den Inhalt.
TAFELN = (
    ("restream", "01", "restream.spuren"),
    ("wall", "02", "live.wand"),
    ("discord", "03", "community.puls"),
    ("system", "04", "kern.last"),
    ("brain", "05", "waechter.netz"),
    ("betrieb", "06", "betrieb.schlangen"),
    ("insights", "07", "signal.radar"),
    ("einstellungen", "08", "konfig.stand"),
    ("mcp", "09", "mcp.verbindungen"),
)

# Die Lieferkette einer Sendung, links nach rechts. Die Lichtströme der
# Übersicht laufen an ihr entlang, ihre Stärke folgt dem Wert.
KETTE = ("erfassen", "live", "aufnahme", "kodieren", "versand", "restream", "archiv")

# v5.10-W208: welcher Bereich der Seite ein Glied fuehrt — ein Klick auf das
# Glied springt dorthin.
KETTE_TAB = {"erfassen": "wall", "live": "wall", "aufnahme": "wall", "kodieren": "betrieb",
             "versand": "betrieb", "restream": "restream", "archiv": "insights"}

# Wie viele Namen die Live-Wand und wie viele Spuren der Restream zeigt.
MAX_NAMEN = 12
MAX_SPUREN = 4
MAX_EREIGNISSE = 14

# Lastgrenzen der Maschine. Die Last je Kern teilt nc.sysload schon in
# ok/busy/overloaded; hier kommen Platte, Speicher und Swap dazu. Die Platte
# ist die gefaehrlichste: voll heisst, jede laufende Aufnahme bricht ab.
PLATTE_WARN, PLATTE_FEHLER = 85.0, 95.0
SPEICHER_WARN, SPEICHER_FEHLER = 85.0, 95.0
SWAP_WARN = 80.0

# Unter dieser Trefferquote sagt die Insights-Tafel „niedrig" — aber erst ab
# genug Versuchen, sonst ist eine verpasste Aufnahme von zweien „50 %".
QUOTE_WARN, QUOTE_MIN_VERSUCHE = 50.0, 10

# Waechter-Arbeitsort (nc.lagebild.ORT) -> Tafel, zu der die Drohne fliegt.
# „ziel" (ein Nutzer) haengt am Waechter: der Restream-Waechter zum
# Restream, Aufnahme und Scout zur Live-Wand.
ORT_TAFEL = {
    "kern": "system",
    "platte": "system",
    "datenbank": "betrieb",
    "tunnel": "betrieb",
    "beobachtung": "betrieb",
    "abwehr": "insights",
    "chat": "discord",
    "archiv": "insights",
}

# Ereignisse, die gut sind (gruen) — und welche davon ein Schlüsselmoment.
# Eine gesicherte Aufnahme ist gut, aber Alltag: bei 40 Trackings poppte sonst
# alle paar Minuten ein Fenster auf, und ein Moment, der dauernd kommt, ist
# keiner mehr.
GUT = ("restream.start", "clip.hype", "recording.saved", "recording.restored",
       "kickmod.start", "stream.resolve.ok", "recording.session.joined",
       "backup.system")
GUT_MOMENT = ("restream.start", "clip.hype")
FEHLER_STUFEN = ("error", "critical", "fatal")

# Ereignisart (Praefix vor dem ersten Punkt) -> Tafel, die bei einem
# Schluesselmoment aufleuchtet. Ohne Treffer leuchtet keine — lieber keine
# Tafel als die falsche.
EREIGNIS_TAFEL = {
    "restream": "restream",
    "recording": "wall",
    "manual": "wall",
    "clip": "wall",
    "stream": "wall",
    "tracking": "wall",
    "live_react": "discord",
    "kickmod": "discord",
    "watchdog": "system",
    "disk": "system",
    "backup": "betrieb",
    "archive": "insights",
    "retention_apply": "betrieb",
    "update_rollback": "einstellungen",
    "update_restart": "einstellungen",
}
WARN_STUFEN = ("warning", "warn")


def _gelesen(gelesen, *namen) -> bool:
    """Nur was ausdruecklich gelesen wurde, zaehlt. Eine Quelle, die gar
    nicht erst gefragt wurde, ist genauso unbekannt wie eine, die scheiterte."""
    return all(gelesen.get(n) is True for n in namen)


def _tafel(tab, lage, grund, wert=None, **daten):
    nr, kennung = next((n, k) for t, n, k in TAFELN if t == tab)
    return {"tab": tab, "nr": nr, "kennung": kennung, "lage": lage,
            "grund": grund, "wert": wert, "daten": daten}


def _unbekannt(tab):
    return _tafel(tab, "unbekannt", "nicht_geladen")


# ─── die neun Tafeln ─────────────────────────────────────────────────────

_RS_RANG = {"gestoert": 0, "langsam": 1, "gesund": 2}


def _restream(roh, gelesen):
    if not _gelesen(gelesen, "restream"):
        return _unbekannt("restream")
    gesundheit = {e.get("user", "").lstrip("@").lower(): e
                  for e in (roh.get("restream") or ())}
    lagen = {z["name"]: z["restream"]
             for z in ((roh.get("lagebild") or {}).get("ziele") or ()) if z.get("restream")}
    spuren = []
    for user, e in gesundheit.items():
        spuren.append({"name": user, "lage": lagen.get(user, "gesund" if not e.get("slow") else "langsam"),
                       "speed": e.get("speed"), "bitrate": e.get("bitrate"),
                       "fps": e.get("fps"), "ziele": int(e.get("ntargets") or 0)})
    # Ein Restream, den das Lagebild kennt, die Gesundheit aber nicht (noch
    # kein ffmpeg-Fortschritt), steht trotzdem da — ohne Zahlen.
    for user, lage in lagen.items():
        if user not in gesundheit:
            spuren.append({"name": user, "lage": lage, "speed": None, "bitrate": None,
                           "fps": None, "ziele": 0})
    spuren.sort(key=lambda s: (_RS_RANG.get(s["lage"], 3), s["name"]))
    n = len(spuren)
    if not n:
        return _tafel("restream", "ok", "ruht", 0, spuren=[])
    schlimmste = spuren[0]["lage"]
    lage, grund = {"gestoert": ("fehler", "gestoert"),
                   "langsam": ("warn", "langsam")}.get(schlimmste, ("aktiv", "sendet"))
    return _tafel("restream", lage, grund, n, spuren=spuren[:MAX_SPUREN],
                  weitere=max(0, n - MAX_SPUREN),
                  gestoert=sum(1 for s in spuren if s["lage"] == "gestoert"),
                  langsam=sum(1 for s in spuren if s["lage"] == "langsam"))


def _wall(roh, gelesen):
    if not _gelesen(gelesen, "lagebild") and not _gelesen(gelesen, "zaehler"):
        return _unbekannt("wall")
    lb = roh.get("lagebild") or {}
    z = roh.get("zaehler") or {}
    ziele = lb.get("ziele") or []
    live = z.get("live")
    if live is None:
        live = sum(1 for x in ziele if x.get("live"))
    aufnahme = sum(1 for x in ziele if x.get("aufnahme"))
    namen = [{"name": x["name"], "aufnahme": bool(x.get("aufnahme")),
              "restream": x.get("restream")}
             for x in ziele if x.get("live")][:MAX_NAMEN]
    getrackt = z.get("trackings", lb.get("getrackt"))
    lage, grund = ("aktiv", "live") if live else ("ok", "niemand_live")
    return _tafel("wall", lage, grund, int(live or 0), live=int(live or 0),
                  aufnahme=aufnahme, getrackt=getrackt, namen=namen,
                  weitere=max(0, int(live or 0) - len(namen)))


def _discord(roh, gelesen):
    if not _gelesen(gelesen, "community"):
        return _unbekannt("discord")
    c = roh.get("community") or {}
    daten = dict(mitglieder=c.get("mitglieder"), server=c.get("server"),
                 bekannt=c.get("bekannt"), stammgaeste=c.get("stammgaeste"),
                 chat_rate=c.get("chat_rate"), chat_basis=c.get("chat_basis"),
                 verbunden=bool(c.get("discord_verbunden")))
    wert = c.get("mitglieder") if c.get("mitglieder") is not None else c.get("bekannt")
    if not c.get("discord_verbunden"):
        # Ein konfigurierter Bot ohne Verbindung ist eine Stoerung (W-Discord-
        # Gateway-Tod blieb monatelang unsichtbar); ohne Token ist es Absicht.
        if c.get("discord_konfiguriert"):
            return _tafel("discord", "warn", "discord_getrennt", wert, **daten)
        return _tafel("discord", "aus", "discord_aus", wert, **daten)
    rate, basis = float(c.get("chat_rate") or 0), float(c.get("chat_basis") or 0)
    if rate > 0 and rate >= 2 * max(basis, 1.0):
        return _tafel("discord", "aktiv", "chat_hype", wert, **daten)
    return _tafel("discord", "ok", "verbunden", wert, **daten)


def _system(roh, gelesen):
    if not _gelesen(gelesen, "system"):
        return _unbekannt("system")
    s = roh.get("system") or {}
    last = s.get("last") or {}
    if not last and s.get("platte_prozent") is None:
        # Weder /proc/loadavg noch die Platte lesbar: keine Messung ist kein
        # ruhiges System.
        return _unbekannt("system")
    kerne = int(s.get("kerne") or 1)
    cpu = round(100.0 * float(last.get("per_core") or 0), 1)
    ram = s.get("speicher_prozent")
    platte = s.get("platte_prozent")
    swap = float(s.get("swap_pct") or 0)
    befunde = []      # (lage, grund) — der schlimmste gewinnt
    if platte is not None and platte >= PLATTE_FEHLER:
        befunde.append(("fehler", "platte_voll"))
    elif platte is not None and platte >= PLATTE_WARN:
        befunde.append(("warn", "platte_knapp"))
    zustand = last.get("state")
    if zustand == "overloaded":
        befunde.append(("fehler", "ueberlast"))
    elif zustand == "busy":
        befunde.append(("warn", "last_hoch"))
    if ram is not None and ram >= SPEICHER_FEHLER:
        befunde.append(("fehler", "speicher_voll"))
    elif ram is not None and ram >= SPEICHER_WARN:
        befunde.append(("warn", "speicher_knapp"))
    if swap >= SWAP_WARN:
        befunde.append(("warn", "swap_hoch"))
    befunde.sort(key=lambda b: LAGEN.index(b[0]))
    lage, grund = befunde[0] if befunde else ("ok", "ruhig")
    # Die Farbe jedes Rings — dieselben Grenzen wie die Lage der Tafel, damit
    # ein gelber Ring nie neben einer „ruhigen" Tafel steht.
    stufen = {"cpu": {"overloaded": "fehler", "busy": "warn", "ok": "ok"}.get(zustand, "unbekannt"),
              "ram": _stufe(ram, SPEICHER_WARN, SPEICHER_FEHLER),
              "platte": _stufe(platte, PLATTE_WARN, PLATTE_FEHLER)}
    return _tafel("system", lage, grund, cpu, cpu=cpu, ram=ram, platte=platte, stufen=stufen,
                  swap=swap, kerne=kerne, load=(last.get("avg") or {}).get("1m"),
                  platte_frei_gb=s.get("platte_frei_gb"),
                  fresser=list(s.get("fresser") or [])[:3])


def _stufe(wert, warn, fehler):
    if wert is None:
        return "unbekannt"
    return "fehler" if wert >= fehler else ("warn" if wert >= warn else "ok")


def _brain(roh, gelesen):
    if not _gelesen(gelesen, "ki") and not _gelesen(gelesen, "lagebild"):
        return _unbekannt("brain")
    k = roh.get("ki") or {}
    ags = (roh.get("lagebild") or {}).get("agenten") or []
    aktiv = sum(1 for a in ags if a.get("lage") != "aus")
    taetig = sum(1 for a in ags if a.get("lage") == "taetig")
    llm = k.get("llm") or {}
    daten = dict(agenten=len(ags), aktiv=aktiv, taetig=taetig,
                 fehler=sum(1 for a in ags if a.get("lage") == "fehler"),
                 ueberfaellig=sum(1 for a in ags if a.get("ueberfaellig")),
                 befunde=sum(int(a.get("befunde") or 0) for a in ags),
                 wahl=k.get("wahl") or k.get("chat"), lokal_oben=k.get("lokal_oben"),
                 zaehler=dict(k.get("zaehler") or {}),
                 belegt=int(llm.get("belegt") or 0), wartend=int(llm.get("wartend") or 0),
                 plaetze=llm.get("plaetze"))
    wert = "%d/%d" % (aktiv, len(ags)) if ags else None
    if k and k.get("bruecke_ok") is False:
        return _tafel("brain", "fehler", "bruecke", wert, **daten)
    if daten["fehler"]:
        return _tafel("brain", "fehler", "waechter_fehler", wert, **daten)
    if daten["ueberfaellig"]:
        # Ein Waechter, der seinen Takt dreimal verpasst, heisst: der
        # Bridge-Tick laeuft nicht (W116) — die Stoerung hinter allen.
        return _tafel("brain", "warn", "waechter_ueberfaellig", wert, **daten)
    if daten["wahl"] == "lokal" and k.get("lokal_oben") is False:
        # „Lokal" gewaehlt und kein lokaler Server: jede Frage scheitert.
        return _tafel("brain", "warn", "lokal_aus", wert, **daten)
    if daten["belegt"] or daten["wartend"]:
        return _tafel("brain", "aktiv", "denkt", wert, **daten)
    if taetig:
        return _tafel("brain", "aktiv", "patrouille", wert, **daten)
    return _tafel("brain", "ok", "wach", wert, **daten)


def _betrieb(roh, gelesen):
    if not _gelesen(gelesen, "lagebild"):
        return _unbekannt("betrieb")
    dienste = list((roh.get("lagebild") or {}).get("dienste") or [])
    if not dienste:
        return _unbekannt("betrieb")
    schlimmste = sorted(dienste, key=lambda d: LAGEN.index(d.get("lage", "unbekannt")))[0]
    lage = schlimmste.get("lage", "unbekannt")
    # Alles aus oder alles bereit: dann sagt die Tafel „ruhig", nicht den
    # Namen eines abgeschalteten Dienstes.
    grund = (schlimmste["name"] + ":" + schlimmste.get("grund", "")) \
        if lage in ("fehler", "warn", "unbekannt", "aktiv") else "ruhig"
    enc = next((d for d in dienste if d.get("name") == "encode"), {}).get("werte") or {}
    wert = int(enc.get("laeuft") or 0) + int(enc.get("wartet") or 0)
    return _tafel("betrieb", lage, grund, wert,
                  dienste=[{"name": d.get("name"), "lage": d.get("lage"),
                            "grund": d.get("grund")} for d in dienste])


def _insights(roh, gelesen):
    if not _gelesen(gelesen, "insights"):
        return _unbekannt("insights")
    i = roh.get("insights") or {}
    quote = float(i.get("quote") or 0)
    versuche = int(i.get("versuche") or 0)
    tage = [int(t.get("count") or 0) for t in (i.get("tage") or ())]
    daten = dict(quote=quote, versuche=versuche, erfolgreich=int(i.get("erfolgreich") or 0),
                 tage=tage, heute=tage[-1] if tage else 0, abwehr=i.get("abwehr"))
    if versuche >= QUOTE_MIN_VERSUCHE and quote < QUOTE_WARN:
        return _tafel("insights", "warn", "quote_niedrig", quote, ring="warn", **daten)
    return _tafel("insights", "ok", "quote", quote, ring="ok" if versuche else "aus", **daten)


def _einstellungen(roh, gelesen):
    if not _gelesen(gelesen, "einstellungen"):
        return _unbekannt("einstellungen")
    e = roh.get("einstellungen") or {}
    zahl = dict(e.get("zahl") or {})
    neustart = list(e.get("neustart") or [])
    daten = dict(zahl=zahl, geschuetzt=int(e.get("geschuetzt") or 0),
                 neustart=len(neustart), backend=e.get("backend"))
    wert = int(zahl.get("datenbank") or 0)
    if neustart:
        # Im Deck geaendert, aber der Prozess liest den Wert erst nach einem
        # Neustart — dieselbe Lage wie ein eingespieltes Update (W104).
        return _tafel("einstellungen", "warn", "neustart_noetig", wert, **daten)
    return _tafel("einstellungen", "ok", "aktuell", wert, **daten)


def _mcp(roh, gelesen):
    if not _gelesen(gelesen, "mcp"):
        return _unbekannt("mcp")
    m = roh.get("mcp") or {}
    anzahl, aktiv = int(m.get("anzahl") or 0), int(m.get("aktiv") or 0)
    webui = m.get("webui") or {}
    daten = dict(anzahl=anzahl, aktiv=aktiv, webui=webui.get("webui"),
                 proxy=bool(webui.get("mcp_proxy")), abhilfe=bool(webui.get("abhilfe")))
    wert = "%d/%d" % (aktiv, anzahl)
    if not anzahl:
        return _tafel("mcp", "aus", "keine_server", wert, **daten)
    if webui.get("gefunden") and webui.get("abhilfe"):
        # Server eingetragen, aber die Oberflaeche, die sie anbietet, ist
        # nicht so eingerichtet, dass sie sie zeigt (W197/W198).
        return _tafel("mcp", "warn", "webui_fehlt", wert, **daten)
    return _tafel("mcp", "ok", "bereit", wert, **daten)


_BAUER = {"restream": _restream, "wall": _wall, "discord": _discord, "system": _system,
          "brain": _brain, "betrieb": _betrieb, "insights": _insights,
          "einstellungen": _einstellungen, "mcp": _mcp}


def tafeln(roh, gelesen=None) -> list:
    """Rohdaten -> die neun Tafeln in der Reihenfolge der Tab-Leiste."""
    roh, gelesen = roh or {}, gelesen or {}
    return [_BAUER[tab](roh, gelesen) for tab, _nr, _k in TAFELN]


# ─── Lieferkette, Drohnen, Ereignisse ────────────────────────────────────

def _glied(name, wert, lage):
    return {"name": name, "wert": wert, "lage": lage, "tab": KETTE_TAB.get(name)}


def kette(roh, gelesen, fertig) -> list:
    """Die sieben Glieder der Lieferkette. `fertig` sind die gebauten Tafeln
    (dieselbe Lage soll an beiden Stellen dieselbe sein)."""
    t = {x["tab"]: x for x in fertig}
    wall, rs, ins = t["wall"], t["restream"], t["insights"]
    dienste = {d["name"]: d for d in ((roh.get("lagebild") or {}).get("dienste") or ())}

    def dienst(name, *felder):
        d = dienste.get(name) or {}
        werte = d.get("werte") or {}
        return _glied(name, sum(int(werte.get(f) or 0) for f in felder), d.get("lage", "unbekannt"))

    enc, upl = dienst("encode", "laeuft", "wartet"), dienst("upload", "wartend")
    enc["name"], upl["name"] = "kodieren", "versand"
    enc["tab"], upl["tab"] = KETTE_TAB["kodieren"], KETTE_TAB["versand"]
    erfasst = (roh.get("zaehler") or {}).get("trackings")
    return [
        _glied("erfassen", erfasst, "unbekannt" if erfasst is None else "ok"),
        _glied("live", wall["daten"].get("live"), wall["lage"]),
        _glied("aufnahme", wall["daten"].get("aufnahme"),
               "unbekannt" if wall["lage"] == "unbekannt"
               else ("aktiv" if wall["daten"].get("aufnahme") else "ok")),
        enc, upl,
        _glied("restream", rs["wert"], rs["lage"]),
        _glied("archiv", ins["daten"].get("heute"), ins["lage"] if ins["lage"] == "unbekannt" else "ok"),
    ]


def drohnen(roh, ort_von_name) -> list:
    """Die Waechter als Drohnen: zu welcher Tafel jede fliegt.

    `ort_von_name` ist nc.lagebild.ORT (Name -> „kern", „ziel:restream" …).
    Ein abgeschalteter Waechter fliegt nicht (tafel None = im Hangar) — ein
    Waechter, der patrouilliert, obwohl er aus ist, waere genau die
    Falschanzeige, die das Bild entwertet (W112)."""
    aus = []
    for a in (roh.get("lagebild") or {}).get("agenten") or ():
        if a.get("lage") == "aus":
            tafel = None
        elif a.get("ort") == "ziel":
            art = str(ort_von_name.get(a.get("name"), "")).partition(":")[2]
            tafel = "restream" if art == "restream" else "wall"
        else:
            tafel = ORT_TAFEL.get(a.get("ort"), "system")
        aus.append({"name": a.get("name"), "lage": a.get("lage"), "tafel": tafel,
                    "ziel": a.get("ziel"), "faellig_in_s": a.get("faellig_in_s"),
                    "takt_s": a.get("takt_s"), "ueberfaellig": bool(a.get("ueberfaellig"))})
    return aus


def ereignis(kind, severity) -> dict:
    """Ein Ereignis aus dem Ereignisprotokoll -> {"ton", "moment"}.

    Auch der Live-Push (SSE) traegt diese Einstufung — die Übersicht und das
    Benachrichtigungs-Center sollen ein Ereignis gleich gewichten."""
    k, s = str(kind or ""), str(severity or "").lower()
    tafel = EREIGNIS_TAFEL.get(k.partition(".")[0])
    if s in FEHLER_STUFEN:
        return {"ton": "fehler", "moment": True, "tafel": tafel}
    if s in WARN_STUFEN:
        return {"ton": "warn", "moment": True, "tafel": tafel}
    if k in GUT:
        return {"ton": "gut", "moment": k in GUT_MOMENT, "tafel": tafel}
    return {"ton": "info", "moment": False, "tafel": tafel}


def ereignisse(zeilen) -> list:
    aus = []
    for z in list(zeilen or ())[:MAX_EREIGNISSE]:
        e = {"ts": z.get("ts"), "kind": z.get("kind"), "severity": z.get("severity"),
             "summary": str(z.get("summary") or "")[:160]}
        e.update(ereignis(e["kind"], e["severity"]))
        aus.append(e)
    return aus


def bauen(roh, gelesen, jetzt, ort_von_name=None) -> dict:
    """Der ganze Leitstand aus den Rohdaten (siehe nc/routes/leitstand.py)."""
    roh, gelesen = roh or {}, dict(gelesen or {})
    fertig = tafeln(roh, gelesen)
    zahl = {lage: sum(1 for t in fertig if t["lage"] == lage) for lage in LAGEN}
    return {"ok": True, "tafeln": fertig, "kette": kette(roh, gelesen, fertig),
            "drohnen": drohnen(roh, ort_von_name or {}),
            "ereignisse": ereignisse(roh.get("ereignisse")),
            "zahl": zahl, "quellen": gelesen, "jetzt": round(float(jetzt), 1)}
