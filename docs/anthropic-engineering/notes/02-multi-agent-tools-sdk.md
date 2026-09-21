# Research Notes — Batch B: Multi-agent, Tools, SDK (Anthropic Engineering Blog)

Compiled 2026-09-21. Sourcing note: www.anthropic.com was blocked by the egress proxy, so the full article texts were recovered from verbatim GitHub mirrors (`ai-native-engineer/anthropic-mirror` → `www.anthropic.com/engineering/*.md`, `thevibeworks/claude-code-docs` → `content/blog/engineering/*.md`, and `sxwedo/yiya` for the Agent SDK post), cross-checked against WebSearch snippets that quote the originals. Cookbook prompts were fetched verbatim from `raw.githubusercontent.com/anthropics/claude-cookbooks`. The MCPB spec/CLI docs were fetched from `raw.githubusercontent.com/modelcontextprotocol/mcpb`. Agent SDK docs were fetched from `code.claude.com/docs/en/agent-sdk/*.md`. Anything not verified online is marked "(from memory, unverified)".

---

## 1. How we built our multi-agent research system

- **Title:** How we built our multi-agent research system
- **URL:** https://www.anthropic.com/engineering/multi-agent-research-system (older redirect slug seen in the wild: `/engineering/built-multi-agent-research-system`)
- **Date:** Published Jun 13, 2025
- **Authors:** Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (acknowledges the Anthropic apps engineering team)
- **Blurb:** "Our Research feature uses multiple Claude agents to explore complex topics more effectively. We share the engineering challenges and the lessons we learned from building this system."

### Thesis (one paragraph)
Claude's Research feature is an orchestrator-worker multi-agent system: a lead agent (Claude Opus 4) plans, saves its plan to memory, spawns parallel subagents (Claude Sonnet 4) with tightly specified tasks, synthesizes their compressed findings, iterates, and hands the final report to a separate CitationAgent. Multi-agent systems work chiefly because they let the system *spend more tokens* in parallel context windows on problems that exceed a single context window; on BrowseComp, token usage alone explained 80% of performance variance. This yielded a 90.2% improvement over single-agent Opus 4 on Anthropic's internal research eval, at ~15x the tokens of a chat. The post's lessons are about prompt engineering agents as collaborators (think like your agents, teach delegation, scale effort to complexity, tool design, self-improvement, start wide then narrow, guide thinking, parallelize), evaluating with small samples + LLM-as-judge + humans, and production engineering (durable state, tracing, rainbow deployments, sync-vs-async execution). "The last mile often becomes most of the journey."

### Every concept, method, technique, pattern, principle, recommendation

**Why multi-agent for research**
- A multi-agent system = "multiple agents (LLMs autonomously using tools in a loop) working together"; introduces new challenges in "agent coordination, evaluation, and reliability."
- Research is open-ended, path-dependent, and cannot be hardcoded as a fixed pipeline; "A linear, one-shot pipeline cannot handle these tasks."
- "The essence of search is compression": subagents compress by operating in parallel with their own context windows, "condensing the most important tokens for the lead research agent."
- Separation of concerns: each subagent has distinct tools, prompts, exploration trajectories → reduces path dependency.
- Collective-intelligence analogy: "Once intelligence reaches a threshold, multi-agent systems become a vital way to scale performance."
- **Numbers:** multi-agent (Opus 4 lead + Sonnet 4 subagents) "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval." Example task: identify all board members of the IT S&P 500 companies — multi-agent decomposed and succeeded; single agent failed with "slow, sequential searches."
- **Numbers:** On BrowseComp, three factors explained **95%** of performance variance; **token usage alone explains 80%**; other two factors = number of tool calls and model choice.
- "The latest Claude models act as large efficiency multipliers on token use": upgrading to Sonnet 4 is a larger gain than doubling the token budget on Sonnet 3.7.
- **Cost:** agents use ~**4x** more tokens than chat; multi-agent systems ~**15x** more tokens than chat. Economic viability requires high-value tasks.
- **Poor fit:** domains where all agents must share the same context or have many inter-agent dependencies; "most coding tasks involve fewer truly parallelizable tasks than research"; LLM agents "are not yet great at coordinating and delegating to other agents in real time."
- **Good fit:** "heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools." Excel "especially for breadth-first queries."

**Architecture (orchestrator-worker)**
- User query → LeadResearcher agent → thinks through approach → saves plan to Memory (because context beyond **200,000 tokens** gets truncated; the plan must persist) → creates Subagents (any number) with specific research tasks → each subagent does web searches, evaluates results with **interleaved thinking**, returns findings → LeadResearcher synthesizes, decides whether more research is needed (spawn more subagents / refine strategy) → exits loop → **CitationAgent** processes documents + report to insert citations → results returned to user.
- Subagents "act as intelligent filters."
- Contrast with RAG: RAG = static retrieval of most-similar chunks; this = multi-step dynamic search that "adapts to new findings."

**Eight prompt-engineering principles for research agents**
1. **Think like your agents** — build simulations in the Console with the exact prompts/tools and watch step by step; revealed failures like continuing after sufficient results, overly verbose queries, wrong tool selection. Develop an accurate mental model.
2. **Teach the orchestrator how to delegate** — each subagent needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Vague instructions ("research the semiconductor shortage") caused duplicated searches (one subagent did the 2021 automotive chip crisis, two others duplicated 2025 supply chains).
3. **Scale effort to query complexity** — embed scaling rules: simple fact-finding = **1 agent, 3-10 tool calls**; direct comparisons = **2-4 subagents, 10-15 calls each**; complex research = **>10 subagents** with divided responsibilities. Prevents overinvestment (early agents spawned 50 subagents for simple queries).
4. **Tool design and selection are critical** — "Agent-tool interfaces are as critical as human-computer interfaces." Heuristics given to agents: examine all available tools first; match tool usage to user intent; web search for broad external exploration; prefer specialized tools over generic ones. Each tool needs a distinct purpose and clear description. MCP servers compound the problem with descriptions "of wildly varying quality."
5. **Let agents improve themselves** — Claude 4 models are "excellent prompt engineers"; a **tool-testing agent** given a flawed MCP tool tries it dozens of times and rewrites the description → **40% decrease in task completion time** for future agents.
6. **Start wide, then narrow down** — short, broad queries first, then progressively narrow (mirrors expert human research); agents default to overly long specific queries.
7. **Guide the thinking process** — extended thinking as a "controllable scratchpad": lead agent plans tools, complexity, subagent count, roles; subagents use interleaved thinking after tool results to evaluate quality, find gaps, refine next query. Extended thinking "improved instruction-following, reasoning, and efficiency."
8. **Parallel tool calling transforms speed and performance** — two kinds: (1) lead spins up **3-5 subagents in parallel**; (2) subagents use **3+ tools in parallel**. Cut research time by **up to 90%** for complex queries.

- Overall prompting philosophy: instill good heuristics, not rigid rules; encode how skilled humans research (decompose, evaluate source quality, adjust based on new info, depth vs breadth); set explicit guardrails against spiraling; fast iteration loop with observability and test cases.

**Evaluation**
- Multi-agent systems take different valid paths → need "flexible evaluation methods that judge whether agents achieved the right outcomes while also following a reasonable process."
- **Start evaluating immediately with small samples**: early changes have huge effects (a prompt tweak "might boost success rates from 30% to 80%"); they started with **~20 queries** representing real usage. Don't wait for hundreds of cases.
- **LLM-as-judge**: rubric = factual accuracy, citation accuracy, completeness, source quality, tool efficiency. A **single LLM call with a single prompt outputting 0.0-1.0 scores and a pass/fail grade** was most consistent and human-aligned (vs multiple specialized judges). Works best when test cases have a clear answer (e.g., "top 3 pharma companies by R&D budget"). Scales to hundreds of outputs.
- **Human evaluation** catches hallucinations on unusual queries, system failures, source-selection bias — e.g., early agents preferred SEO content farms over academic PDFs/personal blogs → fixed with source-quality heuristics in prompts.
- Emergent behaviors: small lead-agent changes unpredictably change subagent behavior; best prompts are "frameworks for collaboration" defining division of labor, problem-solving approaches, effort budgets.

**Production reliability**
- **Agents are stateful and errors compound**: durable execution; resume from where the agent was rather than restart; tell the model when a tool is failing and let it adapt; combine with deterministic safeguards (retry logic, regular checkpoints).
- **Debugging needs new approaches**: non-determinism between runs; added **full production tracing**; monitor agent decision patterns and interaction structures "without monitoring the contents of individual conversations" (privacy).
- **Deployment needs careful coordination**: agents are long-running stateful webs; use **rainbow deployments** (gradually shift traffic old→new while both run) so running agents aren't broken.
- **Synchronous execution creates bottlenecks**: lead waits for each set of subagents; can't steer mid-flight; subagents can't coordinate. Asynchronous execution would add parallelism but adds result-coordination, state-consistency, error-propagation challenges; expected to be worth it as tasks lengthen.

