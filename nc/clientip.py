"""nc.clientip — v4.2-W149: wer fragt wirklich, und ist das der Rechner selbst?

════════════════════════════════════════════════════════════════════════
DER BEFUND
════════════════════════════════════════════════════════════════════════
`_auth_guard` liess jede Anfrage von `request.remote_addr == 127.0.0.1` ohne
PIN und ohne Token durch — gedacht fuer den SSH-Tunnel. Der Installer richtet
im Zugang "proxy" aber nginx auf demselben Rechner ein, mit
`proxy_pass http://127.0.0.1:8050`. Hinter diesem Proxy kommt **jede** Anfrage
aus dem Internet als 127.0.0.1 an: das ganze Deck — Update-Funktion,
Einstellungen, Neustart, Loeschknoepfe — war ohne Anmeldung offen, genau in
der Betriebsart, die fuer den Zugriff von aussen gebaut ist. Dieselbe Pruefung
nahm jeden Besucher von der Ratenbegrenzung aus.

Unterscheidbar ist der Tunnel vom Proxy an einer Sache: ein Proxy sagt, fuer
wen er fragt (`X-Forwarded-For` und Verwandte), ein Tunnel nicht. Kommt eine
Anfrage von Loopback und traegt einen solchen Kopf, ist sie NICHT lokal — es
sei denn, der Absender steht in TRUSTED_PROXIES und die von ihm genannte
Adresse ist selbst Loopback.

════════════════════════════════════════════════════════════════════════
DER ZWEITE BEFUND: DER LINKE EINTRAG GEHOERT DEM ANGREIFER
════════════════════════════════════════════════════════════════════════
`_client_ip()` nahm von `X-Forwarded-For` den ERSTEN Eintrag. nginx haengt mit
`$proxy_add_x_forwarded_for` die echte Adresse HINTEN an und laesst vorne
stehen, was der Client mitgeschickt hat. Wer "X-Forwarded-For: 1.2.3.4"
sendet, war damit fuer die PIN-Sperre 1.2.3.4 — und mit jeder Anfrage eine
neue Adresse: fuenf Fehlversuche je erfundener IP, also unbegrenzt.

Richtig ist, von RECHTS zu lesen und vertraute Proxys zu ueberspringen: der
erste Eintrag, der nicht von einem vertrauten Proxy stammt, ist der, den der
letzte vertraute Proxy selbst gesehen hat.
"""

# Koepfe, mit denen ein Proxy sagt, fuer wen er fragt. Einer genuegt, um eine
# Anfrage als weitergeleitet zu erkennen.
WEITERLEITUNGS_KOEPFE = ("X-Forwarded-For", "Forwarded", "X-Real-IP",
                         "CF-Connecting-IP", "True-Client-IP")


def _eintraege(xff):
    return [t.strip() for t in (xff or "").split(",") if t.strip()]


def echte_ip(remote, xff, vertraut) -> str:
    """Die Adresse, auf die wir uns verlassen duerfen. -> str ("?" wenn leer)

    remote:   request.remote_addr
    xff:      der X-Forwarded-For-Kopf (oder "")
    vertraut: Menge der vertrauten Proxy-Adressen (TRUSTED_PROXIES)
    """
    remote = (remote or "").strip()
    if remote not in vertraut:
        return remote or "?"
    kette = _eintraege(xff)
    # Von rechts: jeder vertraute Proxy haengt an, wen er gesehen hat.
    for adr in reversed(kette):
        if adr not in vertraut:
            return adr
    # Nur vertraute Stationen in der Kette — dann ist der aeusserste davon der
    # Absender (z. B. ein curl auf dem Rechner selbst durch den Proxy).
    if kette:
        return kette[0]
    return remote or "?"


