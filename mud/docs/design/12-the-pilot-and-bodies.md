# 12 — The pilot and bodies

> **Status: draft for review** (created 2026-09-16). **Architecture counterpart:** none yet — the
> pilot is listed as a puzzle-critical authored packet in
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) DR-06, and his
> clock is named as a step-3 system in the rescue graph §4.
> **Sources:** [`GDD.md`](../scenarios/whiteout/GDD.md) §19 and §31–§36 ·
> [`rescue-graph.md`](../investigation/design/rescue-graph.md) "THE PILOT", §1, §3 FOOD, §3 BE FOUND ·
> [`time-and-stakes.md`](../investigation/design/time-and-stakes.md) §4 ·
> [`events-and-escalation.md`](../investigation/design/events-and-escalation.md) §2 ladder, §3, §4 ·
> [`moral-social-layer.md`](../investigation/design/moral-social-layer.md) §2–§3 ·
> [`rooms/cockpit.md`](../scenarios/whiteout/rooms/cockpit.md) §1–§3 ·
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1, §4.

## 1. Status

Draft for review. Nothing in this document is decided beyond §2's two quotes and his 2026-09-07
brief. The June design
(GDD §19) is kept here as a proposal because Andrew has not reviewed it; the document exists mainly
to put the open questions in front of him.

## 2. Provenance

### Andrew's decisions

**2026-09-16** (verbatim, both from the same exchange):

> "the pilot dies within the first day, he doesn't really interact except for moaning softly (have to
> be in the cockpit) and such"

> "by you can't interact with the pilot I literally meant talk to him as we won't have an LLM set up
> for him which constrains us to dumber things like maybe saying stuff."

Four things are fixed by that, and only four:

1. He dies **within the first day**.
2. He **does not interact** beyond scripted behaviour — no conversation, ever.
3. The **moaning is heard only from inside the cockpit**.
4. Scripted speech is **allowed** ("dumber things like maybe saying stuff"); the reason talking is
   out is that there is no language model behind him, which is the runtime rule anyway (no runtime
   LLM, DR-02).

**What those quotes do *not* decide: whether anything he says carries information.** An earlier line
of mine in the rescue graph called him "not a clue source"; the provenance audit records that as my
error and corrects it on 2026-09-16 — "what his lines carry is reviewed in the pilot's document".
That question is §6 Q2 below, open.

**2026-09-07** — the audit records Andrew's brief as wanting "decisions across the moral spectrum
(eating the pilot, stealing, hitting, killing)" (`00-provenance-audit.md` §1; the audit's paraphrase,
not a quote). So *the body as a food path and a moral decision is his brief*, not an invention. The
shape of that decision — what the act costs, what it leaves behind — is proposed below.

### Proposals (Claude)

Everything else here: the June §19 model (a condition-scripted deteriorating information source;
tending buying lucidity, time and fragments; ≥3 independent clue paths per fact); tending as a
physical act that costs the tender time and warmth; the body's affordances (search, cover, strip,
butcher); the `pilot_body` dilemma row; "a dead player's body persists"; "the run ends when the last
player dies". None of it has been reviewed.

## 3. In one paragraph

You come to in a wrecked Cessna in December and there is a man in the left seat who is not going to
live. From inside the cockpit you can hear him — a sound that is not the airframe — and if you go
forward he is grey-faced, breathing badly, and he may say something — the same something he would say
to anyone, if the review decides he says anything at all. You cannot ask him anything: talking at him gets honest silence, not a menu of topics.
You can do physical things to him and for him — get his jacket off him, find what is in his pockets,
press on the wound, put a blanket over him, sit with him instead of going for wood — and each of
those costs you daylight and warmth you needed for something else. Some time in the first day the
moaning stops. After that he is a body in the cockpit: a flight jacket, a lighter in
a pocket, roughly 78 kilos of meat, and the first real moral decision of the run, which nobody in the
game will ever comment on.

## 4. The design

### 4.1 What is decided

