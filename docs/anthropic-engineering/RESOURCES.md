# Anthropic Engineering: Resource Catalog

Companion to [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md). Every cookbook, quickstart, spec, SDK repo and documentation page that the engineering articles link to or that implements their concepts, plus the configuration reference for Claude Code. Compiled 2026-09-21 from platform.claude.com, code.claude.com, github.com and raw.githubusercontent.com. URLs were fetched and confirmed unless marked otherwise.

## Article text sources

Article text was verified against the live pages at https://www.anthropic.com/engineering on 2026-09-21: `verification/verify_live.py --source live` confirmed all 26 pages, their publication dates and the quoted figures and configuration strings in `verification/claims.tsv` (see `verification/report.md`), and an independent pass over 192 numeric claims and configuration tokens in the notes found 173 verbatim, 2 paraphrased, 14 sourced from linked docs and cookbooks (labeled inline), and 2 post-publication edits to one page (annotated in the notes). Two pages now redirect: the best-practices post to https://code.claude.com/docs/en/best-practices and the Agent SDK post to https://claude.com/blog/building-agents-with-the-claude-agent-sdk. Offline fallbacks for the verification script are listed in `verification/README.md`.

Additional official repos surfaced while researching the articles:

- https://github.com/anthropics/cwc-long-running-agents (Code with Claude workshop on long-running agents)
- https://github.com/anthropics/claudes-c-compiler (the C compiler built by the agent team, with README and DESIGN_DOC)
- https://github.com/anthropics/original_performance_takehome (the AI-resistant performance take-home)
- https://github.com/anthropics/claude-agent-sdk-demos
- https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md (frontend design skill used by the harness-design post)
- https://github.com/microsoft/playwright-mcp (browser QA in the harness posts)
- https://github.com/openai/simple-evals (BrowseComp eval code referenced in the eval-awareness post)


Companion catalog of official Anthropic cookbooks, quickstarts, specs, SDK repos, and documentation pages referenced by (or implementing concepts from) the Anthropic engineering blog. Compiled 2026-09-21.

Sourcing notes:
- `www.anthropic.com`, `anthropic.com`, `web.archive.org`, `agentskills.io` were network-blocked; everything below was pulled from `platform.claude.com`, `code.claude.com`, `github.com` (rendered tree pages), `raw.githubusercontent.com`, and GitHub code search.
- `github.com/anthropics/anthropic-cookbook` redirects to `github.com/anthropics/claude-cookbooks`; `github.com/anthropics/anthropic-quickstarts` redirects to `claude-quickstarts`. Older docs links (`docs.anthropic.com`, `docs.claude.com`) redirect to `platform.claude.com`.
- `github.com/anthropics/dxt` is now `github.com/anthropics/mcpb` (same README served from both).
- The Agent Skills spec file in `anthropics/skills/spec/agent-skills-spec.md` is now a one-line pointer to `https://agentskills.io/specification`; the spec source is `https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx` (quoted in section C).

---

## (a) Cookbooks & notebooks — `anthropics/claude-cookbooks`

Repo: https://github.com/anthropics/claude-cookbooks (redirect target of `anthropics/anthropic-cookbook`).
Notebook base URL pattern: `https://github.com/anthropics/claude-cookbooks/blob/main/<path>`; directory pattern: `https://github.com/anthropics/claude-cookbooks/tree/main/<dir>`.
Canonical index: `registry.yaml` at the repo root (96 entries; schema in `.github/registry_schema.json`; each entry has `title`, `description`, `path`, `authors`, `date`, `categories`). Descriptions below are taken from the registry.

Repo setup (from `CLAUDE.md`):
```bash
uv sync --all-extras
uv run pre-commit install
cp .env.example .env   # add ANTHROPIC_API_KEY
make format | make lint | make check | make fix | make test
```
Model aliases the repo standardizes on: `claude-sonnet-5`, `claude-haiku-4-5`, `claude-opus-4-8` (never dated IDs). Slash commands in `.claude/`: `/notebook-review`, `/model-check`, `/link-review`.

Top-level directories: `.claude/`, `.github/`, `anthropic_cookbook/` (only `__init__.py`), `capabilities/`, `claude_agent_sdk/`, `coding/`, `cost_optimization/`, `evals/agentic_search/`, `extended_thinking/`, `fable_5_fallback_billing/`, `finetuning/`, `images/`, `managed_agents/`, `misc/`, `multimodal/`, `observability/`, `patterns/agents/`, `scripts/`, `skills/`, `tests/`, `third_party/`, `tool_evaluation/`, `tool_use/`. Root files: `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `authors.yaml`, `registry.yaml`, `pyproject.toml`, `Makefile`, `lychee.toml`, `tox.ini`, `uv.lock`, `uv.toml`, `.env.example`, `.pre-commit-config.yaml`, `requirements-dev.txt`.

### patterns/agents — "Building Effective Agents" reference implementation
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents (README: reference implementation for the *Building Effective Agents* post by Erik Schluntz and Barry Zhang; covers Prompt Chaining, Routing, Multi-LLM Parallelization, Orchestrator-Subagents, Evaluator-Optimizer).
- https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/basic_workflows.ipynb — Basic workflows: three simple multi-LLM workflow patterns (chaining, routing, parallelization) trading cost or latency for improved performance.
- https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/evaluator_optimizer.ipynb — Evaluator-optimizer: one LLM generates, another evaluates in a feedback loop.
- https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/orchestrator_workers.ipynb — Orchestrator-workers: a central LLM dynamically delegates tasks to worker LLMs and synthesizes their results.
- https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/async_multi_agent_orchestration.ipynb — Async multi-agent orchestration: a fixed N-agent team with peer messaging through a shared hub, and dynamically spawned async subagents, reduced to bare messaging/lifecycle mechanics.
- https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/util.py — shared helper (`llm_call`, etc.).
- Prompts used by the multi-agent research system (companion to the "How we built our multi-agent research system" post):
  - https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/prompts/research_lead_agent.md
  - https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/prompts/research_subagent.md
  - https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/prompts/citations_agent.md

### tool_use
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/tool_use (subdirs: `context_engineering/`, `memory_demo/`, `tests/`, `utils/`; files: `memory_tool.py`, `requirements.txt`, `.env.example`).
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/calculator_tool.ipynb — Give Claude a calculator tool for arithmetic.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/customer_service_agent.ipynb — Customer service agent with client-side tools for customer lookup and order management.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/extracting_structured_json.ipynb — Extract structured JSON from inputs via tool use.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_choice.ipynb — Control tool selection with the `tool_choice` parameter (forced/auto).
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_use_with_pydantic.ipynb — Note-saving tool with Pydantic-validated, type-safe tool definitions.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/parallel_tools.ipynb — Parallel tool calls on Claude 3.7 Sonnet using a batch-tool meta-pattern.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/vision_with_tools.ipynb — Combine vision with tools to extract structured data from images (e.g., nutrition labels).
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/memory_cookbook.ipynb — Memory & context management with Claude Sonnet 4.6: persistent memory via the memory tool plus context editing. Helper: https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/memory_tool.py ; demo dir `tool_use/memory_demo/`.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/automatic-context-compaction.ipynb — Automatic context compaction for long-running agentic workflows.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/programmatic_tool_calling_ptc.ipynb — Programmatic tool calling (PTC): Claude writes code that calls tools inside the code-execution environment to cut latency and tokens.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb — Tool search with embeddings: scale to thousands of tools using semantic embeddings for dynamic tool discovery.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_alternate_approaches.ipynb — Alternate tool-search approaches (present in the tree; not in registry).
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/threat_intel_enrichment_agent.ipynb — Threat-intel enrichment agent that investigates IOCs across sources, maps to MITRE ATT&CK, and emits structured reports for SIEM/SOAR.
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/context_engineering/context_engineering_tools.ipynb — Context engineering: memory, compaction, and tool clearing compared for long-running agents (companion: `research_corpus.py`).

### tool_evaluation
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_evaluation/tool_evaluation.ipynb — Tool evaluation: run parallel agent evaluations on tools from task files (`evaluation.xml`). Companion to "Writing effective tools for agents — with agents".
- https://github.com/anthropics/claude-cookbooks/blob/main/tool_evaluation/evaluation.xml — evaluation task definitions.

### skills
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/skills (README "Claude Skills Cookbook"; shows the beta header `anthropic-beta: code-execution-2025-08-25,files-api-2025-04-14,skills-2025-10-02`; built-in skill IDs `xlsx`, `pptx`, `pdf`, `docx`; helpers `skill_utils.py`, `file_utils.py`; dirs `assets/`, `custom_skills/`, `notebooks/`, `sample_data/`).
- https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/01_skills_introduction.ipynb — Introduction to Claude Skills: create documents, analyze data, automate workflows with Excel/PowerPoint/PDF skills.
- https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/02_skills_financial_applications.ipynb — Skills for financial applications: dashboards and portfolio analytics.
- https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb — Building custom Skills: create, deploy, and manage custom skills.
- Custom skill examples: https://github.com/anthropics/claude-cookbooks/tree/main/skills/custom_skills — `analyzing-financial-statements/`, `applying-brand-guidelines/`, `creating-financial-models/`.

### extended_thinking
- https://github.com/anthropics/claude-cookbooks/blob/main/extended_thinking/extended_thinking.ipynb — Extended thinking: transparent step-by-step reasoning with budget management.
- https://github.com/anthropics/claude-cookbooks/blob/main/extended_thinking/extended_thinking_with_tool_use.ipynb — Extended thinking combined with tools for multi-step workflows.

### claude_agent_sdk
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk (README setup: install uv, node, Claude Code CLI; `git clone https://github.com/anthropics/claude-cookbooks.git && cd claude-cookbooks/claude_agent_sdk && uv sync`; `uv run python -m ipykernel install --user --name="cc-sdk-tutorial" --display-name "Python (cc-sdk-tutorial)"`; `.env` with `ANTHROPIC_API_KEY=` and optional `GITHUB_TOKEN=`). Subdirs: `chief_of_staff_agent/`, `hosting/` (`docker/`, `modal/`, `kubernetes/`), `observability_agent/`, `research_agent/`, `scheduled_repository_reviewer/`, `session_browser_demo/`, `site_reliability_agent/`, `utils/`, `vulnerability_detection_agent/`.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/00_The_one_liner_research_agent.ipynb — One-liner research agent: basic agent loop, WebSearch, multimodal.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/01_The_chief_of_staff_agent.ipynb — Chief of staff agent: memory, output styles, plan mode, custom slash commands, hooks, subagent orchestration.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/02_The_observability_agent.ipynb — Observability agent: GitHub/git MCP servers, monitoring, incident response.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/03_The_site_reliability_agent.ipynb — Site reliability agent: read-write MCP tools, Prometheus, safety hooks, incident lifecycle.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/04_migrating_from_openai_agents_sdk.ipynb — Migrating from OpenAI Agents SDK: primitive mapping (tools, guardrails, sessions, handoffs).
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/05_Building_a_session_browser.ipynb — Session browser: list, read, rename, tag, fork Agent SDK sessions on disk.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/06_The_vulnerability_detection_agent.ipynb — Vulnerability detection agent: threat-model a C target, hunt memory-safety bugs, triage into a report.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/07_Hosting_the_agent.ipynb — Hosting the agent: Docker, Modal, Kubernetes with the same container image/HTTP interface.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/08_Dynamic_workflows.ipynb — Dynamic workflows: fact-check a report with parallel verifier and skeptic subagents.
- https://github.com/anthropics/claude-cookbooks/blob/main/claude_agent_sdk/scheduled_repository_reviewer/scheduled_repository_reviewer.ipynb — Scheduled, read-only review agent with session resumption and schema-validated verdicts.

