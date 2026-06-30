"""Whiteout — the hand-curated material table (the quality anchor, DR-04).

Ordinal words: none < very_low < low < med < high < very_high < extreme (mapped to numbers at load
via `world.sim.materials.load_materials`). Props are INTENSIVE (gates / rank-relations), never summed;
mass is per-part/object (extensive), authored on the objects, not here.

**This is world-building content — tune freely.** The starter set below covers the P1 slice objects
(aircraft_seat, multitool, fire-makings, water/snow); the remaining materials (cardboard, paper, wool,
cotton_cloth, bone, flesh, ash, smoke, insulation_batting, fuel-soaked_rag, …) are added as their
objects are authored, toward the ~25-material target.
"""

MATERIAL_TABLE = {
    "synthetic_fabric": {  # the seat cover
        "props": {"cut_resistance": "low", "tear_resistance": "low", "bend_resistance": "very_low",
                  "burnability": "high", "ignition_difficulty": "low", "smoke_toxicity": "high",
                  "insulation": "med", "absorbency": "med"},
        "tags": ("flexible", "flammable", "fabric"),
    },
    "foam": {  # the seat cushion
        "props": {"cut_resistance": "very_low", "tear_resistance": "very_low", "burnability": "very_high",
                  "ignition_difficulty": "low", "smoke_toxicity": "very_high", "insulation": "high",
                  "rigidity": "very_low", "absorbency": "high"},
        "tags": ("soft", "flammable", "insulating"),
    },
    "nylon_webbing": {  # the seatbelt
        "props": {"cut_resistance": "med", "tear_resistance": "high", "bend_resistance": "low",
                  "burnability": "med", "ignition_difficulty": "med", "insulation": "low"},
        "tags": ("strong", "flexible", "cordage"),
    },
    "steel": {  # frame, bolts, multitool blade
        "props": {"cut_resistance": "extreme", "tear_resistance": "extreme", "bend_resistance": "very_high",
                  "burnability": "none", "conductivity": "high", "rigidity": "very_high"},
        "tags": ("metal", "rigid", "conductive"),
    },
    "aluminum": {
        "props": {"cut_resistance": "high", "bend_resistance": "med", "burnability": "none",
                  "conductivity": "high", "rigidity": "high"},
        "tags": ("metal", "conductive"),
    },
    "plastic": {
        "props": {"cut_resistance": "med", "bend_resistance": "low", "burnability": "med",
                  "ignition_difficulty": "med", "smoke_toxicity": "high", "rigidity": "med"},
        "tags": ("synthetic",),
    },
    "rubber": {
        "props": {"cut_resistance": "med", "bend_resistance": "very_low", "burnability": "med",
                  "smoke_toxicity": "high", "insulation": "high", "conductivity": "none"},
        "tags": ("flexible", "insulating"),
    },
    "wood": {
        "props": {"cut_resistance": "med", "bend_resistance": "med", "burnability": "high",
                  "ignition_difficulty": "med", "insulation": "med", "rigidity": "high"},
        "tags": ("natural", "flammable", "fuel"),
    },
    "dry_grass": {  # tinder
        "props": {"cut_resistance": "very_low", "burnability": "extreme", "ignition_difficulty": "very_low",
                  "smoke_toxicity": "low"},
        "tags": ("tinder", "flammable", "fuel"),
    },
    "copper_wire": {
        "props": {"cut_resistance": "med", "bend_resistance": "very_low", "conductivity": "extreme",
                  "rigidity": "low"},
        "tags": ("metal", "conductive", "wire"),
    },
    "glass": {
        "props": {"cut_resistance": "high", "bend_resistance": "extreme", "burnability": "none",
                  "rigidity": "high"},
        "tags": ("brittle", "rigid"),
    },
    "leather": {
        "props": {"cut_resistance": "med", "tear_resistance": "med", "burnability": "low",
                  "insulation": "med"},
        "tags": ("flexible", "fabric"),
    },
    "snow": {
        "props": {"insulation": "med", "potability": "med", "edibility": "low"},
        "tags": ("frozen_water", "cold"),
    },
    "ice": {
        "props": {"cut_resistance": "low", "rigidity": "high", "potability": "med"},
        "tags": ("frozen_water", "cold", "brittle"),
    },
    "water": {
        "props": {"potability": "high", "absorbency": "none"},
        "tags": ("liquid", "extinguisher"),
    },
}