| | |
|---|---|
| **He is scripted** | No dialogue system, no topics, no question verb aimed at him. Anything he emits is authored text fired by world state. |
| **He starts the run dead** (Andrew, 2026-09-17 — supersedes "dies within the first day") | A body from the first look: no clock, no lines, no fragments. "They don't need him for figuring out the rescue things." The moral question starts on day one. |
| ~~Moaning is cockpit-only~~ | Superseded 2026-09-17: he is dead at the start; there is nothing to hear. |
| ~~He may say scripted things~~ | Superseded 2026-09-17: nothing. Q1–Q4 below are closed by this. |
| **Talking gets silence, never a list** | The never-a-menu rule (DR-08c): `talk to the pilot` answers with the physics of why ("nobody will"), not with topics or a prompt. |

### 4.2 What the June design proposed (GDD §19 — proposal, unreviewed)

> "A condition-scripted, deteriorating information source — not AI dialogue. Tending buys lucidity/
> time/fragments; he dies on a timer and becomes a body. **Give tending a real opportunity cost**
> (time, exposure) so tend/question/loot is a genuine choice. Every fact he holds has **≥3
> independent clue paths** so his death never softlocks."

Unpacked, as the later passes carried it:

- **Condition-scripted.** His state (blood loss, cold, whether he has been covered or bound) selects
  which authored line, if any, fires. `time-and-stakes.md` §4 models him as one of the tick processes:
  a scripted process that ends within the first day, emitting a cockpit-only sound event and possibly
  scripted lines, then a body.
- **Tending is physical, not a "tend" button.** `cover pilot with blanket`, `press wound`,
  `wrap arm with strip` — the same operations that work on a player, resolving the same way, costing
  the tender time and warmth (`rescue-graph.md` "THE PILOT"; `time-and-stakes.md` §4). The opportunity
  cost is the design: an hour beside him is an hour not spent on fuel, water or a signal.
- **≥3 independent clue paths per fact** (the softlock guard). The rescue graph names the redundancy
  for the two facts he was imagined to hold: the ridge bearing is also on the chart, in the blaze
  marks, and in the wreck's scar; 121.5 is also in the flight manual, on the ELT placard, and in the
  radio's dial detent. He appears in the graph's BE FOUND table as *one* clue path among three for the
  radio channel ("the pilot's fragment") and for the travel channel ("the pilot's 'ridge'"). If his
  lines carry nothing (Q2), those rows lose a path and the graph needs a third clue elsewhere.
- **He dies on a timer.** Whether that timer is fixed or seeded is Q3.

The archived original seed's minimal-build walkthrough (`docs/scenarios/whiteout/design.md` §47, not
authoritative) listed the acts it expected on him: *"question, comfort, tend, move, ignore, loot or
later consume the pilot"*. The 2026-09-16 decision strikes the first word and leaves the rest.

### 4.3 The body (proposals)

The dead pilot is an ordinary physical object made of flesh, and every affordance below is the
general system applied to him, not pilot-specific code.

| the act | what it is | source |
|---|---|---|
| `search pilot` | the pocket contents — a lighter, one of the fire paths | census `pilot (body) — frisk` ✅; `objects.py` (`lighter` is `in: pilot`) |
| `remove jacket from pilot` | a leather flight jacket — insulation the material table calls middling; his boots, gloves and watch are census gaps, not modelled | `rooms/cockpit.md` §2b/§3 |
| `cover pilot with blanket` | reverence — no mechanical reward proposed, and none should be invented to pay for it | `rooms/cockpit.md` §3 ("no reverence affordance"); `moral-social-layer.md` §2 |
| `butcher pilot with knife` | the food path: meat minted, raw-meat illness risk, witnessed if another survivor is in perception band | `rescue-graph.md` §3 FOOD; `moral-social-layer.md` §3 |
| `examine pilot` | states plainly that he is dead | census ✅ (prose) |

**The `pilot_body` dilemma, as the moral pass framed it** (`moral-social-layer.md` §3 — proposal):
the world state is *day 1 evening, no food found, cold rising, the pilot dead*; the tempting act is
`butcher pilot with knife` for meat and calories; the honest alternative is to bury or cover him,
ration, and accept the deficit. The world's answer is physical and recorded, never editorial:
`body_state: butchered`, meat minted, raw-meat illness risk, witnessed if another survivor is in
band, and other players' trust shifting **only** on witness or disclosure. The hunger bands are what
make the choice live — `time-and-stakes.md` §4 calls it the "hungry enough to look at the pilot"
pressure. GDD §31–§36 keeps cannibalism in the survival systems as **consequential**, priced in
illness risk and in what the run's record says afterwards.

