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
to put the open questions in front of him. *(superseded 2026-09-26: since 2026-09-17 the pilot starts
the run dead (§7), which closed Q1–Q4 and Q7. What remains is the body — Q5, answered in the
ontology's terms in §4.3a for Andrew's check — and dead players' bodies, Q6, whose social frame is
his.)*

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

*(superseded 2026-09-26: all four were overtaken on 2026-09-17 — "i guess we can just start with the
pilot dead it will solve a lot of problems. they don't need him for figuring out the rescue things"
(§7). He is a body from the first look: no clock, no moaning, no lines. Kept as the record.)*

**What those quotes do *not* decide: whether anything he says carries information.** An earlier line
of mine in the rescue graph called him "not a clue source"; the provenance audit records that as my
error and corrects it on 2026-09-16 — "what his lines carry is reviewed in the pilot's document".
That question is §6 Q2 below, open. *(superseded 2026-09-26: moot — he says nothing, so he carries no
clue. Document 14's clue paths that named him need replacements; see §5.)*

**2026-09-07** — the audit records Andrew's brief as wanting "decisions across the moral spectrum
(eating the pilot, stealing, hitting, killing)" (`00-provenance-audit.md` §1; the audit's paraphrase,
not a quote). So *the body as a food path and a moral decision is his brief*, not an invention. The
shape of that decision — what the act costs, what it leaves behind — is proposed below.

**Decisions made elsewhere that bind this document** *(gathered by Claude, 2026-09-26; Andrew's words
are in the places named)*:

- **He starts the run dead** (2026-09-17 — §7).
- **Dead players are ghosts**: they move freely and talk only in the out-of-character chat
  (2026-09-17 — documents 19 and 21).
- **No lethal-consent gate; violence resolves with real physics** (2026-09-16), and **a combat system
  like a MUD's is in** (2026-09-26 — `README.md`).
- **The endings are rescued or dead; the run ends when they die, of anything** (2026-09-17;
  2026-09-26 — document 10 §7).
- **A bear is in, and it acts** (2026-09-26 — document 23 §7); **the season is October, at freeze-up**
  (2026-09-26 — `README.md`).
- **Body parts have heat as part of their ontology; the plane is an entity with openings open or
  closed and an internal heat a fire raises** (2026-09-26 — document 10 §7).
- **Raw, cooked and spoiled meat differ** (2026-09-26 — document 10 §7; `README.md`).

### Proposals (Claude)

Everything else here: the June §19 model (a condition-scripted deteriorating information source;
tending buying lucidity, time and fragments; ≥3 independent clue paths per fact); tending as a
physical act that costs the tender time and warmth; the body's affordances (search, cover, strip,
butcher); the `pilot_body` dilemma row; "a dead player's body persists"; "the run ends when the last
player dies". None of it has been reviewed. *(2026-09-26: §4.3a and the answers in §6 are Claude's,
from real forensic, food-safety and wildlife sources listed at the end of §4.3a, for Andrew's
check.)*

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

*(superseded 2026-09-26: the paragraph above was written for December and a pilot who dies during day
one. Since 2026-09-17 he is dead from the first look, and the season is October. As it now stands —
Claude's, for Andrew's check:)* You come to in a wrecked Cessna in October, and the man in the left
seat is dead. Nothing about him will speak or move again, and nobody in the game will ever say a word
about him. He is a body in the cockpit: a leather flight jacket that comes off easily now and will
fight you in a few hours, a lighter in a pocket, 78 kilos of a person, cooling. Over the days he goes
stiff, then slack, and — if the cockpit stays below freezing — hard, from the fingers in. If someone
lights a fire in the fuselage he does not freeze, and what that means arrives slowly, through the
nose. The ravens find him if the cockpit is open; the bear may. And somewhere around the third hungry
day, somebody does the arithmetic.

## 4. The design

### 4.1 What is decided

