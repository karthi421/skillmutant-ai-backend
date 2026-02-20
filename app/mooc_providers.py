def get_coursera_courses(skill: str):
    return [
        {
            "platform": "Coursera",
            "title": f"{skill.title()} Courses (Audit Free)",
            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg",
            "url": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}",
            "type": "redirect"
        }
    ]


def get_edx_courses(skill: str):
    return [
        {
            "platform": "edX",
            "title": f"{skill.title()} Courses on edX",
            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/8/8f/EdX_Logo.svg",
            "url": f"https://www.edx.org/search?q={skill.replace(' ', '+')}",
            "type": "redirect"
        }
    ]
