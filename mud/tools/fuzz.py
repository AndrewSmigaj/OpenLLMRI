#!/usr/bin/env python3
"""fuzz — the solvability-fuzz harness (DR-18). Roadmap P2.

Drives the ScriptedBrain (greedy / reckless / random-within-affordances) over seeded runs and checks:
every attempt resolves, 0 conservation violations, rescue reachable from every sampled state. Its
wall-sensor output (attempts hitting the generic redirect) is the prioritized build-time authoring queue.
"""
import sys

print("fuzz: not built yet (roadmap P2).")
print("  It will drive the ScriptedBrain over seeded runs and assert: 0 unresolved attempts, 0 "
      "conservation violations, rescue reachable; wall-sensor → the authoring queue.")
print("  See docs/scenarios/whiteout/roadmap.md (P2) and .claude/skills/solvability-fuzz/.")
sys.exit(0)
