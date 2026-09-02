def validate_course(course):

    required = [
        "title",
    ]

    for field in required:
        if not course.get(field):
            raise ValueError(f"course.{field} is required")

    return course


def validate_website(website):

    quick_links = website.get("homepage", {}).get("quick_links", [])

    if len(quick_links) > 4:
        raise ValueError(
            "homepage.quick_links may contain at most four pages"
        )

    pages = website.get("pages", {})

    for page in quick_links:
        if page not in pages:
            raise ValueError(
                f"Unknown homepage quick link '{page}'"
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