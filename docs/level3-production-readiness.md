# Level 3 — Production Readiness Assessment

## Orchestration pattern and state boundaries

**Pattern:** single-orchestrator, multi-tool routing. One agent (Gemini 3.6 Flash, via the `google-genai` SDK's Interactions API) receives every user request and decides, per request, whether to answer directly or call one of two available tools (`get_weather`, `convert_currency`). This is simpler than a multi-agent handoff pattern, and was chosen deliberately: the assignment allows "two tools OR two specialized agent roles," and two tools under one orchestrator avoids the added complexity of inter-agent handoff/state-passing logic that a true multi-agent design would need, while still demonstrating real tool-selection reasoning at runtime.

**State boundaries:** each user request is stateless at the process level - `run_agent()` takes a single string in, returns a single string out, with no shared mutable state between calls. Conversation continuity within one exchange (the model's decision → tool execution → final answer) is carried via Gemini's own `previous_interaction_id`, scoped to that one exchange only. There is no persistent memory across separate user turns in this prototype; each call to `run_agent()` starts a fresh interaction. This is a real, disclosed limitation - not accidental - since Level 3's scope is orchestration and production-readiness assessment, not conversational memory design.

**Agent framework/managed service used:** Google's Gemini API (`google-genai` SDK, Interactions API), a managed LLM service handling the model call and function-calling protocol; no self-hosted agent framework (e.g. LangChain, CrewAI) was layered on top, since the SDK's native tool-calling loop was sufficient for two tools under one orchestrator.

## MCP (Model Context Protocol) decision

**MCP was not used.** Justification, based on current official documentation checked during this project: Google's own Gemini API documentation states remote MCP is not yet supported by Gemini 3 models ("Gemini 3 does not support remote MCP, this is coming soon"). Since the agent's brain in this prototype is Gemini 3.6 Flash, MCP is not currently a viable protocol for this specific stack.

**What was used instead:** the SDK's native JSON-schema function-calling protocol (`type: "function"` tool declarations passed directly to `interactions.create`). This is Google's own first-class, currently-supported tool-calling mechanism for this model family, and is functionally equivalent to MCP's tool-description approach at a schema level - both describe a tool's name, description, and structured parameters. Once Gemini's remote MCP support ships, migrating from ad-hoc function declarations to MCP tool servers would be a moderate refactor, not a full rewrite, since the input (structured tool schemas) and output (structured results) shapes are conceptually similar.

## Least privilege, secret management, traceability, rollback

**Least privilege:** all tool execution passes through a single chokepoint, `_execute_tool()` in `agent.py`, which checks every requested tool name against an explicit allow-list (`ALLOWED_TOOLS = {"get_weather", "convert_currency"}`) before anything runs. A request for any other tool name - whether from a legitimate model quirk or an adversarial prompt-injection attempt - is rejected with a structured error and never executed. This is the single security boundary in the system; evaluation tests (`test_unsafe_tool_request_is_blocked`, `test_prompt_injection_via_tool_name_is_blocked`) verify it directly.

**Secret management:** `GEMINI_API_KEY` is stored as a GitHub Codespaces repository secret, injected as an environment variable at container start, read via `os.getenv()`, never hardcoded or committed. The agent raises immediately if the key is missing rather than failing silently. Neither of the two tools (`get_weather`, `convert_currency`) requires any credential at all - both call fully keyless public APIs (Open-Meteo, Frankfurter) - which minimizes the system's overall secret surface area to exactly one value.

**Traceability:** every request is assigned a short UUID-based `request_id` at the start of `run_agent()`, and every log line for that request (tool selected, tool input, tool result, final answer, latency) is tagged with it. This lets a reviewer follow one request's full path through the system even if multiple requests interleave in output, and is the basis for the runtime evidence screenshots in `demo/`.

**Rollback/versioning approach:** version control via Git is the rollback mechanism for this prototype - every meaningful change was committed and pushed incrementally (visible in the repo's commit history), so reverting to any prior working state (e.g. before the two-tool orchestration change) is a standard `git revert`/`git checkout` operation. At production scale, this would be extended with Git tags per release (e.g. `v1-level1`, `v2-level2`, `v3-level3`) and, for the deployed container specifically, image tagging (e.g. `ai-agent-level3:v1`, `:v2`) so a bad deployment could be rolled back to a specific prior image rather than relying on rebuilding from source history alone.

## Deployment / infrastructure definition

See `Dockerfile` and `app.py` at the repository root: a minimal Flask wrapper exposes `run_agent()` as a `POST /ask` HTTP endpoint plus a `GET /health` check, containerized via a `python:3.12-slim`-based Dockerfile that installs pinned dependencies and never bakes the API key into the image (it must be injected at run time via `-e GEMINI_API_KEY=...` or the hosting platform's secret manager).

**Disclosed limitation:** the Docker build itself was not verified in this Codespace environment, since Docker is not installed by default in this container image. The Dockerfile and reproducible build/run commands are provided as the deployment definition required by the assignment, but an actual container build/run was not executed as part of this submission - stated honestly rather than claimed as tested.

**Reproducible commands (as documented in the Dockerfile):**
```
docker build -t ai-agent-level3 .
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key_here ai-agent-level3
curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{"question": "What is the weather in Dubai?"}'
```

## Assessment: lock-in, residency, networking, identity, model choice, observability, unit economics

**Vendor lock-in:** moderate. The agent's tool-calling logic (`_execute_tool`, the allow-list pattern, structured tool schemas) is largely portable to another LLM provider's function-calling API with moderate refactoring. The deeper lock-in risk is the `google-genai` SDK's specific Interactions API shape (`previous_interaction_id`, `steps`, `output_text`) - switching to, say, OpenAI's or Anthropic's tool-calling API would require rewriting the orchestration loop in `run_agent()`, though the two tool modules (`weather_tool.py`, `currency_tool.py`) would need zero changes since they're provider-agnostic plain Python.

**Data residency:** not controlled or verified in this prototype. Gemini API requests are sent to Google's infrastructure; the specific region(s) processing this project's requests were not configured or confirmed. For a production deployment with residency requirements, this would need explicit region-pinning via Vertex AI's regional endpoints rather than the general-availability Gemini API used here.

**Private networking:** none implemented. All calls (to Gemini, Open-Meteo, Frankfurter) go over the public internet from within the Codespace. A production deployment handling sensitive data would need a VPC/private-endpoint setup for the agent-to-model traffic at minimum; the two public tool APIs, being public read-only data sources, don't warrant private networking.

**Identity federation:** not implemented. Authentication in this prototype is a single static API key, not federated identity (e.g. OIDC/SAML-based service identity, Azure Managed Identity, GCP Workload Identity Federation). At production scale, a managed identity approach would remove the need to manage and rotate a static key manually.

**Model choice:** Gemini 3.6 Flash was chosen for cost/speed (Flash tier) with adequate tool-calling reliability observed in this prototype's manual testing (both tools were correctly selected and correctly skipped for non-tool questions across all runtime evidence). The original plan (GitHub Models) was found retired during this project - a real example of why model/vendor choice needs re-verification at build time, not assumed from outdated documentation.

**Observability:** minimal in this prototype - structured console logging with request IDs and latency only. No centralized log aggregation, no tracing dashboard, no alerting. At production scale, this would need to feed into a real observability platform (e.g. Cloud Logging, Application Insights, or an OpenTelemetry-based pipeline) rather than console output alone.

**Unit economics:** at the assignment's reference scenario (5 developers, 160 workspace-hours each, 20 working days, ~50,000 agent requests/month), the fastest-growing cost is Gemini API token usage if the free tier's request-per-minute/day limits are exceeded - Gemini 3.6 Flash is priced at $1.50/1M input tokens and $7.50/1M output tokens at the time of writing (not independently re-verified against a live pricing page at submission time, per the assignment's disclosure requirement). Since each `run_agent()` call may issue two full model round-trips (initial decision + post-tool-result final answer) rather than one, actual token cost per user question is roughly double a single-turn estimate - a real assumption worth flagging, since it is the main driver of cost growth at scale, more than either tool API (both free/keyless).

## Threat notes (informal)

- **Prompt injection via user input or tool output:** partially mitigated via the system instruction explicitly telling the model to treat tool results and embedded text as untrusted data, plus the allow-list boundary that blocks unauthorized tool execution regardless of what the model is told to do. Not formally red-teamed beyond the two eval tests provided.
- **Secret exposure via logs:** logging only prints tool inputs/outputs and final answers, never the API key itself - verified by code inspection, not automated scanning.
- **Unbounded tool retries/cost:** no rate-limiting or retry-budget logic exists yet; a malicious or buggy client hitting the (currently undeployed) `/ask` endpoint repeatedly could drive up Gemini API cost with no circuit breaker in place - a genuine gap.

## Production-readiness gaps (honest list)

1. No live deployment/hosting - local-in-Codespace and containerization definition only, Docker build unverified in this environment
2. No rate-limiting, abuse protection, or cost circuit-breaker on the (currently undeployed) HTTP endpoint
3. No data residency or private networking controls
4. No identity federation - single static API key
5. No centralized observability/tracing beyond console logs
6. No persistent conversation memory across turns (stateless per-request design, disclosed as intentional scope, not a bug)
7. Threat modeling is informal/manual, not a formal red-team or automated adversarial test suite