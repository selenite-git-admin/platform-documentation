# Site Tools Index

![Version: v1.0](https://img.shields.io/badge/Version-v1.0-informational)  
![Status: Active](https://img.shields.io/badge/Status-Active-green)  
![Owner: AK](https://img.shields.io/badge/Owner-AK-blue)  
![Last Updated: 30-Aug-2025](https://img.shields.io/badge/Last_Updated-30--Aug--2025-lightgrey)

---

## Purpose

The `site_tools/` folder contains **internal maintenance utilities** for the documentation project.  
These scripts are not part of MkDocs build; they are for **content hygiene, audits, and refactoring**.  

Use them with discipline: always `--dry-run` first, always commit backups or diffs before shipping.

---

## Tools

### 1. Remove Bold Utility
- **File:** [`remove_bold.py`](../site_tools/remove_bold.py)  
- **Docs:** [`remove_bold_README.md`](../site_tools/remove_bold_README.md)  
- **Purpose:** Strip unwanted bold styling (`**text**`, `__text__`, `<b>`) from Markdown files under `docs/`.  
- **Features:**  
  - Skips fenced code, inline code, YAML front matter.  
  - Optionally skips headings and preserves label-style bold at line start.  
  - Supports `--backup`, `--dry-run`, `--include`, `--exclude`.  
- **Usage:**  
  ```powershell
  python site_tools/remove_bold.py --path docs --dry-run -v
  python site_tools/remove_bold.py --path docs --backup -v
