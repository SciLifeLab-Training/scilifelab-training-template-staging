def validate_course(course):

    required = [
        "title",
        "start_date",
        "end_date",
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