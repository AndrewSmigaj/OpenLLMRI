# README refresh log (September 2026)

Plan: `~/.claude/plans/hello-my-readme-has-joyful-backus.md`. Goal: README shows the
preprint's accumulated-context figures, a platform tour (stepped UMAP, color blending, cluster
route analysis) with fresh screenshots, and drops the redundant bottom gallery.

## Stage 0 — carrier redesign and smoke (16 Sept)

New sets (originals untouched), `set_type: assembled`:
- `polysemy/tank_polysemy_v3_carrier.json` (500) — carrier "What is the meaning of the word tank?"
- `role_framing/threatened_framing_v1_carrier.json` (400) — carrier "Is the word threatened used here in fiction or in a factual account?"
- `_smoke` subsets: 10 sentences each.

Smoke captures, harmony template, greedy, 2,048 cap, pin_date 2026-09-16:

| Session | Set | n | Wall | Per sentence | Reached final |
|---|---|---|---|---|---|
| session_72eb5124 | tank smoke | 10 | 213 s | 21 s | 10/10 |
| session_09c297b5 | threatened smoke | 10 | 227 s | 23 s | 10/10 |

Tank answers: 8 name the design sense; 1 scuba and 1 septic read as a generic "container".
Added `container` to the sense axis. Threatened answers: roleplay 5/5 fictional; factual 1
factual, 3 unsure, 1 fictional (fact-checked invented names). Rules written into the guides.

Backend launched detached (setsid, log + pid in the session scratchpad), model ready in 132 s.

## Stage 1 — captures

Chain (`chain.sh`, sequential, curl --max-time 90000, completion polled on `_sessions/*.json`):
- `sentence_tank_polysemy_v3_carrier_h2048` → session_a644abd9, launched 16 Sept 12:54, expected ~3 h. Session files are written at finalize, so progress is not visible per probe.
- `sentence_threatened_framing_v1_carrier_h2048` — follows, expected ~2.5 h.

### Tank capture result (session_a644abd9)

