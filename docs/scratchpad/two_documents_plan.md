# The two documents — Claude's plan (2026-10-11)

Related: docs/DESIGN.md (How this document works, K, L24, L26), docs/architecture/one-mud.md,
docs/scratchpad/build_design_page.py

On 2026-10-11 Andrew adopted the documents' shape, requirements first, and the plan's move into the
plan-and-architecture document (DESIGN.md L26.1 to L26.3, each as recommended), and the checks
before he reads each one. The details below (files, scripts, the steps' order) are Claude's; he
reviews them with the documents. It is the first step in the order of work (L21).

## What he asked for

- **2026-10-10:** eventually one coherent architecture document, like the ones he writes with Claude
  in claude.ai, and one coherent design-and-requirements document, unless Claude sees a better
  approach.
- **2026-10-11 (L24):** both in the repo, each published as a page with comments and a form for its
  open questions, with the decisions in a dated log at the end of each.

## The model

Claude read the two documents Andrew updated most recently in claude.ai: a plan-and-architecture
page and a design document, which he keeps for another project. Their shape:
- **one long page each,** with an index down the side, a box to write in under every section
  (saved as you type, collected in a last section with a button to copy it all), questions as
  cards with options and Claude's pick, and coloured marks for status;
- **the plan-and-architecture page:** where we are (now, next, what needs you), how we work (a
  numbered working agreement), what Claude understood from his answers, the phases (each with its
  goal, why, steps, tests and when it is done), a register of known problems, the architecture
  sections, architecture decisions, a decision log, risks and appendices;
- **the design page:** how to use it, the project in his terms, the decisions needed, the current
  build, the design sections, open questions, his requirements (numbered, each with its date, its
  source and its status), what was rejected or retired, a changelog and a glossary;
- **requirements first:** both documents are written from the numbered requirements and cite them,
  checks in the repo catch retired wording, and there are no other plan files.

**Differences here:** this repo is public, so the documents never quote Andrew (requirements are
paraphrased; a page can show his own words only from its private store), and the sources stay
markdown, built into pages by one script, as DESIGN.md is today.

## The steps

| # | Step | Ends with |
|---|---|---|
| 0 | The requirements list | `docs/design/requirements.yaml`: every decision, idea, view, proposal and open question in DESIGN.md's marks, Part L's answers and his rulings on how we work, numbered by area (the goal, principles, lenses, time, the app and its rooms, the MUD and agents, data, studies, the builder, the atlas, interventions, the order of work, how we work). Each has a paraphrase, its dates, its source, its mark and the section that designs it. A script shows every mark in DESIGN.md mapped to a number |
| 1 | Design and requirements | `docs/design/design.md`: how to use it; what OpenLLMRI is for; the decisions needed (cards); what's built; lenses; reading over time; the app and its rooms (the rooms designed, as Claude's proposals, with cards); the MUD and agents in scenarios; studies; the builder; the atlas; interventions; the stories; open questions; the requirements; rejected and retired; terms; changelog; decision log |
| 2 | Plan and architecture | `docs/architecture/plan.md`: where we are; how we work; what Claude understood; the phases (those done, summarized, then the order of work, each with its goal, why, steps, tests, review and when it is done); the register of known problems (the parked items, the open recommendations, the known issues); the architecture (an overview diagram; the backend and the model; capture and the lake; jobs; lenses; the LLM analysts; the records in the repo; the command channel; the MUD, from `one-mud.md`; the new app, with its checklist of current features; testing; running, builds and branches; where things go); architecture decisions; decision log; risks; sources |
| 3 | The pages | one build script (from `build_design_page.py`), with the index, marks, cards (the form's tested code), the write-anywhere boxes and the collected writing. The design page keeps the current page's address and Andrew's answers; the plan page is new. Page checks: every cited requirement exists and is current, no retired wording, references between the pages resolve, every mark in DESIGN.md is accounted for, and none of his stored words appear in the repo |
| 4 | The other documents | DESIGN.md and `one-mud.md` become pointers; documents already superseded (SOFTWARE_OVERVIEW's concepts, LLMud/VISION.md, architecturemud.md, the time design drafts) are listed for deletion, for his yes; the open items in RECOMMENDATIONS.md move to the register (the file's future is his call); CLAUDE.md and the skills point to the new documents |
| 5 | Checks before he reads | an independent audit of every requirement against his words, a readability review, the page checks, and a browser walk of both pages at desktop and phone width with a stand-in store (boxes save and reload) |
| 6 | His review | section by section, through the boxes; Claude reads everything he wrote before each change, and "where we are" is updated every session |

## How sure

- **Nothing is lost in the move** (92%): every mark in DESIGN.md is mapped to a requirement by a
  script, then audited.
- **The pages work** (90%): they reuse the form's code, tested end to end and live since version 32
  of the design page.
- **The shape is what he wants** (85%): he named these documents as the model; L26 shows him the
  outline first.

## Risks

- **Long pages:** the index and the per-section boxes keep them navigable.
- **Sections restating requirements:** sections cite the numbers instead.
- **His words reaching the repo:** the page check.

## Not in this step

The new app's code, slice 2 (capture and jobs), and the animal ontology study (L27), which runs
beside it.
