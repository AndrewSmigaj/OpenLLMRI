# `world/scenarios/whiteout/` — the Whiteout scenario (skeleton)

The first authored world (the GDD: [`docs/scenarios/whiteout/GDD.md`](../../../../docs/scenarios/whiteout/GDD.md)).
**Status: skeleton (P0).** Layout below; content authored from roadmap P1 on.

| Path | What |
|---|---|
| `manifest.py` | PURE data: packet lists + metadata (importable without Evennia, so `make validate` lints it) |
| `build.py` | the Evennia loader: `build()` creates rooms/objects (`make load-scenario SCENARIO=whiteout`) |
| `materials/` | the hand-curated material table (~25; the quality anchor, DR-17) |
| `operations/` | authored operation rules (`*.op`) — the ~20 operation categories |
| `objects/` | cheap objects + the few §43 packets (radio/beacon/pilot/showcase seat) |
| `responses/` | narration / redirect templates (~50 curated signature responses for the slice) |
| `rescue.def` | the rescue graph (additive confidence; distinct scarce resources) |

Authored from the §43 packets as **goals with ≥3 clue/solution paths** (never recipes); everything passes
`make validate` (§44). See [`docs/guides/`](../../../../docs/guides/).
