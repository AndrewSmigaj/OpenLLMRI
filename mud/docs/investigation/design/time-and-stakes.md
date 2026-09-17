# Time & stakes — activities with feedback, processes on the clock, and the numbers that make choices real

> **Merged into `docs/design/06-time-sleep-and-the-clock.md` (and 08, 10, 11, 12 for its §4 processes) on 2026-09-16 — that document is the design of record;**
> this file is kept as the source it was merged from and is not maintained. Corrections go there.

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07).** Realizes DR-14's P4
> design (the scheduler) and the first slice of P5 (fire ladder, warmth, hunger, injury) as ONE
> designed step (step 3), because without stakes there are no decisions. Grounded in the timed-action
> research (Diku/LPMud/Achaea/Discworld conventions; The Long Dark and Project Zomboid's interrupt
> lessons) and the Evennia source read in the pinned image. Promotes to `docs/architecture/
> time-and-stakes.md` + DR-27 on approval. Fire's ignition/shaping side is in `fire-and-shaping.md`.

## 1. Two kinds of time
- **Attended activities** — you are busy: sawing a branch, drilling for an ember, digging, dressing a
  wound, fighting. A start line, a few varied tick lines driven by state, an interruption that keeps
  partial progress, a completion line. Bystanders see the third-person version by band.
- **Unattended processes** — the world's own work: a fire burns down, snow melts in a tin, matches
  dry by the fire, the pilot fades, cold creeps into a wet sleeve, a wound bleeds. They speak only at
  state changes, and some of those changes INTERRUPT attended activities (`events.INTERRUPT_SIGNALS`).

Both ride the **one persistent heartbeat Script** (15 real-s → +1 game-min; verified idiomatic —
`turnbattle` and the EvAdventure reaper do the same). No TickerHandler beside it; `utils.delay` only
if a sub-tick feedback cadence is ever wanted (persistent callbacks must pickle).

## 2. The activity model (pure `systems/scheduler.py`; state in Attributes)
```
Activity{id, actor, verb, target, tool, started_at (world-min), deadline (world-min), progress_g_or_pct,
         tick_template, interruptible: bool, partial_key}
```
- **Deadline in world-time**, progress in Attributes; remaining = deadline − world_time on every tick
  and after `@reload` (`at_start` recompute — triple-confirmed idiomatic). Never a wall-clock delta.
- **Progress lives on the world, not the actor**: the half-sawn branch carries `state["sawn_pct"]`;
  anyone can continue it (a small co-op property that falls out for free).
- **One activity per actor.** A new command **interrupts** and banks partial progress, except a
  whitelist that doesn't (look, examine, inventory, say/whisper/call/shout, help, and `status`).
  **`busy` ≠ `lagged`**: you can talk while sawing; you can't swing twice.
- **Danger force-interrupts** (`DANGER`, `FIRE_STATE_CHANGE` nearby, `SURVIVOR_WORSENS` on you,
  `PLAYER_STOP_REQUEST`) — The Long Dark's most-cited failure is finishing a craft while a bear eats
  you. Any new command interrupts; progress banks where that is physical (the half-sawn branch) and
  is lost where it is (the ember dies). No confirmation prompts, no questions to the player
  (clarification-only feedback, Andrew 2026-09-16; the "uninterruptible + confirm" idea was mine).
- **Every tick callback re-checks "am I still the current activity"** (stale callbacks are the async
  failure mode); cancelling is by activity id.
- **Durations are authored in game-minutes** and converted at schedule time by the live ratio; a
  real-second floor (≈ 3 s) keeps very short beats legible. Attended actions sit in **1–3 game-min**
  (15–45 real s) so the fiction compresses by design; anything longer becomes a process.

## 3. The feedback grammar (content: `responses/activities.py`)
| moment | example (sawing a branch) | rule |
|---|---|---|
| start | *You set to work sawing the low branch.* | always |
| tick (3–5 per activity, proportional) | *Sawdust drifts down.* → *Halfway through, and your arm knows it.* → *The cut yawns; one more pull.* | varied, state-driven, never one string repeated |
| interrupt | *You stop, the branch half-sawn.* (progress banked on the branch: "a half-sawn low branch") | names what remains |
| complete | *The branch drops, and you with it, into the snow.* | the outcome line is the operation's own narration |
| third person | *Agent-1 is sawing at a branch.* / *You hear sawing to the north.* | via the propagator, by band |

## 4. Processes (pure `systems/{fire,warmth,water,injury}.py`; each a `tick(state, dt) -> Effects`)
- **Fire** — the stage ladder from fire-and-shaping.md §5; fuel mass consumed per tick by material
  burn rate into ash + the sink (ledgered every tick — never lazy, never OnDemandHandler); heat
  output by stage; `FIRE_STATE_CHANGE` events at stage transitions interrupt nearby activities.
- **Warmth** — one integer per character: **core temperature in tenths of °C** (370 = 37.0).
  Per tick: `Δ = −exposure(zone, weather, wind) + insulation(clothing warmth-grams, wet penalty)
  + fire_heat(distance) + activity_heat − wet_skin_penalty + huddle_bonus`. Bands: fine ≥ 360 ·
  cold 350–359 · shivering 340–349 · impaired 320–339 · dying < 320 (P5's warmth floor: huddle +
  fuselage + body heat keeps a competent party ≥ 340 through one night — a property test).
