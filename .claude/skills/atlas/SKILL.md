---
name: atlas
version: 2.0.0
preamble-tier: 1
description: Single-skill router. Single-pick by default; auto-fans-out to multi-role bundles (sprint, audit, build-gate, deploy, incident, system-decomp) when the command is inherently cross-functional.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
triggers:
  - atlas
  - which workflow
  - route this
  - pick the right skill
aliases:
  - ai-engineer
  - backend-event-driven
  - backend-fastapi
  - backend-rest-api
  - cloud-architect
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
  - ui-ux-engineers
  - ux-researcher
---

## How routing works

```
command → multi-role signal? ─yes→ role bundle → fan-out + synthesis
                    │
                   no
                    ↓
              intake question → single workflow
```

Default = single-pick. Fan-out only when the signal matches.

## What changed in 2.0

- Multi-role fan-out routing with named role bundles + explicit synthesis rules.
- Signal detector runs before intake; `atlas:single <cat>:<wf>` forces single-pick.
- `Write`/`Edit` in allowed-tools so workflows can produce artifacts natively.
- Routing table lists handoffs inline.
- POSIX paths only (`XDG_STATE_HOME` fallback). Needs POSIX shell (Linux/macOS/WSL).
- Aliases cleaned 47 → 41.

## Preamble

```bash
_ATLAS_HOME="${ATLAS_HOME:-${XDG_STATE_HOME:-$HOME/.local/state}/atlas}"
mkdir -p "$_ATLAS_HOME/sessions" "$_ATLAS_HOME/analytics" "$_ATLAS_HOME/workflows" 2>/dev/null || true
touch "$_ATLAS_HOME/sessions/$$" 2>/dev/null || true
find "$_ATLAS_HOME/sessions" -mmin +120 -type f -exec rm {} + 2>/dev/null || true
_ATLAS_TEL=$(cat "$_ATLAS_HOME/telemetry.mode" 2>/dev/null || echo "off")
_ATLAS_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_ATLAS_START=$(date +%s)
echo "ATLAS_HOME: $_ATLAS_HOME"
echo "TELEMETRY: $_ATLAS_TEL"
echo "BRANCH: $_ATLAS_BRANCH"
```

## Multi-role signal detector

Run BEFORE intake. If matched, skip intake and dispatch the bundle.

```bash
_ATLAS_PROMPT_LC=$(echo "$1" | tr '[:upper:]' '[:lower:]')
case "$_ATLAS_PROMPT_LC" in
  *sprint*|*planning*|*kickoff*)             _ATLAS_MULTIROLE="process:sprint-cycle" ;;
  *audit*|*assess*|*health-check*)           _ATLAS_MULTIROLE="quality:audit-and-assessment" ;;
  *build-gate*|*ready-to-ship*)              _ATLAS_MULTIROLE="process:phase-5-build-gate" ;;
  *go-live*|*launch*|*ship*|*deploy*|*release*) _ATLAS_MULTIROLE="process:phase-9-deploy" ;;
  *incident*|*outage*|*postmortem*)          _ATLAS_MULTIROLE="process:incident-response" ;;
  *design*this*service*|*design*this*system*|*new*microservice*) _ATLAS_MULTIROLE="architecture:system-decomposition" ;;
esac
```

Override: `atlas:single <cat>:<wf>` forces single-pick.

## Role bundle registry

Each bundle: `owner` writes the canonical artifact; contributors write sidecars. Synthesis rules apply when roles disagree.

### `process:sprint-cycle`
| Role | Slice | Path |
|---|---|---|
| PM (owner) | Goal, capacity, in/out scope | `sprint-<slug>.md` |
| BA | Refined stories + acceptance | `sprint-<slug>.stories.md` |
| EM | Team health, cross-team deps, risks | `sprint-<slug>.risks.md` |
| TechLead | Feasibility, debt, spikes | `sprint-<slug>.feasibility.md` |

Synthesis: TechLead feasibility = hard gate; EM P0 risk = hard gate; BA edge cases → "definition of done"; PM owns scope call.

### `quality:audit-and-assessment`
| Role | Slice | Path |
|---|---|---|
| TechLead (owner) | Code health, arch fit, coverage | `audit-<slug>.md` |
| Security | Threat model, secrets, CVE | `audit-<slug>.security.md` |
| EM | Process, PR hygiene, on-call | `audit-<slug>.process.md` |
| SRE | Observability, SLOs, runbooks | `audit-<slug>.ops.md` |

