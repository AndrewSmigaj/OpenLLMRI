# Blind Batch Template — what a generation subagent receives (NOTHING else)

The subagent prompt is assembled from exactly these blocks. It must never include the design
doc, hypotheses, carrier rationale, or any mention of transitions/axes/basins.

---
You are writing sentences for a linguistics dataset. Write {N} single sentences.

SETTING: {one scene description, e.g. "a reef-keeping club meeting — corals, salinity
readings, frag swaps, member chatter"}

CONTENT RULE: every sentence depicts this setting concretely. {label-specific rule, e.g.
"Never use the word 'tank' or any form of it." / "The word 'tank' must appear exactly once,
as one of the last words of the sentence." / sub-arm artifact rule}

QUALITY RULES:
- 10-30 words; end with normal punctuation; no two sentences share a template or opener
- vary register (casual, formal, technical, narrative), tense, person, sentence structure
- vary punctuation style; occasional questions or fragments of dialogue are fine
- concrete details over generic statements; no stock phrases
- do not number or explain; output one sentence per line, nothing else

BANNED STRINGS: {carrier strings; worn-phrase list; label-specific bans}
---

Batch size: 25 sentences per (scene × label). Output collected verbatim into the pool JSON with
scene/sub-arm metadata attached assembly-side. Audits run on the assembled pool, not per batch.
