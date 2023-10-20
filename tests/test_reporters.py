import unittest
import json
from resume_matcher.reporting import JSONReporter, HTMLReporter


class TestReporters(unittest.TestCase):

    def setUp(self):
        self.mock_results = {
            "overall_fit": {
                "overall_score": 0.785,
                "overall_percentage": 78.5,
                "fit_grade": "Good Fit",
                "grade_color": "blue",
                "sub_scores": {
                    "semantic": {"score": 0.80, "percentage": 80.0, "weight": 0.35},
                    "skills": {"score": 0.75, "percentage": 75.0, "weight": 0.35},
                    "tfidf": {"score": 0.81, "percentage": 81.0, "weight": 0.30},
                },
            },
            "lexical_analysis": {
                "top_keywords": [{"term": "python", "contribution": 0.25, "resume_weight": 0.5, "jd_weight": 0.5}]
            },
            "semantic_analysis": {
                "score": 0.80,
                "percentage": 80.0,
                "top_alignments": [
                    {"jd_requirement": "Python experience", "matched_resume_experience": "5 yrs Python", "alignment_score": 0.85}
                ],
            },
            "skill_analysis": {
                "matched_skills": ["Python", "Docker"],
                "missing_skills": ["Kubernetes"],
                "additional_skills": ["PostgreSQL"],
                "recommendations": ["Add Kubernetes experience."],
            },
            "metadata": {"resume_filename": "test_resume.txt", "jd_filename": "test_jd.txt"},
        }

    def test_json_reporter_valid_json(self):
        json_str = JSONReporter.generate(self.mock_results)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["overall_fit"]["overall_percentage"], 78.5)
        self.assertIn("Python", parsed["skill_analysis"]["matched_skills"])

    def test_html_reporter_generates_html(self):
        html_str = HTMLReporter.generate(self.mock_results)
        self.assertIn("<!DOCTYPE html>", html_str)
        self.assertIn("Candidate Fit Evaluation Report", html_str)
        self.assertIn("78.5%", html_str)
        self.assertIn("Kubernetes", html_str)


if __name__ == "__main__":
    unittest.main()