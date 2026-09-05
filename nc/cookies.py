"""nc.cookies — Cookie-Format-Verarbeitung (keine Bot-Abhängigkeiten).

Extrahiert aus bot.py: beliebige Cookie-Eingaben (Header-String, JSON-
Export, Netscape) → Netscape-Format, Dedupe, Alarm-Stufen-Bewertung."""

import json
import re
import threading

# v4.2-W10: Dieselbe Erkennung, die http.cookiejar benutzt. Wer hier einen
# eigenen Test schreibt ("beginnt mit '# Netscape'"), baut sich eine zweite
# Wahrheit — und genau die hat die Reparatur vorher scheitern lassen: eine
# Datei mit Leerzeile VOR dem Kopf galt als "hat Kopf", MozillaCookieJar
# liest den Kopf aber ausschliesslich in der ERSTEN Zeile.
_NETSCAPE_KOPF_RE = re.compile(r"#( Netscape)? HTTP Cookie File")
_KOPF = "# Netscape HTTP Cookie File"

# Der Schreib-Lock der cookies.txt. Liegt hier und nicht in bot.py, weil
# inzwischen drei Wege schreiben (Auto-Refresh, Dashboard-Update, Auto-Bezug)
# und zwei davon bot-frei sind. Zwei Locks waeren keiner.
DATEI_SPERRE = threading.Lock()


def _ganzzahl(x) -> int:
    """Ablaufzeit als int. MozillaCookieJar ruft int(float(feld)) — ein
       'Session', ein leeres Feld oder ein Datumstext toetet dort das GANZE
       Laden mit LoadError, nicht nur die eine Zeile. 0 = Sitzungs-Cookie."""
    try:
        n = int(float(str(x).strip()))
    except (TypeError, ValueError):
        return 0
    return n if n > 0 else 0


def _sauber(x) -> str:
    """Tabs und Zeilenumbrueche raus — im Netscape-Format sind sie Feld- bzw.
       Satztrenner, in Name und Wert also schlicht illegal."""
    return (str(x).replace("\t", "").replace("\r", "").replace("\n", ""))


def _feld_zeile(felder) -> str:
    """Baut aus rohen Feldern EINE Zeile, die MozillaCookieJar wirklich liest.
       '' wenn nichts Brauchbares drin steht.

       Warum jedes Feld angefasst wird statt nur gezaehlt: der Parser in
       http.cookiejar ist streng und stirbt an der ganzen Datei, sobald eine
       Zeile nicht passt (LoadError → get_cookie_health meldet 'parse_error',
       yt-dlp bricht mit rc=1 ab, _load_cookies_dict liefert leer → TikTok 403).
       Drei Faelle sind uns real begegnet:

         1. Feld 2 passt nicht zur Domain. cookiejar prueft
            `assert domain_specified == initial_dot` — '.tiktok.com' mit FALSE
            (oder 'www.tiktok.com' mit TRUE) ist ein harter Abbruch. Wir
            LEITEN das Feld aus der Domain ab, statt es zu glauben.
         2. Mehr als 7 Felder. cookiejar entpackt in genau sieben Namen →
            ValueError. Ein zusaetzlicher Tab im Wert reicht.
         3. Weniger als 7 Felder. Ein leerer Wert plus ein Editor, der
            Zeilenenden trimmt, ergibt sechs — der Cookie fiel vorher still
            unter den Tisch."""
    if len(felder) < 6:
        return ""
    domain = felder[0].strip()
    if not domain or domain.startswith("#"):
        return ""
    path = felder[2].strip() or "/"
    secure = "TRUE" if felder[3].strip().upper() in ("TRUE", "1", "YES") else "FALSE"
    expiry = _ganzzahl(felder[4])
    name = _sauber(felder[5]).strip()
    # Alles ab Feld 7 gehoert zum Wert. Tabs darin sind der Grund, warum
    # cookiejar die Datei sonst gar nicht laedt — also fallen sie weg.
    wert = _sauber("".join(felder[6:])) if len(felder) > 6 else ""
    if not name and not wert:
        return ""
    # Feld 2 aus der Domain ABGELEITET, nicht uebernommen (Fall 1 oben).
    sub = "TRUE" if domain.startswith(".") else "FALSE"
    return "\t".join([domain, sub, path, secure, str(expiry), name, wert])


