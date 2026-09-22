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
        raise ValueError(
            "team.yml must contain a 'team' mapping"
        )

    members = team.get("members")

    if not isinstance(members, list):
        raise ValueError(
            "team.members must be a list"
        )

    if not members:
        raise ValueError(
            "team.members must contain at least one member"
        )

    allowed_roles = {
        "Training lead",
        "Instructor",
        "Contributor",
    }

    course_contact_found = False

    required = [
        "name",
        "roles",
        "affiliation",
    ]

    for member in members:

        member_name = member.get(
            "name",
            "<unnamed member>"
        )

        for field in required:

            if not member.get(field):
                raise ValueError(
                    f"Team member '{member_name}' "
                    f"is missing '{field}'"
                )

        if not isinstance(member["roles"], list):
            raise ValueError(
                f"Team member '{member_name}' "
                "roles must be a list"
            )

        if not member["roles"]:
            raise ValueError(
                f"Team member '{member_name}' "
                "must have at least one role"
            )

        invalid_roles = set(member["roles"]) - allowed_roles

        if invalid_roles:
            invalid = ", ".join(sorted(invalid_roles))

            raise ValueError(
                f"Team member '{member_name}' "
                f"has invalid role(s): {invalid}. "
                "Allowed roles are: Training lead, "
                "Instructor, Contributor"
            )

        if member.get("course_contact") is True:

            if not member.get("email"):
                raise ValueError(
                    f"Team member '{member_name}' "
                    "is marked as course_contact but "
                    "has no email address"
                )

            course_contact_found = True

    if not course_contact_found:
        raise ValueError(
            "At least one team member must have "
            "'course_contact: true' and an email address"
        )

    return team