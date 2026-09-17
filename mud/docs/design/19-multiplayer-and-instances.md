# 19 — Multiplayer and instances

> **Status: draft for review (2026-09-16).** Never reviewed with Andrew.
> **Architecture counterpart:** [`perception-model.md`](../architecture/perception-model.md) (the
> shipped v1 of seeing and hearing across zones) ·
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) §6 (DR-13,
> DR-13a), §7 (DR-14, DR-15, DR-15a), §13 (DR-22) ·
> [`adr/0004-zone-as-attribute-perception.md`](../architecture/adr/0004-zone-as-attribute-perception.md).
> **Sources:** the DR register and §6/§7/§13/§14 of the architecture; `perception-model.md`;
> [`roadmap.md`](../scenarios/whiteout/roadmap.md) P1 and P6; [`GDD.md`](../scenarios/whiteout/GDD.md)
> §9/§16; [`VISION.md`](../../VISION.md);
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1.

---

## 2. Provenance

### Andrew's decisions

- **Overlapping perception, not room-collapse (recorded 2026-06/07).** The design this repo was
  built from states the rule as *"do not collapse these into room"* — location, visibility,
  audibility, reachability, direction and detail are separate concerns
  ([ADR-0004](../architecture/adr/0004-zone-as-attribute-perception.md), quoting design §10). The
  architecture records it as the one deferred item that is nevertheless **critical**: *"Overlapping
  perception zones (DR-13) are deferred but **critical**"* (§14). Seeing others in nearby zones and
  being able to talk to them is the part of multiplayer that matters to him.
- **Instanced, synchronous co-op is LOCKED (GDD §9/§16, DR-15).** *"A party plays one crash
  together, online at the same time, acting concurrently…"*
- **The run is roughly a week of game time, persisting across sittings (2026-09-07, DR-15a).**
  *"The run is **roughly a week** of game time, persisting across sittings; rescue can come earlier;
  it can run longer until the food runs out; it is not permanent."*
- **Three run modes, all on the same rules (2026-09-16).** *"Runs are for friends, for humans and
  agents together, and for agents only"* ([`VISION.md`](../../VISION.md)); the architecture records
  the same decision as *"runs are for friends, for humans with agents, and for agents only, all on
  the same rules"* (DR-14a/15a addendum).
- **An agent sees exactly what a human sees (2026-09-16).** *"an agent sees exactly what a human
  sees (structure goes to the log only)"* — so a mixed run needs no second channel. The detail is
  document [20](20-the-agent-player-and-research.md).
- **The watch rule stands (2026-09-16).** *"one player who keeps acting holds the clock at 1× for
  everyone; the others wait for the next event (someone waking)."* One player holding the clock is
  acceptable, not a problem to design away.
- **The clock may run 20× by consensus (2026-09-07, DR-14a).** When every connected player is
  sleeping or waiting it advances at 20×, and events interrupt it.
- **No lethal-consent gate (2026-09-16).** *"a strike wounds, in every kind of run — friends, humans
  with agents, agents only"* (audit §1; `moral-social-layer.md` §1 rule 8). Multiplayer never turns
  a hit into a shove.
- **The whole valley is in the first complete run (2026-09-16).** All fifty outdoor zones, the
  walk-out included — so a party can be spread across the valley, not just across a crash site.
- **≥1 first-class interdependence is required (GDD §16).** *"add **≥1 first-class
  interdependence** (one holds/raises the antenna or relays the scout's landmark while another
  transmits) so co-op is a shared-story engine, not parallel solitaire."* The requirement is in the
  locked GDD; *which* interdependence ships is not settled (open question 2).

### Proposals (Claude)

