"""
TF-IDF Vectorizer and similarity scoring using scikit-learn.
"""

from typing import Dict, List, Tuple, Any
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_matcher.preprocessing.cleaner import TextCleaner
from resume_matcher.preprocessing.stopwords import get_stopwords


class TfidfMatcher:
    """Computes TF-IDF lexical match and feature attribution between documents."""

    def __init__(
        self,
        ngram_range: Tuple[int, int] = (1, 2),
        sublinear_tf: bool = True,
        min_df: int = 1,
    ):
        """
        Initialize the TF-IDF Matcher.

        Args:
            ngram_range: Lower and upper boundary of n-grams (1, 2 = unigrams + bigrams).
            sublinear_tf: Apply sublinear scaling (1 + log(tf)) to dampen word frequency dominance.
            min_df: Minimum document frequency for terms.
        """
        raw_stopwords = get_stopwords(include_domain=True)
        # Strip contractions to keep stop words strictly alphanumeric for sklearn's internal tokenizer
        clean_stopwords = set()
        for w in raw_stopwords:
            sub_tokens = re.findall(r"\b\w+\b", w.lower())
            clean_stopwords.update(sub_tokens)

        self.stopwords = sorted(list(clean_stopwords))
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            sublinear_tf=sublinear_tf,
            min_df=min_df,
            stop_words=self.stopwords,
            lowercase=True,
            token_pattern=r"(?u)\b[\w\+\#\.\/]{2,}\b",  # Preserves tokens like C++, C#, .NET, CI/CD
        )

    def match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Score the fit between a resume and job description using TF-IDF.

        Args:
            resume_text: Text content of the resume.
            jd_text: Text content of the job description.

        Returns:
            Dictionary containing similarity score, percentage, and top contributing keywords.
        """
        clean_resume = TextCleaner.clean(resume_text, lowercase=True)
        clean_jd = TextCleaner.clean(jd_text, lowercase=True)

        if not clean_resume.strip() or not clean_jd.strip():
            return {
                "score": 0.0,
                "percentage": 0.0,
                "top_keywords": [],
                "terms_analyzed": 0,
            }

        # Fit vectorizer on both documents
        tfidf_matrix = self.vectorizer.fit_transform([clean_resume, clean_jd])
        resume_vec = tfidf_matrix[0]
        jd_vec = tfidf_matrix[1]

        # Compute cosine similarity
        raw_sim = float(cosine_similarity(resume_vec, jd_vec)[0][0])
        sim_score = float(np.clip(raw_sim, 0.0, 1.0))

        # Extract top contributing keywords to the similarity score
        top_keywords = self._extract_top_contributors(resume_vec, jd_vec, top_k=15)

        return {
            "score": sim_score,
            "percentage": round(sim_score * 100, 2),
            "top_keywords": top_keywords,
            "terms_analyzed": tfidf_matrix.shape[1],
        }

    def _extract_top_contributors(
        self,
        resume_vec,
        jd_vec,
        top_k: int = 15,
    ) -> List[Dict[str, Any]]:
        """Identify which shared terms contributed most to the dot product."""
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        
        # Element-wise product of TF-IDF weights
        prod_vector = (resume_vec.toarray()[0] * jd_vec.toarray()[0])
        non_zero_indices = np.where(prod_vector > 0)[0]

        if len(non_zero_indices) == 0:
            return []

        # Sort by contribution descending
        sorted_indices = non_zero_indices[np.argsort(-prod_vector[non_zero_indices])]
        top_indices = sorted_indices[:top_k]

        contributors = []
        resume_weights = resume_vec.toarray()[0]
        jd_weights = jd_vec.toarray()[0]

        for idx in top_indices:
            term = feature_names[idx]
            contributors.append({
                "term": term,
                "contribution": float(round(prod_vector[idx], 4)),
                "resume_weight": float(round(resume_weights[idx], 4)),
                "jd_weight": float(round(jd_weights[idx], 4)),
            })

        return contributors