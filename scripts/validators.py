def validate_course(course):

    required = [
        "title",
        "description",
        "mode",
        "language",
        "target_audience",
        "learning_outcomes",
        "organizers",
        "contact",
    ]

    for field in required:
        if not course.get(field):
            raise ValueError(f"course.{field} is required")

    if not isinstance(course["learning_outcomes"], list):
        raise ValueError("course.learning_outcomes must be a list")

    if not course["learning_outcomes"]:
        raise ValueError(
            "course.learning_outcomes must contain at least one item"
        )

    if not isinstance(course["organizers"], list):
        raise ValueError("course.organizers must be a list")

    if not course["organizers"]:
        raise ValueError(
            "course.organizers must contain at least one item"
        )

    if not isinstance(course["contact"], dict):
        raise ValueError("course.contact must be a mapping")

    if not course["contact"].get("email"):
        raise ValueError("course.contact.email is required")

    return course

def validate_website(website):

    pages = website.get("pages", {})

    required_pages = [
        "content",
        "syllabus",
    ]

    for page in required_pages:

        if page not in pages:
            raise ValueError(
                f"Required page '{page}' is missing"
            )

    return website


def validate_schedule(events):

    if not isinstance(events, list):
        raise ValueError("schedule.yml must contain an 'events' list")

    return events


def validate_team(team):

    if not isinstance(team, dict):
        raise ValueError("team.yml must contain a 'team' mapping")

    members = team.get("members") or []

    if not isinstance(members, list):
        raise ValueError("team.members must be a list")

    required = [
        "name",
        "roles",
        "affiliation",
    ]

    for member in members:

        member_name = member.get("name", "<unnamed member>")

        for field in required:

            if not member.get(field):
                raise ValueError(
                    f"Team member '{member_name}' is missing '{field}'"
                )

    return team