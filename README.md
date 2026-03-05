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

## Landing authoring model

- `index.qmd` is the stable landing entrypoint.
- `_sections/*.qmd` contains authored page copy and structure.
- `scripts/generate_landing.py` validates data and generates `_generated/*.qmd` dynamic partials.
- `data/instances.yml` is the source of truth for current/previous instance links and visibility.
- `data/ui.yml` controls dynamic CTA and instance-band labels.

Do not edit `_generated/*` manually.

## Local contributor workflow

Prerequisites:

- Python 3.12
- Quarto 1.3.340 (same pin as CI workflows)

Setup and checks:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/generate_landing.py
quarto render
```

Rendered output is written to `_site/`.

## Course instance workflow

Create a new instance by creating a new `release-YYMM` branch from `release-0000`, then update content and `_quarto.yml` in that branch. On push, the release workflow deploys only that instance folder to `gh-pages`.

## Deploy safety invariants

- Keep `.nojekyll` on `gh-pages`.
- The landing and instance workflows share `deploy-gh-pages` concurrency control to avoid deploy races.
- Never use root-level sync like `rsync -a --delete _site/ gh-pages/`; this can remove instance directories.
- Publish landing root with allowlist copy only (`index.html`, `styles.css`, `site_libs/`, `index_files/`, `img/`).
- Keep raw data out of published output (`gh-pages/data/` and root `*.yml` must not exist).
- `gh-pages` is machine-managed output; manual commits are last-resort incident recovery only.

## Additional docs

- Contributor runbook: `docs/landing-runbook.md`
- Legacy-to-new migration map: `docs/landing-migration-map.md`
