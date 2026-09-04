def validate_course(course):

    required = [
        "title",
        "description",
        "mode",
        "language",
        "target_audience",
        "learning_outcomes",
        "course_leaders",
        "organizers",
        "contact",
    ]

    for field in required:
        if not course.get(field):
            raise ValueError(f"course.{field} is required")

    if not isinstance(course["learning_outcomes"], list):
        raise ValueError("course.learning_outcomes must be a list")

    if not course["learning_outcomes"]:
        raise ValueError("course.learning_outcomes must contain at least one item")

    if not isinstance(course["course_leaders"], list):
        raise ValueError("course.course_leaders must be a list")

    if not course["course_leaders"]:
        raise ValueError("course.course_leaders must contain at least one person")

    for leader in course["course_leaders"]:

        name = leader.get("name", "<unnamed course leader>")

        if not leader.get("name"):
            raise ValueError(
                f"Course leader '{name}' is missing 'name'"
            )

    if not isinstance(course["organizers"], list):
        raise ValueError("course.organizers must be a list")

    if not course["organizers"]:
        raise ValueError("course.organizers must contain at least one item")

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

    if not isinstance(team, list):
        raise ValueError("team.yml must contain a 'team' list")

    required = [
        "name",
        "roles",
        "affiliation",
        "image",
    ]

    for member in team:

        member_name = member.get("name", "<unnamed member>")

        for field in required:

            if not member.get(field):
                raise ValueError(
                    f"Team member '{member_name}' is missing '{field}'"
                )

    return team