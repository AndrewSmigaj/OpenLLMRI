# 06 — Time, sleep and the clock

> **Status: draft for review.** Architecture counterpart:
> [`../architecture/tick-and-scheduler.md`](../architecture/tick-and-scheduler.md) (its basic clock is
> built; its scheduler section predates DR-14a — see *The design* §3 below) and
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §7
> (DR-14, DR-14a, DR-27). Sources:
> [`../investigation/design/time-and-stakes.md`](../investigation/design/time-and-stakes.md) §1, §2, §3,
> §5, §6, §7, §8 and the two architecture documents above. §4 of that pass (the processes: fire, warmth,
> hunger, injury, drying, the pilot) belongs to other documents — see *Interactions* below.

## Provenance

### Andrew's decisions
- **The clock itself is his original design**, locked before the September sessions and kept as
  written (GDD §0b: "the June text below is kept as written"): **a continuously running real-time
  clock** that nobody can stall or yank — the world moves whether or not the party acts.
- **(2026-09-07, amending DR-14/DR-15 — `time-and-stakes.md` §8).** "Andrew's decisions: players can
  **sleep**; there is a way to **move the clock forward if ALL players agree**, and **events can
  interrupt it**; the run is **roughly a week**, rescue can come earlier, and it can run longer until
  the food runs out — not a permanent game: the escalation ladder... kills a party that is not
  rescued."
- **(2026-09-16 — the watch rule, `time-and-stakes.md` §8 / `00-provenance-audit.md` §4).** A single
  player who keeps acting holds the clock at 1× for everyone — decided by Andrew: "**the others wait
  for the next event, such as someone waking, and do something else meanwhile**" — the watch is a real
  co-op role (one tends the fire while three sleep; the fire can be banked to last the watch).
- **Clarification-only feedback (2026-09-16, general rule, applied here).** No confirmation prompts, no
  questions to the player when an activity is interrupted; the "uninterruptible + confirm" idea was
  Claude's and is dropped.

### Proposals (Claude)
Everything else in this document is a proposal, offered because Andrew's decisions above need a
mechanism to run on:
- the **activity model** (the `Activity` record; deadline in world-time; progress on the world, not the
  actor; one activity per actor; force-interrupt on danger);
- **durations** in game-minutes (1–3 for attended actions) and the real-second floor;
- the **feedback grammar** (start / tick / interrupt / complete / third-person lines);
- the **non-interrupting command whitelist** (look, examine, inventory, say/whisper/call/shout, help,
  status);
- the mechanics of the **consensus advance** (the 20× multiplier and its specific list of interrupting
  conditions) and of **sleep as a priced resource** (fatigue, the bedding score, the next-day cost) —
  these operationalize Andrew's "sleep" and "moves forward if all agree" decisions but the numbers and
  triggers are Claude's;
- `status` showing **bands, never numbers**;
- the **build order** inside step 3 (`time-and-stakes.md` §7).
DR-27 itself (*Activities & processes*) is recorded in `implementation-architecture.md` as "designed
2026-09; promoted with the time-and-stakes pass" — i.e. a proposal, not one of Andrew's decisions.

## In one paragraph
The clock never stops. While one player saws at a branch, the fire someone lit an hour ago is quietly
burning down, and the tea reaching a boil is a line spoken to the room the moment it happens — nobody
had to ask. If a new command comes in mid-saw, the half-sawn branch stays half-sawn, banked for anyone
to finish; if a wolf howls close by, the saw stops on its own, no questions asked. When the whole party
stops to sleep or wait, hours blur past in a breath — until the fire drops to embers, or something loud
enough happens nearby, and the world snaps back to real pace. If one person keeps acting while the
others try to sleep, the clock holds at its normal pace for everyone; the others wait for the next thing
to happen and get on with something else in the meantime.

## The design


