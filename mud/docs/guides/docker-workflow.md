# Docker Workflow

The day-to-day developer loop. **Everything (the MUD) runs in Docker**; the one
exception is the torch bot-agent, which runs on the host
([bot-harness.md](bot-harness.md)). Stack: Evennia 6.0.0 + PostgreSQL 16, ports
**4000** telnet / **4001** website / **4002** websocket client.

## First-time bring-up

Run these in order. They are idempotent except `init` (one-time scaffold).

```
make build                      # build the evennia image (psycopg2-binary + pytest)
make init                       # ONE-TIME: scaffold the Evennia game dir
make migrate                    # create the schema in Postgres
make accounts                   # create admin (#1, via pty) + bot account
make load-scenario SCENARIO=whiteout   # load a scenario (defaults to smoketest)
make up                         # run the server in the foreground
telnet localhost 4000           # connect and play
```

### `make accounts` — the pty gotcha

**Evennia 6.0.0's `createsuperuser` infinitely loops when stdin is not a TTY**
(it keeps printing *"skipped due to not running in a TTY"*). So Account #1 must be
created over a **real pseudo-terminal**. The repo does this with
[`scripts/create_superuser.py`](../../scripts/create_superuser.py), which drives
`docker compose run ... createsuperuser` under a pty using **`pexpect`** on the
host — so you need `pip install pexpect` on the host.

`make accounts` runs that pty step, then pipes
[`scripts/bootstrap_accounts.py`](../../scripts/bootstrap_accounts.py) into
`evennia shell` to create the bot account. **Once Account #1 exists, everything
else — `evennia shell`, scenario loading, the server — works non-interactively.**
See [ADR-0002](../architecture/adr/0002-evennia-docker-postgres.md).

## Everyday commands

| Command | Does |
|---|---|
| `make up` / `make up-d` | run the server (foreground / detached) |
| `make down` | stop the stack |
| `make restart` | reload the running server (`evennia reload`) |
| `make logs` | follow the evennia logs |
| `make load-scenario SCENARIO=<name>` | (re)load a scenario's `build()` |
| `make shell` | open an Evennia/Django shell |
| `make agent` | run the scripted bot-player from the host |

## Test & validate

```
make test        # Tier 1: pure sim/ unit tests — no DB, no Evennia boot
make test-int    # Tier 2: Evennia integration tests against a test DB
make validate SCENARIO=<name>   # §44 content-lint
make verify      # compose config check + make test + make validate
```

See [../architecture/testing.md](../architecture/testing.md) and
[validation-rules.md](validation-rules.md).

## Reset

```
make reset-db    # DESTROY the Postgres volume (docker compose down -v) and start fresh
```

After `reset-db` you must re-run `migrate`, `accounts` and `load-scenario`.

## Two Docker quirks worth knowing

- **`make init` uses `docker run`, not compose.** Compose would auto-create the
  `./game` bind-mount empty first, which makes Evennia's `--init game` refuse.
- **The image entrypoint word-splits its arguments.** Any command that carries
  quotes — notably `evennia shell -c "from ... import build; build()"` — must
  bypass the wrapper with **`--entrypoint`**. That is why `load-scenario`,
  `accounts` and `test`/`validate` pass `--entrypoint evennia` (or `--no-deps`)
  rather than a quoted `bash -c "..."`. The compose `command:` likewise hands the
  entrypoint a single script path (`sh server/docker_start.sh`) instead of a
  quoted chain.

## Related

- [adding-a-scenario.md](adding-a-scenario.md) — what `load-scenario` runs.
- [loop-workflow.md](loop-workflow.md) — the authoring loop on top of these.
- [bot-harness.md](bot-harness.md) — the host-side bot.
