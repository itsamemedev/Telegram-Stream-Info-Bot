"""nc.updater — Selbst-Update aus dem GitHub-Repo (bot-frei, stdlib-only).

════════════════════════════════════════════════════════════════════════
WOFUER
════════════════════════════════════════════════════════════════════════
Holt den aktuellen Stand des oeffentlichen Repos, vergleicht ihn Datei fuer
Datei mit dem Bestand auf der Platte und schreibt die Unterschiede — mit
vorherigem Backup und moeglichem Rueckrollen. Bedient wird das aus dem
Dashboard (Uebersicht, ganz vorn) und per Telegram-Kommando.

════════════════════════════════════════════════════════════════════════
DIE DREI REGELN, DIE HIER ALLES TRAGEN
════════════════════════════════════════════════════════════════════════
1. **Betriebsdaten sind unantastbar.** `.env`, Datenbanken, Logs, Aufnahmen,
   das Archiv und die vom News-Agenten geschriebene `website/news.json` werden
   NIE angefasst (`PROTECTED`). Ein Update, das die `.env` mit der
   `.env.example` ueberschreibt, kostet 352 Variablen — genau das verhindert
   die Liste.
2. **Nur hinzufuegen und ersetzen, nie loeschen.** Eine lokale Datei, die im
   Archiv fehlt, bleibt liegen. Andernfalls raeumt ein Update eigene Skripte
   und Notizen weg, und das faellt erst Wochen spaeter auf.
3. **Nichts wird geschrieben, bevor das Backup steht.** Jede Datei, die
   ersetzt wird, liegt vorher im Backup-ZIP. `rollback()` stellt genau diesen
   Stand wieder her.

════════════════════════════════════════════════════════════════════════
WARUM BOT-FREI
════════════════════════════════════════════════════════════════════════
Wie nc.news/nc.marketing: die Entscheidungslogik — was ist geschuetzt, was
aendert sich, was wandert ins Backup — sind reine Funktionen ueber Namen und
Hashes. Ein Update laesst sich damit trocken durchrechnen (`dry_run`), ohne
dass eine einzige Datei angefasst wird, und die Fallstricke (Zip-Slip,
absolute Pfade) sind ohne laufenden Bot testbar.
"""

import hashlib
import io
import json
import os
import posixpath
import threading
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field

from nc import sicherpfad as _nc_sicherpfad   # v4.2-W2: ein Riegel fuer alle
from nc import laufstand as _nc_laufstand     # v5.11.4: Marke fuer „teilweise"

# ───────────────────────────────────────────────────────────────────────
# Vorgaben
# ───────────────────────────────────────────────────────────────────────

REPO_DEFAULT = "itsamemedev/Telegram-Stream-Info-Bot"
BRANCH_DEFAULT = "main"
STATE_FILE = ".nc_update.json"          # zuletzt eingespielter Stand
BACKUP_DIR = "backups"
USER_AGENT = "NIGHTCRAWLER-Updater"

# Deckel gegen ein entartetes Archiv. Ein einzelnes File > 40 MB oder ein
# Archiv > 200 MB entpackt gehoert nicht in dieses Repo — dann stimmt etwas
# nicht, und ein voller Datentraeger legt den Bot lahm.
MAX_FILE_BYTES = 40 * 1024 * 1024
MAX_TOTAL_BYTES = 200 * 1024 * 1024

# ───────────────────────────────────────────────────────────────────────
# Was NIE ueberschrieben wird
# ───────────────────────────────────────────────────────────────────────
# Praefixe (Ordner) und exakte Namen. Verglichen wird auf dem normalisierten
# POSIX-Pfad relativ zur Wurzel, klein geschrieben.

PROTECTED_PREFIXES = (
    ".git/", ".venv/", "venv/", "env/", "logs/", "log/",
    "recordings/", "aufnahmen/", "archive/", "archiv/",
    "backups/", "backup/", "data/", "db/", "build/",
    "__pycache__/", ".pytest_cache/", ".mypy_cache/", ".ruff_cache/",
    "node_modules/", "models/", "voices/", "tmp/", "temp/",
)

PROTECTED_NAMES = (
    ".env", ".env.local", ".env.production",
    "config.json", "app_config.json", "cookies.txt", "cookies.json",
    # v5.4-W195: die Datei, die der Bot WIRKLICH liest (bot.py COOKIE_FILE).
    # Geschuetzt war nur „cookies.txt" — ein Name, den nichts schreibt.
    "tiktok_cookies.txt",
    STATE_FILE,
    # Der News-Agent schreibt diese Datei im Betrieb. Kaeme sie aus dem
    # Archiv zurueck, waere die Website schlagartig wieder auf dem Stand
    # des letzten Commits — inklusive verschwundener News.
    "website/news.json",
)

PROTECTED_SUFFIXES = (
    ".db", ".db-wal", ".db-shm", ".sqlite", ".sqlite3",
    ".log", ".session", ".pyc", ".bak", ".pem", ".key",
)


# ───────────────────────────────────────────────────────────────────────
# Konfiguration (Injection statt Modul-Konstanten — .env wird teils erst
# nach den ersten Imports geladen, siehe CLAUDE.md)
# ───────────────────────────────────────────────────────────────────────

