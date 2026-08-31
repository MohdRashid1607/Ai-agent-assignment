# Executive Recommendation

## Selected stack
**Microsoft — GitHub Codespaces + GitHub Copilot + Microsoft Foundry**

## Runner-up
**Google (Cloud Workstations + Gemini Code Assist + Vertex AI Agent Builder)** and **AWS (developer tooling + Amazon Q Developer + Bedrock AgentCore)** tied at 71/100 each — see `docs/comparison.md` for the full weighted breakdown.

## Decision
Microsoft scored 86/100 against Google and AWS's 71/100, driven by categories that were verified hands-on in this prototype rather than assumed from documentation: cloud developer experience, agentic coding capability, and DevOps/Git integration. A working To-Do CLI application was built end-to-end in a GitHub Codespace using GitHub Copilot (Free tier) for code generation, with two real bugs found, diagnosed, and fixed, and three automated tests passing — all evidence is in this repository.

## Major tradeoffs
- **Microsoft's advantage is partly a fairness gap, not just a technical one:** it is the only stack tested hands-on at Level 1. Google and AWS were scored from current official documentation, not live accounts, per this track's scope. This is disclosed as a limitation below, not hidden.
- **Google's biggest risk is a live migration event, not a hypothetical one:** Gemini Code Assist's free individual-tier IDE extension was deprecated on June 18, 2026, with users redirected to a new tool ("Antigravity") — a genuine disruption risk for any team relying on the free tier today.
- **AWS's agent runtime (Bedrock AgentCore) is arguably more modular and framework-agnostic** than Microsoft Foundry (supports LangChain, Strands, custom frameworks, any model), which could matter more at Level 2/3 where the actual agent runtime is exercised, rather than at Level 1 where only the coding-assistant layer was tested.
- **Cost could not be fully pinned down for any stack.** Exact current per-seat and per-compute-hour pricing was not independently re-verified against live pricing pages at submission time for any of the three stacks — flagged transparently in `docs/security-cost.md` rather than estimated as fact.

## Next step
Before treating this as a final platform decision at a team level, a Level 2/3-style hands-on prototype should be run on Google and AWS as well, so all three stacks are judged on tested evidence rather than mixing tested (Microsoft) against documented (Google, AWS) evidence — this asymmetry is the single biggest limitation of this Level 1 result.