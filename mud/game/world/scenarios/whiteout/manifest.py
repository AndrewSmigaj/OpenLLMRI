"""Whiteout scenario manifest — PURE data (importable without Evennia, so `make validate` can lint it).

Packet lists + metadata for the scene. Authored from roadmap P1 on; nothing here yet. See
world/scenarios/whiteout/README.md and the GDD.
"""
from __future__ import annotations

NAME = "whiteout"
MATERIALS: list = []      # the hand-curated material table (~25; the quality anchor)
OPERATIONS: list = []     # OperationPacket list (the ~20 operation categories)
OBJECTS: list = []        # cheap objects + ObjectPacket for the puzzle-critical few
RESPONSES: dict = {}      # narration / redirect template ids → text
# Built incrementally (roadmap P1+). Empty = nothing authored yet.
