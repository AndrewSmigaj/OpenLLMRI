"""Attention, word by word, on the tank sentences: what the read token " tank" drew on at each layer,
for each sense, for each branch where the lens's nodes part, and for the expert nodes that the
sentence's own attention fills (read-only; the proposal in docs/design/design.md#attention;
docs/research/attention_and_experts.md, "Attention, word by word").

It reads the per-source parts that cpu_pass.py keeps (data/lake/<session>/studies/
attention_cpu_pass.npz) and works out:
- **weights against amounts:** at each layer, the heads' mean weight on the sentence's first token
  and on " tank" itself, beside those positions' share of the amount attention drew (the norms of
  their parts), and the sinks' share of the weight;
- **what each item drew on:** each word's share of the amount, its pieces summed, at each layer (a
  word's share is 0 in a sentence without it). " tank" itself is kept apart;
- **words beyond chance for a group of items:** the mean share in the group minus the mean share in
  the rest of a pool, for every word in at least 3 of the group's items; the group is shuffled
  within the pool 1,000 times, and a word counts when it beats the 95th percentile of the largest
  difference any word reaches in a shuffle (at that layer, or over the layers tested together).
  Beside it, the same for the word's presence alone (is the word simply commoner in the group);
- **picked words:** whether the three words each sentence drew on most (its first word left out) carry
  its sense: a held-out logistic regression from those words to the sense, against three words
  picked at random from the same sentence and against all its words;
- **senses:** each sense against the other four, at every layer; split-half agreement (Spearman,
  over words, between two random halves of the items) and the agreement of the two measures (the
  amount, and the signed share of attention's output) over the same words;
- **roles:** the share drawn from the read word itself, the token just before it, the first token
  and the other words, for each sense and each branch, tested the same way (both directions);
- **traced back** (an approximation, for the test): every position's state split among the
  positions it came from, by the lengths of its parts, chained from layer 0, so a word the read
  token reaches through another position counts;
- **branches:** at every split point of the tank lens, each branch against the node's other items,
  over the layers up to the one where the branch's items arrive, tested together;
- **expert nodes:** for the expert nodes the routing study found filled by the item's own attention
  (results/routing_tank.json), each word's push toward the expert (its part of the expert's router
  score minus its mean part over the 32 experts), the node's items against the layer's other items;
  and how much of the node's lead for its expert came from that layer's attention and how much from
  the state the layer started from.

Usage, from the repo root, after cpu_pass.py tank:
  .venv/bin/python docs/studies/attention_experts/analysis/attention_words.py
writes results/attention_words_tank.json and figures/attention_words_*.png.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
from common import LAKE, MODEL, RESULTS, figure_path, load_capture, stream, write_results
from scipy.stats import spearmanr

SHUFFLES = 1000
MIN_ITEMS = 5  # a word enters the analysis when at least this many items hold it
MIN_IN_GROUP = 3  # and is tested for a group when at least this many of the group's items hold it
TOP = 6


def word_spans(tokens: Sequence[int], read: int, decode) -> List[Tuple[str, List[int]]]:
    """The words before the read token: (key, positions). A word starts at the first token, at a token
    whose text starts with a space, and at punctuation; its key is its text, stripped and lowercased."""
    words: List[Tuple[str, List[int]]] = []
    for pos in range(read):
        piece = decode([tokens[pos]])
        starts = pos == 0 or piece[:1].isspace() or not piece.strip().isalnum() or not words
        if starts or not words[-1][0][-1:].isalnum():
            words.append((piece, [pos]))
        else:
            words[-1] = (words[-1][0] + piece, words[-1][1] + [pos])
    return [(text.strip().lower(), positions) for text, positions in words]


def by_word(values: np.ndarray, spans: List[List[Tuple[str, List[int]]]], vocab: Dict[str, int]) -> np.ndarray:
    """[items, layers, sources] -> [items, layers, words]: each word's positions summed."""
    out = np.zeros((values.shape[0], values.shape[1], len(vocab)))
    for b, item in enumerate(spans):
        for key, positions in item:
            if key in vocab:
                out[b, :, vocab[key]] += np.nansum(values[b, :, positions], axis=0)
    return out