@dataclass
class UpdaterConfig:
    root: str = "."
    repo: str = REPO_DEFAULT
    branch: str = BRANCH_DEFAULT
    token: str = ""                 # optionales GitHub-Token (Rate-Limit)
    timeout: float = 30.0
    enabled: bool = True            # Schreiben erlaubt? Pruefen geht immer.
    restart_cmd: str = ""           # z. B. "systemctl restart tiktok-bot"
    keep_backups: int = 10


_CFG = UpdaterConfig()
_LOG = None


def configure(**kw):
    """Konfiguration nachreichen. Unbekannte Schluessel werden ignoriert,
       damit ein aelterer Aufrufer nicht am neuen Feld zerbricht."""
    global _LOG
    if "logger" in kw:
        _LOG = kw.pop("logger")
    for k, v in kw.items():
        if hasattr(_CFG, k) and v is not None:
            setattr(_CFG, k, v)
    return _CFG


def settings():
    """Der aktive Stand — ohne Token, der gehoert nicht in eine API-Antwort."""
    return {"repo": _CFG.repo, "branch": _CFG.branch, "root": _CFG.root,
            "enabled": bool(_CFG.enabled), "has_token": bool(_CFG.token),
            "restart_cmd": _CFG.restart_cmd, "keep_backups": _CFG.keep_backups}


def _log(level, msg, *a):
    if _LOG is None:
        return
    try:
        getattr(_LOG, level)(msg, *a)
    except Exception:
        # Der Fehlerkanal selbst bleibt still — Loggen erzeugt hier Rekursion.
        pass


# ───────────────────────────────────────────────────────────────────────
# Reine Helfer — hier steckt die Entscheidungslogik, voll testbar
# ───────────────────────────────────────────────────────────────────────

def strip_archive_root(name: str) -> str:
    """GitHub packt alles unter `<repo>-<branch>/`. Diese eine Ebene faellt weg.

    Liefert "" fuer den Wurzeleintrag selbst — der Aufrufer ueberspringt ihn."""
    name = (name or "").replace("\\", "/").lstrip("/")
    if "/" not in name:
        return ""
    return name.split("/", 1)[1]


def normalize(rel: str) -> str:
    """Auf POSIX normalisieren. Liefert "" fuer alles, was aus der Wurzel
       ausbrechen wuerde — der Zip-Slip-Riegel."""
    rel = (rel or "").replace("\\", "/").strip()
    if not rel or rel.startswith("/") or ":" in rel.split("/", 1)[0]:
        return ""                       # absolut oder Laufwerksbuchstabe
    norm = posixpath.normpath(rel)
    if norm in (".", "..") or norm.startswith("../") or norm.startswith("/"):
        return ""
    return norm


def is_protected(rel: str) -> bool:
    """Gehoert der Pfad zu den Betriebsdaten, die ein Update nie anfasst?"""
    rel = normalize(rel)
    if not rel:
        return True                     # unbrauchbar = auf keinen Fall schreiben
    low = rel.lower()
    if low in PROTECTED_NAMES:
        return True
    if any(low.startswith(p) for p in PROTECTED_PREFIXES):
        return True
    if any(low.endswith(s) for s in PROTECTED_SUFFIXES):
        return True
    # Auch in Unterordnern: .../logs/... , .../__pycache__/...
    parts = low.split("/")
    if any((p + "/") in PROTECTED_PREFIXES for p in parts[:-1]):
        return True
    if parts[-1] in PROTECTED_NAMES:
        return True
    return False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class Plan:
    """Was ein Update tun WUERDE. Getrennt vom Ausfuehren, damit `dry_run`
       exakt dasselbe rechnet wie der Ernstfall."""
    new: list = field(default_factory=list)        # [rel, ...]
    changed: list = field(default_factory=list)    # [rel, ...]
    same: int = 0
    protected: list = field(default_factory=list)  # uebersprungen (Betriebsdaten)
    rejected: list = field(default_factory=list)   # unbrauchbarer Pfad / zu gross
    total_bytes: int = 0

    def touched(self):
        return list(self.new) + list(self.changed)

    def as_dict(self):
        return {"new": self.new, "changed": self.changed, "same": self.same,
                "protected": self.protected, "rejected": self.rejected,
                "bytes": self.total_bytes,
                "count": len(self.new) + len(self.changed)}


def build_plan(entries, local_hash):
    """Aus (rel, size, sha) je Archiv-Datei den Plan bauen.

    `local_hash(rel)` liefert den sha256 der lokalen Datei oder None, wenn es
    sie nicht gibt. Rein — kein Dateisystem, kein Netz, keine Reihenfolge-
    abhaengigkeit."""
    plan = Plan()
    for rel, size, sha in entries:
        norm = normalize(rel)
        if not norm:
            plan.rejected.append(rel or "?")
            continue
        if size > MAX_FILE_BYTES:
            plan.rejected.append(norm)
            continue
        if is_protected(norm):
            plan.protected.append(norm)
            continue
        cur = local_hash(norm)
        if cur is None:
            plan.new.append(norm)
            plan.total_bytes += size
        elif cur != sha:
            plan.changed.append(norm)
            plan.total_bytes += size
        else:
            plan.same += 1
    plan.new.sort()
    plan.changed.sort()
    plan.protected.sort()
    return plan


