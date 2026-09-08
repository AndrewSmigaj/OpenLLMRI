"""Whiteout — the player SLOTS (players-and-kit.md; Andrew 2026-09-07): what each survivor wore, carried
in their pockets, and suffered in the crash. A slot is authored; the run seed permutes which player gets
which. `outfit(slot)` returns OBJECT_TABLE-style rows to load INTO a character (the loader's parent):
worn items carry `worn_by`; pockets are a container the owner has already searched; the injury is
state on the character (`character_state`). Tunable content. Nothing here is random at runtime.

Wearables declare the DR-25a fields: `covers` (head · torso · arms · hands · legs · feet), `wind`
(0–1, the outer shell stops wind), `waterproof` (0–1); mittens set `fine_work: False`.
"""
from __future__ import annotations

SLOTS: dict = {
    "guide": {
        "label": "the guide", "seat": "right seat", "zone": "cockpit",
        "injury": {"kind": "bruised ribs", "part": "chest", "severity": 2, "bleeding": 0,
                   "note": "bending and lifting hurt; heavy work is slow"},
        "wearing": [
            {"sim_id": "parka", "name": "down parka", "aliases": ["parka", "coat"], "materials": ["nylon_shell", "down"],
             "mass_g": 1600, "state": {"covers": ["torso", "arms", "head"], "wind": 0.9, "waterproof": 0.7}},
            {"sim_id": "baselayer", "name": "wool base layer", "aliases": ["base layer", "thermals", "underlayer"],
             "materials": ["wool"], "mass_g": 400, "state": {"covers": ["torso", "arms", "legs"], "wind": 0.1}},
            {"sim_id": "boots_insulated", "name": "insulated boots", "aliases": ["boots"], "materials": ["rubber", "insulation_batting"],
             "mass_g": 1400, "state": {"covers": ["feet"], "wind": 0.9, "waterproof": 0.9}},
            {"sim_id": "gloves_guide", "name": "leather work gloves", "aliases": ["gloves", "work gloves"], "materials": ["leather"],
             "mass_g": 200, "state": {"covers": ["hands"], "wind": 0.6, "waterproof": 0.4}},
            {"sim_id": "hat_wool", "name": "wool hat", "aliases": ["hat", "beanie"], "materials": ["wool"], "mass_g": 90,
             "state": {"covers": ["head"], "wind": 0.3}},
        ],
        "pockets": [
            {"sim_id": "penknife", "name": "pocketknife", "aliases": ["knife", "penknife"], "materials": ["steel"], "mass_g": 80,
             "state": {"form": "blade", "edge": 0.7, "leverage": 0.15}},
            {"sim_id": "lighter_guide", "name": "brass lighter", "aliases": ["lighter"], "materials": ["steel"], "mass_g": 40,
             "state": {"ignition": True}},
            {"sim_id": "chocolate_guide", "name": "chocolate bar", "aliases": ["chocolate", "bar"], "materials": ["chocolate"], "mass_g": 60},
            {"sim_id": "compass_lanyard", "name": "compass on a lanyard", "aliases": ["compass", "lanyard"], "materials": ["plastic", "nylon_webbing"],
             "mass_g": 40, "state": {"reads": "north"}},
        ],
    },
    "townie": {
        "label": "the townie", "seat": "1A", "zone": "mid_cabin",
        "injury": {"kind": "cut", "part": "forearm", "severity": 2, "bleeding": 2,
                   "note": "a deep cut, bleeding through the sleeve; press it, bind it"},
        "wearing": [
            {"sim_id": "denim_jacket", "name": "denim jacket", "aliases": ["jacket"], "materials": ["denim"], "mass_g": 700,
             "state": {"covers": ["torso", "arms"], "wind": 0.4, "waterproof": 0.1}},
            {"sim_id": "hoodie", "name": "cotton hoodie", "aliases": ["hoodie", "sweatshirt"], "materials": ["cotton_cloth"], "mass_g": 550,
             "state": {"covers": ["torso", "arms", "head"], "wind": 0.2}},
            {"sim_id": "jeans", "name": "jeans", "aliases": ["trousers", "pants"], "materials": ["denim"], "mass_g": 600,
             "state": {"covers": ["legs"], "wind": 0.4}},
            {"sim_id": "sneakers", "name": "sneakers", "aliases": ["shoes", "trainers"], "materials": ["cotton_cloth", "rubber"], "mass_g": 700,
             "state": {"covers": ["feet"], "wind": 0.3, "waterproof": 0.1}},
        ],
        "pockets": [
            {"sim_id": "phone_townie", "name": "phone", "aliases": ["mobile", "cell"], "materials": ["glass", "plastic"], "mass_g": 180,
             "state": {"powered": True, "battery": 60, "light": True, "signal": False}},
            {"sim_id": "wallet", "name": "wallet", "aliases": ["billfold"], "materials": ["leather"], "mass_g": 120,
             "state": {"container": True, "open": True}},
            {"sim_id": "cash", "name": "fold of cash", "aliases": ["cash", "money", "bills"], "materials": ["paper"], "mass_g": 8, "in": "wallet"},
            {"sim_id": "id_card", "name": "driver's licence", "aliases": ["licence", "license", "id", "card"], "materials": ["plastic"], "mass_g": 6, "in": "wallet"},
            {"sim_id": "gum", "name": "pack of gum", "aliases": ["gum"], "materials": ["chocolate"], "mass_g": 20},
            {"sim_id": "keys", "name": "ring of keys", "aliases": ["keys", "key"], "materials": ["steel"], "mass_g": 60, "state": {"form": "piece"}},
            {"sim_id": "earbuds", "name": "earbuds", "aliases": ["headphones", "earphones"], "materials": ["copper_wire", "rubber"], "mass_g": 30,
             "state": {"form": "cord"}},
        ],
    },
    "nurse": {
        "label": "the nurse", "seat": "1B", "zone": "mid_cabin",
        "injury": {"kind": "sprain", "part": "ankle", "severity": 2, "bleeding": 0,
                   "note": "walking costs double; a splint and a stick would halve it"},
        "wearing": [
            {"sim_id": "fleece_jacket", "name": "fleece jacket", "aliases": ["fleece", "jacket"], "materials": ["fleece"], "mass_g": 500,
             "state": {"covers": ["torso", "arms"], "wind": 0.2}},
            {"sim_id": "hiking_boots", "name": "hiking boots", "aliases": ["boots"], "materials": ["leather", "rubber"], "mass_g": 1100,
             "state": {"covers": ["feet"], "wind": 0.7, "waterproof": 0.5}},
            {"sim_id": "scarf", "name": "wool scarf", "aliases": ["scarf"], "materials": ["wool"], "mass_g": 150,
             "state": {"covers": ["head"], "wind": 0.3}},
            {"sim_id": "gloves_thin", "name": "thin gloves", "aliases": ["gloves"], "materials": ["cotton_cloth"], "mass_g": 60,
             "state": {"covers": ["hands"], "wind": 0.2}},
            {"sim_id": "leggings", "name": "leggings", "aliases": ["trousers", "pants"], "materials": ["cotton_cloth"], "mass_g": 250,
             "state": {"covers": ["legs"], "wind": 0.1}},
        ],
        "pockets": [
            {"sim_id": "med_pouch", "name": "medical pouch", "aliases": ["pouch", "med kit", "medkit"], "materials": ["synthetic_fabric"], "mass_g": 120,
             "state": {"container": True, "open": False}},
            {"sim_id": "gauze", "name": "gauze pads", "aliases": ["gauze", "pads"], "materials": ["cotton_cloth"], "mass_g": 40, "in": "med_pouch"},
            {"sim_id": "tape_med", "name": "roll of medical tape", "aliases": ["tape"], "materials": ["plastic"], "mass_g": 30, "in": "med_pouch"},
            {"sim_id": "ibuprofen", "name": "bottle of ibuprofen", "aliases": ["ibuprofen", "pills", "painkillers"], "materials": ["plastic"], "mass_g": 40,
             "in": "med_pouch", "state": {"count": 20}},
            {"sim_id": "suture_kit", "name": "suture kit", "aliases": ["sutures", "needle"], "materials": ["steel", "nylon_webbing"], "mass_g": 30,
             "in": "med_pouch", "state": {"form": "point"}},
            {"sim_id": "lip_balm", "name": "lip balm", "aliases": ["balm", "chapstick"], "materials": ["wax"], "mass_g": 12},
            {"sim_id": "hair_ties", "name": "hair ties", "aliases": ["ties", "elastics"], "materials": ["rubber"], "mass_g": 5,
             "state": {"form": "cord"}},
            {"sim_id": "pen", "name": "ballpoint pen", "aliases": ["pen"], "materials": ["plastic"], "mass_g": 10, "state": {"form": "rod"}},
        ],
    },
    "salesman": {
        "label": "the salesman", "seat": "2A", "zone": "rear_cabin",
        "injury": {"kind": "concussion", "part": "head", "severity": 2, "bleeding": 0,
                   "note": "tires fast; the first day is a fog"},
        "wearing": [
            {"sim_id": "overcoat", "name": "wool overcoat", "aliases": ["overcoat", "coat"], "materials": ["wool"], "mass_g": 1500,
             "state": {"covers": ["torso", "arms", "legs"], "wind": 0.5, "waterproof": 0.2}},
            {"sim_id": "dress_shirt", "name": "dress shirt", "aliases": ["shirt"], "materials": ["cotton_cloth"], "mass_g": 250,
             "state": {"covers": ["torso", "arms"], "wind": 0.1}},
            {"sim_id": "slacks", "name": "wool slacks", "aliases": ["trousers", "pants", "slacks"], "materials": ["wool"], "mass_g": 500,
             "state": {"covers": ["legs"], "wind": 0.3}},
            {"sim_id": "dress_shoes", "name": "dress shoes", "aliases": ["shoes"], "materials": ["leather"], "mass_g": 800,
             "state": {"covers": ["feet"], "wind": 0.5, "waterproof": 0.3, "grip": 0.1}},
            {"sim_id": "gloves_leather", "name": "leather gloves", "aliases": ["gloves"], "materials": ["leather"], "mass_g": 150,
             "state": {"covers": ["hands"], "wind": 0.6, "waterproof": 0.4}},
            {"sim_id": "scarf_silk", "name": "silk scarf", "aliases": ["scarf"], "materials": ["cotton_cloth"], "mass_g": 60,
             "state": {"covers": ["head"], "wind": 0.2}},
        ],
        "pockets": [
            {"sim_id": "lighter_metal", "name": "steel lighter", "aliases": ["lighter"], "materials": ["steel"], "mass_g": 55, "state": {"ignition": True}},
            {"sim_id": "flask", "name": "hip flask", "aliases": ["flask"], "materials": ["steel"], "mass_g": 300,
             "state": {"container": True, "open": False, "form": "vessel"}},
            {"sim_id": "whisky_flask", "name": "whisky", "aliases": ["spirit", "liquor"], "materials": ["alcohol"], "mass_g": 200, "in": "flask"},
            {"sim_id": "reading_glasses", "name": "reading glasses", "aliases": ["glasses", "spectacles", "lens"], "materials": ["glass", "plastic"],
             "mass_g": 30, "state": {"form": "blade", "focus": 0.5}},
            {"sim_id": "notebook", "name": "notebook", "aliases": ["book", "notepad"], "materials": ["paper"], "mass_g": 120},
        ],
    },
    "kid": {
        "label": "the kid", "seat": "2B", "zone": "rear_cabin",
        "injury": {"kind": "shock", "part": "none", "severity": 1, "bleeding": 0,
                   "note": "unhurt and slow to act the first hours"},
        "wearing": [
            {"sim_id": "ski_jacket", "name": "ski jacket", "aliases": ["jacket"], "materials": ["nylon_shell", "fleece"], "mass_g": 1100,
             "state": {"covers": ["torso", "arms", "head"], "wind": 0.9, "waterproof": 0.8}},
            {"sim_id": "snow_pants", "name": "snow pants", "aliases": ["pants", "trousers"], "materials": ["nylon_shell", "fleece"], "mass_g": 800,
             "state": {"covers": ["legs"], "wind": 0.9, "waterproof": 0.8}},
            {"sim_id": "snow_boots", "name": "snow boots", "aliases": ["boots"], "materials": ["rubber", "insulation_batting"], "mass_g": 1300,
             "state": {"covers": ["feet"], "wind": 0.9, "waterproof": 0.9}},
            {"sim_id": "mittens", "name": "ski mittens", "aliases": ["mittens", "mitts"], "materials": ["nylon_shell", "fleece"], "mass_g": 160,
             "state": {"covers": ["hands"], "wind": 0.9, "waterproof": 0.7, "fine_work": False}},
        ],
        "pockets": [
            {"sim_id": "phone_kid", "name": "phone", "aliases": ["mobile", "cell"], "materials": ["glass", "plastic"], "mass_g": 180,
             "state": {"powered": True, "battery": 85, "light": True, "signal": False}},
            {"sim_id": "candy", "name": "candy bar", "aliases": ["candy", "bar"], "materials": ["chocolate"], "mass_g": 55},
            {"sim_id": "multitool_kid", "name": "multitool", "aliases": ["tool", "knife"], "materials": ["steel"], "mass_g": 150,
             "state": {"form": "blade", "edge": 0.8, "leverage": 0.5}},
            {"sim_id": "sunglasses", "name": "sunglasses", "aliases": ["shades", "glasses"], "materials": ["plastic"], "mass_g": 30,
             "state": {"covers": ["eyes"], "shade": 0.8}},
        ],
    },
}


def outfit(slot_id: str) -> list:
    """Rows to load INTO a character (the loader's parent): the worn things (worn_by set at load by
    the caller), a `pockets` container already searched by its owner, and its contents."""
    slot = SLOTS[slot_id]
    rows = []
    for w in slot["wearing"]:
        r = {k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v) for k, v in w.items()}
        r.setdefault("state", {})
        r["state"]["worn"] = True                    # the loader marks worn_by=<character>
        rows.append(r)
    pk = f"pockets_{slot_id}"
    rows.append({"sim_id": pk, "name": "pockets", "aliases": ["pocket", "my pockets"], "materials": ["synthetic_fabric"],
                 "mass_g": 20, "state": {"container": True, "open": True, "searched": True}})
    for it in slot["pockets"]:
        r = {k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v) for k, v in it.items()}
        if "in" not in r:
            r["in"] = pk
        rows.append(r)
    return rows


def character_state(slot_id: str) -> dict:
    """The character's own starting state: the slot, the zone (their seat's), and the injury."""
    slot = SLOTS[slot_id]
    inj = dict(slot["injury"])
    return {"slot": slot_id, "zone": slot["zone"], "wounds": [inj] if inj.get("kind") not in (None, "none") else [],
            "seat": slot["seat"]}