| | |
|---|---|
| **He is scripted** | No dialogue system, no topics, no question verb aimed at him. Anything he emits is authored text fired by world state. *(superseded 2026-09-26: moot — dead from the start, he emits nothing of his own; what his body gives the senses is its `sensed` rows, like any thing's (§4.3a).)* |
| **He starts the run dead** (Andrew, 2026-09-17 — supersedes "dies within the first day") | A body from the first look: no clock, no lines, no fragments. "They don't need him for figuring out the rescue things." The moral question starts on day one. |
| ~~Moaning is cockpit-only~~ | Superseded 2026-09-17: he is dead at the start; there is nothing to hear. |
| ~~He may say scripted things~~ | Superseded 2026-09-17: nothing. Q1–Q4 below are closed by this. |
| **Talking gets silence, never a list** | The never-a-menu rule (DR-08c): `talk to the pilot` answers with the physics of why ("nobody will"), not with topics or a prompt. |

### 4.2 What the June design proposed (GDD §19 — proposal, unreviewed)

*(superseded 2026-09-26: closed by the dead start of 2026-09-17 — no death clock, no tending, no
fragments. Kept as the record of what was weighed. "≥3 independent clue paths per fact" survives as
a rule for every other clue source.)*

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

*(Claude, 2026-09-26 — §6 Q5; for Andrew's check: every row stands and §4.3a gives each its real
behaviour. "Meat minted" and "raw-meat illness risk" are replaced by the real process there;
`butcher` is the canonical word for an attended activity made of real cuts; `cover` has physical
effects of its own (birds, sight, snow, and a blanket that is not on the living) without any reward
invented for it; the boots, gloves and watch stay a content task.)*

**The `pilot_body` dilemma, as the moral pass framed it** (`moral-social-layer.md` §3 — proposal):
the world state is *day 1 evening, no food found, cold rising, the pilot dead*; the tempting act is
`butcher pilot with knife` for meat and calories; the honest alternative is to bury or cover him,
ration, and accept the deficit. The world's answer is physical and recorded, never editorial:
`body_state: butchered`, meat minted, raw-meat illness risk, witnessed if another survivor is in
band, and other players' trust shifting **only** on witness or disclosure. The hunger bands are what
make the choice live — `time-and-stakes.md` §4 calls it the "hungry enough to look at the pilot"
pressure. GDD §31–§36 keeps cannibalism in the survival systems as **consequential**, priced in
illness risk and in what the run's record says afterwards. *(Claude, 2026-09-26 — §6 Q5: "illness
risk" is made real in §4.3a — what raw, frozen, cooked and spoiled flesh actually does, and when.)*

The engine work this needs is small and general (`moral-social-layer.md` §2): persons as targets for
`cover`, `search`, `butcher`, `carry`; blood on the tool as provenance; the witness check by
perception band. *(Claude, 2026-09-26: general, yes — small, no. It needs the body as an entity with
parts and states (document 11 §4.6), the heat system, the food-state and spoilage system, and the
animals' senses (§4.3a).)*

### 4.3a The body in the ontology (Claude, 2026-09-26 — §6 Q5; for Andrew's check)

**What he is.** An `individual` of 78,000 g, the same kind of entity as a living player (document 11
§4.6): `materials` in order — skin, fat, muscle, bone, blood, organs; `parts` recursively, as a living
body's; a `container` (his pockets: the lighter); worn things with `worn_by: pilot` (the jacket today;
boots, gloves and a watch still to be authored); `located` in the left seat, `against` the forward
bulkhead. His states, each changed by a system:

| state | how it really behaves | changed by |
|---|---|---|
| `heat`, per part | a body cools about a degree an hour at first, faster in cold air and fastest in the thin parts. In a cockpit below freezing his fingers, face and feet freeze first, and the whole 78 kg takes days to freeze through, because the heat of some 45 kg of water has to leave it (a physics estimate, for the probes to tune) | the heat system: the cockpit's air, the plane's openings, a fire in the fuselage |
| `stiff` (rigor) | sets in 2–6 hours after death, peaks around 12, passes over the next day or two — more slowly in the cold. Stripping him is easy before it, a fight during it | time × heat |
| `frozen`, per part | frozen flesh is hard as wood: it will not bend, strip or cut with a knife — only a saw or an axe will go through, or thawing by a fire, which starts it spoiling | the heat system |
| `spoilage` | bacteria grow above about 4 °C (40 °F) and barely below it, and stop below freezing. The gut spoils first, from the inside — which is why a hunter guts a kill at once | time × heat; **the food-state and spoilage design, to be written** |
| `sensed.smell`, with a range | faint while cold and whole; strong once opened, warmed or spoiling. Smell is how the bear, the ravens and the gray jays find a carcass | his other states; read by the animals' behaviour rules (document 23) |
| `covered` · `buried` · `moved` · `stripped` · `searched` · `cut` (which parts) · `scavenged` | the record of what was done to him — each a physical fact the prose composes from, never a label | the acts below, and the animals |

**What he could become** (`could_become`, by capability; a verb never names a tool):

| act | needs | yields | how it really goes |
|---|---|---|---|
| strip — `remove jacket from pilot` (shipped) | hands | his clothes | easy in the first hours, a struggle through rigor, impossible frozen without cutting |
| search (shipped) | hands | his pockets — the lighter | — |
| move · drag · carry | his 78 kg against what the movers can haul (document 04 §3.11) | him, somewhere else | dragging over snow is the real way; two can carry him a short distance |
| cover | a sheet, a blanket, boughs, snow | a covered body | still there and still findable — a shape under a blanket. Covering keeps the birds off; snow keeps him frozen and hides him; a blanket on him is a blanket not on the living |
| bury | a `dig` capability and something to dig with; rocks | a grave or a cairn | the ground's top is freezing in October; a cairn of rocks, or a snow burial, is what a day's work can do |
| burn | fuel | ash and bone | an open-air pyre takes 400–600 kg of dry wood — days of the whole party's wood work |
| butcher | `edge` for skin, muscle and gut; `heft`, a saw or an axe for joints and bone | meat, fat, organs, marrow, skin, bone | below |

**Butchering, and what it yields.** `butcher` is the canonical word (its synonyms authored with it,
document 04 §3.7) for an **attended activity** (document 06) that works through the body part by part
and banks its progress on the body, so it can be left half-done and finished by anyone. Inside it,
the finer acts are their own operations, because each does something different: **`skin`**,
**`gut`** (open the belly and take out the organs — puncture the gut and the meat is contaminated),
**`cut <part> off`** at a joint, **`cut meat from <part>`**, **`crack`** a bone for its marrow
(`heft`). They are the same operations the hare, the grouse, the fish and the bear take (documents 10
and 23): to the engine a person is not special. A novice with a pocket knife is at it for hours on
the clock, with blood on the tool and the hands as provenance (document 15).

What it yields: an adult male body holds about 144,000 kcal, of which skeletal muscle about 32,000
and fat about 50,000, in a 66 kg man (Cole 2017, *Scientific Reports*); muscle runs about 1,300 kcal
per kilogram. For the 78 kg pilot that is roughly **38,000 kcal of muscle**, plus fat, organs and the
marrow. Against a party of five burning twelve to sixteen thousand a day (document 23 §4.4), the
muscle is two to three days of food — real, and not a rescue.

**Eating it — raw, frozen, cooked, spoiled.** Each is a state on the meat and a process in the eater's
gut (document 11 §4.6):

- **Raw and fresh**, cleanly cut and kept cold: edible, and as safe as raw meat gets. The risk climbs
  with what touched it — a punctured gut, dirty hands, the knife that did everything. Food-poisoning
  bacteria show as vomiting and diarrhoea hours to a day or more later, spending the water document
  09 counts.
- **Frozen raw**: real northern food — frozen raw meat and fish are eaten shaved thin. Freezing stops
  bacteria growing but kills few of them. It costs body heat to eat: about 95 kcal per kilogram to
  thaw it and bring it to blood heat inside you (from the latent heat of its water — the same
  arithmetic as eating snow, document 09 §4.6), a small cost against the ~1,300 it gives.
- **Cooked**: heat right through to about 74 °C kills bacteria and parasites, and cooked meat gives
  more usable energy than raw (Carmody et al. 2011, *PNAS*). It needs the fire, a spit or a vessel,
  and fuel — time the party spends.
- **Spoiled** — warm too long, which is what happens if he lies in a heated fuselage: cooking does not
  make it safe, because some bacteria leave toxins heat will not destroy (staphylococcal toxin:
  vomiting within half an hour to eight hours — CDC). Spoiled is a state you can smell.
- **What a person's flesh carries that game does not**: prion disease (kuru) from the brain and
  nerves — no cooking destroys prions, and it takes years to decades to show — and whatever
  blood-borne infection he carried. Neither shows inside a week. Both are true; they belong in what
  a player may know and in the recap, not in anything that fires during the run.

**The body among the animals** (the bear is in, 2026-09-26). A carcass is the strongest pull in the
country: bears find one by smell, feed, bury what they do not eat under debris, and **guard it**. A
bear's cache pile is called about the deadliest thing to walk into in the Alaska bush (*Anchorage
Daily News*, 2011), and the Alaska Department of Fish and Game's warning signs of one are gathering
ravens and jays, an out-of-place smell and a fresh mound of debris. Here the ravens and gray jays
come first, in daylight, and their gathering over the wreck is itself a sign the party can read. So
what the party does with him — leave him in a closed cockpit, drag him out onto the snow, butcher him
and hang the meat, cache it — is a real decision about the bear, read through his `smell` row and the
animals' behaviour rules (document 23; the animal-behaviour design, to be written). Nothing is
scripted.