def _cookies_input_to_netscape(raw: str):
    """B63: Konvertiert beliebigen Cookie-Input nach Netscape-Format (das was
       MozillaCookieJar / yt-dlp lesen). Akzeptiert zwei Formate:

         1) Netscape-Text  — wie ihn die Extension 'Get cookies.txt LOCALLY'
            exportiert (tab-getrennt, '# Netscape HTTP Cookie File'-Header).
         2) JSON-Array     — wie ihn 'Cookie-Editor' / 'EditThisCookie' liefert:
            [{"name","value","domain","path","secure","expirationDate"}, ...]

       Returns (netscape_text, anzahl_cookies). Wirft bei kaputtem JSON.

       Die Ausgabe ist NORMALISIERT, nicht durchgereicht: jede Datenzeile hat
       exakt sieben Felder, Feld 2 passt zur Domain, die Ablaufzeit ist eine
       Zahl, und der Kopf steht in Zeile 1. Alles andere hat MozillaCookieJar
       schon abgelehnt — siehe _feld_zeile().

       Wichtig:
         - HttpOnly-Cookies: manche Tools schreiben '#HttpOnly_<domain>' an den
           Zeilenanfang. MozillaCookieJar würde die als Kommentar werfen → die
           kritischen Auth-Cookies (sessionid_ss) gingen verloren. Wir strippen
           den Marker, damit sie geparst werden.
         - Tabs-zu-Spaces: Copy-Paste macht aus Tabs oft Spaces. Wir reparieren
           solche Zeilen, damit MozillaCookieJar sie wieder versteht.
         - BOM: Editoren unter Windows schreiben ein U+FEFF vor den Kopf.
           Das verschiebt die Formaterkennung um ein Zeichen.
    """
    roh = (raw or "").lstrip("\ufeff")
    s = roh.lstrip().lstrip("\ufeff")
    if not s:
        return _KOPF + "\n", 0

    # ── Format 1: JSON (Cookie-Editor / EditThisCookie) ──────────────────────
    if s[:1] in ("[", "{"):
        data = json.loads(s)
        if isinstance(data, dict):
            # manche Tools wrappen: {"cookies":[...]} oder {"data":[...]}
            data = data.get("cookies") or data.get("data") or []
        if not isinstance(data, list):
            return _KOPF + "\n", 0
        out = [_KOPF, "# Aktualisiert via TikTokBot-Dashboard", ""]
        count = 0
        for c in data:
            if not isinstance(c, dict):
                continue
            name = c.get("name")
            if not name:
                continue
            exp = (c.get("expirationDate") or c.get("expires")
                   or c.get("expiry") or 0)
            zeile = _feld_zeile([
                str(c.get("domain") or ".tiktok.com"),
                "",                                    # wird abgeleitet
                str(c.get("path") or "/"),
                "TRUE" if c.get("secure") else "FALSE",
                exp,
                name,
                "" if c.get("value") is None else c.get("value"),
            ])
            if zeile:
                out.append(zeile)
                count += 1
        return "\n".join(out) + "\n", count

    # ── Format 2: Netscape-Text ──────────────────────────────────────────────
    lines = roh.splitlines()
    out = []
    # Der Kopf muss in ZEILE 1 stehen — cookiejar liest genau eine Zeile weit.
    if not (lines and _NETSCAPE_KOPF_RE.search(lines[0])):
        out.append(_KOPF)
    count = 0
    for l in lines:
        ls = l.strip()
        # HttpOnly-Marker entfernen, damit der Cookie nicht als Kommentar verschwindet
        if ls.startswith("#HttpOnly_"):
            ls = ls[len("#HttpOnly_"):]
        if not ls:
            out.append("")
            continue
        if ls.startswith(("#", "$")):
            out.append(ls)
            continue
        felder = ls.split("\t")
        if len(felder) < 6:
            # evtl. mit Spaces statt Tabs (Copy-Paste-Schaden)? reparieren.
            # Ab Feld 7 wieder mit Space zusammensetzen — der Wert selbst darf
            # welche enthalten, die sechs Kopffelder nie.
            teile = ls.split()
            if len(teile) < 6:
                continue                     # Muell-Zeile ueberspringen
            felder = teile[:6] + ([" ".join(teile[6:])] if len(teile) > 6 else [])
        zeile = _feld_zeile(felder)
        if zeile:
            out.append(zeile)
            count += 1
    return "\n".join(out) + "\n", count

