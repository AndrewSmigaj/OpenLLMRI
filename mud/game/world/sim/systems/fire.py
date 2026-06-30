"""world.sim.systems.fire — fire state ladder + hazards (§31). Pure. Built in roadmap P5.

Fire as a state machine (unlit → smouldering → small → steady → spreading → dangerous) with smoke,
spread and burn-through hazards. See systems/README.md.
"""
from __future__ import annotations
