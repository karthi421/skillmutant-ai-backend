from groq import Groq
import os
from typing import List
INTERVIEW_ROUNDS = [
    "introduction",
    "technical_core",
    "deep_technical",
    "system_design",
    "behavioral",
    "hr"
]
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"


def generate_interview_question(
    skills: List[str],
    role: str,
    company: str,
    round_type: str,
    difficulty: str = "medium",
    previous_questions: List[str] = None,
):
    previous_questions = previous_questions or []

    round_instructions = {
        "introduction": "Start with a strong introductory or background question.",
        "technical_core": "Ask a practical coding or implementation-based question.",
        "deep_technical": "Ask a deep optimization or architecture-level question.",
        "system_design": "Ask a scalable system design question relevant to the role.",
        "behavioral": "Ask a real-world behavioral or conflict-resolution question.",
        "hr": "Ask culture-fit or career growth question."
    }

    instruction = round_instructions.get(round_type, "")

    prompt = f"""
You are a senior interviewer at {company}.

Interviewing for role: {role}
Difficulty: {difficulty}
Round Type: {round_type}

Candidate skills:
{", ".join(skills)}

Previously asked:
{previous_questions if previous_questions else "None"}

Instructions:
- {instruction}
- Must be realistic and company-level.
- Avoid generic textbook questions.
- Do not repeat previous questions.
- Only output the question.
"""

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a strict, intelligent interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)
        return "Tell me about a challenging project you worked on."