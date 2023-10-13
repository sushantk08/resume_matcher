"""
Dashboard view implementations for Streamlit.
"""

import streamlit as st
from resume_matcher.ui.components import render_document_input
from resume_matcher.engine import ResumeMatcher


def render_single_match_view(matcher: ResumeMatcher, config: dict):
    """Render the primary single resume vs job description matching workflow."""
    col1, col2 = st.columns(2)

    with col1:
        resume_input, resume_name = render_document_input(
            title="Candidate Resume",
            key_prefix="resume",
        )

    with col2:
        jd_input, jd_name = render_document_input(
            title="Job Description",
            key_prefix="jd",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze Candidate Fit", type="primary", use_container_width=True)

    if analyze_btn:
        if not resume_input:
            st.error("Please upload or paste a Candidate Resume.")
            return
        if not jd_input:
            st.error("Please upload or paste a Job Description.")
            return

        with st.spinner("Analyzing fit across TF-IDF, embeddings, and skill taxonomy..."):
            results = matcher.match(
                resume_input=resume_input,
                jd_input=jd_input,
                resume_filename=resume_name,
                jd_filename=jd_name,
                weights=config["weights"],
            )
            # Store in session state for tab rendering
            st.session_state["match_results"] = results
            st.session_state["has_analyzed"] = True