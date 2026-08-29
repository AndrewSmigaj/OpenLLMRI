#!/usr/bin/env python3
"""Generic run chain: posts each manifest entry's set with its substring; asserts
expected probe count. Usage: run_chain.py MANIFEST LOG EXPECTED_PROBES"""
import json, sys, time, urllib.request, glob, os
from pathlib import Path
import pandas as pd

manifest_path, log_path, expect = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
entries = json.load(open(manifest_path))
if not log_path.exists():
    log_path.write_text("set\tsession\tprobes\tstatus\n")
done = {l.split("\t")[0] for l in log_path.read_text().splitlines()[1:] if l}
for e in entries:
    name, sub = e["name"], e["substring"]
    if name in done: continue
    payload = json.dumps({"sentence_set_name": name, "generate_output": False,
                          "capture_static_substring": sub}).encode()
    req = urllib.request.Request("http://localhost:8000/api/probes/sentence-experiment",
                                 data=payload, headers={"Content-Type": "application/json"})
    sid = "ERR"
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            sid = json.load(r).get("session_id", "ERR")
    except Exception as ex:
        print(f"[{name}] request error: {ex}; checking orphan...", flush=True)
        time.sleep(20)
        for f in sorted(glob.glob("data/lake/_sessions/session_*.json"), key=os.path.getmtime)[-3:][::-1]:
            d = json.load(open(f))
            if d.get("sentence_set_name") == name:
                sid = d["session_id"]; break
    n = 0
    try:
        t = pd.read_parquet(f"data/lake/{sid}/tokens.parquet", columns=["probe_id"])
        n = len(t)
    except Exception:
        pass
    status = "ok" if n == expect else "err"
    with open(log_path, "a") as f:
        f.write(f"{name}\t{sid}\t{n}\t{status}\n")
    print(f"[{name}] {sid} probes={n} {status}", flush=True)
print("=== chain complete ===")
