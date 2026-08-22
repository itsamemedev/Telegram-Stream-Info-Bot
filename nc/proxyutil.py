"""nc.proxyutil — reine Proxy-URL-Helfer (keine Bot-Abhängigkeiten).

Extrahiert aus bot_v37.py. _normalize_proxy_url ergänzt ein fehlendes Schema,
_proxy_key liefert den kanonischen Router-Key (matcht 'http://ip:port' und
'ip:port' auf denselben Pool-Eintrag). Beide rein string-basiert.
"""

import re
import time as _time_mod



# ProxyHealth-Schwellen (per configure() aus bot_v37.py injiziert).
_PROXY_EVICT_AFTER_FAILS = 4
_PROXY_FAST_MS = 500
_PROXY_MEDIUM_MS = 1500


def configure_proxyhealth(evict_after_fails=None, fast_ms=None, medium_ms=None):
    global _PROXY_EVICT_AFTER_FAILS, _PROXY_FAST_MS, _PROXY_MEDIUM_MS
    if evict_after_fails is not None: _PROXY_EVICT_AFTER_FAILS = int(evict_after_fails)
    if fast_ms is not None: _PROXY_FAST_MS = int(fast_ms)
    if medium_ms is not None: _PROXY_MEDIUM_MS = int(medium_ms)


def _normalize_proxy_url(url: str) -> str:
    """'1.2.3.4:8080' -> 'http://1.2.3.4:8080'. Lässt socks5:// etc. intakt."""
    if "://" in url:
        return url
    return "http://" + url


def _proxy_key(url: str) -> str:
    """Kanonischer Router-Key. Strippt ein führendes 'http://' (HTTP-Proxies
       liegen im Pool ALS 'ip:port' ohne Schema), behält aber socks5://, https://
       etc. (anderes Protokoll = anderer Proxy). So matchen 'http://1.2.3.4:80',
       '1.2.3.4:80' auf denselben Eintrag — verhindert verlorene Test-Resultate."""
    if url.startswith("http://"):
        return url[len("http://"):]
    return url


def _proxy_scheme(url: str) -> str:
    """Erkennt das Schema eines Proxy-Eintrags. Default http."""
    if "://" in url:
        return url.split("://", 1)[0].lower()
    return "http"


def _tunnel_mask(u):
    if not u:
        return None
    try:
        return re.sub(r"://([^@/]+)@", "://***@", str(u))
    except Exception:
        return "***"


