import unittest
import tempfile
import os
from resume_matcher.extractors import TxtExtractor, ExtractionError


class TestTxtExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = TxtExtractor()

    def test_extract_from_plain_text_file(self):
        sample_text = "Software Engineer\nExperience with Python and SQL."
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".txt") as f:
            f.write(sample_text)
            temp_path = f.name

        try:
            extracted = self.extractor.extract_from_file(temp_path)
            self.assertEqual(extracted, sample_text)
        finally:
            os.remove(temp_path)

    def test_extract_from_bytes(self):
        sample_text = "Data Scientist\nMachine Learning Specialist."
        byte_data = sample_text.encode("utf-8")
        extracted = self.extractor.extract_from_bytes(byte_data)
        self.assertEqual(extracted, sample_text)

    def test_missing_file_raises_error(self):
        with self.assertRaises(ExtractionError):
            self.extractor.extract_from_file("non_existent_file.txt")

    def test_empty_file_raises_error(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            with self.assertRaises(ExtractionError):
                self.extractor.extract_from_file(temp_path)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()