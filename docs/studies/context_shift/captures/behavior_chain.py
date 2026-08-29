#!/usr/bin/env python3
"""Behavior-cell chain (D8): generation-on + forced-final first-token logprobs.
Usage: behavior_chain.py MANIFEST LOG PROBE(tank|fr)"""
import json, sys, time, urllib.request, glob, os
from pathlib import Path
import pandas as pd

TOKSETS = {
    "tank": {"answer_starters": ["In", "The", "A", "It"],
             "sense_words": [" aquarium", " vehicle", " military", " fish", " water", " armored"]},
    "fr": {"refusal_starters": ["I", "If", "Sorry", "It"],
           "compliance_starters": ["Here", "Sure", "Dear", "Of"]},
}
manifest_path, log_path, probe = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
entries = json.load(open(manifest_path))
if not log_path.exists():
    log_path.write_text("set\tsession\tprobes\thas_gen\thas_lp\tstatus\n")
done = {l.split("\t")[0] for l in log_path.read_text().splitlines()[1:] if l}
for e in entries:
    name = e["name"]
    if name in done: continue
    payload = json.dumps({"sentence_set_name": name, "generate_output": True,
                          "capture_static_substring": e["substring"],
                          "logit_token_sets": TOKSETS[probe],
                          "logit_forced_final": True}).encode()
    req = urllib.request.Request("http://localhost:8000/api/probes/sentence-experiment",
                                 data=payload, headers={"Content-Type": "application/json"})
    sid = "ERR"
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            sid = json.load(r).get("session_id", "ERR")
    except Exception as ex:
        print(f"[{name}] request error: {ex}; checking orphan...", flush=True)
        time.sleep(15)
        for f in sorted(glob.glob("data/lake/_sessions/session_*.json"), key=os.path.getmtime)[-3:][::-1]:
            d = json.load(open(f))
            if d.get("sentence_set_name") == name:
                sid = d["session_id"]; break
    n, hg, hl = 0, 0, 0
    try:
        t = pd.read_parquet(f"data/lake/{sid}/tokens.parquet",
                            columns=["generated_text", "first_token_logprobs_json"])
        n = len(t); hg = int(t.generated_text.notna().sum()); hl = int(t.first_token_logprobs_json.notna().sum())
    except Exception:
        pass
    status = "ok" if (n == 1 and hg and hl) else "err"
    with open(log_path, "a") as f:
        f.write(f"{name}\t{sid}\t{n}\t{hg}\t{hl}\t{status}\n")
    print(f"[{name}] {sid} n={n} gen={hg} lp={hl} {status}", flush=True)
print("=== behavior chain complete ===")
