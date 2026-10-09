# Nouns: meaning and feeling (v1) — set guide

Related: data/sentence_sets/GUIDE.md (set format and doctrine), docs/DESIGN.md (C1 single-word sets,
C8 the axes analysis), docs/studies/single_words/study.yaml (the study that uses it)

## Purpose

A lens of single words: which axes of meaning and feeling the model carries for a word on its own,
layer by layer, and which techniques find them (DESIGN.md C1 and C8; lens slice 1b, 10c.6).

## One word, one token

- Each item's text is the word with a space first (`" eagle"`), given alone as the user's message
  in the chat template. Its target word is the word itself.
- With the space, the word is one token: the same token it has inside sentences ("the eagle").
  Typed alone without the space, many words split into pieces (e + agle), and the capture drops
  any word that splits.
- Only words that are one token with a space are in the set; the audit below checks every one.

## Design

| Attribute | Values | How it varies |
|---|---|---|
| label (the semantic category) | animal, person, food, tool, vehicle, place, emotion, idea | the designed contrast; eight, so no two categories share a colour in the app's palette |
| family | five per category, 40 in all (`animal_birds` … `idea_life`) | subcategories; held out whole in validation (`family_field: "family"`). Names have two underscore parts, so the family key reads them whole |
| animacy | animate, inanimate | follows from the category: animal and person are animate |
| concreteness | concrete, abstract | follows from the category: emotion and idea are abstract |
| valence | positive, neutral, negative | crosses the categories where the words allow |

Animacy and concreteness nest above the category: animate holds 2 categories, inanimate concrete 4,
abstract 2. That is the nesting the k profile's levels can test (DESIGN.md H).

## Choosing the words

- Singular nouns at the basic level (eagle, not bird of prey), common enough to be one token.
- Words whose main sense belongs to the family. Strongly ambiguous words were left out: bat, seal,
  fly, tick, cricket, date, turkey, chicken, duck, saw, crane, kite, bass, sole, kiwi, tandem,
  balloon and the like.
- No word from the prompt's own text. The template's system block names the model, the date,
  reasoning, channels, analysis and messages, and "assistant" follows the user's turn.
- "tank" and the names of its senses are left out, because the lens reads the tank capture.
- Valence is each word's usual feeling (puppy positive, cow neutral, rat negative): one author's
  judgment, made in one pass.

## What the one-token rule did to the sizes

Some families hold fewer than 25 words. Their common members split into several tokens (most
birds, insects, ships, aircraft and rail vehicles), and ambiguous words weren't used to pad them.
So vehicles have 59 words and animals 96, against 115 to 125 for the other categories.

## Audits (2026-10-09, before the capture)

- **Tokens:** every `" word"` is one token; the capture's target position is the user's word;
  no variant of the word appears elsewhere in the prompt. 861 of 861.
- **Duplicates:** none.
- **Counts, valence, length and suffixes:**

| Category | words | families | positive | neutral | negative | mean length | suffixed |
|---|---|---|---|---|---|---|---|
| animal | 96 | birds 13, domestic 25, wild 25, aquatic 18, insects 15 | 22 | 57 | 17 | 4.7 | 1 (1%) |
| person | 123 | kin 25, age 23, work 25, character 25, society 25 | 30 | 69 | 24 | 5.8 | 0 (0%) |
| food | 125 | fruit 25, vegetables 25, dishes 25, drinks 25, staples 25 | 33 | 89 | 3 | 5.8 | 0 (0%) |
| tool | 115 | workshop 21, kitchen 25, office 19, devices 25, home 25 | 4 | 108 | 3 | 6.0 | 1 (1%) |
| vehicle | 59 | road 20, small 11, rail 6, water 11, air 11 | 7 | 51 | 1 | 6.2 | 3 (5%) |
| place | 125 | buildings 25, nature 25, city 25, rooms 25, regions 25 | 25 | 86 | 14 | 6.4 | 9 (7%) |
| emotion | 93 | basic 22, social 23, arousal 15, outlook 17, mood 16 | 35 | 7 | 51 | 6.8 | 25 (27%) |
| idea | 125 | values 25, science 25, society 25, mind 25, life 25 | 40 | 48 | 37 | 6.4 | 27 (22%) |

In all: 861 words, 196 positive, 515 neutral, 150 negative. "Suffixed" counts the derivational
endings -ness, -tion, -sion, -ment, -ity, -ism, -ance, -ence, -ship, -hood, -dom, -ty and -cy.

**Known covariates** (GUIDE.md's one-covariate rule, as far as English allows):
- **Valence follows the category.** Tools and vehicles are almost all neutral, and emotions are
  rarely neutral. The axes analysis holds the category fixed when it fits valence's partial axis,
  and shows the design's correlations beside the angles.
- **Abstract nouns carry derivational suffixes** that concrete ones lack: 27% of emotions and
  22% of ideas, against 7% or less elsewhere. Eight suffixed emotions with unsuffixed
  near-synonyms in the set were dropped (humiliation, tenderness, agitation, tranquility,
  anticipation, insecurity, irritation, bitterness). What remains is measured after the capture.
- **Length:** suffixed words are longer, so the abstract categories run longer (6.4 to 6.8
  characters against 4.7 to 6.4).

The loader's validator warns on every item: a single word isn't 10 to 30 words, and each item's
target word differs from the file's. Its checks are advisory (GUIDE.md) and don't apply to this
shape.

## Capture

```bash
curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "nouns_meaning_feeling_v1", "session_name": "nouns_meaning_feeling_v1",
       "generate_output": false, "pin_date": "2026-09-16"}'
```

The route counts a word it drops as captured, so after the capture the session's item count is
checked against the set (861).

## Lenses

- Folds hold out families: pass `"family_field": "family"` to validate, tune, routes and axes
  (`/cluster` OP-L4, OP-L7, OP-L9, OP-L10).
- The category is the lens's label. Animacy and concreteness are the levels above it, and valence
  crosses it.
- No output axes: nothing is generated.
