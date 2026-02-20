PLATFORM_LOGOS = {
    "LinkedIn": "https://cdn-icons-png.flaticon.com/512/174/174857.png",
    "Naukri": "https://static.naukimg.com/s/4/100/i/naukri_Logo.png",
    "Internshala": "https://internshala.com/static/images/favicon.ico",
    "Unstop": "https://unstop.com/favicon.ico",
}

DEFAULT_SKILL_THUMBNAIL = "https://img.freepik.com/free-vector/job-search-concept-illustration_114360-1086.jpg"


def resolve_thumbnail(platform: str) -> str:
    return PLATFORM_LOGOS.get(platform, DEFAULT_SKILL_THUMBNAIL)
