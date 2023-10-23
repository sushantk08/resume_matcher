# 📄 Resume / Job Description Matcher

An end-to-end **resume-to-job matching and fit scoring engine** with an interactive **Streamlit web application** and command-line interface. The project combines lexical matching, semantic similarity, technical skill extraction, ATS-style keyword analysis, and candidate ranking to help evaluate how well a resume matches a job description.

---

## 🌟 Overview

The **Resume / Job Description Matcher** analyzes a candidate's resume against a job description and produces an overall fit assessment.

Instead of relying on simple keyword matching alone, the project combines multiple techniques:

- **Lexical Overlap** using TF-IDF with sublinear term-frequency scaling and N-grams.
- **Semantic Understanding** using `sentence-transformers` and dense neural embeddings.
- **Technical Competency Analysis** using spaCy `PhraseMatcher` and a curated technical skills taxonomy.
- **ATS Guidance** through missing keyword detection and resume-tailoring recommendations.
- **Candidate Ranking** for batch evaluation of multiple resumes against a single job description.
- **Interactive Reports** through Streamlit and exported HTML/JSON results.

The goal is to provide a practical, explainable approach to resume screening rather than depending on a single similarity score.

---

## 🎯 Project Objectives

The application is designed to answer questions such as:

- How closely does a resume match a specific job description?
- Which required technical skills are already present?
- Which important keywords are missing?
- How semantically similar is the candidate's experience to the job requirements?
- Which candidate is the strongest match when multiple resumes are available?
- What areas of the resume could be improved for better ATS alignment?

---

## 🚀 Key Features

### 🔤 1. Lexical Matching

The project uses **TF-IDF** from `scikit-learn` to measure important terms shared between the resume and job description.

It uses:

- TF-IDF vectorization.
- Sublinear TF scaling.
- Word N-grams.
- Cosine similarity.

This helps identify direct terminology overlap between candidate and employer text.

---

### 🧠 2. Semantic Similarity

Keyword overlap alone can miss relationships between differently worded sentences. To address this, the application uses **Sentence Transformers**.

The default model is:

```text
all-MiniLM-L6-v2
```

Resume and job-description text are transformed into dense vector embeddings and compared using semantic similarity.

For example, a resume mentioning:

```text
Built scalable REST services using Python.
```

can still be considered relevant to a job description mentioning:

```text
Develop backend APIs and scalable web services with Python.
```

This provides a stronger measure of contextual similarity than exact keyword matching alone.

---

### 🛠️ 3. Technical Skill Extraction

The project uses **spaCy PhraseMatcher** together with a curated technical skill taxonomy to identify technology-related competencies.

Examples include:

- Python
- Java
- FastAPI
- Flask
- Django
- SQL
- PostgreSQL
- MongoDB
- Docker
- AWS
- Git
- React
- Pandas
- NumPy
- Machine Learning

The extracted skills are compared between the resume and job description to identify matches and gaps.

---

### 📊 4. Composite Fit Scoring

The application combines multiple signals instead of relying on one metric.

A conceptual scoring pipeline is:

```text
Resume + Job Description
            │
            ├── TF-IDF / N-gram Similarity
            │
            ├── Semantic Embedding Similarity
            │
            ├── Technical Skill Matching
            │
            └── Keyword Gap Analysis
                     │
                     ▼
              Combined Fit Score
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Match Analysis        ATS Guidance
```

The final result provides a more informative view of candidate fit than raw keyword overlap.

---

### 🔎 5. Missing Keyword Detection

The system identifies important terms found in the job description but not detected in the resume.

This can highlight potential gaps such as:

```text
Missing Skills:
- FastAPI
- Docker
- AWS
- PostgreSQL
```

This information can be used to improve resume alignment before applying for a role.

---

### ✍️ 6. Resume Tailoring Sandbox

The interactive application provides an in-browser workspace for reviewing and tailoring resume content.

This allows users to:

- Review the match result.
- Identify missing keywords.
- Edit resume content.
- Improve technical terminology.
- Re-check the match after making changes.

---

### 📈 7. Batch Candidate Ranking

Multiple resumes can be evaluated against a single job description.

The batch workflow can:

1. Load resumes from a directory.
2. Extract relevant information.
3. Calculate fit scores.
4. Compare technical skills.
5. Rank candidates.
6. Support quick candidate triage.

Example:

```text
Candidate A    91.4%
Candidate B    84.7%
Candidate C    78.2%
Candidate D    69.5%
```

This makes the project useful not only for individual resume analysis but also for basic candidate screening workflows.

---

### 🖥️ 8. Streamlit Web Interface

A browser-based interface is provided through Streamlit.

The interface allows users to interact with the matching engine without needing to work entirely from the command line.

Typical workflow:

```text
Upload / Select Resume
          ↓
Provide Job Description
          ↓
Run Matching Engine
          ↓
View Overall Fit
          ↓
Review Skill Matches
          ↓
Review Missing Keywords
          ↓
Tailor Resume
          ↓
Run Match Again
```

