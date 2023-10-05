"""
Text cleaning and normalization module.
"""

import re
import unicodedata


class TextCleaner:
    """Cleans and standardizes raw text extracted from documents."""

    # Unicode bullet characters (includes dots, squares, arrows, triangles, stars, checkmarks)
    BULLETS_PATTERN = re.compile(
        r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\u25CB\u25B6\u25BA\u25C4\u25BC\u25B2\u27A4\u2713\u2714\u2605\u2013\u2014\*\-]"
    )

    # URLs and email addresses
    URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    # Phone numbers
    PHONE_PATTERN = re.compile(
        r"(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}\b"
    )

    @classmethod
    def clean(
        cls,
        text: str,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_phones: bool = True,
        lowercase: bool = False,
    ) -> str:
        """
        Normalize and clean raw document text.

        Args:
            text: Input raw string.
            remove_urls: If True, strips web URLs.
            remove_emails: If True, strips email addresses.
            remove_phones: If True, strips phone numbers.
            lowercase: If True, converts text to lowercase.

        Returns:
            Normalized and cleaned text.
        """
        if not text:
            return ""

        # 1. Unicode normalization (convert fancy quotes, non-breaking spaces, accents)
        normalized = unicodedata.normalize("NFKC", text)
        normalized = normalized.replace("\xa0", " ")

        # 2. Strip URLs, emails, and phone numbers
        if remove_urls:
            normalized = cls.URL_PATTERN.sub(" ", normalized)
        if remove_emails:
            normalized = cls.EMAIL_PATTERN.sub(" ", normalized)
        if remove_phones:
            normalized = cls.PHONE_PATTERN.sub(" ", normalized)

        # 3. Replace bullet characters with space
        normalized = cls.BULLETS_PATTERN.sub(" ", normalized)

        # 4. Normalize multiple whitespace and empty line sequences
        normalized = re.sub(r"[ \t]+", " ", normalized)
        normalized = re.sub(r"\n\s*\n+", "\n\n", normalized)

        if lowercase:
            normalized = normalized.lower()

        return normalized.strip()