Synthesis: Security P0 = blocker; SRE veto on "ship" if runbook missing; TechLead owns RAG + top-5.

### `process:phase-5-build-gate`
| Role | Slice | Path |
|---|---|---|
| EM (owner) | Ship/hold/scope-cut decision | `gate-<slug>.md` |
| PM | Spec coverage vs must-haves | `gate-<slug>.coverage.md` |
| Security | Threat-model controls, pen-test | `gate-<slug>.security.md` |
| SRE | SLO met, observability, on-call | `gate-<slug>.ops.md` |

Synthesis: Security + SRE both must say go; PM coverage gap = hold unless deferred; EM owns decision + rollback plan.

### `process:phase-9-deploy`
| Role | Slice | Path |
|---|---|---|
| SRE (owner) | Rollout, dashboards, rollback | `deploy-<slug>.md` |
| PM | Comms, success metric | `deploy-<slug>.comms.md` |
| Security | Prod sign-off, secrets, access | `deploy-<slug>.security.md` |
| EM | Retro seed, lessons | `deploy-<slug>.retro.md` |

Synthesis: SRE owns rollout + rollback; Security gates 100%; PM owns customer comms.

### `process:incident-response`
| Role | Slice | Path |
|---|---|---|
| SRE (owner) | Timeline, root cause, mitigation | `incident-<slug>.md` |
| EM | Action items + owners | `incident-<slug>.actions.md` |
| PM | Customer impact, comms | `incident-<slug>.impact.md` |
| Security (opt) | Threat intel if security-classified | `incident-<slug>.security.md` |

Synthesis: SRE drives; EM/PM contribute during; blameless by default; action items must have owner + date.

### `architecture:system-decomposition`
| Role | Slice | Path |
|---|---|---|
| Architect (owner) | Bounded contexts, contracts, diagram | `arch-system-<slug>.md` |
| DBA | Data ownership, consistency, migrations | `arch-system-<slug>.data.md` |
| Security | Trust boundaries, authn/authz | `arch-system-<slug>.security.md` |
| SRE | SLOs, deploy topology | `arch-system-<slug>.ops.md` |
| Platform | K8s/IaC, multi-region, cost | `arch-system-<slug>.platform.md` |

Synthesis: Architect owns structure; Security veto on trust boundaries; SRE veto on missing SLO; Platform cost blocks only if >30% over budget.

## Dispatch + synthesis contract

1. Spawn workers in parallel — each gets role, slice, sidecar path.
2. Workers write ONLY to their sidecar. No cross-talk.
3. Timeout: 5 min per role. Missing → annotate `MISSING: <role>` and proceed.
4. Owner reads sidecars in order: blockers → feasibility → scope → detail.
5. If a blocker says no, that's the primary outcome.

## Intake (single-pick path only)

Skip if signal detector matched. Otherwise AskUserQuestion once:

> What stage is this work at?

- A) Discovery — what to build and why
- B) Architecture — system structure
- C) Implementation — code
- D) Data — storage, movement, modeling
- E) Quality — QA, tests, review
- F) Operations — production runtime
- G) Security — auth, crypto, design
- H) Process — team/lifecycle

Mix → earliest stage. Ambiguous after 1 question → ask deliverable shape (spec/plan/code/test/runbook). After 2 → act.

## Routing table (single-pick)

