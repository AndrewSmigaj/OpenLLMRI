> **ARCHIVED — original AI seed.** This is the first AI-written design and is kept for provenance.
> The **authoritative design is now `GDD.md`** in this folder, which supersedes this document (it
> inverts the authoring model, replaces the real-time clock, commits to instanced runs, makes
> conservation a runtime ledger, and cuts the §46 density numbers — see `GDD.md` §0 Changelog). The
> review that produced the GDD is in `../../investigation/`. Section numbers here (§N) are preserved
> as anchors; `GDD.md` Appendix A maps them.

# WHITEOUT

## Systemic Multiplayer Survival Puzzle MUD Design Document

## 1. One-Sentence Pitch

**Whiteout** is a multiplayer systemic survival puzzle MUD where survivors of a snowy plane crash improvise with every object around them to survive cold, injury, hunger, weather, disorientation and uncertainty until rescue, escape or collapse.

## 2. High Concept

Whiteout is a text-forward multiplayer survival adventure inspired by MUDs, MOOs and classic point-and-click adventure games.

The player is not solving one fixed chain of “use object on object” puzzles. The player is surviving inside a dense causal world. A plane seat is not a single noun. It is fabric, foam, webbing, buckles, bolts, aluminum, plastic, stitching, dirt, frost, blood, heat, weight, attachments and possible uses. The player can inspect it, cut it, tear it, pry it, burn it, salvage it, tie it, wrap it, wear it badly, use it medically, use it structurally, ruin it, contaminate it, lose it, give it away or turn it into new objects.

The central promise is:

> The player survives by understanding the world, not by guessing the author’s intended verb-object pair.

This is one authored scenario, not a procedural scenario generator. The crash layout, radio damage, pilot state, weather arc, beacon state and rescue possibilities are authored. LLMs help interpret and expand interactions, but the scenario itself is deliberately designed.

The first scenario should be small in geography but extremely deep in interaction. A single crash cabin, one dying pilot, one fire, one seat, one battery, one beacon, one radio and one worsening storm should already feel like a living world.

## 3. Binding Design Decisions

### 3.1 One Authored Scenario

Whiteout begins with one authored crash scenario.

There are no difficulty settings, no randomized radio damage, no procedural scene variants and no alternate “easy/normal/hard” versions. Replayability comes from player choices, multiplayer coordination, timing, survival tradeoffs, object interactions and multiple rescue routes.

### 3.2 Multiplayer First

Whiteout is a MUD-style shared world. Multiple human players act at the same time. The game must never assume that a single player owns the clock, the room, the puzzle chain or the camera.

Long actions do not jump the world clock forward. They become scheduled activities that progress on ticks.

### 3.3 No Autonomous NPCs

There are no autonomous NPC companions, no AI party members, no NPC planning, no NPC morale simulation and no NPC task assignment system.

The scenario may contain:

```text
human players
the dying pilot
dead bodies
unconscious people
trapped or injured noninteractive passengers
environmental events
scripted fragments
physical objects
```

Only human players make strategic decisions.

The dying pilot is not an AI conversation character. He is a scripted, deteriorating information source and then a body.

### 3.4 The World Is The Puzzle

There should not be a single “tree-cutting puzzle.” There should be trees, slopes, axes, knives, snow, rope, time, fatigue, cold hands, falling hazards, noise, visibility and several reasons a fallen tree might matter.

Sometimes cutting a tree becomes the solution because the world supports it.

### 3.5 Everything Physical Should Be Tryable

Players should be able to attempt sensible, desperate, silly, wasteful and non-survival actions.

Examples:

```text
hold up a shirt to block wind from a flame
wear the seat cover like a cape
lick the frozen latch
throw a suitcase into the ravine
write a message in the snow
make a snowman
stack food trays into a tower
sing to calm people down
kick the radio
sleep under luggage
wave a shirt at the sky
burn the wrong thing
drink unsafe water
run away alone
try to carry the pilot
eat the dead
```

Not everything needs to work. Everything should resolve.

Bad response:

```text
You can't do that.
```

Good response:

```text
You hold the shirt in front of the flame. It blocks the wind for a few seconds, but the cloth flaps too wildly to protect the tinder. If you stretched it between branches or luggage, it might work as a windbreak.
```

## 4. Thoroughness Policy: Deep Model, Short Mandatory Chains

This document must not be interpreted as a guide to make shallow puzzles.

Whiteout should be **model-deep** and **requirement-light**.

Model-deep means:

```text
objects have parts
parts have materials
materials have properties
actions have physical effects
outputs become real objects
failed attempts explain why they failed
silly attempts resolve through the same world model
long-chain improvisations are supported
```

Requirement-light means:

```text
major goals should not require every possible subsystem to be repaired
players should not be forced through 20 mandatory steps for one objective
one authored problem can have many optional improvements and alternate methods
minimum success can be compact while the interaction space remains broad
```

Example:

```text
The radio’s authored blockers are power, antenna and useful location information.
That does not mean the radio is shallow.
It means players do not have to repair the microphone, speaker, knob, fuse, board and every wire before having fun.
Those parts still exist, can be inspected, damaged, tested, described, misused or incorporated into alternate solutions.
```

The correct design discipline is:

```text
model everything plausible
require only the core authored blockers
reward deeper work with better quality, safer outcomes, more rescue confidence or fewer costs
```

## 5. Boundary Of “Do Anything”

Whiteout should not literally simulate every possible human action. It should support every survival-relevant or physically legible action that can be expressed through these operation categories:

```text
move matter
separate matter
join matter
change temperature
change wetness
change shape
change containment
change location
change contamination
change ownership
change knowledge
change injury state
change signal visibility
change search/rescue confidence
change morale
change attention
change noise
change visibility
change audibility
```

This creates the feeling of an ontologically dense text world without requiring infinite bespoke scripting.

## 6. Scenario Premise

A small passenger plane crashes in a remote fictional mountain wilderness. The flight deviated from its planned route, so searchers do not know the exact crash location.

Starting state:

```yaml
time: day_1_11_30_am
season: midwinter
temperature_c: -8
weather: light_snow_starting
visibility_m: 250
daylight_remaining_hours: 5
survivors_initial: human_players_plus_pilot_and_bodies
radio_status: no_power_and_broken_exterior_antenna
beacon_status: weak_or_intermittent
wreck_status: unstable
search_status: active_but_wrong_area
```

The scenario starts before the full whiteout. This gives players a short window to see landmarks, gather supplies, orient themselves, question the pilot and make early decisions before conditions degrade.

## 7. Major Survival And Rescue Paths

The game must support multiple ways of being rescued or surviving long enough for rescue. No single path should be the “real” solution.

Major rescue and survival paths:

```text
stay near the crash and survive until searchers arrive
repair or improve the beacon
repair and operate the radio
create visible signals from the crash site
use smoke, firelight, mirror flashes, bright fabric or SOS markings
combine radio contact with landmark information
combine weak beacon with visible ground signal
travel to a better signal or visibility location
reach the weather relay
reach the logging road or abandoned camp
follow the river or terrain clue toward civilization
survive long enough for weather to clear and search aircraft to spot the wreck
```

These paths can overlap. A weak radio call plus a smoky fire plus an improved beacon may be enough. A good beacon but no shelter may still fail if everyone freezes. A strong visible signal may matter only during a weather window. A group that leaves the crash site may find better terrain or doom itself by leaving the search area.

The rescue system should reward layered efforts:

```text
beacon narrows the search
radio provides human communication
landmarks help searchers locate the crash
smoke and visual signals help aircraft spot the group
staying alive preserves the chance of rescue
moving intelligently can create new routes
moving blindly can make rescue harder
```

## 8. Weather Progression

The storm escalates over the first day.

