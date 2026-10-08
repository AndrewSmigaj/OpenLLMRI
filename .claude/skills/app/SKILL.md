---
name: app
description: Steer the open app from Claude Code — show a view, build a lens through the command channel, watch the app's event stream, read the command log
---

# The app's command channel

Claude Code, Claude agents and the MUD use one small command interface (DESIGN.md E7):
`POST /api/commands` with a verb.
- **`show`** sends a view to every open app, which opens it at once (200, with how many apps heard
  it).
- **`build`** starts a lens build in the background and returns its job at once (202). Open apps
  see its progress, and see the new lens when it's done.

Every command is logged to `data/lake/_commands.jsonl`. Open apps listen on a server-sent event
stream, `GET /api/app/events`: `show`, `job` (any job's state and progress), `lens` (a lens was
built, validated, worked out, reported on, cut or saved) and `ping`.

In the MUD, the polysemy lab's `lens` command uses the same channel: `lens build` sends a `build`
command. `lens show` opens a lens in that player's own app, through the MUD's `app_command`
message rather than the stream.

## A view

A view is the app's view state; give only what differs from the defaults, `session` at least:

| Field | Meaning |
|---|---|
| `session`, `lens`, `legacy` | the capture, the lens or legacy schema, and whether it's legacy |
| `layer`, `zoom` | the first layer in view; 6, 12 or 24 steps in view |
| `color`, `color2`, `fade`, `stripes`, `gradient` | the colour axis, a second axis, the value it fades, stripes, the palette |
| `rank`, `top` | the expert chart's rank (1 to 4); expert links kept per layer (null for all) |
| `sel`, `tab` | the selection (`L12C0`, `L12C0>L13C2`, `probe:<id>`); the lower tab |
| `workspace` | `layers` (the default) or `build` |

## Operations

### OP-1: Show a view in the open apps

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/commands -H "Content-Type: application/json" -d '{"verb": "show", "by": "claude-code", "view": {"session": "SESSION_ID", "lens": "LENS", "layer": 10, "zoom": 6, "sel": "L12C0"}}' | $PY -m json.tool
```

`delivered: 0` means no app is open: start the frontend (`/server` OP-5) and open
http://localhost:5173.

### OP-2: Build a lens

`lens` takes what `POST /api/lenses` takes (`session_id`, `name`, `k` or `k_per_layer` or
`k_auto`, `n_neighbors`, `dimensions`, `filters`, ...; see `/cluster`). The reply carries the job.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/commands -H "Content-Type: application/json" -d '{"verb": "build", "by": "claude-code", "lens": {"session_id": "SESSION_ID", "name": "NAME", "k": 5, "n_neighbors": 15}}' | $PY -m json.tool
```

Follow it with `curl -s http://localhost:8000/api/jobs/JOB_ID`, then show it (OP-1).

### OP-3: Watch the event stream

What the open apps hear, for 30 seconds:

```bash
timeout 30 curl -sN http://localhost:8000/api/app/events
```

### OP-4: Read the command log

The latest commands, newest last, with their results (a job id, how many apps heard a `show`,
or the backend's refusal):

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s "http://localhost:8000/api/commands?limit=10" | $PY -m json.tool
```

## Rules

- **Commands steer every open app**, a researcher's included: say what you're about to show
  before sending it while someone is working in the app.
- **The backend only accepts browser calls from the app** (`APP_ORIGINS` in the root `.env`,
  default `http://localhost:5173`); curl and the MUD's server aren't affected.
