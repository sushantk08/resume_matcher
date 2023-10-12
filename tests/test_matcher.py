import unittest
from resume_matcher.engine import ResumeMatcher, FitScorer


class TestResumeMatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.matcher = ResumeMatcher()

    def test_composite_scoring_calculation(self):
        score_data = FitScorer.calculate_composite_score(
            tfidf_score=0.80,
            semantic_score=0.70,
            skill_coverage_score=0.90,
        )
        self.assertIn("overall_percentage", score_data)
        self.assertGreater(score_data["overall_percentage"], 75.0)
        self.assertEqual(score_data["fit_grade"], "Strong Match")

    def test_end_to_end_matching_pipeline(self):
        resume = (
            "Senior Backend Engineer with 5 years experience in Python, FastAPI, and PostgreSQL.\n"
            "Proficient in Docker containerization and AWS deployments.\n"
            "Built automated CI/CD pipelines using GitHub Actions."
        )
        jd = (
            "Looking for a Senior Python Developer with expertise in FastAPI and PostgreSQL.\n"
            "Experience with Docker, Kubernetes, and AWS required.\n"
            "Must be familiar with CI/CD."
        )

        result = self.matcher.match(resume, jd)

        # Check overarching structure
        self.assertIn("overall_fit", result)
        self.assertIn("lexical_analysis", result)
        self.assertIn("semantic_analysis", result)
        self.assertIn("skill_analysis", result)

        overall = result["overall_fit"]
        # Calibrated threshold for partial skill match
        self.assertGreater(overall["overall_percentage"], 60.0)

        # Check matched skills
        matched = result["skill_analysis"]["matched_skills"]
        self.assertIn("Python", matched)
        self.assertIn("FastAPI", matched)
        self.assertIn("Docker", matched)
        self.assertIn("AWS", matched)

        # Check missing skill
        self.assertIn("Kubernetes", result["skill_analysis"]["missing_skills"])


if __name__ == "__main__":
    unittest.main()