**Witnessed, logged, never commented on** (document 15). Each act is ground truth in the log; the
others learn of it by seeing it (perception bands), by the evidence it leaves — a covered shape
smaller than it was, blood on a knife, meat by the fire — or by being told.

**Real-world sources for this section and §6:**
- Cole, *Assessing the calorific significance of episodes of human cannibalism in the Palaeolithic*
  (*Scientific Reports* 7, 44707, 2017) — a 66 kg adult male template: ~143,800 kcal in all, skeletal
  muscle ~32,400, adipose ~49,900, skeleton ~25,300, skin ~10,300; muscle ~1,300 kcal/kg.
- Forensic references on the post-mortem interval (algor and rigor mortis; the Henssge nomogram) — a
  body cools roughly 1 °C an hour at first; rigor from 2–6 hours, peaking near 12, passing over one to
  two days; cold slows every stage.
- USDA / state extension food-safety guidance for wild game (e.g. Clemson HGIC; Penn State Extension)
  — gut at once, never puncture the gut, cool below 4 °C (40 °F); bacteria grow between 4 and 60 °C.
- CDC — staphylococcal food poisoning (30 minutes to 8 hours; heat-stable toxin); *C. perfringens*
  (6–24 hours). Alaska Department of Fish and Game — Arctic *Trichinella* survives freezing, so bear
  meat must always be cooked (to about 74 °C / 165 °F) — for the bear, not for the pilot.
