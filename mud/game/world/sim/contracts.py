"""world.sim.contracts — the FROZEN backbone dataclasses every sim module + the shell speak.

This is the contract between the pure functional core (world/sim/**, no Evennia) and the Evennia
imperative shell. **STATUS: design-frozen (P0).** Changing a field here ripples through the whole
engine — treat edits as a contract change (note it in the roadmap), not a casual tweak.

Hard rules (enforced by lints; see tools/ and .claude/agents/engine-reviewer.md):
  * Pure: stdlib only. No evennia/django imports anywhere under world/sim/**.
  * Deterministic (DR-12): no dbid/uuid/datetime/wall-clock values in EntityState — they leak
    nondeterminism into snapshots. Ids in the pure layer are seeded logical ids.
  * Conservation (DR-11): conserved quantities are REAL integers (grams). Ordinals are intensive
    properties only (gates and rank-relations), never summed.

References are to the GDD §-anchors and the architecture decisions register (DR-NN).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# Materials & objects (DR-04, DR-06)
# ---------------------------------------------------------------------------

# Intensive ordinal scale (DR-04). Authoring uses the words; the baked table stores the numbers.
ORDINAL: dict[str, float] = {
    "none": 0.0, "very_low": 0.15, "low": 0.3, "med": 0.5,
    "high": 0.7, "very_high": 0.85, "extreme": 1.0,
}


@dataclass(frozen=True)
class Material:
    """An ordinal property vector (DR-04). `props` are INTENSIVE (cut/tear/bend resistance,
    burnability, insulation, conductivity…) in [0, 1] — used only as gates and rank-relations,
    never summed. Mass is NOT here; it is an extensive quantity carried by EntityState/Part."""
    id: str
    props: dict[str, float] = field(default_factory=dict)   # baked: ordinals already → numbers
    tags: tuple[str, ...] = ()


@dataclass
class Part:
    """A removable part of an object (DR-06). Carries its own mass (integer grams) so the ledger
    balances a removal, and what it becomes when detached (`outputs_when_removed`)."""
    id: str
    material: str
    mass_g: int                                  # extensive, integer grams
    attachment: str = "fixed"                    # fixed | bolted | stitched | tied | wedged | ...
    outputs_when_removed: tuple[str, ...] = ()   # derived-object template ids


@dataclass
class EntityState:
    """The snapshot the pure core sees (mirrors an Evennia Object). Built per resolution from
    Attributes and discarded after Effects apply. Logical ids only — never a dbid/uuid (DR-12)."""
    id: str
    name: str
    materials: list[str] = field(default_factory=list)
    parts: list[Part] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    mass_g: int = 0                              # extensive, integer grams (DR-11)
    state: dict = field(default_factory=dict)    # temperature_c, wetness, contamination{}, damage, ...
    provenance: list[str] = field(default_factory=list)   # §24: where it came from
    owner: Optional[str] = None


# ---------------------------------------------------------------------------
# Operations (DR-05): ONE interface. Common stateless cases are the declarative
# schema below (run by operations/interpreter); stateful ones (radio FSM, the
# systems/*) are plain Python behind the same interface and register identically.
# Predicate/Modifier/EffectSpec form a small, CLOSED expression language so that
# all authored/generated content is bounded and checkable.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Predicate:
    """One node of the closed precondition language (compare a property, check a tag, require a
    tool quality…), evaluated deterministically over EntityState/Material/zone."""
    kind: str                # "prop_ge" | "has_tag" | "tool_quality_ge" | "reachable" | ...
    args: tuple = ()


@dataclass(frozen=True)
class Modifier:
    """A qualitative outcome modifier (harder if frozen; slower if cold_hands)."""
    kind: str
    args: tuple = ()


@dataclass(frozen=True)
class EffectSpec:
    """A declarative description of an effect the operation produces (separate→outputs,
    conserve(...)); compiled to concrete Effects against a given attempt + world."""
    kind: str
    args: tuple = ()


@dataclass(frozen=True)
class DurationSpec:
    """How long the operation takes: f(resistance, tool, modifiers) -> minutes (declarative)."""
    base_minutes: int = 0
    args: tuple = ()


@dataclass(frozen=True)
class PartialSpec:
    """What 'progress without completion' yields when the actor's budget < required."""
    keeps_progress: bool = True


@dataclass(frozen=True)
class FailureSpec:
    """Which authored redirect/explanation to emit when a precondition fails."""
    redirect_id: Optional[str] = None