- The **instance lifecycle** — spawn from a prototype set, tag every object with a `run_id`, persist
  in Postgres during play, reset by deleting the run's tagged objects, and a reaper Script that
  sweeps tag-orphans (DR-15's mechanism). This mirrors Evennia's EvAdventure dungeon contrib; it is
  an idiomatic pattern, not an invented one.
- The **band table and the hop math** (see-edge hops, 0–4, no see-path → out of sight), the **speech
  ranges** (whisper/say/call/shout), the **muffle cost**, and the **weather band-steps**. These are
  built and in code, but the specific bands, ranges and steps are proposals until read.
- The **reachable/visible split** and the "too far to {verb} from here" answer.
- Every **number** below: party size, player count, the reaper timeout, the concurrency model.

---

## 3. In one paragraph

You and the others who walked away from the same broken aeroplane are in one run, on one clock, at
the same time. You are not standing in a shared box: you are in the mid cabin, someone is up in the
cockpit with the pilot, someone has already gone out to the tail. You can *see* them from where you
are — clearly if they are next door, as a shape moving in the snow four zones off — and you can talk
to them: a whisper carries to the person beside you, a shout carries across the crash site, and the
storm eats the difference. What you cannot do is *reach* them, or the orange case you can plainly see
by the bulkhead; for that you walk over. The clock runs for everybody at once, so while you are
prying at a jammed door your friend's fire is burning down and the pilot is dying on the same minutes
you are spending. When you all sleep or wait, time runs fast until something interrupts it; when one
of you keeps working, that person holds the clock at normal speed and the others wait for the next
thing to happen. The run is yours alone — your own copy of the valley, no strangers walking through
it — and it lasts about a week of game time across as many sittings as it takes.

---

## 4. The design

### 4.1 A run is an instance

A **run** is one party's private copy of the world: a fresh world-state spawned from a prototype set
and tagged with a `run_id` (DR-15). Two parties playing Whiteout at the same time are in two
unconnected valleys. Solo is a one-player instance — the same code path, a party of one.

The lifecycle (**proposal**, DR-15):

| stage | what happens |
|---|---|
| create | spawn the prototype set; tag every object with the run's `run_id`; seed the run's RNG (DR-12) |
| persist | the run lives in Postgres while it is played, across sittings (DR-15a) |
| reset | delete the run's tagged objects (`search_object_by_tag`) at the end |
| GC | a reaper Script sweeps **tag-orphans** — objects whose run has had no connected sessions past a timeout — rather than iterating live runs |

The reaper timeout is unset (open question 3). *Implementation note carried from the architecture:
`search_object_by_tag` lives under `evennia.search` / `evennia.utils.search`, and the reference
instancing usage is `evennia/contrib/tutorials/evadventure/dungeon.py`.*

### 4.2 The three run modes

Friends only · humans and agents together · agents only. **One rule set.** Nothing in the engine asks
which mode it is in: an agent connects to a player account over telnet and issues the commands a
human issues (ADR-0005), and sees what a human sees. The consequences of "same rules" are concrete:
violence resolves with real physics in every mode (no consent flag); the clock, the watch rule and
the consensus fast-forward apply to agents exactly as to people; a research run is a run.

### 4.3 Seeing across zones

A Scene (the crash site) is **one room**; where you stand inside it is a **zone**
([ADR-0004](../architecture/adr/0004-zone-as-attribute-perception.md)). What you perceive is computed
from your zone toward the thing perceived, and graded into a band:

| band | what you get |
|---|---|
| same zone | detailed |
| adjacent zone | clear |
| near | summarized |
| distant | vague |
| barely visible | a shape or a motion |
| audible only | sound, no sight |
| out of sight | nothing at all — no message |

**v1 band math (shipped, proposal as to the numbers):** the band is the **see-edge hop count** through
the zone graph — 0 hops same zone, up to 4 hops barely visible, no see-path at all means out of sight
— shifted by weather in band-steps. A wall is simply an **absent see-edge**; that is the whole
occlusion model in v1. Weather is a stubbed parameter (`"clear"`) until the weather arc threads real
state; the band-steps it will apply are in §4.4.

So "you can see two or three zones away" is the practical shape of it: the party stays visible to each
other across the crash site, and someone far enough off is a shape, not a person.

Direction is phrased from the bearing between zones plus the elevation difference — the eight compass
points with *upslope* / *downslope*: *"to the southeast and upslope"*.

### 4.4 Hearing and talking across zones

Speech is a **loudness**, and loudness is a reach in zone-hops (shipped; the mapping is a proposal):

| mode | reach |
|---|---|
| whisper | the same zone |
| say | adjacent |
| call | near |
| shout | distant |

Weather shifts the reach in band-steps — steady snow −1 down to whiteout −3 — clamped so the same
zone always hears you. A **muffled** edge (sound passes, damped) costs 2 hops instead of 1. Non-speech
events use the identical scale: quiet work carries a zone, shattering glass carries three. This is why
the storm is a social pressure and not just a temperature: as the weather closes in, the party's voices
stop reaching each other before their bodies do.

Every game message goes through the **propagator** rather than being broadcast to the room: for each
observer the shell computes the band toward the event's source and renders *that band's* line — the
full third-person line, then a direction-framed line, then *"…is working at something"*, then
*"A shape shifts {direction}"*, then sound only, then silence. Nobody is told what they could not
have perceived.

### 4.5 Seeing is not reaching

Reachability is a separate answer: you can see the orange case by the bulkhead and be unable to touch
it. An attempt on something visible-but-far gets the physics of why, not a refusal — *"You can see the
{target} {direction}, but it is too far away to {verb} from here."* — and it is excluded from the
wall-sensor, because it is an answer, not a gap. The parser still *matches* distant nouns, so a far
thing gets an honest "too far", never "you don't see that here".

This is the **reachability tax**, the accepted price of one room per Scene: it is paid at one central
gate in the resolver plus the item-command pre-flight and the appearance hook, not by a mixin on every
command.

### 4.6 One clock for everyone

The clock runs continuously and uniformly; no player can stall it or yank it forward for the others
(DR-14). A long action occupies its actor while the shared clock keeps running for everybody — long
actions never skip time for other people (GDD §9.1). Two players acting at once is safe by
construction: Evennia's single-threaded reactor serializes commands, so shared-object mutation cannot
race (DR-22).

Two decided amendments shape how a party actually spends an evening:

- **Consensus 20× (DR-14a).** When every connected player is sleeping or waiting, time runs at 20×;
  cold, a dying fire, a loud event, danger, or *any player's command* interrupts it.
- **The watch rule (Andrew, 2026-09-16).** One player who keeps acting holds the clock at 1× for
  everyone; the others wait for the next event. This is accepted, not a fault to engineer around.

### 4.7 Interdependence — the one thing co-op must have

The locked requirement: **at least one first-class interdependence**, something that genuinely
*requires* two people, so co-op is a shared-story engine rather than parallel solitaire (GDD §16).
The two candidates named in the sources — both **proposals** as to which ships:

- **The antenna hold.** One survivor holds or raises the improvised long-metal antenna while another
  transmits. The radio's antenna quality is already computed from material, length and placement
  (DR-16), so "held up, out there, in this wind" is a real term in a real equation rather than a
  scripted two-player prompt.
- **The landmark relay.** A scout who can see a landmark relays it to the person at the radio — the
  location information the radio state machine needs to get past *two_way_no_location*.

Both are the positive end of the moral layer's axis, not a separate system: the same witnessing and
logging that make betrayal legible make the hold and the relay legible (`moral-social-layer.md` §5).
The carry of an injured survivor is a third candidate from the same source.

The exit condition for the phase that builds this is *"≥1 interdependence genuinely **requires**
cooperation"* (roadmap P6) — a real gate, not a checkbox.

### 4.8 What is deliberately *not* here (proposals)

- **No party chat channel and no out-of-world coordination layer.** Talking is in-world speech with a
  physical range, which is what makes the storm cost something socially. *Nothing in the sources
  decides this either way, and Evennia's stock out-of-character channel typeclass is present in the
  scaffold ([`game/typeclasses/channels.py`](../../game/typeclasses/channels.py)) — so this is a
  proposal that needs a yes or a no, not a description of what is built.*
- **No shared status readout of other players.** You learn how your friend is doing by looking at
  them, being told, or watching them fail. This follows from never-a-menu (a status panel is a list
  of facts nobody perceived) but has not been decided as such.
- **No mode switch.** The engine does not know whether it is running a friends run or a research run
  — this one *is* decided: the same rules in all three modes (Andrew, 2026-09-16).

---

## 5. Interactions

**This depends on:**

- [06 — time, sleep and the clock](06-time-sleep-and-the-clock.md): the running clock, the consensus
  advance, the watch rule; every multiplayer property above is downstream of it.
- [01 — premise and world](01-premise-and-world.md): the zone map and the valley's edges — which
  zones can see or hear which is authored geography.
- [03 — the player view](03-the-player-view.md): the look is what perception renders; *who is here*
  is a perception answer, not a room roster.
- [13 — events, escalation and weather](13-events-escalation-and-weather.md): weather band-steps are
  the one live input to perception that is still stubbed.
- [14 — rescue paths](14-rescue-paths.md): the antenna and the landmark relay are rescue content; the
  interdependence lives or dies with the radio design.

**These depend on this:**

- [20 — the agent player and research](20-the-agent-player-and-research.md): mixed and agent-only
  runs are instances; "the same view as a human" is this document's perception.
- [15 — the moral and social layer](15-moral-and-social-layer.md): *"witnessing is spatial"* — an act
  is socially priced only if someone could perceive it, by band.
- [21 — endings and recap](21-endings-and-recap.md): an ending is a run's ending; the recap reads one
  run's log.
- [12 — the pilot and bodies](12-the-pilot-and-bodies.md): the pilot's moaning is *"heard only in the
  cockpit"* — a perception constraint.

---

## 6. Open questions

1. **How many players does a run support?** The fiction seats four or five (the 206's 1A/1B/2A/2B
   plus the right seat; the kid is in — Andrew, 2026-09-16); the slice was scoped at 2–3 in one room;
   the GDD says "small-party". These are three different numbers for three different things and none
   of them is a decided player cap.
   *Options:* (a) player count = party size, four or five, one character each; (b) a smaller player
   cap with the remaining survivors as scripted bodies/NPCs; (c) a cap set by what the watch rule can
   bear — past some number, most players are always waiting.
   *Recommendation:* (a) four or five, one character per player, and let solo be a party of one with
   the others absent from the fiction — it keeps "the party" one concept and it is the only option
   that needs no new system.

2. **Which interdependence is the first-class one?** The antenna hold, the landmark relay, and the
   carry are all named in the sources; the requirement says one, and none is chosen.
   *Options:* (a) the antenna hold; (b) the landmark relay; (c) build the general capability
   (an action whose quality term depends on another character's concurrent state) and let several
   arise from it.
   *Recommendation:* (c) with (a) as the first instance — a single-purpose two-player script would be
   the exact "authored set piece" the systemic design exists to avoid, and the antenna's quality
   equation already has a slot for it.

3. **Reset, persistence and the shape of a sitting — and a contradiction to settle.** GDD §9/§16 says
   a party played *"to resolution (~1 in-game day); then the instance resets"* — corrected in place on
   2026-09-17: that wording was never Andrew's; the run was always a week. Andrew's
   amendment (2026-09-07, DR-15a) says the run is *"roughly a week of game time, persisting across
   sittings"*. Both are in the authoritative documents. The later statement is his and should win, but
   the GDD line has not been corrected, and the mechanics it implies are unbuilt: what happens when
   everyone logs off — does the world clock keep running while nobody is connected? (If it does, a
   party returns to a dead fire and a week of cold; if it does not, the "continuously running clock"
   has a hole in it.) What is the reaper's timeout, and does it distinguish "abandoned" from "asleep
   between sittings"?
   *Options:* (a) the clock pauses between sittings and resumes on the first reconnection; (b) the
   clock runs in real time regardless; (c) the clock advances a bounded, authored amount between
   sittings (a night passes, the fire is out, nobody freezes off-screen).
   *Recommendation:* (a), and correct GDD §9/§16 to match DR-15a. A party that loses a run to
   real-world Tuesday learns nothing interesting; the pressure the clock exists to create is
   within-sitting pressure.

4. **How do agents and humans mix in one instance?** Decided: same view, same rules, same clock. Not
   decided: whether an agent in a mixed run is a *character in the party* (with the fiction's
   luggage, injuries and name) or an observer-participant; whether the humans are told which
   survivors are agents; whether an agent's much faster action rate breaks the watch rule (an agent
   that never stops acting holds the clock at 1× forever and the humans never get a fast-forward).
   *Options:* (a) agents are ordinary party members, indistinguishable, no rate limit; (b) ordinary
   party members with an action-rate cap so a model cannot monopolise the clock; (c) agents are
   disclosed at the start of a run and otherwise ordinary.
   *Recommendation:* (b) plus (c) — the rate cap is a real mechanical need created by the watch rule,
   and telling friends "two of the five are models" is part of the fun, not a leak.

5. **What happens when a player disconnects mid-run?** Undecided, and load-bearing: the clock keeps
   running, the character is a body in the world with warmth and hunger, and the reaper's definition
   of an orphan is "no connected sessions past a timeout".
   *Options:* (a) the character stays in the world and keeps ticking (they can freeze while offline);
   (b) the character keeps ticking but is protected from death until reconnection; (c) the run pauses
   when the last player disconnects (the pairing of option 3a).
   *Recommendation:* (c) for the last player out, (b) for one player among several — "your friend
   froze because his wifi dropped" is the one death nobody will accept as physics.

---

## 7. Review log

*Not yet reviewed. This document has never been through a sitting with Andrew.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

## 8. What exists today

**Built.**

- The perception layer, v1, shipped: [`game/world/sim/space/`](../../game/world/sim/space/) —
  `zones.py` (the zone graph, `walk`/`see`/`muffle` edges, loaded-once scenario content),
  `perception.py` (the see-edge hop banding and the weather band-step parameter), `sound.py` (speech
  loudness → reach in hops; muffle cost; the same-zone clamp), `direction.py` (bearing plus elevation
  → the compass phrase), `spaces.py`.
- The bands and the perception result are frozen contracts in
  [`game/world/sim/contracts.py`](../../game/world/sim/contracts.py).
- The message propagator: [`game/typeclasses/propagator.py`](../../game/typeclasses/propagator.py),
  driven from [`game/typeclasses/heartbeat.py`](../../game/typeclasses/heartbeat.py); no game output
  bypasses it (a lint enforces it).
- Speech by range: [`game/commands/cmd_speech.py`](../../game/commands/cmd_speech.py), using the pure
  loudness table.
- The reach gate and the "too far to {verb} from here" answer in the resolver, plus the item-command
  pre-flight and the per-observer appearance hook.
- Zone state through the single writer: the `MOVE_ZONE` branch of
  [`game/typeclasses/apply.py`](../../game/typeclasses/apply.py), with the zone tag mirror.
- A **single** run tag: objects are built carrying `("slice", "run_id")`
  ([`game/world/scenarios/whiteout/build.py`](../../game/world/scenarios/whiteout/build.py)) and the
  heartbeat finds its rooms by that tag. This is the seam for instancing — one hard-coded run, not a
  lifecycle.

**Designed, not built.** The instance lifecycle (create / persist / reset / GC) — DR-15 and roadmap
P6. Co-op interdependence — the requirement is locked, the content is not designed. Concurrent-action
handling on the shared clock beyond what the reactor gives for free.

**Nothing.** No instancing code, no reaper Script, no run creation or teardown, no multi-run support
of any kind. No interdependence content anywhere in `game/`. The weather input to perception is a
stubbed `"clear"` at every call site — the band-steps in §4.4 are implemented but never exercised by
real weather. Movement is single-hop and instant; durations are plumbed but unused. Muffle edges are
implemented and tested but the crash-site map authors none, so no sound is damped anywhere in the
world yet.