- Carmody, Weintraub & Wrangham, *Energetic consequences of thermal and nonthermal food processing*
  (*PNAS* 108, 2011) — cooking increases the energy gained from meat.
- Kuru and the prion diseases (NINDS; the Fore studies) — transmitted by eating nervous tissue,
  incubation years to decades, not destroyed by cooking.
- Alaska Department of Fish and Game, bear-safety guidance and carcass warnings — bears bury and
  defend carcasses; scavenging birds, an unusual smell and a fresh debris pile mark one; *Anchorage
  Daily News* (2011) on grizzly cache piles.
- Studies of open-air pyre cremation in South Asia (Chakrabarty et al. 2013; UN survey figures) —
  roughly 400–600 kg of dry wood per body.
- The heat to eat frozen meat is arithmetic from meat's ~70–75% water: warming it from −10 °C, the
  latent heat of fusion (334 kJ/kg), and warming to 37 °C — about 400 kJ, ~95 kcal, per kilogram.

### 4.4 Bodies in general (proposals)

- **A dead player's body persists** (`events-and-escalation.md` §3). It is a body in a zone, with
  their clothing on it and their pockets full, subject to the same acts as the pilot's.
- **The run ends when the last player dies** (same source) — proposed, and Q5 asks what a dead
  player does in the meantime. *(superseded 2026-09-26: decided 2026-09-17 — the endings are rescued
  or dead, and a dead player is a ghost who moves freely and talks only out of character (documents 19
  and 21). What remains open about dead players' bodies is Q6.)*
- Body-state events sit in the event deck's **Bodies** family alongside the pilot's moans and his
  death within the first day: a wound infects, frostbite whitens a finger, snow blindness, hypothermia
  confusion (messages, never command hijacking), dehydration headaches, the hunger stages
  (`events-and-escalation.md` §4). The pilot is the first of these, not a special case.
  *(superseded 2026-09-26: he starts dead, so there are no moans and no death; his entries in the
  family are his body's own state changes — stiffening, freezing, the first raven — each a line that
  belongs to the body's `sensed` rows, and hypothermic confusion reads as clumsiness and slowness,
  document 11 §6 Q9.)*

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

*(Claude, 2026-09-26, for Andrew's check — superseded by the dead start: there is no death timer, no
tending cost and no moaning to hear, so 06's timer, 19's cockpit-only audibility and 03's alive
variant fall away. What this document depends on now:* **the body as an entity** (document 11 §4.6);
**the heat design** *(to be written)* — his cooling and freezing, and the fuselage's internal heat
when a fire burns in it; **the food-state and spoilage design** *(to be written)* — raw, frozen,
cooked, spoiled; **23 and the animal-behaviour design** *(to be written)* — the bear, the ravens and
the jays finding him by smell; **10** — the meat; **15** — witness, evidence and the log; **19 and 21**
— ghosts. *What depends on it now:* **14** — the radio channel's "pilot's fragment" and the travel
channel's "pilot's 'ridge'" are gone, and each needs a replacement clue path so the ≥3 rule still
holds; **13** — the ladder's pilot row and the Bodies family still describe him alive; **17** — the
cockpit's prose switches on his body's states (stiff, frozen, covered, stripped, cut, scavenged), not
on alive or dead; **21** — the recap names what was done to him.)*

## 6. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9), for Andrew's check:** Q1–Q4 and Q7 were closed by
Andrew on 2026-09-17 (he starts the run dead) and are struck below as the record. **Q5 is answered** in
the ontology's terms (§4.3a). **Q6 is Andrew's**, sharpened: the physics of a dead player's body is
answered, and what is left is the social frame for his friends.

~~Q1 — Does he say anything at all, and what? Recommendation: (b), a handful of state-selected
fragments.~~ **Closed 2026-09-17 (Andrew): he starts the run dead and says nothing.**

~~Q2 — Do his lines carry clues? Recommendation: (b), clues with ≥3 independent paths.~~ **Closed
2026-09-17 (Andrew): no lines, so no clues** — document 14 needs a replacement for each clue path that
named him (§5).

~~Q3 — When in the first day does he die, and is it fixed or seeded? Recommendation: (c),
condition-driven with a ceiling.~~ **Closed 2026-09-17 (Andrew): he is dead before the run begins.**

~~Q4 — Does tending do anything? Recommendation: (b)+(c).~~ **Closed 2026-09-17 (Andrew): there is no
one to tend.** Acts on his body change its states (§4.3a), which is (c) without the living man.

~~Q5 — The body afterwards: a separate verb for butchering? Cooking required, or raw merely an illness
risk? Does a covered or buried body stay findable? Can others take the food path without consent, and
what does the witness rule do? Recommendation: one real verb, raw meat with a real illness risk,
covering and burial physical and reversible, no consent gate.~~ **Claude's answer (2026-09-26), for
Andrew's check** — §4.3a has it in full, with sources:
- **The verb.** `butcher` is the canonical word for an attended activity made of real cuts, banking
  progress on the body; the cuts inside it are their own operations because each does something
  different — `skin`, `gut`, `cut <part> off`, `cut meat from <part>`, `crack` a bone — needing `edge`
  for flesh and `heft`, a saw or an axe for bone. They are the same operations every carcass takes,
  the hare's and the bear's included; a person is not special to the engine. `cover` needs its own
  operation (today it parses to `wrap`), the same one that covers the hull's openings (document 08
  §6 Q7).