**Conclusion**
- "the last mile often becomes most of the journey"; compound errors; gap between prototype and production wider than anticipated.
- Success requires "careful engineering, comprehensive testing, detail-oriented prompt and tool design, robust operational practices, and tight collaboration between research, product, and engineering teams."
- Clio usage plot: top use cases — developing software systems (10%), professional/technical content (8%), business growth/revenue strategies (8%), academic research/educational material (7%), researching people/places/organizations (5%).

**Appendix tips**
- **End-state evaluation** for state-mutating agents: judge final state, not process; for complex workflows break into discrete checkpoints where specific state changes should have occurred.
- **Long-horizon conversation management**: summarize completed phases into external memory; spawn fresh subagents with clean contexts when limits approach, with careful handoffs; retrieve stored plan from memory.
- **Subagent output to a filesystem** to minimize the "game of telephone": subagents store artifacts (code, reports, visualizations) in external systems and pass lightweight references back to the coordinator; improves fidelity, reduces token overhead.

### Concrete configurations / prompts / tool definitions / workflow steps

**Tools named in the prompts (cookbook):** `run_blocking_subagent` (lead creates a subagent; task in `prompt` param), `complete_task` (submit final report / subagent findings), `web_search`, `web_fetch`, `google_drive_search`, gmail tools, gcal tools, `repl`, `slack_search`, `slack_user_profile`, `asana_user_info`, `asana_search_tasks`, `evaluate_source_quality` (explicitly disabled: "DO NOT use the evaluate_source_quality tool ever ... It is broken"). Template variable `{{.CurrentDate}}`.

**Open-sourced prompts (fetched verbatim; summarized):**

*`research_lead_agent.md`* (~23 KB)
- Role: "expert research lead, focused on high-level research strategy, planning, efficient delegation to subagents, and final report writing."
- `<research_process>` 4 steps: (1) **Assessment and breakdown** (concepts, entities, facts needed, temporal constraints, expected output form); (2) **Query type determination** — *Depth-first* (many perspectives on one issue; e.g., "most effective treatments for depression", "what caused 2008 crisis"), *Breadth-first* (independent sub-questions; e.g., "compare Nordic economies", "net worths of all Fortune 500 CEOs"), *Straightforward* (single focused investigation; e.g., "population of Tokyo", "tell me about bananas"); (3) **Detailed research plan** per type (depth-first: 3-5 methodological approaches; breadth-first: enumerate sub-questions, crisp boundaries, aggregation plan — example "EU tax systems": one subagent to list EU countries, then 4 subagents for N/W/E/S Europe via the batch tool; straightforward: most direct path + verification). For each step ask: can it be split? multiple perspectives? expected output? strictly necessary?; (4) **Methodical plan execution** — "default to using 3 subagents for most queries"; parallel where possible; for non-parallelizable steps attempt yourself first; Bayesian updating; if running out of time stop spawning and write the report.
- `<subagent_count_guidelines>`: simple = 1 subagent (always at least 1); standard = 2-3; medium = 3-5 (e.g., AI in healthcare → 4: regulatory, clinical, economic, technological); high complexity = 5-10, **maximum 20** ("Fortune 500 CEOs birthplaces and ages" → 10 subagents × 50 CEOs). "More subagents = more overhead."
- `<delegation_instructions>`: deploy immediately after plan; use `run_blocking_subagent`; order by priority/dependency; all substantial info-gathering delegated; task allocation per query type (depth-first: sequence approaches; breadth-first: framework facts first; straightforward: one subagent handling ~half the work); avoid overlap; every subagent instruction includes: specific objective (ideally 1), expected output format, background context, key questions, suggested starting points and reliability criteria, specific tools, scope boundaries. Includes an exemplar task description (semiconductor supply chain: TSMC/Samsung/Intel IR pages, SEC EDGAR, SEMI/Gartner/IDC, CHIPS Act at commerce.gov, EU Chips Act...). Lead's role: coordinate and synthesize, not primary research.
- `<answer_formatting>`: review fact list; output final in Markdown via `complete_task`; "Do not include ANY Markdown citations, a separate agent will be responsible for citations."
- `<use_available_internal_tools>`: always try read-only integration tools once or twice (Slack, Asana, GitHub, Google Suite); never use write tools; pattern: an Asana subagent, a Slack subagent, a Google Drive subagent, a Web Search subagent.
- `<use_parallel_tool_calls>`: "MUST use parallel tool calls for creating multiple subagents (typically running 3 subagents at the same time)."
- `<important_guidelines>`: high information density; track discrepancies; stop at diminishing returns; "NEVER create a subagent to generate the final report"; avoid harmful research topics; no clarifying questions.

*`research_subagent.md`* (~9 KB)
- `<research_process>`: (1) **Planning** with a "research budget": simple tasks <5 tool calls, medium ~5, hard ~10, very difficult/multi-part up to 15; (2) **Tool selection** (internal tools ALWAYS prioritized when present; ALWAYS `web_fetch` to get full contents after search or when a URL is provided; avoid repl for simple counting); (3) **Research loop** = OODA (observe, orient, decide, act); "MINIMUM of five distinct tool calls, up to ten for complex queries"; never repeat identical queries.
- `<research_guidelines>`: concise, dense reporting; moderately broad queries, "under 5 words"; broaden if few results; prioritize significant/important/precise/high-quality facts; prioritize recency & consistency on conflicts; surface unresolved conflicts to lead.
- `<think_about_source_quality>`: flag speculation (future tense, "could/may"), aggregators, false authority, passive voice + nameless sources, marketing/spin language, cherry-picked data; epistemic honesty.
- `<use_parallel_tool_calls>`: invoke 2 tools simultaneously.
- `<maximum_tool_call_limit>`: hard limit **20 tool calls and ~100 sources** ("the subagent will be terminated"); stop at ~15 calls; use `complete_task`.

*`citations_agent.md`* (~3 KB)
- Input: report in `<synthesized_text>` + sources; output identical text with citations in `<exact_text_with_citation>` tags.
- Rules: do NOT modify text or whitespace; only cite where sources directly support claims; avoid unnecessary citations; cite meaningful semantic units at sentence ends; minimize sentence fragmentation; no redundant citations to the same source within one sentence; preamble/thinking BEFORE the opening tag; non-identical text is rejected.

### Hyperlinks in the article (verified where possible)
- Research feature announcement: https://www.anthropic.com/news/research (blocked; from article)
- BrowseComp: https://openai.com/index/browsecomp/
- Interleaved thinking / extended thinking docs: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#interleaved-thinking → canonical now https://platform.claude.com/docs/en/build-with-claude/extended-thinking (verified 200)
- Anthropic Console: https://console.anthropic.com/
- MCP intro: https://modelcontextprotocol.io/introduction
- Open-source prompts in Cookbook: article links https://platform.claude.com/cookbook/patterns-agents-basic-workflows (verified 200 — that page is the "Basic workflows" notebook: chain/parallel/route). The actual prompt files: https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts → `research_lead_agent.md`, `research_subagent.md`, `citations_agent.md` (raw URLs verified 200).
- Rainbow deployments: https://brandon.dimcheff.com/2018/02/rainbow-deploys-with-kubernetes/
- Clio: https://www.anthropic.com/research/clio
- Courses: https://anthropic.skilljar.com/

### Implementation checklist
1. Decide fit: is the task breadth-first, high-value, parallelizable, exceeding one context window, and tolerant of ~15x chat token cost? If not (e.g., tightly coupled coding), use a single agent.
2. Define the orchestrator-worker topology: lead agent (strongest model) + N subagents (cheaper/faster model) + a separate citation/post-processing agent.
3. Give the lead a memory/plan store that survives context truncation (~200k tokens); persist the plan at the start.
4. Write the lead prompt: assessment → query-type classification (depth/breadth/straightforward) → plan → parallel execution; embed subagent-count and tool-call budgets scaled to complexity; require every subagent brief to include objective, output format, tools/sources, boundaries; forbid delegating the final report.
5. Write the subagent prompt: budget, OODA loop, min/max tool calls, source-quality heuristics, "start broad then narrow", parallel tool calls, hard termination limits, `complete_task` return.
6. Build/curate tools with distinct purposes and clear descriptions; add tool-selection heuristics to prompts; run a tool-testing agent to rewrite bad descriptions.
7. Enable extended/interleaved thinking for planning and post-tool-result evaluation.
8. Parallelize: spawn 3-5 subagents at once; have subagents issue 3+ tool calls at once.
9. Build a ~20-query eval from real usage immediately; add an LLM judge (single prompt, 0-1 scores + pass/fail on accuracy, citation accuracy, completeness, source quality, tool efficiency); add human review passes.
10. Add production tracing of decisions/interaction patterns (privacy-preserving), retries, checkpoints, resume-from-failure, and tool-failure messaging to the model.
11. Deploy with rainbow deployments; consider async subagent execution later.
12. Store large subagent artifacts in a filesystem/artifact store and pass references; summarize phases into memory for long-horizon runs; use end-state evaluation for state-mutating agents.

