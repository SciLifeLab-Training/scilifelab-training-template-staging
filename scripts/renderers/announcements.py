from datetime import date


def render_announcements(announcements):

    if not announcements:

        return """
::: {.course-announcements}

<div class="course-announcements-content">

<div class="course-section-label">

COURSE ANNOUNCEMENTS

</div>

<div class="course-announcement-empty">

No active announcements.

</div>

</div>

:::
""".strip()

    # Sort newest first.
    announcements = sorted(
        announcements,
        key=lambda announcement: announcement["date"],
        reverse=True,
    )

    # Show only the two most recent announcements.
    announcements = announcements[:2]

    cards = []

    for announcement in announcements:

        announcement_date = announcement["date"]

        # Format YYYY-MM-DD as "10 May".
        if isinstance(announcement_date, date):

            formatted_date = announcement_date.strftime("%-d %B")

        else:

            formatted_date = str(announcement_date)

        cards.append(
            f"""
<div class="course-announcement">

<div class="course-announcement-date">

{formatted_date}

</div>

<h3 class="course-announcement-title">

{announcement["title"]}

</h3>

{announcement["text"]}

</div>
""".strip()
        )

    return f"""
::: {{.course-announcements}}

<div class="course-announcements-content">

<div class="course-section-label">

COURSE ANNOUNCEMENTS

</div>

{"".join(cards)}

<a class="course-announcements-link" href="announcements.qmd">

View all announcements →

</a>

</div>

:::
""".strip()