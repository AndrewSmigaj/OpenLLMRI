"""The closure chain — Andrew's example, as typed commands (approved 2026-09-07). A minted shard is a
real blade; the freed cover is a sheet; burning it leaves ash. Source: the plan / ontology-closure.md."""
from __future__ import annotations

PROBES = [
    {"id": "chain.break_bottle", "zone": "rear_cabin",
     "steps": ["break bottle"], "expect": "SUCCESS", "tier_prefix": "op:break:shatter",
     "status": "pass", "source": "ontology-closure.md §1 (the example chain, step 1)"},
    {"id": "chain.shard_cuts_cover", "zone": "rear_cabin",
     "steps": ["break bottle", "take shard", "cut cover off 12c with shard"],
     "expect": "SUCCESS", "tier_prefix": "op:cut:free",
     "status": "pass", "source": "ontology-closure.md §1 (the example chain, step 2)"},
    {"id": "chain.burn_the_cover", "zone": "rear_cabin", "holds": ["lighter"],
     "steps": ["break bottle", "take shard", "cut cover off 12c with shard", "burn fabric with lighter"],
     "expect": "SUCCESS", "tier_prefix": "op:burn:success",
     "status": "pass", "source": "ontology-closure.md §1 (the example chain, step 3)"},
    {"id": "chain.shard_cannot_cut_steel", "zone": "rear_cabin",
     "steps": ["break bottle", "take shard", "cut bolt off 12c with shard"],
     "expect": "REDIRECT", "tier_prefix": "op:cut:too_dull",
     "status": "pass", "source": "ontology-closure.md §3 (a shard is not a hacksaw)"},
    {"id": "chain.strip_ties", "zone": "rear_cabin", "holds": ["multitool"],
     "steps": ["cut cover off 12c with multitool", "tear fabric", "tie strip to 12c"],
     "expect": "SUCCESS", "tier_prefix": "op:tie:knot",
     "status": "pass", "source": "ontology-closure.md §3 (cordage by form)"},
    {"id": "chain.make_fire_teaches", "zone": "cockpit",
     "steps": ["make fire with sticks"], "expect": "REDIRECT", "tier_prefix": "op:make:fire",
     "status": "pass", "source": "live smoke 2026-09-07 (make bound the fire extinguisher)"},
    {"id": "chain.use_echoes_the_verb", "zone": "rear_cabin",
     "steps": ["break bottle", "take shard", "use shard on 12c cushion"], "expect": "SUCCESS",
     "tier_prefix": "use>op:cut", "status": "pass", "source": "live smoke 2026-09-07"},
    {"id": "chain.and_splits_and_it_binds", "zone": "rear_cabin",
     "steps": ["break bottle", "take shard", "examine it"], "expect": "SUCCESS",
     "tier_prefix": "op:examine", "status": "pass", "source": "live smoke 2026-09-07 (anaphora)"},
]
