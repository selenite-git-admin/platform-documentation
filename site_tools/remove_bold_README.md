# Remove Bold Utility — Documentation Cleanup

![Version: v1.0](https://img.shields.io/badge/Version-v1.0-informational)  
![Status: Stable](https://img.shields.io/badge/Status-Stable-green)  
![Owner: AK](https://img.shields.io/badge/Owner-AK-blue)  
![Last Updated: 30-Aug-2025](https://img.shields.io/badge/Last_Updated-30--Aug--2025-lightgrey)

---

## Purpose

`remove_bold.py` is a maintenance utility that **removes Markdown bold formatting**  
from `.md` files under `docs/` in a safe, controlled way.

This was built to:
- Normalize style across documentation.
- Remove leftover `**bold**` or `__bold__` emphasis from playbooks.
- Keep headings, labels, and code blocks intact.

---

## Features

- Removes:
  - `**text**` → `text`
  - `__text__` → `text`
  - `<strong>text</strong>` or `<b>text</b>` → `text`
- Skips:
  - Fenced code blocks (``` / ~~~)
  - Inline code spans (`like_this`)
  - YAML front matter
  - Headings (`# H1`, `## H2`, `Setext ===/---`)
- Preserves:
  - Leading label-style bold (e.g., `**CFO Pain:** …`)
- Options:
  - `--backup` → write `.bak` files before editing
  - `--dry-run` → preview changes without writing
  - `--include` / `--exclude` → glob filters
  - `--skip-headings` / `--no-skip-headings`
  - `--skip-leading-bold` / `--no-skip-leading-bold`

---

## Usage

Run from project root:

```powershell
# Preview changes, no edits
python remove_bold.py --dry-run -v

# Apply changes to all docs with backups
python remove_bold.py --path docs --backup -v

# Limit scope (example: only GTM subfolder)
python remove_bold.py --path docs\gtm --backup -v
