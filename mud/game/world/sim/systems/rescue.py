"""world.sim.systems.rescue — additive-confidence rescue + the radio FSM (DR-16, §37-39). Pure.

confidence = Σ weight·value, capped at 1; rescued = weather_window AND confidence ≥ threshold;
monotonic & always-reachable. Channels (beacon/radio/landmark/visual/smoke/stay) draw on DISTINCT
scarce resources so route choice is real and total warmth failure doesn't kill every route. The radio
is an authored FSM packet (dead → powered_static → weak_receive → weak_transmit → two_way_no_location →
useful_contact). Built in roadmap P5.
"""
from __future__ import annotations


def confidence(channels: dict) -> float:
    """Additive, capped rescue confidence from the per-channel 0..1 values. Implemented in roadmap
    P5."""
    raise NotImplementedError("systems.rescue.confidence — roadmap P5")
