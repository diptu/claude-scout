---
name: agentic-runtime-design
description: Guides Claude through designing or reviewing a production-grade runtime for AI agents — covering modularity, security boundaries, deployment portability, and observability — for use when a user is building or hardening a system that runs autonomous or tool-using AI agents.
---

# Agentic Runtime Design

This skill helps with designing, reviewing, or hardening the runtime layer that
executes AI agents — the code that manages an agent's tool calls, model
invocations, state, and connections to external systems. Apply it when a user
is building an agent framework or platform (not a single agent script), asking
how to make agent execution production-ready, or reviewing an existing agent
runtime for gaps in modularity, security, or portability.

## When to apply this skill

- The user is building infrastructure that runs multiple agents or agent
  types, not a one-off script calling an LLM.
- The user asks about deploying agents across different environments (local
  dev, cloud, edge/on-prem) and wants the same agent logic to work in all of
  them.
- The user is designing how an agent accesses tools, secrets, storage, or
  external APIs and wants to avoid tightly coupling agent logic to a specific
  vendor or environment.
- The user is reviewing an agent system for production-readiness: secrets
  handling, sandboxing, logging, error recovery, or multi-tenant isolation.

## Core design principles to apply

1. **Separate agent logic from infrastructure.** The code that defines what an
   agent does (its prompts, tool selection, reasoning loop) should not
   directly import a specific database driver, cloud SDK, or vector store
   client. Introduce a thin interface (storage, model access, logging, secrets)
   between agent logic and the concrete backend, so the same agent definition
   can run against different backends by swapping an implementation, not by
   editing the agent.

2. **Make components swappable, not hardcoded.** Model provider, vector
   storage, conversation/session storage, and secret storage are the four
   components most likely to change between a developer's laptop and a
   production deployment. When designing or reviewing a runtime, check that
   each of these is behind an interface with at least a local/in-memory
   implementation and a production implementation, rather than one
   implementation baked into agent code.

3. **Treat the deployment target as a runtime configuration, not a rewrite.**
   A well-designed agent runtime should let the same agent run as a local CLI
   process, a long-running server, or inside a container/edge device by
   changing configuration (which backend implementations are wired in) rather
   than changing the agent's own code. When reviewing a design, flag any place
   where "how do I deploy this elsewhere?" would require touching agent logic.

4. **Isolate what an agent can reach.** An agent runtime should enforce
   explicit boundaries on what tools, data, and network endpoints a given
   agent instance can access — don't let agent code reach arbitrary
   filesystem paths, arbitrary URLs, or shared secrets by default. When
   reviewing a runtime, check that tool/resource access is allow-listed per
   agent or per task rather than globally available, and that credentials for
   different backends are scoped and not shared across unrelated agents.

5. **Build in observability from the start.** Every agent run should produce
   a traceable record of which model calls were made, which tools were
   invoked with what arguments, and what the outcome was. When designing a
   runtime, recommend logging each step of the agent's reasoning/tool loop
   with enough detail to debug a failure after the fact, not just the final
   output.

6. **Plan for partial failure.** Tool calls, model calls, and external APIs
   will time out or error. A production agent runtime needs a defined
   behavior for retrying, falling back, or surfacing the failure to the
   caller — don't let a single failed tool call silently corrupt agent state
   or hang the process indefinitely.

## How to apply these steps

When a user brings a concrete agent system to design or review:

1. Identify the agent logic (prompts, decision loop, tool selection) and list
   every place it currently touches a concrete backend (a specific database,
   cloud service, or SDK call) directly.
2. For each of those touchpoints, propose or evaluate an interface boundary:
   what's the minimal contract (methods/inputs/outputs) agent logic needs from
   that component, independent of which backend implements it.
3. Check the four commonly-hardcoded components (model provider, vector
   storage, session storage, secrets) specifically, since they're the most
   common source of environment lock-in.
4. Walk through what changes if this system needs to run in a second
   environment (e.g. moving from local dev to cloud, or cloud to edge). If the
   answer involves editing agent logic rather than swapping a configured
   backend, flag it as a design gap.
5. Review access boundaries: what can each agent reach (tools, files,
   network, secrets), and is that scoped explicitly or implicitly open.
6. Review failure handling and logging for the tool-call/model-call loop, and
   recommend concrete logging points or retry/fallback behavior where missing.
7. Summarize findings as a short list of concrete gaps and fixes, prioritized
   by which ones block moving from a working prototype to something safe to
   run in production.
