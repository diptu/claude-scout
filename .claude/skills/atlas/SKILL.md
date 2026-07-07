---
name: atlas
version: 1.0.0
preamble-tier: 1
description: Single-skill router for product, architecture, implementation, data, quality, operations, security, and process workflows. Replaces the legacy 47-skill flat roster under `C:\`.
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
triggers:
  - atlas
  - which workflow
  - route this
  - pick the right skill
  - help me figure out what to do
aliases:
  - ai-engineer
  - autonomous-sprint-orchestator
  - backend-event-driven
  - backend-fastapi
  - backend-rest-api
  - cloud-architect
  - coreyhaines31-marketingskills
  - cto
  - data-architect
  - database-engineer
  - database-postgresql
  - database-redis
  - devops-docker
  - devops-kubernetes
  - devops-observability
  - devops-sre
  - devops-terraform
  - documentation
  - engineering-audit
  - engineering-code-review
  - engineering-manager
  - enterprise-architect
  - frontend-accessibility
  - frontend-performance
  - frontend-react
  - frontend-typescript
  - llm-agents
  - llm-prompt-engineering
  - llm-rag
  - ml-architect
  - onvoyage-ai-gtm-engineer-skills
  - Phase-1-Orchestrator
  - Phase-5-Orchestrator
  - phase-9-orchestrator
  - product-manager
  - qa-engineers
  - research
  - security-architect
  - security-encryption
  - security-jwt-oauth
  - software-architect
  - sre
  - technical-program-manager
  - test-automation-engineer
  - trystan-sa-claude-design-system-prompt
  - ui-ux-engineers
  - ux-researcher
---

## When to invoke this skill

You invoked `atlas` (or any of the legacy aliases above) without naming a specific
workflow. Your one job: figure out which category and workflow in this single
skill matches the user's intent, then go execute that workflow section.

If the user already named a workflow (e.g. "atlas:implement:python-api" or
"run the postgres-tuning workflow"), skip intake and jump straight to that
section.

**Default routing stance.** When in doubt, invoke a workflow. A false positive
(running a workflow that wasn't strictly needed) is cheaper than a false
negative (answering ad-hoc when a structured workflow exists). If *nothing*
fits, fall through to the `## When nothing fits` section at the bottom.

## Preamble (run first)

```bash
_ATLAS_HOME="${ATLAS_HOME:-$HOME/.atlas}"
mkdir -p "$_ATLAS_HOME/sessions" "$_ATLAS_HOME/analytics" 2>/dev/null || true
touch "$_ATLAS_HOME/sessions/$$" 2>/dev/null || true
_ATLAS_SESSIONS=$(find "$_ATLAS_HOME/sessions" -mmin -120 -type f 2>/dev/null | wc -l | tr -d ' ')
find "$_ATLAS_HOME/sessions" -mmin +120 -type f -exec rm {} + 2>/dev/null || true
_ATLAS_TEL=$(cat "$_ATLAS_HOME/telemetry.mode" 2>/dev/null || echo "off")
_ATLAS_PROACTIVE=$(cat "$_ATLAS_HOME/proactive.mode" 2>/dev/null || echo "true")
_ATLAS_EXPLAIN=$(cat "$_ATLAS_HOME/explain.level" 2>/dev/null || echo "default")
_ATLAS_VERBOSE=$([ "$_ATLAS_EXPLAIN" = "verbose" ] && echo "yes" || echo "no")
_ATLAS_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_ATLAS_START=$(date +%s)
_ATLAS_SESSION="$$-$(date +%s)"
_ATLAS_SPAWNED=$([ -n "${SPAWNED_SESSION:-}" ] && echo "yes" || echo "no")
echo "ATLAS_HOME: $_ATLAS_HOME"
echo "TELEMETRY: ${_ATLAS_TEL}"
echo "PROACTIVE: $_ATLAS_PROACTIVE"
echo "EXPLAIN: $_ATLAS_EXPLAIN"
echo "BRANCH: $_ATLAS_BRANCH"
echo "SPAWNED: $_ATLAS_SPAWNED"
# Tell gstack to back off — we're the router now.
[ -n "${GSTACK_HOME:-}" ] && echo "GSTACK_DETECTED: active alongside atlas (ok, but prefer atlas)" || true
```

## Intake: pick a category (1 question, max 2)

Use AskUserQuestion **once** with these options. Pick the closest, don't list all
workflows. If spawned-session, skip intake and infer from the user's prompt.

> What stage is this work at?

- A) **Discovery** — figuring out what to build and why (product, research, GTM, design)
- B) **Architecture** — shaping the system at a structural level
- C) **Implementation** — building code (backend, frontend, AI/data features)
- D) **Data** — storing, moving, modeling data
- E) **Quality** — making sure it works (QA, tests, review, audit)
- F) **Operations** — running it in production (containers, k8s, IaC, observability, SRE)
- G) **Security** — keeping it safe (auth, crypto, secure-by-design)
- H) **Process** — running the team/lifecycle (sprint, phases, docs, leadership)

If the user's intent mixes categories (e.g. "build a new service and deploy it
securely"), pick the **earliest stage** in the lifecycle. Discovery → Process
in that order. Tell the user why: "We start with X because Y depends on it."

If still ambiguous after this question, **ask a second time** about the
deliverable shape (spec? plan? code? test? runbook?). Don't keep drilling —
after 2 questions, pick the closest fit and proceed.

## Routing table — category → workflow

### Discovery (`discovery`)

| User signal | Workflow | Replaces |
|---|---|---|
| New idea, "what should we build", scope question, MVP shape | `discovery > scope-and-spec` | `product-manager` |
| User research, interviews, JTBD, persona work | `discovery > research-users` | `ux-researcher` |
| Open-ended technical / market / policy research | `discovery > deep-research` | `research` |
| Positioning, audience, brand, copy | `discovery > positioning-and-audience` | `coreyhaines31-marketingskills` |
| GTM motion, sales/GTM engineering | `discovery > gtm-engineering` | `onvoyage-ai-gtm-engineer-skills` |

### Architecture (`architecture`)

