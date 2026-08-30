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

import asyncio
import os
import time as _time_mod
from dataclasses import dataclass
import hashlib
from datetime import datetime, timedelta, timezone

from nc import creatoragg as _nc_creatoragg
from nc import freeai as _nc_freeai
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set
from nc.dbwrap import db_conn
from nc.envnum import env_int as _env_int

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
    # v4.1-W10 (CodeQL py/weak-sensitive-data-hashing): usedforsecurity=False
    # sagt Bibliothek und Prüfwerkzeug, was hier wirklich passiert — eine
    # Inhalts-Id für den Dedup, kein Schutz. Der WERT bleibt derselbe; ein
    # Wechsel auf sha256 wuerde jede bereits veroeffentlichte Meldung einmalig
    # zur Neu-Meldung machen, weil ihre Id sich aendert.
    h = hashlib.new("sha1", f"{category}|{title}|{body}|{extra}".encode("utf-8"),
                    usedforsecurity=False).hexdigest()
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


# ---------------------------------------------------------------------------
# v4.1-W4: die Bot-Seite der News, aus dem Monolithen geloest.
#
# Bis hierher lag hier nur der bot-freie Textbau (build_items, merge,
# render_json); Faktenerhebung, Config, Zustand, das Schreiben von news.json
# und der KI-Pfad blieben in bot.py — und damit auch die acht /api/news-Routen.
# Erst der Kern, dann die Routen: nc/routes/news.py kostet null nc.ctx-Slots.
#
# Woertlich uebernommen; ersetzt wurden nur die frueheren Modul-Globals.
# ---------------------------------------------------------------------------


class _Conf(dict):
    """Wirft laut statt einen nackten KeyError zu liefern.

    Ein fehlender Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler
    der Route — und er soll den Namen nennen, der fehlt, statt im naechsten
    except-Block zu verschwinden.
    """

    def __missing__(self, key):
        raise RuntimeError(
            "%s ist nicht konfiguriert (%r fehlt) — configure(...) fehlt im "
            "Startpfad von bot.py" % (__name__, key))


_conf = _Conf()


class _LazyLog:
    """Der Logger des Bots, erst beim Zugriff geholt — beim Import ist er None."""

    def __getattr__(self, name):
        return getattr(_conf["log"], name)


log = _LazyLog()


def configure(*, log, bot_file, llm_chat, stats_write, ai_timeout, bot_version,
              kick_channel_url, kick_stream_key, twitch_stream_key,
              youtube_stream_key, yt_ingest_cache):
    """Vom Bot genau einmal beim Start gerufen.

    bot_file ist der Pfad der BOT-Quelle, kein __file__ dieses Moduls:
    output_path() legt news.json in den website/-Ordner NEBEN dem Bot. Mit dem
    __file__ des Fachmoduls waere das nc/website/ geworden — die oeffentliche
    Seite haette ab dem Umzug still eine Datei gelesen, die niemand mehr
    schreibt. Dieselbe Falle wie in W3.

    yt_ingest_cache wandert als REFERENZ: der YouTube-Pfad des Bots schreibt
    den Cache, collect_facts() liest ihn. Eine Kopie waere ab dem Start
    eingefroren.
    """
    _conf.update(log=log, bot_file=bot_file, llm_chat=llm_chat,
                 stats_write=stats_write, ai_timeout=ai_timeout,
                 bot_version=bot_version, kick_channel_url=kick_channel_url,
                 kick_stream_key=kick_stream_key, twitch_stream_key=twitch_stream_key,
                 youtube_stream_key=youtube_stream_key,
                 yt_ingest_cache=yt_ingest_cache)


def enabled() -> bool:
    return bool(_cfg_get("news.enabled",
                         os.getenv("NEWS_ENABLED", "0").strip().lower() in ("1", "true", "yes", "on")))


def output_path() -> str:
    """Zielpfad fuer news.json. Default: der website/-Ordner neben dem Bot.
       Ueber NEWS_OUTPUT_DIR auf den echten nginx-Root umstellbar."""
    d = os.getenv("NEWS_OUTPUT_DIR", "").strip() or \
        os.path.join(os.path.dirname(os.path.abspath(_conf["bot_file"])), "website")
    return os.path.join(d, "news.json")


