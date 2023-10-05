"""
Document extraction module.
"""

from resume_matcher.extractors.base import BaseExtractor, ExtractionError
from resume_matcher.extractors.txt_extractor import TxtExtractor
from resume_matcher.extractors.pdf_extractor import PdfExtractor
from resume_matcher.extractors.docx_extractor import DocxExtractor
from resume_matcher.extractors.factory import DocumentExtractorFactory

__all__ = [
    "BaseExtractor",
    "ExtractionError",
    "TxtExtractor",
    "PdfExtractor",
    "DocxExtractor",
    "DocumentExtractorFactory",
]