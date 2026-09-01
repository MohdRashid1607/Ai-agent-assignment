# Architecture

## Level 1 — Coding-assistant-built CLI app

```
[You, browser]
      |
      v
[GitHub.com] ---------------------------------+
      |                                        |
      | opens                                  | stores
      v                                        v
[GitHub Codespace]                       [Git Repository]
  (cloud VM, browser VS Code)             (todo.py, tests/, docs/)
      |
      v
[Python 3.12 runtime, in-VM]
      |
      | assisted by
      v
[GitHub Copilot Free]  (suggests code; not present at runtime)
```
The To-Do CLI is deterministic, rule-based code (`if/elif` branches). Copilot helped *write* it but is not involved when it *runs*. No AI component executes at runtime in Level 1.

## Level 2 — Tool-calling weather agent

```
[You, terminal in Codespace]
        |
        | text question
        v
[agent.py - run_agent()]
        |
        | interaction.create(model, input, tools=[WEATHER_TOOL])
        v
[Gemini 3.6 Flash]  <-- authenticated via GEMINI_API_KEY (Codespaces secret)
        |
        | model decides: answer directly, OR call a tool
        v
   +---------+-----------------------------+
   | no tool needed                        | tool call: get_weather(city)
   v                                        v
[Gemini answers directly]          [weather_tool.py]
                                            |
                                            | HTTPS, keyless
                                            v
                                  [Open-Meteo geocoding + forecast APIs]
                                            |
                                            v
                                  structured result: {status, city,
                                  temperature_c, windspeed_kmh, ...}
                                  OR {status: "error", reason: ...}
                                            |
                                            | sent back via
                                            | previous_interaction_id
                                            v
                                  [Gemini 3.6 Flash - final answer]
                                            |
                                            v
                                  [printed to user + logged:
                                   request, tool selected, tool input,
                                   tool result, final answer, latency]

                                            |
                                            | (not yet live - see
                                            |  Deployment plan below)
                                            v
                                  [Deployment target: containerized
                                   Flask endpoint (app.py + Dockerfile),
                                   e.g. Azure Container Apps - defined,
                                   not deployed in this submission]
```

## Plain-language explanation

**Where the code runs:** Inside the same GitHub Codespace VM as Level 1 - `agent.py` executes as a normal Python process in that cloud VM, not on your local machine.

**Where the AI model runs:** Gemini 3.6 Flash runs on Google's infrastructure, not in the Codespace. `agent.py` sends the user's text to Gemini's API over HTTPS and receives back either a direct answer or a tool-call instruction - the model itself is remote.

**Where the tool runs:** `get_weather()` executes locally, inside the Codespace, as plain Python - it makes its own separate HTTPS calls to Open-Meteo (a different, unrelated service from Gemini). The result is sent back to Gemini as text so the model can compose a final natural-language answer.

**Is this actually agentic, unlike Level 1?** Yes - this is the key difference the assignment is testing for. Gemini decides *at runtime, per request* whether a tool is needed at all (a math or greeting question gets answered directly; a weather question triggers a tool call) - that decision is not hardcoded by the developer. Level 1's Copilot never runs at request-time and never decides anything; it only assisted during development.

**Where the secret lives:** `GEMINI_API_KEY` is stored as a GitHub Codespaces repository secret (Settings -> Codespaces -> repository secrets), injected into the Codespace as an environment variable at container start. It is never committed to the repository, never hardcoded in `agent.py` (the code reads it via `os.getenv("GEMINI_API_KEY")` and raises a clear error if missing, rather than failing silently or falling back to a hardcoded value).

## Deployment plan

The Level 2 agent currently runs **locally inside the cloud-hosted GitHub Codespace** (a terminal-based CLI loop), not behind a deployed public HTTP endpoint. This is explicitly permitted by the assignment when the selected trial/tier doesn't readily support endpoint deployment — the free tiers used here (Codespaces, Gemini API free tier) are oriented around interactive/dev use, not production hosting.

**Why not deployed now:** exposing a public endpoint would require either (a) a paid hosting tier (Azure App Service, Cloud Run, etc.) with its own cost and IAM setup, or (b) keeping the Codespace running continuously and exposing its port publicly — both add real cost and security surface area (a public endpoint calling a paid API needs its own auth, rate-limiting, and abuse protection) that isn't justified for a Level 2 prototype demo.

**If deployment were required next:**
1. Wrap `agent.py`'s `run_agent()` function in a minimal Flask or FastAPI app with a single `POST /ask` endpoint.
2. Deploy that app to a free/low-cost container host (e.g. Azure Container Apps consumption tier, Google Cloud Run free tier, or Render's free web service tier) — to keep consistent with the Microsoft-first stack, Azure Container Apps would be the first choice to trial.
3. Move `GEMINI_API_KEY` from a Codespaces secret to that platform's equivalent secret manager (e.g. Azure Key Vault reference or Container Apps secret) — same principle, different vault.
4. Add basic rate-limiting and input validation at the endpoint layer before accepting public traffic, since a public endpoint calling a metered external API needs abuse protection that a local CLI tool run by a single trusted user does not.
5. Re-run the same 3+ test scenarios against the deployed endpoint (not just the local function) to confirm parity.

## Components mapped to the assignment's required layers

| Layer | Level 1 | Level 2 |
|---|---|---|
| Cloud workspace | GitHub Codespaces | GitHub Codespaces (same repo) |
| Coding agent | GitHub Copilot Free (dev-time only) | GitHub Copilot Free (dev-time only) |
| Agent runtime | Not applicable | Gemini 3.6 Flash via `google-genai` SDK, tool-calling loop in `agent.py` |
| Tool | None | `weather_tool.py` -> Open-Meteo (keyless, public) |
| Secrets | None needed | `GEMINI_API_KEY` as a Codespaces repository secret |
| Delivery | Git commit/push | Git commit/push; `requirements.txt` pins `google-genai`, `requests`, `pytest` |