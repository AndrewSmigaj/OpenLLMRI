"""Where a lens's nodes part ways (DESIGN.md C5, C7): a split point is a node whose items go to two
next-layer nodes or more, each taking a real share of them. One rule for the report cards
(services/llm), node details and the attention-and-experts account (services/lenses/writers.py);
the app's card ids copy it (frontend utils/cardId.ts)."""

from __future__ import annotations

from collections import Counter
from typing import Any, List, Tuple

import numpy as np

SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE = 5, 0.15  # a branch holds at least this many items and this share


def branches_of(view: Any, li: int, node: int) -> List[Tuple[int, int]]:
    """The next-layer nodes that take a real share of a node's items: (node, items), biggest first."""
    mask = view.nodes[:, li] == node
    floor = max(SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE * int(mask.sum()))
    return [(int(b), n) for b, n in Counter(view.nodes[mask, li + 1].tolist()).most_common() if n >= floor]


def split_points(view: Any) -> List[Tuple[int, int, int]]:
    """Every node whose items part ways at the next layer: (layer, node, items in its second
    branch), the biggest second branch first."""
    found = []
    for li in range(len(view.layers) - 1):
        for node in np.unique(view.nodes[:, li]).tolist():
            branches = branches_of(view, li, int(node))
            if len(branches) >= 2:
                found.append((view.layers[li], int(node), branches[1][1]))
    return sorted(found, key=lambda s: -s[2])
