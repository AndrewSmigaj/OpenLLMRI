#!/usr/bin/env python3
"""Create Evennia's superuser (Account #1) over a real pty.

Evennia 6.0.0 loops forever on `createsuperuser --noinput` when stdin is not a
TTY, so automated/Docker superuser creation needs a pseudo-terminal. This host
helper drives `docker compose run` under a pty (via pexpect) and answers the
prompts. It is safe to re-run: if Account #1 already exists Evennia won't prompt
and we exit cleanly.

Credentials are read from .env (EVENNIA_SUPERUSER / _EMAIL / _PASSWORD).
`make accounts` calls this.
"""
import os
import sys

try:
    import pexpect
except ImportError:
    sys.exit("pexpect not installed on host. Run: pip install pexpect")


def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())


load_dotenv()

user = os.environ.get("EVENNIA_SUPERUSER", "admin")
email = os.environ.get("EVENNIA_SUPERUSER_EMAIL", "")
password = os.environ.get("EVENNIA_SUPERUSER_PASSWORD")
if not password:
    sys.exit("EVENNIA_SUPERUSER_PASSWORD not set (.env)")

child = pexpect.spawn(
    "docker compose run --rm evennia evennia createsuperuser",
    timeout=180,
    encoding="utf-8",
)
child.logfile_read = sys.stdout

try:
    # Evennia may print "already exists"/skip if #1 is present; tolerate EOF early.
    i = child.expect([r"[Uu]sername.*?:", pexpect.EOF])
    if i == 1:
        print("\n[create_superuser] no prompt (superuser likely already exists)")
        sys.exit(0)
    child.sendline(user)
    child.expect(r"[Ee]mail.*?:")
    child.sendline(email)
    child.expect(r"[Pp]assword:")
    child.sendline(password)
    child.expect(r"[Pp]assword.*?again.*?:")
    child.sendline(password)
    child.expect(pexpect.EOF)
    print("\n[create_superuser] done")
except pexpect.exceptions.TIMEOUT:
    sys.exit("\n[create_superuser] timed out waiting for a prompt")
