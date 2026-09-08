"""Tier-1: the probe corpus (DR-18a) — every `status: pass` probe passes on the pure core, and the
passing count never drops below the committed BASELINE (the ratchet)."""
from world.scenarios.whiteout import content, probes as probes_pkg
from world.scenarios.whiteout.authored import AUTHORED
from world.scenarios.whiteout.objects import OBJECT_TABLE
from world.sim.testing.probes import run_all, run_probe, summarize

MATS = content.load()


def test_every_pass_probe_passes():
    failing = []
    for p in probes_pkg.PROBES:
        if p.get("status") != "pass":
            continue
        r = run_probe(p, OBJECT_TABLE, MATS, AUTHORED)
        if not r.passed:
            failing.append(f"{p['id']}: {r.reason}")
    assert not failing, "\n".join(failing)


def test_passing_count_never_drops_below_baseline():
    s = summarize(run_all(probes_pkg.PROBES, OBJECT_TABLE, MATS, AUTHORED))
    assert s["passing"] >= probes_pkg.baseline(), s


def test_every_probe_cites_a_source_and_has_a_status():
    for p in probes_pkg.PROBES:
        assert p.get("source"), p["id"]
        assert p.get("status") in ("pass", "todo"), p["id"]
        assert p.get("steps"), p["id"]
