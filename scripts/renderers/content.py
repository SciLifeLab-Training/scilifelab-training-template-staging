import re
from pathlib import Path

from renderers.navbar import (
    render_navbar_meta,
    render_navbar_links,
)

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content"


def render_content_overview(sections):
    if not sections:
        return ""

    html = []

    for section in sections:
        pages = []

        for page in section["pages"]:
            href = page["path"].relative_to(CONTENT_DIR).with_suffix(".html")

            pages.append(
                f"""
<li>
<a href="{href}">{page["title"]}</a>
</li>
""".strip()
            )

        html.append(
            f"""
<div class="course-content-section">

<div class="course-content-section-label">
{section["label"]}
</div>

<h2>{section["title"]}</h2>

<ul class="course-content-pages">
{"".join(pages)}
</ul>

</div>
""".strip()
        )

    return "\n".join(html)


def render_content_navbar(course, website):
    meta = render_navbar_meta(course)
    links = render_navbar_links(website)

    # Quarto tries to resolve HTML hrefs during rendering.
    # The actual URLs are assigned by JavaScript after the page loads.
    links = re.sub(r'href="[^"]+"', 'href="#"', links)

    return """
    
<div class="course-navbar">

<div class="course-navbar-layout">

<div class="course-navbar-content">

<div class="course-navbar-title">
""" + meta + """
</div>

<div class="course-navbar-menu">

<div class="course-navbar-links">
""" + links + """
</div>

</div>

</div>

<div class="course-navbar-brand">

<img
    src=""
    data-course-asset="img/scilifelab-logo-full-neg.png"
    class="course-navbar-logo"
>

</div>

</div>

</div>

<script>
document.documentElement.classList.add("course-content-page");

document.addEventListener("DOMContentLoaded", function () {

    const navbar = document.querySelector(".course-navbar");
    const footer = document.querySelector(".landing-footer");

    /*
     * Move the shared site chrome outside Quarto's
     * main-content / TOC grid.
     */

    if (navbar) {
        document.body.insertBefore(navbar, document.body.firstChild);
    }

    if (footer) {
        document.body.appendChild(footer);
    }

    const pathname = window.location.pathname;
    const contentMarker = "/content/";

    const siteRoot = pathname.includes(contentMarker)
        ? pathname.split(contentMarker)[0] + "/"
        : "./";

    const currentPage =
        pathname.split("/").pop() || "index.html";

    const isContentPage =
        pathname.includes("/content/");

    document.querySelectorAll(".course-navbar-link").forEach(function (link) {

        const page = link.dataset.page;

        const expectedPage =
            page === "index.qmd"
                ? "index.html"
                : page.replace(".qmd", ".html");

        link.href = siteRoot + expectedPage;

        if (
            isContentPage
                ? page === "content/index.qmd"
                : expectedPage === currentPage
        ) {
            link.classList.add("course-navbar-link-active");
        }

    });

    document.querySelectorAll("[data-course-asset]").forEach(function (image) {
        image.src = siteRoot + image.dataset.courseAsset;
    });

});
</script>
""".strip()


def render_content_footer():
    return """
<footer class="landing-footer">

<div class="landing-footer__meta">

By SciLifeLab Training Hub. Licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">
CC BY 4.0
</a>.

<br>

Built with Quarto and hosted on GitHub Pages.

</div>

<div class="landing-footer__actions">

<a
    href="https://github.com/SciLifeLab-Training/scilifelab-training-template-staging/tree/main"
    class="landing-footer__image-link"
>

<img
    src=""
    data-course-asset="img/github-neg.png"
    alt="GitHub"
    class="landing-footer__image"
>

</a>

</div>

</footer>
""".strip()