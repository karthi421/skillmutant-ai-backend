from typing import List, Dict

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


def match_jobs_to_resume(
    skills: List[str],
    target_role: str,
    jobs: List[Dict]
) -> List[Dict]:

    enriched = []

    for job in jobs:
        job["relevance"] = calculate_relevance(job, skills, target_role)
        job["reason"] = generate_reason(job, skills)
        enriched.append(job)

    enriched.sort(key=lambda x: x["relevance"], reverse=True)
    return enriched
