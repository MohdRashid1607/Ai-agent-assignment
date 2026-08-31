# Level 1 — Cloud Development Environment with Agentic AI

## Purpose
This repository is the Level 1 (Beginner) submission for the internship assignment "Cloud Development Environment with Agentic AI." It demonstrates building a small Python application inside a browser-based cloud workspace (GitHub Codespaces), using an AI coding assistant (GitHub Copilot) to generate and improve the code, then testing and correcting the result.

## Selected track
**Level 1 — Beginner: Explore and demonstrate** (assigned by supervisor).

## What this app does
A simple command-line To-Do List manager: add a task, list tasks, mark a task complete, remove a task, exit. Tasks are stored in memory for the session (no persistence between runs by design, per Level 1 scope).

## Setup
1. Open this repository in GitHub Codespaces (Code → Codespaces tab → Create codespace on main).
2. Confirm Python is available: `python3 --version` (tested on Python 3.12.1).
3. Install dependencies: `pip3 install -r requirements.txt`

## Run
```
python3 todo.py
```
Follow the on-screen menu (1–5) to add, list, complete, or remove tasks, or exit.

## Test
```
pytest tests/test_todo.py -v
```
3 automated tests are included, covering: adding a task, completing a task, and removing a task.

## AI assistance disclosure
GitHub Copilot (Free tier) was used to generate the initial implementation of all four core functions (`add_task`, `list_tasks`, `complete_task`, `remove_task`) and the `main()` menu loop, from descriptive comments. Two corrections were made by the intern after review:
1. Copilot's generated code was missing the `if __name__ == "__main__": main()` entry point, so the script did nothing when run — fixed by the intern.
2. The menu's number-entry prompts crashed with `ValueError` on non-numeric input — fixed by the intern by wrapping the conversions in `try/except ValueError`.

Full prompt-by-prompt evidence, before/after screenshots, and terminal output are in `demo/`.

## Known limitations
- No data persistence — tasks are lost when the program exits (in-memory only, acceptable at Level 1 scope)
- No external tool calls, APIs, or agent runtime — this is a coding-assistant-assisted app, not an agentic application (see `docs/architecture.md` for the distinction)
- The Google and AWS comparison entries in `docs/comparison.md` are documentation-based, not hands-on tested, per Level 1 track requirements

## Repository structure
```
README.md              This file
todo.py                 Application source
tests/test_todo.py      Automated tests
conftest.py              pytest path configuration
requirements.txt         Pinned dependency (pytest)
.gitignore               Excludes cache/venv artifacts
docs/comparison.md        Scorecard: Microsoft vs Google vs AWS
docs/architecture.md      Architecture diagram and explanation
docs/security-cost.md     Security analysis and cost model
demo/                     Screenshots / evidence
```

## Declaration
I confirm that I tested or directly verified every claim marked as tested, cited the source of factual platform claims, disclosed where AI assistance was used, and did not include confidential information or credentials in this submission.