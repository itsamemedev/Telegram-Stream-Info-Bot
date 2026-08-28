"""nc.news — B163: oeffentliche Projekt-News fuer die Website (bot-frei).

════════════════════════════════════════════════════════════════════════
WOFUER
════════════════════════════════════════════════════════════════════════
Erzeugt in regelmaessigen Abstaenden AN DIE OEFFENTLICHKEIT gerichtete News zu
drei Themen: dem Projekt, den getrackten Creatorn (aggregiert) und der KI. Diese
landen als news.json neben der statischen Website und werden dort im News-Bereich
angezeigt. Das ist legitimes Internet-Marketing: frische, oeffentliche Inhalte,
die ueber Suche/Teilen Besucher anziehen — kein Spam-Push.

Bewusst OEFFENTLICH, nicht ans Entwickler-Team: keine Build-Nummern, keine
internen Fehlerbilder, kein „B163 ausgeliefert". Formuliert wird fuer Leser der
Website. Und bewusst AGGREGIERT bei Creatorn (Anzahl, Aktivitaet) statt einzelne
Personen herauszustellen — datensparsam und zugleich das bessere Marketing.

════════════════════════════════════════════════════════════════════════
v4.1 — WARUM DIE ITEMS AUSFUEHRLICHER SIND
════════════════════════════════════════════════════════════════════════
Bis v4.0 war ein Item EIN Satz. Das las sich wie eine Statuszeile, nicht wie
eine Nachricht: ein Besucher, der zum ersten Mal auf der Seite landet, erfuhr
daraus nichts, was ihn bleiben liess — und eine Suchmaschine fand pro Item ~30
Woerter Text. Ab v4.1 traegt ein Item deshalb mehrere Felder:

    lead      Ein Anreisser-Satz (die Kurzfassung fuer Vorschau und Teaser)
    body      Fliesstext in MEHREREN Absaetzen, getrennt durch "\\n\\n"
    metrics   [{label, value}] — die harten Zahlen als Kennzahlen-Leiste
    bullets   [str] — die Details, die im Fliesstext nur stoeren wuerden
    tags      [str] — Themen-Chips

Alle neuen Felder sind OPTIONAL. Aeltere Items in einer bestehenden news.json
haben sie nicht; die Website rendert dann eben nur, was da ist. Und `body`
bleibt das Feld, das eine optionale KI-Formulierung ersetzt — Kennzahlen und
Details stammen weiterhin ausschliesslich aus echten Fakten und werden von der
KI nie angefasst.

════════════════════════════════════════════════════════════════════════
WARUM BOT-FREI
════════════════════════════════════════════════════════════════════════
Wie nc.marketing/nc.restream_guard steckt die Logik — welche Items, Dedup, wann
generieren — in reinen Funktionen. Der Bot liefert die ECHTEN Fakten (Zahlen aus
DB/Brain) und optionale KI-Formulierungen; erfunden wird hier nichts. So bleibt
die Struktur testbar und ein Fehler kann die Website nicht mit Muell fluten.
"""

from dataclasses import dataclass
import hashlib

PROJECT = "project"
CREATORS = "creators"
AI = "ai"
CATEGORIES = (PROJECT, CREATORS, AI)

CATEGORY_LABEL = {PROJECT: "Projekt", CREATORS: "Creator", AI: "KI"}


@dataclass
class NewsConfig:
    enabled: bool = False
    auto: bool = False                 # Hintergrund-Loop generiert selbst? (Default: nur manuell)
    categories: tuple = CATEGORIES
    cadence_hours: float = 24.0
    quiet_start: int = 0               # start==end → keine Ruhezeit
    quiet_end: int = 0
    max_items: int = 20                # News-Historie deckeln


@dataclass
class NewsState:
    last_gen_ts: float = 0.0
    count: int = 0


def _in_quiet(hour: int, qs: int, qe: int) -> bool:
    qs %= 24
    qe %= 24
    if qs == qe:
        return False
    if qs < qe:
        return qs <= hour < qe
    return hour >= qs or hour < qe