class ProxyHealth:
    """Health-State eines einzelnen Proxys. EWMA-Latenz + Erfolgsrate."""
    __slots__ = ("url", "scheme", "source", "ewma_latency", "ok", "fail",
                 "streak_fail", "streak_ok", "last_ok_ts", "last_used_ts",
                 "anonymity", "country", "city", "isp", "evicted")

    def __init__(self, url, scheme="http", source="", latency=None,
                 country="", city="", isp=""):
        self.url = url
        self.scheme = scheme
        self.source = source
        self.ewma_latency = float(latency) if latency else None
        self.ok = 1 if latency else 0
        self.fail = 0
        self.streak_fail = 0
        self.streak_ok = 1 if latency else 0
        self.last_ok_ts = _time_mod.monotonic() if latency else 0
        self.last_used_ts = 0
        self.anonymity = "unknown"
        self.country = country
        self.city = city
        self.isp = isp
        self.evicted = False

    def record(self, ok: bool, latency_ms=None):
        """Ergebnis einer echten Nutzung einspeisen — der Router lernt daraus."""
        if ok:
            self.ok += 1
            self.streak_ok += 1
            self.streak_fail = 0
            self.last_ok_ts = _time_mod.monotonic()
            if latency_ms is not None:
                # EWMA mit alpha=0.3 (neuere Messungen gewichten, aber glätten)
                if self.ewma_latency is None:
                    self.ewma_latency = float(latency_ms)
                else:
                    self.ewma_latency = 0.7 * self.ewma_latency + 0.3 * float(latency_ms)
        else:
            self.fail += 1
            self.streak_fail += 1
            self.streak_ok = 0
            if self.streak_fail >= _PROXY_EVICT_AFTER_FAILS:
                self.evicted = True

    @property
    def total(self):
        return self.ok + self.fail

    @property
    def success_rate(self):
        return (self.ok / self.total) if self.total else 0.0

    @property
    def tier(self):
        if self.ewma_latency is None:
            return "untested"
        if self.ewma_latency < _PROXY_FAST_MS:
            return "fast"
        if self.ewma_latency < _PROXY_MEDIUM_MS:
            return "medium"
        return "slow"

    @property
    def score(self):
        """Composite 0..100. Erfolgsrate dominiert, Latenz moduliert,
           frische Erfolge bonus, fail-streak malus."""
        if self.evicted or self.ewma_latency is None:
            return 0.0
        sr = self.success_rate                      # 0..1
        # Latenz-Faktor: 1.0 bei 0ms → 0.0 bei 3000ms+
        lat_factor = max(0.0, 1.0 - (self.ewma_latency / 3000.0))
        base = (0.65 * sr + 0.35 * lat_factor) * 100.0
        # Anonymität-Bonus (elite/anonymous bevorzugen)
        if self.anonymity == "elite":
            base += 6
        elif self.anonymity == "anonymous":
            base += 3
        elif self.anonymity == "transparent":
            base -= 10   # transparent = leakt echte IP → Sicherheitsrisiko
        # Fail-streak malus
        base -= self.streak_fail * 5
        return max(0.0, min(100.0, base))

    def to_dict(self):
        return {
            "url": self.url, "scheme": self.scheme, "source": self.source,
            "latency_ms": round(self.ewma_latency) if self.ewma_latency is not None else None,
            "success_rate": round(self.success_rate, 3),
            "ok": self.ok, "fail": self.fail,
            "streak_fail": self.streak_fail,
            "score": round(self.score, 1),
            "tier": self.tier,
            "anonymity": self.anonymity,
            "country": self.country, "city": self.city, "isp": self.isp,
            "last_ok_secs_ago": int(_time_mod.monotonic() - self.last_ok_ts) if self.last_ok_ts else None,
            "socks": self.scheme.startswith("socks"),
        }


# ---- Proxy-Auswahl (V37 Welle 3): aus bot_v37.py extrahiert ----------------
# Injection: _TUNNEL (dict-Referenz, mutable), PROXY_LIST (Listen-Referenz),
# RECORD_PROXY (fester String), Router per GETTER (PROXY_ROUTER wird im Bot
# erst spät instanziiert — ein Lambda löst die Reihenfolge-Falle).
import random
import threading

_HAS_SOCKS = False
_PROXY_POOL = []
_PROXY_POOL_LOCK = threading.Lock()
_PROXY_STRATEGY_DEFAULT = "weighted"


def configure_router(has_socks=None, proxy_pool=None, pool_lock=None,
                     strategy_default=None):
    global _HAS_SOCKS, _PROXY_POOL, _PROXY_POOL_LOCK, _PROXY_STRATEGY_DEFAULT
    if has_socks is not None: _HAS_SOCKS = has_socks
    if proxy_pool is not None: _PROXY_POOL = proxy_pool
    if pool_lock is not None: _PROXY_POOL_LOCK = pool_lock
    if strategy_default is not None: _PROXY_STRATEGY_DEFAULT = strategy_default
from typing import Optional

_TUNNEL = {"override": None, "forced_off": False}
_RECORD_PROXY = ""
_PROXY_LIST = []
_ROUTER_GET = lambda: None   # noqa: E731


def configure_proxy_select(tunnel=None, record_proxy=None, proxy_list=None,
                           router_getter=None):
    global _TUNNEL, _RECORD_PROXY, _PROXY_LIST, _ROUTER_GET
    if tunnel is not None: _TUNNEL = tunnel
    if record_proxy is not None: _RECORD_PROXY = record_proxy
    if proxy_list is not None: _PROXY_LIST = proxy_list
    if router_getter is not None: _ROUTER_GET = router_getter