---

### 📄 9. Exportable Reports

Single candidate evaluations can be exported into multiple formats.

Supported outputs include:

- HTML reports for human-readable review.
- JSON reports for structured downstream processing.

Example:

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt \
  --export-html report.html \
  --export-json report.json
```

---

## 🛠️ Tech Stack

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Language** | Python | Core application logic |
| **Web UI** | Streamlit | Interactive browser interface |
| **Text Processing** | scikit-learn | TF-IDF and lexical similarity |
| **Semantic NLP** | sentence-transformers | Dense embeddings and semantic similarity |
| **NLP** | spaCy | Phrase matching and technical skill extraction |
| **Similarity** | Cosine Similarity | Comparing text and embeddings |
| **Data Processing** | Python standard library / project utilities | Text loading and processing |
| **Reporting** | HTML, JSON | Result export |
| **Testing** | Python test runner / project test suite | Automated validation |

---

## 🧱 Matching Pipeline

The application follows a multi-stage matching process.

```text
                ┌──────────────────────┐
                │ Resume + Job Posting │
                └──────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Text Cleanup   TF-IDF/N-grams   Embeddings
             │             │             │
             │             ▼             ▼
             │       Lexical Score   Semantic Score
             │             │             │
             └──────┬──────┴──────┬──────┘
                    ▼             ▼
              Skill Extraction   Keyword Analysis
                    │             │
                    └──────┬──────┘
                           ▼
                    Composite Result
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Fit Score     Skill Gaps    ATS Guidance
```

---

## 📂 Example Project Structure

```text
resume-job-matcher/
│
├── main.py                         # CLI entry point
├── app.py                          # Streamlit web application
├── run_tests.py                    # Automated test runner
├── requirements.txt                # Python dependencies
├── README.md
│
├── examples/
│   ├── resumes/
│   │   ├── senior_backend_python.txt
│   │   ├── data_engineer.txt
│   │   └── software_engineer.txt
│   │
│   └── job_descriptions/
│       ├── senior_python_backend_jd.txt
│       └── data_engineer_jd.txt
│
├── ...                             # Matching engine and NLP modules
└── ...                             # Tests and supporting utilities
```

> The exact repository structure may contain additional modules used by the matching engine, scoring logic, UI, and tests.

---

## 🚀 Quickstart

### 1. Prerequisites

Make sure Python 3.10+ is installed.

Check your Python version:

```bash
python --version
```

It is recommended to create and use a virtual environment for the project.

---

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The first execution may also download the required NLP/embedding model depending on the project's implementation.

---

## 🖥️ Launch the Web Interface

Start the Streamlit application using:

```bash
python main.py --gui
```

Or directly through Streamlit:

```bash
streamlit run app.py
```

After startup, Streamlit will provide a local browser URL where the application can be opened.

---

## 💻 Command-Line Usage

### Single Resume Match

Evaluate one resume against one job description:

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt
```

---

### Single Match with HTML and JSON Reports

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt \
  --export-html report.html \
  --export-json report.json
```

This generates:

```text
report.html
report.json
```

---

### Batch Candidate Ranking

Evaluate several resumes against the same job description:

```bash
python main.py \
  --batch-resumes examples/resumes/ \
  --jd examples/job_descriptions/senior_python_backend_jd.txt
```

The engine processes the resumes in the supplied directory and ranks candidates according to the project's matching logic.

---

## 🧪 Running Automated Tests

Run the project's test suite with:

```bash
python run_tests.py
```

A successful test run should validate the core matching functionality and supporting application behavior implemented in the repository.

---

## 🔬 Testing the CLI

### Test a Single Match

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt \
  --export-html report.html
```

### Test Batch Candidate Triage

```bash
python main.py \
  --batch-resumes examples/resumes/ \
  --jd examples/job_descriptions/senior_python_backend_jd.txt
```

---

## 📊 Example Output

A typical analysis can contain information such as:

```text
==================================================
Resume / Job Description Match Report
==================================================

Overall Fit Score: 86.7%

Lexical Similarity:   81.4%
Semantic Similarity:  89.2%
Technical Skill Fit:  88.5%

Matched Skills:
- Python
- FastAPI
- SQL
- Docker
- REST API

Missing / Weak Keywords:
- AWS
- Kubernetes

ATS Recommendations:
- Highlight cloud deployment experience.
- Add relevant AWS terminology where accurate.
- Strengthen backend scalability descriptions.
==================================================
```

> Output formatting and exact score names depend on the implementation used in the repository.

---

## 🧮 Matching Methodology

The system uses multiple perspectives to evaluate candidate fit.

### Lexical Similarity

TF-IDF represents terms based on their importance within the resume and job description. N-grams help preserve useful short phrases instead of evaluating every word completely independently.

### Semantic Similarity

Sentence Transformer embeddings capture contextual relationships between pieces of text. Cosine similarity can then be used to measure how close the resulting embeddings are.

### Skill Matching

