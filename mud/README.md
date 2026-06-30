# Whiteout

**Whiteout** is a text-forward, multiplayer, *systemic* survival-puzzle MUD on
[Evennia](https://www.evennia.com/). Survivors of a snowy plane crash improvise with every
object around them to outlast cold, injury, hunger and a worsening storm until rescue,
escape or collapse. You survive by *understanding the world*, not by guessing the author's
intended verb-object pair.

This repo (`MUDExperiments`) hosts a reusable simulation engine (the "interaction system")
plus multiple authored scenarios. Whiteout is the first.

Stack: **Evennia 6.0.0**, Python 3.13, Django 6.0.6, **PostgreSQL 16**. The MUD runs
entirely in Docker on ports **4000** (telnet), **4001** (website), **4002** (websocket).

## Prerequisites
- **Docker** + Docker Compose (the MUD runs entirely in containers).
- Host **`python3`** with **`pexpect`** (`pip install pexpect`) — needed only for
  `make accounts`, which creates Account #1 over a pty (Evennia's `createsuperuser` loops
  without a TTY).

## Quickstart
```sh
docker compose build      # build the Evennia image
make init                 # one-time: scaffold the Evennia game dir
cp .env.example .env      # then edit passwords; .env is gitignored
make accounts             # create the admin superuser + bot account
make load-scenario        # load the smoketest scene (SCENARIO=smoketest)
make up                   # run the server
```
Then connect:
```sh
telnet localhost 4000
connect admin <password>   # the EVENNIA_SUPERUSER_PASSWORD from your .env
```
Run `make help` to see every target. Useful ones: `make logs`, `make restart`,
`make test` (pure unit tests), `make validate` (content lint), `make verify`.

## Bot harness
`agent/` is a host-side bot that plays the game over telnet (`make agent` runs the scripted
brain). It runs on the **host**, not in Docker — the torch brain needs your model weights +
GPU. See `agent/README.md`.

## Read more
- [`VISION.md`](VISION.md) — what we're building and the non-negotiables.
- [`docs/scenarios/whiteout/design.md`](docs/scenarios/whiteout/design.md) — the full design.
- [`docs/scenarios/whiteout/roadmap.md`](docs/scenarios/whiteout/roadmap.md) — the build order.
- [`docs/`](docs/) — architecture overview and authoring guides.
- [`CLAUDE.md`](CLAUDE.md) — orientation for Claude Code working in this repo.
