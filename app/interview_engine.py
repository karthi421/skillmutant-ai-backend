from typing import List
import random

QUESTION_BANK = {
    "communication": [
        "Tell me about yourself.",
        "Explain a challenge you faced and how you handled it."
    ],
    "technical": [
        "Explain a project you worked on.",
        "How would you optimize your solution?"
    ],
    "hr": [
        "Why do you want to join this company?",
        "Where do you see yourself in 3 years?"
    ]
}

def generate_interview_question(skills: List[str], role: str):
    category = random.choice(list(QUESTION_BANK.keys()))
    return random.choice(QUESTION_BANK[category])