def config() -> "NewsConfig":
    stored = _cfg_get("news.config", {}) or {}
    cats = stored.get("categories")
    if not cats:
        cats = [c.strip() for c in os.getenv("NEWS_CATEGORIES", "project,creators,ai").split(",") if c.strip()]
    cats = tuple(c for c in cats if c in CATEGORIES) or CATEGORIES

    def _b(v, envname):
        return bool(v) if isinstance(v, bool) else (os.getenv(envname, "0").strip().lower() in ("1", "true", "yes", "on"))
    return NewsConfig(
        enabled=enabled(),
        auto=_b(stored.get("auto"), "NEWS_AUTO"),
        categories=cats,
        cadence_hours=float(stored.get("cadence_hours") or _env_int("NEWS_CADENCE_HOURS", 24)),
        quiet_start=int(stored.get("quiet_start", _env_int("NEWS_QUIET_START", 0))),
        quiet_end=int(stored.get("quiet_end", _env_int("NEWS_QUIET_END", 0))),
        max_items=max(1, int(stored.get("max_items", _env_int("NEWS_MAX_ITEMS", 20)))))


def state() -> "NewsState":
    s = _cfg_get("news.state", {}) or {}
    return NewsState(last_gen_ts=float(s.get("last_gen_ts", 0) or 0),
                              count=int(s.get("count", 0) or 0))


def state_save(ts, count):
    _cfg_set("news.state", {"last_gen_ts": ts, "count": int(count)})


def read_items() -> list:
    import json
    try:
        with open(output_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("items", []) if isinstance(data, dict) else []
    except Exception:
        return []


def write_items(items) -> tuple:
    import json
    path = output_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        payload = render_json(items, _time_mod.time())
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)                 # atomar — kein halb geschriebenes news.json
        return True, path
    except Exception as e:
        return False, str(e)[:200]


def collect_facts() -> dict:
    """Sammelt ECHTE, AGGREGIERTE Fakten (keine Einzelpersonen) fuer die News."""
    facts = {"version": _conf["bot_version"]}
    plats = []
    if _conf["kick_channel_url"] or _conf["kick_stream_key"]:
        plats.append("Kick")
    if _conf["twitch_stream_key"]:
        plats.append("Twitch")
    if _conf["youtube_stream_key"] or _conf["yt_ingest_cache"].get("key"):
        plats.append("YouTube")
    facts["platforms"] = plats
    try:
        with db_conn() as c:
            facts["tracked"] = c.execute("SELECT COUNT(*) AS n FROM trackings").fetchone()["n"]
            # v4.0: Tages-Live-Report. Wer war in den letzten 24 h live? Signal ist
            # der Live-Erkennungs-Log (recording_attempts.started_at) — intern
            # genutzt, in der OEFFENTLICHEN News NIE als "Aufnahme" formuliert,
            # sondern ausschliesslich als "war live".
            _cut = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
            _rows = c.execute(
                "SELECT DISTINCT username FROM recording_attempts "
                "WHERE started_at >= ? AND username IS NOT NULL "
                "ORDER BY username", (_cut,)).fetchall()
            _live = [r["username"] for r in _rows if (r["username"] or "").strip()]
            facts["live_today"] = _live
            facts["live_today_count"] = len(_live)

            # v4.1: Wochenbild. Der Tageswert allein hat keinen Massstab — "2 live"
            # sagt nichts, "2 heute, 11 in sieben Tagen" schon. Aggregiert in
            # Python statt per GROUP BY/DISTINCT-Datumsfunktion: datetime()/DATE()
            # gibt es so nur in SQLite, die Query waere auf MariaDB gestorben.
            _cut7 = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            _r7 = c.execute(
                "SELECT username, started_at FROM recording_attempts "
                "WHERE started_at >= ? AND username IS NOT NULL", (_cut7,)).fetchall()
            _u7, _d7, _s7 = set(), set(), 0
            for _r in _r7:
                _u = (_r["username"] or "").strip()
                if not _u:
                    continue
                _s7 += 1
                _u7.add(_u)
                _d7.add(str(_r["started_at"] or "")[:10])
            facts["live_7d_count"] = len(_u7)
            facts["active_days_7d"] = len({d for d in _d7 if d})
            facts["sessions_7d"] = _s7

            # Eingerichtete Sende-Ziele — oeffentlich unbedenklich (nur die ANZAHL,
            # nie Label, URL oder Key).
            try:
                facts["restream_targets"] = c.execute(
                    "SELECT COUNT(*) AS n FROM restreams WHERE enabled = 1").fetchone()["n"]
            except Exception as _e:
                log.debug("_news_facts restream_targets: %s", _e)

            # Was die Moderation in der Woche tatsaechlich getan hat.
            try:
                facts["mod_actions_7d"] = c.execute(
                    "SELECT COUNT(*) AS n FROM kick_mod_log WHERE ts >= ?",
                    (_cut7,)).fetchone()["n"]
            except Exception as _e:
                log.debug("_news_facts mod_actions_7d: %s", _e)
            try:
                facts["ai_answers_7d"] = c.execute(
                    "SELECT COUNT(*) AS n FROM ai_interactions "
                    "WHERE created_at >= ? AND ok = 1", (_cut7,)).fetchone()["n"]
            except Exception as _e:
                log.debug("_news_facts ai_answers_7d: %s", _e)

            # Wissenszuwachs der Woche = juengster minus aeltester Messpunkt im
            # Fenster. Negative Werte (Speicher wurde geleert) fallen weg statt
            # als "-40 gelernt" auf der Website zu landen.
            try:
                _g = c.execute(
                    "SELECT ts, triples FROM brain_growth WHERE ts >= ? ORDER BY ts",
                    (_cut7,)).fetchall()
                if len(_g) >= 2:
                    _delta = int(_g[-1]["triples"] or 0) - int(_g[0]["triples"] or 0)
                    if _delta > 0:
                        facts["kg_growth_7d"] = _delta
            except Exception as _e:
                log.debug("_news_facts kg_growth_7d: %s", _e)
    except Exception as _e:
        log.debug("_news_facts DB: %s", _e)
    try:
        from brain import get_brain
        b = get_brain()
        if b:
            st = b.knowledge.stats() or {}
            facts["kg_facts"] = int(st.get("triples", 0) or 0)
            try:
                ag = b.agents.status()
                facts["agents_active"] = len(ag.get("agents", ag)) if isinstance(ag, dict) else len(ag)
            except Exception:
                facts["agents_active"] = 0
    except Exception:
        pass
    return facts


