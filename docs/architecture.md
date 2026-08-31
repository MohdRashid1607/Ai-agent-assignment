# Architecture — Level 1 Prototype

## Diagram (text form — redraw as an image for the final submission if preferred)

```
[You, browser]
      |
      | HTTPS
      v
[GitHub.com] --------------------------------+
      |                                       |
      | opens                                 | stores
      v                                       v
[GitHub Codespace]                      [Git Repository]
  (cloud VM, browser-based VS Code)      (todo.py, tests/, docs/,
      |                                   requirements.txt, .gitignore)
      | runs
      v
[Python 3.12 runtime, in-VM]
      |
      | assisted by
      v
[GitHub Copilot Free]
  (suggests code inline + via Chat,
   billed against Anthropic/OpenAI-class
   model behind GitHub's own service)
```

## Plain-language explanation

**Where the code runs:** Inside the GitHub Codespace — a temporary cloud virtual machine that GitHub provisions on demand. When you ran `python3 todo.py`, execution happened entirely on that remote VM, not on your local laptop. Your browser is just a window into it (via VS Code's web UI).

**Where the code is stored:** In the GitHub repository (`Ai-agent-assignment`), which is separate from the Codespace VM itself. The VM is ephemeral — if deleted, your code is safe as long as it's committed and pushed to GitHub, which is why we ran `git add`, `git commit`, `git push` after every meaningful change.

**Is the coding assistant "agentic," or is the app itself agentic?**
- **GitHub Copilot (the assistant)** shows agent-*like* behavior: it can read surrounding code/comments, generate multi-line completions, and (in Chat/Agent mode) propose multi-file changes — but in this Level 1 prototype we only used it for single-function completions and manual correction, not autonomous multi-step execution.
- **The To-Do app itself is NOT agentic.** It is a deterministic, rule-based CLI program: given input, it runs fixed branches of code (`if/elif`) with no planning, no tool-calling, and no model inference at runtime. It doesn't decide anything — it just executes what was typed.
- The distinction matters for the assignment's Section 10 question ("difference between the coding agent and the agent you built") — at Level 1 we did not build an agent at all; Copilot was the only AI component involved, used purely as a coding assistant during development, not at runtime.

## Components mapped to the assignment's required layers

| Layer | Component in this prototype |
|---|---|
| Cloud workspace | GitHub Codespaces (this repo) |
| Coding agent | GitHub Copilot Free (inline suggestions + Chat) |
| Agent SDK/runtime | Not applicable at Level 1 — no runtime agent was built |
| Delivery | Git commit/push to GitHub; `requirements.txt` for dependency pinning |
| Enterprise controls | Not exercised at Level 1 (no IAM/secrets were needed — app has no external calls or credentials) |