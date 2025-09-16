#!/usr/bin/env python3
"""
remove_rule.py — Remove Markdown horizontal rules and collapse excess blank lines.

Removes horizontal rules (***, ---, ___ with optional spaces) while:
- Skipping fenced code blocks (``` or ~~~).
- Preserving YAML front matter delimiters at the top (--- ... ---).
- Preserving Setext heading underlines ("---"/"===" under a title line) by default.

Also collapses **excess blank lines** (more than one → a single blank line) outside
front matter and fenced code blocks. You can disable this with --no-collapse-blank-lines.

Usage:
  python remove_rule.py --dry-run -v
  python remove_rule.py --path docs --backup -v
  python remove_rule.py --include "docs/guides/**/*.md" --exclude "docs/adr/**" -v
"""

from __future__ import annotations
import argparse
import pathlib
import re
import sys
import fnmatch
from typing import List, Tuple

# Fences / headings / front matter
FENCE_RE = re.compile(r'^\s*([`~]{3,})(.*)$')                     # start/end fenced code
FRONT_MATTER_DELIM = re.compile(r'^\s*---\s*$')                   # YAML front matter fence
SETEXT_UNDERLINE_RE = re.compile(r'^\s*(=+|-+)\s*$')              # setext underline

# Horizontal rule: three or more of the same marker (*, -, _) allowing spaces
HR_LINE_RE = re.compile(r'^\s*([*\-_])(?:\s*\1){2,}\s*$')

def _norm(pat: str) -> str:
    """Normalize glob patterns to POSIX style so Windows backslashes work."""
    return pat.replace('\\', '/')

def should_process(path: pathlib.Path, includes: List[str], excludes: List[str]) -> bool:
    """Glob filtering with normalized patterns."""
    p = path.as_posix()
    if includes and not any(fnmatch.fnmatch(p, _norm(pat)) for pat in includes):
        return False
    if excludes and any(fnmatch.fnmatch(p, _norm(pat)) for pat in excludes):
        return False
    return True

def is_setext_underline(lines: List[str], idx: int) -> bool:
    """Return True iff the line at idx is a Setext underline for the previous non-empty line."""
    if idx <= 0 or idx >= len(lines):
        return False
    if not SETEXT_UNDERLINE_RE.match(lines[idx]):
        return False
    return bool(lines[idx - 1].strip())

def should_remove_as_hr(lines: List[str], idx: int, keep_setext: bool) -> bool:
    """Decide whether the current line is an HR we should remove."""
    line = lines[idx]
    if not HR_LINE_RE.match(line):
        return False
    # If it's a potential Setext underline using '-', preserve when requested
    if keep_setext and set(line.strip()) <= {'-'} and is_setext_underline(lines, idx):
        return False
    return True

def process_text(text: str, keep_setext: bool, collapse_blank_lines: bool) -> Tuple[str, int, int]:
    lines = text.splitlines(keepends=False)
    out_lines: List[str] = []
    in_fence = False
    fence_marker = None
    in_front_matter = False
    total_removed_hr = 0
    total_collapsed_blanks = 0

    # detect YAML front matter only at the very top
    if lines and FRONT_MATTER_DELIM.match(lines[0] or ''):
        in_front_matter = True

    def _append_line_outside_fence(line: str):
        nonlocal total_collapsed_blanks
        if collapse_blank_lines and line.strip() == '':
            # collapse: if last output line is already blank, skip this one
            if out_lines and out_lines[-1].strip() == '':
                total_collapsed_blanks += 1
                return
        out_lines.append(line)

    for idx, line in enumerate(lines):
        # Front matter passthrough
        if in_front_matter:
            out_lines.append(line)
            if idx != 0 and FRONT_MATTER_DELIM.match(line):
                in_front_matter = False
            continue

        # Fenced code passthrough
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                if marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                    in_fence = False
                    fence_marker = None
            out_lines.append(line)
            continue

        if in_fence:
            # inside fence, do not collapse blanks or remove HRs
            out_lines.append(line)
            continue

        # Outside fences and front matter
        if should_remove_as_hr(lines, idx, keep_setext=keep_setext):
            total_removed_hr += 1
            # skip adding this line
            continue

        _append_line_outside_fence(line)

    # Preserve trailing newline if present
    trailing_nl = text.endswith('\n')
    result = '\n'.join(out_lines) + ('\n' if trailing_nl else '')
    return result, total_removed_hr, total_collapsed_blanks

def process_file(path: pathlib.Path, dry_run: bool, verbose: bool, keep_setext: bool, collapse_blank_lines: bool, backup: bool) -> Tuple[Tuple[int,int], bool]:
    original = path.read_text(encoding='utf-8', errors='replace')
    new_text, removed_hr, collapsed_blanks = process_text(original, keep_setext=keep_setext, collapse_blank_lines=collapse_blank_lines)
    modified = ((removed_hr + collapsed_blanks) > 0) and (new_text != original)
    if verbose:
        print(f"[{'CHG' if modified else 'OK '}] {path}  (removed_hr={removed_hr}, collapsed_blanks={collapsed_blanks})")
    if modified and not dry_run:
        if backup:
            path.with_suffix(path.suffix + ".bak").write_text(original, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
    return (removed_hr, collapsed_blanks), modified

def main():
    ap = argparse.ArgumentParser(description="Remove Markdown horizontal rules and collapse excess blank lines from a docs/ tree.")
    ap.add_argument("--path", default="docs", help="Root folder to scan (default: ./docs)")
    ap.add_argument("--ext", nargs="*", default=[".md", ".markdown"], help="Markdown file extensions")
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    ap.add_argument("--backup", action="store_true", help="Write .bak backups before modifying")
    ap.add_argument("--include", action="append", default=[], help="Glob pattern to include (repeatable)")
    ap.add_argument("--exclude", action="append", default=[], help="Glob pattern to exclude (repeatable)")
    ap.add_argument("--keep-setext", dest="keep_setext", action="store_true", default=True,
                    help="Preserve Setext heading underlines (default)")
    ap.add_argument("--no-keep-setext", dest="keep_setext", action="store_false",
                    help="Also remove Setext underlines made of '-'")
    ap.add_argument("--collapse-blank-lines", dest="collapse_blank_lines", action="store_true", default=True,
                    help="Collapse consecutive blank lines into a single blank line (default)")
    ap.add_argument("--no-collapse-blank-lines", dest="collapse_blank_lines", action="store_false",
                    help="Do not collapse consecutive blank lines")
    args = ap.parse_args()

    root = pathlib.Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: Path not found or not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    total_files = total_mod = 0
    sum_removed_hr = 0
    sum_collapsed_blanks = 0

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
                (removed_hr, collapsed_blanks), modified = process_file(
                    p,
                    dry_run=args.dry_run,
                    verbose=args.verbose,
                    keep_setext=args.keep_setext,
                    collapse_blank_lines=args.collapse_blank_lines,
                    backup=args.backup,
                )
                sum_removed_hr += removed_hr
                sum_collapsed_blanks += collapsed_blanks
                total_mod += 1 if modified else 0

    if args.verbose or args.dry_run:
        print(f"\nScanned: {total_files} files | Modified: {total_mod} | Rules removed: {sum_removed_hr} | Blank lines collapsed: {sum_collapsed_blanks} | Dry-run: {args.dry_run}")
    # CI gate: non-zero if changes would occur
    if args.dry_run and total_mod > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
