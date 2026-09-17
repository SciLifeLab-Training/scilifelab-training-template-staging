def render_navbar_meta(course):

    title = course["title"]

    return f"""
<h1>{title}</h1>
""".strip()


def render_navbar_links(website, available_pages):

    links = [
        ("Overview", "index.qmd"),
        ("Course Content", "content/index.qmd"),
        ("Syllabus", "syllabus.qmd"),
        ("Team", "team.qmd"),
    ]

    optional_pages = [
        ("Schedule", "schedule.qmd", "schedule"),
        ("Practical info", "practicalinfo.qmd", "practical"),
        ("Precourse", "precourse.qmd", "precourse"),
        ("FAQ", "faq.qmd", "faq"),
        ("Resources", "resources.qmd", "resources"),
    ]

    for title, page, page_id in optional_pages:

        if page_id in available_pages:
            links.append((title, page))

    html = []

    for title, page in links:

        html.append(
            f'<a class="course-navbar-link" '
            f'href="{page}" '
            f'data-page="{page}">'
            f'{title}'
            '</a>'
        )

    return "\n".join(html)