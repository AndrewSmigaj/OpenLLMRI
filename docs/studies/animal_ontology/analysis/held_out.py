"""The study's second measure: how well each axis is read on taxonomic orders a reader never saw
(docs/research/animal_ontology.md). It takes the lens's axes analysis, which holds out whole orders
(the set's hold-out design), and keeps two readers per axis and layer, as κ (agreement beyond
chance):
  - a linear probe on the residual stream: the ceiling, what is linearly there;
  - the lens's nodes at the version's k (from its validation).
Beside each, the line an axis must beat: the 95th percentile of the same reader's scores for decoy
axes (random values given per family), pooled over layers. An axis read on unseen orders is the
strongest evidence that the model carries it beyond descent.

Usage, from the repo root (the backend running, the lens validated and its axes analysed):
  .venv/bin/python docs/studies/animal_ontology/analysis/held_out.py SESSION LENS
Writes results/held_out.json; figures.py draws it.
"""
from __future__ import annotations

import argparse
import json
import urllib.request

from ontology_common import write_results

API = "http://localhost:8000/api"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session")
    parser.add_argument("lens")
    args = parser.parse_args()
    with urllib.request.urlopen(f"{API}/sessions/{args.session}/lenses/{args.lens}/axes", timeout=60) as r:
        axes = json.loads(r.read())
    attributes = list(axes["attributes"])
    probe = [layer["real"] for layer in axes["scores"]["probe"]]
    lens_at_k = axes["umap"]["at_k"]
    result = {
        "session": args.session, "lens": args.lens, "version": axes["version"],
        "layers": axes["layers"], "attributes": attributes,
        "folds": axes["folds"], "level": axes["level"], "k_per_layer": axes["k_per_layer"],
        "probe": [{a: layer.get(a) for a in attributes} for layer in probe],
        "probe_line": axes["thresholds"]["probe"],
        "lens": [{a: layer.get(a) for a in attributes} for layer in lens_at_k],
        "lens_line": axes["umap"]["thresholds"]["at_k"],
        "recovered": {"probe": axes["recovered"]["probe"], "lens": axes["recovered"]["umap_at_k"]},
    }
    print(f"{len(attributes)} axes over {len(result['layers'])} layers, folds: "
          f"{axes['folds'].get('n_folds')} by {axes['folds'].get('field')}")
    for name in ("probe", "lens"):
        line = result[f"{name}_line"]
        best = {a: max((layer[a], i) for i, layer in enumerate(result[name]) if layer[a] is not None)
                for a in attributes}
        print(f"  {name}: " + "; ".join(
            f"{a} peak {kappa:.2f} at L{result['layers'][i]}" + ("" if kappa > line[a] else " (under the line)")
            for a, (kappa, i) in best.items()))
    print(f"wrote {write_results('held_out', result)}")


if __name__ == "__main__":
    main()
