#!/usr/bin/env python3
"""Behavior-cell chain, regeneration (v2): same cells and payload as behavior_chain.py,
with a longer generation cap and the chat-template date pinned to each cell's
original capture day, so each new completion is an exact extension of the frozen
one under greedy decoding.

Usage: behavior_chain_v2.py MANIFEST LOG PROBE(tank|fr) [--cap N] [--pin-date auto|YYYY-MM-DD]
                            [--suffix _v2] [--only name1,name2,...] [--repeat K]

--pin-date auto  looks each cell's frozen capture date up in captures/capture_manifest.csv.
--suffix         is appended to the session_name (never to the sentence-set name), so
                 regenerated sessions are distinguishable from the frozen ones.
--repeat K       fires each cell K times with session_name suffixes _r1.._rK (determinism check).
Log columns: set, session, probes, has_gen, has_lp, status, cap, pinned_date, reached_final, gen_chars, seconds.
"""
import argparse, csv, glob, json, os, sys, time, urllib.request
from pathlib import Path
import pandas as pd

TOKSETS = {
    "tank": {"answer_starters": ["In", "The", "A", "It"],
             "sense_words": [" aquarium", " vehicle", " military", " fish", " water", " armored"]},
    "fr": {"refusal_starters": ["I", "If", "Sorry", "It"],
           "compliance_starters": ["Here", "Sure", "Dear", "Of"]},
}
ap = argparse.ArgumentParser()
ap.add_argument("manifest"); ap.add_argument("log"); ap.add_argument("probe", choices=["tank", "fr"])
ap.add_argument("--cap", type=int, default=2048)
ap.add_argument("--pin-date", default="auto")
ap.add_argument("--suffix", default="_v2")
ap.add_argument("--only", default="")
ap.add_argument("--repeat", type=int, default=1)
a = ap.parse_args()
log_path = Path(a.log)
entries = json.load(open(a.manifest))
if a.only: entries = [e for e in entries if e["name"] in set(a.only.split(","))]

frozen_date = {}
for r in csv.DictReader(open("docs/studies/context_shift/captures/capture_manifest.csv")):
    if r["file"].startswith("_sessions/") and r["sentence_set"] not in frozen_date:
        frozen_date[r["sentence_set"]] = r["capture_date"]

COLS = "set\tsession\tprobes\thas_gen\thas_lp\tstatus\tcap\tpinned_date\treached_final\tgen_chars\tseconds\n"
if not log_path.exists(): log_path.write_text(COLS)
done = {l.split("\t")[0] for l in log_path.read_text().splitlines()[1:] if l}

def find_orphan(session_name):
    time.sleep(15)
    for f in sorted(glob.glob("data/lake/_sessions/session_*.json"), key=os.path.getmtime)[-5:][::-1]:
        d = json.load(open(f))
        if d.get("session_name") == session_name: return d["session_id"]
    return "ERR"

for e in entries:
    for rep in range(1, a.repeat + 1):
        name = e["name"]
        key = name if a.repeat == 1 else f"{name}_r{rep}"
        if key in done: continue
        pin = frozen_date.get(name) if a.pin_date == "auto" else a.pin_date
        if a.pin_date == "auto" and pin is None:
            print(f"[{name}] no frozen capture date in capture_manifest.csv; skipping", flush=True); continue
        session_name = f"sentence_{name}{a.suffix}" + (f"_r{rep}" if a.repeat > 1 else "")
        payload = json.dumps({"sentence_set_name": name, "session_name": session_name,
                              "generate_output": True, "max_new_tokens": a.cap, "pin_date": pin,
                              "capture_static_substring": e["substring"],
                              "logit_token_sets": TOKSETS[a.probe], "logit_forced_final": True}).encode()
        req = urllib.request.Request("http://localhost:8000/api/probes/sentence-experiment",
                                     data=payload, headers={"Content-Type": "application/json"})
        t0 = time.time(); sid = "ERR"
        try:
            with urllib.request.urlopen(req, timeout=3600) as r:
                sid = json.load(r).get("session_id", "ERR")
        except Exception as ex:
            print(f"[{key}] request error: {ex}; checking orphan...", flush=True)
            sid = find_orphan(session_name)
        secs = round(time.time() - t0, 1)
        n, hg, hl, fin, chars = 0, 0, 0, 0, 0
        try:
            t = pd.read_parquet(f"data/lake/{sid}/tokens.parquet", columns=["generated_text", "first_token_logprobs_json"])
            n = len(t); hg = int(t.generated_text.notna().sum()); hl = int(t.first_token_logprobs_json.notna().sum())
            g = t.generated_text.iloc[0] or ""; fin = int("assistantfinal" in g); chars = len(g)
        except Exception:
            pass
        status = "ok" if (n == 1 and hg and hl) else "err"
        with open(log_path, "a") as f:
            f.write(f"{key}\t{sid}\t{n}\t{hg}\t{hl}\t{status}\t{a.cap}\t{pin}\t{fin}\t{chars}\t{secs}\n")
        print(f"[{key}] {sid} n={n} gen={hg} lp={hl} final={fin} chars={chars} {secs}s {status}", flush=True)
print("=== behavior chain v2 complete ===")
