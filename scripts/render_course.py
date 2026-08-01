#!/usr/bin/env python3

from loaders import (
    load_course,
    load_website,
    load_schedule,
)

from validators import (
    validate_course,
    validate_website,
    validate_schedule,
)
from writer import write_partial

from renderers.welcome import render_welcome
from renderers.navbar import (
    render_navbar_meta,
    render_navbar_links,
)
from renderers.upcoming import render_upcoming

from renderers.quick_links import render_quick_links


def main():
    print("Running course renderer...")

    course = validate_course(load_course())
    website = validate_website(load_website())
    events = validate_schedule(load_schedule())

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
    render_navbar_links(website),
    )

    write_partial(
    "upcoming.qmd",
    render_upcoming(events),
)

    write_partial(
    "quick_links.qmd",
    render_quick_links(website),
)

if __name__ == "__main__":
    main()