def should_generate(cfg: NewsConfig, state: NewsState, now_ts: float, now_hour: int):
    """Reine Auto-Generier-Entscheidung → (bool, grund)."""
    if not cfg.enabled:
        return False, "disabled"
    if not cfg.auto:
        return False, "manual_only"
    if not cfg.categories:
        return False, "no_categories"
    if _in_quiet(now_hour, cfg.quiet_start, cfg.quiet_end):
        return False, "quiet_hours"
    if state.last_gen_ts and (now_ts - state.last_gen_ts) < cfg.cadence_hours * 3600:
        return False, "cadence"
    return True, "due"


def item_id(category: str, title: str, body: str, extra: str = "") -> str:
    """Inhalts-Id fuer den Dedup in merge(). `extra` nimmt ab v4.1 die neuen
       Felder auf: aendert sich NUR eine Kennzahl oder ein Detailpunkt, ist das
       eine neue Meldung — ohne `extra` waere sie als Duplikat verschwunden."""
    h = hashlib.sha1(f"{category}|{title}|{body}|{extra}".encode("utf-8")).hexdigest()
    return h[:12]


# ════════════════════════════════════════════════════════════════════════
# Bausteine fuer die Texte. Jede Funktion nimmt NUR echte facts entgegen und
# laesst weg, was nicht belegt ist — eine fehlende Zahl wird nie zu einer 0
# im Fliesstext ("0 Fakten gelernt" ist die peinlichste Form von Ehrlichkeit).
# ════════════════════════════════════════════════════════════════════════

def _int(facts: dict, key: str) -> int:
    try:
        return int(facts.get(key) or 0)
    except (TypeError, ValueError):
        return 0


def _platforms_text(facts: dict) -> str:
    p = [n for n in ("Kick", "Twitch", "YouTube") if n in (facts.get("platforms") or [])]
    if not p:
        return "mehreren Plattformen"
    if len(p) == 1:
        return p[0]
    return ", ".join(p[:-1]) + " und " + p[-1]


def _join(parts) -> str:
    """Absaetze zu einem Body. Leere Teile fallen weg — so entsteht nie eine
       Leerzeile, wenn ein Fakt fehlt."""
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def _lead(category: str, facts: dict) -> str:
    """Der Anreißer: ein Satz, der auch allein stehen kann (Vorschau, Teaser)."""
    if category == PROJECT:
        return (f"Ein Stream, mehrere Kanäle, eine wachsame KI — so arbeitet "
                f"Azrael Sentinel auf {_platforms_text(facts)}.")
    if category == CREATORS:
        lc, total = _int(facts, "live_today_count"), _int(facts, "tracked")
        if lc and total:
            return f"Heute waren {lc} von {total} begleiteten Creatorn live."
        if total:
            return (f"Heute war noch niemand der {total} begleiteten Creator live — "
                    f"der Tag ist aber nicht vorbei.")
        return "Der tägliche Blick auf die Creator, die wir begleiten."
    if category == AI:
        return ("Azrael Sentinel lernt im Betrieb weiter — hier steht, "
                "wie weit die KI inzwischen ist.")
    return ""


