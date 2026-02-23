from fastapi import APIRouter
from typing import Dict

import json

router = APIRouter()
import os
import re
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-70b-versatile"
router = APIRouter()
# you already have this installed

# ===============================
# AI QUESTION GENERATOR
# ===============================
@router.post("/ai/mock-interview/question")
def generate_question(data: Dict):
    role = data["job_role"]
    company = data["company"]
    skills = data.get("resume_skills", [])
    previous = data.get("previous_answers", [])

    asked_questions = {a["question"].strip().lower() for a in previous}

    last_answer = previous[-1]["answer"].strip().lower() if previous else ""
    weak_answer = len(last_answer.split()) < 3 or "don't know" in last_answer

    # Decide interview phase
    if not previous:
        phase = "personal"
    elif weak_answer:
        phase = "simpler"
    elif len(previous) < 3:
        phase = "behavioral"
    else:
        phase = "technical"

    prompt = f"""
You are a HUMAN interviewer.

Ask ONE short interview question.

Rules (STRICT):
- Ask ONLY one question
- Max 15 words
- Never repeat previous questions
- Do NOT ask the same behavioral question again
- If candidate said "I don't know", switch topic or simplify
- Do NOT mention coaching, AI, or explanations

Interview phase: {phase}

Role: {role}
Company: {company}
Skills: {", ".join(skills) if skills else "N/A"}

Previously asked questions:
{list(asked_questions)}

Return ONLY the question.
"""

    # Try up to 3 times to avoid repetition
    '''
    for _ in range(3):
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": QUESTION_MODEL if "QUESTION_MODEL" in globals() else OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 40
                }
            },
            timeout=20
        )

        question = response.json()["response"].strip()

        if question.lower() not in asked_questions:
            return {"question": question}

    # Fallback (guaranteed non-repeat)
    return {
        "question": "Can you briefly describe one project you enjoyed working on?"
    }
    '''

    for _ in range(3):
        try:
            completion = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are a human interviewer asking short interview questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )

            question = completion.choices[0].message.content.strip()

        # Remove accidental quotes
            question = question.replace('"', '').strip()

            if question.lower() not in asked_questions:
                return {"question": question}

        except Exception as e:
            print("Groq question error:", e)
# ===============================
# AI ANSWER EVALUATION
# ===============================
@router.post("/ai/mock-interview/evaluate")
def evaluate_answer(data: Dict):
    question = data["question"]
    answer = data["answer"]
    role = data.get("job_role", "the role")

    prompt = f"""
You are a HUMAN interviewer evaluating a candidate's response.

Evaluate the answer below.

Role: {role}
Question: {question}
Answer: {answer}

RULES:
- Be realistic and fair
- Scores must reflect interview standards
- Feedback must be short and actionable

Return STRICT JSON only:
{{
  "communication": number (0-100),
  "technical": number (0-100),
  "confidence": number (0-100),
  "problem_solving": number (0-100),
  "feedback": string
}}
"""
    ''''
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EVALUATION_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 120
            }
        },
        timeout=30
    )

    result = json.loads(response.json()["response"])
    '''
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You evaluate interview answers fairly and realistically."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        raw = completion.choices[0].message.content

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError("Invalid JSON from Groq")

        result = json.loads(match.group())

    except Exception as e:
        print("Groq evaluation error:", e)
        return {
            "scores": {
                "communication": 60,
                "technical": 60,
                "confidence": 60,
                "problem_solving": 60,
            },
            "overall": 60,
            "feedback": "Evaluation could not be generated. Try again."
       }
    overall = (
        result["communication"]
        + result["technical"]
        + result["confidence"]
        + result["problem_solving"]
    ) // 4

    return {
        "scores": {
            "communication": result["communication"],
            "technical": result["technical"],
            "confidence": result["confidence"],
            "problem_solving": result["problem_solving"],
        },
        "overall": overall,
        "feedback": result["feedback"]
    }
