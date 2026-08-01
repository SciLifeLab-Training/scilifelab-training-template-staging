
# Month abbreviations used throughout the course website.
MONTHS = [
    "JAN", "FEB", "MAR", "APR",
    "MAY", "JUN", "JUL", "AUG",
    "SEP", "OCT", "NOV", "DEC",
]

def render_upcoming(events):

    if not events:
        return ""
    
    event = events[0]

    # Get the event start and end times.
    start = event["start"]
    end = event["end"]

    # Format date and time components.
    group = event["group"].upper()
    day = start.strftime("%d")
    month = MONTHS[start.month - 1]
    time = f"{start:%H:%M}–{end:%H:%M}"

    # Format event metadata.
    title = event["title"]
    event_type_class = event["type"].lower().replace("_", "-")
    event_type = event["type"].replace("_", " ").title()

    # Render speaker if available.
    speaker_html = ""
    if event["people"]:
        speaker = ", ".join(event["people"])
        speaker_html = (
            f'<div class="course-upcoming-speaker">'
            f'<i class="bi bi-person"></i>{speaker}'
            f'</div>'
        )

    # Render location if available.
    location_html = ""
    if event["location"]:
        location_html = (
            f'<div class="course-upcoming-location">'
            f'<i class="bi bi-geo-alt"></i>{event["location"]}'
            f'</div>'
        )

    return f"""
<div class="course-upcoming-card">

<div class="course-upcoming-day">
<div class="course-upcoming-weekday">{group}</div>
<div class="course-upcoming-date">{day}</div>
<div class="course-upcoming-month">{month}</div>
</div>

<div class="course-upcoming-details">

<div class="course-upcoming-top">
<span class="course-upcoming-time">{time}</span>
<span class="course-upcoming-type course-type-{event_type_class}">{event_type}</span></div>

<h3 class="course-upcoming-title">{title}</h3>

{speaker_html}

{location_html}

</div>

<div class="course-upcoming-status">
<div class="course-upcoming-countdown">Starts in 2 days</div>
<a class="course-upcoming-link" href="schedule.qmd">Full schedule →</a>
</div>

</div>
""".strip()