def short_sha(sha: str) -> str:
    return (sha or "")[:7]


def describe(check: dict) -> str:
    """Einzeiler fuer Telegram/Log. Sagt den Zustand, nicht das Verfahren."""
    if not check.get("ok"):
        return f"Update-Pruefung fehlgeschlagen: {check.get('error') or 'unbekannt'}"
    if check.get("teilweise"):
        fehl = check.get("fehlgeschlagen") or []
        return ("Unvollstaendig eingespielt: %d Datei(en) nicht geschrieben (%s) — "
                "der Bestand ist gemischt. Erneut aktualisieren."
                % (len(fehl), (", ".join(fehl[:3]) + (" …" if len(fehl) > 3 else "")) or "?"))
    if check.get("update_available"):
        r = check.get("remote") or {}
        return (f"Neuer Stand verfuegbar: {short_sha(r.get('sha'))} "
                f"vom {(r.get('date') or '?')[:10]} — {r.get('message') or ''}".strip())
    if not check.get("local_known"):
        return ("Stand unbekannt (noch kein Update ueber diesen Weg eingespielt) — "
                "Vergleich per Trockenlauf moeglich.")
    return "Alles aktuell."


# ───────────────────────────────────────────────────────────────────────
# Pfade
# ───────────────────────────────────────────────────────────────────────

def _root() -> str:
    return os.path.abspath(_CFG.root or ".")


def _abs(rel: str) -> str:
    """Absoluter Zielpfad — mit zweitem Riegel gegen Ausbruch aus der Wurzel.

    Die Pruefung ist bewusst doppelt: `normalize()` faengt `../` im Archiv-
    namen, diese hier faengt zusaetzlich Symlinks und Sonderfaelle des
    Dateisystems. Ein Zip-Slip schreibt sonst nach /etc.

    v4.2-W2: Der Anspruch stand schon im Kommentar, die Umsetzung hielt ihn
    NICHT ein. `os.path.abspath` loest Symlinks nicht auf — steht in der
    Wurzel ein Link `raus -> /etc`, dann ist `abspath(root/raus/passwd)`
    genau `root/raus/passwd`, die startswith-Pruefung sagt "drin", und
    geschrieben wird nach /etc/passwd. Nur `realpath` loest den Link auf.
    Nachgemessen: abspath+startswith = True, realpath+commonpath = False.

    Ausserdem `commonpath` statt `startswith`: `/opt/nc2` beginnt mit
    `/opt/nc`, liegt aber nicht darin.
    """
    root = _root()
    p = os.path.abspath(os.path.join(root, rel))
    if not _nc_sicherpfad.unter(root, p):
        raise ValueError(f"Pfad verlaesst die Wurzel: {rel}")
    return p


def _state_path() -> str:
    return os.path.join(_root(), STATE_FILE)


def local_state() -> dict:
    """Der zuletzt ueber diesen Weg eingespielte Stand. {} wenn noch keiner."""
    try:
        with open(_state_path(), "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _write_state(d: dict):
    tmp = _state_path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _state_path())


def _git_head() -> str:
    """Falls die Ablage ein Git-Checkout ist, ist der HEAD die ehrlichste
       Quelle fuer den lokalen Stand. Auf dem Server (ZIP-Auslieferung)
       existiert .git nicht — dann greift der State-File."""
    try:
        head = os.path.join(_root(), ".git", "HEAD")
        with open(head, "r", encoding="utf-8") as f:
            line = f.read().strip()
        if line.startswith("ref:"):
            ref = line.split(" ", 1)[1].strip()
            rp = os.path.join(_root(), ".git", *ref.split("/"))
            if os.path.exists(rp):
                with open(rp, "r", encoding="utf-8") as f:
                    return f.read().strip()
            packed = os.path.join(_root(), ".git", "packed-refs")
            with open(packed, "r", encoding="utf-8") as f:
                for ln in f:
                    if ln.strip().endswith(" " + ref):
                        return ln.split(" ", 1)[0].strip()
            return ""
        return line if len(line) == 40 else ""
    except Exception:
        return ""


def local_head() -> tuple:
    """(sha, quelle). quelle ∈ {"update", "teilweise", "git", ""}.

    v5.11.4 (UPD-1): nach einem Update mit Fehlschlaegen traegt der Stand die
    Marke `+teilweise` — der alte Stand plus der Hinweis, dass die Platte
    gemischt ist. Ohne sie meldeten check(), /healthz, /api/version und der
    Laufstand „aktuell" fuer einen Bestand, der weder alt noch neu ist."""
    st = local_state()
    if st.get("teilweise"):
        basis = st.get("sha") or _git_head()
        return basis + _nc_laufstand.TEILWEISE_MARKE, "teilweise"
    if st.get("sha"):
        return st["sha"], "update"
    g = _git_head()
    if g:
        return g, "git"
    return "", ""


# ───────────────────────────────────────────────────────────────────────
# Netz
# ───────────────────────────────────────────────────────────────────────

def _open(url: str, accept: str):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT, "Accept": accept,
        **({"Authorization": f"Bearer {_CFG.token}"} if _CFG.token else {}),
    })
    return urllib.request.urlopen(req, timeout=_CFG.timeout)


