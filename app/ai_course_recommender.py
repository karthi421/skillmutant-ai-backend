"""
AI Course Recommender
--------------------
Decides WHAT the student should learn next and WHY,
based on resume analysis.
"""

from typing import List, Dict


def identify_priority_skills(
    current_skills: List[str],
    missing_skills: List[str],
    readiness: int,
) -> List[str]:
    """
    Decide which skills matter most right now.
    """

    # Safety
    if not missing_skills:
        return []

    # Core logic (MVP but intelligent)
    if readiness < 50:
        # Very weak → focus on fundamentals
        return missing_skills[:3]

    elif readiness < 70:
        # Medium → focus on 2 important gaps
        return missing_skills[:2]

    else:
        # Almost ready → polish 1 key skill
        return missing_skills[:1]


def generate_learning_plan(
    current_skills: List[str],
    missing_skills: List[str],
    target_role: str,
    readiness: int,
) -> List[Dict]:
    """
    High-level AI reasoning output.
    """

    priority_skills = identify_priority_skills(
        current_skills,
        missing_skills,
        readiness
    )

    plan = []

    for skill in priority_skills:
        plan.append({
            "skill": skill,
            "priority_reason": (
                f"{skill} is required to improve your readiness "
                f"for {target_role} roles."
            )
        })

    return plan
