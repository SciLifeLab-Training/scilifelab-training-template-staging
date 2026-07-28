def render_navbar(course, website):

    title = course["title"]

    return f"""
# Navbar

Course: **{title}**
""".strip() + "\n"