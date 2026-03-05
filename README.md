# The SciLifeLab course template

This template supports a two-layer site model on GitHub Pages:

- `main`: customizable landing page source (hero, cards, links, contributors).
- `release-*`: one branch per course instance, rendered into a dated subdirectory on `gh-pages`.

## Branch model

1. `main`
   - Holds landing source files (`index.qmd`, `_sections/*`, `styles.css`) and instance metadata (`data/instances.yml`).
   - Uses pre-render script `scripts/generate_landing.py` to validate metadata and generate dynamic partials in `_generated/*`.
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

- `index.qmd`: landing entrypoint composition.
- `_sections/*.qmd`: authored landing copy and structure.
- `data/instances.yml`: current/previous instance metadata and visibility.
- `data/ui.yml`: labels for dynamic buttons and instance-band copy (only documented keys are allowed; unknown keys fail validation).
- `styles.css`: visual design.
- `scripts/generate_landing.py`: metadata validation + dynamic partial generation (`_generated/*`).

The generator no longer writes `index.qmd`; it validates `data/instances.yml` and writes only dynamic include files into `_generated/*` before render.
Do not edit `_generated/*` manually.

## Course instance workflow

Create a new instance by creating a new `release-YYMM` branch from `release-0000`, then update content and `_quarto.yml` in that branch. On push, the release workflow deploys only that instance folder to `gh-pages`.

## Notes

- Keep `.nojekyll` on `gh-pages`.
- The landing and instance workflows share a single concurrency group to avoid deployment races.
- `gh-pages` should not be edited manually.
