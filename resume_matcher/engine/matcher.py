"""
Master orchestrator connecting document extractors, models, and gap analysis.
"""

from typing import Union, Dict, Any
import io

from resume_matcher.extractors import DocumentExtractorFactory
from resume_matcher.models import TfidfMatcher, EmbeddingMatcher
from resume_matcher.analysis import GapAnalyzer, SkillExtractor
from resume_matcher.engine.scorer import FitScorer


class ResumeMatcher:
    """End-to-end resume to job description fit evaluation orchestrator."""

    def __init__(
        self,
        tfidf_matcher: TfidfMatcher = None,
        embedding_matcher: EmbeddingMatcher = None,
        gap_analyzer: GapAnalyzer = None,
    ):
        self.tfidf_matcher = tfidf_matcher or TfidfMatcher()
        self.embedding_matcher = embedding_matcher or EmbeddingMatcher()
        self.gap_analyzer = gap_analyzer or GapAnalyzer()

    def match(
        self,
        resume_input: Union[str, bytes, io.BytesIO],
        jd_input: Union[str, bytes, io.BytesIO],
        resume_filename: str = "resume.txt",
        jd_filename: str = "job_description.txt",
        weights: Dict[str, float] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate fit between a resume and job description.

        Args:
            resume_input: File path, text string, raw bytes, or stream.
            jd_input: File path, text string, raw bytes, or stream.
            resume_filename: Filename used for extractor format detection.
            jd_filename: Filename used for extractor format detection.
            weights: Optional custom scoring weights.

        Returns:
            Comprehensive match results dictionary.
        """
        # 1. Document Extraction
        resume_text = self._resolve_text(resume_input, resume_filename)
        jd_text = self._resolve_text(jd_input, jd_filename)

        # 2. TF-IDF Lexical Match & Key Contributors
        tfidf_res = self.tfidf_matcher.match(resume_text, jd_text)

        # 3. Dense Embedding Semantic Match & Sentence Alignment
        emb_res = self.embedding_matcher.match(resume_text, jd_text)
        alignments = self.embedding_matcher.find_best_alignments(resume_text, jd_text, top_k=5)

        # 4. Technical Skill Gap Analysis
        gap_res = self.gap_analyzer.analyze(resume_text, jd_text)

        # 5. Composite Fit Scoring
        score_breakdown = FitScorer.calculate_composite_score(
            tfidf_score=tfidf_res["score"],
            semantic_score=emb_res["score"],
            skill_coverage_score=gap_res["skill_coverage_percentage"] / 100.0,
            weights=weights,
        )

        return {
            "overall_fit": score_breakdown,
            "lexical_analysis": tfidf_res,
            "semantic_analysis": {
                "score": emb_res["score"],
                "percentage": emb_res["percentage"],
                "top_alignments": alignments,
            },
            "skill_analysis": gap_res,
            "metadata": {
                "resume_char_count": len(resume_text),
                "jd_char_count": len(jd_text),
                "resume_filename": resume_filename,
                "jd_filename": jd_filename,
            },
        }

    @staticmethod
    def _resolve_text(doc_input: Union[str, bytes, io.BytesIO], filename: str) -> str:
        """Resolve input into raw text string."""
        if isinstance(doc_input, str):
            # If string looks like a file path that exists, extract it
            import os
            if os.path.exists(doc_input) and os.path.isfile(doc_input):
                return DocumentExtractorFactory.extract_text(doc_input, filename=doc_input)
            # Otherwise treat as raw text content directly
            return doc_input

        # Byte or stream input (e.g. Streamlit uploaded file)
        return DocumentExtractorFactory.extract_text(doc_input, filename=filename)