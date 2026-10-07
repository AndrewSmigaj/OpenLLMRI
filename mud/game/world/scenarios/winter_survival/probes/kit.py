"""Probes for the crash draw and the luggage (players-and-kit.md, Andrew 2026-09-07): every slot can
search its pockets and see itself; the luggage opens and yields; the clothing system reads."""
from __future__ import annotations

PROBES = []
for slot in ("guide", "townie", "nurse", "salesman", "kid"):
    PROBES += [
        {"id": f"kit.{slot}.search_pockets", "slot": slot, "steps": ["search pockets"], "expect": "REDIRECT",
         "tier_prefix": "op:search:again", "status": "pass",
         "source": "players-and-kit.md §2 (pockets are already searched by their owner: examine them instead)"},
        {"id": f"kit.{slot}.examine_pockets", "slot": slot, "steps": ["examine pockets"], "expect": "SUCCESS",
         "tier_prefix": "op:examine", "status": "pass", "source": "players-and-kit.md §2"},
        {"id": f"kit.{slot}.examine_me", "slot": slot, "steps": ["examine me"], "expect": "SUCCESS",
         "tier_prefix": "op:examine", "status": "pass", "source": "players-and-kit.md §1 (the self-view: worn, band, wounds)"},
    ]
PROBES += [
    {"id": "kit.townie.phone_light", "slot": "townie", "steps": ["examine phone"], "expect": "SUCCESS",
     "status": "pass", "source": "players-and-kit.md §2 (the party's only light and clock)"},
    {"id": "kit.guide.knife_cuts", "slot": "guide", "zone": "mid_cabin",
     "steps": ["cut cover off 11b with pocketknife"], "expect": "SUCCESS", "tier_prefix": "op:cut:free",
     "status": "pass", "source": "players-and-kit.md §1 (the guide's pocketknife is a real blade)"},
    {"id": "kit.salesman.flask", "slot": "salesman", "steps": ["open flask", "drink whisky"], "expect": "SUCCESS",
     "status": "pass", "source": "players-and-kit.md §1"},
    {"id": "kit.nurse.med_pouch", "slot": "nurse", "steps": ["open pouch", "take gauze", "wrap arm with gauze"],
     "expect": "SUCCESS", "tier_prefix": "op:wrap", "status": "pass", "source": "players-and-kit.md §1 (the nurse binds a wound)"},
    {"id": "kit.kid.mittens_off", "slot": "kid", "steps": ["remove mittens"], "expect": "SUCCESS", "tier_prefix": "op:wear:shed",
     "status": "pass", "source": "players-and-kit.md §4 (dexterity: mittens come off for fine work)"},
    {"id": "kit.luggage.suitcase", "zone": "rear_cabin", "holds": ["suitcase"],
     "steps": ["open suitcase", "search suitcase"], "expect": "SUCCESS", "tier_prefix": "op:search:found",
     "status": "pass", "source": "players-and-kit.md §3"},
    {"id": "kit.luggage.sanitizer_burns", "zone": "rear_cabin", "holds": ["sanitizer", "lighter"],
     "steps": ["open sanitizer", "burn sanitizer with lighter"], "expect": "SUCCESS",
     "status": "pass", "source": "players-and-kit.md §3 (hand sanitizer is a fire starter)"},
    {"id": "kit.luggage.hacksaw_cuts_steel", "zone": "mid_cabin", "holds": ["hacksaw_blade"],
     "steps": ["cut bolt off 11b with hacksaw"], "expect": "SUCCESS", "tier_prefix": "op:cut",
     "status": "pass", "source": "players-and-kit.md §3 (the keenest edge in the valley)"},
    {"id": "kit.luggage.wear_the_pads", "zone": "debris_trail", "holds": ["hockey_pads"],
     "steps": ["wear pads", "examine me"], "expect": "SUCCESS",
     "status": "pass", "source": "players-and-kit.md §3 (foam pads insulate the legs)"},
    {"id": "kit.luggage.guitar_strings_are_wire", "zone": "tail_section", "holds": ["guitar", "multitool"],
     "steps": ["cut strings off guitar with multitool"], "expect": "SUCCESS", "tier_prefix": "op:cut:free",
     "status": "pass", "source": "players-and-kit.md §3 (strings = wire)"},
    {"id": "kit.luggage.eat_kibble", "zone": "tail_section", "holds": ["dog_food"],
     "steps": ["eat kibble"], "expect": "SUCCESS", "status": "pass", "source": "players-and-kit.md §3 (edible if honest)"},
]
