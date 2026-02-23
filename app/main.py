from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import pdfplumber
import os
from dotenv import load_dotenv
import json
import requests

from fastapi import APIRouter
from groq import Groq
router = APIRouter()


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
load_dotenv()  # ⬅️ THIS IS REQUIRED
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-70b-versatile"
# ================== CORE AI MODULES ==================
from app.skill_extractor import (
    extract_skills,
    extract_and_categorize_skills
)
from app.ai_resume_suggester import generate_resume_suggestions
from app.project_extractor import extract_projects
from app.ai_project_ideas import generate_project_ideas
from app.ai_course_recommender import generate_learning_plan
from app.course_aggregator import fetch_courses_for_skill, enrich_courses
from app.job_provider import fetch_jobs_for_skill
from app.job_matcher import match_jobs_to_resume
from app.interview_engine import generate_interview_question
from app.interview_scoring import score_answer
from app.ai_mock_interview import router as mock_router
from app.mock_interview_evaluator import evaluate_interview
from app.rooms import router as rooms_router
from app.ws_rooms import room_signaling
from app.ai_room_chat import router as ai_room_router
from app.routes.account import router as account_router
from app.routes.quiz import router as quiz_router

from app.routes.dashboard_ai import router as dashboard_ai_router










# ================== APP INIT ==================
app = FastAPI(
    title="SkillMutant AI Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(mock_router)
app.include_router(rooms_router)
app.include_router(ai_room_router)
app.include_router(account_router)
app.include_router(quiz_router)
app.include_router(dashboard_ai_router)

# ================== UTILITIES ==================
def extract_text_from_pdf(file: UploadFile) -> str:
    """Safely extract text from PDF resume"""
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def normalize_skills(raw_skills) -> List[str]:
    """Extract only skill names from mixed structures"""
    skills = []
    for item in raw_skills:
        if isinstance(item, dict):
            name = item.get("name")
            if name:
                skills.append(name.strip())
        elif isinstance(item, str):
            skills.append(item.strip())
    return list(set(skills))

# =========================================================
# ================= RESUME ANALYSIS =======================
# =========================================================

@app.post("/analyze-resume")
def analyze_resume(
    resume: UploadFile = File(...),
    target_role: str = Form(...),
    token: str = Form(None)
):
    # ---------- Extract resume text ----------
    resume_text = extract_text_from_pdf(resume)

    # ---------- Raw skill extraction ----------
    raw_skills = extract_skills(resume_text)
    skills = normalize_skills(raw_skills)

    # ---------- Categorization + confidence ----------
    categories, confidence = extract_and_categorize_skills(raw_skills)

    # ---------- Resume suggestions ----------
    resume_suggestions = generate_resume_suggestions(resume_text)

    # ---------- Project extraction ----------
    raw_projects = extract_projects(resume_text)

    projects = [
        {
            "description": p,
            "hire_score": 70 + min(len(skills), 20),
            "interview_questions": [
                "Explain the architecture of this project",
                "What challenges did you face?",
                "How would you scale this system?"
            ],
            "ai_improvements": [
                "Add measurable impact (numbers, metrics)",
                "Improve documentation clarity",
                "Highlight problem-solving decisions"
            ]
        }
        for p in raw_projects
    ]

    # ---------- Project ideas ----------
    try:
        project_ideas = generate_project_ideas(skills=skills, role=target_role)
    except TypeError:
        project_ideas = generate_project_ideas(skills=skills)

    # ---------- ATS Score ----------
    ats_score = min(95, 50 + len(skills) * 4)

    # ---------- Final response ----------
    if token:
        log_progress_activity(
            token,
            "resume",
            "Analyzed resume using AI"
        )

    return {
        # ===== SKILL GRAPH (CRITICAL) =====
        "categories": categories,
        "confidence": confidence,

        # ===== ATS =====
        "ats_score": ats_score,
        "ats_verdict": "Resume analyzed successfully",
        "ats_checklist": [
            {
                "item": "Keyword match",
                "status": True,
                "fix": ""
            },
            {
                "item": "Clear section headings",
                "status": False,
                "fix": "Use Skills / Experience / Projects headings"
            }
        ],

        # ===== CORE INTELLIGENCE =====
        "projects": projects,
        "resume_suggestions": resume_suggestions,
        "project_ideas": project_ideas,

        # ===== COURSE INPUT =====
        "current_skills": skills,
        "missing_skills": [],
        "readiness": ats_score,
        "target_role": target_role,
        "skills": skills,                 # ✅ for ResumeAnalysis.jsx
        "best_role": target_role
    }

# =========================================================
# ================= COURSE RECOMMENDER ====================
# =========================================================
@app.post("/ai/recommend-courses")
def recommend_courses(data: Dict):
    """
    FINAL LOGIC:
    1. User search (absolute priority)
    2. AI resume-based fallback
    """

    # -----------------------------
    # USER SEARCH MODE (STRICT)
    # -----------------------------
    user_query = data.get("query") or data.get("user_query")

    if user_query:
        skill = user_query.strip()

        courses = fetch_courses_for_skill(skill)
        enriched = enrich_courses(skill, courses)

        return {
            "recommendations": [
                {
                    "skill": skill,
                    "priority_reason": f"Strictly based on your search: {skill}",
                    "courses": enriched
                }
            ]
        }

    # -----------------------------
    # AI RESUME MODE (DEFAULT)
    # -----------------------------
    current_skills = data.get("current_skills", [])
    target_role = data.get("target_role", "")
    readiness = data.get("readiness", 0)

    EXPECTED_SKILLS_BY_ROLE = {
        "Frontend Developer": ["React", "JavaScript", "TypeScript"],
        "Backend Developer": ["Python", "FastAPI", "SQL"],
        "Full Stack Developer": ["React", "Node.js", "SQL"],
        "Software Developer": ["DSA", "OOP", "System Design"],
    }

    expected = EXPECTED_SKILLS_BY_ROLE.get(target_role, [])
    missing_skills = [s for s in expected if s not in current_skills]

    learning_plan = generate_learning_plan(
        current_skills=current_skills,
        missing_skills=missing_skills,
        target_role=target_role,
        readiness=readiness
    )

    if not learning_plan:
        learning_plan = [
            {
                "skill": skill,
                "priority_reason": "Recommended to strengthen your profile"
            }
            for skill in current_skills[:3]
        ]

    recommendations = []

    for step in learning_plan:
        skill = step["skill"]
        courses = fetch_courses_for_skill(skill)
        enriched = enrich_courses(skill, courses)

        recommendations.append({
            "skill": skill,
            "priority_reason": step["priority_reason"],
            "courses": enriched
        })
    token = data.get("token")
    if token:
        log_progress_activity(
            token,
            "course",
            "Viewed AI course recommendations"
        )

    return { "recommendations": recommendations }
# app/main.py






@app.post("/ai/recommend-jobs")
def recommend_jobs(data: Dict):
    skills = data.get("skills", [])
    target_role = data.get("target_role", "")

    all_jobs = []
    for skill in skills[:5]:
        all_jobs += fetch_jobs_for_skill(skill)

    matched = match_jobs_to_resume(
        skills=skills,
        target_role=target_role,
        jobs=all_jobs
    )
    token = data.get("token")
    if token:
        log_progress_activity(
            token,
            "job",
            "Viewed AI job recommendations"
        )

    return {
        "jobs": matched
    }


@app.post("/ai/start-interview")
def start_interview(data: dict):
    question = generate_interview_question(
        data["resume_skills"],
        data["job_role"]
    )
    return { "question": question }


@app.post("/ai/evaluate-answer")
def evaluate_answer(data: dict):
    score = score_answer(data["answer"])
    return score


@router.post("/ai/mock-interview/final-evaluation")
def final_interview_evaluation(data: dict):
    import json, re, requests, datetime

    job_role = data.get("job_role")
    company = data.get("company")
    answers = data.get("answers", [])
    token = data.get("token")

    # ===============================
    # BUILD TRANSCRIPT
    # ===============================
    transcript = ""
    for i, a in enumerate(answers, 1):
        transcript += f"""
Question {i}: {a.get('question')}
Candidate Answer: {a.get('answer')}
"""

    prompt = f"""
You are a senior interviewer at {company}, interviewing for a {job_role} role.

Evaluate the interview transcript below.

Transcript:
{transcript}

STRICT RULES:
- Respond with ONLY valid JSON
- No markdown
- No explanation

JSON format:
{{
  "score": {{
    "communication": number,
    "confidence": number,
    "clarity": number,
    "technical_relevance": number
  }},
  "feedback": {{
    "strengths": [string, string, string],
    "weaknesses": [string, string, string],
    "advice": [string, string, string]
  }}
}}
"""

    result = None

    # ===============================
    # CALL OLLAMA (SAFE)
    # ===============================
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            raw = response.json().get("response", "")
            match = re.search(r"\{[\s\S]*\}", raw)

            if match:
                result = json.loads(match.group())
    except Exception as e:
        print("⚠️ Ollama error:", e)
    """
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a senior technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        raw = completion.choices[0].message.content
        match = re.search(r"\{[\s\S]*\}", raw)

        if match:
            result = json.loads(match.group())

    except Exception as e:
        print("⚠️ Groq error:", e)
    # ===============================
    # FALLBACK (NEVER BREAK UI)
    # ===============================
    if not result:
        result = {
            "score": {
                "communication": 60,
                "confidence": 60,
                "clarity": 60,
                "technical_relevance": 60
            },
            "feedback": {
                "strengths": ["Interview completed successfully"],
                "weaknesses": ["Evaluation could not be generated"],
                "advice": ["Try again later for detailed feedback"]
            }
        }

    # ===============================
    # SAVE TO JOBS HUB / PROGRESS
    # ===============================
    if token:
        avg_score = round(sum(result["score"].values()) / 4)

        log_progress_activity(
            token,
            "mock_interview",
            f"Mock Interview: {company} ({job_role})",
            meta={
                "company": company,
                "role": job_role,
                "score": avg_score,
                "feedback": result["feedback"],
                "date": datetime.datetime.utcnow().isoformat()
            }
        )

    return result


app.include_router(router)

@app.websocket("/ws/rooms/{room_id}/{user_id}")
async def room_ws(websocket: WebSocket, room_id: str, user_id: str):
    await room_signaling.connect(room_id, user_id, websocket)

    try:
        
        #while True:
        #    message = await websocket.receive_json()

            # Broadcast media status updates
        #    if message.get("type") == "media-status":
        #        await room_signaling.broadcast(
        #            room_id,
        #            message,
        #            exclude=user_id
        #        )
        while True:
            message = await websocket.receive_json()

            msg_type = message.get("type")

    # 🔁 WebRTC signaling relay
            if msg_type in ["offer", "answer", "ice"]:
                await room_signaling.relay(
                    room_id,
                    sender_id=user_id,
                    payload={
                        **message,
                        "target": message.get("to") or message.get("target")
                    }
                )

    # Broadcast media status updates
            elif msg_type == "media-status":
                await room_signaling.broadcast(
                    room_id,
                    {
                        **message,
                        "from": user_id
                    },
                    exclude=user_id
                )


    except WebSocketDisconnect:
        await room_signaling.disconnect(room_id, user_id)
MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:5000")

def log_progress_activity(
    token: str,
    activity_type: str,
    title: str,
    meta: dict | None = None
):
    try:
        payload = {
            "type": activity_type,
            "title": title,
        }

        if meta:
            payload["meta"] = meta

        requests.post(
            f"{MAIN_BACKEND_URL}/progress/activity",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=2,
        )
    except Exception as e:
        # NEVER crash interview flow
        print("Progress log failed:", e)

from fastapi import APIRouter
from pydantic import BaseModel

import json
import re

router = APIRouter()


class QuizRequest(BaseModel):
    topic: str
    count: int = 5


@router.post("/ai/generate-quiz")
def generate_quiz(payload: QuizRequest):
    topic = payload.topic.lower().strip()
    final_count = payload.count
    request_count = final_count + 2  # ask more than needed
    
    if not topic:
        return {"questions": []}

    prompt = f"""
Generate {request_count} SIMPLE beginner-level multiple-choice questions about "{topic}".

Rules:
- Beginner level
- Clear conceptual understanding
- No tricky questions
- Add short explanation (1-2 lines)
- Output STRICT JSON only

FORMAT:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "answer": "Correct Option",
      "explanation": "Short explanation why the answer is correct."
    }}
  ]
}}
"""
    """
    try:
        raw = subprocess.check_output(
            ["ollama", "run", "phi3:mini"],
            input=prompt,
            text=True,
            encoding="utf-8",
            timeout=30
        )

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return {"questions": []}

        data = json.loads(match.group())
        questions = data.get("questions", [])

    except Exception as e:
        print("QUIZ AI ERROR:", e)
        return {"questions": []}
    """

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You generate beginner-level MCQs in strict JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        raw = completion.choices[0].message.content

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return {"questions": []}

        data = json.loads(match.group())
        questions = data.get("questions", [])

    except Exception as e:
        print("QUIZ AI ERROR:", e)
        return {"questions": []}
    # 🔒 Strong Validation
    valid = []
    seen_questions = set()

    for q in questions:
        if not isinstance(q, dict):
            continue

        question = q.get("question")
        options = q.get("options")
        answer = q.get("answer")

        explanation = q.get("explanation")

        if (
            isinstance(question, str)
            and isinstance(options, list)
            and isinstance(explanation, str)
            and explanation.strip() != ""
            and len(options) == 4
            and answer in options
        ):

            # remove duplicates
            if question.strip().lower() not in seen_questions:
                seen_questions.add(question.strip().lower())
                valid.append({
                    "question": question.strip(),
                    "options": options,
                    "answer": answer,
                    "explanation": explanation.strip()
                })

    return {"questions": valid[:final_count]}