```yaml
day_1_11_30:
  weather: light_snow
  visibility_m: 250
  wind: low
  effects:
    - landmarks_visible
    - tracks_clear
    - outdoor_movement_possible

day_1_13_00:
  weather: steady_snow
  visibility_m: 120
  wind: rising
  effects:
    - tracks_begin_softening
    - exposed_players_cool_faster
    - search_visibility_worse

day_1_15_00:
  weather: heavy_snow
  visibility_m: 50
  wind: moderate
  effects:
    - landmarks_harder_to_use
    - fire_harder_to_start
    - SOS_marks_begin_filling
    - distant_people_seen_as_shapes

day_1_17_00:
  weather: near_whiteout
  visibility_m: 15_to_30
  wind: strong
  effects:
    - travel_dangerous
    - tracks_vanish_quickly
    - poor_signal_visibility
    - shelter_urgent
    - camp_can_disappear_from_view_at_short_range

night_1:
  weather: whiteout_or_intermittent_gusts
  temperature_c: -15_to_-20
  effects:
    - severe_cold_risk
    - fire_and_shelter_critical
    - sounds_carry_strangely
    - navigation_dangerous
```

Weather modifies visibility, audibility, fire difficulty, snow accumulation, track persistence, shelter urgency, rescue chance and whether players can see each other at range.

## 9. Multiplayer Time And Activity Ticks

### 9.1 Core Rule

Long actions never jump the global clock.

Bad:

```text
Player A builds shelter.
Four hours instantly pass.
Player B loses daylight while reading room text.
```

Correct:

```text
Player A starts building shelter.
The task enters the activity scheduler.
Player A becomes busy.
Player B continues acting.
The global clock advances in small ticks while timed activities progress.
```

### 9.2 World Clock

```yaml
world_time:
  day: 1
  hour: 12
  minute: 14
  light_level: overcast_day
  temperature_c: -9
  weather: steady_snow
```

### 9.3 Tick Model

Recommended default:

```yaml
tick:
  real_seconds: 10_to_20
  game_minutes: 1
  applies_when: live_action_mode
```

Each tick updates:

```text
character activity progress
stamina
cold exposure
injury state
fire state
smoke state
weather
task interruptions
noise events
track aging
snow accumulation
rescue search state
visibility and audibility
```

### 9.4 Activity Messages

Doing things should feel like MUD combat or MUD crafting. Players receive tick messages while working.

Actor view:

```text
You saw at the frozen webbing. A few more nylon fibers part.

Progress: 7 / 18 minutes.
Stamina: 82%.
Hands: occupied.
Cold hands penalty: mild.
```

Nearby observer view:

```text
Mara saws at the frozen seatbelt with a pocketknife.
```

Distant visible view:

```text
Someone near the rear seats is working at something.
```

Audible-only view:

```text
You hear faint scraping from somewhere inside the wreck.
```

Out of sight and out of hearing:

```text
No message.
```

### 9.5 Stamina And Breaks

Characters have stamina, fatigue and body-condition modifiers.

```yaml
worker_state:
  stamina: 0.82
  fatigue: 0.18
  hand_warmth: 0.65
  pain: 0.10
  hunger_modifier: 0.95
  hydration_modifier: 0.90
```

Low stamina should slow progress, increase mistakes and suggest breaks. It should not always hard-block action.

Possible player responses:

```text
continue
pause
rest
switch tasks
call for help
change tool
change method
warm hands
eat
drink
ask another player to take over
```

### 9.6 Clock Modes

**Planning Mode**

Used when no meaningful timed activity is running.

```text
examining is free
reading is free
planning is free
talking is free
global clock does not advance
```

**Live Action Mode**

Starts when any player begins a timed activity.

```text
global clock advances in ticks
tasks gain progress each tick
players can interrupt, help, move, inspect, talk or start other actions
```

**Fast-Forward Mode**

Allowed only when all active human players are busy, resting, sleeping, waiting, traveling, unconscious, dead/watching or explicitly opted into fast-forward.

Fast-forward stops automatically when something important happens:

```text
a task completes
a fire changes state
a survivor worsens
weather changes
a scripted event triggers
a rescue signal occurs
a player requests stop
danger appears
```

## 10. Space Model: Scene, Zone, Direction And Perception

Traditional MUD rooms are too chunky. Pure coordinates are too fiddly. Whiteout uses overlapping perceptual spaces.

The core concepts:

```text
scene: broad dramatic space
zone: position inside that scene
perception: what you can see, hear, reach or manipulate from your zone
direction: where perceived things are relative to you
detail: how clearly they are perceived
```

A player has:

```yaml
position:
  scene: crash_basin
  zone: camp_edge
```

When the player types `look`, the game calculates:

```text
things in your zone
things in adjacent visible zones
distant landmarks
people visible at range
sounds audible at range
weather-limited visibility
blocked sightlines
reachable objects
manipulable objects
relative direction of visible things
detail level of visible things
```

Do not collapse these into “room.”

Use separate concepts:

```text
location: where you physically are
visibility: what you can see
audibility: what you can hear
reachability: what you can manipulate
direction: where the perceived thing is relative to you
detail: how clearly it is perceived
```

## 11. Directional Perception Language

Visible people, landmarks, exits and activity should be described using positional language relative to the player’s current zone.

At camp:

```text
The wrecked plane looms beside you, its broken fuselage half-buried in snow. Andrew kneels near the wing panel, trying to coax a fire from a nest of shavings.
```

One zone north:

```text
To the south, the wrecked plane lies in the snow behind you. Andrew is still near the wing panel, bent over a small smoking fire-start.
```

Farther north:

```text
Farther south, the plane is a broken shape through the falling snow. Someone moves near a dim patch of smoke.
```

Near whiteout range:

```text
To the south, the wreck is almost lost in the snow. You can no longer make out who is there.
```

Out of sight:

```text
The plane is no longer visible through the trees and snow.
```

The rendering rule:

```text
perception = visibility + audibility + distance band + relative direction + detail level + weather distortion + terrain occlusion
```

## 12. Relative Direction Model

Zones should have coordinates or graph-position metadata so the game can compute direction phrases.

```yaml
zone:
  id: forest_fringe
  scene: crash_basin
  position:
    x: 0
    y: 120
    elevation: 8
  terrain_tags:
    - trees
    - snow
    - partial_cover
```

If `camp_core` is at `x: 0, y: 0`, then from `forest_fringe`, camp is south.

Direction phrase options:

```text
north
south
east
west
northeast
northwest
southeast
southwest
upslope
downslope
ahead
behind you
to your left
to your right
toward the wreck
toward the treeline
back toward camp
beyond the wing
past the ravine
near the cockpit
inside the cabin
outside the fuselage
```

Compass language is useful for clarity, but landmark-relative language is often more natural. In whiteout or confusion, the game may prefer “back toward camp” over exact compass directions if the character no longer confidently knows north.

## 13. Overlapping Perceptual Zones

Zones behave like overlapping rooms.

Near camp:

```text
You stand at the edge of the crash camp. The wreck lies behind you, half-buried in snow. Several players are working near the fire. Ahead, the treeline thickens into dark spruce.
```

A little farther out:

```text
You are among the first trees. The camp is still visible behind you as movement and firelight through the falling snow. Spruce trunks crowd the slope ahead.
```

Farther still:

```text
You are in the snowy forest. The crash camp is no longer visible through the trees and blowing snow. The world is reduced to trunks, wind and your own footprints.
```

Typing `look` always reflects actual perception. If camp falls out of sight, it no longer appears in the main description.

## 14. Perception Bands

Objects, people, sounds and activity messages are routed by perception band.

```yaml
perception_band:
  same_zone: detailed
  adjacent_zone: clear
  near_visible: summarized
  distant_visible: vague
  barely_visible: shape_or_motion
  audible_only: sound
  out_of_sight: none
```

Example activity routing:

