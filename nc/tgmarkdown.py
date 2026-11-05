"""nc.tgmarkdown — Telegram-HTML in Discord-Markdown übersetzen (rein).

v4.2-W138. Discord führt die Telegram-Befehle über `_run_tg_handler` aus und
übersetzte das HTML bis hierher mit einer Zeile:

    re.sub(r"</?(?:b|i|code|pre|u|s)>", "**", out)

Damit wurde aus JEDEM dieser Tags ein Fettdruck — auch aus `<pre>`. Die
Tabellen in `/tiktok` (Metriken, Zeitleiste) bestehen aus Leerzeichen-
Ausrichtung und brauchen eine Festbreitenschrift; fett und proportional
gesetzt war die Spalte nicht mehr lesbar. `<a href>`, `<blockquote>` und
die HTML-Entitäten (`&amp;`, `&lt;`) blieben gar unübersetzt und standen
wörtlich im Discord-Kanal. „Nicht detailliert genug" war auf Discord
deshalb auch eine Frage der Darstellung, nicht nur des Inhalts.
"""

import html
import re

_A = re.compile(r'<a\s+href="([^"]*)"\s*>(.*?)</a>', re.S | re.I)
_PRE = re.compile(r"<pre>(.*?)</pre>", re.S | re.I)
_CODE = re.compile(r"<code>(.*?)</code>", re.S | re.I)
_QUOTE = re.compile(r"<blockquote(?:\s+expandable)?>(.*?)</blockquote>", re.S | re.I)
_REST = re.compile(r"</?[a-zA-Z][^>]*>")
_EINFACH = (("b", "**"), ("strong", "**"), ("i", "*"), ("em", "*"),
            ("u", "__"), ("s", "~~"))


def html_zu_md(text: str) -> str:
    text = text or ""
    # Festbreite zuerst herausnehmen: darin darf kein anderer Ersatz greifen
    # (ein "*" in einer Tabelle ist ein Zeichen, kein Kursivbeginn).
    bloecke = []

    def _parken(inhalt, zaun):
        bloecke.append(zaun + html.unescape(inhalt) + zaun)
        return f"\x00{len(bloecke) - 1}\x00"

    text = _PRE.sub(lambda m: _parken("\n" + m.group(1).strip("\n") + "\n", "```"), text)
    text = _CODE.sub(lambda m: _parken(m.group(1), "`"), text)
    text = _A.sub(lambda m: f"[{_REST.sub('', m.group(2))}]({m.group(1)})", text)
    text = _QUOTE.sub(
        lambda m: "\n".join("> " + z for z in m.group(1).strip().split("\n")), text)
    for tag, md in _EINFACH:
        text = re.sub(rf"</?{tag}>", md, text, flags=re.I)
    text = _REST.sub("", text)
    text = html.unescape(text)
    return re.sub(r"\x00(\d+)\x00", lambda m: bloecke[int(m.group(1))], text)


def teilen(text: str, grenze: int = 1900) -> list:
    """In Stücke ≤ grenze an Absatzgrenzen schneiden.

    Der alte Schnitt lag starr bei je 1900 Zeichen — mitten in einem
    ```-Block, und Discord setzte den Rest der Nachricht dann als Code.
    Absätze (Leerzeile) sind die natürliche Grenze; die Tabellen aus
    `nc.fmt.pre_table` enthalten keine. Nur ein einzelner Absatz über der
    Grenze wird hart geschnitten.
    """
    stuecke, akt = [], ""
    for absatz in (text or "").split("\n\n"):
        kandidat = absatz if not akt else akt + "\n\n" + absatz
        if len(kandidat) <= grenze:
            akt = kandidat
            continue
        if akt:
            stuecke.append(akt)
        while len(absatz) > grenze:
            stuecke.append(absatz[:grenze])
            absatz = absatz[grenze:]
        akt = absatz
    if akt:
        stuecke.append(akt)
    return stuecke
