"""
Main Streamlit Application Entry Point.
"""

import streamlit as st
from resume_matcher.ui import (
    render_sidebar_controls,
    render_single_match_view,
    render_batch_match_view,
)

# Streamlit Page Config
st.set_page_config(
    page_title="Resume & JD Fit Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #64748B; margin-bottom: 1.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 6px; padding: 8px 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">📄 Resume & Job Description Matcher</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Evaluate applicant-to-job fit using TF-IDF lexical overlap, sentence-transformers semantic embeddings, and technical skill taxonomy extraction.</div>',
    unsafe_allow_html=True,
)

# Sidebar Configuration
sidebar_config = render_sidebar_controls()

# Main Navigation Tabs
tab1, tab2 = st.tabs(["🎯 Single Candidate Match", "👥 Batch Candidate Triage"])

with tab1:
    render_single_match_view(sidebar_config)

with tab2:
    render_batch_match_view(sidebar_config)