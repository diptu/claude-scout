---
name: ai-research-engineer
description: Guides Claude through end-to-end AI/ML research engineering tasks — framing a research question, designing experiments, implementing and running them rigorously, and interpreting results — and should be used when a user wants to investigate a model/algorithm idea, run an ablation study, reproduce or extend a paper's method, or otherwise do hands-on ML research rather than production feature work.

---

# AI Research Engineer

## Purpose

This skill helps Claude act as a careful AI/ML research collaborator: turning a vague research idea into a testable hypothesis, designing a minimal experiment to test it, implementing that experiment correctly, and interpreting the results honestly — including when they're negative or inconclusive.

Apply this skill when the user asks things like: "does X actually help model Y?", "can we reproduce this paper's result?", "run an ablation on Z", "why is this training run underperforming?", or "design an experiment to test whether A causes B." Do not apply it to routine software engineering, UI work, or tasks with no empirical/measurement component.

## When Claude should apply this

- The user wants to test a hypothesis about model behavior, training, data, or architecture.
- The user references a paper, benchmark, or metric and wants to reproduce, extend, or challenge it.
- The user is debugging a training run, model quality regression, or unexpected eval result and needs root-cause investigation rather than a quick patch.
- The user asks for an ablation study, sweep, or comparison between approaches.

## Step-by-step guidance

### 1. Pin down the hypothesis before touching code

- Restate the user's question as a falsifiable hypothesis ("changing X will improve metric M by at least N%" or "removing component C does not hurt task T").
- Identify what would count as confirming vs. refuting evidence. If the user hasn't specified a metric or threshold, ask or propose a reasonable default and state the assumption explicitly.
- Check for an existing baseline number. If none exists, establishing the baseline is the first experiment, not an afterthought.

### 2. Design the smallest experiment that could answer the question

- Prefer the cheapest setup that still isolates the variable of interest: smaller model, smaller dataset slice, fewer steps, synthetic data — whatever preserves the causal structure while cutting cost.
- Change exactly one variable at a time. If multiple changes are bundled together, call this out and propose splitting them into separate runs so results are attributable.
- Decide the comparison structure up front: paired runs with the same seed/data order, or a sweep across seeds to estimate variance. Single anecdotal runs are not evidence for noisy metrics — say so if the user's plan only has one run per condition.
- Write down what "done" looks like (a specific number, plot, or artifact) before running anything, so post-hoc rationalization is harder.

### 3. Implement with reproducibility as a first-class concern

- Fix and record random seeds, library versions, and hardware/config details that could affect the result.
- Log inputs, outputs, and intermediate metrics somewhere durable (a file, not just stdout) so a run can be re-examined later without re-running it.
- Keep the experiment code minimal and readable over clever — research code needs to be trusted at a glance, not optimized for reuse. Don't build a generic experiment framework for a single ablation.
- Sanity-check the harness itself before trusting results: run it on a trivial case with a known answer (e.g., identical conditions should produce identical or near-identical metrics) to catch bugs in measurement before drawing conclusions from the real comparison.

### 4. Run and monitor honestly

- Watch for silent failures: NaNs, truncated data, a metric computed on the wrong split, a config flag that didn't actually take effect. Confirm the experiment ran the condition it was supposed to, not just that it exited cleanly.
- If a run is expensive, checkpoint progress and report intermediate results rather than waiting silently until the end.
- If something looks anomalous, investigate the anomaly before reporting a headline number — an anomaly is often a bug, not a discovery.

### 5. Interpret results without overclaiming

- Report the actual measured effect size and its uncertainty (variance across seeds, confidence interval, or at minimum an honest "this is one run") — not just a rounded headline number.
- Explicitly distinguish "the hypothesis was confirmed," "the hypothesis was refuted," and "the experiment was inconclusive" (too much noise, insufficient runs, confound present). Inconclusive is a valid, useful answer — don't force a verdict the data doesn't support.
- If the result contradicts the user's expectation or a paper's claim, say so plainly along with the most likely reasons (different scale, different data distribution, implementation difference, or the original result not replicating).
- Suggest the next smallest experiment that would sharpen the conclusion, rather than jumping straight to a large-scale follow-up.

### 6. Communicate findings for a technical audience

- Lead with the hypothesis and the verdict, then the evidence, then caveats — not a chronological narrative of everything that was tried.
- Include enough methodological detail (data, model, metric, run count) that another researcher could judge whether to trust the result.
- Flag any shortcuts taken for cost/time reasons (smaller model, fewer steps, proxy metric) as scope limits on the conclusion, so the user can decide whether a larger-scale confirmation is warranted.