```yaml
activity: feeding_fire
actor: mara
location: camp_core
```

Same zone:

```text
Mara kneels by the fire, feeding thin shavings into the flame.
```

Near visible:

```text
To the south, Mara is crouched near the fire.
```

Distant visible:

```text
Farther south, someone near the fire is moving around.
```

Barely visible:

```text
A shape shifts near the plane, then vanishes in blowing snow.
```

Audible only:

```text
A faint voice carries through the trees, then vanishes in the wind.
```

Out of perception:

```text
No message.
```

Quiet actions route less far than loud actions. A player hiding food may only be noticed by someone nearby, watching or searching. Chopping, shouting, metal impacts, explosions, fire flare-ups and fuselage shifts route much farther.

## 15. Speech, Shouting And Sound

Speaking is not global. Voice commands should have distinct ranges.

Supported commands:

```text
say "..."
call "..."
shout "..."
whisper to Andrew "..."
yell toward camp "..."
listen south
look south
watch camp
wave toward camp
signal south with flashlight
```

Baseline voice ranges in clear conditions:

```yaml
voice_ranges_clear:
  whisper:
    detailed: same_zone
    faint: very_near

  say:
    detailed: same_zone
    clear: adjacent_zone
    muffled: nearby

  call:
    clear: nearby
    muffled: mid_distance

  shout:
    clear: mid_distance
    muffled: far
    faint: very_far
```

Weather and terrain modifiers:

```yaml
voice_modifiers:
  light_snow: normal
  steady_snow: range_minus_1_band
  heavy_snow: range_minus_2_bands
  whiteout: range_minus_3_bands
  strong_wind_toward_listener: range_plus_1_band
  strong_wind_away_from_listener: range_minus_1_or_2_bands
  strong_crosswind: words_distorted
  inside_fuselage: muffled_by_walls
  forest: blocked_and_scattered
  ravine: echoes_and_distortion
```

Examples:

Same zone:

```text
Andrew says, "I need more dry shavings."
```

One zone north:

```text
To the south, Andrew says, "I need more dry shavings."
```

Farther north:

```text
A voice calls from the south, but the words blur in the wind.
```

Shout from camp:

```text
From the south, Andrew shouts, "Bring the webbing!"
```

Whiteout version:

```text
A shout comes from somewhere south of you. You cannot make out the words.
```

A normal `say` should reach the same zone and possibly adjacent zones. A `shout` travels farther but costs stamina, may attract attention and may still fail in wind.

## 16. Starting Layout

Players begin buckled into different seats inside the same shared scene.

```yaml
starting_scene: wreck_cabin

players:
  player_1:
    zone: middle_left_seat_row
    state:
      buckled_in: true
      disoriented: true

  player_2:
    zone: rear_right_seat_row
    state:
      buckled_in: true
      bruised: true

  player_3:
    zone: front_left_seat_row
    state:
      buckled_in: true
      near_pilot: true

  player_4:
    zone: rear_aisle_floor
    state:
      not_buckled: true
      prone: true
```

Everyone is in the wrecked cabin scene, but their immediate affordances differ. The rear player has the lavatory, rear luggage and rear seats nearby. The front player has the pilot, cockpit threshold and forward bulkhead nearby. The middle player has blocked aisles, food cart debris and collapsed seats.

## 17. Look Commands

### `look` or `l`

Shows scene plus local zone, using relative direction and visible detail.

Rear cabin example:

```text
You are in the rear of the wrecked cabin. Snow blows through a cracked window above the last row of seats. The rear lavatory door hangs half-open behind you. Several overhead bins have burst open, spilling bags into the aisle.

Farther forward, the middle cabin is choked with bent seats and dangling oxygen masks.
```

Forest-edge example:

```text
You stand among the first spruce trees north of the crash camp. Snow gathers on the branches overhead. To the south, the wrecked plane is still visible through the snowfall, and Andrew crouches near a smoking fire pit. Farther north, the forest thickens into darker snow-shadow.
```

### `look around`

Shows immediate vicinity.

```text
Nearby: rear seats, cracked window, torn backpack, rear overhead bin, lavatory door, loose insulation, Mara buckled into the opposite row.
```

### `scan cabin`

Shows broad scene awareness.

```text
The cabin slopes slightly nose-down. The front section is darker and more crushed. Someone is moving near the cockpit threshold. Snow is beginning to collect in the aisle.
```

### `look south`, `look north`, `look forward`, `look aft`

Shows directional perception.

```text
To the south, the camp is still visible through the trees. The fire is only smoke for now. Andrew is crouched beside it, working with something small in his hands.
```

```text
Toward the front, the middle aisle is blocked by a collapsed seat frame. You might climb over it or crawl underneath.
```

### `examine object`

Works fully only if the object is in vicinity.

Distant object:

```text
You can see the orange case near the front bulkhead, but it is too far away to inspect from here.
```

## 18. Movement And Exits

There are two kinds of movement.

### Zone Transitions

These move the player within a scene.

```text
move forward
move aft
cross aisle
climb over seats
crawl toward cockpit
step into rear aisle
walk north
walk toward the forest
move closer to the fire
back away from camp
```

Zone transitions change perception and reachability, but not necessarily the broad scene.

### Scene Transitions

These move the player into a different scene.

```text
enter lavatory
enter cockpit
crawl outside through window
exit fuselage
go into tail section
enter forest
enter rock shelter
```

A scene transition changes the main room context.

## 19. The Dying Pilot

The pilot is a scripted, deteriorating information source. He does not have AI dialogue.

The pilot can:

```text
mumble
gasp
pass out
wake briefly
respond weakly under specific conditions
die
be searched
be moved
be tended
be ignored
be robbed
be covered
be buried
be burned
be consumed in extreme circumstances
```

Typing `talk to pilot` should usually produce weak, fragmented behavior.

```text
You lean close and speak to the pilot.

His eyelids flutter. He makes a wet sound in his throat, but the words do not come. After a few seconds, his head rolls sideways again.
```

### 19.1 Pilot Condition Track

```yaml
pilot:
  entity_type: scripted_survivor
  autonomous_ai: false
  initial_state:
    consciousness: fading
    airway: poor
    bleeding: severe_internal
    pain: extreme
    cold_exposure: rising
    shock: severe
  timers:
    pass_out_window_minutes: 3_to_8
    death_without_tending_minutes: 15_to_35
    death_with_basic_tending_minutes: 35_to_90
  interaction_mode: condition_scripted
```

The pilot should pass out quickly if players simply interrogate him. He is more likely to produce useful fragments if players physically tend to him.

Useful tending actions:

```text
keep him warm
support his head and neck
clear snow from his face
keep him still
hold his hand
talk calmly
reduce wind exposure
move debris off him if possible
cover him
check breathing
```

Tending does not need to save him permanently. It buys clarity, time and information.

### 19.2 Pilot Fragment Triggers

Pilot information is fragmented and conditional.

```yaml
pilot_fragments:
  route_deviation:
    text: '"North... we were north of the route..."'
    conditions:
      - pilot_consciousness_above: 0.25
      - player_is_tending: true
      - fragment_not_already_given: true

  red_ridge:
    text: '"Red ridge... saw it before we dropped..."'
    conditions:
      - pilot_warmed_somewhat: true
      - player_mentions_landmarks_or_location: true

  beacon_location:
    text: '"Beacon... front bulkhead... orange case..."'
    conditions:
      - player_mentions_rescue_or_beacon: true
      - pilot_consciousness_above: 0.20

  radio_hint:
    text: '"Radio... needs power... antenna outside..."'
    conditions:
      - player_mentions_radio_or_cockpit: true
      - pilot_supported_or_pain_reduced: true

  river_hint:
    text: '"River runs out... logging road maybe..."'
    conditions:
      - pilot_near_death: true
      - fragment_not_already_given: true
```

