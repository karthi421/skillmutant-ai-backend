from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from groq import Groq
import os
import json

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/ai/dashboard-assistant")
async def dashboard_assistant(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    def stream():
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield json.dumps({
                    "message": {
                        "content": chunk.choices[0].delta.content
                    }
                }) + "\n"

    return StreamingResponse(stream(), media_type="text/plain")