def _dedupe_cookie_text(netscape_text: str):
    """Entfernt doppelte Cookie-NAMEN (z.B. msToken unter .tiktok.com UND
       www.tiktok.com) und behält pro Name nur die beste Variante — exakt nach
       derselben Regel wie _load_cookies_dict(): spezifischere Domain (ohne
       führenden Punkt) gewinnt, bei Gleichstand die längere Expiry. So
       verschwindet die 'mehrfach unter verschiedenen Domains'-Warnung und der
       Bot sendet garantiert den Wert, den auch die Health-Anzeige sieht.
       Werte werden NICHT verändert — nur die unterlegene Zeile entfällt.
       Returns (bereinigter_text, anzahl_entfernt)."""
    lines = netscape_text.splitlines()
    best = {}                  # name -> (spec, expiry, idx)
    is_data = set()
    for i, l in enumerate(lines):
        ls = l.strip()
        if not ls or ls.startswith("#"):
            continue
        parts = ls.split("\t")
        if len(parts) < 7:
            continue
        is_data.add(i)
        domain, name = parts[0], parts[5]
        try: expiry = int(parts[4])
        except (ValueError, IndexError): expiry = 0
        spec = 0 if domain.startswith(".") else 1
        prev = best.get(name)
        if prev is None or (spec, expiry) > (prev[0], prev[1]):
            best[name] = (spec, expiry, i)
    keep = {v[2] for v in best.values()}
    out, removed = [], 0
    for i, l in enumerate(lines):
        if i in is_data and i not in keep:
            removed += 1
            continue
        out.append(l)
    return "\n".join(out) + "\n", removed

def _cookie_alarm_level(h):
    """get_cookie_health() → (level, telegram_html). level: ok|warn|crit.
       Nutzt das bereits berechnete status/headline aus get_cookie_health()."""
    status = h.get("status")
    head = h.get("headline") or "Cookie-Problem"
    if status in ("missing", "parse_error", "critical"):
        return "crit", ("🚨 <b>COOKIE-ALARM</b>\n\n" + head +
                        "\n\nOhne gültige Auth-Cookies scheitern Aufnahmen (TikTok 403). "
                        "Bitte <code>cookies.txt</code> neu exportieren.")
    if status == "warning":
        od = h.get("oldest_expiry_days")
        extra = (f"\nKritischer Cookie noch ~{od}d gültig." if (od is not None and od >= 0) else "")
        return "warn", ("⚠️ <b>COOKIE-WARNUNG</b>\n\n" + head + extra +
                        "\n\nVor Ablauf neu exportieren — sonst brechen Aufnahmen still ab.")
    return "ok", ""


# ─────────────────────────────────────────────────────────────────────────────
# v4.1-W32: cookies.txt lesen — aus bot.py hierher.
#
# Warum es hierher gehoert: die Funktion parst eine Datei und loest eine
# Namenskollision auf. Beides ist Cookie-Format-Verarbeitung, also genau das,
# wofuer dieses Modul da ist. Im Monolithen hing sie nur an der Konstanten
# COOKIE_FILE und am Logger fest.
#
# Der Rumpf ist woertlich uebernommen — die Aufloesung nach Domain-Spezifitaet
# und Expiry ist ein Bugfix, dessen Symptom ("Dashboard zeigt Cookies aktuell,
# TikTok liefert trotzdem 403") niemand ein zweites Mal suchen will.
import os
import time as _time
from http.cookiejar import LoadError, MozillaCookieJar

_KONF = {"datei": "tiktok_cookies.txt", "log": None}


def configure(datei=None, log=None, kritisch=None, reparieren=None,
              autorefresh_info=None, autofetch_info=None):
    """Vom Bot einmal beim Start gerufen.

    Die vier Zusaetze aus v4.2-W21 gehoeren zu gesundheit(): die Liste der
    kritischen Cookie-Namen, der Reparaturweg (schreibt die Datei neu, liegt
    bot-seitig weil er den Schreib-Lock und das Backup fuehrt) und die beiden
    Auskuenfte ueber Auto-Refresh und Auto-Bezug fuers Deck.
    """
    global _KRITISCH
    if datei is not None:
        _KONF["datei"] = datei
    if log is not None:
        _KONF["log"] = log
    if kritisch is not None:
        _KRITISCH = tuple(kritisch)
    for k, v in (("reparieren", reparieren),
                 ("autorefresh_info", autorefresh_info),
                 ("autofetch_info", autofetch_info)):
        if v is not None:
            _KONF[k] = v