@dataclass(frozen=True)
class Operation:
    """A unit of behavior registered behind one interface (DR-05). The declarative form below is
    what lets most "add a verb" be a data edit. BUILD ORDER: write the first 2-3 operations as
    plain Python functions FIRST; extract the interpreter only once repetition is undeniable."""
    id: str                                      # "cut"
    verbs: tuple[str, ...]                        # synonyms feed the parser: cut, saw, slice
    roles: tuple[str, ...] = ("actor", "target")  # ("actor","target","tool?")
    relations: tuple[str, ...] = ()              # relations this op accepts (off, against, between…)
    preconditions: tuple[Predicate, ...] = ()
    modifiers: tuple[Modifier, ...] = ()
    effects: tuple[EffectSpec, ...] = ()
    duration: DurationSpec = field(default_factory=DurationSpec)
    partial: PartialSpec = field(default_factory=PartialSpec)
    failure: FailureSpec = field(default_factory=FailureSpec)
    priority: int = 0                            # tie-break for specificity dispatch (DR-05)


# ---------------------------------------------------------------------------
# The taught grammar: VERB X [RELATION Y] [WITH Z]   (DR-08 / GDD §25a)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NounRef:
    """A resolved reference to a reachable entity or one of its parts ("the cover OF the seat")."""
    entity_id: str
    part_id: Optional[str] = None


@dataclass(frozen=True)
class ActionAttempt:
    """The parsed, structured action (DR-08). The RELATION slot + Y make two-object actions
    (cut…off…, wedge…against…, tie…between…) FIRST-CLASS. `Y` is a tuple so `between` can carry a
    pair. `verb` is the canonical operation id (post-synonym)."""
    actor: str
    verb: str
    X: Optional[NounRef] = None                  # primary target (a thing or a part)
    relation: Optional[str] = None               # off | onto | against | between | into | from | ...
    Y: Optional[tuple[NounRef, ...]] = None       # secondary object(s); a pair for `between`
    tool: Optional[NounRef] = None               # WITH Z
    raw: str = ""                                # the original typed line (wall-sensor / trace)


@dataclass(frozen=True)
class ParseError:
    """Returned by parse() when input doesn't fit the taught grammar — carries a help nudge that
    teaches the format, never a hard 'you can't do that'."""
    reason: str
    nudge: str = ""


# --- Parser I/O additions (contract change, P1.5 — additive; no existing field changed) ---

@dataclass(frozen=True)
class Reachable:
    """A parser-input descriptor: everything the parser needs to MATCH a typed noun to an entity/part.
    The shell builds one per reachable entity (from EntityState + the Evennia object's aliases), so the
    frozen EntityState stays lean while the parser gets aliases/ident/part-labels."""
    id: str
    name: str
    aliases: tuple[str, ...] = ()
    ident: str = ""                                # short player designator, e.g. "11B"
    parts: tuple[tuple[str, str], ...] = ()         # (part_id, part_label) pairs


@dataclass(frozen=True)
class DisambigOption:
    """One option in a Disambiguation."""
    label: str      # human-readable, e.g. "aircraft seat 11B's cover"
    ref: str        # the token the player re-issues to pick it, e.g. "11b cover"
    # (contract change, slice-fix — ADDITIVE; defaults preserve the prior shape.) The concrete
    # identity behind the option, so the shell's numbered menu binds a pick by entity — immune to
    # reordering, and identical objects (three "glass shard"s) stay distinguishable.
    entity_id: str = ""             # the Reachable.id this option denotes
    part_id: Optional[str] = None   # set when the ambiguity is over parts


@dataclass(frozen=True)
class Disambiguation:
    """Returned by parse() when a noun matches multiple things (user refinement). The shell prints a
    NUMBERED menu; the player's number re-runs the WHOLE original line via parse(..., bindings={term:
    (entity_id, part_id)}) — so RELATION/Y/WITH survive the pick by construction. (Distinctly-named
    options can still be re-issued by `ref`.)"""
    term: str
    options: tuple[DisambigOption, ...]


# ---------------------------------------------------------------------------
# Effects & Events (DR-10)
# ---------------------------------------------------------------------------

class EffectKind(str, Enum):
    SET_ATTR = "set_attr"
    ADJUST_ATTR = "adjust_attr"
    CREATE_OBJECT = "create_object"
    REMOVE_PART = "remove_part"
    CONSUME = "consume"
    MOVE_ZONE = "move_zone"
    SET_OWNER = "set_owner"