def ist_https(remote, koepfe, vertraut, tls_direkt=False, schema="") -> bool:
    """Kam die Anfrage beim Browser ueber HTTPS an? (v4.2-W152)

    Die Sitzungs-Cookies trugen `Secure` nur bei DASHBOARD_TLS_CERT — also
    nur, wenn das Deck selbst TLS spricht. Im Zugang "proxy" terminiert nginx
    das TLS, das Deck sieht http, und PIN- wie Token-Cookie gingen ohne
    `Secure` hinaus: ein einziger Aufruf ueber http:// (Lesezeichen, Tippfehler,
    Port 80 der Vorlage) traegt sie im Klartext ueber die Leitung.
    `X-Forwarded-Proto` zaehlt nur von einem vertrauten Proxy — sonst koennte
    ihn jeder setzen (dann allerdings nur zu seinem eigenen Nachteil)."""
    if tls_direkt or (schema or "").lower() == "https":
        return True
    if (remote or "").strip() not in vertraut:
        return False
    proto = (koepfe.get("X-Forwarded-Proto") or "").split(",")[-1].strip().lower()
    return proto == "https"


# v5.2-W190: Namen, unter denen der Tunnel das Deck erreicht. Alles andere im
# Host-Kopf heisst: der Browser glaubt, er spreche mit einer FREMDEN Domain.
_LOKALE_NAMEN = ("localhost", "ip6-localhost", "ip6-loopback")


def _host_name(host) -> str:
    """'localhost:3000' -> 'localhost', '[::1]:3000' -> '::1' (klein, ohne Punkt am Ende)."""
    h = (host or "").strip().lower()
    if h.startswith("["):
        h = h[1:].split("]", 1)[0]
    elif h.count(":") == 1:
        h = h.split(":", 1)[0]
    return h.rstrip(".")


def host_ist_lokal(host, erlaubt=()) -> bool:
    """Nennt der Host-Kopf diesen Rechner (oder einen ausdruecklich erlaubten Namen)?

    v5.2-W190 (SEC, DNS-Rebinding): Der Tunnel-Zugang gilt ohne Token und PIN.
    Eine fremde Seite, die der Betreiber im selben Browser offen hat, kann ihren
    eigenen Namen kurz auf 127.0.0.1 umbiegen (DNS-Rebinding). Der Browser
    haelt das danach fuer DIESELBE Seite — er schickt `Sec-Fetch-Site:
    same-origin`, also greift auch nc/herkunft nicht, und er gibt ihr die
    Antworten zu lesen. Erkennbar ist das allein am Host-Kopf: dort steht der
    Name der fremden Seite, nicht localhost. Ein leerer Kopf (HTTP/1.0, Skripte)
    ist kein Browser und bleibt lokal.
    """
    h = _host_name(host)
    if not h:
        return True
    if h in _LOKALE_NAMEN or h.endswith(".localhost"):
        return True
    if h == "::1" or h.startswith("127."):
        teile = h.split(".")
        return h == "::1" or (len(teile) == 4 and all(t.isdigit() for t in teile))
    return h in {_host_name(e) for e in erlaubt if (e or "").strip()}


def ist_lokal(remote, koepfe, vertraut, loopback, host_erlaubt=None) -> bool:
    """Kommt die Anfrage wirklich vom Rechner selbst (SSH-Tunnel, curl)?

    koepfe: Mapping der Request-Kopfzeilen (request.headers).
    host_erlaubt: zusaetzlich erlaubte Host-Namen (DASHBOARD_HOSTNAMEN). Ist es
      nicht None, muss der Host-Kopf lokal sein (v5.2-W190, DNS-Rebinding).
    """
    remote = (remote or "").strip()
    if remote not in loopback:
        return False
    if host_erlaubt is not None and not host_ist_lokal(koepfe.get("Host") or "", host_erlaubt):
        return False
    weitergeleitet = any((koepfe.get(k) or "").strip() for k in WEITERLEITUNGS_KOEPFE)
    if not weitergeleitet:
        return True
    # Ein Proxy auf diesem Rechner hat weitergeleitet. Lokal ist das nur, wenn
    # wir ihm vertrauen UND er selbst sagt, die Anfrage kam von hier.
    # Ohne X-Forwarded-For (nur X-Real-IP o. ae.) gibt es keine Kette, die
    # sich von rechts lesen liesse — dann wird nicht geraten.
    if remote not in vertraut or not (koepfe.get("X-Forwarded-For") or "").strip():
        return False
    return echte_ip(remote, koepfe.get("X-Forwarded-For") or "", vertraut) in loopback
