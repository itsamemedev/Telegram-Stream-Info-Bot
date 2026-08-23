"""nc.sysrun — v4.0-W26: privilegierter Kommando-Runner (direkt → sudo -n).

Verbatim aus bot_v37 herausgelöst. Rein logisch (die einzige Aussenwirkung ist
subprocess.run), kein Bot-Zustand. Führt ein Kommando aus — erst direkt, bei
rc!=0 passwortlos via 'sudo -n' — und gibt (rc, stdout, stderr, used_sudo)
zurück, ohne je zu hängen (timeout). Bitgenau gegen den Monolithen geprüft,
inklusive der Reihenfolge der Aufrufe und der Fehlercodes (124=Timeout,
127=nicht gefunden).
"""


def run_priv(args, timeout=6, sudo_first=False):
    """Führt ein Kommando aus: erst direkt; bei rc!=0 (z.B. Permission) via 'sudo -n'
       (passwortlos). Returns (rc, stdout, stderr, used_sudo). Kein Hang (timeout).

       sudo_first=True: für Kommandos, die zwingend Root brauchen (cscli muss die
       root-only LAPI-Credentials lesen, sonst nil-Pointer-Panic). Dann zuerst
       'sudo -n', erst danach der Direktaufruf als Fallback — so entsteht der
       hässliche Panic gar nicht erst, wenn die sudoers-Regel sitzt."""
    import subprocess

    def _run(cmd):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return p.returncode, p.stdout, p.stderr
        except FileNotFoundError:
            return 127, "", "not found"
        except subprocess.TimeoutExpired:
            # B138: eigener Code 124. Vorher kam ein Timeout als rc=1 mit dem
            # Text "Command ... timed out" zurueck und fiel in den Sammelzweig
            # von _crowdsec_status — der Betreiber bekam eine sudoers-Anleitung,
            # obwohl nur die LAPI haengt.
            return 124, "", f"Zeitüberschreitung nach {timeout}s: {' '.join(cmd[:3])}"
        except Exception as e:
            return 1, "", str(e)

    if sudo_first:
        rc, out, err = _run(["sudo", "-n"] + args)
        if rc == 0:
            return rc, out, err, True
        sudo_err = err
        rc2, out2, err2 = _run(args)
        if rc2 == 0:
            return rc2, out2, err2, False
        # beide gescheitert: die sudo-Diagnose ist aussagekräftiger als der Panic
        return (rc2 or rc), out2, (sudo_err or err2), True

    rc, out, err = _run(args)
    if rc == 0:
        return rc, out, err, False
    first_err = err
    rc2, out2, err2 = _run(["sudo", "-n"] + args)
    return rc2, out2, (err2 or first_err), True
