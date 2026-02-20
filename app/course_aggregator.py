import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

from app.freecodecamp_provider import get_freecodecamp_courses

load_dotenv()

# =======================
# ENV
# =======================
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


# =========================================================
# 🔹 YOUTUBE (REAL API)
# =========================================================
def fetch_youtube_videos(query: str, max_results: int = 25) -> List[Dict]:
    """
    HIGH PRECISION SEARCH
    Enforces topic relevance
    """

    if not YOUTUBE_API_KEY:
        return []

    # 🔒 Hard-enforced learning query
    strict_query = f"{query} data structures algorithms course"

    params = {
        "part": "snippet",
        "q": strict_query,
        "type": "video",
        "videoCategoryId": "27",  # Education
        "maxResults": min(max_results, 50),
        "key": YOUTUBE_API_KEY,
        "relevanceLanguage": "en",
        "safeSearch": "strict",
        "order": "relevance",
    }

    res = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
    res.raise_for_status()

    results = []
    for item in res.json().get("items", []):
        snippet = item["snippet"]
        video_id = item["id"].get("videoId")

        if not video_id:
            continue

        title = snippet["title"].lower()

        # 🚨 HARD FILTER (NO DSA → NO RESULT)
        if query.lower() not in title and "data structure" not in title:
            continue

        results.append({
            "platform": "YouTube",
            "title": snippet["title"],
            "creator": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "type": "video",
        })

    return results

# =========================================================
# 🔹 UDEMY (REDIRECT)
# =========================================================
def fetch_udemy_courses(skill: str) -> List[Dict]:
    q = skill.replace(" ", "+")
    return [{
        "platform": "Udemy",
        "title": f"{skill} Courses on Udemy",
        "creator": "Udemy Instructors",
        "thumbnail": "https://img-c.udemycdn.com/course/750x422/default.jpg",
        "url": f"https://www.udemy.com/courses/search/?q={q}",
        "type": "redirect",
    }]


# =========================================================
# 🔹 COURSERA (REDIRECT)
# =========================================================
def fetch_coursera_courses(skill: str) -> List[Dict]:
    q = skill.replace(" ", "+")
    return [{
        "platform": "Coursera",
        "title": f"{skill} Programs on Coursera",
        "creator": "Top Universities",
        "thumbnail": "https://d3njjcbhbojbot.cloudfront.net/web/images/favicons/android-icon-192x192.png",
        "url": f"https://www.coursera.org/search?query={q}",
        "type": "redirect",
    }]


# =========================================================
# 🔹 AGGREGATOR (USES ALL ABOVE)
# =========================================================
def fetch_courses_for_skill(skill: str) -> List[Dict]:
    courses = []

    # YouTube (strict)
    courses.extend(fetch_youtube_videos(skill, 30))

    # Free platforms (exact match)
    courses.extend(get_freecodecamp_courses(skill))

    # Legal redirects (exact keyword)
    courses.extend(fetch_udemy_courses(skill))
    courses.extend(fetch_coursera_courses(skill))

    return courses


# =========================================================
# 🔹 ENRICH
# =========================================================
def enrich_courses(skill: str, courses: List[Dict]) -> List[Dict]:
    for c in courses:
        c["skill"] = skill
        c["cta"] = "Start Learning"
    return courses
