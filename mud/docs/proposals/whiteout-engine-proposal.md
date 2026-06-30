# Proposal — targeted improvements to the Whiteout design

**This is not a redesign.** The goals, the engine, and the action model are the original design's
(`docs/scenarios/whiteout/design.md`). This proposal argues for a **short list of improvements** to how
they're built, grounded in the research (`docs/investigation/research/`) and the lens review
(`docs/investigation/lenses/`). The authoritative result is `docs/scenarios/whiteout/GDD.md` (§0a
improvements, §0b optional). Here is the *why* behind each.

---

## 0. What stays exactly as you designed it
- The goals: survive-by-understanding · everything-interacts · one dense authored scene · multiple
  rescue routes · every-attempt-resolves · no autonomous NPCs.
- The engine: objects → parts → materials → conservation (§20–24); ~20 operation categories (§5);
  actions via a structured, *taught* grammar — `VERB X [RELATION Y] [WITH Z]` + synonyms (§25/§25a); the
  resolution tiers (§26).
This proposal touches none of that. It improves six things and records the now-locked mechanic decisions
(clock + session model, GDD §9).

## 1. Runtime is fully deterministic; the LLM is a build-time tool only
**Your design already says "deterministic engine owns state; LLM proposes interpretation/prose" (§41).**
The improvement is to make that absolute: **remove the runtime LLM tier (§26) and the runtime
intent-fallback (§41).** During play the engine never calls an LLM; every interaction and response is
pre-built. The LLM's job is entirely in the **workshop**: help author the material table, the operation
rules, the objects, and the response text — which a validator + a human approve and bake into data.

**Mental model (the chair):** materials are kinds of LEGO with properties; an object is a parts-list;
operations are rules in a pre-written rulebook. At runtime the engine is a clerk reading the rulebook:
`cut the cover with the multitool` → look up CUT → "is the edge ≥ fabric's resistance? yes" → cover
becomes loose fabric (conservation carries its frost) → print the authored line. `cut the steel bolt`
→ "edge ≥ steel? no" → print the authored *why-not*. No imagination, no LLM.

**Why:** the research is decisive — AI Dungeon (no ground truth → incoherence) and GPT-as-simulator
(~60% transition accuracy, compounding error) prove the LLM must never own or step state. Keeping it
out of runtime also **deletes** a column of risks the lens review raised (runtime determinism AR4,
latency AR9/IM4, parser mis-parse GD21, cache trust AR3). This is the single biggest simplification and
it matches your "no LLMs in the scene."

## 2. Author materials + operation rules richly; keep objects cheap
**Your §4 already says "model-deep, requirement-light"; your §5/§21 already have operations + materials.**
The improvement is to make the *operation×material rules* the default workhorse and keep **objects
cheap** (just material/part tags), reserving the heavy §43 packet for the handful of puzzle-critical
objects. *Why:* the research validates few-uniform-rules-over-many-objects (BotW's 3 chemistry rules;
ScienceWorld 25 actions → ~200k pairs), and the lens review rated the heavy-packet-per-object default
unaffordable at density (IM5). Same expressiveness, a fraction of the authoring.

## 3. Make conservation a runtime assertion (a ledger), not just a content-check
**Your §24 lists conservation and §44 lints it.** The improvement: enforce it **at commit** with a
per-transform ledger (material/mass-against-an-environment-sink/contamination/heat/provenance/length-
count must balance, else reject). *Why:* the review's lone RED was that conservation lived in prose, not
runtime (AR15), and the model didn't fully close — there was no environment sink for burn/melt/boil
(AR11). This is the flagship invariant to build first; it's what makes "everything interacts"
*trustable*.

## 4. Add a global-resource softlock check + a warmth floor
**Your §44 guarantees ≥3 paths per critical fact** — keep it. The improvement adds a check the per-fact
rule can't do: **global** world-state reachability, so a party can't burn/spend its way into an
unwinnable state (the review and the softlock probe both found the warmth/fire→stamina bottleneck sits
under *all* rescue routes). Two design commitments fix it: a **no-materials warmth floor** (survive one
night without fire) and **rescue routes drawing on distinct scarce resources**. *Why:* this is the only
way to honestly answer "smart players can always progress" (Q3).

## 5. Build the one-room ontology slice first
**Your §42 build order starts with the tick engine and perception** — the hardest systems and the least
able to prove the game is fun. The improvement: build a **single-player, one-room vertical slice of the
ontology first** (the chair + a few objects + the operation/material core + the deterministic parser +
the conservation ledger + ~50 curated signature responses), and **playtest it.** *Why:* the make-or-
break is whether pre-authored, validated responses *feel alive*; that's empirical, and this slice is
the cheapest experiment that settles it before you invest in perception/multiplayer/weather.

## 6. Coverage = invariants + a fuzzer + a curated set (not 700 enumerated tests)
**Your §45/§46 ask for 700+ enumerated tests and hundreds of objects.** The improvement: define "done"
as **the operation×material matrix complete + property-tested, plus a ≥10k-attempt fuzz corpus** (0
unresolved, 0 conservation violations, rescue reachable), plus a small **hand-curated golden set** for
quality. *Why:* you can't enumerate an open space (IM6); invariants + fuzz cover it, and the curated set
is the only thing that certifies *quality* (the validator proves an action resolves and conserves,
never that it reads well).

---

## Mechanic decisions — now LOCKED (see GDD §9 / §0b)
These once-open choices are decided; recorded here so this proposal doesn't conflict with the GDD:
- **Clock — a continuously running real-time clock (LOCKED).** The world advances in real time on its
  own; it can't be poked, stalled, or yanked by players. Event-/turn-based time was **rejected** as
  clunky for multiplayer.
- **Session model — instanced, synchronous co-op runs (LOCKED)** (~1 in-game day, then reset).
- **Remaining nice-to-haves (still optional):** a knowledge/uncertainty layer (believed-vs-true) and an
  auto-generated end-of-run recap story. Pure additions.

## The build-time toolchain (how the LLM helps author, sanely)
At build time only: `ontology-generator` drafts materials/operations/objects → `make validate` + the
conservation ledger gate them → `solvability-fuzz` finds dead-ends + unauthored attempts (the
wall-sensor) → a human curates the golden material values + signature prose → playtest. Automate what
can be *proven* (resolution, conservation, solvability); a human curates what can only be *judged*
(quality, fun). See `docs/investigation/claude-code-build-practices.md`.

## Bottom line
Six improvements + three optional choices, on top of your unchanged goals and engine, with runtime made
fully deterministic. The risk that matters is fun, and it's empirical — so the first move is the
one-room slice and a playtest. Full design: `../scenarios/whiteout/GDD.md`. Calibrated certainty:
`../investigation/certainty-assessment.md`.
