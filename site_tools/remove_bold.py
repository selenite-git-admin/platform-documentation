#!/usr/bin/env python3
"""
remove_bold.py — Strip bold formatting from Markdown files under ./docs

Features:
- Removes Markdown bold (**text**, __text__) and HTML bold tags (<strong>, <b>).
- Skips fenced code blocks (``` or ~~~) and inline code spans (`code`).
- Skips YAML front matter at the top of a file.
- Optional: Skip headings (ATX "#" and Setext "underlines") [default ON].
- Optional: Preserve a leading label-style bold at the start of a line [default ON].
- Optional: Create .bak backups before modifying files.
- Optional: Include/Exclude glob patterns to target a subset of files.

Usage:
  python remove_bold.py --dry-run -v
  python remove_bold.py --path docs --include "docs/gtm/**/*.md" --exclude "docs/brand-guide/**" -v
  python remove_bold.py --backup -v
  python remove_bold.py --no-skip-headings
  python remove_bold.py --no-skip-leading-bold

Exit codes:
  0 on success (or no changes)
  1 on dry-run with modifications (useful in CI)
  2 on an invalid path
"""

from __future__ import annotations
import argparse
import fnmatch
import pathlib
import re
import sys
from typing import Tuple, List

# Regexes
FENCE_RE = re.compile(r'^\s*([`~]{3,})(.*)$')                     # start/end of fenced code block
INLINE_CODE_SPLIT_RE = re.compile(r'(`+[^`]*`+)')                 # split keeping inline code spans
HTML_B_TAGS_RE = re.compile(r'</?(?:strong|b)\s*>', re.IGNORECASE)

# Bold patterns for segments outside code:
MD_BOLD_DOUBLE_RE = re.compile(r'\*\*(.+?)\*\*', re.DOTALL)
MD_BOLD_UNDERS_RE = re.compile(r'__(.+?)__', re.DOTALL)

FRONT_MATTER_DELIM = re.compile(r'^\s*---\s*$')
ATX_HEADING_RE = re.compile(r'^\s*#{1,6}\s+')
SETEXT_UNDERLINE_RE = re.compile(r'^\s*(=+|-+)\s*$')

def process_line_outside_code(line: str) -> Tuple[str, int]:
    """
    Remove bold markers from a single line that is OUTSIDE a fenced code block.
    Preserves inline code spans (backticks). Returns (new_line, changes_count).
    """
    parts = INLINE_CODE_SPLIT_RE.split(line)
    changed = 0
    for i in range(0, len(parts), 2):  # even indices: outside inline code
        seg = parts[i]
        before = seg
        # Remove HTML bold tags first
        seg = HTML_B_TAGS_RE.sub('', seg)
        # Replace **text** → text
        seg, c1 = MD_BOLD_DOUBLE_RE.subn(r'\1', seg)
        # Replace __text__ → text
        seg, c2 = MD_BOLD_UNDERS_RE.subn(r'\1', seg)
        changed += c1 + c2
        if seg != before:
            parts[i] = seg
    return ''.join(parts), changed

# If True, keep leading **label** or __label__ at the beginning of a non-code/non-heading line.
def _preserve_leading_bold_segment(seg: str, enable: bool) -> tuple[str, int]:
    if not enable:
        return seg, 0
    # Match optional indentation then a single leading bold span (**...** or __...__)
    m = re.match(r'^(\s*)(\*\*.+?\*\*|__.+?__)(.*)$', seg, flags=re.DOTALL)
    if not m:
        return seg, 0
    indent, leading_bold, rest = m.groups()
    # Do not alter the leading bold; process only the rest (outside inline code already)
    processed_rest, changes = process_line_outside_code(rest)
    return indent + leading_bold + processed_rest, changes

def process_line_outside_code_with_leading(line: str, skip_leading_bold: bool) -> tuple[str, int]:
    """
    Like process_line_outside_code, but preserves a leading **bold** or __bold__ segment if configured.
    """
    parts = INLINE_CODE_SPLIT_RE.split(line)
    changed_total = 0

    if parts:
        # Preserve the very first outside-code part's leading bold if present
        preserved, ch = _preserve_leading_bold_segment(parts[0], enable=skip_leading_bold)
        if preserved != parts[0]:
            parts[0] = preserved
        changed_total += ch

    # Now strip the rest; if we preserved leading bold in parts[0], protect it while stripping other bolds
    for i in range(0, len(parts), 2):
        if i == 0 and skip_leading_bold:
            before = parts[0]
            # Remove HTML bold tags
            seg = HTML_B_TAGS_RE.sub('', before)
            # Protect the leading bold by temporarily marking it, then strip others
            lead_match = re.match(r'^(\s*)(\*\*.+?\*\*|__.+?__)', before, flags=re.DOTALL)
            if lead_match:
                seg_marked = re.sub(r'^(\s*)(\*\*.+?\*\*|__.+?__)', r'\1@@LEADING_BOLD@@', seg, count=1, flags=re.DOTALL)
                seg_marked, c1 = MD_BOLD_DOUBLE_RE.subn(r'\1', seg_marked)
                seg_marked, c2 = MD_BOLD_UNDERS_RE.subn(r'\1', seg_marked)
                seg_final = seg_marked.replace('@@LEADING_BOLD@@', lead_match.group(0))
                parts[0] = seg_final
                changed_total += (c1 + c2)
                continue
            # If no leading bold, just strip normally
        new_seg, ch = process_line_outside_code(parts[i])
        if new_seg != parts[i]:
            parts[i] = new_seg
        changed_total += ch

    return ''.join(parts), changed_total

