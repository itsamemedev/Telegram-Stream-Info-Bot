"""nc.abwehrlage — v5.8-W199: Sperrliste (CrowdSec) und SSH-Angriffe, aus bot.py geloest.

Zeigt Angriffe (fehlgeschlagene SSH-Logins) und die Sperrliste, geo-lokalisiert
fuer die Weltkarte im Deck. Liest Server-Logs und CrowdSec; wo dem Bot-User
Rechte fehlen, wird 'sudo -n' versucht und sonst ein klarer Hinweis mit
Abhilfe zurueckgegeben (kein Absturz).

Die Koerper sind woertlich aus dem Monolithen uebernommen (dort ab v4.0-W18,
B132, B138). Ersetzt wurden nur die Namen, die dort Modul-Globals waren:
die vier CROWDSEC_*-Werte kommen per configure() herein — als Werte, die der
Bot nach load_dotenv() gelesen hat, nie als Modul-Konstante dieses Moduls
(CLAUDE.md, W67). Der Zugang zu den Routen bleibt in nc/routes/abwehr.py:
der Bot traegt crowdsec_status und ssh_angriffe dort als HAKEN ein.

Ohne Bot-Import, ohne Netz beim Import — isoliert pruefbar.
"""

import json
import logging
import os
import re
import shutil
import time

from nc import binresolve as _nc_binresolve
from nc import crowdsec as _nc_crowdsec
from nc import geoip as _nc_geoip
from nc import journalperm as _nc_journalperm
from nc import meldetakt as _nc_meldetakt
from nc import sysrun as _nc_sysrun

log = logging.getLogger("TikTokBot")

# Die Vorgaben entsprechen denen im Bot; configure() ueberschreibt sie beim Start.
_KONF = {"lapi_host": "127.0.0.1", "lapi_port": 8083, "bouncer_key": "", "lapi_url": ""}

# Drossel der LAPI-Fehlerzeile je HTTP-Status (v4.1-W12). Im Monolithen lag
# sie per globals().setdefault — hier ist sie schlicht Modulzustand.
_CROWDSEC_LOG_STATE = {}

_CSCLI_CACHE = [None]      # gefundener Pfad; solange None wird neu gesucht

AUTHLOG_HINT = ("Auth-Log nicht lesbar: Bot-User in die Gruppen 'adm' und 'systemd-journal' "
                "aufnehmen und den Dienst neu starten — Gruppenrechte greifen erst im neuen "
                "Prozess, ein blosses 'usermod' ohne Neustart aendert nichts.")


def configure(*, lapi_host=None, lapi_port=None, bouncer_key=None, lapi_url=None):
    """Vom Bot einmal beim Start gerufen, mit den Werten aus der .env."""
    for k, v in (("lapi_host", lapi_host), ("lapi_port", lapi_port),
                 ("bouncer_key", bouncer_key), ("lapi_url", lapi_url)):
        if v is not None:
            _KONF[k] = v


# B132: fail2ban laeuft auf diesem Server nicht mehr — ersetzt durch CrowdSec.
# Der alte Aufruf blieb im Code stehen und lieferte dauerhaft "nicht
# erreichbar": leere Bannliste, leere Weltkarte, ohne dass irgendwo stand warum.
def cscli_bin():
    """Absoluter cscli-Pfad. Wichtig fuer sudoers: eine Regel wie
       'NOPASSWD: /usr/bin/cscli' matcht nur, wenn sudo GENAU diesen Pfad
       aufruft. Liegt cscli in /usr/local/bin (haeufig bei CrowdSec), scheiterte
       'sudo -n cscli' bisher stumm → Passwortabfrage → Panic vom rechtelosen
       Direktaufruf. Deshalb den echten Pfad ermitteln und ueberall nutzen.

       B138: Rueckgabe None statt des Platzhalters "cscli". Mit dem Platzhalter
       lief 'sudo -n cscli' los, sudo antwortete 'sudo: cscli: command not
       found', und die Fehlerzuordnung sah darin wegen des Praefix 'sudo:' ein
       fehlendes Recht — der Betreiber befolgte eine sudoers-Anleitung fuer ein
       Programm, das es auf dem Server gar nicht gibt."""
    # v4.0-W60: Aufloesung nach nc/binresolve.py (which zuerst, dann Kandidaten,
    # sonst None — which/exists injiziert, gegen Mocks bewiesen).
    return _nc_binresolve.resolve(
        "cscli",
        ("/usr/bin/cscli", "/usr/local/bin/cscli", "/usr/sbin/cscli",
         "/usr/local/sbin/cscli"),
        shutil.which, os.path.exists)


