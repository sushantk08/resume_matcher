"""
Similarity metrics and vector normalization utilities.
"""

from typing import Union
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarity(
    vector_a: Union[np.ndarray, list],
    vector_b: Union[np.ndarray, list],
) -> float:
    """
    Compute cosine similarity between two 1D or 2D vectors.

    Args:
        vector_a: First vector or matrix.
        vector_b: Second vector or matrix.

    Returns:
        Cosine similarity score as a float between 0.0 and 1.0.
    """
    a = np.asarray(vector_a)
    b = np.asarray(vector_b)

    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)

    sim = cosine_similarity(a, b)[0][0]
    # Bound score between 0.0 and 1.0
    return float(np.clip(sim, 0.0, 1.0))


def normalize_scores(scores: np.ndarray) -> np.ndarray:
    """Normalize an array of scores to a [0, 1] range using min-max scaling."""
    arr = np.asarray(scores, dtype=float)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val == min_val:
        return np.ones_like(arr)
    return (arr - min_val) / (max_val - min_val)