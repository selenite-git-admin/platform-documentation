# Remove Rule Utility — Documentation Cleanup

**Status:** Stable · **Version:** v1.1

## Purpose
- Remove Markdown **horizontal rules** (`***`, `---`, `___`) safely.
- **Collapse excess blank lines** (more than one → a single blank line) outside fenced code blocks and front matter.

## Safety
- Skips YAML front matter and fenced code blocks.
- Preserves **Setext headings** by default (title lines underlined with `---` or `===`).

## Usage
```bash
# Preview (CI-friendly). Exits 1 if changes would occur.
python site_tools/remove_rule.py --path docs --dry-run -v

# Apply with backups
python site_tools/remove_rule.py --path docs --backup -v

# Apply without backups
python site_tools/remove_rule.py --path docs -v
```

## Options
- `--keep-setext` / `--no-keep-setext` — preserve or remove Setext underlines (default: keep)
- `--collapse-blank-lines` / `--no-collapse-blank-lines` — enable/disable blank-line collapsing (default: on)
- `--include` / `--exclude` — glob filters (use **forward slashes** even on Windows)
- `--backup` — write `.bak` before modifying files
- `--dry-run` — don’t write; print what would change

## Notes
Blank-line collapsing only runs **outside** front matter and fenced code to avoid breaking code and sample formatting.
