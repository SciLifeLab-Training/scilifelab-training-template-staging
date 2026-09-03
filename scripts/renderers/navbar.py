def render_navbar_meta(course):

    title = course["title"]

    return f"""
<h1>{title}</h1>
""".strip()


def render_navbar_links(website):

    links = [
        ("Overview", "index.qmd"),
        ("Schedule", "schedule.qmd"),
        ("Course Content", "content/index.qmd"),
        ("Syllabus", "syllabus.qmd"),
        ("Course Team", "team.qmd"),
        ("Practical info", "practicalinfo.qmd"),
    ]

    html = []

    for title, page in links:

        html.append(
            f'<a class="course-navbar-link" href="{page}" data-page="{page}">{title}</a>'
        )

    return "\n".join(html)