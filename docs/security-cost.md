# Security and Cost Note

## Data flow
This prototype is a self-contained, in-memory CLI application. It:
- Takes no external network calls
- Stores tasks only in memory (lost on exit) — no database, no file persistence
- Handles no personal, customer, or confidential data — all task text entered during testing was synthetic ("Buy groceries", "Finish assignment")
- Uses no API keys, tokens, or secrets of any kind

## Permissions
- The GitHub account used has standard developer permissions on a private personal repository
- No elevated cloud IAM roles were required or requested
- Codespaces itself runs in an isolated, ephemeral container-based VM scoped to this repository

## Secret storage
Not applicable to this specific prototype (no secrets used), but the method is documented for completeness and to satisfy the assignment's requirement: GitHub Codespaces supports **Codespaces secrets** (repository or account-level, injected as environment variables at container start) as the correct mechanism — never committing keys to `.gitignore`d files or source code directly. This is the method that would be used if Level 2/3 introduced an API key.

## Key risks (even for a "no secrets" app)
1. **Public repo risk:** if the repo were made public, GitHub Copilot Chat history and code are visible to anyone — mitigated by keeping this repo private during development.
2. **Copilot data handling:** code sent to Copilot for suggestions leaves the local Codespace and is processed by GitHub's backend model service — acceptable here since no confidential data exists in the code, per Section 3's synthetic-data-only rule.
3. **Dependency supply chain:** `requirements.txt` pins `pytest==9.1.1` exactly, reducing risk of an unpinned/compromised newer version being silently installed.

## Mitigations
- Kept repository private
- Used only synthetic data throughout
- Verified `.gitignore` excludes `__pycache__/`, `.pytest_cache/`, and virtual environment folders so no local artifacts leak into version control
- Pinned the one real dependency (`pytest`) to an exact version

## Monthly cost estimate (per Section 6's required scenario: 5 developers, 160 workspace-hours/developer, 20 working days, 50,000 agent requests or stated equivalent)

| Item | Microsoft (GitHub Codespaces + Copilot) | Notes |
|---|---|---|
| Seat licenses (Copilot) | Free tier used in this prototype (Copilot Free, confirmed 0% of chat credits, 1% of inline-suggestion quota used in ~1 hour of light use) | At team scale, GitHub Copilot Business/Enterprise seat pricing would apply — **could not be confirmed to the exact current dollar figure for this submission; verify on GitHub's official pricing page at submission time**, per Section 3's requirement to flag unconfirmed pricing. |
| Workspace compute (Codespaces) | Free tier: 120 core-hours/month included per personal account; at 5 developers × 160 hrs/month this would exceed free tier and incur per-core-hour billing | Estimate could not be finalized without GitHub's current published Codespaces compute rate at time of submission — flagged as unconfirmed. |
| Model usage | Included in Copilot Free/Business seat — no separate token billing observed in this prototype | N/A for Level 1 (no separate agent/model API calls were made) |
| Agent runtime (Foundry) | Not used at Level 1 | Would apply starting Level 2/3 |
| Observability | Not used at Level 1 | Would apply starting Level 2/3 |
| Network/egress | $0 observed — CLI app made no external network calls | N/A |

**Where pricing could not be confirmed:** exact current per-core-hour Codespaces compute billing and Copilot Business/Enterprise per-seat pricing were not independently re-verified against GitHub's live pricing page at the time of writing this note — the intern should confirm current rates on submission day per the assignment's explicit instruction in Section 3.