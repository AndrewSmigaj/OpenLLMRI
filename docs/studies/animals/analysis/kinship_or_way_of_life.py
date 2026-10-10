"""Kinship or way of life, layer by layer (the animal study, 10d.5).

The set's guide lists 33 animals whose kinship and way of life disagree: mammals that swim or fly,
birds that don't fly, animals named "fish" that aren't fish, legless animals outside the snakes,
and a fish that walks. For each of them, two sets of other animals:
  - kin: its own group, without the trait that sets it apart (for a dolphin, mammals that don't
    swim);
  - look-alikes: animals with that trait from other groups (for a dolphin, non-mammals that swim).
    For a named "fish" they are fish whose names don't end in "fish" (the name's own pull is the
    split-word analysis's); for a legless animal, the snakes; for the mudskipper, non-fish that
    walk.
At every layer, among the animal's 10 nearest neighbours: K kin and W look-alikes, each against
its chance level (10 times the set's share of the other animals). The index
    log2((K + 0.5) / (expected K + 0.5)) - log2((W + 0.5) / (expected W + 0.5))
is above 0 when the neighbours lean to kin, below 0 when they lean to look-alikes.

The null: the same index with the animals' positions shuffled (each item takes another's place)
1,000 times, from a seeded stream of its own for each count, space and layer; the band is the
middle 95% of each kind's mean index.

Whether a name split divides the space at every layer (split_words.py), and the one-token names
are mostly mammals, so the index is also counted within the animal's own token count: only the
neighbours with the animal's token count are counted, against chance in that pool, and the null
shuffles positions within each token count.

Two spaces: the lens's own embedding, and the residual stream in the validation's raw recipe.

  .venv/bin/python docs/studies/animals/analysis/kinship_or_way_of_life.py SESSION LENS
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List

import numpy as np
from common import (
    NEIGHBOURS,
    SEED,
    band,
    figure_path,
    lens_embedding,
    lens_items,
    neighbours,
    raw_layers,
    write_results,
)

KINDS = {
    "mammals that swim": ["whale", "humpback", "dolphin", "orca", "porpoise", "narwhal", "beluga", "manatee",
                          "dugong", "seal", "walrus", "otter", "beaver", "muskrat", "nutria", "platypus"],
    "mammals that fly": ["bat", "colugo"],
    "birds that don't fly": ["penguin", "ostrich", "emu", "cassowary", "rhea", "kakapo"],
    'named "fish", not fish': ["starfish", "jellyfish", "cuttlefish", "crayfish", "silverfish"],
    "legless, not snakes": ["eel", "caecilian", "slowworm"],
    "a fish that walks": ["mudskipper"],
}
SNAKE_TAXA = {"Serpentes", "Elapidae", "Viperidae", "Boidae", "Colubridae"}
SHUFFLES = 1000


def is_snake(entry: Dict[str, Any]) -> bool:
    tax = entry["taxonomy"]
    return tax["name"] in SNAKE_TAXA or tax["family"] in SNAKE_TAXA


def sets_for(kind: str, i: int, items: List[Dict[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    """(kin, look-alikes) as boolean masks over the items, never holding the animal itself."""
    me = items[i]["entry"]
    group = np.array([it["entry"]["group"] for it in items])
    move = np.array([it["entry"]["categories"]["movement"] for it in items])
    word = np.array([it["entry"]["target_word"] for it in items])
    named_fish = np.char.endswith(word.astype(str), "fish")
    snake = np.array([is_snake(it["entry"]) for it in items])
    same = group == me["group"]
    if kind in ("mammals that swim", "mammals that fly", "birds that don't fly", "a fish that walks"):
        trait = move == me["categories"]["movement"]
        kin, look = same & ~trait, ~same & trait
    elif kind == 'named "fish", not fish':
        kin, look = same & ~named_fish, (group == "fish") & ~named_fish
    else:  # legless, not snakes
        kin, look = same & ~snake, snake.copy()
    kin[i] = look[i] = False
    return kin, look


def index_of(nn_row: np.ndarray, kin: np.ndarray, look: np.ndarray, pool: np.ndarray) -> tuple[float, int, int]:
    """The index among the neighbours in the pool (the items that may count, never the animal),
    against chance in the pool."""
    counted = nn_row[pool[nn_row]]
    k, w = int(kin[counted].sum()), int(look[counted].sum())
    size = pool.sum()
    ek, ew = len(counted) * (kin & pool).sum() / size, len(counted) * (look & pool).sum() / size
    return float(np.log2((k + 0.5) / (ek + 0.5)) - np.log2((w + 0.5) / (ew + 0.5))), k, w


def shuffled_places(rng, classes: np.ndarray) -> np.ndarray:
    """A permutation of the items that keeps each one within its class."""
    place = np.arange(len(classes))
    for c in np.unique(classes):
        idx = np.flatnonzero(classes == c)
        place[idx] = rng.permutation(idx)
    return place


def space_scores(points: np.ndarray, members: Dict[str, List[int]], masks, rng,
                 classes: np.ndarray) -> Dict[str, Any]:
    """`classes` limits the count to the animal's own class (all zeros: every item counts)."""
    nn = neighbours(points)
    pools = {}
    for idx in members.values():
        for i in idx:
            pools[i] = classes == classes[i]
            pools[i][i] = False
    per_animal, per_kind = {}, {}
    for kind, idx in members.items():
        values = []
        for i in idx:
            kin, look = masks[i]
            value, k, w = index_of(nn[i], kin, look, pools[i])
            per_animal[i] = {"index": value, "kin": k, "look": w}
            values.append(value)
        per_kind[kind] = {"mean": float(np.mean(values))}
    nulls = {kind: [] for kind in members}
    for _ in range(SHUFFLES):
        place = shuffled_places(rng, classes)  # item j now sits where item place[j] was
        where = np.empty_like(place)
        where[place] = np.arange(len(points))
        for kind, idx in members.items():
            vals = []
            for i in idx:
                kin, look = masks[i]
                row = where[nn[place[i]]]  # the items now sitting next to item i's new place
                vals.append(index_of(row, kin, look, pools[i])[0])
            nulls[kind].append(float(np.mean(vals)))
    for kind in members:
        per_kind[kind]["band"] = band(np.array(nulls[kind]))
    return {"kinds": per_kind, "animals": per_animal}


