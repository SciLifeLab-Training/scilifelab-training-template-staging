def render_quick_links(website):
    """Render the homepage quick links section."""

    pages = website["pages"]
    quick_links = website["homepage"]["quick_links"]

    cards = []

    for key in quick_links:

        page = pages[key]

        cards.append(
            f"""
<div class="course-link-card">

<i class="bi bi-{page["icon"]} course-link-icon"></i>

<div class="course-link-content">

<h3>{page["title"]}</h3>

<p>{page["description"]}</p>

<a href="{page["href"]}">
View {page["title"].lower()} →
</a>

</div>

</div>
""".strip()
        )

    return (
        '<div class="course-links-grid">\n'
        + "\n".join(cards)
        + "\n</div>"
    )