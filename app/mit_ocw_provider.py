def get_mit_ocw_courses(skill: str):
    base_url = "https://ocw.mit.edu/search/"

    return [
        {
            "platform": "MIT OpenCourseWare",
            "title": f"{skill.title()} – MIT University Courses",
            "thumbnail": "https://ocw.mit.edu/images/ocw-logo.png",
            "url": f"{base_url}?q={skill.replace(' ', '+')}",
            "type": "redirect"
        }
    ]
