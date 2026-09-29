# 21 — Endings

> **Status: draft for review.** Architecture counterpart: none — the run lifecycle is DR-15/DR-15a in
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) §2. `PLAN.md` E14 builds the endings.

The endings — rescued or dead — and what a dead player becomes: a ghost.

## 2. Decisions

### Andrew's decisions

- **Two endings: rescued or dead** (2026-09-17). Walking out is not an ending — Holt's cabin is
  supplies. Surviving long enough is one of the ways of being rescued, and the hardest (2026-09-17).
- **The run ends when they die, of anything** (2026-09-26).
- **What kills** (2026-09-27): **nothing kills instantly** — death comes by the body running down, on
  real clocks, with time to respond; the bear and a knife kill through the bleeding they cause. Poison
  makes people very sick but never kills. Dangerous places injure but never kill outright.
- **A run is about a week of game time in one sitting of two or three hours**, which the players can
  pause and return to (2026-09-17, 2026-09-27).
- **No hard time barriers** (2026-09-07): rescue can come earlier than the week's end; instead of
  time-window barriers, the things that cause death increase, so a party that is not rescued dies
  honestly. There is no set arc — what to do is the players' decision.
- **Rescue comes three ways** — the radio, a signal a plane can see, surviving long enough — with the
  same flyovers every run and the default rescue on day 7 (2026-09-17, 2026-09-27; document 14 §3).
- **Ghosts** (2026-09-17, 2026-09-27): a dead player becomes a ghost and moves freely. Ghosts hear
  one another; the living do not hear ghosts. Anyone, living or dead, can use the out-of-character
  chat.
- **The run ends at its endings; there is no recap** (2026-09-27).

### Proposals (Claude)

- An ending belongs to a person; the run is over when nobody is left alive in the valley (§4.1).
- Rescue per findable group, as real searches go (§4.3); the pickup by helicopter on solid ground.
- After day 7 nothing is a cutoff: passes continue while the weather allows (§4.4).
- Two properties checked like the numbers they are: the day-7 rescue reaches every findable party,
  and the ladder closes on a party that stays unfindable (§4.4).
- What a ghost sees and does beyond Andrew's decision (§4.5).

## 3. In one paragraph

A run ends one of two ways, and neither is a clock running out. Either you are found — a faint voice on
the radio that wants to know where you are and says they will come at the next daylight good for flying;
smoke a search plane can see, got up in the time between hearing its engines and seeing it; or, hardest
of all, staying alive and findable until the search reaches you on the seventh day — and a helicopter
sets down near you. Or you die: of the cold, of blood loss, or to the bear. Death comes one person at a
time. Whoever dies becomes a ghost, drifting through the valley, heard only by the other ghosts, and the
run is over when nobody is left alive there. Reaching Holt's cabin is not an ending — it is a stove,
some stores and a roof, and somewhere findable to wait.

## 4. The design

### 4.1 Two endings (Andrew, 2026-09-17)