| Signal | Workflow | Handoff |
|---|---|---|
| **Discovery** | | |
| New idea, MVP shape | `discovery:scope-and-spec` | → `architecture:module-design` |
| User research, JTBD | `discovery:research-users` | → `discovery:scope-and-spec` |
| Open research | `discovery:deep-research` | → `discovery:scope-and-spec` |
| Positioning, audience | `discovery:positioning-and-audience` | → `implementation:ai-feature` |
| GTM motion | `discovery:gtm-engineering` | → bundle `process:sprint-cycle` |
| **Architecture** | | |
| Service decomposition | `architecture:system-decomposition` | → bundle if multi-role |
| Module design | `architecture:module-design` | → `implementation:python-api` |
| Cloud landing zone | `architecture:cloud-landing-zone` | → `operations:infra-as-code` |
| ML system | `architecture:ml-system-design` | → `implementation:agent-system` |
| Data architecture | `architecture:data-architecture` | → `data:database-engineering` |
| Threat model | `architecture:secure-by-design` | → `security:auth-and-tokens` |
| Design system | `architecture:design-system` | → `implementation:react-app` |
| UI/UX | `architecture:ui-ux` | → `implementation:accessibility` |
| **Implementation** | | |
| Python API / FastAPI | `implementation:python-api` | after `rest-api-design` first |
| REST design | `implementation:rest-api-design` | → `python-api` or `react-app` |
| Async messaging | `implementation:async-messaging` | → `quality:test-automation` |
| React app | `implementation:react-app` | → `accessibility` + `performance` |
| TS setup | `implementation:typescript-app` | → `react-app` |
| A11y | `implementation:accessibility` | → `quality:test-automation` |
| Web perf | `implementation:performance` | → `operations:observability` |
| LLM agent | `implementation:agent-system` | → `prompts-and-evals` |
| Prompts/evals | `implementation:prompts-and-evals` | → `agent-system` |
| RAG | `implementation:rag-pipeline` | → `prompts-and-evals` |
| AI feature E2E | `implementation:ai-feature` | → bundle `process:phase-5-build-gate` |
| **Data** | | |
| DB schema/migrations | `data:database-engineering` | → `postgres-tuning` if PG |
| Postgres tuning | `data:postgres-tuning` | → `operations:observability` |
| Redis / cache | `data:redis-and-cache` | → `operations:observability` |
| **Quality** | | |
| QA cycle | `quality:qa-loop` | → `test-automation` |
| Test framework | `quality:test-automation` | → bundle `process:phase-5-build-gate` |
| PR review | `quality:code-review` | → bundle if audit-scope |
| Audit | `quality:audit-and-assessment` | → bundle if multi-role |
| **Operations** | | |
| Containers | `operations:containers` | → `kubernetes` |
| K8s | `operations:kubernetes` | → `observability` |
| Terraform | `operations:infra-as-code` | → `security:cryptography` |
| Observability | `operations:observability` | → `sre-practice` |
| SRE / SLOs | `operations:sre-practice` | → bundle `process:phase-5-build-gate` |
| **Security** | | |
| Crypto / KMS | `security:cryptography` | → `auth-and-tokens` |
| JWT / OAuth | `security:auth-and-tokens` | → `architecture:secure-by-design` |
| **Process** | | |
| Sprint | `process:sprint-cycle` | → bundle if multi-role |
| Docs | `process:documentation` | — |
| EM work | `process:engineering-management` | — |
| Program mgmt | `process:program-management` | — |
| Tech strategy | `process:tech-leadership` | → `phase-1-discovery` |

## Workflows (compact)

Full SOPs live in companion files at `~/.local/state/atlas/workflows/<cat>-<wf>.md`. Each entry below is a one-line summary.

**Discovery.** `scope-and-spec` → `spec-<slug>.md`. `research-users` → n=5-8, themes→insights→product changes. `deep-research` → 2+ sources per claim, narrative. `positioning-and-audience` → beachhead + voice + CTAs. `gtm-engineering` → buyer roles + moment of value + SLAs.

**Architecture.** `system-decomposition` → bounded contexts + contracts + diagram. `module-design` → DDD + state model + errors + fitness fns. `cloud-landing-zone` → regions + accounts + IAM + cost + DR. `ml-system-design` → topology + eval harness + drift detectors. `data-architecture` → store map + projection + lineage + governance. `secure-by-design` → trust boundaries + STRIDE + controls. `design-system` → tokens (primitives→semantic→component) + a11y. `ui-ux` → journey (≤9 steps) + 5-state matrix.

**Implementation.** `python-api` → async + Pydantic v2 + DI + layered + observability. `rest-api-design` → OpenAPI 3.1 + cursor pagination + RFC 7807 + idempotency. `async-messaging` → outbox + idempotent consumers + sagas + DLQ + AsyncAPI. `react-app` → RSC + TanStack Query + Zod + Vitest/Playwright. `typescript-app` → `strict: true` + branded IDs + result types + `tsc --noEmit` CI. `accessibility` → WCAG 2.1 AA + keyboard + axe-core. `performance` → LCP<2.5s, INP<200ms, CLS<0.1 + RUM. `agent-system` → typed state + tool schemas + checkpointing + 50-case evals. `prompts-and-evals` → rubric + 50-200 cases + JSON schema + CI gate. `rag-pipeline` → hybrid retrieval + reranker + citations + freshness. `ai-feature` → model pick + streaming + eval harness + guardrails + $/req budget.