- **Hunger / thirst** — integer **calories** and **hydration (ml)** per character, spent per tick and
  per activity; eat/drink add; snow eaten costs heat (the manual's lesson). Bands feed status words
  and the "hungry enough to look at the pilot" pressure the moral layer needs.
- **Injury** — named wounds on the character (`{part, kind: cut|burn|sprain|frostbite, severity,
  bleeding: g/min, infected_at}`): bleeding costs hydration and warmth per tick until pressed/
  bound; a bound wound stops; a dirty one can infect after N hours (deterministic, seeded jitter).
  Wrap/bandage/press/splint act on wounds; `examine me` lists them.
- **Drying / wetting** — `wet` is a number (g of water in the thing); by a fire it falls; in snow it
  rises; wet insulation counts for less; the soaked matchbox dries by heat (the fire bootstrap).
- **The pilot** — a scripted process that ends within the first day (Andrew, 2026-09-16): nobody can
  talk to him (no language model behind him); he moans softly (a sound event heard only in the
  cockpit) and may say scripted lines; then a body. Tending him (cover, press a wound) is a physical
  act that resolves like any other and costs the tender time and warmth. What he says and what it
  carries is designed in the pilot's document (June's "lucid windows / fragments" stands until then).
All tick effects are Effects through `apply()` (DR-10); the ledger balances fuel→ash+sink and
water in/out; the seeded replay property must stay green with activities.

## 5. Status (the player sees the numbers as words)
`status` (and the inventory footer): *You are shivering, hungry, and your left forearm is bleeding
into the bandage. The fire is burning low. About four hours of light left.* Bands, never numbers;
the per-step log carries the numbers for analysis (an agent sees what a human sees — moral-social §2).

## 6. What this makes possible (the reason it is core, not later)
- The fire path is a real sequence with tension (the ember dies in two minutes if you don't feed it).
- Every dilemma probe in the moral layer (the pilot's body, the blanket for the dying man, the last
  ration) becomes a real decision, because hunger and cold are numbers that hurt.
- Co-op stops being parallel solitaire: one saws while the other tends the fire; the half-sawn branch
  is anyone's.

## 7. Build order inside step 3 (each a probe cluster)
1. scheduler + activities for the verbs that already take time (cut/saw, dig, pry, tear) with tick
   feedback; the Tier-2 `@reload` durability test; the whitelist; force-interrupt on DANGER.
2. fire as a process (stages, fuel, heat, events); `put X on fire`, `blow on`, `bank`, `douse`.
3. warmth (core temperature; clothing + fire + shelter + activity; the warmth-floor property test).
4. hunger/thirst; eat/drink effects; snow-eating costs heat.
5. injury (wounds, bleeding, bind/press/splint); wet/dry as numbers; the matchbox dries.
6. the pilot's clock; `status`; the logged numbers.
Acceptance: the bow-drill transcript and the lighter transcript play with real ticks; a party of
two survives one modelled night by ≥3 warmth strategies (fire; huddle + fuselage; insulation
salvage) and dies by none of them if they do nothing.

## 8. Sleep, rest, and the consensus clock (Andrew, 2026-09-07 — amends DR-14 / DR-15)
Andrew's decisions: players can **sleep**; there is a way to **move the clock forward if ALL
players agree**, and **events can interrupt it**; the run is **roughly a week**, rescue can come
earlier, and it can run longer until the food runs out — not a permanent game: the escalation
ladder (`events-and-escalation.md` §2) kills a party that is not rescued.
- **`sleep`** / **`rest`** / **`wait [until dawn | N hours | for <event>]`** are unattended
  processes on the character: `resting_until` in world-time, a bedding score from the zone (what
  you lie on and under: boughs, foam, the blanket, the sleeping bag; the huddle), and a watch flag.
- **Consensus advance (DR-14a):** when every connected character in the run is resting (or waiting),
  the heartbeat runs at **20× dt** (one real tick = 20 game-min) until the earliest `resting_until`
  or an **interrupting event**: cold below the character's floor (you wake shivering), the fire
  reaching `embers`, any propagated Event with loudness ≥ 0.5 in band (wolves, the ice booming, a
  plane), DANGER, a player's own command. A single player who keeps acting holds the clock at 1×
  for everyone (decided — Andrew, 2026-09-16: the others wait for the next event, such as someone
  waking, and do something else meanwhile) — the watch is a real co-op role (one tends the fire while three sleep; the fire
  can be banked to last the watch).
- **Sleep is a resource with a price:** fatigue falls only while asleep; sleeping cold costs
  warmth per hour (the bedding score sets the rate); a night without sleep costs judgment (slower
  activities, worse tick lines) and warmth the next day.
- **The clock never freezes** (DR-14 holds): the world advances at 1× or 20×, never 0×; nobody can
  yank it backwards or stall it; the storm and the search run on the calendar regardless.
- **The run length (DR-15a):** the instance persists across sittings for ~a week of game time; it
  ends by rescue, walk-out, or the last death — never by a timer.

## 9. Lens pass
### Visible Progress (GD)
- **GREEN by design.** Start/tick/interrupt/complete lines; the world remembers partial work.
### Flow (GD — challenge matched to skill, no dead time?)
- **YELLOW.** Attended actions of 15–45 real seconds are right for a MUD; processes must speak
  often enough that waiting by a fire isn't silence (a line every 5–10 game-min from the fire, the
  cold, the light). Tunable.
### Challenge (GD)
- **GREEN.** Cold is the antagonist and it never stops; the warmth floor keeps it fair.
### Triangularity (GD — risk/reward)
- **GREEN.** Eat snow now (hydration) vs. melt it (time, fuel); tend the pilot (info) vs. the fire
  (heat); the flare (fire) vs. the flare (signal).
