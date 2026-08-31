# Comparison Scorecard — Cloud Dev Environment + AI Coding Agent (Level 1)

Scoring method: 1 (poor) – 5 (excellent) per category, weighted score = score ÷ 5 × category weight.
Stacks compared: **Microsoft** (GitHub Codespaces + GitHub Copilot + Microsoft Foundry) vs **Google** (Cloud Workstations + Gemini Code Assist + Vertex AI Agent Builder) vs **AWS** (developer tooling + Amazon Q Developer + Bedrock AgentCore).

Note: at Level 1, the Microsoft stack was tested hands-on (this repo). Google and AWS are evaluated from current official documentation only, as permitted for this track — no live account was provisioned for them.

| Category | Weight | Microsoft (tested) | Google (doc-based) | AWS (doc-based) |
|---|---|---|---|---|
| Cloud developer experience | 15% | **5/5** — Codespaces launched in <60s from repo, browser IDE, zero local setup. Evidence: this repo. | **4/5** — Cloud Workstations gives a full preconfigured browser IDE with reproducible "workstation configurations," but requires more upfront GCP project/cluster setup than Codespaces. [Google Cloud Docs](https://docs.cloud.google.com/workstations/docs/overview) | **3/5** — AWS has Cloud9-style and IDE toolkit options, but there isn't a single one-click browser workspace as tightly integrated with the repo host as Codespaces is with GitHub. |
| Agentic coding capability | 15% | **5/5** — Copilot generated all four core functions plus a menu loop from comments; ghost-text and Chat both worked in free tier. Evidence: `evidence-01` to `evidence-02` screenshots, this repo's commit history. | **3/5** — Gemini Code Assist offers agent mode, chat, and code generation, but as of June 18, 2026 the **individual free tier IDE extension was deprecated** in favor of a new tool called "Antigravity" — a real migration risk to flag. [Google Cloud Docs](https://docs.cloud.google.com/gemini/docs/codeassist/overview) | **4/5** — Amazon Q Developer includes autonomous agents that can plan multi-step changes (refactors, dependency upgrades) and a free individual tier via AWS Builder ID, no AWS account required initially. |
| Agent development/runtime | 15% | **4/5** — Microsoft Foundry Agent Service provides managed agent runtime with tools/models/memory (not hands-on tested at Level 1; doc-based for this row). | **4/5** — Vertex AI Agent Builder (Agent Development Kit + Agent Engine) supports multi-agent orchestration and the open Agent2Agent (A2A) protocol, now a Linux Foundation project with 150+ backing organizations. | **4/5** — Bedrock AgentCore is framework-agnostic (LangChain, Strands, custom) with separate Runtime, Memory, Identity, Gateway, and Observability modules — a more modular/composable design than a single all-in-one service. |
| Security and governance | 15% | **4/5** — Microsoft Entra ID + Azure controls (doc-based claim; not exercised hands-on in this Level 1 prototype). | **4/5** — Integrated with Google Cloud IAM; Cloud Audit Logs for admin actions. | **4/5** — Bedrock AgentCore uses scoped, per-session IAM credentials plus CloudTrail audit — a fine-grained model well suited to multi-tenant agent isolation. |
| Observability and evaluation | 10% | **3/5** — Not exercised at Level 1 (no agent runtime built); scored conservatively pending Level 2/3 verification. | **4/5** — Built-in monitoring, evaluation, and session logs in Vertex AI. | **4/5** — Deep CloudWatch integration with traces, token usage, and OpenTelemetry support. |
| DevOps and integration | 10% | **5/5** — Native GitHub Actions + Git integration tested directly in this repo (commits, push, CI-ready). | **3/5** — Google Cloud integrates with Cloud Build/Git, but the workflow is less unified than GitHub's native Actions-on-the-same-platform model. | **3/5** — AWS integrates with CodePipeline/CodeBuild, but again a separate service from the repo host unless using CodeCatalyst. |
| Cost and licensing | 10% | **4/5** — Codespaces and Copilot both have usable free tiers for individuals (Copilot Free confirmed working in this prototype, 0% credits used). | **3/5** — Gemini Code Assist has a free individual tier, but core IDE-extension access for individuals was just discontinued (June 2026), pushing users toward the newer Antigravity tool — adds migration cost/uncertainty. | **3/5** — Amazon Q Developer free tier exists via Builder ID; Pro tier starts at $19/user/month once teams need higher limits. |
| Enterprise fit | 10% | **4/5** — Strong Microsoft 365/Entra ecosystem fit; widely supported in UAE enterprise/government Microsoft-based environments (doc-based claim, to verify per org). | **3/5** — Strong for GCP-native, RAG-heavy workloads; smaller regional enterprise footprint in this region compared to Microsoft. | **3/5** — Strong for AWS-native shops; broad global region coverage but less pre-existing enterprise-desktop integration than Microsoft 365. |

## Weighted totals (score ÷ 5 × weight, summed)

- **Microsoft:** (5/5×15)+(5/5×15)+(4/5×15)+(4/5×15)+(3/5×10)+(5/5×10)+(4/5×10)+(4/5×10) = 15+15+12+12+6+10+8+8 = **86 / 100**
- **Google:** (4/5×15)+(3/5×15)+(4/5×15)+(4/5×15)+(4/5×10)+(3/5×10)+(3/5×10)+(3/5×10) = 12+9+12+12+8+6+6+6 = **71 / 100**
- **AWS:** (3/5×15)+(4/5×15)+(4/5×15)+(4/5×15)+(4/5×10)+(3/5×10)+(3/5×10)+(3/5×10) = 9+12+12+12+8+6+6+6 = **71 / 100**

## Recommendation

**Microsoft (GitHub Codespaces + GitHub Copilot + Microsoft Foundry) wins at 86/100**, driven mainly by categories that were *hands-on verified* in this prototype (developer experience, agentic coding capability, DevOps/Git integration) rather than assumed. Google and AWS tie as runners-up at 71/100 each, both held back on evidence gathered today by real, dated facts: Google's individual free-tier Gemini Code Assist IDE extension was deprecated on June 18, 2026 in favor of "Antigravity" (a genuine migration risk, not a guess), and AWS's tooling, while strong on agent runtime modularity (Bedrock AgentCore), is a less tightly unified developer-experience/DevOps story than GitHub's own ecosystem.

**Caveat / limitation:** Microsoft's score benefits from being the only stack tested hands-on at this level. A fair Level 2/3 re-evaluation should hands-on test Google and AWS as well before treating this as final — this is explicitly flagged as a limitation of this Level 1 prototype, not a hidden assumption.

## Sources
- Google Cloud Workstations overview — https://docs.cloud.google.com/workstations/docs/overview
- Gemini Code Assist Standard/Enterprise overview + deprecation notice — https://docs.cloud.google.com/gemini/docs/codeassist/overview
- Vertex AI Agent Builder — https://leanware.co/insights/vertex-ai-agent-builder
- Amazon Bedrock AgentCore — https://aws.amazon.com/bedrock/agentcore/
- Amazon Q Developer pricing/features — https://www.superblocks.com/blog/amazon-qdeveloper-pricing
- AgentCore vs Vertex vs Foundry comparison — https://tech-insider.org/aws-bedrock-agentcore-vs-azure-ai-foundry-vs-vertex-ai-agent-builder-2026/