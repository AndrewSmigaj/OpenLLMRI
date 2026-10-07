"""Idempotently create the bot accounts, each with a character to play.

- AGENT_ACCOUNT / AGENT_ACCOUNT_PASSWORD (mud/.env): the MUD's own bot account;
- EVENNIA_AGENT_USER / EVENNIA_AGENT_PASS (the repo root's .env; compose passes these two in): the
  account the backend's agent runner logs in with.

An account that exists without a character gets one: the runner plays a character, and accounts
made by code (evennia.create_account) have none. A character is placed in the start room, which the
server's first start creates; on a new database run this again after `make up-d` (the first run
has to come before it: the first start needs Account #1). A bot account is kept out of every
channel and refuses pages: text sent to it would reach the agent's observation, so its prompt.

Run inside the evennia container's Django shell (works once Account #1 exists):

    cat scripts/bootstrap_accounts.py | docker compose run --rm -T --entrypoint evennia evennia shell

`make accounts` wraps this (after creating the superuser via scripts/create_superuser.py).
The superuser (Account #1) is NOT created here — Evennia warns against making
superusers via the shell, and its non-TTY createsuperuser loops; see
scripts/create_superuser.py for that.
"""
import os

from django.conf import settings
from evennia.objects.models import ObjectDB
from evennia.utils.utils import class_from_module

Account = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)


def keep_quiet(account) -> None:
    """No channel posts and no pages reach a bot account."""
    from evennia.comms.models import ChannelDB
    for channel in ChannelDB.objects.get_subscriptions(account):
        channel.disconnect(account)
        print(f"[bootstrap] {account.key!r} left the channel {channel.key!r}")
    account.locks.add("msg:false()")


bots = {}
for name_var, password_var in (("AGENT_ACCOUNT", "AGENT_ACCOUNT_PASSWORD"),
                               ("EVENNIA_AGENT_USER", "EVENNIA_AGENT_PASS")):
    name, password = os.environ.get(name_var), os.environ.get(password_var)
    if not name or not password:
        print(f"[bootstrap] {name_var} or {password_var} unset; skipping")
    else:
        bots.setdefault(name, password)

for name, password in bots.items():
    account = Account.objects.filter(username__iexact=name).first()
    if account is None:
        account, errors = Account.create(username=name, password=password,
                                         email=os.environ.get("AGENT_ACCOUNT_EMAIL", ""))
        if account is None:
            print(f"[bootstrap] could not create {name!r}: {'; '.join(errors)}")
            continue
        print(f"[bootstrap] created bot account {name!r}")
    else:
        print(f"[bootstrap] bot account {name!r} already exists")
    keep_quiet(account)
    if not list(account.characters.all()):
        if ObjectDB.objects.get_id(settings.START_LOCATION) is None:
            print(f"[bootstrap] {name!r} gets its character once the start room exists: "
                  "run `make accounts` again after the server's first start (`make up-d`)")
            continue
        character, errors = account.create_character()
        if character is None:
            print(f"[bootstrap] could not give {name!r} a character: {'; '.join(errors or [])}")
        else:
            print(f"[bootstrap] gave {name!r} the character {character.key!r}")
