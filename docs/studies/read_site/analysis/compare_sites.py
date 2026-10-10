"""Where to read a single word: at its last token, or at the message's end marker (DESIGN.md C1, L16).

Slice 1c reads a single word at its last token. On both of its sets, whether the word split into
several tokens then divides the space at every layer (docs/research/animals.md), and the proposal
was to read every word at the token after it: the message's end marker `<|end|>`, the same token for
every item. Both sets were captured again with the end marker stored as a second site
(`capture_static_substring`). At the word's own site the new captures equal the old ones bit for
bit, so the read site is the only difference. The same lenses were built at both sites (same
settings, seed and folds), validated, analysed on their axes, and run through the studies' scripts.

This script fits nothing: it reads those outputs and puts the two sites side by side, layer by layer.
- **Animals:**
  - the group held out, by the lens's nodes (k 8) and by the logistic ceiling, and the token count
    held out;
  - the share of each animal's 10 nearest neighbours that share its group, and that share a
    one-token name's token count;
  - the token-count probe and the "-fish" piece;
  - for each kind of animal whose kinship and way of life disagree, the layers where it leans to
    kin, or to its look-alikes, beyond chance.
- **Objects:** the three classes and the token count held out (k 3); the harm axis's held-out
  accuracy; where the dual-purpose objects sit.
- **Both:** each attribute's held-out probe κ from the axes analysis.

  .venv/bin/python docs/studies/read_site/analysis/compare_sites.py

Writes results/compare_sites.json and figures/compare_sites.png beside this file.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).parent
LAKE = ROOT / "data/lake"
ANIMAL_RESULTS = ROOT / "docs/studies/animals/analysis/results"
OBJECT_RESULTS = ROOT / "docs/studies/objects_harm/analysis/results"

SITES = {"last": "the word's last token", "end": "the end marker"}
ANIMALS = {"last": ("session_6e485e10", "animals-k8-n15"), "end": ("session_5ce62b52", "animals-end-k8-n15")}
OBJECTS = {"last": ("session_2be574c4", "objects-k3-n15"), "end": ("session_079e85fb", "objects-end-k3-n15")}
HARM = {"last": ("session_2be574c4", "harm-axis"), "end": ("session_079e85fb", "harm-axis-end")}
ANIMAL_K, OBJECT_K = "8", "3"
LAYERS = list(range(24))
COLOURS = {"last": "#1d4ed8", "end": "#d97706"}


def lens_json(session: str, lens: str, name: str) -> Any:
    return json.loads((LAKE / session / "lenses" / lens / name).read_text(encoding="utf-8"))


def result(folder: Path, name: str) -> Any:
    return json.loads((folder / f"{name}.json").read_text(encoding="utf-8"))


def heldout(validation: Dict[str, Any], k: str, attribute: str, score: str) -> List[float]:
    """A held-out score of the lens's nodes at k, per layer."""
    return [validation["layers"][str(layer)][k]["heldout"][attribute][score] for layer in LAYERS]


def ceiling(validation: Dict[str, Any], score: str) -> List[float]:
    """The logistic probe on the raw states, trained on the label, held out on the same folds."""
    return [validation["comparison"][str(layer)]["ceiling"][score] for layer in LAYERS]


def probe_kappa(axes: Dict[str, Any]) -> Dict[str, List[float]]:
    """Each attribute's held-out probe κ per layer (the axes analysis)."""
    rows = axes["scores"]["probe"]
    return {a: [rows[i]["real"][a] for i in range(len(axes["layers"]))] for a in axes["attributes"]}


def by_layer(results: Dict[str, Any], space: str, pick) -> List[float]:
    return [pick(results["spaces"][space][str(layer)]) for layer in LAYERS]


def animals(site: str) -> Dict[str, Any]:
    session, lens = ANIMALS[site]
    validation = lens_json(session, lens, "validation.json")
    taxonomy = result(ANIMAL_RESULTS, f"taxonomic_neighbourhoods_{lens}")
    split = result(ANIMAL_RESULTS, f"split_words_{lens}")
    kinship = result(ANIMAL_RESULTS, f"kinship_or_way_of_life_{lens}")
    out: Dict[str, Any] = {
        "session": session, "lens": lens,
        "group_nodes_ami": heldout(validation, ANIMAL_K, "label", "ami"),
        "group_nodes_kappa": heldout(validation, ANIMAL_K, "label", "kappa"),
        "group_ceiling_ami": ceiling(validation, "ami"),
        "tokens_nodes_ami": heldout(validation, ANIMAL_K, "tokens", "ami"),
        "tokens_nodes_kappa": heldout(validation, ANIMAL_K, "tokens", "kappa"),
        "neighbours": {},
        "kinship": {"all names": kinship["beyond_chance"],
                    "within token count": kinship["within_token_count"]["beyond_chance"]},
    }
    for space in ("lens", "raw"):
        out["neighbours"][space] = {
            "group": by_layer(taxonomy, space, lambda r: r["group"]["observed"]),
            "group_chance": by_layer(taxonomy, space, lambda r: r["group"]["chance"]),
            "one_token_with_one_token": by_layer(split, space, lambda r: r["same_count"]["one token"]["observed"]),
            "one_token_chance": by_layer(split, space, lambda r: r["same_count"]["one token"]["chance"]),
            "tokens_probe": by_layer(split, space, lambda r: r["tokens_probe"]),
            "fish_piece": by_layer(split, space, lambda r: r["fish_piece"]["fish"]["observed"]),
            "fish_piece_chance": by_layer(split, space, lambda r: r["fish_piece"]["fish"]["chance"]),
        }
    axes_path = LAKE / session / "lenses" / lens / "axes.json"
    if axes_path.exists():
        out["probe_kappa"] = probe_kappa(json.loads(axes_path.read_text(encoding="utf-8")))
    return out


