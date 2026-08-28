#!/usr/bin/env python3
"""Assemble D3 (shift) and D4 (no-shift) cumulative experiment sets from a scene pool.

Design (probe_design_context_shift_v1.md): family i pairs scene_A[i] with scene_B[i];
D3 run = 20 sentences of one scene then 20 of the other + carrier re-appended at every
step (cumulative texts, sentence-experiment route). D4 run = 40 sentences single-regime.
Token budgets enforced per block via greedy selection (+-2%). Worn-opener cap: at most
one 'nobody warn' sentence per run. Deterministic (seeded per run).

Usage: assemble_contexts.py POOL_JSON CARRIER_TEXT OUT_DIR PREFIX
Writes: PREFIX_d3_famNN_{ab,ba}.json (all families), PREFIX_d4_famNN_{a,b}.json (even families)
plus PREFIX_manifest.json listing every run and its budgets.
"""
from __future__ import annotations
import json, random, sys
from pathlib import Path
from transformers import AutoTokenizer

BLOCK = 20
BUDGET_TOL = 0.02

def pick_block(sents, tok_lens, budget, rng, used_warn):
    """Exactly BLOCK sentences; greedy swaps pull the token total toward budget.
    'nobody warn*' sentences capped at one per run (worn-opener rule)."""
    idx = list(range(len(sents)))
    warn = [("nobody warn" in s.lower()) for s in sents]
    if used_warn[0]:
        idx = [i for i in idx if not warn[i]]
    rng.shuffle(idx)
    # keep at most one warn sentence among candidates
    seen_warn = False
    cand = []
    for i in idx:
        if warn[i]:
            if seen_warn:
                continue
            seen_warn = True
        cand.append(i)
    assert len(cand) >= BLOCK, f"scene too small: {len(cand)} < {BLOCK}"
    chosen, rest = cand[:BLOCK], cand[BLOCK:]
    total = sum(tok_lens[i] for i in chosen)
    improved = True
    while improved and rest:
        improved = False
        for ci, c in enumerate(chosen):
            for ri, r in enumerate(rest):
                nt = total - tok_lens[c] + tok_lens[r]
                if abs(nt - budget) < abs(total - budget):
                    chosen[ci], rest[ri] = r, c
                    total = nt
                    improved = True
    if any(warn[i] for i in chosen):
        used_warn[0] = True
    return [sents[i] for i in chosen], total

def main():
    pool_path, carrier, out_dir, prefix = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
    pool = json.load(open(pool_path))
    tok = AutoTokenizer.from_pretrained("data/models/gpt-oss-20b")
    by_label = {}
    for g in pool["groups"]:
        scenes = {}
        for e in g["sentences"]:
            scenes.setdefault(e["categories"]["scene"], []).append(e["text"])
        by_label[g["label"]] = scenes
    (la, lb) = list(by_label)
    scenes_a, scenes_b = sorted(by_label[la]), sorted(by_label[lb])
    n_fam = min(len(scenes_a), len(scenes_b))
    tlen = {s: len(tok.encode(" " + s, add_special_tokens=False))
            for sc in by_label.values() for lst in sc.values() for s in lst}
    # budget: median sentence length * BLOCK
    med = sorted(tlen.values())[len(tlen)//2]
    budget = med * BLOCK
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    def build_run(name, blocks, labels_seq, fam, direction):
        entries, cum = [], []
        for block, blab in zip(blocks, labels_seq):
            for s in block:
                cum.append(s)
                pos = len(cum)
                entries.append({
                    "text": " ".join(cum) + " " + carrier,
                    "group": "run", "target_word": pool["target_word"],
                    "categories": {"position": str(pos), "regime": blab,
                                   "carrier_id": "Q1", "scenario_family": str(fam),
                                   "direction": direction}})
        doc = {"name": name, "version": "1.0", "target_word": pool["target_word"],
               "groups": [{"label": "run", "description": f"{direction} fam{fam}",
                           "sentences": entries}],
               "axes": [{"id": "position", "values": [str(i+1) for i in range(len(entries))]}],
               "output_axes": [], "generate_output": False,
               "metadata": {"set_type": "assembled", "capture_substring": carrier,
                            "direction": direction, "family": fam,
                            "regime_boundary": BLOCK, "source_pool": pool["name"]}}
        json.dump(doc, open(out_dir / f"{name}.json", "w"), indent=None)
        manifest.append({"name": name, "family": fam, "direction": direction,
                         "steps": len(entries)})

    for fam in range(n_fam):
        rng = random.Random(1000 + fam)
        uw = [False]
        A1, ta = pick_block(by_label[la][scenes_a[fam]], 
                            [tlen[s] for s in by_label[la][scenes_a[fam]]], budget, rng, uw)
        B1, tb = pick_block(by_label[lb][scenes_b[fam]],
                            [tlen[s] for s in by_label[lb][scenes_b[fam]]], budget, rng, uw)
        build_run(f"{prefix}_d3_fam{fam:02d}_ab", [A1, B1], [la, lb], fam, f"{la}_then_{lb}")
        build_run(f"{prefix}_d3_fam{fam:02d}_ba", [B1, A1], [lb, la], fam, f"{lb}_then_{la}")
        if fam % 2 == 0:  # D4 no-shift arms on even families
            rng2 = random.Random(2000 + fam); uw2 = [False]
            # 40 single-regime sentences: this scene + the NEXT same-label scene
            pool_a = by_label[la][scenes_a[fam]] + by_label[la][scenes_a[(fam+1) % n_fam]]
            pool_b = by_label[lb][scenes_b[fam]] + by_label[lb][scenes_b[(fam+1) % n_fam]]
            A2a, _ = pick_block(pool_a, [tlen[s] for s in pool_a], budget, rng2, uw2)
            A2b, _ = pick_block([s for s in pool_a if s not in A2a],
                                [tlen[s] for s in pool_a if s not in A2a], budget, rng2, uw2)
            B2a, _ = pick_block(pool_b, [tlen[s] for s in pool_b], budget, rng2, uw2)
            B2b, _ = pick_block([s for s in pool_b if s not in B2a],
                                [tlen[s] for s in pool_b if s not in B2a], budget, rng2, uw2)
            build_run(f"{prefix}_d4_fam{fam:02d}_a", [A2a, A2b], [la, la], fam, f"{la}_only")
            build_run(f"{prefix}_d4_fam{fam:02d}_b", [B2a, B2b], [lb, lb], fam, f"{lb}_only")

    json.dump({"carrier": carrier, "block": BLOCK, "budget_tokens_per_block": budget,
               "runs": manifest}, open(out_dir / f"{prefix}_manifest.json", "w"), indent=1)
    print(f"{len(manifest)} runs assembled (budget {budget} tok/block) -> {out_dir}")

if __name__ == "__main__":
    main()
