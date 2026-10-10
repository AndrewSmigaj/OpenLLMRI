"""Words that split, layer by layer (the animal study, 10d.5).

A name that splits into several tokens is read at its last token (DESIGN.md C1). Three questions:

1. **The last piece:** do split names group by their last piece in early layers (goldfish,
   catfish, starfish all end in "fish")? For every split name whose last piece another split name
   shares, the share of its 10 nearest neighbours ending in the same piece, against chance (the
   set's share of such names); and for the "-fish" names, fish and not fish apart.
2. **How early the token count is read:** a logistic probe on one token against several, held
   out (5 folds, stratified), at every layer.
3. **When split names sit with their kin:** the share of the 10 nearest neighbours in the same
   group, for split names and one-token names, against chance; beside it, the share of neighbours
   with the same token count (one or several), which says how far the token count shapes the
   neighbourhoods.

Three spaces: the lens's own embedding, the residual stream in the validation's raw recipe, and the same
with each token count's mean taken out first (an offset between one-token and split names removed).

  .venv/bin/python docs/studies/animals/analysis/split_words.py SESSION LENS
"""
from __future__ import annotations

import sys
from collections import Counter
from typing import Any, Dict, List

import numpy as np
from common import (
    NEIGHBOURS,
    ROOT,
    SEED,
    figure_path,
    lens_embedding,
    lens_items,
    neighbours,
    raw_layers,
    write_results,
)


def last_pieces(words: List[str]) -> List[str]:
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(ROOT / "data/models/gpt-oss-20b")
    return [tokenizer.decode(tokenizer.encode(" " + w, add_special_tokens=False)[-1:]) for w in words]


def piece_share(nn: np.ndarray, pieces: np.ndarray, who: np.ndarray) -> Dict[str, float]:
    """For the items in `who`: the mean share of their neighbours with the same last piece, and
    chance (the mean share of the other items with it)."""
    same = pieces[nn[who]] == pieces[who][:, None]
    others = np.array([(pieces == pieces[i]).sum() - 1 for i in who])
    return {"observed": float(same.mean()), "chance": float(np.mean(others / (len(pieces) - 1)))}


def probe(points: np.ndarray, target: np.ndarray) -> float:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    return float(balanced_accuracy_score(target, cross_val_predict(model, points, target, cv=folds)))


def kin_share(nn: np.ndarray, group: np.ndarray, who: np.ndarray) -> Dict[str, float]:
    same = group[nn[who]] == group[who][:, None]
    others = np.array([(group == group[i]).sum() - 1 for i in who])
    return {"observed": float(same.mean()), "chance": float(np.mean(others / (len(group) - 1)))}


def main(session: str, lens: str) -> None:
    items = lens_items(session, lens)
    words = [it["entry"]["target_word"] for it in items]
    group = np.array([it["entry"]["group"] for it in items])
    split = np.array([it["entry"]["categories"]["tokens"] == "several" for it in items])
    recorded = np.array([int(it["target_token_count"] or 1) for it in items])
    if not np.array_equal(split, recorded > 1):
        raise SystemExit("the capture's token counts disagree with the set's tokens category")
    pieces = np.array(last_pieces(words), dtype=object)
    shared = Counter(pieces[split])
    with_partner = np.flatnonzero(split & np.array([shared[p] > 1 for p in pieces]))
    fish_piece = np.array([p.strip() == "fish" for p in pieces]) & split
    fish_names = {"fish": np.flatnonzero(fish_piece & (group == "fish")),
                  "not fish": np.flatnonzero(fish_piece & (group != "fish"))}
    embedding = lens_embedding(session, lens)
    layers = list(range(embedding.shape[0]))
    raw = raw_layers(session, [it["probe_id"] for it in items], layers)
    centred = raw_layers(session, [it["probe_id"] for it in items], layers, centre_within=split)
    results: Dict[str, Any] = {
        "session": session, "lens": lens, "items": len(items), "neighbours": NEIGHBOURS,
        "split": int(split.sum()), "one_token": int((~split).sum()),
        "shared_pieces": {p: n for p, n in shared.most_common() if n > 1},
        "fish_piece_names": {k: [words[i] for i in v] for k, v in fish_names.items()},
        "spaces": {"lens": {}, "raw": {}, "raw, token count centred": {}}}
    for layer in layers:
        for space, points in (("lens", embedding[layer]), ("raw", raw[layer]),
                              ("raw, token count centred", centred[layer])):
            nn = neighbours(points)
            results["spaces"][space][layer] = {
                "last_piece": piece_share(nn, pieces, with_partner),
                "fish_piece": {k: piece_share(nn, pieces, v) for k, v in fish_names.items() if len(v)},
                # not in the centred space: its group means use every item, held-out ones included
                "tokens_probe": None if space == "raw, token count centred" else probe(points, split.astype(int)),
                "kin": {"split": kin_share(nn, group, np.flatnonzero(split)),
                        "one token": kin_share(nn, group, np.flatnonzero(~split))},
                "same_count": {"split": kin_share(nn, split, np.flatnonzero(split)),
                               "one token": kin_share(nn, split, np.flatnonzero(~split))},
            }
        lens_row = results["spaces"]["lens"][layer]
        print(f"L{layer:02d} lens: last piece {lens_row['last_piece']['observed']:.2f} "
              f"(chance {lens_row['last_piece']['chance']:.2f}); tokens probe {lens_row['tokens_probe']:.2f}; "
              f"kin split {lens_row['kin']['split']['observed']:.2f}, one token {lens_row['kin']['one token']['observed']:.2f}")
    path = write_results(f"split_words_{lens}", results)
    chart(results, lens)
    print(f"wrote {path}")


