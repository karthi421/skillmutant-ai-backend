import re

def calculate_keyword_score(resume_text, target_role):
    keywords = target_role.lower().split()
    matches = sum(
        1 for k in keywords if k in resume_text.lower()
    )
    return min(100, matches * 20)


def calculate_skill_score(skills):
    if not skills:
        return 30
    return min(100, 40 + len(skills) * 5)


def calculate_structure_score(resume_text):
    sections = ["experience", "projects", "skills", "education"]

    score = 0
    text = resume_text.lower()

    for s in sections:
        if s in text:
            score += 25

    return score


def calculate_experience_score(resume_text):
    bullets = len(re.findall(r"•|-", resume_text))
    numbers = len(re.findall(r"\d+", resume_text))

    score = min(100, bullets * 3 + numbers * 2)

    return score


def compute_ats_score(resume_text, skills, target_role):
    keyword = calculate_keyword_score(resume_text, target_role)
    skill = calculate_skill_score(skills)
    structure = calculate_structure_score(resume_text)
    experience = calculate_experience_score(resume_text)

    ats_score = int(
        keyword * 0.35 +
        skill * 0.25 +
        structure * 0.20 +
        experience * 0.20
    )

    breakdown = {
        "keyword_match": keyword,
        "skill_strength": skill,
        "resume_structure": structure,
        "experience_quality": experience
    }

    return ats_score, breakdown