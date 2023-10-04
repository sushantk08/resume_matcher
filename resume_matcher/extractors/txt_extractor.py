"""
Text extractor for plain text (.txt) and Markdown (.md) documents.
"""

import io
from typing import Union
from resume_matcher.extractors.base import BaseExtractor, ExtractionError


class TxtExtractor(BaseExtractor):
    """Extractor for plain text, CSV, and Markdown files."""

    ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "ascii"]

    def extract_from_file(self, file_path: str) -> str:
        """Extract text from a .txt or .md file."""
        self._validate_file_path(file_path)

        for encoding in self.ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                    return self._clean_raw_text(content)
            except (UnicodeDecodeError, LookupError):
                continue
            except Exception as e:
                raise ExtractionError(f"Failed to read file {file_path}: {e}") from e

        raise ExtractionError(
            f"Unable to decode text file '{file_path}' using supported encodings: {self.ENCODINGS}"
        )

    def extract_from_bytes(self, file_bytes: Union[bytes, io.BytesIO], filename: str = "") -> str:
        """Extract text from an in-memory byte buffer."""
        if isinstance(file_bytes, io.BytesIO):
            raw_bytes = file_bytes.getvalue()
        elif isinstance(file_bytes, bytes):
            raw_bytes = file_bytes
        else:
            raise ExtractionError(f"Unsupported byte type: {type(file_bytes)}")

        if not raw_bytes:
            return ""

        for encoding in self.ENCODINGS:
            try:
                content = raw_bytes.decode(encoding)
                return self._clean_raw_text(content)
            except (UnicodeDecodeError, LookupError):
                continue

        raise ExtractionError(
            f"Unable to decode byte content using supported encodings: {self.ENCODINGS}"
        )

    @staticmethod
    def _clean_raw_text(text: str) -> str:
        """Normalize line endings and remove null bytes."""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("\x00", "")
        return text.strip()