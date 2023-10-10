import unittest
from resume_matcher.analysis import GapAnalyzer


class TestGapAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = GapAnalyzer()

    def test_complete_gap_analysis(self):
        resume = (
            "Senior Backend Engineer with strong expertise in Python, Django, and PostgreSQL.\n"
            "Deployed containers with Docker onto Linux servers."
        )
        jd = (
            "Seeking a Senior Backend Engineer proficient in Python, PostgreSQL, Docker, and AWS.\n"
            "Must have experience with Kubernetes and CI/CD pipelines."
        )

        result = self.analyzer.analyze(resume, jd)

        # Matched skills check
        self.assertIn("Python", result["matched_skills"])
        self.assertIn("PostgreSQL", result["matched_skills"])
        self.assertIn("Docker", result["matched_skills"])

        # Missing skills check
        self.assertIn("AWS", result["missing_skills"])
        self.assertIn("Kubernetes", result["missing_skills"])
        self.assertIn("CI/CD", result["missing_skills"])

        # Coverage percentage check (3 matched out of 6 JD skills = 50.0%)
        self.assertEqual(result["skill_coverage_percentage"], 50.0)

        # Recommendations generated
        self.assertTrue(len(result["recommendations"]) > 0)
        self.assertTrue(any("Cloud & DevOps" in r for r in result["recommendations"]))


if __name__ == "__main__":
    unittest.main()