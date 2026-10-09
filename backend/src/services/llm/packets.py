"""Evidence packets (DESIGN.md E8): what an analyst reads about one thing in a lens, and nothing
else. A packet holds numbered facts, the only numbers an analyst may cite, and context: example
sentences, tokens, notes. Packets are hashed and stored, so a card names exactly what it was
written from, and Claude Code reads the same packets through the API.

Card ids name what a card is about:
- `lens`: the lens report; `k`: the k advisor;
- `L12C0`: a cluster node; `L12E5r1`: an expert at a rank;
- `L12C0-L13C2`: a route between nodes; `L12E5-L13E7r1`: an expert route at a rank;
- `split-L12C1`: a split point, a node whose items part ways at the next layer;
- `routes`: the lens's expert pipelines, hubs and the experts involved in each designed value.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from services.lenses.store import LensSettings

Array = np.ndarray[Any, Any]

EXAMPLES = 8
TEXT_CHARS = 220


@dataclass
class Packet:
    card_id: str
    kind: str  # lens, k, node, expert, route, expert_route, split
    subject: str
    lens: Dict[str, Any]  # session_id, name, version
    facts: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, List[str]] = field(default_factory=dict)  # section title -> lines

    def fact(self, what: str, value: Any) -> Optional[str]:
        """Adds a fact and returns its id (none for a value that isn't a finite number)."""
        number = float(value)
        if not math.isfinite(number):
            return None
        fid = f"F{len(self.facts) + 1}"
        self.facts.append({"id": fid, "what": what,
                           "value": int(number) if number.is_integer() else round(number, 3)})
        return fid

    def as_dict(self) -> Dict[str, Any]:
        return {"card_id": self.card_id, "kind": self.kind, "subject": self.subject, "lens": self.lens,
                "facts": self.facts, "context": self.context}


def packet_hash(packet: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]


def fact_values(packet: Dict[str, Any]) -> Dict[str, float]:
    return {f["id"]: f["value"] for f in packet["facts"]}


def render(packet: Dict[str, Any]) -> str:
    """The packet as an analyst reads it."""
    lens = packet["lens"]
    lines = [f"Subject: {packet['subject']}",
             f"Lens: {lens['name']}, version {lens.get('version') or '-'}, capture {lens['session_id']}",
             "", "Facts (cite them by id):"]
    lines += [f"{f['id']}  {f['what']}: {f['value']}" for f in packet["facts"]]
    for title, body in packet["context"].items():
        lines += ["", f"{title}:"] + [f"- {line}" for line in body]
    return "\n".join(lines)


@dataclass
class LensEvidence:
    """Everything the packets of one lens version draw on, read once."""

    view: Any  # a LensView
    folder: Any  # the lens's folder
    axes: Dict[str, List[str]]
    base: Dict[str, Dict[str, int]]  # axis -> value -> items in the lens
    manifest: Dict[str, Any]
    details: Optional[Dict[str, Any]]
    validation: Optional[Dict[str, Any]]
    marks: Optional[Dict[str, Any]]
    search: Optional[Dict[str, Any]] = None  # a tuned lens's search (search.json)
    routes: Optional[Dict[str, Any]] = None  # its pipelines, hubs and experts involved (routes.json)

    @property
    def lens(self) -> Dict[str, Any]:
        return {"session_id": self.view.session_id, "name": self.view.name, "version": self.view.version}


def _read(path: Any) -> Optional[Dict[str, Any]]:
    found: Optional[Dict[str, Any]] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    return found


def load_evidence(session_id: str, name: str, version: Optional[str] = None) -> LensEvidence:
    from services.lenses.flows import axes_of, value_of
    from services.lenses.raw import lens_marks
    from services.lenses.store import lens_dir
    from services.lenses.view import open_lens

    view = open_lens(session_id, name, version)
    folder = lens_dir(session_id, name)
    axes = axes_of(view)
    base = {axis: dict(Counter(v for item in view.items if (v := value_of(item, axis)) is not None)) for axis in axes}
    return LensEvidence(view, folder, axes, base, _read(folder / "lens.json") or {},
                        _read(folder / "details" / f"{view.version}.json"), _read(folder / "validation.json"),
                        lens_marks(view, folder), _read(folder / "search.json"), _read(folder / "routes.json"))


MANY_VALUES = 8  # an axis with more values shows only the five the population holds most


def _makeup(p: Packet, ev: LensEvidence, mask: Array, name: str,
            against: Optional[Array] = None, against_name: str = "all items", compare: bool = True) -> None:
    """The population's share of each designed value, beside the same share in a comparison
    population (the whole lens by default) unless `compare` is off."""
    from services.lenses.flows import value_of

    idx = np.flatnonzero(mask)
    other = np.flatnonzero(against) if against is not None else np.arange(len(ev.view.items))
    for axis, values in ev.axes.items():
        held = Counter(v for i in idx if (v := value_of(ev.view.items[int(i)], axis)) is not None)
        theirs = Counter(v for i in other if (v := value_of(ev.view.items[int(i)], axis)) is not None)
        shown = values
        if len(values) > MANY_VALUES:
            p.fact(f"distinct values of {axis} in {name}", len(held))
            if compare:
                p.fact(f"distinct values of {axis} in {against_name}", len(theirs))
            shown = [v for v, _ in held.most_common(5)]
        for value in shown:
            p.fact(f"share of {name} with {axis} = {value}", held[value] / max(len(idx), 1))
            if compare:
                p.fact(f"share of {against_name} with {axis} = {value}", theirs[value] / max(len(other), 1))


def _moves(p: Packet, ev: LensEvidence, mask: Array, li: int, name: str) -> None:
    """Where the population's items sit at the layers before and after."""
    view = ev.view
    if li > 0:
        for node, n in Counter(view.nodes[mask, li - 1].tolist()).most_common(4):
            p.fact(f"items of {name} that were in L{view.layers[li - 1]}C{node} the layer before", n)
    if li + 1 < len(view.layers):
        for node, n in Counter(view.nodes[mask, li + 1].tolist()).most_common(4):
            p.fact(f"items of {name} that go on to L{view.layers[li + 1]}C{node}", n)


def _experts_at(p: Packet, ev: LensEvidence, mask: Array, li: int, name: str, rank: int = 1) -> None:
    """The experts the population's items are routed to at a rank, and their mean gate weight."""
    view, layer = ev.view, ev.view.layers[li]
    for expert, n in Counter(view.experts[mask, li, rank - 1].tolist()).most_common(4):
        p.fact(f"items of {name} routed to L{layer}E{expert} at rank {rank}", n)
    p.fact(f"mean gate weight of the rank {rank} expert for {name} (the model's own top four weights)",
           float(view.weights[mask, li, rank - 1].mean()))


def _examples(ev: LensEvidence, mask: Array, key: str, count: int = EXAMPLES) -> List[str]:
    """Up to `count` of the population's sentences with their labels: see `example_indices`."""
    view = ev.view
    return [f"[{view.items[i].get('label')}] " + " ".join(str(view.items[i].get("input_text") or "").split())[:TEXT_CHARS]
            for i in example_indices(ev, mask, key, count)]


def example_indices(ev: LensEvidence, mask: Array, key: str, count: int = EXAMPLES) -> List[int]:
    """Up to `count` of the population's items, in proportion to its labels (largest remainder;
    the commonest label first), the same ones each time."""
    view = ev.view
    idx = sorted(np.flatnonzero(mask).tolist(),
                 key=lambda i: hashlib.sha256(f"{key}:{view.items[i]['probe_id']}".encode()).hexdigest())
    by_label: Dict[str, List[int]] = {}
    for i in idx:
        by_label.setdefault(str(view.items[i].get("label")), []).append(i)
    take = min(count, len(idx))
    quota = {label: take * len(found) / max(len(idx), 1) for label, found in by_label.items()}
    slots = {label: int(q) for label, q in quota.items()}
    for label in sorted(quota, key=lambda lab: slots[lab] - quota[lab])[:take - sum(slots.values())]:
        slots[label] += 1
    return [i for label, found in sorted(by_label.items(), key=lambda kv: -len(kv[1])) for i in found[:slots[label]]]


def _tokens(tokens: List[Any]) -> str:
    return ", ".join(json.dumps(token, ensure_ascii=False) for token, _ in tokens)


def _layer_scores(p: Packet, ev: LensEvidence, li: int, k: int) -> None:
    """The layer's held-out agreement with the label at the version's k, when validated."""
    layer = ev.view.layers[li]
    entry = (ev.validation or {}).get("layers", {}).get(str(layer), {}).get(str(k)) or {}
    held = (entry.get("heldout") or {}).get("label")
    if held and ev.validation:
        folds = ev.validation["folds"]
        p.fact(f"held-out agreement of the nodes at L{layer} with the label, at this k (kappa)", held["kappa"])
        p.fact("folds in the validation", folds["n_folds"])
        p.context["validation"] = [f"held out by {folds['kind']}"
                                   + (", weaker than holding out scene families" if folds.get("weaker") else "")]


def _node_details(p: Packet, ev: LensEvidence, layer: int, node: int) -> None:
    """The node's worked-out details, when there are any: neurons, logit lens, surface, routing."""
    at = (ev.details or {}).get("layers", {}).get(str(layer))
    found = (at or {}).get("nodes", {}).get(str(node))
    if not at or not found:
        p.context["not worked out yet"] = ["the node's neurons, logit lens, surface check and routing measures"]
        return
    for neuron, r in found["neurons"][:5]:
        p.fact(f"correlation of neuron n{neuron}'s value with membership of the node", r)
    p.context["tokens the node's centre favours more than the layer's average item does (logit lens)"] = [
        _tokens(found["logit_lens"]["distinctive"])]
    if at.get("surface_kappa") is not None:
        p.fact("how well surface features alone predict the layer's nodes, held out (kappa)", at["surface_kappa"])
    surface = found.get("surface")
    if surface:
        if surface["feature"]:
            p.fact(f"how well {surface['feature']} alone separates the node from the rest (AUC; 0.5 is not at all)",
                   surface["auc"])
        word = surface["first_word"]
        p.fact(f"share of the node's items starting with the word {json.dumps(word['word'])}", word["in_node"])
        p.fact("share of the layer's other items starting with that word", word["outside"])
        p.context["surface check"] = ["flagged: a surface feature separates this node strongly" if surface["flagged"]
                                      else "not flagged"]
    if at.get("routing_effect") is not None and found.get("routing"):
        p.fact("share of the next layer's routing variance that this layer's nodes explain", at["routing_effect"])
        p.fact("this node's part of that share", found["routing"]["share"])
        p.fact("how far the node's mean routing sits from the layer's (in items' typical distances)",
               found["routing"]["shift"])


def _layer_index(view: Any, layer: int) -> int:
    if layer not in view.layers:
        raise ValueError(f"L{layer} is not in this lens")
    return int(view.layers.index(layer))


def population_packet(ev: LensEvidence, li: int, mask: Array, name: str) -> Packet:
    """A node-shaped packet for any population of items at a layer: its size and make-up, where
    its items come from and go, its experts and examples. Node packets build on it; the analyst
    tests use it for made-up populations."""
    layer = ev.view.layers[li]
    p = Packet(name, "node", f"cluster node {name}: items the lens puts together at L{layer}", ev.lens)
    p.fact(f"items in {name}", int(mask.sum()))
    p.fact("items in the lens", len(ev.view.items))
    _makeup(p, ev, mask, name)
    _moves(p, ev, mask, li, name)
    _experts_at(p, ev, mask, li, name)
    p.context[f"example sentences from {name}, with their labels"] = _examples(ev, mask, name)
    return p


def node_packet(ev: LensEvidence, layer: int, node: int) -> Packet:
    view = ev.view
    li = _layer_index(view, layer)
    mask = view.nodes[:, li] == node
    if not mask.any():
        raise ValueError(f"L{layer}C{node} is not a node of version {view.version}")
    name, k = f"L{layer}C{node}", int(view.nodes[:, li].max()) + 1
    p = population_packet(ev, li, mask, name)
    p.fact(f"nodes at L{layer} (this version's k)", k)
    _layer_scores(p, ev, li, k)
    marked = (ev.marks or {}).get("layers", {}).get(str(layer))
    if marked is not None:
        p.fact(f"items of {name} grouped differently in raw space (co-members overlap under half)",
               marked["nodes"].get(name, 0))
    _node_details(p, ev, layer, node)
    return p


def expert_packet(ev: LensEvidence, layer: int, expert: int, rank: int) -> Packet:
    view = ev.view
    li = _layer_index(view, layer)
    mask = view.experts[:, li, rank - 1] == expert
    if not mask.any():
        raise ValueError(f"no item is routed to L{layer}E{expert} at rank {rank}")
    name = f"L{layer}E{expert}'s items"
    p = Packet(f"L{layer}E{expert}r{rank}", "expert",
               f"expert L{layer}E{expert} at rank {rank}: the items the router sends to it", ev.lens)
    p.fact(f"items routed to L{layer}E{expert} at rank {rank}", int(mask.sum()))
    p.fact("items in the lens", len(view.items))
    p.fact(f"mean gate weight L{layer}E{expert} gets from them (the model's own top four weights)",
           float(view.weights[mask, li, rank - 1].mean()))
    _makeup(p, ev, mask, name)
    for node, n in Counter(view.nodes[mask, li].tolist()).most_common(4):
        p.fact(f"of them, items in cluster node L{layer}C{node}", n)
    for step, word in ((-1, "before"), (1, "next")):
        if 0 <= li + step < len(view.layers):
            other = view.layers[li + step]
            for e, n in Counter(view.experts[mask, li + step, rank - 1].tolist()).most_common(4):
                p.fact(f"of them, items routed to L{other}E{e} at rank {rank} the layer {word}", n)
    p.context[f"example sentences routed to L{layer}E{expert}, with their labels"] = _examples(ev, mask, p.card_id)
    return p


def link_packet(ev: LensEvidence, layer: int, a: int, layer2: int, b: int, rank: Optional[int] = None) -> Packet:
    """A route between two cluster nodes, or between two experts at a rank (`rank` given): its
    items against the source's other items."""
    view = ev.view
    li = _layer_index(view, layer)
    if li + 1 >= len(view.layers) or view.layers[li + 1] != layer2:
        raise ValueError(f"L{layer2} doesn't follow L{layer} in this lens")
    kind, letter = ("expert_route", "E") if rank else ("route", "C")
    codes = view.experts[:, :, rank - 1] if rank else view.nodes
    source, target = codes[:, li] == a, codes[:, li + 1] == b
    mask = source & target
    if not mask.any():
        raise ValueError(f"no item goes from L{layer}{letter}{a} to L{layer2}{letter}{b}")
    start, end = f"L{layer}{letter}{a}", f"L{layer2}{letter}{b}"
    card = f"{start}-{end}" + (f"r{rank}" if rank else "")
    what = f"experts at rank {rank}" if rank else "cluster nodes"
    p = Packet(card, kind, f"the route from {start} to {end} ({what}): the items that take it", ev.lens)
    p.fact("items on the route", int(mask.sum()))
    p.fact(f"items at {start}", int(source.sum()))
    p.fact(f"items at {end}", int(target.sum()))
    p.fact("items in the lens", len(view.items))
    rest = source & ~target
    _makeup(p, ev, mask, "the route's items", against=rest, against_name=f"{start}'s other items")
    if not rank:
        _experts_at(p, ev, mask, li, "the route's items")
    p.context["example sentences on the route, with their labels"] = _examples(ev, mask, card)
    if rest.any():
        p.context[f"example sentences from {start}'s other items"] = _examples(ev, rest, card + "-rest", 4)
    return p


SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE = 5, 0.15  # a branch holds at least this many items and this share


def branches_of(view: Any, li: int, node: int) -> List[Any]:
    """The next-layer nodes that take a real share of a node's items: (node, items), biggest first."""
    mask = view.nodes[:, li] == node
    floor = max(SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE * int(mask.sum()))
    return [(int(b), n) for b, n in Counter(view.nodes[mask, li + 1].tolist()).most_common() if n >= floor]


def split_points(view: Any) -> List[Any]:
    """Every node whose items part ways at the next layer: (layer, node, items in its second
    branch), the biggest second branch first."""
    found = []
    for li in range(len(view.layers) - 1):
        for node in np.unique(view.nodes[:, li]).tolist():
            branches = branches_of(view, li, int(node))
            if len(branches) >= 2:
                found.append((view.layers[li], int(node), branches[1][1]))
    return sorted(found, key=lambda s: -s[2])


def split_packet(ev: LensEvidence, layer: int, node: int) -> Packet:
    from sklearn.metrics import adjusted_mutual_info_score

    from services.lenses.flows import value_of

    view = ev.view
    li = _layer_index(view, layer)
    if li + 1 >= len(view.layers):
        raise ValueError(f"L{layer} is the lens's last layer")
    branches = branches_of(view, li, node)
    if len(branches) < 2:
        raise ValueError(f"L{layer}C{node} doesn't split at the next layer")
    name, nxt = f"L{layer}C{node}", view.layers[li + 1]
    mask = view.nodes[:, li] == node
    p = Packet(f"split-{name}", "split", f"split point {name}: its items part ways at L{nxt}", ev.lens)
    p.fact(f"items in {name}", int(mask.sum()))
    for b, n in branches:
        p.fact(f"items of {name} going on to L{nxt}C{b}", n)
    kept = np.flatnonzero(mask & np.isin(view.nodes[:, li + 1], [b for b, _ in branches]))
    branch = view.nodes[kept, li + 1]
    for axis in ev.axes:
        values = [str(value_of(view.items[int(i)], axis)) for i in kept]
        if len(set(values)) > 1:
            p.fact(f"agreement between the branches and {axis} among these items (AMI; 0 none, 1 complete)",
                   float(adjusted_mutual_info_score(values, branch)))
    _makeup(p, ev, mask, name)
    for b, _ in branches:
        part = mask & (view.nodes[:, li + 1] == b)
        _makeup(p, ev, part, f"the branch to L{nxt}C{b}", compare=False)
        p.context[f"example sentences going on to L{nxt}C{b}"] = _examples(ev, part, f"{p.card_id}-{b}", 4)
    return p


def _ami(a: List[Any], b: Any) -> float:
    from sklearn.metrics import adjusted_mutual_info_score

    return float(adjusted_mutual_info_score([str(x) for x in a], [str(x) for x in b]))


def _lens_layer(p: Packet, ev: LensEvidence, li: int, axis_values: Dict[str, List[str]]) -> None:
    view, layer = ev.view, ev.view.layers[li]
    nodes, tag = view.nodes[:, li], f"L{layer}:"
    k = int(nodes.max()) + 1
    p.fact(f"{tag} nodes", k)
    settings = LensSettings.model_validate(ev.manifest.get("settings") or {})
    if settings.per_layer is not None:  # this layer's own UMAP settings, tuned or set by hand
        how = "tuned" if settings.source_at(li) == "tuned" else "set by hand"
        p.fact(f"{tag} UMAP neighbours ({how})", settings.per_layer[li].n_neighbors)
        p.fact(f"{tag} UMAP dimensions ({how})", settings.per_layer[li].dimensions)
    for axis, values in axis_values.items():
        p.fact(f"{tag} agreement of the nodes with {axis} (AMI, in-sample)", _ami(values, nodes))
    if li + 1 < len(view.layers):
        p.fact(f"{tag} how much L{view.layers[li + 1]}'s nodes follow from these (AMI)", _ami(nodes.tolist(), view.nodes[:, li + 1]))
    first = view.experts[:, li, 0]
    p.fact(f"{tag} experts used at rank 1", len(set(first.tolist())))
    if "label" in axis_values:
        p.fact(f"{tag} agreement of the rank 1 expert with the label (AMI)", _ami(axis_values["label"], first))
    entry = (ev.validation or {}).get("layers", {}).get(str(layer), {}).get(str(k)) or {}
    held = (entry.get("heldout") or {}).get("label")
    if held:
        p.fact(f"{tag} held-out agreement with the label at this k (kappa)", held["kappa"])
    compared = (ev.validation or {}).get("comparison", {}).get(str(layer), {})
    raw = (compared.get("raw_ward") or {}).get(str(k))
    if raw:
        p.fact(f"{tag} the same for raw space (PCA-50 then Ward) at this k (kappa)", raw["kappa"])
    if compared.get("ceiling"):
        p.fact(f"{tag} the supervised ceiling (logistic regression, kappa)", compared["ceiling"]["kappa"])
    at = (ev.details or {}).get("layers", {}).get(str(layer)) or {}
    if at.get("routing_effect") is not None:
        p.fact(f"{tag} share of the next layer's routing variance the nodes explain", at["routing_effect"])
    if at.get("surface_kappa") is not None:
        p.fact(f"{tag} how well surface features alone predict the nodes (kappa, held out)", at["surface_kappa"])
    marked = (ev.marks or {}).get("layers", {}).get(str(layer))
    if marked is not None:
        p.fact(f"{tag} items grouped differently in raw space", len(marked["marked"]))
    if li + 1 < len(view.layers):  # the transition's main links, by the split-branch rule
        nxt = view.layers[li + 1]
        for node in range(k):
            inside = nodes == node
            floor = max(SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE * int(inside.sum()))
            for target, n in Counter(view.nodes[inside, li + 1].tolist()).most_common():
                if n >= floor:
                    p.fact(f"{tag} items going from L{layer}C{node} to L{nxt}C{target}", n)
    for node in range(k):
        members = np.flatnonzero(nodes == node)
        if members.size and "label" in axis_values:
            top, n = Counter(axis_values["label"][int(i)] for i in members).most_common(1)[0]
            p.fact(f"{tag} items in L{layer}C{node}", int(members.size))
            p.fact(f"{tag} share of L{layer}C{node} with label = {top}", n / members.size)


def lens_packet(ev: LensEvidence) -> Packet:
    from services.lenses.flows import value_of

    view = ev.view
    p = Packet("lens", "lens", f"the lens {view.name} across its layers: its cluster and expert flows", ev.lens)
    p.fact("items in the lens", len(view.items))
    p.fact("layers in the lens", len(view.layers))
    settings = ev.manifest.get("settings", {})
    if not settings.get("per_layer"):  # a tuned lens states each layer's own settings instead
        p.fact("UMAP neighbours (n_neighbors)", settings.get("n_neighbors", float("nan")))
        p.fact("UMAP dimensions", settings.get("dimensions", float("nan")))
    for axis, counts in ev.base.items():
        for value, n in sorted(counts.items(), key=lambda kv: -kv[1])[:MANY_VALUES]:
            p.fact(f"items with {axis} = {value}", n)
    check = ev.manifest.get("self_check")
    if check:
        p.fact("self-check: planted classes recovered (ARI)", check["planted"]["ari_k5"])
        p.fact("self-check: the least it must reach", check["thresholds"]["planted_ari"])
        p.fact("self-check: structure found in pure noise (AMI)", check["null"]["ami_k5"])
        p.fact("self-check: the most it may reach", check["thresholds"]["null_ami"])
    else:
        p.context["self-check"] = ["none recorded: this lens was built before builds ran one"]
    p.context["flows"] = ["only the links that carry a real share of their source node's items are listed"]
    axis_values = {axis: [str(value_of(item, axis)) for item in view.items] for axis in ev.axes}
    for li in range(len(view.layers)):
        _lens_layer(p, ev, li, axis_values)
    if ev.validation:
        folds = ev.validation["folds"]
        p.fact("folds in the validation", folds["n_folds"])
        p.context["validation"] = [f"held out by {folds['kind']}"
                                   + (", weaker than holding out scene families" if folds.get("weaker") else "")]
    else:
        p.context["validation"] = ["not validated yet: there are no held-out scores"]
    if not ev.details:
        p.context["node details"] = ["not worked out yet: no routing or surface measures"]
    _routes_digest(p, ev)
    return p


ROUTE_PIPELINES = 8  # pipelines a routes packet describes, the strongest first
ROUTE_EXPERTS = 2  # experts involved a routes packet lists per designed value


def _chain(pipeline: Dict[str, Any]) -> str:
    steps = [f"L{layer}E{expert}" for layer, expert in zip(pipeline["layers"], pipeline["experts"])]
    return " > ".join(steps if len(steps) <= 8 else steps[:4] + ["..."] + steps[-3:])


def _members_of(ev: LensEvidence, pipeline: Dict[str, Any]) -> Array:
    index = {item["probe_id"]: i for i, item in enumerate(ev.view.items)}
    mask = np.zeros(len(ev.view.items), dtype=bool)
    mask[[index[m] for m in pipeline["member_ids"] if m in index]] = True
    return mask


def _route_makeup(p: Packet, ev: LensEvidence, tag: str, mask: Array) -> None:
    """A pipeline's members' shares on each designed axis, beside all items' shares: the two values
    of each axis that its members hold most, worked out from the evidence's own items (so a decoy
    with shuffled values shows shuffled shares)."""
    from services.lenses.flows import value_of

    n, total = int(mask.sum()), len(ev.view.items)
    for axis in ev.axes:
        tally = Counter(v for i in np.flatnonzero(mask) if (v := value_of(ev.view.items[int(i)], axis)) is not None)
        for value, count in tally.most_common(2):
            p.fact(f"{tag}: share of its members with {axis} = {value}", count / n)
            p.fact(f"{tag}: share of all items with {axis} = {value}", ev.base[axis].get(value, 0) / total)


def routes_packet(ev: LensEvidence) -> Packet:
    if not ev.routes:
        raise ValueError("work out the lens's routes first (POST .../routes)")
    view, routes = ev.view, ev.routes
    p = Packet("routes", "routes", f"the expert pipelines, hubs and experts involved in {view.name}", ev.lens)
    p.fact("items in the lens", len(view.items))
    p.fact("items a pipeline or hub must hold at least", routes["min_items"])
    p.fact("pipelines found", len(routes["pipelines"]))
    p.fact("hubs found", len(routes["hubs"]))
    chains: List[str] = []
    for pipeline in routes["pipelines"][:ROUTE_PIPELINES]:
        tag = pipeline["id"]
        mask = _members_of(ev, pipeline)
        p.fact(f"{tag}: layers it spans", len(pipeline["layers"]))
        p.fact(f"{tag}: members (items keeping its experts among their four)", int(mask.sum()))
        p.fact(f"{tag}: its members' mean credit (the geometric mean of their weights along it)", pipeline["mean_weight"])
        p.fact(f"{tag}: members taking it as their top expert at every layer", pipeline["rank1"])
        _route_makeup(p, ev, tag, mask)
        before = ", ".join(f"L{b['layer']}E{b['expert']}" for b in pipeline["before"]) or "none"
        after = ", ".join(f"L{a['layer']}E{a['expert']}" for a in pipeline["after"]) or "none"
        chains.append(f"{tag}: {_chain(pipeline)}; {'found again' if pipeline['replicated'] else 'not found again'} in "
                      f"both halves of the folds; experts before it: {before}; after it: {after}")
    p.context["pipelines"] = chains or ["none: no group of items keeps the same experts for three layers"]
    hubs: List[str] = []
    for hub in routes["hubs"]:
        tag = f"{hub['id']} (L{hub['layer']}E{hub['expert']})"
        p.fact(f"{tag}: effective number of sources, between items", hub["sources"])
        p.fact(f"{tag}: weighted items", hub["weighted"])
        hubs.append(f"{tag}: from " + ", ".join(f"L{hub['layer'] - 1}E{f['expert']}" for f in hub["from"]))
    p.context["hubs"] = hubs or ["none: at every expert the items arrive from much the same experts"]
    involved: List[str] = []
    for axis, values in routes["involved"].items():
        for value, found in values.items():
            p.fact(f"{axis} = {value}: experts whose weight differs from the rest beyond chance", len(found["experts"]))
            for cell in found["experts"][:ROUTE_EXPERTS]:
                tag = f"{axis} = {value}: L{cell['layer']}E{cell['expert']}"
                p.fact(f"{tag}, mean weight difference (positive: more weight on {value})", cell["diff"])
                p.fact(f"{tag}, how well its weight tells {value} apart (AUC)", cell["auc"])
            if found["experts"]:
                involved.append(f"{axis} = {value}: permutations moved {found['permuted']} together")
    p.context["experts involved"] = involved or ["none beyond chance"]
    p.context["reading these"] = ["a pipeline every value takes in about its usual share is a trunk, not a pattern",
                                  "a pipeline found again in both halves of the folds is less likely to be chance"]
    return p


def _routes_digest(p: Packet, ev: LensEvidence) -> None:
    """The lens report's facts on pipelines, hubs and the experts involved (the routes card has more)."""
    from services.lenses.flows import value_of

    if not ev.routes:
        p.context["pipelines and hubs"] = ["not worked out yet"]
        return
    routes = ev.routes
    p.fact("expert pipelines found", len(routes["pipelines"]))
    p.fact("hubs found", len(routes["hubs"]))
    lines: List[str] = []
    for pipeline in routes["pipelines"][:3]:
        tag = pipeline["id"]
        mask = _members_of(ev, pipeline)
        p.fact(f"{tag}: members", int(mask.sum()))
        p.fact(f"{tag}: layers it spans", len(pipeline["layers"]))
        if "label" in ev.axes:
            top, count = Counter(str(value_of(ev.view.items[int(i)], "label")) for i in np.flatnonzero(mask)).most_common(1)[0]
            p.fact(f"{tag}: share of its members with label = {top}", count / max(1, int(mask.sum())))
        lines.append(f"{tag}: {_chain(pipeline)}")
    for value, found in (routes["involved"].get("label") or {}).items():
        p.fact(f"label = {value}: experts whose weight differs from the rest beyond chance", len(found["experts"]))
    p.context["pipelines and hubs"] = lines or ["no pipeline: no group of items keeps the same experts for three layers"]


def k_packet(ev: LensEvidence) -> Packet:
    if not ev.validation:
        raise ValueError("validate the lens first: the k advisor reads its k profile")
    view, validation = ev.view, ev.validation
    p = Packet("k", "k", f"the k profile of {view.name}: how many nodes to cut at each layer", ev.lens)
    p.fact("items in the lens", len(view.items))
    p.fact("folds in the validation", validation["folds"]["n_folds"])
    suggestions = ev.manifest.get("suggestions", {})
    tuned = {int(w["layer"]): w for w in (ev.search or {}).get("winners", [])}
    for li, layer in enumerate(view.layers):
        tag, k = f"L{layer}:", int(view.nodes[:, li].max()) + 1
        profile = validation["layers"].get(str(layer), {})
        held = {int(kk): e["heldout"]["label"] for kk, e in profile.items() if (e.get("heldout") or {}).get("label")}
        p.fact(f"{tag} k in this version", k)
        if k in held:
            p.fact(f"{tag} held-out AMI with the label at this version's k", held[k]["ami"])
            p.fact(f"{tag} held-out kappa with the label at this version's k", held[k]["kappa"])
        if held:
            best = max(held, key=lambda kk: (held[kk]["ami"], -kk))
            p.fact(f"{tag} the k with the best held-out AMI (choosing by it is selection-biased)", best)
            p.fact(f"{tag} that best held-out AMI", held[best]["ami"])
        if layer in tuned and tuned[layer].get("test"):
            p.fact(f"{tag} the tuning's k, chosen by held-out AMI on selection folds", tuned[layer]["k"])
            p.fact(f"{tag} the tuned layer's AMI on the test portion the tuning never saw", tuned[layer]["test"]["ami"])
        seed = (profile.get(str(k)) or {}).get("seed_ari")
        if seed is not None:
            p.fact(f"{tag} agreement across seeds at this version's k (ARI)", seed)
        found = suggestions.get(str(layer)) or {}
        if found.get("elbow"):
            p.fact(f"{tag} k by the elbow method (in-sample, no labels)", found["elbow"])
        if found.get("silhouette"):
            p.fact(f"{tag} k by silhouette (in-sample, no labels)", found["silhouette"])
        for level in found.get("levels") or []:
            p.fact(f"{tag} a k where the hierarchy has a clear level (in-sample)", level)
    folds = validation["folds"]
    p.context["validation"] = [f"held out by {folds['kind']}"
                               + (", weaker than holding out scene families" if folds.get("weaker") else "")]
    p.context["choosing k"] = ["held-out AMI scores how well the nodes match the classes on held-out items; held-out "
                               "kappa keeps rising with k because smaller nodes are purer",
                               "picking the k that maximises a held-out score is selection-biased; a tuned lens's test "
                               "score was never used in choosing",
                               "the elbow, silhouette and hierarchy levels don't use the labels"]
    return p


CARD_IDS = "lens, k, routes, L12C0, L12E5r1, L12C0-L13C2, L12E5-L13E7r1 or split-L12C1"


def build_packet(ev: LensEvidence, card_id: str) -> Packet:
    """The packet for a card id (see the module's docstring)."""
    if card_id == "lens":
        return lens_packet(ev)
    if card_id == "k":
        return k_packet(ev)
    if card_id == "routes":
        return routes_packet(ev)
    if m := re.fullmatch(r"split-L(\d+)C(\d+)", card_id):
        return split_packet(ev, int(m[1]), int(m[2]))
    if m := re.fullmatch(r"L(\d+)C(\d+)", card_id):
        return node_packet(ev, int(m[1]), int(m[2]))
    if m := re.fullmatch(r"L(\d+)E(\d+)r([1-4])", card_id):
        return expert_packet(ev, int(m[1]), int(m[2]), int(m[3]))
    if m := re.fullmatch(r"L(\d+)C(\d+)-L(\d+)C(\d+)", card_id):
        return link_packet(ev, int(m[1]), int(m[2]), int(m[3]), int(m[4]))
    if m := re.fullmatch(r"L(\d+)E(\d+)-L(\d+)E(\d+)r([1-4])", card_id):
        return link_packet(ev, int(m[1]), int(m[2]), int(m[3]), int(m[4]), rank=int(m[5]))
    raise ValueError(f"'{card_id}' isn't a card id ({CARD_IDS})")
