---
name: llm-pipeline-architect
description: Guides the design of modular LLM application pipelines (RAG, agents, semantic search, conversational systems) with explicit, inspectable stages for retrieval, routing, memory, and generation; use when a user wants to architect, structure, or refactor an LLM-powered application rather than write a single monolithic prompt.
---

# LLM Pipeline Architect

This skill helps design LLM-powered applications as explicit, composable
pipelines instead of a single opaque prompt or an unstructured tangle of API
calls. It applies whenever a user is building or restructuring something like
retrieval-augmented generation (RAG), a multi-step agent, a semantic search
system, a document Q&A tool, or a conversational assistant with memory.

## When to apply this skill

Apply this skill when the user's request involves any of:

- Building a system that combines retrieval (search over documents/vectors)
  with generation (an LLM producing an answer).
- Designing an agent that needs to decide between multiple tools, data
  sources, or sub-tasks (routing).
- Adding conversational memory or multi-turn state to an LLM application.
- Refactoring a single giant prompt or a script full of ad-hoc API calls into
  something maintainable and testable.
- Any request that mentions "pipeline," "orchestration," "RAG," "agent
  workflow," or "semantic search" in the context of building software.

Do not apply this skill to one-off prompt-writing tasks, simple chatbot
wrappers with no retrieval or multi-step logic, or requests that are really
about model selection/pricing rather than application architecture.

## Core idea: pipelines as explicit stage graphs

Treat the application as a directed graph of named, single-responsibility
stages rather than one function that does everything. Each stage should:

- Take a well-defined input and produce a well-defined output (a "document,"
  a "query," a "ranked list of candidates," an "answer with citations").
- Be swappable without touching the rest of the graph (e.g. a keyword
  retriever can be replaced by a vector retriever without changing the
  generation stage).
- Be individually testable in isolation, with fixed inputs and expected
  output shapes.

When a user asks for a pipeline, sketch the stage graph in words or a small
diagram before writing code: what goes in, what comes out, and which stages
are optional or conditional.

## Step-by-step guidance

1. **Clarify the task shape first.** Ask (or infer from context) whether the
   system is primarily: retrieval + generation (RAG), multi-step reasoning
   with tool calls (agent), pure search/ranking (semantic search), or
   turn-based dialogue with state (conversational). This determines which
   stages are needed.

2. **Separate retrieval from generation.** Never let a single call both
   fetch context and produce the final answer implicitly. Make retrieval its
   own explicit stage: given a query, return a ranked/filtered set of
   documents or chunks, with enough metadata (source, score) to support
   citations or debugging. Only pass the retrieved context to a distinct
   generation stage afterward.

3. **Make routing decisions explicit, not implicit in a prompt.** If the
   system must choose between multiple tools, data sources, or sub-pipelines
   (e.g. "search the docs" vs. "call the calculator" vs. "ask a clarifying
   question"), model that choice as its own routing stage with a small,
   enumerable set of outcomes — rather than hoping a single freeform prompt
   reliably picks the right path. State what signal the router uses to
   decide (keywords, a classifier, an LLM call with a constrained output).

4. **Treat memory as a stage with a defined read/write contract.** Decide
   explicitly: what gets stored (raw turns, summaries, extracted facts),
   when it's written, and how it's retrieved for the next turn. Avoid
   silently growing an unbounded prompt history — call out truncation,
   summarization, or windowing strategy as a deliberate design choice.

5. **Design for inspectability.** At each stage boundary, the intermediate
   output should be loggable and testable on its own — the retrieved
   documents, the router's chosen path, the memory state before generation.
   This is what makes the pipeline debuggable instead of a black box; when
   something goes wrong, the user should be able to point at which stage
   produced a bad output.

6. **Keep stages composable across use cases.** A retrieval stage built for
   one pipeline should be reusable in another (e.g. the same document
   retriever powering both a Q&A pipeline and a summarization pipeline).
   Favor small, focused stages over large multi-purpose ones.

7. **Validate the whole graph end-to-end, not just stages in isolation.**
   After stages are wired together, walk through at least one concrete
   example query through every stage, checking that each handoff (query →
   retrieved docs → routed path → memory-augmented context → final answer)
   produces what the next stage expects.

## Anti-patterns to flag

- A single giant prompt that tries to retrieve, reason, route, and answer
  all at once — hard to debug and hard to improve incrementally.
- Retrieval and generation fused so tightly that swapping the retriever
  requires rewriting the generation logic.
- Memory implemented as "just append everything to the prompt" with no
  bound or summarization strategy, leading to context overflow or drift.
- Routing logic buried inside a prompt's instructions rather than being an
  observable, testable decision point.
- No way to inspect intermediate outputs, so failures can only be diagnosed
  by re-reading the final answer and guessing which stage went wrong.
