# Game-design lenses (GD1–GD25)

GD1–GD19 adapt lenses from Jesse Schell, *The Art of Game Design: A Book of Lenses* (3rd ed.).
GD20–GD25 are immersive-sim / interactive-fiction lenses for systemic "do-anything" text worlds.
Each: **key question** · *what to look for* · applies-when.

**SCOPE & CONSTRAINTS.** These lenses review design **execution** — mechanics, systems, pacing, feel,
structure — *within* the locked vision (genre, premise, core promise, and any user-locked decisions; see
`VISION.md` and the GDD/plan "Decisions" lists). They do **not** recommend changing the vision itself. If
a finding's only fix would alter the genre, premise, or a locked decision, reframe it as a
*risk-within-the-vision* (mitigations that keep the decision intact) or mark it *"outside scope —
vision-level flag"* for the user to decide — never "build something else." (See `SKILL.md` Protocol
steps 2 & 4.)

---

### GD1 Essential Experience
**What experience must the player have, and is every system in service of it?**
*Name the single feeling; check each mechanic delivers or distracts from it. UI/parser friction
that buries the feeling is the usual culprit.* — Applies to any design at any stage.

### GD2 The Toy
**Is it fun to play with before there's a goal?**
*Strip the objective: is messing with the world delightful on its own? If not, goals won't save
it.* — Applies to sandbox/systemic/sensory designs.

### GD3 Curiosity
**What questions does the game put in the player's mind, and does it make them want answers?**
*Hooks that raise "what's behind that?", "could I…?"; affordance hints that open more than they
close.* — Applies to exploration/puzzle/systemic.

### GD4 Fun (chore audit)
**Where is the pleasure, and where is the chore masquerading as depth?**
*Walk every repeated action (timers, resource accounting, grinds); mark each "tension" or
"tedium". Depth ≠ fun.* — Applies whenever there is repetition or sim depth.

### GD5 Endogenous Value
**Do players value in-world things for in-world reasons?**
*Do resources/relationships acquire felt worth, or stay spreadsheet tokens? Value must come from
the game's own goals, not external scoring.* — Applies to economies/survival/RPG.

### GD6 Problem Solving
**What problems does the game ask, and how many genuinely different solutions exist?**
*Count honest solution paths; check they require different reasoning, not reskins.* — Applies to
puzzle/strategy/systemic.

### GD7 Meaningful Choices
**Are choices meaningful, or is there a dominant strategy that collapses them?**
*Find the always-best option; if one exists, the choice is fake. Look for balanced alternatives
with different profiles.* — Applies wherever the player chooses.

### GD8 Triangularity
**Is high-risk/high-reward weighed against low-risk/low-reward?**
*The classic risk gradient: is the bold play tempting AND dangerous, the safe play viable but
lesser?* — Applies to any risk/resource design.

### GD9 Skill vs Chance
**Is progress earned by skill/understanding or by chance, and is the mix right for the audience?**
*Where randomness enters — does it feel fair and legible, or arbitrary? Determinism suits
puzzle/imm-sim.* — Applies wherever RNG or timers exist.

### GD10 Interest Curve
**Does the player's engagement rise, spike, and resolve over a session?**
*Sketch the curve: a hook, rising tension, spikes, a climax. Hunt the mid-game sag.* — Applies to
any timed/session experience.

### GD11 Failure
**When players fail, do they blame themselves and want to retry — or blame the game and quit?**
*Failures must teach. A flat wall ("nope") is the enemy; informative, fair failure invites
mastery.* — Applies to any challenge.

### GD12 Freedom / Indirect Control
**How do you make a bounded world feel boundless, steering without caging?**
*Where is the real ceiling (verb set / content), and how invisible is it? Constraints disguised
as affordances, environment that suggests rather than forces.* — Applies to open/systemic designs.

### GD13 Imagination
**How much does the player's mind fill in, and is that doing work for you?**
*Especially text: evocative-but-sparse beats exhaustive. The asset only holds if the filled-in
world stays consistent.* — Applies to text/minimalist/horror.

### GD14 Accessibility
**How does a newcomer learn what's possible without a manual?**
*First-minutes teaching; the gap between the promised verbs and the parsed verbs; gentle
affordance surfacing.* — Applies to any complex interface.

### GD15 Story–Mechanic Harmony (Unification)
**Do the mechanics tell the intended story, or fight it?**
*Each mechanic should dramatize the theme (e.g. scarcity mechanics → felt desperation), not break
immersion with bookkeeping.* — Applies to narrative games.

### GD16 Cooperation
**What does the design make players do together that is fun, not just logistics?**
*Interdependence that creates shared moments (one holds while another acts); is co-op a story
engine or a chore splitter?* — Applies to multiplayer/co-op.

### GD17 Goals
**Does the player always know a meaningful next goal — short and long?**
*Open/emergent designs risk "what do I do?"; check for legible near goals without a quest-log
crutch.* — Applies to open-ended designs.

### GD18 Time / Pressure
**Is the pressure of time felt AND fair?**
*Clocks/timers must read as drama, not punishment for thinking/reading. Watch wall-clock waiting
and forced pace.* — Applies to real-time/timed designs.

### GD19 Reward
**What does the game give for clever or deep play, and is it legible enough to motivate it?**
*Are deeper efforts rewarded with safety/quality/options, and does the player SEE the reward?* —
Applies to mastery/crafting/survival.

### GD20 Affordance Discoverability *(immersive-sim)*
**Can players find what's possible without being spoiled or stranded?**
*The tightrope between guess-the-verb (too few hints) and checklist (too many). Examine-text and
environmental cues are the dial.* — Applies to systemic/parser worlds.

### GD21 Parser / Intent Legibility *(IF)*
**Does the player trust the game understood what they meant?**
*A silent mis-parse that does the wrong thing is worse than a clean "didn't understand."
Disambiguation, confirmation on low confidence, echoing intent.* — Applies to NL/parser input.

### GD22 "Do-Anything" Expectation Management *(immersive-sim)*
**Does the promise of "everything" survive contact with the wall?**
*Find where a sensible attempt can't be represented; the failure must stay in-fiction and physical
— never "not implemented." How is the boundary hidden?* — Applies to open/systemic promises.

### GD23 Systemic Consistency *(immersive-sim contract)*
**Does the same rule apply everywhere, so players can trust the simulation?**
*If fire+foam=toxic-smoke once, it must everywhere; authored special-cases are where the contract
leaks and players stop trusting the world.* — Applies to systemic worlds.

### GD24 Emergent Narrative *(operative → resultant)*
**Do simple actions combine into stories the author never scripted?**
*Trace 2–3 unscripted chains end to end; is there a capture/payoff (a retelling, an ending
record)?* — Applies to systemic/sandbox/sim.

### GD25 Resolution-Not-Success *(text-world core)*
**Does every attempt produce a real, physical answer (not success, but resolution)?**
*Audit how informative failure is generated AT SCALE without hand-authoring each case; "You can't
do that" is a defect.* — Applies to "try-anything" designs.
