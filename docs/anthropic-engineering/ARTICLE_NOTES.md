# Anthropic Engineering: Per-Article Research Notes

Detailed notes for all 26 posts, grouped into the batches in which they were researched. Each note records the article's thesis, every concept and technique, every configuration and prompt quoted or reconstructed, every hyperlink, an implementation checklist, and dependencies on other posts. Verification markers inside the notes: confirmed online, partially confirmed, or "(from memory, unverified)". Source labels: facts drawn from a linked cookbook, docs page, spec or repository rather than from the article body carry that source inline (for example `[docs]`, `[cookbook]`, `[mirror]`, "experiments PR #90", "MANIFEST.md"); an independent pass on 2026-09-21 found 173 of 192 numeric claims and configuration tokens verbatim on the live pages, 2 paraphrased, 14 sourced from those linked materials, and 2 live-page edits since publication, which are annotated where they occur (the byline and framework list in "Building effective agents").

| # | Article | Notes file |
|---|---------|------------|
| 1 | Introducing Contextual Retrieval | [notes/01-foundations.md](./notes/01-foundations.md) |
| 2 | Building effective agents | [notes/01-foundations.md](./notes/01-foundations.md) |
| 3 | Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet | [notes/01-foundations.md](./notes/01-foundations.md) |
| 4 | The "think" tool | [notes/01-foundations.md](./notes/01-foundations.md) |
| 5 | Claude Code: Best practices for agentic coding | [notes/01-foundations.md](./notes/01-foundations.md) |
| 6 | How we built our multi-agent research system | [notes/02-multi-agent-tools-sdk.md](./notes/02-multi-agent-tools-sdk.md) |
| 7 | Desktop Extensions: One-click MCP server installation | [notes/02-multi-agent-tools-sdk.md](./notes/02-multi-agent-tools-sdk.md) |
| 8 | Writing effective tools for AI agents, using AI agents | [notes/02-multi-agent-tools-sdk.md](./notes/02-multi-agent-tools-sdk.md) |
| 9 | A postmortem of three recent issues | [notes/02-multi-agent-tools-sdk.md](./notes/02-multi-agent-tools-sdk.md) |
| 10 | Building agents with the Claude Agent SDK | [notes/02-multi-agent-tools-sdk.md](./notes/02-multi-agent-tools-sdk.md) |
| 11 | Effective context engineering for AI agents | [notes/03-context-skills-sandbox-mcp.md](./notes/03-context-skills-sandbox-mcp.md) |
| 12 | Equipping agents for the real world with Agent Skills | [notes/03-context-skills-sandbox-mcp.md](./notes/03-context-skills-sandbox-mcp.md) |
| 13 | Making Claude Code more secure and autonomous with sandboxing | [notes/03-context-skills-sandbox-mcp.md](./notes/03-context-skills-sandbox-mcp.md) |
| 14 | Code execution with MCP | [notes/03-context-skills-sandbox-mcp.md](./notes/03-context-skills-sandbox-mcp.md) |
| 15 | Introducing advanced tool use on the Claude Developer Platform | [notes/03-context-skills-sandbox-mcp.md](./notes/03-context-skills-sandbox-mcp.md) |
| 16 | Effective harnesses for long-running agents | [notes/04-harnesses-and-evals.md](./notes/04-harnesses-and-evals.md) |
| 17 | Demystifying evals for AI agents | [notes/04-harnesses-and-evals.md](./notes/04-harnesses-and-evals.md) |
| 18 | Designing AI-resistant technical evaluations | [notes/04-harnesses-and-evals.md](./notes/04-harnesses-and-evals.md) |
| 19 | Building a C compiler with a team of parallel Claudes | [notes/04-harnesses-and-evals.md](./notes/04-harnesses-and-evals.md) |
| 20 | Quantifying infrastructure noise in agentic coding evals | [notes/06-infrastructure-noise.md](./notes/06-infrastructure-noise.md) |
| 21 | Eval awareness in Claude Opus 4.6's BrowseComp performance | [notes/04-harnesses-and-evals.md](./notes/04-harnesses-and-evals.md) |
| 22 | Harness design for long-running application development | [notes/05-systems-2026.md](./notes/05-systems-2026.md) |
| 23 | How we built Claude Code auto mode | [notes/05-systems-2026.md](./notes/05-systems-2026.md) |
| 24 | Scaling Managed Agents: Decoupling the brain from the hands | [notes/05-systems-2026.md](./notes/05-systems-2026.md) |
| 25 | An update on recent Claude Code quality reports | [notes/05-systems-2026.md](./notes/05-systems-2026.md) |
| 26 | How we contain Claude across products | [notes/05-systems-2026.md](./notes/05-systems-2026.md) |

Date corrections applied after the notes were written: "How we contain Claude across products" was published May 25, 2026 (the batch brief guessed March); "How we built Claude Code auto mode" was published March 25, 2026 and revised in August 2026 when auto mode became the default.
