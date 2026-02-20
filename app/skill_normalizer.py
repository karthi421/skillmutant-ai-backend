# app/skill_normalizer.py

SKILL_SYNONYMS = {
    "dsa": [
        "data structures",
        "algorithms",
        "data structures and algorithms",
        "dsa"
    ],
    "ml": [
        "machine learning",
        "ml"
    ],
    "ai": [
        "artificial intelligence",
        "ai"
    ],
    "frontend": [
        "frontend development",
        "html css javascript",
        "react"
    ],
    "backend": [
        "backend development",
        "node js",
        "django",
        "spring boot"
    ],
}

def normalize_skill(skill: str) -> dict:
    key = skill.lower().strip()

    for canonical, variants in SKILL_SYNONYMS.items():
        if key == canonical or key in variants:
            return {
                "canonical": canonical,
                "queries": variants
            }

    # fallback
    return {
        "canonical": key,
        "queries": [key]
    }