Each player's run ends **rescued** or **dead**. The run is over when no player is left alive in the
valley — all rescued, all dead, or some of each (Andrew, 2026-09-26: the run ends when they die, of
anything). *(The per-person reading is proposed by Claude, for Andrew's check.)*

Three properties hold for both:

- **No ending is a barrier.** Each is reached through the physics — a signal in the air, a voice on
  the radio, a body's state — not through a rule that stops the run.
- **Every ending is honest.** The search comes on its schedule (document 14 §3.5) to a party that can
  be found; death comes from the state of a body. The ladder raises the danger (document 13) and the
  party's choices meet it.
- **The run is seeded and replayable** (DR-12): the same run replays the same week, which is what the
  research uses (document 20). The final state of any run can be rebuilt from its seed and its
  commands whenever it is wanted.

### 4.2 Death (Andrew, 2026-09-26, 2026-09-27)

Death is not something this document decides. It is a body's state crossing the line in the system
that reaches it — **nothing kills instantly** (2026-09-27): death comes by the body running down on a
real clock, so a player always has time to respond. **The cold** (warmth and the heat system —
document 08), **blood loss** (wounds — document 11, and the combat system, still to be written,
`PLAN.md` A10; the bear and a knife kill this way), **thirst** (document 09), a wound's infection, a
bleed inside the skull, carbon monoxide (document 11 §4.6). Each owning system draws its line from
physiology; this document only reads that a body died.

Two things never kill: poison makes a person very sick (document 23 — the baneberry, the water
hemlock, the deadly galerina), and dangerous places — thin ice, a fall — injure and never kill
outright.

### 4.3 Rescue, per findable group *(proposed by Claude, for Andrew's check)*

A pass finds whoever is findable at that moment — at the wreck, at the cabin, or under a signal
(document 14 §3). Real searchers who find part of a party learn from them how many were aboard and
where the rest went, and search on from there. So a group found first is rescued and tells the
searchers, and the rest are found at the next pass if they are findable there. A rescued player leaves
the valley; while others still play, they stay in the out-of-character chat, which anyone can use.

The pickup is a helicopter setting down on solid ground — the wreck's clearing, a gravel bar, the
shore. A lake that is skinning over with new ice takes neither floats nor skis (document 13 §4.2).

### 4.4 After day 7, and when the sitting ends first *(proposed by Claude, for Andrew's check)*

- **After day 7, nothing is a cutoff.** The flyover schedule is the rescue clock (document 14 §3.5),
  and day 7 is the default rescue for a party that can be found. After it, if they are not found,
  passes continue while the weather allows, each a chance, as real searches go: a search is scaled
  back, but traffic does not stop. The 1963 search for Helen Klaben and Ralph Flores, down in a Yukon
  winter, was called off within about two weeks, and a passing bush plane saw their SOS in a clearing
  on day 49. The world never announces that a search is suspended; the planes simply come less often,
  which the party hears.
- **A party that stays unfindable meets the ladder** (document 13) — and real life is the caution:
  Klaben and Flores lived 49 days on almost no food, so hunger alone does not end a week; it is the
  deepening cold, wet, injury and exhaustion together that close in. Two properties are checked like the
  numbers they are: **the day-7 rescue reaches every findable party** (`PLAN.md` E14's fuzz), and **the
  ladder closes on an unfindable party**. The second is measured, not assumed; if the fuzz finds
  competent unfindable parties outliving the sitting, that is a finding for the ladder, never a reason
  for a cutoff.
- **When the sitting ends first**, with someone alive and unrescued, someone in the party types the pause
  command, and the run is resumed like any other (Andrew, 2026-09-17, 2026-09-27, 2026-09-28).

### 4.5 Ghosts (Andrew, 2026-09-17, 2026-09-27)

A dead player becomes a **ghost** and moves freely. **Ghosts hear one another; the living do not hear
ghosts. Anyone, living or dead, can use the out-of-character chat** (document 19 §4.8).

What follows from the rest of the design *(proposed by Claude, for Andrew's check)*:

- **A ghost sees everyone** (Andrew, 2026-09-28), a hidden person included, and otherwise what anyone
  standing where it is would see — the same composed look, banded by the same perception, weather and
  darkness included (document 03; an agent sees what a human sees, and so does a ghost). Nothing else
  extra: no view into closed things, no party-wide status, no map of caches.
- **It moves unhindered** — no terrain, snow, cold or hunger slows it; it has no body.
- **Its body stays where it died**, clothed, pockets full: mass is never lost (DR-11). What the living
  may do with it is documents 12 and 15, and that the ghost may be watching is part of it.
- **It cannot act on the world** — no Effects, and nobody alive perceives it. In the log it is a
  perceiver of its own kind, recorded apart from `witnessed_by`, because it cannot testify inside the
  world (document 15).

### 4.6 The end-to-end run the roadmap gates on

P7's exit gate names a minimal run that must play through: **wake → free yourself → find the pilot's
body → salvage a seat → make a fire → improvise a radio antenna → be rescued**. It is a smoke test of
the endings, not a script a player is meant to follow.

## 5. Interactions

**Depends on:** rescue (14) — the three ways, the voice, the flyover schedule and the day-7 rescue;
events, escalation and weather (13) — the ladder and the weather the search flies in; time and the
clock (06) — the week in one sitting, and pausing; the systems that kill — warmth (08) for the cold,
injury and first aid (11) for blood loss, infection and the rest, water (09) for thirst, the bear (23)
and the combat system (no document yet, `PLAN.md` A10), the heat system (no document yet) for carbon
monoxide; the systems that hurt without killing — food (10) and the poisons (23); multiplayer and instances (19) — what a run
is, the out-of-character chat and the perception a ghost sees by; the pilot and bodies (12) — bodies
persist; the moral and social layer (15) — the log and who witnessed what.

**Depended on by:** the agent player and research (20) — a run's end is the boundary of a research
episode; the world-building loops (22) — agents playing to an ending is how walls get found.

## 6. Open questions

None open.

## 7. Review log

- **2026-09-17 (Andrew):** two endings, rescued or dead; the walk-out is not an ending and the cabin is
  supplies; surviving long enough is a way of being rescued; a dead player is a ghost.
- **2026-09-26 (Andrew):** the run ends when they die, of anything.
- **2026-09-26 (Claude, self-review):** answered for Andrew's check — endings per person, rescue per
  findable group, nothing a cutoff after day 7, the ladder measured by the fuzz; what a ghost sees and
  does.
- **2026-09-27 (Andrew):** there is no recap; ghosts hear ghosts, the living cannot, and anyone can use
  the out-of-character chat; nothing kills instantly — death comes by the body running down.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Nothing is built.** Specifically:

- No ending of any kind is implemented. `game/world/sim/systems/rescue.py` exists as a stub whose
  functions raise `NotImplementedError` ("roadmap P5"); `game/world/sim/systems/clock.py` notes that
  "real warmth/fire/cold-death is P5". There is no death, no rescue, no run-end condition.
- No event log: nothing writes an applied `ActionResult` anywhere (the log is designed in document 20
  §4.4).
- A run-lifecycle seam exists, and only a seam: `game/world/scenarios/whiteout/build.py` tags
  everything it loads with `run_id = "slice"`, and the heartbeat and `apply()` carry that tag through
  — so a run is addressable, but there is one hard-coded run and no lifecycle, no pause, no close.

**Designed, not built:** the two endings as end conditions, per person; death as each system's line;
bodies persisting; rescue per findable group; ghosts. Nothing of the ghost exists — no state for a
dead player, no free movement, no ghost-to-ghost hearing; the out-of-character channel typeclass is
Evennia's stock one in `game/typeclasses/channels.py`.
