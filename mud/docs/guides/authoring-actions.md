# Authoring Actions (operations)

> Rewritten 2026-09-07 for the closure loop (DR-05b / DR-26). Verbs are **pure Python handlers** over
> material properties, forms, capabilities and attachments — one handler cuts fabric, webbing and foam
> differently because the *materials* differ. There is no DSL (retired, DR-05b) and no per-object code.

## Where a verb lives
- `game/world/sim/operations/handlers/<op>.py` — a pure module with `VERBS = (...)` (the canonical verb
  first, then synonyms) and `resolve_<op>(attempt, world, materials) -> ActionResult | None`.
- `game/world/sim/operations/registry.py` — one `Op(...)` entry: `relations` the verb accepts,
  `applies_to` (material tags / attachments the coarse redirect suggests it for).
- `game/world/scenarios/<scenario>/responses/*.py` — the narration templates (`<op>.<outcome>`).
- Extra synonyms and particle forms — `game/world/sim/parser/vocab.py` (`SYNONYMS`, `PARTICLES`).

## The tier ladder as implemented (`resolver/tiers.py`)
0 the **reach gate** (a far thing → "too far to {verb} from here") · 1 **authored** (a per-object rule from
`authored.py`) · 3 the **handler** · 4 **generic physics** (`resolver/physics.py`: a property-based answer
when the handler returns `None`) · 5 the **coarse redirect** (≤2 plausible verbs). Everything resolves;
nothing says "you can't do that". The wall-sensor logs tier-5 hits to `gaps.jsonl`.

## The handler skeleton
```python
VERBS = ("scrape", "scratch", "abrade")

def resolve_scrape(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)          # X may be a thing or a part
    if ent is None:
        return None                                    # let the resolver answer
    mat = material_of(attempt.X, world, materials)
    if mat is None or "rigidity" not in mat.props:
        return None                                    # not scrapeable → tier 4 / redirect
    edge = capability(attempt.tool, world, "edge")     # authored OR derived (DR-26); 0 = bare hands
    if edge < 0.2:
        return ActionResult(Resolution.REDIRECT, tier="op:scrape:no_edge",
                            narration=narrator.narrate("scrape.no_edge", {...}))
    eff = (effects.adjust_attr(ent.id, "frost", -1),
           effects.create_object("water", derived_id(ent.id, "melt"),
                                 {"material": "water", "mass_g": 20, "form": "liquid",
                                  "provenance": [f"scraped from {ent.id}"]}))
    return ActionResult(Resolution.SUCCESS, effects=eff, tier="op:scrape:frost",
                        events=(Event(EventKind.IMPACT, ent.id, loudness=0.2),),
                        narration=narrator.narrate("scrape.frost", {...}))
```
Rules the skeleton encodes:
1. **The material gate comes first** (a dull blade is dull whatever the attachment).
2. **Read capabilities, never tool identities**: `capability(ref, world, "edge")` — a shard, a knife and a
   torn sheet all answer; the value is authored or derived from material × form.
3. **Attachments gate HOW, never WHETHER** (the DR-05a table): severable → intact; mechanical → scraps
   (cut/tear) or intact (pry); integral → refuse + physics + one sibling near-miss.
4. **Mint with a form.** Every `create_object` names the `form` of what it makes (`shard`, `strip`,
   `scrap`, `piece`, `sheet`, `shavings`, `bundle`, `ember`, `ash`, `liquid`…). Mass is integer grams and
   the pieces sum to the original; the ledger rejects anything else.
5. **Narration only from templates**, filled from the projected post-state; never a prose-only change.
6. **Return `None` when the verb doesn't apply to X at all** so tier 4 can answer physically.
7. **Accessories are implicit** when unambiguous (a handhold for the drill, a reachable flame for melt) and
   are **named in the prose**; the primary tool is always the explicit `with Z`.
8. **Duration** goes in `duration_minutes` (game-minutes); the scheduler turns it into an attended
   activity with tick feedback (DR-27) — never sleep, never wall-clock.

## Shaping verbs (`carve`, `split`, `shave`, `whittle`, `notch`, `string`, `bundle`)
Their grammar is `VERB X into <form> [with Z]`; the form arrives as a pseudo-noun in `attempt.Y`
(`form:spindle`). A real entity in Y means "one like that". The handler checks the material/form is
shapeable into the target form, consumes/transforms X, and mints the output with the new form.

## Adding a verb — checklist
- [ ] handler module + `VERBS`; registry `Op` with `relations` and `applies_to`
- [ ] response templates for every outcome (success / partial / each refusal) — `{tool}` arrives
      pre-articled ("the multitool" / "your bare hands"); never write an article before it
- [ ] synonyms/particles the phrasing corpus showed (`vocab.py`)
- [ ] probes: the success case, the honest failure(s), the silly case; cite their source
- [ ] a Tier-1 test: resolves, conserves, the redirect is informative
- [ ] `make test-host && make validate && make probes` green; `make render-scenes` read

## Naming rules (still current)
Derived template ids compose material-first (`glass_shard`, `synthetic_fabric_strip`); the display key is
the id with underscores → spaces, so the order IS the player-facing name.

## Related
[authoring-objects.md](authoring-objects.md) · [validation-rules.md](validation-rules.md) ·
[`../architecture/ontology-closure.md`](../architecture/ontology-closure.md)