def strip_bold_from_text(text: str, skip_headings: bool, skip_leading_bold: bool) -> Tuple[str, int]:
    """
    Process full Markdown text, skipping YAML front matter and fenced code blocks.
    Optionally skip headings; optionally preserve leading label-style bold.
    Returns (new_text, total_changes).
    """
    lines = text.splitlines(keepends=False)
    out_lines: List[str] = []
    in_fence = False
    fence_marker = None
    in_front_matter = False
    total_changes = 0

    # Detect YAML front matter only if present at the very start
    if lines and FRONT_MATTER_DELIM.match(lines[0] or ''):
        in_front_matter = True

    for ln, line in enumerate(lines):
        # Handle YAML front matter block at the very top
        if in_front_matter:
            out_lines.append(line)
            if ln != 0 and FRONT_MATTER_DELIM.match(line):
                in_front_matter = False
            continue

        # Handle fenced code blocks
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                # Only end fence if markers match char and length or longer
                if marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                    in_fence = False
                    fence_marker = None
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        # Headings: skip if requested (ATX or Setext underline lines)
        if skip_headings:
            if ATX_HEADING_RE.match(line):
                out_lines.append(line)
                continue
            if ln > 0 and SETEXT_UNDERLINE_RE.match(line) and lines[ln - 1].strip():
                out_lines.append(line)
                continue

        # Outside fences and front matter → process
        new_line, changed = process_line_outside_code_with_leading(line, skip_leading_bold=skip_leading_bold)
        total_changes += changed
        out_lines.append(new_line)

    return '\n'.join(out_lines) + ('' if text.endswith('\n') else ''), total_changes

def should_process(path: pathlib.Path, includes: List[str], excludes: List[str]) -> bool:
    p = str(path.as_posix())
    if includes:
        if not any(fnmatch.fnmatch(p, pat) for pat in includes):
            return False
    if excludes:
        if any(fnmatch.fnmatch(p, pat) for pat in excludes):
            return False
    return True

def process_file(path: pathlib.Path, dry_run: bool, verbose: bool, skip_headings: bool, backup: bool, skip_leading_bold: bool) -> Tuple[int, bool]:
    original = path.read_text(encoding='utf-8', errors='replace')
    new_text, changes = strip_bold_from_text(original, skip_headings=skip_headings, skip_leading_bold=skip_leading_bold)
    modified = (changes > 0 and new_text != original)
    if verbose:
        print(f"[{'CHG' if modified else 'OK '}] {path}  (replacements={changes})")
    if modified and not dry_run:
        if backup:
            bak = path.with_suffix(path.suffix + ".bak")
            bak.write_text(original, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
    return changes, modified

def main():
    ap = argparse.ArgumentParser(description="Strip bold formatting from Markdown files under a docs/ folder.")
    ap.add_argument("--path", default="docs", help="Root folder to scan (default: ./docs)")
    ap.add_argument("--ext", nargs="*", default=[".md", ".markdown"], help="Markdown file extensions to include")
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    ap.add_argument("--skip-headings", dest="skip_headings", action="store_true", default=True, help="Skip heading lines (ATX/Setext) [default]")
    ap.add_argument("--no-skip-headings", dest="skip_headings", action="store_false", help="Do not skip headings")
    ap.add_argument("--backup", action="store_true", help="Write .bak backups before modifying")
    ap.add_argument("--include", action="append", default=[], help="Glob pattern to include (can be repeated)")
    ap.add_argument("--exclude", action="append", default=[], help="Glob pattern to exclude (can be repeated)")
    ap.add_argument(
        "--skip-leading-bold", dest="skip_leading_bold",
        action="store_true", default=True,
        help="Preserve leading **bold**/__bold__ labels at start of line [default]"
    )
    ap.add_argument(
        "--no-skip-leading-bold", dest="skip_leading_bold",
        action="store_false",
        help="Also strip leading bold labels at line start"
    )
    args = ap.parse_args()

    root = pathlib.Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: Path not found or not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    total_files = 0
    total_changes = 0
    total_modified = 0

    skip_dirs = {".git", ".venv", "node_modules", ".mypy_cache", ".pytest_cache", ".cache"}

    for p in root.rglob("*"):
        if p.is_dir():
            if p.name in skip_dirs:
                continue
        else:
            if p.suffix.lower() in args.ext and p.is_file():
                if not should_process(p, args.include, args.exclude):
                    continue
                total_files += 1
                changes, modified = process_file(
                    p,
                    dry_run=args.dry_run,
                    verbose=args.verbose,
                    skip_headings=args.skip_headings,
                    backup=args.backup,
                    skip_leading_bold=args.skip_leading_bold,
                )
                total_changes += changes
                total_modified += 1 if modified else 0

    if args.verbose or args.dry_run:
        print(f"\nScanned: {total_files} files | Modified: {total_modified} | Replacements: {total_changes} | Dry-run: {args.dry_run}")
    # Exit code non-zero if dry-run with modifications (useful in CI)
    if args.dry_run and total_modified > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