Every pilot fact needs redundant clue paths. The pilot makes things easier. His death must not softlock the scenario.

```yaml
fact: route_deviation_north
clue_paths:
  - pilot_fragment
  - cockpit_nav_log
  - torn_map_mark
  - landmark_alignment
  - radio_rescuer_questioning
```

### 19.3 Pilot Death And Body

When the pilot dies, he becomes a body object.

```yaml
dead_pilot:
  entity_type: body
  former_identity: pilot
  location:
  clothing:
  inventory:
  injuries:
  temperature:
  wetness:
  contamination:
  mass:
  social_weight: high
  edible_in_extreme_emergency: true
```

Possible body interactions:

```text
search body
take clothing
take keys or tools
move body
drag body
cover body
bury body
burn body
leave body
use body as weight
use body as grim windbreak
butcher body
cook meat
eat meat
hide evidence
mark grave
```

Cannibalism is mechanically possible because the world is physically permissive. It should be slow, grim, consequential and recorded in the ending. It is not a normal crafting path.

## 20. Object Model

Every object is a structured entity.

```yaml
object_template:
  id:
  display_name:
  aliases:
  category:
  description_base:
  mass_kg:
  size:
  location:
  scene:
  zone:
  portable:
  temperature_c:
  wetness:
  dirtiness:
  damage:
  contamination:
  parts:
  materials:
  attachments:
  relationships:
  capabilities:
  default_affordances:
  transformation_rules:
  survival_uses:
  non_survival_uses:
  failure_modes:
  sensory_descriptions:
  perception_rules:
  tests:
```

Objects are not inventory tokens. They are physical structures.

## 21. Materials

Materials drive possibility.

```yaml
material_template:
  id:
  display_name:
  density:
  rigidity:
  flexibility:
  cut_resistance:
  tear_resistance:
  bend_resistance:
  burnability:
  ignition_difficulty:
  smoke_toxicity:
  insulation_value:
  waterproofness:
  absorbency:
  edible:
  potable:
  contamination_risk:
  conducts_heat:
  conducts_electricity:
  cold_behavior:
  heat_behavior:
  wet_behavior:
  common_transformations:
```

First-scenario material library:

```text
snow
ice
water
blood
skin
meat
bone
fat
wool
cotton
synthetic_fabric
nylon_webbing
foam
leather
rubber
plastic
glass
aluminum
steel
copper
wire_insulation
paper
cardboard
dry_wood
green_wood
bark
aviation_fuel
charcoal
ash
electronics_board
battery_material
```

## 22. Parts And Attachments

Objects decompose through parts and attachments.

Example aircraft seat:

```yaml
aircraft_seat:
  parts:
    seat_cover:
      material: synthetic_fabric
      attached_by: stitching
      removable_by: [cut, tear, unstitch]
    cushion:
      material: polyurethane_foam
      attached_by: clips_and_friction
      removable_by: [pull, pry, cut_cover]
    seatbelt:
      material: nylon_webbing
      attached_by: bolted_anchor
      removable_by: [cut, unbolt, pry_anchor]
    buckle:
      material: steel
      attached_by: webbing_loop
      removable_by: [cut_webbing, unthread]
    frame:
      material: aluminum
      attached_by: bolts_and_bent_floor_rail
      removable_by: [unbolt, pry, saw, break_with_force]
    tray_table:
      material: plastic
      attached_by: hinge
      removable_by: [unscrew, snap, pry]
    bolts:
      material: steel
      attached_by: threaded
      removable_by: [wrench, pliers, improvised_tool]
```

Every attachment has:

```yaml
attachment:
  method:
  strength:
  accessible:
  required_tool_quality:
  duration:
  failure_modes:
  resulting_state:
```

## 23. Result Objects

Every produced object becomes a first-class world object.

Bad:

```text
You get cloth.
```

Good:

```yaml
seat_cover_loose:
  source: aircraft_seat_01
  material: synthetic_fabric
  size: 80_cm_by_90_cm
  condition: ragged
  wetness: frosty
  contamination:
    smoke_smell: 0.1
    fuel_residue: 0.0
  capabilities:
    - wrap
    - cover
    - cut_into_strips
    - dry
    - burn
    - signal
    - filter_large_debris
    - insulate_poor
    - patch_clothing
    - wear_badly
    - wave
    - decorate
```

If cut again:

```yaml
fabric_strips:
  count: 5
  material: synthetic_fabric
  length_each_cm: 60_to_80
  capabilities:
    - tie
    - bind
    - lash
    - bandage_substitute
    - mark_trail
    - tinder_when_dry
    - make_flag
    - make_crude_mask
```

Those strips can then interact with splints, branches, wounds, sleds, shelters, luggage, bodies, trail markers and tools.

## 24. Conservation Rules

Transformations preserve:

```text
material
approximate mass
temperature
wetness
contamination
damage
ownership
provenance
```

If a fuel-contaminated panel becomes a water tray, the water can become unsafe. If bloody cloth becomes a bandage, blood remains relevant. If a strap is cut, the pieces add up to the original length.

## 25. Core Action Model

The old adventure model is:

```text
use object A on object B
```

Whiteout uses:

```text
actor + action + target + tool + method + desired_result + time_budget
```

Example:

```text
carefully cut the frozen seatbelt with the pocketknife so we can use it as lashing
```

Parsed:

```yaml
action_attempt:
  actor: player
  action: cut
  target: seatbelt_03
  tool: pocketknife_01
  method: saw_slowly
  manner: carefully
  desired_result: nylon_webbing_length
  time_budget_minutes: 20
```

Resolution:

```text
parse intent
resolve references
check vicinity, reachability and perception
collect rules from action, actor, target, tool, parts, materials, location and weather
check physical requirements
predict effects
validate state changes
schedule or complete action
emit events
route tick messages by perception
commit effects
narrate from actual state
update affordances
```

## 26. Action Resolution Priority

Resolve actions in this order:

```text
authored puzzle rule
object-specific rule
part-specific rule
material rule
generic physics rule
LLM interpretation into existing action
plausible failure with explanation
```

## 27. Action Families

Core action families:

```text
examine
search
take
drop
move
carry
drag
push
pull
throw
kick
open
close
sit
lie_down
wear
wave
write
draw
stack
lick
taste
smell
listen
shout
call
say
whisper
sing
pray
joke
insult
apologize
cut
saw
tear
scrape
carve
puncture
pry
wedge
bend
break
attach
detach
tie
untie
wrap
cover
uncover
stuff
brace
support
burn
ignite
extinguish
heat
cool
melt
freeze
boil
dry
soak
pour
fill
empty
mix
clean
contaminate
eat
drink
cook
preserve
repair
test
operate
dismantle
assemble
climb
cross
dig
bury
track
navigate
signal
talk
comfort
threaten
trade
wait
rest
sleep
```

Every action family has:

```yaml
action_family:
  id:
  synonyms:
  required_roles:
  optional_roles:
  physical_checks:
  knowledge_checks:
  skill_modifiers:
  tool_quality_model:
  duration_model:
  progress_model:
  interruption_model:
  stamina_model:
  perception_routing:
  state_effects:
  emitted_events:
  created_objects:
  partial_success_states:
  failure_modes:
  player_feedback:
  silly_or_non_survival_handling:
  tests:
```

## 28. Scenario Brainstorming Requirement

Before implementing a location, object or workflow, generate what players might try.

For each major object, location and survival goal, brainstorm attempts in these categories:

```text
obvious useful actions
expert survival actions
wrong but plausible actions
desperate actions
silly actions
harmful actions
social actions
cooperative actions
antagonistic actions
long-chain actions
irreversible actions
body-related actions
wasteful actions
actions that create noise
actions that create smoke
actions that consume time
actions that reveal clues
actions that change visibility
actions that change audibility
```

Then classify every attempt as:

