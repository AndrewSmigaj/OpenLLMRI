"""Idempotently create the non-superuser bot player account from env.

Run inside the evennia container's Django shell (works once Account #1 exists):

    cat scripts/bootstrap_accounts.py | docker compose run --rm -T --entrypoint evennia evennia shell

`make accounts` wraps this (after creating the superuser via scripts/create_superuser.py).
The superuser (Account #1) is NOT created here — Evennia warns against making
superusers via the shell, and its non-TTY createsuperuser loops; see
scripts/create_superuser.py for that.
"""
import os

from django.contrib.auth import get_user_model

User = get_user_model()  # Evennia's AccountDB

name = os.environ.get("AGENT_ACCOUNT")
if not name:
    print("[bootstrap] AGENT_ACCOUNT unset; skipping bot account")
elif User.objects.filter(username=name).exists():
    print(f"[bootstrap] bot account {name!r} already exists")
else:
    from evennia import create_account

    create_account(
        name,
        os.environ.get("AGENT_ACCOUNT_EMAIL", ""),
        os.environ["AGENT_ACCOUNT_PASSWORD"],
    )
    print(f"[bootstrap] created bot account {name!r}")
