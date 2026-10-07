---
name: setup
description: First-time project setup — venv, .env files, the MUD (Evennia 6 in Docker) and its accounts, the model
---

# Project Setup

Full setup for someone cloning the repo from scratch. After this, `/server` starts everything and `/agent` runs sessions.

Needs: Python 3.10.12, Node.js 20.19+, Docker with compose, and a CUDA GPU with 16 GB.

All commands resolve `$ROOT` and `$PY` at the top:

```bash
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
```

---

## Operations

### OP-1: Create virtual environment and install dependencies

`make setup` installs the exact working environment (Python 3.10.12 and `backend/requirements.lock.txt`; never `requirements.txt`, whose loose versions can break the MXFP4 model loading), the frontend's packages, and turns on the repo's pre-commit hook.

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT" && make setup
```

### OP-2: Create the root `.env`

The root `.env` is read by the backend (`load_dotenv()` in `main.py`, before any schema imports), by the MUD's compose file and by the app. Format is bare `KEY=VALUE` (no `export`). This generates the password of the account the backend's agent plays (`EVENNIA_AGENT_USER` / `EVENNIA_AGENT_PASS`) and never prints it.

```bash
ROOT=$(git rev-parse --show-toplevel) && cp -n "$ROOT/.env.example" "$ROOT/.env" && sed -i "s|^EVENNIA_AGENT_PASS=change-me$|EVENNIA_AGENT_PASS=$(openssl rand -hex 16)|" "$ROOT/.env" && echo ".env ready. Edit it to set OPENAI_API_KEY and other keys."
```

### OP-3: Create the MUD's `.env`

`mud/.env` holds the MUD's Postgres credentials, its admin account (Account #1) and its own bot account. This generates the three passwords and never prints them.

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT/mud" && cp -n .env.example .env && for k in POSTGRES_PASSWORD EVENNIA_SUPERUSER_PASSWORD AGENT_ACCOUNT_PASSWORD; do sed -i "s|^$k=changeme-.*|$k=$(openssl rand -hex 16)|" .env; done && echo "mud/.env ready."
```

### OP-4: Build and start the MUD

The MUD runs in Docker on the ports in the root `.env` (`MUD_TELNET_PORT` 4000, `MUD_WEB_PORT` 4001, `MUD_WS_PORT` 4002). In order:
- `make build` builds the pinned image;
- `make migrate` creates the database;
- `make accounts` creates Account #1, which the server's first start needs, and the bot accounts;
- `make up-d` is the first start: it creates the start room and builds the institute (the hub, the polysemy lab, the simulator);
- `make accounts` again gives the bot accounts their characters, in the start room.

Run with `run_in_background: true`; the image build takes a few minutes the first time.

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT/mud" && make build && make migrate && make accounts && make up-d && until docker logs llmri-mud-evennia 2>&1 | grep -q "Evennia Server successfully started"; do sleep 3; done && make accounts && echo "MUD ready on the ports in the root .env"
```

### OP-5: Download model

~40GB download. Run with `run_in_background: true`.

```bash
ROOT=$(git rev-parse --show-toplevel) && "$ROOT/.venv/bin/pip" install "huggingface_hub[cli]" && huggingface-cli download openai/gpt-oss-20b --local-dir "$ROOT/data/models/gpt-oss-20b"
```

---

## Full setup sequence

Run in order for a fresh clone:

1. **OP-1** — venv, dependencies, hooks
2. **OP-2** — the root `.env` (then edit it to add API keys)
3. **OP-3** — the MUD's `.env`
4. **OP-5** — download the model (`run_in_background: true`, takes a while)
5. **OP-4** — build and start the MUD (`run_in_background: true`)
6. `/server` OP-3 — start the backend (`run_in_background: true`)
7. `/server` OP-5 — start the frontend (`run_in_background: true`)
8. `/server` OP-4 — wait for the model to load (`run_in_background: true`)

---

## Troubleshooting

### `make accounts` says a bot account "gets its character once the start room exists"

The server hasn't finished its first start yet. Run `make accounts` in `mud/` again once `docker logs llmri-mud-evennia` shows "Evennia Server successfully started".

### The hub, lab or simulator is missing

`make institute` in `mud/` builds them (idempotent).

### Agent auth fails after setup

The backend must be fully restarted after `.env` changes — `schemas.py` reads env vars at import time. Do `/server` OP-2 then OP-3. If the account has no character, run `make accounts` in `mud/`.
