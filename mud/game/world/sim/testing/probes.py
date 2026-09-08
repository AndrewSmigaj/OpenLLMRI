"""world.sim.testing.probes — the probe runner (DR-18a). Pure.

A **probe** is one typed command chain in one zone with an expected outcome class:
    {"id": "...", "zone": "mid_cabin", "holds": ["bottle"],
     "steps": ["break bottle", "take shard", "cut cover off seat with shard"],
     "expect": "SUCCESS" | "REDIRECT" | "PARTIAL", "tier_prefix": "op:cut" (optional),
     "status": "pass" | "todo", "source": "rooms/cockpit.md §5 item 4"}
It runs the REAL parser on the typed lines against a `PureWorld` loaded from the scenario's
OBJECT_TABLE, resolves through the real tiers (with the scenario's AUTHORED rules), applies effects
through the in-memory writer, and compares the LAST step's resolution (and tier prefix) to `expect`.
A disambiguation mid-chain takes the first option unless the step names a pick as `line => n`.
`status: pass` probes are CI-enforced; `todo` probes are the work queue; the passing count is the
sufficiency score and may never drop below the committed BASELINE (the ratchet).
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

from world.sim.contracts import Disambiguation, ParseError, Resolution
from world.sim.operations.registry import VERB_TO_OP
from world.sim.parser import parse
from world.sim.resolver import resolve
from world.sim.testing.pure_world import LedgerError, PureWorld

OUTCOMES = {"SUCCESS": Resolution.SUCCESS, "REDIRECT": Resolution.REDIRECT, "PARTIAL": Resolution.PARTIAL}


@dataclass
class StepResult:
    line: str
    kind: str                 # "ok" | "parse_error" | "disambiguation" | "ledger_error"
    tier: str = ""
    resolution: str = ""
    narration: str = ""


@dataclass
class ProbeResult:
    probe: dict
    passed: bool
    reason: str = ""
    steps: list = field(default_factory=list)


def _pick(step: str):
    """`take shard => 2` names the menu option to take on a disambiguation; default the first."""
    if "=>" in step:
        line, n = step.rsplit("=>", 1)
        return line.strip(), max(1, int(n.strip()))
    return step, 1


def run_step(world: PureWorld, materials, line: str, authored=None, pick: int = 1) -> StepResult:
    bindings = None
    for _ in range(3):                                   # a pick may itself re-ambiguate; bound the loop
        res = parse(line, VERB_TO_OP, world.reachables(), bindings=bindings)
        if isinstance(res, ParseError):
            return StepResult(line, "parse_error", narration=res.nudge)
        if isinstance(res, Disambiguation):
            opt = res.options[min(pick, len(res.options)) - 1]
            bindings = dict(bindings or {})
            bindings[res.term] = (opt.entity_id, opt.part_id)
            continue
        attempt = replace(res, actor=world.actor_id)
        action = resolve(attempt, world, materials, authored=authored)
        if action.effects:
            try:
                world.apply(action.effects)
            except LedgerError as err:
                return StepResult(line, "ledger_error", tier=action.tier, narration=str(err))
        return StepResult(line, "ok", tier=action.tier, resolution=action.resolution.value,
                          narration=action.narration)
    return StepResult(line, "disambiguation", narration="could not settle a disambiguation")


def run_probe(probe: dict, rows, materials, authored=None, default_zone="mid_cabin") -> ProbeResult:
    world = PureWorld.from_table(rows, actor_zone=probe.get("zone"), default_zone=default_zone)
    for held in probe.get("holds", ()):
        try:
            world.give(held)
        except KeyError:
            return ProbeResult(probe, False, f"holds: unknown object {held!r}")
    steps = []
    for step in probe.get("steps", ()):
        line, pick = _pick(step)
        sr = run_step(world, materials, line, authored=authored, pick=pick)
        steps.append(sr)
        if sr.kind != "ok":
            return ProbeResult(probe, False, f"{sr.kind} at {line!r}: {sr.narration}", steps)
    if not steps:
        return ProbeResult(probe, False, "no steps", steps)
    last = steps[-1]
    want = OUTCOMES.get(str(probe.get("expect", "SUCCESS")).upper())
    if want is None:
        return ProbeResult(probe, False, f"bad expect {probe.get('expect')!r}", steps)
    if last.resolution != want.value:
        return ProbeResult(probe, False, f"expected {want.value}, got {last.resolution} ({last.tier}): "
                                          f"{last.narration}", steps)
    prefix = probe.get("tier_prefix")
    if prefix and not last.tier.startswith(prefix):
        return ProbeResult(probe, False, f"expected tier {prefix}*, got {last.tier}", steps)
    return ProbeResult(probe, True, "", steps)


def run_all(probes, rows, materials, authored=None, default_zone="mid_cabin") -> list:
    return [run_probe(p, rows, materials, authored, default_zone) for p in probes]


def summarize(results) -> dict:
    """Counts: pass-status probes passing/failing, todo probes passing (promotable) / failing."""
    out = {"pass_ok": 0, "pass_fail": 0, "todo_ok": 0, "todo_fail": 0}
    for r in results:
        st = r.probe.get("status", "todo")
        key = ("pass" if st == "pass" else "todo") + ("_ok" if r.passed else "_fail")
        out[key] += 1
    out["passing"] = out["pass_ok"] + out["todo_ok"]
    out["total"] = len(results)
    return out