```text
supported by existing action family
needs object-specific rule
needs material-specific rule
needs special authored rule
should fail informatively
should become a test case
```

The goal is not to make every attempt succeed. The goal is to make every attempt resolve.

## 29. Immediate First-Minute Attempts

Players may immediately try to:

```text
look around
call for survivors
search themselves
check inventory
free themselves from a seatbelt
wake another player
run outside
search luggage
grab food
grab alcohol
grab tools
find a lighter
find the pilot
question the pilot
comfort the pilot
tend the pilot
loot the pilot
try to carry the pilot
start a fire inside
start a fire outside
use clothing as warmth
use clothing as wind protection
open the cockpit
kick open a jammed door
break a window
crawl through wreckage
follow footprints
mark the crash site
write SOS in snow
ignore everyone and leave
pray
panic
make jokes
throw things
try to eat snow
lick metal
hide supplies
sabotage supplies
```

Each should have a defined response path.

## 30. Workflow Design

Important goals are workflows, not recipes.

```yaml
workflow:
  goal:
  success_conditions:
  failure_conditions:
  required_knowledge:
  required_resources:
  optional_resources:
  stages:
  alternate_paths:
  partial_success_states:
  consequences:
  clue_paths:
  silly_attempts:
  desperate_attempts:
  tests:
```

Critical workflows:

```text
escape seat restraint
question or tend the dying pilot
survive first night
make sustained fire
make safe water
treat bleeding
treat hypothermia
salvage aircraft seat
repair beacon
repair radio
create visible signal
build usable shelter
navigate to nearby landmark
handle death and bodies
```

## 31. Fire System

Fire is a workflow.

A sustained fire requires:

```text
ignition source
tinder
kindling
fuel
oxygen
wind protection
dry-enough conditions
maintenance
```

Fire states:

```text
no_fire
spark
ember
small_flame
kindling_fire
sustained_fire
coal_bed
dying_fire
ash
```

Possible ignition methods:

```text
matches, rare and possibly wet
lighter, possibly empty but still sparking
flare, easy but one-use and dangerous indoors
battery and conductive material
focused sunlight through lens
existing ember transfer
hot metal shortly after crash, limited window
fuel-assisted ignition, powerful and dangerous
friction fire, possible but hard in cold/wet conditions
```

Fire hazards:

```text
toxic smoke from foam or plastic
carbon monoxide in enclosed fuselage
burn injury
fuel flare
spreading fire
loss of useful materials
attracting attention
melting structural snow
revealing position
draining limited fuel
```

Improvised wind blocking should support many objects:

```text
shirt
seat cover
luggage
body
aircraft panel
snow wall
tree trunk
blanket
plastic tray
dead body
living person standing nearby
```

A shirt held by hand should usually be poor but informative:

```text
You hold the shirt between the flame and the wind. It helps for a few seconds, then snaps sideways and nearly smothers the tinder. It needs a frame or weight to work as a windbreak.
```

A shirt stretched between branches or weighted with luggage can become a crude windbreak.

## 32. Warmth System

Warmth can come from more than fire.

Sources of warmth and heat retention:

```text
fire
windbreak
shelter
dry clothing
layering
insulation from ground
huddling
heated stones
hot water containers
moving out of wind
closing fuselage gaps
snow trench
snow wall
reduced sweating and exertion
sharing body heat
```

Warmth calculations should account for:

```text
ambient temperature
wind exposure
wet clothing
clothing insulation
shelter insulation
ground contact
fatigue
calorie deficit
fire distance
body condition
```

## 33. Water System

Water sources:

```text
snow
ice
creek water
stored drinks
canned food liquid
condensation
unsafe aircraft fluids
```

Water actions:

```text
gather
melt
boil
filter
store
spill
freeze
contaminate
clean container
```

Containers matter:

```text
bottle
canteen
pot
food can
plastic bag
glove
helmet
folded aircraft panel
improvised bark or fabric carrier
```

Melted snow is not automatically safe if the container is dirty, fuel-contaminated, bloody or made of toxic material.

## 34. Shelter System

Shelters are evaluated by properties, not recipes.

```yaml
shelter:
  wind_blocking: 0.70
  insulation: 0.45
  waterproofing: 0.30
  structural_stability: 0.60
  fire_safety: 0.40
  capacity: 4
  smoke_ventilation: 0.20
```

Possible shelters:

```text
stabilized fuselage
snow trench
snow wall
snow cave
lean-to
rock overhang
aircraft panels
parachute or tarp
luggage wall
logs and branches
seats and cushions
```

Partial shelters matter. A half-built windbreak can reduce heat loss before becoming a full shelter.

## 35. Injury And Medicine

Injuries include:

```text
bleeding
broken limb
concussion
burns
frostbite
hypothermia
infection
shock
dehydration
smoke inhalation
exhaustion
```

Medical actions are systemic.

Examples:

```text
cloth can become a bandage
seatbelt webbing can become a tourniquet or splint tie
branches, aluminum frames or poles can become splints
alcohol wipes can disinfect
boiling water or flame can clean some metal tools
snow can reduce swelling but worsen cold exposure
painkillers improve function but can mask danger
moving an injured person can save them from cold but worsen injuries
```

## 36. Food, Death And Bodies

Food categories:

```text
passenger snacks
airline meals
canned food
animals
fish
scarce winter plant material
human remains, emergency option
```

Bodies are physical objects with identity and social weight.

```yaml
body:
  identity:
  clothing:
  inventory:
  mass:
  temperature:
  wetness:
  injuries:
  contamination:
  relationship_significance:
  morale_impact:
  edible_in_extreme_emergency:
```

Possible body interactions:

```text
search
move
carry
drag
cover
bury
burn
leave
protect_from_animals
use_clothing
recover_inventory
identify
mourn
hide
use_as_grim_windbreak
use_as_emergency_food
```

Cannibalism is mechanically possible but slow, grim and consequential. It requires time, tools, preparation, cooking or freezing for safety, and it affects the ending.

## 37. Beacon Workflow

The beacon is one rescue path, not the only rescue path.

Purpose:

```text
The beacon improves search confidence and starts or strengthens rescue progress.
The group still has to survive, keep it transmitting and make themselves discoverable.
```

Beacon workflow:

```text
find beacon
notice weak or intermittent behavior
access casing
diagnose power, antenna, switch or moisture issue
find or improvise tool
secure connection
warm or insulate battery
improve antenna placement
test signal
protect from snow
survive while rescue search narrows
```

Beacon signal ladder:

```yaml
beacon_signal_quality:
  off: 0
  intermittent_weak: 15
  weak_but_stable: 35
  stable_at_crash_site: 55
  stable_with_clear_antenna: 70
  elevated_on_ridge_or_tree: 85
```

Beacon success does not instantly win. It narrows the search, especially when paired with visual signals, radio contact, smoke, firelight or staying near the wreck.

## 38. Authored Radio Workflow

The radio is part of the single authored crash scene. It is not procedurally generated, and there are no easy, normal or hard variants.

The radio should be deep enough to feel real, but not so deep that players have to repair every subsystem. The authored first-scene radio has two real mechanical blockers plus an information problem.

The authored core radio puzzle is:

```text
The radio has no power.
The outside antenna is broken.
The rescuers need useful location information.
```

That is the core route, not the whole interaction space. The microphone, speaker, frequency knob and internal transceiver are damaged-looking but working enough for gameplay. Players can still inspect them, test them, damage them, misinterpret them, or use them in wrong-but-plausible ways.

### 38.1 Authored First-Scene Radio State

```yaml
cockpit_radio:
  state: damaged_but_salvageable

  active_blockers:
    - no_power
    - broken_or_missing_external_antenna
    - unknown_useful_location_information

  working_enough:
    - transceiver
    - speaker
    - microphone
    - frequency_knob
    - push_to_talk

  degraded_but_not_blocking:
    - static
    - cold_stiff_controls
    - intermittent_signal
    - battery_drain
```

