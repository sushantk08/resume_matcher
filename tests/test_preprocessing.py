import unittest
from resume_matcher.preprocessing import TextCleaner, get_stopwords


class TestPreprocessing(unittest.TestCase):

    def test_cleaner_removes_urls_and_emails(self):
        raw = "Contact me at john.doe@example.com or visit https://johndoe.dev for projects."
        cleaned = TextCleaner.clean(raw, remove_urls=True, remove_emails=True)
        self.assertNotIn("john.doe@example.com", cleaned)
        self.assertNotIn("https://johndoe.dev", cleaned)
        self.assertIn("Contact me at", cleaned)
        self.assertIn("for projects.", cleaned)

    def test_cleaner_normalizes_bullets(self):
        raw = "• Python\n▪ Docker\n★ Kubernetes\n► CI/CD"
        cleaned = TextCleaner.clean(raw)
        self.assertNotIn("•", cleaned)
        self.assertNotIn("▪", cleaned)
        self.assertNotIn("★", cleaned)
        self.assertNotIn("►", cleaned)
        self.assertIn("Python", cleaned)
        self.assertIn("CI/CD", cleaned)

    def test_stopwords_retrieval(self):
        general = get_stopwords(include_domain=False)
        self.assertIn("the", general)
        self.assertIn("and", general)
        self.assertNotIn("resume", general)

        domain = get_stopwords(include_domain=True)
        self.assertIn("resume", domain)
        self.assertIn("responsibilities", domain)


if __name__ == "__main__":
    unittest.main()