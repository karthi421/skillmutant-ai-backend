TECH_STACK = [
    "python", "java", "c++", "react", "node", "mongodb",
    "mysql", "flask", "fastapi", "django",
    "machine learning", "api", "cloud"
]

def analyze_project(project_text: str):
    text = project_text.lower()

    tech_used = [t for t in TECH_STACK if t in text]

    complexity = (
        "High" if len(tech_used) >= 4 else
        "Medium" if len(tech_used) >= 2 else
        "Low"
    )

    hire_score = (
        85 if complexity == "High" else
        65 if complexity == "Medium" else
        45
    )

    verdict = (
        "Strong recruiter-attractive project"
        if hire_score >= 80 else
        "Good project, needs stronger impact explanation"
        if hire_score >= 60 else
        "Basic project, limited hiring value"
    )

    return {
        "tech_stack": tech_used,
        "complexity": complexity,
        "hire_score": hire_score,
        "verdict": verdict
    }