def cscli_path():
    """Pfad zur Laufzeit ermitteln statt beim Import einzufrieren.

       B138: vorher stand das Ergebnis in der Modul-Konstante _CSCLI. Wer
       CrowdSec nachinstalliert hatte, bekam bis zum naechsten Bot-Neustart
       weiter 'cscli nicht gefunden'. Ein Fund wird gemerkt, ein Fehlschlag
       nicht — nur so wirkt eine Nachinstallation sofort, und shutil.which plus
       vier os.path.exists sind pro Panel-Aufruf billig genug."""
    if _CSCLI_CACHE[0]:
        return _CSCLI_CACHE[0]
    p = cscli_bin()
    if p:
        _CSCLI_CACHE[0] = p
    return p


def sudo_hinweis():
    """Hinweis mit dem ECHTEN Pfad. sudoers verlangt einen absoluten Pfad — der
       frueher eingebaute Platzhalter 'cscli' haette eine Regel ergeben, die
       sudo stillschweigend nie anwendet."""
    p = cscli_path() or "/usr/bin/cscli"
    return ("CrowdSec nicht abfragbar: dem Bot-User (ubuntu) passwortlosen Zugriff geben — "
            f"/etc/sudoers.d/nightcrawler: 'ubuntu ALL=(root) NOPASSWD: {p}' "
            "(Pfad muss exakt stimmen), danach prüfen: sudo systemctl status crowdsec")


def darf_journal_lesen():
    """Darf dieser Prozess Auth-Logs/Journal ueberhaupt lesen?

       Braucht es, weil journalctl ohne Gruppenrecht mit rc=0 und
       '-- No entries --' antwortet: Erfolg im Rueckgabecode, Leere im Inhalt.
       Ohne diese Pruefung ist 'niemand greift an' nicht von 'ich darf nicht
       hinsehen' zu unterscheiden — genau das leere Panel."""
    try:
        import grp

        def _gid_of(name):
            try:
                return grp.getgrnam(name).gr_gid
            except KeyError:
                return None
        # v4.0-W62b: Entscheidung nach nc/journalperm.py (Werte injiziert, bewiesen).
        return _nc_journalperm.may_read(set(os.getgroups()), _gid_of, os.geteuid())
    except Exception:
        return True   # Nicht-Linux/unklar: lieber nicht faelschlich Alarm schlagen


def crowdsec_via_lapi():
    """v4.0-W18: Sperrliste ueber die CrowdSec-LAPI mit einem Bouncer-Schluessel.
       Braucht KEIN Root (der cscli-Weg schon — daher die sudoers-Regel). Gibt
       None zurueck, wenn kein Schluessel gesetzt ist -> Aufrufer nimmt cscli."""
    if not _KONF["bouncer_key"]:
        return None
    import urllib.error
    import urllib.request
    host, port = _KONF["lapi_host"], _KONF["lapi_port"]
    url = _nc_crowdsec.decisions_url(_KONF["lapi_url"], host, port)
    req = urllib.request.Request(url, headers=_nc_crowdsec.headers(_KONF["bouncer_key"]))
    try:
        with urllib.request.urlopen(req, timeout=6) as r:      # noqa: S310 (feste URL)
            raw = r.read().decode("utf-8", "replace")
        data = json.loads(raw) if raw.strip() else []
    except urllib.error.HTTPError as e:
        status, hint, fix = _nc_crowdsec.explain_status(e.code)
        # v4.1-W12: gedrosselt UND mit Abhilfe. Vorher stand hier 109 Mal in
        # dreieinhalb Stunden dieselbe Zeile "CrowdSec-LAPI HTTP 403" — der
        # Dashboard-Takt ruft diesen Weg alle zwei Minuten auf, und ein 403
        # ist ein DAUERZUSTAND (Schluessel nicht registriert), kein Ereignis.
        # Was dabei fehlte, war ausgerechnet das Wichtige: hint und fix gingen
        # nur an die API zurueck, nie ins Log. Wer den Log las, sah 109 Mal
        # eine Zahl und nie, was zu tun ist. Jetzt: beim ersten Mal und danach
        # hoechstens alle 15 Minuten, dafuer mit Grund und Abhilfe.
        _st = _CROWDSEC_LOG_STATE
        _now = time.time()
        _prev = _st.get(e.code) or {"ts": 0.0, "n": 0}
        _prev["n"] += 1
        if _now - _prev["ts"] >= 900:
            _sup = _prev["n"] - 1
            log.warning("Abwehr: CrowdSec-LAPI HTTP %s — %s Abhilfe: %s%s",
                        e.code, hint, fix,
                        (f" (×{_sup} unterdrueckt seit der letzten Meldung)"
                         if _sup > 0 else ""))
            _prev["ts"] = _now
            _prev["n"] = 0
        _st[e.code] = _prev
        return {"ok": False, "status": status, "error": f"HTTP {e.code}",
                "hint": hint, "fix": fix, "jails": [], "total_banned": 0,
                "engine": "crowdsec", "via": "lapi"}
    except Exception as e:
        return {"ok": False, "status": "lapi_tot", "error": str(e)[:160],
                "hint": (f"CrowdSec-LAPI ({host}:{port}) "
                         "nicht erreichbar."),
                "fix": "sudo systemctl restart crowdsec && sudo cscli lapi status",
                "jails": [], "total_banned": 0, "engine": "crowdsec", "via": "lapi"}
    jails, total = _nc_crowdsec.parse_decisions(data)
    return {"ok": True, "status": ("ok" if total else "leer"), "via_sudo": False,
            "engine": "crowdsec", "via": "lapi", "jails": jails,
            "total_banned": total}


