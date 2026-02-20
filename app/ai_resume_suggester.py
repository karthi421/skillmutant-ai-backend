import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama3-8b-8192"


def generate_resume_suggestions(skills):
    try:
        prompt = f"""
You are a technical recruiter.

A student resume has NO projects listed.
Based on the following skills, suggest:

1. Why missing projects is a problem
2. 3–5 project ideas that align with these skills
3. What recruiters expect to see in such projects

Skills:
{', '.join(skills)}
"""

        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a senior technical recruiter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        text = completion.choices[0].message.content

        return [
            s.strip("- ").strip()
            for s in text.split("\n")
            if len(s.strip()) > 10
        ]

    except Exception:
        return [
            "Your resume does not list any projects, which is a major concern for recruiters.",
            "Add at least 2–3 projects demonstrating real-world problem solving.",
            "Projects should show how you apply your skills, not just list technologies.",
            "Consider building small but complete applications aligned with your career goal."
        ]