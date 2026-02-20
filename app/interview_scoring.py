def score_answer(answer: str):
    length_score = min(len(answer.split()) * 2, 40)

    communication = 30 if len(answer.split()) > 20 else 15
    clarity = 20 if "because" in answer.lower() else 10

    return {
        "communication": communication,
        "clarity": clarity,
        "confidence": length_score,
        "total": communication + clarity + length_score
    }
