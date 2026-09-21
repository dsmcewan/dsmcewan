# Research notes — Batch C: Anthropic engineering posts on context, skills, sandboxing, MCP, advanced tool use

Compiled 2026-09-21. Network constraints: anthropic.com, web.archive.org, agentskills.io, simonwillison.net, medium.com, dev.to, substack and most third-party blogs were EGRESS-BLOCKED. Verified sources actually fetched: platform.claude.com docs (tool-search-tool, programmatic-tool-calling, define-tools, code-execution-tool, memory-tool, context-editing, agent-skills overview + best-practices, skills-guide), code.claude.com docs (skills, sandboxing, sandbox-environments, settings-reference, mcp, claude-code-on-the-web), raw GitHub (anthropic-experimental/sandbox-runtime README, anthropics/skills README + skill-creator SKILL.md + template, agentskills/agentskills docs/specification.mdx, anthropics/claude-cookbooks notebooks), the Claude Cookbook page for context engineering, and many WebSearch snippets that quote the articles verbatim. Anything not confirmed by one of those is marked **(from memory, unverified)**. Code blocks marked "reconstructed" are faithful reconstructions of the article's samples from snippets + memory; exact whitespace/comments may differ.

---

## 1. Effective context engineering for AI agents

- **Title:** Effective context engineering for AI agents
- **URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Date:** September 29, 2025 (verified via search snippets; published alongside Claude Sonnet 4.5 / Claude Agent SDK launch)
- **Authors:** Anthropic Applied AI team — Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (verified). Acknowledged contributors **(from memory, unverified)**: Rafi Ayub, Hannah Moran, Cal Rueb, Connor Jennings, Molly Vorwerck, Drew Roper, Jenny Lu.

### Thesis (one paragraph)
Building with LLMs is shifting from *prompt engineering* (finding the right words) to *context engineering*: deliberately curating and maintaining the optimal set of tokens (system prompt, tools, examples, message history, retrieved data, metadata) that the model sees at each step of inference. Because LLMs have a finite "attention budget" and suffer "context rot" as context grows, the guiding principle is to find "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." The post lays out how to do that for each context component, when to retrieve context just-in-time vs. up front, and three techniques for long-horizon agents — compaction, structured note-taking, and sub-agent architectures — and closes by saying to "do the simplest thing that works" and lean on increasingly capable models rather than prescriptive scaffolding.

### Concepts, principles, recommendations (exhaustive)

**Context engineering vs. prompt engineering**
- "Context" = the set of tokens included when sampling from an LLM. Context engineering = "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."
- Prompt engineering = writing/organizing instructions (esp. system prompt) for one-shot classification/text tasks. Context engineering "considers the entire state available to the model — not just the prompt, but tools, examples, message history, retrieved data, and metadata."
- Framing question: "what configuration of context is most likely to generate our model's desired behavior?"
- Context engineering is iterative and cyclical: curation happens "each time we decide what to pass to the model," as agents loop over turns and accumulate tool outputs.
- Core question: "what configuration of context is most likely to generate our model's desired behavior?" and "which tokens deserve to be there at every step."

