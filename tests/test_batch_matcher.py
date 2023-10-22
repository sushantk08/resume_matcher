import unittest
from resume_matcher.engine import ResumeMatcher, BatchMatcher


class TestBatchMatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.matcher = ResumeMatcher()
        cls.batch_matcher = BatchMatcher(cls.matcher)

    def test_ranking_order_descending(self):
        strong_resume = (
            "Senior Backend Engineer with 6 years experience in Python, FastAPI, and PostgreSQL.\n"
            "Deployed containers with Docker onto AWS using Kubernetes and CI/CD pipelines."
        )
        weak_resume = (
            "Frontend developer experienced in HTML, CSS, React, and Figma design.\n"
            "Built personal portfolios and UI wireframes."
        )
        target_jd = (
            "Seeking a Senior Python Backend Developer with FastAPI, PostgreSQL, Docker, and AWS."
        )

        leaderboard = self.batch_matcher.rank_candidates(
            resumes=[weak_resume, strong_resume],
            filenames=["weak_candidate.txt", "strong_candidate.txt"],
            jd_input=target_jd,
        )

        # 1. Verify 2 candidates processed
        self.assertEqual(len(leaderboard), 2)

        # 2. Verify strong candidate ranked #1
        self.assertEqual(leaderboard[0]["rank"], 1)
        self.assertEqual(leaderboard[0]["candidate"], "strong_candidate.txt")
        self.assertEqual(leaderboard[1]["rank"], 2)
        self.assertEqual(leaderboard[1]["candidate"], "weak_candidate.txt")

        # 3. Verify score ordering
        self.assertGreater(leaderboard[0]["overall_percentage"], leaderboard[1]["overall_percentage"])

    def test_dataframe_conversion(self):
        mock_leaderboard = [
            {
                "rank": 1,
                "candidate": "candidate_a.pdf",
                "overall_percentage": 88.5,
                "fit_grade": "Strong Match",
                "grade_color": "green",
                "semantic_score": 85.0,
                "skills_score": 90.0,
                "tfidf_score": 89.0,
                "matched_skills": ["Python", "Docker", "AWS"],
                "missing_skills": ["Kubernetes"],
            }
        ]
        df = BatchMatcher.to_dataframe(mock_leaderboard)
        self.assertEqual(len(df), 1)
        self.assertIn("Rank", df.columns)
        self.assertIn("Candidate File", df.columns)
        self.assertIn("Overall Fit", df.columns)
        self.assertEqual(df.iloc[0]["Rank"], "#1")


if __name__ == "__main__":
    unittest.main()