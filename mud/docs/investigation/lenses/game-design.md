# Game-design lenses — finding cards (GD1–GD25)

**Scope.** Reviewing the *intended* build of **Whiteout** — the original design
(`docs/scenarios/whiteout/design.md`, §1–49) **as amended by** the engine proposal
(`docs/proposals/whiteout-engine-proposal.md`: operation×material engine, cheap objects,
resolve-then-crystallize loop, instanced co-op runs, event-driven clock, vertical-slice-first,
auto-generated story). Where the proposal fixes a design risk I say so; where the risk survives I
flag it. Goal under test: **is it FUN (not merely deep), and does the "do-anything" promise survive
the wall?** Adversarial throughout — hunting the failure, not confirming the pitch. Leverage ratings
are from `docs/investigation/lenses/triage.md`; HIGH lenses get a paragraph, MED a few sentences.

---

### GD1 Essential Experience
- **Verdict:** GREEN
- **Evidence:** §2 "survives by understanding the world, not by guessing the author's intended verb-object pair"; perception (§10–15), conservation (§24), rescue confidence (§39) all serve "the world is the puzzle."
- **Note:** The single feeling — *understand a living, physically-modeled world under pressure* — is named clearly and nearly every system dramatizes it. Certain because the spine is explicit and coherent. The one drag is UI/parser friction (the §9.4 stat-block HUD "Progress 7/18 · Stamina 82% · Hands occupied" competes with the "living world" mood); that delivery risk is real but is owned by GD4/GD18, not by the experience definition.

### GD2 The Toy
- **Verdict:** YELLOW
- **Evidence:** §3.5 / §29 toy attempts (lick the frozen latch, wear the seat cover as a cape, stack food trays); §40 examine-hints; proposal §8 "The Toy first" and §10.1 vertical slice whose goal is "prove try-anything → resolves plausibly → feels alive."
- **Severity:** high
- **What would change the verdict:** a shipped vertical slice where naive players stay delighted poking the cabin for 2+ minutes with **zero** rescue intent, AND evidence that *generic-physics* responses (not just the one authored example) read as specific and witty rather than same-y.
- **Note:** This is the make-or-break lens and it is currently a **promise, not a proven asset**. The design supplies exactly **one** delightful toy response — the §3.5/§31 shirt-windbreak ("flaps too wildly… stretch it between branches"). Everything else is a list of attempts, not a demonstrated delight. The adversarial worry: the proposal's cheap-object/rich-operation inversion (proposal §2) means ~80–90% of objects ride **generic** physics, and generic resolvers tend to emit correct-but-dry text ("barely marks it; needs a real edge" — proposal §3.1 template). If poking ten objects yields ten variations of the same templated physics line, the toy is depth without delight. Toy-quality is also **unvalidated** — "feels alive" (proposal §10.1) is the success criterion but there is no test, rubric, or playtest gate for it. The whole downstream stack rests on this 2-minute experience being magic, and right now its magic is one paragraph deep.

### GD3 Curiosity
- **Verdict:** GREEN
- **Evidence:** §40 examine ("You could probably: cut it… unbolt it… pry the anchor… use it to restrain/bind/lash"); §38.2 antenna clue ("torn metal base juts from the skin, cable hanging loose, rimed with ice"); §11 perception ("someone moves near a dim patch of smoke").
- **Note:** Strong "could I…?" and "what happened here?" hooks; the broken antenna and the dying pilot are good mystery seeds, and perception-at-range provokes "who's that?". One tension: §40's affordance *list* can **close** curiosity by spoiling the answer before the player wonders the question — handed to GD20.

