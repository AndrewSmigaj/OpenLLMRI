# Overnight queue, 2026-10-19 and 2026-10-20

Andrew kept the order of work (L36, 2026-10-20): no Winter Survival work now, so the first
version's Winter Survival boxes are gone. The heavy steps run as one chain, each step its own
`mlock heavy` hold on the shared machine (`~/.claude/machine/README.md`), with the job worker run
directly (no backend; while the chain runs, the backend must not be started, or its scheduler
would mark the running job interrupted).

## The chain (started 2026-10-20, 12:16 local)

- [x] **A.** The attention-write lens test: `docs/studies/attention_experts/analysis/attention_lens.py`
  on framing, calibration, friend/foe and tank (the state, attention's write and the experts' write,
  each held out as a lens's validation is), about 10 to 15 minutes.
- [x] **B.** The four re-scores, one hold each, through `services.jobs.worker`:
  - tank-k5-n15-tuned (`job_20261020T191548323465_a2c726`, resubmitted; the 2026-10-16 job was marked
    interrupted by the scheduler's own `adopt`, which removed its temporary folder);
  - calibration-q1-k2-n15-tuned (`job_20261016T194251688980_8c699e`);
  - words-k8-n15-tuned (`job_20261016T194251702945_ee050b`);
  - animals-k8-n15-tuned (`job_20261016T194251716634_241a34`).

## After each step

- [x] **A done:** section 11 of `docs/research/attention_and_experts.md` and the study's ledger;
  the design page's attention section and L35 rewritten around the result; the requirements
  (the earlier attention proposals retired, the new ones added); marks audit, readability review,
  near-quote scan; both pages republished; commit.
- [x] **B done, one lens at a time:** its tuning section in `docs/research/lens_core_validation.md`
  (tank, calibration), `single_words.md` or `animals.md`, every number re-read at every layer it
  names, and its study's ledger.
- [x] **All four done:** the single-words showcase's "one draw" caveat and republish; the
  RECOMMENDATIONS.md entry for 10g; Built marks for LENS-21 to LENS-24 and ARCH-13; numbers audit,
  readability review, near-quote scan; pages republished; memory; commit. That ends 10g.

## Log

- 2026-10-20 12:16: chain started; step A waits behind two other projects' quiet measurements.
- 2026-10-20 12:56: step A done (the attention-write lens test); the where-attention-reads check
  ran after it, also through the lock.
- 2026-10-20 13:42: the tank re-score done; its write-up is in `docs/research/lens_core_validation.md`.
  The calibration re-score started.
- 2026-10-20, afternoon: section 11 of the attention note, the study's ledger, L35 and the attention
  section rewritten; three independent reviews (marks, numbers, readability) and a second-round
  audit applied; near-quote scan clean; both pages republished (design v41, plan v8).
- 2026-10-20 15:16, 16:05, 16:36: the calibration, words and animals re-scores done; the chain
  ended at 16:36. Each was written up (calibration in `docs/research/lens_core_validation.md`,
  `single_words.md`, `animals.md`), every number re-read at every layer, with its study's ledger
  and a new tuning line in the lens core's. The three saved lenses' atlas entries rewritten (only
  their validation headline changed).
- 2026-10-20, evening: 10g.8: the single-words showcase rebuilt and republished, the
  RECOMMENDATIONS.md entry, LENS-21, LENS-22 and LENS-24 marked built and LENS-23 in part;
  numbers audit, readability review, near-quote scan; both pages republished (design v42, plan
  v9); memory; commit. That ends 10g.