A curated technical taxonomy and spaCy PhraseMatcher identify explicit technology and competency mentions.

### Keyword Gap Analysis

Job-description terms that are important but absent from the resume can be surfaced as potential gaps.

### Final Assessment

The individual signals are combined into the project's overall fit assessment. This approach reduces reliance on a single metric and creates a more actionable result.

---

## 🎯 ATS-Oriented Analysis

The application is designed to provide practical ATS-oriented guidance.

It can help identify:

- Missing technical terms.
- Missing tools and frameworks.
- Weak terminology overlap.
- Skills that appear in the job description but not in the resume.
- Areas where resume wording can be made more closely aligned with a target role.

The system is intended as a decision-support tool rather than a replacement for human recruitment judgment.

---

## 🧠 Why Use Multiple Matching Techniques?

A simple keyword matcher has limitations.

For example:

```text
Resume:
"Developed scalable backend services using Python."

Job Description:
"Build high-performance Python APIs for distributed systems."
```

The wording is different even though the concepts are strongly related.

A robust matcher can combine:

```text
Exact / Phrase Overlap
          +
Semantic Similarity
          +
Technical Skill Matching
          +
Keyword Gap Analysis
          ↓
More Informative Candidate Fit Assessment
```

This is one of the main technical goals of the project.

---

## 🔄 End-to-End Workflow

```text
1. Load Resume
       ↓
2. Load Job Description
       ↓
3. Normalize and preprocess text
       ↓
4. Calculate lexical similarity
       ↓
5. Generate semantic embeddings
       ↓
6. Calculate semantic similarity
       ↓
7. Extract technical skills
       ↓
8. Compare candidate and job skills
       ↓
9. Detect missing keywords
       ↓
10. Calculate overall fit
       ↓
11. Generate ATS guidance
       ↓
12. Display or export report
```

---

## 📦 Example Use Cases

### 👨‍💻 Job Seekers

A candidate can compare their resume against different job descriptions and identify skills or terminology that deserve attention.

### 👩‍💼 Recruiters

Recruiters can quickly compare multiple candidate resumes against a target role and prioritize profiles for manual review.

### 🎓 Students & Freshers

Students can use the project to understand how resumes can be matched against technical job descriptions and where their skill gaps may exist.

### 🧪 NLP Learning Project

The project provides a practical example of combining classical NLP techniques with modern embedding-based semantic search.

---

## 🧰 Technical Concepts Demonstrated

This project demonstrates practical knowledge of:

- Python application development.
- Natural Language Processing.
- TF-IDF vectorization.
- N-gram text features.
- Cosine similarity.
- Sentence embeddings.
- Transformer-based semantic similarity.
- spaCy NLP pipelines.
- PhraseMatcher.
- Information extraction.
- Technical skill taxonomies.
- Streamlit application development.
- CLI application design.
- Batch processing.
- Candidate ranking.
- JSON report generation.
- HTML report generation.
- Automated testing.

---

## ⚠️ Limitations

Resume matching is inherently difficult because job descriptions and resumes can use different terminology, contain incomplete information, or describe skills with different levels of detail.

Important limitations include:

- Similarity scores do not guarantee candidate suitability.
- A missing keyword does not necessarily mean a candidate lacks the skill.
- Semantic similarity can produce matches that require human verification.
- Results depend on the quality of the supplied resume and job description.
- ATS guidance should only recommend truthful resume improvements; candidates should not add skills they do not actually possess.

The application should therefore be treated as an **assistive matching and analysis tool**, not as an automated hiring decision maker.

---

## 📈 Possible Future Improvements

Potential future enhancements include:

- PDF and DOCX resume parsing.
- Multi-language resume matching.
- Skill synonym and abbreviation expansion.
- Experience-level detection.
- Education and certification matching.
- Job-title similarity scoring.
- Explainable score breakdowns.
- Improved ranking calibration using labeled datasets.
- Historical application tracking.
- Resume version management.
- Automated report dashboards.
- Database-backed candidate storage.
- REST API around the matching engine.
- Cloud deployment.
- CI/CD automation.

---

## 🔐 Responsible Usage

This project should be used to support human decision-making rather than make final employment decisions automatically.

For candidates, the tailoring functionality should be used to improve clarity and relevance **without misrepresenting qualifications or adding skills that the candidate does not have**.

For recruiters, automated scores should be treated as one signal among many and reviewed alongside experience, interviews, portfolio work, and other relevant evidence.

---

## 📄 License

Add the license used by your repository here.

For example:

```text
MIT License
```

---

## 👨‍💻 Project Summary

**Resume / Job Description Matcher** is a practical NLP-focused application that combines **TF-IDF lexical similarity, sentence-transformer semantic embeddings, spaCy-based technical skill extraction, ATS keyword analysis, and candidate ranking** into a single workflow.

It demonstrates how classical NLP techniques and modern embedding models can work together to solve a real-world problem: understanding how closely a candidate profile aligns with a job description and turning that analysis into actionable feedback.