def main(session: str, lens: str) -> None:
    items = lens_items(session, lens)
    words = [it["entry"]["target_word"] for it in items]
    members = {kind: [words.index(w) for w in names if w in words] for kind, names in KINDS.items()}
    missing = [w for names in KINDS.values() for w in names if w not in words]
    masks = {i: sets_for(kind, i, items) for kind, idx in members.items() for i in idx}
    embedding = lens_embedding(session, lens)
    layers = list(range(embedding.shape[0]))
    raw = raw_layers(session, [it["probe_id"] for it in items], layers)
    results: Dict[str, Any] = {"session": session, "lens": lens, "items": len(items), "neighbours": NEIGHBOURS,
                               "shuffles": SHUFFLES, "kinds": KINDS, "missing": missing,
                               "sizes": {words[i]: {"kin": int(masks[i][0].sum()), "look": int(masks[i][1].sum())}
                                         for idx in members.values() for i in idx},
                               "one_token": [w for w in words if items[words.index(w)]["entry"]["categories"]["tokens"] == "one"
                                             and any(w in names for names in KINDS.values())],
                               "spaces": {"lens": {}, "raw": {}},
                               "within_token_count": {"spaces": {"lens": {}, "raw": {}}}}
    every = np.zeros(len(items), dtype=np.int64)
    token_count = np.array([it["entry"]["categories"]["tokens"] == "several" for it in items], dtype=np.int64)
    for layer in layers:
        for si, (space, points) in enumerate((("lens", embedding[layer]), ("raw", raw[layer]))):
            for mi, (where_to, classes) in enumerate(((results["spaces"], every),
                                                      (results["within_token_count"]["spaces"], token_count))):
                rng = np.random.default_rng([SEED, mi, si, layer])
                scores = space_scores(points, members, masks, rng, classes)
                scores["animals"] = {words[i]: v for i, v in scores["animals"].items()}
                where_to[space][layer] = scores
        print(f"L{layer:02d} lens " + "  ".join(f"{kind[:14]} {results['spaces']['lens'][layer]['kinds'][kind]['mean']:+.2f}"
                                               for kind in members))
    for block in (results, results["within_token_count"]):
        block["beyond_chance"] = {space: {kind: {
            "kin": [layer for layer in layers if by_layer[layer]["kinds"][kind]["mean"] > by_layer[layer]["kinds"][kind]["band"][1]],
            "look-alikes": [layer for layer in layers if by_layer[layer]["kinds"][kind]["mean"] < by_layer[layer]["kinds"][kind]["band"][0]],
        } for kind in members} for space, by_layer in block["spaces"].items()}
    path = write_results(f"kinship_or_way_of_life_{lens}", results)
    chart(results, lens, "", "")
    chart({**results, **results["within_token_count"]}, lens, "_within_token_count", ", counted within each token count")
    print(f"wrote {path}")
    for name, block in (("all names", results), ("within token count", results["within_token_count"])):
        for space, kinds in block["beyond_chance"].items():
            for kind, sides in kinds.items():
                print(f"{name:18s} {space:4s} {kind:28s} kin beyond chance at {sides['kin']}; look-alikes at {sides['look-alikes']}")


