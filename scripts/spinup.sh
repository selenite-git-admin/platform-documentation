#!/usr/bin/env bash
# Spin up a new docs repo from this template using GitHub CLI.
# Usage: ./scripts/spinup.sh my-org my-new-docs
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. See https://cli.github.com/"
  exit 1
fi

ORG="${1:-}"
NAME="${2:-}"
if [[ -z "$ORG" || -z "$NAME" ]]; then
  echo "Usage: $0 <org-or-user> <repo-name>"
  exit 1
fi

TEMPLATE_REPO="$(git config --get remote.origin.url | sed 's#.*/##' | sed 's/.git$//')"
if [[ -z "$TEMPLATE_REPO" ]]; then
  echo "Run this from a cloned template repository."
  exit 1
fi

echo "Creating new repo $ORG/$NAME from template..."
gh repo create "$ORG/$NAME" --template "$ORG/$TEMPLATE_REPO" --public -y

echo "Cloning new repo..."
git clone "https://github.com/$ORG/$NAME.git"
cd "$NAME"

# Basic renames in mkdocs.yml and README
sed -i.bak "s|Your Project Docs|$NAME|g" mkdocs.yml && rm mkdocs.yml.bak
sed -i.bak "s|https://github.com/your-org/your-repo|https://github.com/$ORG/$NAME|g" mkdocs.yml && rm mkdocs.yml.bak
sed -i.bak "s|your-org/your-repo|$ORG/$NAME|g" mkdocs.yml && rm mkdocs.yml.bak

git add .
git commit -m "chore: initial rename to $NAME"
git push origin main

echo "Enabling GitHub Pages (gh-pages branch)..."
gh api -X PUT "repos/$ORG/$NAME/pages" -f source[branch]='gh-pages' -f source[path]='/' || true

echo "Done. Next steps:"
echo "  cd $NAME"
echo "  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
echo "  mkdocs serve  # http://127.0.0.1:8000"
