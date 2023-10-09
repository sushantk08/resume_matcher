"""
Domain intelligence and skill analysis module.
"""

from resume_matcher.analysis.taxonomy import SKILL_TAXONOMY, SKILL_ALIASES
from resume_matcher.analysis.skill_extractor import SkillExtractor

__all__ = [
    "SKILL_TAXONOMY",
    "SKILL_ALIASES",
    "SkillExtractor",
]