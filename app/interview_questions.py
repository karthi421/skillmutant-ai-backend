def generate_questions(project):
    tech = project["analysis"]["tech_stack"]
    complexity = project["analysis"]["complexity"]

    questions = [
        "Explain the problem your project solves.",
        "Why did you choose this architecture?",
        "What challenges did you face and how did you solve them?"
    ]

    if "python" in tech:
        questions.append("Why did you choose Python for this project?")
    if "react" in tech:
        questions.append("How did you manage state and component design?")
    if "machine learning" in tech:
        questions.append("How did you evaluate your ML model performance?")
    if complexity == "High":
        questions.append("How would you scale this project for 1M users?")

    return questions
