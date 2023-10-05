"""
Factory for creating and resolving document extractors based on file extension.
"""

import os
from typing import Dict, Type, Union
import io

from resume_matcher.extractors.base import BaseExtractor, ExtractionError
from resume_matcher.extractors.txt_extractor import TxtExtractor
from resume_matcher.extractors.pdf_extractor import PdfExtractor
from resume_matcher.extractors.docx_extractor import DocxExtractor


class DocumentExtractorFactory:
    """Factory to resolve and invoke the appropriate extractor for a document."""

    _EXT_MAP: Dict[str, Type[BaseExtractor]] = {
        ".txt": TxtExtractor,
        ".md": TxtExtractor,
        ".csv": TxtExtractor,
        ".pdf": PdfExtractor,
        ".docx": DocxExtractor,
    }

    @classmethod
    def get_extractor(cls, filename_or_path: str) -> BaseExtractor:
        """
        Return an extractor instance based on the file extension.

        Args:
            filename_or_path: File name or path.

        Returns:
            An instance of BaseExtractor.

        Raises:
            ExtractionError: If the file extension is unsupported.
        """
        _, ext = os.path.splitext(filename_or_path.lower())
        if not ext:
            # Fallback to plain text if extension is absent
            return TxtExtractor()

        extractor_cls = cls._EXT_MAP.get(ext)
        if not extractor_cls:
            supported = ", ".join(cls._EXT_MAP.keys())
            raise ExtractionError(
                f"Unsupported file format '{ext}'. Supported formats: {supported}"
            )
        return extractor_cls()

    @classmethod
    def extract_text(
        cls,
        file_input: Union[str, bytes, io.BytesIO],
        filename: str = "",
    ) -> str:
        """
        Convenience method to extract text from a file path or in-memory buffer.

        Args:
            file_input: Path to file (str), raw bytes (bytes), or stream (BytesIO).
            filename: Name of the file (required when file_input is bytes or BytesIO).

        Returns:
            Extracted text content as a string.
        """
        if isinstance(file_input, str):
            extractor = cls.get_extractor(file_input)
            return extractor.extract_from_file(file_input)

        if not filename:
            raise ExtractionError("Filename must be provided when extracting from bytes/stream.")

        extractor = cls.get_extractor(filename)
        return extractor.extract_from_bytes(file_input, filename=filename)