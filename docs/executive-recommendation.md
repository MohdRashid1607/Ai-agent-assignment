# Executive Recommendation

## Selected stack
**Microsoft — GitHub Codespaces + GitHub Copilot + Microsoft Foundry**

## Runner-up
**Google (Cloud Workstations + Gemini Code Assist + Vertex AI Agent Builder)** and **AWS (developer tooling + Amazon Q Developer + Bedrock AgentCore)** tied at 71/100 each — see `docs/comparison.md` for the full weighted breakdown.

## Decision
Microsoft scored 86/100 against Google and AWS's 71/100, driven by categories verified hands-on across all three levels of this prototype rather than assumed from documentation: cloud developer experience, agentic coding capability, and observability. A working To-Do CLI app (Level 1), a real tool-calling agent (Level 2), and a two-tool orchestrator with a tested prompt-injection defense and a 10-case eval suite (Level 3) were all built end-to-end in a GitHub Codespace — all evidence is in this repository.

## Major tradeoffs
- **Microsoft's advantage is partly a fairness gap, not just a technical one:** it is the only stack tested hands-on. Google and AWS were scored from current official documentation, not live accounts. This is disclosed as a limitation below, not hidden.
- **Google's biggest risk is a live migration event, not a hypothetical one:** Gemini Code Assist's free individual-tier IDE extension was deprecated on June 18, 2026, with users redirected to a new tool ("Antigravity") — a genuine disruption risk for any team relying on the free tier today.
- **AWS's agent runtime (Bedrock AgentCore) is arguably more modular and framework-agnostic** than Microsoft Foundry (supports LangChain, Strands, custom frameworks, any model) — and Microsoft's own Foundry Agent Service was not directly exercised either (this prototype's agent brain is Gemini's API via a custom orchestrator, not Foundry, after GitHub Models was retired). Neither stack's managed agent-runtime service was hands-on tested.
- **Cost could not be fully pinned down for any stack.** Exact current per-seat and per-compute-hour pricing was not independently re-verified against live pricing pages at submission time for any of the three stacks — flagged transparently in `docs/security-cost.md` rather than estimated as fact.

## Next step
Before treating this as a final platform decision at a team level, a hands-on prototype should be run on Google and AWS as well, so all three stacks are judged on tested evidence rather than mixing tested (Microsoft) against documented (Google, AWS) evidence — this asymmetry is the single biggest limitation of this result.