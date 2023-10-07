import unittest
from resume_matcher.models import TfidfMatcher, compute_cosine_similarity


class TestTfidfMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = TfidfMatcher(ngram_range=(1, 2))

    def test_identical_documents_score_high(self):
        text = "Senior Python Engineer with Docker, Kubernetes, AWS, and PostgreSQL experience."
        result = self.matcher.match(text, text)
        self.assertAlmostEqual(result["score"], 1.0, places=2)
        self.assertAlmostEqual(result["percentage"], 100.0, places=1)
        self.assertTrue(len(result["top_keywords"]) > 0)

    def test_unrelated_documents_score_low(self):
        resume = "Professional pastry chef specializing in French bakery, cakes, and desserts."
        jd = "Senior Distributed Systems Engineer working with C++, Rust, and Linux kernel."
        result = self.matcher.match(resume, jd)
        self.assertLess(result["score"], 0.15)

    def test_top_keyword_contribution(self):
        resume = "Python Developer building REST APIs with FastAPI, Docker, and PostgreSQL."
        jd = "Looking for a Python Developer to build FastAPI backend services using PostgreSQL and Docker."
        result = self.matcher.match(resume, jd)
        
        matched_terms = [k["term"] for k in result["top_keywords"]]
        self.assertIn("python", matched_terms)
        self.assertIn("fastapi", matched_terms)
        self.assertIn("docker", matched_terms)
        self.assertIn("postgresql", matched_terms)

    def test_empty_input_handling(self):
        result = self.matcher.match("", "Some JD text")
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["percentage"], 0.0)
        self.assertEqual(result["top_keywords"], [])


if __name__ == "__main__":
    unittest.main()