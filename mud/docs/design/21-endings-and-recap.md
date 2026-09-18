# 21 — Endings and the recap

> **Status: draft for review** (created 2026-09-16). **Architecture counterpart:** none — the run
> lifecycle is DR-15/DR-15a in [`implementation-architecture.md`](../architecture/implementation-architecture.md)
> §2, and the recap has no spec.
> **Sources:** [`events-and-escalation.md`](../investigation/design/events-and-escalation.md) §3 (and
> §1, §2, §6) · [`roadmap.md`](../scenarios/whiteout/roadmap.md) P7 ·
> [`GDD.md`](../scenarios/whiteout/GDD.md) §0b ·
> [`moral-social-layer.md`](../investigation/design/moral-social-layer.md) §1–§3 ·
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1, §4.

## 1. Status

Draft for review, and thin on purpose. One thing here is Andrew's (the shape of a run); the four
endings are a proposal he has not seen, and the provenance audit lists them in §4, "still needing
Andrew's call". The recap is an explicitly optional nice-to-have that nobody has specified. This
document is mostly open questions, and that is the honest state of it.

## 2. Provenance

### Andrew's decisions

**The shape of a run (2026-09-07**, recorded in the provenance audit §1 and in DR-15a; the audit's
paraphrase of his brief, not a verbatim quote**):** the game runs **roughly a week**; **rescue can
come earlier**; it **can run longer until the food runs out**; it is **not permanent**. Instead of
hard time-window barriers, **increase the things that cause death** so that a party that is not
rescued dies honestly. **There is no set arc** — what to do is the players' decision.

That gives the ending system its whole frame: a run ends because the world got the better of the
party or because they got out of it, never because a timer expired. No ending may be a barrier.

### Proposals (Claude)

- **The four endings** as named and described in §4.1 — rescued, walked out, dead, still going. The
  provenance audit lists "the four endings incl. 'still going'" under §4, *Still needing Andrew's
  call*.
- **"The run ends when the last player dies"** and **"a dead player's body persists"** (events §3).
- **"The ladder guarantees an ending within ~two weeks of game time for any party"** (events §3) — a
  claim about the escalation numbers, which are themselves proposals.
- **The recap** — an auto-generated end-of-run narrative read out of the deterministic event log.
  GDD §0b lists it among the "remaining nice-to-haves (**genuinely optional — drop freely**)"; the
  roadmap puts it in P7 and calls it "the optional nice-to-have". It originates in the investigation
  brainstorm §9 as "the run's auto-generated story".

## 3. In one paragraph

A run ends four ways, and none of them is a clock running out: a helicopter puts down on the ice
because something you did was visible from the air at the moment a plane went over; you reach Holt's
cabin and the stove works; you die of cold or hunger or thin ice; or nothing has ended yet, which is
its own answer — the cold is deeper every night and the wood is farther away every day, so "still
going" is not stable and everyone can feel that. If the recap is built, the last thing a run produces
is a short true story of it, assembled from the log the engine already keeps: who went for the
battery, what got burned, what was done to the pilot, which plane missed you, how it ended.

## 4. The design


> **Decided with Andrew, 2026-09-17:** there are **two endings, rescued or dead**. "Walked out" is not an
> ending (the cabin is supplies) and "still going" is gone: **surviving long enough is a rescue path**,
> the hardest, because the search eventually reaches a findable party while the ladder makes every day
> worse. A dead player becomes a **ghost** — moves freely, talks only in the global out-of-character
> chat. The four-ending text below is the September draft, reviewed in block 4.

### 4.1 The four endings (proposal — `events-and-escalation.md` §3)

| ending | what happens | what makes it happen |
|---|---|---|
| **Rescued** | a helicopter on the ice by afternoon, or a plane drops a note | an overflight sees a signal inside a weather window **and** rescue confidence is over the threshold (the additive-confidence model, design 14) |
| **Walked out** | Holt's cabin: the stove, a radio or a snowmachine | the travel route; "we can outlast this" counts as rescue confidence too |
| **Dead** | cold, starvation, a fall through the ice, carbon monoxide in a closed fuselage, the wreck sliding | the survival math, individually or all at once. *Proposed:* the run ends when the last player dies, and a dead player's body persists |
| **Still going** | no cutoff | the ladder is claimed to force an ending within ~two weeks of game time for any party, because cold and food only get worse |

