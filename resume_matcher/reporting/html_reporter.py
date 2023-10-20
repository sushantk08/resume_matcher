"""
Standalone HTML visual report generator.
"""

from typing import Dict, Any
from datetime import datetime


class HTMLReporter:
    """Generates self-contained, printable HTML fit reports."""

    @classmethod
    def generate(cls, results: Dict[str, Any]) -> str:
        """Generate a complete, single-file HTML document."""
        overall = results["overall_fit"]
        sub = overall["sub_scores"]
        skills = results["skill_analysis"]
        keywords = results["lexical_analysis"]["top_keywords"]
        alignments = results["semantic_analysis"]["top_alignments"]
        meta = results.get("metadata", {})

        color_map = {
            "green": "#10B981",
            "blue": "#3B82F6",
            "orange": "#F59E0B",
            "red": "#EF4444",
        }
        accent = color_map.get(overall.get("grade_color", "blue"), "#3B82F6")

        # HTML Badges
        matched_badges = "".join(
            f'<span class="badge badge-match">{s}</span>' for s in skills["matched_skills"]
        ) or "<em>None</em>"

        missing_badges = "".join(
            f'<span class="badge badge-miss">{s}</span>' for s in skills["missing_skills"]
        ) or "<em>None</em>"

        # Table rows for keywords
        kw_rows = "".join(
            f"<tr><td><b>{k['term']}</b></td><td>{k['contribution']}</td><td>{k['resume_weight']}</td><td>{k['jd_weight']}</td></tr>"
            for k in keywords[:10]
        ) or "<tr><td colspan='4'>No shared keywords detected.</td></tr>"

        # Recommendations list
        recs_list = "".join(
            f"<li>{r}</li>" for r in skills["recommendations"]
        )

        # Sentence alignments list
        align_html = "".join(
            f"""
            <div class="card" style="margin-bottom: 12px;">
                <div style="font-weight: 600; color: #1E293B;">Target Requirement:</div>
                <div style="color: #475569; margin: 4px 0 8px 0; font-style: italic;">&ldquo;{a['jd_requirement']}&rdquo;</div>
                <div style="font-weight: 600; color: #059669;">Matched Resume Evidence ({a['alignment_score']*100:.1f}% Match):</div>
                <div style="color: #1F2937; margin-top: 4px;">&bull; {a['matched_resume_experience']}</div>
            </div>
            """
            for a in alignments[:4]
        )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Candidate Evaluation Report - {overall['overall_percentage']}% Fit</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #F8FAFC; color: #1E293B; margin: 0; padding: 32px 16px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 36px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px; }}
        .badge {{ display: inline-block; padding: 4px 10px; margin: 3px 4px 3px 0; border-radius: 6px; font-weight: 500; font-size: 0.85rem; }}
        .badge-match {{ background-color: #DEF7EC; color: #03543F; border: 1px solid #BCF0DA; }}
        .badge-miss {{ background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #FBD5D5; }}
        .score-box {{ text-align: right; }}
        .score-val {{ font-size: 2.8rem; font-weight: 800; color: {accent}; line-height: 1; }}
        .score-tier {{ background-color: {accent}; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px; }}
        .metric-card {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; text-align: center; }}
        .metric-val {{ font-size: 1.6rem; font-weight: 700; color: #1E293B; }}
        .metric-lbl {{ font-size: 0.85rem; color: #64748B; margin-top: 4px; }}
        .card {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 0.9rem; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #E2E8F0; }}
        th {{ background-color: #F1F5F9; color: #475569; font-weight: 600; }}
        h2 {{ font-size: 1.3rem; color: #0F172A; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-top: 28px; }}
        ul {{ padding-left: 20px; color: #334155; }}
        li {{ margin-bottom: 6px; }}
        .footer {{ text-align: center; margin-top: 36px; font-size: 0.8rem; color: #94A3B8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 style="margin: 0; font-size: 1.8rem; color: #0F172A;">Candidate Fit Evaluation Report</h1>
                <p style="margin: 4px 0 0 0; color: #64748B;">Generated on {timestamp}</p>
                <p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #94A3B8;">Resume: {meta.get('resume_filename', 'resume.txt')} | Target: {meta.get('jd_filename', 'job_description.txt')}</p>
            </div>
            <div class="score-box">
                <div class="score-val">{overall['overall_percentage']}%</div>
                <span class="score-tier">{overall['fit_grade']}</span>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-val">{sub['semantic']['percentage']}%</div>
                <div class="metric-lbl">🧠 Semantic Alignment</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{sub['skills']['percentage']}%</div>
                <div class="metric-lbl">🛠️ Hard Skills Coverage</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{sub['tfidf']['percentage']}%</div>
                <div class="metric-lbl">🔤 TF-IDF Keyword Match</div>
            </div>
        </div>

        <h2>🛠️ Technical Skills Comparison</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="card">
                <h3 style="margin-top: 0; color: #059669; font-size: 1rem;">✅ Matched Skills ({len(skills['matched_skills'])})</h3>
                {matched_badges}
            </div>
            <div class="card">
                <h3 style="margin-top: 0; color: #DC2626; font-size: 1rem;">⚠️ Missing Skills ({len(skills['missing_skills'])})</h3>
                {missing_badges}
            </div>
        </div>

        <h2>💡 Resume Tailoring Recommendations</h2>
        <div class="card">
            <ul>{recs_list}</ul>
        </div>

        <h2>🎯 Core Requirements Alignment</h2>
        {align_html}

        <h2>🔤 Top Contributing Technical Keywords</h2>
        <table>
            <thead>
                <tr>
                    <th>Matched Keyword / Phrase</th>
                    <th>Weight Contribution</th>
                    <th>Resume Density</th>
                    <th>JD Importance</th>
                </tr>
            </thead>
            <tbody>
                {kw_rows}
            </tbody>
        </table>

        <div class="footer">
            Resume Matcher Engine &bull; Pure Python &bull; Streamlit GUI
        </div>
    </div>
</body>
</html>
"""
        return html