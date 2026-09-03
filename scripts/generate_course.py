#!/usr/bin/env python3
"""Generate Quarto partials for a SciLifeLab course instance."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
GENERATED_DIR = ROOT / "_generated"

COURSE_FILE = DATA_DIR / "course.yml"
SCHEDULE_FILE = DATA_DIR / "schedule.yml"
TEAM_FILE = DATA_DIR / "team.yml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class ValidationError(ValueError):
    """Raised when course data is missing or invalid."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and require a top-level mapping."""
    if not path.exists():
        raise ValidationError(f"Required file not found: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValidationError(
            f"{path.relative_to(ROOT)} must contain a top-level mapping."
        )

    return data


def require_string(data: dict[str, Any], key: str, context: str) -> str:
    """Get a required non-empty string."""
    value = data.get(key)

    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context}.{key} must be a non-empty string.")

    return value.strip()


def format_date(date_string: str) -> str:
    """Convert YYYY-MM-DD to e.g. 12 May 2026."""
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError(
            f"Invalid date {date_string!r}. Use YYYY-MM-DD."
        ) from exc

    return f"{date.day} {date.strftime('%B %Y')}"


def format_date_range(start_string: str, end_string: str) -> str:
    """Format a course date range."""
    try:
        start = datetime.strptime(start_string, "%Y-%m-%d")
        end = datetime.strptime(end_string, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Course dates must use YYYY-MM-DD.") from exc

    if end < start:
        raise ValidationError("course.end_date cannot be before course.start_date.")

    if start.year == end.year and start.month == end.month:
        return f"{start.day}–{end.day} {start.strftime('%B %Y')}"

    if start.year == end.year:
        return (
            f"{start.day} {start.strftime('%B')}–"
            f"{end.day} {end.strftime('%B %Y')}"
        )

    return f"{format_date(start_string)}–{format_date(end_string)}"


def format_schedule_date(date_string: str) -> str:
    """Format YYYY-MM-DD as e.g. Tue, May 12."""
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError(
            f"Invalid date {date_string!r}. Use YYYY-MM-DD."
        ) from exc

    return f"{date.strftime('%a')}, {date.strftime('%b')} {date.day}"


def write_partial(filename: str, content: str) -> None:
    """Write a generated Quarto partial."""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    path = GENERATED_DIR / filename
    path.write_text(content.strip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_course(data: dict[str, Any]) -> dict[str, Any]:
    course = data.get("course")

    if not isinstance(course, dict):
        raise ValidationError("course.yml must contain a 'course' mapping.")

    title = require_string(course, "title", "course")
    start_date = require_string(course, "start_date", "course")
    end_date = require_string(course, "end_date", "course")
    location = require_string(course, "location", "course")

    # Validate dates now so errors appear before rendering.
    format_date_range(start_date, end_date)

    welcome = course.get("welcome", "")
    if not isinstance(welcome, str):
        raise ValidationError("course.welcome must be text.")

    announcements = data.get("announcements", [])

    if announcements is None:
        announcements = []

    if not isinstance(announcements, list):
        raise ValidationError("announcements must be a list.")

    return {
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "location": location,
        "timezone": course.get("timezone", "Europe/Stockholm"),
        "welcome": welcome.strip(),
        "announcements": announcements,
    }


def validate_schedule(data: dict[str, Any]) -> list[dict[str, Any]]:
    days = data.get("days")

    if not isinstance(days, list):
        raise ValidationError("schedule.yml must contain a 'days' list.")

    for day_index, day in enumerate(days):
        context = f"days[{day_index}]"

        if not isinstance(day, dict):
            raise ValidationError(f"{context} must be a mapping.")

        require_string(day, "date", context)
        require_string(day, "label", context)

        sessions = day.get("sessions", [])

        if not isinstance(sessions, list):
            raise ValidationError(f"{context}.sessions must be a list.")

        for session_index, session in enumerate(sessions):
            session_context = f"{context}.sessions[{session_index}]"

            if not isinstance(session, dict):
                raise ValidationError(f"{session_context} must be a mapping.")

            require_string(session, "start", session_context)
            require_string(session, "end", session_context)
            require_string(session, "title", session_context)
            require_string(session, "type", session_context)

    return days


def validate_team(data: dict[str, Any]) -> list[dict[str, Any]]:
    team = data.get("team", [])

    if not isinstance(team, list):
        raise ValidationError("team.yml must contain a 'team' list.")

    for index, member in enumerate(team):
        context = f"team[{index}]"

        if not isinstance(member, dict):
            raise ValidationError(f"{context} must be a mapping.")

        require_string(member, "name", context)
        require_string(member, "role", context)

    return team


# ---------------------------------------------------------------------------
# Homepage partials
# ---------------------------------------------------------------------------

def render_course_header(course: dict[str, Any]) -> str:
    dates = format_date_range(course["start_date"], course["end_date"])

    return f"""
::: {{.course-header}}

# {course["title"]}

::: {{.course-meta}}
<span class="course-meta__item">{dates}</span>
<span class="course-meta__separator">•</span>
<span class="course-meta__item">{course["location"]}</span>
:::

:::
"""


def render_welcome(course: dict[str, Any]) -> str:
    if not course["welcome"]:
        return ""

    return course["welcome"]


def render_next_up(days: list[dict[str, Any]]) -> str:
    """
    First implementation: show the first scheduled session.

    Later this will become date/time aware and select the actual
    upcoming session.
    """
    first_day = None
    first_session = None

    for day in days:
        sessions = day.get("sessions", [])

        if sessions:
            first_day = day
            first_session = sessions[0]
            break

    if first_day is None or first_session is None:
        return """
::: {.next-session-empty}
No sessions have been added to the schedule yet.
:::
"""

    date = datetime.strptime(first_day["date"], "%Y-%m-%d")
    day_name = date.strftime("%A")
    month = date.strftime("%b").upper()

    instructor = first_session.get("instructor", "")
    location = first_session.get("location", "")

    details = []

    if instructor:
        details.append(instructor)

    if location:
        details.append(location)

    details_text = "\n\n".join(details)

    return f"""
::: {{.section-label}}
NEXT UP
:::

::: {{.next-session}}

::: {{.next-session-date}}
<span>{day_name.upper()}</span>
<strong>{date.day}</strong>
<span>{month}</span>
:::

::: {{.next-session-content}}
<span class="session-time">{first_session["start"]} – {first_session["end"]}</span>
<span class="session-type session-type--{first_session["type"]}">{first_session["type"].upper()}</span>

### {first_session["title"]}

{details_text}
:::

::: {{.next-session-action}}
[Full schedule →](schedule.qmd)
:::

:::
"""


def render_course_links() -> str:
    return """
::: {.section-label}
COURSE LINKS
:::

::: {.course-links}

::: {.course-link}
::: {.course-link-content}
### [Schedule](schedule.qmd)

Full course programme

[View schedule →](schedule.qmd)
:::
:::

::: {.course-link}
::: {.course-link-content}
### [Course content](content/index.qmd)

Slides, exercises and resources

[Browse content →](content/index.qmd)
:::
:::

::: {.course-link}
::: {.course-link-content}
### [Assignments](assignments/index.qmd)

Tasks and submission information

[View assignments →](assignments/index.qmd)
:::
:::

::: {.course-link}
::: {.course-link-content}
### [Practical information](practical.qmd)

Location, travel and contact information

[Practical information →](practical.qmd)
:::
:::

:::
"""


def render_announcements(course: dict[str, Any]) -> str:
    announcements = course["announcements"]

    if not announcements:
        return ""

    items = []

    for index, announcement in enumerate(announcements):
        context = f"announcements[{index}]"

        if not isinstance(announcement, dict):
            raise ValidationError(f"{context} must be a mapping.")

        date_string = require_string(announcement, "date", context)
        title = require_string(announcement, "title", context)

        text = announcement.get("text", "")
        if not isinstance(text, str):
            raise ValidationError(f"{context}.text must be text.")

        date = datetime.strptime(date_string, "%Y-%m-%d")
        display_date = f"{date.day} {date.strftime('%b')}"

        items.append(
            f"""
::: {{.announcement}}
::: {{.announcement-date}}
{display_date}
:::

::: {{.announcement-content}}
**{title}**

{text}
:::
:::
"""
        )

    return """
::: {.section-label}
COURSE ANNOUNCEMENTS
:::

::: {.announcements}
""" + "\n".join(items) + """
:::
"""


def render_team(team: list[dict[str, Any]]) -> str:
    if not team:
        return ""

    members = []

    for member in team:
        affiliation = member.get("affiliation", "")
        image = member.get("image", "")

        if image:
            portrait = (
                f'<img src="{image}" alt="" class="course-team__photo">'
            )
        else:
            # Deliberately simple fallback for now.
            portrait = '<div class="course-team__placeholder">●</div>'

        affiliation_markup = (
            f'<span class="course-team__affiliation">{affiliation}</span>'
            if affiliation
            else ""
        )

        members.append(
            f"""
::: {{.course-team__member}}
{portrait}

::: {{.course-team__details}}
**{member["name"]}**

<span class="course-team__role">{member["role"]}</span>
{affiliation_markup}
:::
:::
"""
        )

    return """
::: {.section-label}
COURSE TEAM
:::

::: {.course-team}
""" + "\n".join(members) + """
:::
"""


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

def render_schedule(
    course: dict[str, Any],
    days: list[dict[str, Any]],
) -> str:
    """Render the complete course schedule."""

    if not days:
        return """
# Schedule

No schedule has been added yet.
"""

    date_range = format_date_range(
        course["start_date"],
        course["end_date"],
    )

    # ---------------------------------------------------------
    # Day navigation
    # ---------------------------------------------------------

    day_navigation = []

    for index, day in enumerate(days):
        date = datetime.strptime(day["date"], "%Y-%m-%d")
        day_id = f"day-{index + 1}"

        active_class = " schedule-day-link--active" if index == 0 else ""

        day_navigation.append(
            f"""
<button
  type="button"
  class="schedule-day-link{active_class}"
  data-day="{day_id}"
>
  <strong>{day["label"]}</strong>
  <span>{format_schedule_date(day["date"])}</span>
</button>
"""
        )

    # ---------------------------------------------------------
    # Individual days
    # ---------------------------------------------------------

    day_sections = []

    for day_index, day in enumerate(days):
        date = datetime.strptime(day["date"], "%Y-%m-%d")
        day_id = f"day-{day_index + 1}"

        sessions_markup = []

        for session in day.get("sessions", []):
            session_type = session["type"].lower()

            instructor = session.get("instructor", "")
            location = session.get("location", "")
            materials = session.get("materials", [])

            meta_parts = []

            if instructor:
                meta_parts.append(
                    f'<span class="schedule-session__instructor">'
                    f'{instructor}'
                    f'</span>'
                )

            if location:
                meta_parts.append(
                    f'<span class="schedule-session__location">'
                    f'{location}'
                    f'</span>'
                )

            meta_markup = "\n".join(meta_parts)

            material_links = []

            if materials:
                if not isinstance(materials, list):
                    raise ValidationError(
                        f"Materials for session {session['title']!r} "
                        "must be a list."
                    )

                for material in materials:
                    if not isinstance(material, dict):
                        raise ValidationError(
                            f"Each material for session "
                            f"{session['title']!r} must be a mapping."
                        )

                    label = material.get("label")
                    url = material.get("url")

                    if not isinstance(label, str) or not label.strip():
                        raise ValidationError(
                            f"A material for session "
                            f"{session['title']!r} is missing a label."
                        )

                    if not isinstance(url, str) or not url.strip():
                        raise ValidationError(
                            f"A material for session "
                            f"{session['title']!r} is missing a URL."
                        )

                    material_links.append(
                        f'[{label}]({url})'
                        '{.schedule-material}'
                    )

            materials_markup = " ".join(material_links)

            sessions_markup.append(
                f"""
::: {{.schedule-session .schedule-session--{session_type}}}

::: {{.schedule-session__time}}
{session["start"]} – {session["end"]}
:::

::: {{.schedule-session__marker}}
:::

::: {{.schedule-session__content}}

<span class="session-type session-type--{session_type}">{session_type.upper()}</span>

### {session["title"]}

::: {{.schedule-session__meta}}
{meta_markup}
:::

:::

::: {{.schedule-session__materials}}
{materials_markup}
:::

:::
"""
            )

        day_sections.append(
            f"""
::: {{#{day_id} .schedule-day}}

## {day["label"]} – {date.strftime("%A")}, {date.strftime("%B")} {date.day}

::: {{.schedule-timeline}}
{"".join(sessions_markup)}
:::

:::
"""
        )

    # ---------------------------------------------------------
    # Complete schedule
    # ---------------------------------------------------------

    return f"""
::: {{.schedule-header}}

# Schedule

::: {{.schedule-header__meta}}
{date_range} <span class="schedule-meta-separator">•</span> {course["location"]}
:::

:::

::: {{.schedule-layout}}

::: {{.schedule-sidebar}}

{"".join(day_navigation)}

::: {{.schedule-time-note}}
**All times in CEST**

Times are subject to change.
:::

:::

::: {{.schedule-main}}
{"".join(day_sections)}
:::

:::
"""


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

def generate() -> None:
    course_data = load_yaml(COURSE_FILE)
    schedule_data = load_yaml(SCHEDULE_FILE)
    team_data = load_yaml(TEAM_FILE)

    course = validate_course(course_data)
    days = validate_schedule(schedule_data)
    team = validate_team(team_data)

    write_partial("course-header.qmd", render_course_header(course))
    write_partial("welcome.qmd", render_welcome(course))
    write_partial("next-up.qmd", render_next_up(days))
    write_partial("course-links.qmd", render_course_links())
    write_partial("announcements.qmd", render_announcements(course))
    write_partial("course-team.qmd", render_team(team))
    write_partial("schedule.qmd", render_schedule(course, days))

    print("Generated course partials:")
    print("  _generated/course-header.qmd")
    print("  _generated/welcome.qmd")
    print("  _generated/next-up.qmd")
    print("  _generated/course-links.qmd")
    print("  _generated/announcements.qmd")
    print("  _generated/course-team.qmd")
    print("  _generated/schedule.qmd")


def main() -> None:
    try:
        generate()
    except ValidationError as exc:
        print(f"ValidationError: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()