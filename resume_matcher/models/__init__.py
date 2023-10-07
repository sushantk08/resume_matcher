"""
Models module for lexical and semantic vector representation.
"""

from resume_matcher.models.similarity import (
    compute_cosine_similarity,
    normalize_scores,
)
from resume_matcher.models.tfidf_model import TfidfMatcher

__all__ = [
    "compute_cosine_similarity",
    "normalize_scores",
    "TfidfMatcher",
]