### managed_agents (Claude Managed Agents)
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/managed_agents (README; setup: `ANTHROPIC_API_KEY`, optional `GITHUB_TOKEN`, `MONGO_URI`; fixtures in `example_data/`; `utilities.py`; subdirs `cma-mcp/`, `example_data/{gate,iterate,orchestrate}`, `linear/`, `mongodb_on_cma/`, `roadtrip_planner/`, `self_hosted_sandboxes/{cf,cf-worker,daytona,docker,modal,vercel}`, `sentry/`, `slack/`).
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/data_analyst_agent.ipynb — Data analyst agent: CSV to narrative HTML report with interactive charts, sandboxed environment, file mounting.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/slack_data_bot.ipynb — Slack data analyst bot with multi-turn follow-ups on one session.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/sre_incident_responder.ipynb — SRE incident responder: reads logs/runbooks, root-causes, opens a fix PR, waits for approval.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_iterate_fix_failing_tests.ipynb — Entry-point tutorial: agent/environment/session creation, file mounts, streaming event loop.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_operate_in_production.ipynb — Production setup: vault-backed MCP credentials, `session.status_idled` webhook, `session.budget_reached`, `inference_geo`, resource CRUD.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_prompt_versioning_and_rollback.ipynb — Server-side prompt versioning and rollback (`agents.update`, version pinning on `sessions.create`).
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_orchestrate_issue_to_pr.ipynb — Issue-to-PR orchestration with CI failure recovery.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_explore_unfamiliar_codebase.ipynb — Unfamiliar codebase exploration.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_gate_human_in_the_loop.ipynb — Human-in-the-loop expense approval gates.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_with_mongodb_atlas.ipynb — Fraud review agent with MongoDB Atlas: vector, full-text, RRF, `$graphLookup` retrieval patterns.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_remember_user_preferences.ipynb — Memory store so agents remember user preferences across sessions.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_coordinate_specialist_team.ipynb — Multiagent coordinator with heterogeneous specialists, scoped toolsets, `thread_created`/`thread_message_received` events.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_watch_subagents_live.ipynb — Stream coordinator and subagents live with per-thread `event_deltas`, `initial_events`, per-agent effort.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_verify_with_outcome_grader.ipynb — Outcomes: grade-and-revise loop (`user.define_outcome`, `span.outcome_evaluation_*` events).
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_consult_an_advisor.ipynb — Advisor entry: a working model consults a stronger model mid-turn.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_cap_session_spend.ipynb — Budgets: enforced list-cost budget, `session.usage` events, `budget_reached`, `sessions.update`.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb — Big model plans, small models execute; per-thread `usage.list_cost` metering.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_use_skills_from_a_repo.ipynb — Mount a repo so its `.claude/skills` is discovered at session start.
- https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_pin_inference_geo.ipynb — Data residency: `model.inference_geo`, `allowed_inference_geos`, `agent_with_overrides`.
- Supporting READMEs: `managed_agents/slack/README.md`, `managed_agents/sentry/README.md`, `managed_agents/linear/README.md`, `managed_agents/cma-mcp/README.md`, `managed_agents/mongodb_on_cma/README.md`, `managed_agents/roadtrip_planner/README.md`, `managed_agents/self_hosted_sandboxes/README.md` (+ `cf/`, `cf-worker/`, `daytona/`, `docker/`, `modal/`, `vercel/` READMEs).

### observability
- https://github.com/anthropics/claude-cookbooks/blob/main/observability/usage_cost_api.ipynb — Usage & cost Admin API cookbook.

### evals
- https://github.com/anthropics/claude-cookbooks/blob/main/evals/agentic_search/reproduce_agentic_search_benchmarks.ipynb — Reproduce DeepSearchQA and BrowseComp scores with a Messages API harness using programmatic tool calling, server-side compaction, and task budgets (utils in `evals/agentic_search/utils/`).

### capabilities
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/capabilities (README; each guide has `guide.ipynb`, `README.md`, and an `evaluation/` dir with README).
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/classification/guide.ipynb — Classification with RAG and chain-of-thought (insurance tickets).
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/retrieval_augmented_generation/guide.ipynb — RAG with summary indexing and reranking, plus an evaluation suite.
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/contextual-embeddings/guide.ipynb — Contextual retrieval: add context to chunks before embedding, with prompt caching, BM25, and reranking (companion to the "Introducing Contextual Retrieval" post).
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/summarization/guide.ipynb — Summarization of legal documents with evaluation and advanced techniques.
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/text_to_sql/guide.ipynb — Text-to-SQL with RAG, chain-of-thought, self-improvement.
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/knowledge_graph/guide.ipynb — Knowledge graph construction: NER, relation extraction, entity resolution, multi-hop querying with structured outputs.
- https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/content_moderation/guide.ipynb — Content policy enforcement: compile policy prose into JSON rules, typed field extraction, deterministic rule engine with audit trail.

### misc
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb — Prompt caching through the Claude API.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/speculative_prompt_caching.ipynb — Speculative prompt caching to reduce TTFT by warming cache while users type.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/building_evals.ipynb — Building evals: robust evaluation systems (code-graded, model-graded).
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/generate_test_cases.ipynb — Generate synthetic test cases for a prompt template.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/batch_processing.ipynb — Message Batches API (50% cost reduction).
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/using_citations.ipynb — Citations for document-grounded answers.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/pdf_upload_summarization.ipynb — "Uploading" PDFs and summarizing.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/how_to_enable_json_mode.ipynb — Prompting for "JSON mode".
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/how_to_make_sql_queries.ipynb — SQL from natural language with schema context.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/building_moderation_filter.ipynb — Moderation filter via prompt rules/categories.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb — Metaprompt: generate starting prompts.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/read_web_pages_with_haiku.ipynb — Summarize web pages with Claude 3 Haiku.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/sampling_past_max_tokens.ipynb — Continue past max_tokens via prefill.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/session_memory_compaction.ipynb — Session memory compaction with background threading and prompt caching.
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/admin_api.ipynb — Manage your organization with the Admin API (`client.beta.organization`).
- (`misc/data/` holds fixtures. The root README still links `misc/illustrated_responses.ipynb`, which no longer exists in the tree.)

### multimodal
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/getting_started_with_vision.ipynb — Passing images into Claude.
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/best_practices_for_vision.ipynb — Vision best practices.
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/reading_charts_graphs_powerpoints.ipynb — Charts, graphs, slide decks.
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/how_to_transcribe_text.ipynb — Transcribe documents/forms.
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/using_sub_agents.ipynb — Haiku as a sub-agent with Opus for synthesis.
- https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/crop_tool.ipynb — Zoom/crop tool for fine image detail.
- (`multimodal/documents/` holds sample files.)

### coding / cost_optimization / finetuning / fable_5_fallback_billing
- https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb — Prompting for distinctive frontend designs.
- https://github.com/anthropics/claude-cookbooks/blob/main/cost_optimization/cost_optimization.ipynb — Eval-driven cost optimization checklist for agents (pass rate vs cost per task, Pareto-optimal config).
- https://github.com/anthropics/claude-cookbooks/blob/main/finetuning/finetuning_on_bedrock.ipynb — Finetuning Claude 3 Haiku on Amazon Bedrock (`finetuning/datasets/`).
- https://github.com/anthropics/claude-cookbooks/blob/main/fable_5_fallback_billing/guide.ipynb — Classifier fallback and billing for Claude Fable 5 (server-side and SDK fallback to Opus 4.8).

### third_party
Dir: https://github.com/anthropics/claude-cookbooks/tree/main/third_party (`Deepgram/`, `ElevenLabs/`, `LlamaIndex/`, `MongoDB/`, `Pinecone/`, `VoyageAI/`, `Wikipedia/`, `WolframAlpha/`).
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/Deepgram/prerecorded_audio.ipynb — Transcribe audio with Deepgram, generate interview questions.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/ElevenLabs/low_latency_stt_claude_tts.ipynb — Low-latency voice assistant (STT/TTS) (+ `stream_voice_assistant_websocket.py`).
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/Basic_RAG_With_LlamaIndex.ipynb — Basic RAG pipeline.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/Multi_Document_Agents.ipynb — Multi-document agents (ReAct DocumentAgents).
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/Multi_Modal.ipynb — Multimodal via LlamaIndex Anthropic MultiModal LLM.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/ReAct_Agent.ipynb — ReAct agent.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/Router_Query_Engine.ipynb — RouterQueryEngine.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/SubQuestion_Query_Engine.ipynb — SubQuestionQueryEngine.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/MongoDB/rag_using_mongodb.ipynb — RAG with MongoDB.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb — RAG with Pinecone.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/Pinecone/claude_3_rag_agent.ipynb — RAG agents with LangChain v1.
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/VoyageAI/how_to_create_embeddings.md — Embeddings with Voyage AI (markdown guide).
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/Wikipedia/wikipedia-search-cookbook.ipynb — Iterative Wikipedia search (legacy, Claude 2).
- https://github.com/anthropics/claude-cookbooks/blob/main/third_party/WolframAlpha/using_llm_api.ipynb — Wolfram Alpha LLM API as a tool.

---

## (b) Quickstarts — `anthropics/claude-quickstarts`

Repo: https://github.com/anthropics/claude-quickstarts (redirect target of `anthropics/anthropic-quickstarts`). Top-level: `agents/`, `autonomous-coding/`, `browser-use-demo/`, `computer-use-best-practices/`, `computer-use-demo/`, `customer-support-agent/`, `financial-data-analyst/`, `managed-agents/` (`assistant-ui/`*, `chat-sdk/`, `copilot-kit-ag-ui/`, `knowledge-wiki/`, `linear/`, `mcp-server-typescript/`, `roadtrip-planner/`, `self-hosted-sandboxes/`*, `sentry/`, `slack/`), `CLAUDE.md`, `pyproject.toml`. (*listed in `managed-agents/README.md` but not visible in the rendered tree listing.)

