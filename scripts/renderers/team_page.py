from html import escape


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

        html.append(f'<h2>{escape(heading)}</h2>')

        html.append(
            '<p class="course-team-section-description">'
            f'{escape(description)}'
            '</p>'
        )

        html.append(f'<div class="{grid_class}">')

        for person in members:

            name = escape(str(person.get("name", "")))
            job_title = escape(str(person.get("job_title", "")))
            affiliation = escape(str(person.get("affiliation", "")))
            bio = escape(str(person.get("bio", "")))
            email = person.get("email", "")
            image = person.get("image", "")

            html.append('<article class="course-team-card">')

            if image:
                html.append(
                    '<img '
                    'class="course-team-card-photo" '
                    f'src="{escape(image, quote=True)}" '
                    f'alt="{name}">'
                )

            html.append('<div class="course-team-card-body">')

            html.append(
                '<h3 class="course-team-card-name">'
                f'{name}'
                '</h3>'
            )

            if job_title:
                html.append(
                    '<div class="course-team-card-job-title">'
                    f'{job_title}'
                    '</div>'
                )

            if affiliation:
                html.append(
                    '<div class="course-team-card-affiliation">'
                    f'{affiliation}'
                    '</div>'
                )

            # Course contact
            if person.get("course_contact"):

                html.append(
                    '<div class="course-team-card-contact">'
                )

                html.append(
                    '<span class="course-team-contact-badge">'
                    '<i class="bi bi-envelope"></i>'
                    'Course contact'
                    '</span>'
                )

                if email:
                    html.append(
                        f'<a class="course-team-contact-email" '
                        f'href="mailto:{escape(email, quote=True)}">'
                        f'{escape(email)}'
                        '</a>'
                    )

                html.append('</div>')

            # Optional biography
            if bio:
                html.append(
                    '<p class="course-team-card-bio">'
                    f'{bio}'
                    '</p>'
                )

            # Profile links
            links = []

            if email:
                links.append(
                    f'<a href="mailto:{escape(email, quote=True)}" '
                    'aria-label="Email" title="Email">'
                    '<i class="bi bi-envelope"></i>'
                    '</a>'
                )

            if person.get("orcid"):
                orcid = escape(
                    str(person["orcid"]),
                    quote=True,
                )

                links.append(
                    f'<a href="{orcid}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="ORCID" title="ORCID">'
                    '<img '
                    'src="https://cdn.simpleicons.org/orcid" '
                    'alt="" '
                    'class="course-team-social-icon">'
                    '</a>'
                )

            if person.get("github"):
                github = escape(
                    str(person["github"]),
                    quote=True,
                )

                links.append(
                    f'<a href="{github}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="GitHub" title="GitHub">'
                    '<i class="bi bi-github"></i>'
                    '</a>'
                )

            if person.get("linkedin"):
                linkedin = escape(
                    str(person["linkedin"]),
                    quote=True,
                )

                links.append(
                    f'<a href="{linkedin}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="LinkedIn" title="LinkedIn">'
                    '<i class="bi bi-linkedin"></i>'
                    '</a>'
                )

            if person.get("website"):
                website = escape(
                    str(person["website"]),
                    quote=True,
                )

                links.append(
                    f'<a href="{website}" '
                    'target="_blank" rel="noopener" '
                    'aria-label="Website" title="Website">'
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