---
name: llm-platform-architect
description: Guides the design and review of LLM-powered application components (RAG pipelines, agent workflows, model routing, evaluation, and dataset management) for teams building an internal GenAI platform; use when a user is architecting, extending, or auditing a system that combines multiple LLM capabilities into one product.
---

# LLM Platform Architect

Helps design and review systems that combine several LLM-powered capabilities — retrieval-augmented generation (RAG), agent/workflow orchestration, model management, evaluation, and fine-tuning/dataset pipelines — into a single coherent internal platform, the way an enterprise GenAI devops platform would. Apply this skill when a user is building or extending a system that needs more than one of these capabilities to work together, not when they're building a single standalone LLM feature.

## When to apply this skill

- The user is designing or reviewing a platform that lets multiple teams build LLM-powered workflows (chatbots, agents, document Q&A) on shared infrastructure.
- The user needs to reason about how RAG, agents, evaluation, and model selection should compose rather than live as isolated features.
- The user is deciding how to manage multiple LLM providers/models, track datasets used for fine-tuning or evaluation, or add observability across many LLM call sites.
- The user asks for a review of an existing GenAI system's architecture and wants to know what's missing or over-built.

Do not apply this skill for a single, simple LLM call (e.g. "summarize this text") — that's not a platform-design question.

## Core areas to reason about

When helping with this kind of system, walk through these areas and call out which ones are actually relevant to the user's stated scope — most systems need only two or three of these, not all of them:

1. **Workflow/agent orchestration** — Is the system composing multiple LLM calls and tools into a graph (sequential steps, branching, loops, human-in-the-loop approval)? Identify the minimal orchestration primitive needed (a linear pipeline vs. a full agent loop vs. a DAG of steps) rather than defaulting to the most general one.

2. **RAG (retrieval-augmented generation)** — If the system needs to ground answers in documents: what's the ingestion path (parsing, chunking, embedding), what's the retrieval strategy (vector search, hybrid, reranking), and how is retrieved context fed back into the prompt. Flag when a simpler approach (full-document context, keyword search) would suffice instead of a vector database.

3. **Model management** — If more than one LLM/model is in play: how is routing decided (cost, latency, capability), how are credentials and provider configs kept out of application code, and how is a model swap tested before rollout.

4. **Evaluation** — Distinguish "does it run" checks (exit codes, schema validation, timeouts) from "is the output good" checks (LLM-as-judge, human review, golden datasets). Push for the cheapest check that would actually catch a real failure mode, and be explicit about which failures each check catches.

5. **Dataset management** — For any fine-tuning or evaluation dataset: where does it live, how is it versioned, and how is it kept separate from production user data (PII, licensing).

6. **Observability** — Whether individual LLM calls, agent steps, and evaluation results are logged somewhere a human can inspect after the fact, especially when something goes wrong in production.

7. **Enterprise/system management** — Access control, audit trail, and multi-tenant isolation, but only when the user's system actually serves multiple teams/customers — don't propose this for a single-team internal tool.

## Step-by-step approach

1. Ask (or infer from context) which of the seven areas above are actually in scope for the current task — resist the urge to design all seven at once.
2. For each in-scope area, identify the simplest mechanism that satisfies the actual requirement, and name a concrete alternative that would be over-engineering for this scale.
3. Check how the areas interact: e.g., does the evaluation step need to know which model version produced an answer (model management ↔ evaluation), or does the agent workflow need retrieval results logged for later audit (RAG ↔ observability).
4. Surface gaps explicitly rather than silently assuming coverage — e.g., "there's no dataset versioning here, so a fine-tune run can't be reproduced later."
5. When reviewing an existing system, prefer flagging missing guardrails (no eval before promoting a workflow change, no audit trail on who approved a prompt change) over proposing new features.
6. When proposing new capability, describe it in terms of the smallest working piece first (a single retrieval step, a single eval check, a single model route) and only add orchestration complexity once that piece is proven to work manually.
