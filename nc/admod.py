"""nc.admod — v4.0-W56: der Allowlist-Bauer für die Werbe-Moderation.

Aus _ad_allowlist herausgelöst: baut die Menge der EIGENEN Domains/Kanalnamen,
die nicht als Fremdwerbung gewertet werden. Rein — Kanal-URL, Kanalnamen und der
Domain-Regex rein, das Set raus; das Lesen der Env-Variablen bleibt beim Aufrufer.
Bitgenau gegen den Monolithen geprüft.
"""

# eigene Plattform-Domains gelten immer als erlaubt
_OWN_PLATFORMS = ("kick.com", "twitch.tv", "youtube.com", "youtu.be", "tiktok.com")


def build_allowlist(channel_url, channel_names, url_re):
    """Eigene Domains/Kanalnamen, die NICHT als Fremdwerbung gelten.
       channel_url: eigene Kanal-URL (Domain wird via url_re extrahiert);
       channel_names: iterierbare Kanalnamen (#/@ und Whitespace werden entfernt);
       url_re: kompilierter Domain-Regex mit der Domain in Gruppe 1."""
    allow = set()
    v = (channel_url or "").strip().lower()
    m = url_re.search(v)
    if m:
        allow.add(m.group(1))
    for name in channel_names:
        v = (name or "").strip().lstrip("#@").lower()
        if v:
            allow.add(v)
    allow.update(_OWN_PLATFORMS)
    return allow
