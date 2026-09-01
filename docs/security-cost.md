# Security and Cost Note

## Region, model, and runtime record

Per the assignment's rule to record region, model, and runtime used:
- **Model:** Gemini 3.6 Flash (`gemini-3.6-flash`), Google's Gemini API, free tier
- **Runtime:** GitHub Codespaces (cloud VM), Python 3.12.14
- **Region:** not explicitly pinned or confirmed for either GitHub Codespaces or the Gemini API in this prototype — both were used via their general-availability endpoints without selecting a specific region. This is disclosed as a gap: a production deployment with data residency requirements would need to explicitly confirm and pin the region for both the compute (Codespaces/hosting) and the model API call (e.g. via Vertex AI's regional endpoints for Gemini, rather than the general API used here).
- **Paid features used:** none — Codespaces free tier, Copilot Free tier, Gemini API free tier, Open-Meteo and Frankfurter (both fully free/keyless) were used throughout.

## Data flow

**Level 1 (To-Do CLI):** self-contained, in-memory app. No external network calls, no persistence, no secrets. Synthetic task data only ("Buy groceries", etc.).

**Level 2 (Weather agent):** a real external data flow now exists:
1. User types a question in the Codespace terminal.
2. `agent.py` sends the question over HTTPS to Google's Gemini API (authenticated with `GEMINI_API_KEY`).
3. If Gemini decides a tool is needed, `agent.py` calls `weather_tool.py` locally, which makes its own separate HTTPS calls to Open-Meteo's geocoding and forecast APIs (keyless, no auth).
4. The tool's structured result is sent back to Gemini (as text) to compose the final answer, which is printed to the user and logged.

No personal or confidential data flows through this pipeline — inputs are city names and general questions, not user accounts, private data, or credentials.

## Permissions
- Standard GitHub developer permissions on a private personal repository — no elevated cloud IAM roles.
- Codespaces runs in an isolated, ephemeral container-based VM scoped to this repository.
- The Gemini API key is scoped to a personal Google AI Studio account with free-tier access; it grants no access beyond calling the Gemini API itself.

## Secret storage
`GEMINI_API_KEY` is stored as a **GitHub Codespaces repository secret** (Settings → Codespaces → repository secrets), scoped only to this repository. It is injected as an environment variable automatically when the Codespace starts.

- The code reads it via `os.getenv("GEMINI_API_KEY")` in `agent.py`.
- If the variable is missing, the agent raises a clear `RuntimeError` immediately rather than silently failing or falling back to a hardcoded value.
- The key is never written into any source file, never committed to Git, and `.gitignore` excludes any local `.env`-style file should one be added later.
- Verification method used (safe, does not expose the key): `echo $GEMINI_API_KEY | wc -c` — confirms the variable is set and non-empty without ever printing its value.

**A real lesson learned:** during setup, the Codespace's default `GITHUB_TOKEN` (a separate, short-lived, session-scoped token GitHub auto-generates) was accidentally shown in a chat conversation with an AI assistant while debugging. It was not committed to the repository and is session-scoped/auto-rotated, so the practical exposure was minimal — but it is documented here as a real, concrete example of why secret values should never be pasted anywhere outside their intended secret store, even in a low-risk context.

## Key risks
1. **Public repo risk:** if made public, code and Copilot history are visible to anyone — mitigated by keeping the repo private.
2. **Third-party data handling:** the Gemini API and Open-Meteo both receive request data (the user's question and city name respectively) as part of normal operation — acceptable here since no confidential data is ever entered, per the assignment's synthetic-data-only rule.
3. **Dependency supply chain:** `requirements.txt` pins exact versions (`pytest==9.1.1`, `google-genai==2.20.0`, `requests==2.34.2`) rather than leaving them unpinned.
4. **Tool failure handling:** `weather_tool.py` wraps all external calls in `try/except` and always returns a structured `{"status": "error", "reason": ...}` dict rather than raising an unhandled exception that could crash the agent loop or leak a raw stack trace to the end user.
5. **Unsupported tool requests:** if the model ever requested a tool name other than `get_weather`, `agent.py` returns a structured error rather than attempting to execute an undefined function.

## Mitigations
- Repository kept private
- Only synthetic/public data used throughout (task text, city names)
- Secret stored via Codespaces secrets, never in source or Git history
- All dependencies pinned to exact versions
- All external calls (Gemini, Open-Meteo) wrapped in error handling with structured, non-crashing failure responses

## Monthly cost estimate (per required scenario: 5 developers, 160 workspace-hours/developer, 20 working days)

| Item | Detail | Notes |
|---|---|---|
| Codespaces compute | Free tier: 120 core-hours/month per personal account; 5 developers × 160 hrs/month would exceed this | Exact per-core-hour overage rate not independently re-verified against GitHub's live pricing page at submission time — flagged as unconfirmed per Section 3. |
| GitHub Copilot | Free tier used throughout this prototype (0% chat credits used at last check) | Team-scale Business/Enterprise seat pricing not independently re-verified at submission time. |
| Gemini API (agent brain) | Free tier used throughout (no billing enabled); paid tier is $1.50 / 1M input tokens and $7.50 / 1M output tokens for Gemini 3.6 Flash if free-tier limits were exceeded at scale | Confirmed from Google's own model pricing announcement at time of writing; should still be re-checked on submission day since pricing can change. |
| Open-Meteo (tool) | $0 — free, keyless public API, no billing tier used | N/A |
| Observability | Not implemented beyond console logging in this prototype | Would need a dedicated logging/observability service at production scale |

**Where pricing could not be fully confirmed:** exact current GitHub Codespaces per-core-hour overage billing and Copilot Business/Enterprise per-seat pricing were not independently re-verified against live pricing pages at the time of writing — the intern should confirm current rates on submission day, per the assignment's explicit instruction.