Three properties hold across all four:

- **No ending is a barrier.** Every one of them is reached through the physics — a signal in the air,
  a walk, a core temperature — not through a rule that stops the run.
- **Every ending is honest.** Nothing is scripted to happen on day N; the ladder raises the numbers
  and the party's choices meet them.
- **The run is seeded and replayable** (DR-12): the same run replays the same week, which is what
  makes both the research use and the recap possible.

### 4.2 The recap (proposal, explicitly optional)

**What it is.** A deterministic, auto-generated narrative of the run, assembled at the end from the
run's event log — no language model in it, because there is no language model in the running game
(DR-02). The roadmap's P7 deliverable calls it "the **auto-generated end-of-run recap**
(deterministic, from the run's event log — the optional nice-to-have)".

**What it reads.** The log the moral and social layer already specifies (`moral-social-layer.md` §2):
every applied `ActionResult` with actor, verb, X, Y, tool, tier, zone, world-time, the effects, the
characters who perceived it by band, and the moral tags computed by a pure `moral.tag(...)`. Because
every state change is an Effect through `apply()` (DR-10) and narration may never claim what no Effect
did (DR-11), the log *is* what happened — so a recap built from it cannot flatter or invent.

**What it would name.** The moral pass counts the recap as one of the three diegetic consequences
("physiology, other players' reactions, the recap — never a meter"), and notes that "every dilemma
leaves a trace in the world and the log; the recap can name it". The events pass lists the beats it
would have to draw on: "tracks that circle, a plane that misses you, a wolverine in the cache: these
are stories the recap can name."

**What the roadmap asks of it.** One test: "the recap matches the actual event log (narration↔Effect
at the story level)", and an exit gate where "the recap reads true to what happened".

**Its standing.** Optional. GDD §0b: "Remaining nice-to-haves (genuinely optional — drop freely): a
knowledge/uncertainty layer (believed-vs-true) and an auto-generated end-of-run recap story. Pure
additions." Nothing else in the design depends on it existing.

### 4.3 The end-to-end run the roadmap gates on

P7's exit gate also names a minimal run that must play through: **wake → free yourself → meet the
pilot → salvage a seat → make a fire → improvise a radio antenna → survive / get rescued**. The
roadmap cites this as "§47"; there is no §47 in the current GDD (its anchor map ends at §46) — the
anchor points into the archived original seed (`docs/scenarios/whiteout/design.md` §47, not
authoritative), where it is a longer list of everything a first playable build should let a party do.
The roadmap's one-line version above is what survives into the live docs. It is a smoke test of the
endings, not a script a player is meant to follow.

## 5. Interactions

**Depends on:** rescue paths (14) for the confidence threshold and the weather window that decide
*rescued*, and for the walk-out route; events, escalation and weather (13) for the ladder that makes
"still going" unstable and for the search timeline; time and the clock (06) for what "roughly a week"
means in sittings; injury and first aid (11), warmth (08), water (09) and food (10) for the death
conditions; the moral and social layer (15) for the log the recap reads; multiplayer and instances
(19) for what a run *is* and when one is over; the pilot and bodies (12) for bodies persisting.

**Depended on by:** the agent player and research (20) — a run's end is the boundary of a research
episode, and the log is the artifact; the world-building loops (22) — agents playing to an ending is
how walls get found.

## 6. Open questions

**Q1 — Are these the four endings?**
Options: (a) as listed; (b) fewer — fold "walked out" into "rescued", since both are "you got out";
(c) more — separate "rescued by your own signal" from "found by chance", which the log can already
tell apart.
*Recommendation:* (a). The four are cheap because three of them are just states the systems already
produce, and "walked out" feels different enough to a player to be worth its own name.