def objects(site: str) -> Dict[str, Any]:
    session, lens = OBJECTS[site]
    validation = lens_json(session, lens, "validation.json")
    harm_session, harm_lens = HARM[site]
    harm = lens_json(harm_session, harm_lens, "validation.json")
    readings = result(OBJECT_RESULTS, f"harm_axis_{harm_lens}")
    out: Dict[str, Any] = {
        "session": session, "lens": lens, "harm_lens": harm_lens,
        "class_nodes_ami": heldout(validation, OBJECT_K, "label", "ami"),
        "class_ceiling_ami": ceiling(validation, "ami"),
        "tokens_nodes_ami": heldout(validation, OBJECT_K, "tokens", "ami"),
        "tokens_nodes_kappa": heldout(validation, OBJECT_K, "tokens", "kappa"),
        "harm_heldout_accuracy": [harm["layers"][str(layer)]["accuracy"] for layer in LAYERS],
        "harm_heldout_kappa": [harm["layers"][str(layer)]["kappa"] for layer in LAYERS],
        "dual_median": [q["median"] for q in readings["classes"]["dual"]],
        "dual_above_zero": readings["dual_above_zero"],
        "harm_best_layer": readings["best_layer"],
        "dual_ranked_at_best": readings["dual_ranked_at_best"],
    }
    axes_path = LAKE / session / "lenses" / lens / "axes.json"
    if axes_path.exists():
        out["probe_kappa"] = probe_kappa(json.loads(axes_path.read_text(encoding="utf-8")))
    return out


def span(values: List[float], layers: List[int]) -> str:
    picked = [values[layer] for layer in layers]
    return f"{min(picked):.2f} to {max(picked):.2f}"


def main() -> None:
    results = {"sites": SITES, "layers": LAYERS,
               "animals": {s: animals(s) for s in SITES}, "objects": {s: objects(s) for s in SITES}}
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / "compare_sites.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    chart(results)
    a, o = results["animals"], results["objects"]
    middle = list(range(4, 18))
    for s in SITES:
        n = a[s]["neighbours"]
        print(f"{SITES[s]}:")
        print(f"  animals, one-token names' neighbours that are one-token, every layer: lens "
              f"{span(n['lens']['one_token_with_one_token'], LAYERS)}, raw {span(n['raw']['one_token_with_one_token'], LAYERS)}")
        print(f"  animals, group's neighbour share L4-L17: lens {span(n['lens']['group'], middle)}, "
              f"raw {span(n['raw']['group'], middle)}")
        print(f"  animals, group held out L4-L17: nodes AMI {span(a[s]['group_nodes_ami'], middle)}, "
              f"ceiling AMI {span(a[s]['group_ceiling_ami'], middle)}")
        print(f"  animals, token count held out by the nodes (kappa), every layer: {span(a[s]['tokens_nodes_kappa'], LAYERS)}")
        print(f"  objects, token count held out by the nodes (kappa), every layer: {span(o[s]['tokens_nodes_kappa'], LAYERS)}")
        print(f"  objects, harm axis held-out accuracy L4-L15: {span(o[s]['harm_heldout_accuracy'], list(range(4, 16)))}; "
              f"best L{o[s]['harm_best_layer']}")
    print(f"wrote {out / 'compare_sites.json'}")


