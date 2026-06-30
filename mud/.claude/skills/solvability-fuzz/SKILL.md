---
name: solvability-fuzz
description: Drive seeded, reproducible runs over a Whiteout scenario (via the ScriptedBrain / a simulated player) to find UNRESOLVED attempts and GLOBAL softlocks that the per-fact ≥3-paths rule can't catch. Use to assess "can smart players always make progress" and to feed the wall-sensor / crystallize queue. Reports against an oracle of §44 invariants.
allowed-tools: Read, Bash, Write, Grep, Glob
---

# Solvability fuzz — find dead-ends and unresolved attempts empirically

The ≥3-solution-paths rule (design §44) is enforced *per fact*; it cannot see **global**
world-state softlock (the only long-metal antenna burned AND all fuel spent AND the pilot dead
before any clue fired AND everyone hypothermic). The only way to *find* that is to drive runs and
check. This skill is the oracle (proposal §5; lenses AR6, IM10).

## What it checks (the oracle)
1. **Unresolved attempts** — any action that fell through to generic-redirect with no physical
   answer (a GD25 / "wall" defect). Source: the engine's **wall-sensor log**.
2. **Global softlock** — a reachable world-state from which no rescue path remains. Detect via a
   resource-exhaustion / reachability check over the rescue graph (proposal §5).
3. **Invariant violations** — conservation breaks, non-monotonic rescue confidence, a timed action
   that jumped the clock, narration referencing state with no backing Effect.
4. **Irreversibility traps** — an irreversible action that removes the *last* means to a goal with
   no degraded fallback (prefer degradation-over-hard-loss).

## Procedure
1. **Pick a seed** (deterministic — the run must replay identically; AR4). Record it.
2. **Drive the run.** Use the bot harness with the scripted brain against a loaded scenario:
   `make load-scenario SCENARIO=<name>` then `python agent/runner.py --brain scripted --seed <n>`
   (once the harness/engine exist). Strategies to script: greedy-survival, reckless (burn/spend
   everything), pilot-ignored, and random-within-affordances.
3. **Collect** the wall-sensor log + the rescue-graph state at end-of-run + any invariant assertions
   that fired.
4. **Classify** every flagged item: unresolved-attempt | global-softlock | invariant-violation |
   irreversibility-trap | false-alarm.
5. **Report** → write `docs/investigation/probes/fuzz-<scenario>-<seed>.md`: counts per class, the
   worst dead-end with its action trace, and the prioritized fix queue. Unresolved attempts go to the
   `ontology-generator` crystallize mode; softlocks go to design (add a degraded fallback or a clue
   path).
6. **Regression.** Keep seeds + expected oracle results so fixes don't reintroduce dead-ends.

## Before the engine exists (current state)
The engine/scenarios are not built yet. In that case run this as a **manual / paper** walk: trace
the rescue graph and one irreversible-action chain by hand against the design, and write the same
report shape. (That is exactly the P5.5 "softlock walk" probe.)

## Output
A fuzz/softlock report with: seed, runs, unresolved-attempt count, the worst global-softlock trace,
invariant violations, and the prioritized fix queue. Calibrates the certainty answer for "smart
players can always progress, no impossible/softlocked states" (Q3).
