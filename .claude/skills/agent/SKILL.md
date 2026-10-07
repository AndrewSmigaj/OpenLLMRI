---
name: agent
description: Start, monitor, inspect, and troubleshoot agent scenario sessions via the backend /api/agent endpoint
---

# Agent Session Management

Run agent scenario sessions through the backend's `/api/agent` endpoint. Agent sessions play scenarios from the library (`data/scenarios/`) in the MUD tick by tick, and capture residual-stream activations at target word positions. The runner loads each scenario through the MUD's control channel (a fresh instance every time) and records the MUD's `stage_entered` / `scenario_complete` events. Results land in `data/lake/<session_id>/`.

This is the canonical reference for starting, monitoring, inspecting, stopping, and troubleshooting agent sessions. **Do not reconstruct the curl recipe from schemas.py** — use the operation blocks below verbatim.

## Prerequisites

The backend (with the model loaded) and the MUD must both be up:

1. Backend: `/server` OP-1, then OP-3 + OP-4 if it isn't loaded.
2. The MUD (`mud/`, in Docker): `make up-d` in `mud/` starts it on the ports in the root `.env` (`MUD_WS_PORT`; 14002 on the `one-mud` branch). Its log should say "Scaffold Dynamics Server".
3. Once per database, in `mud/`: `make institute` (the hub, lab and simulator) and `make accounts`, which creates the backend's agent account (`EVENNIA_AGENT_USER` / `EVENNIA_AGENT_PASS` from the root `.env`) with a character.

No build step: the MUD reads scenarios straight from the library, so an edited file is played as it is on its next load.

## Constants

| Constant | Value |
|----------|-------|
| Backend URL | `http://localhost:8000` |
| Start endpoint | `POST /api/agent/start` |
| Resume endpoint | `POST /api/agent/resume` |
| Stop endpoint | `POST /api/agent/stop` |
| Results dir | `$ROOT/data/lake/<session_id>/` |
| Tick log | `$ROOT/data/lake/<session_id>/tick_log.jsonl` |
| Probe results | `$ROOT/data/lake/<session_id>/probe_results.jsonl` |
| Session analysis | `$ROOT/data/lake/<session_id>/session_analysis.md` |
| Report (named) | `$ROOT/data/lake/reports/<date>_<session_name>_<...>.md` |
| Request schema | `backend/src/api/schemas.py:AgentStartRequest` |
| MUD websocket | `ws://localhost:$MUD_WS_PORT` (root `.env`) |
| Scenario library | `$ROOT/data/scenarios/` (format: its `README.md`) |

All commands resolve `$ROOT` and `$PY` at the top:

```bash
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
```

## Required parameters

Every `/api/agent/start` call **must** include:

