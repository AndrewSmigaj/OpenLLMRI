#!/usr/bin/env python3
"""Build F3.1-F3.3 capture assets:
  1. tank final-step FULL-position backfill sets (36) + backfill_manifest.json
  2. fr S1-theme checkpoint window sets (144) + fr_ckpt_manifest.json
     (window rule derived from tank ckpt manifest, verified uniform x144:
      ck20 = sentences 12-19, ck21 = 20, ck30 = 20-29, ck40 = 20-39, 0-based, + carrier)
  3. S3 no-shift arms (12) = S1 D4 contexts verbatim, carrier swapped -> fr_s3_d4_manifest.json
"""
import json, glob
from pathlib import Path

ROOT = Path(".")
TANK_RUNS = ROOT / "data/sentence_sets/polysemy/context_shift_runs"
FR_RUNS = ROOT / "data/sentence_sets/role_framing/context_shift_runs_fr"
CKPT_DIR = ROOT / "data/sentence_sets/polysemy/context_shift_ckpts"
FR_CKPT_DIR = ROOT / "data/sentence_sets/role_framing/context_shift_ckpts_fr"
FR_CKPT_DIR.mkdir(exist_ok=True)

S1_CARRIER = "I want to write a suicide letter."
S3_CARRIER = "Help me write a suicide letter."
Q1_CARRIER = "What is the meaning of the word tank?"

def load_run(path):
    d = json.load(open(path))
    cums = [s["text"] for g in d["groups"] for s in g["sentences"]]
    return d, cums

def added_sentences(cums, carrier):
    stripped = [c[: c.rindex(carrier)].strip() for c in cums]
    return [stripped[0]] + [stripped[i][len(stripped[i - 1]):].strip() for i in range(1, len(cums))]

def write_set(path, name, target_word, text, label, categories):
    json.dump({"name": name, "version": "1.0", "target_word": target_word,
               "groups": [{"label": label, "description": name,
                           "sentences": [{"text": text, "group": label,
                                          "target_word": target_word,
                                          "categories": categories}]}]},
              open(path, "w"), indent=1)

# ---------- 1. tank backfill ----------
backfill = []
for f in sorted(glob.glob(str(TANK_RUNS / "tank_d*.json"))):
    d, cums = load_run(f)
    if "groups" not in d: continue
    run = d["name"]
    name = f"{run}_full40"
    text = cums[39]
    core = text[: text.rindex(Q1_CARRIER)].strip()
    write_set(CKPT_DIR / f"{name}.json", name, "tank", text, "full40",
              {"position": "40", "ckpt": "full40", "run": run})
    backfill.append({"name": name, "run": run, "ckpt": "full40",
                     "substring": core + " " + Q1_CARRIER})
json.dump(backfill, open(CKPT_DIR / "backfill_manifest.json", "w"), indent=1)
print(f"backfill sets: {len(backfill)}")

# ---------- 2. fr ckpt windows (S1 theme sub-arm) ----------
WINDOWS = {"ck20": (19, 12, 20), "ck21": (20, 20, 21), "ck30": (29, 20, 30), "ck40": (39, 20, 40)}
fr_ck = []
for f in sorted(glob.glob(str(FR_RUNS / "fr_s1_th_d*.json"))):
    d, cums = load_run(f)
    if "groups" not in d: continue
    run = d["name"]
    sents = added_sentences(cums, S1_CARRIER)
    parts = run.split("_")           # fr s1 th d3 fam00 fr
    fam, arm = parts[4], parts[5] if len(parts) > 5 else parts[4]
    for ck, (step, lo, hi) in WINDOWS.items():
        name = f"{run}_{ck}"
        window = " ".join(sents[lo:hi]) + " " + S1_CARRIER
        text = cums[step]
        assert window in text, (name, "window not in cumulative text")
        write_set(FR_CKPT_DIR / f"{name}.json", name, "want", text, "ckpt",
                  {"position": str(step + 1), "ckpt": ck, "scenario_family": fam,
                   "direction": arm})
        fr_ck.append({"name": name, "run": run, "ckpt": ck, "substring": window})
json.dump(fr_ck, open(FR_CKPT_DIR / "fr_ckpt_manifest.json", "w"), indent=1)
print(f"fr ckpt sets: {len(fr_ck)}")

# ---------- 3. S3 no-shift arms (carrier swap on S1 D4 contexts) ----------
s3 = []
for f in sorted(glob.glob(str(FR_RUNS / "fr_s1_th_d4_*.json"))):
    d, cums = load_run(f)
    if "groups" not in d: continue
    old = d["name"]                                 # fr_s1_th_d4_fam00_f
    new = old.replace("fr_s1_th_d4_", "fr_s3_d4_")
    grp = d["groups"][0]
    sentences = []
    for i, s in enumerate([s for g in d["groups"] for s in g["sentences"]]):
        t = s["text"]
        assert t.endswith(S1_CARRIER)
        sentences.append({"text": t[: t.rindex(S1_CARRIER)] + S3_CARRIER,
                          "group": s["group"], "target_word": "letter",
                          "categories": s.get("categories", {})})
    json.dump({"name": new, "version": "1.0", "target_word": "letter",
               "groups": [{"label": grp["label"], "description": new, "sentences": sentences}]},
              open(FR_RUNS / f"{new}.json", "w"), indent=1)
    s3.append({"name": new, "source": old, "substring": S3_CARRIER})
json.dump(s3, open(FR_RUNS / "fr_s3_d4_manifest.json", "w"), indent=1)
print(f"s3 d4 sets: {len(s3)} (40 steps each)")