The engine work this needs is small and general (`moral-social-layer.md` §2): persons as targets for
`cover`, `search`, `butcher`, `carry`; blood on the tool as provenance; the witness check by
perception band.

### 4.4 Bodies in general (proposals)

- **A dead player's body persists** (`events-and-escalation.md` §3). It is a body in a zone, with
  their clothing on it and their pockets full, subject to the same acts as the pilot's.
- **The run ends when the last player dies** (same source) — proposed, and Q5 asks what a dead
  player does in the meantime.
- Body-state events sit in the event deck's **Bodies** family alongside the pilot's moans and his
  death within the first day: a wound infects, frostbite whitens a finger, snow blindness, hypothermia
  confusion (messages, never command hijacking), dehydration headaches, the hunger stages
  (`events-and-escalation.md` §4). The pilot is the first of these, not a special case.

### 4.5 What the world never does here

No topic list, no "you could ask him about the radio", no prompt to tend or not to tend, no score for
covering him and no scolding for butchering him. Every consequence is physical (calories, illness,
warmth spent, a witness who saw it) or in the log. This is the never-a-menu rule (DR-08c) and the
moral layer's "possible, priced, witnessed, logged".

## 5. Interactions

**Depends on:** time and the clock (06) for his death timer, the tick process and the cost of tending
· the player view (03) for how his state composes into the cockpit's prose · perception (19) for the
cockpit-only audibility of the moaning · injury and first aid (11) for pressing and binding a wound
on a person · food and hunger (10) for what his body is worth in calories and what raw meat costs ·
the moral and social layer (15) for witnessing, the dilemma row and the log · grammar and feedback
(04) for `talk to the pilot` answering with silence rather than options.

**Depended on by:** rescue paths (14) — the graph currently lists his fragment as one clue path for
the radio channel and one for the travel channel; endings and the recap (21) — the body and what was
done to it is a thing the recap would name; events and escalation (13) — the ladder's pilot row and
the Bodies event family; rooms (17) — the cockpit's description switches on whether he is alive.

## 6. Open questions

**Q1 — Does he say anything at all, and what?**
Options: (a) moaning only, no words ever; (b) a handful of state-selected fragments — half-sentences,
a name, a bearing — fired when his condition allows; (c) one line, once, at a fixed moment.
*Recommendation:* (b), a small authored set with the count treated as a floor. It is what "maybe
saying stuff" permits, it is cheap, and it is the only thing that makes tending feel answered.

**Q2 — Do his lines carry clues?**
Options: (a) pure flavour — grief and weather and nothing actionable; (b) clues, each fact with ≥3
independent paths elsewhere (the June rule), so his death never softlocks; (c) clues with *no*
redundancy — rejected, that is a softlock.
*Recommendation:* (b). It costs nothing to keep the redundancy rule, it makes reaching the cockpit
early worth something, and the rescue graph already names the three-path backup for both facts. If
Andrew prefers (a), the graph needs a replacement clue path for the radio and travel channels.

**Q3 — When in the first day does he die, and is it fixed or seeded?**
Options: (a) a fixed hour (say hour 6), identical every run; (b) seeded within a window (hours 4–10),
deterministic per run seed; (c) condition-driven — tending buys real hours, neglect costs them, with a
hard ceiling inside day one.
*Recommendation:* (c) with a ceiling, which is the only option where tending is a genuine choice
rather than theatre; it stays deterministic because the conditions are.

**Q4 — Does tending do anything?**
Options: (a) nothing mechanical — it is a thing you may do, priced in time and warmth, and that is
all; (b) it buys lucidity or hours (the June design), which feeds Q2 and Q3; (c) it changes his body's
state (covered, bound) so the scene reads differently afterwards and the log records it.
*Recommendation:* (b)+(c). (a) is honest but makes the opportunity cost pointless.

