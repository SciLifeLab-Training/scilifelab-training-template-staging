def render_welcome(course):

    title = course["title"]
    subtitle = course.get("subtitle")
    start = course.get("start_date")
    end = course.get("end_date")
    location = course.get("location")

    lines = [
        f"# {title}",
    ]

    if subtitle:
        lines.append("")
        lines.append(f"## {subtitle}")

    if start or end:
        lines.append("")
        lines.append(f"**Dates:** {start} – {end}")

    if location:
        lines.append(f"**Location:** {location}")

    return "\n".join(lines) + "\n"