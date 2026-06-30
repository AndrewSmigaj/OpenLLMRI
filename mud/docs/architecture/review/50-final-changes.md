# A7 — Final changes & re-scored certainty

What the lens pass (A3/A4) and the deep research (A6) changed in `implementation-architecture.md`, and
the **re-scored** certainty. The document is now **v3 (research-refined)**.

## What changed across the review
**v1 → v2 (lens hardening, `20-lens-findings.md`):** closed the lone RED by making the conservation
ledger an **enforced, atomic, transaction-wrapped mutation choke-point** (lint forbids raw writes; tick
state is Effects too); drew the **operations DSL envelope** ("plain functions first, extract later");
made **determinism an enforced contract**; added a **debris policy + `Part.mass`** and an **accountable
environment sink**; named the **quality gate** (golden set + playtest).

**v2 → v3 (research refinement, `40-research-notes.md`):**
1. **The one correction:** conserved mass is a **real, integer-quantized** quantity; **ordinals are only
   intensive gates**; **energy is a gate, not a balanced channel** (qualitative-physics result).
2. **Specificity dispatcher** for deterministic rule precedence (Inform 7 lesson).
3. **Cache-invalidation-on-rollback** for the Evennia eager-cache footgun.
4. **Recompute activity progress on `at_start`** after `@reload`.
5. **Instance from a prototype set; reaper sweeps tag-orphans** — confirmed near-identical to the
   official **EvAdventure dungeon contrib**.
6. **Relations & gaps, not absolute thresholds**, for outcomes and the informative redirect.

No decision was reversed at any stage; every change was additive hardening or a confidence-raising
refinement.

## Re-scored certainty (v3) — same rubric as `30-certainty.md`
Δ shows the movement from the v2 baseline. (C = confidence 0–100, K = criticality 1–3.)

| DR | Decision | C (v2→v3) | K | Δ | Driver of the change |
|----|----------|-----------|---|---|----------------------|
| DR-01 | Core/shell split | 90 | 3 | — | proven |
| DR-02 | No runtime LLM | 95 | 3 | — | proven |
| DR-03 | Content as data | 75 | 2 | — | hybrid; fine |
| DR-04 | Material ordinals + golden table | 80→**85** | 3 | +5 | BotW/imm-sim precedent; relations-not-arithmetic refinement |
| DR-05 | Operation model (hybrid DSL) | 65→**72** | 3 | +7 | Inform 7/TADS are hybrids; PDDL tier ladder; "functions first" endorsed; + specificity dispatcher |
| DR-06 | Object model + debris + Part.mass | 78 | 2 | — | hardened in v2 |
| DR-07 | Attributes + Tags single truth | 82→**85** | 3 | +3 | Tag-mirror is the documented Evennia idiom; same-txn write supported |
| DR-08 | Deterministic parser | 85 | 2 | — | proven |
| DR-09 | Resolver tiers + redirect | 80→**88** | 3 | +8 | affordance/parser-IF/CAPE convergence on gap-ranked redirect |
| DR-10 | Enforced atomic mutation path | 80→**82** | 3 | +2 | `transaction.atomic` over Attr+Tag confirmed; + cache-rollback fix |
| DR-11 | Conservation ledger + sink | 70→**78** | 3 | +8 | sink = textbook control-volume; worked balances close; real-mass correction |
| DR-12 | Determinism (enforced) | 85 | 3 | — | proven recipe |
| DR-13 | Perception/zones | 80→**83** | 2 | +3 | per-action WorldView cheap (idmapper cache) |
| DR-14 | Clock/scheduler + @reload | 75→**83** | 2 | +8 | `@reload` persistence + Script restore confirmed; recompute-on-`at_start` |
| DR-15 | Instanced sessions | 68→**83** | 2 | +15 | **EvAdventure dungeon contrib implements it almost line-for-line** |
| DR-16 | Rescue + radio FSM | 78 | 2 | — | reasoned; small authored FSM |
| DR-17 | Build pipeline | 80 | 2 | — | standard asset pipeline |
| DR-18 | Coverage/fuzz | 82 | 3 | — | proven methods |
| DR-19 | Test strategy (two tiers) | 88 | 2 | — | demonstrated in the scaffold |
| DR-20 | Observability | 85 | 1 | — | standard |
| DR-21 | Module/file layout | 88 | 1 | — | conventional |
| DR-22 | Vertical slice scope | 88 | 3 | — | strongly de-risking |

## New aggregate
- **Σ(C·K) = 4429 · Σ(K) = 53 → Overall architecture confidence ≈ 84 / 100** (up from **≈81**).
- **No decision is below 72.** The architecture sits solidly in "Sound", with the two load-bearing
  uncertainties (DR-05, DR-11) now backed by external precedent and reduced to **empirical "prove-it-in-
  the-slice" items** rather than open design questions.

## Residual risks (ranked R = (100−C)·K) — and where they retire
1. **DR-05 operation model (R=84).** The DSL boundary is now well-grounded (Inform 7/TADS hybrids,
   specificity dispatch) but its *exact* envelope is empirical → **retired by building 2–3 operations as
   functions in the slice and only then extracting the DSL.**
2. **DR-11 conservation energy fidelity (R=66).** Mass closes exactly; energy-as-gate is the modeling
   simplification to validate → **retired by the slice's fire/cut balances + the ledger property test.**
3. **DR-18/DR-10 (R=54).** Coverage definition + the cache-rollback fix → retired by the fuzz harness +
   the apply() rollback test.
4. The rest are ≥78 and standard.

## Bottom line
The deep review + research moved the architecture from **"sound on paper" (~81)** to **"sound, enforced,
and externally corroborated" (~84)**, with one substantive correction (real-mass conservation) and a
handful of idiomatic-Evennia confirmations (the instancing pattern especially). **The remaining
uncertainty is concentrated in two decisions whose right home is the vertical slice** — exactly where the
GDD already puts the first build. The architecture is ready to implement; the slice is the experiment
that retires what's left.

*One housekeeping item (from `40-research-notes.md`): the Evennia source the research cited was labeled
4.5.0/docs-latest while our container reports 6.0.0 — a 5-minute re-check of the Attribute/Tag/Script
APIs against the installed 6.0.0 before relying on exact line numbers.*