This means the intended radio path is:

```text
find/access the radio
discover it has no power
restore or improvise power
hear static or partial reception
inspect outside of the plane
see the broken antenna
replace, extend or improvise an antenna using something long and metal
attempt contact
hear that the signal is weak
adjust antenna placement or improve the improvised antenna
get partial messages through static
provide enough route or landmark information
increase rescue confidence
survive until rescue can act
```

The player does not also need to repair the microphone, speaker, knob, every fuse, every wire and the internal board.

### 38.2 Broken Antenna Visibility

The broken antenna should be discoverable by inspecting the outside of the plane.

Example:

```text
The top of the fuselage is scraped bare where the antenna should be. A torn metal base juts from the skin, with a short length of cable hanging loose and rimed with ice.
```

This clue should be visible from outside near the fuselage, not from staring at the radio panel forever.

The radio should hint at this too:

```text
The radio lights up and hisses, but the static has a hollow, empty quality. The set seems alive, but deaf.
```

### 38.3 Antenna Solutions

The antenna can be improved with anything plausibly long and metal, especially if elevated or connected to the broken antenna lead.

Possible materials:

```text
aircraft wire
copper cable
aluminum seat frame
metal pole
long strip of fuselage metal
seat frame tubing
metal luggage handle
wire from electronics
beacon antenna, as a costly tradeoff
knife or tool used only as a poor temporary conductor
```

Better antenna traits:

```text
longer
metal
connected to antenna lead
raised outside the fuselage
not buried in snow
not touching too much wreckage
not held by someone freezing their hands for too long
less shielded by terrain
```

Poor antenna traits:

```text
too short
inside the fuselage
buried in snow
poorly connected
touching random metal
held by hand shakily
covered in ice
```

Antenna quality should be computed from material, length, connection, height, placement, snow/ice coverage, surrounding wreckage and weather. This allows long metal objects to work without requiring every object to have a custom radio rule.

### 38.4 Radio Feedback

The person responding over the radio should explicitly indicate signal quality so players can reason about the antenna.

Examples:

```text
"... unidentified aircraft ... signal weak ... repeat ..."

"... hearing you faintly ... improve your antenna if you can ..."

"... too much static ... say again ..."

"... we have partial transmission ... need location ... landmarks ..."

"... your signal is stronger now ... continue ..."
```

This feedback tells players that adjusting the antenna matters. They should be able to try moving it, raising it, lengthening it, connecting it better or clearing snow.

### 38.5 Static And Persistence

If the radio has power but no usable antenna, it should mostly produce static. However, repeated attempts should sometimes get fragments through. The system should not hard-block persistent players forever.

Radio behavior with no antenna or bad antenna:

```yaml
bad_antenna_radio_behavior:
  normal_result: mostly_static
  occasional_result: broken_fragment
  repeated_attempts:
    - small_chance_of_getting_attention
    - high_time_cost
    - battery_drain
    - player_cold_if_outside_adjusting
    - repeated_message_fragments
```

The other side can loop through a few partial messages:

```text
"... unidentified aircraft ... repeat ..."
"... if you can hear ... transmit location ..."
"... search area ... negative contact ..."
"... need landmarks ... ridge, river, road ..."
"... signal weak ... improve antenna ..."
```

This allows stubborn players to make slow progress, while still making antenna repair the better path.

### 38.6 Radio Progress States

```yaml
radio_progress:
  dead:
    description: no lights, no sound
    rescue_effect: none

  powered_static:
    description: the radio lights up and hisses
    rescue_effect: confirms power works

  weak_receive:
    description: broken voices come through static
    rescue_effect: players may learn searchers are looking in the wrong area

  weak_transmit:
    description: rescuers may hear a distress call but not enough to locate the crash
    rescue_effect: search confidence increases slightly

  two_way_contact_no_location:
    description: rescuers answer, but ask where the crash is
    rescue_effect: players need landmarks, route clues or beacon support

  useful_contact:
    description: rescuers have enough information to narrow the search
    rescue_effect: rescue becomes likely when weather allows
```

### 38.7 Radio Is Not Instant Rescue

Even useful contact does not immediately end the scenario.

After useful contact, players may still need to:

```text
keep the radio powered
repeat contact during a weather window
keep the beacon or visual signal active
stay near the known rescue area
survive cold, injury and nightfall
prepare extraction signals
clear snow from SOS markings
maintain smoke or firelight when searchers are nearby
```

### 38.8 Location Information

The radio can get rescuers’ attention, but players need useful location information.

Location information can come from:

```text
pilot fragment before he dies
cockpit nav log
torn map mark
visible red ridge before whiteout
river direction
landmark alignment
weather relay sign or label
description of basin, wreck orientation or ridge shape
beacon signal combined with partial radio contact
visual signal spotted during a weather break
```

The radio should support imperfect communication. Players do not need exact coordinates. They can provide fragments, and the rescue system aggregates confidence.

## 39. Search And Rescue Simulation

Rescue is simulated, not scripted.

```yaml
search_and_rescue:
  search_area:
  aircraft_schedule:
  weather_limits:
  beacon_confidence:
  radio_confidence:
  visual_signal_confidence:
  last_known_route:
  landmark_confidence:
  ground_team_distance:
```

Player actions alter search:

```text
strong beacon narrows search
weak beacon helps slowly
radio contact gives direct clues
bad radio contact still increases confidence slightly
smoke helps only if visible
SOS helps only if uncovered
radio message helps only if location info is useful
moving away from the wreck can help or doom the group
fire at night may be visible
bright objects on snow may be spotted
poor weather can delay rescue despite good signals
```

Rescue confidence should be additive and partial. Players can be rescued through different combinations.

Example rescue combinations:

```text
stable beacon plus surviving at crash site
weak radio contact plus red ridge description
smoke signal plus aircraft weather break
SOS in snow plus bright fabric plus clear daylight
radio static fragments plus improved antenna plus pilot route clue
beacon signal plus visible fire at night
travel to weather relay and use its equipment
follow river to logging road
reach abandoned camp and signal from there
```

The game should not require one perfect rescue path.

## 40. User Interface

Whiteout supports both natural language and structured MUD commands.

Natural language examples:

```text
cut the seatbelt with the pocketknife
warm the battery near the fire
tie the webbing around the branch and the sled
use the shiny panel to signal the aircraft
hold my shirt up to block the wind from the flame
crawl toward the cockpit
look toward the camp
shout to the people by the fire
walk north
listen south
inspect the outside of the plane for antenna damage
connect the aluminum frame to the antenna lead
raise the wire higher
try the radio again
```

Traditional MUD commands:

```text
look
l
look around
look north
look south
scan cabin
examine seat
inventory
say
call
shout
whisper
give
take
drop
follow
stop
status
tasks
time
weather
map
move forward
move aft
enter lavatory
exit fuselage
```

Examining objects reveals plausible affordances without spoiling everything.

```text
The seatbelt is still bolted to the aircraft seat. The webbing is strong, slightly frayed and stiff with frost.

You could probably:
- cut it with a sharp tool
- unbolt it with the right tool
- pry at the anchor
- use it to restrain, bind, lash or strap something
```

## 41. LLM Role

Good LLM uses:

```text
interpret unusual player phrasing
generate object descriptions from structured state
draft object templates
draft special interactions
generate tests
explain failed actions naturally
summarize complicated situations
brainstorm player attempts
generate wrong-but-plausible and silly action cases
```

Bad LLM uses:

```text
invent state changes directly
decide survival math
grant impossible success
forget object state
contradict deterministic simulation
create puzzle-critical objects without validation
```

The deterministic engine owns state. The LLM proposes interpretations and prose.

## 42. Content Production Workflow

Build the game through passes.