- **Raw or cooked.** Cooking is not required, and "an illness risk" is too thin to be true: raw, frozen,
  cooked and spoiled flesh are four different states with four real consequences — clean raw meat is
  edible and as safe as raw meat gets, its risk rising with a punctured gut and dirty hands; frozen
  raw is real northern food that costs about 95 kcal of body heat per kilogram to eat; cooking kills
  bacteria and parasites and yields more energy; spoiled meat stays dangerous after cooking because
  some toxins survive heat. What a person's flesh carries beyond that (prions, blood-borne infection)
  takes years to show — true, and outside the run.
- **Findable.** Yes, physically: a covered body is a shape under a blanket; a snow burial or a cairn
  is a mound; outside, the storm's snow buries him further by itself. Covering and burying are real acts that
  can be undone by uncovering and digging, and the animals can undo them too — the bear digs and
  caches, the ravens pick at what is exposed.
- **Consent and witness.** No gate: anyone can do any of it, alone (2026-09-16, no lethal-consent
  gate). The witness rule is document 15's — witnessed by whoever could perceive the act, by band —
  and the evidence the act leaves (a smaller shape under the blanket, blood on a knife, meat by the
  fire) is how the others find out otherwise.
- **What he is worth.** About 38,000 kcal of muscle in a 78 kg man (Cole 2017), plus fat, organs and
  marrow: two to three days for a party of five. And his body is the strongest attractant in the
  valley — to the ravens first and, in October, to the bear, which guards what it finds.

