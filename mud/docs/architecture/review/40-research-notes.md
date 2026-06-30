# A6 — Research synthesis (raising architecture certainty)

Ties together the two deep investigations — `40-research-evennia.md` (Evennia source + docs) and
`40-research-design.md` (Inform 7 / TADS / PDDL / qualitative physics) — into per-decision deltas and a
concrete **refinements-to-apply** list for A7. **Net: every decision survived; none needs reversal;
confidence rose on all seven researched items, biggest on DR-15.** Residual risks narrowed to
"prove-it-in-the-slice" items.

## Per-decision findings & deltas
| DR | Verdict | C: was→now | The finding (cited in the source files) |
|----|---------|-----------|------------------------------------------|
| DR-15 instancing | **CONFIRM (strong)** | 68 → **83** | The official **EvAdventure dungeon contrib implements our pattern almost line-for-line** (tag-by-`run_id`, create-on-start, `delete()` via `search_object_by_tag`, hourly reaper on `last_updated`); Arx Shardhaven too. It's idiomatic, not invented. |
| DR-14 activity persistence | **CONFIRM** | 75 → **83** | `@reload` is a warm reboot: `.db`/Attributes persist, `.ndb` doesn't; persistent Scripts + `TickerHandler` restore on reload. |
| DR-09 redirect | **CONFIRM** | 80 → **88** | Affordance theory + parser-IF practice (Emily Short) + precondition-error correction (CAPE) converge on: rank by **smallest unmet-precondition gap**, prefer same target, cap 2–3, **name the verb not the solution**. |
| DR-04 ordinals | **IMPROVE** | 80 → **85** | BotW + immersive sims prove few discrete types × consistent rules = combinatorial depth; Stevens measurement-theory caveat: drive outcomes from **rank relations and gaps**, not absolute arithmetic; 7 levels is fine. |
| DR-11 conservation | **CONFIRM + IMPROVE + 1 correction** | 70 → **78** | The accountable sink **is** the textbook control-volume / system+surroundings method; monotonic absorb-only avoids de Kleer's qualitative-arithmetic ambiguity; **both worked balances (foam-burn, 5-strip cut) close.** |
| DR-05 operation model | **CONFIRM + IMPROVE** | 65 → **72** | Inform 7 & TADS 3 are **themselves hybrids** (declarative precondition/phase skeleton over arbitrary code); PDDL's STRIPS→ADL→PDDL+ ladder marks the tier boundary; rule-of-three / complexity-clock / Greenspun all endorse **"plain functions first, extract the DSL later."** |
| DR-07 / DR-10 Evennia state | **CONFIRM / IMPROVE** | 82→85 / 80→82 | Attribute+Tag writes commit in one `transaction.atomic`; the `.db=` lint is feasible. **Footgun found:** Evennia updates in-memory caches eagerly with no rollback hook → a rolled-back `apply()` leaves a stale value. |

## The refinements to apply in A7 (concrete)
1. **DR-11 — conserved quantities are REAL numbers, not ordinals (the one correction).** Ordinals cannot
   carry a conservation balance (qualitative arithmetic is ambiguous: `[+]+[−]=?`). So: **mass is real
   `mass_kg`, integer-quantized** (à la Factorio/Oxygen-Not-Included to kill float drift); **ordinals are
   used only for intensive properties/gates** (resistances, burnability thresholds); **energy is a
   *gate*, not an ordinal balance.** The ledger balances quantized mass + the accountable sink; it does
   not try to "add ordinals."
2. **DR-05 — add a deterministic specificity dispatcher.** The Inform 7 lesson is that *rule precedence*
   is where declarative systems leak; make rule ordering **explicit and deterministic** (most-specific
   wins; ties broken by a declared priority), and keep the DSL **internal + capped** (a fixed node set),
   with plain Python for anything beyond it. Build 2–3 operations as functions first; extract the DSL
   only once the repetition is proven.
3. **DR-10 — cache-invalidation-on-rollback.** Keep "ledger checks *before* any write" (already the
   design) and, in the `apply()` transaction's `except`, call `reset_cache()` on every touched
   Attribute/Tag handler so a rollback can't leave a stale in-memory value; the lint must also catch
   **in-place `SaverList`/`SaverDict` mutation** as a write.
4. **DR-14 — recompute activity progress on `at_start`.** Persist each Activity's start/deadline/progress
   to Attributes and **recompute elapsed from the world clock on `at_start`**, rather than trusting a
   timer's elapsed estimate across a reload.
5. **DR-15 — spawn from a prototype set; reaper sweeps tag-orphans.** Build the instanced zone from a
   **prototype set** (Evennia spawner) and have the reaper **sweep tag-orphans** (objects whose run is
   gone), not just iterate live runs. Cite EvAdventure dungeon as the reference implementation.
6. **DR-04 / DR-09 — relations and gaps.** Outcomes key off **cross-factor rank relations + graded
   gaps**, not absolute ordinal thresholds (DR-04). The redirect ranks candidate operations by
   **smallest unmet-precondition gap**, same-target first, capped at 2–3, naming the verb (DR-09).

## What did NOT change
No decision was challenged at the redesign level. DR-01/02 (core-shell, no-runtime-LLM) remain the
safest. The hybrid operation model, the conservation ledger, ordinal materials, Tag-mirrored state,
instanced runs, and the deterministic mutation path all **survived contact with the literature and the
Evennia source** — and most got *more* idiomatic (DR-15 especially).

## Version note (flagged for a quick check)
The Evennia agent verified against source it labeled **4.5.0 / docs-latest**, while our running container
reports **Evennia 6.0.0**. The findings are about stable subsystems (Attributes, Tags, Scripts,
transactions, spawner, tags-search) unlikely to differ, but a 5-minute re-check against the installed
6.0.0 is worth doing before relying on exact source line numbers.