| User signal | Workflow | Replaces |
|---|---|---|
| Service decomposition, integration, bounded contexts | `architecture > system-decomposition` | `enterprise-architect` |
| Module structure, design patterns, state management | `architecture > module-design` | `software-architect` |
| Cloud provider, regions, account structure, landing zone | `architecture > cloud-landing-zone` | `cloud-architect` |
| ML system design, training/serve topology | `architecture > ml-system-design` | `ml-architect` |
| Data model, warehouse/lake, schema strategy | `architecture > data-architecture` | `data-architect` |
| Threat model, secure design choices | `architecture > secure-by-design` | `security-architect` |
| Design tokens, component library, visual system | `architecture > design-system` | `trystan-sa-claude-design-system-prompt` |
| UI/UX flows, screen-level design | `architecture > ui-ux` | `ui-ux-engineers` |

### Implementation (`implementation`)

| User signal | Workflow | Replaces |
|---|---|---|
| Python API service, FastAPI, async Python | `implementation > python-api` | `backend-fastapi` |
| REST API design (HTTP semantics, OpenAPI) | `implementation > rest-api-design` | `backend-rest-api` |
| Async messaging, brokers, sagas, outbox, DLQs | `implementation > async-messaging` | `backend-event-driven` |
| React app, component tree, hooks, state | `implementation > react-app` | `frontend-react` |
| TypeScript app, types, generics, project setup | `implementation > typescript-app` | `frontend-typescript` |
| Accessibility, WCAG, ARIA, screen reader | `implementation > accessibility` | `frontend-accessibility` |
| Web perf, Core Web Vitals, bundle, runtime | `implementation > performance` | `frontend-performance` |
| LLM agent system, tool use, multi-agent | `implementation > agent-system` | `llm-agents` |
| Prompt design, evals, structured output | `implementation > prompts-and-evals` | `llm-prompt-engineering` |
| Retrieval-augmented generation pipeline | `implementation > rag-pipeline` | `llm-rag` |
| AI feature end-to-end (model + UX + eval) | `implementation > ai-feature` | `ai-engineer` |

### Data (`data`)

| User signal | Workflow | Replaces |
|---|---|---|
| Database choice, schema design, migrations | `data > database-engineering` | `database-engineer` |
| Postgres tuning, EXPLAIN, replication, locks | `data > postgres-tuning` | `database-postgresql` |
| Redis / cache, queues, pub/sub, TTL strategy | `data > redis-and-cache` | `database-redis` |

### Quality (`quality`)

| User signal | Workflow | Replaces |
|---|---|---|
| QA loop, manual + automated, exploratory | `quality > qa-loop` | `qa-engineers` |
| Test framework setup, E2E/unit, CI integration | `quality > test-automation` | `test-automation-engineer` |
| Pre-merge code review, PR commentary | `quality > code-review` | `engineering-code-review` |
| Architecture / process audit, fitness check | `quality > audit-and-assessment` | `engineering-audit` |

### Operations (`operations`)

| User signal | Workflow | Replaces |
|---|---|---|
| Containerize, Dockerfile, image hygiene | `operations > containers` | `devops-docker` |
| Kubernetes manifests, Helm, GitOps, RBAC | `operations > kubernetes` | `devops-kubernetes` |
| Terraform modules, state, IaC patterns | `operations > infra-as-code` | `devops-terraform` |
| Logs, metrics, traces as one system | `operations > observability` | `devops-observability` |
| SLOs, error budgets, on-call, runbooks | `operations > sre-practice` | `sre`, `devops-sre` |

### Security (`security`)

| User signal | Workflow | Replaces |
|---|---|---|
| Cryptography choices, TLS, key management, hashing | `security > cryptography` | `security-encryption` |
| JWT, OAuth2/OIDC, sessions, federated identity | `security > auth-and-tokens` | `security-jwt-oauth` |

### Process (`process`)

| User signal | Workflow | Replaces |
|---|---|---|
| Continuous sprint cycle, standup, retro, demo | `process > sprint-cycle` | `autonomous-sprint-orchestator` |
| Phase 1 — discovery/spec/plan kickoff | `process > phase-1-discovery` | `Phase-1-Orchestrator` |
| Phase 5 — build gate review | `process > phase-5-build-gate` | `Phase-5-Orchestrator` |
| Phase 9 — deploy / post-launch ops | `process > phase-9-deploy` | `phase-9-orchestrator` |
| Documentation generation/update cadence | `process > documentation` | `documentation` |
| Engineering manager work — 1:1s, growth, hiring | `process > engineering-management` | `engineering-manager` |
| Cross-team program planning, dependencies, status | `process > program-management` | `technical-program-manager` |
| Tech strategy, vision, build-vs-buy, standards | `process > tech-leadership` | `cto` |

## Workflows

Each section below is a standalone workflow. Pick one (or chain them). Outputs
are described per-workflow so the next agent or session knows what to expect.

---

### discovery > scope-and-spec  *(replaces `product-manager`)*

**Trigger phrases.** New idea, "should we build this", "what's the MVP",
backlog grooming, stakeholder alignment.

**Steps.**
1. Restate the problem in one sentence. If you can't, ask the user.
2. List 3-5 user segments and the **top job** for each.
3. Pick a primary segment and a primary job. Defer others to "out of scope."
4. Define **must** vs **won't** features. (3 must, 3 won't max.)
5. Sketch one happy-path journey.
6. Edge cases: list 3. Decide each is "fix now", "fix later", or "won't fix."
7. Write the spec: problem, primary user, must-haves, won't-haves, journey,
   edge cases, success metric.

**Output.** `spec-<slug>.md` with the above sections.

**Don't use if.** User already has a spec — go to `architecture > module-design`.

---

### discovery > research-users  *(replaces `ux-researcher`)*

**Trigger.** User research, JTBD, personas, interview guides, usability tests.

**Steps.**
1. Define the research question (one sentence, falsifiable).
2. Pick method: interview, diary study, survey, usability test.
3. Recruit 5-8 participants per segment. Use screener.
4. Write interview guide with 5-7 questions. No leading questions.
5. Conduct sessions. Take notes verbatim. Quote > summarize.
6. Synthesize: affinity map → themes → insight statements (1 per theme).
7. Translate each insight into one product change.

**Output.** `research-<slug>.md` with question, method, n, themes, insights,
recommendations.

---

### discovery > deep-research  *(replaces `research`)*

