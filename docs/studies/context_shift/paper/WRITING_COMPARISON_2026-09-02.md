# How papers are written, and how ours is written (2 September 2026)

Three sources: Mensh and Kording's "Ten simple rules for structuring papers" (PLOS
Computational Biology, 2017); Gopen and Swan's "The Science of Scientific Writing"
(American Scientist, 1990); and Anthropic's July 2026 paper "Verbalizable
Representations Form a Global Workspace in Language Models" (Gurnee, Sofroniew,
Lindsey and colleagues), which I pulled as a human-written paper in our field. I
measured its prose and ours with the same script.

## 1. What the guides say

**The whole paper carries one message.** Mensh and Kording: "Focus on a single
message; papers that simultaneously focus on multiple contributions tend to be less
convincing about each." The title is the most refined form of that message.

**Write for people who do not know the work.** Their second rule, verbatim: "Write for
flesh-and-blood human beings who do not know your work." Readers hold only a few
things in working memory at once, so "minimize the number of loose threads that the
reader has to keep in mind at any one time."

**Every unit has the same shape: context, content, conclusion.** At the scale of the
paper, the introduction is context, the results are content, the discussion is the
conclusion. At the scale of a paragraph, "the first sentence defines the topic or
context" and "the last sentence provides the conclusion to be remembered." A results
paragraph opens with the question it answers, gives the evidence, and ends with the
answer.

**The abstract tells the complete story in that shape.** Context: what gap the paper
fills and why it matters. Content: "Here we" did this, and found this. Conclusion: the
answer to the question the context posed. Their warning, verbatim: "This structure
helps you avoid the most common mistake with the abstract, which is to talk about
results before the reader is ready to understand them."

**Terms and words.** "Define technical terms clearly because readers can become
frustrated when they encounter a word that they don't understand. Avoid abbreviations
and acronyms." And: "Resist the temptation to use a different word to refer to the
same concept — doing so makes readers wonder if the second word has a slightly
different meaning."

**Inside the sentence.** Gopen and Swan's rules are about where readers expect things.
The subject and its verb should be close together; a subject separated from its verb
by a long insertion "burdens and obstructs the reader." The end of a sentence is the
stress position, where readers put emphasis, so the important new information belongs
there. The start of a sentence is the topic position, where readers expect context and
familiar material, so old information comes first and new information last. Long
sentences are not the problem in themselves: "Long sentences need not be difficult to
read; they are only difficult to write." What makes a sentence hard is presenting
information out of the order the reader expects.

## 2. How the Anthropic paper does it

The paper opens with an image any reader can hold: "If the mind is an ocean, we spend
our lives floating at the surface." Paragraph two states the thesis in one plain
sentence: "In this paper, we present evidence that an analogous functional
distinction has emerged in modern AI models." Paragraphs three through five each
explain one concept the reader will need (access consciousness; its functional
properties; global workspace theory), one paragraph per concept, before any of them is
used in an argument. Paragraph six asks the question the paper answers.

They name a new thing with a plain sentence: "Collectively, the J-lens vectors
comprise a subcomponent of the model's representational space which we term the
J-space."

They state a result with one measurement per sentence, the sample and the number
together: "Across 90 two-hop prompts, swapping the probes' J-space components flips
the model's answer on 61% of trials."

They hedge in separate sentences, not inside the claim: "The Jacobian lens is an
imperfect tool, which we believe only approximately and incompletely captures the
model's underlying workspace structure." And: "We do not claim that language models
reproduce the full architecture global workspace theory ascribes to the brain."

They write in the first person, present tense, active voice: we find, we observe, we
identify, we test.

## 3. The numbers

I ran the same measurements over their paper (349 paragraphs) and ours (57).

