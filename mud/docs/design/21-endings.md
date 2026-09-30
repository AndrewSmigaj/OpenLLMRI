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
  same flyovers every run (2026-09-17, 2026-09-27; document 14 §3).
- **Ghosts** (2026-09-17, 2026-09-27): a dead player becomes a ghost and moves freely. Ghosts hear
  one another; the living do not hear ghosts. Anyone, living or dead, can use the out-of-character
  chat.
- **The run ends at its endings; there is no recap** (2026-09-27).
- **Endings per person, rescue per group** (2026-09-28): an ending belongs to a person, and the run is
  over when nobody is left alive in the valley; a pass rescues whoever is findable, as real searches
  go, by helicopter on solid ground. **A rescued player still gets to hang out**, in the lobby.
- **The game ends on day 7** (2026-09-29): the rescuers find everyone still alive; a rescuer entering a
  room with characters rescues them, and they are transported to the lobby. The early ways home get
  out sooner, and the last 24 hours are the hardest (§4.3).
- **The lobby** (2026-09-29): a small room inside the simulation — windows, couches, warm drinks —
  where the rescued and the dead are back in their own bodies, look up their character, talk, go back
  in as silent watchers, and are offered a T-shirt by a polite robot (§4.5).

### Proposals (Claude)

- Where the rescuers walk is the game's rules, and what they say a small model (§4.3).
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
anything). An ending belongs to a person (2026-09-28).

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

### 4.3 Rescue (Andrew, 2026-09-28, 2026-09-29)

**The game ends on day 7** (Andrew, 2026-09-29). That morning the helicopter comes for everyone still alive — the survived-long-enough rescue — and its crew find the people wherever they are: when a rescuer enters a room with any characters in it, they get the *you are rescued* text and are transported to the lobby, still in the simulation. Everyone alive is rescued; nobody is left out and no extra storm or bad weather is needed. The early ways home — the radio, a signal a plane sees — bring the helicopter sooner, and a party that can speedrun it gets out sooner. For those early routes to be worth the work, **the last 24 hours before the day-7 rescue are the hardest of the run** — the day-6 flurry and the coldest night (document 13 §4.2). *(Proposed by Claude, for Andrew's check:)* where the rescuers walk is the game's own rules, so they always reach everyone — the helicopter's thermal camera shows a warm body through the trees — and what they say is played by a small language model, so the rescue never depends on how well the model does.

An early rescue finds whoever is findable at that moment — at the wreck, at the cabin, or under a
signal (document 14 §3); real searchers who find part of a party learn from them where the rest went,
and the crew go to them the same way.

The pickup is a helicopter setting down on solid ground — the wreck's clearing, a gravel bar, the
shore. A lake that is skinning over with new ice takes neither floats nor skis (document 13 §4.2).

### 4.4 When the sitting ends first

Someone alive and unrescued when the sitting ends: someone in the party types `pause game`, and the
run is resumed like any other (Andrew, 2026-09-17, 2026-09-27, 2026-09-28). No run goes past day 7.

### 4.5 Ghosts (Andrew, 2026-09-17, 2026-09-27)

A dead player becomes a **ghost** and moves freely. **Ghosts hear one another; the living do not hear
ghosts. Anyone, living or dead, can use the out-of-character chat** (document 19 §4.8).

**The lobby** (Andrew, 2026-09-28, 2026-09-29) — the name is still to be chosen. A player who is rescued or dies is transported there: a small room inside the simulation, with windows, a couple of couches and warm things to drink. Players are back in their own bodies. There are displays where they look up information about their character; a sign gives the command to go back into the simulation as a silent watcher — through its door they move around the world at a quick speed, seeing everyone, acting on nothing, heard only by the others watching; they talk to each other in the room itself, or stay in the chat; and there are a few fun things to do, still to be designed. A polite robot, played by a language model, offers each of them a T-shirt — one about surviving or one about dying, by how they got there.

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
- **2026-09-29 (Andrew):** the game ends on day 7 — the rescuers find everyone still alive, and a
  rescuer entering a room rescues whoever is in it; early routes get out sooner; the last 24 hours are
  the hardest; the lobby, with its displays, its sign, its silent-watcher door and a T-shirt from a
  polite robot; nothing after day 7.

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