### Pass 1: Multiplayer Tick Engine

Implement:

```text
global clock
planning mode
live action mode
fast-forward mode
character activities
work blocks
progress
tick messages
stamina
breaks
interrupts
cooperation between human players
offline stances
```

Acceptance test:

```text
One player starts a 90-minute shelter task.
Another player can keep acting.
The world clock advances gradually.
The first player receives tick progress.
The first player can interrupt.
The task keeps partial progress.
```

### Pass 2: Scene, Zone, Direction And Perception Engine

Implement:

```text
scene
zone
zone coordinates
relative direction calculation
adjacent zones
scene transitions
zone transitions
visibility bands
audibility bands
reachability
manipulability
directional look descriptions
perception-routed emotes
weather-reduced perception
sound propagation
speech ranges
look commands
```

Acceptance test:

```text
A player walking north from camp toward the forest sees the camp in detail, then to the south with less detail, then vaguely, then only by sound, then not at all.
Activity messages from camp fade according to distance, weather, line of sight and action loudness.
Speaking, calling and shouting travel different distances.
```

### Pass 3: World State And Entity System

Implement:

```text
WorldState
Entity
Part
Material
Attachment
RelationshipGraph
Inventory
Location
EffectSystem
EventSystem
Narrator
```

Acceptance test:

```text
An object can contain parts.
A part can be removed.
The removed part becomes a new object.
Material, temperature, wetness and contamination are preserved.
```

### Pass 4: Action Family Engine

Implement generic actions first:

```text
examine
search
take
move
throw
kick
wear
write
lick
shout
cut
tear
scrape
carve
puncture
pry
bend
break
tie
wrap
attach
detach
heat
cool
melt
dry
soak
ignite
burn
extinguish
fill
pour
repair
test
operate
signal
wait
sleep
```

Acceptance test:

```text
The same cut action can cut fabric, webbing, foam and clothing differently based on material and tool.
```

### Pass 5: First Deep Object

Implement one aircraft seat to extreme depth.

Required interactions:

```text
inspect cover
cut cover
tear cover
wear cover badly
wave cover
use cover as wind screen poorly
stretch cover into windbreak
remove cushion
cut foam
burn foam outside
discover toxic smoke
cut seatbelt
unbolt seatbelt with proper or improvised tool
pry frame loose
bend aluminum frame
remove bolts
use fabric as bandage, wrap, signal, patch or filter
use foam as insulation, padding, poor tinder or toxic fuel
use webbing as lashing, tourniquet, sled strap or splint tie
use frame as splint, lever, shelter rib or antenna support
use frame as crude radio antenna material
```

Acceptance test:

```text
The seat can be physically dismantled through several plausible methods.
All outputs are first-class objects.
All outputs have survival uses, non-survival uses or explicit non-uses.
```

### Pass 6: First-Minute Scenario

Implement the first 30 to 45 minutes deeply.

Required:

```text
players start buckled in different zones
dying pilot
pilot clue fragments
pilot death timer
freeing self or others from restraints
panic and calling out
basic searching
weather beginning as light snow
visible landmarks before whiteout
first scavenging choices
first moral choices
```

Acceptance test:

```text
Players can save time, waste time, help the pilot, ignore the pilot, loot the pilot or question him.
The pilot can die without softlocking the scenario.
```

### Pass 7: Fire, Water, Warmth

Implement:

```text
fire progression
tinder/kindling/fuel distinction
smoke
toxic smoke
wind effects
shirt-as-windbreak attempt
snow melting
water containers
contamination
wetness
drying
body temperature
shelter warmth
huddling
insulation
```

Acceptance test:

```text
The players can survive first night through at least three warmth strategies.
Several bad fire ideas are allowed and fail informatively.
```

### Pass 8: Beacon And Radio

Implement beacon first, then the authored radio.

Beacon acceptance tests:

```text
Beacon repair is not one click.
At least three clue paths identify the fault.
A repaired beacon improves rescue but does not instantly win.
```

Radio acceptance tests:

```text
The radio has no power at first.
Restoring power produces static or partial reception.
The broken antenna can be found by inspecting the outside of the plane.
Anything plausibly long and metal can be tried as antenna material.
Better antenna placement improves signal quality.
The other side gives weak-signal feedback.
Repeated attempts with poor signal can eventually pass fragments, but slowly and unreliably.
Useful radio contact improves rescue confidence but does not instantly win.
```

### Pass 9: Rescue Routes

Implement multiple rescue routes as overlapping confidence paths.

Required rescue methods:

```text
beacon rescue
radio rescue
visual signal rescue
smoke or firelight rescue
weather-window aircraft spotting
travel to better signal point
travel to road, relay or camp
combined partial-signal rescue
```

Acceptance test:

```text
The group can be rescued through at least four distinct combinations of actions.
No single object or single puzzle is required for all rescue endings.
```

### Pass 10: Brainstorm And Fuzzing Pass

For every important object and location, have the LLM generate attempted actions in categories:

```text
useful
wrong
desperate
silly
harmful
social
cooperative
antagonistic
long-chain
```

Then map each attempt to:

```text
existing action family
new special rule
informative failure
test case
```

Acceptance test:

```text
For each major object, at least 50 player attempts are generated, classified and either supported or given specific failure feedback.
```

## 43. Authoring Templates

### 43.1 Object Authoring Packet

```yaml
object_authoring_packet:
  identity:
    id:
    name:
    aliases:
    category:
    description:
    scene:
    zone:
    mass:
    size:

  perception:
    visible_from:
    audible_from:
    reachable_from:
    manipulable_from:
    occlusion_rules:
    direction_rendering:
    distance_detail_templates:
    weather_visibility_modifiers:

  parts:
    - id:
      material:
      attachment:
      removable_by:
      damaged_by:
      outputs_when_removed:

  states:
    temperature:
    wetness:
    damage:
    contamination:
    ownership:
    accessibility:

  affordances:
    examine:
    move:
    cut:
    tear:
    pry:
    break:
    heat:
    cool:
    wet:
    dry:
    burn:
    tie:
    wrap:
    wear:
    throw:
    write_on:
    lick_or_taste:
    use_as_tool:
    use_as_material:

  transformations:
    - action:
      requirements:
      duration:
      tick_feedback:
      outputs:
      partial_outputs:
      failure_modes:

  survival_uses:
    warmth:
    shelter:
    water:
    food:
    medicine:
    fire:
    signaling:
    navigation:
    repair:

  non_survival_uses:
    jokes:
    decoration:
    noise:
    comfort:
    communication:
    wasting_time:

  tests:
    success_cases:
    failure_cases:
    conservation_cases:
    silly_cases:
    perception_cases:
```

### 43.2 Action Family Packet

```yaml
action_family_packet:
  id:
  synonyms:
  required_roles:
  optional_roles:
  physical_checks:
  knowledge_checks:
  skill_modifiers:
  tool_quality:
  duration_model:
  progress_model:
  tick_feedback_model:
  stamina_model:
  perception_routing:
  interruption_model:
  state_effects:
  emitted_events:
  created_objects:
  partial_success:
  failure_modes:
  player_feedback:
  tests:
```

### 43.3 Workflow Packet

```yaml
workflow_packet:
  id:
  goal:
  why_it_matters:
  success_conditions:
  failure_conditions:
  stages:
  required_systems:
  useful_objects:
  alternate_paths:
  partial_success_states:
  clue_paths:
  time_pressure:
  tick_events:
  silly_attempts:
  desperate_attempts:
  consequences:
  validation_tests:
```

## 44. Validation Rules

The content validator should check:

```text
no prose-only state changes
every generated object has material and location
every derived object has capabilities or explicit non-uses
critical goals have at least three solution paths
critical hidden facts have at least three clue paths
critical repairs include inspect/access/diagnose/repair/test stages
long actions never jump global time
every timed action has tick feedback
every timed action can be interrupted or explicitly marked uninterruptible
every important action has failure feedback
conservation rules are followed
survival-critical objects have tests
silly/non-survival interactions exist for major objects
perception routing exists for major activity messages
distant objects cannot be manipulated unless a ranged action supports it
weather changes visibility and audibility
look descriptions use relative direction for visible distant features
speaking, calling and shouting have different propagation rules
radio has one authored damage state, not procedural variants
radio success is not instant rescue
multiple rescue routes are possible
LLM-generated rules cannot override core physics without approval
```

## 45. Testing Strategy

Example tests:

```text
Can cut dry fabric with sharp knife.
Frozen fabric is harder to tear than warm fabric.
Can cut nylon webbing with pocketknife, but slowly.
Cannot cut steel bolt with pocketknife.
Can melt clean snow in clean pot.
Melting snow in fuel-contaminated panel creates unsafe water.
Burning foam creates heat and toxic smoke.
Seatbelt webbing can lash branch splint.
Wet cloth insulates worse than dry cloth.
Large fire inside unventilated fuselage creates smoke hazard.
A 90-minute task does not instantly advance time for other players.
An interrupted shelter remains partially useful.
The pilot can die before giving all clues.
Pilot death does not softlock the scenario.
Holding a shirt by hand gives poor wind protection.
Stretching fabric over a frame can improve wind protection.
Licking frozen metal risks injury.
Wearing a seat cover gives little warmth but affects description.
A player walking north into the forest gradually loses sight of camp to the south.
A player out of sight does not receive visual activity messages from camp.
A loud metallic bang routes farther than quiet pocketing of food.
A normal say reaches nearby players but not distant forest players.
A shout travels farther than say but becomes muffled in heavy snow.
Look south shows the camp if visible and omits it when obscured.
Radio has no power before power is restored.
Radio with power but no antenna produces mostly static.
Broken antenna is discoverable by inspecting the outside of the plane.
Long metal objects can be tried as antenna material.
A better antenna improves signal clarity.
The responder can say the signal is weak.
Repeated radio attempts with bad signal can produce partial fragments.
Useful radio contact increases rescue confidence but does not instantly win.
Beacon plus visual signal can rescue without full radio success.
Radio plus landmark information can rescue without beacon success.
Travel to relay, road or camp can rescue without radio or beacon success.
```

## 46. First Scenario Scope

Initial locations and zones:

```text
wreck cabin
rear cabin
middle cabin
front cabin
cockpit threshold
rear lavatory
cockpit
tail section
wreck exterior
camp core
camp edge
treeline edge
forest fringe
deep forest
shallow ravine
rock shelter
frozen creek
```

Primary objects:

```text
8 aircraft seats
1 cockpit console
1 damaged radio
1 weak beacon
1 cockpit battery
1 cracked window
1 emergency kit
12 luggage pieces
4 overhead bins
2 food carts
1 fuel leak
1 torn insulation panel
1 detached wing panel
1 broken exterior antenna mount
1 dead branch pile
3 small trees
1 dying pilot
several bodies or unconscious noninteractive passengers
```

Target density:

```yaml
first_scenario:
  locations_and_zones: 15_to_25
  primary_objects: 60_to_100
  derived_objects: 300_to_800
  action_families: 40_to_70
  authored_workflows: 12_to_18
  major_survival_goals: 6_to_10
  critical_solution_paths_per_goal: 3_or_more
  rescue_route_combinations: 4_or_more
  brainstormed_attempts_per_major_object: 50_plus
  explicit_tests: 700_plus
```

The player will not discover all content in one run. The density exists so experimentation feels real.

## 47. Minimal Playable Build

The first playable build should allow this complete experience:

```text
Players wake after the crash.
They begin in different seats and zones within the same cabin scene.
Snow is beginning, but visibility is still good enough to see some landmarks.
They inspect their local vicinity.
They free themselves or help others free themselves.
They discover the dying pilot.
They can question, comfort, tend, move, ignore, loot or later consume the pilot.
They salvage at least one aircraft seat into useful parts.
They move through overlapping perceptual zones.
They see camp in detail, then to the south with less detail, then lose sight of camp when walking far enough into forest.
They receive activity messages only when perception supports them.
They can say, call, shout and whisper with different ranges.
They attempt fire through several plausible methods.
They can try bad ideas, such as holding up a shirt to block wind.
They melt or fail to melt snow safely.
They improve warmth through shelter, insulation, huddling or fire.
Long actions show tick progress, stamina and interruptions.
Snow worsens into heavy snow and later whiteout.
Night falls gradually through multiplayer time.
Cold, injury, smoke, fire and visibility update.
At least one person may live or die based on action.
Beacon repair can begin rescue progress but not instantly win.
Radio repair can produce static, partial contact, weak signal feedback and eventual rescue confidence.
Players can pursue rescue by beacon, radio, visual signal, smoke, firelight, weather-window spotting, travel or combinations of partial successes.
```

## 48. Repo Structure

```text
/src
  /engine
    worldState.ts
    entity.ts
    parts.ts
    materials.ts
    relationships.ts
    scene.ts
    zone.ts
    perception.ts
    direction.ts
    soundPropagation.ts
    actionResolver.ts
    activityScheduler.ts
    effectSystem.ts
    eventSystem.ts
    timeSystem.ts
    weatherSystem.ts
    survivalSystem.ts
    knowledgeSystem.ts
    rescueSystem.ts
    narrator.ts

  /actions
    examine.ts
    search.ts
    move.ts
    shout.ts
    say.ts
    listen.ts
    cut.ts
    tear.ts
    scrape.ts
    carve.ts
    puncture.ts
    pry.ts
    break.ts
    bend.ts
    heat.ts
    melt.ts
    burn.ts
    ignite.ts
    tie.ts
    wrap.ts
    attach.ts
    detach.ts
    pour.ts
    fill.ts
    repair.ts
    test.ts
    operate.ts
    signal.ts
    silly.ts
    social.ts

  /content
    /materials
    /objects
    /scenes
    /zones
    /workflows
    /puzzles
    /scenario

  /llm
    intentParser.ts
    contentGenerator.ts
    attemptBrainstormer.ts
    narratorAdapter.ts
    prompts

  /validation
    validators.ts
    conservationChecks.ts
    solvabilityChecks.ts
    coverageChecks.ts
    perceptionChecks.ts
    directionChecks.ts
    soundPropagationChecks.ts
    rescueRouteChecks.ts
    sillyInteractionChecks.ts

  /tests
    actionFamilies.test.ts
    materials.test.ts
    multiplayerTime.test.ts
    perceptionZones.test.ts
    directionalLook.test.ts
    soundPropagation.test.ts
    crashSiteInteractions.test.ts
    fireWaterShelter.test.ts
    pilot.test.ts
    beaconRadio.test.ts
    rescueRoutes.test.ts
    survival.test.ts
```

## 49. Final Binding Principle

Whiteout should not be built as a giant list of magical object pairs.

It should be built as:

```text
one authored crash scenario
multiplayer scheduled time
MUD-like tick progress
stamina and breaks
overlapping perceptual zones
directional descriptions
visibility, audibility and reachability separation
perception-routed activity messages
speech and sound propagation
rich object decomposition
generic action families
material behavior
first-class derived objects
deep workflows with short mandatory chains
partial success states
scripted dying pilot pressure
authored radio damage
weather escalation
multiple rescue paths
LLM-generated long-tail attempts
deterministic validation
clear failure explanations
```

The first milestone is not a giant wilderness. The first milestone is a crash site so dense and reactive that looking from different seats, freeing yourself, questioning one dying pilot, walking north from camp into the forest, seeing the camp fade south behind you, dismantling one aircraft seat, making one fire, improvising one radio antenna, treating one injury and surviving one night already feels like a living world.
