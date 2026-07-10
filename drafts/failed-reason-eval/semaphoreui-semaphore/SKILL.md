---
name: ansible-devops-orchestration
description: Guides Claude through designing, reviewing, and troubleshooting Ansible/Terraform/OpenTofu/Terragrunt automation workflows, including how to structure projects for use with a centralized DevOps UI/API layer like Semaphore — use when a user is writing playbooks, provisioning infrastructure, setting up CI/CD for infrastructure-as-code, or wants to expose automation tasks through a web UI and API instead of raw CLI invocations.

# Ansible & Infrastructure-as-Code DevOps Orchestration

## What this skill helps with

This skill helps structure and review Infrastructure-as-Code (IaC) automation —
Ansible playbooks, Terraform/OpenTofu configurations, Terragrunt wrappers, and
PowerShell-based DevOps scripts — so that they are clean to run both from the
command line and from a centralized orchestration layer (a "DevOps control
plane" UI/API that stores inventories, variables, environments, and run
history, and exposes RBAC-controlled execution to a team).

Use it when the user is:
- Writing or reviewing Ansible playbooks, roles, or inventories.
- Writing or reviewing Terraform/OpenTofu modules or Terragrunt configs.
- Setting up a project so it can be triggered by a task runner/scheduler
  (cron-like schedules, webhooks, API calls) rather than only by hand.
- Migrating ad-hoc shell scripts into structured, auditable IaC.
- Designing role-based access, secret storage, or environment separation for
  a team running shared infrastructure automation.
- Debugging why a playbook or Terraform plan behaves differently when run
  from an orchestration tool versus a local terminal (usually environment,
  working directory, or credential-passing differences).

## When to apply

Apply this skill whenever the conversation involves `.yml`/`.yaml` Ansible
playbooks, `inventory` files, `.tf`/`.tfvars`/`terragrunt.hcl` files, or
PowerShell DevOps scripts, or when the user mentions running such tooling
from a shared team-facing system rather than a single developer's machine.

## Step-by-step guidance

1. **Identify the automation type first.** Ask (or infer from file
   extensions) whether the task is configuration management (Ansible),
   provisioning (Terraform/OpenTofu), or wrapper/DRY-orchestration
   (Terragrunt) — each has different idempotency guarantees and failure
   modes, and advice should not be mixed across them without saying so.

2. **Structure for repeatable, non-interactive execution.** Whether or not
   the user is using a centralized runner, playbooks and IaC should already
   assume:
   - No interactive prompts (`--ask-become-pass`, `terraform apply` without
     `-auto-approve`, etc. should be flagged as blockers for automated runs).
   - Explicit inventory/variable sources rather than relying on local shell
     state (e.g. prefer `-i inventory/production.yml` and `extra-vars` files
     over environment variables set ad hoc in a terminal).
   - Idempotent tasks (Ansible) or plan-before-apply discipline (Terraform):
     always recommend reviewing a dry-run/plan output before an apply/run
     step, and call out any task that is not safely re-runnable.

3. **Separate secrets from code.** Recommend Ansible Vault, environment
   variables injected at run time, or a secret manager — never hardcoded
   credentials in playbooks, inventories, or `.tfvars` committed to version
   control. If the user's files contain what looks like a real secret, flag
   it immediately rather than continuing silently.

4. **Design for environment separation.** Encourage distinct
   inventories/variable files (or Terraform workspaces / Terragrunt
   directory-per-environment layouts) for dev/staging/production, so the
   same playbook or module can be promoted across environments by changing
   inputs, not code.

5. **Think in terms of "task templates" for a control-plane UI.** If the
   user wants their automation runnable by a team through a UI/API rather
   than only by CLI, help them define each playbook/module as a self
   contained, parameterized unit:
   - Clear required/optional input variables with sensible defaults.
   - A single, well-documented entry point (one playbook per task, one
     Terraform root module per stack) rather than scripts that chain
     multiple unrelated operations.
   - Output/logging that is meaningful when read after the fact (e.g. in a
     run history log), not just when watched live in a terminal.
   - RBAC-friendly boundaries: which environments/inventories a given
     task/role should be allowed to target, so access can be scoped per
     team or per environment later.

6. **Review for CI/CD readiness.** Check that:
   - Linting is in place (`ansible-lint`, `terraform validate`/`tflint`).
   - Exit codes are meaningful (a failed task should fail the run, not be
     swallowed).
   - Long-running or destructive operations (deletes, force-replace
     resources, `--force` flags) require an explicit confirmation step or
     are gated behind a plan/dry-run review, never auto-applied silently.

7. **When troubleshooting orchestrator vs. local discrepancies**, check in
   this order: working directory assumptions (relative paths breaking),
   environment variables/credentials not being passed through, differing
   tool versions between the runner and the local machine, and inventory or
   variable file resolution order.

## Guidance for output

When producing playbooks, Terraform modules, or related config, prefer
minimal, idiomatic examples over exhaustive boilerplate: use standard module
directory layout for Terraform (`main.tf`, `variables.tf`, `outputs.tf`),
standard role layout for Ansible (`tasks/`, `defaults/`, `handlers/`), and
avoid inventing custom directory conventions unless the user's project
already has one. Always call out any step that would require secrets,
destructive changes, or production access before suggesting it be run.
