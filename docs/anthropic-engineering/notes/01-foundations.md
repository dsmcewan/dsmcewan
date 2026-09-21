# Research notes — Anthropic Engineering blog, Batch A (foundations)

Compiled 2026-09-21. Sources: WebSearch snippets that quote the articles verbatim, the locally cloned `anthropics/claude-cookbooks` repo (shallow clone, HEAD 2026-09-21), `code.claude.com` / `platform.claude.com` docs, `swe-bench/experiments` and `SWE-agent/SWE-agent` GitHub files, plus prior knowledge. anthropic.com, web.archive.org and most third-party mirrors (medium, simonwillison.net, dev.to, substack, datacamp, learnprompting, the-decoder, infoq, gist, github.io pages, translate.goog…) are blocked by the egress proxy, so the article bodies could not be re-read directly. Anything not confirmed by a search snippet, a doc page, or a repo file is marked **(from memory, unverified)**.

Verification legend used below:
- ✅ = confirmed online this session (search snippet quoting the article, doc page, or repo file)
- 🟡 = partially confirmed (structure/number confirmed, exact wording from memory)
- ❓ = (from memory, unverified)

URL-canonicalisation facts confirmed this session:
- `anthropic.com/news/<slug>` and `anthropic.com/research/<slug>` → now `anthropic.com/engineering/<slug>` for all five posts (search results list both old and new paths). ✅
- `github.com/anthropics/anthropic-cookbook` → renamed `github.com/anthropics/claude-cookbooks` (the old URL still redirects; clone of the new name succeeded). ✅
- Contextual-embeddings cookbook moved from `skills/contextual-embeddings/guide.ipynb` → `capabilities/contextual-embeddings/guide.ipynb` (there is no `skills/contextual-embeddings` directory in the current repo; `skills/` now holds the Agent Skills cookbook). ✅ It is also published as a page at `https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide`. ✅
- `patterns/agents/` still exists in `claude-cookbooks` with `README.md`, `basic_workflows.ipynb`, `evaluator_optimizer.ipynb`, `orchestrator_workers.ipynb`, `async_multi_agent_orchestration.ipynb` (new), `util.py`, `prompts/{citations_agent,research_lead_agent,research_subagent}.md` (new, from the multi-agent research post). ✅
- `docs.anthropic.com/en/docs/...` → `platform.claude.com/docs/en/...` (API docs) and `docs.anthropic.com/en/docs/claude-code/...` → `code.claude.com/docs/en/...` (Claude Code docs). ✅ (both new hosts fetched successfully; old host is blocked here so the redirect itself could not be observed).

---

## 1. Introducing Contextual Retrieval

- **Title:** Introducing Contextual Retrieval
- **URL:** https://www.anthropic.com/engineering/contextual-retrieval (original: https://www.anthropic.com/news/contextual-retrieval — the cookbook still links to the `/news/` URL ✅)
- **Date:** 19 September 2024 ✅ (search results: "September 2024")
- **Authors:** No individual byline on the post ❓ (from memory, unverified — published as an Anthropic team post)

### Thesis (one paragraph)
Traditional RAG chunks documents, embeds the chunks and retrieves by similarity, but chunking strips away the context that makes a chunk findable ("The company's revenue grew by 3% over the previous quarter" — which company? which quarter?). Contextual Retrieval fixes this at pre-processing time by asking Claude to write a short (50–100 token) chunk-specific context that situates each chunk within its whole document, and prepending that context to the chunk before both embedding it ("Contextual Embeddings") and indexing it for BM25 ("Contextual BM25"). Across nine datasets, this cut top-20 retrieval failures by 35% (embeddings alone), 49% (embeddings + BM25) and 67% when a reranker is added; with prompt caching the one-off cost is ~$1.02 per million document tokens. ✅

### Every concept, method, principle, number
- **RAG background** ✅: knowledge base split into chunks "usually no more than a few hundred tokens"; embedded; stored in a vector DB; at query time find chunks by semantic similarity and add them to the prompt.
- **Semantic-embedding weakness / BM25 complement** ✅: embeddings can miss exact lexical matches (error codes, identifiers); BM25 (Best Matching 25) builds on TF-IDF and is good for exact matches; "hybrid search" = embeddings + BM25 with rank fusion (Reciprocal Rank Fusion is named). Example ❓ (memory): a query for "Error code TS-999" — embeddings find generic error-code content, BM25 finds the exact string.
- **A note on simply using a longer prompt** ✅: if the knowledge base is < 200,000 tokens (~500 pages), skip RAG and put the whole knowledge base in the prompt; prompt caching (released a few weeks earlier) makes this cheap — "reducing latency by > 2x and costs by up to 90%". Link: https://www.anthropic.com/news/prompt-caching ✅ (docs now https://platform.claude.com/docs/en/build-with-claude/prompt-caching).
- **The context conundrum in traditional RAG** ✅: SEC filing example; original chunk "The company's revenue grew by 3% over the previous quarter."; contextualized chunk "This chunk is from an SEC filing on ACME corp's performance in Q2 2023; the previous quarter's revenue was $314 million. The company's revenue grew by 3% over the previous quarter."
- **Contextual Retrieval = two sub-techniques** ✅: **Contextual Embeddings** and **Contextual BM25**. Context is prepended "before embedding it and before creating the BM25 index".
- **Other prior approaches noted (and why they fall short)** 🟡: adding generic document summaries to chunks, hypothetical document embedding (HyDE), summary-based indexing — "yield low gains". (list from memory; the cookbook independently contrasts HyDE.)
- **Implementing Contextual Retrieval** ✅: use Claude (Claude 3 Haiku in the experiments) with the prompt below; output is "usually 50-100 tokens"; one pass over the whole corpus at ingestion time.
- **Cost** ✅: "Assuming 800 token chunks, 8k token documents, 50 token context instructions, and 100 tokens of context per chunk, the one-time cost to generate contextualized chunks is $1.02 per million document tokens." Prompt caching is what makes it cheap: load the document into cache once, reference it for every chunk.
- **Methodology** ✅: experiments across "various knowledge domains (codebases, fiction, ArXiv papers, Science Papers), embedding models, retrieval strategies, and evaluation metrics"; metric = "1 minus recall@20" (fraction of relevant docs NOT in the top 20); headline chart uses "the top-performing embedding configuration (Gemini Text 004)" and top-20 chunks; all embedding providers tested gained; "Gemini and Voyage embeddings to be particularly effective" (footnote: OpenAI, Cohere and others also tested ✅).
- **Results** ✅:
  - Contextual Embeddings: top-20 failure rate 5.7% → 3.7% (−35%).
  - Contextual Embeddings + Contextual BM25: 5.7% → 2.9% (−49%).
  - Reranked Contextual Embeddings + Contextual BM25: 5.7% → 1.9% (−67%).
  - "Embeddings+BM25 is better than embeddings on their own"; "adding context to chunks improves retrieval accuracy" ✅.
- **Implementation considerations** ✅ (section explicitly lists):
  1. *Chunk boundaries* — chunk size, boundary and overlap affect results.
  2. *Embedding model* — all improve; Gemini and Voyage best.
  3. *Custom contextualizer prompts* — the generic prompt works, but tailor it (e.g. include a glossary of key terms).
  4. *Number of chunks* — "passing the top-20 chunks to the model is more effective than just the top-10 or top-5" (they tried 5, 10, 20).
  5. *Always run evals* — "Response generation may be improved by passing it the contextualized chunk" ✅/🟡 exact wording from memory.
