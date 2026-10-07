# `world/llm/` — build-time authoring seams (NEVER runtime)

> **Hard rule (LOCKED): there is NO runtime LLM.** The runtime is 100% deterministic. The LLM is a
> **build-time authoring tool only** — *the LLM helps build the world; it is never in the world.* See
> [`docs/architecture/llm-integration.md`](../../../docs/architecture/llm-integration.md) and GDD §41.

This package holds the **offline, build-time** seams the authoring tools use — never anything called
during play, never anything in the Twisted reactor. Everything here runs in the workshop and its output
is **validated + human-curated + baked into data** the deterministic runtime loads.

Planned seams (build-time only):
- **ontology drafting** — draft material vectors, operation rules, cheap objects, and response/redirect
  text (the `ontology-generator` skill). Every draft is validated (content-lint + the conservation
  ledger) and curated before baking.
- **gap-filling** — the fuzzer's **wall-sensor** queue (sensible attempts with no authored rule) is
  drafted here, validated, and baked. Players never trigger generation; the engine never calls a model.

> The *other* LLM integration — an external bot that **plays** the MUD with the user's local torch model
> — lives in the repo-root [`agent/`](../../../agent/): a participant **client**, not engine code. It
> issues normal commands like a human; the engine treats it identically and stays deterministic.