def chart(results: Dict[str, Any], lens: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    spaces = (("lens", "the lens's embedding"), ("raw", "raw: standardized, 50 PCs"),
              ("raw, token count centred", "raw, each token count's\nmean taken out"))
    fig, axes = plt.subplots(len(spaces), 3, figsize=(15, 11.5), sharex=True)
    for row, (space, title) in enumerate(spaces):
        by_layer = results["spaces"][space]
        layers = sorted(int(k) for k in by_layer)
        ax = axes[row][0]
        ax.plot(layers, [by_layer[x]["last_piece"]["observed"] for x in layers], color="#1d4ed8", lw=2,
                label="split names sharing a last piece")
        ax.plot(layers, [by_layer[x]["last_piece"]["chance"] for x in layers], color="#1d4ed8", lw=1, ls=":")
        for kind, colour in (("fish", "#059669"), ("not fish", "#dc2626")):
            if kind in by_layer[layers[0]]["fish_piece"]:
                ax.plot(layers, [by_layer[x]["fish_piece"][kind]["observed"] for x in layers], color=colour, lw=1.5,
                        label=f'"-fish" names, {kind}')
        ax.set_ylabel(f"{title}\nshare of neighbours, same last piece")
        ax.set_ylim(0, 1)
        ax.legend(fontsize=8)
        ax = axes[row][1]
        if by_layer[layers[0]]["tokens_probe"] is None:
            ax.text(0.5, 0.5, "not read here: the centring\nused every item", ha="center", va="center",
                    transform=ax.transAxes, fontsize=9, color="#6b7280")
        else:
            ax.plot(layers, [by_layer[x]["tokens_probe"] for x in layers], color="#7c3aed", lw=2)
        ax.axhline(0.5, color="#374151", lw=0.8, ls=":")
        ax.set_ylim(0.4, 1.0)
        ax.set_ylabel("balanced accuracy, held out")
        ax = axes[row][2]
        for kind, colour in (("split", "#d97706"), ("one token", "#0891b2")):
            ax.plot(layers, [by_layer[x]["kin"][kind]["observed"] for x in layers], color=colour, lw=2,
                    label=f"{kind}: same group")
            ax.plot(layers, [by_layer[x]["kin"][kind]["chance"] for x in layers], color=colour, lw=1, ls=":")
        ax.plot(layers, [by_layer[x]["same_count"]["one token"]["observed"] for x in layers], color="#0891b2",
                lw=1.2, ls="--", label="one token: same token count")
        ax.plot(layers, [by_layer[x]["same_count"]["one token"]["chance"] for x in layers], color="#0891b2", lw=0.8, ls=":")
        ax.set_ylim(0, 1)
        ax.set_ylabel("share of neighbours in the same group")
        ax.legend(fontsize=8)
        for ax in axes[row]:
            ax.grid(alpha=0.25)
    axes[0][0].set_title("1. grouping by the last piece")
    axes[0][1].set_title("2. one token or several, read by a probe")
    axes[0][2].set_title("3. split names with their kin")
    for ax in axes[-1]:
        ax.set_xlabel("layer")
    fig.suptitle(f"Words that split: {lens} ({results['split']} split, {results['one_token']} one token; dotted: chance)",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(figure_path(f"split_words_{lens}"), dpi=150)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
