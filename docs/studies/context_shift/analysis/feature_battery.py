#!/usr/bin/env python3
"""Deterministic surface-feature battery over the v1 sentence pools (confound appendix).

Per sentence, only features that need no linguistic judgment: length, punctuation,
type-token ratio, opener class, and within-scene template overlap. These are the
inputs to the confound-ceiling classifier in confound_features_analysis.py, which
asks how far the two classes separate on surface features alone — the number that
tells a reader whether the reading in §3.1 could be "some other variance."

No second-AI rater and no judgment tags (tense, register, valence): those would be a
second confounded model reading, not a clean surface baseline.

Input : data/sentence_sets/{polysemy/tank_scene_pools_v1.json,
        role_framing/fiction_real_scene_pools_v1.json}
Output: docs/studies/context_shift/analysis/confound_features.csv
        one row per sentence: task, cls, scene, idx, <feature columns>.

Run from the repository root:  .venv/bin/python docs/studies/context_shift/analysis/feature_battery.py
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("docs/studies/context_shift/analysis/confound_features.csv")
POOLS = [
    ("tank", "data/sentence_sets/polysemy/tank_scene_pools_v1.json"),
    ("fr", "data/sentence_sets/role_framing/fiction_real_scene_pools_v1.json"),
]

# ---- helpers replicated from pool_audit_v2.py (that module runs + sys.exits at import,
#      so it cannot be imported) and scene_heldout_calibration.py (_scene lives in main()).
FUNC = set("""a an the and or but if of in on at to for with by from as is are was were be been being it its
this that these those i we you he she they them his her their my our your me us not no so than then too very
just also only into over under after before during about against between out up down off""".split())


def toks(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z']+", s.lower()) if w not in FUNC]


def jac(a: set, b: set) -> float:
    return len(a & b) / max(1, len(a | b))


def opener(s: str) -> str:
    w = s.split()[0].strip('"“‘').rstrip(",").lower()
    if w in ("the", "a", "an"):
        return "article"
    if w in ("i", "we", "you", "he", "she", "they", "it", "my", "our", "her", "his"):
        return "pronoun"
    if s.split()[0].startswith(('"', "“")):
        return "quote"
    if w in ("who", "what", "why", "how", "did", "do", "does", "was", "is", "are",
             "have", "has", "would", "will", "can", "could", "should"):
        return "question"
    if w in ("by", "under", "over", "between", "after", "before", "during", "at", "on",
             "in", "behind", "down", "per", "from", "somewhere", "along", "inside",
             "tonight", "every"):
        return "prep/adv"
    return "other"


OPENER_CLASSES = ["article", "pronoun", "quote", "question", "prep/adv", "other"]


def _scene(raw: str) -> str:
    # batch-file naming drift gave one setting two names across sub-arms
    # (01_novelist vs 01_novelist_editor). Scene id = first two underscore tokens.
    parts = raw.split("_")
    return "_".join(parts[:2]) if len(parts) >= 2 else raw


def word_4grams(s: str) -> set:
    t = toks(s)
    return {tuple(t[i:i + 4]) for i in range(max(0, len(t) - 3))}


def scalar_features(text: str) -> dict:
    words = text.split()
    n_tok = max(1, len(words))
    n_chr = max(1, len(text))
    alpha = re.findall(r"[A-Za-z']+", text)
    lower = [w.lower() for w in alpha]
    return {
        "n_tokens": len(words),
        "n_chars": len(text),
        "n_sentences": len(re.findall(r"[.!?]+", text)),
        "ttr": len(set(lower)) / max(1, len(lower)),
        "mean_word_len": float(np.mean([len(w) for w in alpha])) if alpha else 0.0,
        "comma_rate": text.count(",") / n_tok,
        "semicolon_rate": text.count(";") / n_tok,
        "quote_present": float(('"' in text) or ("“" in text) or ("”" in text)),
        "dash_present": float(("—" in text) or (" - " in text)),
        "digit_rate": sum(c.isdigit() for c in text) / n_chr,
    }


def build():
    rows = []
    for task, path in POOLS:
        pool = json.load(open(path))
        for g in pool["groups"]:
            cls = g["label"]
            # group sentences by normalized scene for the within-scene overlap feature
            by_scene = defaultdict(list)
            texts = []
            for i, sent in enumerate(g["sentences"]):
                scene = _scene((sent.get("categories") or {}).get("scene", "?"))
                by_scene[scene].append(i)
                texts.append((i, scene, sent["text"]))
            grams = {i: word_4grams(t) for i, _, t in texts}
            for i, scene, text in texts:
                feats = scalar_features(text)
                # within-scene 4-gram overlap: mean Jaccard with same-class same-scene peers
                peers = [j for j in by_scene[scene] if j != i]
                feats["within_scene_4gram"] = (
                    float(np.mean([jac(grams[i], grams[j]) for j in peers])) if peers else 0.0
                )
                op = opener(text)
                for oc in OPENER_CLASSES:
                    feats[f"opener_{oc.replace('/', '_')}"] = float(op == oc)
                rows.append({"task": task, "cls": cls, "scene": scene, "idx": i, **feats})
    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {OUT}: {len(df)} sentences, {df.shape[1]} columns")
    for task in df.task.unique():
        sub = df[df.task == task]
        print(f"  {task}: {dict(sub.cls.value_counts())}, {sub.scene.nunique()} scenes")
    return df


if __name__ == "__main__":
    build()
