#!/usr/bin/env python3
"""
remove_em_dash.py — Replace Unicode em dashes (—) in Markdown under ./docs

Default replacement is a single hyphen "-" to align with STE style.

Safety:
- Skips fenced code blocks (``` or ~~~) and inline code spans (`code`).
- Skips YAML front matter at the top.
- Skips ATX and Setext headings by default (configurable).

Usage:
  python remove_em_dash.py --dry-run -v
  python remove_em_dash.py --path docs --backup -v
  python remove_em_dash.py --replacement " - " --also-en-dash -v
"""

from __future__ import annotations
import argparse
import pathlib
import re
import sys
import fnmatch
from typing import List, Tuple

FENCE_RE = re.compile(r'^\s*([`~]{3,})(.*)$')
INLINE_CODE_SPLIT_RE = re.compile(r'(`+[^`]*`+)')
FRONT_MATTER_DELIM = re.compile(r'^\s*---\s*$')
ATX_HEADING_RE = re.compile(r'^\s*#{1,6}\s+')
SETEXT_UNDERLINE_RE = re.compile(r'^\s*(=+|-+)\s*$')

EM_DASH = "\u2014"
EN_DASH = "\u2013"

def _norm(pat: str) -> str:
    """Normalize glob patterns to POSIX style so Windows backslashes work."""
    return pat.replace('\\', '/')

def should_process(path: pathlib.Path, includes: List[str], excludes: List[str]) -> bool:
    p = path.as_posix()
    if includes and not any(fnmatch.fnmatch(p, _norm(pat)) for pat in includes):
        return False
    if excludes and any(fnmatch.fnmatch(p, _norm(pat)) for pat in excludes):
        return False
    return True

def replace_outside_code_segment(seg: str, repl: str, also_en: bool) -> Tuple[str, int]:
    count = 0
    c1 = seg.count(EM_DASH)
    if c1:
        seg = seg.replace(EM_DASH, repl)
    count += c1
    if also_en:
        c2 = seg.count(EN_DASH)
        if c2:
            seg = seg.replace(EN_DASH, repl)
        count += c2
    return seg, count

def process_line(line: str, repl: str, also_en: bool) -> Tuple[str, int]:
    parts = INLINE_CODE_SPLIT_RE.split(line)  # keep code spans intact
    changes = 0
    for i in range(0, len(parts), 2):  # even indices are outside code
        parts[i], c = replace_outside_code_segment(parts[i], repl, also_en)
        changes += c
    return ''.join(parts), changes

def process_text(text: str, skip_headings: bool, repl: str, also_en: bool) -> Tuple[str, int]:
    lines = text.splitlines(keepends=False)
    out_lines: List[str] = []
    in_fence = False
    fence_marker = None
    in_front_matter = False
    total_changes = 0

    if lines and FRONT_MATTER_DELIM.match(lines[0] or ''):
        in_front_matter = True

    for ln, line in enumerate(lines):
        if in_front_matter:
            out_lines.append(line)
            if ln != 0 and FRONT_MATTER_DELIM.match(line):
                in_front_matter = False
            continue

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
            out_lines.append(line)
            continue

        # Headings (optional skip)
        if skip_headings:
            if ATX_HEADING_RE.match(line):
                out_lines.append(line)
                continue
            if ln > 0 and SETEXT_UNDERLINE_RE.match(line) and lines[ln - 1].strip():
                out_lines.append(line)
                continue

        new_line, ch = process_line(line, repl, also_en)
        out_lines.append(new_line)
        total_changes += ch

    trailing_nl = text.endswith('\n')
    result = '\n'.join(out_lines) + ('\n' if trailing_nl else '')
    return result, total_changes

def process_file(path: pathlib.Path, dry_run: bool, verbose: bool, skip_headings: bool, backup: bool, repl: str, also_en: bool) -> Tuple[int, bool]:
    original = path.read_text(encoding='utf-8', errors='replace')
    new_text, changes = process_text(original, skip_headings=skip_headings, repl=repl, also_en=also_en)
    modified = (changes > 0 and new_text != original)
    if verbose:
        print(f"[{'CHG' if modified else 'OK '}] {path}  (replacements={changes})")
    if modified and not dry_run:
        if backup:
            path.with_suffix(path.suffix + ".bak").write_text(original, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
    return changes, modified

def main():
    ap = argparse.ArgumentParser(description="Replace em dash (—) characters in Markdown under docs/.")
    ap.add_argument("--path", default="docs", help="Root folder to scan (default: ./docs)")
    ap.add_argument("--ext", nargs="*", default=[".md", ".markdown"], help="Markdown file extensions")
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    ap.add_argument("--backup", action="store_true", help="Write .bak backups before modifying")
    ap.add_argument("--include", action="append", default=[], help="Glob pattern to include (repeatable)")
    ap.add_argument("--exclude", action="append", default=[], help="Glob pattern to exclude (repeatable)")
    ap.add_argument("--skip-headings", dest="skip_headings", action="store_true", default=True,
                    help="Skip heading lines (ATX/Setext) [default]")
    ap.add_argument("--no-skip-headings", dest="skip_headings", action="store_false",
                    help="Also process headings")
    ap.add_argument("--replacement", default="-",
                    help="Replacement string for em dashes (default: '-')")
    ap.add_argument("--also-en-dash", dest="also_en", action="store_true", default=False,
                    help="Also replace en dashes (–) with the same replacement")
    args = ap.parse_args()

    root = pathlib.Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: Path not found or not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    total_files = total_mod = total_changes = 0
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
                    repl=args.replacement,
                    also_en=args.also_en
                )
                total_changes += changes
                total_mod += 1 if modified else 0

    if args.verbose or args.dry_run:
        print(f"\nScanned: {total_files} files | Modified: {total_mod} | Replacements: {total_changes} | Dry-run: {args.dry_run}")
    # CI gate: non-zero if changes would occur
    if args.dry_run and total_mod > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