def get_random_proxy() -> Optional[str]:
    # v37: Laufzeit-Tunnel-Steuerung (Polen-VPS). Override hat Vorrang vor allem;
    # forced_off erzwingt Direktverbindung. Default (None/False) = unverändert.
    if _TUNNEL.get("forced_off"):
        return None
    if _TUNNEL.get("override"):
        return _TUNNEL["override"]
    # 403-FIX, Priorität 0: expliziter RECORD_PROXY. Wenn gesetzt, läuft ALLES
    # (Resolve + Pull) über diesen einen Proxy → konsistente Egress-IP, gleiche
    # Region/Reputation wie die Cookie-Herkunft. Das ist der einzige Hebel der
    # Datacenter-403 wirklich behebt (mit einem Residential-/Mobile-Proxy).
    if _RECORD_PROXY:
        return _RECORD_PROXY
    # Priorität 1: manuell konfigurierte statische PROXY_LIST (unverändertes
    # Verhalten für bestehende Setups).
    if _PROXY_LIST:
        return random.choice(_PROXY_LIST)        # C18
    # Priorität 2 (NEU): wenn keine statische Liste da ist, den vom ProxyRouter
    # als "best" bewerteten Proxy aus dem dynamischen Pool nutzen. So beeinflusst
    # das professionelle Routing tatsächlich den echten Traffic — aber NUR wenn
    # der Operator keine eigene Liste gesetzt hat (kein Override expliziter Config).
    try:
        best = (_ROUTER_GET() or _NoRouter()).select()
        if best:
            return _normalize_proxy_url(best)
    except Exception:
        pass
    return None


def _pick_pull_proxy(exclude=None):
    """Wählt einen Proxy für PULL/Resolve: RECORD_PROXY → PROXY_LIST → bester GESUNDER
       aus dem (TikTok-validierten) Pool. exclude=Menge gescheiterter URLs → Rotation
       beim Reconnect statt denselben kaputten Proxy erneut. None = direkt (kein Proxy)."""
    if _TUNNEL.get("forced_off"):
        return None
    if _TUNNEL.get("override"):
        return _TUNNEL["override"]
    if _RECORD_PROXY:
        return _RECORD_PROXY
    ex = exclude or set()
    if _PROXY_LIST:
        pool = [p for p in _PROXY_LIST if p not in ex]
        return random.choice(pool) if pool else random.choice(_PROXY_LIST)
    try:
        best = (_ROUTER_GET() or _NoRouter()).select(exclude=ex)
        if best:
            return _normalize_proxy_url(best)
    except Exception:
        pass
    return None


class _NoRouter:
    def select(self, exclude=None):
        return None


