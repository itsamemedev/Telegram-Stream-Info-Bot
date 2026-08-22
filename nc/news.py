"""nc.news — B163: oeffentliche Projekt-News fuer die Website (bot-frei).

════════════════════════════════════════════════════════════════════════
WOFUER
════════════════════════════════════════════════════════════════════════
Erzeugt in regelmaessigen Abstaenden kurze, AN DIE OEFFENTLICHKEIT gerichtete
News zu drei Themen: dem Projekt, den getrackten Creatorn (aggregiert) und der
KI. Diese landen als news.json neben der statischen Website und werden dort im
News-Bereich angezeigt. Das ist legitimes Internet-Marketing: frische,
oeffentliche Inhalte, die ueber Suche/Teilen Besucher anziehen — kein Spam-Push.

Bewusst OEFFENTLICH, nicht ans Entwickler-Team: keine Build-Nummern, keine
internen Fehlerbilder, kein „B163 ausgeliefert". Formuliert wird fuer Leser der
Website. Und bewusst AGGREGIERT bei Creatorn (Anzahl, Aktivitaet) statt einzelne
Personen herauszustellen — datensparsam und zugleich das bessere Marketing.

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


def item_id(category: str, title: str, body: str) -> str:
    h = hashlib.sha1(f"{category}|{title}|{body}".encode("utf-8")).hexdigest()
    return h[:12]


def _platforms_text(facts: dict) -> str:
    p = [n for n in ("Kick", "Twitch", "YouTube") if n in (facts.get("platforms") or [])]
    if not p:
        return "mehreren Plattformen"
    if len(p) == 1:
        return p[0]
    return ", ".join(p[:-1]) + " und " + p[-1]


def _static_body(category: str, facts: dict) -> str:
    """Deterministische Fallback-Texte aus ECHTEN Fakten (ohne KI)."""
    if category == PROJECT:
        return (f"Unsere Plattform begleitet Live-Streams in Echtzeit — mit "
                f"Restream auf {_platforms_text(facts)} und KI-gestuetzter "
                f"Moderation rund um die Uhr. Version {facts.get('version', '')}.").strip()
    if category == CREATORS:
        total = facts.get("tracked", 0)
        live = [u for u in (facts.get("live_today") or []) if u]
        lc = facts.get("live_today_count", len(live))
        if lc and live:
            shown = ", ".join(live[:12])
            more = " u.\u202fa." if lc > len(live[:12]) else ""
            return (f"Tages-Report: Heute waren {lc} von {total} begleiteten "
                    f"Creatorn live{more}: {shown}.")
        if lc:
            return f"Tages-Report: Heute waren {lc} von {total} begleiteten Creatorn live."
        return (f"Aktuell begleiten wir {total} Creator. Heute war bislang niemand live "
                f"— sobald jemand startet, taucht er hier im Tages-Report auf.")
    if category == AI:
        ft = facts.get("kg_facts", 0)
        ag = facts.get("agents_active", 0)
        ag_txt = (f"{ag} KI-Waechter behalten den Betrieb rund um die Uhr im Blick. "
                  if ag else "Unsere KI behaelt den Betrieb rund um die Uhr im Blick. ")
        ft_txt = (f"Ihr Wissensspeicher umfasst inzwischen {ft} gelernte Fakten."
                  if ft else "Sie lernt laufend aus dem Streaming-Alltag dazu.")
        return ag_txt + ft_txt
    return ""


def _title(category: str, facts: dict) -> str:
    return {
        PROJECT: "Was Azrael Sentinel kann",
        CREATORS: "Live heute — Tages-Report",
        AI: "Fortschritt der KI",
    }.get(category, CATEGORY_LABEL.get(category, "News"))


def build_items(facts: dict, *, phrasings: dict = None, categories=CATEGORIES,
                now_ts: float = 0.0) -> list:
    """Baut je Kategorie EIN Item aus echten facts. phrasings[cat] = optionaler
       KI-Text (ersetzt nur den Body); ohne → statische Vorlage. Nichts wird erfunden."""
    phrasings = phrasings or {}
    items = []
    for cat in categories:
        if cat not in CATEGORIES:
            continue
        title = _title(cat, facts)
        body = (phrasings.get(cat) or "").strip() or _static_body(cat, facts)
        if not body:
            continue
        items.append({
            "id": item_id(cat, title, body),
            "ts": now_ts,
            "category": cat,
            "category_label": CATEGORY_LABEL.get(cat, cat),
            "title": title,
            "body": body,
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
