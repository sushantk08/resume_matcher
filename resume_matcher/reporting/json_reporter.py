"""
JSON report generator for resume match results.
"""

import json
from typing import Dict, Any
import numpy as np


class JSONReporter:
    """Serializes match results into clean, portable JSON."""

    @classmethod
    def generate(cls, results: Dict[str, Any], indent: int = 2) -> str:
        """
        Convert match results dictionary to a formatted JSON string.

        Args:
            results: Results dictionary from ResumeMatcher.
            indent: Indentation spaces for pretty printing.

        Returns:
            JSON string representation.
        """
        sanitized = cls._sanitize(results)
        return json.dumps(sanitized, indent=indent, ensure_ascii=False)

    @classmethod
    def _sanitize(cls, data: Any) -> Any:
        """Recursively convert NumPy scalars and arrays to native Python types."""
        if isinstance(data, dict):
            return {k: cls._sanitize(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [cls._sanitize(item) for item in data]
        elif isinstance(data, (np.floating, float)):
            return round(float(data), 4)
        elif isinstance(data, (np.integer, int)):
            return int(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        return data