from collections import OrderedDict

# Month abbreviations used throughout the course website.
MONTHS = [
    "JAN", "FEB", "MAR", "APR",
    "MAY", "JUN", "JUL", "AUG",
    "SEP", "OCT", "NOV", "DEC",
]


def render_schedule(events):

    if not events:
        return ""

    # Sort events chronologically.
    events = sorted(events, key=lambda event: event["start"])

    # Group events by course day while preserving order.
    grouped = OrderedDict()

    for event in events:

        group = event["group"]

        if group not in grouped:
            grouped[group] = []

        grouped[group].append(event)

    #
    # Sidebar
    #

    sidebar = []

    #
    # Timeline
    #

    timeline = []

    for group, day_events in grouped.items():

        first = day_events[0]["start"]

        weekday = first.strftime("%A")
        day = first.day
        month = MONTHS[first.month - 1].title()

        day_id = group.lower().replace(" ", "-")

        #
        # Sidebar entry
        #

        sidebar.append(
    f"""
<div class="course-schedule-day-link">

<a href="#{day_id}">

<div class="course-schedule-day-name">
{group}
</div>

<div class="course-schedule-day-date">
{weekday}, {month} {day}
</div>

</a>

</div>
"""
)

        #
        # Events
        #

        rows = []

        for event in day_events:

            start = event["start"]
            end = event["end"]

            time = f"{start:%H:%M}–{end:%H:%M}"

            event_type = event["type"].replace("_", " ").title()
            event_class = event["type"].lower()

            people = ", ".join(event["people"])

            speaker_html = ""

            if people:
                speaker_html = f"""
<div class="course-schedule-speaker">
{people}
</div>
"""

            location_html = ""

            if event["location"]:
                location_html = f"""
<div class="course-schedule-location">
<i class="bi bi-geo-alt"></i>
{event["location"]}
</div>
"""

            rows.append(
                f"""
<div class="course-schedule-event">

<div class="course-schedule-time">
{time}
</div>

<div class="course-schedule-details">

<span class="course-schedule-type course-schedule-type-{event_class}">
{event_type}
</span>

<h3 class="course-schedule-title">
{event["title"]}
</h3>

{speaker_html}

</div>

<div class="course-schedule-location-column">

{location_html}

</div>

</div>
"""
            )

        timeline.append(
            f"""
<section
id="{day_id}"
class="course-schedule-day">

<h2 class="course-schedule-day-heading">
{group} – {weekday}, {month} {day}
</h2>

{''.join(rows)}

</section>
"""
        )

    return f"""
<div class="course-schedule">

<div class="course-schedule-sidebar">

{''.join(sidebar)}

</div>

<div class="course-schedule-timeline">

{''.join(timeline)}

</div>

</div>
""".strip()