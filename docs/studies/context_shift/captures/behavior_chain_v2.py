#!/usr/bin/env python3
"""Behavior-cell chain, regeneration (v2): same cells and payload as behavior_chain.py,
with a longer generation cap and the chat-template date pinned to each cell's
original capture day, so each new completion is an exact extension of the frozen
one under greedy decoding.

Sampled arm (7 September 2026): with --sample the same cells are generated under
do_sample=True at the given temperature and top_p (no top-k truncation), with the
RNG seeded per request; the prompt tokens are unchanged (date still pinned), only
the decoding differs. Without --sample the payload is byte-identical to the greedy
regeneration's.

Usage: behavior_chain_v2.py MANIFEST LOG PROBE(tank|fr) [--cap N] [--pin-date auto|YYYY-MM-DD]
                            [--suffix _v2] [--only name1,name2,...] [--repeat K]
                            [--sample] [--temperature 1.0] [--top-p 1.0] [--seed N]

--pin-date auto  looks each cell's frozen capture date up in captures/capture_manifest.csv.
--suffix         is appended to the session_name (never to the sentence-set name), so
                 regenerated sessions are distinguishable from the frozen ones.
--repeat K       fires each cell K times with session_name suffixes _r1.._rK (determinism check).
--sample         request sampled decoding; --seed is sent with every request.
Log columns: set, session, probes, has_gen, has_lp, status, cap, pinned_date, reached_final,
gen_chars, seconds, sampled, temperature, top_p, seed.
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
ap.add_argument("--sample", action="store_true")
ap.add_argument("--temperature", type=float, default=1.0)
ap.add_argument("--top-p", type=float, default=1.0)
ap.add_argument("--seed", type=int, default=None)
a = ap.parse_args()
if a.sample and a.seed is None:
    sys.exit("--sample requires --seed so every draw is recorded")
log_path = Path(a.log)
entries = json.load(open(a.manifest))
if a.only: entries = [e for e in entries if e["name"] in set(a.only.split(","))]

frozen_date = {}
# The frozen capture day is the EARLIEST session date for the sentence set among the
# original corpora. The manifest now also lists the regenerated, date-bound, smoke,
# and sampled sessions (later dates), so "first row" is no longer the frozen one.
for r in csv.DictReader(open("docs/studies/context_shift/captures/capture_manifest.csv")):
    if not r["file"].startswith("_sessions/"): continue
    if any(w in r["corpus"] for w in ("regenerated", "date-bound", "smoke", "sampled")): continue
    d = r["capture_date"]
    if r["sentence_set"] not in frozen_date or d < frozen_date[r["sentence_set"]]:
        frozen_date[r["sentence_set"]] = d

COLS = ("set\tsession\tprobes\thas_gen\thas_lp\tstatus\tcap\tpinned_date\treached_final\tgen_chars\tseconds"
        "\tsampled\ttemperature\ttop_p\tseed\n")
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
        body = {"sentence_set_name": name, "session_name": session_name,
                "generate_output": True, "max_new_tokens": a.cap, "pin_date": pin,
                "capture_static_substring": e["substring"],
                "logit_token_sets": TOKSETS[a.probe], "logit_forced_final": True}
        if a.sample:
            body.update({"do_sample": True, "temperature": a.temperature, "top_p": a.top_p, "seed": a.seed})
        payload = json.dumps(body).encode()
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
        samp = (int(a.sample), a.temperature if a.sample else "", a.top_p if a.sample else "", a.seed if a.sample else "")
        with open(log_path, "a") as f:
            f.write(f"{key}\t{sid}\t{n}\t{hg}\t{hl}\t{status}\t{a.cap}\t{pin}\t{fin}\t{chars}\t{secs}"
                    f"\t{samp[0]}\t{samp[1]}\t{samp[2]}\t{samp[3]}\n")
        print(f"[{key}] {sid} n={n} gen={hg} lp={hl} final={fin} chars={chars} {secs}s {status}"
              + (f" seed={a.seed}" if a.sample else ""), flush=True)
print("=== behavior chain v2 complete ===")
