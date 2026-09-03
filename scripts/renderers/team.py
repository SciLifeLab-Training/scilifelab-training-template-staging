def render_team(team):

    # Only show the first two team members on the homepage.
    preview = team[:2]

    members = []

    for person in preview:

        role = ", ".join(person["roles"])

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
"""
        )

    return "\n".join(members).strip()