> **Decided with Andrew, 2026-09-17 (supersedes the "20× by consensus" and any "watch rule" wording below):**
> the clock always runs faster than real time — **15 game-minutes per real minute** (X); `propose fast
> forward` raises it to **180×** (Y) when every player agrees; events drop it back to X; a player who
> does not agree keeps it at X. Time controls are taught in the pre-scenario tutorial and are in `help`.
> A run is **one sitting of two or three hours** covering roughly a week of game time (about 26 real
> minutes per game day at X/Y with five active hours a day); halt and resume allowed; a member missing
> at resume is incapacitated where they lie. The heartbeat ticks every 4 real seconds (one game-minute).
> Attended actions of one to three game-minutes take 4–12 real seconds; half an hour of sawing takes
> two real minutes. The section below is the September draft and is reviewed in block 2.

### The running clock
One persistent heartbeat drives everything: **15 real-seconds → +1 game-minute** (verified against the
Evennia `turnbattle` and EvAdventure `reaper` conventions — a single Script, no `TickerHandler` beside
it; `utils.delay` only if a sub-tick feedback cadence is ever wanted, since persistent callbacks must
pickle). It is never advanced by a player's action or by chat, and no one player can stall or yank it
for the others — turn-based time was considered and set aside as too clunky for a group playing
together. Underneath, the clock is a **deterministic logical clock**: the wall-clock only decides
*when* a tick fires; a pure function of `(state, dt)` decides *what* it does, with every draw from the
per-run seeded RNG — so the fuzzer and replay drive logical ticks directly and stay byte-reproducible.

### Activities with feedback
Two kinds of time ride the same heartbeat. **Attended activities** are what this document designs:
sawing a branch, drilling for an ember, digging, dressing a wound, fighting — a start line, a few
varied tick lines driven by state, an interruption that keeps partial progress, a completion line.
**Unattended processes** are the world's own work; this document names them once, under
*Interactions*, and their design lives in other documents.

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
- **One activity per actor.** A new command **interrupts** and banks partial progress, except a
  whitelist that doesn't: look, examine, inventory, say/whisper/call/shout, help, and `status`.
  **`busy` ≠ `lagged`**: you can talk while sawing; you can't swing twice.
- **Danger force-interrupts** (`DANGER`, `FIRE_STATE_CHANGE` nearby, `SURVIVOR_WORSENS` on you,
  `PLAYER_STOP_REQUEST`) — the most-cited failure mode in this genre is finishing a craft while a
  predator closes in. Any new command interrupts; progress banks where that is physical (the
  half-sawn branch) and is lost where it isn't (the ember dies). No confirmation prompts, no questions
  to the player.
- **Every tick callback re-checks "am I still the current activity"** (a stale callback is the classic
  async failure mode); cancelling is by activity id.
- **Durations are authored in game-minutes** and converted at schedule time by the live ratio, with a
  real-second floor (≈3 s) so very short beats stay legible. Attended actions are proposed at
  **1–3 game-minutes** (15–45 real seconds) so the fiction compresses by design; anything longer
  becomes a process instead (see *Interactions*).

The feedback grammar (content: `responses/activities.py`):

| moment | example (sawing a branch) | rule |
|---|---|---|
| start | *You set to work sawing the low branch.* | always |
| tick (3–5 per activity, proportional) | *Sawdust drifts down.* → *Halfway through, and your arm knows it.* → *The cut yawns; one more pull.* | varied, state-driven, never one string repeated |
| interrupt | *You stop, the branch half-sawn.* (progress banked on the branch: "a half-sawn low branch") | names what remains |
| complete | *The branch drops, and you with it, into the snow.* | the outcome line is the operation's own narration |
| third person | *Agent-1 is sawing at a branch.* / *You hear sawing to the north.* | via the propagator, by band |

### Sleep and the consensus advance
`sleep` / `rest` / `wait [until dawn | N hours | for <event>]` are unattended processes on the
character: `resting_until` in world-time, a bedding score from the zone (what you lie on and under —
boughs, foam, the blanket, the sleeping bag; the huddle), and a watch flag.

**Consensus advance (DR-14a):** when every connected character in the run is resting or waiting, the
heartbeat runs at **20× dt** (one real tick = 20 game-minutes) until the earliest `resting_until` or an
**interrupting event**: cold below the character's floor (you wake shivering), the fire reaching
`embers`, any propagated Event with loudness ≥ 0.5 in band (wolves, the ice booming, a plane), `DANGER`,
or a player's own command.