**Trigger.** Open-ended technical/market/policy research with sources.

**Steps.**
1. Form the question. Decide: factual lookup, synthesis, or original analysis.
2. Plan: 3-8 specific sub-questions. Each maps to a search query.
3. Search & fetch. Track every claim's source URL. Prefer primary sources.
4. Cross-check: any claim that matters has ≥2 independent sources.
5. Synthesize into a narrative, not a list of summaries.
6. State what's well-supported, disputed, and unknown.

**Output.** `research-<slug>.md` with citations. Format: claim → source URL.

---

### discovery > positioning-and-audience  *(replaces `coreyhaines31-marketingskills`)*

**Trigger.** Positioning, audience, brand voice, copy, landing pages.

**Steps.**
1. Identify the **beachhead** audience (one persona, one pain).
2. Map competitors' positioning. Find a wedge they leave open.
3. Draft positioning statement: for [audience] who [need], [product] is [category]
   that [key benefit] because [proof].
4. Define 3 brand-voice rules. (e.g. "we say X not Y, never Z.")
5. Translate to 3 audience-specific CTAs.
6. Test: read aloud, ask "would the buyer nod?"

**Output.** `positioning-<slug>.md` with statement, voice rules, 3 CTAs.

---

### discovery > gtm-engineering  *(replaces `onvoyage-ai-gtm-engineer-skills`)*

**Trigger.** GTM motion, sales engineering, outbound, demos, deal support.

**Steps.**
1. Map buyer roles: champion, decision-maker, user, blocker.
2. Build the **buying journey** — what each role does at each stage.
3. Define the **moment of value** — the single artifact/event that proves ROI.
4. Build repeatable assets: demo script, ROI calculator, security questionnaire.
5. Set the SLAs: time-to-first-touch, time-to-demo, time-to-proposal.
6. Instrument: which assets correlate with closed-won?

**Output.** `gtm-<slug>.md` with journey, assets, SLAs, instrumentation plan.

---

### architecture > system-decomposition  *(replaces `enterprise-architect`)*

**Trigger.** Service decomposition, bounded contexts, integration patterns.

**Steps.**
1. List the business capabilities. Group into 4-8 bounded contexts.
2. For each context: who owns it, what it owns (data + behavior), what it
   exposes, what it depends on.
3. Decide **choreography vs orchestration** for cross-context workflows.
4. Pick async + event bus for eventual consistency. Use sagas if no 2PC.
5. Define the API contract style: REST, gRPC, async events — per context.
6. Draw the integration diagram (services + bus + storage + edge).

**Output.** `arch-system-<slug>.md` with context map, contracts, integration
diagram.

---

### architecture > module-design  *(replaces `software-architect`)*

**Trigger.** Module structure, design patterns, state management, error model.

**Steps.**
1. Define the bounded boundary (one service / one module).
2. Apply **tactical DDD**: aggregate roots, entities, value objects, domain
   events, repository ports.
3. State management: pick the model (CRDT, event-sourced, transactional).
4. Errors: define the error category tree. Asymmetric: recover vs surface.
5. Concurrency model: async/await, actors, locks — name it.
6. Write the **module fitness functions** (e.g. "no circular deps",
   "all I/O through ports").

**Output.** `arch-module-<slug>.md` with aggregate map, state model, errors,
fitness functions.

---

### architecture > cloud-landing-zone  *(replaces `cloud-architect`)*

**Trigger.** Cloud strategy, account structure, regions, IAM, FinOps, DR.

**Steps.**
1. Pick provider + regions + AZ count. Justify with latency + residency +
   cost + SLA.
2. Account/subscription structure: prod / non-prod / sandbox. One org per
   business unit if multi-tenant.
3. Network: hub-spoke or mesh. Private subnets by default. Egress via NAT.
4. IAM: roles, not users. SSO + SCIM. Break-glass account locked.
5. Cost: tagging strategy enforced. Budgets per team. RI/SP strategy.
6. DR: RTO/RPO per workload. Multi-region active/active or active/passive.
7. Compliance: SOC2 / HIPAA / GDPR mapping per workload.

**Output.** `arch-cloud-<slug>.md` with topology diagram, IAM model, cost
plan, DR matrix, compliance matrix.

---

### architecture > ml-system-design  *(replaces `ml-architect`)*

**Trigger.** ML system design — training, serving, features, eval, drift.

