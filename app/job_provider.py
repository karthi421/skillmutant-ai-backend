from typing import List, Dict
from datetime import datetime

SEARCH_VARIANTS = [
    "{skill} Developer",
    "{skill} Engineer",
    "Software Engineer {skill}",
    "{skill} Intern",
    "{skill} Fresher",
]


def generate_job_links(skill: str, platform: str, base_url: str) -> List[Dict]:
    jobs = []

    for variant in SEARCH_VARIANTS:
        query = variant.format(skill=skill)

        jobs.append({
            "title": query,
            "company": "Multiple Companies",
            "platform": platform,
            "url": base_url.format(query=query.replace(" ", "%20")),
            "posted": datetime.utcnow().isoformat(),
        })

    return jobs


def fetch_jobs_for_skill(skill: str) -> List[Dict]:
    jobs = []

    jobs += generate_job_links(
        skill,
        "LinkedIn",
        "https://www.linkedin.com/jobs/search/?keywords={query}"
    )

    jobs += generate_job_links(
        skill,
        "Naukri",
        "https://www.naukri.com/{query}-jobs"
    )

    jobs += generate_job_links(
        skill,
        "Internshala",
        "https://internshala.com/internships/keywords-{query}"
    )

    jobs += generate_job_links(
        skill,
        "Unstop",
        "https://unstop.com/search/{query}"
    )

    return jobs
