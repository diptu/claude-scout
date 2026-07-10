---
name: llm-rag-agent-builder
description: Guides Claude through designing and building LLM applications, RAG pipelines, and AI agents from scratch, covering architecture choices, retrieval strategies, and evaluation; use when a user wants to build, debug, or improve a RAG system, LLM-powered agent, or other generative AI application.
---

# LLM & RAG Application Builder

This skill helps design, implement, and troubleshoot real-world LLM applications: retrieval-augmented generation (RAG) pipelines, AI agents with tool use, and other LLM-powered systems. Apply it whenever a user is building a new AI feature, debugging a RAG pipeline's poor answer quality, or deciding between architectural approaches for an agent.

## When to apply this skill

- The user wants to build or prototype a RAG system, chatbot, or document Q&A tool
- The user is designing an agent that needs to call tools, use memory, or plan multi-step tasks
- The user's existing RAG pipeline is returning irrelevant or low-quality answers
- The user is choosing between architectures (single LLM call vs. agent loop vs. multi-agent) for a task
- The user asks about chunking, embeddings, vector search, or evaluation for an LLM application

## Step-by-step guidance

### 1. Clarify the actual task before picking an architecture

Ask (or infer from context) what the system needs to do: answer questions over a fixed document set, take actions in the world, hold multi-turn state, or some mix. Many "RAG" requests are actually simpler (a single well-crafted prompt with the right context stuffed in) or more complex (need an agent loop with tool calls) than the user assumes. Don't reach for RAG or an agent framework by default — start with the simplest architecture that could work, and only add retrieval or agentic loops once a plain prompt demonstrably falls short (context too large, knowledge changes too often, or the task requires taking actions).

### 2. If building RAG, work through each stage deliberately

- **Ingestion & chunking**: Chunk size should match how the user will ask questions — small chunks (100-300 tokens) for precise fact lookup, larger chunks (500-1000+ tokens) for narrative or multi-fact answers. Prefer semantic or structure-aware chunking (split on headings/sections) over fixed-size splitting when the source documents have clear structure.
- **Embeddings & indexing**: Pick an embedding model appropriate to the domain (general-purpose vs. code vs. multilingual). Note whether the vector store needs metadata filtering (e.g., by date, source, or user) alongside similarity search — this is often more impactful on quality than the embedding model choice itself.
- **Retrieval**: Default to hybrid retrieval (dense vector search + keyword/BM25) when precision matters, since pure embedding search misses exact-match terms (IDs, names, error codes). Consider a reranking step after initial retrieval if the top-k results are noisy.
- **Generation**: Keep the retrieved context clearly delimited in the prompt (e.g., with tags or headers) so the model can distinguish retrieved facts from instructions. Instruct the model explicitly to say when the retrieved context doesn't contain an answer, rather than letting it fabricate one.

### 3. If building an agent, design the loop explicitly

- Define the agent's available tools narrowly and give each one a precise description — vague tool descriptions are the most common cause of an agent picking the wrong tool.
- Decide up front whether the task needs a single agent with a tool loop, or genuinely benefits from multiple specialized agents (e.g., a researcher agent and a writer agent). Default to a single agent; only split into multiple agents when one agent's context or role would otherwise become unmanageably broad.
- Build in an explicit stop condition (max iterations, a "done" signal from the model, or a user-confirmation gate) so the agent loop can't run away.
- For agents that take real-world actions (file writes, API calls, purchases), separate "read/plan" steps from "act" steps, and confirm before irreversible actions.

### 4. Evaluate before declaring it done

Don't ship an LLM application on vibes. For RAG, assemble a small set of representative question/answer pairs (10-30 is enough to start) and check: does retrieval surface the right chunks, and does generation produce a correct, grounded answer from them? For agents, walk through several realistic task scenarios end-to-end, including ones where a tool call should fail or return nothing, and confirm the agent handles that gracefully rather than hallucinating a result. Treat "does it work on the happy path" and "does it degrade sensibly on the unhappy path" as two separate checks.

### 5. Iterate on the weakest link, not the whole system

When answer quality is poor, diagnose which stage is failing before changing code: retrieve the raw chunks returned for a failing query and inspect them directly. If the right information isn't in the retrieved chunks, the problem is retrieval (chunking, embedding, or search), not generation — no amount of prompt tuning fixes a generation step that never received the right context. If the right chunks are present but the answer is still wrong, the problem is prompt/generation, not retrieval.