async def phrase(cat, facts) -> "str | None":
    """v4.0-W63-Marker: _news_phrase folgt unten (unverändert)."""
    return await phrase_impl(cat, facts)


def creator_activity(days: int = 7) -> list:
    """Aktivität je getracktem User im Fenster (aus recording_attempts), inkl.
       inaktiver User. Aggregation in nc/creatoragg.py."""
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=max(1, days))).isoformat()
        with db_conn() as c:
            rows = c.execute(
                "SELECT username, started_at, outcome FROM recording_attempts "
                "WHERE started_at >= ? AND username IS NOT NULL", (cut,)).fetchall()
            tracked = [r["username"] for r in
                       c.execute("SELECT username FROM trackings").fetchall()
                       if (r["username"] or "").strip()]
        return _nc_creatoragg.summarize(rows, tracked)
    except Exception as e:
        log.debug("_creator_activity: %s", e)
        return []


def creator_facts_line(u: dict) -> str:
    """Kompakte Faktenzeile für Azraels Prompt/Anzeige."""
    if not u["sessions"]:
        return "war im Zeitraum nicht live"
    oc = u.get("outcomes") or {}
    fails = sum(v for k, v in oc.items()
                if k not in ("success", "ok", "running", "?"))
    last = (u.get("last_seen") or "")[:16].replace("T", " ")
    part = f"{u['sessions']}× live an {u['active_days']} Tag(en), zuletzt {last}"
    if fails:
        part += f", {fails} Aufnahme(n) fehlgeschlagen (Zugriff/Region)"
    return part


async def azrael_creator_take(username: str, factline: str) -> str:
    """Azraels (kurze) Einschätzung zu einem Creator. Leerer String, wenn KI aus
       oder nicht erreichbar — dann zeigt das Dashboard nur die Fakten."""
    if os.getenv("NEWS_CREATOR_AI", "1").strip().lower() not in ("1", "true", "yes", "on"):
        return ""
    try:
        msgs = [
            {"role": "system", "content":
             "Du bist Azrael Sentinel, der wachsame KI-Waechter dieses Stream-Setups. "
             "Bewerte einen getrackten Creator in EINEM knappen deutschen Satz (max 30 "
             "Woerter): sachlich, leicht sardonisch, kein Fliesstext-Vorwort, keine "
             "Anrede, keine Emojis."},
            {"role": "user", "content":
             f"Creator @{username}. Aktivitaet: {factline}. Dein Urteil in einem Satz:"},
        ]
        text, _err = await _conf["llm_chat"](msgs, timeout=_conf["ai_timeout"])
        return (text or "").strip().split("\n")[0][:240]
    except Exception:
        return ""


async def creator_dossier_generate(days: int = 7, max_users: int = 30) -> dict:
    """Baut je getracktem User Fakten + Azraels Take und cacht das Ergebnis in
       app_config (news.creators). Auf Abruf oder ueber die News-Kadenz."""
    global _CREATOR_DOSSIER_LOCK
    if _CREATOR_DOSSIER_LOCK is None:
        _CREATOR_DOSSIER_LOCK = asyncio.Lock()
    async with _CREATOR_DOSSIER_LOCK:
        acts = creator_activity(days)[:max(1, max_users)]
        items = []
        for u in acts:
            factline = creator_facts_line(u)
            take = await azrael_creator_take(u["username"], factline)
            items.append({
                "username": u["username"], "sessions": u["sessions"],
                "active_days": u["active_days"], "last_seen": u["last_seen"],
                "outcomes": u["outcomes"], "summary": factline, "azrael": take,
            })
        payload = {"items": items, "generated_ts": datetime.now(timezone.utc).isoformat(),
                   "days": days}
        try:
            _cfg_set("news.creators", payload)
        except Exception as e:
            log.debug("news.creators speichern: %s", e)
        return payload


