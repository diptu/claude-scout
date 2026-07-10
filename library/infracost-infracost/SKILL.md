---
name: cloud-cost-estimation
description: Estimates the cloud cost impact of infrastructure-as-code changes (Terraform, CloudFormation, Pulumi, etc.) before they're merged or applied, and should be used whenever a user modifies infrastructure definitions, asks "how much will this cost," or requests a cost review of a PR/diff.
---

# Cloud Cost Estimation

This skill helps surface the dollar impact of infrastructure changes before
they reach production — the same problem tools like Infracost solve by
diffing infrastructure-as-code and pricing out the delta. Claude should apply
this skill whenever infrastructure code changes (Terraform, CloudFormation,
Pulumi, Bicep, ARM templates, Kubernetes manifests with resource requests,
etc.) or whenever a user directly asks about cloud spend, budget impact, or
"what will this cost."

## When to apply this skill

- A diff or PR touches `.tf`, `.tfvars`, CloudFormation YAML/JSON, Pulumi
  source, Bicep, or Kubernetes resource manifests.
- The user asks "how much would this cost," "will this increase our bill,"
  or "review this change for cost impact."
- The user is deciding between instance types, storage tiers, database
  engines, or scaling configurations and wants a cost-informed
  recommendation.
- Before recommending an architecture change (e.g. adding a NAT gateway,
  switching to provisioned IOPS, adding read replicas), proactively note the
  cost implication even if not asked.

## Step-by-step guidance

1. **Identify what resources are being added, changed, or removed.** Read
   the diff (or the full IaC file if no diff is available) and list every
   resource block affected — provider, resource type, and the specific
   attributes that drive cost (instance size, storage size/type, IOPS,
   replica count, region, egress-heavy configurations, reserved vs.
   on-demand pricing, etc.).

2. **Classify each change as cost-neutral, cost-increasing, or
   cost-decreasing.** Renaming a resource or changing a tag is neutral;
   bumping an instance class, enabling multi-AZ, adding autoscaling max
   capacity, or provisioning more storage is increasing; downsizing,
   deleting unused resources, or switching to cheaper storage tiers is
   decreasing.

3. **Estimate the magnitude, not just the direction.** For each
   cost-affecting change, reason through the pricing model:
   - Compute: hourly rate × instance count × hours/month (730 hrs is a
     reasonable default for "always on").
   - Storage: per-GB-month rate × size, plus IOPS/throughput surcharges
     where relevant.
   - Data transfer: flag any change that increases cross-AZ, cross-region,
     or public egress traffic — this is the cost category engineers most
     often miss.
   - Managed services (databases, caches, queues): note that these often
     have a step-function pricing model — moving one tier up can be a much
     bigger jump than the raw resource size suggests.
   - If exact current pricing isn't known with confidence, give an order-
     of-magnitude estimate and say so explicitly rather than presenting a
     fabricated precise figure.

4. **Compare against the existing baseline.** State the estimated
   before/after monthly cost delta for each changed resource, and a total
   delta for the change set, not just per-resource numbers in isolation.

5. **Flag the highest-leverage cost risks first.** Order findings by dollar
   impact, not by file order. Call out anything that scales with usage
   (autoscaling ceilings, storage that grows unbounded, per-request pricing)
   since those carry open-ended risk beyond the estimate.

6. **Suggest cheaper equivalents where they don't compromise the stated
   requirements.** E.g. spot/preemptible instances for fault-tolerant
   workloads, gp3 over io2 where IOPS needs are modest, lifecycle policies
   for storage that's being added, right-sizing instance classes to actual
   observed load if that data is available.

7. **Present the result as a concise cost-impact summary**: a short table
   or list of resource → change → estimated monthly delta, followed by the
   total delta and any risk flags from step 5-6. Avoid re-explaining what
   the infrastructure change does — focus the summary on the financial
   impact, since the diff itself already shows the "what."

8. **Be explicit about confidence and assumptions.** Cloud pricing varies
   by region, commitment level (on-demand/reserved/savings-plan), and
   negotiated discounts Claude cannot see. State the assumptions used
   (region, pricing tier, on-demand rates) so the reader can adjust the
   estimate if their actual contract differs.
