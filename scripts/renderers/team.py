def render_team(team):

    members = team.get("members") or []

    # Show up to two training leads on the homepage.
    training_leads = [
        person
        for person in members
        if "Training lead" in person.get("roles", [])
    ]

    preview = training_leads[:2]

    rendered_members = []

    for person in preview:

        role = ", ".join(person.get("roles", []))

        image = person.get("image", "")
        name = person.get("name", "")
        affiliation = person.get("affiliation", "")

        if image:

            image_html = f"""
<img
    class="course-team-photo"
    src="{image}"
    alt="{name}">
""".strip()

        else:

            image_html = ""

        rendered_members.append(
            f"""
<div class="course-team-member">

{image_html}

<div class="course-team-details">

<div class="course-team-name">
{name}
</div>

<div class="course-team-role">
{role}
</div>

<div class="course-team-affiliation">
{affiliation}
</div>

</div>

</div>
""".strip()
        )

    if not rendered_members:
        return ""

    return f"""
::: {{.course-team}}

<div class="course-team-content">

<div class="course-section-label">

TEAM

</div>

{"".join(rendered_members)}

<a class="course-team-link" href="team.qmd">

View full team →

</a>

</div>

:::
""".strip()