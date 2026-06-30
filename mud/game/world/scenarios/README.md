# `world/scenarios/` — authored content

Each scenario is one authored world/experience; the repo hosts many (Whiteout is the first). Content is
**cheap objects + ordinal materials + pre-authored operation rules**, with full §43 packets only for
puzzle-critical objects (radio / beacon / pilot / showcase seat).

> **Status: skeleton (P0).** The Whiteout subpackage layout + a `_template/` are in place; content is
> authored from P1 on (see
> [`docs/scenarios/whiteout/roadmap.md`](../../../docs/scenarios/whiteout/roadmap.md)).

```
world/scenarios/<name>/
  manifest.py    # PURE data: packet lists + metadata (importable without Evennia, so `make validate` lints it)
  build.py       # the Evennia loader: build() creates rooms/objects (make load-scenario SCENARIO=<name>)
  materials/     # the hand-curated material table (the quality anchor, DR-17)
  operations/    # authored operation rules (*.op)
  objects/       # cheap objects + the few §43 packets
  responses/     # narration / redirect templates
  rescue.def     # the rescue graph (additive confidence; distinct resources)
```

Authored from the §43 packets; everything passes `make validate` (the §44 content-lint hard gate). See
the authoring guides in [`docs/guides/`](../../../docs/guides/).
