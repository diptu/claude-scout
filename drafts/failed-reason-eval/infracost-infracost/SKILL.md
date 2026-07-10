---
name: cloud-cost-estimation
description: Estimates and reviews the cost impact of infrastructure-as-code changes (Terraform, CloudFormation, Pulumi, etc.) before they're applied, so cost regressions are caught during code review instead of after the cloud bill arrives.
---

# Cloud Cost Estimation

This skill helps catch expensive infrastructure changes before they're deployed, by reasoning about the cost impact of infrastructure-as-code (IaC) diffs the same way a FinOps engineer would review a pull request.

## When to apply this skill

Apply this skill when:
- The user is adding, modifying, or reviewing Terraform, CloudFormation, Pulumi, CDK, or other IaC files.
- The user asks "how much will this cost," "will this change increase our bill," or similar.
- A pull request or diff touches resource definitions for compute (EC2, GCE, Azure VMs), storage (S3, EBS, GCS, disks), databases (RDS, DynamoDB, Cloud SQL), networking (NAT gateways, load balancers, data transfer), or managed services (Kubernetes clusters, serverless functions, managed caches/queues).
- The user is setting up CI/CD and wants cost checks as part of the pipeline (a "cost gate" alongside lint/test gates).
- The user wants a cost comparison between two IaC configurations (e.g. before/after a scaling change, or choosing between instance types).

## What "shift FinOps left" means here

The core idea: cost review should happen at the same time as code review, not after the fact in a monthly bill audit. Treat cost impact as a property of the diff, the same way you'd treat a security or correctness issue — call it out inline, with the specific resource and line responsible, rather than as a vague afterthought.

## Step-by-step guidance

1. **Identify what changed.** Read the IaC diff (or full file if no diff is available) and list every resource that is newly created, resized, or whose replication/count changed. Ignore resources that are untouched or only have metadata/tag changes.

2. **Classify each changed resource by cost driver.** For each one, identify:
   - Base unit cost (e.g. per-hour instance price, per-GB storage price, per-request pricing).
   - Scaling dimensions that multiply the base cost (instance count, replica count, autoscaling max, storage size, provisioned IOPS/throughput).
   - Any usage-based components that are hard to pin down exactly (data transfer, request volume, API calls) — call these out as "usage-dependent, direction only" rather than inventing a precise number.

3. **Estimate directionally, and numerically when possible.** If the user has given (or the repo contains) real pricing data, produce an actual monthly delta. Otherwise, still give a clear directional estimate ("this roughly triples compute spend for this service" or "this adds a new NAT gateway, ~$32/month base plus per-GB data processing charges") rather than refusing to estimate. Always state assumptions (region, on-demand vs. reserved pricing, hours/month) explicitly next to the number.

4. **Flag the highest-leverage changes first.** Sort findings so the biggest cost movers are listed first — a change from `db.t3.micro` to `db.r5.24xlarge` matters more than a tag update, even if the tag update has more diff lines.

5. **Watch for common cost traps**, and call them out even if not directly asked:
   - Resources with no auto-scaling floor/ceiling (unbounded scale-up).
   - Storage or snapshots with no lifecycle/expiration policy.
   - Load balancers, NAT gateways, or managed databases left provisioned in non-production environments.
   - Multi-AZ or cross-region replication added without discussion of whether it's needed.
   - Instance/disk types upgraded "to be safe" without a stated performance requirement.

6. **Present findings as a short table or list**, one row per resource: resource name, what changed, estimated cost impact (or direction), and confidence (exact / estimated / usage-dependent). Keep prose commentary below the table to the 2-3 points that most affect the decision.

7. **When asked to set up a CI cost gate**, describe it as a step that runs on IaC pull requests: diff the proposed state against the currently applied state, estimate the delta, and fail (or comment) if the increase exceeds a threshold the user defines. Keep the guidance conceptual — don't assume a specific tool is installed unless the user has confirmed one is available in the project.

8. **Be honest about estimate uncertainty.** Cloud pricing varies by region, commitment discounts, and negotiated enterprise rates. State estimates as ranges or directional calls when exact pricing isn't known, rather than presenting a fabricated precise dollar figure as fact.
