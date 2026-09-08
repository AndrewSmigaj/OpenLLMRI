#!/usr/bin/env python3
"""probes — run the scenario's probe corpus on the pure core (DR-18a). Host, no Evennia.

  python3 tools/probes.py [scenario] [-v] [--todo] [--write-baseline] [--filter SUBSTR]

Exit 1 if any `status: pass` probe fails, or if the passing count dropped below BASELINE (the
ratchet). `--write-baseline` records the current passing count. `-v` prints failing transcripts;
`--todo` also lists todo probes that now pass (promote them to `pass`).
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario", nargs="?", default="whiteout")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--todo", action="store_true", help="list todo probes that pass (promotable)")
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--filter", default="")
    ap.add_argument("--phrasing", action="store_true", help="the phrasing corpus: parse rate by condition")
    a = ap.parse_args()

    content = importlib.import_module(f"world.scenarios.{a.scenario}.content")
    objects = importlib.import_module(f"world.scenarios.{a.scenario}.objects")
    probes_pkg = importlib.import_module(f"world.scenarios.{a.scenario}.probes")
    try:
        authored = importlib.import_module(f"world.scenarios.{a.scenario}.authored").AUTHORED
    except ModuleNotFoundError:
        authored = None
    from world.sim.testing.probes import run_all, summarize

    materials = content.load()
    if a.phrasing:
        a.filter = a.filter or "phrasing."
    probes = [p for p in probes_pkg.PROBES if a.filter in p["id"]]
    results = run_all(probes, objects.OBJECT_TABLE, materials, authored)
    if a.phrasing:
        import collections
        by = collections.defaultdict(lambda: [0, 0])
        for r in results:
            key = ".".join(r.probe["id"].split(".")[1:3])          # model.condition
            by[key][0] += int(r.passed)
            by[key][1] += 1
        for k in sorted(by):
            ok, n = by[k]
            print(f"  phrasing {k}: {ok}/{n} parsed ({100 * ok // max(1, n)}%)")
        if a.verbose:
            for r in results:
                if not r.passed:
                    print(f"    - {r.probe['steps'][0]!r}: {r.reason[:100]}")
    s = summarize(results)
    base = probes_pkg.baseline()
    print(f"probes: {s['passing']}/{s['total']} passing — pass-status {s['pass_ok']} ok / "
          f"{s['pass_fail']} FAILING; todo {s['todo_ok']} passing (promotable) / {s['todo_fail']} open; "
          f"baseline {base}")
    bad = [r for r in results if r.probe.get("status") == "pass" and not r.passed]
    for r in bad:
        print(f"  FAIL {r.probe['id']}: {r.reason}")
        if a.verbose:
            for st in r.steps:
                print(f"       > {st.line}\n         [{st.kind} {st.tier}] {st.narration}")
    if a.todo:
        for r in results:
            if r.probe.get("status") != "pass" and r.passed:
                print(f"  promotable: {r.probe['id']}  ({r.steps[-1].tier})")
        if a.verbose:
            for r in results:
                if r.probe.get("status") != "pass" and not r.passed:
                    print(f"  todo {r.probe['id']}: {r.reason[:110]}")
    if a.write_baseline and not a.filter:
        with open(probes_pkg.BASELINE_PATH, "w", encoding="utf-8") as fh:
            fh.write(f"{s['passing']}\n")
        print(f"baseline written: {s['passing']}")
        return 0
    if bad:
        return 1
    if not a.filter and s["passing"] < base:
        print(f"RATCHET: passing count {s['passing']} dropped below baseline {base}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
