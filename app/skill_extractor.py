def extract_skills(text: str):
    print("✅ extract_skills USING FALLBACK ONLY")

    # Simple keyword-based extraction (stable & fast)
    SKILLS = [
        "HTML", "CSS", "JavaScript", "TypeScript",
        "React", "Node.js", "Python", "Java",
        "Spring", "SQL", "Git", "REST", "FastAPI",
        "Mongodb","data science","Cyber security"
    ]

    found = []
    lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower:
            found.append({
                "name": skill,
                "description": f"Hands-on experience with {skill} as identified from resume.",
                "confidence": 0.75
            })

    return found

def extract_and_categorize_skills(raw_skills):
    """
    Deterministic categorization (NO AI)
    """

    CATEGORY_MAP = {
        "frontend": ["HTML", "CSS", "JavaScript", "TypeScript", "React"],
        "backend": ["Python", "Java", "Node.js", "Spring", "FastAPI"],
        "database": ["SQL", "MongoDB", "PostgreSQL"],
        "tools": ["Git", "Docker"]
    }

    categories = {}
    confidence = {}

    for skill in raw_skills:
        name = skill["name"]
        confidence[name] = int(skill.get("confidence", 0.75) * 100)

        placed = False
        for category, skills in CATEGORY_MAP.items():
            if name in skills:
                categories.setdefault(category, []).append({
                    "name": name,
                    "description": skill.get("description", "")
                })
                placed = True
                break

        if not placed:
            categories.setdefault("other", []).append({
                "name": name,
                "description": skill.get("description", "")
            })

    return categories, confidence
