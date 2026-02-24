import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"


def generate_ai_questions(project_description: str):
    """
    Generate recruiter interview questions strictly based on the given project.
    """

    try:
        prompt = f"""
You are a senior technical interviewer.

A candidate has worked on the following project:

\"\"\"{project_description}\"\"\"

Generate 6–8 interview questions that a real recruiter would ask
SPECIFICALLY about THIS project.

Rules:
- Questions must be based ONLY on the project details
- Cover architecture, logic, decisions, edge cases, and improvements
- Avoid generic questions
- Do not repeat questions
- Do not mention the word "resume"

Return ONLY a bullet list of questions.
"""

        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an experienced software interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        text = completion.choices[0].message.content

        questions = [
            q.strip("- ").strip()
            for q in text.split("\n")
            if q.strip().startswith("-")
        ]

        unique_questions = list(dict.fromkeys(questions))

        return unique_questions[:8]

    except Exception:
        return [
            "Can you explain the core problem this project solves?",
            "What were the main technical challenges in this project?",
            "Why did you choose this approach or architecture?",
            "How would you improve or scale this project further?",
            "What edge cases did you consider in this implementation?",
        ]