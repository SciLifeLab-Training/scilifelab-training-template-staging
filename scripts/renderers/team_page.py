def render_team_page(team):

    role_sections = [
        (
            "Training leads",
            "Training leads are responsible for the overall development, coordination, and delivery of the training.",
            "Training lead",
            "course-team-grid-leads",
        ),
        (
            "Instructors",
            "Instructors teach, facilitate, or otherwise contribute directly to the educational activities.",
            "Instructor",
            "course-team-grid-members",
        ),
        (
            "Contributors",
            "Contributors provide expertise, content, materials, or other support to the training.",
            "Contributor",
            "course-team-grid-members",
        ),
    ]

    html = []

    html.append('<div class="course-team-page">')

    html.append('<header class="course-team-page-header">')
    html.append('<div class="course-team-page-label">Training team</div>')
    html.append('<h1>Meet the training team</h1>')
    html.append(
        '<p class="course-team-page-intro">'
        'This training is developed and delivered by a team of experts '
        'from SciLifeLab and partner organisations. Here you can find '
        'information about the training leads, instructors, and contributors.'
        '</p>'
    )
    html.append('</header>')

    for heading, description, role, grid_class in role_sections:

        members = [
            person
            for person in team
            if role in person.get("roles", [])
        ]

        if not members:
            continue

        html.append('<section class="course-team-section">')
        html.append(f'<h2>{heading}</h2>')
        html.append(
            f'<p class="course-team-section-description">{description}</p>'
        )

        html.append(f'<div class="{grid_class}">')

        for person in members:

            html.append('<article class="course-team-card">')

            if person.get("image"):
                html.append(
                    '<img '
                    'class="course-team-card-photo" '
                    f'src="{person["image"]}" '
                    f'alt="{person["name"]}">'
                )

            html.append('<div class="course-team-card-body">')

            html.append(
                f'<h3 class="course-team-card-name">'
                f'{person["name"]}'
                f'</h3>'
            )

            if person.get("job_title"):
                html.append(
                    f'<div class="course-team-card-job-title">'
                    f'{person["job_title"]}'
                    f'</div>'
                )

            if person.get("affiliation"):
                html.append(
                    f'<div class="course-team-card-affiliation">'
                    f'{person["affiliation"]}'
                    f'</div>'
                )

            links = []

            if person.get("email"):
                links.append(
                    f'<a href="mailto:{person["email"]}" '
                    'aria-label="Email" title="Email">'
                    '<i class="bi bi-envelope"></i>'
                    '</a>'
                )

            if person.get("orcid"):
                links.append(
                    f'<a href="{person["orcid"]}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="ORCID" title="ORCID">'
                    '<img '
                    'src="https://cdn.simpleicons.org/orcid" '
                    'alt="" '
                    'class="course-team-social-icon">'
                    '</a>'
                )

            if person.get("github"):
                links.append(
                    f'<a href="{person["github"]}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="GitHub" title="GitHub">'
                    '<i class="bi bi-github"></i>'
                    '</a>'
                )

            if person.get("linkedin"):
                links.append(
                    f'<a href="{person["linkedin"]}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="LinkedIn" title="LinkedIn">'
                    '<i class="bi bi-linkedin"></i>'
                    '</a>'
                )

            if person.get("website"):
                links.append(
                    f'<a href="{person["website"]}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="Website">'
                    '<i class="bi bi-globe2"></i>'
                    '</a>'
                )

            if links:
                html.append(
                    '<div class="course-team-card-links">'
                    + "\n".join(links)
                    + '</div>'
                )

            html.append('</div>')
            html.append('</article>')

        html.append('</div>')
        html.append('</section>')

    html.append('</div>')

    return "\n".join(html).strip()