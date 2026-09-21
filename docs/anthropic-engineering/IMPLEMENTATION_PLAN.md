# Anthropic Engineering Blog: Phased Implementation Plan

Source index: https://www.anthropic.com/engineering

This document turns every concept published on Anthropic's engineering blog (September 2024 through April 2026, 26 articles) into a single ordered implementation program. Each phase lists the articles it draws from, the concepts to implement, the concrete methods, techniques and configurations, the official cookbooks and docs to use, an ordered checklist, and exit criteria. A companion catalog of every hyperlink, cookbook, quickstart, spec and configuration reference lives in [RESOURCES.md](./RESOURCES.md). Per-article research notes live in [ARTICLE_NOTES.md](./ARTICLE_NOTES.md).

## How this plan was built

- The article list was assembled from the engineering index page and verified through search results and Anthropic's own announcements.
- Article content was reconstructed from search snippets that quote the posts, from official cookbooks, quickstarts, specs and docs that the posts link to, and from third-party coverage. Where a detail could not be verified against a live source it is marked "(unverified)".
- Ordering follows dependency, not publication date. Foundational patterns (tool design, workflow patterns, context management) come before the systems that compose them (multi-agent research, long-running harnesses, managed agents, containment).

## Article index (chronological)

| # | Date | Title | URL |
|---|------|-------|-----|
| 1 | 2024-09-19 | Introducing Contextual Retrieval | https://www.anthropic.com/engineering/contextual-retrieval |
| 2 | 2024-12-19 | Building effective agents | https://www.anthropic.com/engineering/building-effective-agents |
| 3 | 2025-01-06 | Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet | https://www.anthropic.com/engineering/swe-bench-sonnet |
| 4 | 2025-03-20 | The "think" tool: Enabling Claude to stop and think | https://www.anthropic.com/engineering/claude-think-tool |
| 5 | 2025-04-18 | Claude Code: Best practices for agentic coding | https://www.anthropic.com/engineering/claude-code-best-practices |
| 6 | 2025-06-13 | How we built our multi-agent research system | https://www.anthropic.com/engineering/multi-agent-research-system |
| 7 | 2025-06-26 | Claude Desktop Extensions: One-click MCP server installation | https://www.anthropic.com/engineering/desktop-extensions |
| 8 | 2025-09-11 | Writing effective tools for AI agents, using AI agents | https://www.anthropic.com/engineering/writing-tools-for-agents |
| 9 | 2025-09-17 | A postmortem of three recent issues | https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues |
| 10 | 2025-09-29 | Building agents with the Claude Agent SDK | https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk |
| 11 | 2025-09-29 | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 12 | 2025-10-16 | Equipping agents for the real world with Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| 13 | 2025-10-20 | Making Claude Code more secure and autonomous with sandboxing | https://www.anthropic.com/engineering/claude-code-sandboxing |
| 14 | 2025-11-04 | Code execution with MCP: Building more efficient agents | https://www.anthropic.com/engineering/code-execution-with-mcp |
| 15 | 2025-11-24 | Introducing advanced tool use on the Claude Developer Platform | https://www.anthropic.com/engineering/advanced-tool-use |
| 16 | 2025-11-26 | Effective harnesses for long-running agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| 17 | 2026-01-09 | Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| 18 | 2026-01-21 | Designing AI-resistant technical evaluations | https://www.anthropic.com/engineering/AI-resistant-technical-evaluations |
| 19 | 2026-02-05 | Building a C compiler with a team of parallel Claudes | https://www.anthropic.com/engineering/building-c-compiler |
| 20 | 2026-03-06 | Eval awareness in Claude Opus 4.6's BrowseComp performance | https://www.anthropic.com/engineering/eval-awareness-browsecomp |
| 21 | 2026-03-24 | Harness design for long-running application development | https://www.anthropic.com/engineering/harness-design-long-running-apps |
| 22 | 2026-03 | How we built Claude Code auto mode: a safer way to skip permissions | https://www.anthropic.com/engineering/claude-code-auto-mode |
| 23 | 2026-03 | How we contain Claude across products | https://www.anthropic.com/engineering/how-we-contain-claude |
| 24 | 2026-04-08 | Scaling Managed Agents: Decoupling the brain from the hands | https://www.anthropic.com/engineering/managed-agents |
| 25 | 2026-04-23 | An update on recent Claude Code quality reports | https://www.anthropic.com/engineering/april-23-postmortem |

Dates for rows 22 and 23 are approximate (late March 2026); the index page could not be fetched directly. No engineering posts after April 23, 2026 surfaced in search as of September 2026.

## Phase map

| Phase | Theme | Articles | Outcome |
|-------|-------|----------|---------|
| 0 | Foundations and workbench | 5, 9, 25 | Claude Code installed and configured, eval harness skeleton, observability baseline |
| 1 | Retrieval and knowledge | 1 | Contextual retrieval pipeline with reranking |
| 2 | Agent building blocks | 2, 4 | Workflow patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), think tool |
| 3 | Tool design and evaluation | 8, 15, 14, 7 | Tool authoring loop, tool evals, tool search, programmatic tool calling, MCP code execution, packaged MCP servers |
| 4 | Context engineering | 11, 12 | Context budgeting, compaction, memory tool, structured note-taking, Agent Skills |
| 5 | Coding agents and the Agent SDK | 3, 10 | SWE-bench style coding agent, Agent SDK application |
| 6 | Multi-agent systems | 6, 19 | Orchestrator-subagent research system, parallel agent teams on shared repos |
| 7 | Long-running harnesses | 16, 21 | Session-spanning harness with initializer, feature list, progress files, planner/generator/evaluator loops |
| 8 | Security, sandboxing, containment | 13, 22, 23 | Sandbox runtime, auto mode classifiers, product-wide containment model |
| 9 | Evaluation program | 17, 18, 20 | Capability and regression evals, graders, leak-resistant and AI-resistant task design |
| 10 | Managed and scaled agents | 24 | Brain/hands decoupling, durable session logs, checkpoint and resume |
| 11 | Operations and continuous improvement | 9, 25 | Postmortem practice, dogfooding, per-model eval gates on every prompt change |

## Dependency graph

```mermaid
graph TD
  P0[Phase 0 Foundations] --> P1[Phase 1 Retrieval]
  P0 --> P2[Phase 2 Agent building blocks]
  P2 --> P3[Phase 3 Tool design and evaluation]
  P3 --> P4[Phase 4 Context engineering]
  P4 --> P5[Phase 5 Coding agents and Agent SDK]
  P3 --> P6[Phase 6 Multi-agent systems]
  P4 --> P6
  P5 --> P7[Phase 7 Long-running harnesses]
  P6 --> P7
  P5 --> P8[Phase 8 Security and containment]
  P0 --> P9[Phase 9 Evaluation program]
  P3 --> P9
  P7 --> P10[Phase 10 Managed and scaled agents]
  P8 --> P10
  P9 --> P11[Phase 11 Operations]
  P10 --> P11
```
