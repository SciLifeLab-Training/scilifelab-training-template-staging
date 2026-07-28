from datetime import datetime


def format_date(date):

    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    return date.strftime("%d %b %Y")


def render_navbar_meta(course):

    title = course["title"]

    start = format_date(course["start_date"])
    end = format_date(course["end_date"])

    location = course["location"]

    return f"""
<h1 class="navbar-title">{title}</h1>

<p class="navbar-meta">
{start} – {end}
&nbsp;&nbsp;&bull;&nbsp;&nbsp;
{location}
</p>
""".strip()


def render_navbar_links(website):

    pages = website["pages"]

    links = [
        ("Overview", "index.qmd"),
    ]

    if pages.get("schedule"):
        links.append(("Schedule", "schedule.qmd"))

    if pages.get("practical"):
        links.append(("Practical info", "practical.qmd"))

    if pages.get("resources"):
        links.append(("Resources", "resources.qmd"))

    if pages.get("faq"):
        links.append(("FAQ", "faq.qmd"))

    if pages.get("team_page"):
        links.append(("Team", "team.qmd"))

    html = []

    for title, page in links:

        html.append(
            f'<a class="navbar-link" href="{page}">{title}</a>'
        )

    return "\n".join(html)