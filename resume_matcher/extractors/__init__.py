"""
Document extraction module.
"""

from resume_matcher.extractors.base import BaseExtractor, ExtractionError
from resume_matcher.extractors.txt_extractor import TxtExtractor

__all__ = ["BaseExtractor", "ExtractionError", "TxtExtractor"]