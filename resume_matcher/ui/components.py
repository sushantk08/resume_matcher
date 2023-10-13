"""
Reusable UI widgets and configuration components for Streamlit.
"""

from typing import Tuple, Dict, Any, Union
import streamlit as st
import io


def render_sidebar_controls() -> Dict[str, Any]:
    """Render the sidebar with scoring weight sliders and analysis settings."""
    with st.sidebar:
        st.header("⚙️ Scoring Weights")
        st.caption("Adjust how much each model contributes to the final fit score.")

        semantic_w = st.slider(
            "Semantic Embeddings (Context)",
            min_value=0.10,
            max_value=0.60,
            value=0.35,
            step=0.05,
            help="Weight given to sentence-transformers conceptual understanding.",
        )
        skills_w = st.slider(
            "Hard Skills Match (Taxonomy)",
            min_value=0.10,
            max_value=0.60,
            value=0.35,
            step=0.05,
            help="Weight given to direct technical skills coverage.",
        )
        tfidf_w = st.slider(
            "TF-IDF Lexical (Keywords)",
            min_value=0.10,
            max_value=0.60,
            value=0.30,
            step=0.05,
            help="Weight given to exact keyword and n-gram overlap.",
        )

        st.divider()
        st.header("🔍 Model Settings")
        top_alignments = st.slider("Top Aligned Sentences", 3, 10, 5)

        return {
            "weights": {
                "semantic": semantic_w,
                "skills": skills_w,
                "tfidf": tfidf_w,
            },
            "top_alignments": top_alignments,
        }


def render_document_input(
    title: str,
    key_prefix: str,
    sample_text: str = "",
) -> Tuple[Union[str, bytes, io.BytesIO], str]:
    """
    Render a tabbed document input allowing either file upload or text pasting.

    Returns:
        Tuple of (content, filename)
    """
    st.subheader(title)
    tab_upload, tab_paste = st.tabs(["📁 Upload Document", "✍️ Paste Text"])

    with tab_upload:
        uploaded_file = st.file_uploader(
            f"Upload {title} (.pdf, .docx, .txt)",
            type=["pdf", "docx", "txt", "md"],
            key=f"{key_prefix}_file",
        )
        if uploaded_file is not None:
            return uploaded_file, uploaded_file.name

    with tab_paste:
        pasted_text = st.text_area(
            f"Or paste raw {title} content here:",
            value=sample_text,
            height=260,
            key=f"{key_prefix}_text",
        )
        if pasted_text.strip():
            return pasted_text, f"{key_prefix}.txt"

    return "", ""