### GD4 Fun (chore audit)
- **Verdict:** YELLOW
- **Evidence:** §9.4 tick-saw ("You saw at the frozen webbing… Progress 7/18 minutes… Stamina 82%"); §9.5 five worker meters (stamina/fatigue/hand-warmth/pain/hunger/hydration); §24 per-object temperature/wetness/contamination accounting; proposal §7 event-driven clock + action-chunking, §8 "depth only while it teaches (Koster)."
- **Severity:** high
- **What would change the verdict:** an explicit chore-audit playtest rating each repeated action *tension* vs *tedium*, plus confirmation that action-chunking actually fires for the common repair/craft chains and that tick messages escalate stakes rather than counting minutes.
- **Note:** This is the deciding lens for "fun, not just deep," and the design is **dense with bookkeeping that must each earn its keep**. An 18-minute saw (§9.4) is many near-identical ticks; five live meters per worker (§9.5) is a lot to babysit; conservation (§24) is rich but fiddly. The proposal lands real fixes — the event-driven clock kills idle drain, action-chunking (Hadean-Lands lesson) collapses a *mastered* chain to one command, and "tick messages escalate stakes" (brainstorm §8: "the wind shifts; your fingers won't close"). These convert the worst RED (the §9.3 wall-clock heartbeat) into something workable. But the residual is genuinely uncertain: the **first** seatbelt-saw is tense, the **fifth** is tedium, and chunking-in-a-text-game while *preserving felt desperation* is unproven; "depth only while it teaches" is the right principle but a principle, not a mechanism. Many meters + many ticks is exactly where depth masquerades as fun.

### GD5 Endogenous Value
- **Verdict:** GREEN
- **Evidence:** §31 scarcity ("matches, rare and possibly wet"; "lighter, possibly empty"); limited fuel/daylight (§6); conservation makes a cut strap permanently shorter (§24).
- **Note:** Survival stakes give tinder, charge, the one knife and warmth real felt worth, and conservation enforces that loss is permanent, so hoarding/triage decisions matter in-world. Mild adversarial caveat: aggressive do-anything improvisation can **erode** scarcity (why guard the knife if any sharp edge serves?), but material gating (§45 "cannot cut steel bolt with pocketknife") keeps key bottlenecks real. Low uncertainty.

### GD6 Problem Solving
- **Verdict:** GREEN
- **Evidence:** §7 rescue paths (beacon / radio / visual / smoke / travel / weather-window); §38.3 antenna from many materials; §39 "rescued through at least four distinct combinations."
- **Note:** The headline problems demand genuinely **different reasoning** — RF/electrical (beacon), comms+information (radio), navigation (travel), thermoregulation (stay alive) — not reskins. Honest path-variety. One soft spot: the *visual* cluster (smoke, firelight, bright fabric, SOS, mirror flash — §7/§39) collapses to a single reasoning mode ("be conspicuous"), so the "four combinations" lean on fewer than four distinct *cognitive* problems than the count implies.

### GD7 Meaningful Choices
- **Verdict:** YELLOW
- **Evidence:** stay-vs-leave (§7 "moving away… can help or doom"; §8 weather worsens travel hourly); §39 additive rescue confidence; §38.3 beacon-antenna-as-antenna "costly tradeoff"; §19.1 tend-vs-interrogate pilot.
- **Severity:** med-high
- **What would change the verdict:** a tuned **opportunity-cost** model where pursuing one rescue method measurably sacrifices another (shared fuel/daylight/labour/warmth), plus a demonstration that "stay and signal" does **not** strictly dominate the travel routes.
- **Note:** Two latent dominant strategies threaten to collapse the choice space. **(1) Stay dominates travel.** The weather arc (§8) makes leaving monotonically more dangerous as the day worsens, while staying lets rescue confidence accrue at a known location (§39) — so the rational play converges on "stay, signal, survive," and the travel-rescue routes (weather relay, logging road, abandoned camp — §7) risk being a *trap* dressed as a choice rather than a live alternative. **(2) Additive confidence becomes a checklist, not a choice.** §39 makes beacon + radio + smoke + SOS all simply *add* to a hidden confidence pool; if they don't **compete** for a shared scarce resource, the optimal play is "do all of them," which is logistics, not decision. The design has the raw ingredients for real tradeoffs (limited fuel §31, limited daylight §6, bodies-on-task, the §38.3 beacon-vs-antenna sacrifice — a genuinely good triangle) but never makes the rescue methods *rivalrous*, so the meaningful choice is asserted (§7 "no single path should be the real solution") more than it is mechanically guaranteed.

