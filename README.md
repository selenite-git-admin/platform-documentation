# mkdocs-material-template

A reusable, batteries‑included template for launching new documentation sites with MkDocs + Material.

## Quick start

```bash
# 0) Implement virtualenv
python -m venv venv

# 1) Use a virtualenv
venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run locally
mkdocs serve --dev-addr=127.0.0.1:8000 # (or your preferred port)

# 4) Build & deploy (locally, optional)
mkdocs gh-deploy --force
```

## Recommended: Use as a GitHub Template
1. Push this repo to GitHub (once) and mark it as **Template** (Settings → Template repository).
2. Click **Use this template** → name your new docs repo.
3. (Optional) Enable GitHub Pages on the new repo: Settings → Pages → Build from **gh-pages** branch.

## Structure
```
mkdocs.yml
requirements.txt
.github/workflows/ci.yml
docs/
  index.md
  overview/getting-started.md
  guides/authoring.md
  reference/_placeholder.md
  assets/stylesheets/extra.css
  assets/javascripts/extra.js
scripts/spinup.sh
.gitignore
LICENSE
```

## Versioned docs (optional)
This template includes `mike` for versioning.

```bash
# First deployment creates 'latest' alias
mike deploy 0.1 --update-aliases latest
mike set-default latest
git push origin gh-pages
```

## Notes
- Edit `mkdocs.yml` → `site_name`, `repo_url`, and `extra.social`.
- Add your logo/favicon under `docs/assets/` and reference via `theme.logo` and `theme.favicon`.
- If you don’t want versioning, you can ignore `mike`.