- **Customer Support Agent** — https://github.com/anthropics/claude-quickstarts/tree/main/customer-support-agent — Next.js support chat with Amazon Bedrock Knowledge Bases; `npm run dev`, `npm run dev:left|right|chat`, `npm run build:*`; AWS Amplify deployment; env `NEXT_PUBLIC_INCLUDE_LEFT_SIDEBAR` / `NEXT_PUBLIC_INCLUDE_RIGHT_SIDEBAR`.
- **Financial Data Analyst** — https://github.com/anthropics/claude-quickstarts/tree/main/financial-data-analyst — Next.js chat with interactive data visualization; `npm install`, create `.env.local`, `npm run dev` (http://localhost:3000).
- **Computer Use Demo** — https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo — Dockerized desktop environment (supports `computer_toolset_20260801`); run: `docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -v $HOME/.anthropic:/home/computeruse/.anthropic -p 5900:5900 -p 8501:8501 -p 6080:6080 -p 8080:8080 -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest`; Bedrock via `-e API_PROVIDER=bedrock -e AWS_PROFILE=...`, Vertex via `-e API_PROVIDER=vertex`; dev: `./setup.sh`, `docker build . -t computer-use-demo:local`; recommends XGA 1024x768.
- **Computer Use Best Practices** — https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-best-practices — native-macOS reference agent (run in a VM): explicit tool definitions, image sizing/pruning, prompt caching, server-side compaction, batched tool calls, sandboxed shell, trajectory recording. Setup: `python3.13 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && python -m playwright install chromium` (or `uv sync && uv run playwright install chromium`); `cp .env.example .env`; run `python -m computer_use "open TextEdit and type hello world"`; env toggles `CU_ENABLE_COMPUTER_USE_TOOLS`, `CU_ENABLE_BROWSER_USE_TOOLS`, `CU_JPEG_QUALITY`, `CU_BROWSER_VIEWPORT`; dev UIs: `python -m streamlit run dev_ui/trajectory_viewer/app.py`, `python -m uvicorn dev_ui.localization_demo.server:app --reload --port 8001`, `python -m uvicorn dev_ui.tool_panel.server:app --reload`; tests `python -m pytest`.
- **Browser Use Demo** — https://github.com/anthropics/claude-quickstarts/tree/main/browser-use-demo — Playwright-backed `browser` tool with DOM element targeting; `docker-compose up --build` (`--watch` for dev); UI http://localhost:8080, noVNC http://localhost:6080, VNC :5900.
- **Autonomous Coding Agent** — https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding — two-agent pattern (initializer + coding agent) with the Claude Agent SDK; progress persisted in `feature_list.json` + git. Setup: `npm install -g @anthropic-ai/claude-code`, `pip install -r requirements.txt`, `export ANTHROPIC_API_KEY='...'`; run `python autonomous_agent_demo.py --project-dir ./my_project [--max-iterations 3] [--model claude-sonnet-4-5-20250929]`. Files: `autonomous_agent_demo.py`, `agent.py`, `client.py`, `security.py` (`ALLOWED_COMMANDS` bash allowlist; OS sandbox; filesystem restricted to project dir), `progress.py`, `prompts.py`, `prompts/app_spec.txt`, `prompts/initializer_prompt.md`, `prompts/coding_prompt.md`. Generated project gets `feature_list.json`, `init.sh`, `claude-progress.txt`, `.claude_settings.json`.
- **Managed Agents** (index README: https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents). Common prereqs: `ant` CLI ≥ 1.19 (`brew install anthropics/tap/ant`), `ant auth login` or `ANTHROPIC_API_KEY`; most support `claude "walk me through setting this up"` (reads `skill.md`).
  - **Chat SDK** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/chat-sdk — research analyst in a browser chat (Vercel Chat SDK), one session per conversation, `event_deltas` streaming; `npm install`, `cp .env.example .env`, `npm run setup`, `npm run dev`; `setup/agent-config.ts` holds model + system prompt.
  - **CopilotKit + AG-UI** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/copilot-kit-ag-ui — finance assistant with generative UI via `@ag-ui/claude-managed-agents`; Node 22+; `npm install`, `npm run setup`, `npm run dev` (runtime :8787, web :5173); `npm run build && npm start`; `npm run setup -- --force`.
  - **Knowledge Wiki** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/knowledge-wiki — distill an M&A data room (SEC EDGAR) into a versioned memory-store wiki with parallel extraction, resolve pass, and a consolidation dream (`client.beta.dreams`); `pip install -r requirements.txt`, `export EDGAR_USER_AGENT="name email"`, `python3 build_manifest.py`, `python3 fetch_data_room.py --tier=mini`, `jupyter lab distill_documents_into_knowledge_wiki.ipynb`.
  - **Linear** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/linear — stateless Bun webhook bridge on Linear's Agent Platform (`AgentSessionEvent` → `sessions.create` with metadata; `session.status_idled` → `createAgentActivity`); `bun install`, `./agents/setup.sh`, `bun run dev`; `LINEAR_ALLOWED_ORG_IDS`.
  - **MCP Server (TypeScript)** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/mcp-server-typescript — nine MCP tools over the Sessions API (`wait_for_idle` collapses the event stream), stdio or Streamable HTTP; `bun install`; `printf 'CLAUDE_ENVIRONMENT_ID=%s\n' "$(ant beta:environments create --transform id --raw-output < environment.yaml)" >> .env`; `claude mcp add managed-agents -- bun --env-file="$PWD/.env" run "$PWD/src/server.ts"`; `ALLOWED_AGENT_IDS`.
  - **Road Trip Planner** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/roadtrip-planner — Next.js on a raw session: `event_deltas` SSE proxy, vault `injection_location`, `agent_with_overrides` model override, `multiagent` reviewer thread; `npm install`, `cp .env.example .env` (NPS + Windy keys), `./agents/setup.sh`, `npm run dev`; `./agents/teardown.sh`; `ant beta:vaults:credentials update --vault-id ... --credential-id ... --auth '{type: environment_variable, injection_location: {header: true, body: false}}'`.
  - **Sentry** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/sentry — scheduled deployment (`0 9 * * 1-5`), `sentry-cli` with vault env-var credential substituted by the egress proxy; `uv sync`, `cp .env.example .env`, `./agents/setup.sh`, `uv run python deploy.py`, `uv run python run_now.py`.
  - **Slack** — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/slack — stateless Bun webhook bridge (`@mention` → `sessions.create` with `slack_channel`/`slack_thread_ts` metadata; `session.status_idled` → `chat.postMessage`); `bun install`, `./agents/setup.sh`, `bun run dev`; agent YAML in `agents/slack-assistant/agent.yaml`.
  - **assistant-ui** and **self-hosted-sandboxes** (`docker/`, `docker-memory/`) are described in the managed-agents README.

---

## (c) Specs & repos

