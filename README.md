# Cloud Development Environment with Agentic AI — Level 1 & Level 2

## Purpose
This repository is the intern submission for the assignment "Cloud Development Environment with Agentic AI," covering:
- **Level 1 (Beginner):** a small Python app built with an AI coding assistant inside a browser-based cloud workspace.
- **Level 2 (Intermediate):** a real tool-calling AI agent, running inside the same cloud workspace.

## Selected tracks
Both **Level 1** and **Level 2** were assigned by the supervisor (confirmed by phone call after initial "Start level 1" instruction).

---

## Level 1 — To-Do CLI app

A command-line To-Do List manager: add a task, list tasks, mark a task complete, remove a task, exit. In-memory storage only (no persistence between runs, by design).

**Run:**
```
python3 todo.py
```

**Test:**
```
pytest tests/test_todo.py -v
```

**AI assistance disclosure:** GitHub Copilot (Free tier) generated the initial implementation of all four core functions and the menu loop from descriptive comments. Two corrections were made by the intern:
1. Missing `if __name__ == "__main__": main()` entry point — script did nothing when run. Fixed.
2. Menu crashed with `ValueError` on non-numeric input. Fixed by wrapping conversions in `try/except ValueError`.

Evidence: `demo/00` through `demo/07` screenshots.

---

## Level 2 — Weather tool-calling agent

A real AI agent: given a natural-language question, **Gemini 3.6 Flash decides at runtime** whether to answer directly or call a weather tool, then composes the final answer from the tool's result.

- **Agent brain:** Google Gemini API (`gemini-3.6-flash`, free tier), via the `google-genai` SDK's Interactions API.
- **Tool:** `weather_tool.py` — calls Open-Meteo's free, keyless geocoding + forecast APIs given a city name.
- **Note on model choice:** the plan originally called for GitHub Models as the agent's brain, but research confirmed GitHub Models was fully retired on July 30, 2026. Pivoted to Google Gemini's free tier instead — a real example of the assignment's "confirm current availability" requirement in practice, not a hypothetical one.

**Setup — secret:**
`GEMINI_API_KEY` must be set as a GitHub Codespaces repository secret (Settings → Codespaces → repository secrets, scoped to this repo). It is injected automatically as an environment variable when the Codespace starts. Never commit this key to source or `.gitignore`d files.

**Run:**
```
python3 agent.py
```
Type a question (e.g. "What's the weather in Dubai?" or "What is 5 + 5?"), or `exit` to quit. Each run prints the request, which tool (if any) was selected, the tool's input/output, the final answer, and latency.

**Test:**
```
pytest -v
```
Covers Level 1's 3 tests plus Level 2's tool-calling test scenarios (successful weather lookup, invalid city / tool failure, and a non-weather question that triggers no tool call).

---

## Setup (both levels)
1. Open this repository in GitHub Codespaces (Code → Codespaces tab → Create codespace on main). The `.devcontainer/devcontainer.json` pins Python 3.12 and auto-installs dependencies.
2. Confirm Python: `python3 --version`
3. Dependencies are auto-installed via the devcontainer, or manually: `pip3 install -r requirements.txt`
4. Set `GEMINI_API_KEY` as a Codespaces secret before running `agent.py` (see Level 2 section above).

## Known limitations
- Level 1's To-Do app has no persistence and no agent runtime by design (coding-assistant-assisted, not agentic — see `docs/architecture.md`).
- Level 2's agent currently runs locally inside the Codespace rather than behind a deployed public endpoint — see the deployment plan in `docs/architecture.md` for the reasoning and next steps.
- The Google and AWS comparison entries in `docs/comparison.md` are documentation-based, not hands-on tested, per Level 1 scope.
- Some pricing figures in `docs/security-cost.md` are flagged as unconfirmed against live pricing pages at submission time, per the assignment's instruction to disclose rather than guess.

## Repository structure
```
README.md                  This file
todo.py                     Level 1: To-Do CLI source
agent.py                    Level 2: Gemini tool-calling agent
weather_tool.py              Level 2: Open-Meteo weather tool
tests/test_todo.py           Level 1 automated tests
tests/ (agent tests)         Level 2 automated tests
conftest.py                   pytest path configuration
requirements.txt              Pinned dependencies (pytest, google-genai, requests)
.gitignore                    Excludes cache/venv artifacts
.devcontainer/devcontainer.json  Reproducible workspace config
docs/comparison.md             Scorecard: Microsoft vs Google vs AWS
docs/architecture.md           Architecture diagrams (Level 1 + Level 2) and explanation
docs/security-cost.md          Security analysis and cost model (both levels)
docs/executive-recommendation.md  Executive summary
demo/                          Screenshots / evidence (both levels)
```

## Declaration
I confirm that I tested or directly verified every claim marked as tested, cited the source of factual platform claims, disclosed where AI assistance was used, and did not include confidential information or credentials in this submission.