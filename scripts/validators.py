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
    return website

def validate_schedule(events):

    if not isinstance(events, list):
        raise ValueError("schedule.yml must contain an 'events' list")

    return events