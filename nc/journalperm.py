"""nc.journalperm — v4.0-W62b: Darf der Prozess das Journal/Auth-Log lesen?

Reine Entscheidung, aus _darf_journal_lesen herausgelöst: Mitglied einer der
Gruppen (adm/systemd-journal) ODER root. Die Systemzugriffe (os.getgroups,
grp.getgrnam, os.geteuid) und der breite Fallback→True bleiben beim Aufrufer;
hier kommen nur die aufgelösten Werte rein. gid_of(name) liefert die gid oder
None für unbekannte Gruppen (die werden übersprungen).

WHY: journalctl antwortet ohne Gruppenrecht mit rc=0 und '-- No entries --' —
Erfolg im Code, Leere im Inhalt. Ohne diese Prüfung ist 'niemand greift an' nicht
von 'ich darf nicht hinsehen' zu unterscheiden (das leere Abwehr-Panel).
"""


def may_read(my_gids, gid_of, euid, groups=("adm", "systemd-journal")):
    """True, wenn eine der Gruppen zu my_gids gehört (gid_of(name) → gid|None),
       sonst True nur für root (euid == 0)."""
    for name in groups:
        g = gid_of(name)
        if g is not None and g in my_gids:
            return True
    return euid == 0