### GD8 Triangularity
- **Verdict:** GREEN
- **Evidence:** §31 fuel-assisted ignition ("powerful and dangerous": flare/burn/spread) vs friction fire; §31 fire inside the fuselage (warmth vs CO / toxic smoke); §38.3 beacon antenna as radio antenna ("costly tradeoff" — sacrifice one rescue path to boost another); §31 "loss of useful materials" (burn for heat vs keep for tools); §19.3/§36 cannibalism (calories vs morale/ending); §7/§39 leave (new routes vs leaving the search area).
- **Note:** Arguably the **strongest** lens in the set. Multiple independent, in-fiction high-risk/high-reward axes are concretely specified, each with a viable-but-lesser safe option — the textbook risk gradient. Conservation + scarcity make bold plays simultaneously tempting and genuinely dangerous (a burned frame is *gone*). Certain because the structure is explicit and varied across at least five distinct axes. The only open item is **tuning** the probabilities (e.g. fuel-flare odds) into the fair zone so the bold play is *sometimes* correct — a balance problem (GD9), not a structural one.

### GD9 Skill vs Chance
- **Verdict:** GREEN
- **Evidence:** deterministic lean throughout; stochastic bits = pilot timers (§19.1 "3 to 8 minutes," "15 to 35 minutes"), §38.5 "small_chance_of_getting_attention" / "occasional broken fragment"; proposal §4 seeds RNG + deterministic replay.
- **Note:** Determinism suits an imm-sim/puzzle and the redundant clue paths (§19.2) keep randomized pilot-death from gating information by luck. One watch-item: §38.5's random radio fragments paired with "high time cost / battery drain" can feel like an unfair *grind on a coin-flip* (a GD18 cost on a chance event); make the persistence-pays curve legible so it reads as earned, not lucky.

