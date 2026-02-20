# app/freecodecamp_provider.py

def get_freecodecamp_courses(skill: str):
    """
    Virtual API for freeCodeCamp using official search URLs
    """

    base_url = "https://www.freecodecamp.org/search"

    return [
        {
            "platform": "freeCodeCamp",
            "title": f"{skill.title()} Courses on freeCodeCamp",
            "thumbnail": "https://www.freecodecamp.org/news/content/images/size/w200/2020/02/freecodecamp-logo.png",
            "url": f"{base_url}?q={skill.replace(' ', '+')}",
            "type": "redirect"
        }
    ]
