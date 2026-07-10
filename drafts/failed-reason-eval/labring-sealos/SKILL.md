---
name: cloud-native-app-lifecycle
description: Guides Claude through planning and managing the full lifecycle of a cloud-native application — from local/cloud IDE development through containerized deployment, managed database provisioning, and microservice orchestration — for use whenever a user is standing up, deploying, or operating an app on a Kubernetes-style cloud platform.
---

# Cloud-Native App Lifecycle

This skill helps plan and reason through the full lifecycle of a cloud-native
application: development environment setup, containerization, deployment,
managed database provisioning, microservice architecture, and scaling —
mirroring the workflow of an all-in-one cloud operating system (develop in an
IDE, ship to production, manage everything as one connected system).

## When to apply this skill

Apply this skill when the user is:

- Setting up or configuring a development environment for an app meant to
  run in the cloud (containers, dev/prod parity, cloud IDEs).
- Deploying an application to a Kubernetes-based or container-orchestrated
  platform.
- Provisioning or configuring managed databases (MySQL, PostgreSQL, Redis,
  MongoDB) for an application.
- Designing or refactoring an application into a microservice architecture.
- Debugging issues that span the boundary between "my code" and "the
  platform it runs on" (networking, service discovery, resource limits,
  storage, secrets).
- Asking how to go from "it works on my machine" to "it's running in
  production" for a cloud-native app.

## Core mental model

Treat the application lifecycle as one continuous pipeline, not disconnected
steps handled by different tools with no shared context:

1. **Develop** — code, dependencies, and local config should be defined in a
   way that maps directly onto how the app will run in production
   (containerize early; avoid environment drift).
2. **Package** — turn the app into a container image with an explicit,
   minimal set of dependencies and a clear entrypoint.
3. **Provision data layer** — stand up managed databases separately from
   application containers, with connection details injected via environment
   variables or secrets, never hardcoded.
4. **Deploy** — describe the desired running state (replicas, resource
   limits, health checks, networking) declaratively rather than as a
   sequence of imperative commands.
5. **Operate** — plan for scaling, observability, and updates as ongoing
   concerns, not afterthoughts bolted on post-launch.

## Step-by-step guidance

When helping a user with a cloud-native app task, work through these steps:

1. **Clarify the target platform and constraints.** Ask (or infer from the
   repo) whether this is Kubernetes, a managed PaaS, or a custom setup.
   Identify what's already defined (Dockerfiles, Helm charts, docker-compose
   files, k8s manifests) before proposing anything new.

2. **Separate stateless and stateful components.** Application code
   (stateless, horizontally scalable) should be treated differently from
   databases and persistent storage (stateful, need backup/restore
   strategy, careful scaling). Never suggest baking database data into an
   application container image.

3. **Design the microservice boundaries deliberately.** If the user is
   splitting a monolith or adding a new service, check that each service:
   - Owns its own data (no shared database tables across services).
   - Has a clear, narrow API contract with other services.
   - Can be deployed and scaled independently.
   Avoid over-splitting — a handful of well-bounded services beats a dozen
   tightly-coupled micro-services that all deploy together anyway.

4. **Make configuration environment-aware, not environment-specific.** Use
   environment variables, config maps, or secrets for anything that differs
   between dev/staging/prod (database URLs, API keys, feature flags).
   Flag any hardcoded host names, credentials, or ports as a portability
   risk.

5. **Provision managed databases correctly.**
   - Confirm the engine (MySQL, PostgreSQL, Redis, MongoDB) matches the
     application's actual query/consistency needs, not just what's
     familiar.
   - Recommend connection pooling appropriate to the app's concurrency
     model.
   - Ensure credentials are passed via secrets/env injection, and that
     backup/retention expectations are explicit before going to production.

6. **Write deployment specs declaratively.** When producing or editing
   deployment manifests (Kubernetes YAML, compose files, platform configs),
   specify:
   - Resource requests/limits (CPU, memory) sized to the workload.
   - Health/readiness checks so the platform can detect and recover from
     failures automatically.
   - Replica counts and scaling policy appropriate to expected load.

7. **Plan the path to production explicitly.** Before calling a deployment
   "done," walk through: does it build reproducibly, does it start clean
   from zero state, does it recover from a pod/container restart, and is
   there a rollback path if the new version misbehaves.

8. **Keep the whole lifecycle visible.** When making a change in one part
   of the system (e.g. adding a new microservice), check its ripple effects
   on the rest — new database needs, updated service discovery, additional
   ingress/networking rules, and monitoring coverage — instead of treating
   each piece as an isolated task.

## What to avoid

- Don't propose infrastructure changes (new database engines, new
  orchestration platforms) unless the user's constraints call for it —
  match the existing platform choices already in the codebase.
- Don't collapse stateful and stateless concerns into the same deployment
  unit for convenience.
- Don't hardcode secrets or environment-specific values into application
  code or container images.
- Don't over-engineer a microservice split for an app that's better served
  by staying a well-structured monolith — recommend splitting only when
  there's a clear independent-scaling or independent-deploy need.