def crowdsec_status():
    """B132: Bannliste aus CrowdSec statt fail2ban.

    CrowdSec ist hier nicht nur das Vorhandene, sondern der bessere Partner:
    `cscli -o json` liefert strukturierte Daten. Das alte fail2ban-Modul
    parste Freitext ("Jail list:", "Currently banned:") — bei jeder
    Formataenderung ein stiller Ausfall.

    Die Rueckgabeform bleibt bewusst identisch (jails / total_banned), damit
    Weltkarte und alle Aufrufer unveraendert weiterlaufen. Eine CrowdSec-
    Entscheidung wird auf das Jail-Modell abgebildet: 'jail' ist die Herkunft
    (crowdsec, cscli, CAPI), 'ips' sind die gesperrten Adressen.
    """
    # W18: wenn ein Bouncer-Schluessel hinterlegt ist, ueber die LAPI gehen —
    # kein Root noetig. Nur wenn das fehlschlaegt/fehlt, der alte cscli-Weg.
    _lapi = crowdsec_via_lapi()
    if _lapi is not None and _lapi.get("ok"):
        _nc_meldetakt.zuruecksetzen("crowdsec")
        return _lapi
    host, port = _KONF["lapi_host"], _KONF["lapi_port"]
    cscli = cscli_path()
    if not cscli:
        # B138: zuerst pruefen, OB es das Programm gibt. sudo meldet ein
        # fehlendes Programm mit einer Zeile, die mit 'sudo:' beginnt — die
        # Zuordnung unten hat das bisher als fehlendes Recht gedeutet und den
        # Betreiber in eine sudoers-Datei geschickt, die nichts repariert.
        log.warning("Abwehr: cscli nicht gefunden — weder im PATH noch in /usr/bin, "
                    "/usr/local/bin, /usr/sbin, /usr/local/sbin")
        return {"ok": False, "status": "fehlt",
                "error": "cscli nicht gefunden",
                "hint": "CrowdSec ist auf diesem Server nicht installiert — "
                        "es fehlt also nicht das Recht, sondern das Programm.",
                "fix": "sudo apt install crowdsec && sudo systemctl enable --now crowdsec",
                "jails": [], "total_banned": 0, "engine": "crowdsec"}
    rc, out, err, sudo = _nc_sysrun.run_priv([cscli, "decisions", "list", "-o", "json"],
                                             sudo_first=True)
    if rc != 0:
        e = ((err or out or "").strip())
        el = e.lower()
        if rc == 124 or "zeitüberschreitung" in el or "timed out" in el:
            status = "timeout"
            hint = "cscli antwortet nicht innerhalb des Zeitlimits — haengt die LAPI?"
            fix = "sudo systemctl restart crowdsec && sudo cscli lapi status"
        elif ("password is required" in el or "a terminal is required" in el
              or el.startswith("sudo:")):
            status = "kein_sudo"
            hint = sudo_hinweis()
            fix = (f"echo 'ubuntu ALL=(root) NOPASSWD: {cscli}' | sudo tee "
                   "/etc/sudoers.d/nightcrawler && sudo systemctl restart tiktok-bot")
        elif ("connection refused" in el or f":{port}" in el
              or ":8080" in el or "panic" in el
              or "nil pointer" in el or "unable to list decisions" in el
              or "dial tcp" in el):
            status = "lapi_tot"
            # W17: Port ist konfigurierbar (Henry faehrt die LAPI auf 8083) —
            # ein fest verdrahtetes 8080 im Hinweis schickt den Betreiber sonst
            # auf die falsche Faehrte.
            hint = (f"CrowdSec-Dienst/LAPI ({host}:{port}) "
                    "antwortet nicht.")
            fix = "sudo systemctl restart crowdsec && sudo cscli lapi status"
        else:
            status = "fehler"
            hint = sudo_hinweis()
            fix = f"sudo -n {cscli} decisions list -o json"
        # log.warning statt stillem Verschlucken: ein leeres Abwehr-Panel war
        # bisher im journalctl nicht wiederzufinden.
        # v4.2-W133: gedrosselt — das Deck fragt im Minutentakt, und ein
        # Dauerzustand schrieb 106 gleiche Zeilen in dreieinhalb Stunden.
        # Ein neuer Status meldet sich sofort (nc/meldetakt.py).
        laut, weg = _nc_meldetakt.melden("crowdsec", status, time.monotonic())
        if laut:
            log.warning("Abwehr: cscli rc=%s status=%s: %s — Abhilfe: %s%s", rc,
                        status, e[:200], fix, _nc_meldetakt.zusatz(weg))
        return {"ok": False, "status": status,
                "error": (e or "cscli nicht erreichbar")[:300],
                "hint": hint, "fix": fix, "jails": [], "total_banned": 0,
                "engine": "crowdsec"}
    try:
        data = json.loads(out or "null")
    except ValueError:
        log.warning("Abwehr: cscli lieferte kein JSON (%d Zeichen Ausgabe)", len(out or ""))
        return {"ok": False, "status": "json_kaputt",
                "error": "cscli lieferte kein gueltiges JSON",
                "hint": "Das Ausgabeformat hat sich geaendert oder eine Warnung stand vor dem JSON.",
                "fix": f"{cscli} decisions list -o json | head -c 400",
                "jails": [], "total_banned": 0, "engine": "crowdsec"}
    # Ohne Entscheidungen gibt cscli 'null' aus, nicht '[]'. Das ist ein
    # Erfolg, kein Fehler — dann ist schlicht niemand gesperrt.
    _nc_meldetakt.zuruecksetzen("crowdsec")   # naechster Ausfall meldet sofort
    rows = data or []
    by_origin, total = {}, 0
    for d in rows:
        # Je nach cscli-Version flach oder unter 'decisions' geschachtelt.
        # Beides akzeptieren, statt sich auf eine Variante zu verlassen.
        for dec in (d.get("decisions") or [d]):
            ip = (dec.get("value") or "").strip()
            if not ip:
                continue
            origin = (dec.get("origin") or "crowdsec").strip()
            e = by_origin.setdefault(origin, {"jail": origin, "ips": [],
                                              "banned_now": 0,
                                              "banned_total": None,
                                              "scenarios": {}})
            if ip not in e["ips"]:
                e["ips"].append(ip)
                e["banned_now"] += 1
                total += 1
            sc = (dec.get("scenario") or "").split("/")[-1]
            if sc:
                e["scenarios"][sc] = e["scenarios"].get(sc, 0) + 1
    # B138: 'leer' ist ein Erfolgszustand — cscli hat geantwortet, es ist nur
    # niemand gesperrt. Das Frontend muss das vom Rechteproblem trennen koennen.
    return {"ok": True, "status": ("ok" if total else "leer"), "via_sudo": sudo,
            "engine": "crowdsec", "cscli": cscli,
            "jails": list(by_origin.values()), "total_banned": total}