**Why context matters: the finite attention budget**
- "Studies on needle-in-a-haystack style benchmarking have uncovered the concept of *context rot*: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." (Links to Chroma's "Context Rot" research — https://research.trychroma.com/context-rot — **link target from memory, unverified**.)
- LLMs have an "attention budget"; "every new token introduced depletes this budget by some amount."
- Architectural reason: transformers attend pairwise across all tokens → n² relationships for n tokens; attention gets "stretched thin" as context grows.
- Training-data reason: models see far more short sequences than long ones, so they have less experience/fewer specialized parameters for long-range dependencies. Position-encoding interpolation lets models handle longer sequences with degraded token-position understanding.
- Result: a "gradient" of degradation, not a cliff. Models remain capable at long context but with reduced precision on retrieval and long-range reasoning.
- Therefore: "context must be treated as a finite resource with diminishing marginal returns."

**Anatomy of effective context**
- Guiding principle: "find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

*System prompts*
- "Extremely clear and use simple, direct language that presents ideas at the right altitude for the agent."
- "Right altitude" = "the Goldilocks zone between two common failure modes": (a) "hardcode complex, brittle logic in their prompts to elicit exact agentic behavior" → fragility, maintenance burden; (b) "vague, high-level guidance that fails to give the LLM concrete signals for desired outputs or falsely assumes shared context."
- Best: "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics to guide behavior."
- Organize into distinct sections (e.g. `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`) using XML tags or Markdown headers, though "the exact formatting of prompts is likely becoming less important as models become more capable."
- "Strive for the minimal set of information that fully outlines your expected behavior. Note that minimal does not necessarily mean short."
- Recommended process: "start by testing a minimal prompt with the best model available… then add clear instructions and examples to improve performance based on failure modes found during initial testing."

*Tools*
- Tools define the contract between agents and their environment; they should "promote efficiency" — "returning information that is token-efficient" and "encouraging efficient agent behaviors."
- "Tools should be self-contained, robust to error, and unambiguous in their intended use."
- Input parameters should be descriptive, unambiguous, and "play to the inherent strengths of the model."
- Common failure: "bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use." Heuristic: "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."
- Curate a "minimal viable set of tools," which also eases maintenance and pruning. (Cross-references the "Writing tools for agents" post.)

*Examples (few-shot)*
- Few-shot is a well-known best practice, but don't "stuff a laundry list of edge cases into a prompt."
- "Curate a set of diverse, canonical examples that effectively portray the expected behavior of the agent." "For an LLM, examples are the 'pictures' worth a thousand words."
- Overall: "be thoughtful and keep your context informative, yet tight."

**Context retrieval and agentic search**
- Traditional approach: embedding-based pre-inference retrieval (RAG) surfacing context up front.
- Emerging approach: "just-in-time" context — "agents maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."
- Claude Code example: uses this to do complex analysis over large databases "without ever loading the full data objects into context"; writes targeted queries, stores results, uses `head`/`tail` on large files.
- Analogy: "mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks."
- Metadata is signal: "file sizes suggest complexity; naming conventions hint at purpose; timestamps can be a proxy for relevance"; a `test_utils.py` in a `tests` folder vs `src/core_logic.py` implies different purpose. "The metadata of these references provides a mechanism to efficiently refine behavior."
- Progressive disclosure: "Agents can progressively discover relevant context through exploration," building understanding layer by layer and keeping only what's relevant in working memory.
- Trade-off: runtime exploration is slower than pre-computed retrieval; can misnavigate. A hybrid is often best.
- Claude Code "employs a hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees."
- Hybrid fits when content is fairly static (legal, finance) — retrieve some up front for speed, discover the rest at runtime.
- "As models improve, the trend is toward letting intelligent models act intelligently" — less human curation, more agent autonomy; "do the simplest thing that works."

**Long-horizon tasks** (tasks that span more than one context window, e.g. large codebase migrations, long research projects)
1. *Compaction*: "taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary." Claude Code's auto-compact passes message history to the model to summarize; preserves "architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs or messages." Tuning: "start by maximizing recall… then iterate to improve precision." "Tool result clearing" — once a tool was called deep in history, "the agent rarely needs to see the raw result again" — is "one of the safest, lightest touch forms of compaction" and "was most recently launched as a feature on the Claude Developer Platform" (context editing / `clear_tool_uses_20250919`).
2. *Structured note-taking (agentic memory)*: "the agent regularly writes notes persisted to memory outside of the context window," pulled back later. Examples: Claude Code creating a to-do list; a custom agent maintaining a `NOTES.md`. Claude playing Pokémon: "maintains precise tallies across thousands of game steps — tracking… training progress, remembering combat strategies, maintaining maps of explored regions"; after context resets, reads its own notes and continues multi-hour sequences. The memory tool (file-based directory) is available "in public beta on the Claude Developer Platform" alongside Claude Sonnet 4.5.
3. *Sub-agent architectures*: specialized sub-agents with clean context windows; "the main agent coordinates with a high-level plan while subagents perform deep technical work." "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)." Clear "separation of concerns." Anthropic's multi-agent research system showed "substantial improvements over single-agent systems on complex research tasks."
- Choosing: compaction for tasks needing extensive back-and-forth; note-taking for iterative development with clear milestones; multi-agent for parallel exploration.

**Conclusion**
- "Context is a critical but finite resource for AI agents."
- As models get smarter, "less prescriptive engineering" is needed; goal is to "do the simplest thing that works."

### Concrete configuration / API surface referenced (verified from platform docs)
- **Memory tool**: `{"type": "memory_20250818", "name": "memory"}` in `tools`. No beta header required today (was `context-management-2025-06-27` at launch — **launch-time header from memory, unverified**). Client-side; commands `view` (with optional `view_range`), `create` (`file_text`), `str_replace` (`old_str`,`new_str`), `insert` (`insert_line`,`insert_text`), `delete`, `rename` (`old_path`,`new_path`). All paths under `/memories`; must guard against path traversal (`/memories/../../secrets.env`). API auto-injects a system instruction: "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE… ASSUME INTERRUPTION…". SDK helpers: `BetaLocalFilesystemMemoryTool` (Python/TS), `BetaAbstractMemoryTool` (Python/C#), `betaMemoryTool` (TS), `BetaMemoryToolHandler` (Java). Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- **Context editing** (beta header `anthropic-beta: context-management-2025-06-27`, request param `context_management.edits[]`):
  - `clear_tool_uses_20250919`: `trigger` (default `{"type":"input_tokens","value":100000}`; also `tool_uses`), `keep` (default `{"type":"tool_uses","value":3}`), `clear_at_least` (`{"type":"input_tokens","value":N}`), `exclude_tools: [...]`, `clear_tool_inputs: bool` (default false). Cleared results replaced with placeholder text; invalidates prompt cache prefix.
  - `clear_thinking_20251015`: `keep: {"type":"thinking_turns","value":N}` or `"all"`; must be listed before `clear_tool_uses` when combined.
  - Response: `context_management.applied_edits[]` with `cleared_tool_uses`, `cleared_input_tokens`, `cleared_thinking_turns`. `count_tokens` supports `context_management` and returns `original_input_tokens`.
  - Docs: https://platform.claude.com/docs/en/build-with-claude/context-editing
- **Server-side compaction** (later, Jan 2026): `compact_20260112`, beta `compact-2026-01-12`, `trigger` default 150K (min 50K), `instructions`, `pause_after_compaction`. Docs: https://platform.claude.com/docs/en/build-with-claude/compaction
- Example (verified from docs):
```python
response = client.beta.messages.create(
    model="claude-opus-5", max_tokens=4096,
    messages=[{"role": "user", "content": "Create a Python calculator app"}],
    tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool", "max_characters": 10000},
           {"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{
        "type": "clear_tool_uses_20250919",
        "trigger": {"type": "input_tokens", "value": 30000},
        "keep": {"type": "tool_uses", "value": 3},
        "clear_at_least": {"type": "input_tokens", "value": 5000},
        "exclude_tools": ["web_search"]}]},
)
```
- Cookbook results (verified, https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools): research agent reading 8 docs (~40K tokens each, 320K total). Baseline peak 335,279 tokens (hits 200K limit); compaction@180K → peak 169,164, one ~2,783-token summary; clearing@30K keep=4 → peak 173,137, 4 clearing events, 7/8 file reads cleared; memory: session 2 without memory 8 file reads/peak 333,977 vs with memory 4 reads/peak 172,623.

### Links referenced by / relevant to the article
- Chroma "Context Rot" research: https://research.trychroma.com/context-rot **(from memory, unverified)**
- Anthropic "How we built our multi-agent research system": https://www.anthropic.com/engineering/multi-agent-research-system
- "Writing effective tools for AI agents—using AI agents": https://www.anthropic.com/engineering/writing-tools-for-agents
- "Building effective agents": https://www.anthropic.com/engineering/building-effective-agents
- Claude Agent SDK: https://code.claude.com/docs/en/agent-sdk (article linked docs.claude.com/en/api/agent-sdk/overview at the time — **unverified**)
- Memory tool docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- Context editing docs: https://platform.claude.com/docs/en/build-with-claude/context-editing
- Compaction docs: https://platform.claude.com/docs/en/build-with-claude/compaction
- Cookbook notebook: https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/context_engineering/context_engineering_tools.ipynb ; cookbook page https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools ; memory cookbook https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/memory_cookbook.ipynb ; https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/automatic-context-compaction.ipynb
- Claude Plays Pokémon (Twitch/X thread) **(from memory, unverified)**
- Third-party summaries seen in search: https://howaiworks.ai/blog/anthropic-context-engineering-for-agents, https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/anthropic/, https://inkeep.com/blog/fighting-context-rot, https://quyennv.com/blog/context-engineering-for-ai-agents/

### Implementation checklist
1. Inventory every token source in your agent loop: system prompt, tool definitions, examples, history, retrieved docs, metadata.
2. Rewrite the system prompt at the "right altitude": sections (`<background_information>`, `<instructions>`, tool guidance, output description), simple language, minimal-but-complete; test a minimal prompt on the best model first, then add instructions/examples from observed failures.
3. Prune tools to a minimal, non-overlapping set; make each self-contained, error-robust, token-efficient in outputs, with unambiguous names/params (apply "Writing tools for agents").
4. Replace edge-case laundry lists with 3–5 diverse canonical examples.
5. Prefer just-in-time retrieval: expose lightweight references (paths, queries, URLs) and tools like grep/glob/`head`/`tail`; drop stable, always-needed context (e.g. CLAUDE.md) in up front (hybrid).
6. Add compaction: enable server-side `clear_tool_uses_20250919` (tune `trigger`/`keep`/`exclude_tools`), or `compact_20260112`; tune for recall first then precision.
7. Add structured note-taking: give the agent a `NOTES.md`/to-do file or the `memory_20250818` tool with a path-traversal-safe handler; instruct it to record progress and re-read on start.
8. For parallelizable research, split into sub-agents that return 1–2K-token summaries to an orchestrator.
9. Measure with real long-horizon tasks (peak context tokens, task success), iterate, and remove scaffolding as models improve.

### Dependencies on other Anthropic engineering articles
- Builds on "Building effective agents" (Dec 2024) and "Writing effective tools for AI agents" (Sep 2025); cites "How we built our multi-agent research system" (Jun 2025). Later posts that depend on it: "Effective harnesses for long-running agents" (Nov 2025, memory + initializer pattern), Agent Skills post (progressive disclosure), Code execution with MCP, Advanced tool use (docs explicitly call tool search "an instance of the broader just-in-time retrieval principle described in Effective context engineering").

---

## 2. Equipping agents for the real world with Agent Skills

- **Title:** Equipping agents for the real world with Agent Skills
- **URL:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Date:** October 16, 2025 (verified; same day as the product announcement https://claude.com/blog/skills)
- **Authors:** Barry Zhang, Keith Lazuka, Mahesh Murag (verified via search snippet). Companion talk: "Don't build agents, build skills instead" (Barry Zhang & Mahesh Murag, AI Engineer).

### Thesis
General-purpose agents (Claude + a code-execution/filesystem environment) lack the *procedural knowledge* — the organizational context, workflows, and domain conventions — that human experts carry. Agent Skills fix this with a simple, open, filesystem-based format: a directory containing a `SKILL.md` (YAML frontmatter with `name` and `description`, plus Markdown instructions) and optional bundled scripts, references and assets. Skills work like "an onboarding guide for a new hire." Because the agent loads them through *progressive disclosure* — only name/description are always in context; the body loads on trigger; bundled files load or execute only as needed — the amount of expertise a skill can carry is "effectively unbounded" without paying a context cost. Skills can include executable code for deterministic steps, compose with MCP tools, and are portable across Claude.ai, Claude Code, the Claude Agent SDK and the Developer Platform.

### Concepts, principles, recommendations (exhaustive)
- **Definition:** "Agent Skills are organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks."
- **Motivation:** models are capable generalists but lack "the procedural knowledge needed to perform specialized tasks consistently"; previously users re-explained context each conversation or built bespoke agents. Skills let one general agent be "specialized" on demand and "composable."
- **Prerequisite architecture:** Skills assume a *code execution environment* — "an agent like Claude can access the filesystem, run bash commands, and execute code." The agent reads skill files with the same bash/file tools it uses for anything else.
- **Anatomy of a skill:**
  - `SKILL.md` (required) — YAML frontmatter with `name` and `description` (metadata) followed by Markdown instructions (the body).
  - Optional bundled files: additional Markdown (e.g. `forms.md`, `reference.md`), `scripts/` (executable code), templates/assets.
  - Example in the post: a `pdf` skill — `SKILL.md` with quick-start instructions; `forms.md` for form-filling; `reference.md` for detailed API reference; `scripts/fill_form.py`, `scripts/validate.py` (file names reconstructed from docs; the docs' canonical example uses `FORMS.md`, `REFERENCE.md`, `scripts/fill_form.py`).
- **Progressive disclosure** ("the core design principle that makes skills flexible and scalable"):
  1. Level 1 — metadata (`name` + `description`) is "pre-loaded into the system prompt" at startup for every installed skill (~100 tokens each per docs). "Gives the agent enough information to decide whether a skill is relevant, without loading the full content."
  2. Level 2 — when the task matches, the agent reads the full `SKILL.md` body (docs: keep < 5k tokens / < 500 lines).
  3. Level 3+ — "linked files form the third level and beyond, which the agent navigates and discovers only as needed." "The amount of context bundled into a skill is effectively unbounded."
  - Analogy: a table of contents → chapters → appendices; or a new hire's onboarding folder.
- **Skills can include code:** "for tasks requiring deterministic reliability" — e.g. a Python script that extracts PDF form fields. Scripts are *executed*, not read, so "only their output enters context"; more reliable, consistent and cheaper than having the model regenerate the code each time.
- **Relationship to MCP:** Skills "complement Model Context Protocol (MCP) servers by teaching agents more complex workflows that involve external tools" — MCP provides tool access; skills provide know-how for using those tools well (docs advise fully-qualified names `Server:tool_name` inside skills).
- **Where skills run:** Claude.ai (upload zip, Settings > Features), Claude Code (`~/.claude/skills/`, `.claude/skills/`, plugins), Claude Agent SDK, Claude Developer Platform (Skills API + code execution container). Anthropic ships pre-built document skills (`pptx`, `xlsx`, `docx`, `pdf`) that power Claude's file creation.
- **Authoring guidance (from post + docs):**
  - Start from a workflow you repeatedly explain to Claude; capture it as a skill; keep `SKILL.md` concise ("Claude is already very smart" — only add context it lacks).
  - Write the `description` in third person, saying what the skill does AND when to use it, with trigger keywords; skill-creator adds: make descriptions "a little bit pushy" because Claude tends to under-trigger.
  - Use the bundled `skill-creator` skill to scaffold, test, benchmark and optimize skills; iterate with Claude itself ("Claude A" authors, "Claude B" tests).
  - Set the right "degree of freedom": prose for open-ended tasks, parameterized pseudocode for preferred patterns, exact scripts for fragile sequences.
  - Prefer checklists/workflows and validate→fix feedback loops; keep file references one level deep; add a table of contents to reference files > 100 lines; avoid time-sensitive info; consistent terminology; forward-slash paths.
  - Test with every model you'll use (Haiku/Sonnet/Opus) and build evals before writing extensive docs.
- **Security:** "install skills only from trusted sources"; audit less-trusted skills thoroughly (scripts, fetched URLs, tool use patterns); treat like installing software; malicious skills can exfiltrate data or misuse tools.
- **Looking ahead:** Anthropic "hopes to enable agents to create, edit, and evaluate Skills on their own, letting them codify their own patterns of behavior into reusable capabilities"; skills as a shared, portable format across the ecosystem (later formalized as the open Agent Skills spec at agentskills.io, Dec 18, 2025, adopted by Microsoft/GitHub/VS Code, Cursor, Goose, Amp, OpenCode, OpenAI).

### Concrete formats, files, commands, API (verified)

**Agent Skills spec (agentskills.io / github.com/agentskills/agentskills/docs/specification.mdx)**
```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...
```
Frontmatter fields:
| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1–64 chars; lowercase a–z, 0–9, hyphens; no leading/trailing/consecutive hyphens; must match directory name |
| `description` | Yes | 1–1024 chars, non-empty; what it does + when to use it |
| `license` | No | license name or bundled file |
| `compatibility` | No | ≤500 chars; environment requirements |
| `metadata` | No | string→string map |
| `allowed-tools` | No | space-separated pre-approved tools (experimental), e.g. `Bash(git:*) Bash(jq:*) Read` |
Progressive disclosure budgets: metadata ~100 tokens; instructions < 5000 tokens recommended; keep `SKILL.md` under 500 lines; references one level deep. Validate with `skills-ref validate ./my-skill`.

Minimal SKILL.md:
```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
# PDF Processing
## Quick start
Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```
Platform-docs field rules (Claude API): `name` cannot contain XML tags or the reserved words "anthropic"/"claude"; `description` max 1024 chars, no XML tags.

**Claude Code SKILL.md frontmatter** (https://code.claude.com/docs/en/skills): `name`, `description`, `when_to_use`, `disable-model-invocation` (bool; hide from Claude, user-only e.g. `/deploy`), `user-invocable` (bool; false = hidden from `/` menu), `allowed-tools` (e.g. `Bash(git add *) Bash(git commit *)`), `disallowed-tools`, `model`, `effort` (`low|medium|high|xhigh|max`), `context: fork`, `agent` (`Explore|Plan|general-purpose`), `background` (bool), `argument-hint`, `arguments` (named positional), `paths` (globs gating auto-load), `shell` (`bash|powershell`), `hooks`, `metadata`, `license`, `compatibility`. Substitutions: `$ARGUMENTS`, `$ARGUMENTS[N]`/`$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_EFFORT}`. Dynamic context injection: `` !`git diff HEAD` `` (disable with `disableSkillShellExecution: true`). Locations: `~/.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`, nested `<subdir>/.claude/skills/`, managed/enterprise, `--add-dir`, plugins (`/plugin-name:skill-name`). Visibility: `"skillOverrides": {"deploy": "off", "legacy": "name-only"}`; permission rules `Skill(commit)`, `Skill(deploy *)`. Install Anthropic's examples: `/plugin marketplace add anthropics/skills` then install `document-skills` or `example-skills`.

**Skills API (Developer Platform)** (https://platform.claude.com/docs/en/build-with-claude/skills-guide): requires the code execution tool; up to 20 skills per request; upload < 30 MB uncompressed; workspace-scoped.
```python
from anthropic.lib import files_from_dir
skill = client.skills.create(files=files_from_dir("financial_skill"))   # skill_01…, skill.latest_version_id (skver_…)
client.skills.versions.create(skill_id=skill.id, files=files_from_dir("financial_skill"))
client.skills.list(source="custom"); client.skills.retrieve(skill_id=...); client.skills.delete(skill_id=...)
response = client.messages.create(
    model="claude-opus-5", max_tokens=4096,
    container={"skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"},
                          {"type": "custom", "skill_id": skill.id, "version": "latest"}]},
    messages=[{"role": "user", "content": "Create a presentation about renewable energy"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```
Beta headers at launch (Oct 2025): `skills-2025-10-02`, `code-execution-2025-08-25`, `files-api-2025-04-14` **(from memory; current docs no longer require them)**. Endpoints: `/v1/skills`, `/v1/skills/{id}/versions`. Generated files come back as `file_id`s (`bash_code_execution_tool_result` → `bash_code_execution_result.content[].file_id`) and are downloaded with the Files API. Multi-turn: reuse `container.id`; handle `stop_reason == "pause_turn"`.

**skill-creator** (https://github.com/anthropics/skills/tree/main/skills/skill-creator): loop "intent capture → draft → test → evaluate → improve → repeat"; anatomy `SKILL.md` + `scripts/`, `references/` (<300 lines ideal, TOC if longer), `assets/`; three-level loading (metadata ~100 words, body <500 lines, resources unlimited); evals in `evals/evals.json`, per-eval `eval_metadata.json`, `timing.json`, `grading.json`; `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`; `python <skill-creator>/eval-viewer/generate_review.py <workspace>/iteration-N --skill-name my-skill --benchmark …/benchmark.json [--previous-workspace …] [--static out.html]`; description optimizer `python -m scripts.run_loop --eval-set trigger-eval.json --skill-path <skill> --model <id> --max-iterations 5 --verbose` (20 trigger queries, 60/40 train/test); packaging `python -m scripts.package_skill <path/to/skill-folder>` → `.skill` file. Template: `template/SKILL.md` (`name: template-skill`, placeholder description, "Insert instructions below").

Repo layout (https://github.com/anthropics/skills): `skills/` (creative, dev/technical incl. `mcp-builder`, `webapp-testing`; enterprise/comms; document skills `docx`, `pdf`, `pptx`, `xlsx` source-available), `spec/` (now points to https://agentskills.io/specification), `template/`.

### Links
- Product post: https://claude.com/blog/skills ; Skills explained: https://claude.com/blog/skills-explained ; Building agents with skills: https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work ; Improving skill-creator: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- Docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview ; best practices https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices ; quickstart https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart ; API guide https://platform.claude.com/docs/en/build-with-claude/skills-guide ; enterprise https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise ; Claude Code skills https://code.claude.com/docs/en/skills ; Agent SDK https://code.claude.com/docs/en/agent-sdk
- Repos: https://github.com/anthropics/skills ; spec https://agentskills.io/specification (source https://github.com/agentskills/agentskills) ; validator `skills-ref` https://github.com/agentskills/agentskills/tree/main/skills-ref
- Cookbook: https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction (GitHub: https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- Help center: https://support.claude.com/en/articles/12512176-what-are-skills , …/12512180-using-skills-in-claude , …/12512198-creating-custom-skills , …/12580051-teach-claude-your-way-of-working-using-skills
- Guide PDF: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Course: https://anthropic.skilljar.com/introduction-to-agent-skills ; DeepLearning.AI course https://www.deeplearning.ai/courses/agent-skills-with-anthropic

### Implementation checklist
1. Pick one repetitive, high-value workflow you keep re-explaining to Claude.
2. Create `<skill-name>/SKILL.md` with `name` (lowercase-hyphen, = dir name) and a third-person `description` that states what + when, with trigger keywords (slightly "pushy").
3. Write a concise body (<500 lines): quick start, step-by-step workflow/checklist, output template, 2–3 input/output examples; assume Claude knows generalities.
4. Move deep material to `references/*.md` (one level deep, TOC if >100 lines) and deterministic steps to `scripts/*.py` with explicit error handling and documented constants; say "Run X" vs "See X".
5. Declare `compatibility`/dependencies; use fully-qualified MCP tool names; no Windows paths; no time-sensitive info.
6. Install: Claude Code `.claude/skills/` or `~/.claude/skills/` (or plugin); claude.ai upload zip; API `client.skills.create(files=files_from_dir(...))` + `container.skills` + `code_execution` tool.
7. Build ≥3 evals (`evals/evals.json`), run with/without skill via skill-creator, review in eval viewer, iterate; optimize description triggering.
8. Test on Haiku/Sonnet/Opus and in fresh sessions; gather team feedback.
9. Audit any third-party skill before installing; scope permissions (`allowed-tools`, `disable-model-invocation` for side-effecting skills).
10. Version and share (Skills API versions, plugins, git).

### Dependencies on other Anthropic engineering articles
- Applies "Effective context engineering" (just-in-time loading / progressive disclosure). Complements "Writing tools for agents" and MCP posts (skills teach tool usage). Referenced later by "Code execution with MCP" (skills directory + SKILL.md for saved code) and "Effective harnesses for long-running agents." Agent SDK post ("Building agents with the Claude Agent SDK") describes the same filesystem/bash foundation.

---

## 3. Making Claude Code more secure and autonomous with sandboxing

- **Title:** Making Claude Code more secure and autonomous with sandboxing (product-blog mirror title: "Beyond permission prompts: making Claude Code more secure and autonomous")
- **URL:** https://www.anthropic.com/engineering/claude-code-sandboxing (mirror: https://claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous)
- **Date:** October 20, 2025 (verified; same day as Claude Code on the web launch)
- **Authors:** not shown in any reachable snippet. **(from memory, unverified)**: written by Claude Code security engineer David Dworken with the Claude Code team.

### Thesis
Claude Code's per-command permission prompts protect users but cause "approval fatigue" (users approve the vast majority of prompts — ~93% **(from memory/third-party, unverified)**) without actually stopping a prompt-injected agent. Instead of asking permission for every action, Anthropic defines OS-enforced boundaries — *filesystem isolation* (only the working directory and explicitly allowed paths are writable) and *network isolation* (all egress goes through a proxy outside the sandbox that enforces a domain allowlist) — built on Linux bubblewrap and macOS Seatbelt. Inside those boundaries Claude runs freely. Two features ship on this foundation: the sandboxed Bash tool in Claude Code (`/sandbox`) and Claude Code on the web (sandboxed cloud VMs with a credential-holding git proxy). In internal use this "safely reduces permission prompts by 84%." The runtime is open-sourced as `@anthropic-ai/sandbox-runtime` (srt).

### Concepts, principles, recommendations (exhaustive)
- **Threat model:** prompt injection — a "prompt-injected Claude" could modify sensitive system files, leak data, or download malware. Permission prompts are a poor control because they interrupt constantly and users rubber-stamp them.
- **Two isolation boundaries (both required):**
  - *Filesystem isolation*: "ensures that Claude can only access or modify specific directories" — "particularly important in preventing a prompt-injected Claude from modifying sensitive system files." Default: read+write to the current working directory (and subdirs); reads elsewhere allowed; writes outside blocked (e.g. `~/.bashrc`, `/bin`).
  - *Network isolation*: "ensures that Claude can only connect to approved servers," preventing "leaking sensitive information or downloading malware." Implemented by "only allowing internet access through a unix domain socket connected to a proxy server running outside the sandbox"; the proxy enforces the domain allowlist (and can prompt the user for new domains).
  - Why both: "Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation, a compromised agent could backdoor system resources to gain network access."
- **OS primitives:** Linux → bubblewrap (namespaces, bind mounts marking dirs read/write, network namespace removed; socat bridges the Unix socket to the proxy; optional seccomp filter blocks Unix-socket creation). macOS → Seatbelt (`sandbox-exec` with dynamically generated profiles; proxy reachable on localhost ports). Windows: not supported at launch (srt later added an alpha using a dedicated `srt-sandbox` user + WFP rules + NTFS ACLs).
- **Result:** "In internal usage, sandboxing safely reduces permission prompts by 84%." "By defining set boundaries within which Claude can work freely, we increase security and agency."
- **Sandboxed Bash tool:** run `/sandbox` in Claude Code; commands that can run sandboxed are auto-approved; commands that need something outside the boundary (e.g. non-allowed host) fall back to the normal permission flow ("Bash command (unsandboxed)"); Claude can request `dangerouslyDisableSandbox` retry unless disabled.
- **Claude Code on the web:** each session runs in an isolated Anthropic-managed VM; network limited to an allowlist (configurable per cloud environment; can be fully disabled); git credentials never enter the sandbox — a proxy authenticates with scoped credentials on the session's behalf ("custom-built scoped credentials that the proxy verifies before attaching the appropriate authentication token"); API keys likewise injected outside the sandbox.
- **Open source:** the same primitives published as `anthropic-experimental/sandbox-runtime` (npm `@anthropic-ai/sandbox-runtime`, CLI `srt`, Apache-2.0) — "to help the broader ecosystem build more secure agentic systems"; usable for agents, local MCP servers, bash commands, arbitrary processes.
- **Limitations acknowledged:** sandboxing "reduces risk but is not a complete isolation boundary"; allowing broad domains (e.g. `github.com`) creates exfiltration paths (domain fronting; proxy decides on client hostname without TLS inspection); Unix-socket allowlisting (e.g. `/var/run/docker.sock`) can escalate; over-broad `allowWrite` (dirs on `$PATH`, shell rc files) enables escalation; Linux `enableWeakerNestedSandbox` weakens isolation inside unprivileged containers; sandbox covers only Bash subprocesses — Read/Edit/WebFetch, MCP servers and hooks run in-process/on host (use srt or containers to cover them); env vars are inherited unless scrubbed.

### Concrete configuration (verified from code.claude.com/docs/en/sandboxing + settings-reference)

**Enable / commands**
```
/sandbox                       # panel: Mode (auto-allow vs regular permissions), Overrides (allowUnsandboxedCommands), Config, Dependencies
claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'
sudo apt-get install bubblewrap socat     # Linux/WSL2 (Fedora: sudo dnf install bubblewrap socat)
npm install -g @anthropic-ai/sandbox-runtime   # optional seccomp filter for Unix-socket blocking
npx @anthropic-ai/sandbox-runtime claude       # wrap the whole Claude Code process (covers MCP servers + hooks)
srt "curl example.com" ; srt --debug … ; srt --settings /path/config.json npm install
```
Ubuntu 24.04+ AppArmor profile for bwrap userns (from docs):
```
sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOT'
abi <abi/4.0>,
include <tunables/global>
profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
  include if exists <local/bwrap>
}
EOT
sudo systemctl reload apparmor
```

**Claude Code `settings.json` sandbox schema** (all keys from settings-reference):
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "failIfUnavailable": false,
    "allowUnsandboxedCommands": true,
    "excludedCommands": ["docker *"],
    "enableWeakerNestedSandbox": false,
    "enableWeakerNetworkIsolation": false,
    "allowAppleEvents": false,
    "bwrapPath": "/usr/bin/bwrap",
    "socatPath": "/usr/bin/socat",
    "ripgrep": "/usr/bin/rg",
    "ignoreViolations": [],
    "filesystem": {
      "disabled": false,
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyWrite": [".env"],
      "denyRead": ["~/.aws/credentials", "~/.ssh"],
      "allowRead": ["."],
      "allowManagedReadPathsOnly": false
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "deniedDomains": ["uploads.github.com"],
      "strictAllowlist": false,
      "allowManagedDomainsOnly": false,
      "allowLocalBinding": true,
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowAllUnixSockets": false,
      "allowMachLookup": [],
      "httpProxyPort": 8080,
      "socksProxyPort": 8081,
      "tlsTerminate": {}
    },
    "credentials": {
      "files": [{"path": "~/.aws/credentials", "mode": "deny"},
                {"path": "~/.config/gh/hosts.yml", "mode": "mask", "extract": "oauth_token:\\s*(\\S+)", "injectHosts": ["api.github.com"]}],
      "envVars": [{"name": "GITHUB_TOKEN", "mode": "deny"},
                  {"name": "GH_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"]}],
      "awsPairs": [{"accessKeyIdVar": "MY_KEY_ID", "secretAccessKeyVar": "MY_SECRET_KEY", "sessionTokenVar": "MY_SESSION_TOKEN"}],
      "sigv4": {"streaming": "passthrough"},
      "allowPlaintextInject": false
    }
  }
}
```
Semantics: default writes = cwd + session `$TMPDIR` + `--add-dir`/`permissions.additionalDirectories`; default reads = whole machine minus denied paths (credential files readable unless denied!). Path prefixes: `/abs`, `~/`, `./` or bare = project-relative (project settings) or `~/.claude`-relative (user settings). Narrower rule wins for overlapping read rules. Protected paths always denied for writes: `.claude` settings/skills/agents/commands/hooks dirs, `.mcp.json`, `.git/hooks`, `.git/config`, shell rc files, `~/.claude`, `~/.claude.json`, `.credentials.json`. `Edit`/`Read` permission rules and `WebFetch(domain:...)` rules merge into the same lists. Managed enforcement example: `{"sandbox": {"enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false}}`; lock lists with `allowManagedReadPathsOnly` / `allowManagedDomainsOnly`. Ask rule `Bash(dangerouslyDisableSandbox:true)` forces a prompt on every unsandboxed retry. Env: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips credentials from all subprocesses. Claude Code adds `WebFetch(domain:…)` allow rules when you pick "Yes, and don't ask again" at a network prompt. Troubleshooting: `jest --no-watchman`; Go CLIs (`gh`, `gcloud`, `terraform`) may fail TLS on macOS → `excludedCommands` or `enableWeakerNetworkIsolation`; `docker` incompatible → exclude; Apple Events blocked (`allowAppleEvents`); unprivileged containers → `enableWeakerNestedSandbox`.

**srt (`~/.srt-settings.json`) schema** (verified README):
```json
{
  "network": {"allowedDomains": ["github.com", "*.npmjs.org"], "deniedDomains": ["malicious.com"]},
  "filesystem": {"denyRead": ["~/.ssh"], "allowRead": [], "allowWrite": [".", "/tmp"], "denyWrite": [".env"]}
}
```
Model: network allow-only (all denied by default; HTTP/HTTPS via HTTP proxy, other TCP via SOCKS5; Linux Unix-socket + socat bridge, macOS localhost ports in Seatbelt profile, Windows loopback port range). Reads deny-then-allow (`denyRead` then `allowRead` re-opens); writes allow-only (`allowWrite`, `denyWrite` wins). macOS supports globs (`*.ts`, `**/*.json`); Linux literal paths. Extra keys mentioned by docs/README: `enableWeakerNetworkIsolation`, `allowGitConfig`, `mandatoryDenySearchDepth`; built-in denies of `.git/hooks`, `.git/config`, `.mcp.json`, `.claude/commands`, `.claude/agents`, shell startup files. Library API:
```typescript
import { SandboxManager } from '@anthropic-ai/sandbox-runtime'
await SandboxManager.initialize({ network: { allowedDomains: ['example.com'] }, filesystem: { allowWrite: ['.'] } })
const wrapped = await SandboxManager.wrapWithSandbox('curl https://example.com')
```
Dependencies: Linux bubblewrap, socat, ripgrep (gcc/libseccomp-dev for custom seccomp); macOS ripgrep only; Windows bundled `srt-win.exe` + one-time elevated `windows-install`. For wrapping Claude Code: allow writes to project dir, `~/.claude`, `~/.claude.json`, `/tmp`; allow domains `api.anthropic.com`, `claude.ai`, `platform.claude.com`; `mkdir -p ~/.claude && echo '{}' > ~/.claude.json` first on Linux.

**Isolation ladder** (sandbox-environments doc): sandboxed Bash tool (Bash/PowerShell/Monitor + children) → sandbox runtime (whole process incl. file tools, MCP, hooks) → dev container (`.devcontainer/`, default-deny iptables firewall; safe for `--dangerously-skip-permissions`) → custom container → VM (Firecracker, Docker Sandboxes https://docs.docker.com/ai/sandboxes/) → cloud sessions (Anthropic-managed VM, proxy allowlist, git proxy with scoped credentials). `--dangerously-skip-permissions` refuses to run as root; always run it inside a container/VM/srt.

### Links
- Article: https://www.anthropic.com/engineering/claude-code-sandboxing ; mirror https://claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous
- Open-source runtime: https://github.com/anthropic-experimental/sandbox-runtime ; npm https://www.npmjs.com/package/@anthropic-ai/sandbox-runtime
- Docs: https://code.claude.com/docs/en/sandboxing ; https://code.claude.com/docs/en/sandbox-environments ; https://code.claude.com/docs/en/settings-reference#sandbox-settings ; https://code.claude.com/docs/en/devcontainer ; https://code.claude.com/docs/en/security ; https://code.claude.com/docs/en/claude-code-on-the-web ; https://code.claude.com/docs/en/cloud-environments ; https://code.claude.com/docs/en/agent-sdk/secure-deployment ; https://code.claude.com/docs/en/permission-modes
- Example settings: https://github.com/anthropics/claude-code/tree/main/examples/settings
- bubblewrap https://github.com/containers/bubblewrap ; socat http://www.dest-unreach.org/socat/ ; Apple Seatbelt (`sandbox-exec`)
- Related Anthropic posts: "How we contain Claude across products" https://www.anthropic.com/engineering/how-we-contain-claude ; auto mode https://www.anthropic.com/engineering/claude-code-auto-mode ; Claude Code on the web launch (Simon Willison summary https://simonw.substack.com/p/claude-code-for-web-a-new-asynchronous ; InfoQ https://www.infoq.com/news/2025/11/anthropic-claude-code-sandbox)

### Implementation checklist
1. Install deps (Linux/WSL2: `bubblewrap`, `socat`; optional seccomp via `npm i -g @anthropic-ai/sandbox-runtime`; macOS: nothing). Fix Ubuntu 24.04 AppArmor if needed.
2. Run `/sandbox`, choose auto-allow mode; confirm Dependencies tab is clean.
3. Set `sandbox.enabled: true` in `~/.claude/settings.json`; add `filesystem.allowWrite` for tool caches (`~/.kube`, build dirs) instead of `excludedCommands`.
4. Lock down secrets: `credentials.files` deny for `~/.aws`, `~/.ssh`; `credentials.envVars` deny or `mask` (+`network.tlsTerminate`, `injectHosts`); or `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`.
5. Pre-allow only needed domains (`network.allowedDomains`), avoid broad hosts; consider `strictAllowlist`; add `deniedDomains` for upload endpoints.
6. For unattended runs, disable the escape hatch (`allowUnsandboxedCommands: false`), set `failIfUnavailable: true`, and put the whole process in srt / dev container / VM (never `--dangerously-skip-permissions` on a bare host).
7. Org rollout: deliver `sandbox` keys via managed settings; set `allowManagedReadPathsOnly` / `allowManagedDomainsOnly`; keep `excludedCommands` narrow.
8. Optionally route through a TLS-inspecting corporate proxy (`httpProxyPort`/`socksProxyPort`) for content filtering.
9. Review writable paths and anything created after unattended sessions; audit `Bash command (unsandboxed)` approvals.

### Dependencies on other Anthropic engineering articles
- Extends Claude Code security/permissions model (Claude Code best practices post). Later posts build on it: "How we contain Claude across products," Claude Code auto mode, Agent SDK secure deployment. The "Code execution with MCP" and Skills posts assume a sandboxed execution environment like this one.

---

## 4. Code execution with MCP: Building more efficient agents

- **Title:** Code execution with MCP: Building more efficient agents
- **URL:** https://www.anthropic.com/engineering/code-execution-with-mcp
- **Date:** November 4, 2025 (verified)
- **Authors:** Adam Jones and Conor Kelly (verified). Acknowledgements (from search snippet): Jeremy Fox, Jerome Swannack, Stuart Ritchie, Molly Vorwerck, Matt Samuels, Maggie Vo.

### Thesis
MCP (open-sourced Nov 2024; thousands of servers, SDKs in every major language, industry standard) lets agents connect to many tools, but the default pattern — load every tool definition into context and pass every intermediate result back through the model — becomes slow and expensive at scale. Two costs dominate: tool definitions bloat the context window (hundreds of thousands of tokens before a task starts) and intermediate results (e.g. a 50,000-token transcript) get copied through the model twice. The fix: present MCP servers as *code APIs* in a filesystem (one TypeScript file per tool, one directory per server), give the agent a code execution sandbox, and let it *write programs* that import and compose tools. The agent discovers tools progressively by exploring the filesystem, filters/aggregates data in the sandbox, uses real control flow, keeps sensitive data out of the model, persists state to files, and saves working code as reusable skills (`./skills/` + `SKILL.md`). In Anthropic's example, this cut token usage from 150,000 to 2,000 — a 98.7% reduction — at the cost of needing secure sandboxing, resource limits and monitoring.

### Concepts and claims (exhaustive)
- **MCP context:** "an open standard for connecting AI agents to external systems"; thousands of MCP servers; SDKs in all major languages; "the industry standard for connecting agents to tools and data."
- **How agents use MCP today:** tool definitions loaded directly into context; each tool call flows through the model.
- **Problem 1 — tool definitions overload the context window.** Example definitions the post shows (reconstructed):
  ```
  gdrive.getDocument
    Description: Retrieves a document from Google Drive
    Parameters: documentId (required, string) — The ID of the document to retrieve; fields (optional, string) — Specific fields to return
    Returns: Document object with title, content, metadata, permissions, etc.
  salesforce.updateRecord
    Description: Updates a record in Salesforce
    Parameters: objectType (required, string) — Type of Salesforce object (Lead, Contact, Account); recordId (required, string); data (required, object) — Fields to update
    Returns: Updated record object with confirmation
  ```
  With thousands of tools, "agents may process hundreds of thousands of tokens before reading a request."
- **Problem 2 — intermediate tool results consume additional tokens.** Example: "get the meeting transcript from Google Drive and attach it to the Salesforce lead record":
  ```
  TOOL CALL: gdrive.getDocument(documentId: "abc123")
  → returns "Discussed Q4 goals... [full transcript text]"
  TOOL CALL: salesforce.updateRecord(objectType: "SalesMeeting", recordId: "00Q5f000001abcXYZ", data: { "Notes": "Discussed Q4 goals... [full transcript text]" })
  ```
  The transcript is copied into context twice; "for a 2-hour meeting" that may be 50,000 tokens; large docs can exceed the window entirely. Models can also make errors copying large data.
- **Solution — code execution with MCP:** "presents MCP servers as code APIs rather than direct tool calls," giving agents a code execution environment so they "write actual programs that interact with tools." "LLMs are proficient at writing code" — exploit that.
- **Filesystem-as-tool-tree pattern** (reconstructed from snippets):
  ```
  servers
  ├── google-drive
  │   ├── getDocument.ts
  │   ├── ... (other tools)
  │   └── index.ts
  ├── salesforce
  │   ├── updateRecord.ts
  │   ├── ... (other tools)
  │   └── index.ts
  └── ... (other servers)
  ```
  Each tool file (reconstructed; snippet-verified core lines):
  ```typescript
  // ./servers/google-drive/getDocument.ts
  import { callMCPTool } from "../../../client.js";

  interface GetDocumentInput { documentId: string; }
  interface GetDocumentResponse { content: string; }

  /* Read a document from Google Drive */
  export async function getDocument(input: GetDocumentInput): Promise<GetDocumentResponse> {
    return callMCPTool<GetDocumentResponse>('google_drive__get_document', input);
  }
  ```
  Agent-written program (snippet-verified):
  ```typescript
  // Read transcript from Google Docs and add to Salesforce prospect
  import * as gdrive from './servers/google-drive';
  import * as salesforce from './servers/salesforce';

  const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
  await salesforce.updateRecord({
    objectType: 'SalesMeeting',
    recordId: '00Q5f000001abcXYZ',
    data: { Notes: transcript }
  });
  ```
  The agent discovers tools "by exploring the filesystem: listing the `./servers/` directory to find available servers, then reading the specific tool files it needs." Reads `google-drive/index.ts` when it needs Drive; reads Salesforce module only if needed; "everything else stays unloaded." Result: "token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%."
- **Benefit 1 — Progressive disclosure:** "Models are great at navigating filesystems." Alternative: a `search_tools` tool "to find relevant definitions" with a `detail` parameter selecting "name only, name and description, or the full definition with schemas" to conserve context. Analogous to tool search (cf. article 5).
- **Benefit 2 — Context-efficient tool results:** filter in code. Example (snippet-verified):
  ```typescript
  const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
  const pendingOrders = allRows.filter(row => row["Status"] === 'pending');
  console.log(`Found ${pendingOrders.length} pending orders`);
  console.log(pendingOrders.slice(0, 5)); // Only log first 5 for review
  ```
  "Fetch 10,000 spreadsheet rows… return only 5 pending orders… the 9,995 irrelevant rows never touch the context window." Also aggregation, summarization, transformation in code.
- **Benefit 3 — More powerful control flow:** loops, conditionals, error handling run in code "rather than chaining individual tool calls." Example polling (snippet-verified):
  ```typescript
  let found = false;
  while (!found) {
    const messages = await slack.getChannelHistory({ channel: 'C123456' });
    found = messages.some(m => m.text.includes('deployment complete'));
    if (!found) await new Promise(r => setTimeout(r, 5000));
  }
  console.log('Deployment notification received');
  ```
  Runs "entirely in the execution environment instead of alternating between MCP calls and sleep commands through your agent loop"; reduces "time to first token" and latency.
- **Benefit 4 — Privacy-preserving operations:** "Intermediate results stay in the execution environment by default"; "the agent only sees what you explicitly log or return." Data can flow gdrive→Salesforce "without ever entering the model's context." Going further, the MCP client can *tokenize PII*: the harness intercepts tool results and replaces emails/phones/names with placeholders; the model sees `[EMAIL_1]`, `[PHONE_1]`, `[NAME_1]`; the client de-tokenizes when the data is passed to the next tool "so the real data flows Google Sheets → Salesforce without going through the model." Example (reconstructed):
  ```typescript
  const sheet = await gdrive.getSheet({ sheetId: 'abc123' });
  for (const row of sheet.rows) {
    await salesforce.updateRecord({
      objectType: 'Lead',
      recordId: row.salesforceId,
      data: { Email: row.email, Phone: row.phone, Name: row.name }
    });
  }
  console.log(`Updated ${sheet.rows.length} leads`);
  ```
  Enables "deterministic security rules — like restricting where data can flow."
- **Benefit 5 — State persistence and skills:** filesystem lets agents "maintain state across operations" — write intermediate results to `./workspace/`, resume later (reconstructed):
  ```typescript
  const leads = await salesforce.query({ query: "SELECT Id, Name, Email FROM Lead LIMIT 1000" });
  const csvData = leads.map(l => `${l.Id},${l.Name},${l.Email}`).join('\n');
  await fs.writeFile('./workspace/leads.csv', csvData);
  // Later: const saved = await fs.readFile('./workspace/leads.csv', 'utf-8');
  ```
  Save working code as reusable functions (snippet-verified shape):
  ```typescript
  // In ./skills/save-sheet-as-csv.ts
  import * as gdrive from './servers/google-drive';
  export async function saveSheetAsCsv(sheetId: string) {
    const data = await gdrive.getSheet({ sheetId });
    const csv = data.map(row => row.join(',')).join('\n');
    await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
    return `./workspace/sheet-${sheetId}.csv`;
  }
  // Later, in any agent execution
  import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
  const csvPath = await saveSheetAsCsv('abc123');
  ```
  "Adding a SKILL.md file to these saved functions creates a structured skill that models can reference and use" → "over time, this allows your agent to build a toolbox of higher-level capabilities, evolving the scaffolding that it needs to work most effectively." (Links to the Agent Skills post.)
- **Trade-offs / costs:** "Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add operational overhead and security considerations that direct tool calls avoid. The benefits… should be weighed against these implementation costs."
- **Conclusion:** "Code execution with MCP enables agents to use context more efficiently by loading tools on demand, filtering data before it reaches the model, and executing complex logic in a single step." Same pattern as Cloudflare's "Code Mode" ("LLMs are better at writing code to call MCP, than at calling MCP directly"). Anthropic asks builders to share implementations; encourages the MCP community; guidance is transport-agnostic.

### Concrete mechanics / how to implement (harness side)
- MCP client generates one module per server from `tools/list`, with typed wrappers calling `callMCPTool(name, input)`; naming convention `server__tool` (e.g. `google_drive__get_document`).
- Provide a `search_tools(query, detail)` helper optionally.
- Give the model one tool: run TypeScript/JS (or Python) in a sandbox with `./servers/`, `./workspace/`, `./skills/` mounted; capture stdout as the tool result.
- Tokenize PII at the client boundary; de-tokenize on egress to other tools; enforce data-flow rules deterministically.
- Persist `./workspace/` and `./skills/` across runs; add `SKILL.md` frontmatter to saved helpers so they become Agent Skills.
- Anthropic-hosted equivalent: Programmatic Tool Calling on the Developer Platform (`code_execution` tool + `allowed_callers`) — see article 5; Claude Code equivalent: MCP tool search (`ToolSearch`, default in v2.1+, `ENABLE_TOOL_SEARCH=false` to disable).

### Links
- Article: https://www.anthropic.com/engineering/code-execution-with-mcp
- MCP: https://modelcontextprotocol.io ; MCP intro post https://www.anthropic.com/news/model-context-protocol ; MCP registry https://github.com/modelcontextprotocol/registry **(link presence in article unverified)**
- Agent Skills post: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Cloudflare Code Mode: https://blog.cloudflare.com/code-mode/
- Third-party coverage: https://simonwillison.net/2025/Nov/4/code-execution-with-mcp/ ; https://www.mbgsec.com/archive/2025-11-08-code-execution-with-mcp-building-more-efficient-ai-agents-anthropic/ (archived copy) ; https://www.marktechpost.com/2025/11/08/anthropic-turns-mcp-agents-into-code-first-systems-with-code-execution-with-mcp-approach/ ; https://danielmiessler.com/blog/anthropic-downplays-mcps ; https://obot.ai/resources/learning-center/mcp-anthropic/
- Community implementations: https://github.com/elusznik/mcp-server-code-execution-mode ; https://github.com/ArtemisAI/code-execution-with-MCP ; https://github.com/agentic-dev-io/mcp-code-execution ; https://github.com/bug-ops/mcp-execution ; MCP discussion https://github.com/orgs/modelcontextprotocol/discussions/639 ; Apple CodeAct https://machinelearning.apple.com/research/codeact
- Related docs: programmatic tool calling https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling ; code execution tool https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool ; MCP connector https://platform.claude.com/docs/en/agents-and-tools/mcp-connector ; Claude Code MCP https://code.claude.com/docs/en/mcp

### Implementation checklist
1. Stand up a sandboxed code runtime (container/VM/srt) with CPU/memory/time limits, no ambient credentials, logging of executed code.
2. Write an MCP client that connects to servers, calls `tools/list`, and generates `./servers/<server>/<tool>.ts` wrappers + `index.ts` with typed inputs/outputs and a `callMCPTool` bridge (RPC from sandbox to host).
3. Expose to the model a single "execute code" tool plus a short system prompt explaining the directory layout (`./servers`, `./workspace`, `./skills`) and optionally `search_tools(query, detail)`.
4. Instruct the model to explore (`ls ./servers`, read only needed files), filter/aggregate in code, and `console.log` only what it needs.
5. Add PII tokenization/de-tokenization at the client boundary and deterministic data-flow policies.
6. Persist `./workspace/` and `./skills/`; encourage saving reusable helpers with `SKILL.md`.
7. Measure tokens/latency vs direct tool calling (target ~98% reduction on definition-heavy tasks); monitor for runaway loops; add timeouts.
8. If on the Claude API, consider the managed alternative: `code_execution_20260120` + `allowed_callers` (Programmatic Tool Calling) and Tool Search.

### Dependencies on other Anthropic engineering articles
- Depends on MCP (Nov 2024), Agent Skills post (Oct 2025) for the skills concept, context-engineering post (progressive disclosure/just-in-time). Realized in product as Programmatic Tool Calling + Tool Search ("Advanced tool use," Nov 24 2025) and Claude Code MCP tool search. Assumes sandboxing like article 3.

---

## 5. Introducing advanced tool use on the Claude Developer Platform

- **Title:** Introducing advanced tool use on the Claude Developer Platform
- **URL:** https://www.anthropic.com/engineering/advanced-tool-use
- **Date:** November 24, 2025 (verified; launched with Claude Opus 4.5)
- **Authors:** not shown in reachable snippets **(unverified)**.

### Thesis
As agents gain access to hundreds or thousands of tools (especially via MCP), two costs explode: tool definitions eat the context window and every tool call round-trips through the model with its full result. The post introduces three beta features on the Claude Developer Platform (beta header `advanced-tool-use-2025-11-20`): **Tool Search Tool** (defer tool definitions and let Claude discover them on demand — ~85% fewer tool-definition tokens, and accuracy gains e.g. Opus 4 49%→74%, Opus 4.5 79.5%→88.1% on an MCP eval), **Programmatic Tool Calling** (Claude writes Python that calls tools inside the code-execution sandbox so intermediate results never enter context — 37% fewer tokens on complex research tasks, 43,588→27,297, with accuracy up 25.6%→28.5% on internal knowledge retrieval and 46.5%→51.2% on GIA), and **Tool Use Examples** (`input_examples` on tool definitions to show usage conventions JSON Schema can't express — 72%→90% accuracy on complex parameter handling). Together: search to find tools, code to orchestrate them, examples to call them correctly.

### Concepts, numbers, guidance (exhaustive)

**Motivation**
- "A typical multiserver setup (GitHub, Slack, Sentry, Grafana, and Splunk)" — five servers, 58 tools — "consumes ~55K tokens" of definitions before the conversation starts; internally at Anthropic, tool definitions consumed 134K tokens before optimization.
- Tool confusion grows with library size — e.g. similarly named `notification-send-user` vs `notification-send-channel` **(example from memory, unverified)**; accuracy degrades beyond ~30–50 tools (docs).

**Tool Search Tool**
- Mechanism: include a tool search tool in `tools`; send every tool definition but mark most `defer_loading: true`; Claude initially sees only the search tool + non-deferred tools; when it needs a capability it searches; API returns `tool_reference` blocks (up to 5 by default; Claude can set `limit` 1–10,000) and expands them into full definitions inline (prefix untouched → prompt cache preserved); Claude then calls the discovered tool.
- Variants: `tool_search_tool_regex_20251119` (Claude writes Python `re.search()` patterns, case-insensitive, max 200 chars, e.g. `"get_.*_data"`, `"database.*query|query.*database"`) and `tool_search_tool_bm25_20251119` (natural-language query, max 500 chars). Custom client-side search (embeddings etc.) can return `tool_reference` blocks in a normal `tool_result`.
- Searches tool names, descriptions, argument names and argument descriptions.
- Results: "preserves 191,300 tokens of context compared to 122,800 with the traditional approach" → "85% reduction in token usage while maintaining access to your full tool library." MCP evaluation: "Opus 4 improved from 49% to 74%, and Opus 4.5 improved from 79.5% to 88.1% with Tool Search Tool enabled."
- When to use: >10 tools; definitions >10K tokens; accuracy dropping with tool count; aggregating MCP servers (200+ tools); growing tool library. Not needed for <10 small tools all used every request. Keep 3–5 most-used tools non-deferred; namespace names (`github_`, `slack_`); describe tool categories in the system prompt; monitor which tools get discovered.
- MCP integration: for MCP connector tools, set `defer_loading` on the `mcp_toolset` entry's `default_config` or per-tool `configs`. Claude Code applied the same idea to MCP servers (`ToolSearch`, default in v2.1+).
- Limits: ≤10,000 deferred tools per request; at least one non-deferred tool (never defer the search tool); `defer_loading` + `cache_control` on the same tool → 400. Errors: `invalid_tool_input`, `unavailable`, `too_many_requests`, `execution_time_exceeded`. Batch API supported. Streaming emits `server_tool_use` + `tool_search_tool_result` events. Models: Sonnet 4.5+, Opus 4.5+, Haiku 4.5 (not Opus 4.1 or earlier).

**Programmatic Tool Calling**
- Problem: each tool call is a round trip through the model; results land in context even when only a summary is needed. Example: budget compliance for 20 employees = 20 round trips, thousands of expense line items in context.
- Mechanism: tools you opt in with `allowed_callers: ["code_execution_20250825"]` (now `code_execution_20260120`/`20260521`) are exposed inside the code-execution container as async Python functions; Claude writes a script; when the script calls a tool, "code execution pauses and the API returns a `tool_use` block" with `caller: {"type": "code_execution_20260120", "tool_id": "srvtoolu_…"}`; you return the `tool_result` (must be the only content in that user message; text-only); execution resumes; "intermediate results are not loaded into Claude's context window"; only the final stdout/output enters context. Tools callable in parallel via `asyncio.gather`.
- Example (reconstructed from snippets): 
  ```python
  team = await get_team_members("engineering")
  levels = list(set(m["level"] for m in team))
  budgets = dict(zip(levels, await asyncio.gather(*[get_budget_by_level(l) for l in levels])))
  expenses = await asyncio.gather(*[get_expenses(m["id"], "Q3") for m in team])
  exceeded = []
  for member, exp in zip(team, expenses):
      total = sum(e["amount"] for e in exp)
      limit = budgets[member["level"]]["travel_limit"]
      if total > limit:
          exceeded.append({"name": member["name"], "spent": total, "limit": limit})
  print(json.dumps(exceeded))
  ```
  "Reducing consumption from 200KB of raw expense data to just 1KB of results" — returns "only the four employees who exceeded their limits."
- Results: "Claude for Excel uses Programmatic Tool Calling to read and modify spreadsheets with thousands of rows without overloading the model's context window." Internal knowledge-retrieval benchmark 25.6% → 28.5%; GIA benchmark 46.5% → 51.2%; average token usage on complex research tasks 43,588 → 27,297 (−37%). Later docs add: 75-tool project-management benchmark −38% billed input tokens with no accuracy change; τ²-bench (sequential single calls) unchanged accuracy, ~8% more cost; production traffic with 10–49 tools sees 20–40% savings; BrowseComp/DeepSearchQA +11% with −24% input tokens when added to search.
- When to use: fan-out/parallel operations over many items; large filterable results; agentic search/retrieval; multi-step chains with conditional logic. Weak fit: strictly sequential reasoning-dependent steps, few small calls (container overhead), tools needing immediate user feedback. Best practices: document output format (JSON) in descriptions; return structured, concise data; choose `["direct"]` OR `["code_execution_…"]` per tool, not both; reuse `container` ids; respond before `expires_at` (pending call times out ~4 min; idle container reclaimed ~5 min; 30-day max). Not a security boundary (validate tool outputs; `allowed_callers` is guidance). Incompatible with `strict: true` tools, `tool_choice` forcing, `disable_parallel_tool_use`, recursive `$ref` schemas, MCP-connector tools, computer/browser toolsets.

**Tool Use Examples**
- Problem: "JSON Schema excels at defining structure — types, required fields, allowed enums — but it can't express usage patterns: when to include optional parameters, which combinations make sense, or what conventions your API expects" (date formats, ID formats, nested objects, escalation conventions).
- Mechanism: optional `input_examples` array on a tool definition; each example must validate against `input_schema` (else 400); examples are rendered alongside the schema in the prompt. Cost ~20–50 tokens per simple example, ~100–200 for complex nested ones. Works with tool search (examples expand with the deferred definition). Not for server tools (web search, code execution) or client toolsets.
- Example (reconstructed from snippets):
  ```json
  {
    "name": "create_ticket",
    "description": "Create a support ticket",
    "input_schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "labels": {"type": "array", "items": {"type": "string"}},
        "reporter": {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"},
                     "contact": {"type": "object", "properties": {"email": {"type": "string"}, "phone": {"type": "string"}}}},
                     "required": ["id"]},
        "due_date": {"type": "string"},
        "escalation": {"type": "object", "properties": {"level": {"type": "integer", "minimum": 1, "maximum": 3},
                       "notify_manager": {"type": "boolean"}, "sla_hours": {"type": "integer"}}}
      },
      "required": ["title"]
    },
    "input_examples": [
      {"title": "Login page returns 500 error", "priority": "critical", "labels": ["bug", "authentication", "production"],
       "reporter": {"id": "USR-12345", "name": "Jane Smith", "contact": {"email": "jane@acme.com", "phone": "+1-555-0123"}},
       "due_date": "2024-11-06", "escalation": {"level": 2, "notify_manager": true, "sla_hours": 4}},
      {"title": "Add dark mode support", "labels": ["feature-request", "ui"], "reporter": {"id": "USR-67890", "name": "Alex Chen"}},
      {"title": "Update API documentation"}
    ]
  }
  ```
  Teaches: date format `YYYY-MM-DD`, ID prefix `USR-`, when to include nested `contact`/`escalation`, minimal vs full calls.
- Results: "Tool Use Examples improve parameter accuracy from 72% to 90% by demonstrating usage patterns beyond JSON schema constraints" (complex parameter handling).
- When to use: complex nested structures, many optional params, format-sensitive inputs, APIs with conventions/implicit rules. Skip for simple single-param tools; prioritize descriptions first.

**Putting it together / getting started**
- Enable with `anthropic-beta: advanced-tool-use-2025-11-20` (at launch; tool search + PTC + examples now GA without a header per current docs).
- Combine: Tool Search to find the right tool among thousands; PTC to orchestrate multi-step, data-heavy workflows; Examples to call tools with the right shape. Works with MCP servers (mcp_toolset deferred loading) and Claude Code.
- Design tools for the "just-in-time" era: descriptive names/keywords, namespacing, output-format documentation.

### Concrete API surface (verified from platform docs)
Tool Search request:
```json
{"model": "claude-opus-5", "max_tokens": 2048,
 "messages": [{"role": "user", "content": "What is the weather in San Francisco?"}],
 "tools": [
   {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
   {"name": "get_weather", "description": "Get the weather at a specific location",
    "input_schema": {"type": "object", "properties": {"location": {"type": "string"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}}, "required": ["location"]},
    "defer_loading": true},
   {"name": "search_files", "description": "Search through files in the workspace", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}, "defer_loading": true}
 ]}
```
Response blocks: `server_tool_use` (`name: tool_search_tool_regex`, `input: {"pattern": "weather", "limit": 10}` or `{"query": ...}` for BM25) → `tool_search_tool_result` (`content: {"type": "tool_search_tool_search_result", "tool_references": [{"type": "tool_reference", "tool_name": "get_weather"}]}`) → `tool_use`. Never send a `tool_result` for `srvtoolu_…` ids; resend the full `tools` array each turn. Custom search: return `{"type": "tool_result", "tool_use_id": "...", "content": [{"type": "tool_reference", "tool_name": "discovered_tool_name"}]}`. MCP: `{"type": "mcp_toolset", "mcp_server_name": "...", "default_config": {"defer_loading": true}, "configs": [{"tool_name": "...", "defer_loading": false}]}` (shape per docs' MCP toolset configuration).

PTC request:
```json
{"model": "claude-opus-5", "max_tokens": 4096,
 "messages": [{"role": "user", "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"}],
 "tools": [
   {"type": "code_execution_20260120", "name": "code_execution"},
   {"name": "query_database", "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
    "input_schema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL query to execute"}}, "required": ["sql"]},
    "allowed_callers": ["code_execution_20260120"]}
 ]}
```
Response: `server_tool_use` (`name: code_execution`, `input.code: "rows = json.loads(await query_database({'sql': ...}))..."`) + `tool_use` with `caller: {"type": "code_execution_20260120", "tool_id": "srvtoolu_abc123"}` + top-level `container: {"id": "container_xyz789", "expires_at": ...}`, `stop_reason: "tool_use"`. Continue with `container: "container_xyz789"` and a user message containing only `tool_result` blocks; final `code_execution_tool_result` → `{"type": "code_execution_result", "stdout": ..., "stderr": "", "return_code": 0, "content": []}`. `allowed_callers` values: `["direct"]` (default), `["code_execution_20260120"]`, or both. Code-execution tool versions: `code_execution_20250522` (Python only, legacy), `code_execution_20250825` (Bash + files), `code_execution_20260120` (adds REPL state persistence + PTC), `code_execution_20260521` (same runtime; describes the 90-second per-cell limit). No beta header required today; legacy headers `code-execution-2025-05-22`, `code-execution-2025-08-25` still accepted. Container: Linux, no internet, 30-day expiry, checkpoint after ~5 min idle. Pricing: same as code execution; PTC tool results don't count as input tokens.

Cookbook (verified): `programmatic_tool_calling_ptc.ipynb` uses `client.beta.messages.create(betas=["advanced-tool-use-2025-11-20"], ...)`, sets `tool["allowed_callers"] = ["code_execution_20250825"]`, tool `{"type": "code_execution_20250825", "name": "code_execution"}`, mock API `utils/team_expense_api.py` with `get_team_members`, `get_expenses`, `get_custom_budget` ($5,000 standard quarterly travel limit), passes `container_id` back, checks `caller.type`. `tool_search_with_embeddings.ipynb`: client-side `tool_search` tool, SentenceTransformer `all-MiniLM-L6-v2` (384-d) cosine similarity, returns `tool_reference` blocks, header `advanced-tool-use-2025-11-20`, "cutting context usage by 90%+", consider when >20 tools. `tool_search_alternate_approaches.ipynb`: `describe_tool` pattern; list tool names in system prompt; add discovered tools with `defer_loading: true` to preserve cache; tools needn't be in `tools` until discovered.

### Links
- Article: https://www.anthropic.com/engineering/advanced-tool-use
- Docs: tool search https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool ; programmatic tool calling https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling ; tool use examples (now in) https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples (old URL …/tool-use/tool-use-examples now 404) ; tool reference https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference ; code execution https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool ; MCP connector https://platform.claude.com/docs/en/agents-and-tools/mcp-connector ; prompt caching with tools https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching ; strict tool use https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
- Cookbooks: https://github.com/anthropics/claude-cookbooks/tree/main/tool_use — `tool_search_with_embeddings.ipynb` (https://platform.claude.com/cookbook/tool-use-tool-search-with-embeddings), `tool_search_alternate_approaches.ipynb`, `programmatic_tool_calling_ptc.ipynb` (https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc), plus `memory_cookbook.ipynb`, `automatic-context-compaction.ipynb`, `context_engineering/context_engineering_tools.ipynb`, `tool_choice.ipynb`, `parallel_tools.ipynb`, `tool_use_with_pydantic.ipynb`, `extracting_structured_json.ipynb`, `customer_service_agent.ipynb`, `vision_with_tools.ipynb`, `calculator_tool.ipynb`
- Claude Code MCP tool search: https://code.claude.com/docs/en/mcp (`ENABLE_TOOL_SEARCH=false` to disable; default in v2.1+)
- Related: Claude for Excel; "Improved web search with dynamic filtering" https://claude.com/blog/improved-web-search-with-dynamic-filtering ; benchmarks BrowseComp https://arxiv.org/abs/2504.12516 , τ²-bench https://arxiv.org/abs/2506.07982 , DeepSearchQA https://github.com/google-deepmind/deepsearchqa
- Third-party: https://growthmethod.com/anthropic-tool-search/ ; https://tessl.io/blog/anthropic-brings-mcp-tool-search-to-claude-code ; LiteLLM support https://docs.litellm.ai/docs/providers/anthropic_tool_search ; AWS Bedrock PTC post https://aws.amazon.com/blogs/machine-learning/implementing-programmatic-tool-calling-on-amazon-bedrock/

### Implementation checklist
1. Audit your tool library: count tools and definition tokens; if >10 tools or >10K tokens (or any MCP aggregation), adopt Tool Search.
2. Add `{"type": "tool_search_tool_regex_20251119" | "tool_search_tool_bm25_20251119", ...}`; set `defer_loading: true` on all but the 3–5 hottest tools; namespace names, enrich descriptions with user-facing keywords; add a system-prompt line listing tool categories; for MCP connector use `mcp_toolset.default_config.defer_loading`.
3. Handle `server_tool_use` / `tool_search_tool_result` blocks passively; resend the full `tools` array each turn; never `tool_result` the `srvtoolu_` id.
4. For data-heavy/fan-out workflows, add `{"type": "code_execution_20260120", "name": "code_execution"}` and `allowed_callers: ["code_execution_20260120"]` on safe, idempotent tools; document JSON output shapes in descriptions.
5. Implement the PTC loop: on `stop_reason: tool_use` with `caller.type == code_execution_…`, run the tool, reply with a user message of only `tool_result` (string) blocks, pass `container` id; respond well within ~4 min; log `caller` and container ids.
6. For complex/nested/format-sensitive tools, add 2–3 schema-valid `input_examples` (a full example, a partial one, a minimal one).
7. Keep `cache_control` on a non-deferred tool; avoid `strict` on PTC tools; don't force `tool_choice` for code-only tools.
8. Measure: input tokens, accuracy, latency with/without each feature on representative traffic; iterate on descriptions based on what Claude searches for.

### Dependencies on other Anthropic engineering articles
- Productizes the ideas of "Code execution with MCP" (Nov 4 2025) and the just-in-time principle from "Effective context engineering" (docs cite both). Builds on "Writing tools for agents" (descriptions, namespacing, consolidation) and MCP. Complements Agent Skills (skills + tool search + PTC in one agent) and Claude Code's MCP tool search.

---

## Cross-article synthesis
- **Shared principle:** context is finite; load information just-in-time (context engineering) → skills' progressive disclosure, filesystem-as-tool-tree, `defer_loading`/tool search, PTC keeping results out of context, context editing/compaction/memory.
- **Shared prerequisite:** a sandboxed execution environment (article 3 / code execution container) that can run scripts, read files, and call tools — the substrate for Skills, Code-execution-with-MCP and PTC.
- **Layering an agent (2025-11 Anthropic stack):** system prompt at the right altitude + minimal tool set + examples (1) → Skills folder for procedural knowledge (2) → sandboxed runtime with allowlists (3) → MCP servers exposed as code / deferred tools (4) → Tool Search + PTC + input_examples on the API (5) → compaction/memory for long horizons (1).
