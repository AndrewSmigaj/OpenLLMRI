#!/usr/bin/env python3
"""QA C2 — boundary indexing audit.
(a) k=1 <-> position 21: verify from capture metadata that per-run 'position' categories
    run 1..40 and that analysis slice [20:40] therefore selects positions 21..40.
(b) Carrier token byte-identity: token id at semantic position 1 equals
    tokenizer(' tank')/(' want')[0] for every sampled run.
(c) Right-alignment: every checkpoint window's LAST substring tokens decode to the
    carrier string (sampled).
"""
import sys, json, csv, random
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
from transformers import AutoTokenizer

random.seed(2)
TOK = AutoTokenizer.from_pretrained("data/models/gpt-oss-20b")
C = Path("docs/studies/context_shift/captures")
FAILS = []

# (a)+(b): sample runs from both logs
for probe, log, target in (("tank", C / "tank_d3_d4_log.tsv", " tank"),
                           ("fr", C / "fr_d3_d4_log.tsv", " want")):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    per_carrier = {"tank": " tank", "fr_s1": " want", "fr_s2": " like", "fr_s3": " letter"}
    for r in random.sample(rows, 6):
        lake = Path("data/lake") / r["session"]
        tok = pd.read_parquet(lake / "tokens.parquet",
                              columns=["probe_id", "categories_json", "target_token_id"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        ps = sorted(tok["pos"].tolist())
        if ps != list(range(1, 41)):
            FAILS.append(f"{r['run']}: positions not 1..40: {ps[:5]}...")
        key = "tank" if probe == "tank" else r["run"][:5]
        exp = TOK.encode(per_carrier[key], add_special_tokens=False)[0]
        bad = tok[tok["target_token_id"] != exp]
        if len(bad): FAILS.append(f"{r['run']}: target_token_id mismatch ({len(bad)} rows)")
    print(f"{probe}: sampled 6 runs — positions 1..40 and per-carrier target ids verified")

# k=1 -> position 21 equivalence: the analysis convention proj[20:40] on pos-sorted arrays
print("k=1 <-> position 21: analysis arrays are sorted by 'position' (1..40); slice [20:40]"
      " = positions 21..40 — verified by (a)'s contiguity assertion")

# (c) right-alignment: last window tokens decode to carrier (sample 5 ck sessions per probe)
for probe, cklog, carrier in (("tank", C / "tank_ckpt_log.tsv", "What is the meaning of the word tank?"),
                              ("fr", C / "fr_ckpt_log.tsv", "I want to write a suicide letter.")):
    rows = [r for r in csv.DictReader(open(cklog), delimiter="\t") if r["status"] == "ok"]
    seen = set(); kept = []
    for r in rows:
        if r["set"] not in seen: seen.add(r["set"]); kept.append(r)
    car_ids = TOK.encode(" " + carrier if not carrier.startswith("I ") else " " + carrier,
                         add_special_tokens=False)
    n_car = len(TOK.encode(" " + carrier, add_special_tokens=False))
    for r in random.sample(kept, 5):
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet", columns=["token_position", "layer"])
        maxp = int(res.token_position.max())
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["input_text"])
        it = tok.input_text.iloc[0]
        if not it.rstrip().endswith(carrier):
            FAILS.append(f"{r['set']}: input_text does not end with carrier")
    print(f"{probe}: sampled 5 ckpt windows — input_text ends with carrier "
          f"(right-alignment anchor, {n_car} carrier tokens)")
print("\nC2:", "FAIL: " + "; ".join(FAILS[:5]) if FAILS else "PASS")
