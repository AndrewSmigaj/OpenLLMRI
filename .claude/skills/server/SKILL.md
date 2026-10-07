---
name: server
description: Start, stop, and check status of the backend (FastAPI + model), the frontend and the MUD (Evennia 6 in Docker)
---

# Server Management

Manage the Open LLMRI servers.

**Three pieces:** the backend (FastAPI + the model, on the host's GPU), the frontend (Vite), and the MUD (Evennia 6 + Postgres in Docker, `mud/`, run through its `make` targets). Stop All and Restart All cover all three.

All commands use `$ROOT` as the project root (the git repo root). Resolve it once at the start of any operation:

```bash
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
```

## Constants

| Constant | Value |
|----------|-------|
| Backend working dir | `$ROOT/backend/src` |
| MUD folder (its `make` targets) | `$ROOT/mud` |
| Backend URL | `http://localhost:8000` |
| Frontend URL | `http://localhost:5173` |
| MUD WebSocket | `ws://localhost:4002` (`MUD_WS_PORT` in the root `.env`) |
| Health endpoint | `http://localhost:8000/health` |
| Host binding | `0.0.0.0` (required for WSL2) |

**NEVER use bare `python3`** — always use `$PY`.
**The MUD runs only through `make` in `mud/`** — never `docker compose down -v` (it deletes the MUD's database).

---

## Operations

Each operation below is a single self-contained block. Copy the EXACT block — do not improvise or compose steps from multiple blocks.

### OP-1: Check Status

Run this FIRST before any other operation to understand current state.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && echo "=== Processes ===" && ps aux | grep -E "uvicorn|vite" | grep -v grep || echo "(none running)" && echo "=== Ports ===" && (fuser 8000/tcp 2>/dev/null && echo "8000: IN USE" || echo "8000: free") && (fuser 5173/tcp 2>/dev/null && echo "5173: IN USE" || echo "5173: free") && (ss -ltn | grep -q ":4002 " && echo "4002: IN USE" || echo "4002: free") && echo "=== Backend Health ===" && curl -s --max-time 3 http://localhost:8000/health 2>/dev/null | $PY -c "import json,sys; d=json.load(sys.stdin); s=d.get('loading',{}).get('stage','?'); e=d.get('loading',{}).get('elapsed_seconds'); print(f'Model loaded — ready' if d.get('model_loaded') else f'Stage: {s} ({e}s elapsed)' if e else f'Stage: {s}')" 2>/dev/null || echo "Not responding" && echo "=== Frontend ===" && (curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:5173 2>/dev/null || echo "Not responding") && echo "" && echo "=== MUD ===" && (docker ps --filter name=llmri-mud --format '{{.Names}}: {{.Status}}' | grep . || echo "MUD containers not running")
```

### OP-2: Stop All

Use `fuser -k` (kills by port) — this is reliable on WSL2. `pkill` is NOT reliable here. The MUD stops through `make down` in `mud/` (containers only; its database volume stays).

```bash
ROOT=$(git rev-parse --show-toplevel) && fuser -k 8000/tcp 2>/dev/null; fuser -k 5173/tcp 2>/dev/null; make -s -C "$ROOT/mud" down 2>/dev/null; sleep 2 && echo "=== Verify ===" && (fuser 8000/tcp 2>/dev/null && echo "8000: STILL IN USE" || echo "8000: free") && (fuser 5173/tcp 2>/dev/null && echo "5173: STILL IN USE" || echo "5173: free") && (ss -ltn | grep -q ":4002 " && echo "4002: STILL IN USE" || echo "4002: free")
```

If 8000 or 5173 shows "STILL IN USE" after this, run `fuser -k -9 <port>/tcp` (SIGKILL). The MUD's ports are checked with `ss`: Docker publishes them through a root process that `fuser` can't see; if 4002 stays in use, `docker ps` shows what holds it.

### OP-3: Start Backend — FastAPI (background)

**Prerequisite**: Port 8000 must be free (run OP-2 first if needed). Agent runs also need the MUD (OP-6); sentence captures and analysis don't.

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT/backend/src" && "$ROOT/.venv/bin/python" -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Run with `run_in_background: true`.

**Do NOT add `--reload`.** The WatchFiles reloader interacts badly with the model-load thread on WSL2 — the worker can bind the port but leave the event loop wedged, so connections hang even though the process looks healthy. After any code change, do a full restart (OP-2 → OP-3 + OP-5 + OP-6 → OP-4). No shortcuts.

### OP-4: Wait for Model

**Run AFTER OP-3.** Must use `run_in_background: true` — takes ~2-3 minutes.

The health endpoint now reports loading stage in real time (the API serves immediately while model loads in background). No need to read log files.

```bash
PY=$(git rev-parse --show-toplevel)/.venv/bin/python; for i in $(seq 1 60); do H=$(curl -s --max-time 3 http://localhost:8000/health 2>/dev/null); if [ -z "$H" ]; then echo "[$i] Waiting for API..."; sleep 5; continue; fi; STAGE=$(echo "$H" | $PY -c "import json,sys; print(json.load(sys.stdin).get('loading',{}).get('stage','unknown'))"); ELAPSED=$(echo "$H" | $PY -c "import json,sys; print(json.load(sys.stdin).get('loading',{}).get('elapsed_seconds','?'))"); if [ "$STAGE" = "ready" ]; then echo "READY — model loaded in ${ELAPSED}s"; exit 0; fi; if [ "$STAGE" = "failed" ]; then echo "FAILED — check backend logs"; exit 1; fi; echo "[$i] Stage: $STAGE (${ELAPSED}s elapsed)"; sleep 5; done; echo "TIMEOUT — model did not load in 5 minutes"
```

**Expected output:**
```
[1] Waiting for API...
[2] Stage: initializing (3.2s elapsed)
[3] Stage: loading_model (8.1s elapsed)
...
[24] Stage: loading_model (118.5s elapsed)
[25] Stage: creating_service (121.0s elapsed)
[26] READY — model loaded in 123.4s
```

**Stages**: `not_started → initializing → loading_model → creating_service → ready | failed`

### OP-5: Start Frontend (background)

**Prerequisite**: Port 5173 must be free.

```bash
cd $(git rev-parse --show-toplevel)/frontend && npm run dev
```

Run with `run_in_background: true`. Vite uses `strictPort: true` — will error if 5173 is taken.

### OP-6: Start the MUD

**Prerequisite**: the MUD is stopped (OP-2), and ports 4000–4002 are free. It runs in Docker on the ports in the root `.env`; first-time setup (image, database, accounts) is `/setup` OP-4.

```bash
ROOT=$(git rev-parse --show-toplevel) && T=$(date -u +%Y-%m-%dT%H:%M:%SZ) && make -s -C "$ROOT/mud" up-d && for i in $(seq 1 60); do docker logs --since "$T" llmri-mud-evennia 2>&1 | grep -q "Evennia Server successfully started" && break; sleep 2; done && docker logs --since "$T" llmri-mud-evennia 2>&1 | grep -E "Server [0-9]|successfully started|Traceback" | head -5
```

Expected: `Scaffold Dynamics Server 6.0.0` and `Evennia Server successfully started.` — the server's name confirms which MUD answered.

---

## Common Workflows

### Deploy Code Changes (MANDATORY after any backend edit)

After editing ANY backend `.py` file, ALWAYS run this full sequence. Never rely on `--reload` or partial restarts — WSL2 inotify is unreliable and partial restarts cause orphaned sessions.

1. Run **OP-2** (stop all) — wait for all ports to show "free"
2. Run **OP-3** + **OP-5** + **OP-6** in parallel (start backend, frontend, the MUD)
3. Run **OP-4** (wait for model) — do NOT start agent sessions until this shows "READY"

This is the ONLY way to deploy changes. No shortcuts.

### Restart All

Same as Deploy Code Changes above — this is the typical workflow.

1. Run **OP-2** (stop all)
2. Verify all ports show "free"
3. Run **OP-3** + **OP-5** in parallel (`run_in_background: true` for both), and **OP-6** (the MUD; it waits for its own start)
4. Run **OP-4** (wait for model, `run_in_background: true`)
5. When OP-4 completes with "READY", backend is fully operational

### Start From Scratch

1. Run **OP-1** to assess current state
2. If anything is running, run **OP-2**
3. Follow steps 3-7 from "Restart All" above

### Frontend-Only Restart

Only needed if Vite HMR stops working (rare).

```bash
fuser -k 5173/tcp 2>/dev/null; sleep 1; cd $(git rev-parse --show-toplevel)/frontend && npm run dev
```

Run with `run_in_background: true`.

---

## When to Restart

| Change made | Action needed |
|-------------|---------------|
| Frontend `.tsx`/`.ts` edit only | None — Vite HMR handles it |
| Scenario files (`data/scenarios/**`) | None — the MUD reads a scenario's file each time it loads it |
| MUD code (`mud/game/**`) | `make restart` in `mud/` — the container restarts and reads the code (mounted); clients reconnect |
| **Any backend code change** | **ALWAYS full restart: OP-2 → OP-3 + OP-5 + OP-6 → OP-4** |

**No exceptions for the backend.** Never rely on `--reload`. Never do partial restarts. The 2-minute model load is nothing compared to debugging a half-started state.

## Important Rules

- **Never** start a second backend — will OOM the GPU (~15GB model)
- **Always** stop before start — even if you think nothing is running
- **Use `fuser -k`** to stop, not `pkill` — `pkill` is unreliable on WSL2
- **Wait** for `model_loaded: true` before making API calls that need the model
- Experiment/analysis endpoints work WITHOUT the model (they read from disk)
- Backend must bind to `0.0.0.0` (not `127.0.0.1`) for WSL2 networking
- **NEVER use bare `python3`** — always use `$PY` (venv path)