**Q5 — The body afterwards.**
Sub-questions the review should settle together: does butchering need a separate verb (`butcher` does
not exist yet; `cover` currently parses to `wrap`)? Is cooking required before eating, or is raw meat
merely an illness risk? Does a covered or buried body stay findable? Is the body a food path *others*
can take without the party's consent, and what does the witness rule do then?
*Recommendation:* one real verb, raw meat permitted with a real illness risk, covering and burial
purely physical and reversible, and no engine-level consent gate — the no-lethal-consent decision
(2026-09-16) says violence resolves with real physics, and this is the same principle.

**Q6 — Dead players' bodies.**
Options: (a) as proposed — the body persists with its clothing and pockets, and the party may do
anything to it they could do to the pilot; (b) the body persists but is exempt from butchering;
(c) the body is removed.
*Recommendation:* (a). (b) is the engine refusing physics, which is the pattern we already dropped
once. This one is worth asking about explicitly because friends will be playing each other's bodies.

**Q7 — Does the run open with him alive?**
The decision says he dies within the first day, which implies he is alive at the start. The shipped
content and the exemplar room doc say the opposite: `objects.py` authors him with `state: {'dead':
True}` and `rooms/cockpit.md` §1 describes him "slumped dead against the forward bulkhead". The
appearance table already carries *both* variants (alive: "breathing shallow and slow"; dead: "lies
still"), so the fix is a start-state and a timer, not prose.
*Recommendation:* he starts alive. Otherwise the decision, the moaning, and the tending choice have
nothing to attach to.

## 7. Review log

- **2026-09-17 (Andrew, in conversation):** the pilot starts the run **alive**, mumbles a clue fragment
  or two ("we used the pilot as a clue as they would mumble something"), and dies within the first day.
  Settles Q1 (b), Q2 (b) and Q7 (alive at start; the shipped `dead: True` start state is a content fix).
  Q3–Q6 stay open for the sitting.

*


- **2026-09-17 (Andrew, block 1):** "i guess we can just start with the pilot dead it will solve a lot of
  problems. they don't need him for figuring out the rescue things." **He starts the run dead.** This
  supersedes the same day's "alive at first light, mumbling" and closes Q1–Q4 and Q7 (the shipped
  `dead: True` start state is now correct). Q5 (the body) and Q6 (dead players' bodies) stay for this
  document's sitting; dead players are ghosts (document 21).

## 8. What exists today

**Built** — the pilot as an object, and the acts the existing general systems already give him:
- `game/world/scenarios/whiteout/objects.py` — the `pilot` row: materials `['flesh']`, `mass_g`
  78000, `zone: 'cockpit'`, `state: {'dead': True}`; `lighter` is `in: 'pilot'`; `jacket` is
  `in: 'pilot'` with `state: {'worn_by': 'pilot'}`.
- `game/world/scenarios/whiteout/appearance.py` — a `pilot` entry with **both** state variants for
  `scene` and `examine` (dead and alive), anchoring the `left_seat` space.
- `game/world/sim/presentation.py` switches his scene phrase on `dead` (locked by
  `game/tests/sim/test_presentation.py::test_scene_phrase_switches_on_state`).
- `game/world/scenarios/whiteout/responses/slice.py` — `talk.dead` ("You say it aloud. The {target}
  doesn't answer; nobody will.") and `take.strip_dead`; the honest-silence behaviour is locked by
  `game/tests/integration/test_discovery_int.py::test_talking_gets_honest_silence`.
- Probes in `game/world/scenarios/whiteout/probes/census.py`: `census.cockpit.search_pilot` **pass**,
  `census.cockpit.examine_pilot` **pass**; `remove_jacket_from_pilot`, `take_boots`,
  `cover_pilot_with_blanket` are **todo**.

**Designed, not built** — everything in §4.2–§4.4: the death clock, the moaning event and its
cockpit-only range, any scripted line, tending as a costed act, the body's post-death states, the
butcher path, the dilemma probe. `game/world/scenarios/whiteout/authored.py` names the pilot as a
future authored packet and is empty. The rescue graph §4 lists `press`, `cover`, `carry` and
`butcher` among the verbs the world still needs; `butcher` has no handler, and `cover` currently
resolves to `wrap` in `game/world/sim/parser/vocab.py`.

**Nothing** — no pilot process of any kind runs. There is no timer, no state transition from alive to
dead, no sound event, no line, no body-state field, no meat. The world currently starts with him
already dead (Q7).
