# 06 — Time, sleep and the clock

> **Status: reviewed with Andrew 2026-09-18 — every question answered; finalized at the close; fast
> forward set 2026-09-27.** Architecture counterpart:
> [`../architecture/tick-and-scheduler.md`](../architecture/tick-and-scheduler.md) (its basic clock is
> built; its scheduler section predates fast forward and DR-27, and is updated when this design is
> promoted — `PLAN.md` A6) and
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §7
> (DR-14, DR-14b, DR-27). The processes that run on this clock — fire, warmth, drying, hunger,
> thirst, injury, the pilot's body — are designed in their own documents (§5).

## 2. Decisions

### Andrew's decisions

- **A continuously running real-time clock (Andrew's original design, June 2026; DR-14).** Nobody
  can stall it or yank it; the world moves whether or not the party acts. Turn-based time was set
  aside as too clunky for a group playing together.
- **Sleep, a week, and no permanent game (2026-09-07).** Players can sleep. The clock can be moved
  forward when all the players agree, and events can interrupt it. A run is roughly a week of game
  time; rescue can come earlier, and a run can go longer; it is not a permanent game — the escalation
  ladder kills a party that is not rescued.
- **No questions when an activity is interrupted (2026-09-16)** — the clarification-only rule
  (document 04) applied here: no confirmation prompts.
- **The pace (2026-09-17).** The clock always runs faster than real time: **15 game-minutes per real
  minute**. The time controls are taught in the tutorial and are in `help`.
- **The run (2026-09-17, 2026-09-27).** A run is one sitting of two or three hours — about a week of
  game time — which the players can pause and return to. A missing player's character goes
  catatonic, sits down and stares; the others can keep them alive, and they can die. The only endings
  are rescued or dead.
- **Durations and ambience (2026-09-18).** Small attended jobs take one to three game-minutes; bigger
  ones take as long as they honestly do. Ambience comes from the things present, each with its own
  rhythm, not from a room-level timer.
- **Being awake is being on watch (2026-09-18)** — automatically, with no command; awake players
  receive the events sleepers do not.
- **The commands that don't interrupt an activity (2026-09-18):** look, examine, inventory, speech,
  help, status.
- **The build order (2026-09-18):** scheduler → fire → warmth → hunger and thirst → injury → the
  pilot's body and `status`. The bedding and fatigue numbers are valued with the warmth numbers in
  document 08.
- **Fast forward (2026-09-07, 2026-09-17, 2026-09-27).** Proposed and agreed by the players, fast
  forward runs the clock at **about 150×**. Awake players can stay in it, seeing events go by faster, and type a
  command to slow it when they want to act. **A player waking or any non-ambient event drops it back
  to 15×; ambient events do not.** Sleeping players can chat out of character to pass the time. The
  numbers are tuned by playtesting.

### Proposals (Claude)

Everything else here is a proposal, offered because the decisions above need a mechanism to run on:

- the **activity model** (the `Activity` record; deadline in world-time; progress on the world, not
  the actor; one activity per actor; force-interrupt on danger), and the real-second floor;
- the **feedback grammar** (start / tick / interrupt / complete / third-person lines);
- **which events count as ambient** and which do not (§4.2);
- **sleep as a priced resource** (fatigue, the bedding score, the next-day cost);
- `status` showing **bands, never numbers** (the body reported in words is Andrew's, document 08), and
  the meters beside it (2026-09-27; document 08 §4.9);
- the rate limit on lines during fast forward;
- DR-27 (*Activities & processes*), recorded in `implementation-architecture.md` as designed in
  2026-09 and reviewed here before promotion.

## 3. In one paragraph

The clock never stops. While one player saws at a branch, the fire someone lit an hour ago is quietly
burning down, and the tea reaching a boil is a line spoken to the room the moment it happens — nobody
had to ask. If a new command comes in mid-saw, the half-sawn branch stays half-sawn, banked for anyone
to finish; if a wolf howls close by, the saw stops on its own, no questions asked. When the party
settles in to sleep or wait, the players agree to fast forward and the hours blur past — whoever is
still awake watches the fire burn down and the wind rise at ten times the pace, and the sleepers pass
the time chatting out of character — until someone wakes or something happens that matters, and the
world drops back to its normal pace.

## 4. The design

### 4.1 The running clock

The clock runs at **15 game-minutes per real minute** (Andrew, 2026-09-17): one persistent heartbeat
advances the world **one game-minute every 4 real seconds**. Attended actions of one to three
game-minutes take 4–12 real seconds; half an hour of sawing takes two real minutes.

The heartbeat is a single Script, with no `TickerHandler` beside it (the Evennia `turnbattle` and
EvAdventure `reaper` conventions); `utils.delay` only if a sub-tick feedback cadence is ever wanted,
since persistent callbacks must pickle. It is never advanced by a player's action or by chat, and no
one player can stall or yank it for the others. Underneath, the clock is a **deterministic logical
clock**: the wall-clock only decides *when* a tick fires; a pure function of `(state, dt)` decides
*what* it does, with every draw from the per-run seeded RNG — so the fuzzer and replay drive logical
ticks directly and stay byte-reproducible.

**The clock never freezes** (DR-14): the world advances at 15× or in fast forward, never 0×; nobody
can yank it backwards or stall it; the weather and the search run on the calendar regardless
(documents 13 and 14).

### 4.2 Fast forward (Andrew, 2026-09-27)

- **Starting it.** A player proposes it (`propose fast forward`); it runs when the players agree.
- **The pace.** About **150×** — 150 game-minutes per real minute, ten game-minutes a heartbeat. A
  ten-hour night passes in about four real minutes.
- **Awake players can stay in it.** They see the events go by faster (§4.4) and type a command to
  slow it back to 15× when they want to act.
- **What drops it back to 15×:** a player waking, or any **non-ambient** event. Ambient events do not.
- **Sleepers** can chat out of character to pass the time (document 19).
- **The numbers are tuned by playtesting.**

*(Proposed by Claude, for Andrew's check.)* **Ambient** events are the lines the things present speak
on their own rhythm (§4.4, document 05's `sensed` cadence) — the fire crackling and settling, the
creek running, wind gusting against the hull, a raven calling, a spruce dropping its load of snow.
**Non-ambient** events are the ones that change the party's situation: danger (`DANGER`), the fire
dropping to embers, a propagated sound loud enough in band (loudness ≥ 0.5 — wolves close by, the new
ice cracking, a plane), and a sleeper's cold falling below their floor, which wakes them shivering.

### 4.3 Activities with feedback

Two kinds of time ride the same heartbeat. **Attended activities** are what this document designs:
sawing a branch, drilling for an ember, digging, dressing a wound, taking a body's clothes off,
searching a body, the wreckage, a pile or a container a pocket, a compartment or a layer at a time
(2026-09-28) — a start line, a few varied tick
lines driven by state, an interruption that keeps partial progress, a completion line. **Some
activities are open-ended** (2026-09-28): `tend the fire` keeps a fire fed from the wood at hand until
the player stops it, and runs on through fast forward, so nobody has to keep slowing the clock to add a
stick; when it cannot go on — the wood runs out — it stops, says so, and drops the clock back to 15×.
Keeping watch and fishing a line are the same kind. Fighting is not
one of them: nothing in a fight is automatic, and each attack is its own typed act (2026-09-27).
**Unattended processes** are the world's own work; this document names them once, in §5, and their
design lives in other documents.

The activity model (pure `systems/scheduler.py`; state in Attributes):
```
Activity{id, actor, verb, target, tool, started_at (world-min), deadline (world-min), progress_g_or_pct,
         tick_template, interruptible: bool, partial_key}
```
- **Deadline in world-time, progress in Attributes**; remaining = deadline − world_time on every tick
  and after `@reload` (recomputed from the persisted deadline and the world clock, never a wall-clock
  delta or a timer's elapsed estimate).
- **Progress lives on the world, not the actor**: the half-sawn branch carries its own `sawn_pct`;
  anyone can continue it — a co-op property that falls out for free.
- **One activity per actor.** A new command **interrupts** and banks partial progress, except the
  commands that don't (Andrew, 2026-09-18): look, examine, inventory, say/whisper/call/shout, help,
  and `status`. **`busy` ≠ `lagged`**: you can talk while sawing; you can't swing twice.
  In a fight each attack has a recovery — longer after a heavy swing than a jab; the game says when
  you have recovered, and an attack tried before then is answered that you have not recovered yet
  (2026-09-27).
- **Danger force-interrupts** (`DANGER`, `FIRE_STATE_CHANGE` nearby, `SURVIVOR_WORSENS` on you,
  `PLAYER_STOP_REQUEST`) — the most-cited failure mode in this genre is finishing a craft while a
  predator closes in. Any new command interrupts; progress banks where that is physical (the
  half-sawn branch) and is lost where it isn't (the ember dies). No confirmation prompts, no questions
  to the player (Andrew, 2026-09-16).
- **Every tick callback re-checks "am I still the current activity"** (a stale callback is the classic
  async failure mode); cancelling is by activity id.
- **Durations are authored in game-minutes** and converted at schedule time by the live ratio, with a
  real-second floor (≈3 s) so very short beats stay legible. **Small jobs are one to three
  game-minutes** (Andrew, 2026-09-18) — 4–12 real seconds at 15× — so the fiction compresses by
  design; bigger ones are as long as they honestly are — chopping down a standing dead spruce with the
  hatchet is half an hour of game time, two real minutes — and anything genuinely long runs unattended
  as a process while you do something else (§5).

The feedback grammar (content: `responses/activities.py`):

| moment | example (sawing a branch) | rule |
|---|---|---|
| start | *You set to work sawing the low branch.* | always |
| tick (3–5 per activity, proportional) | *Sawdust drifts down.* → *Halfway through, and your arm knows it.* → *The cut yawns; one more pull.* | varied, state-driven, never one string repeated |
| interrupt | *You stop, the branch half-sawn.* (progress banked on the branch: "a half-sawn low branch") | names what remains |
| complete | *The branch drops, and you with it, into the snow.* | the outcome line is the operation's own narration |
| third person | *Agent-1 is sawing at a branch.* / *You hear sawing to the north.* | via the propagator, by band |

### 4.4 The three streams of text, and where ambience comes from (Andrew, 2026-09-18)

While time passes, a player is reading three different things, and they have different rhythms.

**Their own work.** An attended action gives a start line, a few varied tick lines driven by state,
an interruption that names what remains, and a completion line (§4.3).

**The room's ambience, which comes from the things that are there** — not from a room-level timer.
The fire crackles and settles; the creek runs; wind gusts against the hull; a raven calls; a spruce
drops its load of snow. Each of those lines belongs to the *thing*, carried in its ontology row's
`sensed` field with its own cadence (document 05 §4.5), so a fire burning well speaks more often than
embers do, a quiet room is genuinely quiet, and a room with a fire and a creek in it is alive without
anyone authoring a room script. Ambience is the sum of what is present.

**Other people.** Speech and the third-person view of what others are doing arrive whenever they
happen, through the propagator, by band.

**Under a fast forward, the world does not go quiet — it goes fast** (Andrew, 2026-09-18). Whoever is
awake is on watch, and they watch the night run past: the fire burning down, the wind rising, the
wolves somewhere out along the shore. *(Proposed by Claude: lines are rate-limited in real time so the
stream stays readable rather than unspooling three a second.)* Any non-ambient event drops the clock
back to 15× (§4.2). Sleepers see nothing of the world; they can chat out of character, and later they
will be dreaming ([`IDEAS.md`](IDEAS.md)).

### 4.5 Sleep

`sleep` / `rest` / `wait [until dawn | N hours | for <event>]` are unattended processes on the
character: `resting_until` in world-time, and a bedding score from the zone (what you lie on and
under — boughs, foam, the blankets, the sleeping bag; the huddle). A sleeper wakes at their
`resting_until`, or when something wakes them — and a player waking drops a fast forward back to 15×
(§4.2).

**Sleep is a resource with a price** *(proposal)*: fatigue falls only while asleep; sleeping cold
costs warmth per hour (the bedding score sets the rate); a night without sleep costs judgment (slower
activities, worse tick lines) and warmth the next day. The bedding score and the fatigue numbers are
valued with the warmth numbers in document 08 (Andrew, 2026-09-18).

### 4.6 The watch (Andrew, 2026-09-18)

**Being awake is being on watch.** There is no `keep watch` command and nothing to declare: if you
are awake while the others sleep, you are the one who is there. What that buys is perception — **you
receive the events the sleepers do not**: the fire dropping to embers, tracks circling, a plane
somewhere south. You can wake them. A sleeper gets only what is loud enough to wake them, which is
the perception system's own answer (document 19), not a special rule. The watch is a real co-op role:
one tends the fire while the others sleep — `tend the fire`, an open-ended activity that runs through
fast forward (§4.3) — and the fire can be banked to last the night.

### 4.7 Status: numbers as words

`status` (and the inventory footer) turns the numbers into prose: *You are shivering, hungry, and your
left forearm is bleeding into the bandage. The fire is burning low. About four hours of light left.*
Bands, never raw numbers — an agent sees exactly what a human sees; the per-step log carries the actual
numbers for analysis. The meters show the same body at a glance, as bars in the prompt line (document
08 §4.9). `status` is one of the commands that don't interrupt an activity.

### 4.8 The run

A run is **one sitting of two or three hours** covering about a week of game time; the players can
pause it and come back (Andrew, 2026-09-17) — the run pauses when someone in the party types the pause
command, never by itself (2026-09-28). A player who is missing when the run resumes leaves a
character who goes catatonic, sits down and stares; the others can keep them alive, and they can die
(Andrew, 2026-09-27). The run ends in **rescue or death** — never by a timer; walking out is not an
ending. The search reaches a party it can find on day 7 by default, and rescue can come sooner
(document 14 §3.5).

*(Claude's arithmetic, for the playtests to tune:)* with about five active hours a day at 15× and the
rest in fast forward at 150×, a game day takes about 28 real minutes, and a week a little over three
hours.

### 4.9 Why this is core, not later

The fire path becomes a real sequence with tension (the ember dies in two minutes if you don't feed
it). Every dilemma the moral layer raises — the pilot's body, the last ration — becomes a real
decision, because hunger and cold are numbers that hurt. Co-op stops being parallel solitaire: one
saws while the other tends the fire, and the half-sawn branch is anyone's.

## 5. Interactions

**Depends on:** the taught grammar and resolver
([`04-grammar-and-feedback.md`](04-grammar-and-feedback.md)) — an activity only exists because a
resolved attempt returned a duration; the ontology closure mechanism
([`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md), DR-26) — what a tool and material
can even attempt is decided before an activity is ever scheduled; DR-10's Effects/`apply()` — every
tick's progress and every process change is an Effect, nothing here writes state directly; the
perception/propagator model ([`03-the-player-view.md`](03-the-player-view.md), DR-13) — tick lines
route to the actor and degraded third-person lines to bystanders by band.

**Depended on by (the processes):** the unattended processes ride this same heartbeat, each designed
in its own document, not here. **Fire** — a stage ladder, fuel mass consumed per tick by material
burn rate into ash and the environment sink, heat output by stage, stage transitions that interrupt
nearby activities — designed in [`07-fire-and-shaping.md`](07-fire-and-shaping.md). **Warmth** — one
integer core temperature per character, gained and lost by exposure, insulation, fire distance,
activity heat and huddling, banded into words — and **drying** — wetness as grams of water, rising in
snow and falling by a fire — both designed in
[`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md). **Thirst** — hydration
spent per tick and per activity, and eating snow's cost in body heat — designed in
[`09-water.md`](09-water.md). **Hunger** — calories spent per tick and per activity — designed in
[`10-food-and-hunger.md`](10-food-and-hunger.md). **Injury** — named wounds, bleeding, infection after
untreated hours, binding and splinting — designed in
[`11-injury-and-first-aid.md`](11-injury-and-first-aid.md). **The pilot's body** — he starts the run
dead; his body cools, stiffens and freezes over days, smells, and draws the bear and the ravens —
designed in [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md) §4.3a. The escalation ladder
and the weather ([`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md)) and the
flyovers ([`14-rescue-paths.md`](14-rescue-paths.md) §3.5) also run on this clock. Who agrees to a
fast forward, and the out-of-character chat, are the multiplayer document's
([`19-multiplayer-and-instances.md`](19-multiplayer-and-instances.md)).

## 6. Open questions

None open. Every question this document asked was answered on 2026-09-18, and the clock was set on
2026-09-27; both are written into §4.

## 7. Review log

- **2026-09-16** — first draft, from the time-and-stakes design pass and the architecture's clock
  and scheduler.
- **2026-09-17** — with Andrew: the clock always faster than real time, 15 game-minutes per real
  minute, and a fast forward by agreement; a run is one sitting of two or three hours, paused and
  resumed; the time controls taught in the tutorial.
- **2026-09-18** — reviewed in full with Andrew: small jobs at one to three game-minutes and honest
  durations for bigger ones; ambience from the things present; under a fast forward the world runs
  fast for whoever is awake; being awake is being on watch, automatically; the commands that don't
  interrupt; the build order; the bedding and fatigue numbers valued in document 08.
- **2026-09-27** — with Andrew: fast forward at about 150×; awake players can stay in it and slow it
  to act; a player waking or a non-ambient event drops it to 15×, ambient events do not; sleepers chat
  out of character; the numbers tuned by playtesting; a missing player's character goes catatonic.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built.** [`game/typeclasses/heartbeat.py`](../../game/typeclasses/heartbeat.py) — a persistent global
Script, `interval = 15` real seconds, advancing the world clock by `dt=1` game-minute per tick through
the allow-listed `apply()` writer, then propagating any events. This is the basic P1 clock; its pace
(4 game-minutes per real minute) is not yet the design's 15 (a 4-second heartbeat — `PLAN.md` E1).
[`game/world/sim/systems/clock.py`](../../game/world/sim/systems/clock.py) — the pure `tick(dt,
world_time)` function; deterministic; currently returns no consequential events (a placeholder).
[`game/world/sim/events.py`](../../game/world/sim/events.py) — the `INTERRUPT_SIGNALS` frozenset
(`FIRE_STATE_CHANGE`, `SURVIVOR_WORSENS`, `WEATHER_CHANGE`, `SCRIPTED_TRIGGER`, `RESCUE_SIGNAL`,
`DANGER`, `PLAYER_STOP_REQUEST`) is defined and exported.

**Designed, not built.** `game/world/sim/systems/scheduler.py` documents the `Activity` shape in its
docstring but `advance()` raises `NotImplementedError("systems.scheduler.advance — roadmap P4")` — no
activity is ever actually created, ticked, or interrupted yet. `events.should_interrupt()` likewise
raises `NotImplementedError` (roadmap P4) — nothing consumes `INTERRUPT_SIGNALS` yet. The process stub
files `game/world/sim/systems/{fire,water,shelter,weather}.py` are bare docstrings (roadmap P5); no
`Activity` dataclass exists in `contracts.py`. `responses/activities.py` (the feedback-grammar
templates) does not exist — the scenario's narration currently lives in one file,
`game/world/scenarios/whiteout/responses/slice.py`.

**Nothing.** `sleep`, `rest`, `wait`, fast forward and the command that slows it, the out-of-character
chat for sleepers, the bedding score and fatigue — no verb handlers, no Attributes, no commands exist
anywhere in `game/commands/` or `game/world/sim/operations/handlers/` for any of this.
`game/world/sim/systems/warmth.py` is substantially built (177 lines: `wearable`, `insulation_units`,
`warmth_band`, …) but that is the clothing/insulation math of DR-25, owned by document 08 — it is not
the per-tick core-temperature process §5 points to, which still has no code at all.
