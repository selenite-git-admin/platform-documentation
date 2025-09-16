# Remove Em Dash Utility — Documentation Cleanup

**Status:** Stable · **Version:** v1.0

## Purpose
Replace all **Unicode em dashes** (—) in Markdown with a plain hyphen (`-`) by default. Keeps content STE-friendly and consistent.

## Features
- Replaces:
  - Em dash **—** (U+2014) → **`-`** (default)
  - Optionally en dash **–** (U+2013) with `--also-en-dash`
- Skips:
  - Fenced code blocks (``` / ~~~)
  - Inline code spans (``like_this``)
  - YAML front matter
  - Headings (ATX/Setext) by default (`--skip-headings`)
- Options:
  - `--replacement` — customize output (e.g., `" - "`)
  - `--backup`, `--dry-run`, `--include`, `--exclude`

## Usage
```bash
# Preview changes, no edits (CI-friendly). Exits 1 if changes would occur.
python site_tools/remove_em_dash.py --path docs --dry-run -v

# Apply with backups
python site_tools/remove_em_dash.py --path docs --backup -v

# Preview both em and en dashes with spaced hyphen
python site_tools/remove_em_dash.py --path docs --replacement " - " --also-en-dash --dry-run -v

# Replace both em and en dashes with spaced hyphen
python site_tools/remove_em_dash.py --path docs --replacement " - " --also-en-dash -v
```

## Windows note
Use **forward slashes** in include/exclude globs (e.g., `docs/guides/**/*.md`). The tool normalizes paths to POSIX form.

## Safety notes
- Start with `--dry-run`. In CI, a non-zero exit means edits would be made.
- Headings are skipped by default to avoid changing titles; include them with `--no-skip-headings`.
- Code blocks/spans are skipped to avoid breaking examples.
