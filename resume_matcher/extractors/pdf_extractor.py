"""
PDF document extractor using pypdf.
"""

import io
from typing import Union
from pypdf import PdfReader
from resume_matcher.extractors.base import BaseExtractor, ExtractionError


class PdfExtractor(BaseExtractor):
    """Extractor for Portable Document Format (.pdf) files."""

    def extract_from_file(self, file_path: str) -> str:
        """Extract text from a PDF file path."""
        self._validate_file_path(file_path)
        try:
            reader = PdfReader(file_path)
            return self._extract_text_from_reader(reader)
        except Exception as e:
            raise ExtractionError(f"Failed to read PDF file '{file_path}': {e}") from e

    def extract_from_bytes(self, file_bytes: Union[bytes, io.BytesIO], filename: str = "") -> str:
        """Extract text from PDF in-memory bytes."""
        try:
            if isinstance(file_bytes, bytes):
                stream = io.BytesIO(file_bytes)
            elif isinstance(file_bytes, io.BytesIO):
                stream = file_bytes
            else:
                raise ExtractionError(f"Unsupported byte input type: {type(file_bytes)}")

            reader = PdfReader(stream)
            return self._extract_text_from_reader(reader)
        except Exception as e:
            raise ExtractionError(f"Failed to extract PDF bytes: {e}") from e

    @staticmethod
    def _extract_text_from_reader(reader: PdfReader) -> str:
        """Extract and clean text across all pages in the PDF reader."""
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise ExtractionError("PDF file is password-protected and cannot be read.")

        page_texts = []
        for idx, page in enumerate(reader.pages):
            page_content = page.extract_text()
            if page_content:
                page_texts.append(page_content.strip())

        if not page_texts:
            return ""

        full_text = "\n\n".join(page_texts)
        full_text = full_text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
        return full_text.strip()