- `session_name` (string) — human-readable name used in the report filename
- `scenario_id` (string) — a label the session is anchored to (e.g. the set id)
- `target_words` (list of string) — tokens whose activations to capture each tick
- `scenario_list` (list of string) — scenario **keys**, `<set_id>/<file>`, run in sequence; can be a single entry (OP-5 lists a set's keys)
- `auto_start` (bool) — **MUST be `true`** to launch the agent loop immediately. Default is `false`; omitting it will create a session record that never runs anything.

Optional: `pin_date` (YYYY-MM-DD; the date the chat template shows on every turn — today when omitted, stored with the session so a resume sends the same prompt), `system_prompt` (overrides `DEFAULT_SYSTEM_PROMPT` in `agent_loop.py`), `max_ticks` (default 5), `capture_type_config`, `evennia_username`, `evennia_password` (defaults read from the `.env` file via `load_dotenv()` in `main.py`).

---

## Operations

### OP-1: Start agent session

Replace `SMOKE_NAME`, `FIRST_SCENARIO` (a label, e.g. the set id) and `SCENARIOS` (a JSON array of keys, e.g. `["bus_stop_friend_foe_v2/bus_stop_autistic_meltdown_friend"]`). The response's `session_id` is what you use for OP-2, OP-3, and OP-4.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/agent/start -H "Content-Type: application/json" -d '{"session_name":"SMOKE_NAME","scenario_id":"FIRST_SCENARIO","target_words":["person"],"scenario_list":SCENARIOS,"auto_start":true}' | $PY -m json.tool
```

Save the returned `session_id`. If `auto_start` is omitted or `false`, the session is created but the loop never runs — a very common mistake.

### OP-1B: Resume an existing session

Add more scenarios to a session that already ran (completed or stopped). Results are appended to `probe_results.jsonl`. If the resume list includes scenarios that already have entries (e.g. retrying failures), duplicates will exist in the file. **Always run OP-1C after a resume completes** to deduplicate.

Replace `SESSION_ID` and `SCENARIOS` (a JSON array of scenario keys to run). **Do not pass `evennia_username` or `evennia_password`** — the schema defaults read from `.env`.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/agent/resume -H "Content-Type: application/json" -d '{"session_id":"SESSION_ID","scenario_list":SCENARIOS}' | $PY -m json.tool
```

Optionally pass `"system_prompt":"..."` to override the default prompt for the resumed run.

### OP-1C: Deduplicate probe results after resume

Keeps only the **last** entry per `scenario_name` — later retries replace earlier failures. Run this after a resumed session finishes.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && $PY -c "
import json
path = '$ROOT/data/lake/<session_id>/probe_results.jsonl'
lines = [json.loads(l) for l in open(path) if l.strip()]
seen = {}
for entry in lines:
    seen[entry['scenario_name']] = entry  # last wins
deduped = list(seen.values())
with open(path, 'w') as f:
    for entry in deduped:
        f.write(json.dumps(entry) + '\n')
print(f'Deduplicated: {len(lines)} entries -> {len(deduped)} unique scenarios')
"
```

### OP-2: Monitor a running session

Watch `tick_log.jsonl` grow, one line per tick:

```bash
ROOT=$(git rev-parse --show-toplevel) && tail -f "$ROOT/data/lake/<session_id>/tick_log.jsonl"
```

Or poll the result count to confirm scenarios finish (one line per completed scenario):

```bash
ROOT=$(git rev-parse --show-toplevel) && wc -l "$ROOT/data/lake/<session_id>/probe_results.jsonl"
```

Expected: `wc -l` equals `len(scenario_list)` when the session is done.

### OP-3: Inspect results

Pretty-print every probe result:

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && $PY -c "import json; [print(json.dumps(json.loads(l), indent=2)) for l in open('$ROOT/data/lake/<session_id>/probe_results.jsonl')]"
```

Human-readable per-tick summary (the file is generated at session end):

```bash
ROOT=$(git rev-parse --show-toplevel) && less "$ROOT/data/lake/<session_id>/session_analysis.md"
```

### OP-4: Stop a running session

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/agent/stop -H "Content-Type: application/json" -d '{"session_id":"<session_id>"}' | $PY -m json.tool
```

### OP-5: List a set's scenario keys

Prints the keys of a set (or of one of its named subsets) as a JSON array, ready for `scenario_list`. Replace `SET_ID` (e.g. `bus_stop_friend_foe_v2`); pass a subset name instead of `None` for a subset.

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT/backend/src" && "$ROOT/.venv/bin/python" -c "
import json
from services.agent.scenario_library import scenario_keys
print(json.dumps(scenario_keys('SET_ID', None)))
"
```

---

## Common workflows

### Smoke test a scenario set

1. Prerequisites above: backend ready, the MUD up.
2. OP-5 here for the keys, if you need a whole set or subset.
3. OP-1 here with `scenario_list` set to every key you want exercised. Use a descriptive `session_name` (e.g. `bus_stop_part3_smoke`).
4. OP-2 until `probe_results.jsonl` line count equals `len(scenario_list)`.
5. OP-3 to confirm `error: null` for every entry, and read `correct`, `outcome` and `labels` (from the MUD's `scenario_complete`).

### Single-scenario debug run

Set `scenario_list` to a one-element array with just the scenario you want to debug. Inspect `tick_log.jsonl` for the full generated text and parsed action per tick.

---

## Troubleshooting

### "Evennia login failed for 'agent': the MUD reports logged_in=…, character=…"

The runner confirms its login with the control channel's `status`. Causes, in order of likelihood:

1. **`EVENNIA_AGENT_PASS` not in backend environment.** `main.py` calls `load_dotenv(project_root/".env")` at import time (since 2026-04-11) — if this is still failing, the `.env` file is missing, in the wrong place, or missing the `EVENNIA_AGENT_PASS=...` line. Check:

   ```bash
   ROOT=$(git rev-parse --show-toplevel) && grep EVENNIA_AGENT_PASS "$ROOT/.env"
   ```

2. **Backend wasn't fully restarted after a code change.** `schemas.py` reads `os.environ.get("EVENNIA_AGENT_PASS", "")` at import time as a Pydantic field default — a `--reload` may re-import schemas.py without re-running main.py's module init. Do `/server` OP-2 then OP-3 for a full restart.

3. **The account doesn't exist in this MUD, or has no character.** Run `make accounts` in `mud/` (it gives an existing account without a character one).

4. **Orphaned MUD session holding the agent's character.** The account has one character, so a stale login blocks new logins. Fix: restart the MUD container (`docker compose restart evennia` in `mud/`).

### "read_until_prompt timed out waiting for text"

Almost always a symptom of the auth failure above — the `connect` command never produced a prompt because the password was wrong. Same fixes.

### `probe_results.jsonl` shows `"error": "scenario_not_found"` or `"load_failed"`

- `scenario_not_found`: the key isn't in the library (a typo, or a stem without its `<set_id>/`). `detail` says which part is missing; OP-5 lists the real keys.
- `load_failed`: the MUD refused the load; `detail` carries its reason, e.g. a scenario file that fails validation (the MUD names the file and the field).

### `probe_results.jsonl` shows `"error": "max_ticks_exceeded"`

The agent ran out of turns before reaching a scenario-complete action. Either the agent is struggling (look at `tick_log.jsonl` to see what it was doing) or `max_ticks` is too low for the scenario's state graph. Default is 5; set higher via the request body's `max_ticks` field.

### Session created but no `probe_results.jsonl` ever appears

You forgot `"auto_start": true`. The session exists as a record but the loop never launched. Stop/delete it, re-issue OP-1 with `auto_start: true`.

### Probe results all show `correct: false` despite obvious scenarios

Look at `session_analysis.md` tick 0 game text — if the short_desc for the NPC leaks friend/foe before the agent has a chance to examine, the agent skips the examine step and guesses from vibes. A set a finished study used is frozen, so the fix goes into a new version of the set; the next load plays the edited file. See `data/scenarios/bus_stop_friend_foe_v2/GUIDE.md` for the short_desc / examine rule.

---

## OP-6: Post-run clustering

When a session finishes (`probe_results.jsonl` line count == `len(scenario_list)`),
this skill prompts the user once for how to cluster the run. Defaults come
from the YAML block in `/cluster/SKILL.md`. Agent sessions default to
`steps=[1]` (the post-examine tick).

Print the proposed schema and prompt:

```
Session complete — <N> scenarios captured. Session: <session_id>.

Proposed clustering schema:
  save_as:           <session_name>_k6_n15
  steps:             [1]
  last_occurrence_only: true
  reduction:         UMAP, 6D, n_neighbors=15
  clustering:        hierarchical, k=6 per layer
  (covers all 4 windows × 6 transitions × {cluster, expert ranks 1/2/3})

Answer one of:
  accept                        — build the proposed schema (one /cluster OP-1 call)
  sweep <axis> <values>         — build N schemas, one per value, suffixed names
                                  e.g. sweep steps [0],[1],[0,1]
                                       sweep max_probes 50,100,200
  custom                        — prompt for each parameter (defaults in brackets)
  skip                          — exit without building
```

On `accept`: invoke `/cluster` OP-1 once with the proposed params.

On `sweep <axis> <values>`: invoke `/cluster` OP-1 N times in sequence, one per
value, with `save_as` suffixed appropriately (e.g. `_step0`, `_step1`,
`_step01`). Non-interactive after the first prompt — overnight-friendly.

On `custom`: prompt the user for each of `save_as`, `steps`,
`n_neighbors`, `reduction_dimensions`, `default_k`, showing the proposed
default in brackets. Then invoke `/cluster` OP-1 once with the resulting
params. (A schema always covers all 4 windows × 6 transitions — there is
no per-window customization.)

On `skip`: print the session id and exit.

After all builds complete, print the schema names and exit. The user can then
invoke `/analyze` manually.

---

## Important rules

- **Never start a second backend** while one is already running — will OOM the GPU (~15GB model). Always `/server` OP-2 first.
- **`auto_start: true` is mandatory** for real runs — omit it only when you specifically want to create a dormant session record.
- **Don't push commits unless explicitly asked.** Commits are fine on user request; pushes must be explicit.
- **Agent sessions are single-tenant against Evennia's `agent` account.** Do not run two sessions concurrently.
