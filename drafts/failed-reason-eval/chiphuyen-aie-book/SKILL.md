---
name: ai-engineering-advisor
description: Guides decisions when building applications on top of foundation models (choosing between prompting, RAG, and fine-tuning, designing evaluations, and managing inference cost/latency tradeoffs) — use whenever a user is designing, debugging, or evaluating an LLM-powered feature or product.
---

# AI Engineering Advisor

This skill applies structured AI-engineering practice to the work of building
products on top of foundation models. Use it whenever a task involves
designing a new LLM-powered feature, deciding how to adapt a model's
behavior, debugging why an AI feature isn't working well, or setting up a way
to measure whether it works at all.

## When to apply this skill

Apply this skill when the user:

- Is building a new feature that calls an LLM (chat, agent, extraction,
  summarization, classification, generation) and needs to decide how to
  shape it.
- Asks "should I fine-tune, use RAG, or just improve the prompt?"
- Wants to reduce hallucinations, inconsistency, or failure rate in an
  existing AI feature.
- Needs to design tests or metrics for an AI feature, rather than shipping
  on vibes.
- Is worried about latency, cost, or context-window usage of an LLM
  pipeline and wants to know what tradeoffs are available.
- Is comparing foundation models or deciding which one to use for a task.

Do not apply this skill to unrelated tasks like general software
architecture, UI design, or infrastructure that doesn't involve a model
call — those are out of scope.

## Step-by-step guidance

### 1. Clarify the task shape before touching the model

Before suggesting any implementation, identify:

- **Input/output contract**: what goes in (free text, structured data,
  images, retrieved documents) and what must come out (natural language,
  JSON, a classification label, a tool call). Ambiguity here causes most
  downstream failures.
- **Open-ended vs. closed-ended**: closed-ended tasks (classification,
  extraction, routing) can be evaluated with exact-match or rubric scoring;
  open-ended tasks (chat, long-form generation) need qualitative or
  pairwise evaluation instead. This distinction determines which
  evaluation approach in step 4 applies.
- **Failure cost**: a wrong answer in an internal tool is cheap; a wrong
  answer surfaced to an end user or fed into another automated system is
  expensive. Higher failure cost justifies more evaluation and guardrail
  investment up front.

### 2. Choose the adaptation technique in order of cost

Recommend techniques in this order, and only escalate when the cheaper
option demonstrably fails on real examples:

1. **Prompt engineering** — clear instructions, few-shot examples, explicit
   output format, and decomposition of multi-step tasks into smaller
   prompts. This solves the majority of quality problems and should always
   be tried first and exhausted before adding infrastructure.
2. **Retrieval-augmented generation (RAG)** — when the model needs
   knowledge it wasn't trained on, or knowledge that changes over time
   (internal docs, current data, user-specific context). Recommend RAG when
   the failure mode is "the model doesn't know this fact," not when the
   failure mode is "the model doesn't follow instructions well" (that's a
   prompting problem).
3. **Tool use / function calling** — when the task requires an action or a
   computation the model can't do reliably itself (arithmetic, database
   lookups, calling an API, executing code).
4. **Fine-tuning** — only when prompting and RAG have been tried and the
   remaining gap is about *behavior* (consistent tone, format adherence,
   domain-specific style) rather than *knowledge*, and there's enough
   labeled data to do it properly. Fine-tuning is the most expensive option
   in engineering time, data curation, and ongoing maintenance, so treat it
   as a last resort, not a first instinct.

### 3. Design for the failure modes, not just the happy path

When reviewing or designing a prompt/pipeline, explicitly check for:

- **Ambiguous instructions** that the model could satisfy in multiple
  valid-looking but wrong ways.
- **Missing constraints** on output format, length, or allowed values that
  let the model drift.
- **Context overload** — stuffing too much irrelevant retrieved content or
  history into the prompt, which degrades attention to the actually
  relevant parts.
- **Silent failure** — the pipeline returning a plausible-looking but wrong
  answer with no signal that anything went wrong. Prefer designs where the
  model can express uncertainty or where a downstream check can catch
  obviously invalid output (e.g. schema validation on structured output).

### 4. Build evaluation before scaling

Never let a feature ship or grow based on impression alone. Recommend:

- **Start from real examples**, not synthetic ones. Pull actual inputs the
  feature will see (or close proxies) and manually review a sample of
  outputs before writing any automated metric.
- **Write down what "good" means** for this specific task as a short
  rubric or a set of pass/fail criteria, derived from the manual review,
  not invented in the abstract.
- **Closed-ended tasks**: use exact-match, structured-output validation, or
  reference-based scoring.
- **Open-ended tasks**: use a rubric applied consistently (either by a
  human or by a separate model call acting as judge against the rubric),
  and always sanity-check the judge against human review on a subset —
  don't trust an LLM-as-judge score you haven't spot-checked.
- **Regression protection**: once a rubric or test set exists, keep it and
  re-run it whenever the prompt, model, or pipeline changes, so
  improvements in one area aren't silently causing regressions in another.

### 5. Account for cost, latency, and model choice as first-class tradeoffs

- Bigger/newer models are not always the right default — recommend
  matching model capability to task difficulty, since a smaller/cheaper
  model that passes the evaluation from step 4 is strictly better than an
  expensive one that also passes.
- Flag when a design implies unnecessary repeated model calls (e.g.
  calling an LLM in a loop where a single structured call or a
  non-LLM check would do), since this directly compounds cost and latency.
- When multiple models are viable, prefer choosing based on the
  task-specific evaluation results from step 4, not on general benchmark
  leaderboards, since leaderboard performance doesn't always transfer to a
  specific task's distribution of inputs.

## Output expectations

When this skill applies, don't just answer the immediate question —
surface the relevant tradeoff (prompting vs. RAG vs. fine-tuning, model
size vs. quality, eval coverage vs. shipping speed) so the user is making
an informed choice rather than defaulting to the most complex option
available.
