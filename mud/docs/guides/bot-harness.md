# Bot Harness

How to run the `agent/` bot-**player** — the external LLM harness that connects to
the running MUD like a human and (optionally) logs `(observation, action)` data
for the torch model. This is LLM integration **point 1**
([../architecture/llm-integration.md](../architecture/llm-integration.md);
[ADR-0005](../architecture/adr/0005-llm-bot-player-and-torch.md)).

> The bot is **not** an in-scenario NPC (§3.3). It is a *player* driven by a
> brain. It runs on the **host** (where the torch weights + GPU live), never in
> the Evennia container. It can only send the same commands a human could, so it
> cannot bypass deterministic resolution (§41).

## Run it

With the server up (`make up` / `make up-d`) and the bot account created
(`make accounts`):

```
make agent
# -> python agent/runner.py --brain scripted --host localhost --port 4000
```

`make agent` defaults to the **scripted** brain so it works with no GPU. To use
the local model, run the torch brain directly (needs your weights + GPU on the
host):

```
python agent/runner.py --brain torch   --host localhost --port 4000
python agent/runner.py --brain claude  --host localhost --port 4000
```

It logs in as the bot account (`AGENT_ACCOUNT` from `.env`, created by
[`scripts/bootstrap_accounts.py`](../../scripts/bootstrap_accounts.py)).

## The brain abstraction

A **brain** maps an observation to an action string. The harness is
brain-agnostic; swap with `--brain`:

| Brain | What it does | Needs |
|---|---|---|
| `ScriptedBrain` | deterministic policy / fixed sequences | nothing — default; used in tests & the §28 fuzzing pass |
| `TorchBrain` | local OSS-20B weights | host GPU + weights |
| `ClaudeBrain` | Claude API | API access |

Brains live in [`agent/brains/`](../../agent/brains/). The loop each turn:
**observe → brain.act(observation) → send command → read result → log**.

## Observations: structured `@OBS` + prose fallback

The bot prefers a **structured observation** but degrades gracefully:

- If the server emits an optional structured line — `@OBS <json>` — the brain
  parses the JSON directly (zones, visible/audible/reachable entities, banded
  perception, world clock). This is the clean machine-readable channel.
- If no `@OBS` is present, the bot falls back to issuing **`look`** and parsing the
  human prose appearance. Every brain must handle the prose path, since `@OBS` is
  optional and may be absent in early builds.

This mirrors the perception model: what the bot can observe is exactly what a
human sees from its zone, banded by [perception](../architecture/perception-model.md).

## Data logging

The harness writes the trajectory as **JSONL**, one `(observation, action)` pair
per line — the torch data-collection boundary. This is the corpus for later
training/analysis of `TorchBrain`. Logging is independent of which brain produced
the action, so a `ScriptedBrain` run is still usable data.

## Where it fits

- It is **external**: no synchronous inference ever runs in Evennia's reactor.
- There is **no runtime LLM** — the LLM is a build-time authoring tool only
  ([../architecture/llm-integration.md](../architecture/llm-integration.md)). This harness is a
  *client* (an AI that plays the MUD like a human); its `ScriptedBrain` drives the solvability fuzz
  (roadmap P2 — [roadmap](../scenarios/whiteout/roadmap.md)).

## Related

- [../architecture/adr/0005-llm-bot-player-and-torch.md](../architecture/adr/0005-llm-bot-player-and-torch.md)
- [docker-workflow.md](docker-workflow.md) — get the server + accounts up first.
