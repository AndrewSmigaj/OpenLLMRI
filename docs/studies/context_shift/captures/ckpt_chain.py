#!/usr/bin/env python3
"""Checkpoint capture chain (python — no shell quoting). Resume-safe via TSV log.
Usage: ckpt_chain.py MANIFEST_JSON LOG_TSV
Manifest entries: {"name": set_name, "substring": window_text, ...}
"""
import json, sys, time, urllib.request
from pathlib import Path
import pandas as pd

manifest_path, log_path = sys.argv[1], Path(sys.argv[2])
entries = json.load(open(manifest_path))
if not log_path.exists():
    log_path.write_text("set\tsession\tpositions\tstatus\n")
done = {l.split("\t")[0] for l in log_path.read_text().splitlines()[1:] if l}

for e in entries:
    name, sub = e["name"], e["substring"]
    if name in done:
        continue
    payload = json.dumps({"sentence_set_name": name, "generate_output": False,
                          "capture_static_substring": sub}).encode()
    req = urllib.request.Request("http://localhost:8000/api/probes/sentence-experiment",
                                 data=payload, headers={"Content-Type": "application/json"})
    sid = "ERR"
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            sid = json.load(r).get("session_id", "ERR")
    except Exception as ex:
        print(f"[{name}] request error: {ex}; checking for orphan...")
        time.sleep(20)
        import glob, os
        for f in sorted(glob.glob("data/lake/_sessions/session_*.json"), key=os.path.getmtime)[-3:][::-1]:
            d = json.load(open(f))
            if d.get("sentence_set_name") == name:
                sid = d["session_id"]; break
    npos = 0
    try:
        r = pd.read_parquet(f"data/lake/{sid}/residual_streams.parquet", columns=["token_position"])
        npos = r.token_position.nunique()
    except Exception:
        pass
    status = "ok" if npos > 10 else "err"
    with open(log_path, "a") as f:
        f.write(f"{name}\t{sid}\t{npos}\t{status}\n")
    print(f"[{name}] {sid} pos={npos} {status}", flush=True)
print("=== chain complete ===")