**Data.** `database-engineering` → Postgres-first + reversible migrations + EXPLAIN-justified indexes + PITR. `postgres-tuning` → B-tree/GIN/BRIN + autovacuum per-table + connection pooling. `redis-and-cache` → pattern per use + TTL+jitter + stampede protection + AOF+RDB.

**Quality.** `qa-loop` → test plan + exploratory + severity×frequency. `test-automation` → pyramid + testcontainers + Pact + flake policy + <10min PR. `code-review` → diff<400 LOC + must-fix only. `audit-and-assessment` → rubric + RAG + top-5 with owners.

**Operations.** `containers` → multi-stage + non-root + distroless + digest-pinned + `trivy`. `kubernetes` → Kustomize/Helm + NetworkPolicies deny-default + GitOps. `infra-as-code` → S3+DynamoDB state + pinned versions + plan-in-CI. `observability` → OTel + RED/USE + SLOs + burn-rate alerts. `sre-practice` → SLI→SLO→budget + runbooks + blameless PMs.

**Security.** `cryptography` → TLS 1.2+ + AES-GCM + Ed25519 + Argon2id + cloud KMS + cloud RNG. `auth-and-tokens` → OIDC PKCE + short JWT + refresh rotation + CSRF.

**Process.** `sprint-cycle` → 1-2 wk + capacity + standup + retro + 3-sprint velocity. `documentation` → tutorial/how-to/reference + ADRs + CI link check. `engineering-management` → weekly 1:1s + growth plans + hiring rubric. `program-management` → 2-5 teams + ≤6 milestones + RAID. `tech-leadership` → vision + 5-7 bets + build-vs-buy + standards + debt register.

## When nothing fits

1. State what you heard + categories considered.
2. Pick by deliverable shape: spec / plan / code / test / runbook.
3. State the pick: "I think you want X because Y. If I'm wrong, say so."
4. After 2 intake questions total, **act**.
5. Ambiguous bundle signal (e.g. "release") → prefer conservative: build-gate before deploy.

**Failure modes.**
- Intake timeout/empty → default to closest category from last prompt word.
- User says "none of these" → 1-para freeform plan + ask to confirm.
- Unknown workflow name → propose closest match, ask once.
- Bundle role fails → owner proceeds with `MISSING: <role>`. No retry beyond once.

## Operational self-improvement

```bash
mkdir -p "$_ATLAS_HOME/workflows" 2>/dev/null || true
cat >> "$_ATLAS_HOME/workflows/learnings.md" <<'EOF'
- <YYYY-MM-DD> | <workflow> | <one-sentence insight> | <why durable>
EOF
```

## Plan mode safety

**Allowed.** Reads under `~/.local/state/atlas/` and project; writes to plan file; AskUserQuestion for intake; bundle sidecar writes (so plan shows would-be fan-out).

**Not allowed.** Project file mutations outside plan; bash that runs the workflow (deploys, scans, migrations); production effects.

## Telemetry (opt-in)

```bash
_ATLAS_END=$(date +%s)
_ATLAS_DUR=$(( _ATLAS_END - _ATLAS_START ))
if [ "$_ATLAS_TEL" != "off" ]; then
  _ATLAS_MODE=$([ -n "$_ATLAS_MULTIROLE" ] && echo "fanout" || echo "single")
  echo "{\"skill\":\"atlas\",\"mode\":\"$_ATLAS_MODE\",\"workflow\":\"${_ATLAS_MULTIROLE:-<cat>:<wf>}\",\"branch\":\"$_ATLAS_BRANCH\",\"duration_s\":\"$_ATLAS_DUR\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$_ATLAS_HOME/analytics/usage.jsonl"
fi
```

Disable: `echo off > "$_ATLAS_HOME/telemetry.mode"`.

## Companion files

Long-form SOPs at:
```
~/.local/state/atlas/workflows/
  <cat>-<wf>.md
  <bundle-name>.md
  learnings.md
```

Keep SKILL.md under 2000 lines. Each bundle gets its own file when it grows past a screen.

## Spawned-session awareness

If `SPAWNED_SESSION` set or parent-session metadata present:
- Skip intake; infer intent.
- Multi-role bundles → dispatch in parallel via host spawn primitive.
- No telemetry opt-in prompts.
- End with: mode (single/fanout), workflow, roles dispatched, deliverables, decisions, uncertainties.