### anthropics/skills — https://github.com/anthropics/skills
Layout: `skills/` (example skills), `spec/` (only `agent-skills-spec.md`, now a pointer to https://agentskills.io/specification), `template/SKILL.md`, `README.md`.
Install in Claude Code: `/plugin marketplace add anthropics/skills` then `/plugin install document-skills@anthropic-agent-skills` or `/plugin install example-skills@anthropic-agent-skills`. API: Skills API quickstart (https://platform.claude.com/docs/en/build-with-claude/skills-guide.md). Packaging validator: `package_skill.py` (allows only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`).

Template (`template/SKILL.md`):
```markdown
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---

# Insert instructions below
```

Skill folders under `skills/` (each `https://github.com/anthropics/skills/tree/main/skills/<name>`), with their `description` frontmatter:
- `academy-guide` — recommends matching Claude Academy courses/tutorials when users ask how to use Claude products.
- `algorithmic-art` — algorithmic art with p5.js, seeded randomness, interactive parameter exploration.
- `brand-guidelines` — applies Anthropic's brand colors/typography to artifacts.
- `canvas-design` — visual art in .png/.pdf using design philosophy (posters, static pieces).
- `claude-api` — reference for the Claude API / Anthropic SDK (model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, migration); trigger rules included.
- `discernment-nudge` — appends 2-3 fact-check/assumption follow-up questions after substantive answers.
- `doc-coauthoring` — structured workflow for co-authoring docs, proposals, specs.
- `docx` — create/read/edit Word .docx/.dotx (source-available; proprietary license).
- `frontend-design` — distinctive, intentional visual design for UI.
- `internal-comms` — internal communications formats (status reports, newsletters, incident reports).
- `mcp-builder` — building high-quality MCP servers in Python (FastMCP) or Node/TypeScript.
- `pdf` — read/extract/merge/split/rotate/watermark/fill/encrypt/OCR PDFs (proprietary license).
- `pptx` — create/read/edit .pptx/.potx (proprietary license).
- `skill-creator` — create, improve, eval, and benchmark skills; optimize descriptions for triggering.
- `slack-gif-creator` — animated GIFs optimized for Slack.
- `theme-factory` — 10 preset themes to style artifacts.
- `web-artifacts-builder` — multi-component claude.ai HTML artifacts (React, Tailwind, shadcn/ui).
- `webapp-testing` — Playwright toolkit for testing local web apps.
- `xlsx` — spreadsheets: read/edit/create .xlsx/.xlsm/.csv/.tsv (proprietary license).

#### Agent Skills spec — SKILL.md frontmatter (exact, from `agentskills/agentskills` `docs/specification.mdx`)
Directory structure:
```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```
Frontmatter fields:

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. |
| `description` | Yes | Max 1024 characters. Non-empty. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata` | No | Arbitrary key-value mapping for additional metadata (a map from string keys to string values). |
| `allowed-tools` | No | Space-separated string of pre-approved tools the skill may use. (Experimental) |

`name` rules: 1-64 chars; only `a-z`, `0-9`, `-`; must not start/end with `-`; no consecutive `--`; must match the parent directory name. `description`: 1-1024 chars, describe what and when, include keywords. `compatibility`: 1-500 chars if present. `allowed-tools` example: `allowed-tools: Bash(git:*) Bash(jq:*) Read`. Progressive disclosure: metadata (~100 tokens) at startup; SKILL.md body (<5000 tokens recommended, keep under 500 lines) on activation; `scripts/`, `references/`, `assets/` on demand. Relative file references one level deep. Validate with `skills-ref validate ./my-skill` (https://github.com/agentskills/agentskills/tree/main/skills-ref).

### anthropics/claude-agent-sdk-python — https://github.com/anthropics/claude-agent-sdk-python
- Install: `pip install claude-agent-sdk` (Python 3.10+; bundles the Claude Code CLI; override with `ClaudeAgentOptions(cli_path=...)` or `curl -fsSL https://claude.ai/install.sh | bash`).
- Key APIs: `query(prompt, options)` (async iterator of messages); `ClaudeAgentOptions` (`system_prompt` incl. `{"type":"preset"|"custom", ..., "snapshot": False}`, `max_turns`, `allowed_tools`, `disallowed_tools`, `permission_mode` e.g. `'acceptEdits'`, `cwd`, `mcp_servers`, `hooks`, `can_use_tool`); `ClaudeSDKClient` (bidirectional; `.query()`, `.receive_response()`); `@tool(name, description, schema)` + `create_sdk_mcp_server(name, version, tools)` for in-process MCP servers (tool names `mcp__<server>__<tool>`); `HookMatcher(matcher=..., hooks=[...])` with hook return `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": ...}}`; message types `AssistantMessage`, `UserMessage`, `SystemMessage`, `ResultMessage`; blocks `TextBlock`, `ToolUseBlock`, `ToolResultBlock`; errors `ClaudeSDKError`, `CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `ResultError`, `CLIJSONDecodeError`. Migration: `ClaudeCodeOptions` → `ClaudeAgentOptions`.
- Docs: https://code.claude.com/docs/en/agent-sdk/python.md

### anthropics/claude-agent-sdk-typescript — https://github.com/anthropics/claude-agent-sdk-typescript
- npm package `@anthropic-ai/claude-agent-sdk`; install `npm install @anthropic-ai/claude-agent-sdk` (Node 18+). Formerly the "Claude Code SDK" (migration guide: https://code.claude.com/docs/en/agent-sdk/migration-guide.md). Reference: https://code.claude.com/docs/en/agent-sdk/typescript.md

### anthropics/claude-code — https://github.com/anthropics/claude-code
- Install (npm deprecated): macOS/Linux `curl -fsSL https://claude.ai/install.sh | bash`; Homebrew `brew install --cask claude-code`; Windows `irm https://claude.ai/install.ps1 | iex` or `winget install Anthropic.ClaudeCode`; legacy `npm install -g @anthropic-ai/claude-code`. Run `claude` in a project. Includes `plugins/` directory and `examples/hooks/bash_command_validator_example.py`.
- CHANGELOG (https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) top entries: **2.1.278** — auto mode defaults to the server-side classifier (no classifier billing; `CLAUDE_CODE_AUTO_MODE_SERVER=0` opts out on Bedrock/Vertex/Foundry/gateways); `/status` gains an "Auto mode server" row. **2.1.277** — AGENTS.md support (read when no CLAUDE.md; "Project instructions" in `/config`); `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY=1`; optional `headers:` map on Claude apps gateway upstreams; many fixes (`claude -p`/SDK hang → exit 1, `--resume` empty text block, plugin install, Edit/Write tools, sandbox `excludedCommands` compound-command matching, headless resume cost totals, etc.).

### anthropics/claude-code-action — https://github.com/anthropics/claude-code-action
- GitHub Action for PRs/issues (@claude mentions, issue assignment, explicit `prompt` automation); inputs `prompt` and `claude_args`; structured JSON outputs become Action outputs; runs on your runner; auth via Anthropic API key / WIF, Bedrock, Vertex, Foundry. Quickstart: run `/install-github-app` inside `claude`. Docs in `docs/`: `solutions.md`, `migration-guide.md` (v0.x→v1.0), `setup.md`, `usage.md`, `custom-automations.md`, `configuration.md`, `experimental.md`, `cloud-providers.md`, `capabilities-and-limitations.md`, `security.md`, `faq.md`. Related docs: https://code.claude.com/docs/en/github-actions.md

### anthropic-experimental/sandbox-runtime — https://github.com/anthropic-experimental/sandbox-runtime
- `npm install -g @anthropic-ai/sandbox-runtime`; CLI `srt <command>`, `srt --debug ...`, `srt --settings /path/to/srt-settings.json ...`, `srt --control-fd 3 -- npm test`; library exports `SandboxManager`, `SandboxRuntimeConfig`. Uses `sandbox-exec` (Seatbelt) on macOS and `bubblewrap` on Linux, plus a proxy for network filtering. Settings file default `~/.srt-settings.json`:
```json
{
  "network": { "allowedDomains": ["github.com", "*.github.com"], "deniedDomains": ["malicious.com"], "allowUnixSockets": ["/var/run/docker.sock"], "allowLocalBinding": false },
  "filesystem": { "denyRead": ["~/.ssh"], "allowRead": [], "allowWrite": [".", "src/", "test/", "/tmp"], "denyWrite": [".env", "config/production.json"] },
  "ignoreViolations": { "*": ["/usr/bin", "/System"], "git push": ["/usr/bin/nc"], "npm": ["/private/tmp"] },
  "enableWeakerNestedSandbox": false, "enableWeakerNetworkIsolation": false, "allowAppleEvents": false
}
```
  Other keys: `network.deniedDomainReasons`, `network.deniedResolvedAddresses`, `network.tlsTerminate` (`excludeDomains`, `extraCaCertPaths`, `caCertPath`/`caKeyPath`, `filterRequest`), `network.allowAllUnixSockets`, `javaAgentJarPath`. Network is allow-only; writes are allow-only; reads are deny-then-allow. Same primitives back Claude Code's sandboxed Bash tool.

### anthropics/mcpb (formerly dxt) — https://github.com/anthropics/mcpb (https://github.com/anthropics/dxt serves the same README)
- MCP Bundles: `.mcpb` zip containing a local MCP server + `manifest.json` (spec in `MANIFEST.md`, CLI in `CLI.md`, examples in `examples/`). `npm install -g @anthropic-ai/mcpb`; `mcpb init`; `mcpb pack`. `server.type` = `node` | `python` | `uv` | binary; `server.entry_point`; `mcp_config.env`. Renames: `dxt` CLI → `mcpb`, `.dxt` → `.mcpb`, `@anthropic-ai/dxt` → `@anthropic-ai/mcpb`.

### anthropics/courses — https://github.com/anthropics/courses (default branch `master`)
1. https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals — Claude SDK essentials (API key, params, multimodal prompts, streaming).
2. https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial — step-by-step prompting techniques (AWS Workshop version exists).
3. https://github.com/anthropics/courses/tree/master/real_world_prompting — prompting techniques in complex real-world prompts (Vertex branch: `vertex/real_world_prompting`).
4. https://github.com/anthropics/courses/tree/master/prompt_evaluations — writing production prompt evaluations.
5. https://github.com/anthropics/courses/tree/master/tool_use — implementing tool use.

### anthropics/prompt-eng-interactive-tutorial — https://github.com/anthropics/prompt-eng-interactive-tutorial
- 9 chapters + appendix (Claude 3 Haiku): 1 Basic Prompt Structure; 2 Being Clear and Direct; 3 Assigning Roles; 4 Separating Data from Instructions; 5 Formatting Output & Speaking for Claude; 6 Precognition (Thinking Step by Step); 7 Using Examples; 8 Avoiding Hallucinations; 9 Building Complex Prompts (chatbot, legal, financial, coding); Appendix: Chaining Prompts, Tool Use, Search & Retrieval. Google Sheets version available.

### anthropics/anthropic-sdk-python — https://github.com/anthropics/anthropic-sdk-python
- `pip install anthropic` (Python 3.10+); `from anthropic import Anthropic; client = Anthropic(api_key=...); client.messages.create(model="claude-opus-5", max_tokens=1024, messages=[...])`; v1 migration in `MIGRATION.md`. Docs: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python.md

### anthropics/anthropic-sdk-typescript — https://github.com/anthropics/anthropic-sdk-typescript
- `npm install @anthropic-ai/sdk` (TS ≥ 5.0; Node 20+, Deno, Bun, Cloudflare Workers, Vercel Edge; browser needs `dangerouslyAllowBrowser: true`); `import Anthropic from '@anthropic-ai/sdk'; const client = new Anthropic(); await client.messages.create({ model: 'claude-opus-4-6', max_tokens: 1024, messages: [...] })`. Docs: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/typescript.md

### modelcontextprotocol org — https://github.com/modelcontextprotocol
- **Specification** — https://github.com/modelcontextprotocol/modelcontextprotocol (spec, schema `schema/2026-07-28/schema.ts` and `.json`, docs site https://modelcontextprotocol.io; latest spec revision 2026-07-28: https://modelcontextprotocol.io/specification/2026-07-28). `github.com/modelcontextprotocol/specification` carries the same README.
- **servers** — https://github.com/modelcontextprotocol/servers — reference servers: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time (archived ones at `servers-archived`). Run `npx -y @modelcontextprotocol/server-memory`, `uvx mcp-server-git`; client config shape `{"mcpServers": {"memory": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"]}}}`. Registry: https://registry.modelcontextprotocol.io/
- **python-sdk** — https://github.com/modelcontextprotocol/python-sdk — v2 (spec 2026-07-28); `uv add "mcp[cli]"` / `pip install "mcp[cli]"` (pin `mcp>=1.28,<2` for v1.x); `from mcp.server import MCPServer; mcp = MCPServer("Demo"); @mcp.tool() ...; @mcp.resource("greeting://{name}") ...`; `uv run mcp dev server.py`; `uv run mcp run server.py --transport streamable-http`; client `from mcp import Client; async with Client("http://localhost:8000/mcp") as client: await client.call_tool(...)`. Docs https://py.sdk.modelcontextprotocol.io/
- **typescript-sdk** — https://github.com/modelcontextprotocol/typescript-sdk — v2 split packages `@modelcontextprotocol/server` and `@modelcontextprotocol/client` (+ middleware `@modelcontextprotocol/node|express|fastify|hono`); `import { McpServer } from '@modelcontextprotocol/server'; import { StdioServerTransport } from '@modelcontextprotocol/server/stdio'; server.registerTool('greet', { description, inputSchema: z.object({...}) }, async ({name}) => ({ content: [{type:'text', text}] }))`. Docs https://ts.sdk.modelcontextprotocol.io/v2/

---

## (d) Claude Platform docs — `platform.claude.com`

Index: https://platform.claude.com/docs/llms.txt (629 English pages; full text at https://platform.claude.com/llms-full.txt). Every page is available as Markdown by appending `.md`. Sections below reproduce the index for all non-endpoint pages; the "API Reference" endpoint section (377 pages, mostly `/docs/en/api/beta/...`) is summarized.

### Getting started / Messages
- https://platform.claude.com/docs/en/home.md — Documentation home
- https://platform.claude.com/docs/en/intro.md — Intro to Claude
- https://platform.claude.com/docs/en/get-started.md — Quickstart
- https://platform.claude.com/docs/en/get-api-key.md — Get your API key
- https://platform.claude.com/docs/en/claude_api_primer.md — API usage primer
- https://platform.claude.com/docs/en/build-with-claude/overview.md — Features overview
- https://platform.claude.com/docs/en/build-with-claude/working-with-messages.md — Using the Messages API
- https://platform.claude.com/docs/en/build-with-claude/streaming.md — Streaming messages
- https://platform.claude.com/docs/en/build-with-claude/token-counting.md — Token counting
- https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons.md — Stop reasons and fallback
- https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback.md — Refusals and fallback
- https://platform.claude.com/docs/en/build-with-claude/fallback-credit.md — Fallback credit
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages.md — Mid-conversation system messages and tool changes
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-effort-example.md — Build an orchestration mode
- https://platform.claude.com/docs/en/build-with-claude/multilingual-support.md — Multilingual support
- https://platform.claude.com/docs/en/build-with-claude/embeddings.md — Embeddings
- https://platform.claude.com/docs/en/build-with-claude/fast-mode.md — Fast mode (research preview)
- https://platform.claude.com/docs/en/build-with-claude/task-budgets.md — Task budgets (beta)

### build-with-claude (context, caching, thinking, files, batches, outputs)
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md — Prompt caching
- https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics.md — Cache diagnostics (beta)
- https://platform.claude.com/docs/en/build-with-claude/thinking.md — Thinking (overview)
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md — Extended thinking (legacy)
- https://platform.claude.com/docs/en/build-with-claude/preserved-thinking.md — Preserved thinking
- https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost.md — Steering thinking and cost control
- https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows.md — Thinking in tool and multi-turn workflows
- https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting.md — Troubleshooting thinking
- https://platform.claude.com/docs/en/build-with-claude/effort.md — Effort
- https://platform.claude.com/docs/en/build-with-claude/context-windows.md — Context windows
- https://platform.claude.com/docs/en/build-with-claude/context-editing.md — Context editing
- https://platform.claude.com/docs/en/build-with-claude/compaction.md — Compaction
- https://platform.claude.com/docs/en/build-with-claude/files.md — Files API
- https://platform.claude.com/docs/en/build-with-claude/batch-processing.md — Batch processing
- https://platform.claude.com/docs/en/build-with-claude/citations.md — Citations
- https://platform.claude.com/docs/en/build-with-claude/pdf-support.md — PDF support
- https://platform.claude.com/docs/en/build-with-claude/search-results.md — Search results
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md — Structured outputs
- https://platform.claude.com/docs/en/build-with-claude/vision.md — Vision
- https://platform.claude.com/docs/en/build-with-claude/vision-coordinates.md — Coordinates and bounding boxes
- https://platform.claude.com/docs/en/build-with-claude/skills-guide.md — Using Agent Skills with the API
- Cloud platforms: https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock.md (Opus 4.7+), https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy.md, https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md, https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.md, https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry.md

### agents-and-tools / tool use
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md — Tool use overview
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works.md — How tool use works
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.md — Define tools
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls.md — Handle tool calls
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent.md — Tutorial: build a tool-using agent
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference.md — Tool reference
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-combinations.md — Tool combinations
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner.md — Tool Runner (SDK)
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md — Tool search tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md — Programmatic tool calling
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use.md — Parallel tool use
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use.md — Strict tool use
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming.md — Fine-grained tool streaming
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching.md — Tool use with prompt caching
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context.md — Manage tool context
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use.md — Troubleshooting tool use
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools.md — Server tools
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md — Bash tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md — Code execution tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md — Computer use tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool.md — Browser use tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool.md — Text editor tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool.md — Web search tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool.md — Web fetch tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md — Memory tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool.md — Advisor tool
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md — MCP connector
- https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers.md — Remote MCP servers
- MCP tunnels: https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview.md, .../mcp-tunnels/quickstart.md, .../mcp-tunnels/concepts.md, .../mcp-tunnels/deploy-compose.md, .../mcp-tunnels/deploy-helm.md, .../mcp-tunnels/console.md, .../mcp-tunnels/reference.md, .../mcp-tunnels/security.md, .../mcp-tunnels/troubleshooting.md

### Agent Skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md — Overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md — Quickstart (API)
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md — Skill authoring best practices
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise.md — Skills for enterprise
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md — Claude API skill
- https://platform.claude.com/docs/en/build-with-claude/skills-guide.md — Skills in the API
- Skills API endpoints: https://platform.claude.com/docs/en/api/skills.md, .../api/skills/create.md, .../api/skills/list.md, .../api/skills/retrieve.md, .../api/skills/delete.md, .../api/skills/versions.md, .../api/skills/versions/create.md, .../api/skills/versions/list.md, .../api/skills/versions/retrieve.md, .../api/skills/versions/delete.md

### Managed Agents
- https://platform.claude.com/docs/en/managed-agents/overview.md — Overview
- https://platform.claude.com/docs/en/managed-agents/quickstart.md — Quickstart
- https://platform.claude.com/docs/en/managed-agents/onboarding.md — Build in Console
- https://platform.claude.com/docs/en/managed-agents/agent-setup.md — Define your agent
- https://platform.claude.com/docs/en/managed-agents/sessions.md — Start a session
- https://platform.claude.com/docs/en/managed-agents/session-operations.md — Session operations
- https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md — Session event stream
- https://platform.claude.com/docs/en/managed-agents/budgets.md — Session budgets
- https://platform.claude.com/docs/en/managed-agents/environments.md — Cloud environment setup
- https://platform.claude.com/docs/en/managed-agents/cloud-sandboxes-reference.md — Cloud sandbox reference
- https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md — Self-hosted sandboxes integration guide
- https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security.md — Security model
- https://platform.claude.com/docs/en/managed-agents/vaults.md — Authenticate with vaults
- https://platform.claude.com/docs/en/managed-agents/tools.md — Tools
- https://platform.claude.com/docs/en/managed-agents/mcp-connector.md — MCP connector
- https://platform.claude.com/docs/en/managed-agents/skills.md — Agent Skills
- https://platform.claude.com/docs/en/managed-agents/memory.md — Memory stores
- https://platform.claude.com/docs/en/managed-agents/dreams.md — Dreams
- https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration.md — Multiagent orchestration
- https://platform.claude.com/docs/en/managed-agents/define-outcomes.md — Define outcomes
- https://platform.claude.com/docs/en/managed-agents/permission-policies.md — Permission policies
- https://platform.claude.com/docs/en/managed-agents/scheduled-deployments.md — Scheduled deployments
- https://platform.claude.com/docs/en/managed-agents/webhooks.md — Subscribe to webhooks
- https://platform.claude.com/docs/en/managed-agents/files.md — Attach and download files
- https://platform.claude.com/docs/en/managed-agents/github.md — Access GitHub
- https://platform.claude.com/docs/en/managed-agents/migration.md — Migration
- https://platform.claude.com/docs/en/managed-agents/reference.md — Reference
- (The "harness" concept is covered under agent-setup/tools/reference; there is no separate harness page in the index.)

### Agent SDK
Agent SDK docs live on code.claude.com (see section E, "Agent SDK" list). Entry: https://code.claude.com/docs/en/agent-sdk/overview.md

### Prompt engineering (all pages)
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.md — Overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md — Prompting best practices
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5.md
- Related: https://platform.claude.com/docs/en/about-claude/additional-resources.md, https://platform.claude.com/docs/en/about-claude/glossary.md

### Test and evaluate
- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests.md — Define success criteria and build evaluations (the index currently has a single combined page; no separate "define-success" or "evaluation tool" page is listed)
- Strengthen guardrails: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations.md, .../increase-consistency.md, .../mitigate-jailbreaks.md, .../reduce-prompt-leak.md, .../reduce-latency.md, .../handle-streaming-refusals.md

### Use-case guides
- https://platform.claude.com/docs/en/about-claude/use-case-guides/overview.md, .../ticket-routing.md, .../customer-support-chat.md, .../content-moderation.md, .../legal-summarization.md, .../commerce-agents.md

### Administration (manage-claude)
- https://platform.claude.com/docs/en/manage-claude/admin-api.md — Admin API
- https://platform.claude.com/docs/en/manage-claude/admin-api-keys.md — Create an Admin API key
- https://platform.claude.com/docs/en/manage-claude/authentication.md — Authentication
- https://platform.claude.com/docs/en/manage-claude/user-management.md — User management
- https://platform.claude.com/docs/en/manage-claude/workspaces.md — Workspaces
- https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md — Usage and Cost API
- https://platform.claude.com/docs/en/manage-claude/analytics-api.md — Analytics APIs
- https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api.md — Claude Code Analytics API
- https://platform.claude.com/docs/en/manage-claude/rate-limits-api.md — Rate Limits API
- https://platform.claude.com/docs/en/manage-claude/spend-limits-api.md — Spend Limits API
- https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md — API and data retention
- https://platform.claude.com/docs/en/manage-claude/data-residency.md — Data residency
- https://platform.claude.com/docs/en/manage-claude/access-transparency.md — Access Transparency
- https://platform.claude.com/docs/en/manage-claude/app-attest.md — App Attest
- Compliance API: https://platform.claude.com/docs/en/manage-claude/compliance-api.md, .../compliance-api-access.md, .../compliance-integration-patterns.md, .../compliance-org-data.md, .../compliance-activity-feed.md, .../compliance-content-data.md, .../compliance-sessions.md, .../compliance-errors.md, .../compliance-faq.md
- CMEK: https://platform.claude.com/docs/en/manage-claude/cmek.md, .../cmek-aws-kms.md, .../cmek-azure-key-vault.md, .../cmek-google-cloud-kms.md
- Inference hooks: https://platform.claude.com/docs/en/manage-claude/inference-hooks.md, .../inference-hooks-configuration.md, .../inference-hooks-endpoint.md
- Workload Identity Federation: https://platform.claude.com/docs/en/manage-claude/workload-identity-federation.md, .../wif-reference.md, .../wif-admin-api.md, .../wif-providers/aws.md, .../wif-providers/gcp.md, .../wif-providers/azure.md, .../wif-providers/github-actions.md, .../wif-providers/kubernetes.md, .../wif-providers/okta.md, .../wif-providers/spiffe.md

### Models & pricing
- https://platform.claude.com/docs/en/models/overview.md, https://platform.claude.com/docs/en/about-claude/pricing.md, https://platform.claude.com/docs/en/about-claude/models/choosing-a-model.md, .../models/model-ids-and-versions.md, .../models/optimizing-for-cost-and-intelligence.md, .../models/migration-guide.md, https://platform.claude.com/docs/en/about-claude/model-deprecations.md, https://platform.claude.com/docs/en/resources/overview.md (model cards)
- Model pages: https://platform.claude.com/docs/en/models/{fable-5,fable-5-1,mythos-5,mythos-5-1,opus-5,opus-4-8,opus-4-7,opus-4-6,opus-4-5,sonnet-5,sonnet-4-6,sonnet-4-5,haiku-4-5}/overview.md; migration guides `/models/{fable-5-1,opus-5,sonnet-5,haiku-4-5,fable-5}/migration-guide.md`; what's-new `/models/fable-5-1/whats-new-fable-5-1.md`, `/models/opus-5/whats-new-opus-5.md`, `/models/sonnet-5/whats-new-sonnet-5.md`; https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5.md
- System prompts release notes: https://platform.claude.com/docs/en/release-notes/system-prompts/overview.md (+ one page per model under `/release-notes/system-prompts/claude-<model>.md`)

### CLI, SDKs, and libraries
- https://platform.claude.com/docs/en/cli-sdks-libraries/overview.md; CLI (`ant`): .../cli/quickstart.md, .../cli/using.md, .../cli/authentication.md, .../cli/scripting.md, .../cli/apply.md (`ant apply`), .../cli/sessions-connect.md; SDKs: .../sdks/python.md, .../sdks/typescript.md, .../sdks/java.md, .../sdks/go.md, .../sdks/csharp.md, .../sdks/ruby.md, .../sdks/php.md; .../middleware.md; libraries: .../libraries/openai-sdk.md, .../libraries/apple-foundation-models.md

### API reference (non-endpoint) and endpoints
- https://platform.claude.com/docs/en/api/overview.md, .../api/beta-headers.md, .../api/errors.md, .../api/rate-limits.md, .../api/service-tiers.md, .../api/versioning.md, .../api/ip-addresses.md, .../api/supported-regions.md, .../api/claude-platform-on-aws-iam-actions.md, .../api/claude-code/routines-fire.md; release notes https://platform.claude.com/docs/en/release-notes/overview.md
- Core endpoints: https://platform.claude.com/docs/en/api/messages.md, .../api/messages/create.md, .../api/messages/count_tokens.md, .../api/messages/batches.md (+ create/retrieve/results/list/cancel/delete), .../api/models.md (+ list/retrieve), .../api/files.md (+ upload/list/retrieve_metadata/download/delete), .../api/skills.md (+ versions), .../api/completions.md, .../api/compliance.md, .../api/beta.md (Managed Agents: agents, sessions, environments, vaults, memory, dreams, deployments, webhooks; organization admin, RBAC, service accounts, federation; all under `/docs/en/api/beta/...`).

---

## (e) Claude Code docs — `code.claude.com` with configuration reference

Index: https://code.claude.com/docs/llms.txt (append `.md` to any page). Full page list:
- Getting started: overview.md, quickstart.md, changelog.md; core concepts: how-claude-code-works.md, features-overview.md, claude-directory.md, context-window.md, prompt-caching.md; use: memory.md, sessions.md, common-workflows.md, prompt-library.md, best-practices.md; platforms: platforms.md, remote-control.md, claude-projects.md, mobile.md, chrome.md, computer-use.md, vs-code.md, jetbrains.md, slack.md, claude-tag.md, web-quickstart.md, claude-code-on-the-web.md, routines.md, ultrareview.md, desktop-quickstart.md, desktop.md, desktop-linux.md, desktop-wsl.md, desktop-scheduled-tasks.md, desktop-ios-simulator.md; CI: security-guidance.md, claude-security.md, code-review.md, github-actions.md, github-actions-cloud-providers.md, github-enterprise-server.md, gitlab-ci-cd.md.
- Build: agents.md, sub-agents.md, agent-view.md, agent-teams.md, cross-session-messaging.md, workflows.md, worktrees.md, mcp-quickstart.md, mcp.md, skills.md, discover-plugins.md, plugins.md, plugin-evals.md, artifacts.md, hooks-guide.md, channels.md, scheduled-tasks.md, goal.md, headless.md, deep-links.md, large-codebases.md, troubleshoot-install.md, troubleshooting.md, debug-your-config.md, errors.md.
- Administration: admin-setup.md, setup.md, authentication.md, managed-settings.md, server-managed-settings.md, managed-mcp.md, auto-mode-config.md, third-party-integrations.md, feature-availability.md, amazon-bedrock.md, claude-platform-on-aws.md, google-vertex-ai.md, microsoft-foundry.md, network-config.md, corporate-launcher.md, devcontainer.md, gateways.md, claude-apps-gateway*.md, llm-gateway*.md, monitoring-usage.md, costs.md, analytics.md, plugin-marketplaces.md, plugin-dependencies.md, plugin-hints.md, plugin-relevance.md, security.md, data-usage.md, zero-data-retention.md, communications-kit.md, champion-kit.md.
- Configuration: settings.md, settings-reference.md, settings-example.md, permissions.md, permission-modes.md, sandboxing.md, sandbox-environments.md, cloud-environments.md, self-hosted-environments*.md, model-config.md, fast-mode.md, advisor.md, output-styles.md, terminal-config.md, fullscreen.md, accessibility.md, voice-dictation.md, statusline.md, keybindings.md.
- Reference: cli-reference.md, commands.md, env-vars.md, tools-reference.md, interactive-mode.md, checkpointing.md, hooks.md, plugins-reference.md, channels-reference.md, glossary.md.
- Agent SDK: https://code.claude.com/docs/en/agent-sdk/overview.md, quickstart.md, migration-guide.md, troubleshooting.md, configuration.md, examples.md, agent-loop.md, claude-code-features.md, sessions.md, session-storage.md, streaming-vs-single-mode.md, user-input.md, streaming-output.md, structured-outputs.md, custom-tools.md, mcp.md, tool-search.md, subagents.md, modifying-system-prompts.md, skills.md, plugins.md, permissions.md, hooks.md, file-checkpointing.md, cost-tracking.md, observability.md, todo-tracking.md, hosting.md, secure-deployment.md, typescript.md, typescript-v2-preview.md, python.md (all under `/docs/en/agent-sdk/`).
- What's new: https://code.claude.com/docs/en/whats-new/index.md and weekly pages `whats-new/2026-w13.md` … `2026-w37.md`.

### memory.md — https://code.claude.com/docs/en/memory.md
CLAUDE.md hierarchy (load order, broadest first):
| Scope | Location |
|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` (or `claudeMd` key in `managed-settings.json`) |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` (or `AGENTS.md` when no CLAUDE.md exists, v2.1.277+) |
| Local | `./CLAUDE.local.md` (gitignore it) |
- Files from cwd and every ancestor load at launch and are concatenated (root → cwd; `CLAUDE.local.md` after `CLAUDE.md`); subdirectory CLAUDE.md files load on demand when Claude reads files there. Target under 200 lines; files over 4 MiB are skipped. HTML comments are stripped.
- Imports: `@path/to/import` (relative to the containing file or absolute; recursive up to 4 hops; skipped inside code spans/blocks; e.g. `See @README and @package.json`, `- @~/.claude/my-project-instructions.md`). External imports (outside the working directory) trigger a one-time approval dialog.
- Rules: `.claude/rules/*.md` (recursive; same priority as `.claude/CLAUDE.md`); path-scoped via frontmatter `paths: ["src/api/**/*.ts"]` (globs, brace expansion; budget 1,000 expanded patterns / 4 MiB); user-level `~/.claude/rules/`; symlinks supported.
- Exclusions: `claudeMdExcludes: ["**/monorepo/CLAUDE.md", ...]` (any settings layer; managed CLAUDE.md can't be excluded). `--add-dir` CLAUDE.md loads only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`.
- AGENTS.md: default `claude-md-or-agents-md`; set via `/config` → Project instructions, or `"pluginConfigs": {"agents-md@builtin": {"options": {"instructionFiles": "claude-md-and-agents-md" | "claude-md" | "managed-only"}}}` in user/managed settings. Share one file: `@AGENTS.md` import in CLAUDE.md, or `ln -s AGENTS.md CLAUDE.md`.
- Auto memory: on by default; toggle in `/memory`, `"autoMemoryEnabled": false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; stored at `~/.claude/projects/<project>/memory/` (`MEMORY.md` index — first 200 lines / 25 KB loaded each session — plus topic files like `user_role.md`, `feedback_testing.md`); relocate with `"autoMemoryDirectory": "~/my-custom-memory-dir"`; memory types recorded in frontmatter `type`: `user`, `feedback`, `project`, `reference`; `modified` timestamp added. `/memory` lists and opens files; `/context` shows loaded memory files; `/init` generates CLAUDE.md (`CLAUDE_CODE_NEW_INIT=1` for the interactive flow); `/import` migrates other tools' config.

### settings.md — https://code.claude.com/docs/en/settings.md
Files and scope:
| Scope | File |
|---|---|
| User | `~/.claude/settings.json` |
| Shared project | `.claude/settings.json` (commit it) |
| Project local | `.claude/settings.local.json` (auto-gitignored via global excludes) |
| Managed | `managed-settings.json` / MDM / server-managed settings from claude.ai |
Plus `~/.claude.json` (app state, OAuth, MCP servers, global config keys). `CLAUDE_CONFIG_DIR` relocates the home files.
Precedence (highest first): 1 Managed → 2 CLI args (`--settings <file-or-json>`, `--model`, `--permission-mode`, …) → 3 `.claude/settings.local.json` → 4 `.claude/settings.json` → 5 `~/.claude/settings.json`. List keys (e.g. `permissions.allow`) merge across files; `fallbackModel`, `modelPicker`, `availableModels`, `modelSettings` have special rules. Env vars are decided per pair (`ANTHROPIC_MODEL` beats `model`; `ANTHROPIC_DEFAULT_MODEL` applies only when no file sets `model`). Security exceptions where stricter lower-scope values win: `disableClaudeAiConnectors`, `enableArtifact`/`disableArtifact`, `isolatePeerMachines`, `remoteControlAtStartup`, `crossSessionInbound`, `useAutoModeDuringPlan`, `syncClaudeAiSkills`, `syncClaudeAiPlugins`, `maxEffortLevel`. `/status` shows setting sources; `/config` edits.

### settings-reference.md — https://code.claude.com/docs/en/settings-reference.md
All 231 documented keys: `advisorModel agent agentPushNotifEnabled allowAllClaudeAiMcps allowedChannelPlugins allowedHttpHookUrls allowedMcpServers allowManagedHooksOnly allowManagedMcpServersOnly allowManagedPermissionRulesOnly alwaysThinkingEnabled apiKeyHelper askUserQuestionTimeout attribution attribution.commit attribution.pr attribution.sessionUrl autoCompactEnabled autoCompactWindow autoConnectIde autoContinueAtUsageLimit autoInstallIdeExtension autoMemoryDirectory autoMemoryEnabled autoMode autoMode.classifyAllShell autoScrollEnabled autoUpdatesChannel availableModels awaySummaryEnabled awsAuthRefresh awsCredentialExport axScreenReader bashEditDiffEnabled bashOutputMaxChars blockedMarketplaces browserExternalPageTools channelsEnabled claudeMd claudeMdExcludes cleanupPeriodDays companyAnnouncements copyOnSelect crossSessionInbound defaultShell deniedMcpServers desktopSessionCleanupPeriodDays dialogExpiry diffTool disableAgentView disableAllHooks disableArtifact disableAutoMode disableBrowserExternalNavigation disableBundledSkills disableClaudeAiConnectors disableCommandPluginSources disableDeepLinkRegistration disableDesktopLocalSessions disabledMcpjsonServers disableMobileSimulatorTools disableRemoteControl disableSideloadFlags disableSkillShellExecution disableWorkflows editorMode effortLevel emojiCompletionEnabled enableAllProjectMcpServers enableArtifact enabledMcpjsonServers enabledPlugins enableWorkflows enforceAvailableModels env externalEditorContext extraKnownMarketplaces fallbackModel fastMode fastModePerSessionOptIn feedbackDrafts feedbackSurveyRate fileCheckpointingEnabled fileSuggestion footerLinksRegexes forceLoginGatewayUrl forceLoginMethod forceLoginOrgUUID forceRemoteSettingsRefresh gatewayInternalNetworks gcpAuthRefresh hooks httpHookAllowedEnvVars includeCoAuthoredBy includeGitInstructions inputNeededNotifEnabled isolatePeerMachines keybindingFlavor language managedMcpServers managedSourcesBehavior maxEffortLevel minimumVersion model modelOverrides modelPicker modelPricing modelSettings otelHeadersHelper outputStyle parentSettingsBehavior permissionExplainerEnabled permissions permissions.additionalDirectories permissions.allow permissions.ask permissions.blockReadsOutsideWorkingDirectories permissions.defaultMode permissions.deny permissions.disableBypassPermissionsMode plansDirectory pluginConfigs pluginSuggestionMarketplaces pluginTrustMessage policyHelper policyHelper.path policyHelper.refreshIntervalMs policyHelper.timeoutMs preferredNotifChannel prefersReducedMotion processWrapper promptCacheTtl promptSuggestionEnabled prUrlTemplate remote.defaultEnvironmentId remoteControlAtStartup requiredMaximumVersion requiredMinimumVersion respectGitignore respondToBashCommands sandbox sandbox.allowAppleEvents sandbox.allowUnsandboxedCommands sandbox.autoAllowBashIfSandboxed sandbox.bwrapPath sandbox.credentials sandbox.credentials.allowPlaintextInject sandbox.credentials.awsPairs sandbox.credentials.envVars sandbox.credentials.files sandbox.credentials.sigv4 sandbox.enabled sandbox.enableWeakerNestedSandbox sandbox.enableWeakerNetworkIsolation sandbox.excludedCommands sandbox.failIfUnavailable sandbox.filesystem sandbox.filesystem.allowManagedReadPathsOnly sandbox.filesystem.allowRead sandbox.filesystem.allowWrite sandbox.filesystem.denyRead sandbox.filesystem.denyWrite sandbox.filesystem.disabled sandbox.ignoreViolations sandbox.network sandbox.network.allowAllUnixSockets sandbox.network.allowedDomains sandbox.network.allowLocalBinding sandbox.network.allowMachLookup sandbox.network.allowManagedDomainsOnly sandbox.network.allowUnixSockets sandbox.network.deniedDomains sandbox.network.httpProxyPort sandbox.network.socksProxyPort sandbox.network.strictAllowlist sandbox.network.tlsTerminate sandbox.ripgrep sandbox.socatPath showClearContextOnPlanAccept showThinkingSummaries showTurnDuration skillListingBudgetFraction skillListingMaxDescChars skillOverrides skipAutoPermissionPrompt skipDangerousModePermissionPrompt skipWebFetchPreflight spellcheck spinnerTipsEnabled spinnerTipsOverride spinnerVerbs sshConfigs sshHostAllowlist statusLine strictKnownMarketplaces strictPluginOnlyCustomization strictPluginOnlyCustomization.agents strictPluginOnlyCustomization.hooks strictPluginOnlyCustomization.mcp strictPluginOnlyCustomization.skills subagentPromptCacheTtl subagentStatusLine switchModelsOnFlag syncClaudeAiPlugins syncClaudeAiSkills syntaxHighlightingDisabled taskOutputMaxChars teammateDefaultModel teammateMode terminalProgressBarEnabled terminalTitleFromRename theme timeFormat timeZone tui ultracode useAutoModeDuringPlan verbose viewMode vimInsertModeRemaps voice voiceEnabled wheelScrollAccelerationEnabled workflowKeywordTriggerEnabled workflowSizeGuideline worktree worktree.baseRef worktree.bgIsolation worktree.sparsePaths worktree.symlinkDirectories wslInheritsWindowsSettings`.

Key entries:
- `permissions` — object with `allow`, `ask`, `deny`, `additionalDirectories`, `blockReadsOutsideWorkingDirectories`, `defaultMode`, `disableBypassPermissionsMode`. Rule syntax `Tool` or `Tool(specifier)`: `Bash`, `Bash(npm run *)`, `Read(./.env)`, `WebFetch(domain:example.com)`, `mcp__github__get_*`, `"*"`, `"mcp__*"`. Evaluation: `deny` → `ask` → `allow`, first match wins. `defaultMode`: `"default"` | `"acceptEdits"` | `"plan"` | `"auto"` | `"dontAsk"` | `"bypassPermissions"` | `"manual"` (`auto`/`bypassPermissions` only from user or managed settings). `disableBypassPermissionsMode: "disable"`. Per-session: `--allowedTools`, `--disallowedTools`, `--add-dir`, `--permission-mode`, `--dangerously-skip-permissions`.
  ```json
  { "permissions": { "allow": ["Bash(npm run *)"], "ask": ["Bash(git push *)"], "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Bash(curl *)"], "defaultMode": "acceptEdits", "additionalDirectories": ["../docs/"] } }
  ```
- `model` — alias or full ID, e.g. `{"model": "claude-sonnet-5"}`; overridden by `--model` and `ANTHROPIC_MODEL`; constrained by `availableModels`. Related: `fallbackModel`, `modelOverrides`, `modelPicker`, `modelSettings`, `effortLevel`, `maxEffortLevel`, `alwaysThinkingEnabled`, `promptCacheTtl`, `subagentPromptCacheTtl`, `outputStyle`, `ultracode`, `fastMode`, `advisorModel`.
- `env` — `{"env": {"DISABLE_AUTO_COMPACT": "1", "ANTHROPIC_BASE_URL": "https://proxy.example.com"}}`; overrides shell exports; project/local files can't set `CLAUDE_CONFIG_DIR`, `HOME`, `TMPDIR`, `XDG_*`, `OTEL_LOG_RAW_API_BODIES`, `CLAUDE_CODE_PROCESS_WRAPPER`, `CLAUDE_CODE_SYNC_SKILLS`, etc.
- `hooks` — event → matcher groups → handlers (see hooks.md below); related `disableAllHooks`, `allowManagedHooksOnly`, `allowedHttpHookUrls`, `httpHookAllowedEnvVars`.
- `sandbox` — see sandboxing.md below.
- Memory/context: `autoCompactEnabled`, `autoCompactWindow`, `autoMemoryDirectory`, `autoMemoryEnabled`, `bashOutputMaxChars`, `claudeMd`, `claudeMdExcludes`, `fileCheckpointingEnabled`, `plansDirectory`, `skillListingBudgetFraction`, `skillListingMaxDescChars`, `taskOutputMaxChars`.
- Plugins/MCP: `enabledPlugins`, `extraKnownMarketplaces`, `pluginConfigs`, `strictKnownMarketplaces`, `blockedMarketplaces`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers`, `managedMcpServers`, `allowManagedMcpServersOnly`, `allowAllClaudeAiMcps`.
- Auth/org: `apiKeyHelper`, `forceLoginMethod`, `forceLoginOrgUUID`, `forceLoginGatewayUrl`, `otelHeadersHelper`, `cleanupPeriodDays`, `companyAnnouncements`, `statusLine`, `attribution` (`commit`, `pr`, `sessionUrl`), `includeCoAuthoredBy`.

### hooks.md — https://code.claude.com/docs/en/hooks.md (guide: https://code.claude.com/docs/en/hooks-guide.md)
Locations: `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, managed settings, plugin `hooks/hooks.json`, skill frontmatter `hooks:`, subagent frontmatter `hooks:`. Shape:
```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "./scripts/check.sh", "timeout": 60 } ] } ] } }
```
Handler `type`: `"command"` (`command`, `args` for exec form, `async`, `asyncRewake`, `shell`: `bash`|`powershell`), `"http"` (`url`, `headers`, `allowedEnvVars`), `"mcp_tool"`, `"prompt"` (`prompt` with `$ARGUMENTS`, `model`, `timeout` default 30, `continueOnBlock`), `"agent"` (`prompt`, `timeout` default 60). Common fields: `type`, `if` (permission-rule filter, e.g. `"Bash(git *)"`, `"Edit(*.ts)"`), `timeout` (default 600 for command/http/mcp_tool; 30 on UserPromptSubmit), `statusMessage`, `once` (skill frontmatter only). Matcher: `"*"`/empty = all; plain names or `Edit|Write` / `Edit, Write` exact; anything else is an unanchored JS regex (`^Notebook`, `mcp__memory__.*`). Path placeholders: `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}`.

All hook events: `SessionStart` (matchers `startup`, `resume`, …; supports `CLAUDE_ENV_FILE` for persisting env vars), `Setup` (`init`, `maintenance`; only with `--init-only`/`--init`/`--maintenance`), `InstructionsLoaded` (matcher on `load_reason`: `session_start`, `path_glob_match`, `nested_traversal`, `include`), `UserPromptSubmit`, `UserPromptExpansion` (matches `command_name`), `MessageDisplay`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Notification` (`permission_prompt`, `idle_prompt`, …), `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure` (`error`: `rate_limit`, `overloaded`, `authentication_failed`, …), `TeammateIdle`, `ConfigChange` (`user_settings`, …), `CwdChanged`, `DirectoryAdded`, `FileChanged` (matcher = `|`-separated filenames to watch), `WorktreeCreate`, `WorktreeRemove`, `PreCompact` (`manual`, `auto`), `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `Elicitation`, `ElicitationResult`, `SessionEnd` (matcher on `reason`, e.g. `clear`).

Input JSON (stdin / POST body) common fields: `session_id`, `prompt_id`, `transcript_path`, `cwd`, `scratchpad_dir`, `permission_mode`, `effort.level`, `hook_event_name`; in subagents also `agent_id`, `agent_type`. Tool events add `tool_name`, `tool_input`, `tool_use_id` (PostToolUse adds `tool_response`; PermissionDenied adds `reason`; Stop/SubagentStop add `stop_hook_active`, `last_assistant_message`, `background_tasks`, `session_crons`; SubagentStop adds `agent_transcript_path`). Example:
```json
{ "session_id": "abc123", "prompt_id": "550e8400-...", "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl", "cwd": "/home/user/my-project", "scratchpad_dir": "/tmp/claude-1000/.../scratchpad", "permission_mode": "default", "hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": { "command": "npm test", "description": "Run test suite", "timeout": 120000, "run_in_background": false }, "tool_use_id": "toolu_01ABC123..." }
```
Output: exit 0 = success (stdout JSON parsed; plain stdout added as context only on UserPromptSubmit/UserPromptExpansion/SessionStart/PostModelSwitch); exit 2 = block (stderr is the reason); other codes = non-blocking error. Universal JSON fields: `continue` (false stops Claude), `stopReason`, `suppressOutput` (no-op), `systemMessage`, `terminalSequence`. Decision control: top-level `{"decision": "block", "reason": "..."}` for UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact, TaskCreated; PreToolUse: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"|"deny"|"ask"|"defer", "permissionDecisionReason": "...", "updatedInput": {...}, "additionalContext": "..."}}`; PermissionRequest: `hookSpecificOutput.decision.behavior` `allow`|`deny` (+ `updatedInput`, permission update entries); PermissionDenied: `hookSpecificOutput.retry: true`; PostToolUse: `updatedToolOutput`; SessionStart/SubagentStart/PostModelSwitch: `hookSpecificOutput.additionalContext` (SessionStart also `initialUserMessage`, `watchPaths`, `sessionTitle`, `reloadSkills`); PreModelSwitch: `permissionDecision` allow/deny/ask; WorktreeCreate: print path (or `hookSpecificOutput.worktreePath`); Elicitation/ElicitationResult: `action` accept/decline/cancel + `content`; MessageDisplay: `displayContent`. `additionalContext`/`systemMessage`/`initialUserMessage` capped at 10,000 chars. Prompt/agent hook response schema: `{"ok": true|false, "reason": "...", "impossible": true|false}`. Async: `"async": true` on command hooks. `/hooks` menu lists configured hooks; `--debug` for hook logs. Hooks also run inside subagents. `/goal` is a built-in prompt-based Stop hook.

