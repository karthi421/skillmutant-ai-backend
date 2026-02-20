def evaluate_interview(job_role, company, answers):
    score = {
        "communication": 78,
        "confidence": 72,
        "clarity": 80,
        "technical_relevance": 75,
    }

    feedback = [
        "You communicated your ideas clearly but can improve structure.",
        "Confidence improved in later answers.",
        "Technical explanations were relevant to the role.",
        f"Good alignment with {company}'s expectations for a {job_role}.",
    ]

    return {
        "score": score,
        "feedback": feedback
    }
