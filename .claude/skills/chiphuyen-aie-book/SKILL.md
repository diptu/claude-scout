---
name: ai-engineering-practices
description: Apply structured AI engineering practices (model selection, evaluation design, prompt engineering, RAG/agent architecture, and inference optimization) when building or reviewing LLM-powered features; use whenever a user is designing, building, evaluating, or debugging an application that calls a foundation model.
---

# AI Engineering Practices

This skill helps Claude reason like an AI engineer building production systems on top of foundation models, rather than treating LLM calls as a black box. Apply it whenever the user is designing a new LLM-powered feature, choosing between models or architectures, building an evaluation pipeline, writing prompts, designing a RAG or agent system, or debugging why an AI feature behaves unpredictably.

## When to apply this skill

- The user is building a feature that calls an LLM (chat, summarization, extraction, classification, agents, RAG).
- The user is choosing a model, deciding on architecture (RAG vs. fine-tuning vs. prompting), or optimizing cost/latency.
- The user wants to know if their AI feature "actually works" or needs an evaluation approach.
- The user is debugging inconsistent, hallucinated, or low-quality LLM outputs.
- The user is designing prompts, tool definitions, or context/retrieval pipelines.

## Core workflow

### 1. Clarify the task shape before picking a solution

Before recommending a model or architecture, identify:
- **Input/output shape**: open-ended generation, classification, extraction, multi-turn conversation, or agentic tool use.
- **Constraints**: latency budget, cost ceiling, data sensitivity (can data leave the user's infra?), and whether outputs need to be deterministic/auditable.
- **Failure cost**: what happens when the model is wrong — a wrong chatbot reply is cheap to recover from, a wrong medical or financial output is not. This determines how much evaluation and guardrail investment is justified.

### 2. Prefer the simplest architecture that could work

Default ordering, from cheapest to most expensive to build and maintain:
1. **Prompt engineering** on a strong general-purpose model — start here always.
2. **Retrieval-augmented generation (RAG)** when the model needs facts or context it wasn't trained on, or that change over time (docs, user data, recent events). RAG beats fine-tuning for knowledge injection because it's easier to update and audit.
3. **Tool use / agents** when the task requires taking actions or looking up live information, not just generating text.
4. **Fine-tuning** only when prompting and RAG have been tried and fall short on a specific, measurable dimension (format compliance, latency via smaller model, domain-specific style). Fine-tuning is expensive to iterate on and doesn't fix retrieval or reasoning gaps — don't reach for it first.

Don't recommend a heavier architecture until the lighter one has been tried and shown to be insufficient on the actual data.

### 3. Design evaluation before writing prompts

Treat "does it work" as a measurement problem, not a feeling:
- Define what "correct" means for this specific task — factual accuracy, format compliance, tone, refusal behavior, or some combination. Vague tasks need a rubric before they need a prompt.
- Build a small evaluation set (even 10-20 realistic examples, including edge cases and known failure modes) before iterating on prompts. Iterating on vibes without a fixed eval set causes regressions that go unnoticed.
- Separate two kinds of evaluation:
  - **Does it run** — output parses, respects format, doesn't error or time out.
  - **Is it good** — factually correct, relevant, safe, matches the intended tone. This second kind usually requires either human review, a reference answer to compare against, or a separate "judge" model call — and judge-model evaluations should themselves be spot-checked against human judgment, since judges inherit the same failure modes as the model being judged.
- When using an LLM as a judge, give it the same rubric a human reviewer would use, show it examples of good/bad outputs if possible, and prefer pairwise comparison (A vs. B) over absolute scoring when consistency matters.

### 4. Write prompts as engineering artifacts, not one-off text

- State the task, the output format, and constraints explicitly and early in the prompt — don't bury instructions after long context.
- Give few-shot examples when the desired output format or style is hard to describe abstractly.
- Separate untrusted data from instructions clearly (e.g., delimiters or tags) whenever a prompt includes user-supplied or third-party content, so the model doesn't treat that content as instructions.
- Keep prompts under version control and treat prompt changes like code changes: test against the evaluation set before shipping.

### 5. Design retrieval and context deliberately (for RAG)

- Chunking, retrieval, and ranking quality usually matter more than the generation model choice — debug retrieval first when RAG answers are wrong.
- Keep retrieved context focused: irrelevant or excessive context degrades output quality even on long-context models, it doesn't just cost more tokens.
- Make retrieval failures visible (log what was retrieved) so quality issues can be traced to "found the wrong context" vs. "had the right context but reasoned poorly about it."

### 6. Watch cost and latency as first-class constraints

- Larger/more capable models aren't always the right default — match model size to task difficulty, and measure whether a smaller/cheaper model meets the quality bar before defaulting to the largest available.
- Cache repeated or templated portions of prompts where the underlying platform supports it, and batch or stream where latency budgets allow.
- Treat inference cost as a per-feature budget line, not an afterthought — a feature that's cheap in prototyping can become the dominant cost at scale.

### 7. Close the loop with production feedback

- Real user interactions (thumbs up/down, corrections, escalations) are the highest-signal evaluation data available — feed them back into the evaluation set rather than relying only on the initial hand-built set.
- When a production failure is found, add it to the evaluation set immediately so the same regression can't silently reappear.