> The architecture counterpart, `tick-and-scheduler.md`, still says: *"There is no planning-mode freeze
> and no consensus fast-forward — both were the [turn-driven] flavour we rejected."* That line predates
> Andrew's 2026-09-07 decision; DR-14a supersedes it. The clock still never freezes (0× never happens),
> but it now runs at 20× by consensus — `tick-and-scheduler.md` wants an update to match.

**Sleep is a resource with a price:** fatigue falls only while asleep; sleeping cold costs warmth per
hour (the bedding score sets the rate); a night without sleep costs judgment (slower activities, worse
tick lines) and warmth the next day.

**The clock never freezes** (DR-14 holds): the world advances at 1× or 20×, never 0×; nobody can yank
it backwards or stall it; the storm and the search run on the calendar regardless.

**The run length (DR-15a):** the instance persists across sittings for roughly a week of game time; it
ends by rescue, walk-out, or the last death — never by a timer.

### The watch
When one player keeps acting while others sleep or wait, the clock holds at its normal 1× — it does
not fall back to 20× just because most of the party is down. The others wait for the next event (such
as someone waking) and do something else meanwhile. This makes the watch a real co-op role: one tends
the fire while three sleep, and the fire can be banked to last through it.

### Status: numbers as words
`status` (and the inventory footer) turns the numbers into prose: *You are shivering, hungry, and your
left forearm is bleeding into the bandage. The fire is burning low. About four hours of light left.*
Bands, never raw numbers — an agent sees exactly what a human sees; the per-step log carries the actual
numbers for analysis.

### Why this is core, not later
The fire path becomes a real sequence with tension (the ember dies in two minutes if you don't feed
it). Every dilemma the moral layer raises — the pilot's body, the blanket for the dying man, the last
ration — becomes a real decision, because hunger and cold are numbers that hurt. Co-op stops being
parallel solitaire: one saws while the other tends the fire, and the half-sawn branch is anyone's.

## Interactions
**Depends on:** the taught grammar and resolver
([`04-grammar-and-feedback.md`](04-grammar-and-feedback.md)) — an activity only exists because a
resolved attempt returned a duration; the ontology closure mechanism
([`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md), DR-26) — what a tool and material
can even attempt is decided before an activity is ever scheduled; DR-10's Effects/`apply()` — every
tick's progress and every process change is an Effect, nothing here writes state directly; the
perception/propagator model ([`03-the-player-view.md`](03-the-player-view.md), DR-13) — tick lines
route to the actor and degraded third-person lines to bystanders by band.

**Depended on by (the processes, `time-and-stakes.md` §4):** five unattended processes ride this same
heartbeat, each designed in its own document, not here. **Fire** — a stage ladder, fuel mass consumed
per tick by material burn rate into ash and the environment sink, heat output by stage, stage
transitions that interrupt nearby activities — designed in
[`07-fire-and-shaping.md`](07-fire-and-shaping.md). **Warmth** — one integer core temperature per
character, gained and lost by exposure, insulation, fire distance, activity heat and huddling, banded
into words — and **drying** — wetness as grams of water, rising in snow and falling by a fire — both
designed in [`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md). **Hunger and
thirst** — integer calories and hydration spent per tick and per activity, snow-eating's heat cost —
designed in [`10-food-and-hunger.md`](10-food-and-hunger.md). **Injury** — named wounds, bleeding,
infection after untreated hours, binding and splinting — designed in
[`11-injury-and-first-aid.md`](11-injury-and-first-aid.md). **The pilot** — a scripted process ending
within the first day, tended like any other physical thing — designed in
[`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md). The escalation ladder
([`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md)) and the rescue weather
window ([`14-rescue-paths.md`](14-rescue-paths.md)) also run on this clock.

## Open questions
1. **The non-interrupting command whitelist.** Proposed: look, examine, inventory,
   say/whisper/call/shout, help, status. *Options:* adopt as-is; or add/remove verbs as play surfaces
   ones that should stay silent but currently interrupt (e.g. should checking `examine me` mid-activity
   really cost nothing?). *Recommendation:* adopt as the default (it is already the defined-but-unapproved
   default per the provenance audit) and revise only against a concrete case that comes up in play.
