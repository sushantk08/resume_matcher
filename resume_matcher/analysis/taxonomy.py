"""
Curated technical skill taxonomy with category mappings and aliases.
"""

from typing import Dict, List

# Core taxonomy grouped by engineering domains
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "Bash", "Shell", "HTML", "CSS"
    ],
    "Frameworks & Libraries": [
        "React", "Angular", "Vue", "Next.js", "Node.js", "Express", "Django", "Flask",
        "FastAPI", "Spring Boot", ".NET", "ASP.NET", "Ruby on Rails", "Tailwind CSS",
        "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Keras", "Hugging Face"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "CI/CD", "GitHub Actions", "GitLab CI", "Linux", "Helm",
        "Prometheus", "Grafana", "Nginx", "Serverless", "CloudFormation"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB",
        "Cassandra", "SQLite", "Snowflake", "BigQuery", "Kafka", "RabbitMQ", "Neo4j"
    ],
    "AI & Data Science": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP",
        "Computer Vision", "LLMs", "Generative AI", "Data Engineering", "ETL",
        "Data Pipelines", "Statistical Modeling", "Vector Databases", "LangChain"
    ],
    "Architecture & Methodologies": [
        "Microservices", "REST APIs", "GraphQL", "System Design", "Agile", "Scrum",
        "Test-Driven Development", "TDD", "Unit Testing", "Object-Oriented Programming",
        "Event-Driven Architecture", "Domain-Driven Design", "Design Patterns"
    ]
}

# Alias resolution to canonical names
SKILL_ALIASES: Dict[str, str] = {
    "golang": "Go",
    "k8s": "Kubernetes",
    "postgres": "PostgreSQL",
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node": "Node.js",
    "vuejs": "Vue",
    "vue.js": "Vue",
    "sklearn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "amazon web services": "AWS",
    "google cloud platform": "GCP",
    "ms azure": "Azure",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "ci cd": "CI/CD",
    "tdd": "Test-Driven Development",
    "oop": "Object-Oriented Programming",
    "ml": "Machine Learning",
}