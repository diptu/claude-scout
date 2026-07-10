---
name: llm-pipeline-architect
description: Designs modular, production-ready LLM application architectures (RAG, agents, semantic search, conversational systems) with explicit separation of retrieval, routing, memory, and generation stages; use when a user wants to build, structure, or refactor an LLM-powered pipeline rather than write one large ad-hoc script.
---

# LLM Pipeline Architect

Helps design and implement LLM-powered applications — retrieval-augmented generation (RAG), multi-step agents, semantic search, and conversational systems — as explicit, modular pipelines rather than monolithic scripts. Apply this skill whenever a user asks to build, extend, or debug an application that chains together retrieval, an LLM call, and some form of routing or memory, especially when they're unsure how to structure the pieces or the current implementation has become a tangle of inline logic.

## When to apply this skill

- The user wants to build a RAG system, chatbot, semantic search feature, or agent workflow from scratch.
- An existing LLM application mixes retrieval, prompt construction, memory, and generation in one function or file, and the user wants it untangled.
- The user is deciding how to route a query to different tools, indexes, or models based on intent.
- The user needs to add conversational memory (short-term context, long-term facts, or session state) to an existing single-turn LLM call.
- The user is comparing or combining multiple retrieval sources (vector search, keyword search, structured lookups) and needs a clean way to merge results.

Do not apply this skill to simple, single-shot prompt-completion tasks with no retrieval, routing, or multi-step state — those don't benefit from pipeline structure and adding it would be over-engineering.

## Core design model: pipelines as explicit stages

Treat every LLM application as a directed pipeline of named, single-responsibility stages. Each stage takes typed input, does one job, and produces typed output that the next stage consumes. The four canonical stage categories:

1. **Retrieval** — pulls candidate context from one or more sources (vector index, keyword/BM25 index, database query, API call, file search). A retrieval stage should return raw candidates plus enough metadata (source, score, id) for later stages to filter or cite them. Never let a retrieval stage also decide what to do with the results — that's routing's job.

2. **Routing** — decides which path a request takes: which retriever(s) to call, which prompt template to use, which model to invoke, or whether to skip generation entirely (e.g., a cache hit or a direct-answer shortcut). Routing logic should be a small, inspectable decision point (a classifier call, a rule set, or a lightweight router prompt) — not buried inside a generation stage's prompt.

3. **Memory** — carries state across turns or steps: conversation history, extracted facts, running summaries, or scratchpad state for multi-step agent reasoning. Separate short-term memory (verbatim recent turns, bounded by a window) from long-term memory (summarized or extracted facts, persisted across sessions). Memory should be read explicitly at the start of a pipeline run and written explicitly at the end — not mutated implicitly mid-pipeline.

4. **Generation** — the actual LLM call that produces the user-facing output, given the assembled context (retrieved candidates + memory + the routed prompt template). A generation stage should be swappable: changing the model or prompt template shouldn't require touching retrieval or routing code.

## Step-by-step guidance

When building or refactoring a pipeline:

1. **Map the request to stages first, before writing code.** Sketch the path a single request takes: what gets retrieved, how it's routed, what memory is read/written, and what gets generated. If a step doesn't cleanly fall into one of the four categories, it's usually either orchestration glue (fine to keep thin and explicit) or a sign two responsibilities are tangled together.

2. **Give each stage a narrow, typed interface.** A retrieval stage takes a query and returns a list of scored candidates — not the raw user request, not a rendered prompt. A generation stage takes assembled context and a prompt template — not a database connection. This makes each stage independently testable and swappable.

3. **Keep routing decisions visible and centralized.** If the same conditional logic ("if the query looks like X, do Y") appears in multiple places, consolidate it into one routing stage. A router can be as simple as a few if/elif rules on query features, or as involved as a small classification prompt — match the complexity to the actual ambiguity in the routing decision, not to what seems impressive.

4. **Default to the simplest retrieval that satisfies the query type**, and only combine multiple retrieval sources (hybrid search) when a single source demonstrably misses relevant results. Merging multiple retrievers adds a fusion/re-ranking step — don't add it speculatively.

5. **Make memory explicit and bounded.** For conversational systems, decide up front: how many turns of raw history are kept verbatim, when (if ever) older turns get summarized, and what triggers a memory write. Unbounded verbatim history is the most common source of runaway context growth — cap it deliberately.

6. **Keep generation prompts separate from orchestration code.** Store prompt templates as distinct, named artifacts (not inline string concatenation scattered through the pipeline logic) so they can be iterated on and evaluated without touching retrieval/routing/memory code.

7. **When debugging a misbehaving pipeline, isolate the stage first.** Check what retrieval actually returned, what the router decided, and what memory/context was assembled — before assuming the generation prompt is at fault. Most "the LLM gave a bad answer" issues trace back to bad or missing retrieved context, not the prompt itself.

8. **For multi-step agent workflows**, treat each agent "turn" as a pipeline run: retrieve/observe, route (decide next action), update memory (scratchpad/history), generate (produce the next action or final answer). Loop until a routing decision says to stop. Keep the stopping condition explicit rather than relying on the model to naturally decide when to end.

## Anti-patterns to flag

- A single function that queries a vector store, formats a prompt, calls the LLM, and parses the response all inline — hard to test or swap any one piece.
- Routing logic duplicated across multiple entry points instead of centralized in one place.
- Conversation history appended to forever with no summarization or windowing.
- Prompt templates embedded as multi-line string literals deep inside orchestration logic, making them hard to find or version.
- Retrieval and generation coupled so tightly that changing the retriever requires rewriting the prompt logic, or vice versa.
