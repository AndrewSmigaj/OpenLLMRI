# ADR-0002: Docker-only MUD on Evennia + PostgreSQL 16

- **Status:** Accepted
- **Date:** 2026-06

## Context

Whiteout targets a reproducible, multiplayer-capable server that any contributor
can stand up identically. The stack is **Evennia 6.0.0** on **Python 3.13**,
**Django 6.0.6**, and a real RDBMS. SQLite (Evennia's default) is fine for a
solo demo but we want production-shaped concurrency and migrations from day one.

A wrinkle surfaced immediately: **Evennia 6.0.0's `createsuperuser` infinitely
loops when stdin is not a TTY**, repeatedly printing *"skipped due to not running
in a TTY."* That breaks the obvious `docker compose run ... createsuperuser`
path for bootstrapping Account #1.

## Decision

- **Run the MUD entirely in Docker.** `docker compose` brings up two services:
  `evennia` (built from [`docker/evennia/Dockerfile`](../../../docker/evennia/Dockerfile),
  extending `evennia/evennia:latest` with `psycopg2-binary` + `pytest` /
  `pytest-django`) and `postgres` (**`postgres:16`**). The game dir is
  bind-mounted at `/usr/src/game`. Ports: **4000** telnet, **4001** website,
  **4002** websocket client.
- **Use PostgreSQL 16** as the database (hence `psycopg2-binary`, since the base
  image targets SQLite).
- **Create Account #1 over a real pseudo-terminal.** The repo ships
  [`scripts/create_superuser.py`](../../../scripts/create_superuser.py), a *host*
  helper that drives `docker compose run ... createsuperuser` under a pty via
  **`pexpect`** and answers the prompts from `.env`. It is idempotent (no prompt →
  superuser already exists → exit clean). `make accounts` runs this, then creates
  the bot account through the Django shell with
  [`scripts/bootstrap_accounts.py`](../../../scripts/bootstrap_accounts.py).
- The torch bot-agent is the **one** thing that does *not* run in Docker — it
  runs on the host (see [ADR-0005](0005-llm-bot-player-and-torch.md)).

## Consequences

- **The pty gotcha is solved once.** After Account #1 exists, **all** other
  commands — `evennia shell`, scenario loading, the server itself — work
  **non-interactively**. `pexpect` becomes a host prerequisite for `make accounts`
  (`pip install pexpect`).
- Reproducible stack; Postgres concurrency and migrations match production shape.
- Two Docker quirks to remember (see [../../guides/docker-workflow.md](../../guides/docker-workflow.md)):
  - `make init` uses `docker run` (not compose) so the `./game` bind-mount isn't
    auto-created empty first, which would make `--init game` refuse.
  - The image's entrypoint **word-splits its arguments**, so any command carrying
    quotes (e.g. `evennia shell -c "..."`) must bypass it with `--entrypoint`.