def _warnen(text: str):
    """Gedrosselte Warnung (max. alle 60s).

    BUG-FIX (Tiefenbughunt): bei Permission-denied/Lesefehler landet JEDER der
    21 Aufrufer hier und loggt erneut — im Live-Log sahen wir mehrere Warnungen
    pro Sekunde. Der Erfolgs-Cache greift nicht (wird nur bei Erfolg gesetzt).
    Der Fehler selbst wird NICHT verschluckt — nur die Wiederholung entschaerft."""
    log = _KONF["log"]
    if log is None:
        return
    _now = _time.monotonic()
    if _now - _COOKIE_WARN_TS.get("last", -1e9) >= 60:
        _COOKIE_WARN_TS["last"] = _now
        log.warning(text)
    else:
        log.debug(text + " (gedrosselt)")


def lade_jar(datei=None):
    """v4.2-W10: cookies.txt als MozillaCookieJar — auch wenn die Datei KEIN
       sauberes Netscape-Format ist. Returns (jar, normalisiert).

       Warum es das braucht: cookiejar.load() ist alles-oder-nichts. Eine
       einzige Zeile mit falschem Domain-Flag, einem Extra-Tab oder einer
       Ablaufzeit 'Session' liess bisher JEDEN Leser leer ausgehen — der
       Recorder fuhr ohne Cookies los (TikTok 403), und das Deck meldete
       'parse_error', obwohl 40 gueltige Cookies in der Datei standen.
       Hier wird deshalb im Fehlerfall die normalisierte Fassung gelesen.

       Diese Funktion SCHREIBT NICHT zurueck. Das Reparieren der Datei bleibt
       bei _ensure_cookie_file_netscape() im Bot — ein Leser, der nebenbei
       Dateien umschreibt, ist genau die Sorte Nebenwirkung, die man um drei
       Uhr nachts nicht sucht."""
    pfad = datei or _KONF["datei"]
    cj = MozillaCookieJar(pfad)
    try:
        cj.load(ignore_discard=True, ignore_expires=True)
        return cj, False
    except LoadError as e:
        # ACHTUNG: LoadError ERBT VON OSError. Ein "except OSError: raise" davor
        # faengt genau den Formatfehler weg, um den es hier geht — die
        # Normalisierung liefe dann nie. Deshalb steht dieser Zweig zuerst.
        urspruenglich = e
    except OSError:
        raise                       # fehlt/keine Rechte — nichts zu normalisieren
    except Exception as e:
        # Festhalten: Python raeumt den Namen am Ende des except-Blocks weg,
        # und weiter unten ist genau DIESE Meldung die aussagekraeftige.
        urspruenglich = e

    try:
        with open(pfad, "r", encoding="utf-8", errors="replace") as f:
            text, anzahl = _cookies_input_to_netscape(f.read())
        if anzahl <= 0:
            raise urspruenglich
        # Ueber eine Temp-Datei NEBEN dem Original, nicht im System-Temp:
        # das hier sind Zugangsdaten, und /tmp ist welt-lesbar. 0600, und
        # weg ist sie wieder, bevor die Funktion zurueckkehrt.
        tmp = pfad + ".lesen.tmp"
        fd = os.open(tmp, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
            cj2 = MozillaCookieJar(tmp)
            cj2.load(ignore_discard=True, ignore_expires=True)
        finally:
            try:
                os.remove(tmp)
            except OSError:
                pass
        cj2.filename = pfad         # sonst zeigt ein spaeteres save() ins Nirwana
        return cj2, True
    except LoadError:
        raise urspruenglich from None   # auch normalisiert unlesbar
    except OSError:
        raise
    except Exception:
        raise urspruenglich from None


def load_dict() -> dict:
    """Lädt cookies.txt als dict. B6-Fix: TTL-Cache (5s) damit Recording-
       Bursts nicht für jeden Resolve+ffmpeg-Bau die Datei neu parsen.
       Cache wird invalidiert wenn sich die mtime ändert.

       BUG-FIX (Tiefenbughunt): Browser-Cookie-Exports (z.B. "Get cookies.txt
       LOCALLY") legen denselben Cookie-NAMEN oft mehrfach mit verschiedenen
       DOMAIN-Scopes an — TikTok setzt sessionid teils auf '.tiktok.com',
       teils zusätzlich auf 'www.tiktok.com' je nachdem welche Subdomain
       zuletzt besucht wurde. Die alte Implementierung baute das Ergebnis-
       dict per {c.name: c.value for c in cj} — bei Namens-Kollision über
       mehrere Domains gewinnt schlicht der in MozillaCookieJar zuletzt
       iterierte Eintrag. Das ist NICHT deterministisch nach Aktualität,
       sondern nach Datei-Reihenfolge. Symptom exakt wie beobachtet: das
       Dashboard zeigt 'Cookies aktuell' (get_cookie_health() prüft nur ob
       der NAME vorkommt, nicht welcher Domain-Wert gewinnt), aber TikTok
       liefert trotzdem 403 weil der tatsächlich gesendete sessionid-Wert
       aus einer veralteten/falschen Domain-Variante stammt.

       Fix: bei Namens-Kollision gewinnt der Eintrag mit der SPEZIFISCHEREN
       Domain (ohne führenden Punkt = Domain-exakt, nicht Subdomain-Wildcard)
       UND falls beide gleich spezifisch sind, der mit der LÄNGEREN Expiry
       (= zuletzt vom Server gesetzt/erneuert, meist der frischere Login)."""
    if not os.path.exists(_KONF["datei"]):
        # Nicht cachen damit wir's mitbekommen wenn die Datei plötzlich da ist
        return {}
    try:
        mtime = os.path.getmtime(_KONF["datei"])
    except OSError:
        return {}
    now = _time.monotonic()
    cached = _COOKIES_CACHE.get("v")
    if cached and cached[0] == mtime and (now - cached[1]) < 5.0:
        return cached[2]
    try:
        cj, normalisiert = lade_jar(_KONF["datei"])
        if normalisiert:
            _warnen("cookies.txt ist kein sauberes Netscape-Format — beim Lesen "
                    "normalisiert. Einmal ueber das Deck neu einspielen oder "
                    "automatisch holen lassen, sonst bleibt es Gluecksache.")
        # best[name] = (specificity_rank, expiry, value)
        # specificity_rank: 1 = exakte Domain (kein führender Punkt, höchste
        # Priorität — das ist was ein echter Browser für die aktuell besuchte
        # Seite tatsächlich sendet), 0 = Wildcard-Domain ('.tiktok.com')
        best: dict = {}
        skipped_collisions = 0
        for c in cj:
            specificity = 0 if (c.domain or "").startswith(".") else 1
            expiry = c.expires or 0
            prev = best.get(c.name)
            if prev is None:
                best[c.name] = (specificity, expiry, c.value, c.domain)
            else:
                skipped_collisions += 1
                if (specificity, expiry) > (prev[0], prev[1]):
                    best[c.name] = (specificity, expiry, c.value, c.domain)
        d = {name: val for name, (_, _, val, _) in best.items()}
        if skipped_collisions:
            _KONF["log"].debug(f"load_dict: {skipped_collisions} Domain-Duplikate "
                      f"aufgelöst (spezifischste/frischeste Variante gewählt)")
        _COOKIES_CACHE["v"] = (mtime, now, d)
        return d
    except Exception as e:
        # BUG-FIX (Tiefenbughunt): bei Permission-denied/Lesefehler landet JEDER
        # der 21 Aufrufer hier und loggt erneut — im Live-Log sahen wir mehrere
        # Warnungen pro Sekunde. Der Erfolgs-Cache greift nicht (wird nur bei
        # Erfolg gesetzt). Darum die Warnung hier drosseln: max. alle 60s, sonst
        # verstopft ein einziges Rechteproblem das komplette Log und versteckt
        # echte Fehler. Der Fehler selbst wird NICHT verschluckt — nur die
        # Wiederholung entschärft.
        _warnen(f"Cookies konnten nicht geladen werden: {e}")
        return {}


_COOKIES_CACHE = {}     # B6: {"v": (mtime, loaded_at_monotonic, dict)}
_COOKIE_WARN_TS = {}    # Tiefenbughunt: drosselt die "Cookies unlesbar"-Warnung (max alle 60s)

# Geteilter Zustand, kein Implementierungsdetail: der Bot leert den Cache nach
# einer Cookie-Reparatur, und das Deck liest ihn ueber ctx.cfg. Beide muessen
# DASSELBE Dict sehen — deshalb ein oeffentlicher Name statt einer Kopie.
CACHE = _COOKIES_CACHE


# ══════════════════════════════════════════════════════════════════════════
# v4.2-W21: die Gesundheitsbewertung der cookies.txt, aus bot.py heraus.
#
# Sie stand dort als 147-Zeilen-Funktion mitten im Monolithen und war NIE
# ausgefuehrt worden — obwohl sie die Leiter ist, an der der Betreiber
# ablesen soll, warum ein Pull 403 bekommt. Genau in dieser Leiter steckt
# die Diagnose fuer "403 trotz aktuellem Cookie laut Dashboard": ein
# kritischer Cookie, der unter MEHREREN Domains in der Datei steht. Der
# Browser waehlt je Subdomain situativ, der Bot statisch — er kann den
# falschen erwischen.
#
# Sie gehoert hierher und nicht in ein eigenes Modul: lade_jar() liest die
# Datei, _cookie_alarm_level() liest das Ergebnis. Drei Teile einer Frage.
# ══════════════════════════════════════════════════════════════════════════

# Cookies, ohne die TikTok den Pull ablehnt. Der Bot reicht die Liste herein,
# damit sie an EINER Stelle in .env/bot.py steht.
_KRITISCH: tuple = ()

# Merkt sich, fuer welchen Dateistand die Reparatur schon versucht wurde.
# Der Versuch haengt an der mtime, NICHT am Aufruf: das Deck pollt diese
# Funktion im Sekundentakt. Scheitert das Schreiben (Datei nur lesbar, volle
# Platte), stuende sonst jede Sekunde ein log.error im Journal — und der eine
# echte Grund ginge darin unter.
_COOKIE_REPAIR_STAND: dict = {"mtime": None}


def gesundheit() -> dict:
    """Liefert Dashboard-Widget-Daten. Defensive — gibt immer was zurück,
       auch wenn Datei fehlt."""
    if not os.path.exists(_KONF["datei"]):
        return {
            "exists": False,
            "status": "missing",
            "headline": "cookies.txt fehlt",
            "file_mtime": None, "file_age_days": None,
            "total": 0, "expiring_soon": [], "expired": [],
            "critical_present": [], "critical_missing": list(_KRITISCH),
            "oldest_expiry_days": None,
            "duplicate_domain_cookies": [],
        }
    try:
        st = os.stat(_KONF["datei"])
        mtime = st.st_mtime
        age_days = (_time.time() - mtime) / 86400
    except OSError:
        mtime = None; age_days = None

    # v4.2-W10: NICHT mehr direkt MozillaCookieJar.load(). Der Parser ist
    # alles-oder-nichts — ein falsches Domain-Flag, ein Extra-Tab oder eine
    # Ablaufzeit "Session" reichte, und das Deck meldete "parse_error", obwohl
    # 40 gueltige Cookies in der Datei standen. lade_jar() liest solche Dateien
    # normalisiert; ist das noetig, wird die Datei EINMAL wirklich repariert
    # (mit Backup), damit auch yt-dlp sie wieder frisst.
    krumm = repariert = False
    try:
        cj, normalisiert = lade_jar(_KONF["datei"])
        all_cookies = list(cj)
        if normalisiert:
            krumm = True
            # Der Versuch haengt an der mtime, nicht am Aufruf: das Deck pollt
            # diese Funktion im Sekundentakt. Scheitert das Schreiben (Datei
            # nur lesbar, volle Platte), stuende sonst jede Sekunde ein
            # log.error im Journal — und der eine echte Grund ginge darin
            # unter. Aendert sich die Datei, wird es neu versucht.
            if _COOKIE_REPAIR_STAND.get("mtime") != mtime:
                _COOKIE_REPAIR_STAND["mtime"] = mtime
                repariert = _KONF["reparieren"]()
    except Exception as e:
        return {
            "exists": True, "status": "parse_error",
            "headline": f"cookies.txt unleserlich: {e}",
            "file_mtime": mtime, "file_age_days": age_days,
            "total": 0, "expiring_soon": [], "expired": [],
            "critical_present": [], "critical_missing": list(_KRITISCH),
            "oldest_expiry_days": None,
            "duplicate_domain_cookies": [],
            "repaired": False,
        }

    now = _time.time()
    expiring_soon = []   # < 7 Tage
    expired = []
    present_names = set()
    oldest_expiry_days = None
    # BUG-FIX: trackt pro Cookie-Name ALLE Domain-Varianten. Wenn ein
    # kritischer Cookie (sessionid etc.) unter mehreren Domains gleichzeitig
    # existiert, sendet _load_cookies_dict() nur EINEN davon — der Browser
    # selbst entscheidet je Subdomain situativ, der Bot aber statisch. Das
    # ist die Hauptursache für "403 trotz aktuellem Cookie laut Dashboard".
    name_domains: dict = {}

    for c in all_cookies:
        present_names.add(c.name)
        name_domains.setdefault(c.name, set()).add(c.domain or "?")
        exp = c.expires
        if not exp or exp <= 0:
            # session cookie ohne Expiry — überleben den Browser-Close eh nicht,
            # aber für unsere Zwecke ist das "ewig gültig"
            continue
        days_left = (exp - now) / 86400
        if days_left < 0:
            expired.append({"name": c.name, "days_ago": round(-days_left, 1)})
        elif days_left < 7:
            expiring_soon.append({"name": c.name, "days_left": round(days_left, 1)})
        # Track oldest (nur kritische zählen — Bot-Cookies wie analytics sind egal)
        if c.name in _KRITISCH:
            if oldest_expiry_days is None or days_left < oldest_expiry_days:
                oldest_expiry_days = round(days_left, 1)

    critical_present = [n for n in _KRITISCH if n in present_names]
    critical_missing = [n for n in _KRITISCH if n not in present_names]
    # BUG-FIX: kritische Cookies mit >1 Domain-Variante in der Datei —
    # potenzielle Quelle für falsch aufgelöste/veraltete Werte beim Senden.
    duplicate_domain_cookies = sorted(
        n for n in _KRITISCH
        if len(name_domains.get(n, set())) > 1
    )

    # Status-Bewertung — drei Stufen
    if not critical_present:
        status = "critical"
        headline = "Keine kritischen Auth-Cookies vorhanden"
    elif "sessionid_ss" not in present_names and "sessionid" not in present_names:
        status = "critical"
        headline = "Auth-Cookie sessionid(_ss) fehlt"
    elif expired:
        status = "warning"
        headline = f"{len(expired)} Cookie(s) abgelaufen"
    elif duplicate_domain_cookies:
        # BUG-FIX: das ist die neue, sichtbare Warnung für genau das Problem
        # das du gemeldet hast — "403 trotz aktuellem Cookie".
        status = "warning"
        headline = (f"{', '.join(duplicate_domain_cookies)} mehrfach unter "
                    f"verschiedenen Domains vorhanden — Bot kann den falschen "
                    f"Wert wählen. cookies.txt bereinigen (alte Einträge löschen, "
                    f"frisch exportieren).")
    elif oldest_expiry_days is not None and oldest_expiry_days < 3:
        status = "warning"
        headline = f"Kritischer Cookie läuft in {oldest_expiry_days}d ab"
    elif oldest_expiry_days is not None and oldest_expiry_days < 7:
        status = "warning"
        headline = f"Kritischer Cookie läuft in {oldest_expiry_days}d ab"
    elif age_days and age_days > 30:
        status = "warning"
        headline = f"cookies.txt seit {int(age_days)}d nicht aktualisiert"
    elif krumm:
        # Sichtbar machen, aber nur wenn sonst nichts ansteht: der Betreiber
        # soll wissen, dass sein Export kaputt war — sonst exportiert er beim
        # naechsten Mal wieder genauso, und die Reparatur bleibt Dauerzustand.
        status = "warning"
        headline = ("cookies.txt war kein gueltiges Netscape-Format — "
                    "automatisch repariert (Backup: .bak)" if repariert else
                    "cookies.txt ist kein gueltiges Netscape-Format und liess "
                    "sich nicht reparieren — sie wird nur notduerftig gelesen, "
                    "yt-dlp scheitert daran. Bitte neu exportieren.")
    else:
        status = "ok"
        headline = "Cookies sehen gesund aus"

    return {
        "exists": True, "status": status, "headline": headline,
        "file_mtime": mtime, "file_age_days": round(age_days, 1) if age_days else None,
        "total": len(all_cookies),
        "expiring_soon": sorted(expiring_soon, key=lambda x: x["days_left"]),
        "expired": expired,
        "critical_present": critical_present,
        "critical_missing": critical_missing,
        "oldest_expiry_days": oldest_expiry_days,
        "duplicate_domain_cookies": duplicate_domain_cookies,
        "repaired": krumm,
        "autorefresh": _KONF["autorefresh_info"](),
        "autofetch": _KONF["autofetch_info"](),
    }