- **Reranking** ✅: pipeline = initial retrieval of top-N candidates (they used top-150) → pass N chunks + query to a reranking model → score and keep top-K (they used top-20) → generate. They "ran our tests with the Cohere reranker"; "Voyage also offers a reranker, though we did not have time to test it". Reranking "inevitably adds a small amount of latency, even though the reranker scores all the chunks in parallel"; trade-off between more chunks (accuracy) vs fewer (latency/cost); "recommend experimenting".
- **Conclusion / stack of techniques** ✅: Embeddings + BM25 > embeddings alone; Voyage and Gemini best embeddings; top-20 > top-10 > top-5; contextualizing chunks helps; reranking helps; combine all for max gains.
- **Cookbook note** ✅: "We also provide a cookbook…" (link below).

### Concrete prompts / code / config
Contextualizer prompt (verbatim in article and cookbook) ✅:
```
<document>
{{WHOLE_DOCUMENT}}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{{CHUNK_CONTENT}}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
```
Cookbook implementation details (`capabilities/contextual-embeddings/guide.ipynb`, read locally) ✅:
- `DOCUMENT_CONTEXT_PROMPT = "<document>\n{doc_content}\n</document>"` with `"cache_control": {"type": "ephemeral"}` on that block; `CHUNK_CONTEXT_PROMPT` as above; `messages.create(model=MODEL_NAME, max_tokens=1024/1000, temperature=0.0, ...)`; current notebook uses `MODEL_NAME = "claude-haiku-4-5"` (original used Claude 3 Haiku ❓/🟡).
- Dataset: 9 codebases pre-chunked, 737 chunks, 248 evaluation queries each with a "golden chunk" (`data/codebase_chunks.json`, `data/evaluation_set.jsonl`); metric Pass@k.
- Embeddings: Voyage AI `voyage-2` (batch 128); vector store = in-memory pickle; BM25 = Elasticsearch (`docker run … elasticsearch:9.2.0`, `english` analyzer, BM25 similarity, indexes both `content` and `contextualized_content`); hybrid = top-150 from each side → weighted Reciprocal Rank Fusion (semantic 0.8 / BM25 0.2 default); reranker = Cohere `rerank-english-v3.0` over 10× over-retrieved candidates.
- Results table (cookbook): Baseline RAG Pass@5/10/20 = 80.92 / 87.15 / 90.06%; + Contextual Embeddings = 88.12 / 92.34 / 94.29%; + Contextual BM25 hybrid = 86.43 / 93.21 / 94.99%; + Reranking = 92.15 / 95.26 / 97.45%.
- Caching stats: 61.83% of input tokens read from cache (2.27M tokens at 90% discount) → cost ~$9.20 → ~$2.85 (69% saving); "processing documents sequentially (rather than randomly shuffling chunks) is crucial for maximizing cache efficiency"; cache TTL 5 min.
- Also ships `contextual-rag-lambda-function/` (`lambda_function.py`, `inference_adapter.py`, `s3_adapter.py`) — an AWS Lambda usable as a custom chunking step for a Bedrock Knowledge Base; plus `evaluation/` with Promptfoo scripts (per README).
- Env vars: `VOYAGE_API_KEY`, `ANTHROPIC_API_KEY`, `COHERE_API_KEY`.

### Hyperlinks in / around the article
| Reference | URL | Status |
|---|---|---|
| Article (canonical) | https://www.anthropic.com/engineering/contextual-retrieval | blocked here; confirmed by search |
| Article (original) | https://www.anthropic.com/news/contextual-retrieval | old path ✅ |
| Prompt caching announcement | https://www.anthropic.com/news/prompt-caching | ✅ (search) |
| Prompt caching docs | https://platform.claude.com/docs/en/build-with-claude/prompt-caching (was docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | canonical ✅ |
| Cookbook (as linked in 2024) | https://github.com/anthropics/anthropic-cookbook/tree/main/skills/contextual-embeddings | moved |
| Cookbook (current) | https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/contextual-embeddings/guide.ipynb | ✅ exists locally |
| Cookbook (rendered) | https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide | ✅ fetched |
| Basic RAG cookbook (linked from the guide) | https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/retrieval_augmented_generation/guide.ipynb | ✅ dir exists locally |
| BM25 explainer (linked from cookbook) | https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables | ✅ in notebook |
| Bedrock Knowledge Base docs (cookbook) | https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html | ✅ in notebook |
| Voyage AI / Cohere | https://www.voyageai.com/ , https://cohere.com/ | ✅ in notebook |
| Gemini text-embedding-004 | (named "Gemini Text 004" in the article) | ✅ search |

### Implementation checklist
1. Decide whether you need retrieval at all: if the corpus is < ~200k tokens (~500 pages), put it in the prompt and use prompt caching.
2. Chunk the corpus (article assumes ~800-token chunks; experiment with boundaries/overlap).
3. For each document, load the full document into a cached prompt block; for each chunk call Claude (Haiku-class) with the contextualizer prompt, temperature 0, ~100-token output; process chunks document-by-document so cache hits are maximised.
4. Prepend the generated context to the chunk text → "contextualized chunk".
5. Embed contextualized chunks with a strong embedding model (Voyage or Gemini performed best) and store in your vector DB.
6. Build a BM25 index over the contextualized chunks as well (Elasticsearch or equivalent).
7. At query time retrieve top-150 from both indexes, fuse with rank fusion (RRF; cookbook default 80/20), dedupe.
8. Optionally rerank the ~150 candidates with a reranker (Cohere `rerank-english-v3.0` tested; Voyage also offers one) and keep top-20.
9. Pass the top-20 chunks (more effective than top-10/5) to Claude for generation; consider passing the contextualized version.
10. Build an eval set (queries → golden chunks), measure recall@20 / Pass@k for each stage, and tune chunk size, contextualizer prompt (domain glossary), k, fusion weights, and reranker depth against latency/cost.

### Dependencies
- Builds on: Prompt caching (Aug 2024 news post); the earlier RAG cookbook guide.
- Built on by: *Building effective agents* (the "augmented LLM" retrieval block); later engineering posts on context engineering (Sept 2025) refer back to retrieval strategies; the platform cookbook page is the living version. The think-tool / SWE-bench / Claude Code posts do not depend on it.

---

## 2. Building effective agents

- **Title:** Building effective agents
- **URL:** https://www.anthropic.com/engineering/building-effective-agents (originals: https://www.anthropic.com/research/building-effective-agents and https://www.anthropic.com/news/building-effective-agents — all three appear in search results ✅; the cookbook README links the `/research/` URL ✅)
- **Date:** 19 December 2024 ✅
- **Authors:** Erik Schluntz and Barry Zhang ✅ (cookbook README: "by Erik Schluntz and Barry Zhang"). Acknowledgements ❓ (memory): "Written by Erik Schluntz and Barry Zhang. This work draws upon our experiences building agents at Anthropic and the valuable insights shared by our customers, for which we're deeply grateful."

### Thesis
After a year working with dozens of teams building LLM agents, Anthropic found that the most successful implementations use simple, composable patterns rather than complex frameworks or libraries. The post defines "agentic systems" as a spectrum from **workflows** (LLMs and tools orchestrated through predefined code paths) to **agents** (LLMs dynamically directing their own process and tool use), catalogues five workflow patterns plus the autonomous agent, gives guidance on when each is worth its cost/latency, and closes with three principles — simplicity, transparency, and a carefully engineered agent-computer interface (ACI). ✅

