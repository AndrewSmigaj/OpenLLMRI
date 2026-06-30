# Loop Workflow

The agentic authoring loop: **anchor → author → verify → repeat**, driven by
Claude Code's built-in `/loop` skill. This is how content is produced one small,
validated increment at a time.

> Why a loop: Whiteout is built in passes ([roadmap](../scenarios/whiteout/roadmap.md))
> from authoring *packets* (§43) gated by *validation* (§44). A tight loop that
> re-anchors on the design every iteration keeps work from drifting away from the
> non-negotiables.

## The four beats

```
        ┌─────────────────────────────────────────────┐
        ▼                                             │
1. ANCHOR ──► 2. AUTHOR ──► 3. VERIFY ──► (pass?) ────┘
   read the      write one      make verify / /verify
   ground truth  small piece    fix until green
```

### 1. Anchor

Re-read the ground truth *before* each work session so the loop returns to a
fixed point when it drifts:

- [`../../VISION.md`](../../VISION.md) — the non-negotiables.
- The authoritative design — [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md)
  (cite sections as "§N") — and the [roadmap](../scenarios/whiteout/roadmap.md)
  for *which phase (P0–P7)* you're in.

### 2. Author

Make **one** small, coherent change, from its packet template and guide:

- an object → [authoring-objects.md](authoring-objects.md) (`ObjectPacket`)
- an action family → [authoring-actions.md](authoring-actions.md) (`ActionFamilyPacket`)
- a workflow → [authoring-workflows.md](authoring-workflows.md) (`WorkflowPacket`)

Keep rules pure (`world/sim/**`); keep the Evennia shell thin
([../architecture/overview.md](../architecture/overview.md)).

### 3. Verify

Run the gate. Locally that is:

```
make verify SCENARIO=<name>   # compose config check + make test + make validate
```

— the fast pure tests ([../architecture/testing.md](../architecture/testing.md))
plus the §44 content-lint ([validation-rules.md](validation-rules.md)). In Claude
Code, the **`/verify`** step plays the change and confirms it behaves. Fix until
green; a red gate is the loop's stop condition, not a suggestion.

### 4. Repeat

Loop back to anchor for the next increment.

## Driving it with `/loop`

Use Claude Code's built-in **`/loop`** skill to run the cycle automatically — e.g.
self-paced, or on an interval — re-anchoring and re-verifying each pass. Keep each
iteration's scope to something `make verify` can check in one go: one object, one
action family, one workflow stage. End an iteration only when the gate is green.

## Concrete example (one iteration)

1. **Anchor:** roadmap P1 = "the co-op vertical slice → the fun gate" (the GDD slice success test).
2. **Author:** add `scenarios/whiteout/objects/aircraft_seat.py` as an
   `ObjectPacket` with parts that dismantle several ways, each output first-class
   with uses or explicit non-uses.
3. **Verify:** `make verify SCENARIO=whiteout` — pure tests for the dismantle
   conservation, validator confirms every output has uses + tests exist.
4. **Repeat:** next iteration, the seat's outputs feed the splint/shelter
   workflows.

## Related

- [docker-workflow.md](docker-workflow.md) — the commands the loop calls.
- [validation-rules.md](validation-rules.md) — what `make verify` enforces.
- [../scenarios/whiteout/roadmap.md](../scenarios/whiteout/roadmap.md) — the passes.
