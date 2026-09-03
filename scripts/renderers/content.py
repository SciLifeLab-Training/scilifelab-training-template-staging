from pathlib import Path


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