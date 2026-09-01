# Cloud Development Environment with Agentic AI — Level 1, 2 & 3

## Purpose
This repository is the intern submission for the assignment "Cloud Development Environment with Agentic AI," covering all three tracks:
- **Level 1 (Beginner):** a small Python app built with an AI coding assistant inside a browser-based cloud workspace.
- **Level 2 (Intermediate):** a real tool-calling AI agent, running inside the same cloud workspace.
- **Level 3 (Advanced):** the Level 2 agent extended into a two-tool orchestrator, evaluated for production readiness.

## Selected tracks
All three levels were completed, per supervisor confirmation (phone call, after initial "Start level 1" instruction, later expanded to cover all three levels plus a consolidated presentation and a final website).

---

## Level 1 — To-Do CLI app

A command-line To-Do List manager: add a task, list tasks, mark a task complete, remove a task, exit. In-memory storage only (no persistence between runs, by design).

**Run:**
```
python3 src/todo.py
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
python3 src/agent.py
```
Type a question (e.g. "What's the weather in Dubai?" or "What is 5 + 5?"), or `exit` to quit. Each run prints the request, which tool (if any) was selected, the tool's input/output, the final answer, and latency.

**Test:**
```
pytest -v
```
Covers Level 1's 3 tests plus Level 2's tool-calling test scenarios (successful weather lookup, invalid city / tool failure, and a non-weather question that triggers no tool call).

---

## Level 3 — Orchestrated multi-tool agent + production readiness

The Level 2 agent was extended with a **second tool**, turning it into a real orchestrator that routes between two capabilities at runtime:
- `get_weather` (Open-Meteo, existing from Level 2)
- `convert_currency` (Frankfurter API — free, keyless, ECB reference rates)

**What's new at this level (beyond just "another tool"):**
- **Least-privilege boundary:** every tool call passes through a single allow-list checkpoint (`_execute_tool()` in `agent.py`) before executing — an unauthorized or unexpected tool name is rejected, never run.
- **Traceability:** every request gets a short UUID, logged alongside which tool was selected, its input/output, the final answer, and latency.
- **Prompt-injection defense:** the system instruction explicitly tells the model to treat tool results and user input as untrusted data, not as commands — tested directly in the eval suite.
- **Evaluation suite:** `tests/test_level3_eval.py` — 10 tests across 5 required categories (correctness, unsafe tool requests, prompt injection, timeouts, malformed tool output), all deterministic (mocked network calls, no live API cost per run).
- **Deployment definition:** `app.py` (Flask wrapper exposing `POST /ask`) + `Dockerfile` — provided as a reproducible deployment definition. **Not live-deployed**, and the Docker build itself wasn't verified in this Codespace (Docker isn't installed there by default) — disclosed honestly rather than claimed as tested.
- **Production-readiness assessment:** `docs/level3-production-readiness.md` covers the orchestration pattern, why MCP wasn't used (Gemini 3 doesn't support remote MCP yet, per official docs), secret/rollback approach, and a full assessment of lock-in, data residency, private networking, identity federation, model choice, observability, and unit economics — plus an honest list of production gaps.

**Run (same agent, now with 2 tools):**
```
python3 src/agent.py
```
Try: `What's the weather in Tokyo?` or `Convert 100 USD to EUR` or `What is 5+5?` (no tool needed).

**Test:**
```
pytest -v
```
16 tests total (3 Level 1 + 3 Level 2 + 10 Level 3).

---


## Setup (all levels)
1. Open this repository in GitHub Codespaces (Code → Codespaces tab → Create codespace on main). The `.devcontainer/devcontainer.json` pins Python 3.12 and auto-installs dependencies.
2. Confirm Python: `python3 --version`
3. Dependencies are auto-installed via the devcontainer, or manually: `pip3 install -r requirements.txt`
4. Set `GEMINI_API_KEY` as a Codespaces secret before running `agent.py` (see Level 2/3 sections above).

## Known limitations
- Level 1's To-Do app has no persistence and no agent runtime by design (coding-assistant-assisted, not agentic — see `docs/architecture.md`).
- The Level 2/3 agent currently runs locally inside the Codespace rather than behind a deployed public endpoint — a deployment definition (`app.py`, `Dockerfile`) is provided but not live-deployed; see `docs/level3-production-readiness.md` for the reasoning and reproducible commands.
- The Docker build itself was not verified in this Codespace environment (Docker isn't installed there by default) — disclosed honestly rather than claimed as tested.
- The Google and AWS comparison entries in `docs/comparison.md` are documentation-based, not hands-on tested, per Level 1 scope.
- Some pricing figures in `docs/security-cost.md` and `docs/level3-production-readiness.md` are flagged as unconfirmed against live pricing pages at submission time, per the assignment's instruction to disclose rather than guess.
- The agent has no persistent memory across separate user turns (stateless per-request design) — a disclosed scope choice, not a bug.

## Repository structure
```
README.md                  This file
todo.py                     Level 1: To-Do CLI source
agent.py                    Level 2/3: Gemini multi-tool orchestrator
weather_tool.py              Weather tool (Open-Meteo)
currency_tool.py              Level 3: Currency conversion tool (Frankfurter)
app.py                       Level 3: Flask HTTP wrapper (deployment definition)
Dockerfile                    Level 3: Reproducible container build definition
tests/test_todo.py           Level 1 automated tests
tests/test_agent.py           Level 2 automated tests
tests/test_level3_eval.py     Level 3 evaluation suite (5 required categories)
conftest.py                   pytest path configuration
requirements.txt              Pinned dependencies (pytest, google-genai, requests, flask)
.gitignore                    Excludes cache/venv artifacts
.devcontainer/devcontainer.json  Reproducible workspace config
docs/comparison.md             Scorecard: Microsoft vs Google vs AWS
docs/architecture.md           Architecture diagrams (Level 1 + Level 2) and explanation
docs/security-cost.md          Security analysis and cost model (Level 1 + 2)
docs/level3-production-readiness.md  Level 3: orchestration, MCP decision, least privilege,
                                       deployment, full production-readiness assessment
docs/executive-recommendation.md  Executive summary
demo/                          Screenshots / evidence (all 3 levels)
```

## Declaration
I confirm that I tested or directly verified every claim marked as tested, cited the source of factual platform claims, disclosed where AI assistance was used, and did not include confidential information or credentials in this submission.