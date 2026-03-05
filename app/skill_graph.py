SKILL_GRAPH = {

    "Python": ["FastAPI", "Flask", "Django", "Machine Learning"],
    "JavaScript": ["React", "Node.js", "Next.js"],
    "React": ["Redux", "Frontend Architecture"],
    "SQL": ["Database Design", "PostgreSQL"],
    "Machine Learning": ["Deep Learning", "Data Science"],

    "DSA": ["System Design", "Algorithms"],
    "System Design": ["Distributed Systems", "Scalability"]

}


def build_skill_graph(user_skills):

    graph = {}

    for skill in user_skills:

        related = SKILL_GRAPH.get(skill, [])

        graph[skill] = {
            "related_skills": related
        }

    return graph

def detect_skill_gaps(user_skills):

    missing = []

    for skill in user_skills:

        related = SKILL_GRAPH.get(skill, [])

        for r in related:
            if r not in user_skills:
                missing.append(r)

    return list(set(missing))