---
name: llm-devops-platform-design
description: Guides Claude through designing or reviewing an internal LLM application platform (workflow orchestration, RAG, agents, model management, evaluation, fine-tuning, observability) as one cohesive system; use when a user is building enterprise-grade GenAI infrastructure rather than a single point solution.
---

# LLM DevOps Platform Design

This skill helps design, review, or extend an internal platform for building and
operating LLM-powered applications at organizational scale — the kind of system
that needs to support many teams, many use cases, and a full lifecycle from
prototyping to production, rather than a single script or app calling an LLM
API.

## When to apply this skill

Apply this skill when the user's request involves more than one of the
following, or explicitly asks for a "platform," "internal tool," or
"devops layer" for LLM work:

- Building a visual or config-driven workflow/pipeline builder for chaining
  LLM calls, tools, and data sources.
- Standing up retrieval-augmented generation (RAG) infrastructure (ingestion,
  chunking, embedding, vector storage, retrieval tuning).
- Designing or orchestrating agents that call tools, other agents, or
  external systems.
- Managing multiple LLM providers/models behind one interface (routing,
  fallback, cost/latency tracking, credential management).
- Building evaluation harnesses to score model or pipeline outputs.
- Preparing datasets for supervised fine-tuning (SFT) or managing dataset
  versions.
- Adding enterprise concerns: role-based access control, multi-tenant
  isolation, audit logging, approval workflows.
- Adding observability: tracing LLM calls, logging prompts/responses,
  tracking token usage and cost, alerting on failures or drift.

Do not apply this skill to a one-off script that calls an LLM API directly
for a single task — that doesn't need platform-level structure. Reserve it
for genuinely multi-component, multi-team, or long-lived systems.

## Step-by-step guidance

1. **Clarify scope before designing.** Ask (or infer from context) which of
   the seven capability areas above are actually in scope for this request.
   Do not propose building all of them if the user only needs one — treat
   each as an independently useful module, not a package deal.

2. **Separate the pipeline/workflow layer from the model layer.** Design the
   part that defines *what steps run in what order* (prompts, retrieval
   steps, tool calls, branching logic) independently from *which model or
   provider executes each step*. This lets the user swap models or add
   providers without redesigning workflows, and swap workflows without
   touching model configuration.

3. **For RAG components**, design ingestion, chunking, and retrieval as
   distinct stages with their own configuration (chunk size/overlap,
   embedding model, retrieval top-k, reranking). Make retrieval quality
   independently testable from generation quality — a bad answer might be a
   retrieval problem or a generation problem, and conflating them makes
   debugging much harder.

4. **For agent orchestration**, define each agent's available tools, its
   termination/handoff conditions, and what happens on tool failure, before
   writing prompts. Keep agent definitions declarative (a config or spec)
   rather than hard-coded control flow where possible, so non-engineers can
   adjust behavior without code changes.

5. **For model management**, centralize provider credentials and model
   selection behind one interface so callers request a model by role
   ("fast/cheap," "high-quality," "long-context") rather than by
   provider-specific name. Track which model actually served each request
   for cost and debugging purposes.

6. **For evaluation**, distinguish two kinds of checks and don't conflate
   them: mechanical checks (did it run, did it error, is the output
   well-formed) versus quality checks (is the output actually good, judged
   by a human, a rubric, or a second model). Build the mechanical checks
   first; they're cheap and catch most regressions. Only add quality
   judging where the user has explicitly asked for it — don't default to
   LLM-as-judge everywhere just because it's available.

7. **For SFT/dataset management**, keep raw collected data, curated/cleaned
   training data, and versioned training-ready datasets in clearly separate
   stages so a bad curation pass doesn't corrupt the raw source, and so
   training runs are reproducible against a specific dataset version.

8. **For enterprise/system management concerns** (RBAC, multi-tenancy, audit
   logs, approvals), treat these as cross-cutting layers that wrap the
   capabilities above rather than features of any single module — e.g. an
   audit log should capture events from the workflow engine, the agent
   layer, and the model layer uniformly, not be reimplemented per module.

9. **For observability**, ensure every LLM call (whether from a workflow,
   an agent, or a direct API call) is traceable back to: which
   user/tenant/workflow triggered it, which model served it, what it cost,
   how long it took, and whether it succeeded. Build this as a shared
   concern injected at the model-management layer (step 5) rather than
   added ad hoc in each component, so nothing gets missed.

10. **Favor incremental delivery.** Recommend building and validating one
    capability end-to-end (e.g., a single RAG pipeline in production) before
    generalizing it into a reusable platform module. A platform built ahead
    of real usage tends to guess wrong about what needs to be configurable.

## Output guidance

When asked to design such a system, produce a concrete component breakdown
(what each layer does, its inputs/outputs, and its boundaries with adjacent
layers) rather than an abstract architecture diagram description. When asked
to implement part of it, implement only the requested module and make its
interface to the other layers explicit, so the rest of the platform can be
added later without rework.
