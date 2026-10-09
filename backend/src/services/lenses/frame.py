"""The 3-D view of a lens in its own space (DESIGN.md E5; lens slice 1b).

Each layer is drawn on three directions of the lens's own embedding: the embedding itself where
the layer has three dimensions, otherwise its first three principal components, which hold 90 to
100% of a 6-D embedding's variance on the slice-1 lenses. UMAP's and PCA's orientations are
arbitrary, so each later layer is turned onto the one before by orthogonal Procrustes over all
the lens's items: a rotation or a reflection, never a scaling, so no distance within a layer
changes, and trajectories become paths rather than jumps (on the tank lens the median
layer-to-layer mismatch fell from 1.39 to 0.30). The first layer's axes point toward their longer
tails. Items read through the lens pass through the same chain. The frame is worked out when it
is served, in milliseconds; nothing is stored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Sequence, Tuple

import numpy as np

Array = np.ndarray[Any, Any]


@dataclass
class Frame:
    means: List[Array]  # each layer's centre
    bases: List[Array]  # each layer's three directions, as orthonormal columns (D_l x 3)
    shares: List[float]  # the share of each layer's variance the three directions hold

    def project(self, li: int, points: Array) -> Array:
        """Points of the li-th layer's embedding (N x D, padded columns allowed) in the frame."""
        basis = self.bases[li]
        result: Array = (points[:, :basis.shape[0]] - self.means[li]) @ basis
        return result


def principal(centred: Array) -> Tuple[Array, float]:
    """The three main directions of centred points (columns, D x 3) and the share of the variance
    they hold. Three dimensions or fewer are kept as they are."""
    dims = centred.shape[1]
    if dims <= 3:
        return np.eye(dims, 3), 1.0
    _, singular, vt = np.linalg.svd(centred, full_matrices=False)
    total = float((singular ** 2).sum())
    return vt[:3].T, float((singular[:3] ** 2).sum() / total) if total > 0 else 1.0


def procrustes(moving: Array, target: Array) -> Array:
    """The orthogonal 3 x 3 matrix (a rotation or a reflection) that best turns `moving` onto
    `target`, both N x 3: argmin over R of |moving R - target|."""
    u, _, vt = np.linalg.svd(moving.T @ target)
    turn: Array = u @ vt
    return turn


def lens_frame(embeddings: Sequence[Array]) -> Frame:
    """The frame of each layer's embedding (N x D_l each, the same items in the same order)."""
    means: List[Array] = []
    bases: List[Array] = []
    shares: List[float] = []
    previous = None
    for points in embeddings:
        mean = points.mean(axis=0)
        basis, share = principal(points - mean)
        projected = (points - mean) @ basis
        if previous is None:
            signs = np.sign((projected ** 3).sum(axis=0))
            basis = basis * np.where(signs == 0, 1.0, signs)
        else:
            basis = basis @ procrustes(projected, previous)
        previous = (points - mean) @ basis
        means.append(mean)
        bases.append(basis)
        shares.append(round(share, 4))
    return Frame(means, bases, shares)