def chart(results: Dict[str, Any]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    a, o = results["animals"], results["objects"]
    fig, axes = plt.subplots(3, 3, figsize=(17, 13.5))

    def lines(ax, series, title, ylabel, chance=None, ylim=(0, 1)):
        for s in SITES:
            for values, style, tag in series(s):
                ax.plot(LAYERS, values, color=COLOURS[s], ls=style, lw=2 if style == "-" else 1.4,
                        label=f"{SITES[s]}{tag}")
        if chance is not None:
            ax.plot(LAYERS, chance, color="#6b7280", ls=":", lw=1.2, label="chance")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("layer")
        ax.set_ylabel(ylabel)
        ax.set_ylim(*ylim)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)

    lines(axes[0, 0], lambda s: [(a[s]["neighbours"]["lens"]["one_token_with_one_token"], "-", ", lens"),
                                 (a[s]["neighbours"]["raw"]["one_token_with_one_token"], "--", ", raw")],
          "Animals: one-token names' neighbours that are one-token names",
          "share of 10 nearest neighbours", chance=a["last"]["neighbours"]["lens"]["one_token_chance"])
    lines(axes[0, 1], lambda s: [(a[s]["tokens_nodes_kappa"], "-", ", animals (k 8)"),
                                 (o[s]["tokens_nodes_kappa"], "--", ", objects (k 3)")],
          "Whether the word split, read by the lens's nodes", "held-out κ", ylim=(-0.2, 1.05))
    lines(axes[0, 2], lambda s: [(a[s]["neighbours"]["raw"]["fish_piece"], "-", ", raw")],
          'The 18 fish named "…fish": neighbours whose name ends in "fish"', "share of 10 nearest neighbours",
          chance=a["last"]["neighbours"]["raw"]["fish_piece_chance"])
    lines(axes[1, 0], lambda s: [(a[s]["neighbours"]["lens"]["group"], "-", ", lens"),
                                 (a[s]["neighbours"]["raw"]["group"], "--", ", raw")],
          "Animals: neighbours sharing the animal's group", "share of 10 nearest neighbours",
          chance=a["last"]["neighbours"]["lens"]["group_chance"])
    lines(axes[1, 1], lambda s: [(a[s]["group_nodes_ami"], "-", ", the lens's nodes (k 8)"),
                                 (a[s]["group_ceiling_ami"], "--", ", logistic ceiling")],
          "Animals: the group on held-out orders", "held-out AMI", ylim=(-0.05, 1))
    lines(axes[1, 2], lambda s: [(o[s]["harm_heldout_accuracy"], "-", "")],
          "Objects: the harm axis on held-out domains", "held-out accuracy (benign vs harmful)",
          chance=[0.5] * len(LAYERS), ylim=(0.4, 1))

    kinds = list(a["last"]["kinship"]["all names"]["lens"].keys())
    for ax, space in ((axes[2, 0], "lens"), (axes[2, 1], "raw")):
        x = np.arange(len(kinds))
        for i, s in enumerate(SITES):
            beyond = a[s]["kinship"]["all names"][space]
            kin = [len(beyond[k]["kin"]) for k in kinds]
            look = [-len(beyond[k]["look-alikes"]) for k in kinds]
            ax.bar(x + (i - 0.5) * 0.38, kin, width=0.36, color=COLOURS[s], label=f"{SITES[s]}: to kin")
            ax.bar(x + (i - 0.5) * 0.38, look, width=0.36, color=COLOURS[s], alpha=0.45, hatch="//",
                   label=f"{SITES[s]}: to look-alikes")
        ax.axhline(0, color="#374151", lw=0.8)
        ax.set_xticks(x, [k.replace(", not ", ",\nnot ").replace(" that ", "\nthat ") for k in kinds], fontsize=8)
        ax.set_ylabel("layers beyond chance (of 24)")
        ax.set_ylim(-24, 24)
        ax.set_title(f"Kinship or way of life ({'the lens' if space == 'lens' else 'raw space'}): where each kind leans",
                     fontsize=11)
        ax.grid(alpha=0.25, axis="y")
        ax.legend(fontsize=7, loc="lower left")

    ax = axes[2, 2]
    groups = [("animals", a, ("label", "habitat", "movement", "diet", "wild_or_domestic", "tokens")),
              ("objects", o, ("label", "harm", "tokens"))]
    names, ticks = [], []
    position = 0.0
    middle = list(range(4, 24))
    for set_name, block, attributes in groups:
        start = position
        for attribute in attributes:
            for i, s in enumerate(SITES):
                kappa = block[s].get("probe_kappa", {}).get(attribute)
                if kappa is None:
                    continue
                ax.bar(position + (i - 0.5) * 0.38, float(np.mean([kappa[layer] for layer in middle])), width=0.36,
                       color=COLOURS[s], label=SITES[s] if not names else None)
            names.append("group" if (set_name == "animals" and attribute == "label") else
                         "class" if attribute == "label" else attribute.replace("wild_or_domestic", "wild or\ndomestic"))
            ticks.append(position)
            position += 1.25
        ax.text((start + position - 1.25) / 2, -0.25, set_name, transform=ax.get_xaxis_transform(), ha="center",
                fontsize=9, fontweight="bold")
        position += 0.6
    ax.set_xticks(ticks, names, fontsize=8, rotation=30, ha="right", rotation_mode="anchor")
    ax.set_ylabel("held-out probe κ, mean over L4–L23")
    ax.set_ylim(0, 1.05)
    ax.set_title("A linear probe on each attribute (the axes analysis)", fontsize=11)
    ax.grid(alpha=0.25, axis="y")
    ax.legend(fontsize=8)

    fig.suptitle("Where a single word is read: its last token, or the end marker after it "
                 "(the same lenses, settings and folds at both sites)", fontsize=13)
    fig.tight_layout()
    figures = HERE / "figures"
    figures.mkdir(exist_ok=True)
    fig.savefig(figures / "compare_sites.png", dpi=150)


if __name__ == "__main__":
    main()
