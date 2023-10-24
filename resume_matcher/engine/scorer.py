"""
Multi-factor fit scoring engine combining lexical, semantic, and skill signals.
"""

from typing import Dict, Any


class FitScorer:
    """Calculates composite fit scores and qualitative tiers."""

    DEFAULT_WEIGHTS = {
        "semantic": 0.35,  # sentence-transformers dense embedding score
        "tfidf": 0.30,     # scikit-learn TF-IDF lexical score
        "skills": 0.35,    # Hard skills coverage ratio
    }

    @classmethod
    def calculate_composite_score(
        cls,
        tfidf_score: float,
        semantic_score: float,
        skill_coverage_score: float,
        weights: Dict[str, float] = None,
    ) -> Dict[str, Any]:
        """
        Compute weighted composite fit score.

        Args:
            tfidf_score: Lexical similarity (0.0 to 1.0).
            semantic_score: Dense embedding similarity (0.0 to 1.0).
            skill_coverage_score: Skills coverage ratio (0.0 to 1.0).
            weights: Optional custom weights dictionary.

        Returns:
            Dictionary with overall score, percentage, sub-scores, and qualitative grade.
        """
        w = weights or cls.DEFAULT_WEIGHTS
        total_weight = w.get("semantic", 0.35) + w.get("tfidf", 0.30) + w.get("skills", 0.35)

        # Normalize weights if sum != 1.0
        w_semantic = w.get("semantic", 0.35) / total_weight
        w_tfidf = w.get("tfidf", 0.30) / total_weight
        w_skills = w.get("skills", 0.35) / total_weight

        composite = (
            (semantic_score * w_semantic) +
            (tfidf_score * w_tfidf) +
            (skill_coverage_score * w_skills)
        )

        overall_percentage = round(composite * 100, 2)
        fit_grade, grade_color = cls._get_fit_tier(overall_percentage)

        return {
            "overall_score": round(composite, 4),
            "overall_percentage": overall_percentage,
            "fit_grade": fit_grade,
            "grade_color": grade_color,
            "sub_scores": {
                "semantic": {
                    "score": round(semantic_score, 4),
                    "percentage": round(semantic_score * 100, 2),
                    "weight": round(w_semantic, 2),
                },
                "tfidf": {
                    "score": round(tfidf_score, 4),
                    "percentage": round(tfidf_score * 100, 2),
                    "weight": round(w_tfidf, 2),
                },
                "skills": {
                    "score": round(skill_coverage_score, 4),
                    "percentage": round(skill_coverage_score * 100, 2),
                    "weight": round(w_skills, 2),
                },
            },
        }

    @staticmethod
    def _get_fit_tier(percentage: float):
        """Assign an evaluation tier based on the final percentage."""
        if percentage >= 80.0:
            return "Strong Match", "green"
        elif percentage >= 65.0:
            return "Good Fit", "blue"
        elif percentage >= 50.0:
            return "Moderate Fit", "orange"
        else:
            return "Low Fit", "red"