def absaetze(text) -> str:
    """v4.1: KI-Antwort auf saubere Absaetze normalisieren. Der Website-Renderer
       trennt an "\n\n" — ohne diese Normalisierung liefert ein Modell mal drei
       Leerzeilen, mal einzelne Umbrueche mitten im Satz, und die Seite zeigt
       entweder Luecken oder einen einzigen Klotz."""
    zeilen = [z.strip() for z in (text or "").replace("\r", "").split("\n")]
    absaetze, puffer = [], []
    for z in zeilen:
        if z:
            # Aufzaehlungszeichen fliegen raus: die Details stehen auf der Website
            # in einer eigenen Liste, im Fliesstext waeren sie doppelt.
            puffer.append(z.lstrip("-*\u2022 ").strip())
        elif puffer:
            absaetze.append(" ".join(puffer))
            puffer = []
    if puffer:
        absaetze.append(" ".join(puffer))
    return "\n\n".join(a for a in absaetze if a)


async def phrase_impl(cat, facts) -> "str | None":
    """Optionale KI-Formulierung aus den ECHTEN Fakten (kein Erfinden). self-gated."""
    if os.getenv("NEWS_AI_FLAVOR", "1").strip().lower() not in ("1", "true", "yes", "on"):
        return None
    try:
        base = _static_body(cat, facts)
        label = {"project": "das Projekt",
                 "creators": "einen Tages-Report der heute live gewesenen Creator "
                             "(die Namen aus den Fakten duerfen genannt werden)",
                 "ai": "die KI"}.get(cat, cat)
        # v4.1: ausfuehrlich statt Statuszeile. Die alte Vorgabe "1-2 Saetze" hat
        # aus jeder Meldung eine Zeile gemacht — fuer einen Erstbesucher wertlos
        # und fuer Suchmaschinen zu duenn. Jetzt drei Absaetze; die Absatzgrenzen
        # muessen deshalb erhalten bleiben (frueher: .replace("\n", " ")).
        msgs = [{"role": "system", "content": "Du schreibst oeffentliche Website-News auf Deutsch. "
                 "Schreibe GENAU DREI Absaetze, getrennt durch eine Leerzeile, zusammen 110-180 Woerter: "
                 "(1) was gerade passiert ist, (2) was das konkret bedeutet, (3) eine sachliche Einordnung. "
                 "Sachlich-einladend, ganze Saetze, KEINE Hashtags, KEINE Emojis, KEINE Ueberschriften, "
                 "KEINE Aufzaehlungszeichen, KEINE erfundenen Zahlen. Nutze AUSSCHLIESSLICH die genannten "
                 "Fakten und uebernimm jede Zahl unveraendert. WICHTIG: Erwaehne NIEMALS Aufnahmen, "
                 "Aufzeichnungen, Mitschnitte oder Recording — die Plattform nimmt oeffentlich nichts auf; "
                 "sprich ausschliesslich von Live-Begleitung, Restream und Moderation."},
                {"role": "user", "content": f"Formuliere eine ausfuehrliche oeffentliche News ueber {label} "
                 f"aus diesen Fakten, ohne neue Zahlen zu erfinden: {base}"}]
        out = await asyncio.wait_for(_nc_freeai.chat(msgs, timeout=20), timeout=24)
        out = absaetze(out)
        return out[:1600] or None
    except Exception:
        return None


async def generate(manual: bool = False) -> dict:
    cfg = config()
    if not cfg.categories:
        return {"ok": False, "error": "Keine Kategorien aktiv"}
    facts = await asyncio.to_thread(collect_facts)
    phrasings = {}
    for cat in cfg.categories:
        p = await phrase(cat, facts)
        if p:
            phrasings[cat] = p
    now = _time_mod.time()
    fresh = build_items(facts, phrasings=phrasings, categories=cfg.categories, now_ts=now)
    existing = await asyncio.to_thread(read_items)
    merged = merge(existing, fresh, cfg.max_items)
    ok, info = await asyncio.to_thread(write_items, merged)
    await asyncio.to_thread(_conf["stats_write"])
    if ok:
        st = state()
        state_save(now, st.count + 1)
        log.info("News generiert (%d Items gesamt, %d neu, manual=%s) → %s",
                 len(merged), len(fresh), manual, info)
    return {"ok": ok, "items": len(merged), "new": len(fresh),
            "path": info if ok else None, "error": None if ok else info}
