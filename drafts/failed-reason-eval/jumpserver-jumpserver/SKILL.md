---
name: privileged-access-review
description: Guides Claude through designing, configuring, or auditing privileged/remote access setups (SSH, RDP, Kubernetes, database, and RemoteApp access) using centralized bastion/PAM principles — use when a user needs to harden how humans or services reach production systems, review access control policies, or add session auditing to remote access infrastructure.

# Privileged Access Review

This skill helps design, configure, and audit **Privileged Access Management (PAM)** setups: the layer that sits between people and the SSH servers, RDP hosts, Kubernetes clusters, databases, or internal web apps ("RemoteApps") they need to reach. It captures the core lessons of mature bastion/PAM platforms — centralize access, record everything, grant least privilege, and never hand out raw credentials — and applies them regardless of which specific tool (open-source bastion, cloud-native session manager, or custom jump host) is in play.

## When to apply this skill

Apply this skill when the user asks Claude to:

- Design or review a bastion host / jump server architecture for SSH or RDP access.
- Set up or audit access control for Kubernetes clusters, databases, or internal admin panels used by multiple engineers or teams.
- Add session recording, command auditing, or approval workflows for privileged operations.
- Replace shared credentials (a shared root password, a shared `.pem` key passed around Slack) with per-user, revocable, auditable access.
- Investigate "who has access to what" or "who did what" after an incident involving privileged systems.
- Write onboarding/offboarding procedures for access to production infrastructure.

Do not apply this skill to ordinary application-level authentication/authorization (login forms, OAuth for end users) — it is specifically about privileged/administrative access to infrastructure and internal systems.

## Core principles to apply

1. **Centralize the choke point.** Every privileged connection (SSH, RDP, database client, `kubectl`, internal web app) should route through one auditable gateway rather than connecting directly to targets. If a design has engineers SSHing straight into production hosts with individual keys and no central log, flag that as the primary gap.

2. **Never distribute raw long-lived credentials.** Users authenticate to the gateway (SSO, MFA, short-lived cert, or per-user account); the gateway holds and injects the actual target credentials (root password, database password, kubeconfig) at connection time. The user should never need to know or copy the target's real secret.

3. **Record and log every session.** For interactive sessions (SSH/RDP terminal, RemoteApp), the gateway should capture session recordings (keystrokes, screen, or terminal output) and command history. For database access, log executed queries. This is what makes "who did what" answerable after the fact.

4. **Grant least-privilege, scoped, and time-boxed access.** Access should be assignable per-user or per-team, per-asset (specific host/cluster/database), and ideally per-account-on-that-asset (e.g. a specific Linux user or DB role), not "give this person the whole environment." Prefer access grants with expiry over permanent grants; flag standing access to production as something that should have a review/expiry cadence.

5. **Support approval workflows for higher-risk actions.** For sensitive targets or commands (e.g. connecting to a production database, running `DROP TABLE`, RDP into a domain controller), route the request through an approval step (manager or security-lead sign-off) rather than instant self-service.

6. **Make revocation immediate and centralized.** Offboarding or role change should be a single action at the gateway (disable the user's account there) rather than having to hunt down every host, database, and cluster where that person's key or password was distributed.

7. **Cover all access modalities uniformly, not just SSH.** The same centralize-record-scope-revoke model should apply whether the target is a Linux/Windows host (SSH/RDP), a Kubernetes cluster (`kubectl` exec/proxy), a database (MySQL/Postgres/etc. client), or an internal web app (RemoteApp/web proxy) — don't leave one modality as an unmonitored side door.

## Step-by-step guidance

When asked to design a new privileged access setup:

1. Enumerate every target type in scope (Linux hosts, Windows hosts, Kubernetes, databases, internal web apps) and confirm none of them will be reachable by a path that bypasses the central gateway.
2. Define the identity source (existing SSO/LDAP/local accounts) the gateway will authenticate users against, and require MFA for privileged sessions.
3. Design the credential vault: how target credentials (SSH keys, RDP passwords, DB passwords, kubeconfig tokens) are stored, rotated, and injected without ever being shown to the end user.
4. Define the access-grant model: user/group → asset/account mapping, with expiry dates for anything touching production.
5. Define what gets recorded (session replay, command logs, query logs) and where those records are stored and for how long, since audit logs are the main deliverable of a PAM setup.
6. Identify which actions need an approval step and who the approver is.
7. Write the offboarding procedure: a single disable action at the gateway plus a checklist of any credentials that existed *outside* the gateway before migration (these need manual rotation once, then should never recur).

When asked to audit an existing setup, walk through principles 1–7 above as a checklist and call out every place where a target is reachable directly (not through the gateway), where a credential is long-lived and human-known, or where sessions aren't recorded — these are the highest-value findings.

When asked to investigate an incident, start from the gateway's session recordings and access-grant history for the affected asset and time window; if no such central log exists, the audit's first recommendation should be to establish one before investigating further.
