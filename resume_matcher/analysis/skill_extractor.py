"""
Technical skill extractor using spaCy PhraseMatcher and pattern recognition.
"""

import re
from typing import Dict, List, Set, Any
from collections import Counter
import spacy
from spacy.matcher import PhraseMatcher

from resume_matcher.preprocessing.nlp_pipeline import NLPPipeline
from resume_matcher.analysis.taxonomy import SKILL_TAXONOMY, SKILL_ALIASES


class SkillExtractor:
    """Extracts and categorizes technical skills from resumes and job descriptions."""

    def __init__(self):
        self.nlp = NLPPipeline.get_nlp()
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.skill_to_category: Dict[str, str] = {}
        
        # Inverted index: canonical skill -> category
        for category, skills in SKILL_TAXONOMY.items():
            for skill in skills:
                self.skill_to_category[skill.lower()] = category

        # Build spaCy phrase patterns for skills and aliases
        patterns = []
        for category, skills in SKILL_TAXONOMY.items():
            for skill in skills:
                patterns.append(self.nlp.make_doc(skill))

        for alias in SKILL_ALIASES.keys():
            patterns.append(self.nlp.make_doc(alias))

        self.matcher.add("TECHNICAL_SKILLS", patterns)

        # Explicit regex for punctuation-sensitive terms that tokenizers might split
        self.punct_skills_patterns = {
            "C++": re.compile(r"\bC\+\+\b", re.IGNORECASE),
            "C#": re.compile(r"\bC\#\b", re.IGNORECASE),
            ".NET": re.compile(r"(?:\b|\s)\.NET\b", re.IGNORECASE),
            "CI/CD": re.compile(r"\bCI\/CD\b", re.IGNORECASE),
            "Node.js": re.compile(r"\bNode\.js\b", re.IGNORECASE),
            "Next.js": re.compile(r"\bNext\.js\b", re.IGNORECASE),
            "Vue.js": re.compile(r"\bVue\.js\b", re.IGNORECASE),
        }

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Extract categorized technical skills and frequencies from text.

        Args:
            text: Raw input text from resume or job description.

        Returns:
            Dictionary containing list of skills, category groupings, and counts.
        """
        if not text or not text.strip():
            return {
                "skills": [],
                "by_category": {},
                "counts": {},
                "total_skills": 0,
            }

        doc = self.nlp(text)
        detected_canonical: List[str] = []

        # 1. Match via spaCy PhraseMatcher
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            span_text = span.text.strip().lower()

            # Check if it's an alias or canonical skill
            if span_text in SKILL_ALIASES:
                canonical = SKILL_ALIASES[span_text]
            else:
                # Find matching canonical title from taxonomy
                canonical = next(
                    (s for s in self.skill_to_category if s == span_text),
                    span.text.title()
                )
                # Map back to display case
                canonical = self._to_display_case(canonical)

            detected_canonical.append(canonical)

        # 2. Match punctuation-sensitive skills via regex
        for skill_name, pattern in self.punct_skills_patterns.items():
            found_count = len(pattern.findall(text))
            for _ in range(found_count):
                detected_canonical.append(skill_name)

        if not detected_canonical:
            return {
                "skills": [],
                "by_category": {},
                "counts": {},
                "total_skills": 0,
            }

        # Count frequencies and deduplicate
        counts = dict(Counter(detected_canonical))
        unique_skills = sorted(list(counts.keys()))

        # Group by category
        by_category: Dict[str, List[str]] = {}
        for skill in unique_skills:
            cat = self._get_category_for_skill(skill)
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(skill)

        return {
            "skills": unique_skills,
            "by_category": by_category,
            "counts": counts,
            "total_skills": len(unique_skills),
        }

    def _get_category_for_skill(self, skill: str) -> str:
        """Resolve category for a canonical skill name."""
        skill_lower = skill.lower()
        if skill_lower in self.skill_to_category:
            return self.skill_to_category[skill_lower]
        # Check alias
        if skill_lower in SKILL_ALIASES:
            canonical = SKILL_ALIASES[skill_lower].lower()
            return self.skill_to_category.get(canonical, "Other Technical")
        return "Other Technical"

    @staticmethod
    def _to_display_case(skill_lower: str) -> str:
        """Find the original case from taxonomy."""
        for skills in SKILL_TAXONOMY.values():
            for s in skills:
                if s.lower() == skill_lower:
                    return s
        return skill_lower.title()