### sub-agents.md — https://code.claude.com/docs/en/sub-agents.md
Locations (priority): managed settings (1) → `--agents '<json>'` CLI flag (2) → `.claude/agents/*.md` (3, scanned recursively, walked up to repo root) → `~/.claude/agents/*.md` (4) → plugin `agents/` (5, identifier `plugin:sub:name`). Files are watched live. Frontmatter (only `name` and `description` required): `name`, `description`, `tools`, `disallowedTools`, `model` (`sonnet`|`opus`|`haiku`|`fable`|full ID|`inherit`), `permissionMode` (`default`|`acceptEdits`|`auto`|`dontAsk`|`bypassPermissions`|`plan`|`manual`), `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory` (`user` → `~/.claude/agent-memory/<name>/`; `project` → `.claude/agent-memory/<name>/`; `local` → `.claude/agent-memory-local/<name>/`), `background`, `omitClaudeMd`, `effort` (`low`|`medium`|`high`|`xhigh`|`max`), `isolation: worktree`, `color`, `initialPrompt`, `experimental.cacheTtl` (`5m`|`1h`). Example:
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. ...
```
CLI form: `claude --agents '{"code-reviewer": {"description": "...", "prompt": "...", "tools": ["Read","Grep","Glob","Bash"], "model": "sonnet"}}'`. `--append-subagent-system-prompt[-file]` in `-p` mode. Frontmatter `Stop` hooks become `SubagentStop`. `CLAUDE_CODE_SUBAGENT_MODEL[_FORCE]` env vars. Built-in subagents include `general-purpose`, `Explore`, `Plan`. `claude plugin validate <dir>` checks agent frontmatter.

### skills.md — https://code.claude.com/docs/en/skills.md
Locations: `~/.claude/skills/<name>/SKILL.md` (personal), `.claude/skills/<name>/SKILL.md` (project; nested dirs allowed), `.claude/commands/*.md` (single-file), plugin `skills/<name>/SKILL.md` (`/plugin:name`), skills synced from claude.ai (`/anthropic-skills:name`), bundled skills (`/verify`, `/code-review`, `/simplify`, `/workflow-authoring`, `/deep-research`…). Command name = directory name (project/personal) or frontmatter `name` (plugins). Frontmatter (all optional; `description` recommended): `name`, `description` (with `when_to_use`, capped at 1,536 chars in the listing), `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`, `shell` (`bash`|`powershell`), `metadata`, `license`, `compatibility`. Outside Claude Code (claude.ai uploads, Skills API, `package_skill.py`) only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are allowed. Substitutions: `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`. Dynamic context injection: `` !`git diff HEAD` `` lines run before Claude reads the skill. Example:
```markdown
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```
Restrict via `permissions.deny: ["Skill"]` or `Skill(name)` rules; `/reload-skills`; evals with `skill-creator`.

### sandboxing.md — https://code.claude.com/docs/en/sandboxing.md
`/sandbox` panel (Mode: auto-allow vs regular permissions; Overrides; Config) writes to `.claude/settings.local.json`. macOS Seatbelt; Linux/WSL2 need `bubblewrap` + `socat`; no native Windows. One-session: `claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'`. Config:
```json
{ "sandbox": { "enabled": true, "autoAllowBashIfSandboxed": true, "failIfUnavailable": false, "allowUnsandboxedCommands": true, "excludedCommands": ["docker *"],
  "filesystem": { "allowWrite": ["/tmp/build", "~/.kube"], "denyWrite": [], "denyRead": ["~/.aws/credentials"], "allowRead": ["."], "allowManagedReadPathsOnly": false, "disabled": false },
  "network": { "allowedDomains": ["github.com", "*.npmjs.org", "api.example.com:443"], "deniedDomains": ["uploads.github.com"], "allowLocalBinding": true, "allowUnixSockets": [], "allowAllUnixSockets": false, "strictAllowlist": false, "allowManagedDomainsOnly": false, "httpProxyPort": 0, "socksProxyPort": 0, "tlsTerminate": false },
  "credentials": { "files": [], "envVars": [], "awsPairs": [], "sigv4": [], "allowPlaintextInject": false },
  "ignoreViolations": {}, "enableWeakerNestedSandbox": false, "enableWeakerNetworkIsolation": false, "allowAppleEvents": false, "ripgrep": "", "bwrapPath": "", "socatPath": "" } }
```
Path prefixes: `/` absolute, `~/` home, `./` or bare = project root (project settings) or `~/.claude` (user settings). Defaults: write to cwd, session `$TMPDIR`, and `--add-dir`/`permissions.additionalDirectories`; read everything except protected paths (`.claude/*` settings, skills, agents, commands, hooks, `.mcp.json`, shell rc files, `~/.claude.json`, `.credentials.json`). Network prompts on first new domain; `WebFetch(domain:...)` allow rules feed the allowlist; auto mode uses per-command allowed domains. Managed enforcement: `{"sandbox": {"enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false}}` plus `allowManagedReadPathsOnly`, `allowManagedDomainsOnly`. Escape hatch: `dangerouslyDisableSandbox` tool parameter. Standalone equivalent: `@anthropic-ai/sandbox-runtime` (https://code.claude.com/docs/en/sandbox-environments.md).

### auto-mode-config.md — https://code.claude.com/docs/en/auto-mode-config.md
Auto mode = `--permission-mode auto` / `permissions.defaultMode: "auto"`; a classifier reviews tool calls after `deny`/`ask` rules. `autoMode` block is read only from `~/.claude/settings.json`, managed settings, or `--settings` (not project files):
```json
{ "autoMode": {
  "environment": ["$defaults", "Source control: github.example.com/acme-corp and all repos under it", "Trusted cloud buckets: s3://acme-build-artifacts", "Trusted internal domains: *.corp.example.com", "Key internal services: Jenkins at ci.example.com"],
  "allow": ["$defaults", "Deploying to the staging namespace is allowed"],
  "soft_deny": ["$defaults", "Never run database migrations outside the migrations CLI"],
  "hard_deny": ["$defaults", "Never send repository contents to third-party code-review APIs"],
  "classifyAllShell": true } }
```
Precedence inside the classifier: `hard_deny` → `soft_deny` → `allow` → explicit user intent. `"$defaults"` splices built-in rules; omitting it replaces the list. Human checkpoints: `permissions.ask: ["Bash(git push *)", "Bash(gh pr create *)"]`. Commands: `claude auto-mode defaults`, `claude auto-mode config`, `/auto-mode-setup`, `/permissions` → Auto mode tab. Related settings: `disableAutoMode`, `useAutoModeDuringPlan`, `skipAutoPermissionPrompt`; env `CLAUDE_CODE_AUTO_MODE_SERVER=0`.

### agent-teams.md — https://code.claude.com/docs/en/agent-teams.md
Experimental; enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (shell or `{"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}`). Lead session spawns teammates (full Claude Code sessions) via the Agent tool with a `name`; shared task list; mailbox at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`; config `~/.claude/teams/{team-name}/config.json`; tasks `~/.claude/tasks/{team-name}/`; team name `session-<first 8 chars of session id>`. Display modes: in-process (agent panel; arrows/Enter/Esc, `x` to stop, Ctrl+T task list) or split-pane (tmux/iTerm2). Model selection order: spawn prompt → subagent definition `model` → `CLAUDE_CODE_SUBAGENT_MODEL` → lead's model (`teammateDefaultModel` removed in v2.1.234). Subagent definitions can be used as teammate roles (`tools`, `model`, body applied; `skills` not). Quality gates via `TeammateIdle`, `TaskCreated`, `TaskCompleted` hooks (exit 2 blocks). Not available in `-p`/SDK sessions. Limitations: no resume of in-process teammates, one team per session, no nested teams, lead is fixed.

### workflows.md — https://code.claude.com/docs/en/workflows.md
Dynamic workflows = JavaScript scripts Claude writes to orchestrate many subagents. Trigger with the keyword `ultracode` in a prompt (or "use a workflow"), `/effort ultracode`, or a saved command; bundled `/deep-research <question>`. Manage with `/workflows` (keys: `p` pause, `x` stop, `r` restart, `s` save, `f` filter). Save to `.claude/workflows/<name>.js` (project) or `~/.claude/workflows/` (personal); plugins ship `workflows/` (`/plugin:name`). Script shape:
```javascript
export const meta = { name: 'audit-routes', description: 'Audit every route handler for missing auth checks' }
const found = await agent('List every .ts file under src/routes/.', { schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } } })
const audits = await pipeline(found.files, file => agent(`Audit ${file} for missing authentication checks.`, { label: file }))
return audits.filter(Boolean)
```
API: `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`, global `args`; `Date.now()`/`Math.random()` throw (determinism for resume). Limits: 16 concurrent agents default (`CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` 1–256), 4,096 items per `parallel`/`pipeline`, 1,000 agents per run, no `import()`, no mid-run input. Settings: `enableWorkflows`, `disableWorkflows`, `workflowKeywordTriggerEnabled`, `workflowSizeGuideline`, `subagentPromptCacheTtl`, `MAX_STRUCTURED_OUTPUT_RETRIES`. Authoring reference: `/workflow-authoring` skill.

### headless.md — https://code.claude.com/docs/en/headless.md
- `claude -p "<prompt>"` (`--print`); `--bare` skips hooks/skills/plugins/MCP/CLAUDE.md/auto-memory (needs `ANTHROPIC_API_KEY` or `apiKeyHelper`); load context with `--append-system-prompt`, `--append-system-prompt-file`, `--system-prompt`, `--settings <file-or-json>`, `--mcp-config <file-or-json>`, `--strict-mcp-config`, `--agents <json>`, `--plugin-dir <path>`, `--plugin-url <url>`, `--add-dir`.
- Output: `--output-format text|json|stream-json`; `json` returns `result`, `session_id`, `total_cost_usd`, usage; `--json-schema '<schema>'` puts validated output in `structured_output`; `stream-json` needs `--verbose` (+ `--include-partial-messages` for token deltas; `--forward-subagent-text`); events: `system/init` (`model`, `tools`, `mcp_servers`, `mcp_server_errors`, `plugins`, `plugin_errors`, `capabilities`), `system/api_retry`, `system/plugin_install`, `assistant`/`user` (with `parent_tool_use_id`), `stream_event`, `result` (with `permission_denials`).
- Permissions: `--allowedTools "Bash,Read,Edit"` / `"Bash(git diff *),Bash(git commit *)"`, `--disallowedTools`, `--permission-mode auto|acceptEdits|dontAsk|plan|default`, `--dangerously-skip-permissions`, `--permission-prompts none`, `--permission-prompt-tool`.
- Sessions: `--continue`, `--resume <session_id | /path/to/transcript.jsonl>`, `--no-session-persistence`; `session_id=$(claude -p "Start" --output-format json | jq -r '.session_id')`.
- Misc: stdin piping (10 MB cap), exit codes (0 ok, non-zero fail, 143 on SIGTERM), `--init-only`/`--init`/`--maintenance` fire `Setup` hooks, slash commands in prompt strings (`/model sonnet`, `/config key=value`), `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`.

### best-practices.md — https://code.claude.com/docs/en/best-practices.md
Core themes: give Claude a verification loop (tests, build, screenshots; `/verify`, `/goal`, Stop hooks, review subagents); explore → plan → code (plan mode); specific prompts with rich context; CLAUDE.md under control (`/init`, `/context`, include/exclude table, emphasis with "IMPORTANT"); permissions (`/permissions`, `/sandbox`, auto mode default on Pro/Max/Team); CLI tools (`gh`, `aws`, `gcloud`, `sentry-cli`); MCP (`claude mcp add --transport http notion https://mcp.notion.com/mcp`); hooks for must-happen actions; skills (`.claude/skills/<name>/SKILL.md`, `disable-model-invocation: true`, `$ARGUMENTS`); subagents (`.claude/agents/*.md`); plugins (`/plugin`); session management (`/clear`, `/compact`, `/rewind`, `--resume`); automation (`claude -p`, `--output-format json|stream-json --verbose`, fan-out loops with `--allowedTools`, `/batch`, `claude --permission-mode auto -p`, adversarial review with `/code-review`); failure patterns (kitchen-sink session, repeated corrections, over-specified CLAUDE.md, trust-then-verify gap, infinite exploration).

### plugins.md — https://code.claude.com/docs/en/plugins.md (reference: https://code.claude.com/docs/en/plugins-reference.md; marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md)
Manifest `.claude-plugin/plugin.json`: `{"name": "my-first-plugin", "description": "...", "version": "1.0.0", "author": {"name": "Your Name"}}` (+ `homepage`, `repository`, `license`, component path fields). Layout (all at plugin root, never inside `.claude-plugin/`): `skills/<name>/SKILL.md`, `commands/*.md`, `agents/*.md`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `monitors/monitors.json`, `bin/`, `settings.json` (only `agent` and `subagentStatusLine`), `workflows/*.js`; single-skill plugins may place `SKILL.md` at the root. Test with `claude --plugin-dir ./my-first-plugin`; skills are namespaced `/my-first-plugin:hello`; `/reload-plugins`; scaffold with `claude plugin init my-tool` (creates `~/.claude/skills/my-tool/`, loads as `my-tool@skills-dir`); `claude plugin validate`, `claude plugin install`; install marketplaces with `/plugin marketplace add <owner/repo>` and `/plugin install <name>@<marketplace>`. Env in plugin hooks/skills: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}`, `$CLAUDE_PLUGIN_OPTION_<KEY>`. Settings: `enabledPlugins`, `extraKnownMarketplaces`, `pluginConfigs`, `strictKnownMarketplaces`, `blockedMarketplaces`, `strictPluginOnlyCustomization`.

### mcp.md — https://code.claude.com/docs/en/mcp.md (quickstart: https://code.claude.com/docs/en/mcp-quickstart.md)
Commands:
```bash
claude mcp add --transport http <name> <url> [--header "Authorization: Bearer token"] [--scope local|project|user]
claude mcp add --transport sse <name> <url>            # deprecated transport
claude mcp add [--env KEY=value] --transport stdio <name> -- <command> [args...]
claude mcp add-json <name> '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'
claude mcp add-json local '{"type":"stdio","command":"/path/to/cli","args":["--api-key","abc"],"env":{"CACHE_DIR":"/tmp"}}'
claude mcp add-json events '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{...}}'
claude mcp list | claude mcp get <name> | claude mcp remove <name> | claude mcp reset-project-choices
claude mcp serve                                        # expose Claude Code as a stdio MCP server
/mcp                                                    # in-session status
```
Scopes: local (default, `~/.claude.json` under the project path), project (`.mcp.json` at repo root, committed; approval prompt in interactive sessions), user (`~/.claude.json`); precedence local → project → user → plugin → claude.ai connectors; `managedMcpServers` ranks above all. `.mcp.json` shape:
```json
{ "mcpServers": { "shared-server": { "type": "http", "url": "${API_BASE_URL:-https://api.example.com}/mcp", "headers": { "Authorization": "Bearer ${API_KEY}" }, "alwaysLoad": true },
                  "local": { "type": "stdio", "command": "npx", "args": ["-y", "@example/mcp-server"], "env": {} } } }
```
`type` is required for `url` entries (`http`, `streamable-http` alias, `sse`, `ws`); `${VAR}` / `${VAR:-default}` expansion in `command`, `args`, `env`, `url`, `headers` (credential names like `ANTHROPIC_API_KEY` read as empty); `headersHelper` for dynamic headers; `oauth` block (`clientId`, `callbackPort`) with `--client-secret`; `CLAUDE_PROJECT_DIR` is set for stdio servers. Tool search: `ENABLE_TOOL_SEARCH` (`true`|`auto`|`auto:N`|`false`), `alwaysLoad`, tool `_meta` `"anthropic/alwaysLoad": true`, deny `ToolSearch` via permissions; output limit env `MAX_MCP_OUTPUT_TOKENS`; `--mcp-config`, `--strict-mcp-config`, `MCP_TIMEOUT`; settings `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers`, `managedMcpServers`. Claude Desktop config for `claude mcp serve`: `{"mcpServers": {"claude-code": {"type": "stdio", "command": "claude", "args": ["mcp", "serve"], "env": {}}}}`.

### .claude directory reference — https://code.claude.com/docs/en/claude-directory.md
| File | Scope | Purpose |
|---|---|---|
| `CLAUDE.md` | project + `~/.claude/` | instructions every session |
| `rules/*.md` | project + global | topic rules, optional `paths:` |
| `settings.json` | project + global | permissions, hooks, env, model |
| `settings.local.json` | project | personal overrides (gitignored) |
| `.mcp.json` | project root | team MCP servers |
| `.worktreeinclude` | project root | gitignored files to copy into worktrees |
| `skills/<name>/SKILL.md`, `commands/*.md` | project + global | skills / single-file prompts |
| `output-styles/*.md` | project + global | output styles |
| `agents/*.md` | project + global | subagents |
| `workflows/*.js` | project + global | dynamic workflows |
| `agent-memory/<name>/` | project + global | subagent memory |
| `~/.claude.json` | global | app state, OAuth, personal MCP servers |
| `~/.claude/projects/<project>/memory/` | global | auto memory |
| `~/.claude/keybindings.json`, `~/.claude/themes/*.json` | global | shortcuts, themes |
