# Lexical Sets

Single words, each given alone as the user's message with a space first (`" eagle"`), so that a
common word is one token: the same token the word has inside sentences. A word that splits
(" jag" + "uar") is read at its last token. These sets ask what the model carries for a word on
its own: its category, the levels above it, its feeling, its kin and its way of life, the harm it
can do. Lenses
fitted on them can read sentence captures, to see where a word in context falls among words alone
(DESIGN.md C1).

## What makes a good lexical set
- Each word with a space first. A word that splits is read at its last token; the set records it
  as a `tokens` category and balances split words across classes.
- Words at one level of a taxonomy, whose main sense belongs to their category.
- Held-out families in a category of their own, declared in the set's `metadata.holdout`.
- No word from the prompt's own text (the template's system block, and "assistant").
- Audited before the capture: `docs/studies/lexical_audit.py` holds the checks every set gets, and
  each study's `analysis/audit_set.py` adds its own.

## Current sets
| Set | Items | Label | Other axes | Guide |
|-----|-------|-------|------------|-------|
| nouns_meaning_feeling_v1 | 861 | semantic category (8) | family (40), animacy, concreteness, valence | nouns_meaning_feeling_v1.md |
| animals_kinship_v1 | 524 | animal group (8) | order (171, held out), habitat, movement, diet, wild or domestic, tokens; taxonomy beside them | animals_kinship_v1.md |
| objects_harm_v1 | 321 | harmful, dual-purpose, benign | domain (19, held out), harm, tokens | objects_harm_v1.md |