def chart(results: Dict[str, Any], lens: str, suffix: str, note: str) -> None:
    """Two figures: each kind's mean index with its own null band (a row per space), and every
    animal's index per layer."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    kinds = list(results["kinds"])
    spaces = (("lens", "the lens's embedding"), ("raw", "raw: standardized, 50 PCs"))
    fig, axes = plt.subplots(2, len(kinds), figsize=(3.2 * len(kinds), 6.2), sharex=True, sharey=True)
    for row, (space, title) in enumerate(spaces):
        by_layer = results["spaces"][space]
        layers = sorted(int(k) for k in by_layer)
        for col, kind in enumerate(kinds):
            ax = axes[row][col]
            mean = [by_layer[layer]["kinds"][kind]["mean"] for layer in layers]
            lo = [by_layer[layer]["kinds"][kind]["band"][0] for layer in layers]
            hi = [by_layer[layer]["kinds"][kind]["band"][1] for layer in layers]
            ax.fill_between(layers, lo, hi, color="#9ca3af", alpha=0.3, lw=0)
            ax.plot(layers, mean, color="#1d4ed8", lw=2)
            ax.axhline(0, color="#374151", lw=0.8)
            ax.grid(alpha=0.25)
            if row == 0:
                ax.set_title(f"{kind} ({len(results['kinds'][kind])})", fontsize=10)
            if row == 1:
                ax.set_xlabel("layer")
        axes[row][0].set_ylabel(f"{title}\nmean index (+ kin, − look-alikes)", fontsize=9)
    fig.suptitle(f"Kinship or way of life: {lens}{note} (grey: positions shuffled, middle 95%)", fontsize=12)
    fig.tight_layout()
    fig.savefig(figure_path(f"kinship_or_way_of_life_{lens}{suffix}"), dpi=150)

    fig, axes = plt.subplots(1, 2, figsize=(13, 7.5))
    for ax, (space, title) in zip(axes, spaces):
        by_layer = results["spaces"][space]
        layers = sorted(int(k) for k in by_layer)
        animals = [w for kind in kinds for w in results["kinds"][kind] if w not in results["missing"]]
        grid = np.array([[by_layer[layer]["animals"][w]["index"] for layer in layers] for w in animals])
        image = ax.imshow(grid, aspect="auto", cmap="RdBu", vmin=-4, vmax=4)
        ax.set_yticks(range(len(animals)), animals, fontsize=7)
        ax.set_xticks(range(0, len(layers), 2), [str(layers[j]) for j in range(0, len(layers), 2)], fontsize=8)
        ax.set_xlabel("layer")
        ax.set_title(title, fontsize=11)
    fig.colorbar(image, ax=axes, shrink=0.8, label="index: blue leans to kin, red to look-alikes")
    fig.suptitle(f"Kinship or way of life, animal by animal: {lens}{note}", fontsize=12)
    fig.savefig(figure_path(f"kinship_or_way_of_life_animals_{lens}{suffix}"), dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
