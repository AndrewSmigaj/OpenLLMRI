"""world.sim.space.perception — separate visibility / audibility / reachability / detail (DR-13).

Each is its own distance/weather/occlusion-aware band (§14). `look` renders perception; reachability
gates manipulation (the resolver only binds reachable nouns). Pure. Built in roadmap P3.
"""
from __future__ import annotations
