def render_navbar_meta(course):

    title = course["title"]

    return f"""
<div class="course-navbar-title">
<h1>{title}</h1>
</div>
""".strip()


def render_navbar_links(website, current_page):

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

        classes = "course-navbar-link"

        if page == current_page:
            classes += " course-navbar-link-active"

        html.append(
            f'<a class="{classes}" href="{page}">{title}</a>'
        )

    return "\n".join(html)