| Measure | Anthropic paper | Our draft |
|---|---|---|
| Words per sentence (mean) | 24.7 | 30.9 |
| Sentences over 35 words | 18% | 33% |
| Numbers per paragraph (mean) | 1.2 | 5.5 |
| Paragraphs with two numbers or fewer | 83% | 42% |
| Most numbers in one paragraph | — | 28 |
| Em-dashes per 1,000 words | 2.0 | 22.3 |
| Parentheses per 1,000 words | 11.7 | 18.5 |
| Semicolons per 1,000 words | 2.7 | 14.5 |
| Words per paragraph (mean) | 114 | 127 |

The two that matter most: we put four to five times as many numbers into prose as they
do, and we use eleven times as many em-dashes. The em-dashes are how the extra
numbers and the caveats get inserted mid-sentence. The semicolons, five times theirs,
are how findings get chained into one sentence instead of ending it.

## 4. Side by side

Theirs, a results paragraph (102 words, three numbers):

> This observation led us to hypothesize that the J-space is capable of holding a
> larger number of concepts at a time if they have some coherent relationship, but has
> a more limited capacity to simultaneously represent entirely unrelated concepts. To
> measure these effects more precisely, we apply the J-lens at each comma, counting a
> list word as present if its best rank over the workspace band falls within the top
> 25. We then compare lists of related words against lists of unrelated words drawn at
> random.

Ours, the remnant-gap paragraph from section 3.2 as it stands (one sentence of it):

> Both directions of both tasks show positive gaps under family-clustered bootstrap:
> tank →vehicle +2.16 [1.87, 2.44] — equivalently 1.09× the no-shift amplitude, the
> distance from the class midpoint to the matched reference; a shortfall larger than
> the amplitude itself means this plateau sits at the class midpoint, the transition
> stopped at half-way; tank →aquarium +1.15 [0.82, 1.45]; fiction→real +0.38 [0.28,
> 0.49]; real→fictional +0.35 [0.11, 0.58].

Their paragraph opens with what they thought, says what they did, and says what they
compared. A reader can say it aloud. Ours is one sentence holding twelve numbers, two
unit systems, an aside inside an aside, and four semicolon-chained results. The same
content, written their way, is a table of the four gaps plus one sentence: "The gap
is positive in both directions of both tasks (Table 1). In the largest case,
tank→vehicle, the plateau sits at the midpoint between the two senses: twenty
sentences of vehicle evidence leave the reading halfway."

## 5. What I take from this

The difference between their writing and mine is not vocabulary or mathematics. It
is four habits, all measurable:

1. **One measurement per sentence, one or two numbers per paragraph.** Everything else
   goes in a figure caption or a table. This alone would remove most of the reading
   burden in sections 3.2 and 3.6.
2. **Sentences of about twenty-five words, and none over thirty-five.** A sentence over
   thirty-five words is almost always two sentences with a dash in the middle.
3. **An aside is a sentence, not an insertion.** Caveats, definitions, and sample sizes
   get their own sentence after the claim. Em-dashes are for one aside per paragraph
   at most; parentheses for units and figure references only.
4. **Introduce before use.** Each term the reader will need gets a sentence that
   explains it before the argument leans on it; new terms are coined with "we call
   this".

Plus the two structural rules from the guides that the section review already asked
for: every paragraph opens with its question or topic and closes with its answer; old
information first, new information last.

These are mechanical enough to check. When I rewrite a section, I can run the same
script over it and report sentence length, numbers per paragraph, and dash density
against the Anthropic figures before you read it. That makes the standard something
you can verify rather than something I assert.

## Sources

- Mensh B, Kording K (2017). Ten simple rules for structuring papers. PLOS
  Computational Biology 13(9): e1005619. https://pmc.ncbi.nlm.nih.gov/articles/PMC5619685/
- Gopen G, Swan J (1990). The Science of Scientific Writing. American Scientist 78(6).
- Gurnee W, Sofroniew N, Lindsey J, et al. (2026). Verbalizable Representations Form a
  Global Workspace in Language Models. Transformer Circuits Thread.
  https://transformer-circuits.pub/2026/workspace/index.html
- Anthropic research summary of the same work:
  https://www.anthropic.com/research/global-workspace
