from setuptools import setup, find_packages

setup(
    name="resume_matcher",
    version="0.1.0",
    description="Resume and Job Description Fit Matcher with Streamlit GUI",
    author="Developer",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.20.0",
        "pypdf>=3.0.0",
        "python-docx>=0.8.11",
        "pandas>=1.5.0",
    ],
    entry_points={
        "console_scripts": [
            "resume-matcher=resume_matcher.cli:main",
        ],
    },
)