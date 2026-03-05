def calculate_skill_overlap(user_skills, job_skills):

    if not job_skills:
        return 0

    overlap = len(set(user_skills) & set(job_skills))

    return min(100, (overlap / len(job_skills)) * 100)


def calculate_role_similarity(job_title, target_role):

    if not job_title or not target_role:
        return 0

    title = job_title.lower()
    role = target_role.lower()

    if role in title:
        return 100

    if role.split()[0] in title:
        return 70

    return 40


def calculate_skill_depth(user_skills):

    if len(user_skills) >= 10:
        return 100

    return min(100, len(user_skills) * 10)


def compute_job_match_score(user_skills, job, target_role):

    job_skills = job.get("skills", [])

    overlap = calculate_skill_overlap(user_skills, job_skills)

    role_score = calculate_role_similarity(
        job.get("title", ""),
        target_role
    )

    depth = calculate_skill_depth(user_skills)

    final_score = int(
        overlap * 0.5 +
        role_score * 0.3 +
        depth * 0.2
    )

    return final_score