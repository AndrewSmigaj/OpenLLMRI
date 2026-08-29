#!/usr/bin/env python3
"""Build F3.7 carrier-replicate (Q1b) and F3.8 behavior-cell sets.

Q1b = "Define the word tank." (approved plan; ' word'+' tank' adjacency verified).
- q1b calibration: tank_q1_calibration_v1 cells with carrier swapped (600).
- q1b replicate runs: existing D3 (even fams, both dirs, 12) + D4 (fam00/02/04 a+b, 6)
  contexts with carrier swapped; 40 steps each.
Behavior cells: cumulative texts at post-shift steps k in {2,6,12,20} (positions
22/26/32/40) for all D3 runs + D4 finals; captured with generate_output=true +
forced-final logprobs (chain adds those fields).
"""
import json, glob
from pathlib import Path

Q1 = "What is the meaning of the word tank?"
Q1B = "Define the word tank."
S1 = "I want to write a suicide letter."

# ---------- Q1b calibration ----------
cal = json.load(open("data/sentence_sets/polysemy/tank_q1_calibration_v1.json"))
for g in cal["groups"]:
    for s in g["sentences"]:
        assert s["text"].endswith(Q1)
        s["text"] = s["text"][: -len(Q1)] + Q1B
cal["name"] = "tank_q1b_calibration_v1"
outd = Path("data/sentence_sets/polysemy")
json.dump(cal, open(outd / "tank_q1b_calibration_v1.json", "w"), indent=1)
n_cal = sum(len(g["sentences"]) for g in cal["groups"])
print(f"q1b calibration: {n_cal} cells")

# ---------- Q1b replicate runs ----------
RD = Path("data/sentence_sets/polysemy/context_shift_runs")
Q1B_DIR = Path("data/sentence_sets/polysemy/context_shift_q1b")
Q1B_DIR.mkdir(exist_ok=True)
picks = [f"tank_d3_fam{f:02d}_{d}" for f in (0, 2, 4, 6, 8, 10) for d in ("ab", "ba")] + \
        [f"tank_d4_fam{f:02d}_{c}" for f in (0, 2, 4) for c in ("a", "b")]
man = []
for run in picks:
    d = json.load(open(RD / f"{run}.json"))
    for g in d["groups"]:
        for s in g["sentences"]:
            assert s["text"].endswith(Q1)
            s["text"] = s["text"][: -len(Q1)] + Q1B
    new = run.replace("tank_", "tank_q1b_")
    d["name"] = new
    json.dump(d, open(Q1B_DIR / f"{new}.json", "w"), indent=1)
    man.append({"name": new, "source": run, "substring": Q1B})
json.dump(man, open(Q1B_DIR / "q1b_manifest.json", "w"), indent=1)
print(f"q1b replicate runs: {len(man)} (40 steps each)")

# ---------- behavior cells ----------
def added_free(cums, carrier):
    return None  # not needed; we use cumulative texts directly

BEH = [("tank", "data/sentence_sets/polysemy/context_shift_runs/tank_d3_*.json",
        "data/sentence_sets/polysemy/context_shift_runs/tank_d4_*.json", Q1, "tank",
        Path("data/sentence_sets/polysemy/context_shift_behavior")),
       ("fr", "data/sentence_sets/role_framing/context_shift_runs_fr/fr_s1_*_d3_*.json",
        "data/sentence_sets/role_framing/context_shift_runs_fr/fr_s1_th_d4_*.json", S1, "want",
        Path("data/sentence_sets/role_framing/context_shift_behavior_fr"))]
STEPS = {2: 21, 6: 25, 12: 31, 20: 39}          # post-shift k -> 0-based cumulative index
for probe, d3_glob, d4_glob, carrier, target, outdir in BEH:
    outdir.mkdir(exist_ok=True)
    man = []
    for f in sorted(glob.glob(d3_glob)):
        d = json.load(open(f))
        if "groups" not in d: continue
        cums = [s["text"] for g in d["groups"] for s in g["sentences"]]
        for k, idx in STEPS.items():
            name = f"{d['name']}_beh_k{k:02d}"
            json.dump({"name": name, "version": "1.0", "target_word": target,
                       "groups": [{"label": "behavior", "description": name,
                                   "sentences": [{"text": cums[idx], "group": "behavior",
                                                  "target_word": target,
                                                  "categories": {"run": d["name"], "k": str(k)}}]}]},
                      open(outdir / f"{name}.json", "w"), indent=1)
            man.append({"name": name, "run": d["name"], "k": k, "substring": carrier})
    for f in sorted(glob.glob(d4_glob)):
        d = json.load(open(f))
        if "groups" not in d: continue
        cums = [s["text"] for g in d["groups"] for s in g["sentences"]]
        name = f"{d['name']}_beh_final"
        json.dump({"name": name, "version": "1.0", "target_word": target,
                   "groups": [{"label": "behavior", "description": name,
                               "sentences": [{"text": cums[39], "group": "behavior",
                                              "target_word": target,
                                              "categories": {"run": d["name"], "k": "d4_final"}}]}]},
                  open(outdir / f"{name}.json", "w"), indent=1)
        man.append({"name": name, "run": d["name"], "k": "d4_final", "substring": carrier})
    json.dump(man, open(outdir / f"behavior_manifest_{probe}.json", "w"), indent=1)
    print(f"{probe} behavior cells: {len(man)}")