class _ProxyRouter:
    """Thread-safe Router über die Proxy-Healths. Wählt nach Strategie."""
    def __init__(self):
        self._lock = threading.Lock()
        self._healths = {}      # url -> ProxyHealth
        self._rr_idx = 0
        self.strategy = _PROXY_STRATEGY_DEFAULT

    def sync_from_pool(self):
        """Übernimmt neue Proxies aus _PROXY_POOL, behält Health bestehender."""
        with _PROXY_POOL_LOCK:
            pool = list(_PROXY_POOL)
        with self._lock:
            seen = set()
            for p in pool:
                url = p.get("url")
                if not url:
                    continue
                key = _proxy_key(url)
                seen.add(key)
                if key not in self._healths:
                    self._healths[key] = ProxyHealth(
                        url=key, scheme=_proxy_scheme(url),
                        source=p.get("source", ""), latency=p.get("latency_ms"),
                        country=p.get("country", ""), city=p.get("city", ""),
                        isp=p.get("isp", ""))
                    # B68: Anonymität aus dem Pool übernehmen (vom Refresh gesetzt)
                    if p.get("anonymity"):
                        self._healths[key].anonymity = p["anonymity"]
                else:
                    h = self._healths[key]
                    # Geo aus dem Pool nachziehen (kommt vom enrichment)
                    h.country = p.get("country", h.country)
                    h.city = p.get("city", h.city)
                    h.isp = p.get("isp", h.isp)
                    # B68: Anonymität nachziehen — aber ein bekanntes Ergebnis nicht
                    # mit "unknown" überschreiben
                    pa = p.get("anonymity")
                    if pa and pa != "unknown":
                        h.anonymity = pa
            # Evicted + nicht mehr im Pool → entfernen
            for key in list(self._healths):
                if self._healths[key].evicted and key not in seen:
                    del self._healths[key]

    def set_strategy(self, strategy: str) -> bool:
        if strategy not in ("fastest", "round_robin", "weighted"):
            return False
        with self._lock:
            self.strategy = strategy
        return True

    def healthy(self):
        return [h for h in self._healths.values()
                if not h.evicted and h.streak_fail < _PROXY_EVICT_AFTER_FAILS]

    def select(self, strategy=None, exclude=None):
        """Liefert die url des gewählten Proxys (oder None). exclude=Menge von URLs, die
           gerade gescheitert sind → für Rotation beim Reconnect (anderer Proxy)."""
        strat = strategy or self.strategy
        ex = exclude or set()
        with self._lock:
            cands = [h for h in self.healthy() if h.url not in ex]
            if not cands:
                cands = self.healthy()      # alle excluded → lieber denselben als gar keinen
            if not cands:
                return None
            if strat == "fastest":
                # höchster Score (Latenz+Erfolg) zuerst
                best = max(cands, key=lambda h: h.score)
            elif strat == "round_robin":
                cands.sort(key=lambda h: h.url)
                self._rr_idx = (self._rr_idx + 1) % len(cands)
                best = cands[self._rr_idx]
            elif strat == "weighted":
                import random as _r
                weights = [max(0.1, h.score) for h in cands]
                best = _r.choices(cands, weights=weights, k=1)[0]
            else:
                best = cands[0]
            best.last_used_ts = _time_mod.monotonic()
            return best.url

    def report(self, url: str, ok: bool, latency_ms=None):
        with self._lock:
            h = self._healths.get(_proxy_key(url))
            if h:
                h.record(ok, latency_ms)

    def evict(self, url: str):
        """Sofort-Eviction nach klarem Block (403/407/Timeout im echten Pull/Resolve),
           ohne auf die Fail-Streak-Schwelle zu warten — verhindert, dass der nächste
           Versuch wieder denselben kaputten Proxy zieht (Anti-Buffering-Rotation)."""
        with self._lock:
            h = self._healths.get(_proxy_key(url))
            if h:
                h.fail += 1
                h.streak_ok = 0
                h.streak_fail = max(h.streak_fail + 1, _PROXY_EVICT_AFTER_FAILS)
                h.evicted = True

    def set_anonymity(self, url: str, anon: str):
        with self._lock:
            h = self._healths.get(_proxy_key(url))
            if h:
                h.anonymity = anon

    def stats(self):
        with self._lock:
            healths = [h.to_dict() for h in self._healths.values()]
        healths.sort(key=lambda d: d["score"], reverse=True)
        tiers = {"fast": 0, "medium": 0, "slow": 0, "untested": 0}
        anon = {"elite": 0, "anonymous": 0, "transparent": 0, "unknown": 0}
        for h in healths:
            tiers[h["tier"]] = tiers.get(h["tier"], 0) + 1
            anon[h["anonymity"]] = anon.get(h["anonymity"], 0) + 1
        healthy = [h for h in healths if h["score"] > 0 and h["streak_fail"] < _PROXY_EVICT_AFTER_FAILS]
        avg_lat = None
        lats = [h["latency_ms"] for h in healthy if h["latency_ms"] is not None]
        if lats:
            avg_lat = round(sum(lats) / len(lats))
        return {
            "strategy": self.strategy,
            "socks_supported": _HAS_SOCKS,
            "total": len(healths),
            "healthy": len(healthy),
            "avg_latency_ms": avg_lat,
            "tiers": tiers,
            "anonymity": anon,
            "evict_after_fails": _PROXY_EVICT_AFTER_FAILS,
            "proxies": healths,
        }
