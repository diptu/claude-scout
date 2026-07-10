---
name: rag-agent-architecture-guide
description: Guides Claude through designing and implementing retrieval-augmented generation (RAG) pipelines and LLM-powered agent applications, covering architecture choices, common failure modes, and implementation patterns; use whenever a user wants to build, debug, or improve a RAG system, an AI agent, or an LLM-integrated application.

# RAG & Agent Architecture Guide

This skill helps design and implement real-world applications built around large language models: retrieval-augmented generation (RAG) pipelines, autonomous or semi-autonomous agents, and hybrid systems that combine the two. Apply it when a user is starting a new LLM-powered feature, debugging poor retrieval or agent behavior, or asking how to structure such a system well.

## When to apply this skill

- The user wants to build a system that answers questions over private/custom documents (RAG).
- The user is building an agent that calls tools, makes multi-step decisions, or orchestrates other agents.
- The user is debugging symptoms like irrelevant retrieved chunks, hallucinated answers despite retrieval, agents looping or calling the wrong tool, or slow/expensive pipelines.
- The user asks for a comparison of architectural approaches (e.g., "should I use RAG or fine-tuning?", "single agent or multi-agent?").

## Step 1: Clarify the actual requirement before architecting

Before proposing an architecture, establish:
1. **Data shape** — structured (DB/API) vs. unstructured (docs, PDFs, wikis) vs. mixed. This determines whether RAG, tool-calling, or both are needed.
2. **Freshness needs** — does the answer need to reflect data that changes hourly/daily, or is it mostly static? Static data can be embedded once; frequently-changing data favors tool-calling over re-embedding.
3. **Latency/cost budget** — a single-pass RAG call is cheap and fast; multi-step agentic loops are slower and costlier. Don't reach for an agent when a single retrieval + generation call solves the problem.
4. **Failure tolerance** — is this a user-facing chat answer (some hallucination tolerable, correct with follow-up) or a system that triggers actions (needs strict guardrails, human confirmation, or deterministic validation)?

Do not default to the most sophisticated architecture. A single well-tuned retrieval call beats a multi-agent pipeline for most "answer questions about my docs" requests.

## Step 2: RAG pipeline design

When a RAG pipeline is warranted, walk through each stage deliberately rather than accepting library defaults blindly:

- **Chunking**: chunk size and overlap should match the source's natural structure (paragraphs, sections, code functions) rather than a fixed arbitrary token count. Recommend semantic or structure-aware chunking over naive fixed-size splitting when documents have clear headings or logical units.
- **Embedding model choice**: match the embedding model's domain (general text, code, multilingual) to the corpus. Mismatched embedding models are a common silent cause of poor retrieval.
- **Retrieval strategy**: start with plain vector similarity search; add hybrid search (vector + keyword/BM25) when queries include exact terms, IDs, or names that embeddings blur. Add re-ranking as a second pass only if the top-k results are noisy — don't add it preemptively.
- **Context assembly**: retrieved chunks should be deduplicated, ordered by relevance, and trimmed to fit the context window with room left for the system prompt and conversation history. Always cite or attribute which chunk supports which claim, so the user can spot ungrounded answers.
- **Evaluation**: any RAG change should be checked against a small fixed set of representative queries with known-good answers, not just eyeballed on one example. If no such set exists, suggest building one first — even 10-15 queries surface real regressions.

## Step 3: Agent design

When the task needs multi-step reasoning or tool use:

- **Start single-agent**: one agent with a clear set of tools and a tight system prompt outperforms a multi-agent setup for most tasks. Reach for multiple specialized agents only when a single agent's context or tool set has genuinely become unwieldy (too many unrelated tools, conflicting instructions for different subtasks).
- **Tool design**: each tool should do one well-defined thing with a narrow, typed interface. Vague, catch-all tools ("do_anything") cause the agent to misuse them or loop. Give each tool a description that states exactly when to call it and what it returns.
- **Bound the loop**: always cap the number of agent steps/iterations and define what happens on cap-out (return partial results with an explanation, not a silent failure or infinite retry).
- **Guard irreversible actions**: any tool that writes, deletes, sends, or spends should require an explicit confirmation step or a human-in-the-loop checkpoint before executing, unless the user has explicitly authorized full autonomy for that action.
- **Memory/state**: keep only what the agent needs for the current task in its working context; summarize or discard old tool outputs rather than letting transcripts grow unbounded, which degrades reasoning quality and increases cost.

## Step 4: Diagnosing common failures

When asked to debug an existing RAG or agent system, check these first, in order:

1. **Retrieval is wrong** — print/log the actual retrieved chunks for the failing query. If they're irrelevant, the problem is chunking/embedding/retrieval, not the LLM's reasoning. Most "hallucination" complaints are actually retrieval failures in disguise.
2. **Context is right but the answer is still wrong** — check if the retrieved context is contradictory, too long (key fact buried), or missing an explicit instruction to only answer from provided context.
3. **Agent picks the wrong tool** — check tool descriptions for ambiguity or overlap; two tools with similar-sounding purposes are a frequent cause.
4. **Agent loops or stalls** — check the step cap and the termination condition; a vague "stop when done" condition is a common culprit versus a concrete, checkable success criterion.

## Step 5: Recommend incrementally, not exhaustively

When proposing an architecture or a fix, give one concrete recommended path plus the one or two decision points that matter most (e.g., "start with plain vector search; add hybrid search only if you see queries with exact IDs/names failing"). Avoid presenting a full menu of every possible technique (fine-tuning, multi-agent orchestration, knowledge graphs, etc.) unless the user's stated constraints actually call for that level of sophistication.
