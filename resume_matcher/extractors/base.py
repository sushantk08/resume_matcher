"""
Abstract base class for all document extractors.
"""

from abc import ABC, abstractmethod
from typing import Union
import os
import io


class ExtractionError(Exception):
    """Raised when an error occurs during document extraction."""
    pass


class BaseExtractor(ABC):
    """Abstract base class defining the document extraction interface."""

    @abstractmethod
    def extract_from_file(self, file_path: str) -> str:
        """
        Extract text content from a file path.

        Args:
            file_path: Path to the target document.

        Returns:
            Extracted text as a string.

        Raises:
            ExtractionError: If the file cannot be read or processed.
        """
        pass

    @abstractmethod
    def extract_from_bytes(self, file_bytes: Union[bytes, io.BytesIO], filename: str = "") -> str:
        """
        Extract text content from an in-memory byte buffer (e.g. Streamlit file upload).

        Args:
            file_bytes: Raw bytes or BytesIO stream.
            filename: Optional original filename for format validation.

        Returns:
            Extracted text as a string.

        Raises:
            ExtractionError: If the bytes cannot be decoded or processed.
        """
        pass

    def _validate_file_path(self, file_path: str) -> None:
        """Validate that a file exists and is accessible."""
        if not os.path.exists(file_path):
            raise ExtractionError(f"File not found: {file_path}")
        if not os.path.isfile(file_path):
            raise ExtractionError(f"Target path is not a file: {file_path}")
        if os.path.getsize(file_path) == 0:
            raise ExtractionError(f"File is empty: {file_path}")