def remote_head() -> dict:
    """Der neueste Commit des Branches. Wirft bei Netz-/HTTP-Fehlern."""
    url = f"https://api.github.com/repos/{_CFG.repo}/commits/{_CFG.branch}"
    with _open(url, "application/vnd.github+json") as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    commit = d.get("commit") or {}
    author = commit.get("author") or {}
    msg = (commit.get("message") or "").strip().splitlines()
    return {"sha": d.get("sha") or "", "date": author.get("date") or "",
            "message": msg[0] if msg else "", "author": author.get("name") or "",
            "url": d.get("html_url") or ""}


def zip_url() -> str:
    return f"https://codeload.github.com/{_CFG.repo}/zip/refs/heads/{_CFG.branch}"


def repo_url() -> str:
    return f"https://github.com/{_CFG.repo}"


def commit_zip_url(sha: str) -> str:
    """Archiv GENAU dieses Commits. Siehe download_zip()."""
    return f"https://codeload.github.com/{_CFG.repo}/zip/{sha}"


def download_zip(progress=None, sha: str = "") -> bytes:
    """Das Archiv holen. `progress(gelesen, gesamt_oder_None)` optional.

    v4.2-W149: mit `sha` das Archiv GENAU des Commits, den remote_head()
    gemeldet hat. Vorher kam immer der Branch-Kopf: ein Push zwischen
    Abfrage und Download spielte den neueren Stand ein und schrieb den
    aelteren SHA nach .nc_update.json — /healthz, /api/version und
    nc/laufstand.py meldeten danach einen Stand, der nicht auf der Platte
    lag."""
    url = commit_zip_url(sha) if sha else zip_url()
    with _open(url, "application/zip") as r:
        total = int(r.headers.get("Content-Length") or 0) or None
        buf = io.BytesIO()
        read = 0
        while True:
            chunk = r.read(262144)
            if not chunk:
                break
            read += len(chunk)
            if read > MAX_TOTAL_BYTES:
                raise ValueError("Archiv groesser als erlaubt — abgebrochen.")
            buf.write(chunk)
            if progress:
                progress(read, total)
    return buf.getvalue()


# ───────────────────────────────────────────────────────────────────────
# Pruefen
# ───────────────────────────────────────────────────────────────────────

def check() -> dict:
    """Billige Pruefung: ein GitHub-API-Aufruf, kein Download."""
    sha, src = local_head()
    st = local_state()
    teilweise = src == "teilweise"
    if teilweise:
        sha = sha[:-len(_nc_laufstand.TEILWEISE_MARKE)]
    out = {"ok": True, "repo": _CFG.repo, "branch": _CFG.branch,
           "repo_url": repo_url(), "zip_url": zip_url(),
           "enabled": bool(_CFG.enabled),
           "local": {"sha": sha, "short": short_sha(sha), "source": src},
           "local_known": bool(sha) or teilweise, "last_update": st or None,
           "teilweise": teilweise,
           "fehlgeschlagen": list(st.get("fehlgeschlagen") or []) if teilweise else []}
    try:
        rem = remote_head()
    except urllib.error.HTTPError as e:
        out.update(ok=False, error=f"GitHub antwortete {e.code} — "
                   f"{'Rate-Limit, spaeter erneut' if e.code in (403, 429) else 'Repo/Branch pruefen'}")
        out["summary"] = describe(out)
        return out
    except Exception as e:
        out.update(ok=False, error=f"GitHub nicht erreichbar: {e}")
        out["summary"] = describe(out)
        return out
    rem["short"] = short_sha(rem.get("sha"))
    out["remote"] = rem
    # Ehrlich bleiben: ohne bekannten lokalen Stand ist "es gibt ein Update"
    # eine Behauptung, kein Befund. Dann sagt der Trockenlauf die Wahrheit.
    # Teilweise eingespielt heisst: es gibt etwas einzuspielen, auch wenn der
    # Ziel-SHA schon der aktuelle ist — die fehlenden Dateien.
    out["update_available"] = bool(teilweise or (sha and rem.get("sha") and sha != rem["sha"]))
    out["summary"] = describe(out)
    return out


# ───────────────────────────────────────────────────────────────────────
# Anwenden
# ───────────────────────────────────────────────────────────────────────

