# Overnight queue, 2026-10-19

Worked by a `/loop` every 30 minutes, one box per firing. The plan behind it: the plan page's L36
(Winter Survival now?) and its "Where we are".

## How each firing works

1. Read this file and Andrew's answers: ArtifactData `list` of `answers` on the plan page
   (L36, L36.1) and on the design page (L33, L35).
2. Take the first unticked box whose condition holds. A box whose condition doesn't hold yet is
   skipped; say so in the log.
3. Before CPU-heavy work, check `free -g`. Below 6 GB available, don't start it: log it and stop.
4. Do that one box, as far as one bounded chunk goes. Commit locally by explicit paths, after
   listing the index. Tick the box (or note where it stopped), add a line to the log, stop.
5. Never load the model, never push, never delete lake data, never touch the held node-card files
   (`backend/src/services/lenses/{atlas,data,details,model_weights,writers}.py`,
   `backend/src/services/llm/packets.py`, `backend/tests/test_lens_writers.py`,
   `frontend/src/components/layers/{NodeDetails,SplitWriters}.tsx`, `frontend/src/types/lens.ts`).
6. When every box is ticked, or waits on an answer that hasn't come, write the morning summary
   below and end the loop.

Conditions: **machine** = Andrew said the machine is free tonight; **L36**, **L36.1**, **L35.7**,
**L33** = his answer on that card.

## The research software

- [ ] **R1** [machine] Start the backend without the model (`/server` OP-3b, `LOAD_MODEL=0`,
  `JOB_WORKERS` at its default while memory is free), then OP-4 until `skipped`. Submit the tank
  re-score again (`POST /api/sessions/session_1434a9be/lenses/tank-k5-n15-tuned/rescore`, draws 5);
  check that the calibration, words and animals re-scores start from the queue. About 3 to 4 hours
  of CPU in all.
- [ ] **R2** [R1; a re-score done] One finished re-score per firing: its tuning section in
  `docs/research/lens_core_validation.md` (tank, calibration), `single_words.md` or `animals.md`,
  every number re-read at every layer it names, and its study's ledger.
- [ ] **R3** [R2 done for all four] The single-words showcase's "one draw" caveat and its republish
  (read the live page back first); the RECOMMENDATIONS.md entry for 10g; Built marks for LENS-21 to
  LENS-24 and ARCH-13; an independent numbers audit, a readability review and the near-quote scan;
  both pages republished; the memory note.
- [ ] **R4** [L35.7 step 1 approved; the re-scores finished, so the cores are free] The CPU pass on
  the calibration and framing captures: `cpu_pass.py`'s prompts rebuilt in the chat template with
  each capture's pinned date, checked against the stored states; sections 9 and 10 of
  `docs/research/attention_and_experts.md` and the study's ledger updated.
- [ ] **R5** [L33 answered] As answered. As recommended: the held node-card code goes onto a branch
  without a checkout, and the atlas entries of the three saved versions are rewritten on `main`'s
  code.

## Winter Survival

- [ ] **W1** [L36: Winter Survival now] The map review made ready: read the map page
  (https://claude.ai/artifact/FT89UNSYHqzF12yE2LHkc5) back; check each region against
  `mud/PLAN.md` §5 and the design documents that name it; republish it with a box per region (keep,
  change, Other with a note) and the check's findings beside each. No repo files change.
- [ ] **W2** [L36.1: build M1] Pilot M1: re-read document 05 §4.5 and §4.5a, document 22 and the
  pilot plan's changes (`~/.claude/plans/world-building-pilot.md` §2); a certainty table here first
  (stop if a load-bearing row is below 90%); then the store's schema, canonical YAML, the validator,
  `make validate-ontology` and the store's README, with host tests; `make verify` green; document
  22's "What exists today" and `mud/PLAN.md` updated.
- [ ] **W3** [W1 or W2 done] The memory resume notes (the one-MUD plan, the program) updated.

## Morning summary

(written when the loop ends)

## Log

(one line per firing)