### Dependencies on other Anthropic engineering articles
- Builds on "Building effective agents" (Dec 2024) orchestrator-workers pattern (implied; the cookbook link is the "patterns/agents" notebook from that post).
- Feeds forward into "Writing effective tools for agents" (Sep 2025) — the tool-testing agent/40% result is the seed of that post — and "Building agents with the Claude Agent SDK" (subagents/compaction), and "Effective context engineering for AI agents" (memory, compaction, subagent context isolation).

---

## 2. Claude Desktop Extensions: One-click MCP server installation

- **Title:** Desktop Extensions: One-click MCP server installation for Claude Desktop
- **URL:** https://www.anthropic.com/engineering/desktop-extensions
- **Date:** Published Jun 26, 2025; update note dated Sep 11, 2025: "Claude Desktop Extensions now use the .mcpb (MCP Bundle) file extension instead of .dxt. Existing .dxt extensions will continue to work... purely a naming convention update."
- **Authors:** Not bylined in the mirrored text. (From memory, unverified: the DXT work was led by Felix Rieseberg of the Claude Desktop team.)
- **Blurb:** "Desktop Extensions make installing MCP servers as easy as clicking a button. We share the technical architecture and tips for creating good extensions."
- **Naming history:** Originally "DXT" (`.dxt` files, `dxt_version` manifest field, `@anthropic-ai/dxt` npm package, repo `anthropics/dxt`). Renamed Sep 2025 to "MCPB / MCP Bundles" (`.mcpb`, `manifest_version`, `@anthropic-ai/mcpb`, repo now at https://github.com/modelcontextprotocol/mcpb; `anthropics/dxt` and `anthropics/mcpb` URLs are still referenced in the article and README and redirect). The current article text has been updated to mcpb naming; the June 2025 original used `npx @anthropic-ai/dxt init` / `npx @anthropic-ai/dxt pack` and `"dxt_version": "0.1"` (from memory, unverified — consistent with the mirrored README's rename notice).

### Thesis
Local MCP servers were powerful but nearly unusable for non-developers: they needed runtimes, manual JSON config edits, dependency wrangling, had no discovery, and no update path. Desktop Extensions (`.mcpb`, formerly `.dxt`) package an entire MCP server plus dependencies and a `manifest.json` into a zip that Claude Desktop installs with one click, with a bundled Node.js runtime, OS-keychain secret storage, a user-config UI, automatic updates, a curated in-app directory, and enterprise controls (Group Policy/MDM, allow/blocklists, private directories). The spec, CLI toolchain (`mcpb init/pack`), schemas, and reference code are open-sourced (versioned 0.1 deliberately) so other AI desktop apps can adopt the format.

### Every concept, method, technique, principle, recommendation
- **Problem statement** ("Addressing the MCP installation problem"): developer tools required (Node/Python); manual configuration (JSON edits); dependency management (conflicts/version mismatches); no discovery mechanism (search GitHub); update complexity (manual reinstall). → MCP servers "remained largely inaccessible to non-technical users."
- **Before/after**: Before = `npm install -g @example/mcp-server`, edit `~/.claude/claude_desktop_config.json`, restart, "Hope it works." After = download `.mcpb`, double-click, click "Install."
- **Definition**: "A Desktop Extension is a zip archive containing the local MCP server as well as a `manifest.json`." Only required file is `manifest.json`.
- **Claude Desktop handles**: built-in runtime (ships Node.js), automatic updates, secure secrets (OS keychain).
- **Manifest contents**: human-readable info (name, description, author), feature declaration (tools, prompts), user configuration, runtime requirements. Three supported extension types: Node.js, Python, classic binaries/executables.
- **User config flow**: developer declares `user_config` (e.g., `api_key`, `sensitive: true, required: true`); Claude won't enable the extension until supplied; stores in OS secret vault; substitutes `${user_config.api_key}` at launch; `${__dirname}` → unpacked extension directory.
- Claude Desktop will: display a config UI, validate inputs before enabling, securely store sensitive values, pass config as args or env vars per developer choice.
- **Template literals / dynamic configuration**: `${__dirname}`, `${user_config.key}`, `${HOME}`, `${TEMP}` (system env vars).
- **Cross-platform support** via platform overrides (article shows a `platforms` block with `win32`/`darwin` keys; the current spec names this `platform_overrides`).
- **Feature declaration** (`tools`, `prompts` arrays) so users understand capabilities up front.
- **Testing locally**: drag `.mcpb` into Claude Desktop Settings → shows human-readable info, required permissions/config, "Install" button.
- **Extension directory**: curated, built into Claude Desktop; browse/search/install one click. Submission: follow the form guidelines, test on Windows and macOS, submit form, Anthropic reviews for quality and security.
- **Open ecosystem**: open-sourcing the complete MCPB spec, packaging/validation tools, reference implementation code, TypeScript types and schemas. "Package once, run anywhere that supports MCPB." Spec deliberately versioned **0.1**.
- **Security (users)**: sensitive data in OS keychain; automatic updates; audit installed extensions.
- **Security (enterprise)**: Group Policy (Windows) and MDM (macOS) support; pre-install approved extensions; blocklist specific extensions or publishers; disable the directory entirely; deploy private extension directories.
- **Language recommendation** (README): implement servers in **Node.js** rather than Python — Node ships with Claude Desktop; Python bundles can't portably include compiled deps (e.g., pydantic). Later spec added `uv` server type (v0.4+) to solve Python packaging.
- **Building with Claude Code**: a canonical prompt block instructing Claude to read README.md / MANIFEST.md / examples, create manifest + server using `@modelcontextprotocol/sdk`, stdio transport, clear schemas/validation/consistent JSON, error handling and timeouts, logging, docs, and test that tool calls return structured responses.
- **Internal example**: a PyBoy GameBoy-emulator extension letting Claude play (link to "Claude plays Pokémon" research).
- Closing: "The same creativity that brought us thousands of MCP servers can now reach millions of users with just one click."

### Concrete configurations, manifests, CLI commands, directory layouts

**Directory layouts (from article/README)**
```
extension.mcpb (ZIP archive)
├── manifest.json         # Extension metadata and configuration (REQUIRED)
├── server/               # MCP server implementation
├── dependencies/         # All required packages/libraries
└── icon.png              # Optional
# Node.js: manifest.json, server/index.js, node_modules/, package.json, icon.png
# Python:  manifest.json, server/main.py, server/utils.py, lib/ (or server/lib, server/venv), requirements.txt, icon.png
# Binary:  manifest.json, server/my-server, server/my-server.exe, icon.png
# UV (v0.4+): manifest.json (server.type="uv"), pyproject.toml, .mcpbignore, src/server.py
```

**Minimal manifest (article; field originally `dxt_version`, now `manifest_version`)**
```json
{
  "manifest_version": "0.3",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A simple MCP extension",
  "author": { "name": "Extension Author" },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": { "command": "node", "args": ["${__dirname}/server/index.js"] }
  }
}
```
(The article's mirrored text shows `"mcpb_version": "0.1"`; the current spec at MANIFEST.md uses `"manifest_version": "0.3"`, last updated 2025-12-02.)

**Manifest with user config (article)**: adds `"env": {"API_KEY": "${user_config.api_key}"}` and
```json
"user_config": { "api_key": { "type": "string", "title": "API Key", "description": "Your API key for authentication", "sensitive": true, "required": true } }
```

**Full manifest fields (MANIFEST.md, verified):**
- Required: `manifest_version`, `name`, `version` (semver), `description` (localizable), `author{name, email?, url?}`, `server{type, entry_point, mcp_config}`.
- Optional: `display_name`, `long_description` (markdown), `icon`, `icons[{src,size,theme}]`, `repository{type,url}`, `homepage`, `documentation`, `support`, `screenshots[]`, `tools[{name,description}]`, `tools_generated` (bool), `prompts[{name,description,arguments[],text}]`, `prompts_generated`, `keywords[]`, `license`, `privacy_policies[]` (required when connecting to external services), `compatibility{claude_desktop, <client>, platforms[darwin|win32|linux], runtimes{python,node}}`, `user_config{}`, `_meta{}` (reverse-DNS keys, e.g. `com.microsoft.windows.package_family_name`, `static_responses`), `localization{resources: "…/${locale}.json", default_locale}`.
- `server.type`: `node` | `python` | `binary` | `uv` (v0.4+).
- `server.mcp_config`: `command`, `args[]`, `env{}`, `platform_overrides{win32|darwin|linux → command/args/env}`. Binaries get `.exe` auto-appended on Windows.
- Variable substitution: `${__dirname}`, `${HOME}`, `${DESKTOP}`, `${DOCUMENTS}`, `${DOWNLOADS}`, `${pathSeparator}`/`${/}`, `${user_config.KEY}` (arrays from `multiple: true` expand into separate args).
- `user_config.<key>`: `type` (`string`|`number`|`boolean`|`directory`|`file`), `title`, `description`, `required` (default false), `default` (supports `${HOME}` etc.), `multiple` (dir/file), `sensitive` (string → masked + keychain), `min`/`max` (number).
- Prompt text templates use `${arguments.<name>}`.
- Resources are not declared (dynamic by nature).

**CLI (CLI.md, verified)**: `npm install -g @anthropic-ai/mcpb` (article: `npx @anthropic-ai/mcpb init` [supports `--yes`], `npx @anthropic-ai/mcpb pack`; original: `@anthropic-ai/dxt`). Commands: `mcpb init [directory]`, `mcpb validate <manifest|dir>`, `mcpb pack <directory> [output]` (validates, excludes dev files, max-compression zip), `mcpb sign <file> [--cert|-c cert.pem] [--key|-k key.pem] [--intermediate|-i …] [--self-signed]`, `mcpb verify <file>`, `mcpb info <file>`, `mcpb unsign <file>`. `.mcpbignore` for custom exclusions. Default exclusions: `.DS_Store`, `.git/`, `*.log`, `node_modules/.cache/`, `node_modules/.bin/`, `*.map`, `.env.local`, `package-lock.json`, `yarn.lock`, etc. Signatures: PKCS#7 DER appended with `MCPB_SIG_V1` / `MCPB_SIG_END` markers (detached; unsigned files stay valid zips).

**Getting-started commands (article)**
```
npm install -g @anthropic-ai/mcpb
mcpb init
mcpb pack
```
Claude Code prototyping: `Settings > Developer` (local MCP) or `Settings > Extensions` (MCPB) in Claude Desktop; `claude mcp add <name> <command> [args...]` in Claude Code (from article 3).

**Reference example** (`examples/hello-world-node/manifest.json`, verified): `manifest_version 0.3`, tool `get_current_time`, user_config examples of every type (`api_key` sensitive string, `verbose_logging` boolean, `max_results` number 1-100, `config_file` file, `workspace_directory` directory default `${HOME}/Documents`, `debug_mode` string), args like `--verbose=${user_config.verbose_logging}`, `compatibility.claude_desktop ">=0.10.0"`, `privacy_policies: []`.

### Hyperlinks
- Manifest spec: https://github.com/anthropics/dxt/blob/main/MANIFEST.md → canonical https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md (raw verified)
- Examples: https://github.com/anthropics/dxt/tree/main/examples → https://github.com/modelcontextprotocol/mcpb/tree/main/examples
- Developer docs/repo: https://github.com/anthropics/dxt → https://github.com/modelcontextprotocol/mcpb (README verified); CLI docs https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md
- Claude Code prompt references: https://github.com/anthropics/mcpb/blob/main/README.md, /MANIFEST.md, /tree/main/examples
- Enterprise/MCP docs: https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop (now support.claude.com; blocked); also https://support.claude.com/en/articles/12702546-deploying-enterprise-grade-mcp-servers-with-desktop-extensions and https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop (from search results)
- Submission form: https://docs.google.com/forms/d/14_Dmcig4z8NeRMB_e7TOyrKzuZ88-BLYdLvS6LPhiZU/edit and https://forms.gle/tyiAZvch1kDADKoP9
- Claude plays Pokémon: https://www.anthropic.com/news/visible-extended-thinking
- PyBoy: https://github.com/Baekalfen/PyBoy
- npm: https://www.npmjs.com/package/@anthropic-ai/mcpb (was @anthropic-ai/dxt)
- Current Claude docs page: https://claude.com/docs/connectors/building/mcpb (from search; blocked)

### Implementation checklist
1. Build/choose a local MCP server (prefer Node.js; use `@modelcontextprotocol/sdk`, stdio transport).
2. Put server files in a folder (`server/index.js` etc.); `npm install --production` so `node_modules` is bundled.
3. `npm install -g @anthropic-ai/mcpb`; run `mcpb init` (or `--yes`) to generate `manifest.json`.
4. Fill manifest: name/version/description/author; `server.type/entry_point/mcp_config` with `${__dirname}`; declare `tools`/`prompts`; add `compatibility` (platforms, runtimes, claude_desktop); add `privacy_policies` if external services.
5. Declare `user_config` for API keys (`sensitive: true`) and directories (`type: directory, multiple: true, default: ["${HOME}/Documents"]`); wire via `env` or `args`.
6. Add `platform_overrides` for Windows/macOS differences; add `.mcpbignore`.
7. `mcpb validate .` then `mcpb pack .` → `.mcpb`; optionally `mcpb sign` (self-signed for dev, CA cert for prod) and `mcpb verify`.
8. Test: drag into Claude Desktop Settings > Extensions; confirm config UI, keychain storage, tool listing.
9. Test on both Windows and macOS; submit to the directory via the form; Anthropic reviews.
10. Enterprise: configure Group Policy/MDM, allowlist/blocklist, private directory as needed.

### Dependencies on other Anthropic articles
- Referenced by "Writing effective tools for agents" as the way to wrap tools for testing in Claude Desktop.
- Relies on MCP (modelcontextprotocol.io). Related to Claude Desktop local-MCP help-center docs.

---

## 3. Writing effective tools for AI agents — using AI agents

- **Title:** Writing effective tools for agents — with agents
- **URL:** https://www.anthropic.com/engineering/writing-tools-for-agents
- **Date:** Published Sep 11, 2025
- **Authors:** Ken Aizawa; contributions from Research (Barry Zhang, Zachary Witten, Daniel Jiang, Sami Al-Sheikh, Matt Bell, Maggie Vo), MCP (Theodora Chu, John Welsh, David Soria Parra, Adam Jones), Product Engineering (Santiago Seira), Marketing (Molly Vorwerck), Design (Drew Roper), Applied AI (Christian Ryan, Alexander Bricken).
- **Blurb:** "Agents are only as effective as the tools we give them. We share how to write high-quality tools and evaluations, and how you can boost performance by using Claude to optimize its tools for itself."

### Thesis
Tools are "a new kind of software which reflects a contract between deterministic systems and non-deterministic agents," so they must be designed for agents rather than as thin wrappers over APIs. The recommended workflow is: prototype tools quickly (in a local MCP server/DXT, tested in Claude Code or Claude Desktop), build a realistic evaluation with verifiable outcomes, run simple agentic loops programmatically while collecting accuracy plus runtime/tool-call/token/error metrics, read transcripts and CoT, and then let Claude Code analyze transcripts and rewrite tools/descriptions — using held-out test sets to avoid overfitting. Principles distilled from doing this on Anthropic's internal Slack/Asana tools: build few consolidated, high-impact tools; namespace them; return high-signal, natural-language context; optimize token efficiency (pagination/filtering/truncation, 25k-token cap in Claude Code, `response_format` concise vs detailed = ~⅓ tokens); and prompt-engineer descriptions as if onboarding a new hire (unambiguous parameter names like `user_id`).

### Every concept, method, technique, principle, recommendation
**What is a tool**
- Deterministic software = contract between deterministic systems (`getWeather("NYC")`); tools = contract between deterministic systems and non-deterministic agents (agent may call the tool, answer from knowledge, ask a clarifying question, hallucinate, or fail to grasp the tool).
- Design tools for agents, not like functions/APIs for developers. Goal: "increase the surface area over which agents can be effective." Ergonomic-for-agents tools are also intuitive for humans.

**How to write tools (workflow)**
- **Build a prototype**: hard to anticipate ergonomics without hands-on use; use Claude Code (possibly one-shot) and give it docs for libraries/APIs/SDKs incl. MCP SDK; LLM-friendly docs often at `llms.txt` (Anthropic's: https://docs.anthropic.com/llms.txt). Wrap tools in a local MCP server or Desktop Extension (DXT) to test in Claude Code / Claude Desktop. Connect to Claude Code: `claude mcp add <name> <command> [args...]`. Claude Desktop: `Settings > Developer` (MCP) or `Settings > Extensions` (DXT). Tools can also be passed directly to Anthropic API calls. Test yourself; collect user feedback.
- **Run an evaluation**: generate many tasks grounded in real-world use (real data sources, internal knowledge bases, microservices); avoid simplistic sandboxes; strong tasks may need "multiple tool calls—potentially dozens."
  - Strong task examples: "Schedule a meeting with Jane next week to discuss our latest Acme Corp project. Attach the notes from our last project planning meeting and reserve a conference room."; "Customer ID 9182 reported that they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected…"; "Customer Sarah Chen just submitted a cancellation request. Prepare a retention offer. Determine: (1) why they're leaving, (2) what retention offer…, (3) any risk factors…"
  - Weak examples: "Schedule a meeting with jane@acme.corp next week."; "Search the payment logs for `purchase_complete` and `customer_id=9182`."; "Find the cancellation request by Customer ID 45892."
  - Pair each prompt with a verifiable response/outcome; verifier from exact string match to Claude-as-judge; avoid overly strict verifiers (formatting/punctuation/phrasing). Optionally specify expected tools but avoid overfitting to strategies.
  - Run programmatically with direct LLM API calls; "simple agentic loops (`while`-loops wrapping alternating LLM API and tool calls): one loop for each evaluation task"; single task prompt + tools per agent.
  - Instruct evaluation agents to output structured response blocks plus **reasoning and feedback blocks**, emitted *before* tool calls to trigger CoT; or turn on interleaved thinking with Claude.
  - Metrics beyond accuracy: total runtime of tool calls and tasks, number of tool calls, total token consumption, tool errors. Tool-call tracking reveals workflows and consolidation opportunities.
  - Graphs shown: "Held-out test set performance of our internal Slack tools" and "…Asana tools" (human-written vs Claude-optimized).
- **Analyzing results**: agents are partners for spotting contradictory descriptions, inefficient implementations, confusing schemas; but "what agents omit… can often be more important"; "LLMs don't always say what they mean" (links Tracing Thoughts research). Read CoT and raw transcripts; read between the lines. Lots of redundant tool calls → rightsize pagination/token limits; lots of invalid-parameter errors → clearer descriptions/examples. Example: Claude web search tool — Claude "needlessly appending `2025` to the tool's `query` parameter," fixed via description.
- **Collaborating with agents**: concatenate evaluation transcripts and paste into Claude Code; Claude refactors many tools at once and keeps implementations/descriptions self-consistent. Most advice in the post came from repeatedly optimizing internal tools with Claude Code on evals built over the internal workspace. **Held-out test sets** prevented overfitting and showed gains beyond "expert" (human- or Claude-written) implementations.

**Principles**
- **Choosing the right tools**: more tools ≠ better; anti-pattern = wrapping every API endpoint. Agents have limited context vs cheap computer memory: `list_contacts` returning ALL contacts wastes context; prefer `search_contacts` or `message_contact`. Build "a few thoughtful tools targeting specific high-impact workflows" matching eval tasks, then scale. Consolidate multi-step operations: `schedule_event` instead of `list_users`+`list_events`+`create_event`; `search_logs` (relevant lines + context) instead of `read_logs`; `get_customer_context` instead of `get_customer_by_id`+`list_transactions`+`list_notes`. Each tool: clear distinct purpose; let agents subdivide tasks like a human would; reduce intermediate-output context. Too many/overlapping tools distract.
- **Namespacing**: group related tools under common prefixes (MCP clients sometimes do by default); by service (`asana_search`, `jira_search`) and by resource (`asana_projects_search`, `asana_users_search`). Prefix- vs suffix-based namespacing "have non-trivial effects on our tool-use evaluations. Effects vary by LLM" → choose per your evals. Failure modes: wrong tool, right tool/wrong params, too few tools, misprocessed responses. Names reflecting natural task subdivisions reduce tools loaded into context and "offload agentic computation from the agent's context back into the tool calls."
- **Returning meaningful context**: return only high-signal info; prioritize contextual relevance over flexibility; eschew low-level technical identifiers (`uuid`, `256px_image_url`, `mime_type`) in favor of `name`, `image_url`, `file_type`. Resolving UUIDs to semantic names (or even a 0-indexed ID scheme) "significantly improves Claude's precision in retrieval tasks by reducing hallucinations." When IDs are needed for chaining (`search_user(name='jane')` → `send_message(id=12345)`), expose a `response_format` enum (`"concise"` | `"detailed"`), GraphQL-like. Slack example: `thread_ts`, `channel_id`, `user_id` only in detailed; detailed = **206 tokens**, concise = **72 tokens** (~⅓). Response structure (XML/JSON/Markdown) affects performance; no one-size-fits-all; pick by eval.
- **Token efficiency**: implement pagination, range selection, filtering, and/or truncation with sensible defaults. "For Claude Code, we restrict tool responses to **25,000 tokens** by default." When truncating, steer agents (e.g., many small targeted searches instead of one broad). Prompt-engineer error responses to be specific and actionable, not opaque codes/tracebacks (examples of truncated response, unhelpful vs helpful error response shown as images).
- **Prompt-engineering tool descriptions**: "think of how you would describe your tool to a new hire"; make implicit context explicit (query formats, niche terminology, resource relationships); enforce with strict data models; unambiguous parameter names (`user_id` not `user`). Small refinements yield dramatic gains: Claude Sonnet 3.5 reached SOTA on SWE-bench Verified after precise tool-description refinements. Read Developer Guide best practices; understand how tools are loaded into the system prompt; use MCP tool annotations (open-world access, destructive changes).
- **Looking ahead**: re-orient software practice from deterministic to non-deterministic; effective tools are "intentionally and clearly defined, use agent context judiciously, can be combined together in diverse workflows, and enable agents to intuitively solve real-world tasks"; keep an evaluation-driven approach as MCP and models evolve. Footnote 1: techniques are "beyond training the underlying LLMs themselves."

### Concrete configurations / code / commands
- `claude mcp add <name> <command> [args...]`
- `enum ResponseFormat { DETAILED = "detailed", CONCISE = "concise" }`
- Tool naming examples: `search_contacts`, `message_contact`, `schedule_event`, `search_logs`, `get_customer_context`, `asana_search`, `jira_search`, `asana_projects_search`, `asana_users_search`, `search_user(name='jane')`, `send_message(id=12345)`.
- **Tool evaluation cookbook** (https://platform.claude.com/cookbook/tool-evaluation-tool-evaluation, published Sep 10, 2025; GitHub `tool_evaluation/tool_evaluation.ipynb` + `tool_evaluation/evaluation.xml`, both verified):
  - `EVALUATION_PROMPT` system prompt: agent MUST use tools, output `<summary>` (steps, tools/order/why, inputs, outputs), `<feedback>` (tool names clear? params documented? descriptions accurate? errors/too many tokens? specific actionable improvements), `<response>` (concise; `NOT_FOUND` if unsolvable; numbers/IDs/exact text only; response last).
  - `agent_loop(prompt, tools)`: `client.messages.create(model="claude-sonnet-4-6", max_tokens=4096, system=EVALUATION_PROMPT, tools=tools)`; `while response.stop_reason == "tool_use"` dispatch tool, time it, record `tool_metrics[tool_name] = {"count", "durations"}`, append `tool_result`, loop.
  - `evaluation.xml` format: `<evaluation><task><prompt>…</prompt><response>…</response></task>…</evaluation>` (8 calculator tasks: compound interest 11614.72, projectile 87.25, sphere 304.65, std dev 7.61, pH 4.46, mortgage 1013.37, photon 3.61e-19, quadratic root 2).
  - `evaluate_single_task` → `score = int(response == expected)`, duration, tool call counts, summary, feedback; `run_evaluation(eval_path, tools)` → Markdown report (Accuracy, Average Task Duration, Average Tool Calls per Task, Total Tool Calls, per-task Prompt/Ground Truth/Actual/Correct/Duration/Tool Calls/Summary/Feedback).
  - Deliberately unhelpful `calculator_tool` (empty `description` and empty `expression` description) → result 7/8 (87.5%), avg 22.73 s, 7.75 tool calls/task, 62 total; feedback repeatedly asks for documented syntax (`**` not `^`), supported functions (round, sqrt, log), better error messages — demonstrating how the feedback drives description improvements.

### Hyperlinks
- MCP intro: https://modelcontextprotocol.io/docs/getting-started/intro ; MCP: https://modelcontextprotocol.io/ ; MCP SDK: https://modelcontextprotocol.io/docs/sdk ; local servers: https://modelcontextprotocol.io/docs/develop/connect-local-servers ; tool annotations: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- Claude Code: https://www.anthropic.com/claude-code
- llms.txt: https://docs.anthropic.com/llms.txt
- Desktop extensions: https://www.anthropic.com/engineering/desktop-extensions
- Tool use overview: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview ; implement tool use best practices: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#best-practices-for-tool-definitions and #tool-use-system-prompt → canonical now https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools (verified 307 redirect)
- Tool evaluation cookbook: https://platform.claude.com/cookbook/tool-evaluation-tool-evaluation (verified 200) ; GitHub https://github.com/anthropics/claude-cookbooks/tree/main/tool_evaluation
- Interleaved thinking: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#interleaved-thinking
- Tracing thoughts: https://www.anthropic.com/research/tracing-thoughts-language-model
- Web search tool: https://www.anthropic.com/news/web-search
- SWE-bench Sonnet: https://www.anthropic.com/engineering/swe-bench-sonnet
- Courses: https://anthropic.skilljar.com/

### Implementation checklist
1. Identify a few high-impact workflows; design consolidated tools (not endpoint wrappers) with distinct purposes and namespaced names.
2. Prototype quickly with Claude Code (feed it `llms.txt`/SDK docs); wrap in a local MCP server or MCPB; connect via `claude mcp add …` or Claude Desktop settings; try them by hand.
3. Generate dozens of realistic, multi-step eval tasks with verifiable answers (and optional expected tools); avoid trivial sandboxes; store as prompt/response pairs (e.g., XML like the cookbook).
4. Run a simple programmatic agent loop per task with a system prompt requiring summary/feedback/response blocks (or interleaved thinking); record accuracy, runtime, tool-call count, tokens, errors.
5. Read transcripts and CoT; look for redundant calls, invalid params, omitted behaviors.
6. Paste concatenated transcripts into Claude Code and let it refactor tools and descriptions; keep a held-out test set; iterate until performance plateaus.
7. Apply principles: return high-signal natural-language fields; add `response_format` (concise/detailed); add pagination/filtering/truncation with a token cap (~25k); write actionable error messages; describe tools like onboarding a new hire; unambiguous param names; test XML vs JSON vs Markdown response formats; test prefix vs suffix namespacing; add MCP tool annotations.
8. Re-run evals on every change; ship.

### Dependencies on other Anthropic articles
- Extends the "Tool design and selection" and "Let agents improve themselves" sections of the multi-agent research post.
- References "Desktop Extensions", "SWE-bench Sonnet", and is referenced by "Building agents with the Claude Agent SDK" (Tools section) and by the later "Advanced tool use" / "Effective context engineering" posts.

---

## 4. A postmortem of three recent issues

- **Title:** A postmortem of three recent issues
- **URL:** https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
- **Date:** Published Sep 17, 2025
- **Authors:** Sam McAllister, with thanks to Stuart Ritchie, Jonathan Gray, Kashyap Murali, Brennan Saeta, Oliver Rausch, Alex Palcuie, and others. (Some third-party coverage attributes it to Todd Underwood, Head of Reliability — the article byline itself is Sam McAllister.)
- **Blurb:** "This is a technical report on three bugs that intermittently degraded responses from Claude. Below we explain what happened, why it took time to fix, and what we're changing."

### Thesis
Between early August and early September 2025, three overlapping infrastructure bugs — a context-window routing error (Sonnet 4 short-context requests sent to 1M-context servers, worsened by an Aug 29 load-balancer change to 16% of requests at peak), an output-corruption misconfiguration on TPU servers (Thai/Chinese characters, syntax errors), and an XLA:TPU approximate top-k miscompilation exposed by a sampling rewrite (bf16/fp32 mixed precision) — intermittently degraded Claude's quality. Anthropic states plainly it never degrades quality for load/time-of-day; the causes were bugs. Detection was slow because the bugs overlapped across platforms with different symptoms, evals were too noisy (Claude "recovers well from isolated mistakes"), and privacy controls limited engineer access to user conversations. Remediation: more sensitive evals, continuous evals on true production systems, faster privacy-preserving debugging tooling, plus a request for continued user feedback (`/bug`, thumbs-down, feedback@anthropic.com).

### Every fact, root cause, timeline entry, detection failure, remediation
**Serving context**
- Claude served via first-party API, Amazon Bedrock, Google Cloud Vertex AI; hardware: AWS Trainium, NVIDIA GPUs, Google TPUs. "Strict equivalence standards for model implementations" across platforms; any infra change requires validation across all platforms.
- Statement: "We never reduce model quality due to demand, time of day, or server load. The problems our users reported were due to infrastructure bugs alone." / "In these recent incidents, we didn't meet that bar."

**Timeline (Claude API)**
- Early Aug: user reports hard to distinguish from normal feedback variation.
- **Aug 5**: Bug 1 introduced (~0.8% of Sonnet 4 requests).
- **Aug 11**: change merged containing a minimized reproducer that root-caused the Dec 2024 "bug" as expected `xla_allow_excess_precision` behavior.
- **Aug 12**: Bedrock misrouting peak 0.18% of Sonnet 4 requests (from this date).
- **Aug 25**: Bug 2 (TPU misconfiguration / output corruption) deployed; Bug 3's triggering token-selection code deployed.
- **Aug 26**: sampling-code rewrite deployed (removed Dec 2024 workaround → exposed approximate top-k bug).
- **Aug 27–Sep 16**: Vertex AI misrouting <0.0004%.
- **Aug 28**: Opus 4/4.1 output corruption ends (affected Aug 25–28).
- **Aug 29**: routine load-balancing change increases short-context traffic to 1M servers; negative reports spike (connection not immediately made).
- **Aug 31**: worst hour — **16%** of Sonnet 4 requests misrouted.
- Late Aug: investigation opened.
- **Sep 2**: Bug 2 rolled back (Sonnet 4 corruption Aug 25–Sep 2).
- **Sep 4**: Bug 1 routing fix deployed; Bug 3 rolled back for Haiku 3.5.
- **Sep 12**: Bug 3 rolled back for Opus 3 (after compatible user reports); Sonnet 4 also rolled back "out of an abundance of caution" though not reproducible.
- **Sep 16**: routing fix rollout complete on first-party + Vertex AI.
- **Sep 18**: routing fix rollout complete on Bedrock.
- **Sep 17**: postmortem published.

**Bug 1 — Context window routing error**
- Some Sonnet 4 requests misrouted to servers configured for the upcoming 1M-token context window. 0.8% initially → 16% at peak hour Aug 31. ~**30% of Claude Code users** who made requests in the period had at least one message misrouted. Bedrock peak 0.18%; Vertex <0.0004%.
- Routing is **"sticky"**: once served by the wrong server, follow-ups likely stayed there → some users hit much harder.
- Resolution: fixed routing logic so short- and long-context requests go to the correct pools; deployed Sep 4; rollouts complete Sep 16 (1P, Vertex) / Sep 18 (Bedrock).

**Bug 2 — Output corruption**
- Aug 25 misconfiguration on Claude API TPU servers; a runtime performance optimization occasionally assigned high probability to tokens that should rarely appear — Thai/Chinese characters in English responses (e.g., "สวัสดี" mid-response), obvious code syntax errors.
- Affected Opus 4.1 and Opus 4 Aug 25–28; Sonnet 4 Aug 25–Sep 2. Third-party platforms not affected.
- Resolution: rolled back Sep 2; added detection tests for unexpected character outputs to the deployment process.

**Bug 3 — Approximate top-k XLA:TPU miscompilation**
- Aug 25 code to improve token selection triggered a latent XLA:TPU compiler bug; confirmed on Haiku 3.5; possibly a subset of Sonnet 4 and Opus 3 on Claude API; third-party platforms unaffected.
- Deep dive: top-p sampling with thresholds "typically 0.99 or 0.999"; models partitioned across tens of chips → distributed sort. Dec 2024: TPU implementation occasionally dropped the most probable token at temperature 0 → workaround deployed. Root cause: probabilities computed in **bf16**, vector processor is **fp32-native**; XLA converts some ops to fp32 under the `xla_allow_excess_precision` flag (default true) → ops disagreed on the highest-probability token → token dropped. Aug 26 rewrite fixed precision and top-p limit handling and removed the December workaround → exposed a deeper bug in the **approximate top-k** op (`jax.lax.approx_max_k`), which "sometimes returned completely wrong results, but only for certain batch sizes and model configurations"; behavior varied with preceding/following ops and whether debugging tools were enabled; same prompt could pass then fail. Reproducer shared with XLA:TPU engineers returns correct results on CPU.
- Resolution: (a) working with the XLA:TPU team on a compiler fix; (b) switched from approximate to **exact top-k** (its performance penalty was no longer prohibitive) and standardized additional ops on fp32. "Model quality is non-negotiable, so we accepted the minor efficiency impact." Footnote 4: the corrected top-k may slightly change token inclusion near the top-p threshold; some users may benefit from re-tuning top-p.

**Why detection was difficult**
- Ordinary validation: benchmarks + safety evals + performance metrics; spot checks; small canary groups.
- Evals "simply didn't capture the degradation users were reporting, in part because Claude often recovers well from isolated mistakes."
- Privacy/security controls limit engineer access to user interactions not reported as feedback → couldn't examine/reproduce.
- Different symptoms per platform at different rates → "random, inconsistent degradation."
- Relied too heavily on noisy evaluations; couldn't connect online reports to specific changes; Aug 29 spike not linked to the load-balancing change.

**What's changing (remediation commitments)**
1. **More sensitive evaluations** that reliably differentiate working vs broken implementations; keep improving.
2. **Quality evaluations in more places**: run continuously on true production systems (would have caught the routing/load-balancing error).
3. **Faster debugging tooling**: infrastructure to debug community-sourced feedback without sacrificing privacy; bespoke tools to reduce remediation time.
- Ask for user signal: `/bug` in Claude Code, thumbs-down in Claude apps, feedback@anthropic.com for external evaluation methods.

### Concrete artifacts mentioned
- Flag: `xla_allow_excess_precision` (default true). Op: approximate top-k / `jax.lax.approx_max_k`. Images: Dec 2024 patch snippet; Aug 11 minimized reproducer; Slack reproducer message. Command: `/bug`. Email: feedback@anthropic.com.
- Footnotes: [1] XLA:TPU compiles XLA HLO (often from JAX) to TPU instructions; [2] distributed sort across tens of chips, vectorized ops vs serial algorithms; [3] approximate top-k accepted inaccuracy in lowest-probability tokens, but the bug dropped the highest; [4] top-p re-tuning note.

### Hyperlinks
- 1M context window docs: https://docs.claude.com/en/docs/build-with-claude/context-windows#1m-token-context-window and https://docs.claude.com/en/docs/build-with-claude/context-windows (now platform.claude.com)
- Temperature glossary: https://docs.claude.com/en/docs/about-claude/glossary#temperature
- bf16: https://github.com/tensorflow/tensorflow/blob/f41959ccb2d9d4c722fe8fc3351401d53bcf4900/tensorflow/core/framework/bfloat16.h
- fp32-native vector processor paper: https://dl.acm.org/doi/pdf/10.1145/3360307
- approx top-k JAX docs: https://docs.jax.dev/en/latest/_autosummary/jax.lax.approx_max_k.html ; algorithm paper: https://arxiv.org/pdf/2206.14286
- XLA architecture: https://openxla.org/xla/architecture ; JAX: https://docs.jax.dev/en/latest
- Coverage: https://simonwillison.net/2025/Sep/17/anthropic-postmortem/ ; https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs/ ; HN https://news.ycombinator.com/item?id=45281139 (from mirrors/search, unverified directly)

### Implementation checklist (for teams running model-serving infra)
1. Route by request type explicitly (short vs long context pools); test load-balancer changes against routing invariants; beware sticky sessions amplifying misroutes.
2. Add output-anomaly detectors (unexpected scripts/characters, syntax-error rates) to the deploy pipeline and canaries.
3. Treat numerical-precision changes (bf16/fp32, excess-precision flags, approximate ops) as quality-affecting; prefer exact ops when the cost is acceptable; standardize precision for sampling-critical paths.
4. When removing a workaround, prove the root cause and re-run targeted repros across batch sizes/configs; keep reproducers small and share with compiler vendors.
5. Build evals sensitive enough to distinguish working vs broken implementations (not just aggregate benchmarks); run them continuously in production, per platform.
6. Build privacy-preserving debugging tooling that can act on reported feedback; correlate report spikes with deploy/change logs.
7. Communicate transparently: explicit "we don't throttle quality" statement, timelines, per-platform impact, and user feedback channels.

### Dependencies on other Anthropic articles
- Standalone; later referenced by the April 2026 "An update on recent Claude Code quality reports" postmortem (https://www.anthropic.com/engineering/april-23-postmortem, from search).

---

## 5. Building agents with the Claude Agent SDK

- **Title:** Building agents with the Claude Agent SDK
- **URL:** https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk (mirror shows it now canonically at https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- **Date:** September 29, 2025
- **Authors:** Thariq Shihipar, with notes/editing from Molly Vorwerck, Suzanne Wang, Alex Isken, Cat Wu, Keir Bradwell, Alexander Bricken, Ashwin Bhat.
- **Blurb:** "The Claude Agent SDK is a collection of tools that helps developers build powerful agents on top of Claude Code. In this article, we walk through how to get started and share our best practices."

### Thesis
Claude Code's harness turned out to be a general agent harness (used internally for research, video, note-taking, and "almost all of our major agent loops"), so the Claude Code SDK is renamed the Claude Agent SDK. Its core design principle is "give your agents a computer" — the same terminal/file tools programmers use. Agents run a loop of **gather context → take action → verify work → repeat**; the post maps SDK features onto each phase via an email-agent example: context via agentic (file-system/grep) search, optional semantic search, subagents with isolated contexts, and automatic compaction; action via well-designed tools, bash/scripts, code generation, and MCP integrations; verification via rules-based feedback (linting, validators), visual feedback (screenshots, Playwright), and LLM-as-judge. Then test by inspecting failures, asking whether the agent has the right tools/information/rules, and building representative evals.

### Every concept, technique, recommendation
- **Background**: "Building effective agents" (2024) → Claude Code released for internal dev productivity → became far more than a coding tool. Rename: Claude Code SDK → **Claude Agent SDK**.
- **Giving Claude a computer**: Claude needs the tools programmers use daily — find files, write/edit, lint, run, debug, iterate. Terminal access made it good at non-coding tasks too (read CSVs, search web, build visualizations, interpret metrics). "The key design principle behind the Claude Agent SDK is to give your agents a computer, allowing them to work like humans do."
- **New types of agents**: finance agents (portfolio, external APIs, store data, run calculations); personal assistants (travel, calendar, appointments, briefs, internal data sources); customer support (high-ambiguity tickets, user data, external APIs, message users, escalate to humans); deep research agents (search file systems across large document collections, synthesize, cross-reference, generate reports).
- **The agent loop**: gather context → take action → verify work → repeat.
- **Gather context**
  - *Agentic search & the file system*: the file system "represents information that could be pulled into the model's context"; Claude uses bash like `grep` and `tail` to decide how to load large files (logs, uploads); folder/file structure is "a form of context engineering." Email agent: store prior conversations in a `Conversations` folder.
  - *Semantic search*: faster but "less accurate, more difficult to maintain, and less transparent"; chunking → embeddings → vector query. Start with agentic search; add semantic search only for speed or more variation.
  - *Subagents*: supported by default; two benefits — parallelization and context management (isolated context windows, return only relevant info). Email agent: "search subagent" fanning out multiple queries over email history, returning excerpts not full threads.
  - *Compaction*: automatically summarizes previous messages as the context limit approaches; built on Claude Code's `/compact` slash command.
- **Take action**
  - *Tools*: "the primary building blocks of execution"; prominent in context → design for context efficiency; tools should be the primary actions (email agent: `fetchInbox`, `searchEmails`). Links to custom tools docs and the tools post.
  - *Bash & scripts*: general-purpose flexible work; email example: write code to download a PDF attachment, convert to text, search it.
  - *Code generation*: "Code is precise, composable, and infinitely reusable"; ask "which tasks would benefit from being expressed as code?"; Claude.ai file creation is built entirely on code generation (Python scripts generating Excel/PowerPoint/Word). Email example: user-defined inbound-email rules implemented as code run on the event.
  - *MCPs*: standardized integrations (auth + API calls handled); connect to Slack, GitHub, Google Drive, Asana without custom OAuth; email example: `search_slack_messages`, `get_asana_tasks`; growing MCP ecosystem (modelcontextprotocol/servers).
- **Verify your work**: agents that check/improve their own output "catch mistakes before they compound, self-correct when they drift, and get better as they iterate." Three approaches:
  - *Defining rules*: best form of feedback — clearly defined rules + which rule failed and why; linting; generate TypeScript and lint it rather than plain JavaScript (more feedback layers); email: validate address (error) and check whether user has emailed them before (warning).
  - *Visual feedback*: screenshots/renders for UI generation/testing; screenshot generated HTML email and feed back; checks for layout, styling, content hierarchy, responsiveness (single screenshot has limited viewport info); use a Playwright MCP server to automate screenshots at multiple viewports and test interactions.
  - *LLM as a judge*: another model judges against fuzzy rules; "generally not a very robust method, and can have heavy latency tradeoffs," but useful where any boost is worth it; email: a subagent judges draft tone against prior messages.
- **Testing and improving**: look carefully at failures; "put yourself in its shoes: does it have the right tools for the job?" Questions: misunderstands task → missing info → restructure search APIs; fails repeatedly → add a formal rule in tool calls; can't fix errors → give more useful/creative tools; performance varies as features are added → build a representative test set for programmatic evals based on customer usage.
- **Getting started**: SDK gives Claude a computer to write files, run commands, iterate; migrate existing Claude Code SDK users via the migration guide.

### Concrete SDK details (from docs, verified at code.claude.com)
- **Packages**: TypeScript `@anthropic-ai/claude-agent-sdk` (was `@anthropic-ai/claude-code`); Python `claude-agent-sdk` (was `claude-code-sdk`). Repos: https://github.com/anthropics/claude-agent-sdk-python (verified; created Jun 2025), https://github.com/anthropics/claude-agent-sdk-typescript (verified; created Sep 27, 2025), demos https://github.com/anthropics/claude-agent-sdk-demos (verified; includes `email-agent`).
- **Install**: `npm install @anthropic-ai/claude-agent-sdk` (+ `npm install --save-dev tsx`), or `pip install claude-agent-sdk` / `uv add claude-agent-sdk`. Node 18+ / Python 3.10+. SDKs bundle a native Claude Code binary. Set `ANTHROPIC_API_KEY`; or `CLAUDE_CODE_USE_BEDROCK=1`, `CLAUDE_CODE_USE_VERTEX=1`, `CLAUDE_CODE_USE_FOUNDRY=1`, `CLAUDE_CODE_USE_ANTHROPIC_AWS=1`.
- **Migration breaking changes**: Python `ClaudeCodeOptions` → `ClaudeAgentOptions`; imports `claude_code_sdk` → `claude_agent_sdk`; system prompt no longer Claude Code's by default — use `systemPrompt: { type: "preset", preset: "claude_code" }` (optionally `append`) or a custom string; settings/filesystem loading is opt-in via `setting_sources`.
- **Quickstart code (Python)**:
  ```python
  from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
  async for message in query(
      prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
      options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Glob"], permission_mode="acceptEdits"),
  ): ...
  ```
  TypeScript: `for await (const message of query({ prompt, options: { allowedTools: ["Read","Edit","Glob"], permissionMode: "acceptEdits" } }))`.
- **Key `ClaudeAgentOptions` fields** (Python; TS `Options` is camelCase): `tools` (or preset `{"type":"preset","preset":"claude_code"}`), `allowed_tools`, `disallowed_tools`, `system_prompt` (str | preset | custom | file), `mcp_servers`, `strict_mcp_config`, `permission_mode` (`default`, `acceptEdits`, `plan`, `bypassPermissions`, …), `continue_conversation`, `resume`, `session_id`, `fork_session`, `max_turns`, `max_budget_usd`, `model`, `fallback_model`, `cwd`, `cli_path`, `add_dirs`, `env`, `can_use_tool` (callback), `hooks` (PreToolUse, PostToolUse, PreCompact, …), `agents: dict[str, AgentDefinition]` (programmatic subagents: `description`, `prompt`, `tools`, `model`, …), `setting_sources`, `skills`, `plugins`, `sandbox`, `thinking`/`effort`, `output_format`, `enable_file_checkpointing`, `task_budget`, `include_partial_messages`.
- **Custom tools**: `@tool("name", "description", {schema})` (Python) / `tool(name, description, zodSchema, handler)` (TS) → `create_sdk_mcp_server` / `createSdkMcpServer({ name, tools })` → pass in `mcpServers`; handler returns `{ content: [...], structuredContent?, isError? }`; annotations like `readOnlyHint: true` allow parallel calls.
- **Built-in tools**: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, Agent (subagents), NotebookEdit, TodoWrite, etc. Tool combos: `Read/Glob/Grep` read-only; `Read/Edit/Glob` modify; `+Bash` full automation.
- **Subagents** (docs): defined via `agents` option (recommended) or `.claude/agents/*.md`; invoked via the `Agent` tool; isolated context; per-agent tool restrictions and model choice.
- **Sessions**: `resume`, `fork_session`, `list_sessions()`, `get_session_messages()`; **Compaction**: automatic, with `PreCompact` hook (`trigger: manual|auto`).

### Hyperlinks (article)
- Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Claude Code: https://claude.com/product/claude-code ; How Anthropic teams use Claude Code: https://www.anthropic.com/news/how-anthropic-teams-use-claude-code ; harness post: https://claude.com/blog/harnessing-claudes-intelligence
- Key design principle talk (YouTube): https://www.youtube.com/watch?v=vLIDHi-1PVU
- Context management: http://anthropic.com/news/context-management ; Contextual retrieval (semantic search): https://www.anthropic.com/news/contextual-retrieval
- Subagents docs: https://docs.claude.com/en/api/agent-sdk/subagents → canonical https://code.claude.com/docs/en/agent-sdk/subagents (verified)
- /compact: https://docs.claude.com/en/docs/claude-code/sdk/sdk-slash-commands#%2Fcompact-compact-conversation-history
- Writing tools post: https://www.anthropic.com/engineering/writing-tools-for-agents ; Custom tools: https://docs.claude.com/en/api/agent-sdk/custom-tools → https://code.claude.com/docs/en/agent-sdk/custom-tools (verified)
- File creation: https://www.anthropic.com/news/create-files ; Claude.ai: http://claude.ai
- MCP: https://modelcontextprotocol.io/ ; MCP servers: https://github.com/modelcontextprotocol/servers
- Linting (SO): https://stackoverflow.com/questions/8503559/what-is-linting
- Get started: https://docs.claude.com/en/api/agent-sdk/overview → https://code.claude.com/docs/en/agent-sdk/overview (verified) ; Migration: https://docs.claude.com/en/docs/claude-code/sdk/migration-guide → https://code.claude.com/docs/en/agent-sdk/migration-guide (verified)
- Also verified: quickstart https://code.claude.com/docs/en/agent-sdk/quickstart ; Python ref https://code.claude.com/docs/en/agent-sdk/python ; TS ref https://code.claude.com/docs/en/agent-sdk/typescript ; docs index https://code.claude.com/docs/llms.txt ; npm https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk

### Implementation checklist
1. Install the SDK (`npm install @anthropic-ai/claude-agent-sdk` or `pip install claude-agent-sdk`), set `ANTHROPIC_API_KEY` (or Bedrock/Vertex/Foundry env vars); migrate imports/options if coming from the Claude Code SDK.
2. Define the agent's job in terms of the loop: what context it needs, what actions it takes, how it verifies.
3. Context: lay out a working directory/file structure as context engineering (e.g., `Conversations/`); rely on agentic search (grep/tail/glob) first; add vector search via MCP only if needed; define search subagents (`agents={...}`) for parallel, context-isolated retrieval; rely on automatic compaction (hook `PreCompact` if needed).
4. Action: implement a few primary tools as custom tools (`@tool` + `create_sdk_mcp_server`) with context-efficient outputs; allow `Bash` for flexible scripting; push complex/repeatable logic into generated code; add MCP servers (Slack, GitHub, Drive, Asana, Playwright) via `mcp_servers`.
5. Verification: encode rules (validators, linters, typed languages) that return which rule failed and why; add visual feedback (screenshots/Playwright) for visual outputs; optionally an LLM/subagent judge for fuzzy criteria.
6. Configure permissions (`allowed_tools`, `permission_mode`, `can_use_tool`, hooks) and budgets (`max_turns`, `max_budget_usd`).
7. Run, inspect failures, and ask the four diagnostic questions (missing info → better search APIs; repeated failure → formal rule; can't fix → more/creative tools; regressions → representative eval set from customer usage).
8. Build programmatic evals; iterate; deploy (hosting docs: Docker/cloud/CI).

### Dependencies on other Anthropic articles
- Builds directly on "Building effective agents" and "Writing effective tools for agents"; references "Contextual retrieval", "Context management", "How Anthropic teams use Claude Code", and the Claude Code harness post. Later posts that extend it: "Effective context engineering for AI agents", "Effective harnesses for long-running agents", "Equipping agents for the real world with Agent Skills" (from search results).

---

## Cross-article map (Batch B)
- Multi-agent research (Jun 2025) → introduces orchestrator-worker, token-scaling insight, tool-testing agent → **Writing tools** (Sep 2025) formalizes the tool eval/optimization loop → **Agent SDK** (Sep 2025) packages subagents, compaction, custom tools, MCP into a product harness.
- **Desktop Extensions/MCPB** (Jun 2025) is the distribution layer for the MCP tools the tools post says to prototype; the tools post explicitly recommends wrapping prototypes as DXT/MCPB.
- **Postmortem** (Sep 2025) is orthogonal (serving infra) but shares the theme of evaluation sensitivity and privacy-preserving observability seen in the multi-agent post's tracing section.