@dataclass(frozen=True)
class Effect:
    """The ONLY state-mutation instruction. The shell's apply() is the single ENFORCED writer
    (atomic via transaction.atomic, ledger-gated, Attribute + Tag mirror together). No state changes
    any other way — a lint forbids raw obj.db.x= / .attributes.add / .tags.add elsewhere (DR-10)."""
    kind: EffectKind
    target_id: str
    args: dict = field(default_factory=dict)


class EventKind(str, Enum):
    SPEECH = "speech"
    IMPACT = "impact"
    ACTIVITY_TICK = "activity_tick"
    FIRE_STATE_CHANGE = "fire_state_change"
    SURVIVOR_WORSENS = "survivor_worsens"
    WEATHER_CHANGE = "weather_change"
    SCRIPTED_TRIGGER = "scripted_trigger"
    RESCUE_SIGNAL = "rescue_signal"
    DANGER = "danger"
    PLAYER_STOP_REQUEST = "player_stop_request"


@dataclass(frozen=True)
class Event:
    """A perceivable happening, routed to observers by perception band × loudness (DR-13). A subset
    are events.INTERRUPT_SIGNALS that break a pending activity (DR-14) — the running clock itself
    never stops; only the actor's current activity is interrupted."""
    kind: EventKind
    source_id: str
    loudness: float = 0.0
    data: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Resolution outputs (DR-09, DR-11)
# ---------------------------------------------------------------------------

class Resolution(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    REDIRECT = "redirect"            # informative "can't do X here; you could cut/burn/pry…"


@dataclass(frozen=True)
class ActionResult:
    """What resolve() returns (pure). The shell applies effects (ledger-gated) and prints narration.
    EVERY parsed action returns one of these — never a hard refusal (DR-09)."""
    resolution: Resolution
    narration: str = ""
    effects: tuple[Effect, ...] = ()
    events: tuple[Event, ...] = ()
    duration_minutes: int = 0
    partial: bool = False
    tier: str = ""                   # which tier fired, for the decision trace (DR-20)


@dataclass(frozen=True)
class LedgerVerdict:
    """The conservation ledger's pre-commit verdict (DR-11). `ok=False` is a BUG (unphysical
    authored content), not a player failure — it is logged and fails the build."""
    ok: bool
    reason: str = ""
    sink_delta: dict = field(default_factory=dict)   # per-channel mass/energy to the environment sink


# ---------------------------------------------------------------------------
# The read boundary (DR-01): the shell builds this from Evennia once per action;
# the pure core only reads through it and never touches Evennia objects.
# ---------------------------------------------------------------------------

@runtime_checkable
class WorldView(Protocol):
    """Read-only access to EntityStates by id + reachability/zone queries, built by the shell from
    Attributes/Tags/contents per action. `seed_state` carries the per-run seeded RNG (DR-12) so the
    pure core never touches `random`/`time`."""
    seed_state: int

    def get(self, entity_id: str) -> "Optional[EntityState]": ...
    def reachable(self, actor_id: str) -> list[str]: ...
    def in_zone(self, zone: str) -> list[str]: ...


# ---------------------------------------------------------------------------
# Build-time authoring packets (§43; DR-17). Used by tools/ at build time and
# baked to runtime data — NEVER consulted by an LLM at runtime.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ObjectPacket:
    """Authoring packet for a puzzle-critical object (radio/beacon/pilot/showcase seat): a small
    state machine + clue/solution paths. Cheap objects don't need one (DR-06)."""
    id: str
    materials: tuple[str, ...] = ()
    parts: tuple[Part, ...] = ()
    state: dict = field(default_factory=dict)
    clue_paths: tuple[str, ...] = ()         # ≥3 for critical facts (§44)
    solution_paths: tuple[str, ...] = ()     # ≥3 for critical goals (§44)


@dataclass(frozen=True)
class OperationPacket:
    """Authoring packet for an operation/action-family (the §43 'ActionFamilyPacket')."""
    operation: Operation
    responses: dict = field(default_factory=dict)   # success/partial/failure template ids


@dataclass(frozen=True)
class WorkflowPacket:
    """A multi-step authored workflow (e.g. the radio-repair sequence)."""
    id: str
    steps: tuple[str, ...] = ()
