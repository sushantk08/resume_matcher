"""
Dense neural embedding matcher using sentence-transformers.
"""

from typing import Dict, List, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from resume_matcher.preprocessing.cleaner import TextCleaner
from resume_matcher.models.similarity import compute_cosine_similarity


class EmbeddingMatcher:
    """Computes dense neural semantic similarity and sentence-level alignment."""

    _model_instance: Optional[SentenceTransformer] = None

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the Embedding Matcher.

        Args:
            model_name: Hugging Face model identifier (defaults to 'all-MiniLM-L6-v2').
        """
        self.model_name = model_name

    @classmethod
    def get_model(cls, model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
        """Lazy load the sentence transformer model to optimize memory and startup."""
        if cls._model_instance is None:
            cls._model_instance = SentenceTransformer(model_name, device="cpu")
        return cls._model_instance

    def encode(self, text_or_list) -> np.ndarray:
        """Encode text or a list of sentences into dense vector embeddings."""
        model = self.get_model(self.model_name)
        return model.encode(text_or_list, show_progress_bar=False, normalize_embeddings=True)

    def match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Compute semantic similarity between full resume and job description.

        Args:
            resume_text: Raw resume text.
            jd_text: Raw job description text.

        Returns:
            Dictionary containing semantic score, percentage, and vector dimensionality.
        """
        clean_resume = TextCleaner.clean(resume_text)
        clean_jd = TextCleaner.clean(jd_text)

        if not clean_resume.strip() or not clean_jd.strip():
            return {
                "score": 0.0,
                "percentage": 0.0,
                "embedding_dim": 0,
            }

        resume_vec = self.encode(clean_resume)
        jd_vec = self.encode(clean_jd)

        sim_score = compute_cosine_similarity(resume_vec, jd_vec)

        return {
            "score": sim_score,
            "percentage": round(sim_score * 100, 2),
            "embedding_dim": int(resume_vec.shape[0]),
        }

    def find_best_alignments(
        self,
        resume_text: str,
        jd_text: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Identify which specific resume bullet points best align with key requirements in the JD.

        Args:
            resume_text: Full resume text.
            jd_text: Full job description text.
            top_k: Number of top aligned sentence pairs to return.

        Returns:
            List of dictionaries pairing JD requirements to the most relevant resume experience.
        """
        # Split documents into meaningful sentences / bullet points
        resume_sentences = [
            s.strip() for s in resume_text.split("\n")
            if len(s.strip().split()) >= 4
        ]
        jd_sentences = [
            s.strip() for s in jd_text.split("\n")
            if len(s.strip().split()) >= 4
        ]

        if not resume_sentences or not jd_sentences:
            return []

        # Encode all sentences
        resume_vecs = self.encode(resume_sentences)
        jd_vecs = self.encode(jd_sentences)

        # Pairwise cosine similarity matrix: shape (num_jd, num_resume)
        similarity_matrix = np.dot(jd_vecs, resume_vecs.T)

        alignments = []
        # Find the best matching resume sentence for each JD requirement
        for jd_idx in range(len(jd_sentences)):
            best_resume_idx = int(np.argmax(similarity_matrix[jd_idx]))
            best_score = float(similarity_matrix[jd_idx][best_resume_idx])

            alignments.append({
                "jd_requirement": jd_sentences[jd_idx],
                "matched_resume_experience": resume_sentences[best_resume_idx],
                "alignment_score": round(best_score, 4),
            })

        # Sort by highest alignment score
        alignments.sort(key=lambda x: x["alignment_score"], reverse=True)
        return alignments[:top_k]