def _read_archive(data: bytes):
    """(zipfile, [(rel, size, sha), ...]) — Verzeichnisse und die Wurzel raus."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    entries = []
    for info in zf.infolist():
        if info.is_dir():
            continue
        rel = strip_archive_root(info.filename)
        if not rel:
            continue
        entries.append((rel, info.file_size, None, info))
    return zf, entries


def _entries_with_hash(zf, entries):
    out = []
    for rel, size, _sha, info in entries:
        if size > MAX_FILE_BYTES:
            out.append((rel, size, ""))
            continue
        try:
            out.append((rel, size, sha256_bytes(zf.read(info))))
        except Exception:
            out.append((rel, size, ""))
    return out


def _local_hash_fn():
    def fn(rel):
        try:
            p = _abs(rel)
        except ValueError:
            return None
        if not os.path.isfile(p):
            return None
        try:
            return sha256_file(p)
        except Exception:
            return None
    return fn


def _backup(paths, tag: str, neu=(), vorstand=None) -> str:
    """Alle zu ersetzenden Dateien in ein ZIP legen. Liefert den Dateinamen.

    Laeuft VOR dem ersten Schreibvorgang. Ohne diesen Schritt ist ein Update
    nicht rueckrollbar, und Deploy laeuft hier direkt gegen Produktion."""
    bdir = os.path.join(_root(), BACKUP_DIR)
    os.makedirs(bdir, exist_ok=True)
    name = f"nc_update_{tag}.zip"
    path = os.path.join(bdir, name)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        saved = []
        for rel in paths:
            try:
                p = _abs(rel)
            except ValueError:
                continue
            if os.path.isfile(p):
                z.write(p, rel)
                saved.append(rel)
        # v5.11.4 (UPD-2): der Rollback braucht zwei Dinge, die nicht als
        # Datei im ZIP liegen koennen — welche Dateien das Update NEU anlegt
        # (sie gibt es vorher nicht, also auch kein Backup davon) und welchen
        # Stand .nc_update.json vorher trug. `vorstand` None heisst: es gab
        # keine Datei.
        z.writestr("_manifest.json", json.dumps(
            {"created": time.time(), "files": saved, "root": _root(),
             "neu": list(neu), "vorstand": vorstand},
            ensure_ascii=False, indent=2))
    _prune_backups()
    return name


def _prune_backups():
    """Alte Backups abraeumen — sonst laeuft die Platte des Servers voll."""
    keep = max(1, int(_CFG.keep_backups or 10))
    bdir = os.path.join(_root(), BACKUP_DIR)
    try:
        files = sorted((f for f in os.listdir(bdir)
                        if f.startswith("nc_update_") and f.endswith(".zip")))
        for f in files[:-keep]:
            os.remove(os.path.join(bdir, f))
    except Exception as e:
        _log("warning", "Backup-Abraeumen fehlgeschlagen: %s", e)


def list_backups() -> list:
    bdir = os.path.join(_root(), BACKUP_DIR)
    out = []
    try:
        for f in sorted(os.listdir(bdir), reverse=True):
            if not (f.startswith("nc_update_") and f.endswith(".zip")):
                continue
            p = os.path.join(bdir, f)
            try:
                with zipfile.ZipFile(p) as z:
                    n = len([i for i in z.infolist()
                             if not i.is_dir() and i.filename != "_manifest.json"])
            except Exception:
                n = 0
            out.append({"name": f, "size": os.path.getsize(p),
                        "mtime": os.path.getmtime(p), "files": n})
    except Exception:
        pass
    return out


def ausfuehrbar_im_archiv(info) -> bool:
    """Traegt der ZIP-Eintrag ein Ausfuehrungsrecht? GitHub legt den
    Unix-Modus aus dem Git-Baum in die oberen 16 Bit von external_attr."""
    return bool(((getattr(info, "external_attr", 0) or 0) >> 16) & 0o111)


def _write_file(rel: str, data: bytes, ausfuehrbar=None):
    """Atomar schreiben — und das Ausfuehrungsrecht NICHT verlieren.

    v4.2-W148. Bis hierher entstand jede Datei mit den Vorgaberechten (644):
    nach dem ersten Update ueber das Deck waren installer.sh und
    observability.sh nicht mehr ausfuehrbar, und `sudo ./update.sh` endete in
    „Permission denied (os error 13)" — gemeldet auf Ubuntu 26.04.
    `ausfuehrbar`: True/False aus dem Archiv; None = wie die bisherige Datei."""
    p = os.path.normpath(_abs(rel))
    # Zweiter Riegel, sichtbar fuer CodeQL (W98: `sicherpfad.unter()` ist
    # dicht, aber die Datenflussanalyse sieht ihn nicht). Hier ist er nicht
    # redundant: os.stat/os.chmod sind neue Senken, und ein Riegel, den die
    # Analyse nicht sieht, laesst jede kuenftige Senke unbemerkt durch.
    if not p.startswith(_root() + os.sep):
        raise ValueError("Pfad verlaesst die Wurzel: %s" % rel)
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    alt = os.stat(p).st_mode if os.path.exists(p) else None
    tmp = p + ".ncnew"
    with open(tmp, "wb") as f:
        f.write(data)
    if ausfuehrbar is None:
        ausfuehrbar = bool(alt is not None and alt & 0o111)
    modus = (alt & 0o777) if alt is not None else (0o666 & ~_umask())
    modus = (modus | ((modus & 0o444) >> 2)) if ausfuehrbar else (modus & ~0o111)
    os.chmod(tmp, modus)
    os.replace(tmp, p)                  # atomar: nie eine halbe .py auf Platte


def _umask() -> int:
    m = os.umask(0)
    os.umask(m)
    return m


def rechte_angleichen(raw) -> list:
    """Ausfuehrungsrechte nach dem Archiv setzen — auch fuer Dateien, deren
    INHALT gleich ist. Der Plan vergleicht nur SHA-256: eine Datei, an der
    sich nur das Recht geaendert hat (tools/update.sh in W148), waere nie
    geschrieben worden und bliebe fuer immer 644. -> [rel, …] angeglichen"""
    aus = []
    for rel, _size, _sha, info in raw:
        n = normalize(rel)
        if not n or is_protected(n) or not ausfuehrbar_im_archiv(info):
            continue
        try:
            p = os.path.normpath(_abs(n))
            if not p.startswith(_root() + os.sep):
                raise ValueError("ausserhalb von %s" % _root())
        except ValueError as e:
            # Ein Archivname, der aus der Wurzel fuehrt — der Plan verwirft ihn
            # genauso; hier nur sagen, dass er auch kein Recht bekommt.
            _log("warning", "Update: %s liegt ausserhalb der Wurzel, Recht nicht gesetzt (%s)", n, e)
            continue
        if os.path.isfile(p) and not os.stat(p).st_mode & 0o100:
            m = os.stat(p).st_mode & 0o777
            os.chmod(p, m | ((m & 0o444) >> 2))
            aus.append(n)
    if aus:
        _log("info", "Update: Ausfuehrungsrecht gesetzt fuer %s", ", ".join(aus[:10]))
    return aus


def run_update(dry_run: bool = False, progress=None) -> dict:
    """Ein kompletter Durchlauf. Blockiert — der Aufrufer entscheidet ueber
       den Thread. `progress(phase, prozent, text)` optional."""
    def note(phase, pct, text=""):
        if progress:
            try:
                progress(phase, pct, text)
            except Exception:
                pass

    if not dry_run and not _CFG.enabled:
        return {"ok": False, "error": "Update-Schreiben ist abgeschaltet "
                                      "(UPDATE_ENABLED=0)."}
    started = time.time()
    note("check", 2, "Stand bei GitHub abfragen …")
    try:
        rem = remote_head()
    except Exception as e:
        return {"ok": False, "error": f"GitHub nicht erreichbar: {e}"}

    note("download", 8, "Archiv laden …")
    try:
        data = download_zip(lambda got, tot: note(
            "download", 8 + (52 * got / tot if tot else 20),
            f"{got // 1024} KB geladen"), sha=rem.get("sha") or "")
    except Exception as e:
        return {"ok": False, "error": f"Download fehlgeschlagen: {e}"}

    note("compare", 62, "Dateien vergleichen …")
    try:
        zf, raw = _read_archive(data)
    except Exception as e:
        return {"ok": False, "error": f"Archiv unlesbar: {e}"}
    entries = _entries_with_hash(zf, raw)
    plan = build_plan(entries, _local_hash_fn())

    result = {"ok": True, "dry_run": bool(dry_run), "remote": rem,
              "remote_short": short_sha(rem.get("sha")),
              "plan": plan.as_dict(), "backup": None, "written": 0,
              "restart_needed": False, "restart_cmd": _CFG.restart_cmd,
              "duration_s": 0.0}

    if not dry_run:
        try:
            result["rechte"] = rechte_angleichen(raw)
        except OSError as e:
            _log("warning", "Update: Ausfuehrungsrechte nicht angeglichen: %s", e)

    if not plan.touched():
        result["summary"] = "Alles aktuell — keine Datei zu ersetzen."
        if result.get("rechte"):
            result["summary"] += " Ausfuehrungsrecht gesetzt: %s." % ", ".join(result["rechte"])
        result["duration_s"] = round(time.time() - started, 1)
        if not dry_run:
            _remember(rem, [], None)
        note("done", 100, result["summary"])
        return result

    if dry_run:
        result["summary"] = (f"Trockenlauf: {len(plan.new)} neu, "
                             f"{len(plan.changed)} geaendert — nichts geschrieben.")
        result["duration_s"] = round(time.time() - started, 1)
        note("done", 100, result["summary"])
        return result

    note("backup", 68, "Backup anlegen …")
    tag = time.strftime("%Y%m%d-%H%M%S")
    try:
        result["backup"] = _backup(plan.changed, tag, neu=plan.new,
                                   vorstand=local_state() if os.path.isfile(_state_path()) else None)
    except Exception as e:
        # Ohne Backup wird NICHT geschrieben — sonst gibt es keinen Weg zurueck.
        return {"ok": False, "error": f"Backup fehlgeschlagen, Update abgebrochen: {e}"}

    note("write", 74, "Dateien schreiben …")
    by_name = {}
    for rel, _size, _sha, info in raw:
        n = normalize(rel)
        if n:
            by_name[n] = info
    written, failed = [], []
    todo = plan.touched()
    for i, rel in enumerate(todo):
        info = by_name.get(rel)
        if info is None:
            failed.append((rel, "im Archiv nicht gefunden"))
            continue
        try:
            _write_file(rel, zf.read(info), ausfuehrbar_im_archiv(info))
            written.append(rel)
        except Exception as e:
            # Laut werden: ein stiller Fehlschlag hier hinterlaesst einen
            # halb aktualisierten Baum, und genau das faellt erst beim
            # naechsten Start als ImportError auf.
            _log("error", "Update: %s nicht geschrieben: %s", rel, e)
            failed.append((rel, str(e)))
        if todo:
            note("write", 74 + 24 * (i + 1) / len(todo), f"{i + 1}/{len(todo)}")

    result["written"] = len(written)
    result["failed"] = [{"file": f, "error": e} for f, e in failed]
    result["restart_needed"] = bool(written)
    result["ok"] = not failed
    result["summary"] = (
        f"{len(written)} Datei(en) eingespielt"
        + (f", {len(failed)} fehlgeschlagen" if failed else "")
        + f" — Backup {result['backup']}. Neustart noetig.")
    _remember(rem, written, result["backup"], failed=[f for f, _e in failed])
    result["duration_s"] = round(time.time() - started, 1)
    note("done", 100, result["summary"])
    _log("info", "Update eingespielt: %s (%d Dateien)", short_sha(rem.get("sha")), len(written))
    return result


def _remember(rem: dict, written, backup, failed=()):
    """Den eingespielten Stand merken.

    v5.11.4 (UPD-1): bei Fehlschlaegen NICHT den neuen SHA. Bis dahin stand
    er auch nach ENOSPC mitten im Lauf in .nc_update.json — check() sagte
    „Alles aktuell.", das Deck „entspricht dem Repo", /healthz den neuen
    Commit, und ein zweiter Versuch fand nichts mehr zu tun, obwohl die
    Haelfte fehlte. Jetzt: alter Stand, `teilweise` und die Liste."""
    d = {"sha": rem.get("sha") or "", "date": rem.get("date") or "",
         "message": rem.get("message") or "",
         "applied_at": time.time(), "files": list(written)[:500],
         "file_count": len(written), "backup": backup,
         "repo": _CFG.repo, "branch": _CFG.branch}
    if failed:
        alt = local_state()
        d.update(sha=alt.get("sha") or "", date=alt.get("date") or "",
                 message=alt.get("message") or "", teilweise=True,
                 ziel_sha=rem.get("sha") or "", fehlgeschlagen=list(failed)[:200])
    try:
        _write_state(d)
    except Exception as e:
        _log("warning", "Update-Stand nicht gespeichert: %s", e)


def rollback(name: str) -> dict:
    """Ein Backup zurueckspielen. Nur Dateien aus genau diesem ZIP.

    v4.2-W152: nie neben einem laufenden Update. Beide schreiben Datei fuer
    Datei in denselben Baum; nebeneinander entsteht ein Stand, der weder der
    alte noch der neue ist — und das Backup des Updates enthielte schon
    halb zurueckgespielte Dateien. Der Job-Merker gilt fuer beide."""
    if not _CFG.enabled:
        return {"ok": False, "error": "Update-Schreiben ist abgeschaltet."}
    with _JOB_LOCK:
        if _JOB["running"]:
            _log("warning", "Rollback %s abgelehnt: es laeuft gerade ein Update", name)
            return {"ok": False, "error": "Es laeuft gerade ein Update — erst danach "
                                          "zurueckspielen."}
        vorher = dict(_JOB)
        _JOB.update(running=True, phase="rollback", text="Backup wird zurueckgespielt …")
    try:
        return _zurueckspielen(name)
    finally:
        with _JOB_LOCK:
            # Der Stand des letzten Updates bleibt fuer das Deck lesbar.
            _JOB.update(vorher)


def _zurueckspielen(name: str) -> dict:
    """Der eigentliche Rueckspiel-Lauf — nur ueber rollback() aufrufen."""
    # v4.2-W2: derselbe Riegel wie ueberall. Die Praefix-/Suffix-Pruefung
    # bleibt — sie sagt "nur ein Backup, kein beliebiges ZIP" und ist damit
    # eine fachliche Regel, keine Pfad-Pruefung. Die Pfad-Pruefung macht
    # sicher_join, und zwar mit realpath: ein Symlink im Backup-Ordner
    # ueberlebt jede reine Namenspruefung.
    safe = _nc_sicherpfad.sicherer_name(name or "", vorgabe="")
    if not (safe.startswith("nc_update_") and safe.endswith(".zip")):
        return {"ok": False, "error": "Unbekanntes Backup."}
    # v5.11.4: der Pfad entsteht aus dem VERZEICHNIS, nicht aus der Anfrage —
    # der Name aus /api/update/rollback waehlt nur per Zeichenketten-Vergleich
    # einen vorhandenen Eintrag aus. Die Pruefung oben war dicht, aber CodeQL
    # sieht sie nicht (py/path-injection auf isfile/ZipFile, PR #232); dieselbe
    # Antwort wie beim Ordner-Scan in W98: den Pfad gar nicht erst aus
    # Fremdeingabe bauen. sicher_join bleibt fuer den Symlink-Fall.
    verz = os.path.join(_root(), BACKUP_DIR)
    try:
        vorhanden = os.listdir(verz)
    except OSError as e:
        _log("error", "Rollback %s: Backup-Verzeichnis %s nicht lesbar (%s)", safe, verz, e)
        return {"ok": False, "error": f"Backup {safe} nicht gefunden."}
    eintrag = next((e for e in vorhanden if e == safe), None)
    if eintrag is None:
        return {"ok": False, "error": f"Backup {safe} nicht gefunden."}
    try:
        path = _nc_sicherpfad.sicher_join(verz, eintrag)
    except ValueError:
        return {"ok": False, "error": "Unbekanntes Backup."}
    if not os.path.isfile(path):
        return {"ok": False, "error": f"Backup {safe} nicht gefunden."}
    restored, failed, entfernt = [], [], []
    manifest = {}
    try:
        with zipfile.ZipFile(path) as z:
            try:
                manifest = json.loads(z.read("_manifest.json"))
            except (KeyError, ValueError) as e:
                _log("warning", "Rollback %s: kein lesbares Manifest (%s) — neu "
                     "angelegte Dateien und der Vorstand bleiben unberuehrt.", safe, e)
            for info in z.infolist():
                if info.is_dir() or info.filename == "_manifest.json":
                    continue
                rel = normalize(info.filename)
                if not rel or is_protected(rel):
                    continue
                try:
                    _write_file(rel, z.read(info), ausfuehrbar_im_archiv(info))
                    restored.append(rel)
                except Exception as e:
                    _log("error", "Rollback: %s nicht geschrieben: %s", rel, e)
                    failed.append(rel)
    except Exception as e:
        return {"ok": False, "error": f"Backup unlesbar: {e}"}
    # v5.11.4 (UPD-2): was das Update NEU angelegt hat, gab es vorher nicht —
    # also gehoert es nach dem Rollback auch nicht mehr da. Nur genau diese
    # Liste aus dem Manifest, nie „alles, was nicht im Backup steht".
    for rel in (manifest.get("neu") or []) if isinstance(manifest, dict) else []:
        rel = normalize(rel)
        if not rel or is_protected(rel):
            continue
        try:
            p = _abs(rel)
            if os.path.isfile(p):
                os.remove(p)
                entfernt.append(rel)
        except (OSError, ValueError) as e:
            _log("error", "Rollback: %s nicht entfernt: %s", rel, e)
            failed.append(rel)
    _vorstand_zuruecklegen(manifest, safe, failed)
    return {"ok": not failed, "restored": len(restored), "failed": failed,
            "removed": entfernt, "backup": safe,
            "restart_needed": bool(restored or entfernt),
            "restart_cmd": _CFG.restart_cmd,
            "summary": f"{len(restored)} Datei(en) zurueckgespielt"
                       + (f", {len(entfernt)} neu angelegte entfernt" if entfernt else "")
                       + " — Neustart noetig."}


def _vorstand_zuruecklegen(manifest, backup, failed):
    """.nc_update.json auf den Stand VOR dem Update (v5.11.4, UPD-2).

    Ohne das meldete der Bestand nach dem Rollback weiter den neuen Commit:
    check() „Alles aktuell.", und der naechste Update-Lauf haette nichts
    zurueckgeholt. Ein Backup von vor dieser Fassung kennt den Vorstand
    nicht — dann ist der Stand ehrlich unbekannt, nicht der neue."""
    try:
        if isinstance(manifest, dict) and "vorstand" in manifest:
            vor = manifest.get("vorstand")
            d = dict(vor) if isinstance(vor, dict) else {}
        else:
            d = {"sha": ""}
        if failed:
            # Rollback halb: wieder gemischt, und das soll man sehen (UPD-1).
            d.update(teilweise=True, fehlgeschlagen=list(failed)[:200])
        if not d:
            # Vorher gab es keinen Update-Stand: Datei weg, dann gilt wieder
            # git bzw. AUSLIEFERUNG.json — wie vor dem Update.
            if os.path.isfile(_state_path()):
                os.remove(_state_path())
            return
        d["zurueckgespielt"] = backup
        _write_state(d)
    except (OSError, TypeError, ValueError) as e:
        _log("error", "Rollback %s: Update-Stand nicht zurueckgesetzt (%s) — "
             ".nc_update.json nennt weiter den Stand von NACH dem Update.", backup, e)


# ───────────────────────────────────────────────────────────────────────
# Hintergrundlauf + Fortschritt
# ───────────────────────────────────────────────────────────────────────
# Der Download dauert je nach Leitung zehn Sekunden bis eine Minute. Liefe das
# im Flask-Request, wuerde der Browser in einen Timeout laufen und der Operator
# wuesste nicht, ob das Update noch laeuft. Darum: Thread + Statusabfrage.

_JOB_LOCK = threading.Lock()
_JOB = {"running": False, "phase": "idle", "percent": 0, "text": "",
        "started": 0.0, "finished": 0.0, "result": None, "dry_run": False}


def job_state() -> dict:
    with _JOB_LOCK:
        return dict(_JOB)


def _set(**kw):
    with _JOB_LOCK:
        _JOB.update(kw)


def start_update(dry_run: bool = False) -> dict:
    """Startet den Lauf im Hintergrund. Zweiter Start waehrend eines Laufs
       wird abgelehnt — zwei Updates gleichzeitig schreiben sich gegenseitig
       kaputt."""
    with _JOB_LOCK:
        if _JOB["running"]:
            return {"ok": False, "error": "Es laeuft bereits ein Update.",
                    "state": dict(_JOB)}
        _JOB.update(running=True, phase="start", percent=0, text="",
                    started=time.time(), finished=0.0, result=None,
                    dry_run=bool(dry_run))

    def worker():
        try:
            res = run_update(dry_run=dry_run,
                             progress=lambda p, pct, t="": _set(
                                 phase=p, percent=int(max(0, min(100, pct))), text=t))
        except Exception as e:
            _log("error", "Update-Lauf abgebrochen: %s", e, exc_info=True)
            res = {"ok": False, "error": f"Abbruch: {e}"}
        _set(running=False, phase="done", percent=100,
             finished=time.time(), result=res,
             text=(res.get("summary") or res.get("error") or ""))

    threading.Thread(target=worker, name="nc-updater", daemon=True).start()
    return {"ok": True, "started": True, "dry_run": bool(dry_run)}
