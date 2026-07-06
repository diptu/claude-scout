# ⚙️ SKILL.md — DevOps Observability Engineer

## 🧠 Skill Name
devops-observability-core-v1

---

## 🧩 Domain
devops / sre / observability / monitoring / logging / infrastructure-reliability

---

## 🎯 Phase Responsibility
**Platform & Reliability Layer (Post-Development Phase)**

This skill is responsible for ensuring:
- system health visibility
- production reliability
- incident detection & response readiness
- infrastructure observability across all services

---

## 🚀 Core Objective

To make all systems **fully observable, diagnosable, and measurable in production**, ensuring no failure is silent and no degradation goes unnoticed.

---

# 🧭 Primary Responsibilities

## 1. Metrics Engineering
Define and implement system metrics:

- latency (p50, p95, p99)
- throughput (requests/sec)
- error rates
- saturation (CPU, memory, disk, queue depth)

Ensure metrics are:
- consistent
- actionable
- low-noise

---

## 2. Logging Strategy Design
Implement structured logging:

- JSON logs
- correlation IDs
- request tracing context
- service-level log aggregation

Avoid:
- unstructured logs
- noisy debug logs in production
- missing trace context

---

## 3. Distributed Tracing
Enable end-to-end request tracing:

- request lifecycle tracking across services
- latency bottleneck detection
- dependency mapping

Tools conceptually supported:
- OpenTelemetry
- Jaeger / Zipkin patterns

---

## 4. Alerting System Design
Design intelligent alerts:

- threshold-based alerts
- anomaly detection signals
- alert fatigue prevention

Rules:
- every alert must be actionable
- every alert must map to a runbook
- avoid redundant notifications

---

## 5. Dashboard Engineering
Create observability dashboards for:

- system health overview
- service-level performance
- error hotspots
- infrastructure utilization

Dashboards must answer:
> “Is the system healthy right now?”

---

## 6. Incident Detection & Response Support
Support SRE workflows:

- detect incidents early
- classify severity levels
- support root cause analysis
- track incident timelines

---

## 7. Postmortem Data Support
Provide structured data for:

- incident analysis
- failure reproduction
- long-term reliability improvements

Ensure:
- no blame culture
- system-focused debugging

---

# 🧪 Inputs

This skill consumes:

- backend logs
- infrastructure metrics
- deployment events
- system telemetry
- error traces

---

# 📤 Outputs

Generates:

```text
metrics_spec.md
logging_spec.json
alert_rules.yaml
dashboard_layout.md
incident_reports/
runbooks/