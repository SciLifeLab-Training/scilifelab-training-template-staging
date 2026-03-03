# The SciLifeLab course template

This template supports a two-layer site model on GitHub Pages:

- `main`: customizable landing page source (hero, cards, links, contributors).
- `release-*`: one branch per course instance, rendered into a dated subdirectory on `gh-pages`.

## Branch model

1. `main`
   - Holds landing page source files (`index.qmd`, `styles.css`, `data/*`, `scripts/*`).
   - Uses `.github/workflows/deploy-landing.yml` to publish root landing assets to `gh-pages`.
2. `release-YYMM`
   - Holds Quarto content for a specific course run.
   - Uses branch workflow (`.github/workflows/main.yml` on release branches) to publish only `YYMM/` on `gh-pages`.
3. `gh-pages`
   - Deployment output only.
   - Root contains landing page output.
   - Subdirectories (`0000/`, `2505/`, etc.) contain rendered course instances.

## Landing page customization

Edit these files on `main`:

- `data/landing.yml`: hero text, top cards, footer, founders, contributors.
- `data/instances.yml`: current/previous instance metadata and visibility.
- `styles.css`: visual design.
- `templates/index.template.qmd`: layout template used by `scripts/generate_landing.py`.

The landing page is regenerated from data before render.

## Course instance workflow

Create a new instance by creating a new `release-YYMM` branch from `release-0000`, then update content and `_quarto.yml` in that branch. On push, the release workflow deploys only that instance folder to `gh-pages`.

## Notes

- Keep `.nojekyll` on `gh-pages`.
- The landing and instance workflows share a single concurrency group to avoid deployment races.
- `gh-pages` should not be edited manually.
