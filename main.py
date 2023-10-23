"""
Command-Line Interface (CLI) for Resume / Job Description Matcher.
"""

import argparse
import sys
import os
import glob
import subprocess

from resume_matcher.engine import ResumeMatcher, BatchMatcher
from resume_matcher.reporting import JSONReporter, HTMLReporter


def run_single_match(args, matcher: ResumeMatcher):
    """Run evaluation for a single resume against a job description."""
    if not os.path.exists(args.resume):
        print(f"Error: Resume file not found: {args.resume}")
        sys.exit(1)
    if not os.path.exists(args.jd):
        print(f"Error: Job description file not found: {args.jd}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("🚀 Evaluating Candidate Fit...")
    print(f"  Resume: {args.resume}")
    print(f"  Job Description: {args.jd}")
    print("=" * 70)

    results = matcher.match(
        resume_input=args.resume,
        jd_input=args.jd,
        resume_filename=os.path.basename(args.resume),
        jd_filename=os.path.basename(args.jd),
    )

    fit = results["overall_fit"]
    sub = fit["sub_scores"]
    skills = results["skill_analysis"]

    # Terminal Output Dashboard
    print(f"\n🎯 Overall Fit: {fit['overall_percentage']}% [{fit['fit_grade']}]")
    print("-" * 70)
    print(f"  🧠 Semantic Alignment: {sub['semantic']['percentage']}%")
    print(f"  🛠️ Hard Skills Coverage: {sub['skills']['percentage']}%")
    print(f"  🔤 TF-IDF Keyword Match: {sub['tfidf']['percentage']}%")

    print("\n✅ Matched Technical Skills:")
    if skills["matched_skills"]:
        print("   " + ", ".join(skills["matched_skills"]))
    else:
        print("   (None)")

    print("\n⚠️ Missing Required Skills:")
    if skills["missing_skills"]:
        print("   " + ", ".join(skills["missing_skills"]))
    else:
        print("   (None)")

    print("\n💡 Key Recommendations:")
    for rec in skills["recommendations"][:3]:
        print(f"   • {rec}")

    # Export outputs if requested
    if args.export_json:
        json_content = JSONReporter.generate(results)
        with open(args.export_json, "w", encoding="utf-8") as f:
            f.write(json_content)
        print(f"\n📥 Exported JSON report to: {args.export_json}")

    if args.export_html:
        html_content = HTMLReporter.generate(results)
        with open(args.export_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"📄 Exported HTML report to: {args.export_html}")

    print("=" * 70 + "\n")


def run_batch_match(args, matcher: ResumeMatcher):
    """Run batch candidate triage against a job description."""
    if not os.path.exists(args.jd):
        print(f"Error: Job description file not found: {args.jd}")
        sys.exit(1)

    # Collect resume paths from directory or glob pattern
    if os.path.isdir(args.batch_resumes):
        resume_files = []
        for ext in ("*.txt", "*.pdf", "*.docx", "*.md"):
            resume_files.extend(glob.glob(os.path.join(args.batch_resumes, ext)))
    else:
        resume_files = glob.glob(args.batch_resumes)

    if not resume_files:
        print(f"Error: No resume documents found in '{args.batch_resumes}'")
        sys.exit(1)

    print("\n" + "=" * 75)
    print(f"👥 Running Batch Triage on {len(resume_files)} Candidates")
    print(f"  Target Role: {args.jd}")
    print("=" * 75)

    batch_matcher = BatchMatcher(matcher)
    filenames = [os.path.basename(f) for f in resume_files]

    leaderboard = batch_matcher.rank_candidates(
        resumes=resume_files,
        filenames=filenames,
        jd_input=args.jd,
        jd_filename=os.path.basename(args.jd),
    )

    # Display Leaderboard
    print(f"{'Rank':<6} {'Candidate File':<32} {'Fit %':<10} {'Tier':<14} {'Skills Match'}")
    print("-" * 75)
    for c in leaderboard:
        matched_sample = ", ".join(c["matched_skills"][:3]) or "None"
        print(f"#{c['rank']:<5} {c['candidate']:<32} {c['overall_percentage']:<10.1f} {c['fit_grade']:<14} {matched_sample}")
    print("=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Resume / Job Description Fit Matcher (Python + Streamlit + TF-IDF + Embeddings)",
    )
    parser.add_argument("--resume", type=str, help="Path to a candidate resume (.pdf, .docx, .txt)")
    parser.add_argument("--jd", type=str, help="Path to the target job description (.txt, .docx, .pdf)")
    parser.add_argument("--batch-resumes", type=str, help="Directory containing multiple resumes for batch triage")
    parser.add_argument("--export-json", type=str, help="Export result as a JSON file")
    parser.add_argument("--export-html", type=str, help="Export result as a standalone HTML file")
    parser.add_argument("--gui", action="store_true", help="Launch the interactive Streamlit web application")

    args = parser.parse_args()

    if args.gui:
        print("🌐 Launching Streamlit Web App...")
        subprocess.run(["streamlit", "run", "app.py"])
        return

    if args.batch_resumes and args.jd:
        matcher = ResumeMatcher()
        run_batch_match(args, matcher)
    elif args.resume and args.jd:
        matcher = ResumeMatcher()
        run_single_match(args, matcher)
    else:
        # If no arguments provided, default to starting Streamlit
        print("No match arguments specified. Launching Streamlit web interface by default...")
        subprocess.run(["streamlit", "run", "app.py"])


if __name__ == "__main__":
    main()