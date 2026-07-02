# Authoring Action Families

How to add a new **action family** — the generic verbs (`cut`, `examine`, `say`,
`tie`, `burn`, …) that resolve over *any* object by its parts and materials.
Design §27 / §43.2 → the [`ActionFamilyPacket`](../../game/world/sim/contracts.py)
dataclass.

> **⚠️ Being revised (pre-v4).** This guide predates the finalized architecture and still uses the old
> module names (`actions/families/`), the old `ActionAttempt` shape, and a 6-tier ladder. **Authoritative:**
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) —
> DR-08 taught grammar → `ActionAttempt{verb,X,relation,Y,tool}`; DR-09 tiers
> authored→object→**operation×material**→generic→redirect; operations live in `world/sim/operations` +
> `world/sim/resolver`, **not** `actions/`. A proper rewrite lands with roadmap P1 — use the *intent*
> below, not the stale specifics.

> The whole point (§2, §26): the player survives by **understanding the world**,
> not by guessing the author's verb-object pair. A family encodes *how a verb
> interacts with materials and parts*, so one `cut` cuts fabric, webbing and foam
> differently without per-object scripting.

## Two stages, and where a family lives

Actions are **two-stage** (fixes design §26):

- **Stage A — the Evennia command shell.** Parses the **taught grammar**
  `VERB X [RELATION Y] [WITH Z]` (GDD §25a) into a structured
  [`ActionAttempt`](../../game/world/sim/contracts.py) `{actor, verb, X, relation, Y, tool, raw}`.
  **No runtime LLM** — unknown phrasing yields a help nudge that teaches the format (DR-02/DR-08).
- **Stage B — the pure resolver** in
  [`world/sim/actions`](../../game/world/sim/). Resolves the `ActionAttempt`
  deterministically and returns an `ActionResult`.

**An action family is Stage-B content.** It lives in
`world/sim/actions/families/<id>.py` as a pure function over the contract
dataclasses, next to the worked **examine / cut / say** examples. The LLM is
*never* in Stage B ([../architecture/llm-integration.md](../architecture/llm-integration.md)).

## The §26 resolution tiers

Stage B resolves through this priority ladder (the `Resolution` enum — note the
LLM tier from §26 is pulled out into Stage A and is **absent** here):

1. **AUTHORED** — a scenario-authored puzzle rule (e.g. the radio's one authored
   damage state).
2. **OBJECT** — an object-specific rule.
3. **PART** — a part-specific rule.
4. **MATERIAL** — the material's properties decide it (most `cut`/`tear`/`burn`
   outcomes; §21).
5. **PHYSICS** — generic physics fallback.
6. **FAILURE** — a *plausible failure with explanation*. Never "You can't do
   that" (§3.5, §49): a desperate or silly attempt still gets a real physical
   answer.

A family walks the ladder and stops at the first tier that resolves; the result
records *which* tier fired.

## The packet → dataclass mapping (§43.2)

| §43.2 field | `ActionFamilyPacket` field | Notes |
|---|---|---|
| `id`, `synonyms` | `id`, `synonyms` | synonyms feed Stage-A parsing |
| `required_roles` / `optional_roles` | same | e.g. `cut` requires `target`, optional `tool` |
| `physical_checks` | `physical_checks` | reachability, tool quality vs material |
| `duration_model` / `stamina_model` | same | feeds the scheduler (§9; tick feedback) |
| `partial_success_states` | `partial_success_states` | interrupted work stays partial |
| `failure_modes` | `failure_modes` | the explanations the FAILURE tier draws on |
| `tests` | `tests` | success / failure / conservation / silly cases |

## How to add a family

1. **Brainstorm first (§28).** List obvious, clever, desperate and silly attempts
   for the verb against the major objects it touches. This drives the test list.
2. **Author the packet.** Fill an `ActionFamilyPacket` (id, synonyms, roles,
   physical/stamina/duration models, partial/failure states, tests).
3. **Register synonyms in Stage A** so the command shell can route phrasings into
   one `ActionAttempt` with `action == <id>`.
4. **Write the resolver** in `world/sim/actions/families/<id>.py`: a pure function
   `(ActionAttempt, world snapshot) -> ActionResult`. Walk the §26 tiers; return
   `Effect`s (never prose-only — §44), `Event`s (with loudness for perception
   routing), deterministic `narration`, and `duration_minutes` for timed work.
5. **Test in Tier 1** (`make test`) — no DB, no Evennia boot
   ([../architecture/testing.md](../architecture/testing.md)).

## Worked sketch: `cut`

```python
# world/sim/actions/families/cut.py  (pure; no Evennia imports)
from world.sim.contracts import ActionAttempt, ActionResult, Resolution
from world.sim import effects

def resolve_cut(attempt: ActionAttempt, world) -> ActionResult:
    target = world.entity(attempt.target)
    tool = world.entity(attempt.tool) if attempt.tool else None

    # 1-3: authored / object / part overrides checked first (omitted) ...
    # 4: MATERIAL tier — the general case.
    material = world.material_of(target)
    tool_q = world.tool_cut_quality(tool)             # 0 = bare hands
    if tool_q < material.cut_resistance - 0.1:
        return ActionResult(
            success=False, resolution=Resolution.MATERIAL,
            narration=f"The {tool or 'edge'} skates off the {target.display_name}; "
                      "it barely scratches the surface.",
        )
    minutes = world.cut_minutes(material, tool_q)      # nylon webbing: slow
    part = world.severable_part(target)
    return ActionResult(
        success=True, resolution=Resolution.MATERIAL,
        narration=f"You work the blade through the {target.display_name}.",
        effects=[
            effects.remove_part(target.id, part.id),
            effects.create_object(part.outputs_when_removed[0]),  # conserves mass (§24)
        ],
        events=[...],            # loudness drives perception routing (§14)
        duration_minutes=minutes, partial=True,        # schedules onto ticks (§9)
    )
```

The same function cuts fabric, webbing and foam differently because the
*material* differs — roadmap Pass 4's acceptance test. No per-object cut code.

## Naming & narration rules (slice-fix, 2026-07)

- **Derived template ids compose material-first**: `{material_id}_{fragment_word}` (`glass_shard`,
  `synthetic_fabric_strip`) — the shell derives the display key via `replace("_", " ")`, so the
  order IS the player-facing name ("glass shard", never "shard glass"). Authored
  `outputs_when_removed` ids follow the same reads-naturally rule (`loose_fabric` → "loose fabric").
- **`{tool}` arrives pre-articled** via `_helpers.tool_phrase()` — "the multitool" / "your bare
  hands". Templates must never write an article before `{tool}`, never start a sentence with it,
  and any verb governed by `{tool}` must be number-invariant (modals: *won't*, *can't*) — "your
  bare hands" is plural.

## Related

- [authoring-objects.md](authoring-objects.md) — the materials/parts `cut` reads.
- [authoring-workflows.md](authoring-workflows.md) — chaining actions into goals.
- [validation-rules.md](validation-rules.md) — failure-feedback & tick rules (§44).
