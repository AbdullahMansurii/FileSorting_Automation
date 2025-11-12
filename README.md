# 📂 Downloads Sorter

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)

A small Python utility to automatically sort files in your **Downloads** folder into categorized subfolders (Images, Videos, Docs, Code, etc.). Lightweight, single-file, and easy to customize.

---

## Table of Contents
- [Features](#features)
- [How it works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Safety notes](#safety-notes)
- [Suggested improvements](#suggested-improvements)

---

## Features
- Detects file extension and moves file into category folders (e.g. `_Images`, `_Videos`, `_Docs`).
- Skips folders and files that already start with `_`.
- Creates category folders if missing.
- Friendly console logging for actions and errors.

---

## How it works
1. Lists all items in the target `PATH_DOWNLOADS` folder.  
2. For each file (non-directory), it extracts the extension and checks `CATEGORIES` mapping.  
3. Creates a category folder (if not present) and moves the file using `shutil.move`.  
4. Files with unknown/unsupported extensions are moved to `_Others`.

5.

---
##  Safety notes (READ BEFORE RUNNING)
No sensitive data is present in the code (no API keys or passwords). Safe to publish.
Be careful moving system or installer files: The current CATEGORIES contains "System": [".ini", ".dll"]. Moving .dll/.ini files can break installed applications or Windows behaviour. Consider removing system extensions or adding safeguards.
Test with a dry-run first: Add a dry-run mode that prints moves without performing them.
Back up important files before first run.
Run with normal user privileges (avoid running as admin/root).
Be careful with cloud-sync/important folders (e.g., don't point PATH_DOWNLOADS at a folder used by other apps).

##  Suggested improvements
Add a --dry-run CLI flag (print actions without moving).
Use argparse to accept target folder and options.
Handle filename collisions (e.g., append suffix or timestamp).
Option to move to trash (send2trash) instead of permanently moving.
Add configurable exclude patterns (folders or filename globs).
Add logging (file-based) and unit tests.

## Installation

```bash
git clone https://github.com/<your-username>/downloads-sorter.git
cd downloads-sorter
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
pip install -r requirements.txt  # optional (no external deps required)
