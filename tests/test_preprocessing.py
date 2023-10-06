import unittest
from resume_matcher.preprocessing import TextCleaner, get_stopwords, NLPPipeline


class TestPreprocessing(unittest.TestCase):

    def test_cleaner_removes_urls_and_emails(self):
        raw = "Contact me at john.doe@example.com or visit https://johndoe.dev for projects."
        cleaned = TextCleaner.clean(raw, remove_urls=True, remove_emails=True)
        self.assertNotIn("john.doe@example.com", cleaned)
        self.assertNotIn("https://johndoe.dev", cleaned)
        self.assertIn("Contact me at", cleaned)

    def test_nlp_pipeline_tokens_and_chunks(self):
        sample = "Senior Python Engineer developing machine learning pipelines in AWS cloud."
        tokens = NLPPipeline.extract_tokens(sample)
        
        self.assertIn("python", tokens)
        self.assertIn("engineer", tokens)
        self.assertIn("pipeline", tokens)
        self.assertIn("cloud", tokens)

        chunks = NLPPipeline.extract_noun_chunks(sample)
        self.assertTrue(any("machine learning" in c for c in chunks) or any("python" in c for c in chunks))


if __name__ == "__main__":
    unittest.main()