---
name: lenses
description: Review a design or implementation artifact through curated "lens" libraries (game-design — Schell's Book of Lenses + immersive-sim/IF; architecture + code-smell; implementation/feasibility). Use when asked to critique, pressure-test, or assess a design/GDD/spec/subsystem, or to produce per-lens findings and a cross-lens synthesis. Produces finding cards, not vibes.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Lenses — structured multi-perspective review

A *lens* is a short set of questions you hold up to an artifact; each reveals problems a single
perspective misses (after Jesse Schell, *The Art of Game Design: A Book of Lenses*). This skill
applies three curated libraries and emits **finding cards**, then a **cross-lens synthesis** that
surfaces where the lenses *disagree* (the most useful output).

## Libraries (in this folder)
- `game-design.md` — 25 lenses (GD1–GD25): Schell subset + immersive-sim/interactive-fiction.
- `architecture.md` — 17 lenses (AR1–AR17): design integrity + a code-smell/code-debt subset.
- `implementation.md` — 12 lenses (IM1–IM12): feasibility, LLM-in-the-loop, tooling.

Each lens entry gives an **ID**, the **key question**, **what to look for**, and **applies-when**.

## Output: the finding card
For every lens applied, write one card:

```
### <ID> <Lens name>
- **Verdict:** GREEN (holds) | YELLOW (at risk) | RED (broken / unaddressed)
- **Evidence:** the specific design element / file / line / claim examined.
- **Severity:** low | med | high | existential (only if RED/YELLOW).
- **What would change the verdict:** the concrete evidence or change that flips it. *(If the only fix
  would change the vision or a locked decision, write "outside scope — vision-level flag" instead — see
  Protocol step 4.)*
- **Note:** 1–4 sentences. HIGH-leverage lenses get a paragraph; LOW get one line.
```

## Protocol
1. **Scope.** State exactly what artifact(s) you're reviewing and against what goal.
2. **Vision & Locked Decisions (REQUIRED — do this before applying a single lens).** Write down the
   **fixed inputs** this review may NOT touch: the *vision* (genre, premise, core promise, the
   non-negotiables in `VISION.md` / the design's §49) and every **decision the user has explicitly
   locked** (e.g. a GDD "Decisions" section or the plan's "Decisions DECIDED" list). **These are the
   objective the design optimizes *toward* — not variables to optimize.** Lenses pressure-test the
   *execution* against the vision; they never audit, question, or recommend changing the vision or a
   locked decision. If you're unsure whether something is locked, treat it as locked and flag it — do
   not assume it's open.
3. **Triage (optional but recommended for big reviews).** Rate each lens HIGH/MED/LOW *leverage*
   for THIS artifact = (how much it could change the design) × (how uncertain the answer is now).
   Deep-dive the HIGH set; still give every lens a card (shorter for MED/LOW). See
   `docs/investigation/lenses/triage.md` for a worked example.
4. **Apply.** Walk the chosen lenses, writing finding cards. Quote the artifact. Be adversarial:
   look for the *failure*, not confirmation. A lens that says "fine" must say *why it's certain*.
   **Stay inside the vision (step 2):** if a lens uncovers a real problem whose only fix would change
   the vision or a locked decision, do **not** recommend changing it. Instead either (a) reframe it as
   a **risk-within-the-vision** — mitigations that keep the decision intact — or (b) mark it
   **"outside scope — vision-level"** and surface it as a neutral *flag for the user to decide*, never
   as a recommendation to build something else. (E.g. "event-based time would be simpler" against a
   locked real-time clock → reframe to "here's how to make real-time robust," not "switch to
   event-based.")
5. **Group docs.** Collect cards into one file per library (or one combined file).
6. **Cross-lens synthesis.** Write a short doc listing where lenses **conflict** (e.g. a "feel
   boundless" lens vs a "density won't scale" lens) — each conflict names the seam where an
   *unbounded promise meets a bounded mechanism*, and how/whether the design resolves it **within the
   vision** (the resolution may *not* be "drop the promise" when the promise is locked).
7. **Make findings enforceable.** Any finding that implies an invariant ("conservation must hold
   at runtime", "rescue confidence monotonic", "no narration without a backing Effect") should be
   proposed as a new `make validate` rule and/or a property test (hand it to `sim-test-writer`),
   so the review yields *enforced outcomes*, not just prose.

## Running it at scale
For a large artifact, fan out: one subagent per library (mirroring the repo's `engine-reviewer`
style), each producing its group's cards, then a synthesis pass. Keep the goal statement, the
**Vision & Locked Decisions list (step 2)**, and the triage identical across agents — so every agent
optimizes within the same fixed vision and the cards are comparable.

## When NOT to use
Don't use for a trivial change or a single obvious bug — lenses are for design-level judgement and
multi-perspective pressure-testing, where the value is catching what one viewpoint misses.
