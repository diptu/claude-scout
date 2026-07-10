---
name: docker-best-practices
description: Guides Claude through Docker and container best practices—writing efficient Dockerfiles, structuring multi-container apps, debugging containers, and applying production-grade DevOps patterns—use when a user is building, optimizing, securing, or troubleshooting Docker images, containers, or Compose setups.
---

# Docker Best Practices

This skill helps Claude apply real-world Docker and container engineering practices when a user is writing Dockerfiles, composing multi-container applications, debugging container behavior, or preparing containers for production deployment.

## When to apply this skill

Use this skill whenever the user:
- Asks for help writing or reviewing a `Dockerfile` or `docker-compose.yml`
- Wants to reduce image size, build time, or attack surface
- Is debugging a container that won't start, crashes, or behaves differently than expected
- Needs guidance on container networking, volumes, or environment configuration
- Is setting up a container-based CI/CD or local dev workflow
- Asks general "how do I containerize X" or "is this Dockerfile good practice" questions

## Core guidance

### 1. Writing Dockerfiles

- Prefer official, minimal base images (e.g. `-alpine` or `-slim` variants) unless the user has a specific reason to need a fuller OS.
- Pin base image versions explicitly (avoid bare `latest`) so builds are reproducible.
- Order instructions from least to most frequently changing so Docker's build cache is maximally reused — dependency installation before source code copy.
- Combine related `RUN` commands with `&&` and clean up package manager caches in the same layer to avoid bloating image size with intermediate artifacts.
- Use multi-stage builds to keep build-time dependencies (compilers, dev headers) out of the final runtime image.
- Set a non-root `USER` for the running process unless the workload genuinely requires root.
- Use `.dockerignore` to exclude `.git`, local env files, `node_modules`, and other build-irrelevant content from the build context.
- Prefer `COPY` over `ADD` unless remote-fetch or auto-extraction behavior is explicitly needed.
- Declare `EXPOSE` for documentation purposes and set a clear `ENTRYPOINT`/`CMD` pairing — `ENTRYPOINT` for the fixed executable, `CMD` for default arguments the user can override.
- Use `HEALTHCHECK` for services where orchestration needs to know liveness/readiness.

### 2. Multi-container applications (Compose)

- Use `docker-compose.yml` (or `docker compose` v2 syntax) to define related services, and give each service a clear single responsibility rather than bundling multiple processes into one container.
- Use named volumes for persistent data (databases, uploads) rather than relying on the container's writable layer.
- Use a dedicated network per application stack instead of relying on the default bridge network, so service discovery via service name works cleanly.
- Pass configuration via environment variables or `.env` files, not hardcoded into images, so the same image works across dev/staging/prod.
- Use `depends_on` with health checks (not just startup order) when one service must wait for another to be ready.

### 3. Debugging containers

When a container fails to start or behaves unexpectedly, walk through this sequence:
1. Check `docker logs <container>` (or `docker compose logs <service>`) first for crash output.
2. Check `docker inspect` for the exit code and any OOM-kill or restart-loop signals.
3. If the container exits immediately, verify the `CMD`/`ENTRYPOINT` isn't backgrounding itself or exiting because PID 1 finished (containers stop when PID 1 exits).
4. Use `docker exec -it <container> sh` (or `bash` if available) to get a shell into a running container and inspect filesystem state, environment variables, and network reachability from inside.
5. For build-time failures, re-run the build with `--progress=plain` to get full, unbuffered output from each layer.
6. For networking issues, confirm which network the container is attached to and whether the target service is reachable by its Compose service name (not `localhost`) from within the container.

### 4. Image size and security

- Suggest `docker image ls` / `docker history <image>` to identify which layers are contributing the most size, and target those specifically (usually package manager caches or unnecessary dev tooling).
- Recommend scanning images for known vulnerabilities before deploying to production.
- Avoid embedding secrets (API keys, credentials) in image layers, even if later deleted in a subsequent `RUN` — earlier layers still retain them. Use build secrets or runtime environment injection instead.
- Recommend read-only root filesystems (`--read-only`) and dropped capabilities (`--cap-drop=ALL`, adding back only what's needed) for security-sensitive production deployments.

### 5. General workflow advice

- When a user is new to Docker, explain the distinction between an image (a built artifact) and a container (a running instance of that image) before diving into commands.
- When reviewing an existing Dockerfile or Compose file, point out the highest-impact issue first (e.g. "you're running as root" or "you're not using multi-stage builds, so your production image ships a compiler") rather than listing every stylistic nit with equal weight.
- Favor explaining *why* a practice matters (build cache efficiency, layer size, security surface, reproducibility) over just stating the rule, so the user can generalize it to cases this skill doesn't explicitly cover.
