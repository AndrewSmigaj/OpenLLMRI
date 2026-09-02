# Writing standard for the paper

This is the standard every section of the paper is written to and reviewed against.
It comes from three sources: Mensh and Kording, "Ten simple rules for structuring
papers" (PLOS Computational Biology, 2017); Gopen and Swan, "The Science of
Scientific Writing" (American Scientist, 1990); and measurements of a human-written
paper in our field, Anthropic's July 2026 "Verbalizable Representations Form a Global
Workspace in Language Models". The measurements are in
`WRITING_COMPARISON_2026-09-02.md`.

The reader is a person who knows the mathematics and the field but has not seen this
work. They read once, in order, and do not hold more than two or three loose threads
at a time.

## Rules

**Structure**

1. The paper carries one message. Each section has one job, and each paragraph has
   one job.
2. Every paragraph opens with its question or topic and closes with its answer or
   conclusion. A results paragraph says what was asked, what was seen, and what it
   means, in that order.
3. Old information comes before new information. The start of a sentence holds what
   the reader already knows; the end holds the new thing.
4. The subject of a sentence sits next to its verb. An insertion between them is
   moved out into its own sentence.

**Numbers and evidence**

5. One measurement per sentence. One or two numbers per prose paragraph. Everything
   else goes in a table or a figure caption. Prose keeps only the values the
   argument turns on.
6. A sample size, an interval, or a caveat follows the claim as its own sentence. It
   is not inserted into the claim.
7. No claim is stated stronger than its evidence. Suggestive results are called
   suggestive. Exploratory results are called exploratory.

**Sentences and punctuation**

8. Sentences run about 25 words. None run over 35. A sentence over 35 words is
   almost always two sentences.
9. An aside is its own sentence. At most one em-dash aside per paragraph. Parentheses
   are for units, figure references, and citations only.
10. Semicolons do not chain results. Each result ends its sentence.

**Terms**

11. Every term is explained in a sentence before the argument uses it. A new term is
    coined with "we call this".
12. One name per concept, used every time. No synonyms for a defined term.
13. No invented labels, no grid-speak ("task-by-direction"), no notation in prose
    where words serve ("both directions of both tasks", not "2 × 2 conditions"). No
    repository codenames ("ab", "ba", "fr", "D3", "arm") in text, captions, or figure
    legends.
14. No rhetorical flourish. No negation-first reveals ("not merely X, but Y"), no
    announced drama, no restating a measurement lyrically. A declarative sentence
    carrying the claim is the strongest form.

**Voice**

15. First person plural, active voice. Present tense for what the paper shows;
    past tense for what was done.
16. No narrative about our own errors. A correction that changed a printed value is
    stated in one sentence where the evidence needs it, and listed in Appendix A.
17. No biography, no "one of us", no claims about the author's history.

**Completeness**

18. Nothing is left out. Every claim and every number in the previous version of a
    section appears in the new version, in its tables, or in its captions.

**Figures and captions**

19. A caption says what to look at and what it shows, in plain words. Numbers are
    allowed in captions.
20. A figure has a plain-English title or none, plain legend names, labeled axes with
    units, and no internal item numbers or codenames. Figure content does not change
    during the rewrite; only its labeling does.

## Metric targets

Measured per section by `tex/prose_metrics.py`. Tables, headings, and captions are
excluded from the counts. The Anthropic paper's values are in brackets.

| Measure | Target | [Anthropic] |
|---|---|---|
| Words per sentence, mean | ≤ 27 | [24.7] |
| Sentences over 35 words | ≤ 15% | [18%] |
| Em-dashes per 1,000 words | ≤ 6 | [2.0] |
| Semicolons per 1,000 words | ≤ 5 | [2.7] |
| Numbers per prose paragraph, mean | ≤ 2.5 | [1.2] |

Reported for information, not gated: parentheses per 1,000 words [11.7]; words per
paragraph [114]; most numbers in one paragraph.

A section that misses a target needs a stated reason in `draft/REVISION_LOG.md`.
Sections that are mostly definitions (the protocol box, the glossary, the
appendices) may miss the number-density target with a note.

Numbers are also checked by `tex/number_check.py`: every numeral traces to the
findings record or the allowlist, and every numeral in the pre-rewrite version
(`draft_v2/`) survives in the new version.

## Reviewer's brief

You are reading one section of a research paper, with the captions of the figures it
cites and the figures themselves. You have not seen the rest of the paper or any of
the underlying work. Judge the section against the rules above and against your own
sense of whether a person can read it.

Answer these questions, quoting the text where you find a problem:

1. Can a reader who knows the mathematics but not this work follow the section on one
   pass, in order? Where do they get lost?
2. Does each paragraph open with its question or topic and end with its answer?
   Which paragraphs do not?
3. Is every term explained before it is used? Which terms are not?
4. Is the number density acceptable? Which sentences carry more than one measurement?
   Which paragraphs would read better with their numbers in a table?
5. Are the figures readable on their own? Does each caption say what to look at? Are
   there codenames, internal item numbers, missing axis labels, or unexplained bands
   or colors?
6. Compare the section against the inventory of claims and numbers you were given.
   Is anything from the inventory missing?
7. Is any claim stated more strongly than the inventory supports?
8. Is there any rhetorical flourish, invented label, grid-speak, or narrative about
   the authors' own errors?

Return either PASS, or a numbered list of specific fixes. Each fix quotes the text,
says what is wrong, and proposes a replacement. Do not rewrite the section. Do not
soften a finding because it is unflattering.
