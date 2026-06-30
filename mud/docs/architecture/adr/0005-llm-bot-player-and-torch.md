# ADR-0005: LLM as an external bot-player (torch on host), not an in-scenario NPC

- **Status:** Accepted
- **Date:** 2026-06

## Context

We want LLM-driven *characters* in Whiteout — for playtesting, for collecting
`(observation, action)` training data against the local OSS-20B torch model, and
eventually as companions. But the design forbids autonomous in-scenario NPCs
(§3.3): *the dying pilot is scripted, not an AI.* And §41 forbids the LLM from
touching deterministic state. Two further hard constraints:

- Evennia runs on a single-threaded **Twisted reactor**; a synchronous model call
  inside it blocks every player.
- The torch weights need the user's **GPU and local weights**, which live on the
  host, not in the Evennia container.

This must be reconciled with §3.3: how do we have LLM characters *and* "no
autonomous NPCs"?

## Decision

The LLM character is an **external bot-*player* harness**, not an authored NPC.

- It lives in repo-root [`agent/`](../../../agent/) and runs **on the host**
  (torch weights + GPU there), connecting to the server like any human over telnet
  port 4000. It is **not** in the Docker stack.
- **Pluggable brains** in `agent/brains/`: `TorchBrain` (local weights),
  `ClaudeBrain` (API), `ScriptedBrain` (deterministic; used for tests and the §28
  fuzzing pass).
- It is the **torch data-collection boundary**: logs `(observation, action)`
  pairs as JSONL.
- **No synchronous model inference ever runs inside the reactor.** Any server-side
  LLM seams (§41 intent-fallback, narration enrichment) are async/external and
  are **later** work than this harness (see [roadmap](../../scenarios/whiteout/roadmap.md)).

## Consequences

- **§3.3 is satisfied honestly.** There are no autonomous *NPCs*; an LLM character
  is a *player* that happens to be a model. Authored characters (the pilot) stay
  scripted.
- **§41 holds structurally.** A bot-player only sends the same commands a human
  could; it cannot invent state or bypass deterministic resolution. The
  two-stage action pipeline keeps even server-side LLM help in Stage A only —
  shaping an `ActionAttempt`, never resolving it. See
  [../llm-integration.md](../llm-integration.md).
- **The reactor stays responsive** — inference is off-process (host) or async.
- **Cost:** the host needs Python + torch + GPU + weights to run `TorchBrain`;
  `make agent` defaults to `ScriptedBrain` so the loop works without a GPU. See
  [../../guides/bot-harness.md](../../guides/bot-harness.md).
