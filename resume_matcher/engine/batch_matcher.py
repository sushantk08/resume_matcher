"""
Batch candidate ranking and triage engine.
"""

from typing import List, Dict, Any, Union
import io
import pandas as pd
from resume_matcher.engine.matcher import ResumeMatcher


class BatchMatcher:
    """Processes multiple candidates against a target job description and generates ranked leaderboards."""

    def __init__(self, matcher: ResumeMatcher = None):
        self.matcher = matcher or ResumeMatcher()

    def rank_candidates(
        self,
        resumes: List[Union[str, bytes, io.BytesIO]],
        filenames: List[str],
        jd_input: Union[str, bytes, io.BytesIO],
        jd_filename: str = "job_description.txt",
        weights: Dict[str, float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Evaluate and rank a batch of candidate resumes against one job description.

        Args:
            resumes: List of resume files, byte streams, or strings.
            filenames: Corresponding filenames for each resume.
            jd_input: Target job description.
            jd_filename: Filename for the job description.
            weights: Optional custom scoring weights.

        Returns:
            List of candidate evaluation results sorted by overall fit score descending.
        """
        leaderboard = []

        for resume, filename in zip(resumes, filenames):
            res = self.matcher.match(
                resume_input=resume,
                jd_input=jd_input,
                resume_filename=filename,
                jd_filename=jd_filename,
                weights=weights,
            )

            fit = res["overall_fit"]
            skills = res["skill_analysis"]
            sub = fit["sub_scores"]

            leaderboard.append({
                "candidate": filename,
                "overall_percentage": fit["overall_percentage"],
                "fit_grade": fit["fit_grade"],
                "grade_color": fit["grade_color"],
                "semantic_score": sub["semantic"]["percentage"],
                "skills_score": sub["skills"]["percentage"],
                "tfidf_score": sub["tfidf"]["percentage"],
                "matched_skills_count": len(skills["matched_skills"]),
                "missing_skills_count": len(skills["missing_skills"]),
                "matched_skills": skills["matched_skills"],
                "missing_skills": skills["missing_skills"],
                "full_result": res,
            })

        # Sort descending by overall match percentage
        leaderboard.sort(key=lambda x: x["overall_percentage"], reverse=True)

        # Assign 1-indexed ranks
        for rank, item in enumerate(leaderboard, 1):
            item["rank"] = rank

        return leaderboard

    @staticmethod
    def to_dataframe(leaderboard: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert a ranked leaderboard list to a display DataFrame."""
        rows = []
        for c in leaderboard:
            rows.append({
                "Rank": f"#{c['rank']}",
                "Candidate File": c["candidate"],
                "Overall Fit": f"{c['overall_percentage']}%",
                "Tier": c["fit_grade"],
                "Semantic": f"{c['semantic_score']}%",
                "Hard Skills": f"{c['skills_score']}%",
                "Keywords": f"{c['tfidf_score']}%",
                "Matched Skills": ", ".join(c["matched_skills"][:4]) + ("..." if len(c["matched_skills"]) > 4 else ""),
                "Missing Skills": ", ".join(c["missing_skills"][:3]) + ("..." if len(c["missing_skills"]) > 3 else ""),
            })
        return pd.DataFrame(rows)