#!/usr/bin/env python3

from loaders import load_course, load_website
from validators import validate_course, validate_website
from writer import write_partial

from renderers.welcome import render_welcome
from renderers.navbar import render_navbar


def main():
    print("Running course renderer...")

    course = validate_course(load_course())
    website = validate_website(load_website())

    write_partial(
        "welcome.qmd",
        render_welcome(course),
    )

    write_partial(
        "navbar.qmd",
        render_navbar(course, website),
    )


if __name__ == "__main__":
    main()