**Q2 — "Still going" has no cutoff. Is that right?**
The claim that the ladder forces an ending within ~two weeks is an untested consequence of numbers
that are themselves proposals. Options: (a) no cutoff, trust the ladder; (b) no cutoff, but prove it
— a fuzz that plays the ladder forward and asserts no party survives past day N without rescue;
(c) a soft cutoff (the search is called off; the world says so and the party plays on knowing it).
*Recommendation:* (a)+(b). Andrew's "not permanent" is a property of the numbers, so it should be
checked like one; a cutoff would be exactly the hard time barrier he ruled out.

**Q3 — Does a run end when the last player dies?**
Options: (a) yes — the instance closes, the recap is produced; (b) the world keeps running for a
while (the wolverine finds the cache, the fire goes out) and *then* closes, which costs nothing and
makes a better last page; (c) it stays open indefinitely for inspection.
*Recommendation:* (a) for a friends' run, with (c) available as a research-run setting, since an agent
run may want the terminal state preserved for analysis.

**Q4 — What does a dead player do?**
Nothing is designed for this, and in a co-op run among friends it matters more than it does for the
research use. Options: (a) spectate the surviving party (which leaks information across the perception
model and would need care); (b) watch nothing and wait for the recap; (c) drop back into the run as
another survivor — rejected, there is no roster to draw from and it cheapens the death; (d) stay in
the world as a body with no input, seeing only what that zone would show.
*Recommendation:* ask Andrew directly — this is a social question about his friends' evenings, not a
systems question, and (a) versus (b) is a real trade between boredom and spoilers.

**Q5 — What exactly is the recap, and who is it for?**
Options: (a) a short narrative for the *players* — the story they retell, named beats only; (b) a
structured run report for the *researcher* — the event log summarised along the tags, for comparing
runs; (c) both, from the same log, rendered two ways.
*Recommendation:* (c), built (b)-first if it is built at all. The research use needs the summary
whether or not the story is ever generated, and (a) is a rendering of the same material. Note the
constraint: deterministic assembly only, so the prose quality comes from authored templates over
logged facts, not from generation.

**Q6 — Is reaching Holt's cabin an ending or a new phase?**
Events §3 describes "walked out" as an ending, but also as rescue confidence ("we can outlast this").
Those are different things: a party that reaches a stocked cabin with a stove has not been found, it
has stopped losing. Options: (a) reaching the cabin ends the run; (b) it raises confidence and
survivability and the run continues to one of the other three endings; (c) it ends the run only if
the cabin yields a radio or a snowmachine — a way *out*, not just shelter.
*Recommendation:* (c). It keeps the walk-out honest, prices the cabin's contents, and preserves the
distinction between surviving and being rescued.

## 7. Review log

*
from the proposed endings and the optional recap.*

- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** two endings; surviving long enough is a
  rescue path; ghosts. Q1, Q3, Q6 closed; the recap (Q5) stays for the sitting.

## 8. What exists today

**Nothing is built.** Specifically:

- No ending of any kind is implemented. `game/world/sim/systems/rescue.py` exists as a stub whose
  functions raise `NotImplementedError` ("roadmap P5"); `game/world/sim/systems/clock.py` notes that
  "real warmth/fire/cold-death is P5". There is no death, no rescue, no run-end condition.
- **No event log.** The `server/logs/events.jsonl` that the recap would read is designed in
  `moral-social-layer.md` §2 and does not exist; nothing writes an applied `ActionResult` anywhere.
- **No recap generator**, and no test for one.
- **A run-lifecycle seam exists, and only a seam:** `game/world/scenarios/whiteout/build.py` tags
  everything it loads with `run_id = "slice"`, and the heartbeat and `apply()` carry that tag through
  — so a run is addressable, but there is one hard-coded run and no lifecycle, no reset, no close.

**Designed, not built:** everything in §4.1 and §4.2 — the four endings, the death conditions as
end states, bodies persisting, the log's schema, and the recap.
