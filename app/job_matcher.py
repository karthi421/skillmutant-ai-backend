from typing import List, Dict
from app.job_scorer import compute_job_match_score
KEYWORD_SCORE = {
    "developer": 20,
    "engineer": 20,
    "intern": 10,
    "fresher": 10,
}


def calculate_relevance(job: Dict, skills: List[str], target_role: str) -> int:
    score = 30
    title = job["title"].lower()

    for skill in skills:
        if skill.lower() in title:
            score += 15

    for key, value in KEYWORD_SCORE.items():
        if key in title:
            score += value

    if target_role.lower() in title:
        score += 20

    return min(score, 100)


def generate_reason(job: Dict, skills: List[str]) -> str:
    matched = [s for s in skills if s.lower() in job["title"].lower()]

    if matched:
        return f"Matches your skills: {', '.join(matched)}"

    return "Recommended based on your resume and market demand"


def match_jobs_to_resume(skills, target_role, jobs):

    ranked = []

    for job in jobs:

        score = compute_job_match_score(
            skills,
            job,
            target_role
        )

        job["match_score"] = score

        ranked.append(job)

    ranked.sort(
        key=lambda j: j["match_score"],
        reverse=True
    )

    return ranked[:20]