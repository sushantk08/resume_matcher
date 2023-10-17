"""
Dashboard view implementations for Streamlit.
"""

import streamlit as st
from resume_matcher.ui.components import (
    render_document_input,
    render_overall_score_card,
    render_skill_badges,
    render_keyword_table,
    render_tailoring_tab,
)


@st.cache_resource(show_spinner=False)
def get_cached_matcher():
    """Load and cache the NLP models only once."""
    from resume_matcher.engine import ResumeMatcher
    return ResumeMatcher()


def render_single_match_view(config: dict):
    """Render the primary single resume vs job description matching workflow."""
    col1, col2 = st.columns(2)

    sample_resume = (
        "Senior Backend Engineer with 5 years experience in Python, FastAPI, and PostgreSQL.\n"
        "Expertise in Docker containerization, AWS cloud deployments, and automated CI/CD pipelines.\n"
        "Proficient in Microservices architecture, REST APIs, and Linux server management."
    )

    sample_jd = (
        "Seeking a Senior Python Developer with deep experience in FastAPI and PostgreSQL.\n"
        "Requirements:\n"
        "- Strong proficiency in Python and Docker.\n"
        "- Experience deploying to AWS using Kubernetes and CI/CD.\n"
        "- Familiarity with Redis and Kafka is a plus."
    )

    with col1:
        resume_input, resume_name = render_document_input(
            title="Candidate Resume",
            key_prefix="resume",
            sample_text=sample_resume,
        )

    with col2:
        jd_input, jd_name = render_document_input(
            title="Job Description",
            key_prefix="jd",
            sample_text=sample_jd,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze Candidate Fit", type="primary", use_container_width=True)

    if analyze_btn:
        if not resume_input:
            st.error("Please provide a Candidate Resume.")
            return
        if not jd_input:
            st.error("Please provide a Job Description.")
            return

        with st.spinner("⚡ Analyzing candidate fit across models..."):
            matcher = get_cached_matcher()
            results = matcher.match(
                resume_input=resume_input,
                jd_input=jd_input,
                resume_filename=resume_name,
                jd_filename=jd_name,
                weights=config["weights"],
            )
            st.session_state["match_results"] = results
            st.session_state["has_analyzed"] = True
            st.session_state["last_resume_input"] = resume_input
            st.session_state["last_jd_input"] = jd_input

    # Render Results Dashboard
    if st.session_state.get("has_analyzed", False) and "match_results" in st.session_state:
        results = st.session_state["match_results"]
        matcher = get_cached_matcher()

        st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)
        st.subheader("📊 Match Evaluation Dashboard")

        # 1. Top Score Card
        render_overall_score_card(results["overall_fit"])

        # 2. Detailed Breakdown Tabs
        tab_skills, tab_keywords, tab_sentences, tab_tailor = st.tabs([
            "🛠️ Skill Analysis & Gaps",
            "🔤 Keyword Attribution",
            "🎯 Sentence Alignment",
            "💡 Tailoring Advice & Sandbox",
        ])

        with tab_skills:
            skill_res = results["skill_analysis"]
            col_match, col_miss = st.columns(2)

            with col_match:
                st.markdown(f"#### ✅ Matched Skills ({len(skill_res['matched_skills'])})")
                render_skill_badges(skill_res["matched_skills"], badge_type="matched")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"#### ➕ Candidate Extra Skills ({len(skill_res['additional_skills'])})")
                render_skill_badges(skill_res["additional_skills"], badge_type="additional")

            with col_miss:
                st.markdown(f"#### ⚠️ Missing Required Skills ({len(skill_res['missing_skills'])})")
                render_skill_badges(skill_res["missing_skills"], badge_type="missing")

        with tab_keywords:
            st.markdown("#### Key Shared Terms Driving TF-IDF Similarity")
            st.caption("Words and phrases appearing in both documents with the highest statistical relevance.")
            render_keyword_table(results["lexical_analysis"]["top_keywords"])

        with tab_sentences:
            st.markdown("#### Sentence-Level Semantic Alignment")
            st.caption("How specific bullet points in the resume address core JD requirements.")
            alignments = results["semantic_analysis"]["top_alignments"]

            for idx, item in enumerate(alignments, 1):
                with st.expander(f"Alignment #{idx}: {item['alignment_score'] * 100:.1f}% Similarity", expanded=(idx == 1)):
                    st.markdown(f"**Job Requirement:**\n> {item['jd_requirement']}")
                    st.markdown(f"**Matched Resume Experience:**\n* {item['matched_resume_experience']}")

        with tab_tailor:
            # Resolve current text for the sandbox
            current_resume = st.session_state.get("last_resume_input", "")
            if not isinstance(current_resume, str):
                current_resume = matcher._resolve_text(current_resume, "resume.txt")

            current_jd = st.session_state.get("last_jd_input", "")
            if not isinstance(current_jd, str):
                current_jd = matcher._resolve_text(current_jd, "jd.txt")

            render_tailoring_tab(
                results=results,
                matcher=matcher,
                config=config,
                current_resume_text=current_resume,
                jd_text=current_jd,
            )