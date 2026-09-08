"""`python3 -m world.sim.validation <scenario>` — run the §44 content lint over a scenario's tables."""
from __future__ import annotations

import importlib
import os
import sys

from world.sim.validation.content_lint import validate


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    name = argv[0] if argv else "whiteout"
    if name == "smoketest":
        print("validate: smoketest has no authored tables — nothing to lint.")
        return 0
    base = f"world.scenarios.{name}"
    objects = importlib.import_module(f"{base}.objects").OBJECT_TABLE
    content = importlib.import_module(f"{base}.content")
    try:
        probes = importlib.import_module(f"{base}.probes").PROBES
    except ModuleNotFoundError:
        probes = []
    sim_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors, warnings = validate(objects, content.MATERIAL_TABLE, content.ZONE_TABLE, content.SPACE_TABLE,
                                content.APPEARANCE, content.RESPONSES, probes, sim_root=sim_root)
    for w in warnings:
        print(f"  warn: {w}")
    for e in errors:
        print(f"  ERROR: {e}")
    print(f"validate {name}: {len(objects)} objects, {len(content.MATERIAL_TABLE)} materials, "
          f"{len(content.ZONE_TABLE)} zones, {len(probes)} probes — {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
