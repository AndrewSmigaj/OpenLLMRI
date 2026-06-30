# LLM Integration

Where a language model touches Whiteout — and, decisively, where it does **not**.

> **The rule (GDD §3.2 / §41).** **Runtime is fully deterministic. The LLM is a build-time authoring
> tool only and is NEVER called during play.** All interactions are pre-built. The engine never invents
> state, decides survival math, or interprets input with a model at runtime. *The LLM helps build the
> world; it is never in the world.*

## The one and only LLM use: build-time authoring (offline)
In the workshop, before anyone plays, the LLM **assists authoring** — it drafts material property
vectors, operation rules, cheap objects, and response/redirect text. Every draft is then **validated**
(content-lint + the conservation ledger) and **human-curated**, and **baked into data** the runtime
loads. See `docs/investigation/claude-code-build-practices.md` and the `ontology-generator` skill.

- The authored content is *static data + deterministic rules* by the time the game runs.
- Gaps (sensible attempts with no authored rule, found by the fuzzer's **wall-sensor**) are filled the
  same way — at build time — never by a runtime model call.

## Runtime: 100% deterministic (no LLM)
| Runtime stage | How it works | LLM? |
|---|---|---|
| Parse input | deterministic parser: the taught grammar `VERB X [RELATION Y] [WITH Z]` + synonym tables → `ActionAttempt{verb,X,relation,Y,tool}` | **no** |
| Resolve | the §26 tiers over pre-built operation×material rules → `ActionResult` | **no** |
| "Soft" judgements (windbreak ≥ 0.5? morale shift?) | **pre-authored thresholds/rules**, evaluated deterministically | **no** |
| Narrate | pre-written templates filled from real post-Effect state | **no** |
| Unanticipated attempt | pre-written generic redirect + log to the wall-sensor for devs | **no** |

There is no synchronous-inference-in-the-reactor concern at runtime because **there is no runtime
inference at all.**

## Orthogonal: the `agent/` bot-player (a client, not the engine)
Separately from the engine, an external **bot-player** can connect over telnet as a normal player and
issue normal commands ([ADR-0005](adr/0005-llm-bot-player-and-torch.md)). It runs **on the host** with
the user's OSS-20B torch weights; pluggable brains in `agent/brains/` (`ScriptedBrain` deterministic
for the fuzzer, `TorchBrain`, `ClaudeBrain`). This is a **build/test/demo client** — an AI that *plays*
the game like a human. It does **not** run game logic, sits entirely outside the engine, and does not
affect engine determinism. The engine treats its input identically to a human's. It is also the torch
`(observation, action)` data-collection boundary.

## The two-stage pipeline (both stages deterministic)
```
   free text
      │  Stage A — PARSE (deterministic: format + synonyms)
      ▼
  ActionAttempt
      │  Stage B — RESOLVE (deterministic: §26 tiers over pre-built rules; NO LLM)
      ▼
  ActionResult  (Effects + Events + narration from templates)
```
The §26 tiers are **authored → object → part → material → generic physics → informative redirect**.
(The original design's "LLM interpretation" tier is removed — there is no runtime LLM.)

## Related
- [overview.md](overview.md) · [implementation-architecture.md](implementation-architecture.md) (the full how)
- [ADR-0005](adr/0005-llm-bot-player-and-torch.md) — the bot-player decision.
- `docs/investigation/claude-code-build-practices.md` — the build-time authoring loop.
