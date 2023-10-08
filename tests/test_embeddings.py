import unittest
from resume_matcher.models import EmbeddingMatcher


class TestEmbeddingMatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.matcher = EmbeddingMatcher()

    def test_semantic_paraphrase_high_score(self):
        # Lexically distinct but semantically aligned phrases
        resume = "Architected scalable backend infrastructure and distributed microservices with Python."
        jd = "Designed high-availability cloud server architectures using Python backend components."

        result = self.matcher.match(resume, jd)
        # 0.60+ is a strong semantic similarity threshold for paraphrased technical sentences
        self.assertGreater(result["score"], 0.60)
        self.assertGreater(result["percentage"], 60.0)

    def test_unrelated_documents_low_score(self):
        resume = "Experienced kindergarten teacher specializing in early childhood literacy and play."
        jd = "Low-level C++ engineer developing high-frequency trading engines and FPGA drivers."

        result = self.matcher.match(resume, jd)
        self.assertLess(result["score"], 0.35)

    def test_sentence_alignment(self):
        resume = (
            "Profile\n"
            "Led migration of PostgreSQL databases to AWS RDS with zero downtime.\n"
            "Built automated CI/CD pipelines using GitHub Actions and Docker."
        )
        jd = (
            "Requirements\n"
            "Must have experience managing relational database migrations in AWS.\n"
            "Responsible for building continuous deployment workflows."
        )

        alignments = self.matcher.find_best_alignments(resume, jd, top_k=2)
        self.assertTrue(len(alignments) > 0)
        self.assertIn("PostgreSQL", alignments[0]["matched_resume_experience"])


if __name__ == "__main__":
    unittest.main()