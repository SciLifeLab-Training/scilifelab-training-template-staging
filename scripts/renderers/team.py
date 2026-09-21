def render_team(team):

    # Show up to two training leads on the homepage.
    training_leads = [
        person
        for person in team
        if "Training lead" in person.get("roles", [])
    ]

    preview = training_leads[:2]

    members = []

    for person in preview:

        role = ", ".join(person.get("roles", []))

        members.append(
            f"""
<div class="course-team-member">

<img
    class="course-team-photo"
    src="{person["image"]}"
    alt="{person["name"]}">

<div class="course-team-details">

<div class="course-team-name">
{person["name"]}
</div>

<div class="course-team-role">
{role}
</div>

<div class="course-team-affiliation">
{person["affiliation"]}
</div>

</div>

</div>
""".strip()
        )

    if not members:
        return ""

    return f"""
::: {{.course-team}}

<div class="course-team-content">

<div class="course-section-label">

TEAM

</div>

{"".join(members)}

<a class="course-team-link" href="team.qmd">

View full team →

</a>

</div>

:::
""".strip()