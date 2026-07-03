"""Whiteout — the crash-site zone map (DR-13a): positions, edges, survey prose. Tunable content —
Andrew's geography and voice; rewrite freely. Loaded by content.load() via zones.load_zones().

Layout: the plane lies nose-south; the tail breach opens north toward the treeline. Meters,
y+ = north. Edges: `walk` = you can step it; `see` = sightline (a wall is an ABSENT see edge);
`muffle` = sound passes damped (none authored yet — every interior/exterior crossing here is a
physical opening).
"""

ZONE_TABLE = {
    "cockpit": {
        "name": "the cockpit", "x": 0, "y": -8, "elevation": 0,
        "terrain_tags": ["interior", "cramped"],
        "aliases": ["cockpit", "flight deck", "front", "nose of the plane"],
        "look": "Shattered instruments and a crazed windscreen; cold air knifes in off the snow.",
        "adjacent": {
            "mid_cabin": {"walk": True, "see": True},
            "outside_nose": {"see": True},          # the shattered windscreen: sight, no passage
        },
    },
    "mid_cabin": {
        "name": "the mid cabin", "x": 0, "y": -2, "elevation": 0,
        "terrain_tags": ["interior"],
        "aliases": ["mid cabin", "cabin", "middle", "midship"],
        "look": "Buckled seat rows and spilled luggage crowd the aisle.",
        "adjacent": {
            "rear_cabin": {"walk": True, "see": True},
        },
    },
    "rear_cabin": {
        "name": "the rear cabin", "x": 0, "y": 4, "elevation": 0,
        "terrain_tags": ["interior"],
        "aliases": ["rear cabin", "rear", "aft", "back", "tail section"],
        "look": "The hull splits open here; snow sifts through the tear with every gust.",
        "adjacent": {
            "outside_tail": {"walk": True, "see": True},   # the split hull
        },
    },
    "outside_nose": {
        "name": "the snow outside the nose", "x": -4, "y": -12, "elevation": 0,
        "terrain_tags": ["exterior", "snow"],
        "aliases": ["outside the nose", "nose outside", "front outside"],
        "look": "Drifted snow banks against the crumpled nose cone.",
        "adjacent": {
            "fuselage_top": {"walk": True, "see": True},   # a scramble up the buckled panels
            "outside_tail": {"walk": True, "see": True},   # along the hull
        },
    },
    "fuselage_top": {
        "name": "the top of the fuselage", "x": 0, "y": -5, "elevation": 3,
        "terrain_tags": ["exterior", "metal", "exposed"],
        "aliases": ["fuselage top", "roof", "top of the fuselage", "top of the plane"],
        "look": "Wind scours the bare aluminium spine. A torn metal base juts where the antenna "
                "should be, a short cable hanging loose and rimed with ice.",
        "adjacent": {
            "outside_tail": {"see": True},                  # sighting along the spine
        },
    },
    "outside_tail": {
        "name": "the torn tail opening", "x": 3, "y": 10, "elevation": 0,
        "terrain_tags": ["exterior", "snow"],
        "aliases": ["outside the tail", "tail outside", "breach", "outside"],
        "look": "The tail section yawns open onto trampled snow; the treeline stands north.",
        "adjacent": {
            "treeline": {"walk": True, "see": True},
        },
    },
    "treeline": {
        "name": "the treeline", "x": 0, "y": 40, "elevation": 2,
        "terrain_tags": ["exterior", "trees", "cover"],
        "aliases": ["treeline", "trees", "forest", "spruces"],
        "look": "The first spruces close overhead; the wreck is a broken shape back through "
                "the falling snow.",
    },
}
