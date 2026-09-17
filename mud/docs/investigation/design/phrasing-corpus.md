# The phrasing corpus — what agents actually type, and what the parser does with it

> **Status: SCRATCHPAD — design pass + data record (2026-09-07).** The discovery loop's first
> artifact: two agents (Sonnet 5, Haiku 4.5), seven survival tasks, naive (A) and taught (B)
> conditions, 294 lines → `game/world/scenarios/whiteout/probes/phrasing.py` (expect PARSED; status
> measured). Re-run after every parser or vocabulary change; a fresh sample every few clusters.

## 1. Method (the protocol, adjusted to what we can run)
- The agent gets the SCENE (the room prose + what searching found) and a GOAL per task, never the
  target action. Condition A: no grammar told. Condition B: the four-line grammar note + three
  examples on unrelated objects.
- One family, three capability tiers (Haiku / Sonnet / Opus 4.8 once pinned). Cross-family sampling
  waits for the play harness with an API-key brain.
- Each line becomes a probe with `expect: PARSED` — did the line reach the engine *understood* (a
  noun bound, or an intransitive act resolved)? The outcome is not judged here; that is the
  census/graph probes' job.
- Anti-copying: the B examples use different objects than the tasks; a shift toward the examples'
  exact preposition is copying, not generalization (none observed at this sample size).

## 2. The numbers (real parser, real nouns)
| | before (2026-09-07 morning) | after the tolerance layer |
|---|---|---|
| Sonnet 5, taught (B) | 58% | **83%** |
| Sonnet 5, naive (A) | 37% | 78% |
| Haiku, taught (B) | 32% | **79%** |
| Haiku, naive (A) | 23% | 71% |
| census candidate commands | 58% | 73% *(census probes: 26/89 pass)* |

Preposition tally (Sonnet): with 29 · on 24 · to 16 · in 14 · into 10 · from 10 · around 7 · off 7
· over 5 · against 5. Particles seen: put on, blow on, set off, turn on, pick up, scoop up, roll
up, tie off, take out, snap off, zip up.

## 3. What the residue is (the 17–21% that still fails, taught condition)
| category | examples | owner |
|---|---|---|
| verbs that don't exist yet | turn/switch/adjust (toggles), press, spin, wave, fix, carve/whittle (shaping), sit/huddle/rest, dry, block/shield/cover-an-opening, clear, stuff | steps 4–5 (verb gaps), the fire pass (shaping) |
| nouns that don't exist yet | the flame / the fire (no fire entity), the hull tear / the breach, the notch, sticks / twigs / bark (no such objects; only "deadfall branch"), a pulse, "the plane" | the fire pass (fire entity), scenery nouns (step 5), living rooms (more objects) |
| lines that aren't acts | "see if I can tell where we crashed", "keep the cover as a second layer", "let the water cool", "check if bleeding has stopped" | leave: not commands; the guide says state the act |
| junk tokens | "there's", "if no ember, …" (now handled), gerunds (now handled) | done |

Nothing in the residue is a grammar shape. The grammar is sufficient; the vocabulary and the world
are what grow.

## 4. What the samples taught us (rules adopted)
1. Agents type **particles** constantly (`put on`, `take out`, `pick up`) → positional particle table.
2. Agents narrate **intent** in the naive condition and mostly stop in the taught one → trim it, and
   put "state the act" in the guide.
3. **`use X on/to`** is the first thing an untaught agent tries → the teaching verb that echoes.
4. **Synonym drift is bounded**: after the table, unknown verbs are real missing verbs, not
   phrasing.
5. Nouns fail more than verbs: **plurals, adjectives, head nouns** (`the quilted engine cover`),
   **possessives that aren't parts** (`the pilot's jacket`) → all four handled in the binder.
6. The taught condition converges across models (79 vs 83); the naive gap is larger (71 vs 78) —
   another reason the guide goes to agents up front.

## 5. Next samples
- After the verb-gap batch and scenery nouns: re-sample both conditions, N≥20 per task at
  temperature, add Opus 4.8; expect ≥90% taught.
- A cold/primed comparison on five compound acts (`carve … into …`) once shaping exists.
- Log every live-play gap (`server/logs/gaps.jsonl`) into the same corpus.

## 6. Lens pass (Skill · Information · Curiosity)
- **Skill — GREEN:** the taught condition is learnable in four lines; the residue is content.
- **Information — GREEN:** an unknown word gets a clarification and the grammar help; synonyms absorb
  phrasing (no verb suggestions, no verb list — corrected 2026-09-16).
- **Curiosity — YELLOW:** agents in the naive condition tried things the world can't answer yet
  (blow on the flame, cover the tear). Those are the best gaps: they are what a curious player wants.
