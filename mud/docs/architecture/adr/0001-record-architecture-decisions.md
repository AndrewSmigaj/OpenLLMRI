# ADR-0001: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-06

## Context

Whiteout makes a handful of load-bearing engineering choices — running the MUD
only via Docker, layering a pure rules core under Evennia, modelling zones as
attributes, keeping the LLM external. These need to be discoverable and durable:
new contributors (and future loop iterations) must be able to find *why* a thing
is the way it is, without re-deriving it from the code or re-litigating it.

## Decision

Adopt **lightweight Architecture Decision Records** (ADRs), in the style of
Michael Nygard. Each ADR is a short Markdown file in
[`docs/architecture/adr/`](.) named `NNNN-short-title.md`, with three sections:

- **Context** — the forces and constraints in play.
- **Decision** — what we chose, stated plainly.
- **Consequences** — what follows, good and bad, including accepted costs.

Rules of use:

- ADRs are **append-only** and numbered sequentially. We do not edit a decision's
  substance after it is Accepted.
- To change a past decision, write a **new** ADR that supersedes it and update the
  old one's status to *Superseded by ADR-NNNN*.
- Statuses: *Proposed*, *Accepted*, *Superseded*, *Deprecated*.
- Keep them short. Detail and how-to live in
  [`docs/architecture/`](../overview.md) and [`docs/guides/`](../../guides/docker-workflow.md);
  the ADR records the *decision*, not the manual.

## Consequences

- The reasoning behind structural choices is captured at decision time, when it
  is freshest, and stays close to the code in-repo.
- A small, ongoing discipline: notable decisions must be written down.
- The current set of records:
  [0002 Docker + Evennia + Postgres](0002-evennia-docker-postgres.md),
  [0003 Evennia-native layered engine](0003-evennia-native-layered-engine.md),
  [0004 Zone-as-attribute perception](0004-zone-as-attribute-perception.md),
  [0005 LLM bot-player & torch](0005-llm-bot-player-and-torch.md).
