"""
Models module for lexical and semantic vector representation.
"""

from resume_matcher.models.similarity import (
    compute_cosine_similarity,
    normalize_scores,
)
from resume_matcher.models.tfidf_model import TfidfMatcher
from resume_matcher.models.embedding_model import EmbeddingMatcher

__all__ = [
    "compute_cosine_similarity",
    "normalize_scores",
    "TfidfMatcher",
    "EmbeddingMatcher",
]