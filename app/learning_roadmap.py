ROLE_ROADMAPS = {

    "Software Developer": [
        {
            "phase": "Foundation",
            "skills": ["DSA", "OOP"]
        },
        {
            "phase": "Backend Development",
            "skills": ["APIs", "Databases"]
        },
        {
            "phase": "Advanced Engineering",
            "skills": ["System Design", "Scalability"]
        }
    ],

    "Frontend Developer": [
        {
            "phase": "Foundation",
            "skills": ["HTML", "CSS", "JavaScript"]
        },
        {
            "phase": "Frontend Frameworks",
            "skills": ["React", "State Management"]
        },
        {
            "phase": "Advanced Frontend",
            "skills": ["Performance", "Architecture"]
        }
    ],

    "Backend Developer": [
        {
            "phase": "Foundation",
            "skills": ["Python", "SQL"]
        },
        {
            "phase": "API Development",
            "skills": ["FastAPI", "Authentication"]
        },
        {
            "phase": "Advanced Backend",
            "skills": ["System Design", "Caching"]
        }
    ]
}


def generate_learning_roadmap(current_skills, target_role):

    roadmap = ROLE_ROADMAPS.get(target_role)

    if not roadmap:
        return []

    result = []

    for phase in roadmap:

        missing = [
            s for s in phase["skills"]
            if s not in current_skills
        ]

        if missing:

            result.append({
                "phase": phase["phase"],
                "skills": missing
            })

    return result