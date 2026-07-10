---
name: ml-training-research-loop
description: Guides Claude through running an autonomous research loop of small-scale model training experiments (hypothesis, minimal experiment, run, measure, decide) under tight single-GPU compute budgets; use when a user wants to iterate on training a small language or vision model and needs a disciplined experiment cycle rather than one-off scripts.
---

# ML Training Research Loop

This skill helps Claude act as a disciplined research assistant for iterative
model-training experiments on constrained hardware (typically a single GPU).
It applies whenever a user wants to explore or improve a small-scale training
setup — architecture tweaks, hyperparameter changes, data mix changes, or
optimizer changes — and wants each change tested empirically rather than
guessed at.

## When to apply this skill

Use this skill when the user:
- Is training or fine-tuning a small model (nanoGPT/nanochat-scale or similar)
  and wants to try a series of changes to improve a metric (loss, eval
  accuracy, throughput, sample quality).
- Asks Claude to "try a few things and see what works" on a training script.
- Has a single GPU or otherwise limited compute and needs experiments kept
  cheap and comparable.
- Wants a log of what was tried, what happened, and why a decision was made,
  rather than silently rewriting the training script each time.

Do not apply this skill for one-off inference calls, unrelated data analysis,
or large-scale distributed training where a different governance process
already exists — this skill is specifically for the tight
hypothesize-run-measure-decide loop on small, fast-iterating jobs.

## Core loop

Run the following cycle repeatedly, one change at a time:

1. **State the hypothesis.** Before touching code, write one sentence: what
   change is being tried, and what metric it should move (e.g. "lowering
   warmup steps from 200 to 50 should reduce val loss at step 2000"). Never
   start a run without a stated hypothesis — otherwise results can't be
   attributed to a cause.

2. **Design the smallest experiment that tests it.** Prefer the shortest run,
   smallest model, or smallest data slice that can still produce a signal.
   Do not scale up until a cheap version has shown promise. If the user's
   existing training script already supports config flags or overrides, reuse
   them instead of duplicating the script.

3. **Fix everything except the one variable under test.** Keep seed, data
   split, and all other hyperparameters identical to the last baseline run
   unless the hypothesis is specifically about one of those. Changing more
   than one thing per run makes results uninterpretable.

4. **Run it and capture the numbers.** Record the exact command or config
   used, the final (or best) value of the target metric, wall-clock time, and
   any anomalies (loss spikes, NaNs, OOM). If the run fails, capture the
   failure mode itself as a result — a crash is data too.

5. **Compare against the baseline, explicitly.** State whether the metric
   improved, regressed, or was noise-level unchanged, and by how much. Avoid
   declaring victory on a single run if the metric is noisy — rerun with a
   different seed when the delta is small relative to expected run-to-run
   variance.

6. **Decide and record the decision.** Either: keep the change and make it
   the new baseline, discard it and revert, or flag it as inconclusive and
   needing a bigger run. Write this decision down next to the hypothesis and
   result so the sequence of experiments forms a readable log, not just a
   pile of checkpoints.

7. **Pick the next hypothesis based on the result**, not a pre-made list —
   a promising direction should be pushed further immediately (e.g. try a
   slightly larger learning rate next if a smaller one just helped); a dead
   end should be dropped rather than revisited.

## Operating under a compute budget

- Treat GPU time as the scarce resource. Before launching a run, estimate its
  cost (steps × time/step) and check it against how many more experiments are
  wanted in the session.
- Prefer short proxy runs (fewer steps, smaller model) to screen ideas cheaply,
  then confirm only the winners with a longer run.
- Kill runs early that are clearly diverging (NaN loss, loss plateaued far
  above baseline) rather than letting them finish — that time is better spent
  on the next hypothesis.
- Never launch multiple simultaneous training runs on a single GPU; queue them
  sequentially to avoid resource contention that would corrupt timing/throughput
  comparisons.

## Reporting back to the user

At the end of a session (or when asked for status), summarize as a table or
short list: hypothesis tried → result → decision, in chronological order, plus
the current best configuration and its metric value. This lets the user see
the shape of the search, not just the final answer, and lets a future session
resume from the last confirmed baseline instead of re-deriving it.
