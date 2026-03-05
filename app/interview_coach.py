import json
import re
from groq import Groq
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def generate_followup_question(question, answer, role):

    prompt = f"""
You are a senior technical interviewer.

Original Question:
{question}

Candidate Answer:
{answer}

Role:
{role}

Ask ONE intelligent follow-up question based on the candidate answer.

Rules:
- Technical depth
- Short question
- No explanation
"""

    try:
        completion = groq_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("Follow-up generation failed:", e)
        return "Can you explain your reasoning in more detail?"