def beyond(stat_of, values: np.ndarray, group: np.ndarray, pool: np.ndarray, eligible: np.ndarray,
           rng: np.random.Generator, two_sided: bool = False) -> Tuple[np.ndarray, float]:
    """The group's mean minus the pool's other items' mean, per word (values: [items, ..., words];
    the leading axes after items are tested together), and the 95th percentile of the largest
    difference any eligible word reaches when the group is shuffled within the pool (its size either
    way, with two_sided)."""
    idx = np.nonzero(pool)[0]
    x = values[idx].reshape(len(idx), -1)
    k = int(group[idx].sum())
    real = stat_of(x, group[idx])
    mask = np.tile(eligible, x.shape[1] // len(eligible))
    tops = []
    for _ in range(SHUFFLES):
        g = np.zeros(len(idx), dtype=bool)
        g[rng.choice(len(idx), k, replace=False)] = True
        shuffled = stat_of(x, g)
        tops.append(np.max(np.where(mask, np.abs(shuffled) if two_sided else shuffled, -np.inf)))
    return real.reshape(values.shape[1:]), float(np.percentile(tops, 95))


ROLES = ("the read word itself", "the token just before it", "the first token", "the other words")


def roles(amount: np.ndarray, reads: np.ndarray) -> np.ndarray:
    """[items, layers, sources] amounts -> [items, layers, 4] shares by role (ROLES)."""
    out = np.zeros((amount.shape[0], amount.shape[1], len(ROLES)))
    for b, r in enumerate(reads.tolist()):
        a = amount[b, :, : r + 1].astype(np.float64)
        a = a / a.sum(axis=1, keepdims=True)
        out[b, :, 0] = a[:, r]
        out[b, :, 1] = a[:, r - 1] if r >= 1 else 0.0
        out[b, :, 2] = a[:, 0] if r >= 2 else 0.0
        out[b, :, 3] = 1.0 - out[b, :, :3].sum(axis=1)
    return out


def composed(maps: np.ndarray, residual: np.ndarray, reads: np.ndarray) -> np.ndarray:
    """Attention's amounts traced back through the layers (an approximation, for the test): at each
    layer every position's state is split among the positions it came from in proportion to the
    lengths of its parts (its own state before the layer, plus each position's part of attention),
    and the splits are chained from layer 0. The experts work on each position alone, so they move
    nothing between positions. Returns [items, layers, sources]: the read token's state at each
    layer, by the token it came from."""
    n, layers, width, _ = maps.shape
    out = np.full((n, layers, width), np.nan)
    for b, r in enumerate(reads.tolist()):
        chain = np.eye(r + 1)
        for li in range(layers):
            mix = maps[b, li, : r + 1, : r + 1].astype(np.float64)
            mix = np.nan_to_num(mix) + np.diag(residual[b, li, : r + 1].astype(np.float64))
            mix = mix / mix.sum(axis=1, keepdims=True)
            chain = mix @ chain
            out[b, li, : r + 1] = chain[r]
    return out


def picked_words(amount: np.ndarray, spans: List[List[Tuple[str, List[int]]]], layer: int, count: int,
                 rng: np.random.Generator) -> Tuple[List[List[str]], List[List[str]], List[List[str]]]:
    """Per item: the `count` words it drew on most at a layer, `count` words picked at random, and all
    its words; the sentence's first word is left out of all three (the first token often takes a
    large amount whatever it is)."""
    top, random, every = [], [], []
    for b, item in enumerate(spans):
        words = [(key, float(np.nansum(amount[b, layer, positions]))) for key, positions in item if positions[0] != 0]
        keys = [k for k, _ in words]
        top.append([k for k, _ in sorted(words, key=lambda w: -w[1])[:count]])
        random.append([keys[i] for i in rng.permutation(len(keys))[:count]])
        every.append(keys)
    return top, random, every


def predictiveness(bags: List[List[str]], labels: np.ndarray) -> float:
    """Held-out balanced accuracy of a logistic regression from bags of words to the labels (five
    stratified folds)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    vocab = {w: i for i, w in enumerate(sorted({w for bag in bags for w in bag}))}
    x = np.zeros((len(bags), len(vocab)))
    for b, bag in enumerate(bags):
        for w in bag:
            x[b, vocab[w]] = 1.0
    folds = StratifiedKFold(5, shuffle=True, random_state=1)
    guess = cross_val_predict(LogisticRegression(max_iter=2000, C=1.0), x, labels, cv=folds)
    return float(balanced_accuracy_score(labels, guess))


def difference(x: np.ndarray, g: np.ndarray) -> np.ndarray:
    return x[g].mean(axis=0) - x[~g].mean(axis=0)


def listing(stat: np.ndarray, line: float, eligible: np.ndarray, words: List[str], presence: np.ndarray) -> List[Dict[str, Any]]:
    order = [w for w in np.argsort(-stat) if eligible[w] and stat[w] > line]
    return [{"word": words[w], "difference": round(float(stat[w]), 4), "presence_difference": round(float(presence[w]), 3)}
            for w in order[:TOP]]


def run() -> Dict[str, Any]:
    from tokenizers import Tokenizer

    from services.lenses.data import load_routing
    from services.lenses.splits import branches_of, split_points

    cap = load_capture("tank")
    data = np.load(LAKE / cap.session / "studies" / "attention_cpu_pass.npz")
    assert list(data["probe_ids"]) == [item["probe_id"] for item in cap.items]
    tokenizer = Tokenizer.from_file(str(MODEL / "tokenizer.json"))
    decode = lambda ids: tokenizer.decode(list(ids))  # noqa: E731
    reads, token_ids, layers = data["reads"], data["token_ids"], [int(x) for x in data["layers"]]
    amount, share, weight, push, sink = (data[k] for k in ("amount", "share", "weight", "push", "sink"))
    n = len(reads)
    spans = [word_spans(token_ids[b], int(reads[b]), decode) for b in range(n)]
    counts: Dict[str, int] = {}
    for item in spans:
        for key in {k for k, _ in item}:
            counts[key] = counts.get(key, 0) + 1
    words = sorted(k for k, c in counts.items() if c >= MIN_ITEMS)
    vocab = {w: i for i, w in enumerate(words)}
    total = np.nansum(amount, axis=2, keepdims=True)
    draw = by_word(amount / total, spans, vocab)  # [items, layers, words]
    signed = by_word(share, spans, vocab)
    presence = np.zeros((n, len(words)), dtype=bool)
    for b, item in enumerate(spans):
        for key, _ in item:
            if key in vocab:
                presence[b, vocab[key]] = True
    self_share = np.array([amount[b, :, reads[b]] / total[b, :, 0] for b in range(n)])  # [items, layers]
    role_share = roles(amount, reads)
    traced = composed(data["maps"], data["residual"], reads)
    others = traced.copy()
    for b, r in enumerate(reads.tolist()):
        others[b, :, r] = 0.0
    others = others / np.nansum(others, axis=2, keepdims=True)  # the traced shares of the other tokens
    traced_draw = by_word(others, spans, vocab)
    labels = cap.labels
    senses = sorted(set(labels))
    everyone = np.ones(n, dtype=bool)

    # Weights against amounts
    first_weight = np.array([weight[b, :, 0] for b in range(n)])
    first_amount = np.array([amount[b, :, 0] / total[b, :, 0] for b in range(n)])
    self_weight = np.array([weight[b, :, reads[b]] for b in range(n)])
    weights_vs = [{"layer": layers[li], "first_token_weight": float(np.median(first_weight[:, li])),
                   "first_token_amount": float(np.median(first_amount[:, li])),
                   "self_weight": float(np.median(self_weight[:, li])), "self_amount": float(np.median(self_share[:, li])),
                   "sink_weight": float(np.median(sink[:, li]))} for li in range(len(layers))]

    # Senses, layer by layer
    sense_rows: Dict[str, Any] = {}
    for si, sense in enumerate(senses):
        group = labels == sense
        eligible = presence[group].sum(axis=0) >= MIN_IN_GROUP
        pres = difference(presence.astype(float), group)
        rows = []
        for li in range(len(layers)):
            stat, line = beyond(difference, draw[:, li], group, everyone, eligible, stream(7, si, li))
            halves = stream(8, si, li).permutation(n) < n // 2
            a = difference(draw[halves, li], group[halves])
            b = difference(draw[~halves, li], group[~halves])
            s_stat = difference(signed[:, li], group)
            t_stat, t_line = beyond(difference, traced_draw[:, li], group, everyone, eligible, stream(11, si, li))
            ta = difference(traced_draw[halves, li], group[halves])
            tb = difference(traced_draw[~halves, li], group[~halves])
            r_stat = difference(role_share[:, li], group)
            rows.append({"layer": layers[li], "line": round(line, 4), "beyond": int(np.sum(eligible & (stat > line))),
                         "traced_beyond": int(np.sum(eligible & (t_stat > t_line))),
                         "traced_split_half_spearman": float(spearmanr(ta[eligible], tb[eligible]).statistic),
                         "traced_top": listing(t_stat, t_line, eligible, words, pres),
                         "roles_difference": {role: round(float(v), 4) for role, v in zip(ROLES, r_stat)},
                         "split_half_spearman": float(spearmanr(a[eligible], b[eligible]).statistic),
                         "amount_vs_signed_spearman": float(spearmanr(stat[eligible], s_stat[eligible]).statistic),
                         "top": listing(stat, line, eligible, words, pres)})
        sense_rows[sense] = rows

    # Branches where the lens's nodes part: the layers up to the branch's own, tested together
    branch_rows = []
    for which, (layer, node, _) in enumerate(split_points(cap)):
        li = cap.layers.index(layer)
        pool = cap.nodes[:, li] == node
        for bi, (branch, size) in enumerate(branches_of(cap, li, node)):
            group = pool & (cap.nodes[:, li + 1] == branch)
            r_stat, r_line = beyond(difference, role_share[:, : li + 2], group, pool, np.ones(len(ROLES), bool),
                                    stream(12, which, bi), two_sided=True)
            role_hits = [(layers[lj], ROLES[k], round(float(r_stat[lj, k]), 3)) for lj in range(li + 2)
                         for k in range(len(ROLES)) if r_stat[lj, k] > r_line or -r_stat[lj, k] > r_line]
            eligible = presence[group].sum(axis=0) >= MIN_IN_GROUP
            if not eligible.any():
                branch_rows.append({"layer": layer, "node": node, "branch": branch, "items": size, "words": 0,
                                    "roles": role_hits})
                continue
            stat, line = beyond(difference, draw[:, : li + 2], group, pool, eligible, stream(9, which, bi))
            best = np.max(np.where(eligible[None, :], stat, -np.inf), axis=1)
            hits = [(layers[lj], words[w], float(stat[lj, w])) for lj in range(li + 2) for w in range(len(words))
                    if eligible[w] and stat[lj, w] > line]
            top_words = sorted({w for _, w, _ in hits}, key=lambda w: -max(s for _, ww, s in hits if ww == w))[:TOP]
            branch_rows.append({"layer": layer, "node": node, "branch": branch, "items": size, "pool": int(pool.sum()),
                                "line": round(line, 4), "words": len({w for _, w, _ in hits}), "top": top_words,
                                "layers_with_words": sorted({hit[0] for hit in hits}),
                                "labels": {s: int((group & (labels == s)).sum()) for s in senses}, "roles": role_hits,
                                "best_layer": layers[int(np.argmax(best))]})

    # Expert nodes the item's own attention fills
    routing = json.loads((RESULTS / "routing_tank.json").read_text(encoding="utf-8"))
    stored = load_routing(cap.session, [item["probe_id"] for item in cap.items], 1)
    expert_rows = []
    chosen = [nd for nd in routing["nodes"] if nd.get("beyond_chance") and nd["share"] > nd["layer_share"]]
    for which, nd in enumerate(sorted(chosen, key=lambda x: -(x["share"] - x["layer_share"]))[:8]):
        li, e = layers.index(nd["layer"]), nd["expert"]
        first = np.argsort(-stored[:, nd["layer"]], axis=1, kind="stable")[:, 0]
        group = first == e
        with np.errstate(invalid="ignore"):
            relative = push[:, li, :, e] - np.nanmean(push[:, li], axis=2)  # [items, sources]
        word_push = by_word(relative[:, None, :], spans, vocab)[:, 0]
        eligible = presence[group].sum(axis=0) >= MIN_IN_GROUP
        stat, line = beyond(difference, word_push, group, everyone, eligible, stream(10, which))
        expert_rows.append({"layer": nd["layer"], "expert": e, "items": int(group.sum()), "brought": nd["brought"],
                            "labels": nd["labels"], "line": round(line, 4),
                            "top": listing(stat, line, eligible, words, difference(presence.astype(float), group))})

    # Do the words each sentence drew on most carry its sense? (held out, against random words)
    picked = []
    for li in range(len(layers)):
        top, rand, every = picked_words(amount, spans, li, 3, stream(13, li))
        t_top, _, _ = picked_words(np.nan_to_num(others), spans, li, 3, stream(14, li))
        picked.append({"layer": layers[li], "top3": predictiveness(top, labels), "random3": predictiveness(rand, labels),
                       "traced_top3": predictiveness(t_top, labels), "all_words": predictiveness(every, labels)})

    examples = []
    for b in [i for i in range(n) if labels[i] in ("vehicle", "aquarium", "septic") and 8 <= reads[i] <= 12][:9]:
        r, pieces = int(reads[b]), [decode([t]) for t in token_ids[b][: int(reads[b]) + 1]]
        layer_rows = []
        for li in (0, 2, 5, 9, 14, 20):
            a = amount[b, li, : r + 1] / np.nansum(amount[b, li, : r + 1])
            top = [int(j) for j in np.argsort(-a)[:4]]
            back = []
            for j in [j for j in top if j != r][:1]:
                if li >= 1:
                    m = data["maps"][b, li - 1, j, : j + 1].astype(np.float64)
                    m = m / m.sum()
                    back = [(pieces[k].strip(), round(float(m[k]), 2)) for k in np.argsort(-m)[:3]]
            t = others[b, li, : r + 1]
            layer_rows.append({"layer": layers[li], "drew_on": [(pieces[j].strip(), round(float(a[j]), 2)) for j in top],
                               "its_top_word_one_layer_earlier_drew_on": back,
                               "traced": [(pieces[j].strip(), round(float(t[j]), 2)) for j in np.argsort(-np.nan_to_num(t))[:4]]})
        examples.append({"label": str(labels[b]), "text": "".join(pieces), "layers": layer_rows})
    traced_self = [float(np.median([traced[b, li, reads[b]] for b in range(n)])) for li in range(len(layers))]
    traced_first = [[float(np.percentile(others[:, li, 0], q)) for q in (25, 50, 75)] for li in range(len(layers))]

    payload = {"capture": "tank", "session": cap.session, "lens": cap.lens, "items": n, "words": len(words),
               "roles": list(ROLES), "traced_self_median": traced_self, "traced_first_token_quartiles": traced_first, "examples": examples, "picked_words": picked,
               "shuffles": SHUFFLES, "weights_vs_amounts": weights_vs, "senses": sense_rows,
               "branches": branch_rows, "expert_nodes": expert_rows}
    write_results("attention_words_tank", payload)
    figures(cap, spans, amount / total, self_share, layers, payload, decode, token_ids, reads)
    return payload


def figures(cap, spans, amount_of, self_share, layers, payload, decode, token_ids, reads) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # One sentence per sense: its words x layers (the attention row's view of a selected item)
    picks = []
    for sense in ("aquarium", "vehicle", "septic"):
        idx = [b for b in range(len(spans)) if cap.labels[b] == sense and 9 <= len(spans[b]) <= 13]
        picks.append(idx[0])
    fig, axes = plt.subplots(len(picks), 1, figsize=(13, 10))
    for ax, b in zip(axes, picks):
        rows = [key for key, _ in spans[b]] + ["tank (itself)"]
        grid = np.vstack([item_rows(amount_of[b], spans[b]), self_share[b][None, :]])
        im = ax.imshow(grid, aspect="auto", cmap="Blues", vmin=0, vmax=max(0.3, float(np.nanmax(grid[:-1]))))
        ax.set_yticks(range(len(rows)), rows, fontsize=8)
        ax.set_xticks(range(len(layers)), [str(x) for x in layers], fontsize=7)
        ax.set_title(f"{cap.labels[b]}: \"{decode(token_ids[b][: reads[b] + 1]).strip()}…\"", fontsize=10, loc="left")
        fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01, label="share of the amount")
    axes[-1].set_xlabel("layer")
    fig.suptitle("What \" tank\" drew on, word by word and layer by layer (each column sums to 1 with the "
                 "words not shown)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(figure_path("attention_words_items"), dpi=130)
    plt.close(fig)

    # Weights against amounts
    w = payload["weights_vs_amounts"]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(layers, [r["first_token_weight"] for r in w], color="#ee6666", ls="--", label="first token: weight")
    ax.plot(layers, [r["first_token_amount"] for r in w], color="#ee6666", label="first token: share of the amount")
    ax.plot(layers, [r["self_weight"] for r in w], color="#5470c6", ls="--", label="\" tank\" itself: weight")
    ax.plot(layers, [r["self_amount"] for r in w], color="#5470c6", label="\" tank\" itself: share of the amount")
    ax.plot(layers, [r["sink_weight"] for r in w], color="#999999", ls=":", label="the heads' sinks: weight")
    ax.set_xlabel("layer")
    ax.set_ylabel("median over the 499 sentences")
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, ncol=2)
    ax.set_title("Where attention's weight goes, and where the amount it draws comes from", fontsize=10)
    fig.tight_layout()
    fig.savefig(figure_path("attention_words_weights"), dpi=130)
    plt.close(fig)


def item_rows(shares: np.ndarray, spans: List[Tuple[str, List[int]]]) -> np.ndarray:
    """One item's words x layers: each word's share of the amount ([layers, sources] in)."""
    return np.array([np.nansum(shares[:, positions], axis=1) for _, positions in spans])


if __name__ == "__main__":
    result = run()
    for sense, rows in result["senses"].items():
        print(sense, [(r["layer"], [t["word"] for t in r["top"][:4]]) for r in rows if r["layer"] in (0, 2, 5, 10, 16, 23)])
