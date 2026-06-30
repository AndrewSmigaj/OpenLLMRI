# Authoring Workflows

How to author a **goal-level workflow** — a survival objective with *multiple*
clue and solution paths, not a single recipe. Design §30 / §43.3 →
[`WorkflowPacket`](../../game/world/sim/contracts.py).

> Binding principle (§30, §49): **important goals are workflows, not recipes.**
> Whiteout is not "a giant list of magical object pairs." A goal exposes many
> routes; the simulation decides which the player's actions actually satisfy.

## What a workflow is

A `WorkflowPacket` describes a goal (e.g. *escape seat restraint*, *make safe
water*, *repair radio*, *survive first night*) in terms of:

| §43.3 field | `WorkflowPacket` field | Meaning |
|---|---|---|
| `goal`, `why_it_matters` | `goal` | the objective |
| `success_conditions` | `success_conditions` | world states that count as solved |
| `failure_conditions` | `failure_conditions` | states that count as lost |
| `stages` | `stages` | inspect / access / diagnose / repair / test phases (for repairs) |
| `alternate_paths` | `alternate_paths` | ≥3 distinct ways to reach success |
| `clue_paths` | `clue_paths` | ≥3 ways to *learn* each hidden fact |
| `partial_success_states` | `partial_success_states` | interrupted/incomplete still useful |
| `validation_tests` | `tests` | the §44/§45 checks |

A workflow does **not** hard-script a sequence. It declares the *conditions* and
the *paths*; the deterministic systems (fire, water, warmth, rescue) and action
families decide, from real state, whether a given path was satisfied.

## The §44 multiplicity requirement

The validator enforces solvability redundancy (design §44; see
[validation-rules.md](validation-rules.md)):

- **≥ 3 solution paths** for every *critical* goal — no single object may be
  required for all endings.
- **≥ 3 clue paths** for every *critical hidden fact* — the player can discover
  it more than one way.
- **Critical repairs** must include **inspect → access → diagnose → repair →
  test** stages.

This is what makes the pilot able to die before giving every clue *without*
softlocking the scenario (§19), and rescue reachable through overlapping
confidence rather than one perfect path (§39).

## Worked sketch: the radio workflow (§38)

The authored radio (§38) is the canonical multi-path goal. As a `WorkflowPacket`:

```python
from world.sim.contracts import WorkflowPacket

repair_radio = WorkflowPacket(
    id="repair_radio",
    goal="Get a useful transmission out on the cockpit radio.",
    success_conditions=[
        "radio has power",
        "radio has a working-enough antenna",
        "a transmission with usable location info was sent",
    ],
    failure_conditions=["radio destroyed", "battery fully drained with no contact"],
    stages=["inspect", "access", "diagnose", "repair", "test"],   # critical repair
    alternate_paths=[
        "restore cockpit battery power -> improvise a metal antenna -> weak contact",
        "scavenge a long metal object as antenna -> partial signal fragments",
        "radio fragments + pilot's route clue -> enough location info for rescue",
    ],
    clue_paths=[
        "inspecting the outside of the plane reveals the broken antenna mount",
        "static-but-powered radio implies the antenna, not the power, is the fault",
        "the pilot (if tended) names the ridge, giving usable location info",
    ],
    partial_success_states=[
        "powered but static (no antenna)",
        "weak signal, garbled fragments",
        "useful contact but rescue still pending (not instant)",
    ],
    tests=[
        "Radio has no power before power is restored.",
        "Radio with power but no antenna produces mostly static.",
        "Broken antenna is discoverable by inspecting the outside of the plane.",
        "A better antenna improves signal clarity.",
        "Useful contact increases rescue confidence but does not instantly win.",
    ],
)
```

Note the design rules baked in: the radio has **one authored damage state**, not
procedural variants (§38, §44); radio success is **not** instant rescue (§38.7);
and it is only *one* of several rescue routes (beacon, visual signal, travel —
§39).

## Authoring checklist

- [ ] Goal is stated as **conditions**, not a fixed verb sequence.
- [ ] **≥ 3** `alternate_paths`; no single object gates all of them.
- [ ] **≥ 3** `clue_paths` per hidden fact the goal depends on.
- [ ] Critical repairs carry inspect/access/diagnose/repair/test `stages`.
- [ ] `partial_success_states` make interrupted/partial progress useful (§9.5).
- [ ] `tests` cover each path, each clue, and the partial states (§45).
- [ ] Cross-checked against rescue overlap (§39) so the scenario can't softlock.

## Related

- [authoring-actions.md](authoring-actions.md) — the verbs paths are built from.
- [validation-rules.md](validation-rules.md) — the §44 multiplicity gate.
- [adding-a-scenario.md](adding-a-scenario.md) — where workflows live in a scenario.
