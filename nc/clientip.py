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


def ist_lokal(remote, koepfe, vertraut, loopback) -> bool:
    """Kommt die Anfrage wirklich vom Rechner selbst (SSH-Tunnel, curl)?

    koepfe: Mapping der Request-Kopfzeilen (request.headers).
    """
    remote = (remote or "").strip()
    if remote not in loopback:
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
