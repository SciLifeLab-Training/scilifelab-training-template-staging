from utils import format_date


def render_welcome(course):

    title = course["title"]

    start = format_date(course["start_date"])
    end = format_date(course["end_date"])

    location = course["location"]

    return f"""
# {title}

<div class="course-welcome-meta">

<span class="course-welcome-item">
<i class="bi bi-calendar2-event"></i>
{start} – {end}
</span>

<span class="course-welcome-item">
<i class="bi bi-geo-alt"></i>
{location}
</span>

</div>
""".strip()