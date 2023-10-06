"""
NLP pipeline using spaCy for linguistic analysis, entity extraction, and tokenization.
"""

from typing import List, Set, Dict, Any
import spacy
from spacy.tokens import Doc
from resume_matcher.preprocessing.cleaner import TextCleaner
from resume_matcher.preprocessing.stopwords import get_stopwords


class NLPPipeline:
    """Wrapper around spaCy for resume and job description linguistic processing."""

    _nlp = None

    @classmethod
    def get_nlp(cls):
        """Lazy load the spaCy model to optimize startup time."""
        if cls._nlp is None:
            try:
                cls._nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Fallback if model not found
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
                cls._nlp = spacy.load("en_core_web_sm")
        return cls._nlp

    @classmethod
    def process_text(cls, text: str) -> Doc:
        """Process raw text through spaCy pipeline."""
        cleaned = TextCleaner.clean(text)
        nlp = cls.get_nlp()
        return nlp(cleaned)

    @classmethod
    def extract_tokens(
        cls,
        text: str,
        remove_stopwords: bool = True,
        lemmatize: bool = True,
        min_length: int = 2,
    ) -> List[str]:
        """
        Extract normalized tokens (lemmatized and filtered).

        Args:
            text: Input document string.
            remove_stopwords: Whether to remove standard and domain stopwords.
            lemmatize: Whether to lemmatize tokens.
            min_length: Minimum token length.

        Returns:
            List of processed token strings.
        """
        doc = cls.process_text(text)
        stopwords = get_stopwords(include_domain=True) if remove_stopwords else set()
        
        tokens = []
        for token in doc:
            if token.is_punct or token.is_space or token.like_num:
                continue

            raw_tok = token.text.strip().lower()
            lemma_tok = token.lemma_.strip().lower() if lemmatize else raw_tok

            target_tok = lemma_tok if lemma_tok != "-pron-" else raw_tok

            if len(target_tok) < min_length:
                continue

            if remove_stopwords and (target_tok in stopwords or raw_tok in stopwords):
                continue

            tokens.append(target_tok)

        return tokens

    @classmethod
    def extract_noun_chunks(cls, text: str) -> List[str]:
        """Extract multi-word key phrases and noun chunks using spaCy."""
        doc = cls.process_text(text)
        chunks = []
        stopwords = get_stopwords(include_domain=True)

        for chunk in doc.noun_chunks:
            cleaned_chunk = chunk.text.strip().lower()
            # Remove leading articles and stopwords
            words = cleaned_chunk.split()
            filtered_words = [w for w in words if w not in stopwords and len(w) > 1]
            if filtered_words:
                chunks.append(" ".join(filtered_words))

        return list(dict.fromkeys(chunks))  # Deduplicate while preserving order

    @classmethod
    def extract_named_entities(cls, text: str) -> Dict[str, List[str]]:
        """Extract named entities (Organizations, Technologies, Degrees)."""
        doc = cls.process_text(text)
        entities: Dict[str, List[str]] = {}
        for ent in doc.ents:
            label = ent.label_
            if label not in entities:
                entities[label] = []
            if ent.text.strip() not in entities[label]:
                entities[label].append(ent.text.strip())
        return entities