from datetime import date, datetime

def render_registration(registration):

    if not registration.get("enabled"):
        return ""

    closing_date = registration.get("closing_date")
    url = registration.get("url")

    if not closing_date or not url:
        return ""

    if isinstance(closing_date, date):
        formatted_date = closing_date.strftime("%-d %B %Y")

    else:
        closing_date = datetime.strptime(
            str(closing_date),
            "%Y-%m-%d",
        )

        formatted_date = closing_date.strftime("%-d %B %Y")

    return f"""
<div class="course-registration">

<div class="course-registration-content">

<div class="course-registration-title">Registration is open</div>

<div class="course-registration-date">Register before {formatted_date}.</div>

</div>

<a
    class="course-registration-button"
    href="{url}"> Register for this course → </a></div>
""".strip()