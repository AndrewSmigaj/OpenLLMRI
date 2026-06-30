# Validation Rules

The design §44 validation checklist, as an actionable gate. It runs as
**content-lint** over authored scenario content — **not at runtime** — via
`make validate` (and `make verify`).

> Validation is a *gate on content*, not a game system. It catches authoring
> mistakes (an unsolvable goal, a prose-only state change, a missing test) before
> they ship. The deterministic engine still enforces conservation etc. at run
> time; the validator makes sure the *authored data* is well-formed.

## How it runs

```
make validate SCENARIO=<name>   # python -m world.sim.validation.validators <name>
make verify   SCENARIO=<name>   # compose config check + make test + make validate
```

It loads the scenario's authored packets ([`ObjectPacket`](../../game/world/sim/contracts.py),
`ActionFamilyPacket`, `WorkflowPacket`) and lints them with pure checks in
`world/sim/validation/**` — no DB, no Evennia boot. It is the same gate the §28
`/verify` step and the agentic [loop](loop-workflow.md) run every iteration, and
it belongs in CI.

## The checklist (§44)

Each item below is a check the validator performs. Grouped for skimming.

**State integrity**
- [ ] No prose-only state changes (if narration says it happened, an `Effect` did).
- [ ] Conservation rules are followed (mass/material/temp/wetness/contamination/
      ownership/provenance preserved across transforms — §24).
- [ ] Every generated object has a **material** and a **location**.
- [ ] Every derived object has **capabilities or explicit non-uses**.

**Solvability (the multiplicity rules)**
- [ ] Critical goals have **≥ 3 solution paths**.
- [ ] Critical hidden facts have **≥ 3 clue paths**.
- [ ] Critical repairs include **inspect / access / diagnose / repair / test** stages.
- [ ] Multiple rescue routes are possible (no single perfect path — §39).

**Time & actions (§9)**
- [ ] Long actions never jump global time.
- [ ] Every timed action has **tick feedback**.
- [ ] Every timed action can be **interrupted** or is explicitly marked uninterruptible.
- [ ] Every important action has **failure feedback** (never "you can't do that").

**Perception (§10–15)**
- [ ] Perception routing exists for major activity messages.
- [ ] Distant objects cannot be manipulated unless a ranged action supports it.
- [ ] Weather changes visibility and audibility.
- [ ] `look` descriptions use **relative direction** for visible distant features.
- [ ] Speaking, calling and shouting have **different** propagation rules.

**Coverage**
- [ ] Survival-critical objects have **tests**.
- [ ] **Silly / non-survival** interactions exist for major objects.

**Authored-content specifics**
- [ ] Radio has **one authored damage state**, not procedural variants (§38).
- [ ] Radio success is **not** instant rescue (§38.7).

**LLM guardrail**
- [ ] LLM-generated rules cannot override core physics without approval (§41).

## Fixing failures

| Failure | Fix | Guide |
|---|---|---|
| object missing material/location | set `materials` + `scene`/`zone` | [authoring-objects.md](authoring-objects.md) |
| derived object has no uses | add `survival_uses` or explicit `non_survival_uses` | [authoring-objects.md](authoring-objects.md) |
| goal has < 3 paths / clues | add `alternate_paths` / `clue_paths` | [authoring-workflows.md](authoring-workflows.md) |
| timed action lacks tick feedback / interrupt | set `duration_model` + partial states | [authoring-actions.md](authoring-actions.md) |
| no silly interaction | add a `non_survival_uses` entry + test | [authoring-objects.md](authoring-objects.md) |

## Related

- [authoring-objects.md](authoring-objects.md) · [authoring-actions.md](authoring-actions.md) · [authoring-workflows.md](authoring-workflows.md)
- [../architecture/testing.md](../architecture/testing.md) — validation vs the test tiers.
- [loop-workflow.md](loop-workflow.md) — `make verify` in the agentic loop.
