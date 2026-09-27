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
- **Instanced, synchronous co-op is decided (GDD §9/§16, DR-15).** *"A party plays one crash
  together, online at the same time, acting concurrently…"*
- **The run is roughly a week of game time, persisting across sittings (2026-09-07, DR-15a).**
  *"The run is **roughly a week** of game time, persisting across sittings; rescue can come earlier;
  it can run longer until the food runs out; it is not permanent."* *(superseded 2026-09-26, from
  Andrew's 2026-09-17 decision: the week is played in **one sitting of two or three hours** — one shot,
  or two with a halt and resume — a game played in sessions, not an ongoing world; DR-15b.)*
- **Three run modes, all on the same rules (2026-09-16).** *"Runs are for friends, for humans and
  agents together, and for agents only"* ([`VISION.md`](../../VISION.md)); the architecture records
  the same decision as *"runs are for friends, for humans with agents, and for agents only, all on
  the same rules"* (DR-14a/15a addendum).
- **An agent sees exactly what a human sees (2026-09-16).** *"an agent sees exactly what a human
  sees (structure goes to the log only)"* — so a mixed run needs no second channel. The detail is
  document [20](20-the-agent-player-and-research.md).
- **The watch rule stands (2026-09-16).** *"one player who keeps acting holds the clock at 1× for
  everyone; the others wait for the next event (someone waking)."* One player holding the clock is
  acceptable, not a problem to design away. *(superseded 2026-09-26, from Andrew's 2026-09-17 and
  2026-09-18 decisions: the clock always runs at 15 game-minutes per real minute; `propose fast
  forward` raises it to 180× when every player agrees, events drop it back, and a player who does not
  agree keeps it at the base pace — so one player still holds the pace for everyone. "Watch rule" was
  Claude's label and is dropped; being awake is being on watch — document 06.)*
- **The clock may run 20× by consensus (2026-09-07, DR-14a).** When every connected player is
  sleeping or waiting it advances at 20×, and events interrupt it. *(superseded 2026-09-26, from
  Andrew's 2026-09-17 decision: 180× by `propose fast forward`, from a base of 15 game-minutes per
  real minute — DR-14b, document 06.)*
- **No lethal-consent gate (2026-09-16).** *"a strike wounds, in every kind of run — friends, humans
  with agents, agents only"* (audit §1; `moral-social-layer.md` §1 rule 8). Multiplayer never turns
  a hit into a shove.
- **The whole valley is in the first complete run (2026-09-16).** All fifty outdoor zones, the
  walk-out included — so a party can be spread across the valley, not just across a crash site.
  *(annotated 2026-09-26: the walk-out route stays geography, but it is not an ending — the endings
  are rescued or dead, and the cabin is supplies; Andrew, 2026-09-17.)*
- **≥1 first-class interdependence is required (GDD §16).** *"add **≥1 first-class
  interdependence** (one holds/raises the antenna or relays the scout's landmark while another
  transmits) so co-op is a shared-story engine, not parallel solitaire."* The requirement is in the
  GDD; *which* interdependence ships is not settled (open question 2).

**Decided since this draft** *(gathered here 2026-09-26 by Claude from this document's review log,
documents 06, 21 and 23, and `PLAN.md` §5 — Andrew's decisions, not new ones):*

- **Sessions, not persistence (2026-09-17)** — one sitting of two or three hours; halt and resume; a
  member missing at resume is incapacitated where they lie (the party is warned).
- **A dead player is a ghost (2026-09-17)** — moves freely, talks only in the global
  out-of-character chat.
- **Agents may be scaffolded as non-human characters (2026-09-17)** — still players from the
  engine's side; agent runs are short sessions too.
- **In a run with humans, a slow model is simply slow (2026-09-26)** — *"If something is slow they
  are slow there is nothing we can do about it when humans are playing."* Whether anything paces a
  fast agent is open (Q4).
- **The bear, some of the bigger animals and a few birds act (2026-09-26)** — on behaviour rules the
  engine runs, or played from outside by a lightweight model when a run wants it; so animals are
  actors that perceive and are perceived, not only events and sign (document 23).
- **A combat system like a MUD's is in (2026-09-26)** — violence resolves with real physics in every
  kind of run.

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
prying at a jammed door your friend's fire is burning down and the cold in the cabin is climbing on
the same minutes you are spending. When you all agree to fast-forward — to sleep, or to wait out the
dark — time runs fast until something interrupts it; if one of you does not agree, the clock keeps its
normal pace for everyone and the others wait for the next thing to happen. The run is yours alone —
your own copy of the valley, no strangers walking through it — and it covers about a week of game
time in one sitting of two or three hours, or two with a halt between. *(Claude, 2026-09-26 — three
sentences brought up to Andrew's 2026-09-17 decisions: the pilot starts the run dead, the fast
forward is proposed and agreed, and a run is one sitting; for Andrew's check.)*

---

## 4. The design


> **Decided with Andrew, 2026-09-17:** a run is **one sitting of two or three hours** with friends — one shot,
> or two with a halt and resume; not an ongoing world. A member missing at resume is incapacitated where
> they lie (the party is warned). A dead player is a **ghost**: moves freely, talks only in the global
> out-of-character chat. Agent runs are short sessions too. Agents may be scaffolded as non-human
> characters (NHCs) — still players from the engine's side. The clock: 15 game-minutes per real minute,
> `propose fast forward` to 180× by consensus. The sections below are the September draft, reviewed in
> block 4; the empty-instance clock question is closed (halt/resume).

### 4.1 A run is an instance

A **run** is one party's private copy of the world: a fresh world-state spawned from a prototype set
and tagged with a `run_id` (DR-15). Two parties playing Whiteout at the same time are in two
unconnected valleys. Solo is a one-player instance — the same code path, a party of one.

The lifecycle (**proposal**, DR-15):

| stage | what happens |
|---|---|
| create | spawn the prototype set; tag every object with the run's `run_id`; seed the run's RNG (DR-12) |
| persist | the run lives in Postgres while it is played, and across a halt until the party resumes it (DR-15b) *(Claude, 2026-09-26 — §6 Q3)* |
| reset | delete the run's tagged objects (`search_object_by_tag`) at the end |
| GC | a reaper Script sweeps **tag-orphans** — objects whose run has had no connected sessions past a timeout — rather than iterating live runs *(superseded 2026-09-26 — §6 Q3: a halted run is never an orphan; the reaper sweeps a run that has ended, rescued or dead, or been discarded, plus objects whose run no longer exists; for Andrew's check)* |

The reaper timeout is unset (open question 3). *(Claude, 2026-09-26 — §6 Q3: no timeout is needed
once a halt is a state of the run rather than an absence of sessions; for Andrew's check.)* *Implementation note carried from the architecture:
`search_object_by_tag` lives under `evennia.search` / `evennia.utils.search`, and the reference
instancing usage is `evennia/contrib/tutorials/evadventure/dungeon.py`.*

### 4.2 The three run modes

Friends only · humans and agents together · agents only. **One rule set.** Nothing in the engine asks
which mode it is in: an agent connects to a player account over telnet and issues the commands a
human issues (ADR-0005), and sees what a human sees. The consequences of "same rules" are concrete:
violence resolves with real physics in every mode (no consent flag); the clock and the consensus
fast-forward apply to agents exactly as to people; a research run is a run. *(Claude, 2026-09-26:
"the watch rule" struck as a dropped label, 2026-09-17. And, from Andrew's 2026-09-17 and 2026-09-26
decisions: an agent may play a survivor or a non-human character — the bear, one of the bigger
animals, a bird — from outside, through the same grammar; the engine still does not know which it
is.)*

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

*(Claude, 2026-09-26, for Andrew's check — the acting animals.)* The bear, the bigger animals and the
few birds that act (Andrew, 2026-09-26) perceive and are perceived through these same bands: a
survivor sees the bear as a shape four zones off, and the bear hears a shout the way a person does.
One channel the bands do not carry yet is **scent**. A real bear finds meat, a body and a camp by
smell, downwind and far past sight; smoke and cooking carry on the wind for people too. Scent
travels with the wind and lingers where sound does not, so it is not a loudness — it is its own
propagation, owned by a scent-and-wind design, to be written with document 23's animals and
document 13's wind.

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
  *(superseded 2026-09-26, from Andrew's 2026-09-17 decision: the base pace is 15 game-minutes per
  real minute, and `propose fast forward` raises it to 180× when every player agrees; events drop it
  back — document 06.)*
- **The watch rule (Andrew, 2026-09-16).** One player who keeps acting holds the clock at 1× for
  everyone; the others wait for the next event. This is accepted, not a fault to engineer around.
  *(superseded 2026-09-26, from Andrew's 2026-09-17 and 2026-09-18 decisions: a player who does not
  agree to the fast forward keeps the base pace for everyone; the label is dropped; being awake is
  being on watch, and the awake receive the events sleepers do not — document 06.)*

### 4.7 Interdependence — the one thing co-op must have

The requirement: **at least one first-class interdependence**, something that genuinely
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

**The mechanism** *(Claude, 2026-09-26 — §6 Q2; for Andrew's check).* Interdependence is what the
physics gives when an act's needs exceed one body, so it is built once, as a general rule, and every
real case follows from it. An operation's needs — a capability at a level (`heft`, `leverage`), a
free hand, a body's heat, a position, a line of sight — are met by **what the actors present bring
together, read from each one's concurrent state**; and because an activity's progress lives on the
world (document 06), two people can work one job. What that makes real, from how the things actually
work:

- **the antenna held up high** outside while another keys the microphone in the cockpit — the
  antenna's quality already reads height and placement (document 14), and aircraft VHF is line of
  sight, so height is range;
- **the landmark relayed** from where it can be seen to the person at the radio, by the speech and
  sight ranges above;
- **the carry** of someone who cannot walk — an adult is more than one person can carry over snow for
  any distance;
- **the huddle** — another body's heat is by definition another person (document 08); this one
  *genuinely requires* two, which is the P6 gate met by physics;
- bracing a log while another saws it; holding the light while another works; hauling someone out
  through the ice; lifting what one person cannot shift — and whatever else the loops find.

None of these is a two-player script, and almost none is the only path: a person alone can lash the
antenna to a pole or drag a travois (≥3 paths per goal), so cooperation is usually the better answer
rather than the only one — which is what keeps a party of one a real run. Which is built first is
ordering: `PLAN.md` E13 names the antenna hold; the huddle arrives with warmth, earlier in the build
order (document 06).

### 4.8 What is deliberately *not* here (proposals)

- **No party chat channel and no out-of-world coordination layer.** Talking is in-world speech with a
  physical range, which is what makes the storm cost something socially. *Nothing in the sources
  decides this either way, and Evennia's stock out-of-character channel typeclass is present in the
  scaffold ([`game/typeclasses/channels.py`](../../game/typeclasses/channels.py)) — so this is a
  proposal that needs a yes or a no, not a description of what is built.*
  *(annotated 2026-09-26: Andrew's 2026-09-17 ghost decision made an out-of-character channel real —
  a dead player talks only in the global out-of-character chat. The live question is now who reads
  it during a run: §6 Q6.)*
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
  cockpit"* — a perception constraint. *(superseded 2026-09-26: the pilot starts the run dead
  (Andrew, 2026-09-17), so there is no moaning; what document 12 takes from here is witnessing — who
  could see what was done to his body, by band.)*
- *(added 2026-09-26)* [08 — warmth, clothing and shelter](08-warmth-clothing-and-shelter.md): the
  huddle is an interdependence (§4.7). [11 — injury and first aid](11-injury-and-first-aid.md): the
  carry, and tending a survivor who is incapacitated or whose player is gone (§6 Q5).
  [23 — flora and fauna](23-flora-and-fauna.md): the acting animals perceive and are perceived by
  band; scent is a channel still to be designed (§4.4). [21 — endings](21-endings-and-recap.md): the
  ghosts and their out-of-character chat (§6 Q6).

---

## 6. Open questions

~~1. asked:~~ **Answered 2026-09-27 (Andrew):** *"up to 5 people play, empty seats are empty - unused characters can be dead and clothes searched"*; and *"AI agents can play the game with players if they want. otherwise the char is dead if no one plays it"* *The question as it was asked:* **How many people play one run, and what is in a seat nobody plays?** *(Sharpened 2026-09-26 by
   Claude; the draft is kept below as the record.)* The plane carries five survivors — 1A/1B/2A/2B and
   the right seat, the kid included (Andrew, 2026-09-16) — and the pilot, dead at the start. Already
   settled: one survivor per player; an agent, or a model playing a non-human character, is a player
   like any other (2026-09-17); every mode runs on the same rules; freight and mail ride in the plane
   whoever is aboard (document 10 §4.3). Document 16 Q3 asks the same question from the kit side and
   should be answered with this one. What Andrew is deciding is the social shape of an evening: the
   most people one run seats, whether one person alone is a run, and what is in a seat nobody plays.
   *Options for the unplayed seat:* (a) nobody flew in it — and, as on a real Alaskan air-taxi run,
   an empty seat carries freight instead, so the plane holds as much to work with as a full party's;
   (b) its survivor flew and died in the crash — a second body, with clothes and luggage, beside the
   pilot's; (c) its survivor is aboard, alive and incapacitated by the crash — someone the party must
   keep alive from the first minute; (d) an agent plays that survivor (the humans-with-agents mode).
   *Recommendation:* up to five players, one survivor each; one person alone is a run (a party of one
   on the same code path); an unplayed seat is (d) when the run includes agents and (a) otherwise —
   freight in an empty seat is what a 206 on a bush route really flies with, it keeps the world as full
   of material as a full party's, and it adds no body the party did not choose. (b) and (c) are real
   and strong, and each changes the tone of every smaller run — which is why this is his.

   *The draft (2026-09-16), kept as the record:*
   **How many players does a run support?** The fiction seats four or five (the 206's 1A/1B/2A/2B
   plus the right seat; the kid is in — Andrew, 2026-09-16); the slice was scoped at 2–3 in one room;
   the GDD says "small-party". These are three different numbers for three different things and none
   of them is a decided player cap.
   *Options:* (a) player count = party size, four or five, one character each; (b) a smaller player
   cap with the remaining survivors as scripted bodies/NPCs; (c) a cap set by what the watch rule can
   bear — past some number, most players are always waiting.
   *Recommendation:* (a) four or five, one character per player, and let solo be a party of one with
   the others absent from the fiction — it keeps "the party" one concept and it is the only option
   that needs no new system.

~~2. Which interdependence is the first-class one?~~ **Claude's answer (2026-09-26), for Andrew's
   check:** all of them, and every other one the physics gives — picking one was a false either/or
   between authored set pieces, and the draft's own option (c) was the answer. Interdependence is not
   a feature; it is what happens when an act's physical needs exceed one body. In the ontology's
   terms, an operation's needs (a capability at a level — `heft`, `leverage` — a free hand, a body's
   heat, a position, a line of sight) are met by what the actors present bring together, read from
   each one's concurrent state, and an activity's banked progress lets two people work one job
   (document 06). That makes real: the antenna held up high outside while another keys the radio
   (antenna quality already reads height and placement — document 14; aircraft VHF is line of sight,
   so height is range); the landmark relayed to the radio by speech range; the carry (an adult is more
   than one person carries over snow for any distance); the huddle (another body's heat is another
   person — document 08 — and this one *genuinely requires* two, so the roadmap's P6 gate is met by
   physics); bracing a log for the saw; holding the light; hauling someone out through the ice;
   lifting what one person cannot. Almost none is the only path — one person can lash the antenna to
   a pole or drag a travois (≥3 paths per goal) — so a party of one stays a real run. Which is built
   first is ordering (`PLAN.md` E13: the antenna hold; the huddle lands earlier, with warmth). §4.7
   carries the mechanism.

   *The draft (2026-09-16), kept as the record:*
   **Which interdependence is the first-class one?** The antenna hold, the landmark relay, and the
   carry are all named in the sources; the requirement says one, and none is chosen.
   *Options:* (a) the antenna hold; (b) the landmark relay; (c) build the general capability
   (an action whose quality term depends on another character's concurrent state) and let several
   arise from it.
   *Recommendation:* (c) with (a) as the first instance — a single-purpose two-player script would be
   the exact "authored set piece" the systemic design exists to avoid, and the antenna's quality
   equation already has a slot for it.

~~3. Reset, persistence and the shape of a sitting.~~ **Answered 2026-09-17 (Andrew): sessions, not
   persistence** — a run is one sitting of two or three hours covering about a week of game time, one
   shot or two with a halt and resume; a member missing at resume is incapacitated where they lie; the
   empty-instance clock question is closed by the halt (review log). The GDD's one-day wording has
   since been struck (`PLAN.md` §5, 2026-09-17). **Claude's answer (2026-09-26), for Andrew's check,
   on what the draft left — the reaper:** a halted run is never reaped — a halt is the party's choice
   to come back, not an abandonment, so it is a state of the run, not an absence of sessions. The
   reaper sweeps a run when it ends (rescued or dead, document 21) or is discarded, and sweeps objects
   whose run no longer exists. There is no timeout to set, and "abandoned" versus "asleep between
   sittings" is the difference between a discarded run and a halted one. §4.1 is updated to match.

   *The draft (2026-09-16), kept as the record:*
   **Reset, persistence and the shape of a sitting — and a contradiction to settle.** GDD §9/§16 says
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

~~4. asked:~~ **Answered 2026-09-27 (Andrew):** *"we already discussed this which is the speed of typing the command"* — an agent acts at the pace of typing the command; a slow model is simply slow (2026-09-26). *The question as it was asked:* **Does anything pace a fast agent?** *(Sharpened 2026-09-26 by Claude; decided together with
   document 20, whose review log holds Andrew's words; the draft is kept below as the record.)*
   Already settled: an agent is a party member — a survivor in a seat, or a non-human character with
   a persona brief (2026-09-17) — with the same view, rules and clock, never an observer; in a run
   with humans the clock never waits for a slow model (2026-09-26); an agent agrees to `propose fast
   forward` or does not, like anyone, so it can hold the base pace exactly as a person who does not
   agree can. Whether the humans are told who is a model is split out as Q7. And the draft's fear —
   a model monopolising the clock — is mostly answered by the clock's own design: every physical act
   takes its honest game duration and occupies its actor (one activity per actor, document 06), so a
   fast model cannot do more work per game-minute than a person. What it still has is **reaction**:
   no reading or typing, the next act the instant the last one ends. An average typist manages about
   52 words a minute (Dhakal et al., CHI 2018, 168,000 typists) — some seven real seconds for
   `cut cover off seat with shard`, nearly two game-minutes at the base pace. That gap is the whole
   decision. In an agent-only run there is no human pace at all, so the same setting also decides how
   much game time each step costs.
   *Options:* (a) nothing paces it — a fast agent is simply fast, as a slow one is simply slow
   (*"not sure we should cap anything"*, 2026-09-26); (b) the typing pace — a command reaches the
   world no sooner than an average typist could have typed it, and the model's thinking time stays its
   own, so a slow model stays slow (Andrew's own wish, 2026-09-26, document 20); (c) a fixed minimum
   gap between commands (the draft's rate cap).
   *Recommendation:* (b) — it is the agent Andrew described wanting, it takes away only the one
   advantage no person can match, it never makes anything wait for a model, and in an agent-only run
   it is what gives every step an honest cost on the clock. (c) is a cruder (b); (a) lets a model win
   every race to the orange case by reaction alone.

   *The draft (2026-09-16), kept as the record:*
   **How do agents and humans mix in one instance?** Decided: same view, same rules, same clock. Not
   decided: whether an agent in a mixed run is a *character in the party* (with the fiction's
   luggage, injuries and name) or an observer-participant; whether the humans are told which
   survivors are agents; whether an agent's much faster action rate breaks the watch rule (an agent
   that never stops acting holds the clock at 1× forever and the humans never get a fast-forward).
   *Options:* (a) agents are ordinary party members, indistinguishable, no rate limit; (b) ordinary
   party members with an action-rate cap so a model cannot monopolise the clock; (c) agents are
   disclosed at the start of a run and otherwise ordinary.
   *Recommendation:* (b) plus (c) — the rate cap is a real mechanical need created by the watch rule,
   and telling friends "two of the five are models" is part of the fun, not a leak.

~~5. What happens when a player disconnects mid-run?~~ **Claude's answer (2026-09-26), for Andrew's
   check — the half the decided design settles; the other half is the rewritten Q5 below.** When the
   last player leaves, the sitting halts (halt and resume, 2026-09-17): the clock stops because the
   run is halted, which is not a hole in the running clock. When one player among several drops, the
   missing-member rule applies at once rather than only at resume: their survivor is incapacitated
   where they lie, and the party is warned (2026-09-17). An incapacitated survivor is a body in the
   world — core and extremity heat, wetness, hunger, thirst and wounds keep changing by the same
   systems as anyone's — and the party can carry them in, cover them, huddle them, feed them; the
   player returns to whatever state the body is in. The draft's (c) is the first half of this. What
   is left is only whether that body may reach death.

   *The draft (2026-09-16), kept as the record:*
   **What happens when a player disconnects mid-run?** Undecided, and load-bearing: the clock keeps
   running, the character is a body in the world with warmth and hunger, and the reaper's definition
   of an orphan is "no connected sessions past a timeout".
   *Options:* (a) the character stays in the world and keeps ticking (they can freeze while offline);
   (b) the character keeps ticking but is protected from death until reconnection; (c) the run pauses
   when the last player disconnects (the pairing of option 3a).
   *Recommendation:* (c) for the last player out, (b) for one player among several — "your friend
   froze because his wifi dropped" is the one death nobody will accept as physics.

~~5. asked:~~ **Answered 2026-09-27 (Andrew):** *"absolutely, keep in mind this is not a long running MUD, the players can pause the simulation and return later and if they are missing a player their character just goes catatonic, sits down and stares off, the other players can keep them alive though if they want"* *The question as it was asked:* **Can a survivor die while their player is disconnected?** *(Rewritten 2026-09-26 by Claude.)* The
   body is incapacitated where it lies and every system keeps running on it (above). Andrew is
   deciding what an evening with friends can bear: a dropped connection as a death, or not.
   *Options:* (a) yes — the systems run to the end, and keeping the absent friend alive is the party's
   job, like any other incapacitated survivor (the dropout becomes a co-op problem: carry them in,
   cover them, share the fire); (b) the systems run, but the body stops at the brink — alive, gravely
   cold or hurt — until its player returns, and the physics resumes from there; (c) the party decides
   at the moment of the warning whether to halt the sitting for everyone.
   *Recommendation:* (a) with (c) — "incapacitated where they lie" already makes the absent survivor a
   physical body the party must answer for, a body that cannot die would be the one exception to the
   world's physics, and the warning plus the option to halt gives the table its way out. (b) is the
   gentler rule if a death by dropped connection feels wrong at the table.

~~6. asked:~~ **Answered 2026-09-27 (Andrew):** *"ghosts can hear other ghosts, players cannot, anyone can use the OOC chat"* *The question as it was asked:* **Who reads the out-of-character chat?** *(New 2026-09-26 — the ghost decision made real a channel
   §4.8 said did not exist.)* Settled: a dead player is a ghost who moves freely and talks only in the
   global out-of-character chat (2026-09-17); the living talk in the world, where speech has a range
   and the storm eats it (§4.4). Open: whether the living read that chat during a run. A ghost walks
   the whole valley, so whatever it tells the living is scouting from outside the world — where the
   cache is, what is over the ridge, where the bear is.
   *Options:* (a) everyone reads it, living and dead; (b) only the dead read it during the run, and the
   living see it in the recap; (c) everyone reads it, and ghosts are asked by the table not to scout.
   *Recommendation:* (b). In-world speech stays the living's only channel, which is what makes the
   storm a social cost; a dead agent cannot scout for living ones, which a second channel into the
   run would allow (the same-view rule, document 20); and the recap gives the ghosts' commentary back
   to everyone at the end. Friends on a voice call will talk anyway — that is outside the game.

~~7. asked:~~ **Answered 2026-09-27 (Andrew):** *"*sighs* I am concerned now you are asking about a lot of absolutely clearly defined and decided things. AI agents can play the game with players if they want. otherwise the char is dead if no one plays it"* — decided; this question should not have been asked. *The question as it was asked:* **Are the people in a run told which survivors are models?** *(Split out of the draft Q4,
   2026-09-26.)* How an evening with friends feels, and also a research condition: a person who knows
   a companion is a model may treat it differently, and that difference is itself data (document 20
   Q5). A model playing the bear needs no disclosure; this is about survivors.
   *Options:* (a) told at the start, by name; (b) told that models are present, not which; (c) not
   told; revealed in the recap.
   *Recommendation:* (a) for friends' runs — the draft's reason stands: "two of the five are models" is
   part of the fun, not a leak; in a research run the choice is a recorded run condition, so (b) and
   (c) can be studied on purpose.

---

## 7. Review log

*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** sessions, not persistence; halt/resume
  with the missing-member rule; ghosts; NHCs as agent players; Q3 (reset/persistence) closed.
- **2026-09-26 (Andrew, ahead of this document's sitting):** *"not sure we should cap anything, If something
  is slow they are slow there is nothing we can do about it when humans are playing."* Bears on Q4: the
  clock never waits for a slow model; whether a fast agent is paced or capped stays for the sitting
  (document 20 holds the typing-speed wish).
- **2026-09-26 (Claude, self-review — PLAN.md A9):** **Answered for Andrew's check:** Q2 (the
  interdependence — all of them, from one general rule: an act's needs met by what the actors present
  bring together; the huddle genuinely requires two; §4.7 gains the mechanism); Q3's remainder (a
  halted run is never reaped; no timeout; §4.1 updated — the rest of Q3 was Andrew's, 2026-09-17);
  Q5's first half (the last player out halts the sitting; one player dropping is the missing-member
  rule at once). **Rewritten:** Q5 as *can a survivor die while their player is gone?* (the draft's
  "protected from death" stepped around the systems). **Left for Andrew, sharpened:** Q1 (how many
  play, and what is in an unplayed seat — freight, a body, an incapacitated survivor, or an agent;
  one question with document 16 Q3), Q4 (the pace of a fast agent — the typing pace, a cap, or
  nothing; the monopoly fear mostly answered by one activity per actor), Q5, and two new: Q6 (who
  reads the ghosts' out-of-character chat) and Q7 (whether people are told which survivors are
  models). **Stale content marked:** 20× and the watch rule (→ 15 game-min per real min, 180× by
  consensus), persistence across sittings (→ one sitting), the dying pilot in §3 and §5, the walk-out.
  **Added:** the decisions since the draft (§2), the acting animals and scent as a channel still to
  be designed (§4.4), the new interactions (§5).

- **2026-09-27 (Andrew):** Q1 up to five play; empty seats are empty; an unplayed character is dead and its clothes can be searched; agents may play seats. Q4 already decided — the pace of typing the command. Q5 yes — *"the players can pause the simulation and return later and if they are missing a player their character just goes catatonic, sits down and stares off, the other players can keep them alive though if they want"*. Q6 ghosts hear ghosts, players can't, anyone can use the OOC chat. Q7 already decided (*"I am concerned now you are asking about a lot of absolutely clearly defined and decided things"*).

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
P6. Co-op interdependence — the requirement is decided, the content is not designed. Concurrent-action
handling on the shared clock beyond what the reactor gives for free.

**Nothing.** No instancing code, no reaper Script, no run creation or teardown, no multi-run support
of any kind. No interdependence content anywhere in `game/`. The weather input to perception is a
stubbed `"clear"` at every call site — the band-steps in §4.4 are implemented but never exercised by
real weather. Movement is single-hop and instant; durations are plumbed but unused. Muffle edges are
implemented and tested but the crash-site map authors none, so no sound is damped anywhere in the
world yet.
