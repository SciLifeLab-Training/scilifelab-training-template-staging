from utils import format_date


def render_welcome(course):

    title = course["title"]

    start = course.get("start_date")
    end = course.get("end_date")
    location = course.get("location")

    meta = []

    if start and end:
        meta.append(f"""
<span class="course-welcome-item">
<i class="bi bi-calendar2-event"></i>
{format_date(start)} – {format_date(end)}
</span>
""")

    elif start:
        meta.append(f"""
<span class="course-welcome-item">
<i class="bi bi-calendar2-event"></i>
{format_date(start)}
</span>
""")

    elif end:
        meta.append(f"""
<span class="course-welcome-item">
<i class="bi bi-calendar2-event"></i>
{format_date(end)}
</span>
""")

    if location:
        meta.append(f"""
<span class="course-welcome-item">
<i class="bi bi-geo-alt"></i>
{location}
</span>
""")

    meta_html = ""

    if meta:
        meta_html = f"""
<div class="course-welcome-meta">
{''.join(meta)}
</div>
"""

    return f"""
# {title}

{meta_html}
""".strip()