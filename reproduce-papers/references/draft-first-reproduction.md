# Draft-First Reproduction

## Objective

Produce the smallest runnable reproduction that exercises the paper's core claim before trying to match the original setup exactly.

## Build the First Runnable Path

1. Pick one claim, benchmark, or scenario that represents the paper's core contribution.
2. Reduce scope to one end-to-end execution path.
3. Keep interfaces aligned with the paper even if some internals are still approximate.
4. Choose standard, defensible defaults when details are missing.
5. Save every approximation in `gap_tracker.md`.

## What Counts as a Runnable Draft

A runnable draft can be:

- one training and evaluation loop on a reduced dataset
- one inference or analysis pass with comparable outputs
- one benchmark run on a reduced workload
- one detector or attack pipeline run on a safe sample set
- one prototype execution that proves the claimed pipeline can operate end to end

The draft does not need full-scale data, full hardware, or exact final metrics.

## Defaulting Rules

When the paper omits details:

- Prefer defaults that are standard for the stated framework, cited baseline, or benchmark.
- Match the paper's observable interfaces and metric definitions first.
- Keep changes small and reversible.
- State the assumption, the reason it is reasonable, and the likely impact on results.

Do not silently invent hyperparameters, preprocessing, build flags, or evaluation shortcuts.

## Scope Control

Use one of these reductions when full reproduction is not yet feasible:

- a smaller dataset split
- one representative benchmark instead of the full suite
- one model size instead of several variants
- one operating environment instead of every deployment target
- one attack or defense scenario instead of the full matrix

The goal is to prove the path works, not to claim final parity too early.

## Exit Criteria

You can move from draft mode to fidelity work when:

- the pipeline runs end to end
- the required inputs and outputs are defined
- the remaining gaps are explicit
- the next fidelity improvements are clear

Record the result in `implementation_plan.md` and `experiment_log.csv`.
