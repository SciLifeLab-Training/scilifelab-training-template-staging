#!/usr/bin/env python3

from pathlib import Path
import shutil

from loaders import (
    load_course,
    load_website,
    load_content,
    load_schedule,
    load_team,
    load_announcements,
    load_practical_info,
    load_faq,
)

from content import load_content_sections

from validators import (
    validate_course,
    validate_website,
    validate_schedule,
    validate_team,
)

from writer import write_partial

from renderers.welcome import render_welcome
from renderers.navbar import (
    render_navbar_meta,
    render_navbar_links,
)
from renderers.registration import render_registration
from renderers.upcoming import render_upcoming
from renderers.quick_links import render_quick_links
from renderers.announcements import render_announcements
from renderers.team import render_team
from renderers.team_page import render_team_page
from renderers.content import (
    render_content_overview,
    render_content_navbar,
    render_content_footer,
)
from renderers.schedule import render_schedule
from renderers.syllabus import render_syllabus
from renderers.practicalinfo import render_practical_info
from renderers.faq import render_faq


ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "_generated"


def main():
    print("Running course renderer...")

    # Start every render with a clean generated directory.
    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)

    GENERATED_DIR.mkdir()

    course = validate_course(load_course())
    website = validate_website(load_website())
    content = load_content()
    sections = load_content_sections(content)
    registration = website.get("registration", {})
    events = validate_schedule(load_schedule())
    team = validate_team(load_team())
    announcements = load_announcements()
    practical_info = load_practical_info()
    faq = load_faq()

    available_pages = set()

    if events:
        available_pages.add("schedule")

    if practical_info:
        available_pages.add("practical")

    if faq:
        available_pages.add("faq")

    if announcements:
        available_pages.add("announcements")


    write_partial(
        "welcome.qmd",
        render_welcome(course),
    )

    write_partial(
        "navbar_meta.qmd",
        render_navbar_meta(course),
    )

    write_partial(
    "navbar_links.qmd",
    render_navbar_links(website, available_pages),
)

    write_partial(
        "registration.qmd",
        render_registration(registration),
    )

    write_partial(
        "upcoming.qmd",
        render_upcoming(events),
    )

    write_partial(
        "quick_links.qmd",
        render_quick_links(website, events),
    )

    write_partial(
        "announcements.qmd",
        render_announcements(announcements),
    )

    write_partial(
        "team.qmd",
        render_team(team),
    )

    write_partial(
        "team_page.qmd",
        render_team_page(team),
    )

    write_partial(
        "schedule.qmd",
        render_schedule(events, course),
    )

    write_partial(
        "content.qmd",
        render_content_overview(sections),
    )

    write_partial(
        "content-navbar.html",
        render_content_navbar(course, website, available_pages),
    )

    write_partial(
        "content-footer.html",
        render_content_footer(),
    )

    write_partial(
        "syllabus.qmd",
        render_syllabus(course, team),
    )

    write_partial(
    "practicalinfo.qmd",
    render_practical_info(practical_info),
    )

    write_partial(
        "faq.qmd",
        render_faq(faq),
    )

if __name__ == "__main__":
    main()