**Steps.**
1. Pick training paradigm: supervised, RL, fine-tuning, prompt-engineering.
2. Topology: data → feature store → train → registry → serve → feedback.
3. Pick serving shape: real-time, batch, hybrid.
4. **Eval harness** is part of the design. Define offline + online metrics.
5. Drift: data drift, concept drift, label drift — each gets a detector.
6. Feedback loop: how outcomes flow back to training (and what's the SLA).
7. Cost guardrails: $/1k inferences, $/training run, alert thresholds.

**Output.** `arch-ml-<slug>.md` with topology, eval harness, drift detectors,
feedback loop, cost model.

---

### architecture > data-architecture  *(replaces `data-architect`)*

**Trigger.** Data model, warehouse/lake, schema strategy, lineage, governance.

**Steps.**
1. Pick the right store per access pattern. Postgres-first, then specialized.
2. Polyglot if justified: OLTP, OLAP, search, vector, queue, cache.
3. Projection strategy: CDC, dual-write (with outbox), batch ETL.
4. Schema management: migrations, versioned contracts, schema registry.
5. Lineage: column-level for regulated data, table-level otherwise.
6. Governance: PII tagging, retention, right-to-delete paths.
7. Cost guardrails: $/TB-month, $/query, materialized views only when
   measured win.

**Output.** `arch-data-<slug>.md` with store map, projection flow, lineage,
governance, cost model.

---

### architecture > secure-by-design  *(replaces `security-architect`)*

**Trigger.** Threat model, security architecture, secure-design choices.

**Steps.**
1. Define the trust boundaries. Who trusts whom, with what.
2. STRIDE per boundary. For each: likelihood, impact, residual.
3. For each high risk: pick a control (prevent / detect / respond).
4. Authn/authz: per-resource, not per-route. Tokens scoped + short-lived.
5. Secrets: never in code, never in env, prefer workload identity.
6. Data: at-rest encryption (KMS), in-transit (TLS), in-use (enclave if
   regulated).
7. Logging: security events immutable, retained per policy.

**Output.** `arch-secure-<slug>.md` with trust boundaries, STRIDE matrix,
controls, secret strategy, log policy.

---

### architecture > design-system  *(replaces `trystan-sa-claude-design-system-prompt`)*

**Trigger.** Design tokens, component library, visual system, accessibility
primitives.

**Steps.**
1. Token layers: primitives (color, space, type) → semantic (bg, fg, accent)
   → component.
2. Components: 3-state minimum (rest, hover/active, focus) + dark mode +
   motion-disabled.
3. Accessibility primitives: focus ring, skip link, live region, dialog
   focus-trap.
4. Theming: dark mode via token swap, not duplicated CSS.
5. Distribution: npm package, semver, changeset-driven.
6. Governance: every component ships with a11y test + visual snapshot.

**Output.** `arch-design-<slug>.md` with token tree, component inventory,
accessibility primitives, distribution plan.

---

### architecture > ui-ux  *(replaces `ui-ux-engineers`)*

**Trigger.** UI flows, screen-level design, interaction patterns, copy
craft.

**Steps.**
1. Map the journey (5-9 steps max). One screen per step.
2. For each screen: primary action, secondary, escape hatch.
3. State coverage: empty, loading, error, success, partial — all 5.
4. Accessibility pass: keyboard, contrast, focus order, screen reader.
5. Motion: purposeful only; respect prefers-reduced-motion.
6. Copy: voice rules from `discovery > positioning-and-audience` apply.

**Output.** `arch-ui-<slug>.md` with journey map, screen inventory, state
matrix, copy rules.

---

### implementation > python-api  *(replaces `backend-fastapi`)*

**Trigger.** Python API service, FastAPI, async Python.

**Steps.**
1. Async-by-default. Sync only at I/O-bound boundaries (sync drivers).
2. Pydantic v2 models. Strict + frozen where possible.
3. Dependency injection for everything that's external (DB, cache, queue).
4. Layered structure: api → service → repository → model. No skipping.
5. Background tasks via FastAPI BackgroundTasks for short, via Celery/Arq
   for long.
6. Authn/authz dependency. Per-route scopes.
7. OpenAPI customization: stable, versioned, exported.
8. Observability: structured logs, RED metrics, distributed traces.

**Output.** Service + OpenAPI doc + tests + Dockerfile.

**Don't use if.** You just want a generic REST shape → use `rest-api-design`
first, then this for the Python specifics.

---

### implementation > rest-api-design  *(replaces `backend-rest-api`)*

**Trigger.** REST API design, OpenAPI, HTTP semantics.

**Steps.**
1. Resource modeling. Nouns, not verbs. Sub-resources only when 1:many.
2. OpenAPI 3.1. Use `$ref`, examples, error envelope.
3. HTTP semantics: methods, status codes, idempotency keys for unsafe writes.
4. Pagination: cursor-based by default. Link headers (RFC 5988).
5. Filtering: query params, comma-separated lists. No nested query DSL.
6. Optimistic concurrency: `If-Match: <etag>` on updates.
7. Caching: `Cache-Control` + `ETag` + `Vary`. Per-resource.
8. Rate limits: standard headers (`RateLimit-*`), 429 + Retry-After.
9. Versioning: URL path version for breaking changes. Headers only for
   additive.
10. Errors: RFC 7807 problem details. Type URIs.
11. Webhooks: signed payloads, replay window, exponential backoff on
    consumer side.

**Output.** OpenAPI 3.1 doc + design rationale.

---

### implementation > async-messaging  *(replaces `backend-event-driven`)*

**Trigger.** Message brokers, event schemas, sagas, outbox, DLQ.

**Steps.**
1. Pick broker: Kafka (throughput, ordering, replay), RabbitMQ (tasks,
   priority), NATS (lightweight, pub/sub), BullMQ (Node jobs).
2. Define event schema: versioned (Avro/Protobuf/JSON Schema). Registry.
3. Producers: outbox pattern for transactional emission. Never dual-write.
4. Consumers: idempotency by `(event_id, consumer_group)`.
5. Sagas: orchestrator for cross-service consistency. Compensating actions.
6. DLQs: per queue. Inspection UI. Replay tooling.
7. Schema evolution: backward-compat enforced in CI.
8. Observability: end-to-end tracing with event_id as trace context.

**Output.** Event catalog + AsyncAPI contract + runbook for replay/DLQ.

---

### implementation > react-app  *(replaces `frontend-react`)*

**Trigger.** React app, components, hooks, state.

**Steps.**
1. Server-first: Server Components / RSC where possible. Client only when
   needed.
2. Routing: file-based, type-safe routes (TanStack Router / Next.js).
3. State: server state via TanStack Query / SWR. Client state minimal
   (Zustand / Jotai). URL is the source of truth for shareable state.
4. Forms: typed schemas (Zod), progressive enhancement.
5. Data fetching: parallel + suspense + error boundaries.
6. Components: composition over config. Props spread, no `forwardRef`
   unless needed.
7. Testing: Vitest + Testing Library for units, Playwright for E2E.
8. Perf: code-split routes, image opt (next/image), font opt.

**Output.** App + tests + a11y report.

---

### implementation > typescript-app  *(replaces `frontend-typescript`)*

**Trigger.** TypeScript app setup, types, project config.

**Steps.**
1. `strict: true` + `noUncheckedIndexedAccess`. No `any`. Discouraged `as`.
2. One source of truth per concept. Branded types for IDs.
3. Smart defaults: result types, error unions, neverthrow or fp-ts for
   heavy error modeling.
4. Project config: `tsconfig.json` shared, layer overrides, paths.
5. Build: `tsc --noEmit` in CI. Bundle via Vite/Next/etc.
6. Lint/format: ESLint flat config + Prettier + type-aware rules.
7. Tests: `expect-type` for type-level guarantees.

**Output.** TS app with passing `tsc --noEmit` and ESLint.

---

### implementation > accessibility  *(replaces `frontend-accessibility`)*

**Trigger.** A11y, WCAG, ARIA, screen reader, keyboard nav.

**Steps.**
1. Choose WCAG level target. 2.1 AA is the floor.
2. Semantic HTML first. ARIA only when HTML isn't enough.
3. Keyboard: every interactive element reachable + visible focus ring.
4. Color contrast: 4.5:1 (text), 3:1 (large text, UI components).
5. Forms: labels, errors tied to inputs via `aria-describedby`.
6. Modals: focus trap, Esc to close, restore focus to invoker.
7. Live regions: `aria-live` for async changes.
8. Test: axe-core in CI + manual screen reader pass (NVDA/VoiceOver).

**Output.** A11y report with axe-core results + manual test log.

---

### implementation > performance  *(replaces `frontend-performance`)*

**Trigger.** Web perf, Core Web Vitals, bundle, runtime perf.

**Steps.**
1. Set Core Web Vitals target: LCP < 2.5s, INP < 200ms, CLS < 0.1.
2. Measure with RUM (real users), not just Lighthouse.
3. Bundle: route-level code split. No barrel imports from large libs.
4. Images: modern formats (AVIF/WebP), responsive `srcset`, lazy below
   fold.
5. Fonts: subset, preload, `font-display: swap`.
6. Runtime: avoid layout thrash; virtualize long lists; memoize when
   measured.
7. Edge: serve cached HTML at edge. ISR / On-demand revalidation.
8. CI: Lighthouse CI budget.

**Output.** Perf report + before/after metrics.

---

### implementation > agent-system  *(replaces `llm-agents`)*

**Trigger.** LLM agent, tool use, multi-agent orchestration.

**Steps.**
1. Pick framework: LangGraph (stateful), CrewAI (role-based), AutoGen
   (conversation), or hand-rolled.
2. State design: typed state graph. Each node's contract explicit.
3. Tool binding: each tool with explicit schema, timeout, idempotency key.
4. Conditional edges: deterministic when possible; LLM-judge only when
   justified.
5. Checkpointing: serialize state per step. Resume from any node.
6. Subgraphs: encapsulate sub-tasks; pass typed context only.
7. Streaming: stream intermediate tokens to UI as soon as the node yields.
8. Human-in-the-loop: where the cost of error is irreversible — escalate.
9. Evals: 50-case regression set per agent. Block merges on regression.
10. Observability: trace every node with token + latency + outcome.

**Output.** Agent + eval suite + observability dashboard.

---

### implementation > prompts-and-evals  *(replaces `llm-prompt-engineering`)*

**Trigger.** Prompt design, evals, structured output, prompt lifecycle.

**Steps.**
1. Define the eval rubric — if you can't measure it, you can't improve it.
2. Write 50-200 seed cases. Hand-crafted + edge cases.
3. Prompt: task + context + constraints + output format. Few-shot only when
   it measurably helps.
4. Structured output: JSON schema enforced at API level, not in prose.
5. Iterate: change one thing, run eval, diff.
6. Guardrails: input filters (jailbreak/PII), output filters (schema,
   toxicity).
7. Lifecycle: version prompts in git, eval on every change in CI.
8. Cost/latency: log tokens, set budgets.

**Output.** Prompt + JSON schema + eval set + CI gate.

---

### implementation > rag-pipeline  *(replaces `llm-rag`)*

**Trigger.** Retrieval-augmented generation, vector DB, semantic search.

**Steps.**
1. Choose retrieval mode: lexical (BM25), vector, hybrid.
2. Chunking: 200-500 tokens, semantic boundaries, overlap 10-20%.
3. Embedding model: pick by domain (code/legal/medical have tuned options).
4. Vector store: pgvector (small), Qdrant/Weaviate (medium), Pinecone
   (managed).
5. Hybrid: RRF (reciprocal rank fusion) to combine lexical + vector.
6. Reranker: cross-encoder rerank top 50 → top 5. Huge quality lift.
7. Citations: every answer must cite which chunks. Hallucination detector.
8. Eval: end-to-end accuracy on held-out Q&A. Track retrieval recall + answer
   faithfulness separately.
9. Freshness: incremental reindex, soft-delete via tombstone.

**Output.** Pipeline + eval set + freshness runbook.

---

### implementation > ai-feature  *(replaces `ai-engineer`)*

**Trigger.** AI feature end-to-end: model + UX + eval + cost + ops.

**Steps.**
1. Pick the right model for the job (cost ↔ quality ↔ latency).
2. UX: streaming, partial results, graceful degradation on failure.
3. Eval: define offline + online. Build the harness before the feature.
4. Guardrails: input/output validation, schema enforcement, PII redaction.
5. Cost/latency: per-request, with budgets + alerts.
6. Observability: log prompt + response + feedback signal.
7. Feedback loop: thumbs up/down, correction → eval set.

**Output.** Shipped AI feature + eval suite + ops dashboards.

---

### data > database-engineering  *(replaces `database-engineer`)*

**Trigger.** Database choice, schema design, migrations.

**Steps.**
1. Right store per access pattern. Postgres-first.
2. Schema: normalize to 3NF, denormalize for hot read paths.
3. Migrations: forward + backward. Reversible. Tested in staging.
4. Indexes: justified by EXPLAIN ANALYZE. Partial indexes where appropriate.
5. Constraints at the DB level: FK, CHECK, NOT NULL — defense in depth.
6. Connection pooling: pgbouncer / PgBouncer / app-side pool.
7. Backup strategy: PITR + off-region. Restore tested quarterly.

**Output.** Schema + migrations + backup/restore runbook.

---

### data > postgres-tuning  *(replaces `database-postgresql`)*

**Trigger.** Postgres perf, EXPLAIN, locking, replication, vacuum.

**Steps.**
1. Read EXPLAIN ANALYZE output. Identify seq scan, nested loop, hash join
   explosions.
2. Index strategy: B-tree (equality/range), GIN (jsonb/array), BRIN (time-
   series).
3. Vacuum strategy: autovacuum tuned per table. Hot updates → fillfactor.
4. Locks: detect blocking via `pg_locks`. Avoid long transactions.
5. Replication: streaming + logical (for selective subscribers).
6. Connection limits: max_connections low, pooling up.
7. Diagnostics extension pack: pg_stat_statements, auto_explain, pg_locks.

**Output.** Tuning report + before/after metrics.

---

### data > redis-and-cache  *(replaces `database-redis`)*

**Trigger.** Redis / cache, queues, pub/sub, TTL strategy, stampede.

**Steps.**
1. Pick usage pattern: cache / queue / pub-sub / counter / leaderboard.
   Each has different durability knobs.
2. Cache: explicit TTL + jitter. Stale-while-revalidate for hot keys.
3. Stampede protection: request coalescing, single-flight, locks.
4. Pub/sub: at-most-once delivery. Use streams (`XADD`) if durability
   needed.
5. Queues: Streams + consumer groups. Pending list (`XPENDING`) for retries.
6. Eviction: `allkeys-lru` only when memory-bound; otherwise explicit TTL.
7. Persistence: AOF every-second + RDB. Always both for prod.
8. Monitor: hit rate, evictions, fragmentation, replication lag.

**Output.** Redis config + cache stampede test + ops dashboard.

---

### quality > qa-loop  *(replaces `qa-engineers`)*

**Trigger.** QA cycle, manual exploratory testing, defect reporting.

**Steps.**
1. Build a one-page test plan from the spec — must-haves + edge cases.
2. Run an exploratory session per platform. Take notes in a shared doc.
3. Bug template: title, steps, expected, actual, env, screenshot/video,
   severity, frequency.
4. Triage: severity × frequency matrix. P0 = blocker, P1 = major, etc.
5. Close the loop: re-test after fix. Don't trust "fixed in main."
6. Pre-release smoke: top 10 critical paths. ≤ 30 min total.

**Output.** Test plan + bug list + pre-release smoke results.

---

### quality > test-automation  *(replaces `test-automation-engineer`)*

**Trigger.** Test framework setup, unit/integration/E2E, CI integration.

**Steps.**
1. Test pyramid: many unit, fewer integration, few E2E.
2. Unit: deterministic, fast, no I/O. Mock at the boundary.
3. Integration: real DB/cache via testcontainers. Per-test transactions.
4. E2E: Playwright. Cover the top-5 critical paths; don't chase
   coverage %.
5. Contract tests: consumer-driven (Pact) for service boundaries.
6. Flake policy: any test that flakes 3x in a week gets quarantined or
   deleted.
7. CI: parallel, sharded, cached. PR feedback < 10 min ideal.
8. Coverage: meaningful, not maximal. Branch coverage on critical paths.

**Output.** Test framework + CI workflow + coverage dashboard.

---

### quality > code-review  *(replaces `engineering-code-review`)*

**Trigger.** PR review, diff check, "is this safe to merge?"

**Steps.**
1. Read the PR description first. Goal, scope, risk.
2. Diff size: > 400 LOC? Strong signal of scope creep. Push back.
3. Look for: missing tests on new behavior, breaking API changes,
   untyped `any`, swallowed errors, hardcoded secrets, perf cliffs.
4. Architecture fit: matches `arch-module-<slug>` patterns if exists.
5. Tone: praise the good, name the must-fix, distinguish nice-to-haves.
6. Approve with comments, request changes (must-fix only), or reject.

**Output.** PR comments + decision.

---

### quality > audit-and-assessment  *(replaces `engineering-audit`)*

**Trigger.** Audit, health check, "is this project in shape?"

**Steps.**
1. Scope the audit: code, infra, security, process — pick one or all.
2. Use a rubric per surface. Each line: yes/no/partial + evidence.
3. Score. Buckets: healthy / needs-attention / at-risk.
4. Top 5 issues ranked by reversibility × impact.
5. Each top issue gets a 1-sentence "owner + first step" recommendation.

**Output.** `audit-<slug>.md` with rubric, scores, top-5, owners.

---

### operations > containers  *(replaces `devops-docker`)*

**Trigger.** Dockerfile, image hygiene, multi-arch builds.

**Steps.**
1. Multi-stage build. Final stage only carries runtime + deps.
2. Distroless or `alpine` for size; full base only when justified.
3. Non-root user in final stage. Read-only fs where possible.
4. Pin by digest, not tag, for prod reproducibility.
5. BuildKit cache mounts for `apt`, `pip`, `npm`, `go mod`.
6. Image scanning in CI: `trivy` or `grype`. Block on high CVE.
7. Labels: OCI standard (org.opencontainers.image.*).

**Output.** Dockerfile + scan report.

---

### operations > kubernetes  *(replaces `devops-kubernetes`)*

**Trigger.** K8s manifests, Helm, GitOps, RBAC, networking.

**Steps.**
1. Manifests: Kustomize or Helm — pick one, don't mix.
2. Workload shapes: Deployment, StatefulSet, Job, CronJob — one per
   concern.
3. Networking: Ingress + Service. NetworkPolicies deny-by-default +
   explicit allow.
4. RBAC: least privilege. ServiceAccount per workload.
5. Pod security: `securityContext: runAsNonRoot`, readOnlyRootFilesystem,
   drop ALL caps.
6. Resource limits: requests + limits. VPA for suggestions, HPA for
   scaling.
7. GitOps: ArgoCD or Flux. Drift detection. Auto-sync on staging, manual
   on prod.
8. Observability: Prometheus + OpenTelemetry out of the box.

**Output.** Manifests + GitOps setup + security report.

---

### operations > infra-as-code  *(replaces `devops-terraform`)*

**Trigger.** Terraform modules, state, IaC patterns.

**Steps.**
1. State backend: S3 + DynamoDB lock, or Terraform Cloud. Never local.
2. Module structure: small, composable, versioned.
3. Provider versions pinned. Terraform version pinned via `.terraform-
   version`.
4. Plan in CI. Apply gated on manual approval for prod.
5. Variable validation blocks at the module edge.
6. Drift detection: scheduled `plan` to spot divergence.
7. Secrets: never in tfvars. Use AWS Secrets Manager / Vault refs.

**Output.** Modules + state + CI workflow.

---

### operations > observability  *(replaces `devops-observability`)*

**Trigger.** Logs, metrics, traces as one system. SLOs.

**Steps.**
1. **Three pillars are one system.** Trace context flows through logs.
2. Structured logs: JSON. Stable field schema. Sampled by trace.
3. Metrics: RED (rate, errors, duration) for services, USE (utilization,
   saturation, errors) for resources.
4. Traces: OpenTelemetry. Tail sampling, not head sampling.
5. SLOs: per user-facing journey. Error budget on a dashboard, not a doc.
6. Alerting: on burn rate, not on raw threshold. Pages go to humans.
7. Dashboards: per service + per journey + per team.

**Output.** Pipeline + SLOs + dashboards + on-call playbook.

---

### operations > sre-practice  *(replaces `sre`, `devops-sre`)*

**Trigger.** SRE setup, on-call, runbooks, incident response.

**Steps.**
1. SLIs → SLOs → error budgets. Don't skip SLIs.
2. On-call rotation: primary + secondary. Handoff documented.
3. Runbook per alert: trigger, what to check, mitigation, escalation.
4. Incident lifecycle: detect → mitigate → resolve → post-mortem.
5. Post-mortem: blameless, time-stamped, action items with owners.
6. Capacity planning: per service, with growth + step changes.
7. Chaos drills: at least quarterly. Game days scheduled.

**Output.** SLOs + runbooks + post-mortem template.

---

### security > cryptography  *(replaces `security-encryption`)*

**Trigger.** Cryptography choices, TLS, key management, hashing.

**Steps.**
1. TLS everywhere. Disable TLS 1.0/1.1. HSTS preload.
2. Symmetric: AES-GCM (or ChaCha20-Poly1305). Key rotation policy.
3. Asymmetric: Ed25519 / X25519 for new code; RSA only for legacy interop.
4. Hashing: SHA-256 for integrity; Argon2id or scrypt for passwords.
   Never MD5/SHA1.
5. Key management: cloud KMS / HSM. Keys never leave the boundary.
6. At-rest: envelope encryption. Per-data-class keys.
7. In-transit: mTLS for service-to-service.
8. Randomness: `crypto.randomBytes` / `os.urandom` / cloud RNG. Never
   `Math.random`.

**Output.** Crypto design doc + key management policy.

---

### security > auth-and-tokens  *(replaces `security-jwt-oauth`)*

**Trigger.** JWT, OAuth2 / OIDC, sessions, federated identity.

**Steps.**
1. Pick the right auth: cookie sessions for first-party; OIDC for
   federated/API.
2. OIDC: Authorization Code + PKCE for SPAs. Client Credentials for
   service-to-service.
3. JWT: short-lived access (5-15 min). Refresh rotated on use.
   Audience-bound. Don't put PII in the payload.
4. Cookies: `Secure`, `HttpOnly`, `SameSite=Lax|Strict`. CSRF token for
   state-changing requests.
5. Sessions: server-side store. Sliding expiration on activity.
6. Scopes vs claims: scopes = "what", claims = "who". Use scopes for authz.
7. Federation: SAML / OIDC where the customer demands it. Don't roll your
   own.

**Output.** Auth design + token lifecycle + CSRF strategy.

---

### process > sprint-cycle  *(replaces `autonomous-sprint-orchestator`)*

**Trigger.** Continuous sprint cycle, standup, retro, demo.

**Steps.**
1. Backlog triage: incoming → prioritized → sized.
2. Sprint planning: 1 week or 2, pick. Capacity checked. Goal stated.
3. Daily standup: blockers + intentions, not status. 15 min cap.
4. Demo at end of sprint: working software to stakeholders.
5. Retrospective: what worked, what didn't, what we'll try. Action items.
6. Velocity tracked: 3-sprint moving average. Watch for instability.

**Output.** Sprint board + retro notes + velocity chart.

---

### process > phase-1-discovery  *(replaces `Phase-1-Orchestrator`)*

**Trigger.** Kick off: idea → problem → spec.

**Steps.**
1. Restate the problem in one sentence.
2. Map stakeholders and primary user.
3. List 3-5 alternatives. Pick one with reasons.
4. Define MVP scope. Must-haves + won't-haves.
5. Identify open questions and how to answer them.
6. Draft the spec. Sign off.

**Output.** Signed-off spec.

---

### process > phase-5-build-gate  *(replaces `Phase-5-Orchestrator`)*

**Trigger.** Mid-build checkpoint before go-live.

**Steps.**
1. Spec coverage: every must-have implemented and tested.
2. Code review: all PRs closed or explicitly deferred.
3. Test results: green unit + integration + E2E. Coverage meaningful.
4. Security: threat-model controls in place; pen-test results reviewed.
5. Perf: meets the SLO targets under load.
6. Observability: dashboards up; alerts wired; on-call scheduled.
7. Runbook: ops playbook exists and reviewed by who'll carry it.
8. Decision: ship / hold / scope-cut.

**Output.** Build-gate decision record.

---

### process > phase-9-deploy  *(replaces `phase-9-orchestrator`)*

**Trigger.** Post-launch: deploy, monitor, evolve.

**Steps.**
1. Deploy: progressive rollout (canary → % → 100%). Rollback ready.
2. Monitor: SLO dashboards live. Error budget burn alerts.
3. Customer feedback loop: support tickets → backlog → prioritization.
4. Operate: incident response, capacity planning, on-call rotation.
5. Document: release notes, runbook updates, retrospective.
6. Next loop: feed lessons back into `discovery > scope-and-spec`.

**Output.** Rollout dashboard + retrospective.

---

### process > documentation  *(replaces `documentation`)*

**Trigger.** Generate/update docs, keep them in sync with code.

**Steps.**
1. Three layers: tutorial (learn), how-to (task), reference (lookup).
   Don't conflate.
2. Source of truth: code. Docs generated from code where possible
   (OpenAPI, JSDoc, doc-comments).
3. Living docs: in the same repo as the code. CI fails on broken links.
4. Style: short sentences, second-person "you", active voice. Examples
   minimal.
5. Architecture decision records (ADRs): one file per decision. Immutable.
6. Changelog: keep-a-changelog format. Link to PRs/issues.
7. Onboarding: "zero to hello-world in 15 min" gate. Track time.

**Output.** Doc set in repo + onboarding metric.

---

### process > engineering-management  *(replaces `engineering-manager`)*

**Trigger.** 1:1s, growth, hiring, performance.

**Steps.**
1. 1:1s weekly, 30 min, owned by the report. Notes shared.
2. Growth: explicit growth plan per person, reviewed quarterly.
3. Hiring: rubric per role. Calibration across managers monthly.
4. Performance: continuous feedback. Surprises are a manager failure.
5. Team health: psychological safety survey quarterly. Act on results.
6. Project unblocking: balance people work and project work. Default to
   people.

**Output.** 1:1 cadence + hiring rubric + growth plans.

---

### process > program-management  *(replaces `technical-program-manager`)*

**Trigger.** Cross-team programs, dependencies, status.

**Steps.**
1. Identify the cross-team dependency graph. 2-5 teams max per program.
2. Define milestones (≤ 6 across the program life).
3. Weekly sync: blockers + dependencies + decisions needed. Decisions get
   owners.
4. RAID log: risks, assumptions, issues, decisions. Updated weekly.
5. Status report: 1 page. RAG. Top 3 risks. Next milestone.
6. Escalation path: pre-defined. Don't escalate surprises, escalate
   decisions.

**Output.** Program plan + RAID log + status report template.

---

### process > tech-leadership  *(replaces `cto`)*

**Trigger.** Strategy, vision, build-vs-buy, cross-team standards.

**Steps.**
1. Vision: 1-page. 3-year horizon. Honest about trade-offs.
2. Strategy: 5-7 bets. Each with thesis, success metric, owner.
3. Build vs buy: list criteria (cost, time-to-value, lock-in, IP). Default
   to buy unless IP or cost is decisive.
4. Standards: 5-10 cross-team norms (e.g. RFC process, ADR policy,
   observability baseline). Enforced via templates, not memo.
5. Debt register: top-10 engineering debts, each with owner + horizon.
6. Hiring plan: aligned with bets. Manager budget split.

**Output.** Vision doc + bets + standards + debt register.

---

## When nothing fits

If you've gone through intake + the routing table and still can't pick:

1. State what you heard and which category you considered.
2. Pick the **closest** category by deliverable shape (spec / plan / code /
   test / runbook).
3. Proceed with a brief sanity check: "I think you want X because Y. If I'm
   wrong, say so and I'll reroute."
4. Don't keep drilling questions. After 2 intake questions, **act**.
5. Log the misroute via the operational self-improvement section below if
   the user confirms you picked wrong.

## Operational self-improvement

Before completing a workflow, if you discovered a durable workflow fix that
would save 5+ minutes next time, append to `~/.atlas/workflows/learnings.md`:

```bash
mkdir -p "$_ATLAS_HOME/workflows" 2>/dev/null || true
cat >> "$_ATLAS_HOME/workflows/learnings.md" <<'EOF'
- <YYYY-MM-DD> | <workflow> | <one-sentence insight> | <why durable>
EOF
```

Do not log obvious facts or one-time transient errors.

## Plan mode safety

In plan mode, atlas stays in **router mode** — intake + routing table reads
are allowed; workflow execution is not. If the user invoked atlas inside
plan mode to *plan* something, do the routing and outline the workflow
steps without executing code or mutating files outside `~/.atlas/`.

Allowed in plan mode (because they inform the plan):
- reads under `~/.atlas/`
- reads of project files
- writes to the plan file
- AskUserQuestion for intake

Not allowed in plan mode: file mutations under the project, bash that runs
the workflow, deploys.

## Telemetry (light, opt-in)

```bash
_ATLAS_END=$(date +%s)
_ATLAS_DUR=$(( _ATLAS_END - _ATLAS_START ))
mkdir -p "$_ATLAS_HOME/analytics" 2>/dev/null || true
if [ "$_ATLAS_TEL" != "off" ]; then
cat >> "$_ATLAS_HOME/analytics/usage.jsonl" <<EOF
{"skill":"atlas","workflow":"<category>:<workflow>","branch":"$_ATLAS_BRANCH","spawned":"$_ATLAS_SPAWNED","duration_s":"$_ATLAS_DUR","ts":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
fi
rm -f "$_ATLAS_HOME/sessions/$$" 2>/dev/null || true
```

Telemetry content is minimal: which workflow, branch, spawn kind, duration.
No code, no file paths, no prompts. Local-only by default. To disable once:

```bash
echo "off" > "$_ATLAS_HOME/telemetry.mode"
```

To opt out of the proactive intake hints:

```bash
echo "false" > "$_ATLAS_HOME/proactive.mode"
```

To get verbose workflow detail:

```bash
echo "verbose" > "$_ATLAS_HOME/explain.level"
```

## Plan Status Footer

Skills that produce plans (e.g. `discovery > scope-and-spec`,
`architecture > module-design`) include the EXIT PLAN MODE GATE blocking
checklist at the end. Other categories are operational and don't operate
in plan mode.

## Model-Specific Behavioral Patch

**Todo-list discipline.** When walking through a multi-step workflow, mark
each task complete individually. Do not batch-complete at the end.

**Think before heavy actions.** Briefly state your approach for refactors,
migrations, or non-trivial features before executing.

**Voice.** Direct, concrete, builder-to-builder. Name the file, function,
command, and user-visible impact. No em dashes. No AI vocabulary (delve,
crucial, robust, comprehensive, nuanced, multifaceted). Short paragraphs.
End with what to do.

**Completion Status Protocol.** When finishing a workflow:
- **DONE** — completed with evidence.
- **DONE_WITH_CONCERNS** — completed, list concerns.
- **BLOCKED** — cannot proceed; state blocker + what was tried.
- **NEEDS_CONTEXT** — missing info; state exactly what's needed.

## Companion files (next to this SKILL.md)

For deep workflows, the SKILL.md is the **router + summary**. If a workflow
needs a long-form reference (full SOP, template, examples), create:

```
/workspace/.skills/atlas/workflows/
  <category>-<workflow>.md      # 1 per workflow that needs long-form
  learnings.md                 # operational self-improvement log
```

Default rule: keep SKILL.md under 2000 lines. Anything past that, split out
a companion file and link it from the workflow section.

## Spawned-session awareness

If `SPAWNED_SESSION` is set (env) or you detect parent-session agent
metadata, you are running inside a multi-agent orchestrator. In that mode:

- Skip intake. Infer from the parent's intent in the prompt.
- Auto-choose the recommended option in any remaining AskUserQuestion.
- Don't run upgrade, telemetry opt-in, or proactive prompts.
- Focus on completing the workflow and reporting back via prose.
- End with a structured report: workflow chosen, deliverables, decisions,
  anything uncertain.
