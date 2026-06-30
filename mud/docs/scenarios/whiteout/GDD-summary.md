# Whiteout — GDD key points (the one-pager)

The short version of `GDD.md`. **This is your original design + a short list of improvements — not a
redesign.** Same goals, same engine. Runtime is **fully deterministic; no LLM is ever called during
play** (the LLM is a build-time authoring tool only).

## What it is (unchanged)
A text, systemic survival-puzzle game on Evennia. Survive a plane crash by **understanding a
physically-modeled world, not guessing the verb**. One dense scene; rescue wired as additive
confidence. *Every attempt resolves* — never "you can't do that." Input is a **structured, taught
command grammar** — `VERB X [RELATION Y] [WITH Z]` (the RELATION slot makes two-object actions like
`cut … off …` / `wedge … against …` first-class), plus synonyms; everything that fits it and is sensible
resolves via the **generative** operation×material engine — not a canned verb list.

## The engine (unchanged — yours)
Objects → parts → materials → **conservation**; ~20 operation categories (§5); the resolution tiers
(§26). **Mental model:** materials = kinds of LEGO with properties; an object = a parts-list (the chair
= cover/cushion/belt/frame/bolts); operations = pre-written rules. At runtime the engine is a clerk
reading the rulebook — `cut the cover with the knife` → look up CUT → check edge vs fabric → split into
fabric strips → print the authored line. No LLM.

## The improvements (the actual delta — §0a)
1. **Runtime 100% deterministic; all interactions pre-built.** LLM = build-time authoring only (it
   helps write the rulebook; it's never in the running game).
2. **Cheap objects; rich materials + operation rules.** Heavy per-object packets only for puzzle-
   critical objects (radio/beacon/pilot/one showcase seat).
3. **Conservation enforced at runtime** (a ledger that must balance before any change commits) — not
   just documented.
4. **Global-softlock check + a warmth floor** on top of your ≥3-paths-per-fact rule, so smart players
   can't reach an unwinnable state.
5. **Build the one-room slice first** and playtest it, before perception/multiplayer/weather.
6. **Coverage = invariants + a fuzzer + a curated set**, not 700 enumerated tests.

## Locked decisions (§0b/§9) + remaining options
**Locked:** a **continuously running real-time clock** — the world advances on its own; it can't be
poked/stalled by players; event-/turn-based time rejected as clunky for multiplayer · **instanced,
synchronous co-op** runs (~1 in-game day, then reset). **Still optional (drop freely):** a knowledge/
uncertainty layer · an auto-generated end-of-run recap story.

## The honest bottom line
The design is sound and now simpler (no runtime LLM, which also retires the determinism/latency/mis-
parse risks). **The make-or-break is FUN, and it's empirical** — it rests on whether pre-authored,
validated responses read as *specific and witty* rather than dry. No automated check can certify
delight; only a playtest can.
- Works (everything-interacts, dense scene, rescue): **~72%**
- **Fun: ~50% — the make-or-break, settle it with a playtest**
- Solvable, no softlocks (with the warmth-floor + distinct-resources + fuzzer): **~80%**
- Build-time content authorable (with a curated golden table): **~68%**
- Interaction logic sound / improved: **~76%**

## The recommended next move
**Build the single-player vertical slice and playtest it:** one room, ~5 objects, ~25 materials, ~15
operations, the conservation ledger, the deterministic parser + redirect + wall-sensor, ~50 curated
signature responses, a stub radio rescue. *No perception zones, no multiplayer, no clock complexity.*
**Success test:** a new player, no manual, 15 minutes — *"the world felt alive,"* zero "you can't do
that," one delighted "I can't believe that worked." Pass → layer the rest; fail → rethink before
building more.

## Build doctrine (one line)
**Automate what can be *proven* (resolution, conservation, solvability); curate what can only be
*judged* (quality, fun); build the one-room slice first and let the playtest — not the validator —
decide if the world is alive.**

---
**Read more:** `GDD.md` (authoritative) · `../../proposals/whiteout-engine-proposal.md` (the why) ·
`../../investigation/` (brainstorm, research, lens cards + `cross-lens-synthesis.md`, probes,
`certainty-assessment.md`, `scope-and-risk-register.md`, `claude-code-build-practices.md`).
