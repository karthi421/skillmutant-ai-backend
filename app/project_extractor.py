import re

def extract_projects(text: str):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    PROJECT_HEADERS = [
        "projects",
        "academic projects",
        "personal projects",
        "key projects"
    ]

    STOP_HEADERS = [
        "experience",
        "education",
        "skills",
        "certifications",
        "summary",
        "achievements",
        "languages",
        "interests"
    ]

    # 1️⃣ Locate projects section
    start = None
    for i, line in enumerate(lines):
        if line.lower() in PROJECT_HEADERS:
            start = i + 1
            break

    if start is None:
        return []

    # 2️⃣ Find end of section
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].lower() in STOP_HEADERS:
            end = i
            break

    section = lines[start:end]

    projects = []
    current_project = None
    description_buffer = []

    for line in section:
        # 3️⃣ Heuristic: project title line
        is_title = (
            len(line) < 80 and
            not line.startswith(("-", "•")) and
            any(word.isalpha() for word in line.split())
        )

        if is_title:
            # Save previous project
            if current_project:
                projects.append(
                    f"{current_project}: " + " ".join(description_buffer)
                )

            current_project = line
            description_buffer = []

        else:
            description_buffer.append(line)

    # Save last project
    if current_project:
        projects.append(
            f"{current_project}: " + " ".join(description_buffer)
        )

    return projects