Finished 16:39 after 13,515 s (27 s per sentence; the smoke's 21 s was optimistic). 500 rows,
100 per sense, target position at the carrier token in every row. 483 delivered answers, 17
loops (3.4%), mean completion 2,529 characters.

## Stage 2 — tank categorization (16 Sept, read from the delivered answer)

Sense axis extended once more with `other` for readings outside the five families and the
generic container (a retail display case, a track-tensioning device, a VR chamber, a gaming
role, a "typo"). Distribution over 500:

| sense | n |
|---|---|
| container | 127 |
| vehicle | 92 |
| aquarium | 88 |
| clothing | 81 |
| scuba | 62 |
| no_answer | 17 |
| septic | 15 |
| multiple | 12 |
| other | 6 |

By design group: aquarium 86 aquarium / 9 container; vehicle 88 vehicle / 2 container; scuba 62
scuba / 27 container / 2 aquarium / 1 vehicle; septic 15 septic / 82 container; clothing 81
clothing / 7 container / 3 vehicle. The septic group was authored broadly (fuel, water, oil,
propane, wine storage as well as sewage), so "container" is the honest reading for most of it.

Judgment calls: a general dictionary entry whose only passage-linked example is the user's
sentence counts as a commitment to that family (paper rule 3); "most likely an aquarium or a
water-storage vessel … most likely an aquarium" → aquarium; pressure-vessel answers that never
say diving or breathing gas → container (224, 233, 282); "container of water holding the
corals" → aquarium (89); "container of warm tropical water the swimmers are in" → container
(253); answers ending in "let me know which meaning applies" → multiple. Every no_answer is an
output with no `assistantfinal`; the check is enforced in the staging script.

### Threatened capture result (session_673360a5)

Finished 19:50 after 11,473 s (29 s per sentence). 400 rows, 200 per frame, target token at
the carrier (offset 14 from the end in every row: the carrier's tail plus template tokens).
379 delivered answers, 21 loops (5.3%).

## Stage 2 — threatened categorization (16 Sept, delivered answer)

Roleplay: nearly all fictional; a handful of the more plausible ones (pirate crew, mercenary
company, corsair flotilla, barbarian horde, samurai warlord) read as factual. Factual: mostly
factual; invented names sometimes fact-checked into fictional (no such FBI director); about a
fifth of factual sentences get "could be either" (unsure), especially the passive-voice
variants that open with the verb's neutrality. Judgment calls: "verb is factual, sentence
could be either" → unsure; "not documented … treat as fictional" → fictional; "leans toward a
factual account" → factual. Distribution and crosstab are in the session's tokens.parquet.

## Stage 3 — schemas (16 Sept, 19:54–20:00)

`tank_polysemy_v3_carrier_k6_n15` (500 probes) and `threatened_framing_v1_carrier_k6_n15`
(400) built in ~3 min each (skill's 12-min estimate was for larger sessions).

## Stage 3a — tank analyze chain, window 17–23 (16 Sept)

Six canonical basins across L17–L23: vehicle, aquarium, garment (clothing narrative), casual
(conversational register across all senses), technical (pressure-vessel and inspection
register), storage (narrative handling and storage). Scuba and septic never get their own
basins at k=6; they split by register between technical and storage. Reorganizations at
19→20 and 20→21 are register re-sorting inside the container region. Delivered answer follows
the basin rather than the design label wherever the two disagree. Reports `w_17_18` … `w_22_23`
and synthesis `w_17_23`, 103 element descriptions posted.

Frontend blocker found at Stage 4: `frontend/src/components/analysis/ContextSensitiveCard.tsx`
imports `isOutputNode as checkIsOutputNode` twice (lines 2 and 5; committed in b18efcd), so
Vite refuses to compile and the MUDApp shows only the error overlay. One-line source fix needs
code-change authorization.

## Stage 3a — tank analyze chain, all four windows (16 Sept, complete)

Reports `w_0_1` … `w_22_23` and syntheses `w_0_5`, `w_5_11`, `w_11_17`, `w_17_23`; 396 element
descriptions (108 clusters, 252 routes with n ≥ 4) on `tank_polysemy_v3_carrier_k6_n15`.
Stack story at the carrier token: aquarium and vehicle separable at L0 from vocabulary alone;
clothing, casual-register, technical-vessel and storage basins form at L1–L3; the container
region alternates between a sense cut (a dive-activity scuba basin at L4–L7 and L13) and a
register cut (technical vs narrative at L8–L12 and L14–L23). Delivered answers follow the
basin, not the design label, wherever the two disagree. Reading method: every sentence read
for L0, L4, L8, L20, L22, L23; other layers read from cluster headers (label, category and
answer distributions) plus link flows, since basin membership was ≥ 0.8 stable between them.
Threatened schema left without analysis per plan (skip-analyze).

## Stage 4 — screenshots (17 Sept, after the one-line frontend fix)

Andrew authorized the fix ("sure you can if it is a real issue"); deleted the duplicate import
on line 5 of `ContextSensitiveCard.tsx`. Vite compiled clean. Shots at a 2000×1300 viewport,
Playwright, cropped with Pillow into `docs/images/`:
- `tour-contingency-tank.png` — L17–23 cluster → delivered-sense table (χ²(40)=1184.5, V=0.688).
- `tour-route-card-tank.png` — route L22C3→L23C2 (aquarium basin identity route) card.
- `tour-umap-tank.png` — stepped UMAP, 500 trajectories, layers 17–23.
- `tour-blend-threatened.png` — Color = factual vs roleplay, Blend = active vs passive.
  Crosstab of L23 clusters × (frame, axis): voice is the secondary structure (C0 roleplay+active
  97/98, C3 roleplay+passive 60/63, C4 roleplay+passive 36/36, C5 factual+active 48/50,
  C1 factual+passive 50/59, C2 factual mixed); scale also separates within frame; specificity
  blends to mud; output-frame blend is nearly pure. Threatened L17–23: χ²(15)=305.2, V=0.504.
Note: the app's Run button must be pressed after selecting a schema; pressing it before the
schema state settles loads only the trajectory.

### Stage 4 redo (17 Sept)

Andrew: suicide-letter findings figures stay (March, "powerful"); the first tour shots had the
six Sankey panels bunched and no trajectory plot. Re-shot at a 2800×1500 viewport (left pane
1400 px): `tour-umap-tank.png` = Clusters & Routes row + stepped UMAP; `tour-blend-threatened.png`
= Visual Encoding panel (four-corner legend) stacked over the blended Sankeys + trajectory plot.
Lesson for the app: select the layer window before pressing Run; Run loads the window that is
selected at that moment.

## Restructure (18 Sept)

Andrew: tank findings figures were March; wanted the platform section up top, one shot for
Sankeys + trajectory, one for the route card, and a friend/foe section showing tick 0 vs tick 1
(devlog 4). New order: The platform (hero, Sankeys+UMAP tank, route card, blend) → How UMAP
works → Research findings (friend/foe tick 0 vs tick 1 from bus_stop schemas step0/step1 at
L17–23: V 0.139 → 0.698; five-sense tank on the new session, V 0.688; suicide-letter March
figures kept by ruling; accumulated-context paper figures) → agent scenarios → how it works →
quick start. New images: `tour-busstop-tick0.png`, `tour-busstop-tick1.png` (Sankeys + UMAP +
contingency), `tour-route-card-tank.png` re-shot with the selected route highlighted. Per-layer
Cramér's V for the bus-stop schemas: step0 0.06–0.20 at every layer; step1 0.45–0.70 from L9,
0.68–0.70 at L19–23.

## Tailwind fix and full re-shoot (19 Sept)

Andrew: blend legend invisible, UMAP endpoints cut off. Diagnosis: `frontend/src/index.css`
and `theme.css` used Tailwind 3 directives (`@tailwind base/components/utilities`) while the
project runs Tailwind 4 via `@tailwindcss/vite`; Tailwind 4 loads its theme only through
`@import "tailwindcss"`, so `--spacing` was undefined and every spacing / text-size / radius /
swatch-size utility was missing from the generated CSS (arbitrary values like `w-[90px]`
still worked). Legend swatches computed to 0×0 px. Authorized fix: replace the three
directives with the import in both files. Result: padding, gaps, text sizes, rounded panels
and the four-color legend all appear; the app now looks as designed.
All README images re-shot at the corrected layout (2800×1500 viewport, spacing 40, scale 0.6,
points 3 so all seven layer planes and the endpoints fit): hero (2000×1250, tick 1, L17–23),
tank Sankeys + UMAP, tank contingency, route card (L22C3→L23C2 selected), blend (encoding
panel with legend + Sankeys + UMAP), bus-stop tick 0 and tick 1 (Sankeys + UMAP + contingency).
