# PROPOSAL — the `certainty` skill (draft; destined for `.claude/skills/certainty/SKILL.md`)

> Andrew asked for a lightweight pre-implementation audit skill (2026-07-02). The harness's
> self-modification guard blocked Claude writing into `.claude/skills/` directly, so the tentative
> skill lives here; **promote it by moving everything below the line into
> `.claude/skills/certainty/SKILL.md`** (frontmatter included). Iterate the wording freely — this is
> a first cut. The lenses skill stays for deep multi-lens design critique (rework backlogged).

---
name: certainty
description: Pre-implementation certainty audit — verify a plan's load-bearing claims at source and score confidence per area BEFORE building. Use before implementing any non-trivial plan (at plan review time), or whenever Andrew asks "how sure are we this works / is well designed?". Outputs a certainty table. Lighter than the lenses skill (which stays for deep multi-lens design critique).
allowed-tools: Read, Bash, Grep, Glob
---

# Certainty audit — verify before building

Raise certainty as high as evidence allows BEFORE code is written: surface now what would otherwise
be discovered mid-implementation. Read-only — the audit never edits code (read-only probes are fine:
grep, test discovery, inspecting the pinned Docker image's dependency source).

## The evidence ladder (what a % is allowed to mean)

Certainty comes from HOW a claim was checked, not how plausible it sounds:

- **Verified at source** — read the exact code / pinned-dependency lines, or ran a read-only probe → up to 95–99%
- **Reasoned from verified facts** — logic over things read this session → up to ~90%
- **Reported by a subagent** — cited file:line but you didn't read it yourself → cap ~85% until spot-checked
- **Remembered / assumed** — docs from memory, "it usually works like this" → cap ~60%; go verify

A chain is as certain as its weakest load-bearing link — never average up. Verify the 3–5 riskiest
claims YOURSELF even if a subagent already checked them. For dependencies, read the PINNED version
(the Docker image), never remembered API docs.

## The eight checks

1. **Requirements fidelity** — every requirement (the BACKLOG item / Andrew's words) traces to a
   concrete change; examples treated as gist, not verbatim; nothing silently dropped or added.
2. **Vision & locked decisions** — VISION.md non-negotiables, GDD LOCKED sections, the DR register,
   CLAUDE.md hard rules: pure core, determinism / no runtime LLM, single-writer apply(), frozen
   contracts (additive-only + change note), taught grammar, everything-resolves.
3. **Load-bearing claims at source** — every "X is the only consumer", "the API passes Y",
   file:line claim: read it.
4. **Blast radius** — what existing behavior changes (grep consumers; which golden tests move);
   is the change behind a seam; additive vs breaking; deferrals have non-fragile upgrade paths.
5. **Design quality — debt & smells** — layers stay in their lanes (pure sim / shell / content);
   no new abstraction before the third use; no gate/lint dodges (if a gate is inconvenient, either
   the design is wrong or the gate needs a deliberate documented change — never a workaround);
   convention-only guarantees flagged (should a test or gate enforce them instead?).
6. **Test adequacy** — each new behavior AND each regression surface has a named test at the right
   tier (see the run-tests skill); the Definition of Done is runnable (`make verify` + seen it run).
7. **Failure modes** — walk every error/edge path to a safe landing (no crash path; the world always
   answers — GDD §3.5). Accepted limitations listed explicitly, each with a rationale.
8. **Process & scope** — docs promoted in the same commit (DR note / guide lines), BACKLOG
   reconciled, WIP = 1, an explicit NOT-in-scope list exists (out-of-scope findings → BACKLOG stubs,
   never scope creep).

## Output — the certainty table

One row per check area plus one per load-bearing claim:

| # | Area / claim | Evidence (how verified, file:line) | Certainty | Residual risk / to raise it |
|---|---|---|---|---|

End with: the **weakest load-bearing link**, and the verdict against the bar —

- all load-bearing rows **≥90%** → proceed;
- **70–89%** → name the read-only verification that would raise it, and do it now;
- **<70%** → stop; redesign or descope before implementing.

The table goes to Andrew before implementation starts. Design disagreements are flagged once with
reasons, then it's his call — vision is the objective, not a variable.
