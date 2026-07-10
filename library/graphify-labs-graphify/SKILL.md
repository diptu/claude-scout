---
name: codebase-knowledge-graph
description: Build a lightweight knowledge graph linking application code, database schemas, infrastructure config, and docs into one connected model, and use it to trace how a change in one artifact ripples through the rest of the system.
---

# Codebase Knowledge Graph

This skill helps Claude answer cross-cutting questions about a codebase that a single-file or single-directory search can't answer well — questions like "what breaks if I rename this column," "what calls this endpoint," or "which services depend on this config value." Instead of treating code, SQL schemas, infrastructure files, and docs as separate silos, it builds a mental (or written) graph connecting them by shared identifiers: table/column names, function/class names, API routes, environment variables, and config keys.

## When to apply this skill

Apply this when a task requires understanding relationships across artifact types, not just within one file. Signals that this skill is relevant:

- The user asks "what depends on X" or "what would break if I changed X."
- The user asks to trace a database column, config key, or environment variable through the codebase into the application layer (or vice versa).
- The user is planning a schema migration, API contract change, or config rename and wants a blast-radius assessment before making it.
- The user wants an overview of how a project's pieces (app code, database, infra, docs) fit together.
- A bug report mentions symptoms in one layer (e.g. a UI field showing wrong data) that likely originate in another (a SQL query, a migration, an infra setting).

Don't apply it for purely local tasks (fixing a bug confined to one function, writing a new isolated feature) where there's nothing to trace across artifact boundaries.

## Step-by-step approach

1. **Identify the artifact types present.** Scan the repository for the categories of files relevant to the question: application source code, SQL migrations/schema files, infrastructure-as-code (Terraform, Docker Compose, Kubernetes manifests, CI configs), and documentation (README, docs/, ADRs). Not every project has all of these — work with what exists.

2. **Extract the node set for the query at hand.** Rather than indexing the entire repo up front, start from the specific identifier the user cares about (a table name, column, function, endpoint path, env var, or config key) and treat that as the seed node.

3. **Find edges by shared identifiers, not just imports.** Search for the seed identifier's exact name and its common variant forms (snake_case, camelCase, kebab-case, pluralized) across:
   - Application code: variable names, struct/class fields, ORM model definitions, API route strings.
   - Database layer: column/table definitions in schema files and migrations, foreign key references.
   - Infrastructure: environment variable names in Dockerfiles, Compose files, Terraform variables, CI/CD pipeline YAML.
   - Docs: mentions in README/docs that describe the same concept, which may reveal intended behavior not obvious from code alone.

4. **Build a connected picture before proposing changes.** Assemble what you find into an explicit list or short diagram (in your response, not a new file unless asked) showing: seed node → what reads it → what writes it → what config or infra it depends on → what would need to change alongside it. This is the "graph" — it doesn't need a database or visualization tool, just an explicit enumeration of connected artifacts.

5. **Flag gaps and ambiguity.** If the same conceptual entity appears to have inconsistent names across layers (e.g. `user_id` in SQL but `userId` in app code and `USER_ID` in an env var), call this out explicitly rather than silently assuming they're the same or different — ask the user to confirm if it's ambiguous and the consequences of being wrong are significant.

6. **Answer the ripple-effect question directly.** Once the connected artifacts are enumerated, give a concrete answer: what breaks, what needs a coordinated change, and in what order (e.g. migration before deploy, or deploy before migration, depending on backward compatibility needs).

7. **Prefer showing the trace over hiding it.** When presenting the answer, show the chain of references that led to the conclusion (file paths and line numbers where possible) so the user can verify the reasoning rather than trusting an opaque conclusion.
