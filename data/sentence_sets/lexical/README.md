# Lexical Sets

Single words, each given alone as the user's message with a space first (`" eagle"`), so that it
is one token: the same token the word has inside sentences. These sets ask what the model carries
for a word on its own: its category, the levels above it, its feeling. Lenses fitted on them can
read sentence captures, to see where a word in context falls among words alone (DESIGN.md C1).

## What makes a good lexical set
- Every word is one token with a space first; the capture drops words that split.
- Words at one level of a taxonomy, whose main sense belongs to their category.
- Families (subcategories) named in `categories.family`, held out whole in validation.
- No word from the prompt's own text (the template's system block, and "assistant").
- Feeling, length and suffixes audited by category before the capture (the set's guide).

## Current sets
| Set | Items | Label | Other axes | Guide |
|-----|-------|-------|------------|-------|
| nouns_meaning_feeling_v1 | 861 | semantic category (8) | family (40), animacy, concreteness, valence | nouns_meaning_feeling_v1.md |
