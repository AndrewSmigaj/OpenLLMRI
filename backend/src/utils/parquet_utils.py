#!/usr/bin/env python3
"""
Parquet serialization utilities for numpy arrays.
Handles consistent serialization/deserialization across all schemas.
"""

from typing import Any, List, Tuple, cast

import numpy as np


def serialize_array_for_parquet(data: np.ndarray[Any, Any]) -> List[float]:
    """Serialize numpy array for Parquet storage as list<float>."""
    return cast(List[float], data.flatten().tolist())


def deserialize_array_from_parquet(
    data: List[float], dims: Tuple[int, ...]
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Deserialize array from Parquet list<float> storage."""
    return np.array(data, dtype=np.float32).reshape(dims)
