# Authoring Objects

> Rewritten 2026-09-07 for the closure loop (DR-26 / DR-17a). Objects are **rows in a table**, not
> packets. Authoritative: [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md) +
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md).

## The idea (GDD §21, §43)
**Objects are cheap.** An object is a parts-list made of materials with a mass; its *behaviour* comes from
the shared operations over those materials and from the capabilities its material × form derive. You
never write per-object verb code. The heavy authoring goes into materials (`materials/table.py`),
forms and capabilities (engine), prose (`appearance.py`), and — for the handful of puzzle-critical
objects — an authored rule in `authored.py` (the tier-1 seam).

## Where an object lives
`game/world/scenarios/<scenario>/objects.py` → `OBJECT_TABLE: list[dict]`. The loader (`build.py`) walks
the table twice (parents first) and creates the Evennia objects; the pure world (`PureWorld.from_table`)
loads the **same rows** for probes and fuzz, so the two can never drift.

## A row
```python
{
    "sim_id": "seat",                    # logical id (DR-12): stable, never a dbref
    "name": "aircraft seat",             # the display key; the player's noun
    "aliases": ["seat"],                 # extra nouns the parser matches
    "materials": ["steel"],              # primary material first (the body)
    "mass_g": 5000,                      # BODY mass in integer grams, excluding parts (DR-11)
    "zone": "mid_cabin",                 # OR "in": "<parent sim_id>" for stowed things (DR-24)
    "state": {"ident": "11B", "fixed": True},
    "parts": [
        {"id": "cover", "label": "cover", "material": "synthetic_fabric", "mass_g": 200,
         "attachment": "stitched", "outputs_when_removed": ["loose_fabric"]},
        {"id": "cushion", "label": "cushion", "material": "foam", "mass_g": 800,
         "attachment": "clipped", "outputs_when_removed": ["loose_foam"]},
        {"id": "bolt", "label": "bolt", "material": "steel", "mass_g": 30, "attachment": "bolted"},
    ],
}
{"sim_id": "chocolate", "name": "chocolate bar", "aliases": ["chocolate", "bar", "ration"],
 "materials": ["chocolate"], "mass_g": 100, "in": "seatpocket"}     # found by searching the seat
```

### Fields
| field | meaning |
|---|---|
| `sim_id` | unique logical id; derived objects get `derived_id(parent, tag)` ids automatically |
| `name`, `aliases` | what the parser matches (whole phrase, any alias, or a single word of the name) |
| `materials` | material ids from the table; the first is the body's material |
| `mass_g` | integer grams for the body; each part carries its own `mass_g`; the ledger sums them |
| `zone` / `in` | exactly one: placed in a zone, or stowed inside a parent (the parent's zone chains) |
| `state` | the payload the engine reads: `ident`, `fixed`, `container`, `open`, `sealed`, `jammed`, `wet`, `lit`, `ignition`, `powered`, `worn_by`, `form`, and **authored capabilities** (`edge`, `leverage`, …) |
| `parts` | removable parts: `id`, `label`, `material`, `mass_g`, `attachment`, `outputs_when_removed` |

### Attachments (DR-05a — attachment gates HOW a part comes free, never WHETHER)
`stitched` / `sewn` / `tied` / `lashed` / `cordage` / `glued` / `taped` / `grown` → a blade frees the part
intact. `bolted` / `screwed` / `wedged` / `nailed` / `clipped` / `pinned` → pry frees it intact; cut/tear
hack it out as scraps. `fixed` (or unknown) → integral: refuse with the physics + one near-miss. Authors
opt a part INTO extractability by naming a real attachment.

### Forms and capabilities (DR-26)
Give a `state["form"]` when the shape matters: the multitool is a `blade`, a bottle is a `vessel`, a
branch is a `rod`, paracord is `cord`. The engine derives capabilities (edge, point, heft, leverage,
cordage, sheet, vessel, reflective, …) from **material × form × state**, capped at min(material tier,
form tier). An explicit `state["edge"]` (etc.) overrides the derivation — that is how the golden tools
stay hand-tuned. **Every load-bearing capability must show in the examine text** (the signifier rule).

## Prose (`appearance.py`)
Each object gets an entry keyed by `sim_id`: its home `space` in the zone, `anchor` (leads its space as a
full sentence), `scene` (a noun phrase carrying CHARACTER, not position — the frame owns position),
`examine`, `read`, `aggregate`. State-conditioned variants are `[(state_subset | None, text), …]`, first
match wins. Derived objects (shards, strips, scraps) read from **form-keyed generic templates**
(`"{material} shard, one edge wicked-sharp"`), which a name-keyed entry can override. Tell/hide rule:
show functional flavour; never leave a load-bearing item lying in the open — it lives INSIDE something
(DR-24), earned by `open` / `search` / `dig`.

## Checklist (what `make validate` enforces)
- [ ] every material id exists in the table; every attachment is in the taxonomy
- [ ] `mass_g` and part masses are integers; `sim_id` unique
- [ ] exactly one of `zone` / `in`; the parent exists; the zone exists and has a default space
- [ ] an appearance entry exists (warning if missing — the generic fallback is honest but dull)
- [ ] a puzzle-critical object has an `authored.py` rule and ≥3 solution paths in the rescue graph

## Related
[authoring-actions.md](authoring-actions.md) · [validation-rules.md](validation-rules.md) ·
[adding-a-scenario.md](adding-a-scenario.md)
