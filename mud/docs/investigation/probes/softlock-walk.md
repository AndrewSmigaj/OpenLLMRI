# Probe 3 — manual softlock walk (rescue graph + irreversible chains)

**Goal:** calibrate **solvability / "no impossible or softlocked states" (Q3 / AR6, IM10)** by walking
the rescue graph and the irreversible-resource chains by hand, looking for **global** world-states
with no path forward — the kind the per-*fact* ≥3-paths rule (§44) cannot see. This is the
`solvability-fuzz` skill run in its pre-engine "paper" mode.

---

## The rescue graph (from §7, §38, §39)
Winning = enough **additive rescue confidence** + a **weather window** for pickup. Routes:
- **R-stay**: survive at the wreck until searchers arrive.
- **R-beacon**: power/insulate/elevate the beacon → narrows search.
- **R-radio**: power + improvised antenna + location info → contact.
- **R-visual**: smoke / firelight / SOS / bright fabric, spotted in a weather window.
- **R-travel**: reach weather relay / logging road / abandoned camp / follow river.
- **Combos**: weak beacon + ridge description; radio fragments + improved antenna + pilot route clue; etc. (§39 lists ≥9).

Two **meta-resources** gate *all* routes: **WARMTH** (you must survive the night) and **TIME/weather**
(routes need a window). These are the softlock vectors, because they're *resource-exhaustion*
states, not *facts-with-clue-paths*.

## Irreversible-resource inventory
| Resource | Used by | Irreversible? | Degraded fallback exists? |
|----------|---------|---------------|----------------------------|
| Long metal (frame tube, wire) | radio antenna | burnable/consumable | needs: a sacrificed/short piece still works *poorly* (§38.3 "poor temporary conductor") |
| Battery charge | radio + beacon power | cold-drains; finite | warming/insulating the battery recovers some (§37) |
| Dry fuel / tinder | fire → warmth, smoke signal | burns up | charred remains relight easier; green wood as worse fuel |
| Beacon antenna | beacon; can be cannibalized for radio | "costly tradeoff" (§38.3) | leaves beacon weaker, not dead |
| Pilot lucidity/life | location clues | depletes, then dies | ≥3 other clue paths (§19.2, §38.8) |
| Player warmth/health | everything | hypothermia → death | huddle/shelter/insulation are no-material fallbacks (§32) |

## Walk 1 — the location-info fact (the design's showcase)
Pilot dies in minute 6 before any fragment fired. Is "where is the crash?" still obtainable?
→ §38.8 / §19.2 give: cockpit nav log, torn map mark, **red ridge seen before whiteout**, river
direction, landmark alignment, weather-relay label. **≥3 independent paths.** **Verdict: GREEN** —
the per-fact rule works here; pilot death does not softlock location info. (Caveat in Walk 3.)

## Walk 2 — the "everything for the radio" chain (classic systemic softlock)
Party powers the radio by cannibalizing the **beacon** battery AND builds the antenna from the **only**
long metal AND it still reads weak. Now beacon is dead and radio is marginal.
→ Remaining routes: **R-visual** (fire/smoke/bright fabric) and **R-travel** and **R-stay**. Rescue
confidence is *lower* but **not zero** — visual + a weather window still wins (§39 "smoke signal plus
aircraft weather break"). **Verdict: YELLOW, not RED** — the design's *additive, non-exclusive* routes
(§7) are exactly what prevents this from being a hard softlock. **But** it depends on R-visual being
genuinely independent of the resources just spent (it needs *fire*, which needs *fuel/warmth* — see
Walk 3). **Finding: routes are only truly independent if they don't all bottleneck on WARMTH/FIRE.**

## Walk 3 — the real softlock: the WARMTH/FIRE bottleneck (the dangerous one)
Trace: party wastes the lighter early, soaks the dry tinder, burns the foam (toxic, smothers indoors),
and spends the afternoon failing to start a fire. Night falls (§8 night: −15 to −20°C). No sustained
fire, materials wet/spent.
→ Almost **every** route now fails *transitively*: R-visual needs firelight/smoke; R-radio/beacon need
hands that work and a living crew; R-travel in whiteout is lethal; R-stay means freezing. The group
dies not because a fact was unreachable but because **WARMTH collapsed and warmth gates everything.**
**This is a genuine global softlock the §44 per-fact rule does NOT catch. Verdict: RED (design-level),
severity high.**

**Mitigations the design already has (do they save it?):**
- §32 lists warmth sources beyond fire: **huddling, shelter, insulation from ground, closing fuselage
  gaps, snow trench, sharing body heat** — *no-material* fallbacks. If these are real and sufficient
  to survive a night (even miserably), the fire-failure is recoverable → softlock downgrades to
  YELLOW. **So the fix is explicit: guarantee a no-materials warmth floor (huddle + fuselage + bodies)
  that lets a competent-but-unlucky party survive one night without fire.**
- **Degradation-over-hard-loss** everywhere (charred fuel relights; wet tinder dries by body heat;
  smothered fire leaves embers) so "I wasted it" is rarely terminal.

## Walk 4 — irreversibility audit (do any single actions create a wall?)
- Burn the only long metal → antenna route weaker but R-visual/travel remain → not a wall.
- Eat the only food early → hunger pressure, not a wall (warmth/rescue independent).
- Drop the multitool in the ravine → lose the best edge; but improvised edges (glass shard, torn
  metal) exist → degraded, not a wall, **IF** improvised tools are modeled.
**Finding: no single irreversible action is a hard wall PROVIDED (a) the warmth-floor exists and (b)
improvised substitutes exist for every "only" tool.** Both are design commitments to make explicit.

---

## Calibration result (for the certainty doc)
- **Per-fact solvability (location, repairs): GREEN.** The ≥3-clue/≥3-path rule is sound and the
  redundancy is real (Walk 1).
- **Global solvability: at risk.** The one credible hard softlock is the **WARMTH/FIRE bottleneck**
  (Walk 3): warmth gates every route, so total fire/warmth failure on a cold night is terminal and
  invisible to the per-fact rule.
- **Two explicit design commitments make Q3 defensible:**
  1. **A no-materials warmth floor** — huddling + fuselage + shared body heat must let a competent
     party survive one night without fire (so fire-failure is recoverable, not fatal).
  2. **Degradation-over-hard-loss + improvised substitutes** for every "only" resource/tool, so
     irreversible actions degrade rather than wall.
- **And one instrument:** the `solvability-fuzz` harness (seeded reckless/greedy/random brains) must
  run continuously once the engine exists — it is the only thing that will *find* the next global
  softlock the way this walk found the warmth one.
- **Q3 read:** "smart players can always progress, no impossible states" is **achievable but NOT
  free** — it requires the warmth-floor + degradation commitments + the fuzz instrument. With them:
  high confidence. Without them: a real (if rare) class of unrecoverable deaths.