def _static_body(category: str, facts: dict) -> str:
    """Deterministische Fallback-Texte aus ECHTEN Fakten (ohne KI). Mehrere
       Absaetze, durch Leerzeile getrennt; die Website rendert je Absatz ein <p>."""
    if category == PROJECT:
        version = str(facts.get("version") or "").strip()
        tracked = _int(facts, "tracked")
        agents = _int(facts, "agents_active")

        a1 = (f"Azrael Sentinel begleitet Live-Streams in Echtzeit. Ein einziges "
              f"Signal geht herein und läuft parallel auf {_platforms_text(facts)} "
              f"wieder hinaus — die Zuschauer bleiben dort, wo sie ohnehin sind, "
              f"statt zwischen Kanälen zu wechseln.")

        a2 = ("Während gesendet wird, liest unsere KI in allen angeschlossenen "
              "Chats gleichzeitig mit: sie antwortet auf Fragen, greift bei Spam "
              "und Beleidigungen ein und meldet, wenn ein Kanal wegbricht. "
              "Sie läuft auf eigener Hardware, nicht bei einem Cloud-Anbieter — "
              "was im Chat steht, verlässt diesen Rechner nicht.")

        # Jeder Satz steht FÜR SICH. Vorher wurden Teilsätze mit Komma
        # aneinandergereiht — fehlte einer, stand da "Zurzeit begleiten wir 3
        # Creator, ." oder ein Absatz begann klein. Das faellt erst im Betrieb
        # auf, weil im Test immer alle Fakten da sind.
        a3_saetze = []
        if tracked:
            a3_saetze.append(f"Zurzeit begleiten wir {tracked} Creator.")
        if agents:
            a3_saetze.append(f"{agents} Wächter-Agenten halten den Betrieb "
                             f"rund um die Uhr im Blick.")
        if version:
            a3_saetze.append(f"Der aktuelle Stand ist Version {version}; "
                             f"was dazukommt, steht künftig hier.")
        return _join([a1, a2, " ".join(a3_saetze)])

    if category == CREATORS:
        total = _int(facts, "tracked")
        live = [u for u in (facts.get("live_today") or []) if u]
        lc = facts.get("live_today_count", len(live))
        try:
            lc = int(lc or 0)
        except (TypeError, ValueError):
            lc = len(live)

        if lc and live:
            shown = ", ".join(live[:12])
            more = " u. a." if lc > len(live[:12]) else ""
            a1 = (f"Tages-Report: Heute waren {lc} von {total} begleiteten "
                  f"Creatorn live{more}: {shown}.")
        elif lc:
            a1 = f"Tages-Report: Heute waren {lc} von {total} begleiteten Creatorn live."
        else:
            a1 = (f"Aktuell begleiten wir {total} Creator. Heute war bislang niemand live "
                  f"— sobald jemand startet, taucht er hier im Tages-Report auf.")

        # Wochenbild: gibt dem Tageswert erst seinen Maßstab. Ohne echte
        # Wochenzahlen bleibt der Absatz weg statt zu raten.
        sess7 = _int(facts, "sessions_7d")
        live7 = _int(facts, "live_7d_count")
        days7 = _int(facts, "active_days_7d")
        w = []
        if sess7 and live7:
            w.append(f"Über die vergangenen sieben Tage waren {live7} verschiedene "
                     f"Creator zusammen {sess7} Mal auf Sendung.")
        elif live7:
            w.append(f"Über die vergangenen sieben Tage waren {live7} verschiedene "
                     f"Creator auf Sendung.")
        if days7:
            w.append(f"An {days7} der sieben Tage war mindestens ein Kanal aktiv.")
        a2 = " ".join(w)

        a3 = ("Wir zählen hier nur, wer live war — keine Zuschauerzahlen, keine "
              "Einnahmen, keine Bewertungen einzelner Personen. Wer nicht mehr "
              "begleitet werden möchte, schreibt uns und verschwindet aus dieser "
              "Liste.")
        return _join([a1, a2, a3])

    if category == AI:
        ft = _int(facts, "kg_facts")
        ag = _int(facts, "agents_active")
        grow = _int(facts, "kg_growth_7d")
        answers = _int(facts, "ai_answers_7d")
        mods = _int(facts, "mod_actions_7d")

        # "Jeder von ihnen" braucht einen Bezug. Ohne die Zahl gab es keinen —
        # der Absatz las sich dann als "Unsere KI …. Jeder von ihnen …".
        if ag:
            a1 = (f"{ag} KI-Wächter behalten den Betrieb rund um die Uhr im Blick. "
                  f"Jeder von ihnen hat genau eine Aufgabe")
        else:
            a1 = ("Unsere KI behält den Betrieb rund um die Uhr im Blick. Mehrere "
                  "Wächter teilen sich die Arbeit, und jeder hat genau eine Aufgabe")
        a1 += (" — Verbindung, Bildqualität, Chat-Ton, Speicherplatz — und meldet "
               "sich nur, wenn diese Aufgabe kippt. Das ist der Unterschied zu "
               "einem Alarm, der bei allem angeht.")

        # Fehlte ft, fing der Absatz mit einem kleingeschriebenen "allein" an.
        if ft and grow:
            a2 = (f"Ihr Wissensspeicher umfasst inzwischen {ft} gelernte Fakten; "
                  f"allein in den vergangenen sieben Tagen kamen {grow} dazu. ")
        elif ft:
            a2 = f"Ihr Wissensspeicher umfasst inzwischen {ft} gelernte Fakten. "
        elif grow:
            a2 = (f"Allein in den vergangenen sieben Tagen kamen {grow} Fakten "
                  f"in ihrem Wissensspeicher dazu. ")
        else:
            a2 = ""
        a2 += ("Gelernt wird aus dem, was im Stream tatsächlich passiert: wiederkehrende "
               "Namen, Themen, Abläufe. Nichts davon wird zugekauft und nichts an "
               "Dritte weitergegeben.")

        a3_teile = []
        if answers:
            a3_teile.append(f"{answers} Antworten in den Chats")
        if mods:
            a3_teile.append(f"{mods} Moderations-Eingriffe")
        a3 = ""
        if a3_teile:
            a3 = ("In der vergangenen Woche wurden daraus " + " und ".join(a3_teile) +
                  ". Jeder Eingriff steht mit Grund im Protokoll — eine KI, die "
                  "stumm löscht, wäre keine Moderation, sondern Willkür.")
        return _join([a1, a2, a3])
    return ""


