"""Whiteout — the per-zone SPACE table (the scene-space model). Tunable content — Andrew's voice;
rewrite freely. Loaded by content.load() via spaces.load_spaces().

A space is a physical AREA of a zone (the floor, the footwell, overhead). Its FRAME describes
POSITION, never history — it must stay true when a player drops something into it, so it says where
things sit, not how they got there (the zone's own survey line in zones.py carries the history). The
frame slots: `{be}` → is/are (number agreement), `{items}` → the space's loose things, joined. A
space names at most `cap` things, then absorbs the rest into `overflow` (itself look-at-able).

An object lands in a space via its appearance `space` (its home) or a runtime `state['space']` (a
player drop); anything unassigned falls to the zone's `default`. This file covers the plane + its
immediate outside (the scene-spaces.md §4 pass); the rest of the crash cluster is authored later.
"""

SPACE_TABLE = {
    "cockpit": {
        "left_seat": {"order": 10, "frame": "Slung over the seat back beside him {be} {items}.",
                      "aliases": ["seat back", "left seat", "pilot's seat"]},
        "cradle": {"order": 20, "frame": "Below the cradle {be} {items}.",
                   "aliases": ["radio cradle", "cradle"]},
        "footwell": {"order": 30,
                     "frame": "Down in the footwell, against the rudder pedals, {be} {items}.",
                     "aliases": ["footwell", "rudder pedals", "pedals"]},
        "floor": {"order": 40, "frame": "Across the cockpit floor {be} {items}.", "default": True,
                  "cap": 3, "overflow": "a scatter of smaller debris",
                  "aliases": ["cockpit floor", "floor", "deck"]},
    },
    "mid_cabin": {
        "seat_rows": {"order": 10, "frame": "Wedged into the row {be} {items}.",
                      "aliases": ["seat rows", "rows", "row", "seats"]},
        "overhead": {"order": 20, "frame": "Overhead {be} {items}.",
                     "aliases": ["overhead", "bins", "ceiling"]},
        "aisle": {"order": 30, "frame": "Lying in the aisle {be} {items}.", "default": True,
                  "cap": 3, "overflow": "a scatter of spilled luggage",
                  "aliases": ["aisle", "floor"]},
    },
    "rear_cabin": {
        "rear_rows": {"order": 10, "frame": "Against the rear rows {be} {items}.",
                      "aliases": ["rear rows", "rows", "back rows"]},
        "overhead": {"order": 20, "frame": "Overhead {be} {items}.",
                     "aliases": ["overhead", "bin", "ceiling"]},
        "floor": {"order": 30, "frame": "Across the floor {be} {items}.", "default": True,
                  "cap": 3, "overflow": "a scatter of smaller debris",
                  "aliases": ["floor", "rear floor", "deck"]},
    },
    "outside_tail": {
        "hull_side": {"order": 10, "frame": "Rolled against the hull {be} {items}.",
                      "aliases": ["hull", "hull side", "against the hull"]},
        "the_snow": {"order": 20, "frame": "Half-sunk in the snow {be} {items}.", "default": True,
                     "cap": 3, "overflow": "a litter of smaller wreckage",
                     "aliases": ["snow", "the snow", "ground"]},
    },
    # outside_nose / fuselage_top hold no loose objects today — each still needs one default space so
    # a player drop has somewhere honest to land.
    "outside_nose": {
        "the_drift": {"order": 10, "frame": "Half-sunk in the drift {be} {items}.", "default": True,
                      "cap": 3, "overflow": "a litter of smaller wreckage",
                      "aliases": ["drift", "the drift", "snow", "ground"]},
    },
    "fuselage_top": {
        "the_spine": {"order": 10, "frame": "On the bare aluminium {be} {items}.", "default": True,
                      "cap": 3, "overflow": "a scatter of smaller debris",
                      "aliases": ["spine", "the spine", "aluminium", "roof"]},
    },
}