2. **The 1–3 game-minute attended range and the process chatter cadence.** Proposed: 15–45 real
   seconds per attended action; a process line every 5–10 game-minutes so waiting by a fire isn't
   silence. *Options:* keep as the starting tunable; widen or narrow after feel. *Recommendation:* keep
   as proposed and revisit only after the first modelled night (the acceptance test in the design
   source's §7), not in the abstract.
3. **The step-3 build order.** `time-and-stakes.md` §7 proposes: (1) scheduler + activities for the
   verbs that already take time, the whitelist, force-interrupt on danger; (2) fire as a process;
   (3) warmth; (4) hunger/thirst; (5) injury; (6) the pilot's clock + `status`. *Options:* keep this
   order; or reorder. *Recommendation:* keep — it already matches the roadmap's own split (the
   scheduler is P4; fire/warmth/hunger/injury/the pilot are P5), so reordering would cost a second
   sequencing conversation for no evident gain.
4. **The bedding score and fatigue numbers.** Named (boughs, foam, blanket, sleeping bag; the huddle;
   "a night without sleep costs judgment") but not valued anywhere in the sources. *Recommendation:*
   value them alongside 08's warmth numbers, since the bedding score is really a warmth-loss-rate
   input.
5. **How the watch is held.** The sources name a "watch flag" on the sleep/rest process but don't say
   how it's set. *Options:* automatic (whoever is still acting is on watch by definition); an explicit
   command (`keep watch`) that a player must issue to be exempted from the sleep processes'
   fatigue-recovery clock. *Recommendation:* automatic first (it falls out of "a single player who
   keeps acting holds the clock"); add an explicit command only if a player wants to sleep lightly
   *and* be woken preferentially, which the sources don't yet ask for.

## Review log
2026-09-16 — first draft, written from `time-and-stakes.md` §1–3/§5–8, `tick-and-scheduler.md` and
`implementation-architecture.md` §7. 


- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** X = 15, Y = 180, `propose fast forward`
  by consensus, events interrupt; one sitting of two or three hours; halt/resume; "watch rule" was
  Claude's label and is dropped. The rest of this document is reviewed in block 2.

## What exists today
**Built.** [`game/typeclasses/heartbeat.py`](../../game/typeclasses/heartbeat.py) — a persistent global
Script, `interval = 15` real seconds, advancing the world clock by `dt=1` game-minute per tick through
the allow-listed `apply()` writer, then propagating any events. This is the basic, P1 clock.
[`game/world/sim/systems/clock.py`](../../game/world/sim/systems/clock.py) — the pure `tick(dt,
world_time)` function; deterministic; currently returns no consequential events (a placeholder).
[`game/world/sim/events.py`](../../game/world/sim/events.py) — the `INTERRUPT_SIGNALS` frozenset (the
seven event kinds named above) is defined and exported.

**Designed, not built.** `game/world/sim/systems/scheduler.py` documents the `Activity` shape in its
docstring but `advance()` raises `NotImplementedError("systems.scheduler.advance — roadmap P4")` — no
activity is ever actually created, ticked, or interrupted yet. `events.should_interrupt()` likewise
raises `NotImplementedError` (roadmap P4) — nothing consumes `INTERRUPT_SIGNALS` yet. The process stub
files `game/world/sim/systems/{fire,water,shelter,weather}.py` are bare docstrings (roadmap P5); no
`Activity` dataclass exists in `contracts.py`. `responses/activities.py` (the feedback-grammar
templates) does not exist — the scenario's narration currently lives in one file,
`game/world/scenarios/whiteout/responses/slice.py`.

**Nothing.** `sleep`, `rest`, `wait`, the watch flag, the consensus advance, the bedding score and
fatigue — no verb handlers, no Attributes, no commands exist anywhere in `game/commands/` or
`game/world/sim/operations/handlers/` for any of this. `game/world/sim/systems/warmth.py` is
substantially built (177 lines: `wearable`, `insulation_units`, `warmth_band`, …) but that is the
clothing/insulation math of DR-25, owned by document 08 — it is not the per-tick core-temperature
process this document's *Interactions* section points to, which still has no code at all.