def _metrics(category: str, facts: dict) -> list:
    """Die harten Zahlen als Kennzahlen-Leiste. Nur belegte Werte — eine
       Kachel mit „0" ist schlechter als keine Kachel."""
    def row(label, value):
        return {"label": label, "value": str(value)}

    out = []
    if category == PROJECT:
        plats = [n for n in ("Kick", "Twitch", "YouTube") if n in (facts.get("platforms") or [])]
        if plats:
            out.append(row("Ziel-Plattformen", len(plats)))
        if _int(facts, "tracked"):
            out.append(row("Begleitete Creator", _int(facts, "tracked")))
        if _int(facts, "restream_targets"):
            out.append(row("Sende-Ziele", _int(facts, "restream_targets")))
        if _int(facts, "agents_active"):
            out.append(row("Wächter-Agenten", _int(facts, "agents_active")))
        if str(facts.get("version") or "").strip():
            out.append(row("Version", str(facts["version"]).strip()))
    elif category == CREATORS:
        if _int(facts, "tracked"):
            out.append(row("Begleitet", _int(facts, "tracked")))
        out.append(row("Heute live", _int(facts, "live_today_count")))
        if _int(facts, "live_7d_count"):
            out.append(row("Live in 7 Tagen", _int(facts, "live_7d_count")))
        if _int(facts, "sessions_7d"):
            out.append(row("Sendungen (7 Tage)", _int(facts, "sessions_7d")))
    elif category == AI:
        if _int(facts, "agents_active"):
            out.append(row("Wächter", _int(facts, "agents_active")))
        if _int(facts, "kg_facts"):
            out.append(row("Gelernte Fakten", _int(facts, "kg_facts")))
        if _int(facts, "kg_growth_7d"):
            out.append(row("Neu (7 Tage)", f"+{_int(facts, 'kg_growth_7d')}"))
        if _int(facts, "ai_answers_7d"):
            out.append(row("Chat-Antworten (7 Tage)", _int(facts, "ai_answers_7d")))
        if _int(facts, "mod_actions_7d"):
            out.append(row("Moderationen (7 Tage)", _int(facts, "mod_actions_7d")))
    return out


