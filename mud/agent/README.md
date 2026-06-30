# `agent/` — external bot-player harness (planned)

> **Status: stub.** Only the brain *interface* exists ([`brains/base.py`](brains/base.py)).
> The runner/client and concrete brains are **not built yet** — they come once
> there's a scenario worth playing. This README is the plan.

## What this will be
A small program that **plays the MUD as a participant**, not an authored NPC.
Design §3.3 forbids autonomous in-scenario NPCs; this sidesteps that cleanly: the
bot logs into a normal player account (`agent-1`) over telnet and issues the same
commands a human would. The deterministic engine still owns all state (design §41);
a "brain" only chooses the next command.

## Host carve-out
Unlike the MUD (which runs entirely in Docker), this harness runs **on the host** —
the whole point is the user's local **OSS-20B model weights + GPU** via **torch**,
which we keep out of the MUD container.

## Design
One interface — `Brain.act(observation: str) -> str` ([`brains/base.py`](brains/base.py)) —
with pluggable implementations to be added under `brains/`:

| Brain | Purpose |
|-------|---------|
| `ScriptedBrain` | deterministic, zero-dependency — fuzz / playtest (design §42 Pass 10) |
| `TorchBrain` | the user's OSS-20B weights via torch — **the data-collection target** |
| `ClaudeBrain` | lets Claude play the MUD, for testing |

Planned pieces:
- `client.py` — minimal telnet client (connect, `connect <user> <pass>` login, send/recv).
- `runner.py` — connect → log in → loop: observe (`look`, plus an optional structured
  observation) → `brain.act(observation)` → send → **log `(observation, action)` to
  `logs/` as JSONL** (the torch training-data capture point).
- `brains/{scripted,torch,claude}.py` — the three brains above.

Until then there's nothing to run; `make agent` will say so.
