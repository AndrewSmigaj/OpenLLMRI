# Probe 2 — single-object LLM generation spike (aircraft seat)

**Goal:** calibrate **ontology-authoring throughput (Q4 / IM3)** by generating one object the way the
`ontology-generator` skill prescribes (cheap object + ordinal materials + declarative operations),
then running the §44 validation **by hand** and counting the repairs. The repair rate is the IM3
signal: if first-pass generation is mostly clean, LLM-authoring at density is plausible; if it needs
heavy repair, the schema/prompt is the bottleneck.

I act as the generator (qualitative reasoning only; the engine would own the numbers).

---

## Pass 1 — first-draft generation

### Materials (ordinal property vectors)
```yaml
synthetic_fabric: {cut_resistance: low,  tear_resistance: low-med, burnability: med,
                   ignition_difficulty: med, smoke_toxicity: med, insulation: low-med, absorbency: med}
polyurethane_foam:{cut_resistance: low,  rigidity: very_low, burnability: high,
                   ignition_difficulty: low, smoke_toxicity: high, insulation: med-high}
nylon_webbing:    {cut_resistance: med,  tear_resistance: high, burnability: med, smoke_toxicity: med}
aluminum:         {cut_resistance: very_high, rigidity: high, bend_resistance: med, burnability: none,
                   conductivity: high}
steel:            {cut_resistance: extreme, rigidity: very_high, bend_resistance: high, conductivity: med}
```

### Object (cheap form — no per-object affordance list)
```yaml
aircraft_seat:
  materials: [synthetic_fabric, polyurethane_foam, nylon_webbing, aluminum, steel]
  parts:
    seat_cover:  {material: synthetic_fabric,  attachment: stitched(strength: low-med),  outputs:[loose_fabric]}
    cushion:     {material: polyurethane_foam,  attachment: clipped(strength: low),       outputs:[foam_block]}
    seatbelt:    {material: nylon_webbing,      attachment: bolted_anchor(strength: high),outputs:[webbing_length]}
    frame:       {material: aluminum,           attachment: bolted_floor_rail(strength: high), outputs:[frame_tube]}
    bolts:       {material: steel,              attachment: threaded(strength: high)}
  size: large
  mass: ~12kg
  tags: [furniture, salvageable, in_cabin]
  state: {temperature: below_freezing, wetness: frosty, damage: none, contamination: {}}
```

### Operations touched (declarative; engine owns arithmetic)
```yaml
cut:    pre: tool.edge >= target.material.cut_resistance - slack; target.has_sheet_or_strap
        effect: separate -> outputs; conserve(all); partial: keep progress; fail: informative
pry:    pre: lever_tool; attachment in [clipped, friction]
        effect: detach part; fail: "the <attachment> won't give to prying"
unbolt: pre: tool in [wrench, pliers, improvised_turner]; attachment in [threaded, bolted_*]
        effect: detach; partial: per-bolt; fail: "rounded/frozen — needs a better turner"
bend:   pre: target.material.rigidity <= force AND target.thin; effect: deform; fail: informative
burn:   pre: ignition_source; target.material.burnability > none
        effect: combust -> heat + smoke(toxicity from material); fail: "won't catch / too wet"
```

## Pass 2 — run §44 validation by hand (the gate)

Walking `docs/guides/validation-rules.md` / design §44 against the draft above:

| # | §44 rule | Result | Repair needed |
|---|----------|--------|---------------|
| 1 | No prose-only state changes | ✅ all effects declared | — |
| 2 | Conservation (mass/temp/wetness/contamination/provenance) | ⚠️ **outputs don't carry state** | **R1**: `loose_fabric` etc. must inherit `temperature: below_freezing, wetness: frosty` + provenance; I omitted it. |
| 3 | Every object has material + location | ✅ materials + `in_cabin` tag | — |
| 4 | Every derived object has capabilities or explicit non-uses | ⚠️ **derived objects not defined** | **R2**: `loose_fabric/foam_block/webbing_length/frame_tube` need their own cheap-object entries (materials carry, so light) — I named outputs but didn't define them. |
| 5 | Critical repairs have inspect/access/diagnose/repair/test stages | n/a (seat isn't a repair workflow) | — |
| 6 | Long actions: no clock jump, tick feedback, interruptible | ⚠️ **durations/partial unspecified** | **R3**: `cut`/`unbolt` need a duration model + tick feedback; I wrote "partial: keep progress" but no time basis. |
| 7 | Every important action has failure feedback | ✅ each op has `fail:` | — |
| 8 | Silly / non-survival interaction exists for major object | ⚠️ **missing** | **R4**: add `wear(seat_cover)` badly, `wave`, `stack` — the §44 "one silly use per major object". |
| 9 | Survival-critical objects have tests | ⚠️ **no tests authored** | **R5**: add property tests (cut fabric→pieces sum to mass; cannot cut steel bolt with pocketknife; burn foam→toxic smoke). |
| 10 | Hallucinated capability check (proposal/AR16) | ⚠️ **one found** | **R6**: `bend` precondition `target.thin` — the seat *frame* is thin-walled tube (ok) but `aluminum` alone isn't "thin"; the predicate belongs on the *part* (frame_tube), not the material. Mis-grounded. |

### Repair tally
- **6 repairs** on first pass (R1–R6). Of these:
  - 3 are **systematic / template-fixable** (R1 conservation-carry, R2 derived-object stubs, R3
    duration model) — these should be *auto-filled defaults* in the schema, not author work. If the
    generator template carries them, they vanish.
  - 1 is **checklist-mechanical** (R4 silly use) — a prompt reminder fixes it.
  - 1 is **test authoring** (R5) — hand to `sim-test-writer`.
  - 1 is a **genuine grounding error** (R6 mis-placed predicate) — the kind only validation catches;
    exactly why generate-then-validate is non-negotiable.

## Calibration result (for the certainty doc)
- **First-pass clean? No** — 6 issues. **But** 4 of 6 are eliminable by making the *schema carry
  sane defaults* (conservation inheritance, derived-object stubs, duration models) rather than asking
  the LLM to remember them each time. That is the key IM3 lever: **push invariants into the schema +
  validator, so the LLM's job shrinks to the qualitative judgments it's good at.**
- **The 1 grounding error (R6)** confirms the proposal's hard rule: nothing enters without passing
  the validator; the LLM *will* occasionally assert a mis-grounded capability.
- **Throughput estimate:** with a defaults-carrying schema, expected first-pass repair drops to ~1–2
  per object, most of them caught automatically. That makes LLM-authoring at *moderate* density
  (dozens of objects for one dense scene) **plausible**; full §46 density (hundreds + 700 tests)
  remains unrealistic and should be cut (see implementation lens / scope register).
- **Q4 read:** "LLMs will generate everything needed" is **conditionally yes** — *if* coverage is
  redefined as the bounded operation×material matrix (IM6) and the schema carries the invariants so
  validation, not the LLM, guarantees correctness. Unconditionally (hand-author hundreds of full
  packets): no.