### Every concept, pattern, principle, recommendation
- **What are agents?** ✅ "agentic systems" as the umbrella; **Workflows** = "systems where LLMs and tools are orchestrated through predefined code paths"; **Agents** = "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- **When (and when not) to use agents** ✅: "find the simplest solution possible, and only increase complexity when needed"; agentic systems "trade latency and cost for better task performance"; single optimized LLM calls with retrieval and in-context examples are usually enough; workflows for predictability and consistency on well-defined tasks; agents for flexibility and model-driven decision-making at scale.
- **When and how to use frameworks** ✅: named — LangGraph (LangChain), Amazon Bedrock's AI Agent framework, Rivet (drag-and-drop GUI LLM workflow builder), Vellum (GUI tool for building/testing complex workflows). They simplify low-level tasks (calling LLMs, defining/parsing tools, chaining) but "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug" and tempt over-complexity. Recommendation: "start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code." Link to the Anthropic cookbook sample implementations.
- **Building block: the augmented LLM** ✅: an LLM enhanced with **retrieval, tools, and memory**; the model can actively generate search queries, select tools, and decide what to retain. Two focus points ❓/🟡: tailor augmentations to the use case; expose them through a well-documented interface. Mentions the **Model Context Protocol (MCP)** as a simple way to integrate with a growing ecosystem of third-party tools ✅ (search).
- **Workflow: Prompt chaining** ✅: sequence of LLM calls, each processing the previous output; optional programmatic "gate" checks between steps. Use when the task decomposes cleanly into fixed subtasks (trade latency for accuracy). Examples ❓: generate marketing copy → translate; write outline → check criteria → write document.
- **Workflow: Routing** ✅: classify input and dispatch to a specialised prompt/path; separation of concerns. Examples ✅: different customer-service query types (general/refund/technical) → different processes/prompts/tools; easy/common questions → smaller cheaper model (Haiku), hard/unusual → more capable model (Sonnet).
- **Workflow: Parallelization** ✅: two variants — **Sectioning** (independent subtasks in parallel) and **Voting** (same task run multiple times for diverse outputs). Examples ❓/🟡: guardrails (one instance answers while another screens for inappropriate content); automated evals with each call scoring a different aspect; voting on code vulnerabilities; voting on content appropriateness with tuned thresholds.
- **Workflow: Orchestrator-workers** ✅: central LLM dynamically decomposes the task, delegates to workers, synthesises results; differs from parallelization because subtasks are not predefined. Examples ❓/🟡: coding products making complex changes to multiple files; search tasks gathering/analysing information from multiple sources.
- **Workflow: Evaluator-optimizer** ✅: one LLM generates, another evaluates and gives feedback in a loop; good when there are clear evaluation criteria and iterative refinement adds measurable value (analogy: a human writer's iterative editing). Examples ❓/🟡: literary translation with nuance critique; complex multi-round search where the evaluator decides whether more searching is needed.
- **Agents** ✅/🟡: emerging as models gain "understanding complex inputs, engaging in reasoning and planning, using tools reliably, and recovering from errors"; agents "begin their work with either a command from, or interactive discussion with, the human user", then "plan and operate independently, potentially returning to the human for further information or judgement"; must obtain "ground truth" from the environment at each step (tool results, code execution); can pause for human feedback at checkpoints or blockers; tasks end at completion or via stopping conditions (e.g. max iterations). "Implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop." Use for open-ended problems where steps can't be predicted; higher cost and potential for compounding errors → "extensive testing in sandboxed environments, along with the appropriate guardrails". Examples ✅: a coding agent resolving SWE-bench tasks ("edits to many files based on a task description"); Anthropic's computer-use reference implementation.
- **Combining and customizing** 🟡: patterns are composable building blocks, not prescriptions; "measure performance and iterate"; add complexity only when it demonstrably improves outcomes.
- **Summary / core principles** ✅: "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs." Three principles: (1) "Maintain simplicity in your agent's design"; (2) "Prioritize transparency by explicitly showing the agent's planning steps"; (3) "Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."
- **Appendix 1: Agents in practice** ✅ — *Customer support*: chatbot flow + tools (pull customer data, order history, knowledge base articles), programmatic actions (issue refunds, update tickets), success "clearly measured through user-defined resolutions"; companies have shown viability with "usage-based pricing models that charge only for successful resolutions". *Coding agents*: "Code solutions are verifiable through automated tests; Agents can iterate on solutions using test results as feedback; The problem space is well-defined and structured; Output quality can be measured objectively"; "In our own implementation, agents can now solve real GitHub issues in the SWE-bench Verified benchmark based on the pull request description alone" (human review still needed for broader requirements).
- **Appendix 2: Prompt engineering your tools** ✅: tools deserve "just as much prompt engineering attention as your overall prompts". Format choices (diff vs. rewrite whole file; markdown vs. JSON) matter: "Give the model enough tokens to 'think' before it writes itself into a corner"; "Keep the format close to what the model has seen naturally occurring in text on the internet"; "Make sure there's no formatting 'overhead' such as having to keep an accurate count of thousands of lines of code, or string-escaping any code it writes." Rule of thumb: invest in the ACI as much as in HCI. Advice: "Put yourself in the model's shoes… A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools"; use obvious parameter names/descriptions ("like writing a great docstring for a junior developer"); test with many example inputs and iterate; **"Poka-yoke your tools. Change the arguments so that it is harder to make mistakes"** — the SWE-bench agent made mistakes with relative file paths after `cd`, so the tool was changed to require absolute paths and "the model used this method flawlessly"; "we actually spent more time optimizing our tools than the overall prompt" while building the SWE-bench agent ✅.

### Concrete code / prompts (from the cookbook `patterns/agents`, read locally) ✅
- `util.py`: `llm_call(prompt, system_prompt="", model="claude-sonnet-4-6")` (temperature 0.1, max_tokens 4096) and `extract_xml(text, tag)`.
- `basic_workflows.ipynb`: `chain(input, prompts)`, `parallel(prompt, inputs, n_workers=3)` (ThreadPoolExecutor), `route(input, routes)` with a `<reasoning>/<selection>` classifier prompt; examples: 4-step data-cleaning chain, stakeholder impact analysis in parallel, support-ticket routing (billing/technical/account/product).
- `evaluator_optimizer.ipynb`: `generate()` returning `<thoughts>/<response>`, `evaluate()` returning `<evaluation>PASS|NEEDS_IMPROVEMENT|FAIL</evaluation><feedback>`, `loop()` until PASS; example task: O(1) min-stack.
- `orchestrator_workers.ipynb`: `FlexibleOrchestrator` with `ORCHESTRATOR_PROMPT` producing `<analysis>` + `<tasks><task><type/><description/></task></tasks>` and `WORKER_PROMPT`; marketing-copy variations example; notes on N+1 calls, parallelising with asyncio, Opus orchestrator + Haiku workers.
- `async_multi_agent_orchestration.ipynb` and `prompts/*.md` were added later (multi-agent research system).

### Hyperlinks
| Reference | URL | Status |
|---|---|---|
| Article | https://www.anthropic.com/engineering/building-effective-agents | ✅ (search) |
| Cookbook README | https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/README.md (was anthropic-cookbook/…) | ✅ fetched |
| Notebooks | …/patterns/agents/basic_workflows.ipynb, evaluator_optimizer.ipynb, orchestrator_workers.ipynb | ✅ local |
| Model Context Protocol | https://modelcontextprotocol.io/ (article links the MCP intro: https://www.anthropic.com/news/model-context-protocol ❓) | 🟡 |
| SWE-bench Verified | https://www.swebench.com/ ; OpenAI's introduction https://openai.com/index/introducing-swe-bench-verified/ ❓ | 🟡 |
| Computer-use reference implementation | https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo ❓ | 🟡 |
| SWE-bench Sonnet post (Anthropic's own agent) | https://www.anthropic.com/engineering/swe-bench-sonnet | ✅ |
| Frameworks named | LangGraph (https://langchain-ai.github.io/langgraph/), Amazon Bedrock Agents, Rivet (https://rivet.ironcladapp.com/), Vellum (https://www.vellum.ai/) | names ✅, URLs ❓ |
| Poka-yoke | https://en.wikipedia.org/wiki/Poka-yoke | ✅ (search) |
| Video companions (later) | "Building more effective agents" https://www.youtube.com/watch?v=uhJJgc-0iTQ ; Barry Zhang talk https://www.youtube.com/watch?v=D7_ipDqhtwk | ✅ (search) |

### Implementation checklist
1. Write the task as a single, well-prompted LLM call with retrieval and in-context examples; measure it. Only add structure if it fails.
2. If the task decomposes into fixed steps → prompt chaining with programmatic gates between steps.
3. If inputs fall into distinct categories → routing (classifier → specialised prompt/model; cheap model for easy cases).
4. If subtasks are independent or you need robustness → parallelization (sectioning or voting), aggregate programmatically.
5. If subtasks can't be predicted in advance → orchestrator-workers (orchestrator plans, workers execute, orchestrator synthesises).
6. If quality is judgeable and improves with feedback → evaluator-optimizer loop with explicit PASS/FAIL criteria.
7. Only for open-ended, multi-step tasks → an agent loop: LLM + tools + environment feedback, with stopping conditions, checkpoints for human input, sandboxing and guardrails.
8. Engineer the ACI: write tool docstrings like docs for a junior dev, include examples/edge cases, choose natural formats, avoid formatting overhead, poka-yoke arguments (e.g. absolute paths), test tools on many inputs.
9. Keep planning steps visible (transparency) and log tool calls.
10. Call the LLM API directly where possible; if using a framework, read its underlying code. Evaluate, iterate, and remove complexity that does not measurably help.

### Dependencies
- Builds on: *Raising the bar on SWE-bench Verified* (the SWE-bench coding agent is the worked example for agents and for tool-engineering lessons); computer-use reference implementation; MCP announcement.
- Built on by: *The "think" tool* (structured reasoning inside the tool loop), *Claude Code: Best practices* (Claude Code is an agent of exactly this shape; its multi-Claude workflows mirror parallelization/evaluator patterns), and later posts *How we built our multi-agent research system* (orchestrator-workers at scale), *Writing effective tools for agents* (expands Appendix 2), *Effective context engineering for AI agents*.

---

## 3. Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

- **Title:** Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet
- **URL:** https://www.anthropic.com/engineering/swe-bench-sonnet (originals: https://www.anthropic.com/news/swe-bench-sonnet, https://www.anthropic.com/research/swe-bench-sonnet ✅)
- **Date:** Search results date it to late October 2024 (published alongside the 22 Oct 2024 upgraded Claude 3.5 Sonnet release; one result says "October 30, 2024") ✅. The engineering-blog index lists it under Jan 2025 in the task brief — treat "Jan 2025" as the re-listing date on the new Engineering hub ❓.
- **Author:** Erik Schluntz (search snippet: "Erik Schluntz optimizing the SWE-bench agent and writing the blog post"; his GitHub handle `eschluntz` filed the leaderboard submission PR) ✅

### Thesis
The upgraded Claude 3.5 Sonnet scores 49% on SWE-bench Verified (vs. the previous SOTA of 45%) using a deliberately minimal agent: a prompt plus two general-purpose tools — a Bash tool and a file-editing tool — with as much control as possible handed to the model. The post describes that scaffold, argues that tool descriptions deserve careful engineering, and reports that the new model self-corrects, tries alternatives, and is "tenacious" over hundreds of turns. ✅

### Every concept, number, recommendation
- **Benchmark** ✅: SWE-bench = resolve real GitHub issues from popular open-source Python repos; model gets a set-up Python environment and a repo checkout from just before the issue was resolved; must understand, modify and test the code; graded against the real unit tests from the PR that closed the issue. **SWE-bench Verified** = 500-problem, human-reviewed subset guaranteed solvable — "the most clear measure of coding agents' performance".
- **Scaffolding matters** ✅: "The performance of an agent on SWE-bench can vary significantly based on this scaffolding, even when using the same underlying AI model."
- **Design philosophy** ✅: "give as much control as possible to the language model itself, and keep the scaffolding minimal". Agent = prompt + **Bash Tool** + **Edit Tool**. Built on the **SWE-Agent** framework "as a foundation" (search snippet) ✅; the leaderboard submission is named "Tools + Claude 3.5 Sonnet (2024-10-22)" ✅.
- **Bash tool** ✅: "The schema is simple, taking only the command to be run in the environment."
- **Edit tool** ✅: "Custom editing tool for viewing, creating and editing files"; "State is persistent across command calls and discussions with the user"; "we experimented with several different strategies for specifying edits, finding the highest reliability with string replacement" (str_replace with exact-match `old_str`/`new_str`).
- **Tool-description engineering** ✅: "We put a lot of effort into the descriptions and specs for these tools across agentic tasks, testing them to uncover ways the model might misunderstand the spec, then editing descriptions to preempt problems"; "much more attention should go into designing tool interfaces for models" (same lesson later in *Building effective agents*).
- **Sequential tool use / continue prompt** 🟡: the model is prompted to use one tool at a time; if it responds without a tool call it is nudged to continue ("Please continue working on the task on whatever approach you think is suitable…" — wording from memory).
- **Model behaviour** ✅: compared to older models, upgraded 3.5 Sonnet "self-corrects more often and shows an ability to try several different solutions, rather than getting stuck making the same mistake over and over"; "Many successful runs took hundreds of turns… with >100k tokens"; "Some tasks took more than 100 turns before the model submitted its solution; in others, the model kept trying until it ran out of context"; "tenacious—it can often find its way around a problem given enough time, but that can be expensive".
- **Result** ✅: 49% (245/500) — see per-repo breakdown below; previous SOTA 45%. Claude 3.5 Haiku with the same tools: 40.6% (203/500) ✅ (experiments PR #90).
- **Evaluation hygiene** ✅: Anthropic post-processed patches to strip changes to `tox.ini` because SWE-bench `pre_install` steps can leak into the diff and break grading for Sphinx tasks (from the submission README). Other evaluation details (Docker per task, timeouts, 200k context limit, pass@1 with one attempt) ❓ from memory.
- **Outlook** ❓ (memory): the score is not a ceiling; more scaffolding, multiple attempts/pass@N and test-time compute could raise it further; model rather than scaffold is the main driver.

### Concrete prompts / tool definitions
System prompt ❓ (memory): `You are a helpful assistant that can interact with a computer to solve tasks.`

Task prompt (structure and step list confirmed by search snippets; full text reconstructed from memory) 🟡:
```
<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{{ISSUE TEXT}}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!
Your task is to make the minimal changes to non-tests files in the /repo directory to ensure the <pr_description> is satisfied.
Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well
Your thinking should be thorough and so it's fine if it's very long.
```
(Steps 2–4 are quoted verbatim in a search snippet ✅.)

Bash tool definition 🟡 (schema confirmed "command only"; description text from memory):
```json
{
  "name": "bash",
  "description": "Run commands in a bash shell\n* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n* You don't have access to the internet via this tool.\n* You do have access to a mirror of common linux and python packages via apt and pip.\n* State is persistent across command calls and discussions with the user.\n* To inspect a particular line range of a file, e.g. lines 10-20, try 'sed -n 10,20p /path/to/file'.\n* Please avoid commands that may produce a very large amount of output.\n* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
  "input_schema": {
    "type": "object",
    "properties": { "command": { "type": "string", "description": "The bash command to run." } },
    "required": ["command"]
  }
}
```
Edit tool (`str_replace_editor`) — the SWE-agent repo carries the same docstring/args as Anthropic's `text_editor_20241022` (fetched from `tools/edit_anthropic/config.yaml`) ✅:
```
Custom editing tool for viewing, creating and editing files
* State is persistent across command calls and discussions with the user
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep
* The `create` command cannot be used if the specified `path` already exists as a file
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>`
* The `undo_edit` command will revert the last edit made to the file at `path`

Notes for using the `str_replace` command:
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique
* The `new_str` parameter should contain the edited lines that should replace the `old_str`
```
Arguments: `command` (enum `view|create|str_replace|insert|undo_edit`, required), `path` (absolute, required), `file_text`, `old_str`, `new_str`, `insert_line`, `view_range` ([start,end], `[start,-1]` to EOF). The same tool was productised as the Anthropic-defined text editor tool (`text_editor_20241022` → `text_editor_20250124` → `text_editor_20250429` `str_replace_based_edit_tool` → `text_editor_20250728` with `max_characters`) ✅ (platform docs fetched).

Leaderboard submission README (`swe-bench/experiments`, `evaluation/verified/20241022_tools_claude-3-5-sonnet-updated/README.md`) ✅: Resolved 245 (49.0%). By repo: astropy 11/22, django 119/231 (51.52%), matplotlib 12/34, seaborn 0/2, flask 1/1, requests 4/8, xarray 12/22, pylint 3/10, pytest 11/19, scikit-learn 24/32 (75%), sphinx 13/44, sympy 35/75. Haiku 3.5: 203 (40.6%).

### Hyperlinks
| Reference | URL | Status |
|---|---|---|
| Article | https://www.anthropic.com/engineering/swe-bench-sonnet | ✅ |
| Model announcement | https://www.anthropic.com/news/3-5-models-and-computer-use | ✅ (search) |
| SWE-bench paper | https://arxiv.org/abs/2310.06770 | ❓ standard cite |
| SWE-bench site / leaderboard | https://www.swebench.com/ | 🟡 |
| SWE-bench Verified (OpenAI) | https://openai.com/index/introducing-swe-bench-verified/ | 🟡 |
| SWE-agent | https://github.com/SWE-agent/SWE-agent ; paper https://arxiv.org/abs/2405.15793 | ✅ (search) |
| Submission PR | https://github.com/swe-bench/experiments/pull/90 | ✅ fetched |
| Submission README | https://raw.githubusercontent.com/swe-bench/experiments/main/evaluation/verified/20241022_tools_claude-3-5-sonnet-updated/README.md | ✅ fetched |
| Edit-tool config used by SWE-agent | https://github.com/SWE-agent/SWE-agent/blob/main/tools/edit_anthropic/config.yaml | ✅ fetched |
| Text editor tool docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool (was docs.anthropic.com/en/docs/agents-and-tools/tool-use/text-editor-tool) | ✅ fetched |
| Bash tool docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool | 🟡 |
| Model card addendum (Oct 2024) | https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf | ✅ (search) |
| Latent Space interview with Erik Schluntz | https://www.latent.space/p/claude-sonnet | ✅ (search; blocked to fetch) |

### Implementation checklist
1. Start from a minimal loop (SWE-agent or your own): system prompt + task prompt + tool-call loop; no hard-coded workflow stages.
2. Give the model exactly two general tools: `bash` (single `command` string; persistent shell state) and a `str_replace_editor`-style file tool (`view`, `create`, `str_replace`, `insert`, `undo_edit`; absolute paths; exact-match unique `old_str`).
3. Write the tool descriptions like documentation for a junior engineer: state persistence, truncation behaviour, whitespace sensitivity, uniqueness requirement, examples.
4. Put the task workflow in the prompt (explore → write a repro script → edit → rerun repro → consider edge cases) and tell the model long thinking is fine.
5. Nudge the model to keep going when it replies without a tool call; let it run for hundreds of turns / >100k tokens; set a context/turn budget you can afford.
6. Run each task in an isolated container with the repo at the pre-fix commit and hidden tests; grade with the benchmark harness.
7. Sanitise patches for harness artefacts (e.g. drop `tox.ini` changes) before grading.
8. Test the tools adversarially on many inputs, watch for misunderstandings, and iterate on the descriptions (spend more time here than on the prompt).
9. Track cost/turns per task; consider pass@N or multiple attempts only after the single-attempt baseline is solid.

### Dependencies
- Builds on: SWE-agent (Princeton) framework; SWE-bench Verified (OpenAI/Princeton).
- Built on by: *Building effective agents* (uses this agent as its coding example and source of the tool-engineering appendix), *The "think" tool* (SWE-bench variant of the think tool, +1.6%), *Claude Code: Best practices* (Claude Code is the productised descendant: bash + file-edit tools, minimal scaffold), the text-editor / bash tool API docs.

---

## 4. The "think" tool: Enabling Claude to stop and think in complex tool use situations

- **Title:** The "think" tool: Enabling Claude to stop and think in complex tool use situations ✅
- **URL:** https://www.anthropic.com/engineering/claude-think-tool ✅
- **Date:** 20 March 2025 ✅
- **Authors:** No byline on the post ❓ (from memory, unverified)
- **Later editorial note** ✅ (search snippet): the article now carries a note that extended thinking has improved since publication and Anthropic "recommends using extended thinking instead of a dedicated think tool in most cases".

### Thesis
A "think" tool is a no-op tool whose only effect is to append a thought to the log; giving Claude 3.7 Sonnet this tool — plus system-prompt guidance on when to use it — creates a dedicated space for structured reasoning *in the middle* of a multi-step tool-use trajectory (after tool results arrive), unlike extended thinking which happens before the response starts. On τ-bench's policy-heavy airline domain it lifted pass^1 from 0.370 to 0.570 (+54% relative) with an optimized prompt; on retail it helped even without prompting (0.812 vs 0.783); on SWE-bench it added 1.6% on average. ✅

### Every concept, number, recommendation
- **What it is** ✅: "a dedicated space for structured thinking during complex tasks"; lets Claude "stop and think about whether it has all the information it needs to move forward once it starts generating a response".
- **Think tool vs. extended thinking** ✅: extended thinking = reasoning *before* generating a response (good for problem-solving in one shot); think tool = reasoning *mid-response*, "to integrate external tool results on the fly", after new information from tool calls/user; "The 'think' tool allows Claude to pause during response generation to consider whether it has all necessary information to proceed."
- **Evaluation: τ-bench** ✅: "a comprehensive benchmark designed to test a model's ability to use tools in realistic customer service scenarios"; tests realistic conversations with simulated users, consistent policy adherence, and use of tools to access/manipulate the environment database; **pass^k** metric = probability all k independent trials succeed (consistency).
- **Airline results (pass^1)** ✅: baseline 0.370; think tool + optimized prompt 0.570 (54% relative). From memory 🟡: extended thinking 0.412; think tool alone 0.404; the pass^k curve (k=1…5) shows the think+prompt config staying ahead as k grows.
- **Retail results (pass^1)** ✅: baseline 0.783; think tool alone 0.812 (search snippet: "3.7% improvement without additional prompting"); extended thinking 0.770 ❓/🟡. Retail needed no extra prompt because its policies are simpler.
- **SWE-bench** ✅: adding the think tool gave "an isolated improvement of 1.6% on average" (search snippets add "statistically significant, p < .001") and contributed to Claude 3.7 Sonnet's 0.623 SWE-bench Verified score.
- **Where it helps most** ✅: (1) *Tool output analysis* — "reflecting on and processing results from previous tool calls" before acting; (2) *Policy-heavy environments* — verify compliance with detailed guidelines; (3) *Sequential decision making* — multi-step reasoning where errors compound.
- **When NOT to use** ✅: "minimal improvements for non-sequential tool calls or simple instruction following", and it "comes with increased prompt length and output tokens".
- **Best practices** ✅: *Strategic prompting with domain-specific examples* — show what to iterate over, how detailed to be, when to use it; *Place complex guidance in the system prompt*, not the tool description (the tool description stays short/generic); pairing the tool with domain-specific prompting gave the best results.
- **Getting started** ✅ (paraphrased in search snippets): add the tool definition; add instructions on when/how to use it plus domain examples in the system prompt; "monitor and refine" by watching how Claude uses it and adjusting the prompt.
- **Cost note** 🟡: minimal implementation overhead — the tool needs no implementation; only extra tokens.

### Concrete tool definition and prompts
Tool definition ✅ (verbatim):
```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": { "type": "string", "description": "A thought to think about." }
    },
    "required": ["thought"]
  }
}
```
System-prompt guidance for the airline domain ✅ (opening quoted in snippets; example block reconstructed 🟡):
```
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Silver member: 2 free bags per passenger → 6 free bags
  * Gold member: 3 free bags per passenger → 9 free bags
  * Economy: $50 per extra bag
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>
```
(A search snippet confirms the structure: cancellation example checking the 24-hour rule, airline-fault eligibility, business-class status, insurance, and whether segments have already departed.)
SWE-bench variant of the description ❓ (memory): "Use the tool to think about something. It will not obtain new information or make any changes to the repository, but just log the thought. Use it when complex reasoning or brainstorming is needed. For example, if you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective. Alternatively, if you receive some test results, call this tool to brainstorm ways to fix the failing tests." (Community MCP servers reference "the adapted SWE-Bench version" ✅.)

### Hyperlinks
| Reference | URL | Status |
|---|---|---|
| Article | https://www.anthropic.com/engineering/claude-think-tool | ✅ |
| τ-bench paper | https://arxiv.org/abs/2406.12045 | ✅ (search) |
| τ-bench repo | https://github.com/sierra-research/tau-bench | 🟡 |
| Claude 3.7 Sonnet announcement (τ-bench 81.2% retail / 58.4% airline "with a prompt addendum… 'planning' tool") | https://www.anthropic.com/news/claude-3-7-sonnet | ✅ (search) |
| Extended thinking docs | https://platform.claude.com/docs/en/build-with-claude/extended-thinking (was docs.anthropic.com/en/docs/build-with-claude/extended-thinking) | ✅ |
| Tool use docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | ✅ |
| Prompting guidance that supersedes it ("After receiving tool results, carefully reflect on their quality…") | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | ✅ fetched |
| Community MCP implementations | https://github.com/marcopesani/think-mcp-server , https://github.com/cgize/claude-mcp-think-tool , https://github.com/monotykamary/think-tool-mcp , https://github.com/abhinav-mangla/think-tool-mcp | ✅ fetched |
| Simon Willison note | https://simonwillison.net/2025/Mar/21/the-think-tool/ | ✅ exists (blocked) |

### Implementation checklist
1. Confirm the workload fits: long chains of tool calls, detailed policies, or decisions that depend on earlier tool results. Skip for single-shot or trivially sequential tasks.
2. Add the `think` tool definition (no server-side implementation; return an empty/ack tool result and keep the thought in the transcript).
3. In the **system prompt** (not the tool description) add a "## Using the think tool" section: when to call it (before any action/answer after tool results) and what to check (applicable rules, collected info, policy compliance, tool-result correctness).
4. Add 1–3 domain-specific `<think_tool_example_n>` blocks showing the expected granularity.
5. Evaluate with a τ-bench-style harness (simulated user, policy doc, tools) using pass^k for consistency, comparing baseline / extended thinking / think tool / think tool + prompt.
6. Monitor transcripts; refine the prompt examples where the model skips checks or over-thinks; watch token overhead.
7. Re-evaluate against current models — Anthropic now recommends extended/adaptive thinking (with interleaved thinking after tool results) over a dedicated think tool in most cases.

### Dependencies
- Builds on: *Building effective agents* (tool-use loop, ACI, "give the model enough tokens to think"), *SWE-bench Verified* agent (SWE-bench variant experiment), τ-bench (Sierra), Claude 3.7 Sonnet extended thinking.
- Built on by: *Claude Code: Best practices* (the "think"/"think hard"/"ultrathink" budget keywords are the extended-thinking cousin; Claude Code's planning step plays the same role); later docs on interleaved/adaptive thinking effectively absorb the technique.

---

## 5. Claude Code: Best practices for agentic coding

- **Title:** Claude Code: Best practices for agentic coding ✅
- **URL:** https://www.anthropic.com/engineering/claude-code-best-practices ✅ — now superseded by the living docs page https://code.claude.com/docs/en/best-practices ✅ (fetched in full; the anthropic.com page is described in search results as "Engineering at Anthropic" with the original April 2025 text)
- **Date:** 18 April 2025 ✅ (Boris Cherny's launch post)
- **Author:** Boris Cherny (creator of Claude Code) ✅. Acknowledgements ❓ (memory): thanks to Daisy Hollman, Ashwin Bhat, Cat Wu, Sid Bidasaria, Cal Rueb, Nodir Turakulov, Barry Zhang, Drew Hodun and other Anthropic engineers.

### Thesis
Claude Code is "a command line tool for agentic coding" that is intentionally low-level and unopinionated, giving close to raw model access without forcing a workflow. Because of that flexibility, Anthropic's internal teams and early users converged on a set of practices — tune a concise `CLAUDE.md`, curate allowed tools, give Claude more tools (bash/MCP/slash commands), follow explore→plan→code→commit or test-driven and screenshot-driven loops, be specific, course-correct early, manage context, use headless mode for automation, and scale with multiple Claude instances — that make agentic coding reliable across codebases and languages. ✅

### Original April 2025 structure — every practice (structure 🟡 from memory; items marked ✅ were confirmed by search snippets or by the current docs)
**1. Customize your setup**
- a. **Create `CLAUDE.md` files** ✅ — "a special file that Claude automatically pulls into context when starting a conversation". Document: common bash commands; core files and utility functions; code style guidelines; testing instructions; repository etiquette (branch naming, merge vs rebase); developer environment setup (pyenv, compilers); unexpected behaviours/warnings; other info you want remembered. No required format; keep concise and human-readable. Example ✅ (still in current docs):
  ```markdown
  # Bash commands
  - npm run build: Build the project
  - npm run typecheck: Run the typechecker

  # Code style
  - Use ES modules (import/export) syntax, not CommonJS (require)
  - Destructure imports when possible (eg. import { foo } from 'bar')

  # Workflow
  - Be sure to typecheck when you're done making a series of code changes
  - Prefer running single tests, and not the whole test suite, for performance
  ```
  Locations 🟡: repo root (`CLAUDE.md`, checked in; or `CLAUDE.local.md`, git-ignored); any parent directory (monorepos: `root/CLAUDE.md` + `root/foo/CLAUDE.md`, both pulled in when running in `root/foo`); child directories (pulled in on demand when Claude works with files there); home folder `~/.claude/CLAUDE.md` (applies to all sessions). `/init` generates a starter file ✅. Current docs add `@path/to/import` syntax, `.claude/rules/*.md` with `paths:` globs, `AGENTS.md` support, and `/doctor` pruning ✅.
- b. **Tune your `CLAUDE.md` files** 🟡 — iterate like any prompt; don't just dump content; run it through the prompt improver (https://claude.com/blog/prompt-improver ✅ exists); add emphasis like "IMPORTANT" or "YOU MUST" for adherence; use the `#` key to have Claude add an instruction to the relevant `CLAUDE.md`; commit `CLAUDE.md` changes so the team benefits.
- c. **Curate Claude's list of allowed tools** 🟡 — by default Claude asks before anything that might modify the system (file writes, many bash commands, MCP tools). Four ways: select "Always allow" in a prompt; `/permissions` to add/remove (e.g. `Edit`, `Bash(git commit:*)`, `mcp__puppeteer__puppeteer_navigate`); edit `.claude/settings.json` (checked in) or `~/.claude.json`; the `--allowedTools` CLI flag for session-specific permissions ✅ (flag confirmed in headless docs).
- d. **If using GitHub, install the `gh` CLI** ✅ — Claude uses it to create issues, open PRs, read comments; without it Claude can still use the API/MCP.

**2. Give Claude more tools**
- a. **Use Claude with bash tools** 🟡 — Claude inherits your shell environment; tell it the tool name with usage examples, tell it to run `--help`, document frequently used tools in `CLAUDE.md`. (Current docs: `Use 'foo-cli-tool --help' to learn about foo tool…` ✅.)
- b. **Use Claude with MCP** 🟡 — Claude Code is both an MCP server and client. Configure servers in project config (current dir), global config, or a checked-in `.mcp.json` (e.g. Puppeteer, Sentry). Use `--mcp-debug` when troubleshooting. (Current docs: `claude mcp add --transport http notion https://mcp.notion.com/mcp` ✅.)
- c. **Use custom slash commands** 🟡 — store prompt templates in `.claude/commands/<name>.md` (checked in) or `~/.claude/commands/`; they appear in the slash menu; `$ARGUMENTS` passes parameters. Example `.claude/commands/fix-github-issue.md`:
  ```
  Please analyze and fix the GitHub issue: $ARGUMENTS.

  Follow these steps:
  1. Use `gh issue view` to get the issue details
  2. Understand the problem described in the issue
  3. Search the codebase for relevant files
  4. Implement the necessary changes to fix the issue
  5. Write and run tests to verify the fix
  6. Ensure code passes linting and type checking
  7. Create a descriptive commit message
  8. Push and create a PR
  ```
  invoked as `/project:fix-github-issue 1234`. (The current docs carry the same 8 steps as a skill `.claude/skills/fix-issue/SKILL.md` with `disable-model-invocation: true`, invoked `/fix-issue 1234` ✅.)

**3. Try common workflows**
- a. **Explore, plan, code, commit** ✅ — (1) ask Claude to read relevant files/images/URLs, explicitly "don't write any code yet"; consider subagents for sub-questions to preserve context; (2) ask for a plan, using extended-thinking trigger words — `"think"` < `"think hard"` < `"think harder"` < `"ultrathink"` map to increasing thinking budgets ✅; optionally have Claude write the plan to a doc or GitHub issue so you can reset; (3) ask Claude to implement, verifying reasonableness as it goes; (4) ask it to commit and open a PR, and update READMEs/changelogs. Steps 1–2 are the important ones. (Current docs: plan mode via `Shift+Tab` or `claude --permission-mode plan`, `Ctrl+G` to edit the plan ✅.)
- b. **Write tests, commit; code, iterate, commit** ✅ — TDD: ask for tests from expected input/output pairs and say you're doing TDD so it avoids mock implementations; tell it to run tests and confirm they fail (don't write implementation yet); commit the tests; ask for code that passes without modifying tests, iterating until green; optionally verify with independent subagents that the implementation isn't overfitting; commit.
- c. **Write code, screenshot result, iterate** ✅ — give Claude a way to take browser screenshots (Puppeteer MCP server, iOS simulator MCP server, or paste manually); give a visual mock (paste/drag-drop/file path); ask it to implement, screenshot, and iterate until it matches; "usually 2-3 iterations" ✅; then commit.
- d. **Safe YOLO mode** ✅ — `claude --dangerously-skip-permissions` bypasses all permission checks (useful for fixing lint errors or boilerplate); risky (data loss, system corruption, exfiltration via prompt injection) → run only in a container without internet; reference devcontainer at https://github.com/anthropics/claude-code/tree/main/.devcontainer ✅ (search confirms Anthropic's reference devcontainer).
- e. **Use Claude to interact with your codebase (Codebase Q&A)** ✅ — onboarding by asking engineer-style questions: "How does logging work?", "How do I make a new API endpoint?", "What does `async move { ... }` do on line 134 of `foo.rs`?", "What edge cases does `CustomerOnboardingFlowImpl` handle?", "Why does this code call `foo()` instead of `bar()` on line 333?", "What is the equivalent of line 334 of `baz.py` in Java?" — "No special prompting required".
- f. **Use Claude to interact with git** ✅ — search git history ("what changes made it into v1.2.3?", "who owns this feature?"), write commit messages (Claude looks at changes and recent history automatically), handle complex ops (revert, rebase conflicts, compare/graft patches).
- g. **Use Claude to interact with GitHub** 🟡 — create PRs (`pr` shorthand understood), one-shot fixes for review comments ("fix comments on my PR"), fix failing builds/linter warnings, triage/categorise open issues by looping over them.
- h. **Use Claude to work with Jupyter notebooks** 🟡 — open side-by-side in VS Code; Claude can read/write notebooks including image outputs; ask it to clean up or make notebooks "aesthetically pleasing" before showing colleagues.

**4. Optimize your workflow**
- a. **Be specific in your instructions** ✅ — table: "add tests for foo.py" → "write a new test case for foo.py, covering the edge case where the user is logged out. avoid mocks"; "why does ExecutionFactory have such a weird api?" → "look through ExecutionFactory's git history and summarize how its api came to be"; "add a calendar widget" → "look at how existing widgets are implemented on the home page… HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase." Vague prompts are fine when exploring.
- b. **Give Claude images** ✅ — paste screenshots (macOS `cmd+ctrl+shift+4` to clipboard, `ctrl+v` to paste), drag-and-drop, or provide a file path; "essential for UI tasks".
- c. **Mention files you want Claude to look at or work on** ✅ — tab-completion / `@` references.
- d. **Give Claude URLs** ✅ — paste docs/API URLs; use `/permissions` to allowlist domains to avoid repeated prompts.
- e. **Course correct early and often** ✅ — ask for a plan first and say not to code until confirmed; `Escape` to interrupt (preserves context); double-tap `Escape` to jump back in history, edit a previous prompt and explore a different direction; ask Claude to undo changes.
- f. **Use `/clear` to keep context focused** ✅ — between tasks to reset the context window.
- g. **Use checklists and scratchpads for complex workflows** ✅ — for migrations, many lint errors, complex build scripts: have Claude write a Markdown checklist (or GitHub issue), then work through items one by one, checking them off. Example: run lint, write all errors with file:line to a Markdown checklist, fix and verify each.
- h. **Pass data into Claude** ✅ — copy/paste; pipe in (`cat foo.txt | claude`); tell Claude to pull data via bash/MCP/slash commands; ask it to read files or fetch URLs; often combine.

**5. Use headless mode to automate your infra** ✅ — `claude -p "<prompt>"` for non-interactive contexts (CI, pre-commit hooks, build scripts); `--output-format stream-json` for streaming JSON; headless mode doesn't persist between sessions (each invocation is fresh) 🟡. Patterns: **Issue triage** (GitHub Actions on new issue → Claude assigns labels); **Claude as a linter** (subjective review: typos, stale comments, misleading names). Current docs ✅: `--output-format json|stream-json`, `--verbose`, `--allowedTools`, `--permission-mode`, `--append-system-prompt`, `--bare`, `--continue/--resume`, `--json-schema`.

**6. Uplevel with multi-Claude workflows**
- a. **Have one Claude write code; use another Claude to verify** ✅ — writer Claude implements; `/clear` or a second terminal; reviewer Claude reviews; a third Claude reads both and edits. Same for tests: one writes tests, another writes code to pass them. "A fresh context improves code review since Claude won't be biased toward code it just wrote" ✅ (current docs Writer/Reviewer table).
- b. **Have multiple checkouts of your repo** 🟡 — 3–4 checkouts in separate folders, one terminal tab each, cycle through approving/denying; iTerm2 notifications.
- c. **Use git worktrees** ✅ — lighter than full checkouts: `git worktree add ../project-feature-a feature-a`, `cd ../project-feature-a && claude`, repeat for `feature-b`; consistent naming; one tab per worktree; separate IDE windows; `git worktree remove ../project-feature-a` when done. (Current docs: `claude --worktree feature-auth` ✅.)
- d. **Use headless mode with a custom harness** ✅ — *Fanning out* for large migrations/analyses: have Claude write a task list (e.g. 2,000 files to migrate), loop calling `claude -p "<prompt>" --allowedTools Edit Bash(git commit:*)` per task returning OK/FAIL, run on 2–3 files first then scale; *Pipelining*: `claude -p "<your prompt>" --json | your_command`; use `--verbose` for debugging, off in production. (Current docs keep the bash loop with `--allowedTools "Edit,Bash(git commit *)"` ✅.)

Closing 🟡: Claude Code is designed to be flexible; the docs (then https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview, now https://code.claude.com/docs/en/overview ✅) are the reference.

### Additions in the current living version (code.claude.com/docs/en/best-practices, fetched 2026-09) ✅
- Framing: "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."
- "Give Claude a way to verify its work" (tests, build exit codes, linters, screenshot diffs); gates: same-prompt, `/goal` condition, Stop hook (overridden after 8 consecutive blocks), verification subagent; ask for evidence.
- Explore → Plan (`Shift+Tab`, `claude --permission-mode plan`, `Ctrl+G`) → Implement → Commit; skip planning if the diff fits in one sentence.
- `CLAUDE.md` include/exclude table; `/context`, `/doctor`, `/init`; "Would removing this cause Claude to make mistakes?"; emphasis on one line only; `@path` imports; `.claude/rules/`.
- Permissions: auto mode (classifier) on Pro/Max/Team; Manual mode; `/permissions`, `/sandbox`.
- Hooks in `.claude/settings.json`, `/hooks`; Skills in `.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`, `disable-model-invocation`); subagents in `.claude/agents/<name>.md` (frontmatter `name`, `description`, `tools`, `model`); plugins via `/plugin`; MCP via `claude mcp add`.
- "Let Claude interview you" with the `AskUserQuestion` tool → `SPEC.md`, then fresh session.
- Session management: `Esc`, `Esc+Esc`/`/rewind` (checkpoints, summarize from/up to here), `/clear`, `/compact <instructions>`, `/btw`, `/rename`, `claude --continue`, `claude --resume`.
- Scale: `claude -p` with `--output-format json|stream-json --verbose`, `--allowedTools`, `--permission-mode auto`, `/batch <instruction>` (5–30 subagents in worktrees), worktrees, cross-session messaging, desktop app, cloud, agent view, agent teams; adversarial review via `/code-review` or a subagent against `PLAN.md`.
- Failure patterns: kitchen-sink session, correcting over and over, over-specified `CLAUDE.md`, trust-then-verify gap, infinite exploration.

### Hyperlinks
| Reference | URL (then → now) | Status |
|---|---|---|
| Article | https://www.anthropic.com/engineering/claude-code-best-practices | ✅ |
| Living docs version | https://code.claude.com/docs/en/best-practices | ✅ fetched |
| Claude Code overview | https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview → https://code.claude.com/docs/en/overview | ✅ new URL 200 |
| Memory / CLAUDE.md docs | https://docs.anthropic.com/en/docs/claude-code/memory → https://code.claude.com/docs/en/memory | ✅ fetched |
| Common workflows | https://code.claude.com/docs/en/common-workflows | ✅ fetched |
| Headless / programmatic | https://code.claude.com/docs/en/headless | ✅ fetched |
| Permissions / settings | https://code.claude.com/docs/en/permissions , https://code.claude.com/docs/en/settings-reference , https://code.claude.com/docs/en/permission-modes | ✅ linked from docs |
| MCP in Claude Code | https://code.claude.com/docs/en/mcp | ✅ |
| Hooks / Skills / Subagents / Plugins | https://code.claude.com/docs/en/hooks , /docs/en/skills , /docs/en/sub-agents , /docs/en/plugins | ✅ |
| Worktrees / Sessions / Checkpointing | https://code.claude.com/docs/en/worktrees , /docs/en/sessions , /docs/en/checkpointing | ✅ |
| Reference devcontainer | https://github.com/anthropics/claude-code/tree/main/.devcontainer | ✅ (search) |
| Claude Code repo | https://github.com/anthropics/claude-code | ✅ |
| Prompt improver | https://claude.com/blog/prompt-improver (was anthropic.com/news/prompt-improver) ; console docs https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools | ✅ (search) |
| Extended thinking (think/ultrathink) | https://platform.claude.com/docs/en/build-with-claude/extended-thinking | ✅ |
| Puppeteer MCP server | https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer (now archived under servers-archived ❓) | 🟡 |
| iOS simulator MCP server | https://github.com/joshuayoes/ios-simulator-mcp | ❓ |
| GitHub CLI | https://cli.github.com/ | ❓ |
| Model Context Protocol | https://modelcontextprotocol.io/ | 🟡 |
| Launch post | https://www.threads.com/@boris_cherny/post/DImosORT-Us | ✅ (search) |
| "How Anthropic teams use Claude Code" (companion) | https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf | ✅ (search) |

### Implementation checklist
1. Install Claude Code and `gh`; run `/init` to generate `CLAUDE.md`; fill in build/test/lint commands, style rules, repo etiquette, env quirks; keep it short; check it in (use `CLAUDE.local.md` / `~/.claude/CLAUDE.md` for personal items).
2. Configure permissions: `/permissions` allowlist for safe tools (`Edit`, `Bash(git commit:*)`, lint/test commands), commit `.claude/settings.json`; reserve `--dangerously-skip-permissions` for isolated containers (reference devcontainer).
3. Add tools: document bash CLIs in `CLAUDE.md`; add MCP servers via `.mcp.json` / `claude mcp add` (Puppeteer for screenshots, issue trackers, DBs); create `.claude/commands/*.md` (or `.claude/skills/*/SKILL.md`) with `$ARGUMENTS` for repeated workflows.
4. For each task: Explore (read files, no code) → Plan (ask for a plan, use "think hard"/"ultrathink" or plan mode, optionally save plan to a file/issue) → Code → Commit/PR.
5. Prefer verifiable loops: TDD (tests first, confirm fail, commit, implement, don't touch tests) or screenshot iteration against a mock (2–3 rounds).
6. Prompt specifically: name files (`@`), paste images/URLs, describe symptom + location + definition of done; ask for a checklist/scratchpad on large multi-step jobs.
7. Steer aggressively: `Esc` to interrupt, `Esc Esc`/`/rewind` to back up, `/clear` between tasks, `/compact` with focus instructions; after two failed corrections, clear and re-prompt.
8. Automate: `claude -p` in CI/pre-commit for triage, linting, migrations (`--allowedTools`, `--output-format json|stream-json`, `--verbose` while debugging); fan out over a generated task list; pipe results downstream.
9. Scale with multiple Claudes: writer/reviewer split, tests-vs-implementation split, parallel worktrees (`git worktree add …` / `claude --worktree`), one terminal per worktree.
10. Periodically prune `CLAUDE.md`, review what worked, and turn recurring corrections into hooks/skills.

### Dependencies
- Builds on: *Raising the bar on SWE-bench Verified* (Claude Code's bash + str_replace editing tools and minimal scaffold), *Building effective agents* (agent loop, simplicity, ACI; multi-Claude = parallelization/evaluator-optimizer), *The "think" tool* / extended thinking (planning keywords), MCP.
- Built on by: the living `code.claude.com` best-practices doc; later engineering posts (*How Anthropic teams use Claude Code*, *Claude Code sandboxing*, *Effective context engineering*, *Writing effective tools for agents*, *Agent Skills*), and the Claude Agent SDK docs (headless mode became `claude -p` / Agent SDK).

---

## Cross-article dependency map (batch A)
- Contextual Retrieval (Sep 2024) ← Prompt caching; → retrieval block of *Building effective agents*; → later context-engineering posts.
- SWE-bench Sonnet agent (Oct 2024) ← SWE-agent, SWE-bench Verified; → *Building effective agents* (coding-agent example, tool appendix), → *think tool* (SWE-bench experiment), → Claude Code (productised tools), → text-editor/bash tool API docs.
- Building effective agents (Dec 2024) ← SWE-bench agent, computer use, MCP; → think tool, Claude Code best practices, multi-agent research system, writing tools for agents.
- Think tool (Mar 2025) ← Building effective agents, τ-bench, Claude 3.7 extended thinking; → superseded in practice by interleaved/adaptive thinking guidance; concept reused in Claude Code planning.
- Claude Code best practices (Apr 2025) ← all four above; → living docs and every later Claude Code post.
