from fastapi import APIRouter
from pydantic import BaseModel

import os, json, re
from groq import Groq


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-70b-versatile"
router = APIRouter(prefix="/ai")

class QuizRequest(BaseModel):
    topic: str
    count: int = 5

@router.post("/generate-quiz")
def generate_quiz(req: QuizRequest):
    topic = req.topic.strip()
    count = req.count

    prompt = f"""
You are an expert examiner.

Generate {count} UNIQUE multiple-choice questions ONLY about:
"{topic}"

Rules:
- Stay strictly on topic
- No repetition
- No explanations
- Output ONLY valid JSON

Format:
{{
  "questions": [
    {{
      "question": "Question about {topic}",
      "options": ["A","B","C","D"],
      "answer": "A"
    }}
  ]
}}
"""
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert examiner generating MCQs strictly in valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

        raw = completion.choices[0].message.content

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError("Invalid JSON from model")

        parsed = json.loads(match.group())
        questions = parsed.get("questions", [])

    # Hard topic filter
        final = []
        seen = set()

        for q in questions:
            text = q.get("question", "").lower()
            if topic.lower() not in text:
                continue
            if text in seen:
                continue
            seen.add(text)
            final.append(q)

        if not final:
            final = [{
                "question": f"What is {topic}?",
                "options": ["A","B","C","D"],
                "answer": "A"
            }]

        return {"questions": final[:count]}

    except Exception as e:
        print("QUIZ ERROR:", e)
        return {
            "questions": [{
                "question": f"Basics of {topic}",
                "options": ["A","B","C","D"],
                "answer": "A"
            }]
        }
    


    '''
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": GROQ_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5
                }
            },
            timeout=90
        )

        raw = res.json().get("response", "")

        match = re.search(r"\{.*\}", raw, re.S)
        if not match:
            raise ValueError("Invalid JSON from model")

        parsed = json.loads(match.group())
        questions = parsed.get("questions", [])

        # Hard topic filter
        final = []
        seen = set()

        for q in questions:
            text = q.get("question", "").lower()
            if topic.lower() not in text:
                continue
            if text in seen:
                continue
            seen.add(text)
            final.append(q)

        if not final:
            final = [{
                "question": f"What is {topic}?",
                "options": ["A","B","C","D"],
                "answer": "A"
            }]

        return { "questions": final[:count] }

    except Exception as e:
        print("QUIZ ERROR:", e)
        return {
            "questions": [{
                "question": f"Basics of {topic}",
                "options": ["A","B","C","D"],
                "answer": "A"
            }]
        }
    '''