def _bullets(category: str, facts: dict) -> list:
    """Die Details, die im Fließtext nur bremsen würden. Bewusst konkret:
       ein Besucher soll danach wissen, was die Plattform tut — nicht, wie
       modern sie klingt."""
    if category == PROJECT:
        plats = _platforms_text(facts)
        b = [
            f"Restream: ein Signal, gleichzeitig auf {plats} — ohne zweiten Rechner",
            "Moderation in allen angeschlossenen Chats aus einer gemeinsamen Heuristik",
            "AZRAEL antwortet im Chat und spricht dabei genau eine Person an, "
            "statt in den Raum zu rufen",
            "Fällt ein Ziel aus, läuft die Sendung auf den übrigen weiter und "
            "das ausgefallene wird gemeldet",
            "Selbst gehostet auf eigener Hardware — kein Chatverlauf bei einem "
            "Cloud-Anbieter",
        ]
        if _int(facts, "restream_targets"):
            b.append(f"{_int(facts, 'restream_targets')} Sende-Ziele sind eingerichtet "
                     f"und einzeln zuschaltbar")
        return b
    if category == CREATORS:
        b = ["Gezählt wird ausschließlich, ob ein Kanal live war — keine "
             "Zuschauerzahlen, keine Einnahmen",
             "Der Tages-Report entsteht automatisch aus der Live-Erkennung, "
             "nicht aus Handarbeit",
             "Wer nicht gelistet werden möchte, wird auf Zuruf entfernt"]
        if _int(facts, "sessions_7d") and _int(facts, "active_days_7d"):
            b.insert(0, f"{_int(facts, 'sessions_7d')} Sendungen an "
                        f"{_int(facts, 'active_days_7d')} von sieben Tagen")
        return b
    if category == AI:
        b = ["Jeder Wächter-Agent hat genau eine Aufgabe und meldet nur, "
             "wenn diese kippt",
             "Der Wissensspeicher wächst aus dem laufenden Betrieb — "
             "nichts zugekauft, nichts weitergegeben",
             "Jeder Moderations-Eingriff steht mit Grund im Protokoll",
             "Die Sprachmodelle laufen lokal; erst wenn die eigene Hardware "
             "nicht reicht, wird ausgewichen"]
        if _int(facts, "kg_facts"):
            b.insert(0, f"{_int(facts, 'kg_facts')} Fakten im Wissensgraph, "
                        f"laufend fortgeschrieben")
        return b
    return []


def _tags(category: str, facts: dict) -> list:
    base = {
        PROJECT: ["Restream", "Moderation", "Selbst gehostet"],
        CREATORS: ["Tages-Report", "Live", "Aggregiert"],
        AI: ["KI", "Wissensgraph", "Wächter"],
    }.get(category, [])
    plats = [n for n in ("Kick", "Twitch", "YouTube") if n in (facts.get("platforms") or [])]
    if category == PROJECT:
        base = base + plats
    return base


def _title(category: str, facts: dict) -> str:
    return {
        PROJECT: "Was Azrael Sentinel kann",
        CREATORS: "Live heute — Tages-Report",
        AI: "Fortschritt der KI",
    }.get(category, CATEGORY_LABEL.get(category, "News"))


def build_items(facts: dict, *, phrasings: dict = None, categories=CATEGORIES,
                now_ts: float = 0.0) -> list:
    """Baut je Kategorie EIN Item aus echten facts. phrasings[cat] = optionaler
       KI-Text (ersetzt nur den Body); ohne → statische Vorlage. Nichts wird erfunden.

       lead/metrics/bullets/tags stammen IMMER aus den Fakten, nie aus der KI —
       damit eine halluzinierte Zahl gar nicht erst in eine Kennzahl geraten kann."""
    phrasings = phrasings or {}
    items = []
    for cat in categories:
        if cat not in CATEGORIES:
            continue
        title = _title(cat, facts)
        body = (phrasings.get(cat) or "").strip() or _static_body(cat, facts)
        if not body:
            continue
        lead = _lead(cat, facts)
        metrics = _metrics(cat, facts)
        bullets = _bullets(cat, facts)
        tags = _tags(cat, facts)
        extra = "|".join([lead] +
                         [f"{m['label']}={m['value']}" for m in metrics] +
                         list(bullets))
        items.append({
            "id": item_id(cat, title, body, extra),
            "ts": now_ts,
            "category": cat,
            "category_label": CATEGORY_LABEL.get(cat, cat),
            "title": title,
            "lead": lead,
            "body": body,
            "metrics": metrics,
            "bullets": bullets,
            "tags": tags,
        })
    return items


def merge(existing: list, new: list, max_items: int) -> list:
    """Neue Items vorn, exakte Duplikate (per id) fallen weg, Historie gedeckelt."""
    seen = set()
    out = []
    for it in list(new) + list(existing or []):
        i = it.get("id")
        if not i or i in seen:
            continue
        seen.add(i)
        out.append(it)
    out.sort(key=lambda x: x.get("ts", 0), reverse=True)
    return out[:max_items]


def render_json(items: list, now_ts: float) -> dict:
    """Die news.json-Struktur, die die Website liest."""
    return {"generated_at": now_ts, "count": len(items), "items": items}
