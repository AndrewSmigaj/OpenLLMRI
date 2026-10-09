"""Analyst tests (DESIGN.md E8): analysts are tested before they are trusted, and again whenever
their prompts or model change. Three kinds, at one layer of a real lens:

- decoys: populations with no real pattern (random samples of the layer's items, the whole lens
  with its items' designed values shuffled, and that lens's pipes and hubs worked out again); a
  sound analyst doesn't call a pattern clear;
- planted findings: populations built around one label value (it makes up 70% of the items, the
  rest are random), and a pipeline whose members are planted the same way, around a value no
  real pipeline leans to; a sound analyst names it;
- predictive descriptions, after RouterInterp: from a real node's card, a second call picks the
  node's members out of held-out sentences (half are members), scored beside a simple baseline
  that picks the sentences carrying the node's majority label.

A run is kept in `<lake>/_analysts/tests/<job id>.json` with its model and prompt version; cards
written by a matching analyst show as tested.
"""

from __future__ import annotations

import dataclasses
import time
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from services.llm.cards import Budget, best_layer, tests_root, write_card, write_json
from services.llm.packets import (
    LensEvidence,
    example_indices,
    lens_packet,
    load_evidence,
    node_packet,
    population_packet,
    routes_packet,
)
from services.llm.prompts import PICK_SCHEMA, PROMPT_VERSION, pick_prompt
from services.llm.runner import ClaudeRunner, Runner

Array = np.ndarray[Any, Any]

DECOYS, PLANTED, PREDICTED = 2, 3, 3  # random decoys (plus the shuffled lens), planted values, nodes
PLANTED_SHARE = 0.7
HELD_OUT = 10  # held-out members, and as many others, per predicted node
PREDICT_PASS = 0.7  # mean accuracy the descriptions must reach (half the sentences are members)
DEFAULT_TEST_BUDGET = 28


def shuffled(ev: LensEvidence, rng: np.random.Generator) -> LensEvidence:
    """The lens with its items' designed values (the label and categories together) shuffled
    across items, and nothing worked out for it: a decoy lens."""
    from services.lenses.flows import value_of

    view = ev.view
    order = rng.permutation(len(view.items))
    items = [{**item, "label": view.items[int(j)].get("label"), "categories": view.items[int(j)].get("categories", {})}
             for item, j in zip(view.items, order)]
    base = {axis: dict(Counter(v for item in items if (v := value_of(item, axis)) is not None)) for axis in ev.axes}
    manifest = {key: value for key, value in ev.manifest.items() if key != "self_check"}
    return dataclasses.replace(ev, view=dataclasses.replace(view, items=items), base=base, manifest=manifest,
                               details=None, validation=None, marks=None)


def _mask(n: int, picked: Any) -> Array:
    mask = np.zeros(n, dtype=bool)
    mask[np.asarray(picked, dtype=int)] = True
    return mask


def decoy_packets(ev: LensEvidence, li: int, rng: np.random.Generator, size: int) -> List[Dict[str, Any]]:
    """Random samples of the layer's items, named like nodes, then the shuffled lens."""
    view, n = ev.view, len(ev.view.items)
    k = int(view.nodes[:, li].max()) + 1
    found = [population_packet(ev, li, _mask(n, rng.choice(n, size, replace=False)),
                               f"L{view.layers[li]}C{k + i}").as_dict() for i in range(DECOYS)]
    fake = shuffled(ev, rng)
    found.append(lens_packet(fake).as_dict())
    if ev.routes:  # the shuffled lens's pipes and hubs: the same routing, values that no longer go with it
        from services.lenses.routes import compute_routes

        found.append(routes_packet(dataclasses.replace(fake, routes=compute_routes(fake.view))).as_dict())
    return found