### GD10 Interest Curve
- **Verdict:** YELLOW
- **Evidence:** cold-open hook (§16 buckled into different seats, dying pilot, §47); rising tension via weather escalation (§8 light→steady→heavy→whiteout→night) + pilot death timer (§19.1); proposal §6 instanced ~1 in-game-day run; proposal §8 mid-run beats (a search plane that misses you, the pilot's last lucid fragment).
- **Severity:** med
- **What would change the verdict:** authored mid-game spike beats with **concrete triggers** (not a wishlist), a target real-session length validated in playtest, and a plan to keep divergent multiplayer curves from desyncing.
- **Note:** The skeleton is excellent — a strong hook, a built-in rising ramp from weather + pilot clock, and a natural climax at whiteout-night/rescue. The danger both the brainstorm (§8) and the proposal (§8) already name is the **mid-game "survive the night" sag**: after the frantic opening scavenge and pilot drama comes a long flat valley of shelter-building, snow-melting and fire-tending. The proposal's mid-run beats are the right antidote but are listed as *ideas*, not designed beats with triggers and pacing. Two unproven multipliers: (a) sustaining a rising curve across what an event-driven ~1-day run could stretch to 1–3 real hours, deliberately through a tedious valley; and (b) **multiplayer curve desync** — a forest scout and a cabin radio-operator live different arcs, and one player's spike (radio contact) is another's dead air, so "the" interest curve is really N curves that can fall out of phase.

### GD11 Failure
- **Verdict:** GREEN
- **Evidence:** §3.5 / §28 "make every attempt resolve"; §38.4 radio feedback ("improve your antenna if you can"); proposal §8 auto-generated story reframes loss as narrative; proposal §6 instanced runs (permadeath of a run).
- **Note:** "Every attempt resolves" is the right anti-flat-wall stance and informative failure (the §3.5 windbreak redirect) is the model — failures teach and invite a better attempt. Open question lives downstream at GD25 (can that teaching be *generated at scale*) and at AR6/GD7 (a run-ending death from a global softlock would feel like a wall, not a lesson); the auto-story (proposal §8) softens run-loss into "the story of how it went," which is the right emotional cushion.

### GD12 Freedom / Indirect Control
- **Verdict:** YELLOW
- **Evidence:** the ceiling = ~20 operation categories (§5) × ~25 materials (§21); hidden via §40 examine-hints, proposal §3.4 "affordances computed from state + informative redirect," and proposal §3.6 resolve-then-crystallize.
- **Severity:** high
- **What would change the verdict:** evidence (from the vertical slice) that the ~20 operations *compose* into enough surface variety that players don't pattern-match the cage within a session, plus a redirect system that **varies** its steering rather than funnelling visibly to the same handful of verbs.
- **Note:** Making a bounded ~20-verb world feel boundless is the project's core illusion, and the proposal's machinery is the right kind — affordances derived from state, sensible attempts redirected in-fiction, and a crystallize loop that can *mint* new authored rules from play. The combinatorial space is genuinely large (the BotW "few rules × many objects" lesson, proposal §2). **But the primitive ceiling is low and uniform, and uniformity is itself detectable.** A redirect that always steers toward the same ~20 operations will, over a session, teach the player the *shape* of the cage ("everything funnels to cut / burn / tie / heat"). Crucially the crystallize loop expands content **within** the ceiling — new rules are "constrained to existing operations + material state" (proposal §3.6) — so it deepens combinations but cannot grow the primitive vocabulary; an intent needing a genuinely new operation or property can only be redirected, never granted. Boundlessness is real for *combinations* and bounded for *primitives*, and the question the design hasn't answered is whether composition-variety outruns the player's pattern-matching of the verb set. This is the central GD12 ✕ AR5/IM5 tension.

### GD13 Imagination
- **Verdict:** GREEN
- **Evidence:** §11/§13 evocative-sparse perception prose ("the plane is a broken shape through the falling snow"); §2 material-level texture ("fabric, foam, webbing, buckles, bolts").
- **Note:** Text + degraded perception lets the player's mind do real work, which is an asset here. It only holds if the filled-in world stays **consistent** (GD23): the proposal's AR15 runtime assertion — no prose referencing state with no backing Effect — is the guard against the LLM imagining objects/changes that aren't in engine state. Consistency risk handed to GD23.

### GD14 Accessibility
- **Verdict:** YELLOW
- **Evidence:** §40 examine surfaces affordances; §29 first-minute attempts have "defined response paths"; §16/§47 cold open; no explicit tutorial.
- **Severity:** low
- **What would change the verdict:** a deliberate first-five-minutes that teaches *operation composition* by doing, rather than relying on examine-hints alone.
- **Note:** A free-text "do-anything" world has a wide promise/parse gap and no manual; the cold open (buckled in, §16 — first goal is self-evidently "get free") is a nice tutorial-by-constraint, but there's no designed teaching that the ~20 operations exist or that they *compose*. Overlaps GD20/GD21, which carry the heavier signal.

### GD15 Story–Mechanic Harmony (Unification)
- **Verdict:** GREEN
- **Evidence:** scarcity/cold/conservation → felt desperation (intended throughout); §19.3/§36 cannibalism mechanically supported and ending-recorded; brainstorm §8 "tick messages should dramatize desperation, not just meter it."
- **Note:** The mechanics mostly *are* the theme — scarcity dramatizes desperation, conservation makes loss permanent and grief-laden, the body/cannibalism systems carry real weight. The one immersion-breaker is the §9.4 numeric HUD ("Stamina 82%"), a restatement of the GD4 meter-vs-mood concern; resolve it there.

### GD16 Cooperation
- **Verdict:** YELLOW
- **Evidence:** §9.4 one player saws while another acts; §9.5 "ask another player to take over"; §16 different seats → different nearby affordances; §15 cross-zone shout/relay; §38.3 antenna "held by hand shakily"; §32 shared body heat; proposal §10.6 defers multiplayer and lists "cooperation moments" as an unspecified TODO.
- **Severity:** med-high
- **What would change the verdict:** ≥2 **designed** interdependence moments that require simultaneous coordinated action and produce a shared story beat (e.g. one stabilizes the wreck while another extracts the pilot; one relays landmark bearings from the ridge while another talks the rescuer in), made first-class and **not strictly worse than solo**.
- **Note:** This is the least-developed of the HIGH lenses. As written, Whiteout's co-op is mostly **parallel labour** — split the task list, hand off a tiring job, work different zones — which is the "chore splitter," not the "story engine," the lens warns against. The genuine interdependence moments are thin and often *discouraged*: holding the antenna by hand is explicitly the **poor** option (§38.3), huddling (§32) and two-person body-carry (§19) exist but are minor. The design's best latent co-op idea is the **spatial-perception relay** — a scout in the forest calling landmark bearings (§15 shout across zones) back to an operator at the radio (§38.8 needs landmark info) — which *is* real interdependence and produces a story, but it's emergent and unhighlighted, and the proposal pushes all of this to build-step 6 with the moments still unspecified. Instanced runs (proposal §6) correctly make sabotage/theft/cannibalism (§27) socially safe among invited friends; that's a fix for griefing, not for making togetherness *fun*.

### GD17 Goals
- **Verdict:** YELLOW
- **Evidence:** cold-open immediate goals (get free, the dying pilot, the cold); §19.2 pilot fragments point at beacon/radio/landmarks; §38.4 radio responder asks for location; no quest log (good).
- **Severity:** low
- **What would change the verdict:** a reliable **diegetic goal-surfacing channel** (radio responder / pilot consistently naming the next concrete need) so mid-game players always have a legible near goal.
- **Note:** Near goals are well-seeded in the opening and the radio responder's "need landmarks: ridge, river, road" (§38.4) is an elegant no-quest-log goal cue. The risk is the mid-game additive sandbox leaving players adrift ("we have a fire — now what?") because rescue confidence is a *hidden* number (§39); goal legibility depends on environmental/NPC cues that can be missed.

### GD18 Time / Pressure
- **Verdict:** YELLOW
- **Evidence:** §9.3 "10–20 real-seconds = 1 game-minute" wall-clock heartbeat; §9.6 fast-forward requires **all** players idle; §9.1 explicitly wants to avoid "losing daylight while reading room text"; proposal §7 replaces this with an **event-driven clock** (advances only on action) + scheduled activities + consensual fast-forward + action-chunking.
- **Severity:** med
- **What would change the verdict:** a **multiplayer** clock rule that advances fairly without punishing the slow reader, AND a demonstrated mechanism that keeps time-pressure *felt* under an event-driven clock (weather/pilot beats on action-budget or soft real-time triggers that create urgency without wall-clock waiting).
- **Note:** The original §9 heartbeat is the design's most dangerous subsystem and a textbook violation of this lens: a 90-game-minute shelter build = 15–30 real minutes of waiting (brainstorm §5); fast-forward needs *everyone* idle (§9.6), so one AFK player blocks the party or the active player waits in real time; and the wall-clock coupling reintroduces the exact thing §9.1 swears off — you **do** lose game-time while thinking and reading. The proposal's event-driven clock is the correct fix and moves this off RED: no idle drain, thinking is free, long actions don't jump others' clocks. Two residual risks it doesn't fully close. **(a) Multiplayer fairness:** if any player's action advances the shared clock, a fast actor drains daylight on a slow reader — the §9.1 problem returns in multiplayer form, and the proposal doesn't specify whose actions tick the shared world. **(b) Felt pressure:** an event-driven clock that only moves when you act means a cautious player can deliberate **forever** with zero urgency — fairness bought at the cost of the storm's drama. Balancing "fair (no wait-punishment)" against "felt (real urgency)" is the unsolved core, and it's the GD18/GD4 ✕ multiplayer-tick tension flagged in the triage.

### GD19 Reward
- **Verdict:** GREEN
- **Evidence:** §4 "reward deeper work with better quality, safer outcomes, more rescue confidence, fewer costs"; §37 beacon ladder (0→85); §38.6 radio ladder (dead→useful_contact); §38.4 responder feedback ("your signal is stronger now").
- **Note:** Deeper/cleverer play is rewarded and — importantly — the reward is **legible** via the signal ladders and the responder's explicit quality feedback, so the player *sees* improvement. One gap: the aggregate rescue confidence (§39) is a *hidden* number, so visual/beacon/staying-put contributions may go unseen; mirror the radio's diegetic feedback ("your fire is visible from the ridge now") onto the other rescue channels.

### GD20 Affordance Discoverability *(immersive-sim)*
- **Verdict:** YELLOW
- **Evidence:** §40 examine ("You could probably: cut it with a sharp tool / unbolt it / pry at the anchor / use it to restrain, bind, lash"); §40 "Examining objects reveals plausible affordances without spoiling everything"; proposal §3.4 affordances-from-state + informative redirect.
- **Severity:** med-high
- **What would change the verdict:** a tuned, *tested* affordance-surfacing policy — examine hints at material **properties** and a couple of verbs, never the full set; environmental cues over explicit menus — validated so smart players progress without either guess-the-verb dead-ends or checklist-reading.
- **Note:** The discoverability dial sits between guess-the-verb frustration and checklist tedium, and the design currently leans **checklist**: §40's examine *enumerates* affordances, which (i) spoils the joy of "could I…?" (GD3), (ii) makes the verb cage visible (undercutting GD12), and (iii) trains players to do only what's listed — the opposite of the do-anything ethos (§3.5), where the intended player ignores the menu and tries wild things. Yet trimming the list too far reverts to parser guess-the-verb, which is fatal for accessibility (GD14). The proposal's compute-affordances/redirect machinery is the right plumbing but is silent on the **display** question — *how much* to reveal — and that line is per-object and unset. The tension is structural: the same hint that rescues the newcomer (GD14) erodes the boundlessness illusion (GD12) and the discovery thrill (GD3).

### GD21 Parser / Intent Legibility *(IF)*
- **Verdict:** YELLOW
- **Evidence:** §40 NL input ("cut the seatbelt with the pocketknife"); §25 parse → structured ActionAttempt; §26 "LLM interpretation into existing action" (silent, no confirmation in the original); proposal §3.3/§4 Stage-A intent parse with "low-confidence → confirm intent" + echo + cache + deterministic fallback; brainstorm §7.
- **Severity:** med
- **What would change the verdict:** a tuned confidence threshold + the confirm-on-low-confidence loop actually built and tested against adversarial creative phrasings, plus an **irreversible-action guard** (always confirm before destroying a scarce/irreversible object, regardless of confidence).
- **Note:** A silent LLM mis-parse that does the *wrong* thing is worse than a clean "didn't understand," and in a conservation world (§24) a mis-mapped "burn" vs "char" can irreversibly destroy a scarce object and waste real time. The original design has **no** disambiguation — §26 just silently resolves the LLM's guess. The proposal fixes this squarely (echo intent: "You try to *pry* the panel with the knife — yes?"; confirm on low confidence; cache; deterministic timeout fallback), moving it well off RED. Residual risk: the confidence *threshold* is unset (too eager = nag friction = GD4; too confident = silent mis-parse), and parsing "against the engine-computed affordance set" (proposal §3.3) can map a creative intent to the **nearest wrong affordance with high confidence** — the dangerous confidently-wrong case the confirm loop won't catch.

### GD22 "Do-Anything" Expectation Management *(immersive-sim)*
- **Verdict:** YELLOW
- **Evidence:** §3.5 the loud promise ("Everything physical should be tryable"; "Not everything needs to work. Everything should resolve"; "Bad response: *You can't do that.*"); proposal §3.4 affordances-from-state + informative redirect + wall-sensor; proposal §3.6 resolve-then-crystallize; proposal §3.5 soft-adjudication-on-rails.
- **Severity:** high
- **What would change the verdict:** a shipped vertical slice where a large fuzz sample of *sensible* attempts all resolve **plausibly** (not merely validly), the wall-sensor queue stays shallow in live play, crystallize demonstrably mints *fun* rules within the latency budget, and §3.5's "everything" is reframed in player-facing language so the promise isn't read as literal.
- **Note:** This is the **existential** lens and the proposal does more to defuse it than any other, pulling it from a hard "You can't do that" wall (RED) to a soft, honest, slowly self-healing redirect. The machinery is genuinely the best available answer: affordances computed from state, sensible misses redirected in-fiction ("not this, but you could tie it between branches"), a wall-sensor logging every generic-redirect as the authoring queue, and a crystallize loop that turns unhandled attempts into validated cached rules so *play becomes authoring*. But the promise of "**everything** resolves meaningfully" stays overstated, and four seams remain. **(1) The redirect is a tell** — repeated, it teaches the boundary's shape; the honest "not this, but these" maps the cage politely. **(2) New primitives can't be minted** — crystallize is "constrained to existing operations + material state" (proposal §3.6), so an attempt needing a genuinely new operation/property can only ever be redirected, a permanent hard wall. **(3) Validated-but-dull masks the wall** — the validator checks conservation/physics, not *meaning* or *fun*, so a technically-valid mush resolution ("you rub the two covers together; nothing useful happens; conservation holds") passes the gate and ships as the canonical answer to a creative idea. **(4) Latency at the worst moment** — crystallize is a runtime LLM round-trip; the player trying the novel thing waits, and a timeout falls back to the redirect, i.e. the wall fires exactly on the creative attempt. Net: the wall is much better hidden than in the original design, but "everything resolves *well*" is not yet true, and this is the single biggest existential risk in the review.

### GD23 Systemic Consistency *(immersive-sim contract)*
- **Verdict:** YELLOW
- **Evidence:** proposal §2/§3.1 operation×material engine (uniform rules over material vectors) — the right foundation; §26 tier-1 "authored puzzle rule" + object-specific rules (radio/beacon/pilot kept as authored specials, proposal §2); proposal §3.5 soft-adjudication verdicts cached by "situation"; proposal §3.6 runtime-crystallized rules; §24 conservation as the backbone (+ AR15 runtime assertion).
- **Severity:** high
- **What would change the verdict:** a consistency invariant enforced in `make validate` **and** at runtime (same operation+material+tool ⇒ same qualitative outcome everywhere, specials included); coarse-but-predictable soft-verdict caching with a determinism test; and a crystallize **dedup/normalization** step that checks each new rule against the existing rule set, not just against conservation.
- **Note:** "Same rule everywhere, so players can trust the sim" is the imm-sim contract, and the operation×material engine is built precisely to honour it — uniform physics over material properties is the strongest possible base, and conservation-as-runtime-invariant (§24 + AR15) is a real enforcement hook. But three live leak sites threaten the contract. **(1) Authored specials (§26 tier-1):** the radio's bespoke antenna-quality computation (§38.3) and the scripted pilot are overrides of the uniform rule; if the *same* aluminium frame behaves by one logic as "antenna" and another as "lever," the player feels the seam — and the triage names this exact GD23 ✕ §26-tier-1 conflict. **(2) Per-situation soft-verdicts (proposal §3.5):** the LLM judging "does this contraption count as a windbreak ≥0.5," clamped and cached by "situation," will give *different* verdicts to *similar-but-distinct* contraptions unless the cache key is tuned just right — coarse keys break predictability, fine keys break consistency, and inconsistent adjudication is exactly where players stop trusting the world. **(3) Runtime crystallization (proposal §3.6):** two players' divergent minted rules for "the same" interaction can conflict, because the validator gates on conservation, not on *global consistency with the existing rule set*. The foundation is right; the three override channels are where the contract can quietly leak.

### GD24 Emergent Narrative *(operative → resultant)*
- **Verdict:** YELLOW
- **Evidence:** operation×material composition + §24 conservation + §23 first-class derived objects + §14 perception → unscripted chains (cut cover → strips → lash splint → carry pilot; burn foam → toxic smoke → CO scare; the §19.3/§36 cannibalism arc); proposal §8 "the run's auto-generated story" summarizing the deterministic event log into a retrospective narrative.
- **Severity:** med
- **What would change the verdict:** 2–3 unscripted chains demonstrated end-to-end in the vertical slice that *feel like stories*, and an auto-story generator that produces a genuinely affecting retelling (not a log dump) from real run data.
- **Note:** The structure for emergence is sound and — rarer — the design also has the **capture/payoff** the lens demands: the auto-generated retrospective story (proposal §8) is exactly the "ending record" (who you saved, what you burned, how rescue came or didn't), a cheap, high-ROI, ideal LLM use that *captures* the emergent narrative instead of letting it evaporate. Three adversarial caveats keep it YELLOW. (a) Emergence needs **interacting depth**, but the cheap-object inversion (proposal §2) means most objects ride thin generic physics, so the common chains may be shallow ("cut → strip → tie") rather than surprising — the richest emergence lives in the *rare* deep objects. (b) The auto-story is LLM prose over a log; a flat "you cut a seatbelt, then you cut a cover, then you died" dump is not a story, and its faithfulness/quality is unproven. (c) The best emergent stories (sacrifice, betrayal, the relay rescue) need co-op interdependence, which GD16 flagged as thin. The bet's payoff lives here and the bones are good; execution is the risk.

### GD25 Resolution-Not-Success *(text-world core)*
- **Verdict:** YELLOW
- **Evidence:** §3.5 / §28 "make every attempt resolve"; the one canonical example (§3.5/§31 shirt windbreak: "flaps too wildly… if you stretched it between branches or luggage it might work"); §42 Pass 10 / §46 "50+ brainstormed attempts per object" (authoring-time); proposal §3.4 generic-physics + informative-redirect computed from state; proposal §5 fuzz sample "all *resolve*."
- **Severity:** high
- **What would change the verdict:** a vertical-slice demonstration that *derived + narrated* resolutions match the §3.5 example's specificity across a fuzz sample, **judged by humans** (not merely "no 'You can't do that' fired").
- **Note:** This is the game's *voice* — the §3.5 windbreak response is the single best line in the whole design and the reason Whiteout is special. The lens's sharp demand is generating informative failure **at scale without hand-authoring each case**, and the original design gets the *timing* wrong: §28/§42-Pass-10/§46 make it an *authoring* task (brainstorm 50+ attempts per object across hundreds of objects — unaffordable). The proposal's central fix moves it to **runtime**: resolution is *derived* from material/operation state and redirected informatively (proposal §3.4), so the windbreak logic generalizes to any held lightweight fabric vs wind — the correct, scalable mechanism. The unsolved bet is that **derived ≠ specific**. A material-vector resolver naturally emits "the shirt is too light and flexible to block wind effectively" — correct, it *resolves*, but **dry**; the magic of "*it flaps too wildly… stretch it between branches*" is **physical, witty specificity**, and that lives in the narrate-LLM (fact-locked but stylistically free). Whether the LLM reliably re-specifies "low rigidity + wind = ineffective" into §3.5-grade prose, consistently, across a fuzz space, at acceptable latency/cost, is unproven — and "resolves" (verifiable by fuzz, proposal §5) is **not** "resolves interestingly" (not verifiable by fuzz). If the voice degrades to dry-but-valid, the design satisfies its invariant and loses its identity. The gap between "no flat refusal fired" and "the §3.5 magic landed" is the whole game.

---

## Top findings

**1. GD22 — "Do-Anything" Expectation Management (YELLOW, high / existential-adjacent).** The
loudest promise in the design (§3.5 "everything should resolve; *You can't do that* is a defect")
meets a ~20-operation ceiling. The proposal's redirect + wall-sensor + resolve-then-crystallize is
the best available defense and pulls this off a RED wall, but four seams survive: the redirect
*tells* the player the boundary's shape over a session, **new primitives can't be minted** (crystallize
is confined to existing operations — proposal §3.6), the validator passes **valid-but-dull** mush as
canonical, and crystallize latency makes the wall fire on the very creative attempt it's meant to
catch. "Everything resolves *meaningfully*" is still overstated.

**2. GD25 — Resolution-Not-Success (YELLOW, high).** The §3.5 windbreak line *is* the game's voice,
and the proposal correctly moves informative-failure generation from unaffordable authoring (§28/§46)
to runtime-derived physics. But **derived resolutions are dry by default**; the wit/specificity that
makes the voice special is LLM-narration-dependent and unproven at scale, and a fuzz harness can verify
"resolves" but not "resolves *interestingly*." If the voice flattens, the design keeps its invariant and
loses its identity. (Tightly coupled to **GD2 The Toy**, also YELLOW/high — the same dryness risk
decides whether poking the cabin is delightful in the first 2 minutes.)

**3. GD7 — Meaningful Choices (YELLOW, med-high).** Two latent dominant strategies threaten to collapse
the choice space: the weather arc (§8) makes **stay-and-signal strictly dominate the travel routes**
(§7), and **additive rescue confidence** (§39) with no rivalry over a shared scarce resource turns
"pick your rescue path" into "do all of them" — a checklist, not a decision. The good §38.3
beacon-vs-antenna sacrifice shows the design *can* build real tradeoffs; it just hasn't made the rescue
methods compete.

**Single biggest fun-vs-tedium risk (GD4 ✕ GD18).** The moment-to-moment loop — multi-tick repeated
actions (§9.4 18-minute saw), five worker meters to babysit (§9.5), and the deliberately flat
"survive-the-night" valley (GD10) — is where **depth masquerades as fun**. The proposal's event-driven
clock and action-chunking convert the worst RED (the §9.3 wall-clock heartbeat) into something workable,
but the residual is unproven: chunking a repair chain in a *text* game while preserving felt desperation,
and keeping an event-driven clock's pressure *felt* without wall-clock waiting, are both open. Whether
the second seatbelt-saw is tension or tedium is the question that decides if Whiteout is *fun*, not just
deep — and nothing in the design yet proves it is.
