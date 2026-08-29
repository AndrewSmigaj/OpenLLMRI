#!/usr/bin/env python3
"""P5/W4 — behavior cells: reading vs behavior. Run after behavior chains land.

Pass 1 (this script): build the categorization worksheet — per cell: run, k, carrier
reading (own-probe axis, midref), forced-final logprob sets, generated_text. Claude
categorizes the worksheet per /categorize doctrine (tank: first-sense-defined;
fr: refusal / safe-completion / compliance / other), writes *_categorized.csv.
Pass 2 (--stats): rates by reading band + logprob-vs-reading regression with
family-clustered bootstrap. Firewalled expectations: predictions P5 (a,b,c).
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path

C = Path("docs/studies/context_shift/captures")
OUT = Path("docs/studies/context_shift/analysis")
CFG = {
    "tank": dict(log=C / "behavior_tank_log.tsv", L=4,
                 ax=OUT / "axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"),
    "fr": dict(log=C / "behavior_fr_log.tsv", L=14,
               ax=OUT / "axes/axes_session_5247081b_fictional_vs_real_pos1.npz"),
}

def build_worksheet(probe):
    c = CFG[probe]
    ax = np.load(c["ax"]); L = c["L"]
    rows = [r for r in csv.DictReader(open(c["log"]), delimiter="\t") if r["status"] == "ok"]
    out = []
    for r in rows:
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet",
                              columns=["probe_id", "generated_text", "first_token_logprobs_json",
                                       "categories_json"])
        df = res.merge(tok, on="probe_id")
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        reading = float(2.0 * ((X[0] - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"]))
        cats = json.loads(df["categories_json"].iloc[0])
        out.append({"set": r["set"], "session": r["session"], "run": cats.get("run"),
                    "k": cats.get("k"), "reading": round(reading, 3),
                    "logprobs": df["first_token_logprobs_json"].iloc[0],
                    "generated_text": (df["generated_text"].iloc[0] or "")[:400],
                    "category": ""})
    pd.DataFrame(out).to_csv(OUT / f"r6_behavior_worksheet_{probe}.csv", index=False)
    print(f"{probe}: worksheet {len(out)} cells -> r6_behavior_worksheet_{probe}.csv")

def stats(probe):
    df = pd.read_csv(OUT / f"r6_behavior_worksheet_{probe}_categorized.csv")
    print(f"{probe}: n={len(df)}")
    print(df.groupby("category").reading.describe()[["count", "mean", "std"]].to_string())
    # reading-band rates
    df["band"] = pd.cut(df.reading, [-10, -0.5, 0.5, 10], labels=["origin", "mid", "dest"])
    print(pd.crosstab(df.band, df.category, normalize="index").round(2).to_string())
    # logprob primary (fr): refusal-starter mass vs reading
    if probe == "fr":
        def lp(s, key):
            d = json.loads(s)
            return float(np.log(np.sum(np.exp(list(d[key].values())))))
        df["lp_refusal"] = df.logprobs.apply(lambda s: lp(s, "refusal_starters"))
        df["lp_comply"] = df.logprobs.apply(lambda s: lp(s, "compliance_starters"))
        r = np.corrcoef(df.reading, df.lp_refusal - df.lp_comply)[0, 1]
        print(f"corr(reading, refusal-vs-comply logprob margin): {r:.2f}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    for probe in ("tank", "fr"):
        if not CFG[probe]["log"].exists():
            print(f"{probe}: no log yet"); continue
        (stats if mode == "--stats" else build_worksheet)(probe)
