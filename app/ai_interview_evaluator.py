import os
import json
import re
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama3-8b-8192"


def evaluate_full_interview(answers):
    transcript = ""

    for a in answers:
        transcript += f"""
Question: {a['question']}
Answer: {a['answer']}
"""

    prompt = f"""
You are a senior technical interviewer.

Evaluate the following mock interview transcript.

Give:
1. Overall score out of 100
2. Strengths
3. Weaknesses
4. Communication feedback
5. Technical depth feedback

Transcript:
{transcript}

Respond in STRICT JSON format:
{{
  "score": number,
  "feedback": string
}}
"""

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You evaluate interviews fairly and professionally."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        raw = completion.choices[0].message.content

        # Extract JSON safely
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError("Invalid JSON response")

        return json.loads(match.group())

    except Exception:
        return {
            "score": 60,
            "feedback": "Evaluation could not be generated. Please try again."
        }