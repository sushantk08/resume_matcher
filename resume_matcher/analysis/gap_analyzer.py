"""
Keyword and skill gap analyzer comparing resumes against job descriptions.
"""

from typing import Dict, List, Any
from resume_matcher.analysis.skill_extractor import SkillExtractor
from resume_matcher.preprocessing.nlp_pipeline import NLPPipeline


class GapAnalyzer:
    """Analyzes technical skill coverage and keyword gaps between resume and JD."""

    def __init__(self, skill_extractor: SkillExtractor = None):
        self.skill_extractor = skill_extractor or SkillExtractor()

    def analyze(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Perform complete gap analysis between resume and job description.

        Args:
            resume_text: Extracted resume text.
            jd_text: Extracted job description text.

        Returns:
            Dictionary containing matched skills, missing skills, coverage score,
            and tailoring recommendations.
        """
        resume_skills_data = self.skill_extractor.extract_skills(resume_text)
        jd_skills_data = self.skill_extractor.extract_skills(jd_text)

        resume_skills = set(resume_skills_data["skills"])
        jd_skills = set(jd_skills_data["skills"])

        # Set operations
        matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
        missing_skills = sorted(list(jd_skills.difference(resume_skills)))
        additional_skills = sorted(list(resume_skills.difference(jd_skills)))

        # Skill match percentage
        total_jd_skills = len(jd_skills)
        if total_jd_skills > 0:
            coverage_pct = round((len(matched_skills) / total_jd_skills) * 100, 2)
        else:
            coverage_pct = 100.0 if len(resume_skills) > 0 else 0.0

        # Detailed breakdown with categories
        missing_by_category = self._group_by_category(missing_skills)
        matched_by_category = self._group_by_category(matched_skills)

        # Generate actionable resume tailoring recommendations
        recommendations = self._generate_recommendations(
            missing_skills=missing_skills,
            missing_by_category=missing_by_category,
            coverage_pct=coverage_pct,
        )

        return {
            "skill_coverage_percentage": coverage_pct,
            "total_jd_skills": total_jd_skills,
            "total_resume_skills": len(resume_skills),
            "matched_skills": matched_skills,
            "matched_by_category": matched_by_category,
            "missing_skills": missing_skills,
            "missing_by_category": missing_by_category,
            "additional_skills": additional_skills,
            "recommendations": recommendations,
        }

    def _group_by_category(self, skills: List[str]) -> Dict[str, List[str]]:
        """Group a list of skills by their technical category."""
        grouped: Dict[str, List[str]] = {}
        for skill in skills:
            cat = self.skill_extractor._get_category_for_skill(skill)
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(skill)
        return grouped

    def _generate_recommendations(
        self,
        missing_skills: List[str],
        missing_by_category: Dict[str, List[str]],
        coverage_pct: float,
    ) -> List[str]:
        """Generate tailored advice based on gaps identified."""
        recs = []

        if coverage_pct >= 85.0:
            recs.append("Strong technical alignment: Your resume covers most primary competencies requested in the job description.")
        elif coverage_pct >= 60.0:
            recs.append("Moderate alignment: Your core profile fits, but adding key missing technologies will significantly boost ATS ranking.")
        else:
            recs.append("Low direct skill overlap: Consider explicitly incorporating the target role's core technical stack into your project descriptions.")

        for category, skills in missing_by_category.items():
            if skills:
                skill_list = ", ".join(f"'{s}'" for s in skills[:4])
                recs.append(
                    f"Missing {category}: Consider mentioning your experience or projects with {skill_list}."
                )

        if len(missing_skills) > 6:
            recs.append(
                "Tip: If you have academic, project, or hands-on experience with any of the missing tools, create a dedicated 'Technical Skills' summary section at the top of your resume."
            )

        return recs