def planted_packets(ev: LensEvidence, li: int, rng: np.random.Generator, size: int) -> List[Tuple[str, Dict[str, Any]]]:
    """For the commonest label values: a population where the value makes up most of the items."""
    view, n = ev.view, len(ev.view.items)
    labels = np.array([str(item.get("label")) for item in view.items])
    k = int(view.nodes[:, li].max()) + 1 + DECOYS
    found = []
    for i, (value, _) in enumerate(Counter(labels.tolist()).most_common(PLANTED)):
        have, rest = np.flatnonzero(labels == value), np.flatnonzero(labels != value)
        take = min(int(round(PLANTED_SHARE * size)), len(have))
        picked = np.concatenate([rng.choice(have, take, replace=False),
                                 rng.choice(rest, min(size - take, len(rest)), replace=False)])
        found.append((value, population_packet(ev, li, _mask(n, picked), f"L{view.layers[li]}C{k + i}").as_dict()))
    planted = planted_routes(ev, rng)
    return found + ([planted] if planted else [])


def planted_routes(ev: LensEvidence, rng: np.random.Generator) -> Optional[Tuple[str, Dict[str, Any]]]:
    """The lens's routes with its first pipeline's members replaced by a planted group, around the
    label value that real pipelines lean to least, so naming it can only come from the plant."""
    import copy

    real = ev.routes
    if not real or not real["pipelines"]:
        return None
    view = ev.view
    labels = np.array([str(item.get("label")) for item in view.items])
    ids = np.array([item["probe_id"] for item in view.items])

    def lean(value: str) -> float:
        shares = [float(np.mean(labels[np.isin(ids, p["member_ids"])] == value)) for p in real["pipelines"][1:]]
        return max(shares, default=0.0)

    value = min(sorted(set(labels.tolist())), key=lean)
    routes = copy.deepcopy(real)
    size = max(len(routes["pipelines"][0]["member_ids"]) // 2, 20)
    have, rest = np.flatnonzero(labels == value), np.flatnonzero(labels != value)
    take = min(int(round(PLANTED_SHARE * size)), len(have))
    picked = np.concatenate([rng.choice(have, take, replace=False), rng.choice(rest, min(size - take, len(rest)), replace=False)])
    routes["pipelines"][0]["member_ids"] = ids[picked].tolist()
    return value, routes_packet(dataclasses.replace(ev, routes=routes)).as_dict()


def predict(runner: Runner, ev: LensEvidence, li: int, node: int, rng: np.random.Generator,
            budget: Budget) -> Dict[str, Any]:
    """One node's card, then a second call picks its members out of held-out sentences."""
    view, layer = ev.view, ev.view.layers[li]
    name, mask = f"L{layer}C{node}", view.nodes[:, li] == node
    card = write_card(runner, node_packet(ev, layer, node).as_dict(), budget)
    if card is None or card["output"] is None:
        return {"node": name, "error": card["error"] if card else "out of budget"}
    shown = set(example_indices(ev, mask, name))
    members = [i for i in np.flatnonzero(mask).tolist() if i not in shown]
    others = np.flatnonzero(~mask).tolist()
    m = min(HELD_OUT, len(members), len(others))
    chosen = [int(i) for i in rng.permutation(np.concatenate([rng.choice(members, m, replace=False),
                                                               rng.choice(others, m, replace=False)]))]
    truth = [bool(mask[i]) for i in chosen]
    labels = [str(item.get("label")) for item in view.items]
    majority = Counter(labels[i] for i in np.flatnonzero(mask)).most_common(1)[0][0]
    baseline = float(np.mean([(labels[i] == majority) == t for i, t in zip(chosen, truth)]))
    result: Dict[str, Any] = {"node": name, "title": card["output"]["title"], "sentences": len(chosen),
                              "baseline": round(baseline, 3), "accuracy": None, "error": None}
    if not budget.take():
        return {**result, "error": "out of budget"}
    sentences = [" ".join(str(view.items[i].get("input_text") or "").split()) for i in chosen]
    run = runner.run(pick_prompt(card["output"]["title"], card["output"]["summary"], sentences), PICK_SCHEMA)
    if run.output is None:
        return {**result, "error": run.error}
    picked = {int(x) - 1 for x in run.output.get("members", []) if isinstance(x, int)}
    result["accuracy"] = round(float(np.mean([(j in picked) == t for j, t in enumerate(truth)])), 3)
    return result


def _brief(card: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if card is None:
        return {"error": "out of budget", "pattern": None}
    output = card.get("output") or {}
    return {"subject": card["subject"], "title": output.get("title"), "pattern": output.get("pattern"),
            "summary": output.get("summary"), "numbers_passed": (card.get("check") or {}).get("passed"),
            "error": card.get("error")}


def run_tests(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `analyst_tests` job, at one layer of a lens (its best layer by default)."""
    ev = load_evidence(params["session_id"], params["name"], params.get("version"))
    view = ev.view
    layer = int(params["layer"]) if params.get("layer") is not None else best_layer(ev)
    if layer not in view.layers:
        raise ValueError(f"L{layer} is not in this lens")
    li = view.layers.index(layer)
    rng = np.random.default_rng(int(params.get("seed") or 0))
    runner = ClaudeRunner(model=params.get("model"))
    budget = Budget(int(params.get("budget") or DEFAULT_TEST_BUDGET))
    size = int(np.median(list(Counter(view.nodes[:, li].tolist()).values())))
    steps, models = DECOYS + 1 + PLANTED + PREDICTED + (2 if ev.routes else 0), Counter[str]()
    decoys: List[Dict[str, Any]] = []
    for packet in decoy_packets(ev, li, rng, size):
        ctx.progress("decoys", len(decoys), steps)
        card = write_card(runner, packet, budget)
        models.update([card["model"]] if card else [])
        decoys.append({**_brief(card), "clear": _brief(card)["pattern"] == "clear"})
    planted: List[Dict[str, Any]] = []
    for value, packet in planted_packets(ev, li, rng, size):
        ctx.progress("planted findings", len(decoys) + len(planted), steps)
        card = write_card(runner, packet, budget)
        models.update([card["model"]] if card else [])
        output = (card or {}).get("output") or {}
        said = " ".join([str(output.get("title", "")), str(output.get("summary", "")), *map(str, output.get("points", []))])
        planted.append({**_brief(card), "value": value,
                        "found": bool(output) and value.lower() in said.lower() and output.get("pattern") != "none"})
    predicted: List[Dict[str, Any]] = []
    for node, _ in Counter(view.nodes[:, li].tolist()).most_common(PREDICTED):
        ctx.progress("predictive descriptions", len(decoys) + len(planted) + len(predicted), steps)
        predicted.append(predict(runner, ev, li, int(node), rng, budget))
    return _finish(ev, layer, decoys, planted, predicted, models, budget, ctx)


def _finish(ev: LensEvidence, layer: int, decoys: List[Dict[str, Any]], planted: List[Dict[str, Any]],
            predicted: List[Dict[str, Any]], models: "Counter[str]", budget: Budget, ctx: Any) -> Dict[str, Any]:
    """The pass rule, and the record kept for matching cards to tested analysts."""
    accuracies = [p["accuracy"] for p in predicted if p.get("accuracy") is not None]
    mean = round(float(np.mean(accuracies)), 3) if accuracies else None
    passed = (all(d.get("error") is None and not d["clear"] for d in decoys)
              and all(p["found"] for p in planted)
              and len(accuracies) == len(predicted) and mean is not None and mean >= PREDICT_PASS)
    model = models.most_common(1)[0][0] if models else ""
    record = {"format": 1, "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "job_id": ctx.job_id,
              "model": model, "prompt_version": PROMPT_VERSION, "lens": ev.lens, "layer": layer, "passed": passed,
              "rules": {"decoys": "none called a clear pattern", "planted": "every planted value named",
                        "predictive": f"mean accuracy at least {PREDICT_PASS}"},
              "decoys": decoys, "planted": planted, "predicted": predicted, "mean_accuracy": mean, "calls": budget.used}
    write_json(tests_root() / f"{ctx.job_id}.json", record)  # job ids sort by when they were made
    return {"passed": passed, "model": model, "prompt_version": PROMPT_VERSION, "mean_accuracy": mean,
            "calls": budget.used}


def latest_tests() -> Optional[Dict[str, Any]]:
    """The most recent analyst test run, if any."""
    import json

    runs = sorted(tests_root().glob("*.json"))
    found: Optional[Dict[str, Any]] = json.loads(runs[-1].read_text(encoding="utf-8")) if runs else None
    return found
