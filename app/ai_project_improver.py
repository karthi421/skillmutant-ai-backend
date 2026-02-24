import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"


def generate_project_improvements(project_text: str):
    try:
        prompt = f"""
You are a senior software engineer and technical recruiter.

Analyze the following project and suggest
specific improvements to increase hiring chances.

Project Description:
{project_text}
"""

        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert recruiter and mentor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )

        text = completion.choices[0].message.content

        return [
            s.strip("- ").strip()
            for s in text.split("\n")
            if len(s.strip()) > 10
        ]

    except Exception:
        return [
            "Add measurable impact such as scale or performance.",
            "Explain architectural decisions clearly.",
            "Highlight challenges and solutions.",
            "Mention deployment or testing if applicable.",
            "Rewrite description to emphasize problem-solving."
        ]