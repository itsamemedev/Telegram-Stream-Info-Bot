"""nc.binresolve — v4.0-W60: Auflösung eines absoluten Binary-Pfads.

Aus _cscli_bin herausgelöst und generalisiert. Reihenfolge: erst which(name)
(PATH), dann die Kandidatenliste in Reihenfolge (erster existierender gewinnt),
sonst None. Das None (statt eines Platzhalter-Namens) ist wichtig: ein sudoers-
Eintrag 'NOPASSWD: /usr/bin/cscli' matcht nur bei EXAKT diesem Pfad, und ein
'sudo -n <name>' auf ein fehlendes Programm sähe wie ein Rechteproblem aus.
which/exists werden injiziert → ohne echtes Dateisystem testbar.
"""


def resolve(name, candidates, which, exists):
    """Absoluter Pfad zu name: which(name) zuerst, dann der erste existierende
       Kandidat, sonst None. which/exists sind Callables (shutil.which, os.path.exists)."""
    p = which(name)
    if p:
        return p
    for c in candidates:
        if exists(c):
            return c
    return None
