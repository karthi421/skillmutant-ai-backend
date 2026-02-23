import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-70b-versatile"


def generate_project_ideas(skills):
    try:
        prompt = f"""
You are a senior software engineer and recruiter.

A student resume has no projects.
Based on the following skills, suggest project ideas
categorized by difficulty level.

Return ideas in this format:

Beginner:
- idea + short explanation

Intermediate:
- idea + short explanation

Advanced:
- idea + short explanation

Skills:
{', '.join(skills)}
"""

        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a technical mentor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        text = completion.choices[0].message.content

        ideas = {"beginner": [], "intermediate": [], "advanced": []}
        current = None

        for line in text.split("\n"):
            l = line.lower()
            if "beginner" in l:
                current = "beginner"
            elif "intermediate" in l:
                current = "intermediate"
            elif "advanced" in l:
                current = "advanced"
            elif line.strip().startswith("-") and current:
                ideas[current].append(line.strip("- ").strip())

        return ideas

    except Exception:
        return {
            "beginner": [
                "Personal portfolio website – shows basic frontend skills",
                "Simple CRUD application – demonstrates backend fundamentals"
            ],
            "intermediate": [
                "Resume analyzer – combines file handling and APIs",
                "Authentication system – shows security awareness"
            ],
            "advanced": [
                "AI-powered recommendation system – shows applied ML",
                "Scalable backend system – demonstrates system design"
            ]
        }