_PAT_FAIL = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\d{1,3}(?:\.\d{1,3}){3})")
_PAT_INV = re.compile(r"Invalid user (\S+) from (\d{1,3}(?:\.\d{1,3}){3})")
_PAT_IP = re.compile(r"from (\d{1,3}(?:\.\d{1,3}){3})")


def ssh_angriffe(limit=300):
    """Aggregiert fehlgeschlagene SSH-Logins (Angriffe) pro IP aus auth.log/secure,
       Fallback journalctl bzw. sudo. Returns {ok, attacks:[{ip,count,last,users}], ...}."""
    # B138: die Ursache wird festgehalten statt weggeworfen. Vorher verschluckte
    # 'except (PermissionError, FileNotFoundError, OSError): continue' beide
    # Faelle gleich, und journalctl antwortet ohne Gruppenrecht mit rc=0 und
    # '-- No entries --' — das Panel meldete dann 'Keine Angriffe protokolliert',
    # obwohl es nichts lesen durfte. Auf Ubuntu 24.04 gibt es /var/log/auth.log
    # gar nicht mehr, damit war das der Normalfall, nicht der Ausnahmefall.
    text, source, denied = "", None, False
    for p in ("/var/log/auth.log", "/var/log/auth.log.1", "/var/log/secure"):
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", errors="ignore") as f:
                text += f.read()
                source = p
        except PermissionError:
            denied = True
        except OSError as ex:
            log.warning("Abwehr: %s existiert, ist aber nicht lesbar: %s", p, ex)
    if not text:
        rc, out, _e, sudo = _nc_sysrun.run_priv(["journalctl", "-u", "ssh", "-u", "sshd",
                                                 "--no-pager", "-n", "8000"], timeout=8)
        leer = (rc == 0 and "no entries" in (out or "").strip().lower())
        if rc == 0 and out and not leer:
            text, source = out, "journalctl" + ("+sudo" if sudo else "")
        elif leer and darf_journal_lesen():
            # Wir duerfen lesen und es steht wirklich nichts drin: der gute Fall.
            return {"ok": True, "status": "leer", "source": "journalctl",
                    "attacks": [], "total": 0, "unique_ips": 0}
        else:
            denied = True
    if not text:
        rc, out, _e, sudo = _nc_sysrun.run_priv(["cat", "/var/log/auth.log"], timeout=8)
        if rc == 0 and out:
            text, source = out, "auth.log+sudo"
        else:
            denied = True
    if not text:
        status = "keine_rechte" if denied else "keine_logs"
        log.warning("Abwehr: kein Auth-Log lesbar (status=%s)", status)
        return {"ok": False, "status": status,
                "error": ("Auth-Log vorhanden, aber nicht lesbar" if status == "keine_rechte"
                          else "kein Auth-Log und kein Journal-Eintrag gefunden"),
                "hint": (AUTHLOG_HINT if status == "keine_rechte" else
                         "Weder /var/log/auth.log noch das Journal liefern SSH-Zeilen — "
                         "laeuft auf diesem Server ueberhaupt ein sshd?"),
                "fix": ("sudo usermod -aG adm,systemd-journal ubuntu && "
                        "sudo systemctl restart tiktok-bot"
                        if status == "keine_rechte" else "systemctl status ssh"),
                "attacks": [], "total": 0, "unique_ips": 0}
    return auswerten(text, source, limit)


