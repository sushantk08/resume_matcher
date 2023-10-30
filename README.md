# 📄 AI Resume & Job Description Matcher

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://resumematcher-bysushantkulkarni.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A beginner-friendly **Python and NLP project** that compares a resume with a job description and gives a match score.

The project uses **TF-IDF, sentence-transformers, spaCy, and Streamlit** to understand the text, compare skills, identify missing skills, and display the results through an interactive web application.

🔗 **Live Demo:**  
https://resumematcher-bysushantkulkarni.streamlit.app/

---

## 📌 About the Project

When applying for jobs, it can be difficult to know whether a resume matches the requirements of a particular job description.

I built this project to understand how **Python, NLP, machine learning, and web applications** can be used to solve this problem.

The application takes:

- A resume
- A job description

and then analyzes them to provide:

- Overall match score
- Skill matches
- Missing skills
- Text similarity
- Sentence-level comparison
- Suggestions for improving the resume

This project helped me practice working with **real-world text data, NLP libraries, machine learning techniques, file handling, and Streamlit**.

---

## ✨ Main Features

### 1. Resume and Job Description Matching

Upload a resume and a job description and get an overall similarity score.

The application uses three main methods:

- Semantic similarity
- Technical skill matching
- TF-IDF text similarity

### 2. Multiple File Formats

The application can read:

- PDF
- DOCX
- TXT
- Markdown files

### 3. Technical Skill Matching

The project contains a technical skill list covering areas such as:

- Programming Languages
- Frameworks
- Databases
- Cloud & DevOps
- AI/ML
- System Architecture

It checks which skills from the job description are present in the resume.

### 4. Missing Skill Identification

The application identifies skills that appear in the job description but are not found in the resume.

This can help a candidate understand areas they may want to learn or highlight if they already have the relevant experience.

### 5. Sentence-Level Comparison

Resume statements can be compared with job-description requirements to understand which parts of the resume are more closely related to the job.

### 6. Resume Tailoring

The application provides an interactive area where resume text can be modified and analyzed again.

This makes it easier to experiment with different resume wording.

### 7. Batch Resume Matching

Multiple resumes can be compared against the same job description.

The application can display the results together so they can be compared more easily.

### 8. Report Export

The results can be exported as:

- HTML
- JSON

### 9. Streamlit Web Interface

The complete project is available through a simple web interface built using Streamlit.

---

## 🧠 How It Works

The basic flow of the application is:

```text
Resume + Job Description
          │
          ▼
   Extract Text
          │
          ▼
  Clean & Preprocess
          │
          ├───────────────┬────────────────┐
          ▼               ▼                ▼
       TF-IDF       Semantic Matching   Skill Matching
          │               │                │
          └───────────────┴────────────────┘
                          │
                          ▼
                    Match Score
                          │
                          ▼
              Skills & Missing Skills
                          │
                          ▼
                   Results Dashboard
```

---

## 📐 Matching Method

The project combines three different scores.

### 1. Semantic Similarity — 35%

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model converts text into numerical vectors called **embeddings**.

The embeddings are then compared using cosine similarity.

This helps identify text that has a similar meaning even when the exact words are different.

---

### 2. Skill Matching — 35%

The application checks the technical skills found in:

- The resume
- The job description

For example:

```text
Job Description:
Python, FastAPI, PostgreSQL, Docker

Resume:
Python, FastAPI, MySQL

Matched Skills:
Python
FastAPI

Missing Skills:
PostgreSQL
Docker
```

The skill score is based on how many required skills are matched.

---

### 3. TF-IDF Similarity — 30%

The project also uses **TF-IDF** from scikit-learn.

TF-IDF helps identify important words and phrases shared between the resume and job description.

The project considers both:

- Unigrams
- Bigrams

This provides another way to compare the two documents.

---

## 🧮 Overall Score

The three scores are combined using weighted scoring:

```text
Overall Score =
    (Semantic Score × 0.35)
  + (Skill Score × 0.35)
  + (TF-IDF Score × 0.30)
```

The weights can be adjusted in the application according to the selected requirements.

> The score is only an analytical result. It does not guarantee an interview or job selection.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application |
| scikit-learn | TF-IDF and similarity calculations |
| sentence-transformers | Semantic text similarity |
| spaCy | NLP and skill extraction |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| HTML | Report generation |
| JSON | Structured report output |
| Git & GitHub | Version control and project hosting |

---

## 📂 Project Structure

```text
resume_matcher/
│
├── resume_matcher/
│   ├── extractors/
│   │   └── # PDF, DOCX and text extraction
│   │
│   ├── preprocessing/
│   │   └── # Text cleaning and preprocessing
│   │
│   ├── models/
│   │   └── # TF-IDF and semantic matching
│   │
│   ├── analysis/
│   │   └── # Skill analysis and gap detection
│   │
│   ├── engine/
│   │   └── # Matching and scoring logic
│   │
│   ├── reporting/
│   │   └── # HTML and JSON reports
│   │
│   └── ui/
│       └── # Streamlit interface
│
├── examples/
│   ├── resumes/
│   └── job_descriptions/
│
├── tests/
│   └── # Project tests
│
├── app.py
├── main.py
├── run_tests.py
├── requirements.txt
├── setup.py
└── LICENSE
```

---

## 🚀 Run the Project Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/sushantk08/resume_matcher.git
cd resume_matcher
```

### Step 2: Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Start the Application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## 🌐 Live Application

You can try the deployed application here:

### 🔗 https://resumematcher-bysushantkulkarni.streamlit.app/

The live application allows you to upload your resume and job description and see the matching results directly in your browser.

---

## 💻 Command-Line Usage

The project also includes a simple command-line interface.

### Single Resume

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt
```

### Export HTML and JSON Reports

```bash
python main.py \
  --resume examples/resumes/senior_backend_python.txt \
  --jd examples/job_descriptions/senior_python_backend_jd.txt \
  --export-html report.html \
  --export-json report.json
```

### Multiple Resumes

```bash
python main.py \
  --batch-resumes examples/resumes/ \
  --jd examples/job_descriptions/senior_python_backend_jd.txt
```

---

## 🧪 Running Tests

The project includes tests for different parts of the application.

Run:

```bash
python run_tests.py
```

The tests cover areas such as:

- File extraction
- Text preprocessing
- TF-IDF calculations
- Similarity calculations
- Skill extraction
- Reporting

---

## 📚 What I Learned From This Project

While building this project, I gained practical experience with:

- Python project structure
- Object-oriented programming
- File handling
- PDF and DOCX processing
- Natural Language Processing
- TF-IDF
- Cosine similarity
- Transformer-based embeddings
- spaCy
- Streamlit
- Data preprocessing
- Working with external Python libraries
- Writing reusable modules
- Testing Python applications
- Generating HTML and JSON reports
- Deploying a Streamlit application

---

## 🎯 Project Highlights

This project demonstrates my ability to:

- Build a complete Python application from scratch
- Work with real-world text data
- Use machine learning/NLP libraries
- Build an interactive web interface
- Organize code into multiple modules
- Implement a practical problem-solving solution
- Test and deploy a Python application

---

## ⚠️ Disclaimer

This application is created as a learning and portfolio project.

The match score should not be considered a final hiring decision. A resume may be suitable for a position even if the calculated score is low, and a high score does not guarantee an interview or job offer.

---

## 📄 License

 **MIT License**.


---

## 👨‍💻 Author

**Sushant Satish Kulkarni**

Python Developer | Backend Development | Data & AI Applications

- GitHub: https://github.com/sushantk08
- LinkedIn: https://www.linkedin.com/in/sushant-kulkarni08/

---

