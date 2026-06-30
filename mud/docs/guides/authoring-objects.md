# Authoring Objects

> **⚠️ Being revised (pre-v4).** Predates the finalized architecture; some specifics (module paths,
> field names like `mass_kg` → `mass_g`, the §N tier numbering) are stale. **Authoritative:**
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) +
> [GDD](../scenarios/whiteout/GDD.md). A proper rewrite lands with roadmap P1 — use the *intent*, not
> the stale details.

How to author one in-world object, from the design §43.1 **Object Authoring
Packet** to the [`ObjectPacket`](../../game/world/sim/contracts.py) dataclass the
engine and the §44 validator consume.

> Authoring philosophy (§4, §49): **deep model, short mandatory chains.** Model
> everything plausible about the thing; require only the core authored blockers.
> Every object should be *tryable* in many ways, and every attempt should
> *resolve* (§3.5).

## The packet → dataclass mapping

The §43.1 YAML packet is rich (identity, perception, parts, states, affordances,
transformations, survival/non-survival uses, tests). It maps onto `ObjectPacket`
plus the structures it nests:

| §43.1 section | Where it lands |
|---|---|
| `identity` (id, name, aliases, category, description, scene, zone, mass) | `ObjectPacket` top-level fields |
| `parts` | `ObjectPacket.parts: list[Part]` → each `Part` has `material`, `Attachment`, `outputs_when_removed` |
| `states` (temperature, wetness, damage, contamination, ownership) | runtime `EntityState` fields (authored as starting values via `extra`) |
| `affordances` | `ObjectPacket.affordances` |
| `survival_uses` / `non_survival_uses` | `ObjectPacket.survival_uses` / `non_survival_uses` |
| `transformations` / `failure_modes` | resolved by action families + `ObjectPacket.failure_modes` |
| `tests` | `ObjectPacket.tests` |

Materials are referenced by id (`Material.id`, §21); the material's *properties*
(rigidity, cut_resistance, burnability, insulation_value, …) live in the
scenario's material table, not on the object — so "cut" resolves the same way for
anything made of that material (the §26 material tier).

## Conservation is not optional (§24)

Mass, material, temperature, wetness, contamination, damage, ownership and
**provenance** survive every transformation. When a part is removed it becomes a
**first-class object** carrying its share of those properties (§23). The authoring
job is to declare `outputs_when_removed`; the engine enforces conservation. The
validator rejects prose-only changes and objects with no material/location (§44).

## Worked mini-example

A seatbelt webbing length cut from an aircraft seat (design §25's running
example). As an `ObjectPacket`:

```python
from world.sim.contracts import ObjectPacket, Part, Attachment

seatbelt = ObjectPacket(
    id="seatbelt_03",
    name="frozen seatbelt",
    aliases=["belt", "webbing", "strap"],
    category="restraint",
    description="A stiff nylon lap belt, crusted with frost.",
    scene="wreck_cabin",
    zone="rear_seat_row",
    mass_kg=0.4,
    materials=["nylon_webbing"],
    parts=[
        Part(
            id="webbing_length",
            material="nylon_webbing",
            attachment=Attachment(
                method="stitched_buckle",
                strength=0.7,
                accessible=True,
                required_tool_quality=0.3,      # a pocketknife qualifies, slowly
                removable_by=["cut", "saw", "tear"],
                failure_modes=["fibers_fray", "knife_slips"],
            ),
            outputs_when_removed=["nylon_webbing_length"],   # a new first-class object
        ),
    ],
    affordances=["examine", "cut", "saw", "tear", "tie", "wrap", "pull"],
    survival_uses=["lashing for a splint", "securing a shelter tarp"],
    non_survival_uses=["something to fidget with", "a makeshift belt"],
    failure_modes=["frozen webbing resists tearing by hand"],
    tests=[
        "Can cut nylon webbing with a pocketknife, but slowly.",
        "Frozen webbing is harder to tear than warm webbing.",
        "Cutting the webbing yields a nylon_webbing_length (mass conserved).",
    ],
)
```

What the engine does with it:

- **Cut/saw/tear** resolve through the §26 tiers — here mostly the **material**
  tier (`nylon_webbing`'s `cut_resistance` + the tool's quality decide *how
  slowly*), unless an object/part rule overrides.
- Success emits an `Effect(kind="remove_part", payload={"part_id": "webbing_length"})`
  plus a `create_object` for `nylon_webbing_length`; conservation moves mass and
  provenance across (§24).
- The new object is itself authorable/tryable: it has its own affordances and
  survival uses (it can lash a splint — §35).

## Authoring checklist

- [ ] `id`, `name`, `category`, `scene`, `zone`, `mass_kg`, `materials` set
      (validator: every object needs material + location).
- [ ] Every part declares `material`, an `Attachment` (`removable_by`,
      `required_tool_quality`, `failure_modes`) and `outputs_when_removed`.
- [ ] Derived outputs have `survival_uses` **or** explicit `non_survival_uses`
      (validator: every derived object has capabilities or explicit non-uses).
- [ ] At least one **silly / non-survival** use exists for a major object (§44).
- [ ] `tests` include success, failure, conservation, silly and perception cases
      (§43.1 / §45). Survival-critical objects **must** have tests.

## Related

- [authoring-actions.md](authoring-actions.md) — the verbs that act on objects.
- [validation-rules.md](validation-rules.md) — the §44 gate that lints packets.
- [../architecture/overview.md](../architecture/overview.md) — Effects/conservation flow.