def auswerten(text, source, limit=300):
    """Auth-Log-Text zu Angriffen je IP verdichten — rein, ohne Dateizugriff.

    v5.8-W199: aus dem Ende von _parse_ssh_attacks geloest, damit sich die
    Auswertung ohne /var/log pruefen laesst. Private Adressen zaehlen nicht:
    der eigene Rechner und das LAN sind kein Angriff."""
    agg = {}
    for line in text.splitlines():
        if not ("Failed password" in line or "Invalid user" in line
                or "authentication failure" in line or "Connection closed by authenticating" in line):
            continue
        mm = _PAT_FAIL.search(line) or _PAT_INV.search(line)
        if mm:
            user, ip = mm.group(1), mm.group(2)
        else:
            ipm = _PAT_IP.search(line)
            if not ipm:
                continue
            user, ip = "?", ipm.group(1)
        if _nc_geoip.ist_privat(ip):
            continue
        d = agg.setdefault(ip, {"ip": ip, "count": 0, "last": line[:15], "users": set()})
        d["count"] += 1
        d["last"] = line[:15]
        if user and user != "?":
            d["users"].add(user)
    attacks = sorted(agg.values(), key=lambda x: x["count"], reverse=True)[:limit]
    for a in attacks:
        a["users"] = sorted(a["users"])[:6]
    return {"ok": True, "status": ("ok" if agg else "leer"), "source": source,
            "attacks": attacks, "total": sum(a["count"] for a in agg.values()),
            "unique_ips": len(agg)}
