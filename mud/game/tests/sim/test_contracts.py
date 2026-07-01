"""Tier-1 contract tests — enforce the FROZEN contracts + the functional-core boundary (P0).

These run with NO Django/Evennia (the functional-core boundary). They lock the contract surface so a
later change is a deliberate, visible edit — and prove the pure core imports without the framework.
"""
import importlib
import sys

import pytest


def test_pure_core_imports_without_evennia_or_django():
    for m in ["contracts", "materials", "effects", "events", "narrator",
              "conservation.ledger", "parser.grammar", "operations.interpreter",
              "resolver.tiers", "resolver.index", "space.perception",
              "systems.clock", "systems.scheduler", "systems.rescue",
              "validation.content_lint"]:
        importlib.import_module("world.sim." + m)
    leaked = [m for m in sys.modules if m.split(".")[0] in ("evennia", "django")]
    assert not leaked, f"functional core pulled in {leaked}"


def test_contract_surface_present():
    from world.sim.contracts import (  # noqa: F401
        Material, Part, EntityState, Operation, Predicate, Modifier, EffectSpec,
        ActionAttempt, NounRef, ParseError, Effect, EffectKind, Event, EventKind,
        ActionResult, Resolution, LedgerVerdict, WorldView, ObjectPacket, ORDINAL,
    )
    # the ordinal scale is the 7-level none..extreme, monotonic in [0, 1]
    vals = list(ORDINAL.values())
    assert len(ORDINAL) == 7
    assert vals == sorted(vals)
    assert vals[0] == 0.0 and vals[-1] == 1.0
    # the taught-grammar shape: actor + verb + X + relation + Y + tool + raw
    fields = ActionAttempt.__dataclass_fields__
    for slot in ("actor", "verb", "X", "relation", "Y", "tool", "raw"):
        assert slot in fields, f"ActionAttempt missing {slot!r}"


def test_interrupt_signals_subset_of_event_kinds():
    from world.sim.contracts import EventKind
    from world.sim.events import INTERRUPT_SIGNALS
    assert INTERRUPT_SIGNALS <= set(EventKind)
    assert EventKind.DANGER in INTERRUPT_SIGNALS


def test_key_signatures_are_stubs_until_implemented():
    # parse (P1.5) and resolve (P1.4) are still stubs; check() is implemented (P1.3), narrator/materials/
    # effects/operations are implemented — this guards the *remaining* unimplemented seams.
    from world.sim.parser import parse
    from world.sim.resolver import resolve
    for fn, args in [(parse, ("x", None, None)), (resolve, (None, None))]:
        with pytest.raises(NotImplementedError):
            fn(*args)
