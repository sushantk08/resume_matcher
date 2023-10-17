"""
Reusable UI widgets and configuration components for Streamlit.
"""

from typing import Tuple, Dict, Any, Union, List
import streamlit as st
import pandas as pd
import io


def render_sidebar_controls() -> Dict[str, Any]:
    """Render the sidebar with scoring weight sliders and analysis settings."""
    with st.sidebar:
        st.header("⚙️ Scoring Weights")
        st.caption("Adjust model contributions to the final fit score.")

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
    """Render a tabbed document input allowing either file upload or text pasting."""
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


def render_overall_score_card(score_data: Dict[str, Any]):
    """Render the top-level fit score banner and metric cards."""
    pct = score_data["overall_percentage"]
    grade = score_data["fit_grade"]
    color = score_data["grade_color"]

    color_map = {
        "green": "#10B981",
        "blue": "#3B82F6",
        "orange": "#F59E0B",
        "red": "#EF4444",
    }
    hex_color = color_map.get(color, "#3B82F6")

    # Top Banner
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 2px solid {hex_color}; border-radius: 12px; padding: 20px 24px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #1E293B;">Overall Match Fit</h3>
                    <p style="margin: 4px 0 0 0; color: #64748B;">Multi-factor composite score across semantic, lexical, and skill models</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 2.4rem; font-weight: 800; color: {hex_color};">{pct}%</span>
                    <br>
                    <span style="background-color: {hex_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">{grade}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sub-scores columns
    sub = score_data["sub_scores"]
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            label="🧠 Semantic Alignment",
            value=f"{sub['semantic']['percentage']}%",
            help="Concept and experience alignment computed by sentence-transformers.",
        )
        st.progress(sub["semantic"]["score"])

    with c2:
        st.metric(
            label="🛠️ Hard Skills Match",
            value=f"{sub['skills']['percentage']}%",
            help="Percentage of required technical skills present in the resume.",
        )
        st.progress(sub["skills"]["score"])

    with c3:
        st.metric(
            label="🔤 TF-IDF Keyword Overlap",
            value=f"{sub['tfidf']['percentage']}%",
            help="Statistical lexical and phrase similarity computed by scikit-learn.",
        )
        st.progress(sub["tfidf"]["score"])


def render_skill_badges(skills: List[str], badge_type: str = "matched"):
    """Render a collection of colorful skill tags."""
    if not skills:
        st.write("*(None)*")
        return

    styles = {
        "matched": "background-color: #DEF7EC; color: #03543F; border: 1px solid #BCF0DA;",
        "missing": "background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #FBD5D5;",
        "additional": "background-color: #EDF2F7; color: #2D3748; border: 1px solid #E2E8F0;",
    }
    style = styles.get(badge_type, styles["matched"])

    html_badges = "".join(
        f'<span style="{style} display: inline-block; padding: 4px 10px; margin: 3px 4px 3px 0; border-radius: 6px; font-weight: 500; font-size: 0.85rem;">{s}</span>'
        for s in skills
    )
    st.markdown(html_badges, unsafe_allow_html=True)


def render_keyword_table(top_keywords: List[Dict[str, Any]]):
    """Render the top contributing TF-IDF keywords in a formatted dataframe."""
    if not top_keywords:
        st.info("No shared technical keywords detected between documents.")
        return

    df = pd.DataFrame(top_keywords)
    df = df.rename(
        columns={
            "term": "Matched Term / Phrase",
            "contribution": "Score Weight",
            "resume_weight": "Resume Density",
            "jd_weight": "JD Importance",
        }
    )
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

def render_tailoring_tab(results: Dict[str, Any], matcher, config: dict, current_resume_text: str, jd_text: str):
    """Render the actionable resume tailoring advice and interactive live re-scorer."""
    skill_analysis = results["skill_analysis"]
    overall_fit = results["overall_fit"]
    recs = skill_analysis["recommendations"]

    st.markdown("#### 💡 Actionable ATS & Tailoring Guidance")
    st.caption("Strategic changes to align your resume with this position's key requirements.")

    # 1. ATS Compliance Checklist Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        cov_pct = skill_analysis["skill_coverage_percentage"]
        if cov_pct >= 70:
            st.success(f"✅ **Skills Coverage**: {cov_pct}% (Good)")
        else:
            st.warning(f"⚠️ **Skills Coverage**: {cov_pct}% (Needs Work)")

    with c2:
        sem_pct = overall_fit["sub_scores"]["semantic"]["percentage"]
        if sem_pct >= 65:
            st.success(f"✅ **Role Alignment**: {sem_pct}% (Strong)")
        else:
            st.warning(f"⚠️ **Role Alignment**: {sem_pct}% (Moderate)")

    with c3:
        missing_count = len(skill_analysis["missing_skills"])
        if missing_count <= 2:
            st.success(f"✅ **Gaps**: Only {missing_count} missing")
        else:
            st.info(f"ℹ️ **Gaps**: {missing_count} keywords to address")

    # 2. Key Tailoring Bullet Points
    st.markdown("##### 📌 High-Impact Recommendations:")
    for rec in recs:
        st.markdown(f"- {rec}")

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    # 3. Interactive In-Browser Live Re-Scorer
    st.markdown("##### ✍️ Live Resume Tailoring Sandbox")
    st.caption(
        "Try integrating some of the missing skills into the text below and click 'Re-evaluate' to see your new fit score instantly."
    )

    edited_resume = st.text_area(
        "Edit your resume in-place:",
        value=current_resume_text,
        height=220,
        key="sandbox_resume_editor",
    )

    if st.button("🔄 Re-evaluate Fit with Edits", type="secondary"):
        with st.spinner("Re-calculating match score with your updates..."):
            new_results = matcher.match(
                resume_input=edited_resume,
                jd_input=jd_text,
                weights=config["weights"],
            )
            st.session_state["match_results"] = new_results
            st.rerun()