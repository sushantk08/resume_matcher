import unittest
from resume_matcher.analysis import SkillExtractor


class TestSkillExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = SkillExtractor()

    def test_single_and_multi_word_skills(self):
        text = "Experienced in Python, Machine Learning, Docker, and PostgreSQL databases."
        result = self.extractor.extract_skills(text)

        skills = result["skills"]
        self.assertIn("Python", skills)
        self.assertIn("Machine Learning", skills)
        self.assertIn("Docker", skills)
        self.assertIn("PostgreSQL", skills)

    def test_punctuated_skills(self):
        text = "Proficient in C++, C#, .NET core, Node.js, and automated CI/CD workflows."
        result = self.extractor.extract_skills(text)

        skills = result["skills"]
        self.assertIn("C++", skills)
        self.assertIn("C#", skills)
        self.assertIn(".NET", skills)
        self.assertIn("Node.js", skills)
        self.assertIn("CI/CD", skills)

    def test_alias_normalization(self):
        text = "Hands-on experience with K8s, reactjs, and postgres."
        result = self.extractor.extract_skills(text)

        skills = result["skills"]
        # Aliases mapped to canonical display names
        self.assertIn("Kubernetes", skills)
        self.assertIn("React", skills)
        self.assertIn("PostgreSQL", skills)

    def test_categorization(self):
        text = "Python developer deploying Docker containers to AWS with PostgreSQL."
        result = self.extractor.extract_skills(text)

        by_cat = result["by_category"]
        self.assertIn("Languages", by_cat)
        self.assertIn("Python", by_cat["Languages"])
        self.assertIn("Cloud & DevOps", by_cat)
        self.assertIn("Docker", by_cat["Cloud & DevOps"])
        self.assertIn("AWS", by_cat["Cloud & DevOps"])
        self.assertIn("Databases & Storage", by_cat)
        self.assertIn("PostgreSQL", by_cat["Databases & Storage"])


if __name__ == "__main__":
    unittest.main()