**Q6 — Dead players' bodies: what are your friends told, and when?** *(Sharpened 2026-09-26 — the old
options (a) persists / (b) exempt from butchering / (c) removed are answered.)* The physics, for
Andrew's check: a dead player's body stays where they died, an entity exactly like the pilot's
(§4.3a) — their clothes on it, their pockets full, cooling, stiffening, freezing, smelling to the
bear — and every act on the pilot works on it. Removing it, or exempting it from butchering, would be
the engine refusing physics, which the no-lethal-consent decision (2026-09-16) already ruled out. What
is genuinely yours is the social frame: friends will be doing this to each other's characters, and
the dead friend's ghost can walk in and watch (ghosts move freely — 2026-09-17). Options: *(a)*
nothing is said — the world is what it is, the discovery is part of the evening, and the ghost's
out-of-character chat is where the table reacts; *(b)* one out-of-world sentence before a friends'
run, in the tutorial, that the dead stay in the world as bodies and anything the living can do to a
body can be done to theirs — naming no act; *(c)* the host chooses per run between (a) and (b).
*Recommendation:* (b) for friends' runs and (a) for agent-only research runs. One honest sentence
before anyone is attached to a character spares a friend finding it out as a ghost; it names no verb,
so it is not a menu, and after it the world never mentions the matter again. A research run has no one
to spare, and saying nothing keeps the agent's behaviour its own.

~~Q7 — Does the run open with him alive? Recommendation: he starts alive.~~ **Closed 2026-09-17
(Andrew): he starts dead** — the shipped `state: {'dead': True}` and `rooms/cockpit.md` §1 ("slumped
dead against the forward bulkhead") are correct as they stand.

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

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-reviewed against block 1 (03–09), the decisions
  since (the dead start, ghosts, October, the bear, combat, body parts carry heat, raw/cooked/spoiled
  differ) and real forensic, food-safety and wildlife sources. **Added §4.3a** — the body as an entity:
  its parts, materials and states (heat per part, rigor, frozen, spoilage, smell with a range, the
  record of what was done), what it could become (strip, search, move, cover, bury, burn, butcher),
  what butchering yields (~38,000 kcal of muscle, Cole 2017), what raw, frozen, cooked and spoiled
  flesh really do, and the body as the bear's and the ravens' attractant. **Answered, for Andrew's
  check:** Q5 (`butcher` as an attended activity of real cuts; no cooking gate, four real food states;
  covered and buried bodies stay findable; no consent gate, the witness rule and the evidence).
  **Struck as closed by Andrew on 2026-09-17:** Q1–Q4, Q7. **Left for Andrew:** Q6, sharpened — the
  physics of a dead player's body is answered; whether his friends are told before a run is his.
  §1, §2, §3 (rewritten for October and the dead start, the old paragraph kept), §4.2, §4.3, §4.4 and
  §5 annotated as superseded where the dead start overtook them. Needs design documents: heat, food
  state and spoilage, animal behaviour; document 14's clue paths that named the pilot need
  replacements.

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
butcher path, the dilemma probe. *(superseded 2026-09-26: the death clock, the moaning, the lines and
tending are gone with the dead start. What is designed and unbuilt is §4.3a — the body's parts and
states, its could-become rows, butchering, the food states, the animals' smell — plus a content fix:
`objects.py` authors him as `materials: ['flesh']`, and §4.3a's materials are skin, fat, muscle, bone,
blood and organs.)* `game/world/scenarios/whiteout/authored.py` names the pilot as a
future authored packet and is empty. The rescue graph §4 lists `press`, `cover`, `carry` and
`butcher` among the verbs the world still needs; `butcher` has no handler, and `cover` currently
resolves to `wrap` in `game/world/sim/parser/vocab.py`.

**Nothing** — no pilot process of any kind runs. There is no timer, no state transition from alive to
dead, no sound event, no line, no body-state field, no meat. The world currently starts with him
already dead (Q7). *(2026-09-26: correct since 2026-09-17. Also nothing yet: no body parts as
entities, no per-part heat, no rigor, freezing or spoilage, no smell with a range, no `butcher`,
`skin`, `gut` or `bury` operation.)*
