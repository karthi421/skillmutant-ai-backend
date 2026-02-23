from fastapi import APIRouter
import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-8b-instant"

router = APIRouter()



@router.post("/ai/room-chat")
def room_chat(data: dict):
    question = data.get("question", "").strip()
    notes = data.get("notes", "").strip()

    if not question:
        return {"answer": "Please ask a valid question."}

    prompt = f"""
You are an AI teaching assistant helping a group of students.

Context notes:
{notes if notes else "No notes yet."}

Student question:
{question}

Explain clearly in simple words.
"""
    '''
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )

        result = response.json()
        return {"answer": result.get("response", "No response from local AI.")}

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return {
            "answer": "Local AI is not running. Please start Ollama."
        }
    '''
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful teaching assistant explaining concepts clearly in simple words."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
        )

        answer = completion.choices[0].message.content.strip()
        return {"answer": answer}

    except Exception as e:
        print("Groq room chat error:", e)
        return {
            "answer": "AI service temporarily unavailable. Please try again."
        }