---
name: docker-practice-guide
description: Guides Claude through Docker and container best practices — image building, Dockerfiles, Compose, networking, storage, and troubleshooting — for use when a user is writing, reviewing, or debugging Docker-related configuration or workflows.
---

# Docker Practice Guide

This skill helps Claude assist with real-world Docker and container workflows: writing Dockerfiles, structuring multi-container applications, debugging containers, and applying production-grade best practices rather than toy examples.

## When to apply this skill

Apply this skill when the user is:
- Writing or reviewing a `Dockerfile`, `docker-compose.yml`, or `.dockerignore`
- Debugging a container that won't build, start, or behave correctly
- Asking about image size, layer caching, or build performance
- Setting up networking, volumes, or persistent storage between containers
- Migrating an application (or a devops pipeline) to run in containers
- Asking about security hardening for images or running containers
- Comparing Docker concepts (image vs container, volume vs bind mount, CMD vs ENTRYPOINT, etc.)

## Step-by-step guidance

### 1. Clarify the goal before writing config
Before generating a Dockerfile or Compose file, confirm:
- What language/runtime the app uses (this determines base image choice)
- Whether this is for local development, CI, or production deployment
- Whether multiple services need to talk to each other (Compose vs single container)
- Whether there are existing constraints (base image policy, registry, orchestration platform)

### 2. Writing a Dockerfile
Follow these practices, in priority order:
- **Pin the base image tag** (e.g. `python:3.12-slim`, never bare `python` or `latest`) so builds are reproducible.
- **Order instructions for cache efficiency**: copy dependency manifests (`package.json`, `requirements.txt`, `go.mod`) and install dependencies *before* copying the rest of the source, so code changes don't invalidate the dependency-install layer.
- **Use multi-stage builds** when the build toolchain (compilers, dev headers) is not needed at runtime — copy only the compiled artifact into a slim final stage.
- **Minimize layers and image size**: combine related `RUN` commands with `&&`, clean up package manager caches in the same layer they were created (e.g. `apt-get clean && rm -rf /var/lib/apt/lists/*`), and prefer `-slim`/`-alpine` base variants when the app's dependencies support them.
- **Run as a non-root user** in the final image unless there's a specific reason not to (`USER appuser`), and create that user explicitly.
- **Use `COPY` over `ADD`** unless remote URL fetching or tar auto-extraction is actually needed.
- **Prefer `ENTRYPOINT` + `CMD`** together when the image represents a single executable with default arguments; use `CMD` alone for simple default commands.
- **Add a `.dockerignore`** covering `.git`, `node_modules`, build artifacts, and secrets/env files so they don't bloat the build context or leak into the image.
- **Never bake secrets into image layers** — use build secrets (`--mount=type=secret`), environment variables injected at runtime, or a secrets manager instead of `ARG`/`ENV` with credentials.

### 3. Writing docker-compose.yml
- Define one service per container responsibility (app, database, cache, reverse proxy) rather than combining unrelated processes into one container.
- Use named volumes for data that must persist across container recreation (databases, uploads); use bind mounts only for local development source-code syncing.
- Set explicit `depends_on` plus a health check on dependencies (e.g. database) rather than relying on startup order alone, since `depends_on` only waits for container start, not readiness.
- Scope networks explicitly when isolation matters (e.g. a public-facing proxy network separate from an internal database network).
- Pin image versions in Compose the same way as in Dockerfiles — avoid `latest`.

### 4. Debugging containers
When a container fails to build, start, or behave correctly, walk through in order:
- **Build failures**: read the exact failing layer/instruction from the build output; check for missing files (often a `.dockerignore` or build-context path issue) or dependency resolution errors.
- **Container exits immediately**: check the logs (`docker logs <container>` conceptually) for the actual error, and confirm the `CMD`/`ENTRYPOINT` process isn't a one-shot command that naturally exits (containers stop when PID 1 exits).
- **Container starts but app is unreachable**: verify port mapping direction (`host:container`), that the app binds to `0.0.0.0` and not `127.0.0.1` inside the container, and that the right network is attached.
- **Works locally, fails in container**: suspect environment differences — missing environment variables, different file paths/case-sensitivity, or a dependency that was only installed on the host.
- **Data loss between restarts**: check whether the relevant path is actually declared as a volume; anything not in a volume is ephemeral and destroyed with the container.

### 5. Security and production hardening
- Scan images for known vulnerabilities before deploying (treat this as a required step, not optional polish).
- Drop unnecessary Linux capabilities and avoid `--privileged` unless the workload genuinely requires host-level access.
- Set resource limits (CPU/memory) so a single misbehaving container can't starve the host.
- Keep base images updated on a regular cadence rather than pinning once and forgetting.

### 6. Explaining concepts
When the user asks a conceptual question (image vs container, volume vs bind mount, `CMD` vs `ENTRYPOINT`, bridge vs host networking), give a concrete example alongside the definition — a one-line command or config snippet — rather than an abstract explanation only, since Docker concepts are easiest to retain in context.
